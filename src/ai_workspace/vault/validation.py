"""ADR-0035 Save Flow 이후 실행하는 Validation. `AI_RULES`의 Backlink
Rule(`[[...]]`이 실제 문서를 가리키는가)과 Tag Rule(frontmatter에
`tags`가 있는가)을 코드로 확인한다 — EXECUTION_PROFILE 6단계
(Validation)를 Vault 쪽에서 자동화한 것이다."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from ai_workspace.vault.mapping import VAULT_CONTENT_DIRECTORIES

_BACKLINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
_TAGS_LINE_PATTERN = re.compile(r"^tags:\s*\[.*\]\s*$", re.MULTILINE)


@dataclass(frozen=True)
class VaultValidationIssue:
    path: Path
    message: str


def _iter_markdown_files(vault_root: Path) -> list[Path]:
    """`vault_root` 바로 아래 Vault 콘텐츠 디렉터리(16종, Milestone
    27부터 `14 Tasks` 포함)만 스캔한다. Milestone 26부터 `vault_root`
    가 저장소 root와 같아서, 무조건
    `rglob("*.md")`를 하면 `docs/`/`.claude/`/`.agents/` 등 Vault가
    아닌 마크다운까지 걸려 Backlink/Tag Validation을 오염시킨다."""
    files: list[Path] = []
    for name in VAULT_CONTENT_DIRECTORIES:
        directory = vault_root / name
        if directory.is_dir():
            files.extend(directory.rglob("*.md"))
    return sorted(files)


def _document_titles(vault_root: Path) -> set[str]:
    return {p.stem for p in _iter_markdown_files(vault_root)}


def find_broken_backlinks(
    vault_root: Path, only_paths: Iterable[Path] | None = None
) -> list[VaultValidationIssue]:
    """`[[제목]]`이 실제 존재하는 문서(파일명)를 가리키지 않는 경우를
    찾는다. 대상 문서 집합(어떤 제목이 "존재"하는가)은 항상 Vault
    전체를 기준으로 하지만, **어떤 파일의 링크를 검사할지**는
    `only_paths`로 좁힐 수 있다(M24-T07 Incremental Sync) — 예를 들어
    Auto Save가 방금 저장한 파일만 검사하면, 이번 저장과 무관한 Vault
    안의 기존 문제 때문에 저장이 실패한 것처럼 보이는 일을 막는다.
    `only_paths`를 생략하면 기존과 동일하게 Vault 전체를 검사한다."""
    titles = _document_titles(vault_root)
    paths = list(only_paths) if only_paths is not None else _iter_markdown_files(vault_root)
    issues: list[VaultValidationIssue] = []
    for path in paths:
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
