from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.agent import Agent


class AgentNotFoundError(Exception):
    """영속 저장소에 해당 agent_id가 없을 때 발생한다."""


class AgentRepository(ABC):
    """Agent의 영속적인 조회/저장 계약. AgentRegistry(런타임 등록부)와 달리
    프로세스가 재시작된 후에도 저장된 내용이 유지된다. 구체 구현체는
    Milestone 2 이후 FileAgentRepository 등."""

    @abstractmethod
    def load(self, agent_id: str) -> Agent:
        """
        입력: agent_id (빈 문자열이 아닌 식별자)
        출력: agent_id에 해당하는 Agent
        예외: 저장소에 해당 agent_id가 없으면 AgentNotFoundError
        보장: side-effect 없음(read-only). 반환된 Agent는 마지막 save() 이후의
              최신 상태를 반영한다.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, agent: Agent) -> None:
        """
        입력: agent_id가 채워진 Agent 인스턴스
        출력: 없음
        예외: 없음 (동일 agent_id가 이미 있으면 덮어쓴다)
        보장: save(agent) 직후 load(agent.agent_id)를 호출하면 동일한 내용의
              Agent를 반환한다 (멱등적 upsert).
        """
        raise NotImplementedError

    @abstractmethod
    def list_agents(self) -> list[Agent]:
        """
        입력: 없음
        출력: 저장된 모든 Agent의 목록 (없으면 빈 리스트)
        예외: 없음
        보장: 반환된 리스트를 호출자가 수정해도 저장소 내부 상태는 변하지
              않는다 (방어적 복사).
        """
        raise NotImplementedError
