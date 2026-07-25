from __future__ import annotations

from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.workflow_engine import WorkflowEngine


class InMemoryWorkflowEngine(WorkflowEngine):
    """의존관계를 만족하는 실행 순서를 계획하는 최소 구현체(T2-03)."""

    def plan(self, workflow: Workflow) -> list[str]:
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
