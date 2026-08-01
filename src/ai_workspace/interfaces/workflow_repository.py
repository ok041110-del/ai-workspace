from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.workflow import Workflow


class WorkflowNotFoundError(Exception):
    """영속 저장소에 해당 workflow_id가 없을 때 발생한다."""


class WorkflowRepository(ABC):
    """`Workflow`의 영속적인 조회/저장 계약(Milestone 59). `AgentRepository`/
    `AutomationRepository`와 동일한 스타일(`get`/`save`는 upsert,
    `list_workflows`). `AutomationActionExecutor`의 `RUN_WORKFLOW` Action이
    `workflow_id`만 들고 있을 때 실제 `Workflow`를 조회하는 유일한 통로다 —
    이 Interface가 생기기 전에는 이 저장소에 `Workflow`를 workflow_id로
    영속 조회하는 경로가 전혀 없었다."""

    @abstractmethod
    def get(self, workflow_id: str) -> Workflow:
        """
        입력: workflow_id (빈 문자열이 아닌 식별자)
        출력: workflow_id에 해당하는 Workflow
        예외: 저장소에 해당 workflow_id가 없으면 WorkflowNotFoundError
        보장: side-effect 없음(read-only). 반환된 Workflow는 마지막 save()
              이후의 최신 상태를 반영한다.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, workflow: Workflow) -> None:
        """
        입력: workflow_id가 채워진 Workflow 인스턴스
        출력: 없음
        예외: 없음 (동일 workflow_id가 이미 있으면 덮어쓴다)
        보장: save(workflow) 직후 get(workflow.workflow_id)를 호출하면
              동일한 내용의 Workflow를 반환한다 (멱등적 upsert).
        """
        raise NotImplementedError

    @abstractmethod
    def list_workflows(self) -> list[Workflow]:
        """
        입력: 없음
        출력: 저장된 모든 Workflow의 목록 (없으면 빈 리스트)
        예외: 없음
        보장: 반환된 리스트를 호출자가 수정해도 저장소 내부 상태는 변하지
              않는다 (방어적 복사).
        """
        raise NotImplementedError
