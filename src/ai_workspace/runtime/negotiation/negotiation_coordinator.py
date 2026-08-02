from __future__ import annotations

from collections import Counter

from ai_workspace.domain.decision_goal import DecisionGoal
from ai_workspace.domain.engine_selection import EngineSelectionDecision
from ai_workspace.domain.negotiation import AgentProposal, NegotiatedPlan
from ai_workspace.domain.task import Task
from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.workflow_engine import WorkflowEngine


class NegotiationCoordinator:
    """Multi-Agent Negotiation(Milestone 84, ADR-0102): 여러 Agent가 같은
    Task 또는 공유 자원(Provider/Model/Workflow 순서)에 대해 각자
    독립적으로 결정하지 않고, 실행 전 단계에서 선호안(`AgentProposal`)을
    다수결로 조율해 하나의 최종 계획(`NegotiatedPlan`)을 만드는 순수
    오케스트레이션 클래스(`LearningRuntimeAnalyzer`(M54)와 동일한 패턴 —
    새 Core Domain Interface가 아니며, `WorkspaceCore`/`AgentManager`
    어디에도 자동으로 배선되지 않는다. 호출자가 명시적으로 생성·호출해야만
    쓰인다).

    이 클래스는 기존 실행 흐름(`EngineRuntime.run()`/`AgentManager`/
    `WorkflowEngine.plan()`)을 전혀 변경하지 않는다 — `negotiate()`는
    실행 전 계획 수립 단계에서만 호출되는 별도 진입점이며, 그 결과
    (`NegotiatedPlan`)를 실제로 실행에 반영할지는 전적으로 호출자의
    책임이다(`EngineSelectionDecision`/`EngineRecommendation`이 이미
    확립한 "Decision Only" 원칙과 동일).

    **다수결 규칙**: `engine_name`(Provider+사실상 Model 선택)과
    `preferred_workflow_order`(Workflow 순서, 제안한 Agent가 있을 때만)
    각각에 대해 최다 득표 선호안을 채택한다. 득표가 동률이면
    `AgentProposal.priority`(낮을수록 우선, `Agent.priority`(M57)와 동일
    의미)로 대표 제안을 고르는 것이 아니라 **협상 자체를 실패로 간주**한다
    (동률을 임의로 깨는 것은 "합의"가 아니기 때문). Workflow 순서는 추가로
    현재 `workflow.dependencies`를 만족하는지 검증한 뒤에만 채택한다
    (M72 `plan()`의 "현재 dependency 재검증" 원칙과 동일).

    **Fallback(all-or-nothing)**: 제안이 하나도 없거나, engine 다수결이
    동률이거나, workflow 순서 다수결이 동률이거나, 협상된 순서가 현재
    dependency를 어기면 — 부분적으로 채택하지 않고 전체를 기존 단독
    의사결정으로 즉시 전환한다: engine/model은
    `EngineRuntime.decide_engine()`, workflow 순서는(제공됐다면)
    `WorkflowEngine.plan()` 결과를 그대로 쓴다. 이 fallback은 두 인터페이스
    모두 이미 갖고 있는 기존 계약을 그대로 호출할 뿐, 새 로직을 추가하지
    않는다."""

    def __init__(
        self,
        engine_runtime: EngineRuntime,
        workflow_engine: WorkflowEngine | None = None,
    ) -> None:
        self._engine_runtime = engine_runtime
        self._workflow_engine = workflow_engine

    def negotiate(
        self,
        task: Task,
        proposals: list[AgentProposal],
        required_capabilities: frozenset[str] = frozenset(),
        *,
        goal: DecisionGoal = DecisionGoal.BALANCED,
        workflow: Workflow | None = None,
    ) -> NegotiatedPlan:
        if not proposals:
            return self._fallback(task, required_capabilities, goal, workflow, "제안이 없어")

        winner = self._resolve_engine(proposals)
        if winner is None:
            return self._fallback(
                task, required_capabilities, goal, workflow, "engine 선호안이 동률로 충돌해"
            )

        workflow_order: list[str] | None = None
        if workflow is not None:
            proposed_orders = [
                proposal.preferred_workflow_order
                for proposal in proposals
                if proposal.preferred_workflow_order is not None
            ]
            if proposed_orders:
                order_winner = self._resolve_order(proposed_orders)
                if order_winner is None:
                    return self._fallback(
                        task,
                        required_capabilities,
                        goal,
                        workflow,
                        "workflow 순서 선호안이 동률로 충돌해",
                    )
                if not self._respects_dependencies(order_winner, workflow):
                    return self._fallback(
                        task,
                        required_capabilities,
                        goal,
                        workflow,
                        "협상된 workflow 순서가 현재 dependency를 위반해",
                    )
                workflow_order = list(order_winner)
            elif self._workflow_engine is not None:
                workflow_order = self._workflow_engine.plan(workflow)

        decision = EngineSelectionDecision(
            engine_name=winner.engine_name,
            model=winner.model,
            reason=(
                f"{len(proposals)}개 Agent 제안 중 다수결로 "
                f"engine_name={winner.engine_name} 채택(대표 agent_id={winner.agent_id})"
            ),
        )
        return NegotiatedPlan(
            decision=decision,
            workflow_order=workflow_order,
            consensus_reached=True,
            reason="Agent 제안 다수결로 합의",
        )

    @staticmethod
    def _resolve_engine(proposals: list[AgentProposal]) -> AgentProposal | None:
        counts = Counter(proposal.engine_name for proposal in proposals)
        max_count = max(counts.values())
        winners = {name for name, count in counts.items() if count == max_count}
        if len(winners) != 1:
            return None
        (winner_name,) = winners
        group = [proposal for proposal in proposals if proposal.engine_name == winner_name]
        return min(group, key=lambda proposal: proposal.priority)

    @staticmethod
    def _resolve_order(orders: list[tuple[str, ...]]) -> tuple[str, ...] | None:
        counts = Counter(orders)
        max_count = max(counts.values())
        winners = {order for order, count in counts.items() if count == max_count}
        if len(winners) != 1:
            return None
        (winner_order,) = winners
        return winner_order

    @staticmethod
    def _respects_dependencies(order: tuple[str, ...], workflow: Workflow) -> bool:
        if set(order) != set(workflow.task_ids) or len(order) != len(workflow.task_ids):
            return False
        position = {task_id: index for index, task_id in enumerate(order)}
        for task_id, depends_on in workflow.dependencies.items():
            for dependency in depends_on:
                if position[dependency] >= position[task_id]:
                    return False
        return True

    def _fallback(
        self,
        task: Task,
        required_capabilities: frozenset[str],
        goal: DecisionGoal,
        workflow: Workflow | None,
        cause: str,
    ) -> NegotiatedPlan:
        decision = self._engine_runtime.decide_engine(task, required_capabilities, goal=goal)
        workflow_order = (
            self._workflow_engine.plan(workflow)
            if workflow is not None and self._workflow_engine is not None
            else None
        )
        return NegotiatedPlan(
            decision=decision,
            workflow_order=workflow_order,
            consensus_reached=False,
            reason=(
                f"{cause} 합의에 실패해 EngineRuntime.decide_engine()"
                + ("/WorkflowEngine.plan()" if workflow is not None else "")
                + "으로 fallback"
            ),
        )
