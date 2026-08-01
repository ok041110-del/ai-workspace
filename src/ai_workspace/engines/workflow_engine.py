from __future__ import annotations

from ai_workspace.domain.workflow import Workflow
from ai_workspace.domain.workflow_order_memory import WorkflowOrderStat
from ai_workspace.interfaces.engine_registry import EngineRegistry
from ai_workspace.interfaces.engine_selection_policy import EngineSelectionPolicy
from ai_workspace.interfaces.task_engine import TaskEngine, TaskNotFoundError
from ai_workspace.interfaces.workflow_engine import WorkflowEngine

_WorkflowSignature = frozenset[str]


class InMemoryWorkflowEngine(WorkflowEngine):
    """의존관계를 만족하는 실행 순서를 계획하는 최소 구현체(T2-03).

    **Workflow Learning(Milestone 71, ADR-0089)**: `record_run_outcome()`
    으로 기록된, 같은 `task_ids` 조합(`_signature()`)의 과거 실행 순서 중
    성공률이 가장 높은 것이 있으면 `plan()`이 새로 계산하는 대신 그 순서를
    후보로 쓴다. 기록이 없으면(과거 실행 이력 없음) 기존 위상 정렬(DFS
    기반) 그대로 동작한다 — 100% 하위 호환.

    **Workflow Adaptive Planning(Milestone 72, ADR-0090)**: `_signature()`
    는 `dependencies`가 아니라 `task_ids`만으로 키를 잡는다 — 같은 Task
    묶음이 이후 dependency가 바뀐 채로 다시 계획되어도 과거 추천을 우선
    조회한다. 다만 추천은 어디까지나 "힌트"일 뿐이라, `plan()`은 그
    추천 순서가 **현재** `workflow.dependencies`를 실제로 만족하는지
    `_is_valid_order()`로 검증한 뒤에만 채택한다. 검증에 실패하면(추천이
    없거나, 있어도 지금 dependency를 어기면) 기존 DFS 위상 정렬로 완전히
    동일하게 fallback한다 — Workflow 정합성은 학습보다 항상 우선한다.

    **Workflow Cost Optimization(Milestone 73, ADR-0091)**: `recommended_
    order()`가 동일한 최고 성공률로 타이가 난 복수의 학습된 순서 후보를
    만나면, `task_engine`/`engine_registry`/`engine_selection_policy`가
    모두 주입돼 있는 경우에 한해 각 후보의 예상 실행 비용(M64
    `EngineSelectionPolicy`가 고른 Engine의 `estimated_cost_usd` 합)을
    2차 tie-break로 쓴다. 셋 중 하나라도 주입되지 않았거나 비용을 계산할
    수 없으면(Task/후보 조회 실패 등) 비용 비교를 건너뛰고 기존 tie-break
    (표본 수 → 먼저 기록된 순서)로 즉시 fallback한다 — 100% 하위 호환."""

    def __init__(
        self,
        *,
        task_engine: TaskEngine | None = None,
        engine_registry: EngineRegistry | None = None,
        engine_selection_policy: EngineSelectionPolicy | None = None,
    ) -> None:
        self._order_stats: dict[_WorkflowSignature, dict[tuple[str, ...], WorkflowOrderStat]] = {}
        self._task_engine = task_engine
        self._engine_registry = engine_registry
        self._engine_selection_policy = engine_selection_policy

    def plan(self, workflow: Workflow) -> list[str]:
        recommended = self.recommended_order(workflow)
        if recommended is not None and self._is_valid_order(recommended, workflow):
            return recommended
        return self._plan_by_dependency_order(workflow)

    def _is_valid_order(self, order: list[str], workflow: Workflow) -> bool:
        if sorted(order) != sorted(workflow.task_ids):
            return False
        position = {task_id: index for index, task_id in enumerate(order)}
        for task_id, dependencies in workflow.dependencies.items():
            for dependency in dependencies:
                if position[dependency] >= position[task_id]:
                    return False
        return True

    def _plan_by_dependency_order(self, workflow: Workflow) -> list[str]:
        order: list[str] = []
        visited: set[str] = set()

        def visit(task_id: str) -> None:
            if task_id in visited:
                return
            for dependency in workflow.dependencies.get(task_id, set()):
                visit(dependency)
            visited.add(task_id)
            order.append(task_id)

        for task_id in workflow.task_ids:
            visit(task_id)
        return order

    def record_run_outcome(self, workflow: Workflow, order: list[str], success: bool) -> None:
        signature = self._signature(workflow)
        orders = self._order_stats.setdefault(signature, {})
        order_key = tuple(order)
        stat = orders.get(order_key, WorkflowOrderStat())
        orders[order_key] = stat.record(success)

    def recommended_order(self, workflow: Workflow) -> list[str] | None:
        orders = self._order_stats.get(self._signature(workflow))
        if not orders:
            return None
        best_rate: float | None = None
        for stat in orders.values():
            rate = stat.success_rate()
            if rate is not None and (best_rate is None or rate > best_rate):
                best_rate = rate
        if best_rate is None:
            return None
        tied = [
            order_key for order_key, stat in orders.items() if stat.success_rate() == best_rate
        ]
        tied = self._break_tie_by_cost(tied)
        best_order = max(tied, key=lambda order_key: orders[order_key].total)
        return list(best_order)

    def _break_tie_by_cost(self, tied: list[tuple[str, ...]]) -> list[tuple[str, ...]]:
        if len(tied) <= 1:
            return tied
        if self._task_engine is None or self._engine_registry is None:
            return tied
        if self._engine_selection_policy is None:
            return tied
        costs: dict[tuple[str, ...], float] = {}
        for order_key in tied:
            cost = self._order_cost(order_key)
            if cost is None:
                return tied
            costs[order_key] = cost
        min_cost = min(costs.values())
        return [order_key for order_key in tied if costs[order_key] == min_cost]

    def _order_cost(self, order: tuple[str, ...]) -> float | None:
        assert self._task_engine is not None
        assert self._engine_registry is not None
        assert self._engine_selection_policy is not None
        total = 0.0
        for task_id in order:
            try:
                task = self._task_engine.get_task(task_id)
            except TaskNotFoundError:
                return None
            candidates = self._engine_registry.list_candidates(task)
            if not candidates:
                return None
            decision = self._engine_selection_policy.select(task, candidates)
            if decision is None:
                return None
            selected = next(
                (c for c in candidates if c.engine_name == decision.engine_name),
                None,
            )
            if selected is None:
                return None
            total += selected.estimated_cost_usd
        return total

    def _signature(self, workflow: Workflow) -> _WorkflowSignature:
        return frozenset(workflow.task_ids)
