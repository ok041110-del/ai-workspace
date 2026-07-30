from pathlib import Path

from ai_workspace.vault.task_query import list_task_documents

_TASK_CONTENT = """---
tags: [task]
type: task
status: {status}
priority: high
milestone: M29
owner: AI
created: 2026-07-30
updated: 2026-07-30
---

# {title}

## Status

{status}
"""


def _write_task(vault_root: Path, task_id: str, title: str, status: str) -> None:
    tasks_dir = vault_root / "14 Tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    (tasks_dir / f"{task_id}.md").write_text(
        _TASK_CONTENT.format(status=status, title=title), encoding="utf-8"
    )


def _write_archived_task(vault_root: Path, task_id: str, title: str) -> None:
    archive_dir = vault_root / "14 Tasks" / "Archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    (archive_dir / f"{task_id}.md").write_text(
        _TASK_CONTENT.format(status="archived", title=title), encoding="utf-8"
    )


def test_list_task_documents_returns_empty_when_tasks_dir_missing(tmp_path: Path) -> None:
    assert list_task_documents(tmp_path) == []


def test_list_task_documents_parses_frontmatter(tmp_path: Path) -> None:
    _write_task(tmp_path, "T29-01", "설계", "todo")

    documents = list_task_documents(tmp_path)

    assert len(documents) == 1
    document = documents[0]
    assert document.task_id == "T29-01"
    assert document.title == "설계"
    assert document.status == "todo"
    assert document.priority == "high"
    assert document.milestone == "M29"
    assert document.owner == "AI"
    assert document.created == "2026-07-30"
    assert document.updated == "2026-07-30"
    assert document.archived is False


def test_list_task_documents_excludes_files_without_status(tmp_path: Path) -> None:
    tasks_dir = tmp_path / "14 Tasks"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "README.md").write_text("---\ntags: [system]\n---\n\n# 사용법\n", encoding="utf-8")
    _write_task(tmp_path, "T29-01", "설계", "todo")

    documents = list_task_documents(tmp_path)

    assert [document.task_id for document in documents] == ["T29-01"]


def test_list_task_documents_includes_archive_by_default(tmp_path: Path) -> None:
    _write_task(tmp_path, "T29-01", "설계", "todo")
    _write_archived_task(tmp_path, "T28-09", "완료된 Task")

    documents = list_task_documents(tmp_path)

    assert {document.task_id for document in documents} == {"T29-01", "T28-09"}
    archived = next(document for document in documents if document.task_id == "T28-09")
    assert archived.archived is True
    assert archived.status == "archived"


def test_list_task_documents_can_exclude_archive(tmp_path: Path) -> None:
    _write_task(tmp_path, "T29-01", "설계", "todo")
    _write_archived_task(tmp_path, "T28-09", "완료된 Task")

    documents = list_task_documents(tmp_path, include_archived=False)

    assert [document.task_id for document in documents] == ["T29-01"]
