from pathlib import Path

import pytest

from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest
from ai_workspace.vault.router import DocumentRouter, UnroutableVaultKindError


def test_resolve_adr_appends_to_adr_index(tmp_path: Path) -> None:
    router = DocumentRouter(tmp_path)
    request = VaultDocumentRequest(kind=VaultDocumentKind.ADR, title="X", summary="")

    target = router.resolve(request)

    assert target.path == tmp_path / "03 ADR/ADR Index.md"
    assert target.mode == "append"


def test_resolve_daily_uses_request_date(tmp_path: Path) -> None:
    router = DocumentRouter(tmp_path)
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.DAILY, title="", summary="", date="2026-07-27"
    )

    target = router.resolve(request)

    assert target.path == tmp_path / "13 Daily/2026-07-27.md"
    assert target.mode == "create"


def test_resolve_daily_without_date_uses_today(tmp_path: Path) -> None:
    router = DocumentRouter(tmp_path)
    request = VaultDocumentRequest(kind=VaultDocumentKind.DAILY, title="", summary="")

    target = router.resolve(request)

    assert target.path.suffix == ".md"
    assert target.path.parent == tmp_path / "13 Daily"


def test_resolve_unknown_kind_raises() -> None:
    router = DocumentRouter(Path("/vault"))

    with pytest.raises(UnroutableVaultKindError):
        router.resolve(VaultDocumentRequest(kind="unknown", title="", summary=""))  # type: ignore[arg-type]
