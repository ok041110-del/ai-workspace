from __future__ import annotations

import itertools

import pytest
from tests.interfaces.fakes import FakeEngineRuntime
from tests.runtime.engine.test_managed_engine_runtime import (
    RecordingModelEngineAdapter,
    SelectivelyFailingEngineAdapter,
)

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.retry_policy import InvalidRetryPolicyError, RetryPolicy
from ai_workspace.domain.task import Task
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.engine_adapter import (
    CostEstimate,
    EngineAdapter,
    EngineExecutionError,
    EngineResult,
    EngineSessionStatus,
)
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.runtime.engine.managed_engine_runtime import ManagedEngineRuntime
from ai_workspace.runtime.engine.recovering_engine_runtime import RecoveringEngineRuntime


class EventuallySucceedingEngineAdapter(EngineAdapter):
    """지정된 task_id에 대해 처음 fail_count번은 실패하고 이후 성공하는
    테스트 전용 Adapter(M10-T03) — run_parallel()의 개별 Task 재시도를
    검증하기 위함."""

    def __init__(self, flaky_task_id: str, fail_count: int) -> None:
        self._flaky_task_id = flaky_task_id
        self._fail_count = fail_count
        self._attempts: dict[str, int] = {}
        self._id_generator = itertools.count(1)

    def create_session(self) -> str:
        return f"eventual-session-{next(self._id_generator)}"

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        if task.task_id == self._flaky_task_id:
            attempts = self._attempts.get(task.task_id, 0) + 1
            self._attempts[task.task_id] = attempts
            if attempts <= self._fail_count:
                raise EngineExecutionError(f"{task.task_id} 일시 실패({attempts}번째 시도)")
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


class MixedOutcomeEngineAdapter(EngineAdapter):
    """M10-T04 E2E: 즉시 성공/일시 실패 후 성공/영구 실패가 한 배치 안에
    섞인 시나리오를 재현하는 테스트 전용 Adapter."""

    def __init__(self, *, flaky_task_id: str, permanently_failing_task_id: str) -> None:
        self._flaky_task_id = flaky_task_id
        self._permanently_failing_task_id = permanently_failing_task_id
        self._flaky_attempts = 0
        self._id_generator = itertools.count(1)

    def create_session(self) -> str:
        return f"mixed-session-{next(self._id_generator)}"

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        if task.task_id == self._permanently_failing_task_id:
            raise EngineExecutionError(f"{task.task_id} 영구 실패")
        if task.task_id == self._flaky_task_id:
            self._flaky_attempts += 1
            if self._flaky_attempts == 1:
                raise EngineExecutionError(f"{task.task_id} 일시 실패")
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


class ScriptedEngineRuntime(EngineRuntime):
    """미리 정해진 결과/예외 시퀀스를 호출 순서대로 반환하는 테스트 더블."""

    def __init__(self, outcomes: list[EngineResult | Exception]) -> None:
        self._outcomes = list(outcomes)
        self.call_count = 0
        self._task_status: dict[str, EngineSessionStatus] = {}

    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        raise NotImplementedError

    def run(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
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
        self,
        tasks: list[Task],
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
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


def test_run_parallel_retries_individual_task_failure_until_success() -> None:
    """M10-T03: 병렬 배치 안에서 일시적으로 실패한 Task는 개별적으로
    재시도되어 성공한다 — 다른 Task는 첫 병렬 패스에서 이미 성공했으므로
    재시도를 거치지 않는다."""
    managed = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    managed.register_engine(
        "eventual", EventuallySucceedingEngineAdapter(flaky_task_id="t2", fail_count=1)
    )
    runtime = RecoveringEngineRuntime(inner=managed, retry_policy=RetryPolicy(max_attempts=3))

    results = runtime.run_parallel([make_task("t1"), make_task("t2"), make_task("t3")])

    assert [result.success for result in results] == [True, True, True]


def test_run_parallel_exhausts_retries_and_isolates_permanent_failure() -> None:
    """M10-T03: 병렬 배치 안에서 영구적으로 실패하는 Task는 재시도를
    소진한 뒤 그 Task만 실패 결과로 남고, 다른 Task의 결과는 영향받지
    않는다 — run_parallel() 자체는 예외를 던지지 않는다(이전 동작과의
    차이, M10 이전에는 이 시나리오에서 EngineExecutionError가 배치
    전체를 실패시켰다)."""
    managed = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    managed.register_engine("selective", SelectivelyFailingEngineAdapter(failing_task_id="t2"))
    runtime = RecoveringEngineRuntime(inner=managed, retry_policy=RetryPolicy(max_attempts=3))

    results = runtime.run_parallel([make_task("t1"), make_task("t2"), make_task("t3")])

    assert [result.success for result in results] == [True, False, True]


def test_run_parallel_end_to_end_mixed_outcomes_across_full_stack() -> None:
    """M10-T04: 즉시 성공/일시 실패 후 재시도로 성공/영구 실패가 한
    배치 안에 섞여도 각 Task의 최종 결과가 서로 영향을 주지 않고 올바르게
    수렴함을 ManagedEngineRuntime+RecoveringEngineRuntime 전체 스택(실제
    ThreadPoolExecutor 동시 실행 포함)으로 증명한다 — M10의 Milestone
    DoD를 하나의 시나리오로 통합 검증."""
    managed = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    managed.register_engine(
        "mixed",
        MixedOutcomeEngineAdapter(flaky_task_id="t2", permanently_failing_task_id="t3"),
    )
    runtime = RecoveringEngineRuntime(inner=managed, retry_policy=RetryPolicy(max_attempts=3))

    results = runtime.run_parallel(
        [make_task("t1"), make_task("t2"), make_task("t3"), make_task("t4")]
    )

    assert [result.success for result in results] == [True, True, False, True]


def test_run_forwards_model_through_inner_runtime_to_the_adapter() -> None:
    """Milestone 14 DoD 3번: RecoveringEngineRuntime이 model을 새로운
    선택 로직 없이 내부 Runtime까지 그대로 전달한다."""
    adapter = RecordingModelEngineAdapter()
    managed = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    managed.register_engine("mock", adapter)
    runtime = RecoveringEngineRuntime(inner=managed, retry_policy=RetryPolicy())

    runtime.run(make_task(), model="opus")

    assert adapter.received_models == ["opus"]


def test_run_parallel_forwards_model_through_inner_runtime_to_the_adapter() -> None:
    adapter = RecordingModelEngineAdapter()
    managed = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    managed.register_engine("mock", adapter)
    runtime = RecoveringEngineRuntime(inner=managed, retry_policy=RetryPolicy())

    runtime.run_parallel([make_task("t1"), make_task("t2")], model="opus")

    assert adapter.received_models == ["opus", "opus"]


def test_retry_policy_defaults_to_three_attempts() -> None:
    assert RetryPolicy().max_attempts == 3


def test_retry_policy_rejects_non_positive_max_attempts() -> None:
    with pytest.raises(InvalidRetryPolicyError):
        RetryPolicy(max_attempts=0)
