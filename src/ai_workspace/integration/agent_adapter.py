"""Workspace Adapter Layer — Agent Adapter (ADR-0039, Milestone 28-T03).

Core Domain의 `AgentManager`/`AgentRegistry`/`AgentScheduler`
**Interface**에만 의존한다(Interface First) — 구체 구현체
(`InMemoryAgentManager` 등)는 생성자로 주입받고, `vault`는 전혀
알지 못한다. Agent 생성/등록/선택/상태 전이 로직은 여기서 새로 만들지
않고 전부 Core Domain Engine에 위임한다(연결·변환·위임만, ADR-0039)."""

from __future__ import annotations

from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus
from ai_workspace.interfaces.agent_manager import AgentManager
from ai_workspace.interfaces.agent_registry import AgentRegistry
from ai_workspace.interfaces.agent_scheduler import AgentScheduler


class AgentAdapter:
    """Agent 생성·등록·선택·상태 전이를 Core Domain Engine에 위임하는
    Adapter."""

    def __init__(
        self,
        manager: AgentManager,
        registry: AgentRegistry,
        scheduler: AgentScheduler,
    ) -> None:
        self._manager = manager
        self._registry = registry
        self._scheduler = scheduler

    def create_agent(
        self, role: AgentRole, capabilities: frozenset[AgentCapability] = frozenset()
    ) -> Agent:
        """Agent를 생성하고 곧바로 Registry에 등록한다 — 두 Interface를
        잇는 것 자체가 이 Adapter의 역할이다(각각은 독립 계약)."""
        agent = self._manager.create(role, capabilities)
        self._registry.register(agent)
        return agent

    def list_active_agents(self) -> list[Agent]:
        return self._registry.list_active()

    def select_agent(
        self, capability: AgentCapability, max_count: int = 1
    ) -> list[Agent]:
        return self._scheduler.select(self._registry.list_active(), capability, max_count)

    def transition_agent(self, agent: Agent, new_status: AgentStatus) -> Agent:
        return self._manager.transition(agent, new_status)
