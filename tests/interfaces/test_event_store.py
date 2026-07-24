from ai_workspace.interfaces.event_bus import Event

from .fakes import FakeEventStore


def test_record_then_replay_returns_recorded_event() -> None:
    store = FakeEventStore()
    event = Event(event_id="e1", event_type="agent.created")

    store.record(event)

    assert store.replay() == [event]


def test_replay_since_event_id_returns_only_later_events() -> None:
    store = FakeEventStore()
    first = Event(event_id="e1", event_type="agent.created")
    second = Event(event_id="e2", event_type="agent.stopped")
    store.record(first)
    store.record(second)

    assert store.replay(since_event_id="e1") == [second]


def test_replay_returns_defensive_copy() -> None:
    store = FakeEventStore()
    event = Event(event_id="e1", event_type="agent.created")
    store.record(event)

    events = store.replay()
    events.append(Event(event_id="e2", event_type="agent.stopped"))

    assert len(store.replay()) == 1
