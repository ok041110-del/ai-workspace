import pytest

from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import EngineSessionStatus
from ai_workspace.interfaces.engine_runtime import (
    DuplicateEngineError,
    EngineTaskNotFoundError,
    NoSuitableEngineError,
)

from .fakes import FakeEngineAdapter, FakeEngineRuntime


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="Task", status=TaskStatus.TODO)


def test_register_engine_duplicate_raises_error() -> None:
    runtime = FakeEngineRuntime()
    runtime.register_engine("claude_code", FakeEngineAdapter())

    with pytest.raises(DuplicateEngineError):
        runtime.register_engine("claude_code", FakeEngineAdapter())


def test_run_selects_engine_matching_required_capabilities() -> None:
    runtime = FakeEngineRuntime()
    runtime.register_engine("claude_code", FakeEngineAdapter(frozenset({"code_generation"})))

    result = runtime.run(make_task(), required_capabilities=frozenset({"code_generation"}))

    assert result.success is True


def test_run_raises_no_suitable_engine_when_capability_unmatched() -> None:
    runtime = FakeEngineRuntime()
    runtime.register_engine("claude_code", FakeEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task(), required_capabilities=frozenset({"vision"}))


def test_status_reflects_completed_after_run() -> None:
    runtime = FakeEngineRuntime()
    runtime.register_engine("claude_code", FakeEngineAdapter())
    task = make_task()

    runtime.run(task)

    assert runtime.status(task.task_id) == EngineSessionStatus.COMPLETED


def test_cancel_then_status_is_cancelled() -> None:
    runtime = FakeEngineRuntime()
    runtime.register_engine("claude_code", FakeEngineAdapter())
    task = make_task()
    runtime.run(task)

    runtime.cancel(task.task_id)

    assert runtime.status(task.task_id) == EngineSessionStatus.CANCELLED


def test_cancel_unknown_task_raises_not_found() -> None:
    runtime = FakeEngineRuntime()

    with pytest.raises(EngineTaskNotFoundError):
        runtime.cancel("unknown")


def test_status_unknown_task_raises_not_found() -> None:
    runtime = FakeEngineRuntime()

    with pytest.raises(EngineTaskNotFoundError):
        runtime.status("unknown")


def test_run_parallel_preserves_order_and_requires_parallel_support() -> None:
    runtime = FakeEngineRuntime()
    runtime.register_engine("claude_code", FakeEngineAdapter(parallel=True))
    tasks = [make_task("t1"), make_task("t2"), make_task("t3")]

    results = runtime.run_parallel(tasks)

    assert [result.output for result in results] == [
        "t1 완료",
        "t2 완료",
        "t3 완료",
    ]


def test_run_parallel_raises_no_suitable_engine_when_engine_lacks_parallel_support() -> None:
    runtime = FakeEngineRuntime()
    runtime.register_engine("claude_code", FakeEngineAdapter(parallel=False))

    with pytest.raises(NoSuitableEngineError):
        runtime.run_parallel([make_task()])
