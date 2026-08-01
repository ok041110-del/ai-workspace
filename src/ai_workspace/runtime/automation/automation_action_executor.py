from __future__ import annotations

import uuid

from ai_workspace.domain.automation import Action, ActionKind, AutomationRule
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_registry import EngineRegistry
from ai_workspace.interfaces.engine_selection_policy import EngineSelectionPolicy
from ai_workspace.interfaces.workflow_repository import WorkflowRepository
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher
from ai_workspace.runtime.execution.recommendation_orchestration_service import (
    RecommendationOrchestrationService,
)
from ai_workspace.runtime.workflow.workflow_runner import WorkflowRunner


class AutomationActionNotSupportedError(Exception):
    """아직 실제로 실행할 수 없는 Action Kind에 대해 발생한다.
    RUN_WORKFLOW/RUN_RECOMMENDATION은 각각 필요한 협력자
    (`workflow_repository`+`workflow_runner`/`recommendation_
    orchestration_service`)가 주입되지 않은 경우에 발생한다(M38,
    M59)."""


class AutomationActionExecutor:
    """`AutomationRule.action`을 실제로 실행하는 유일한 통로(M21-T04,
    사용자 승인 조건 5 — `ExecutionDispatcher`를 유일한 실행
    진입점으로 유지한다). `AutomationScheduler`(M21-T03)의
    `action_executor` 콜러블로 주입된다 — Scheduler는 이 클래스의
    내부 구현을 전혀 모른다.

    RUN_TASK는 M17/M18 파이프라인을 그대로 재사용한다: 새 `Task`
    생성 → `EngineRegistry.list_candidates()`로 후보 조회 →
    `EngineSelectionPolicy.select()`로 Decision 판단 →
    `ExecutionDispatcher.dispatch()`로 실행. 이 클래스는 새로운
    실행 경로를 만들지 않는다.

    DASHBOARD_REFRESH/NOTIFICATION은 `ExecutionDispatcher`를 거칠
    Task가 없으므로 아무것도 실행하지 않는다(Dashboard는 이미
    `ExecutionDispatcher`가 발행하는 Event로 갱신되고, 실제 알림
    발송은 Out of Scope).

    **RUN_WORKFLOW(Milestone 59, ADR-0077)**: `workflow_repository`/
    `workflow_runner`를 둘 다 주입하면 `workflow_id`로 실제 `Workflow`
    를 조회해 `WorkflowRunner.run()`에 위임한다 — M21부터 이월돼 온
    "Task 단위 실행만 지원" 제약을 해소했다. 둘 중 하나라도 주어지지
    않으면(기본값 `None`) `AutomationActionNotSupportedError`를 던져
    기존 동작과 완전히 동일하다. `Workflow.task_ids`에 해당하는
    Task들은 호출 전에 이미 생성돼 있어야 한다는 `WorkflowRunner`의
    전제 조건을 그대로 물려받는다 — 이 클래스는 Task를 새로 만들지
    않는다."""

    def __init__(
        self,
        *,
        engine_registry: EngineRegistry,
        engine_selection_policy: EngineSelectionPolicy,
        execution_dispatcher: ExecutionDispatcher,
        recommendation_orchestration_service: RecommendationOrchestrationService | None = None,
        workflow_repository: WorkflowRepository | None = None,
        workflow_runner: WorkflowRunner | None = None,
    ) -> None:
        self._engine_registry = engine_registry
        self._engine_selection_policy = engine_selection_policy
        self._execution_dispatcher = execution_dispatcher
        self._recommendation_orchestration_service = recommendation_orchestration_service
        self._workflow_repository = workflow_repository
        self._workflow_runner = workflow_runner

    def __call__(self, rule: AutomationRule) -> None:
        action = rule.action
        if action.kind is ActionKind.RUN_TASK:
            self._run_task(action)
        elif action.kind is ActionKind.RUN_WORKFLOW:
            self._run_workflow(action)
        elif action.kind is ActionKind.RUN_RECOMMENDATION:
            self._run_recommendation(action)
        elif action.kind in (ActionKind.DASHBOARD_REFRESH, ActionKind.NOTIFICATION):
            return

    def _run_task(self, action: Action) -> None:
        assert action.project_id is not None
        assert action.task_title is not None
        task = Task(
            task_id=str(uuid.uuid4()), project_id=action.project_id, title=action.task_title
        )

        candidates = self._engine_registry.list_candidates(task)
        decision = self._engine_selection_policy.select(task, candidates)
        self._execution_dispatcher.dispatch(decision, task)

    def _run_workflow(self, action: Action) -> None:
        if self._workflow_repository is None or self._workflow_runner is None:
            raise AutomationActionNotSupportedError(action.kind.value)
        assert action.workflow_id is not None
        workflow = self._workflow_repository.get(action.workflow_id)
        self._workflow_runner.run(workflow)

    def _run_recommendation(self, action: Action) -> None:
        """`RecommendationOrchestrationService`(M43)가 Experience
        조회 → Recommendation 계산(M35, Adaptation은 M42) → 실행
        (M36/M37, 새 정책 없이 그대로 재사용)까지 전체 흐름을
        제어한다. `manual_trigger=True`를 고정으로 전달한다 — Rule
        자체를 사용자가 명시적으로 만들고 활성화했다는 점에서
        `ExecutionGate`가 막으려는 "실수로 자동 승인되는 경우"에
        해당하지 않는다(M38)."""
        if self._recommendation_orchestration_service is None:
            raise AutomationActionNotSupportedError(action.kind.value)
        self._recommendation_orchestration_service.publish(manual_trigger=True)
