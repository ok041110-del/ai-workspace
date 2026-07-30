"""Intelligence Layer — Current Work Selector (ADR-0047, Milestone 33-T02).

`VaultAdapter.list_tasks()`(M29-T02, 기존 Adapter 메서드)가 이미
노출한 값(`status`/`updated`)만 읽는 순수 함수 계층이다 — 새로운
데이터 접근 경로도, 새로운 지표·점수도 만들지 않는다. "현재 작업"을
찾는 규칙 하나만 추가한다: 활성 상태(in-progress/review) Task 중
`updated`가 가장 최근인 1건. 동률이면 `task_id`가 더 큰 쪽을
결정적으로 고른다."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.integration.vault_adapter import TaskDocumentView

#: "현재 진행 중"으로 취급하는 Vault Task 상태(ADR-0043의 정체 판정과
#: 동일한 집합을 재사용 — 새 상태 분류를 만들지 않는다).
_ACTIVE_STATUSES = frozenset({"in-progress", "review"})


@dataclass(frozen=True)
class CurrentWork:
    """"현재 작업"으로 선택된 Task 한 건의 읽기 전용 뷰."""

    task_id: str
    title: str
    status: str
    milestone: str
    owner: str
    updated: str


class CurrentWorkSelector:
    """Vault Task 목록에서 "현재 작업" 1건(또는 없음)을 고르는 Rule
    기반 Selector. 새 판단 기준이 아니라, 이미 있는 `status`/`updated`
    값에서 하나를 선택하는 로직일 뿐이다."""

    def select(self, tasks: list[TaskDocumentView]) -> CurrentWork | None:
        """
        입력: `VaultAdapter.list_tasks()`가 반환한 Task 목록
        출력: 활성 상태(in-progress/review)이면서 archived가 아닌
              Task 중 `updated`가 가장 최근인 1건을 `CurrentWork`로
              반환. 동률이면 `task_id`가 더 큰 쪽. 활성 Task가 하나도
              없으면 `None`.
        예외: 없음
        보장: side-effect 없음(read-only), 입력 목록을 변경하지 않는다.
        """
        candidates = [
            task for task in tasks if task.status in _ACTIVE_STATUSES and not task.archived
        ]
        if not candidates:
            return None

        chosen = max(candidates, key=lambda task: (task.updated, task.task_id))
        return CurrentWork(
            task_id=chosen.task_id,
            title=chosen.title,
            status=chosen.status,
            milestone=chosen.milestone,
            owner=chosen.owner,
            updated=chosen.updated,
        )
