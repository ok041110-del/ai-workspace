from __future__ import annotations

from ai_workspace.domain.workflow import Workflow
from ai_workspace.domain.workflow_order_memory import WorkflowOrderStat
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
    동일하게 fallback한다 — Workflow 정합성은 학습보다 항상 우선한다."""

    def __init__(self) -> None:
        self._order_stats: dict[_WorkflowSignature, dict[tuple[str, ...], WorkflowOrderStat]] = {}

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
        best_order: tuple[str, ...] | None = None
        best_rank: tuple[float, int] | None = None
        for order_key, stat in orders.items():
            rate = stat.success_rate()
            if rate is None:
                continue
            rank = (rate, stat.total)
            if best_rank is None or rank > best_rank:
                best_rank = rank
                best_order = order_key
        return list(best_order) if best_order is not None else None

    def _signature(self, workflow: Workflow) -> _WorkflowSignature:
        return frozenset(workflow.task_ids)
