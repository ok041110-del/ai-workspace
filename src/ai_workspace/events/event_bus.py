from __future__ import annotations

import itertools
from collections.abc import Callable

from ai_workspace.interfaces.event_bus import Event, EventBus, SubscriptionNotFoundError


class InMemoryEventBus(EventBus):
    """인메모리 pub/sub Event Bus 구현체(ARCHITECTURE.md §3.4~§3.5, §11
    기술 스택, T2-02). EventStore(예: `FileEventStore`)는 이 Bus를
    `subscribe()`로 구독하는 독립 구독자 중 하나일 뿐이며, 별도의 특별
    전달 경로를 갖지 않는다(ADR-0018)."""

    def __init__(self) -> None:
        self._subscribers: dict[str, Callable[[Event], None]] = {}
        self._id_generator = itertools.count(1)

    def publish(self, event: Event) -> None:
        for handler in list(self._subscribers.values()):
            try:
                handler(event)
            except Exception:
                pass

    def subscribe(self, handler: Callable[[Event], None]) -> str:
        subscription_id = f"sub-{next(self._id_generator)}"
        self._subscribers[subscription_id] = handler
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        if subscription_id not in self._subscribers:
            raise SubscriptionNotFoundError(subscription_id)
        del self._subscribers[subscription_id]
