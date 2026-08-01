import pytest

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import EngineSessionStatus
from ai_workspace.interfaces.engine_runtime import (
    DuplicateEngineError,
    EngineTaskNotFoundError,
    NoSuitableEngineError,
)
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="구현하기", status=TaskStatus.TODO)


def test_run_executes_task_via_mock_adapter_and_returns_success() -> None:
    """T2-05 DoD: EngineRuntime.run()이 MockEngineAdapter를 통해 Task를
    "실행"하고 EngineResult(success=True)를 반환한다."""
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())

    result = runtime.run(make_task())

    assert result.success is True


def test_register_engine_duplicate_raises_error() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())

    with pytest.raises(DuplicateEngineError):
        runtime.register_engine("mock", MockEngineAdapter())


def test_run_raises_no_suitable_engine_when_capability_unmatched() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task(), required_capabilities=frozenset({"vision"}))


def test_status_reflects_completed_after_run() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())
    task = make_task()

    runtime.run(task)

    assert runtime.status(task.task_id) == EngineSessionStatus.COMPLETED


def test_cancel_then_status_is_cancelled() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())
    task = make_task()
    runtime.run(task)

    runtime.cancel(task.task_id)

    assert runtime.status(task.task_id) == EngineSessionStatus.CANCELLED


def test_status_unknown_task_raises_not_found() -> None:
    runtime = InMemoryEngineRuntime()

    with pytest.raises(EngineTaskNotFoundError):
        runtime.status("unknown")


def test_estimate_cost_returns_selected_adapters_estimate() -> None:
    runtime = InMemoryEngineRuntime()
    adapter = MockEngineAdapter()
    runtime.register_engine("mock", adapter)

    estimate = runtime.estimate_cost(make_task())

    assert estimate == adapter.estimate_cost(make_task())


def test_estimate_cost_raises_no_suitable_engine_when_capability_unmatched() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.estimate_cost(make_task(), required_capabilities=frozenset({"vision"}))


def test_run_parallel_preserves_order() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())
    tasks = [make_task("t1"), make_task("t2"), make_task("t3")]

    results = runtime.run_parallel(tasks)

    assert [result.success for result in results] == [True, True, True]


def test_run_ensemble_runs_same_task_via_each_named_engine() -> None:
    """M62(ADR-0080): 같은 Task를 여러 등록된 엔진 이름으로 동시에 돌려
    이름별 결과를 얻는다."""
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("claude", MockEngineAdapter())
    runtime.register_engine("codex", MockEngineAdapter())
    task = make_task()

    results = runtime.run_ensemble(task, ["claude", "codex"])

    assert set(results) == {"claude", "codex"}
    assert results["claude"].success is True
    assert results["codex"].success is True


def test_run_ensemble_unregistered_name_yields_failed_result_not_exception() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("claude", MockEngineAdapter())

    results = runtime.run_ensemble(make_task(), ["claude", "unknown"])

    assert results["claude"].success is True
    assert results["unknown"].success is False


def test_run_ensemble_empty_names_returns_empty_dict() -> None:
    runtime = InMemoryEngineRuntime()

    assert runtime.run_ensemble(make_task(), []) == {}
