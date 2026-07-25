from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.event_store import EventStore


class FileEventStore(EventStore):
    """Event를 append-only JSON Lines 파일에 기록하는 파일 기반 구현체
    (ARCHITECTURE.md §3.5, ADR-0014, ADR-0018)."""

    def __init__(self, base_dir: str | Path) -> None:
        self._base_dir = Path(base_dir)
        self._base_dir.mkdir(parents=True, exist_ok=True)
        self._path = self._base_dir / "events.jsonl"

    def record(self, event: Event) -> None:
        data = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "payload": event.payload,
            "source_agent_id": event.source_agent_id,
        }
        with self._path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    def replay(self, since_event_id: str | None = None) -> list[Event]:
        if not self._path.exists():
            return []
        events = [
            self._from_dict(json.loads(line))
            for line in self._path.read_text(encoding="utf-8").splitlines()
            if line
        ]
        if since_event_id is None:
            return events
        for index, event in enumerate(events):
            if event.event_id == since_event_id:
                return events[index + 1 :]
        return []

    @staticmethod
    def _from_dict(data: dict[str, Any]) -> Event:
        return Event(
            event_id=data["event_id"],
            event_type=data["event_type"],
            payload=data["payload"],
            source_agent_id=data["source_agent_id"],
        )
