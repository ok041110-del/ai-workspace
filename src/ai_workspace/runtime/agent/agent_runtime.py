from __future__ import annotations

import itertools

from ai_workspace.domain.agent import AgentCapability, AgentRole, AgentStatus
from ai_workspace.domain.agent_session import AgentSession
from ai_workspace.interfaces.agent_manager import AgentManager
from ai_workspace.interfaces.agent_registry import AgentRegistry
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.llm_policy_engine import LLMPolicyEngine
from ai_workspace.interfaces.remote_agent_dispatcher import RemoteAgentDispatcher


class AgentSessionNotFoundError(Exception):
    """관리 중이지 않은 session_id를 조회/종료하려 할 때 발생한다."""


class AgentRuntime:
    """Agent의 시작/중지/종료(Lifecycle)를 관리하는 최소 오케스트레이터
    (ARCHITECTURE.md §3.4, T2-01). `AgentManager`(생성/상태 전이)와
    `AgentRegistry`(런타임 등록부)만 사용한다. Capability 기준 선택
    (Scheduler), Event 기반 통신(EventBus), Core Engines는 T2-01 범위 밖이며
    이후 Task에서 다룬다 — 지금 미리 끌어오지 않는다(Task Driven
    Development).

    `llm_policy_engine`(선택적, M5-T02)이 주어지면 `start_agent()` 시점에
    Role에 맞는 `LLMPolicyDecision`을 조회해 `AgentSession.llm_policy_decision`
    에 기록한다. 이 Task는 정책을 조회·기록만 할 뿐, 실제 Engine/Adapter
    선택에 반영하지는 않는다(현재 `ManagedEngineRuntime`은 Adapter를 하나만
    등록할 수 있어 Role별로 다른 모델을 실제로 전환할 수 없음 — 실제
    반영은 Multi-Engine Adapter가 준비되는 M5-T05 이후).

    **Self Optimization 피드백(Milestone 67, ADR-0085)**: `record_llm_policy_
    outcome(session_id, success)`은 `CodingAgent`/`ReviewAgent`/
    `DocumentationAgent`가 `engine_runtime.run()` 직후 호출하는 명시적
    피드백 진입점이다. `llm_policy_engine`이 주입되지 않았거나 해당
    session에 결정된 policy가 없으면 아무 것도 하지 않는다(no-op) —
    Agent는 `LLMPolicyEngine` interface 자체를 알 필요 없이 `AgentRuntime`
    한 곳을 통해서만 피드백을 전달한다(M5-T02가 세운 "Agent는
    LLMPolicyEngine을 직접 참조하지 않는다" 경계를 그대로 유지).

    **Distributed Multi-Agent(Milestone 61, ADR-0079)**: `start_agent()`에
    `location`을 주면 생성된 Agent의 `Agent.location`에 그대로 기록한다.
    기본값 `None`이면 M4-T01과 완전히 동일하게 "같은 프로세스" Agent다.
    `remote_agent_dispatcher`(선택적)를 주입하면 `dispatch_event()`로 그
    session의 Agent가 location을 가졌을 때만 원격 전달을 수행한다 —
    location이 없는(로컬) Agent는 이 메서드가 개입하지 않고 기존과 동일하게
    `EventBus.publish()`의 일반 구독 경로로 처리된다."""

    def __init__(
        self,
        *,
        agent_manager: AgentManager,
        agent_registry: AgentRegistry,
        llm_policy_engine: LLMPolicyEngine | None = None,
        remote_agent_dispatcher: RemoteAgentDispatcher | None = None,
    ) -> None:
        self._agent_manager = agent_manager
        self._agent_registry = agent_registry
        self._llm_policy_engine = llm_policy_engine
        self._remote_agent_dispatcher = remote_agent_dispatcher
        self._sessions: dict[str, AgentSession] = {}
        self._session_id_generator = itertools.count(1)

    def start_agent(
        self,
        role: AgentRole,
        capabilities: frozenset[AgentCapability] = frozenset(),
        *,
        location: str | None = None,
    ) -> AgentSession:
        agent = self._agent_manager.create(role, capabilities)
        agent.location = location
        self._agent_registry.register(agent)
        self._agent_manager.transition(agent, AgentStatus.RUNNING)
        session_id = f"agent-session-{next(self._session_id_generator)}"
        llm_policy_decision = (
            self._llm_policy_engine.select(role) if self._llm_policy_engine is not None else None
        )
        session = AgentSession(
            session_id=session_id,
            agent_id=agent.agent_id,
            llm_policy_decision=llm_policy_decision,
        )
        self._sessions[session_id] = session
        return session

    def record_llm_policy_outcome(self, session_id: str, success: bool) -> None:
        if self._llm_policy_engine is None:
            return
        session = self.get_session(session_id)
        if session.llm_policy_decision is None:
            return
        agent = self._agent_registry.get(session.agent_id)
        self._llm_policy_engine.record_outcome(agent.role, session.llm_policy_decision, success)

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

    def dispatch_event(self, session_id: str, event: Event) -> None:
        """`session_id`의 Agent가 원격(location 있음)이면
        `remote_agent_dispatcher`로 전달하고, 로컬(location 없음)이면
        아무 것도 하지 않는다(Milestone 61, ADR-0079) — 로컬 Agent는 이미
        `EventBus.publish()`의 일반 구독 경로로 Event를 받으므로 이 메서드가
        개입할 필요가 없다.

        입력: session_id, event
        출력: 없음
        예외: 해당 Agent가 원격인데 remote_agent_dispatcher가 주입되지
              않았으면 ValueError. remote_agent_dispatcher.dispatch()가
              던지는 예외(예: AgentUnreachableError)는 그대로 전파된다.
        """
        session = self.get_session(session_id)
        agent = self._agent_registry.get(session.agent_id)
        if agent.location is None:
            return
        if self._remote_agent_dispatcher is None:
            raise ValueError(
                f"Agent {agent.agent_id}는 location={agent.location!r}이지만 "
                "remote_agent_dispatcher가 주입되지 않았습니다."
            )
        self._remote_agent_dispatcher.dispatch(agent, event)

    def shutdown(self) -> None:
        for session_id in list(self._sessions):
            self.stop_agent(session_id)
