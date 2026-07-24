from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.agent import Agent


class AgentNotRegisteredError(Exception):
    """AgentRegistry에 등록되지 않은 agent_id를 조회/제거하려 할 때 발생한다."""


class DuplicateAgentRegistrationError(Exception):
    """이미 등록된 agent_id를 다시 등록하려 할 때 발생한다."""


class AgentRegistry(ABC):
    """실행 중인 Agent 인스턴스의 런타임 등록부(runtime registry) 계약.
    ARCHITECTURE.md §3.4 Agent Registry.

    AgentRepository(agent_repository.py)와의 차이: AgentRegistry는 프로세스가
    살아있는 동안만 유지되는 in-memory 등록부이며, 프로세스가 재시작되면
    내용이 사라진다. 재시작 후에도 남아야 하는 영속 정보는 AgentRepository가
    담당한다. 이 둘은 서로 다른 책임을 가지며 혼용하지 않는다."""

    @abstractmethod
    def register(self, agent: Agent) -> None:
        """
        입력: 등록할 Agent
        출력: 없음
        예외: 이미 동일한 agent_id가 등록되어 있으면 DuplicateAgentRegistrationError
        보장: register(agent) 직후 get(agent.agent_id)는 동일한 Agent를 반환한다.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, agent_id: str) -> Agent:
        """
        입력: agent_id
        출력: 등록된 Agent
        예외: 등록되어 있지 않으면 AgentNotRegisteredError
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError

    @abstractmethod
    def list_active(self) -> list[Agent]:
        """
        입력: 없음
        출력: 현재 등록된 모든 Agent의 목록 (없으면 빈 리스트)
        예외: 없음
        보장: 반환된 리스트를 호출자가 수정해도 registry 내부 상태는 변하지
              않는다 (방어적 복사).
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, agent_id: str) -> None:
        """
        입력: agent_id
        출력: 없음
        예외: 등록되어 있지 않으면 AgentNotRegisteredError
        보장: remove(agent_id) 이후 get(agent_id)는 AgentNotRegisteredError를
              발생시킨다.
        """
        raise NotImplementedError
