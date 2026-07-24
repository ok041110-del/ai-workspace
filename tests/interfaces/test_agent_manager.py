import pytest

from ai_workspace.domain.agent import AgentCapability, AgentRole, AgentStatus
from ai_workspace.interfaces.agent_manager import InvalidAgentTransitionError

from .fakes import FakeAgentManager


def test_create_starts_idle_with_given_role_and_capabilities() -> None:
    manager = FakeAgentManager()

    agent = manager.create(AgentRole.CODING, frozenset({AgentCapability.CODING}))

    assert agent.status == AgentStatus.IDLE
    assert agent.role == AgentRole.CODING
    assert AgentCapability.CODING in agent.capabilities


def test_create_generates_unique_agent_ids() -> None:
    manager = FakeAgentManager()

    first = manager.create(AgentRole.CODING)
    second = manager.create(AgentRole.CODING)

    assert first.agent_id != second.agent_id


def test_transition_updates_status() -> None:
    manager = FakeAgentManager()
    agent = manager.create(AgentRole.CODING)

    updated = manager.transition(agent, AgentStatus.RUNNING)

    assert updated.status == AgentStatus.RUNNING


def test_transition_rejects_invalid_move_without_mutating_agent() -> None:
    manager = FakeAgentManager()
    agent = manager.create(AgentRole.CODING)
    manager.transition(agent, AgentStatus.RUNNING)
    manager.transition(agent, AgentStatus.STOPPED)

    with pytest.raises(InvalidAgentTransitionError):
        manager.transition(agent, AgentStatus.RUNNING)

    assert agent.status == AgentStatus.STOPPED
