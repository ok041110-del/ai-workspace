"""ADR-0035 Save Flow 이후 실행하는 Validation. `AI_RULES`의 Backlink
Rule(`[[...]]`이 실제 문서를 가리키는가)과 Tag Rule(frontmatter에
`tags`가 있는가)을 코드로 확인한다 — EXECUTION_PROFILE 6단계
(Validation)를 Vault 쪽에서 자동화한 것이다."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

_BACKLINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
_TAGS_LINE_PATTERN = re.compile(r"^tags:\s*\[.*\]\s*$", re.MULTILINE)


@dataclass(frozen=True)
class VaultValidationIssue:
    path: Path
    message: str


def _iter_markdown_files(vault_root: Path) -> list[Path]:
    return sorted(p for p in vault_root.rglob("*.md"))


def _document_titles(vault_root: Path) -> set[str]:
    return {p.stem for p in _iter_markdown_files(vault_root)}


def find_broken_backlinks(vault_root: Path) -> list[VaultValidationIssue]:
    """Vault 전체에서 `[[제목]]`이 실제 존재하는 문서(파일명)를 가리키지
    않는 경우를 찾는다."""
    titles = _document_titles(vault_root)
    issues: list[VaultValidationIssue] = []
    for path in _iter_markdown_files(vault_root):
        text = path.read_text(encoding="utf-8")
        for match in _BACKLINK_PATTERN.finditer(text):
            target = match.group(1).strip()
            if target not in titles:
                issues.append(
                    VaultValidationIssue(
                        path=path, message=f"존재하지 않는 문서를 가리킴: [[{target}]]"
                    )
                )
    return issues


def find_missing_tags(paths: Iterable[Path]) -> list[VaultValidationIssue]:
    """주어진 파일들이 frontmatter `tags` 필드를 갖고 있는지 확인한다.
    Auto Save가 새로 만든 파일(create 모드)에만 적용한다 — append
    모드는 기존 파일의 frontmatter를 건드리지 않으므로 대상이 아니다."""
    issues: list[VaultValidationIssue] = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or not _TAGS_LINE_PATTERN.search(text):
            issues.append(VaultValidationIssue(path=path, message="frontmatter tags가 없음"))
    return issues
