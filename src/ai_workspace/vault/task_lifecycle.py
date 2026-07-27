"""Milestone 28, T01: Task Lifecycle.

`render_task_file()`(Milestone 27)이 만든 Task 문서(`14 Tasks/
{task_id}.md`)는 지금까지 생성 후에는 상태를 바꿀 방법이 없었다. 이
모듈은 그 이후 Lifecycle(Status Transition, `updated` 자동 갱신,
Archive 처리)을 담당한다 — `sync.py`(Rename/Delete)와 같은 성격의
"문서 생성 이후 관리" 계층이며, Core Domain을 알지 못한다(ADR-0035).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date as date_cls
from enum import Enum
from pathlib import Path

from ai_workspace.vault.atomic import atomic_write_text

_FRONTMATTER_BLOCK = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


class TaskStatus(Enum):
    """M25 요청 Task Lifecycle의 5개 상태."""

    TODO = "todo"
    IN_PROGRESS = "in-progress"
    REVIEW = "review"
    DONE = "done"
    ARCHIVED = "archived"


#: 허용된 상태 전이(Status Transition). `IN_PROGRESS`↔`TODO`/`REVIEW`는
#: 되돌아갈 수 있지만(작업 재개/반려), `DONE`은 `ARCHIVED`로만 전이하고
#: `ARCHIVED`는 종단 상태다 — Task 완료 후 재오픈은 새 Task로 만든다.
_ALLOWED_TRANSITIONS: dict[TaskStatus, frozenset[TaskStatus]] = {
    TaskStatus.TODO: frozenset({TaskStatus.IN_PROGRESS}),
    TaskStatus.IN_PROGRESS: frozenset({TaskStatus.REVIEW, TaskStatus.TODO}),
    TaskStatus.REVIEW: frozenset({TaskStatus.DONE, TaskStatus.IN_PROGRESS}),
    TaskStatus.DONE: frozenset({TaskStatus.ARCHIVED}),
    TaskStatus.ARCHIVED: frozenset(),
}


class TaskNotFoundError(FileNotFoundError):
    """`task_id`에 해당하는 Task 문서를 찾지 못했을 때 발생한다."""


class TaskFrontmatterError(ValueError):
    """Task 문서에 frontmatter 또는 `status` 필드가 없을 때 발생한다."""


class InvalidTaskTransitionError(ValueError):
    """허용되지 않은 Status Transition을 요청했을 때 발생한다."""


@dataclass(frozen=True)
class TaskTransitionResult:
    path: Path
    old_status: TaskStatus
    new_status: TaskStatus
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


def _replace_frontmatter_field(text: str, key: str, value: str) -> str:
    """frontmatter 블록(`---`~`---`) 안의 `key: ...` 줄만 치환한다 — 본문은
    건드리지 않는다. `key`가 없으면 블록 끝에 추가한다."""
    match = _FRONTMATTER_BLOCK.match(text)
    if match is None:
        raise TaskFrontmatterError("frontmatter가 없는 Task 문서입니다")

    block = match.group(1)
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
    if pattern.search(block) is None:
        new_block = f"{block}\n{key}: {value}"
    else:
        new_block = pattern.sub(f"{key}: {value}", block, count=1)

    start, end = match.start(1), match.end(1)
    return text[:start] + new_block + text[end:]


def transition_task_status(
    vault_root: Path,
    task_id: str,
    new_status: TaskStatus,
    *,
    today: str | None = None,
) -> TaskTransitionResult:
    """`14 Tasks/{task_id}.md`의 상태를 `new_status`로 전이한다.

    - 현재 상태를 frontmatter `status`에서 읽어 `_ALLOWED_TRANSITIONS`로
      검증한다. 허용되지 않은 전이는 `InvalidTaskTransitionError`.
    - `status`/`updated`(오늘 날짜, `today`로 고정 가능) frontmatter를
      갱신한다.
    - `new_status`가 `ARCHIVED`면 문서를 `14 Tasks/Archive/{task_id}.md`
      로 옮긴다 — 파일명(=Wikilink 대상)은 그대로라 Backlink는 깨지지
      않는다.
    """
    path = vault_root / "14 Tasks" / f"{task_id}.md"
    if not path.exists():
        raise TaskNotFoundError(task_id)

    text = path.read_text(encoding="utf-8")
    current_raw = _read_frontmatter(text).get("status")
    if current_raw is None:
        raise TaskFrontmatterError(f"{task_id} 문서에 status frontmatter가 없습니다")

    try:
        current_status = TaskStatus(current_raw)
    except ValueError as exc:
        raise TaskFrontmatterError(f"알 수 없는 status 값입니다: {current_raw}") from exc

    if new_status not in _ALLOWED_TRANSITIONS[current_status]:
        raise InvalidTaskTransitionError(
            f"{current_status.value} → {new_status.value} 전이는 허용되지 않습니다"
        )

    day = today or date_cls.today().isoformat()
    updated_text = _replace_frontmatter_field(text, "status", new_status.value)
    updated_text = _replace_frontmatter_field(updated_text, "updated", day)

    archived = new_status is TaskStatus.ARCHIVED
    if archived:
        target_path = vault_root / "14 Tasks" / "Archive" / f"{task_id}.md"
        atomic_write_text(target_path, updated_text)
        path.unlink()
    else:
        target_path = path
        atomic_write_text(target_path, updated_text)

    return TaskTransitionResult(
        path=target_path, old_status=current_status, new_status=new_status, archived=archived
    )
