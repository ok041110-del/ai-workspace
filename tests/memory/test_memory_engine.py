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
