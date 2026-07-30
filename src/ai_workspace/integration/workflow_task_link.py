"""Workspace Adapter Layer — Workflow↔Task Connector (Milestone 28-T04).

Vault Task 문서와 Core Domain `Workflow`/`Task`를 잇는다. Adapter(외부
시스템 하나와의 연결)와 구분되는 **Connector**(여러 Adapter를 조합하는
유스케이스 오케스트레이션, Milestone 28-T05/ADR-0040에서 명명)다 —
`VaultAdapter`/`WorkflowAdapter`를 조합만 하고 자체 상태 전이 규칙은
갖지 않는다. 사용자가 T04 승인 시 제시한 4개 원칙을 그대로 따른다:

1. Workflow ↔ Vault는 직접 의존하지 않는다 — 이 파일은 `vault`를
   전혀 import하지 않고, `VaultAdapter`/`WorkflowAdapter`(둘 다
   Integration Layer 안)를 통해서만 각 쪽에 접근한다.
2. 모든 연결은 Integration Layer를 통해서만 이뤄진다 — 이 파일
   자체가 `integration/` 패키지 안에 있고, `WorkflowTaskLink` 밖의
   어떤 모듈도 두 Adapter를 동시에 조합하지 않는다.
3. Domain 객체는 Markdown/Vault 표현으로 오염되지 않는다 — `Task`/
   `Workflow`에 새 필드를 추가하지 않는다. Vault task_id와 Core
   Domain task_id는 서로 다른 문자열일 수 있으므로(Vault는
   `T28-04` 같은 사람이 붙인 ID, Core Domain은 `TaskEngine`이
   발급하는 `task-N`), 그 매핑은 `Task`/`Workflow`가 아니라
   `models.WorkflowLink` 값 객체가 별도로 들고 있는다(Milestone 28
   Architecture Freeze에서 `workflow_agent_link.py`도 이 값 객체가
   필요하다는 게 드러나, Peer Connector끼리 서로 참조하지 않기
   위해 `workflow_task_link.py`가 아닌 중립 모듈 `models.py`로
   옮겼다). 기존 `Task.workflow_id` 필드(도메인이 이미 갖고 있던
   Workflow 소속 정보)는 그대로 채워 재사용한다 — 새 필드가
   아니다.
4. Adapter는 연결·변환·위임만 수행한다 — 아래 클래스는 ID 변환과
   호출 순서 조합만 하고, Task/Workflow 상태 전이 규칙 자체는
   여전히 `TaskEngine`(Core Domain)과 `vault.task_lifecycle`(Vault)
   에 위임한다. *언제* 전이를 트리거할지(비즈니스 판단)는 호출자
   (향후 Conversation Layer, M28-T06)의 몫이다."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.integration.models import WorkflowLink
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.integration.workflow_adapter import WorkflowAdapter

#: Core Domain `TaskStatus` -> Vault Task Lifecycle 상태 문자열
#: (`vault.task_lifecycle.TaskStatus`). `BLOCKED`/`CANCELLED`는 Vault
#: Task Lifecycle(Todo/In Progress/Review/Done/Archived, Milestone
#: 28-T01)에 대응하는 상태가 없어 의도적으로 제외한다 — 억지로
#: 끼워 맞추지 않는다.
_DOMAIN_TO_VAULT_STATUS: dict[TaskStatus, str] = {
    TaskStatus.TODO: "todo",
    TaskStatus.IN_PROGRESS: "in-progress",
    TaskStatus.REVIEW: "review",
    TaskStatus.DONE: "done",
}


class WorkflowTaskLink:
    """Workflow 생성·상태 변경·Task 상태 반영을 잇는 Integration Layer
    구성 요소. `VaultAdapter`/`WorkflowAdapter`를 조합만 한다."""

    def __init__(self, vault_adapter: VaultAdapter, workflow_adapter: WorkflowAdapter) -> None:
        self._vault = vault_adapter
        self._workflow = workflow_adapter

    def create_workflow_from_vault_tasks(
        self,
        workflow_id: str,
        mission_id: str,
        project_id: str,
        vault_tasks: Sequence[tuple[str, str]],
        dependencies: Mapping[str, set[str]] | None = None,
    ) -> tuple[Workflow, list[WorkflowLink]]:
        """`vault_tasks`(`(vault_task_id, title)` 목록, 이미 Vault에
        존재하는 Task 문서들)마다 Core Domain `Task`를 새로 만들어
        `workflow_id`를 채우고, 그 Task들로 `Workflow`를 만든다.
        `dependencies`는 Vault task_id 기준으로 받아 Core Domain
        task_id로 변환한다(호출자는 Core Domain이 나중에 발급하는
        ID를 몰라도 된다)."""
        links: list[WorkflowLink] = []
        domain_id_by_vault_id: dict[str, str] = {}
        for vault_task_id, title in vault_tasks:
            domain_task = self._workflow.create_task(project_id, title)
            domain_task.workflow_id = workflow_id
            links.append(WorkflowLink(vault_task_id=vault_task_id, domain_task=domain_task))
            domain_id_by_vault_id[vault_task_id] = domain_task.task_id

        domain_task_ids = [link.domain_task.task_id for link in links]
        domain_dependencies = {
            domain_id_by_vault_id[task_id]: {domain_id_by_vault_id[dep] for dep in deps}
            for task_id, deps in (dependencies or {}).items()
        }
        workflow = self._workflow.create_workflow(
            workflow_id, mission_id, domain_task_ids, domain_dependencies
        )
        return workflow, links

    def plan(self, workflow: Workflow) -> list[str]:
        return self._workflow.plan(workflow)

    def transition_and_reflect(
        self, link: WorkflowLink, new_status: TaskStatus, *, today: str | None = None
    ) -> Task:
        """Core Domain `Task`를 `new_status`로 전이하고, Vault Task
        Lifecycle에 대응하는 상태가 있으면 `VaultAdapter`로 Vault
        문서에도 반영한다("Workflow 상태 변경 → Task 상태 반영")."""
        transitioned = self._workflow.transition_task(link.domain_task, new_status)
        vault_status = _DOMAIN_TO_VAULT_STATUS.get(new_status)
        if vault_status is not None:
            self._vault.transition_task(link.vault_task_id, vault_status, today=today)
        return transitioned

    def is_workflow_complete(self, links: Sequence[WorkflowLink]) -> bool:
        """`links`에 속한 모든 Core Domain Task가 `DONE`인지 확인한다
        ("Workflow 종료") — `Workflow` 자체는 상태 필드를 갖지 않으므로
        (원칙 3, Domain 오염 금지) 여기서 파생 값으로 계산한다."""
        return all(
            self._workflow.get_task(link.domain_task.task_id).status is TaskStatus.DONE
            for link in links
        )

    def get_task_status(self, link: WorkflowLink) -> TaskStatus:
        """`link`가 가리키는 Core Domain `Task`의 현재 상태를 조회한다
        (Milestone 28-T06) — `WorkflowAdapter.get_task()`에 그대로
        위임하는 조회 전용 메서드. `ConversationConnector`가 `WorkflowAdapter`
        를 직접 참조하지 않고도 Task별 상태를 모을 수 있게 한다."""
        return self._workflow.get_task(link.domain_task.task_id).status
