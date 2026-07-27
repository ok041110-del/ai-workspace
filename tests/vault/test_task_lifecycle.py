from pathlib import Path

import pytest

from ai_workspace.vault.task_lifecycle import (
    InvalidTaskTransitionError,
    TaskFrontmatterError,
    TaskNotFoundError,
    TaskStatus,
    transition_task_status,
)

_TASK_CONTENT = """---
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

## Status

todo
"""


def _make_task(tmp_path: Path, content: str = _TASK_CONTENT) -> Path:
    task_dir = tmp_path / "14 Tasks"
    task_dir.mkdir(parents=True)
    path = task_dir / "T28-01.md"
    path.write_text(content, encoding="utf-8")
    return tmp_path


def test_transition_updates_status_and_updated_field(tmp_path: Path) -> None:
    vault_root = _make_task(tmp_path)

    result = transition_task_status(
        vault_root, "T28-01", TaskStatus.IN_PROGRESS, today="2026-07-28"
    )

    assert result.old_status is TaskStatus.TODO
    assert result.new_status is TaskStatus.IN_PROGRESS
    assert result.archived is False
    content = result.path.read_text(encoding="utf-8")
    assert "status: in-progress" in content
    assert "updated: 2026-07-28" in content
    assert "created: 2026-07-27" in content


def test_disallowed_transition_raises(tmp_path: Path) -> None:
    vault_root = _make_task(tmp_path)

    with pytest.raises(InvalidTaskTransitionError):
        transition_task_status(vault_root, "T28-01", TaskStatus.DONE)


def test_done_to_archived_moves_file_to_archive_dir(tmp_path: Path) -> None:
    vault_root = _make_task(
        tmp_path, _TASK_CONTENT.replace("status: todo", "status: done")
    )

    result = transition_task_status(vault_root, "T28-01", TaskStatus.ARCHIVED)

    assert result.archived is True
    assert result.path == vault_root / "14 Tasks" / "Archive" / "T28-01.md"
    assert result.path.exists()
    assert not (vault_root / "14 Tasks" / "T28-01.md").exists()
    assert "status: archived" in result.path.read_text(encoding="utf-8")


def test_archived_has_no_further_transitions(tmp_path: Path) -> None:
    vault_root = _make_task(
        tmp_path, _TASK_CONTENT.replace("status: todo", "status: archived")
    )

    with pytest.raises(InvalidTaskTransitionError):
        transition_task_status(vault_root, "T28-01", TaskStatus.TODO)


def test_missing_task_raises_not_found(tmp_path: Path) -> None:
    task_dir = tmp_path / "14 Tasks"
    task_dir.mkdir(parents=True)

    with pytest.raises(TaskNotFoundError):
        transition_task_status(tmp_path, "ghost", TaskStatus.IN_PROGRESS)


def test_missing_status_frontmatter_raises(tmp_path: Path) -> None:
    vault_root = _make_task(tmp_path, "---\ntags: [task]\n---\n\n# X\n")

    with pytest.raises(TaskFrontmatterError):
        transition_task_status(vault_root, "T28-01", TaskStatus.IN_PROGRESS)
