"""Workspace Adapter Layer — Agent Adapter (ADR-0039, Milestone 28-T03).

Core Domain의 `AgentManager`/`AgentRegistry`/`AgentScheduler`
**Interface**에만 의존한다(Interface First) — 구체 구현체
(`InMemoryAgentManager` 등)는 생성자로 주입받고, `vault`는 전혀
알지 못한다. Agent 생성/등록/선택/상태 전이 로직은 여기서 새로 만들지
않고 전부 Core Domain Engine에 위임한다(연결·변환·위임만, ADR-0039)."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus
from ai_workspace.interfaces.agent_manager import AgentManager
from ai_workspace.interfaces.agent_registry import AgentRegistry
from ai_workspace.interfaces.agent_scheduler import AgentScheduler


@dataclass(frozen=True)
class AgentCapabilityView:
    """`AgentAdapter.list_active_agent_capabilities()`가 반환하는 활성
    Agent 하나의 읽기 전용 뷰(ADR-0045, Milestone 31-T02). 호출자는
    `domain.agent.Agent`/`AgentRole`/`AgentCapability`를 직접 import
    하지 않는다(다른 Adapter 공개 메서드와 동일한 원칙)."""

    agent_id: str
    role: str
    capabilities: frozenset[str]
    status: str


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

    def list_active_agent_capabilities(self) -> list[AgentCapabilityView]:
        """활성 Agent 전체를 Capability 관점의 읽기 전용 뷰로 열거한다
        (ADR-0045, Milestone 31-T02) — Intelligence Layer의 Capability
        Analyzer가 Agent 집계에 쓰는 유일한 통로. side-effect 없음
        (read-only)."""
        return [
            AgentCapabilityView(
                agent_id=agent.agent_id,
                role=agent.role.value,
                capabilities=frozenset(capability.value for capability in agent.capabilities),
                status=agent.status.value,
            )
            for agent in self._registry.list_active()
        ]

    def known_capabilities(self) -> frozenset[str]:
        """도메인이 정의한 `AgentCapability` 전체 값을 문자열 카탈로그로
        노출한다(ADR-0045) — Capability Gap Analyzer가 "정의됐지만
        활성 Agent가 없는 Capability"를 판정하는 기준이 된다. 단순
        열거/변환일 뿐 판단(집계·Gap 판정)은 하지 않는다(Adapter는
        비즈니스 로직을 갖지 않는다, ADR-0039)."""
        return frozenset(capability.value for capability in AgentCapability)
