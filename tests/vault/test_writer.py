from pathlib import Path

from ai_workspace.vault.writer import VaultWriter


def test_create_file_writes_new_file(tmp_path: Path) -> None:
    writer = VaultWriter()
    path = tmp_path / "13 Daily/2026-07-27.md"

    changed = writer.create_file(path, "# 2026-07-27\n")

    assert changed is True
    assert path.read_text(encoding="utf-8") == "# 2026-07-27\n"


def test_create_file_does_not_overwrite_existing(tmp_path: Path) -> None:
    writer = VaultWriter()
    path = tmp_path / "note.md"
    path.write_text("original", encoding="utf-8")

    changed = writer.create_file(path, "new content")

    assert changed is False
    assert path.read_text(encoding="utf-8") == "original"


def test_upsert_section_inserts_before_related_docs_heading(tmp_path: Path) -> None:
    writer = VaultWriter()
    path = tmp_path / "Index.md"
    path.write_text(
        "# Index\n\n## ADR-0001: 기존\n\n- 목적: a\n\n## 관련 문서\n\n- [[Overview]]\n",
        encoding="utf-8",
    )

    changed = writer.upsert_section(
        path, "ADR-0002: 신규", "- 목적: b\n- 결정: c\n- 영향: d\n"
    )

    content = path.read_text(encoding="utf-8")
    assert changed is True
    assert content.index("## ADR-0002: 신규") < content.index("## 관련 문서")
    assert "## ADR-0001: 기존" in content
    assert "- 목적: b" in content


def test_upsert_section_replaces_existing_section_with_same_heading(tmp_path: Path) -> None:
    writer = VaultWriter()
    path = tmp_path / "Index.md"
    path.write_text(
        "# Index\n\n## ADR-0001: 제목\n\n- 목적: old\n\n## 관련 문서\n\n- [[Overview]]\n",
        encoding="utf-8",
    )

    writer.upsert_section(path, "ADR-0001: 제목", "- 목적: new\n")

    content = path.read_text(encoding="utf-8")
    assert content.count("## ADR-0001: 제목") == 1
    assert "- 목적: new" in content
    assert "- 목적: old" not in content


def test_upsert_section_is_noop_when_content_unchanged(tmp_path: Path) -> None:
    writer = VaultWriter()
    path = tmp_path / "Index.md"
    original = "# Index\n\n## ADR-0001: 제목\n\n- 목적: same\n\n## 관련 문서\n\n- [[Overview]]\n"
    path.write_text(original, encoding="utf-8")
    mtime_before = path.stat().st_mtime_ns

    changed = writer.upsert_section(path, "ADR-0001: 제목", "- 목적: same\n")

    assert changed is False
    assert path.stat().st_mtime_ns == mtime_before


def test_upsert_section_appends_to_end_when_no_related_docs_heading(tmp_path: Path) -> None:
    writer = VaultWriter()
    path = tmp_path / "Index.md"
    path.write_text("# Index\n\n## 기존\n\n- a\n", encoding="utf-8")

    writer.upsert_section(path, "신규", "- b\n")

    content = path.read_text(encoding="utf-8")
    assert "## 기존" in content
    assert content.index("## 기존") < content.index("## 신규")
