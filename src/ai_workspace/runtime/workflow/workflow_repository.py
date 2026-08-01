from __future__ import annotations

from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.workflow_repository import WorkflowNotFoundError, WorkflowRepository


class InMemoryWorkflowRepository(WorkflowRepository):
    """`Workflow`를 메모리에 보관하는 최소 구현체(Milestone 59).
    `InMemoryAutomationRepository`와 동일한 패턴 — 아직 영속화하지
    않는다(향후 `FileWorkflowRepository` 등으로 확장 가능하도록
    Interface만 보고 구현했다)."""

    def __init__(self) -> None:
        self._workflows: dict[str, Workflow] = {}

    def get(self, workflow_id: str) -> Workflow:
        if workflow_id not in self._workflows:
            raise WorkflowNotFoundError(workflow_id)
        return self._workflows[workflow_id]

    def save(self, workflow: Workflow) -> None:
        self._workflows[workflow.workflow_id] = workflow

    def list_workflows(self) -> list[Workflow]:
        return list(self._workflows.values())
