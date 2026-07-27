from pathlib import Path

from ai_workspace.vault.validation import find_broken_backlinks, find_missing_tags


def test_find_broken_backlinks_detects_link_to_missing_document(tmp_path: Path) -> None:
    (tmp_path / "A.md").write_text("# A\n\n[[B]] [[Missing]]\n", encoding="utf-8")
    (tmp_path / "B.md").write_text("# B\n", encoding="utf-8")

    issues = find_broken_backlinks(tmp_path)

    assert len(issues) == 1
    assert "[[Missing]]" in issues[0].message


def test_find_broken_backlinks_empty_when_all_links_resolve(tmp_path: Path) -> None:
    (tmp_path / "A.md").write_text("# A\n\n[[B]]\n", encoding="utf-8")
    (tmp_path / "B.md").write_text("# B\n\n[[A]]\n", encoding="utf-8")

    assert find_broken_backlinks(tmp_path) == []


def test_find_missing_tags_flags_file_without_frontmatter(tmp_path: Path) -> None:
    path = tmp_path / "A.md"
    path.write_text("# A\n", encoding="utf-8")

    issues = find_missing_tags([path])

    assert len(issues) == 1
    assert "tags" in issues[0].message


def test_find_missing_tags_passes_file_with_tags(tmp_path: Path) -> None:
    path = tmp_path / "A.md"
    path.write_text("---\ntags: [daily]\n---\n\n# A\n", encoding="utf-8")

    assert find_missing_tags([path]) == []


def test_find_missing_tags_ignores_nonexistent_path(tmp_path: Path) -> None:
    assert find_missing_tags([tmp_path / "ghost.md"]) == []
