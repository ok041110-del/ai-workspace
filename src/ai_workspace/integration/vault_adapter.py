"""Workspace Adapter Layer — Vault Adapter (ADR-0039, Milestone 28-T03).

`vault/`를 import하는 Integration Layer의 유일한 구성원이다. 호출자
(Workflow/Agent Adapter, 향후 Conversation Layer)는 이 클래스를 통해서만
Vault Task 문서를 다루고, `vault.task_lifecycle.TaskStatus` 같은 vault
내부 타입을 직접 import하지 않는다 — 이 Adapter의 공개 메서드는 문자열/
`bool`/`Path`/이 파일 안에서 정의한 dataclass만 주고받는다."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from ai_workspace.vault.engine import VaultSaveEngine
from ai_workspace.vault.intelligence_report import write_project_intelligence_report
from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest
from ai_workspace.vault.task_lifecycle import TaskStatus, transition_task_status
from ai_workspace.vault.task_query import list_task_documents
from ai_workspace.vault.task_sync import transition_and_sync


@dataclass(frozen=True)
class TaskTransitionOutcome:
    task_id: str
    old_status: str
    new_status: str
    archived: bool
    daily_updated: bool | None
    milestone_updated: bool | None
    decision_updated: bool | None


@dataclass(frozen=True)
class TaskDocumentView:
    """`VaultAdapter.list_tasks()`가 반환하는 Task 문서 하나의 읽기 전용
    뷰(ADR-0043, Milestone 29-T02). `vault.task_query.TaskDocument`를
    감싸기만 한다 — 호출자는 `vault` 내부 타입을 직접 import하지 않는다
    (다른 `VaultAdapter` 공개 메서드와 동일한 원칙)."""

    task_id: str
    title: str
    status: str
    priority: str
    milestone: str
    owner: str
    created: str
    updated: str
    archived: bool


class VaultAdapter:
    """Vault Task 문서 생성/상태 전이를 Core Domain에 노출하는 Adapter.
    `vault_root` 하나로 바인딩되는 얇은 래퍼이며, 자체 상태를 갖지
    않는다(연결·변환·위임만, ADR-0039)."""

    def __init__(self, vault_root: Path) -> None:
        self._vault_root = vault_root
        self._save_engine = VaultSaveEngine(vault_root)

    def create_task(
        self,
        task_id: str,
        title: str,
        *,
        status: str,
        priority: str,
        milestone: str,
        owner: str,
        created: str,
        updated: str,
        summary: str = "",
        related_docs: Sequence[str] = (),
        extra_fields: Mapping[str, str] | None = None,
    ) -> bool:
        """`14 Tasks/{task_id}.md`를 만든다. 이미 존재하면 아무것도 하지
        않고 `False`를 돌려준다(`VaultWriter.create_file()`과 동일한
        계약)."""
        fields = {
            "task_id": task_id,
            "status": status,
            "priority": priority,
            "milestone": milestone,
            "owner": owner,
            "created": created,
            "updated": updated,
            **(extra_fields or {}),
        }
        request = VaultDocumentRequest(
            kind=VaultDocumentKind.TASK,
            title=title,
            summary=summary,
            related_docs=tuple(related_docs),
            fields=fields,
        )
        return self._save_engine.save(request)

    def transition_task(
        self,
        task_id: str,
        new_status: str,
        *,
        today: str | None = None,
        sync_related_documents: bool = True,
    ) -> TaskTransitionOutcome:
        """Task 상태를 전이한다. `sync_related_documents=True`(기본값)면
        Daily Note/Milestones Index/Decisions Index까지 함께 갱신한다
        (`vault.task_sync.transition_and_sync()`), `False`면 Task 문서
        상태 전이만 한다(`vault.task_lifecycle.transition_task_status()`).
        """
        status = TaskStatus(new_status)
        if sync_related_documents:
            sync_result = transition_and_sync(self._vault_root, task_id, status, today=today)
            return TaskTransitionOutcome(
                task_id=task_id,
                old_status=sync_result.old_status,
                new_status=sync_result.new_status,
                archived=status is TaskStatus.ARCHIVED,
                daily_updated=sync_result.daily_updated,
                milestone_updated=sync_result.milestone_updated,
                decision_updated=sync_result.decision_updated,
            )

        transition_result = transition_task_status(self._vault_root, task_id, status, today=today)
        return TaskTransitionOutcome(
            task_id=task_id,
            old_status=transition_result.old_status.value,
            new_status=transition_result.new_status.value,
            archived=transition_result.archived,
            daily_updated=None,
            milestone_updated=None,
            decision_updated=None,
        )

    def list_tasks(self, *, include_archived: bool = True) -> list[TaskDocumentView]:
        """`14 Tasks/*.md`(+ `include_archived=True`면 `Archive/`도)를
        열거해 `TaskDocumentView` 목록으로 반환한다(ADR-0043, Milestone
        29-T02) — Intelligence Layer가 Project 단위 Task 전체를 조회하는
        유일한 통로다. side-effect 없음(read-only)."""
        documents = list_task_documents(self._vault_root, include_archived=include_archived)
        return [
            TaskDocumentView(
                task_id=doc.task_id,
                title=doc.title,
                status=doc.status,
                priority=doc.priority,
                milestone=doc.milestone,
                owner=doc.owner,
                created=doc.created,
                updated=doc.updated,
                archived=doc.archived,
            )
            for doc in documents
        ]

    def publish_intelligence_report(self, markdown: str) -> Path:
        """`intelligence/report.py`가 렌더링한 Markdown을 `15 Project
        Intelligence/Project Intelligence.md`에 덮어쓴다(ADR-0043,
        Milestone 29-T05). 렌더링 로직은 갖지 않는다 — 이미 만들어진
        문자열을 그대로 받아 쓰기만 한다(연결·위임만, ADR-0039)."""
        return write_project_intelligence_report(self._vault_root, markdown)
