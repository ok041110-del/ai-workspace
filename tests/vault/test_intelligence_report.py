from pathlib import Path

from ai_workspace.vault.intelligence_report import write_project_intelligence_report


def test_write_project_intelligence_report_creates_file(tmp_path: Path) -> None:
    path = write_project_intelligence_report(tmp_path, "# Project Intelligence\n\ncontent\n")

    assert path == tmp_path / "15 Project Intelligence" / "Project Intelligence.md"
    assert path.read_text(encoding="utf-8") == "# Project Intelligence\n\ncontent\n"


def test_write_project_intelligence_report_overwrites_previous_content(tmp_path: Path) -> None:
    write_project_intelligence_report(tmp_path, "old content\n")

    path = write_project_intelligence_report(tmp_path, "new content\n")

    assert path.read_text(encoding="utf-8") == "new content\n"
