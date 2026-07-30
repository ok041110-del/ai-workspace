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
from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest
from ai_workspace.vault.task_lifecycle import TaskStatus, transition_task_status
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
