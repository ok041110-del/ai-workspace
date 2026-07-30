from pathlib import Path

import pytest

from ai_workspace.domain.agent import AgentCapability, AgentRole, AgentStatus
from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.integration.workflow_adapter import WorkflowAdapter
from ai_workspace.integration.workflow_agent_link import (
    AgentNotAssignedError,
    NoAvailableAgentError,
    WorkflowAgentLink,
)
from ai_workspace.integration.workflow_task_link import WorkflowTaskLink
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler


def _make_vault(tmp_path: Path) -> Path:
    (tmp_path / "11 Milestones").mkdir(parents=True)
    (tmp_path / "11 Milestones" / "Milestones Index.md").write_text(
        "# Milestones Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    (tmp_path / "12 Decisions").mkdir(parents=True)
    (tmp_path / "12 Decisions" / "Decisions Index.md").write_text(
        "# Decisions Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    return tmp_path


def _make_links(tmp_path: Path):
    vault_root = _make_vault(tmp_path)
    vault_adapter = VaultAdapter(vault_root)
    workflow_adapter = WorkflowAdapter(InMemoryWorkflowEngine(), InMemoryTaskEngine())
    agent_adapter = AgentAdapter(
        InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler()
    )
    task_link = WorkflowTaskLink(vault_adapter, workflow_adapter)
    agent_link = WorkflowAgentLink(agent_adapter, workflow_adapter)

    vault_adapter.create_task(
        "T28-05a",
        "구현",
        status="todo",
        priority="high",
        milestone="M28",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    _workflow, links = task_link.create_workflow_from_vault_tasks(
        "wf-1", "mission-1", "project-1", [("T28-05a", "구현")]
    )
    return task_link, agent_link, agent_adapter, links


def test_assign_agent_picks_matching_capability(tmp_path: Path) -> None:
    task_link, agent_link, agent_adapter, links = _make_links(tmp_path)
    coding_agent = agent_adapter.create_agent(
        AgentRole.CODING, frozenset({AgentCapability.CODING})
    )
    agent_adapter.create_agent(AgentRole.REVIEWER, frozenset({AgentCapability.REVIEW}))

    assignment = agent_link.assign_agent(links[0], AgentCapability.CODING)

    assert assignment.agent == coding_agent
    assert agent_link.get_assignment(links[0]) == assignment


def test_assign_agent_raises_when_no_candidate(tmp_path: Path) -> None:
    _task_link, agent_link, _agent_adapter, links = _make_links(tmp_path)

    with pytest.raises(NoAvailableAgentError):
        agent_link.assign_agent(links[0], AgentCapability.CODING)


def test_transition_agent_status_requires_assignment(tmp_path: Path) -> None:
    _task_link, agent_link, _agent_adapter, links = _make_links(tmp_path)

    with pytest.raises(AgentNotAssignedError):
        agent_link.transition_agent_status(links[0], AgentStatus.RUNNING)


def test_transition_agent_status_updates_assignment(tmp_path: Path) -> None:
    _task_link, agent_link, agent_adapter, links = _make_links(tmp_path)
    agent_adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    assignment = agent_link.assign_agent(links[0], AgentCapability.CODING)

    transitioned = agent_link.transition_agent_status(links[0], AgentStatus.RUNNING)

    assert transitioned.status is AgentStatus.RUNNING
    assert agent_link.get_assignment(links[0]).agent.status is AgentStatus.RUNNING
    assert transitioned.agent_id == assignment.agent.agent_id


def test_agent_progress_reflects_assigned_task_completion(tmp_path: Path) -> None:
    task_link, agent_link, agent_adapter, links = _make_links(tmp_path)
    agent = agent_adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    agent_link.assign_agent(links[0], AgentCapability.CODING)

    assert agent_link.agent_progress(agent) == 0.0

    task_link.transition_and_reflect(links[0], TaskStatus.IN_PROGRESS, today="2026-07-30")
    task_link.transition_and_reflect(links[0], TaskStatus.REVIEW, today="2026-07-30")
    task_link.transition_and_reflect(links[0], TaskStatus.DONE, today="2026-07-30")

    assert agent_link.agent_progress(agent) == 1.0


def test_agent_progress_is_zero_for_unassigned_agent(tmp_path: Path) -> None:
    _task_link, agent_link, agent_adapter, _links = _make_links(tmp_path)
    idle_agent = agent_adapter.create_agent(AgentRole.RESEARCH)

    assert agent_link.agent_progress(idle_agent) == 0.0
