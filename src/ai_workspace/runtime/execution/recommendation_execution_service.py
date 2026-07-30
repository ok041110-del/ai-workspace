"""Execution Layer — Recommendation Execution Service (ADR-0050, Milestone 36-T03~T04).

M35 `RecommendationIntelligenceService.generate()`가 계산한
`NextAction`을 `ExecutionGate`(승인 판정)/`ActionBuilder`(변환)를
거쳐 실제로 `ExecutionDispatcher`(M18)로 실행한다.
`AutomationActionExecutor`(M21)를 감싸지 않고, 그 내부와 동일한
3단계(`EngineRegistry.list_candidates()` → `EngineSelectionPolicy.
select()` → `ExecutionDispatcher.dispatch()`)를 직접 재사용한다 —
`AutomationActionExecutor.__call__()`은 `EngineExecutionResult`를
버리는 기존 계약이라 실행 결과를 Vault에 남길 수 없기 때문이다
(ADR-0050 결정 4)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path

from ai_workspace.domain.automation import Action
from ai_workspace.domain.execution_result import EngineExecutionResult
from ai_workspace.domain.task import Task
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceService
from ai_workspace.interfaces.engine_registry import EngineRegistry
from ai_workspace.interfaces.engine_selection_policy import EngineSelectionPolicy
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher
from ai_workspace.runtime.execution.recommendation_action_builder import ActionBuilder
from ai_workspace.runtime.execution.recommendation_execution_gate import (
    ExecutionGate,
    GateDecision,
)


@dataclass(frozen=True)
class RecommendationExecutionOutcome:
    """`RecommendationExecutionService.execute()`의 결과. Gate가
    승인하지 않으면 `action`/`result`는 `None`이다."""

    gate_decision: GateDecision
    action: Action | None
    result: EngineExecutionResult | None


class RecommendationExecutionService:
    """M35 Recommendation → M36 Execution을 연결하는 조합 계층.
    `ExecutionGate`/`ActionBuilder`(판정/변환 각각의 책임)와
    `EngineRegistry`/`EngineSelectionPolicy`/`ExecutionDispatcher`
    (M17/M18, 그대로 재사용)만 조합한다 — 새 실행 경로를 만들지
    않는다."""

    def __init__(
        self,
        recommendation_service: RecommendationIntelligenceService,
        vault_adapter: VaultAdapter,
        engine_registry: EngineRegistry,
        engine_selection_policy: EngineSelectionPolicy,
        execution_dispatcher: ExecutionDispatcher,
    ) -> None:
        self._recommendation_service = recommendation_service
        self._vault_adapter = vault_adapter
        self._engine_registry = engine_registry
        self._engine_selection_policy = engine_selection_policy
        self._execution_dispatcher = execution_dispatcher
        self._gate = ExecutionGate()
        self._builder = ActionBuilder()

    def execute(self, *, manual_trigger: bool) -> RecommendationExecutionOutcome:
        """
        입력: manual_trigger(호출자가 수동 트리거임을 명시적으로
              전달해야 함 — 기본값 없음)
        출력: `RecommendationExecutionOutcome`(Gate 판정 + 승인된
              경우 실제 실행 결과)
        예외: 없음 — Gate가 승인하지 않으면 실행 자체를 시도하지
              않고 방어적으로 반환한다.
        보장: Gate가 승인한 경우에만 `ExecutionDispatcher.dispatch()`
              를 호출한다(실제 부작용 발생). Task 상태는 자동으로
              전이하지 않는다(ADR-0050 결정 5).
        """
        report = self._recommendation_service.generate()
        decision = self._gate.check(report.next_action, manual_trigger=manual_trigger)
        if not decision.approved:
            return RecommendationExecutionOutcome(gate_decision=decision, action=None, result=None)

        assert report.next_action is not None
        action = self._builder.build(report.next_action, report.workflow_report)
        assert action.project_id is not None
        assert action.task_title is not None
        task = Task(
            task_id=str(uuid.uuid4()), project_id=action.project_id, title=action.task_title
        )
        candidates = self._engine_registry.list_candidates(task)
        selection_decision = self._engine_selection_policy.select(task, candidates)
        result = self._execution_dispatcher.dispatch(selection_decision, task)

        return RecommendationExecutionOutcome(gate_decision=decision, action=action, result=result)

    def publish(self, *, manual_trigger: bool) -> tuple[RecommendationExecutionOutcome, Path]:
        """`execute()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_recommendation_execution()`에 위임).

        보장: `15 Project Intelligence/Recommendation Execution.md`
              가 이번 결과로 완전히 덮어써진다(누적 append 아님). Task
              상태는 자동으로 전이하지 않는다(ADR-0050 결정 5).
        """
        outcome = self.execute(manual_trigger=manual_trigger)
        markdown = render_markdown(outcome)
        path = self._vault_adapter.publish_recommendation_execution(markdown)
        return outcome, path


def render_markdown(outcome: RecommendationExecutionOutcome) -> str:
    """`RecommendationExecutionOutcome`을 Vault 문서 Markdown으로
    렌더링한다. 순수 함수(입출력 문자열 변환만, I/O 없음)."""
    lines = [
        "---",
        "tags: [recommendation-execution]",
        "type: recommendation-execution",
        "---",
        "",
        "# Recommendation Execution",
        "",
        "> Milestone 36(Execution)이 M35 Recommendation의 next_task "
        "추천을 실제로 실행한 결과다(ADR-0050). source=next_task 외 "
        "4개 NextAction은 지원하지 않음(Not Supported), 자동/주기적 "
        "트리거 없음 — 수동 트리거로만 실행한다. Task 상태는 자동으로 "
        "전이하지 않는다. 매 생성 시 이 문서 전체가 덮어써진다 — "
        "편집해도 다음 생성 때 사라진다.",
        "",
        "## Gate 판정",
        "",
        f"- 승인 여부: {'승인' if outcome.gate_decision.approved else '거부'}",
        f"- 이유: {outcome.gate_decision.reason}",
        "",
    ]
    if outcome.action is not None:
        lines.extend(
            [
                "## 실행된 Action",
                "",
                f"- Project: {outcome.action.project_id}",
                f"- Task: {outcome.action.task_title}",
                "",
            ]
        )
    if outcome.result is not None:
        lines.extend(
            [
                "## 실행 결과",
                "",
                f"- 성공 여부: {'성공' if outcome.result.success else '실패'}",
                f"- Engine: {outcome.result.engine}",
                f"- 소요 시간: {outcome.result.execution_time:.2f}초",
            ]
        )
        if outcome.result.error:
            lines.append(f"- 오류: {outcome.result.error}")
        lines.append("")

    return "\n".join(lines)
