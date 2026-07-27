"""M23-T05: Vault Synchronization.

Create/Update은 이미 `writer.py`(File Creator/File Updater)가 담당한다.
이 모듈은 나머지 파일 관리 정책을 구현한다.

- **Rename**: 문서 파일명을 바꾸고 Vault 전체의 Backlink(`[[제목]]`)를
  함께 갱신한다(Backlink Rule 위반 방지).
- **Delete**: 다른 문서가 아직 참조 중이면 기본적으로 거부한다(Orphan
  Backlink 방지) — `force=True`일 때만 참조가 남아 있어도 삭제한다.
- **Conflict Handling**: `content_hash()`로 파일 내용 해시를 만들고,
  `VaultWriter.upsert_section()`에 `expected_hash`를 넘기면 그 사이에
  파일이 바뀌었을 때 `VaultConflictError`로 실패한다(조용히 덮어쓰지
  않는다).
- **Version Strategy**: 별도 버전 관리 시스템을 새로 만들지 않는다 —
  Vault 콘텐츠는 이미 이 Git 저장소 자체로 버전 관리되므로(Milestone 26
  부터 Vault Root == 저장소 Root), 파일 단위 변경 이력은 git이 담당한다
  (ADR-0035와 동일한 최소 복잡성 원칙).
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from ai_workspace.vault.mapping import VAULT_CONTENT_DIRECTORIES

_BACKLINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


class VaultDocumentNotFoundError(FileNotFoundError):
    """Rename/Delete 대상 문서를 파일명으로 찾지 못했을 때 발생한다."""


class VaultConflictError(RuntimeError):
    """예상 해시와 실제 파일 내용이 달라(다른 경로로 먼저 바뀜) 저장을
    거부할 때 발생한다."""


def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _iter_vault_markdown_files(vault_root: Path) -> list[Path]:
    """Vault 콘텐츠 디렉터리(16종, Milestone 27부터 `14 Tasks` 포함)만
    스캔한다 — `vault_root`가 저장소 root와 같아진 뒤(Milestone 26)
    `docs/`/`.claude/`/`.agents/` 등을 끌어들이지 않기 위함
    (`validation._iter_markdown_files`와 동일한 범위)."""
    files: list[Path] = []
    for name in VAULT_CONTENT_DIRECTORIES:
        directory = vault_root / name
        if directory.is_dir():
            files.extend(directory.rglob("*.md"))
    return sorted(files)


def find_references(vault_root: Path, title: str, *, exclude: Path | None = None) -> list[Path]:
    """`title` 문서를 `[[title]]`로 참조하는 다른 문서 목록을 찾는다."""
    referencing: list[Path] = []
    for path in _iter_vault_markdown_files(vault_root):
        if path == exclude:
            continue
        text = path.read_text(encoding="utf-8")
        if any(match.group(1).strip() == title for match in _BACKLINK_PATTERN.finditer(text)):
            referencing.append(path)
    return referencing


def _find_document_path(vault_root: Path, title: str) -> Path | None:
    matches = [p for p in _iter_vault_markdown_files(vault_root) if p.stem == title]
    return matches[0] if matches else None


def _rename_backlinks_in_text(text: str, old_title: str, new_title: str) -> str:
    pattern = re.compile(r"\[\[" + re.escape(old_title) + r"(?=[\]|#])")
    return pattern.sub(f"[[{new_title}", text)


@dataclass(frozen=True)
class RenameResult:
    old_path: Path
    new_path: Path
    updated_backlink_paths: tuple[Path, ...]


def rename_document(vault_root: Path, old_title: str, new_title: str) -> RenameResult:
    """`old_title` 문서 파일명을 `new_title`로 바꾸고, Vault 전체에서
    그 문서를 가리키는 `[[old_title]]`/`[[old_title|...]]`/
    `[[old_title#...]]`를 전부 `new_title` 기준으로 갱신한다."""
    old_path = _find_document_path(vault_root, old_title)
    if old_path is None:
        raise VaultDocumentNotFoundError(old_title)

    new_path = old_path.with_name(f"{new_title}{old_path.suffix}")
    if new_path.exists():
        raise VaultConflictError(f"이미 존재하는 문서입니다: {new_title}")

    old_path.rename(new_path)

    updated: list[Path] = []
    for path in _iter_vault_markdown_files(vault_root):
        text = path.read_text(encoding="utf-8")
        updated_text = _rename_backlinks_in_text(text, old_title, new_title)
        if updated_text != text:
            path.write_text(updated_text, encoding="utf-8")
            updated.append(path)

    return RenameResult(old_path=old_path, new_path=new_path, updated_backlink_paths=tuple(updated))


@dataclass(frozen=True)
class DeleteResult:
    deleted: bool
    path: Path
    referencing_paths: tuple[Path, ...]


def delete_document(vault_root: Path, title: str, *, force: bool = False) -> DeleteResult:
    """`title` 문서를 삭제한다. 다른 문서가 아직 참조 중이면(Orphan
    Backlink 방지) `force=True`가 아닌 한 삭제하지 않고 참조 목록을
    그대로 돌려준다(`deleted=False`)."""
    path = _find_document_path(vault_root, title)
    if path is None:
        raise VaultDocumentNotFoundError(title)

    referencing = find_references(vault_root, title, exclude=path)
    if referencing and not force:
        return DeleteResult(deleted=False, path=path, referencing_paths=tuple(referencing))

    path.unlink()
    return DeleteResult(deleted=True, path=path, referencing_paths=tuple(referencing))
