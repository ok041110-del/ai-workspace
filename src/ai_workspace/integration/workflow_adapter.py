"""Workspace Adapter Layer — Workflow Adapter (ADR-0039, Milestone 28-T03).

Core Domain의 `WorkflowEngine`/`TaskEngine` **Interface**에만 의존한다
(Interface First, `.ai/RULES.md` §1.3) — 구체 구현체(`InMemoryWorkflowEngine`
등)는 생성자로 주입받고, `vault`는 전혀 알지 못한다. 계획 수립/상태 전이
로직은 여기서 새로 만들지 않고 전부 Core Domain Engine에 위임한다(연결·
변환·위임만, ADR-0039)."""

from __future__ import annotations

from collections.abc import Mapping

from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.interfaces.workflow_engine import WorkflowEngine


class WorkflowAdapter:
    """Workflow/Task 생성·계획·상태 전이를 Core Domain Engine에 위임하는
    Adapter."""

    def __init__(self, workflow_engine: WorkflowEngine, task_engine: TaskEngine) -> None:
        self._workflow_engine = workflow_engine
        self._task_engine = task_engine

    def create_workflow(
        self,
        workflow_id: str,
        mission_id: str,
        task_ids: list[str],
        dependencies: Mapping[str, set[str]] | None = None,
    ) -> Workflow:
        return Workflow(
            workflow_id=workflow_id,
            mission_id=mission_id,
            task_ids=list(task_ids),
            dependencies=dict(dependencies or {}),
        )

    def plan(self, workflow: Workflow) -> list[str]:
        return self._workflow_engine.plan(workflow)

    def create_task(self, project_id: str, title: str) -> Task:
        return self._task_engine.create_task(project_id, title)

    def transition_task(self, task: Task, new_status: TaskStatus) -> Task:
        return self._task_engine.transition(task, new_status)

    def get_task(self, task_id: str) -> Task:
        return self._task_engine.get_task(task_id)
