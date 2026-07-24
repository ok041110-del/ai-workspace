from __future__ import annotations

import itertools

from ai_workspace.domain.project import Project
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.approval_engine import (
    ApprovalActionType,
    ApprovalAlreadyDecidedError,
    ApprovalDecision,
    ApprovalEngine,
    ApprovalRequest,
    ApprovalRequestNotFoundError,
)
from ai_workspace.interfaces.automation_engine import AutomationEngine, DuplicateTriggerError
from ai_workspace.interfaces.engine_adapter import EngineAdapter, EngineExecutionError, EngineResult
from ai_workspace.interfaces.memory_engine import MemoryEngine
from ai_workspace.interfaces.project_repository import ProjectNotFoundError, ProjectRepository
from ai_workspace.interfaces.task_engine import TaskEngine, TaskNotFoundError
from ai_workspace.interfaces.workflow_engine import WorkflowEngine


class FakeProjectRepository(ProjectRepository):
    def __init__(self) -> None:
        self._projects: dict[str, Project] = {}

    def load(self, project_id: str) -> Project:
        if project_id not in self._projects:
            raise ProjectNotFoundError(project_id)
        return self._projects[project_id]

    def save(self, project: Project) -> None:
        self._projects[project.project_id] = project

    def list_projects(self) -> list[Project]:
        return list(self._projects.values())


class FakeWorkflowEngine(WorkflowEngine):
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


class FakeTaskEngine(TaskEngine):
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._id_generator = itertools.count(1)

    def create_task(self, project_id: str, title: str) -> Task:
        if not project_id or not title:
            raise ValueError("project_id와 title은 비어 있을 수 없습니다.")
        task_id = f"task-{next(self._id_generator)}"
        task = Task(task_id=task_id, project_id=project_id, title=title, status=TaskStatus.TODO)
        self._tasks[task_id] = task
        return task

    def transition(self, task: Task, new_status: TaskStatus) -> Task:
        task.transition_to(new_status)
        return task

    def get_task(self, task_id: str) -> Task:
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]


class FakeMemoryEngine(MemoryEngine):
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def remember(self, key: str, value: str) -> None:
        self._store[key] = value

    def recall(self, key: str) -> str | None:
        return self._store.get(key)


class FakeApprovalEngine(ApprovalEngine):
    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}
        self._id_generator = itertools.count(1)

    def submit(self, action_type: ApprovalActionType, description: str) -> ApprovalRequest:
        request_id = f"approval-{next(self._id_generator)}"
        request = ApprovalRequest(
            request_id=request_id, action_type=action_type, description=description
        )
        self._requests[request_id] = request
        return request

    def decide(self, request_id: str, approved: bool) -> ApprovalRequest:
        request = self._requests.get(request_id)
        if request is None:
            raise ApprovalRequestNotFoundError(request_id)
        if request.decision != ApprovalDecision.PENDING:
            raise ApprovalAlreadyDecidedError(request_id)
        request.decision = ApprovalDecision.APPROVED if approved else ApprovalDecision.REJECTED
        return request

    def is_approved(self, request_id: str) -> bool:
        request = self._requests.get(request_id)
        if request is None:
            raise ApprovalRequestNotFoundError(request_id)
        return request.decision == ApprovalDecision.APPROVED


class FakeAutomationEngine(AutomationEngine):
    def __init__(self) -> None:
        self._triggers: list[str] = []

    def register_trigger(self, trigger_id: str, description: str) -> None:
        if trigger_id in self._triggers:
            raise DuplicateTriggerError(trigger_id)
        self._triggers.append(trigger_id)

    def list_triggers(self) -> list[str]:
        return list(self._triggers)


class FakeEngineAdapter(EngineAdapter):
    def run_task(self, task: Task) -> EngineResult:
        return EngineResult(success=True, output=f"{task.task_id} 완료")


class FailingFakeEngineAdapter(EngineAdapter):
    def run_task(self, task: Task) -> EngineResult:
        raise EngineExecutionError("구현 엔진 프로세스를 실행할 수 없습니다.")
