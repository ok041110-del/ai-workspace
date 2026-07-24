from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


class SubscriptionNotFoundError(Exception):
    """등록되지 않은 subscription_id를 구독 해제하려 할 때 발생한다."""


@dataclass
class Event:
    event_id: str
    event_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    source_agent_id: str | None = None


class EventBus(ABC):
    """Agent/Engine/Workspace Core 사이에서 발생하는 Event를 발행/구독하는
    pub/sub 계약. ARCHITECTURE.md §3.4~§3.5, ADR-0018.

    EventStore(event_store.py)는 이 EventBus의 **독립 구독자**(하나의
    subscribe() 호출자)일 뿐이며, 다른 구독자와 동일한 subscribe() 경로를
    통해 등록된다. 구현체는 EventStore를 위한 별도의 특별 전달 경로를 두어서는
    안 된다(ADR-0018)."""

    @abstractmethod
    def publish(self, event: Event) -> None:
        """
        입력: 발행할 Event
        출력: 없음
        예외: 없음
        보장: publish(event) 호출 시점에 등록되어 있던 모든 구독자의 handler가
              event를 인자로 호출된다. 구독자 중 하나가 예외를 던져도 나머지
              구독자 호출에는 영향을 주지 않는다.
        """
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, handler: Callable[[Event], None]) -> str:
        """
        입력: handler (Event를 받아 처리하는 콜백. EventStore를 포함한 모든
              구독자가 이 동일한 시그니처를 사용한다)
        출력: 구독을 식별하는 subscription_id
        예외: 없음
        보장: subscribe(handler) 이후 publish()되는 모든 Event에 대해 handler가
              호출된다. subscribe() 이전에 발행된 Event에 대해서는 호출되지
              않는다.
        """
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, subscription_id: str) -> None:
        """
        입력: subscribe()가 반환한 subscription_id
        출력: 없음
        예외: 등록되어 있지 않으면 SubscriptionNotFoundError
        보장: unsubscribe(subscription_id) 이후 publish()되는 Event에 대해
              해당 handler는 더 이상 호출되지 않는다.
        """
        raise NotImplementedError
