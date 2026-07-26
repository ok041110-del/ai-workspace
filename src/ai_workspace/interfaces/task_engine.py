from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.step import Step
from ai_workspace.domain.task import Task, TaskStatus


class TaskNotFoundError(Exception):
    pass


class TaskEngine(ABC):
    """Task 생성/상태 전이 계약. 구체 구현체는 Milestone 2(T2-03)에서 작성한다.

    `record_step`/`get_steps`(M5-T06)로 Task의 실행 이력(Step)도 함께
    관리한다 — Step의 소유권을 특정 Agent가 아니라 Task의 실행 컨텍스트인
    이 Engine에 둔다(재작업 시도 등은 어느 Agent가 관찰하든 동일한 이력을
    봐야 하므로)."""

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

    @abstractmethod
    def record_step(self, task_id: str, description: str) -> Step:
        """
        입력: task_id(create_task()로 생성되어 있어야 함), description
        출력: 새로 기록된 Step(step_id는 저장소 내에서 유일)
        예외: task_id가 존재하지 않으면 TaskNotFoundError
        보장: record_step() 이후 get_steps(task_id) 결과의 마지막 원소가
              이 Step이다(기록 순서를 보존한다).
        """
        raise NotImplementedError

    @abstractmethod
    def get_steps(self, task_id: str) -> list[Step]:
        """
        입력: task_id
        출력: 해당 task_id에 기록된 Step 목록(기록 순서, 없으면 빈 리스트)
        예외: task_id가 존재하지 않으면 TaskNotFoundError
        보장: side-effect 없음(read-only). 반환된 리스트를 호출자가
              수정해도 내부 상태는 변하지 않는다(방어적 복사).
        """
        raise NotImplementedError
