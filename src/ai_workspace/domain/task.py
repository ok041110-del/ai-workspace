from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


_ALLOWED_TRANSITIONS: dict[TaskStatus, frozenset[TaskStatus]] = {
    TaskStatus.TODO: frozenset({TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED}),
    TaskStatus.IN_PROGRESS: frozenset(
        {TaskStatus.REVIEW, TaskStatus.BLOCKED, TaskStatus.CANCELLED}
    ),
    TaskStatus.REVIEW: frozenset(
        {TaskStatus.DONE, TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED}
    ),
    TaskStatus.BLOCKED: frozenset({TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED}),
    TaskStatus.DONE: frozenset(),
    TaskStatus.CANCELLED: frozenset(),
}


class InvalidTaskTransitionError(ValueError):
    pass


@dataclass
class Task:
    task_id: str
    project_id: str
    title: str
    status: TaskStatus = TaskStatus.TODO
    # Task는 Workflow에 소속되기 전에도 존재할 수 있어 선택 필드로 둔다.
    workflow_id: str | None = None

    def transition_to(self, new_status: TaskStatus) -> None:
        allowed = _ALLOWED_TRANSITIONS[self.status]
        if new_status not in allowed:
            raise InvalidTaskTransitionError(
                f"{self.status.value} -> {new_status.value} 상태 전이는 허용되지 않습니다."
            )
        self.status = new_status
