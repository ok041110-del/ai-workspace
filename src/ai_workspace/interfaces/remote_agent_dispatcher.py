from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.agent import Agent
from ai_workspace.interfaces.event_bus import Event


class AgentUnreachableError(Exception):
    """dispatch() 대상 Agent의 location에 연결할 수 없을 때 발생한다."""


class RemoteAgentDispatcher(ABC):
    """`Agent.location`(Milestone 61, ADR-0079)이 가리키는 위치로 Event를
    전달하는 경계 계약. `ExecutionEnvironment`(M11)가 `EngineAdapter` 내부에서
    "명령을 어디서 실행할지"를 추상화하듯, 이 인터페이스는 Agent Runtime
    레벨에서 "Event를 어느 위치의 Agent에게 전달할지"를 추상화한다.

    location이 `None`인 Agent(기본값, 같은 프로세스)는 이 계약과 무관하다 —
    여전히 기존과 동일하게 `EventBus.publish()`로 모든 구독자에게 방송되고,
    각 Agent가 `is_agent_selected()`(Milestone 13)로 스스로 선택 여부를
    판단한다. 이 인터페이스는 location이 있는(원격이라고 선언된) Agent에게
    Event를 전달할 때만 쓰인다."""

    @abstractmethod
    def dispatch(self, agent: Agent, event: Event) -> None:
        """
        입력: agent (location이 설정된 Agent), event (전달할 Event)
        출력: 없음
        예외: agent.location에 해당하는 목적지가 없거나 연결할 수 없으면
              AgentUnreachableError
        보장: 호출이 성공하면 agent.location이 가리키는 목적지가 event를
              수신한다.
        """
        raise NotImplementedError
