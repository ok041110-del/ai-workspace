import pytest

from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event, SubscriptionNotFoundError


def make_event(event_id: str = "e1") -> Event:
    return Event(event_id=event_id, event_type="task_completed", payload={"task_id": "t1"})


def test_publish_delivers_to_subscriber() -> None:
    bus = InMemoryEventBus()
    received: list[Event] = []
    bus.subscribe(received.append)

    bus.publish(make_event())

    assert received == [make_event()]


def test_publish_delivers_to_multiple_subscribers() -> None:
    bus = InMemoryEventBus()
    received_a: list[Event] = []
    received_b: list[Event] = []
    bus.subscribe(received_a.append)
    bus.subscribe(received_b.append)

    bus.publish(make_event())

    assert received_a == [make_event()]
    assert received_b == [make_event()]


def test_subscriber_exception_does_not_block_other_subscribers() -> None:
    bus = InMemoryEventBus()
    received: list[Event] = []

    def failing_handler(event: Event) -> None:
        raise RuntimeError("boom")

    bus.subscribe(failing_handler)
    bus.subscribe(received.append)

    bus.publish(make_event())

    assert received == [make_event()]


def test_unsubscribe_stops_future_delivery() -> None:
    bus = InMemoryEventBus()
    received: list[Event] = []
    subscription_id = bus.subscribe(received.append)

    bus.unsubscribe(subscription_id)
    bus.publish(make_event())

    assert received == []


def test_unsubscribe_unknown_raises_error() -> None:
    bus = InMemoryEventBus()

    with pytest.raises(SubscriptionNotFoundError):
        bus.unsubscribe("unknown")


def test_publish_before_subscribe_is_not_delivered_retroactively() -> None:
    bus = InMemoryEventBus()
    bus.publish(make_event("early"))
    received: list[Event] = []
    bus.subscribe(received.append)

    assert received == []
