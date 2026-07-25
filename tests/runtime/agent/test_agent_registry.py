import pytest

from ai_workspace.domain.agent import Agent, AgentRole
from ai_workspace.interfaces.agent_registry import (
    AgentNotRegisteredError,
    DuplicateAgentRegistrationError,
)
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry


def test_register_then_get_returns_same_agent() -> None:
    registry = InMemoryAgentRegistry()
    agent = Agent(agent_id="a1", role=AgentRole.CODING)

    registry.register(agent)

    assert registry.get("a1") == agent


def test_register_duplicate_raises_error() -> None:
    registry = InMemoryAgentRegistry()
    registry.register(Agent(agent_id="a1", role=AgentRole.CODING))

    with pytest.raises(DuplicateAgentRegistrationError):
        registry.register(Agent(agent_id="a1", role=AgentRole.REVIEWER))


def test_get_unregistered_raises_not_registered() -> None:
    registry = InMemoryAgentRegistry()

    with pytest.raises(AgentNotRegisteredError):
        registry.get("unknown")


def test_list_active_returns_defensive_copy() -> None:
    registry = InMemoryAgentRegistry()
    registry.register(Agent(agent_id="a1", role=AgentRole.CODING))

    agents = registry.list_active()
    agents.append(Agent(agent_id="a2", role=AgentRole.REVIEWER))

    assert len(registry.list_active()) == 1


def test_remove_then_get_raises_not_registered() -> None:
    registry = InMemoryAgentRegistry()
    registry.register(Agent(agent_id="a1", role=AgentRole.CODING))

    registry.remove("a1")

    with pytest.raises(AgentNotRegisteredError):
        registry.get("a1")


def test_remove_unregistered_raises_not_registered() -> None:
    registry = InMemoryAgentRegistry()

    with pytest.raises(AgentNotRegisteredError):
        registry.remove("unknown")
