from __future__ import annotations

import itertools

from ai_workspace.domain.agent import AgentCapability, AgentRole, AgentStatus
from ai_workspace.domain.agent_session import AgentSession
from ai_workspace.interfaces.agent_manager import AgentManager
from ai_workspace.interfaces.agent_registry import AgentRegistry


class AgentSessionNotFoundError(Exception):
    """관리 중이지 않은 session_id를 조회/종료하려 할 때 발생한다."""


class AgentRuntime:
    """Agent의 시작/중지/종료(Lifecycle)를 관리하는 최소 오케스트레이터
    (ARCHITECTURE.md §3.4, T2-01). `AgentManager`(생성/상태 전이)와
    `AgentRegistry`(런타임 등록부)만 사용한다. Capability 기준 선택
    (Scheduler), Event 기반 통신(EventBus), Core Engines는 T2-01 범위 밖이며
    이후 Task에서 다룬다 — 지금 미리 끌어오지 않는다(Task Driven
    Development)."""

    def __init__(
        self,
        *,
        agent_manager: AgentManager,
        agent_registry: AgentRegistry,
    ) -> None:
        self._agent_manager = agent_manager
        self._agent_registry = agent_registry
        self._sessions: dict[str, AgentSession] = {}
        self._session_id_generator = itertools.count(1)

    def start_agent(
        self, role: AgentRole, capabilities: frozenset[AgentCapability] = frozenset()
    ) -> AgentSession:
        agent = self._agent_manager.create(role, capabilities)
        self._agent_registry.register(agent)
        self._agent_manager.transition(agent, AgentStatus.RUNNING)
        session_id = f"agent-session-{next(self._session_id_generator)}"
        session = AgentSession(session_id=session_id, agent_id=agent.agent_id)
        self._sessions[session_id] = session
        return session

    def stop_agent(self, session_id: str) -> None:
        session = self.get_session(session_id)
        agent = self._agent_registry.get(session.agent_id)
        self._agent_manager.transition(agent, AgentStatus.STOPPED)
        self._agent_registry.remove(session.agent_id)
        del self._sessions[session_id]

    def get_session(self, session_id: str) -> AgentSession:
        if session_id not in self._sessions:
            raise AgentSessionNotFoundError(session_id)
        return self._sessions[session_id]

    def get_agent_state(self, session_id: str) -> AgentStatus:
        session = self.get_session(session_id)
        return self._agent_registry.get(session.agent_id).status

    def shutdown(self) -> None:
        for session_id in list(self._sessions):
            self.stop_agent(session_id)
