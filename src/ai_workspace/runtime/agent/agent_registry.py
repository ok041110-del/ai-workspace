from __future__ import annotations

from ai_workspace.domain.agent import Agent
from ai_workspace.interfaces.agent_registry import (
    AgentNotRegisteredError,
    AgentRegistry,
    DuplicateAgentRegistrationError,
)


class InMemoryAgentRegistry(AgentRegistry):
    """실행 중인 Agent 인스턴스를 인메모리로 관리하는 런타임 등록부 최소
    구현체(ARCHITECTURE.md §3.4, T1-18 계약, M4-T01)."""

    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        if agent.agent_id in self._agents:
            raise DuplicateAgentRegistrationError(agent.agent_id)
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Agent:
        if agent_id not in self._agents:
            raise AgentNotRegisteredError(agent_id)
        return self._agents[agent_id]

    def list_active(self) -> list[Agent]:
        return list(self._agents.values())

    def remove(self, agent_id: str) -> None:
        if agent_id not in self._agents:
            raise AgentNotRegisteredError(agent_id)
        del self._agents[agent_id]
