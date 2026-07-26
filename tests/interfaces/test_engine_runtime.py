import itertools

import pytest

from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import (
    CostEstimate,
    EngineAdapter,
    EngineExecutionError,
    EngineResult,
    EngineSessionStatus,
)
from ai_workspace.interfaces.engine_runtime import (
    DuplicateEngineError,
    EngineTaskNotFoundError,
    NoSuitableEngineError,
)

from .fakes import FakeEngineAdapter, FakeEngineRuntime


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="Task", status=TaskStatus.TODO)


class SelectivelyFailingAdapter(EngineAdapter):
    """지정된 task_id에 대해서만 EngineExecutionError를 던지는 테스트 전용
    Adapter(M10-T01) — run_parallel()의 "개별 Task 실패 격리" 계약을
    FakeEngineRuntime으로 검증하기 위함."""

    def __init__(self, failing_task_id: str) -> None:
        self._failing_task_id = failing_task_id
        self._id_generator = itertools.count(1)

    def create_session(self) -> str:
        return f"session-{next(self._id_generator)}"

    def run(self, session_id: str, task: Task) -> EngineResult:
        if task.task_id == self._failing_task_id:
            raise EngineExecutionError(f"{task.task_id} 실행 실패")
        return EngineResult(success=True, output=f"{task.task_id} 완료")

    def cancel(self, session_id: str) -> None:
        pass

    def status(self, session_id: str) -> EngineSessionStatus:
        return EngineSessionStatus.COMPLETED

    def destroy_session(self, session_id: str) -> None:
        pass

    def capabilities(self) -> frozenset[str]:
        return frozenset()

    def supports_parallel(self) -> bool:
        return True

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=0.0)


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


def test_run_parallel_converts_individual_task_exception_to_failed_result() -> None:
    """M10-T01 계약: 개별 Task의 예외는 그 Task의 EngineResult(success=False)
    로 변환되고, 다른 Task의 결과·길이·순서는 그대로 유지되며,
    run_parallel() 자체는 예외를 던지지 않는다."""
    runtime = FakeEngineRuntime()
    runtime.register_engine("claude_code", SelectivelyFailingAdapter(failing_task_id="t2"))
    tasks = [make_task("t1"), make_task("t2"), make_task("t3")]

    results = runtime.run_parallel(tasks)

    assert len(results) == 3
    assert results[0].success is True
    assert results[1].success is False
    assert results[2].success is True
