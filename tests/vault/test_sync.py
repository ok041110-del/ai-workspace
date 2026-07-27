from pathlib import Path

import pytest

from ai_workspace.vault.sync import (
    VaultConflictError,
    VaultDocumentNotFoundError,
    content_hash,
    delete_document,
    find_references,
    rename_document,
)


def test_content_hash_changes_when_file_content_changes(tmp_path: Path) -> None:
    path = tmp_path / "A.md"
    path.write_text("hello", encoding="utf-8")
    first = content_hash(path)

    path.write_text("hello world", encoding="utf-8")

    assert content_hash(path) != first


def test_find_references_finds_files_linking_to_title(tmp_path: Path) -> None:
    (tmp_path / "A.md").write_text("# A\n\n[[B]]\n", encoding="utf-8")
    (tmp_path / "B.md").write_text("# B\n", encoding="utf-8")
    (tmp_path / "C.md").write_text("# C\n", encoding="utf-8")

    referencing = find_references(tmp_path, "B")

    assert referencing == [tmp_path / "A.md"]


def test_rename_document_renames_file_and_updates_backlinks(tmp_path: Path) -> None:
    (tmp_path / "Old Title.md").write_text("# Old Title\n", encoding="utf-8")
    (tmp_path / "Other.md").write_text(
        "# Other\n\nSee [[Old Title]] and [[Old Title|alias]].\n", encoding="utf-8"
    )

    result = rename_document(tmp_path, "Old Title", "New Title")

    assert not (tmp_path / "Old Title.md").exists()
    assert (tmp_path / "New Title.md").exists()
    assert result.new_path == tmp_path / "New Title.md"
    other_text = (tmp_path / "Other.md").read_text(encoding="utf-8")
    assert "[[New Title]]" in other_text
    assert "[[New Title|alias]]" in other_text
    assert "Old Title" not in other_text


def test_rename_document_missing_source_raises() -> None:
    with pytest.raises(VaultDocumentNotFoundError):
        rename_document(Path("/vault"), "Ghost", "New")


def test_rename_document_conflicts_when_target_exists(tmp_path: Path) -> None:
    (tmp_path / "A.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "B.md").write_text("# B\n", encoding="utf-8")

    with pytest.raises(VaultConflictError):
        rename_document(tmp_path, "A", "B")


def test_delete_document_refuses_when_still_referenced(tmp_path: Path) -> None:
    (tmp_path / "A.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "B.md").write_text("[[A]]\n", encoding="utf-8")

    result = delete_document(tmp_path, "A")

    assert result.deleted is False
    assert (tmp_path / "A.md").exists()
    assert result.referencing_paths == (tmp_path / "B.md",)


def test_delete_document_force_deletes_even_when_referenced(tmp_path: Path) -> None:
    (tmp_path / "A.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "B.md").write_text("[[A]]\n", encoding="utf-8")

    result = delete_document(tmp_path, "A", force=True)

    assert result.deleted is True
    assert not (tmp_path / "A.md").exists()


def test_delete_document_succeeds_when_unreferenced(tmp_path: Path) -> None:
    (tmp_path / "A.md").write_text("# A\n", encoding="utf-8")

    result = delete_document(tmp_path, "A")

    assert result.deleted is True
    assert result.referencing_paths == ()


def test_delete_document_missing_raises() -> None:
    with pytest.raises(VaultDocumentNotFoundError):
        delete_document(Path("/vault"), "Ghost")
