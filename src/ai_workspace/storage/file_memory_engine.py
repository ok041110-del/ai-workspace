from __future__ import annotations

import json
from pathlib import Path

from ai_workspace.interfaces.memory_engine import MemoryEngine

_STORE_FILENAME = "memory_engine.json"


class FileMemoryEngine(MemoryEngine):
    """`MemoryEngine`을 단일 JSON 파일(key→value dict)로 영속화하는
    구현체(Milestone 50, ADR-0067). `storage/`의 File*Repository와
    동일한 패턴(JSON 직렬화, `base_dir` 생성자 주입)을 따르되, entry당
    파일이 아니라 dict 전체를 파일 하나에 담는다 — `ExecutionMemoryStore`
    가 `MemoryEngine.search("")`로 전체 키를 얻는 현재 사용 패턴에
    가장 자연스럽게 맞기 때문이다(YAGNI)."""

    def __init__(self, base_dir: str | Path) -> None:
        self._path = Path(base_dir) / _STORE_FILENAME
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def remember(self, key: str, value: str) -> None:
        data = self._load()
        data[key] = value
        self._save(data)

    def recall(self, key: str) -> str | None:
        return self._load().get(key)

    def search(self, query: str) -> list[str]:
        return [key for key, value in self._load().items() if query in value]

    def _load(self) -> dict[str, str]:
        if not self._path.exists():
            return {}
        return dict(json.loads(self._path.read_text(encoding="utf-8")))

    def _save(self, data: dict[str, str]) -> None:
        self._path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
