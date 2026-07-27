from pathlib import Path

from ai_workspace.vault.auto_save import run_auto_save
from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest


def _make_vault(tmp_path: Path) -> Path:
    adr_index = tmp_path / "03 ADR" / "ADR Index.md"
    adr_index.parent.mkdir(parents=True)
    adr_index.write_text("# ADR Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8")
    overview = tmp_path / "01 Overview" / "Overview.md"
    overview.parent.mkdir(parents=True)
    overview.write_text("---\ntags: [architecture]\n---\n\n# Overview\n", encoding="utf-8")
    return tmp_path


def test_run_auto_save_reports_saved_paths_and_passes_validation(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    requests = [
        VaultDocumentRequest(
            kind=VaultDocumentKind.ADR,
            title="X",
            summary="",
            related_docs=("Overview",),
            fields={"number": "1", "purpose": "p", "decision": "d", "impact": "i"},
        )
    ]

    report = run_auto_save(vault_root, requests)

    assert report.ok is True
    assert len(report.saved_paths) == 1
    assert report.saved_paths[0] == vault_root / "03 ADR/ADR Index.md"
    assert "저장됨: 1개" in report.summary()


def test_run_auto_save_second_call_reports_unchanged(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.ADR,
        title="X",
        summary="",
        fields={"number": "1", "purpose": "p", "decision": "d", "impact": "i"},
    )
    run_auto_save(vault_root, [request])

    report = run_auto_save(vault_root, [request])

    assert report.saved_paths == ()
    assert len(report.unchanged_paths) == 1


def test_run_auto_save_flags_broken_backlink_in_related_docs(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    (vault_root / "04 Backend").mkdir()
    (vault_root / "04 Backend/Backend Index.md").write_text(
        "# Backend Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.BACKEND,
        title="X",
        summary="요약",
        related_docs=("Nonexistent Document",),
    )

    report = run_auto_save(vault_root, [request])

    assert report.ok is False
    assert any("Nonexistent Document" in issue.message for issue in report.validation_issues)


def test_run_auto_save_creates_daily_file_and_validates_its_tags(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.DAILY, title="", summary="", date="2026-07-27"
    )

    report = run_auto_save(vault_root, [request])

    assert report.ok is True
    assert (vault_root / "13 Daily/2026-07-27.md").exists()
