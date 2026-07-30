"""Workspace Adapter Layer — Conversation Connector (Milestone 28-T06, ADR-0041).

Conversation Layer(사용자 입력 해석/요청 라우팅/결과 조합만 담당 —
자연어 이해 자체는 AI 고유 역할이라 코드로 만들지 않는다, `EXECUTION_PROFILE`
의 M23-T06 Execution Engine 절과 같은 전제)가 Task/Workflow/Agent
관련 요청을 처리하기 위해 거치는 **유일한 진입점**이다.

**새 비즈니스 로직을 추가하지 않는다**(사용자 T06 요청): 이 파일의
모든 메서드는 기존 `VaultAdapter`(T03)/`WorkflowTaskLink`(T04)/
`WorkflowAgentLink`(T05) 호출을 그대로 조합·순서 배열하거나, 그
결과를 dataclass로 묶어 돌려줄 뿐이다. 상태 전이 규칙, Agent 선택
기준, Task 분해 판단 등은 전혀 만들지 않는다 — 전부 기존 Core
Domain Engine(`TaskEngine`/`WorkflowEngine`/`AgentManager`/
`AgentScheduler`)과 `vault.task_lifecycle`에 이미 있는 로직에
위임된 채로 남는다.

**Boundary**(사용자 T06 요청, ADR-0041):

- Conversation Layer(이 Connector의 호출자)는 `vault`/Core Domain
  Engine(`WorkflowEngine`/`TaskEngine`)/`AgentManager`를 직접
  참조하지 않는다 — 이 Connector를 통해서만 접근한다.
- 이 Connector 자신도 `vault`, `WorkflowEngine`/`TaskEngine`,
  `AgentManager`(및 그 구체 구현)를 직접 import하지 않는다 —
  `VaultAdapter`/`WorkflowTaskLink`/`WorkflowAgentLink`만 조합한다.
  `tests/integration_layer/test_conversation_connector_boundary.py`
  가 이를 `ast`로 강제한다. Domain 값 타입(`TaskStatus`/
  `AgentCapability`/`Task`/`Workflow`/`Agent`)은 메서드 시그니처에
  그대로 쓴다 — `WorkflowAdapter`/`AgentAdapter`(T03)가 이미
  Integration Layer 밖으로 노출해 온 값이라 새로운 경계 위반이
  아니다(WorkflowTaskLink/WorkflowAgentLink와 동일한 전제).
- **ADR-0040 "Connector끼리 서로 참조하지 않는다" 원칙의 예외**:
  이 Connector는 다른 두 Connector(`WorkflowTaskLink`/
  `WorkflowAgentLink`)를 직접 조합한다 — Peer Connector들이 서로
  참조하지 않는다는 ADR-0040 규칙에 대한 명시적 예외다. Conversation
  Connector는 여러 유스케이스(Task 생성, Workflow 연결, Agent 배정)
  를 "라우팅·조합"하는 것 자체가 존재 이유인 **Orchestrating
  Connector**이기 때문이다(ADR-0041에 근거 기록)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ai_workspace.domain.agent import AgentCapability
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.integration.models import WorkflowLink
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.integration.workflow_agent_link import AgentAssignment, WorkflowAgentLink
from ai_workspace.integration.workflow_task_link import WorkflowTaskLink


@dataclass(frozen=True)
class ConversationTaskRequest:
    """Conversation Layer가 "Task를 만들고 Workflow에 넣고 Agent를
    배정해 달라"고 요청할 때 넘기는 구조화 입력. 자연어를 이 구조로
    바꾸는 것은 Conversation Layer의 몫이다 — 이 Connector는 이미
    해석된 값만 받는다(ADR-0035 결정 3과 같은 전제: 자연어 생성이
    아니라 고정 스키마 값 전달)."""

    vault_task_id: str
    title: str
    status: str
    priority: str
    milestone: str
    owner: str
    created: str
    updated: str
    workflow_id: str
    mission_id: str
    project_id: str
    capability: AgentCapability
    summary: str = ""
    related_docs: Sequence[str] = ()


@dataclass(frozen=True)
class ConversationTaskResult:
    """`ConversationTaskRequest` 처리 결과 — `VaultAdapter`/
    `WorkflowTaskLink`/`WorkflowAgentLink` 호출 결과를 그대로 묶은
    것뿐, 새로 계산한 값이 없다."""

    vault_task_created: bool
    workflow: Workflow
    link: WorkflowLink
    assignment: AgentAssignment


@dataclass(frozen=True)
class ConversationStatusReport:
    """Workflow 하나에 속한 Task들의 현재 상태 요약("결과 조합") —
    Task별 상태 + 전체 완료 여부. 둘 다 기존 `WorkflowTaskLink`
    메서드가 이미 계산해 두는 값을 모은 것뿐이다."""

    task_status_by_vault_id: dict[str, TaskStatus]
    complete: bool


class ConversationConnector:
    """Conversation Layer가 Task/Workflow/Agent 관련 요청을 처리하는
    유일한 진입점(Orchestrating Connector). 기존 `VaultAdapter`/
    `WorkflowTaskLink`/`WorkflowAgentLink`를 조합만 한다."""

    def __init__(
        self,
        vault_adapter: VaultAdapter,
        workflow_task_link: WorkflowTaskLink,
        workflow_agent_link: WorkflowAgentLink,
    ) -> None:
        self._vault = vault_adapter
        self._task_link = workflow_task_link
        self._agent_link = workflow_agent_link

    def handle_task_request(self, request: ConversationTaskRequest) -> ConversationTaskResult:
        """"Task 생성 → Workflow 생성 → Agent Assignment → Vault
        업데이트" 흐름 하나를 그대로 실행한다(M25 요청 원문의 예시
        흐름 — "로그인 기능 만들어줘" → Task → Workflow → Agent →
        Vault). 각 단계는 기존 Adapter/Connector 호출일 뿐, 여기서
        새로 판단하는 것은 없다(순서 배열과 값 전달만)."""
        vault_task_created = self._vault.create_task(
            request.vault_task_id,
            request.title,
            status=request.status,
            priority=request.priority,
            milestone=request.milestone,
            owner=request.owner,
            created=request.created,
            updated=request.updated,
            summary=request.summary,
            related_docs=request.related_docs,
        )
        workflow, links = self._task_link.create_workflow_from_vault_tasks(
            request.workflow_id,
            request.mission_id,
            request.project_id,
            [(request.vault_task_id, request.title)],
        )
        assignment = self._agent_link.assign_agent(links[0], request.capability)
        return ConversationTaskResult(
            vault_task_created=vault_task_created,
            workflow=workflow,
            link=links[0],
            assignment=assignment,
        )

    def advance_task(
        self, link: WorkflowLink, new_status: TaskStatus, *, today: str | None = None
    ) -> Task:
        """Task 상태를 전이하고 Vault에도 반영한다 — `WorkflowTaskLink.
        transition_and_reflect()`를 그대로 호출한다(요청 라우팅)."""
        return self._task_link.transition_and_reflect(link, new_status, today=today)

    def report_status(self, links: Sequence[WorkflowLink]) -> ConversationStatusReport:
        """`links`(하나의 Workflow에 속한 Task들)의 현재 상태를 모은다
        ("결과 조합") — 전이 로직이나 완료 판정 알고리즘을 새로
        만들지 않고 `WorkflowTaskLink.get_task_status()`/
        `is_workflow_complete()`의 결과를 그대로 묶는다."""
        task_status_by_vault_id = {
            link.vault_task_id: self._task_link.get_task_status(link) for link in links
        }
        return ConversationStatusReport(
            task_status_by_vault_id=task_status_by_vault_id,
            complete=self._task_link.is_workflow_complete(links),
        )
