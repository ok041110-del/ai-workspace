"""Intelligence Layer — Project Snapshot Analyzer (ADR-0043, Milestone 29-T02).

`VaultAdapter.list_tasks()`/`AgentAdapter.list_active_agents()`가
이미 노출한 값만 읽어 집계한다 — 새 비즈니스 로직·쓰기 없음(Query
Layer Only, Read Only)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date as date_cls

from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter

#: Vault Task frontmatter `status` 값 중 "완료"로 집계하는 상태
#: (vault.task_lifecycle.TaskStatus.DONE/ARCHIVED와 동일한 문자열,
#: 이 모듈은 vault를 직접 import하지 않으므로 리터럴로 고정한다).
_COMPLETED_STATUSES = frozenset({"done", "archived"})


@dataclass(frozen=True)
class ProjectSnapshot:
    """Project 현재 상태의 집계 스냅샷. Vault Task 문서 전체(및 활성
    Agent 수)로부터 계산되며, 그 자체로는 아무 판단(Health/Risk)도
    내리지 않는다 — 판단은 M29-T03/T04의 책임이다."""

    generated_at: str
    total_tasks: int
    by_status: dict[str, int]
    by_milestone: dict[str, int]
    by_owner: dict[str, int]
    todo_count: int
    in_progress_count: int
    review_count: int
    done_count: int
    archived_count: int
    progress_ratio: float
    active_agent_count: int


@dataclass(frozen=True)
class TaskSnapshotEntry:
    """Snapshot 계산에 쓰인 Task 한 건(Risk/Recommendation이 Task 단위로
    다시 훑어야 할 때를 위해 함께 반환한다, M29-T03/T04에서 사용)."""

    task_id: str
    title: str
    status: str
    priority: str
    milestone: str
    owner: str
    updated: str


@dataclass(frozen=True)
class ProjectSnapshotWithTasks:
    snapshot: ProjectSnapshot
    tasks: list[TaskSnapshotEntry] = field(default_factory=list)


class ProjectSnapshotAnalyzer:
    """Project Snapshot을 계산하는 Read Only Analyzer. `VaultAdapter`
    (필수)/`AgentAdapter`(선택, 미주입 시 `active_agent_count`는 0)에만
    의존한다 — `vault`/Core Domain을 직접 참조하지 않는다."""

    def __init__(
        self,
        vault_adapter: VaultAdapter,
        agent_adapter: AgentAdapter | None = None,
    ) -> None:
        self._vault_adapter = vault_adapter
        self._agent_adapter = agent_adapter

    def analyze(
        self, *, include_archived: bool = True, today: str | None = None
    ) -> ProjectSnapshotWithTasks:
        """
        입력: include_archived(기본 True, `Archive/`의 완료 Task도 포함),
              today(고정 날짜 주입용, 기본값은 오늘 날짜)
        출력: `ProjectSnapshot` + 집계에 쓰인 Task 목록
              (`ProjectSnapshotWithTasks`)
        예외: 없음 — Task가 하나도 없으면 progress_ratio=0.0인 빈
              Snapshot을 반환한다.
        보장: side-effect 없음(read-only).
        """
        documents = self._vault_adapter.list_tasks(include_archived=include_archived)

        by_status: dict[str, int] = {}
        by_milestone: dict[str, int] = {}
        by_owner: dict[str, int] = {}
        for document in documents:
            by_status[document.status] = by_status.get(document.status, 0) + 1
            if document.milestone:
                by_milestone[document.milestone] = by_milestone.get(document.milestone, 0) + 1
            if document.owner:
                by_owner[document.owner] = by_owner.get(document.owner, 0) + 1

        total = len(documents)
        completed = sum(
            count for status, count in by_status.items() if status in _COMPLETED_STATUSES
        )
        progress_ratio = completed / total if total else 0.0
        active_agent_count = (
            len(self._agent_adapter.list_active_agents()) if self._agent_adapter is not None else 0
        )

        snapshot = ProjectSnapshot(
            generated_at=today or date_cls.today().isoformat(),
            total_tasks=total,
            by_status=by_status,
            by_milestone=by_milestone,
            by_owner=by_owner,
            todo_count=by_status.get("todo", 0),
            in_progress_count=by_status.get("in-progress", 0),
            review_count=by_status.get("review", 0),
            done_count=by_status.get("done", 0),
            archived_count=by_status.get("archived", 0),
            progress_ratio=progress_ratio,
            active_agent_count=active_agent_count,
        )
        tasks = [
            TaskSnapshotEntry(
                task_id=document.task_id,
                title=document.title,
                status=document.status,
                priority=document.priority,
                milestone=document.milestone,
                owner=document.owner,
                updated=document.updated,
            )
            for document in documents
        ]
        return ProjectSnapshotWithTasks(snapshot=snapshot, tasks=tasks)
