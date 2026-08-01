from __future__ import annotations

from ai_workspace.domain.agent import Agent
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.remote_agent_dispatcher import (
    AgentUnreachableError,
    RemoteAgentDispatcher,
)


class LoopbackAgentDispatcher(RemoteAgentDispatcher):
    """location별로 등록된 `EventBus`에 Event를 전달하는 최소 구현체
    (Milestone 61, ADR-0079). 실제 네트워크/RPC 없이 같은 프로세스 안에서
    여러 location을 독립된 `EventBus` 단위로 흉내낸다 — 각 location은
    자신만의 `EventBus`를 가지므로, 그 EventBus를 구독하는 Agent들만 해당
    location으로 전달된 Event를 받는다. 향후 실제 네트워크 기반 구현체(예:
    HTTP)로 교체해도 `RemoteAgentDispatcher`를 사용하는 코드는 변경할 필요가
    없다."""

    def __init__(self) -> None:
        self._buses: dict[str, EventBus] = {}

    def register_location(self, location: str, event_bus: EventBus) -> None:
        """location 식별자와 그 location을 대표하는 EventBus를 연결한다.
        같은 location으로 다시 호출하면 앞선 등록을 덮어쓴다."""
        self._buses[location] = event_bus

    def dispatch(self, agent: Agent, event: Event) -> None:
        if agent.location is None or agent.location not in self._buses:
            raise AgentUnreachableError(agent.location)
        self._buses[agent.location].publish(event)
