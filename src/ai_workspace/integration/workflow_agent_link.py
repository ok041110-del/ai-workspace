"""Workspace Adapter Layer — Workflow↔Agent Connector (Milestone 28-T05).

**Adapter vs Connector**(사용자 T05 승인 방향, ADR-0040): Adapter
(`vault_adapter.py`/`workflow_adapter.py`/`agent_adapter.py`)는 외부
시스템 하나와의 연결만 담당한다. Connector(`workflow_task_link.py`의
`WorkflowTaskLink`, 이 파일의 `WorkflowAgentLink`)는 여러 Adapter를
조합해 유스케이스 하나를 오케스트레이션한다. 이 구분에 따라 Agent
배정 책임을 `WorkflowTaskLink`(T04)에 얹지 않고 별도 Connector로
분리했다 — Connector 하나는 유스케이스 하나만 책임진다.

이 Connector는 `AgentAdapter`/`WorkflowAdapter`만 조합한다(Vault는
모른다 — Task 상태를 Vault에 반영하는 것은 이미 `WorkflowTaskLink`
의 책임이고, 여기서 중복하지 않는다). `domain.Task`/`domain.Agent`
에는 필드를 추가하지 않는다(Domain 오염 금지, T04와 동일 원칙) —
Task↔Agent 배정 관계는 이 Connector가 별도로 든다."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ai_workspace.domain.agent import Agent, AgentCapability, AgentStatus
from ai_workspace.domain.task import TaskStatus
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.models import WorkflowLink
from ai_workspace.integration.workflow_adapter import WorkflowAdapter


class NoAvailableAgentError(RuntimeError):
    """요구된 Capability를 가진 활성 Agent가 하나도 없을 때 발생한다."""


class AgentNotAssignedError(KeyError):
    """아직 Agent가 배정되지 않은 Task에 상태 전이를 요청했을 때
    발생한다."""


@dataclass(frozen=True)
class AgentAssignment:
    """`WorkflowLink`(Vault Task↔Core Domain Task) 하나에 배정된
    Agent."""

    link: WorkflowLink
    agent: Agent


class WorkflowAgentLink:
    """Workflow(정확히는 그 소속 Task)에 Agent를 배정·추적하는
    Connector. Agent 생성/등록/선택/상태 전이는 전부 `AgentAdapter`
    (→ Core Domain `AgentManager`/`AgentRegistry`/`AgentScheduler`)
    에 위임한다 — 선택 규칙이나 배정 우선순위 같은 로직을 여기서
    새로 만들지 않는다."""

    def __init__(self, agent_adapter: AgentAdapter, workflow_adapter: WorkflowAdapter) -> None:
        self._agent = agent_adapter
        self._workflow = workflow_adapter
        self._assignments: dict[str, AgentAssignment] = {}

    def assign_agent(self, link: WorkflowLink, capability: AgentCapability) -> AgentAssignment:
        """`capability`를 만족하는 활성 Agent 중 `AgentAdapter.
        select_agent()`(→ `AgentScheduler`)가 고른 하나를 `link`
        (Task)에 배정한다("Agent Assignment")."""
        candidates = self._agent.select_agent(capability, max_count=1)
        if not candidates:
            raise NoAvailableAgentError(capability)
        assignment = AgentAssignment(link=link, agent=candidates[0])
        self._assignments[link.domain_task.task_id] = assignment
        return assignment

    def get_assignment(self, link: WorkflowLink) -> AgentAssignment | None:
        return self._assignments.get(link.domain_task.task_id)

    def transition_agent_status(self, link: WorkflowLink, new_status: AgentStatus) -> Agent:
        """배정된 Agent의 상태를 전이한다("Agent Status" 추적).
        전이 규칙 자체는 `AgentAdapter.transition_agent()`(→
        `AgentManager`)에 위임한다."""
        assignment = self._assignments.get(link.domain_task.task_id)
        if assignment is None:
            raise AgentNotAssignedError(link.vault_task_id)
        transitioned = self._agent.transition_agent(assignment.agent, new_status)
        self._assignments[link.domain_task.task_id] = AgentAssignment(
            link=link, agent=transitioned
        )
        return transitioned

    def agent_progress(self, agent: Agent) -> float:
        """`agent`에게 배정된 Task 중 Core Domain 기준 `DONE`인 비율
        ("Agent Progress"). `Agent`/`Task` 어느 쪽에도 진행률 필드가
        없으므로(Domain 오염 금지) 배정 목록에서 매번 파생 계산한다.
        배정된 Task가 없으면 0.0."""
        assigned_links = [
            assignment.link
            for assignment in self._assignments.values()
            if assignment.agent.agent_id == agent.agent_id
        ]
        if not assigned_links:
            return 0.0
        done = sum(
            1
            for link in assigned_links
            if self._workflow.get_task(link.domain_task.task_id).status is TaskStatus.DONE
        )
        return done / len(assigned_links)

    def list_assignments(self, agent: Agent) -> Sequence[AgentAssignment]:
        return [a for a in self._assignments.values() if a.agent.agent_id == agent.agent_id]
