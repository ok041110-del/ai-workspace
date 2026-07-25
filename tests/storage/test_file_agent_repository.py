from pathlib import Path

import pytest

from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus
from ai_workspace.interfaces.agent_repository import AgentNotFoundError
from ai_workspace.storage.file_agent_repository import FileAgentRepository


def test_save_then_load_returns_same_agent(tmp_path: Path) -> None:
    repo = FileAgentRepository(tmp_path)
    agent = Agent(
        agent_id="a1",
        role=AgentRole.CODING,
        capabilities=frozenset({AgentCapability.CODING, AgentCapability.GIT}),
        status=AgentStatus.RUNNING,
    )

    repo.save(agent)
    loaded = repo.load("a1")

    assert loaded == agent


def test_load_missing_raises_error(tmp_path: Path) -> None:
    repo = FileAgentRepository(tmp_path)

    with pytest.raises(AgentNotFoundError):
        repo.load("unknown")


def test_save_overwrites_existing_agent(tmp_path: Path) -> None:
    repo = FileAgentRepository(tmp_path)
    repo.save(Agent(agent_id="a1", role=AgentRole.CODING))
    repo.save(Agent(agent_id="a1", role=AgentRole.CODING, status=AgentStatus.STOPPED))

    assert repo.load("a1").status == AgentStatus.STOPPED


def test_list_agents_returns_all_saved_agents(tmp_path: Path) -> None:
    repo = FileAgentRepository(tmp_path)
    repo.save(Agent(agent_id="a1", role=AgentRole.CODING))
    repo.save(Agent(agent_id="a2", role=AgentRole.REVIEWER))

    agents = repo.list_agents()

    assert {a.agent_id for a in agents} == {"a1", "a2"}


def test_list_agents_empty_when_no_agents(tmp_path: Path) -> None:
    repo = FileAgentRepository(tmp_path)

    assert repo.list_agents() == []


def test_agent_with_no_capabilities_round_trips(tmp_path: Path) -> None:
    repo = FileAgentRepository(tmp_path)
    repo.save(Agent(agent_id="a1", role=AgentRole.PLANNER))

    loaded = repo.load("a1")

    assert loaded.capabilities == frozenset()


def test_agent_persists_across_new_repository_instance(tmp_path: Path) -> None:
    FileAgentRepository(tmp_path).save(Agent(agent_id="a1", role=AgentRole.CODING))

    reopened = FileAgentRepository(tmp_path)

    assert reopened.load("a1").role == AgentRole.CODING
