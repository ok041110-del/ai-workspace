"""M23-T07: Execution Environment Integration.

vault/(M23-T03~T06)가 이 세션의 실제 실행 환경(Filesystem, 이
저장소의 실제 `Vault/`)에서 동작하는지 검증한다. 단위 테스트
(`tests/vault/`)는 전부 `tmp_path`의 최소 fixture만 다뤘으므로,
여기서는 실제 Vault 트리를 대상으로 (1) Validation이 실제로
깨진 Backlink를 찾아내는지, (2) Auto Save Workflow가 실제 문서
구조 위에서 왕복(저장→검증)에 성공하는지 확인한다."""

from __future__ import annotations

import shutil
from pathlib import Path

from ai_workspace.vault.auto_save import run_auto_save
from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest
from ai_workspace.vault.validation import find_broken_backlinks

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_VAULT_ROOT = _PROJECT_ROOT / "Vault" / "01 Projects" / "AI Workspace"

# AI_RULES/PROMPT_PROFILE/READING_PROFILES/Vault Integration Architecture가
# `[[...]]` 문법을 설명하기 위해 예시로 쓰는 텍스트 — 실제 문서를 가리키는
# Backlink가 아니다(반복적으로 수동 검증에서도 확인된 오탐, PREPARATION_SUMMARY
# 참고). 새로운 진짜 깨진 링크만 실패하도록 이 목록만 허용한다.
_KNOWN_PROSE_EXAMPLE_LINKS = {"이중 대괄호", "링크", "문서 제목", ".."}


def test_vault_root_exists_and_is_readable() -> None:
    """Filesystem 접근 검증: 이 실행 환경에서 실제 Vault 디렉터리를
    찾고 읽을 수 있어야 한다."""
    assert _VAULT_ROOT.is_dir()
    assert (_VAULT_ROOT / "00 System" / "PROJECT_INDEX.md").is_file()


def test_real_vault_has_no_unexpected_broken_backlinks() -> None:
    """Retrieval/Validation 검증: 실제 Vault 전체에서 새로운 깨진
    Backlink가 없어야 한다 — 알려진 프롬프트 예시 텍스트만 허용한다.
    (이 테스트를 작성하며 실제로 EXECUTION_PROFILE.md/Backend Index.md
    에서 줄바꿈으로 깨진 `[[Vault Integration\\nArchitecture]]`/
    `[[Architecture\\n  Overview]]` 링크 2건을 찾아 함께 고쳤다.)"""
    issues = find_broken_backlinks(_VAULT_ROOT)
    unexpected = [
        issue
        for issue in issues
        if issue.message.split("[[")[-1].rstrip("]") not in _KNOWN_PROSE_EXAMPLE_LINKS
    ]

    assert unexpected == []


def test_auto_save_round_trip_against_copy_of_real_vault(tmp_path: Path) -> None:
    """Auto Save 검증: 실제 Vault 트리를 복사한 뒤, 실제 ADR Index
    파일 구조 위에서 저장→검증 왕복이 성공하는지 확인한다."""
    vault_copy = tmp_path / "Vault"
    shutil.copytree(_VAULT_ROOT, vault_copy)
    adr_index_path = vault_copy / "03 ADR" / "ADR Index.md"
    before = adr_index_path.read_text(encoding="utf-8")

    request = VaultDocumentRequest(
        kind=VaultDocumentKind.ADR,
        title="Execution Environment Integration 검증(M23-T07)",
        summary="",
        fields={
            "number": "TEST",
            "purpose": "환경 통합 테스트용 임시 항목",
            "decision": "테스트 전용, 실제 Vault에는 반영되지 않음",
            "impact": "없음",
        },
    )

    report = run_auto_save(vault_copy, [request])

    unexpected = [
        issue
        for issue in report.validation_issues
        if issue.message.split("[[")[-1].rstrip("]") not in _KNOWN_PROSE_EXAMPLE_LINKS
    ]
    assert unexpected == []
    assert adr_index_path in report.saved_paths
    after = adr_index_path.read_text(encoding="utf-8")
    assert after != before
    assert "## ADR-TEST: Execution Environment Integration 검증(M23-T07)" in after
    # 복사본에만 반영됐는지 확인 — 실제 Vault는 건드리지 않는다.
    assert "ADR-TEST" not in (_VAULT_ROOT / "03 ADR" / "ADR Index.md").read_text(encoding="utf-8")
