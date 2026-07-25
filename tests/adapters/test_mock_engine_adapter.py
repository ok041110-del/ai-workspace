import pytest

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import EngineSessionStatus, SessionNotFoundError


def make_task() -> Task:
    return Task(task_id="t1", project_id="p1", title="구현하기", status=TaskStatus.TODO)


def test_run_returns_success_without_calling_real_engine() -> None:
    adapter = MockEngineAdapter()
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is True


def test_estimate_cost_is_always_zero() -> None:
    adapter = MockEngineAdapter()

    estimate = adapter.estimate_cost(make_task())

    assert estimate.estimated_tokens == 0
    assert estimate.estimated_cost_usd == 0.0


def test_status_reflects_completed_after_run() -> None:
    adapter = MockEngineAdapter()
    session_id = adapter.create_session()

    adapter.run(session_id, make_task())

    assert adapter.status(session_id) == EngineSessionStatus.COMPLETED


def test_destroy_session_then_run_raises_not_found() -> None:
    adapter = MockEngineAdapter()
    session_id = adapter.create_session()
    adapter.destroy_session(session_id)

    with pytest.raises(SessionNotFoundError):
        adapter.run(session_id, make_task())


def test_supports_parallel_is_true() -> None:
    adapter = MockEngineAdapter()

    assert adapter.supports_parallel() is True
