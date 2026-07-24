import pytest

from ai_workspace.domain.agent import Agent, AgentRole
from ai_workspace.interfaces.agent_repository import AgentNotFoundError

from .fakes import FakeAgentRepository


def test_save_then_load_returns_same_agent() -> None:
    repository = FakeAgentRepository()
    agent = Agent(agent_id="a1", role=AgentRole.CODING)

    repository.save(agent)

    assert repository.load("a1") == agent


def test_load_unknown_agent_raises_not_found() -> None:
    repository = FakeAgentRepository()

    with pytest.raises(AgentNotFoundError):
        repository.load("unknown")


def test_list_agents_returns_defensive_copy() -> None:
    repository = FakeAgentRepository()
    repository.save(Agent(agent_id="a1", role=AgentRole.CODING))

    agents = repository.list_agents()
    agents.append(Agent(agent_id="a2", role=AgentRole.REVIEWER))

    assert len(repository.list_agents()) == 1
