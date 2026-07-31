from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.observability.vault_runtime_analyzer import VaultRuntimeAnalyzer


def test_analyze_returns_not_connected_when_vault_missing(tmp_path: Path) -> None:
    info = VaultRuntimeAnalyzer().analyze(VaultAdapter(tmp_path), tmp_path)

    assert info.vault_connected is False
    assert info.current_milestone == "Unknown"
    assert info.current_adr == "Unknown"
    assert info.current_pr is None
    assert info.last_modified_epoch is None


def test_analyze_reads_vault_connected_and_latest_adr(tmp_path: Path) -> None:
    milestones_dir = tmp_path / "11 Milestones"
    milestones_dir.mkdir(parents=True)
    (milestones_dir / "Milestones Index.md").write_text(
        "| Milestone | 이름 | 핵심 결과 | 관련 ADR |\n|---|---|---|---|\n"
        "| M44 | Recommendation Explainability | ... | ADR-0061 |\n",
        encoding="utf-8",
    )
    adr_dir = tmp_path / "03 ADR"
    adr_dir.mkdir(parents=True)
    (adr_dir / "ADR Index.md").write_text(
        "## ADR-0061: Recommendation Explainability\n\n- 목적: ...\n"
        "## ADR-0060: Recommendation Vocabulary Decision\n\n- 목적: ...\n",
        encoding="utf-8",
    )

    info = VaultRuntimeAnalyzer().analyze(VaultAdapter(tmp_path), tmp_path)

    assert info.vault_connected is True
    assert info.current_milestone == "M44 Recommendation Explainability"
    assert info.current_adr == "ADR-0061 Recommendation Explainability"


def test_analyze_current_pr_is_not_available(tmp_path: Path) -> None:
    info = VaultRuntimeAnalyzer().analyze(VaultAdapter(tmp_path), tmp_path)

    assert info.current_pr is None
