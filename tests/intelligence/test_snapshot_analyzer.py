from pathlib import Path

from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.snapshot import ProjectSnapshotAnalyzer
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


def _make_agent_adapter() -> AgentAdapter:
    return AgentAdapter(InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler())


#: 순차 전이만 허용된다(vault.task_lifecycle) — 목표 status까지의 경로.
_TRANSITION_CHAIN = ["todo", "in-progress", "review", "done", "archived"]


def _create_task(
    adapter: VaultAdapter, task_id: str, title: str, *, status: str, milestone: str, owner: str
) -> None:
    adapter.create_task(
        task_id,
        title,
        status="todo",
        priority="medium",
        milestone=milestone,
        owner=owner,
        created="2026-07-30",
        updated="2026-07-30",
    )
    target_index = _TRANSITION_CHAIN.index(status)
    for step in _TRANSITION_CHAIN[1 : target_index + 1]:
        adapter.transition_task(task_id, step, today="2026-07-30", sync_related_documents=False)


def test_analyze_returns_empty_snapshot_when_no_tasks(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(_make_vault(tmp_path))
    analyzer = ProjectSnapshotAnalyzer(vault_adapter)

    result = analyzer.analyze(today="2026-07-30")

    snapshot = result.snapshot
    assert snapshot.total_tasks == 0
    assert snapshot.progress_ratio == 0.0
    assert snapshot.by_status == {}
    assert snapshot.active_agent_count == 0
    assert result.tasks == []


def test_analyze_aggregates_status_milestone_and_owner(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    vault_adapter = VaultAdapter(vault_root)
    _create_task(
        vault_adapter, "T29-01", "설계", status="todo", milestone="M29", owner="AI"
    )
    _create_task(
        vault_adapter,
        "T29-02",
        "Snapshot 구현",
        status="in-progress",
        milestone="M29",
        owner="AI",
    )
    _create_task(
        vault_adapter, "T28-09", "완료된 Task", status="done", milestone="M28", owner="User"
    )
    analyzer = ProjectSnapshotAnalyzer(vault_adapter)

    result = analyzer.analyze(today="2026-07-30")
    snapshot = result.snapshot

    assert snapshot.total_tasks == 3
    assert snapshot.todo_count == 1
    assert snapshot.in_progress_count == 1
    assert snapshot.done_count == 1
    assert snapshot.by_milestone == {"M29": 2, "M28": 1}
    assert snapshot.by_owner == {"AI": 2, "User": 1}
    assert snapshot.progress_ratio == 1 / 3
    assert snapshot.generated_at == "2026-07-30"
    assert {task.task_id for task in result.tasks} == {"T29-01", "T29-02", "T28-09"}


def test_analyze_counts_active_agents_when_agent_adapter_injected(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(_make_vault(tmp_path))
    agent_adapter = _make_agent_adapter()
    agent_adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    agent_adapter.create_agent(AgentRole.REVIEWER, frozenset({AgentCapability.REVIEW}))
    analyzer = ProjectSnapshotAnalyzer(vault_adapter, agent_adapter)

    result = analyzer.analyze(today="2026-07-30")

    assert result.snapshot.active_agent_count == 2


def test_analyze_excludes_archived_when_requested(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    vault_adapter = VaultAdapter(vault_root)
    _create_task(vault_adapter, "T29-01", "설계", status="todo", milestone="M29", owner="AI")
    _create_task(
        vault_adapter, "T28-09", "완료된 Task", status="done", milestone="M28", owner="AI"
    )
    vault_adapter.transition_task("T28-09", "archived", today="2026-07-30")
    analyzer = ProjectSnapshotAnalyzer(vault_adapter)

    result = analyzer.analyze(include_archived=False, today="2026-07-30")

    assert result.snapshot.total_tasks == 1
    assert {task.task_id for task in result.tasks} == {"T29-01"}
