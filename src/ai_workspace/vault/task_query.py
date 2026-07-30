"""Milestone 29, T02: Project Snapshot Analyzer의 Vault 데이터 소스.

`14 Tasks/*.md`(및 `Archive/`)를 열거해 frontmatter를 읽기 전용으로
파싱한다. `task_lifecycle.py`/`task_sync.py`와 같은 성격의 "문서
생성 이후 관리" 계층이며 Core Domain을 전혀 모른다(ADR-0035). 이
모듈이 반환하는 값은 Intelligence Layer(`intelligence/`)가 직접
소비하지 않는다 — `integration.vault_adapter.VaultAdapter.
list_tasks()`를 통해서만 노출된다(ADR-0043)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_FRONTMATTER_BLOCK = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_TITLE_LINE = re.compile(r"^# (.+)$", re.MULTILINE)
_TASKS_DIR = "14 Tasks"
_ARCHIVE_DIR = "Archive"


@dataclass(frozen=True)
class TaskDocument:
    """`14 Tasks/{task_id}.md` 한 건의 읽기 전용 스냅샷. `task_id`는
    frontmatter가 아니라 파일명에서 얻는다(생성 시 frontmatter에
    기록하지 않는 필드, `vault.router`가 파일명 결정에만 사용)."""

    task_id: str
    title: str
    status: str
    priority: str
    milestone: str
    owner: str
    created: str
    updated: str
    archived: bool


def _read_frontmatter(text: str) -> dict[str, str]:
    match = _FRONTMATTER_BLOCK.match(text)
    if match is None:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).split("\n"):
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def _extract_title(text: str) -> str:
    match = _TITLE_LINE.search(text)
    return match.group(1).strip() if match else ""


def _parse_task_file(path: Path, *, archived: bool) -> TaskDocument | None:
    text = path.read_text(encoding="utf-8")
    fields = _read_frontmatter(text)
    if "status" not in fields:
        # frontmatter에 status가 없으면 Task 문서가 아니다(예: 14 Tasks/
        # README.md는 tags만 있고 status가 없어 자연스럽게 제외된다).
        return None
    return TaskDocument(
        task_id=path.stem,
        title=_extract_title(text),
        status=fields.get("status", ""),
        priority=fields.get("priority", ""),
        milestone=fields.get("milestone", ""),
        owner=fields.get("owner", ""),
        created=fields.get("created", ""),
        updated=fields.get("updated", ""),
        archived=archived,
    )


def list_task_documents(vault_root: Path, *, include_archived: bool = True) -> list[TaskDocument]:
    """`14 Tasks/*.md`(+ `include_archived=True`면 `Archive/`도 함께)를
    열거해 `TaskDocument` 목록으로 반환한다.

    입력: vault_root, include_archived(기본 True)
    출력: 발견된 Task 문서 목록(파일명 기준 정렬, 없으면 빈 리스트)
    예외: 없음 — `14 Tasks/`가 없으면 빈 리스트를 반환한다.
    보장: side-effect 없음(read-only). frontmatter에 `status`가 없는
          문서(예: README.md)는 결과에서 제외한다.
    """
    tasks_dir = vault_root / _TASKS_DIR
    if not tasks_dir.exists():
        return []

    documents: list[TaskDocument] = []
    for path in sorted(tasks_dir.glob("*.md")):
        document = _parse_task_file(path, archived=False)
        if document is not None:
            documents.append(document)

    if include_archived:
        archive_dir = tasks_dir / _ARCHIVE_DIR
        if archive_dir.exists():
            for path in sorted(archive_dir.glob("*.md")):
                document = _parse_task_file(path, archived=True)
                if document is not None:
                    documents.append(document)

    return documents
