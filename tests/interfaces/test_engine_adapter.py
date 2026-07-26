import pytest

from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import (
    EngineExecutionError,
    EngineSessionStatus,
    SessionNotFoundError,
)

from .fakes import FailingFakeEngineAdapter, FakeEngineAdapter


def make_task() -> Task:
    return Task(task_id="t1", project_id="p1", title="Task", status=TaskStatus.TODO)


def test_create_session_then_run_returns_success_result() -> None:
    adapter = FakeEngineAdapter()
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is True
    assert result.error is None
    assert adapter.status(session_id) == EngineSessionStatus.COMPLETED


def test_run_without_model_behaves_like_before_milestone_14() -> None:
    """Milestone 14 DoD 1번: model을 생략하면 기존과 완전히 동일하게
    동작한다."""
    adapter = FakeEngineAdapter()
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is True
    assert adapter.received_models == [None]


def test_run_records_the_model_passed_in() -> None:
    adapter = FakeEngineAdapter()
    session_id = adapter.create_session()

    adapter.run(session_id, make_task(), model="opus")

    assert adapter.received_models == ["opus"]


def test_run_with_unknown_session_raises_session_not_found() -> None:
    adapter = FakeEngineAdapter()

    with pytest.raises(SessionNotFoundError):
        adapter.run("unknown", make_task())


def test_cancel_sets_status_to_cancelled() -> None:
    adapter = FakeEngineAdapter()
    session_id = adapter.create_session()

    adapter.cancel(session_id)

    assert adapter.status(session_id) == EngineSessionStatus.CANCELLED


def test_destroy_session_then_status_raises_session_not_found() -> None:
    adapter = FakeEngineAdapter()
    session_id = adapter.create_session()

    adapter.destroy_session(session_id)

    with pytest.raises(SessionNotFoundError):
        adapter.status(session_id)


def test_execution_failure_raises_not_result() -> None:
    adapter = FailingFakeEngineAdapter()
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())


def test_estimate_cost_does_not_require_a_session() -> None:
    adapter = FakeEngineAdapter()

    estimate = adapter.estimate_cost(make_task())

    assert estimate.estimated_tokens > 0
