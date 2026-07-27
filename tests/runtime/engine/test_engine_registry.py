import pytest

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_registry import (
    DuplicateEngineRegistrationError,
    EngineNotRegisteredError,
)
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="구현하기", status=TaskStatus.TODO)


def test_register_duplicate_raises_error() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("mock", MockEngineAdapter())

    with pytest.raises(DuplicateEngineRegistrationError):
        registry.register("mock", MockEngineAdapter())


def test_get_returns_registered_adapter() -> None:
    registry = InMemoryEngineRegistry()
    adapter = MockEngineAdapter()
    registry.register("mock", adapter)

    assert registry.get("mock") is adapter


def test_get_unregistered_raises_not_found() -> None:
    registry = InMemoryEngineRegistry()

    with pytest.raises(EngineNotRegisteredError):
        registry.get("unknown")


def test_list_candidates_returns_only_matching_capability() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("claude_code", MockEngineAdapter(frozenset({"claude_code"})))
    registry.register("codex", MockEngineAdapter(frozenset({"codex"})))

    candidates = registry.list_candidates(make_task(), required_capabilities=frozenset({"codex"}))

    assert [candidate.engine_name for candidate in candidates] == ["codex"]


def test_list_candidates_includes_cost_estimate_from_adapter() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("mock", MockEngineAdapter())

    candidates = registry.list_candidates(make_task())

    assert len(candidates) == 1
    assert candidates[0].estimated_tokens == 0
    assert candidates[0].estimated_cost_usd == 0.0
    assert candidates[0].supports_parallel is True


def test_list_candidates_returns_empty_list_when_no_match() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("mock", MockEngineAdapter(frozenset({"claude_code"})))

    assert registry.list_candidates(make_task(), required_capabilities=frozenset({"vision"})) == []
