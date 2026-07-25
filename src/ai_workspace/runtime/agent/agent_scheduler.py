from __future__ import annotations

from ai_workspace.domain.agent import Agent, AgentCapability
from ai_workspace.interfaces.agent_scheduler import AgentScheduler


class InMemoryAgentScheduler(AgentScheduler):
    """Capability 기준으로 실행할 Agent를 선택하는 최소 구현체
    (ARCHITECTURE.md §3.4, T2-02)."""

    def select(
        self, candidates: list[Agent], capability: AgentCapability, max_count: int = 1
    ) -> list[Agent]:
        matched = [agent for agent in candidates if capability in agent.capabilities]
        return matched[:max_count]
