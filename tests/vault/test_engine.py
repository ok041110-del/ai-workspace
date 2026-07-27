from pathlib import Path

from ai_workspace.vault.engine import VaultSaveEngine
from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest


def _make_vault(tmp_path: Path) -> Path:
    adr_index = tmp_path / "03 ADR" / "ADR Index.md"
    adr_index.parent.mkdir(parents=True)
    adr_index.write_text("# ADR Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8")
    return tmp_path


def test_save_adr_appends_section_to_adr_index(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    engine = VaultSaveEngine(vault_root)
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.ADR,
        title="Vault Integration Layer 도입",
        summary="",
        fields={"number": "0035", "purpose": "p", "decision": "d", "impact": "i"},
    )

    changed = engine.save(request)

    content = (vault_root / "03 ADR/ADR Index.md").read_text(encoding="utf-8")
    assert changed is True
    assert "## ADR-0035: Vault Integration Layer 도입" in content


def test_save_daily_creates_new_file(tmp_path: Path) -> None:
    engine = VaultSaveEngine(tmp_path)
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.DAILY, title="", summary="", date="2026-07-27"
    )

    changed = engine.save(request)

    daily_path = tmp_path / "13 Daily/2026-07-27.md"
    assert changed is True
    assert daily_path.exists()
    assert "# 2026-07-27" in daily_path.read_text(encoding="utf-8")


def test_save_returns_false_when_nothing_changes(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    engine = VaultSaveEngine(vault_root)
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.ADR,
        title="X",
        summary="",
        fields={"number": "1", "purpose": "p", "decision": "d", "impact": "i"},
    )
    engine.save(request)

    changed_again = engine.save(request)

    assert changed_again is False
