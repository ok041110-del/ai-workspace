from .fakes import FakeMemoryEngine


def test_remember_then_recall_returns_value() -> None:
    engine = FakeMemoryEngine()

    engine.remember("current_phase", "Phase 1")

    assert engine.recall("current_phase") == "Phase 1"


def test_recall_missing_key_returns_none() -> None:
    engine = FakeMemoryEngine()

    assert engine.recall("missing") is None


def test_remember_overwrites_previous_value() -> None:
    engine = FakeMemoryEngine()
    engine.remember("key", "old")

    engine.remember("key", "new")

    assert engine.recall("key") == "new"


def test_search_returns_keys_whose_value_contains_query() -> None:
    engine = FakeMemoryEngine()
    engine.remember("k1", "project p1 완료")
    engine.remember("k2", "project p2 진행 중")

    assert engine.search("p1") == ["k1"]


def test_search_returns_empty_list_when_no_match() -> None:
    engine = FakeMemoryEngine()
    engine.remember("k1", "value")

    assert engine.search("없음") == []
