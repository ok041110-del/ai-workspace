"""Execution Layer — Task Lifecycle Transitioner (ADR-0051, Milestone 37-T02).

M36 Execution 결과를 이미 존재하는 Task 상태 전이 기계
(`vault/task_lifecycle.py`의 `_ALLOWED_TRANSITIONS`, M28)에 연결
한다 — 새 상태·새 전이 규칙을 만들지 않는다. 문자열 status 값만
주고받는다(`VaultAdapter.transition_task()`가 이미 문자열 인터페이스
이므로, 이 파일은 `vault.task_lifecycle.TaskStatus`를 직접 import
하지 않는다 — §8 규칙 18/19 경계를 넘지 않기 위함)."""

from __future__ import annotations

_TODO = "todo"
_IN_PROGRESS = "in-progress"
_REVIEW = "review"


class TaskLifecycleTransitioner:
    """현재 상태를 먼저 확인하고, 예상과 다르면 아무 것도 하지 않는
    방어적 Rule. Gate 승인 시점과 실제 전이 시점 사이에 Task 상태가
    이미 바뀌어 있어도 예외를 던지지 않고 조용히 건너뛴다."""

    def decide_start(self, current_status: str) -> str | None:
        """
        입력: 실행 시작 직전 Task의 현재 status
        출력: `current_status`가 `todo`면 `"in-progress"`, 아니면
              `None`(전이하지 않음)
        예외: 없음
        보장: side-effect 없음(read-only), 실행하지 않는다.
        """
        if current_status == _TODO:
            return _IN_PROGRESS
        return None

    def decide_completion(self, current_status: str, *, success: bool) -> str | None:
        """
        입력: 실행 완료 직전 Task의 현재 status, success(실행 성공
              여부)
        출력: `current_status`가 `in-progress`면 성공 시 `"review"`,
              실패 시 `"todo"`. 그 외 상태면 `None`(전이하지 않음)
        예외: 없음
        보장: side-effect 없음(read-only), 실행하지 않는다.
        """
        if current_status != _IN_PROGRESS:
            return None
        return _REVIEW if success else _TODO
