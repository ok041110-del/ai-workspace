import pytest

from ai_workspace.interfaces.event_bus import Event, SubscriptionNotFoundError

from .fakes import FakeEventBus, FakeEventStore


def test_publish_calls_subscribed_handlers() -> None:
    bus = FakeEventBus()
    received: list[Event] = []
    bus.subscribe(received.append)

    event = Event(event_id="e1", event_type="agent.created")
    bus.publish(event)

    assert received == [event]


def test_unsubscribe_stops_further_delivery() -> None:
    bus = FakeEventBus()
    received: list[Event] = []
    subscription_id = bus.subscribe(received.append)
    bus.unsubscribe(subscription_id)

    bus.publish(Event(event_id="e1", event_type="agent.created"))

    assert received == []


def test_unsubscribe_unknown_raises_not_found() -> None:
    bus = FakeEventBus()

    with pytest.raises(SubscriptionNotFoundError):
        bus.unsubscribe("unknown")


def test_event_store_subscribes_through_same_path_as_any_subscriber() -> None:
    bus = FakeEventBus()
    store = FakeEventStore()
    bus.subscribe(store.record)

    event = Event(event_id="e1", event_type="agent.created")
    bus.publish(event)

    assert store.replay() == [event]
