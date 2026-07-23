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
