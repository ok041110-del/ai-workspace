"""Workspace Adapter Layer — Connector 공유 값 객체(Milestone 28
Architecture Freeze).

`WorkflowLink`는 원래 `workflow_task_link.py`에 정의돼 있었으나,
`workflow_agent_link.py`(Peer Connector)가 그것을 import하면서 두
Peer Connector가 서로를 참조하는 결과가 됐다 — ADR-0040("Peer
Connector끼리 서로 참조하지 않는다") 위반을 Architecture Freeze
과정에서 발견해 이 모듈로 옮겼다. 새 비즈니스 로직이나 새 Layer/
Interface를 추가한 것이 아니라, 이미 있던 순수 값 객체의 위치만
중립 지점으로 옮긴 것이다."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.domain.task import Task


@dataclass(frozen=True)
class WorkflowLink:
    """Vault task_id 하나와 그에 대응하는 Core Domain `Task` 하나를
    묶는 값 객체. `domain.Task`/`domain.Workflow`에는 필드를 추가하지
    않는다(Domain 오염 금지 원칙, Milestone 28-T04)."""

    vault_task_id: str
    domain_task: Task
