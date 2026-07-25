from __future__ import annotations

import itertools

from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus
from ai_workspace.interfaces.agent_manager import AgentManager, InvalidAgentTransitionError

_ALLOWED_TRANSITIONS: dict[AgentStatus, frozenset[AgentStatus]] = {
    AgentStatus.IDLE: frozenset({AgentStatus.RUNNING, AgentStatus.STOPPED}),
    AgentStatus.RUNNING: frozenset(
        {
            AgentStatus.WAITING,
            AgentStatus.PAUSED,
            AgentStatus.STOPPED,
            AgentStatus.ERROR,
            AgentStatus.IDLE,
        }
    ),
    AgentStatus.WAITING: frozenset({AgentStatus.RUNNING, AgentStatus.STOPPED}),
    AgentStatus.PAUSED: frozenset({AgentStatus.RUNNING, AgentStatus.STOPPED}),
    AgentStatus.ERROR: frozenset({AgentStatus.STOPPED}),
    AgentStatus.STOPPED: frozenset(),
}


class InMemoryAgentManager(AgentManager):
    """Agent 생성과 상태 전이를 관리하는 최소 구현체(ARCHITECTURE.md §3.4,
    T1-18 계약, M4-T01). 허용 전이 규칙은 `Task`(domain/task.py)의
    `_ALLOWED_TRANSITIONS`와 동일한 형태로 이 구현체가 정의한다."""

    def __init__(self) -> None:
        self._id_generator = itertools.count(1)

    def create(
        self, role: AgentRole, capabilities: frozenset[AgentCapability] = frozenset()
    ) -> Agent:
        agent_id = f"agent-{next(self._id_generator)}"
        return Agent(agent_id=agent_id, role=role, capabilities=capabilities)

    def transition(self, agent: Agent, new_status: AgentStatus) -> Agent:
        if new_status not in _ALLOWED_TRANSITIONS[agent.status]:
            raise InvalidAgentTransitionError(
                f"{agent.status} -> {new_status} 전이는 허용되지 않습니다."
            )
        agent.status = new_status
        return agent
