from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.workflow import Workflow


class WorkflowExecutionError(Exception):
    pass


class WorkflowEngine(ABC):
    """Task 실행 순서/의존관계 조율 계약. 구체 구현체는 Milestone 2(T2-03)에서
    작성한다."""

    @abstractmethod
    def plan(self, workflow: Workflow) -> list[str]:
        """
        입력: 순환 의존이 없는(Workflow 생성 시 자체 검증됨) Workflow 인스턴스
        출력: 의존관계를 만족하는 실행 순서로 정렬된 task_id 리스트
              (의존 대상 task_id가 항상 그것에 의존하는 task_id보다 앞선다)
        예외: 계획 수립이 불가능한 상태(예: 알 수 없는 내부 불일치)를 만나면
              WorkflowExecutionError
        보장: 반환된 리스트에는 workflow.task_ids의 모든 원소가 정확히 한 번씩
              포함된다. 입력 workflow는 변경하지 않는다(side-effect 없음).
        """
        raise NotImplementedError
