from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.observability.pipeline_stage_analyzer import PipelineStageAnalyzer
from ai_workspace.observability.snapshot import PipelineStageStatus


def test_analyze_marks_not_yet_when_no_report_published(tmp_path: Path) -> None:
    stages = PipelineStageAnalyzer().analyze(VaultAdapter(tmp_path))

    by_name = {stage.name: stage for stage in stages}
    assert by_name["Recommendation"].status == PipelineStageStatus.OBSERVED_NOT_YET
    assert by_name["Explainability"].status == PipelineStageStatus.OBSERVED_NOT_YET
    assert by_name["Execution"].status == PipelineStageStatus.OBSERVED_NOT_YET
    assert by_name["Experience"].status == PipelineStageStatus.OBSERVED_NOT_YET


def test_analyze_marks_done_when_report_exists(tmp_path: Path) -> None:
    report_dir = tmp_path / "15 Project Intelligence"
    report_dir.mkdir(parents=True)
    (report_dir / "Recommendation Intelligence.md").write_text("dummy", encoding="utf-8")

    stages = PipelineStageAnalyzer().analyze(VaultAdapter(tmp_path))

    by_name = {stage.name: stage for stage in stages}
    assert by_name["Recommendation"].status == PipelineStageStatus.OBSERVED_DONE


def test_analyze_marks_adaptation_and_orchestration_as_structural(tmp_path: Path) -> None:
    stages = PipelineStageAnalyzer().analyze(VaultAdapter(tmp_path))

    by_name = {stage.name: stage for stage in stages}
    assert by_name["Adaptation"].status == PipelineStageStatus.STRUCTURAL_INCLUDED
    assert by_name["Orchestration"].status == PipelineStageStatus.STRUCTURAL_INCLUDED


def test_analyze_marks_memory_as_not_observable(tmp_path: Path) -> None:
    stages = PipelineStageAnalyzer().analyze(VaultAdapter(tmp_path))

    by_name = {stage.name: stage for stage in stages}
    assert by_name["Memory"].status == PipelineStageStatus.NOT_OBSERVABLE


def test_analyze_returns_seven_stages_in_pipeline_order(tmp_path: Path) -> None:
    stages = PipelineStageAnalyzer().analyze(VaultAdapter(tmp_path))

    assert [stage.name for stage in stages] == [
        "Recommendation",
        "Adaptation",
        "Explainability",
        "Orchestration",
        "Execution",
        "Memory",
        "Experience",
    ]
