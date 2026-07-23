import pytest

from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import EngineExecutionError

from .fakes import FailingFakeEngineAdapter, FakeEngineAdapter


def make_task() -> Task:
    return Task(task_id="t1", project_id="p1", title="Task", status=TaskStatus.TODO)


def test_run_task_returns_success_result() -> None:
    adapter = FakeEngineAdapter()

    result = adapter.run_task(make_task())

    assert result.success is True
    assert result.error is None


def test_execution_failure_raises_not_result() -> None:
    adapter = FailingFakeEngineAdapter()

    with pytest.raises(EngineExecutionError):
        adapter.run_task(make_task())
