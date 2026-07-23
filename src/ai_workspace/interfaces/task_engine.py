from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.task import Task, TaskStatus


class TaskNotFoundError(Exception):
    pass


class TaskEngine(ABC):
    """Task 생성/상태 전이 계약. 구체 구현체는 Phase 2에서 작성한다."""

    @abstractmethod
    def create_task(self, project_id: str, title: str) -> Task:
        """
        입력: project_id(빈 문자열 아님), title(빈 문자열 아님)
        출력: 상태가 TaskStatus.TODO인 새 Task
        예외: project_id 또는 title이 비어 있으면 ValueError
        보장: 반환된 Task.task_id는 저장소 내에서 유일하다.
        """
        raise NotImplementedError

    @abstractmethod
    def transition(self, task: Task, new_status: TaskStatus) -> Task:
        """
        입력: 기존 Task, 목표 상태(new_status)
        출력: status가 new_status로 갱신된 Task
        예외: `Task.transition_to()`가 허용하지 않는 전이면
              InvalidTaskTransitionError(도메인 예외)를 그대로 전파한다.
        보장: 예외가 발생하면 task는 변경되지 않은 상태로 남는다(원자적 전이).
        """
        raise NotImplementedError

    @abstractmethod
    def get_task(self, task_id: str) -> Task:
        """
        입력: task_id
        출력: 해당 task_id의 최신 Task
        예외: 존재하지 않으면 TaskNotFoundError
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError
