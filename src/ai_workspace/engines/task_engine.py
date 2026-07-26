from __future__ import annotations

import itertools

from ai_workspace.domain.step import Step
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.task_engine import TaskEngine, TaskNotFoundError


class InMemoryTaskEngine(TaskEngine):
    """Task 생성/상태 전이를 메모리에 보관하는 최소 구현체(T2-03, Step
    실행 이력은 M5-T06에서 추가)."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._id_generator = itertools.count(1)
        self._steps: dict[str, list[Step]] = {}
        self._step_id_generator = itertools.count(1)

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

    def record_step(self, task_id: str, description: str) -> Step:
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        step = Step(
            step_id=f"step-{next(self._step_id_generator)}",
            task_id=task_id,
            description=description,
        )
        self._steps.setdefault(task_id, []).append(step)
        return step

    def get_steps(self, task_id: str) -> list[Step]:
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return list(self._steps.get(task_id, []))
