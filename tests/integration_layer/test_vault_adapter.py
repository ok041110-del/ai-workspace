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
