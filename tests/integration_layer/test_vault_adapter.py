from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter


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


def test_create_task_writes_task_file(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)

    created = adapter.create_task(
        "T28-03",
        "Integration Layer 구현",
        status="todo",
        priority="high",
        milestone="M28",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )

    assert created is True
    content = (vault_root / "14 Tasks" / "T28-03.md").read_text(encoding="utf-8")
    assert "status: todo" in content
    assert "# Integration Layer 구현" in content


def test_create_task_is_idempotent(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)
    adapter.create_task(
        "T28-03",
        "Integration Layer 구현",
        status="todo",
        priority="high",
        milestone="M28",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )

    created_again = adapter.create_task(
        "T28-03",
        "Integration Layer 구현",
        status="todo",
        priority="high",
        milestone="M28",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )

    assert created_again is False


def test_transition_task_with_sync_updates_daily_note(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)
    adapter.create_task(
        "T28-03",
        "Integration Layer 구현",
        status="todo",
        priority="high",
        milestone="M28",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )

    outcome = adapter.transition_task("T28-03", "in-progress", today="2026-07-30")

    assert outcome.old_status == "todo"
    assert outcome.new_status == "in-progress"
    assert outcome.daily_updated is True
    daily_content = (vault_root / "13 Daily" / "2026-07-30.md").read_text(encoding="utf-8")
    assert "- [[T28-03]]" in daily_content


def test_transition_task_without_sync_skips_related_documents(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)
    adapter.create_task(
        "T28-03",
        "Integration Layer 구현",
        status="todo",
        priority="high",
        milestone="M28",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )

    outcome = adapter.transition_task(
        "T28-03", "in-progress", today="2026-07-30", sync_related_documents=False
    )

    assert outcome.old_status == "todo"
    assert outcome.new_status == "in-progress"
    assert outcome.daily_updated is None
    assert not (vault_root / "13 Daily" / "2026-07-30.md").exists()


def test_list_tasks_returns_empty_when_no_tasks(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)

    assert adapter.list_tasks() == []


def test_list_tasks_returns_created_task(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)
    adapter.create_task(
        "T28-03",
        "Integration Layer 구현",
        status="todo",
        priority="high",
        milestone="M28",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )

    tasks = adapter.list_tasks()

    assert len(tasks) == 1
    task = tasks[0]
    assert task.task_id == "T28-03"
    assert task.title == "Integration Layer 구현"
    assert task.status == "todo"
    assert task.priority == "high"
    assert task.milestone == "M28"
    assert task.owner == "AI"
    assert task.archived is False


def test_list_tasks_reflects_transitions_and_archive(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)
    adapter.create_task(
        "T28-03",
        "Integration Layer 구현",
        status="todo",
        priority="high",
        milestone="M28",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    adapter.transition_task("T28-03", "in-progress", today="2026-07-30")
    adapter.transition_task("T28-03", "review", today="2026-07-30")
    adapter.transition_task("T28-03", "done", today="2026-07-30")
    adapter.transition_task("T28-03", "archived", today="2026-07-30")

    tasks = adapter.list_tasks()

    assert len(tasks) == 1
    assert tasks[0].status == "archived"
    assert tasks[0].archived is True

    assert adapter.list_tasks(include_archived=False) == []


def test_publish_intelligence_report_writes_markdown(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)

    path = adapter.publish_intelligence_report("# Project Intelligence\n\ncontent\n")

    assert path == vault_root / "15 Project Intelligence" / "Project Intelligence.md"
    assert path.read_text(encoding="utf-8") == "# Project Intelligence\n\ncontent\n"


def test_publish_project_context_writes_markdown(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)

    path = adapter.publish_project_context("# Project Context\n\ncontent\n")

    assert path == vault_root / "15 Project Intelligence" / "Project Context.md"
    assert path.read_text(encoding="utf-8") == "# Project Context\n\ncontent\n"


def test_publish_capability_report_writes_markdown(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)

    path = adapter.publish_capability_report("# Capability Intelligence\n\ncontent\n")

    assert path == vault_root / "15 Project Intelligence" / "Capability Intelligence.md"
    assert path.read_text(encoding="utf-8") == "# Capability Intelligence\n\ncontent\n"


def test_publish_experience_intelligence_writes_markdown(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)

    path = adapter.publish_experience_intelligence("# Experience Intelligence\n\ncontent\n")

    assert path == vault_root / "15 Project Intelligence" / "Experience Intelligence.md"
    assert path.read_text(encoding="utf-8") == "# Experience Intelligence\n\ncontent\n"


def test_publish_architecture_guardian_writes_markdown(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)

    path = adapter.publish_architecture_guardian("# Architecture Guardian\n\ncontent\n")

    assert path == vault_root / "15 Project Intelligence" / "Architecture Guardian.md"
    assert path.read_text(encoding="utf-8") == "# Architecture Guardian\n\ncontent\n"


def test_report_last_modified_returns_none_when_missing(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)

    mtime = adapter.report_last_modified(
        "15 Project Intelligence", "Recommendation Execution.md"
    )
    assert mtime is None


def test_report_last_modified_returns_mtime_when_published(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    adapter = VaultAdapter(vault_root)
    adapter.publish_recommendation_execution("# Recommendation Execution\n\ncontent\n")

    mtime = adapter.report_last_modified("15 Project Intelligence", "Recommendation Execution.md")

    assert mtime is not None
    assert mtime > 0
