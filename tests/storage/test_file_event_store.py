from pathlib import Path

from ai_workspace.interfaces.event_bus import Event
from ai_workspace.storage.file_event_store import FileEventStore


def make_event(event_id: str) -> Event:
    return Event(event_id=event_id, event_type="task_completed", payload={"task_id": "t1"})


def test_record_then_replay_returns_recorded_event(tmp_path: Path) -> None:
    store = FileEventStore(tmp_path)
    store.record(make_event("e1"))

    assert store.replay() == [make_event("e1")]


def test_replay_preserves_record_order(tmp_path: Path) -> None:
    store = FileEventStore(tmp_path)
    store.record(make_event("e1"))
    store.record(make_event("e2"))
    store.record(make_event("e3"))

    events = store.replay()

    assert [e.event_id for e in events] == ["e1", "e2", "e3"]


def test_replay_since_event_id_returns_only_later_events(tmp_path: Path) -> None:
    store = FileEventStore(tmp_path)
    store.record(make_event("e1"))
    store.record(make_event("e2"))
    store.record(make_event("e3"))

    events = store.replay(since_event_id="e1")

    assert [e.event_id for e in events] == ["e2", "e3"]


def test_replay_unknown_since_event_id_returns_empty(tmp_path: Path) -> None:
    store = FileEventStore(tmp_path)
    store.record(make_event("e1"))

    assert store.replay(since_event_id="unknown") == []


def test_replay_empty_when_nothing_recorded(tmp_path: Path) -> None:
    store = FileEventStore(tmp_path)

    assert store.replay() == []


def test_events_persist_across_new_store_instance(tmp_path: Path) -> None:
    FileEventStore(tmp_path).record(make_event("e1"))

    reopened = FileEventStore(tmp_path)

    assert [e.event_id for e in reopened.replay()] == ["e1"]
