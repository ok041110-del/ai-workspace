"""M23-T04: Auto Save Workflow — Task 완료 후 여러 `VaultDocumentRequest`
를 한 번에 저장하고 Validation까지 수행한다. EXECUTION_PROFILE Standard
Workflow의 5단계(Document Update)에서 GitHub 원문을 갱신한 직후, AI가
관련 요청들을 모아 이 모듈 하나만 호출하면 저장(4단계) → Validation
(6단계) → 완료 보고(7단계) 문구까지 준비된다."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from ai_workspace.vault.connection import connect
from ai_workspace.vault.engine import VaultSaveEngine
from ai_workspace.vault.models import VaultDocumentRequest
from ai_workspace.vault.router import DocumentRouter
from ai_workspace.vault.validation import (
    VaultValidationIssue,
    find_broken_backlinks,
    find_missing_tags,
)


@dataclass(frozen=True)
class AutoSaveReport:
    saved_paths: tuple[Path, ...]
    unchanged_paths: tuple[Path, ...]
    validation_issues: tuple[VaultValidationIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.validation_issues

    def summary(self) -> str:
        lines = [
            f"저장됨: {len(self.saved_paths)}개",
            f"변경 없음: {len(self.unchanged_paths)}개",
        ]
        if self.validation_issues:
            lines.append(f"Validation 실패: {len(self.validation_issues)}건")
            lines.extend(f"  - {issue.path}: {issue.message}" for issue in self.validation_issues)
        else:
            lines.append("Validation 통과")
        return "\n".join(lines)


def run_auto_save(
    vault_root: Path, requests: Sequence[VaultDocumentRequest]
) -> AutoSaveReport:
    """`requests`를 전부 저장한 뒤, **이번 호출이 실제로 저장한
    파일만** Backlink를 검증하고 새로 만든 파일의 Tag를 검증해
    `AutoSaveReport`를 돌려준다(Incremental Sync, M24-T07) — Vault
    전체를 매번 다시 스캔하지 않으므로, 이번 저장과 무관한 기존
    문제 때문에 저장이 실패한 것처럼 보이지 않는다. Vault 전체
    감사가 필요하면 `vault.validation.find_broken_backlinks(vault_root)`
    를 직접 호출한다. 저장 자체는 하나가 실패해도 나머지를 계속
    진행한다 — 부분 실패를 감추지 않고 report에 그대로 남긴다."""
    engine = VaultSaveEngine(vault_root)
    router = DocumentRouter(vault_root)

    saved: list[Path] = []
    unchanged: list[Path] = []
    created: list[Path] = []
    for request in requests:
        target = router.resolve(request)
        changed = engine.save(request)
        (saved if changed else unchanged).append(target.path)
        if changed and target.mode == "create":
            created.append(target.path)

    issues: list[VaultValidationIssue] = []
    issues.extend(find_broken_backlinks(vault_root, only_paths=saved))
    issues.extend(find_missing_tags(created))

    return AutoSaveReport(
        saved_paths=tuple(saved),
        unchanged_paths=tuple(unchanged),
        validation_issues=tuple(issues),
    )


def run_auto_save_on_default_vault(
    requests: Sequence[VaultDocumentRequest], vault_root: Path | None = None
) -> AutoSaveReport:
    """M24-T06 Execution Integration: `vault_root`를 넘기지 않으면
    `vault.connection.connect()`로 실제 Obsidian Vault를 찾아 연결한
    뒤 `run_auto_save()`를 수행한다. "다음 Task 진행" 같은 명령을
    받은 AI가 tmp_path를 직접 계산할 필요 없이 이 함수 하나로 실제
    Vault에 저장한다."""
    connection = connect(vault_root)
    return run_auto_save(connection.root, requests)
