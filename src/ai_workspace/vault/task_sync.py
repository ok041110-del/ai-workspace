"""Milestone 28, T02: Automatic Document Synchronization.

Task 상태가 바뀔 때(`task_lifecycle.transition_task_status()`) 관련
Vault 문서를 자동으로 갱신한다. `docs/ROADMAP.md`는 GitHub 원문이라
Vault가 직접 쓰지 않는다(`AI_RULES`의 "GitHub 문서를 수정하지 않는다")
— 그 대신 Vault 쪽 대응 문서인 `11 Milestones/Milestones Index.md`에
Task 변경 로그를 남기는 것으로 "Roadmap/Milestone 갱신"을 구현한다.

기존 파일 조작 원칙(atomic write, 섹션 단위 upsert, 필요할 때만
쓰기)을 그대로 따르되, `writer.py`의 `upsert_section()`은 섹션
"전체 치환"이라 누적되는 로그에는 맞지 않아 이 모듈만의 "섹션 안
불릿 라인 추가(중복 시 무변경)" 전략(`_upsert_bullet_section()`)을
쓴다."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date as date_cls
from pathlib import Path

from ai_workspace.vault.atomic import atomic_write_text
from ai_workspace.vault.markdown_generator import render_daily_file
from ai_workspace.vault.task_lifecycle import TaskStatus, transition_task_status

_RELATED_DOCS_HEADING = "## 관련 문서"
_BACKLINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")

#: 새 상태가 될 때 Daily Note의 어느 섹션에 기록할지. `ARCHIVED`는
#: 이미 `DONE` 시점에 "완료"로 기록됐으므로 Daily Note를 다시
#: 건드리지 않는다(Milestones Index Task 변경 로그에는 계속 남는다).
_DAILY_SECTION_BY_STATUS: dict[TaskStatus, str] = {
    TaskStatus.TODO: "오늘 작업",
    TaskStatus.IN_PROGRESS: "진행중",
    TaskStatus.REVIEW: "진행중",
    TaskStatus.DONE: "완료",
}


@dataclass(frozen=True)
class TaskSyncResult:
    daily_path: Path
    daily_updated: bool
    milestone_updated: bool
    decision_updated: bool


def _section_bounds(lines: list[str], heading_line: str) -> tuple[int, int] | None:
    start = next((i for i, line in enumerate(lines) if line == heading_line), None)
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def _section_body(text: str, heading: str) -> str | None:
    lines = text.split("\n")
    bounds = _section_bounds(lines, f"## {heading}")
    if bounds is None:
        return None
    start, end = bounds
    return "\n".join(lines[start + 1 : end]).strip()


def _upsert_bullet_section(text: str, heading: str, line: str) -> str:
    """`## {heading}` 섹션에 `line`이 없으면 추가한다(있으면 무변경).
    섹션이 아예 없으면 "## 관련 문서" 앞에 새로 만든다(없으면 파일
    끝에). 섹션이 빈 placeholder(`-`)만 갖고 있으면 그 자리를
    대체한다."""
    lines = text.split("\n")
    heading_line = f"## {heading}"
    bounds = _section_bounds(lines, heading_line)

    if bounds is None:
        insert_at = next(
            (i for i, item in enumerate(lines) if item == _RELATED_DOCS_HEADING), len(lines)
        )
        new_section = [heading_line, "", line, ""]
        return "\n".join(lines[:insert_at] + new_section + lines[insert_at:])

    start, end = bounds
    body = [item for item in lines[start + 1 : end] if item.strip() != ""]
    if line in body:
        return text
    new_body = [line] if body == ["-"] else [*body, line]
    new_section = [heading_line, "", *new_body, ""]
    return "\n".join(lines[:start] + new_section + lines[end:])


def sync_task_change(
    vault_root: Path,
    task_id: str,
    old_status: TaskStatus,
    new_status: TaskStatus,
    *,
    date: str | None = None,
) -> TaskSyncResult:
    """`task_id`의 상태 변경(`old_status`→`new_status`)을 관련 Vault
    문서에 반영한다. 각 문서는 실제로 내용이 바뀔 때만 쓴다."""
    day = date or date_cls.today().isoformat()

    daily_path = vault_root / "13 Daily" / f"{day}.md"
    if not daily_path.exists():
        atomic_write_text(daily_path, render_daily_file(day))
    daily_text = daily_path.read_text(encoding="utf-8")
    daily_updated = False
    daily_section = _DAILY_SECTION_BY_STATUS.get(new_status)
    if daily_section is not None:
        line = f"- [[{task_id}]] {old_status.value} → {new_status.value}"
        new_daily_text = _upsert_bullet_section(daily_text, daily_section, line)
        if new_daily_text != daily_text:
            atomic_write_text(daily_path, new_daily_text)
            daily_updated = True

    milestone_path = vault_root / "11 Milestones" / "Milestones Index.md"
    milestone_updated = False
    if milestone_path.exists():
        milestone_text = milestone_path.read_text(encoding="utf-8")
        log_line = f"- {day} [[{task_id}]] {old_status.value} → {new_status.value}"
        new_milestone_text = _upsert_bullet_section(milestone_text, "Task 변경 로그", log_line)
        if new_milestone_text != milestone_text:
            atomic_write_text(milestone_path, new_milestone_text)
            milestone_updated = True

    decision_updated = False
    task_path = vault_root / "14 Tasks" / f"{task_id}.md"
    if not task_path.exists():
        task_path = vault_root / "14 Tasks" / "Archive" / f"{task_id}.md"
    decisions_index = vault_root / "12 Decisions" / "Decisions Index.md"
    if task_path.exists() and decisions_index.exists():
        decision_body = _section_body(task_path.read_text(encoding="utf-8"), "Decision") or ""
        decision_titles = [m.group(1).strip() for m in _BACKLINK_PATTERN.finditer(decision_body)]
        if decision_titles:
            decisions_text = decisions_index.read_text(encoding="utf-8")
            for title in decision_titles:
                line = f"- [[{task_id}]] → [[{title}]]"
                new_decisions_text = _upsert_bullet_section(decisions_text, "Task 연결", line)
                if new_decisions_text != decisions_text:
                    decisions_text = new_decisions_text
                    decision_updated = True
            if decision_updated:
                atomic_write_text(decisions_index, decisions_text)

    return TaskSyncResult(
        daily_path=daily_path,
        daily_updated=daily_updated,
        milestone_updated=milestone_updated,
        decision_updated=decision_updated,
    )


def transition_and_sync(
    vault_root: Path,
    task_id: str,
    new_status: TaskStatus,
    *,
    today: str | None = None,
) -> TaskSyncResult:
    """`transition_task_status()`로 Task 문서를 전이한 뒤, 그 결과를
    `sync_task_change()`로 관련 문서에 곧바로 반영하는 편의 함수 —
    "Task 변경 시 자동 문서 갱신"의 단일 진입점."""
    result = transition_task_status(vault_root, task_id, new_status, today=today)
    return sync_task_change(
        vault_root, task_id, result.old_status, result.new_status, date=today
    )
