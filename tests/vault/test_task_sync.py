from pathlib import Path

from ai_workspace.vault.task_lifecycle import TaskStatus
from ai_workspace.vault.task_sync import sync_task_change, transition_and_sync

_MILESTONE_INDEX = "# Milestones Index\n\n## 관련 문서\n\n- [[Overview]]\n"
_DECISIONS_INDEX = "# Decisions Index\n\n## 관련 문서\n\n- [[Overview]]\n"

_TASK_WITH_DECISION = """---
tags: [task]
type: task
status: done
priority: high
milestone: M28
owner: AI
created: 2026-07-27
updated: 2026-07-27
---

# 로그인 기능 구현

## Decision

[[Template - Decision]] 방식을 따르기로 함
"""

_TASK_NO_DECISION = """---
tags: [task]
type: task
status: todo
priority: high
milestone: M28
owner: AI
created: 2026-07-27
updated: 2026-07-27
---

# 로그인 기능 구현

## Decision

-
"""


def _make_vault(tmp_path: Path, task_content: str) -> Path:
    (tmp_path / "14 Tasks").mkdir(parents=True)
    (tmp_path / "14 Tasks" / "T28-01.md").write_text(task_content, encoding="utf-8")
    (tmp_path / "11 Milestones").mkdir(parents=True)
    (tmp_path / "11 Milestones" / "Milestones Index.md").write_text(
        _MILESTONE_INDEX, encoding="utf-8"
    )
    (tmp_path / "12 Decisions").mkdir(parents=True)
    (tmp_path / "12 Decisions" / "Decisions Index.md").write_text(
        _DECISIONS_INDEX, encoding="utf-8"
    )
    return tmp_path


def test_sync_creates_daily_note_and_appends_progress_line(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path, _TASK_NO_DECISION)

    result = sync_task_change(
        vault_root, "T28-01", TaskStatus.TODO, TaskStatus.IN_PROGRESS, date="2026-07-28"
    )

    assert result.daily_updated is True
    daily_content = (vault_root / "13 Daily" / "2026-07-28.md").read_text(encoding="utf-8")
    assert "## 진행중" in daily_content
    assert "- [[T28-01]] todo → in-progress" in daily_content


def test_sync_is_idempotent_for_daily_note(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path, _TASK_NO_DECISION)
    sync_task_change(
        vault_root, "T28-01", TaskStatus.TODO, TaskStatus.IN_PROGRESS, date="2026-07-28"
    )

    result = sync_task_change(
        vault_root, "T28-01", TaskStatus.TODO, TaskStatus.IN_PROGRESS, date="2026-07-28"
    )

    assert result.daily_updated is False


def test_sync_appends_task_change_log_to_milestones_index(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path, _TASK_NO_DECISION)

    result = sync_task_change(
        vault_root, "T28-01", TaskStatus.TODO, TaskStatus.IN_PROGRESS, date="2026-07-28"
    )

    assert result.milestone_updated is True
    content = (vault_root / "11 Milestones" / "Milestones Index.md").read_text(encoding="utf-8")
    assert "## Task 변경 로그" in content
    assert "- 2026-07-28 [[T28-01]] todo → in-progress" in content
    assert "## 관련 문서" in content
    assert content.index("## Task 변경 로그") < content.index("## 관련 문서")


def test_sync_updates_decisions_index_when_task_has_decision_link(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path, _TASK_WITH_DECISION)

    result = sync_task_change(
        vault_root, "T28-01", TaskStatus.REVIEW, TaskStatus.DONE, date="2026-07-28"
    )

    assert result.decision_updated is True
    content = (vault_root / "12 Decisions" / "Decisions Index.md").read_text(encoding="utf-8")
    assert "## Task 연결" in content
    assert "- [[T28-01]] → [[Template - Decision]]" in content


def test_sync_skips_decisions_index_when_task_has_no_decision_link(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path, _TASK_NO_DECISION)

    result = sync_task_change(
        vault_root, "T28-01", TaskStatus.REVIEW, TaskStatus.DONE, date="2026-07-28"
    )

    assert result.decision_updated is False
    content = (vault_root / "12 Decisions" / "Decisions Index.md").read_text(encoding="utf-8")
    assert "## Task 연결" not in content


def test_transition_and_sync_moves_task_and_updates_daily(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path, _TASK_NO_DECISION)

    result = transition_and_sync(vault_root, "T28-01", TaskStatus.IN_PROGRESS, today="2026-07-28")

    assert result.daily_updated is True
    task_content = (vault_root / "14 Tasks" / "T28-01.md").read_text(encoding="utf-8")
    assert "status: in-progress" in task_content
    assert "updated: 2026-07-28" in task_content
