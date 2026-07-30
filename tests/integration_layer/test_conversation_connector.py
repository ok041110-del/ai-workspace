from pathlib import Path

from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.conversation_workflow_link import (
    ConversationConnector,
    ConversationTaskRequest,
)
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.integration.workflow_adapter import WorkflowAdapter
from ai_workspace.integration.workflow_agent_link import WorkflowAgentLink
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


def _make_connector(tmp_path: Path) -> tuple[ConversationConnector, AgentAdapter, Path]:
    vault_root = _make_vault(tmp_path)
    vault_adapter = VaultAdapter(vault_root)
    workflow_adapter = WorkflowAdapter(InMemoryWorkflowEngine(), InMemoryTaskEngine())
    agent_adapter = AgentAdapter(
        InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler()
    )
    task_link = WorkflowTaskLink(vault_adapter, workflow_adapter)
    agent_link = WorkflowAgentLink(agent_adapter, workflow_adapter)
    connector = ConversationConnector(vault_adapter, task_link, agent_link)
    return connector, agent_adapter, vault_root


def _request(**overrides: object) -> ConversationTaskRequest:
    fields: dict[str, object] = {
        "vault_task_id": "T28-06a",
        "title": "로그인 기능 구현",
        "status": "todo",
        "priority": "high",
        "milestone": "M28",
        "owner": "AI",
        "created": "2026-07-30",
        "updated": "2026-07-30",
        "workflow_id": "wf-1",
        "mission_id": "mission-1",
        "project_id": "project-1",
        "capability": AgentCapability.CODING,
    }
    fields.update(overrides)
    return ConversationTaskRequest(**fields)  # type: ignore[arg-type]


def test_handle_task_request_creates_task_workflow_and_assigns_agent(tmp_path: Path) -> None:
    connector, agent_adapter, vault_root = _make_connector(tmp_path)
    coding_agent = agent_adapter.create_agent(
        AgentRole.CODING, frozenset({AgentCapability.CODING})
    )

    result = connector.handle_task_request(_request())

    assert result.vault_task_created is True
    assert result.workflow.workflow_id == "wf-1"
    assert result.link.vault_task_id == "T28-06a"
    assert result.assignment.agent == coding_agent
    task_content = (vault_root / "14 Tasks" / "T28-06a.md").read_text(encoding="utf-8")
    assert "status: todo" in task_content


def test_advance_task_updates_domain_and_vault(tmp_path: Path) -> None:
    connector, agent_adapter, vault_root = _make_connector(tmp_path)
    agent_adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    result = connector.handle_task_request(_request())

    transitioned = connector.advance_task(
        result.link, TaskStatus.IN_PROGRESS, today="2026-07-30"
    )

    assert transitioned.status is TaskStatus.IN_PROGRESS
    vault_content = (vault_root / "14 Tasks" / "T28-06a.md").read_text(encoding="utf-8")
    assert "status: in-progress" in vault_content


def test_report_status_combines_task_statuses_and_completion(tmp_path: Path) -> None:
    connector, agent_adapter, _vault_root = _make_connector(tmp_path)
    agent_adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    result = connector.handle_task_request(_request())

    report = connector.report_status([result.link])
    assert report.task_status_by_vault_id == {"T28-06a": TaskStatus.TODO}
    assert report.complete is False

    connector.advance_task(result.link, TaskStatus.IN_PROGRESS, today="2026-07-30")
    connector.advance_task(result.link, TaskStatus.REVIEW, today="2026-07-30")
    connector.advance_task(result.link, TaskStatus.DONE, today="2026-07-30")

    report = connector.report_status([result.link])
    assert report.task_status_by_vault_id == {"T28-06a": TaskStatus.DONE}
    assert report.complete is True
