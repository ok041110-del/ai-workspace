from __future__ import annotations

from ai_workspace.interfaces.memory_engine import MemoryEngine


class InMemoryMemoryEngine(MemoryEngine):
    """장기 메모리 저장/검색만 담당하는 최소 구현체(T2-04). Snapshot 개념을
    전혀 알지 못한다 — Snapshot 생명주기는 `ContextManager`의 책임이다
    (ARCHITECTURE.md §3.8, §8 규칙 7)."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def remember(self, key: str, value: str) -> None:
        self._store[key] = value

    def recall(self, key: str) -> str | None:
        return self._store.get(key)

    def search(self, query: str) -> list[str]:
        return [key for key, value in self._store.items() if query in value]
