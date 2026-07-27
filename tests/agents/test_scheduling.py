from __future__ import annotations

from tests.interfaces.fakes import FakeAgentRegistry, FakeAgentScheduler

from ai_workspace.agents.scheduling import is_agent_selected
from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole


def _register(registry: FakeAgentRegistry, agent_id: str) -> Agent:
    agent = Agent(
        agent_id=agent_id, role=AgentRole.CODING, capabilities=frozenset({AgentCapability.CODING})
    )
    registry.register(agent)
    return agent


def test_is_agent_selected_true_for_the_one_scheduler_picks() -> None:
    registry = FakeAgentRegistry()
    _register(registry, "agent-1")
    _register(registry, "agent-2")
    scheduler = FakeAgentScheduler()

    assert is_agent_selected(registry, scheduler, AgentCapability.CODING, "agent-1") is True


def test_is_agent_selected_false_for_agent_not_picked() -> None:
    registry = FakeAgentRegistry()
    _register(registry, "agent-1")
    _register(registry, "agent-2")
    scheduler = FakeAgentScheduler()

    assert is_agent_selected(registry, scheduler, AgentCapability.CODING, "agent-2") is False


def test_is_agent_selected_false_when_no_candidate_has_capability() -> None:
    registry = FakeAgentRegistry()
    agent = Agent(
        agent_id="agent-1",
        role=AgentRole.REVIEWER,
        capabilities=frozenset({AgentCapability.REVIEW}),
    )
    registry.register(agent)
    scheduler = FakeAgentScheduler()

    assert is_agent_selected(registry, scheduler, AgentCapability.CODING, "agent-1") is False


def test_is_agent_selected_true_for_sole_registered_agent() -> None:
    registry = FakeAgentRegistry()
    _register(registry, "agent-1")
    scheduler = FakeAgentScheduler()

    assert is_agent_selected(registry, scheduler, AgentCapability.CODING, "agent-1") is True
