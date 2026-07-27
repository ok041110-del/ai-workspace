"""M23-T04: Auto Save Workflow — Task 완료 후 여러 `VaultDocumentRequest`
를 한 번에 저장하고 Validation까지 수행한다. EXECUTION_PROFILE Standard
Workflow의 5단계(Document Update)에서 GitHub 원문을 갱신한 직후, AI가
관련 요청들을 모아 이 모듈 하나만 호출하면 저장(4단계) → Validation
(6단계) → 완료 보고(7단계) 문구까지 준비된다."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

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
    """`requests`를 전부 저장한 뒤 Vault 전체 Backlink와 새로 만든 파일의
    Tag를 검증해 `AutoSaveReport`를 돌려준다. 저장 자체는 하나가
    실패해도 나머지를 계속 진행한다 — 부분 실패를 감추지 않고 report에
    그대로 남긴다."""
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
    issues.extend(find_broken_backlinks(vault_root))
    issues.extend(find_missing_tags(created))

    return AutoSaveReport(
        saved_paths=tuple(saved),
        unchanged_paths=tuple(unchanged),
        validation_issues=tuple(issues),
    )
