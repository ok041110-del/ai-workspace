from __future__ import annotations

import json
import uuid
from dataclasses import dataclass

from ai_workspace.domain.execution_memory import ExecutionMemory
from ai_workspace.interfaces.memory_engine import MemoryEngine

_KEY_PREFIX = "execution-memory-"


@dataclass(frozen=True)
class ExecutionMemoryEntry:
    """`ExecutionMemoryStore.query()`가 반환하는 읽기 전용 뷰
    (Milestone 40, ADR-0055). `domain.execution_memory.ExecutionMemory`
    와 필드는 동일하지만 별도 타입이다 — `integration/vault_adapter.py`
    의 `TaskDocumentView`가 `domain.task.Task`를 감싸 노출하는 것과
    같은 이유다: `intelligence/`는 `domain`을 직접 참조할 수 없으므로
    (ARCHITECTURE.md §8 규칙 21), `query()`가 domain 타입을 그대로
    돌려주면 그 경계를 우회하게 된다. `record()`는 여전히 domain의
    `ExecutionMemory`를 받는다 — 쓰기 쪽 호출자(`runtime/execution/`)
    는 domain 참조 제약이 없다."""

    task_id: str
    action: str
    result: str
    timestamp: str
    reason: str | None = None


class ExecutionMemoryStore:
    """`ExecutionMemory`를 기존 `MemoryEngine`(저장/검색만 담당,
    ARCHITECTURE.md §3.8)에 JSON으로 직렬화해 저장/조회하는 얇은
    서비스(Milestone 39). `InMemoryContextManager`가 Snapshot을
    `MemoryEngine`에 JSON으로 저장하는 것과 동일한 패턴이다 —
    `MemoryEngine` interface(remember/recall/search)를 그대로
    재사용할 뿐 확장하지 않는다.

    **저장만, 학습 없음(ADR-0053)**: 이 클래스는 기록을 쌓고
    조회하게만 해준다. 과거 기록을 근거로 추천·판단을 바꾸는 것은
    Learning Engine(M40 이후, 별도 승인 대상)의 책임이다.

    **조회는 View 타입으로(M40, ADR-0055)**: `query()`는 domain
    타입이 아니라 `ExecutionMemoryEntry`를 반환한다 — 아래 참고."""

    def __init__(self, memory_engine: MemoryEngine) -> None:
        self._memory_engine = memory_engine

    def record(self, memory: ExecutionMemory) -> str:
        """
        입력: memory (기록할 ExecutionMemory)
        출력: 저장에 쓰인 key
        예외: 없음
        보장: record(memory) 직후 query()의 결과에 memory와 동일한
              내용의 항목이 포함된다.
        """
        key = f"{_KEY_PREFIX}{uuid.uuid4()}"
        payload = {
            "task_id": memory.task_id,
            "action": memory.action,
            "result": memory.result,
            "timestamp": memory.timestamp,
            "reason": memory.reason,
        }
        self._memory_engine.remember(key, json.dumps(payload, ensure_ascii=False))
        return key

    def query(self, *, task_id: str | None = None) -> list[ExecutionMemoryEntry]:
        """
        입력: task_id (선택 — 지정하면 해당 Task의 기록만 반환)
        출력: 저장된 기록을 `ExecutionMemoryEntry` 목록으로, timestamp
              오름차순 정렬(기록 없으면 빈 리스트)
        예외: 없음
        보장: side-effect 없음(read-only). `MemoryEngine.search("")`가
              "" 는 모든 값의 substring이라는 성질을 이용해 전체
              키를 얻는다 — `MemoryEngine` interface에 새 메서드를
              추가하지 않는다.
        """
        records = []
        for key in self._memory_engine.search(""):
            if not key.startswith(_KEY_PREFIX):
                continue
            stored = self._memory_engine.recall(key)
            if stored is None:
                continue
            payload = json.loads(stored)
            if task_id is not None and payload["task_id"] != task_id:
                continue
            records.append(
                ExecutionMemoryEntry(
                    task_id=payload["task_id"],
                    action=payload["action"],
                    result=payload["result"],
                    timestamp=payload["timestamp"],
                    reason=payload.get("reason"),
                )
            )
        records.sort(key=lambda record: record.timestamp)
        return records
