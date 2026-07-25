from __future__ import annotations

import pytest
from tests.interfaces.fakes import FakeEngineRuntime
from tests.runtime.engine.test_managed_engine_runtime import SelectivelyFailingEngineAdapter

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.retry_policy import InvalidRetryPolicyError, RetryPolicy
from ai_workspace.domain.task import Task
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.engine_adapter import (
    EngineAdapter,
    EngineExecutionError,
    EngineResult,
    EngineSessionStatus,
)
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.runtime.engine.managed_engine_runtime import ManagedEngineRuntime
from ai_workspace.runtime.engine.recovering_engine_runtime import RecoveringEngineRuntime


class ScriptedEngineRuntime(EngineRuntime):
    """미리 정해진 결과/예외 시퀀스를 호출 순서대로 반환하는 테스트 더블."""

    def __init__(self, outcomes: list[EngineResult | Exception]) -> None:
        self._outcomes = list(outcomes)
        self.call_count = 0
        self._task_status: dict[str, EngineSessionStatus] = {}

    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        raise NotImplementedError

    def run(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> EngineResult:
        outcome = self._outcomes[self.call_count]
        self.call_count += 1
        if isinstance(outcome, Exception):
            raise outcome
        self._task_status[task.task_id] = (
            EngineSessionStatus.COMPLETED if outcome.success else EngineSessionStatus.FAILED
        )
        return outcome

    def run_parallel(
        self, tasks: list[Task], required_capabilities: frozenset[str] = frozenset()
    ) -> list[EngineResult]:
        raise NotImplementedError

    def cancel(self, task_id: str) -> None:
        self._task_status[task_id] = EngineSessionStatus.CANCELLED

    def status(self, task_id: str) -> EngineSessionStatus:
        return self._task_status[task_id]


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="demo")


def test_run_returns_first_success_without_retrying() -> None:
    inner = ScriptedEngineRuntime([EngineResult(success=True, output="ok")])
    runtime = RecoveringEngineRuntime(inner=inner, retry_policy=RetryPolicy(max_attempts=3))

    result = runtime.run(make_task())

    assert result.success is True
    assert inner.call_count == 1


def test_run_retries_after_failed_result_then_succeeds() -> None:
    inner = ScriptedEngineRuntime(
        [
            EngineResult(success=False, output="", error="fail"),
            EngineResult(success=True, output="ok"),
        ]
    )
    runtime = RecoveringEngineRuntime(inner=inner, retry_policy=RetryPolicy(max_attempts=3))

    result = runtime.run(make_task())

    assert result.success is True
    assert inner.call_count == 2


def test_run_returns_last_failed_result_after_exhausting_retries() -> None:
    outcomes = [EngineResult(success=False, output="", error=f"fail-{i}") for i in range(3)]
    inner = ScriptedEngineRuntime(outcomes)
    runtime = RecoveringEngineRuntime(inner=inner, retry_policy=RetryPolicy(max_attempts=3))

    result = runtime.run(make_task())

    assert result.success is False
    assert result.error == "fail-2"
    assert inner.call_count == 3


def test_run_retries_after_exception_then_succeeds() -> None:
    inner = ScriptedEngineRuntime([ValueError("boom"), EngineResult(success=True, output="ok")])
    runtime = RecoveringEngineRuntime(inner=inner, retry_policy=RetryPolicy(max_attempts=3))

    result = runtime.run(make_task())

    assert result.success is True
    assert inner.call_count == 2


def test_run_reraises_last_exception_after_exhausting_retries() -> None:
    inner = ScriptedEngineRuntime([ValueError("first"), ValueError("last")])
    runtime = RecoveringEngineRuntime(inner=inner, retry_policy=RetryPolicy(max_attempts=2))

    with pytest.raises(ValueError, match="last"):
        runtime.run(make_task())
    assert inner.call_count == 2


def test_status_delegates_to_inner_runtime() -> None:
    inner = FakeEngineRuntime()
    inner.register_engine("mock", MockEngineAdapter())
    runtime = RecoveringEngineRuntime(inner=inner, retry_policy=RetryPolicy())
    runtime.run(make_task("t1"))

    assert runtime.status("t1") == inner.status("t1")


def test_cancel_delegates_to_inner_runtime() -> None:
    inner = FakeEngineRuntime()
    inner.register_engine("mock", MockEngineAdapter())
    runtime = RecoveringEngineRuntime(inner=inner, retry_policy=RetryPolicy())
    runtime.run(make_task("t1"))

    runtime.cancel("t1")

    assert inner.status("t1") == EngineSessionStatus.CANCELLED


def test_register_engine_delegates_to_inner_runtime() -> None:
    inner = FakeEngineRuntime()
    runtime = RecoveringEngineRuntime(inner=inner, retry_policy=RetryPolicy())

    runtime.register_engine("mock", MockEngineAdapter())
    result = runtime.run(make_task())

    assert result.success is True


def test_run_parallel_delegates_to_inner_runtime() -> None:
    inner = FakeEngineRuntime()
    inner.register_engine("mock", MockEngineAdapter())
    runtime = RecoveringEngineRuntime(inner=inner, retry_policy=RetryPolicy())

    results = runtime.run_parallel([make_task("t1"), make_task("t2")])

    assert [r.success for r in results] == [True, True]


def test_run_parallel_does_not_retry_individual_task_failures() -> None:
    """ADR-0023/M4-T06으로 확인·기록한 알려진 범위: `run_parallel()`은
    `inner.run_parallel()`에 그대로 위임하며 `self.run()`의 재시도 로직을
    거치지 않는다 — 따라서 병렬 배치 안의 개별 Task 실패는
    `RecoveringEngineRuntime`을 통해서도 재시도되지 않는다(단일 `run()`
    호출과의 차이점, 필요 시 이후 Task로 이월)."""
    managed = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    managed.register_engine("selective", SelectivelyFailingEngineAdapter(failing_task_id="t2"))
    runtime = RecoveringEngineRuntime(inner=managed, retry_policy=RetryPolicy(max_attempts=3))

    with pytest.raises(EngineExecutionError):
        runtime.run_parallel([make_task("t1"), make_task("t2"), make_task("t3")])


def test_retry_policy_defaults_to_three_attempts() -> None:
    assert RetryPolicy().max_attempts == 3


def test_retry_policy_rejects_non_positive_max_attempts() -> None:
    with pytest.raises(InvalidRetryPolicyError):
        RetryPolicy(max_attempts=0)
