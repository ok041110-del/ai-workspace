from pathlib import Path

from ai_workspace.vault.capability_report import write_capability_report


def test_write_capability_report_creates_file(tmp_path: Path) -> None:
    path = write_capability_report(tmp_path, "# Capability Intelligence\n\ncontent\n")

    assert path == tmp_path / "15 Project Intelligence" / "Capability Intelligence.md"
    assert path.read_text(encoding="utf-8") == "# Capability Intelligence\n\ncontent\n"


def test_write_capability_report_overwrites_previous_content(tmp_path: Path) -> None:
    write_capability_report(tmp_path, "old content\n")

    path = write_capability_report(tmp_path, "new content\n")

    assert path.read_text(encoding="utf-8") == "new content\n"
