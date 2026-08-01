from pathlib import Path

from ai_workspace.storage.file_memory_engine import FileMemoryEngine


def test_remember_then_recall_returns_same_value(tmp_path: Path) -> None:
    engine = FileMemoryEngine(tmp_path)

    engine.remember("k1", "hello world")

    assert engine.recall("k1") == "hello world"


def test_recall_missing_key_returns_none(tmp_path: Path) -> None:
    engine = FileMemoryEngine(tmp_path)

    assert engine.recall("unknown") is None


def test_remember_overwrites_existing_value(tmp_path: Path) -> None:
    engine = FileMemoryEngine(tmp_path)
    engine.remember("k1", "first")
    engine.remember("k1", "second")

    assert engine.recall("k1") == "second"


def test_search_returns_keys_whose_value_contains_query(tmp_path: Path) -> None:
    engine = FileMemoryEngine(tmp_path)
    engine.remember("k1", "apple pie")
    engine.remember("k2", "banana split")

    assert engine.search("apple") == ["k1"]


def test_search_empty_query_returns_all_keys(tmp_path: Path) -> None:
    engine = FileMemoryEngine(tmp_path)
    engine.remember("k1", "a")
    engine.remember("k2", "b")

    assert set(engine.search("")) == {"k1", "k2"}


def test_search_no_entries_returns_empty_list(tmp_path: Path) -> None:
    engine = FileMemoryEngine(tmp_path)

    assert engine.search("") == []


def test_data_persists_across_new_engine_instance(tmp_path: Path) -> None:
    FileMemoryEngine(tmp_path).remember("k1", "value")

    reopened = FileMemoryEngine(tmp_path)

    assert reopened.recall("k1") == "value"
