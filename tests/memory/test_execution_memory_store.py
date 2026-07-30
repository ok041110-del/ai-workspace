from ai_workspace.domain.execution_memory import ExecutionMemory
from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine


def _make_store() -> ExecutionMemoryStore:
    return ExecutionMemoryStore(InMemoryMemoryEngine())


def test_record_then_query_returns_recorded_memory() -> None:
    store = _make_store()
    memory = ExecutionMemory(
        task_id="M36-T01",
        action="설계",
        result="success",
        timestamp="2026-07-30T00:00:00+00:00",
    )

    store.record(memory)

    assert store.query() == [memory]


def test_query_without_task_id_returns_all_records_sorted_by_timestamp() -> None:
    store = _make_store()
    later = ExecutionMemory(
        task_id="M36-T02", action="b", result="success", timestamp="2026-07-30T02:00:00+00:00"
    )
    earlier = ExecutionMemory(
        task_id="M36-T01", action="a", result="success", timestamp="2026-07-30T01:00:00+00:00"
    )

    store.record(later)
    store.record(earlier)

    assert store.query() == [earlier, later]


def test_query_filters_by_task_id() -> None:
    store = _make_store()
    target = ExecutionMemory(
        task_id="M36-T01", action="a", result="success", timestamp="2026-07-30T00:00:00+00:00"
    )
    other = ExecutionMemory(
        task_id="M36-T02", action="b", result="success", timestamp="2026-07-30T01:00:00+00:00"
    )
    store.record(target)
    store.record(other)

    assert store.query(task_id="M36-T01") == [target]


def test_query_returns_empty_list_when_nothing_recorded() -> None:
    store = _make_store()

    assert store.query() == []


def test_record_preserves_failure_reason() -> None:
    store = _make_store()
    memory = ExecutionMemory(
        task_id="M36-T01",
        action="배포",
        result="failure",
        timestamp="2026-07-30T00:00:00+00:00",
        reason="authentication required",
    )

    store.record(memory)

    assert store.query()[0].reason == "authentication required"


def test_query_ignores_unrelated_keys_in_shared_memory_engine() -> None:
    """같은 `MemoryEngine` 인스턴스를 다른 목적(예: Snapshot)으로도
    쓰는 경우, `search("")`가 모든 key를 반환해도 `ExecutionMemoryStore`
    가 기록한 key만 파싱한다(§8 규칙 7의 Snapshot 경로와 공존 가능)."""
    engine = InMemoryMemoryEngine()
    engine.remember("snapshot-1", "not json execution memory")
    store = ExecutionMemoryStore(engine)
    memory = ExecutionMemory(
        task_id="M36-T01", action="a", result="success", timestamp="2026-07-30T00:00:00+00:00"
    )

    store.record(memory)

    assert store.query() == [memory]
