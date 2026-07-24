from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus


class InvalidAgentTransitionError(Exception):
    """Agent의 상태 전이가 허용되지 않을 때 발생한다."""


class AgentManager(ABC):
    """Agent의 생성과 생명주기(상태 전이)를 관리하는 계약.
    ARCHITECTURE.md §3.4 Agent Manager. Agent 도메인 모델 자체는 상태 전이
    규칙을 갖지 않으므로(Task와 달리 transition_to()가 없음), 허용되는 전이
    규칙은 이 인터페이스의 구체 구현체가 정의한다. 구체 구현은 Milestone 2
    이후에 진행한다."""

    @abstractmethod
    def create(
        self, role: AgentRole, capabilities: frozenset[AgentCapability] = frozenset()
    ) -> Agent:
        """
        입력: role (Agent의 역할), capabilities (Agent가 수행 가능한 능력 집합,
              생략 시 빈 집합)
        출력: IDLE 상태로 생성된 새 Agent
        예외: 없음
        보장: 반환된 Agent의 agent_id는 이 AgentManager가 생성한 다른 어떤
              Agent의 agent_id와도 겹치지 않는다.
        """
        raise NotImplementedError

    @abstractmethod
    def transition(self, agent: Agent, new_status: AgentStatus) -> Agent:
        """
        입력: agent (전이 대상 Agent), new_status (전이하려는 상태)
        출력: 상태가 변경된 Agent
        예외: 허용되지 않는 전이일 경우 InvalidAgentTransitionError
        보장: 전이가 거부되면 agent.status는 호출 전과 동일하게 유지된다
              (부분 변경 없음).
        """
        raise NotImplementedError
