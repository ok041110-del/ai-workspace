"""M24-T08: End-to-End Integration Test — 이 저장소의 실제 Obsidian
Vault(Milestone 26부터 저장소 root 자체가 Vault Root)를 대상으로
한다. `tmp_path`는 전혀 쓰지 않는다(M24 DoD 요구사항 — "tmp_path만
쓰는 테스트는 M24 완료 기준으로 인정하지 않는다").

이 모듈이 만드는 파일은 전부 존재할 수 없는 미래 날짜/고유 제목
("9999-...", "M24 E2E ...")을 써서 실제 문서와 절대 충돌하지 않게
하고, 매 테스트 전후로 스스로 정리한다 — 기존 문서는 생성 이후
전혀 건드리지 않는다. `test_run_auto_save_writes_to_real_adr_index_
and_reports_result`만 예외적으로 실제 `ADR Index.md`(기존 문서)에
임시 섹션을 추가하지만, `finally`로 원본 바이트를 그대로 복원한다."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_workspace.vault.auto_save import run_auto_save
from ai_workspace.vault.connection import VaultConnectionError, connect, resolve_default_vault_root
from ai_workspace.vault.filesystem import VaultFileSystem
from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest
from ai_workspace.vault.sync import delete_document, find_references, rename_document
from ai_workspace.vault.validation import find_broken_backlinks
from ai_workspace.vault.writer import VaultWriter

_VAULT_ROOT = Path(__file__).resolve().parents[2]

_TEST_TITLE = "M24 E2E Scratch 9999-12-31"
_TEST_TITLE_RENAMED = "M24 E2E Scratch 9999-12-31 Renamed"
_REFERRER_TITLE = "M24 E2E Scratch Referrer 9999-12-30"


def _cleanup_scratch_docs() -> None:
    daily_dir = _VAULT_ROOT / "13 Daily"
    for title in (_TEST_TITLE, _TEST_TITLE_RENAMED, _REFERRER_TITLE):
        path = daily_dir / f"{title}.md"
        if path.exists():
            path.unlink()


@pytest.fixture(autouse=True)
def _clean_scratch_docs() -> None:
    _cleanup_scratch_docs()
    yield
    _cleanup_scratch_docs()


def test_connect_to_real_vault() -> None:
    connection = connect(_VAULT_ROOT)
    assert connection.root == _VAULT_ROOT


def test_resolve_default_vault_root_finds_real_vault() -> None:
    assert resolve_default_vault_root(_VAULT_ROOT) == _VAULT_ROOT


def test_connect_rejects_nonexistent_path() -> None:
    with pytest.raises(VaultConnectionError):
        connect(_VAULT_ROOT / "does-not-exist-vault")


def test_real_vault_create_update_rename_delete_round_trip() -> None:
    """Filesystem Adapter(M24-T02) + Vault Writer(M24-T03) + Vault
    Synchronization(M24-T07)을 실제 Vault 위에서 전부 왕복시킨다."""
    fs = VaultFileSystem()
    writer = VaultWriter()
    daily_dir = _VAULT_ROOT / "13 Daily"

    # Create
    doc_path = daily_dir / f"{_TEST_TITLE}.md"
    content = f"---\ntags: [daily]\n---\n\n# {_TEST_TITLE}\n\n## 관련 문서\n\n- [[Overview]]\n"
    fs.create(doc_path, content)
    assert doc_path.exists()
    assert fs.read(doc_path) == content

    referrer_path = daily_dir / f"{_REFERRER_TITLE}.md"
    fs.create(
        referrer_path,
        f"---\ntags: [daily]\n---\n\n# {_REFERRER_TITLE}\n\n[[{_TEST_TITLE}]]\n",
    )
    assert find_references(_VAULT_ROOT, _TEST_TITLE) == [referrer_path]

    # Update
    changed = writer.upsert_section(doc_path, "테스트 섹션", "- 값\n")
    assert changed is True
    assert "## 테스트 섹션" in fs.read(doc_path)

    # Rename — 실제 파일명 변경 + 참조 문서의 Backlink 자동 갱신.
    result = rename_document(_VAULT_ROOT, _TEST_TITLE, _TEST_TITLE_RENAMED)
    assert result.new_path.exists()
    assert not doc_path.exists()
    assert f"[[{_TEST_TITLE_RENAMED}]]" in referrer_path.read_text(encoding="utf-8")

    # Validation — Rename 이후 참조 문서의 링크가 깨지지 않았는지 확인.
    assert find_broken_backlinks(_VAULT_ROOT, only_paths=[referrer_path]) == []

    # Delete — 이번 테스트가 만든 문서만 삭제한다(기존 문서 아님).
    referrer_delete = delete_document(_VAULT_ROOT, _REFERRER_TITLE, force=True)
    assert referrer_delete.deleted is True
    doc_delete = delete_document(_VAULT_ROOT, _TEST_TITLE_RENAMED)
    assert doc_delete.deleted is True
    assert not result.new_path.exists()


def test_run_auto_save_writes_to_real_adr_index_and_restores_it() -> None:
    """Auto Save Workflow(M24-T05)가 실제 `ADR Index.md`에 저장하는지
    확인한다 — 기존 문서를 잠시 바꾸지만 `finally`로 원본을 그대로
    복원해 영구 변경을 남기지 않는다."""
    adr_index_path = _VAULT_ROOT / "03 ADR" / "ADR Index.md"
    before = adr_index_path.read_text(encoding="utf-8")
    try:
        request = VaultDocumentRequest(
            kind=VaultDocumentKind.ADR,
            title=_TEST_TITLE,
            summary="",
            fields={
                "number": "9999",
                "purpose": "M24 E2E 테스트 전용 임시 항목",
                "decision": "테스트 종료 시 즉시 원상 복구됨",
                "impact": "없음",
            },
        )

        report = run_auto_save(_VAULT_ROOT, [request])

        after = adr_index_path.read_text(encoding="utf-8")
        assert report.ok is True
        assert adr_index_path in report.saved_paths
        assert f"## ADR-9999: {_TEST_TITLE}" in after
    finally:
        adr_index_path.write_text(before, encoding="utf-8")

    assert adr_index_path.read_text(encoding="utf-8") == before
