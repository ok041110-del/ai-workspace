from pathlib import Path

from ai_workspace.observability.workspace_info_analyzer import WorkspaceInfoAnalyzer


def test_analyze_reads_project_name_and_latest_milestone(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "ai-workspace"\n', encoding="utf-8"
    )
    milestones_dir = tmp_path / "11 Milestones"
    milestones_dir.mkdir(parents=True)
    (milestones_dir / "Milestones Index.md").write_text(
        "\n".join(
            [
                "| Milestone | 이름 | 핵심 결과 | 관련 ADR |",
                "|---|---|---|---|",
                "| M1 | 기반 구축 | ... | ADR-0006 |",
                "| M44 | Recommendation Explainability | ... | ADR-0061 |",
            ]
        ),
        encoding="utf-8",
    )

    info = WorkspaceInfoAnalyzer().analyze(tmp_path)

    assert info.project_name == "ai-workspace"
    assert info.milestone == "M44 Recommendation Explainability"
    assert info.current_workflow is None


def test_analyze_falls_back_to_unknown_without_guessing(tmp_path: Path) -> None:
    info = WorkspaceInfoAnalyzer().analyze(tmp_path)

    assert info.project_name == "Unknown"
    assert info.milestone == "Unknown"
