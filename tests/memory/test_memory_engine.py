from ai_workspace.memory.memory_engine import InMemoryMemoryEngine


def test_remember_then_recall_returns_value() -> None:
    engine = InMemoryMemoryEngine()

    engine.remember("key", "value")

    assert engine.recall("key") == "value"


def test_recall_missing_key_returns_none() -> None:
    engine = InMemoryMemoryEngine()

    assert engine.recall("missing") is None


def test_remember_overwrites_previous_value() -> None:
    engine = InMemoryMemoryEngine()
    engine.remember("key", "old")

    engine.remember("key", "new")

    assert engine.recall("key") == "new"


def test_search_returns_keys_whose_value_contains_query() -> None:
    engine = InMemoryMemoryEngine()
    engine.remember("k1", "project p1 완료")
    engine.remember("k2", "project p2 진행 중")

    assert engine.search("p1") == ["k1"]


def test_search_returns_empty_list_when_no_match() -> None:
    engine = InMemoryMemoryEngine()
    engine.remember("k1", "value")

    assert engine.search("없음") == []


def test_search_key_itself_is_not_searched() -> None:
    engine = InMemoryMemoryEngine()
    engine.remember("special-key", "일반 내용")

    assert engine.search("special-key") == []
