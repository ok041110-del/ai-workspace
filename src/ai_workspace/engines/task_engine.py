from __future__ import annotations

import itertools

from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.task_engine import TaskEngine, TaskNotFoundError


class InMemoryTaskEngine(TaskEngine):
    """Task 생성/상태 전이를 메모리에 보관하는 최소 구현체(T2-03)."""

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
