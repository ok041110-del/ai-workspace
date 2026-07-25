from __future__ import annotations

import itertools
import threading
import time

import pytest
from tests.interfaces.fakes import FailingFakeEngineAdapter

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.events.event_bus import InMemoryEventBus
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
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.engine.managed_engine_runtime import ManagedEngineRuntime


class SlowEngineAdapter(EngineAdapter):
    """`run()`이 지정된 시간만큼 지연되는 테스트 전용 Adapter — Timeout·
    실행 중 Cancel 시나리오를 재현하기 위한 것으로, 프로덕션 코드에는
    포함하지 않는다."""

    def __init__(self, delay_seconds: float) -> None:
        self._delay_seconds = delay_seconds
        self._sessions: dict[str, EngineSessionStatus] = {}

    def create_session(self) -> str:
        session_id = "slow-session"
        self._sessions[session_id] = EngineSessionStatus.RUNNING
        return session_id

    def run(self, session_id: str, task: Task) -> EngineResult:
        time.sleep(self._delay_seconds)
        self._sessions[session_id] = EngineSessionStatus.COMPLETED
        return EngineResult(success=True, output="완료")

    def cancel(self, session_id: str) -> None:
        self._sessions[session_id] = EngineSessionStatus.CANCELLED

    def status(self, session_id: str) -> EngineSessionStatus:
        return self._sessions[session_id]

    def destroy_session(self, session_id: str) -> None:
        del self._sessions[session_id]

    def capabilities(self) -> frozenset[str]:
        return frozenset({"code_generation"})

    def supports_parallel(self) -> bool:
        return False

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=0.0)


class SlowParallelEngineAdapter(EngineAdapter):
    """`SlowEngineAdapter`와 달리 세션마다 고유 ID를 발급해 `run_parallel()`의
    실제 동시 호출에 안전한 테스트 전용 Adapter(M4-T06) — `SlowEngineAdapter`
    는 세션 ID가 `"slow-session"`으로 고정되어 있어 동시 호출 시 충돌한다."""

    def __init__(self, delay_seconds: float) -> None:
        self._delay_seconds = delay_seconds
        self._sessions: dict[str, EngineSessionStatus] = {}
        self._id_generator = itertools.count(1)

    def create_session(self) -> str:
        session_id = f"slow-parallel-session-{next(self._id_generator)}"
        self._sessions[session_id] = EngineSessionStatus.RUNNING
        return session_id

    def run(self, session_id: str, task: Task) -> EngineResult:
        time.sleep(self._delay_seconds)
        self._sessions[session_id] = EngineSessionStatus.COMPLETED
        return EngineResult(success=True, output="완료")

    def cancel(self, session_id: str) -> None:
        self._sessions[session_id] = EngineSessionStatus.CANCELLED

    def status(self, session_id: str) -> EngineSessionStatus:
        return self._sessions[session_id]

    def destroy_session(self, session_id: str) -> None:
        del self._sessions[session_id]

    def capabilities(self) -> frozenset[str]:
        return frozenset({"code_generation"})

    def supports_parallel(self) -> bool:
        return True

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=0.0)


class SelectivelyFailingEngineAdapter(EngineAdapter):
    """지정된 task_id에 대해서만 `EngineExecutionError`를 던지는 테스트 전용
    Adapter(M4-T06) — `run_parallel()`에서 한 Task의 실패가 다른 Task의
    독립적인 실행을 막지 않음을 증명하기 위함."""

    def __init__(self, failing_task_id: str) -> None:
        self._failing_task_id = failing_task_id
        self._sessions: dict[str, EngineSessionStatus] = {}
        self._id_generator = itertools.count(1)

    def create_session(self) -> str:
        session_id = f"selective-session-{next(self._id_generator)}"
        self._sessions[session_id] = EngineSessionStatus.RUNNING
        return session_id

    def run(self, session_id: str, task: Task) -> EngineResult:
        if task.task_id == self._failing_task_id:
            self._sessions[session_id] = EngineSessionStatus.FAILED
            raise EngineExecutionError(f"{task.task_id} 실행 실패")
        self._sessions[session_id] = EngineSessionStatus.COMPLETED
        return EngineResult(success=True, output="완료")

    def cancel(self, session_id: str) -> None:
        self._sessions[session_id] = EngineSessionStatus.CANCELLED

    def status(self, session_id: str) -> EngineSessionStatus:
        return self._sessions[session_id]

    def destroy_session(self, session_id: str) -> None:
        del self._sessions[session_id]

    def capabilities(self) -> frozenset[str]:
        return frozenset({"code_generation"})

    def supports_parallel(self) -> bool:
        return True

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=0.0)


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="구현하기", status=TaskStatus.TODO)


def test_run_executes_task_via_mock_adapter_and_returns_success() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())

    result = runtime.run(make_task())

    assert result.success is True


def test_register_engine_twice_raises_duplicate_error() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())

    with pytest.raises(DuplicateEngineError):
        runtime.register_engine("mock2", MockEngineAdapter())


def test_run_without_registered_engine_raises_no_suitable_engine() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task())


def test_run_capability_mismatch_raises_no_suitable_engine() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task(), required_capabilities=frozenset({"vision"}))


def test_status_reflects_completed_after_successful_run() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())
    task = make_task()

    runtime.run(task)

    assert runtime.status(task.task_id) == EngineSessionStatus.COMPLETED


def test_engine_execution_error_propagates() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("failing", FailingFakeEngineAdapter())

    with pytest.raises(Exception):
        runtime.run(make_task())


def test_status_unknown_task_raises_not_found() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())

    with pytest.raises(EngineTaskNotFoundError):
        runtime.status("unknown")


def test_cancel_unknown_task_raises_not_found() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())

    with pytest.raises(EngineTaskNotFoundError):
        runtime.cancel("unknown")


def test_cancel_after_completion_marks_status_cancelled() -> None:
    """interfaces/engine_runtime.py의 cancel() 계약은 EngineAdapter.cancel()
    과 달리 "이미 완료된 실행은 상태 유지" 조항이 없다 — cancel(task_id)
    이후 status(task_id)는 예외 없이 항상 CANCELLED다(M3-T03에서
    EngineAdapter.cancel()과 혼동해 이 동작을 "버그"로 오판할 뻔했으나,
    두 인터페이스의 계약 문서를 재확인해 EngineRuntime 쪽은 원래
    구현이 맞다는 것을 확인함)."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())
    task = make_task()
    runtime.run(task)

    runtime.cancel(task.task_id)

    assert runtime.status(task.task_id) == EngineSessionStatus.CANCELLED


def test_run_publishes_started_and_completed_events() -> None:
    event_bus = InMemoryEventBus()
    received: list[Event] = []
    event_bus.subscribe(received.append)
    runtime = ManagedEngineRuntime(event_bus=event_bus)
    runtime.register_engine("mock", MockEngineAdapter())

    runtime.run(make_task())

    event_types = {event.event_type for event in received}
    assert event_types == {"engine_task_started", "engine_task_completed"}


def test_run_timeout_returns_failure_and_marks_status_failed() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("slow", SlowEngineAdapter(delay_seconds=0.3))
    task = make_task()

    result = runtime.run(task, timeout_seconds=0.05)

    assert result.success is False
    assert result.error == "timeout"
    assert runtime.status(task.task_id) == EngineSessionStatus.FAILED


def test_run_timeout_publishes_timeout_event() -> None:
    event_bus = InMemoryEventBus()
    received: list[Event] = []
    event_bus.subscribe(received.append)
    runtime = ManagedEngineRuntime(event_bus=event_bus)
    runtime.register_engine("slow", SlowEngineAdapter(delay_seconds=0.3))

    runtime.run(make_task(), timeout_seconds=0.05)

    assert "engine_task_timeout" in {event.event_type for event in received}


def test_cancel_while_running_overrides_completion_result() -> None:
    """실행 도중 cancel()이 호출되면 이후 완료되더라도 결과가 취소로
    반영됨을 확인한다(구조 검증 — 실제 스레드를 강제 종료하지는 않는다)."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("slow", SlowEngineAdapter(delay_seconds=0.2))
    task = make_task()
    outcome: dict[str, EngineResult] = {}

    def _run() -> None:
        outcome["result"] = runtime.run(task, timeout_seconds=2.0)

    runner = threading.Thread(target=_run)
    runner.start()
    time.sleep(0.05)
    runtime.cancel(task.task_id)
    runner.join()

    assert outcome["result"].success is False
    assert outcome["result"].error == "cancelled"


def test_run_parallel_preserves_order() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())
    tasks = [make_task("t1"), make_task("t2"), make_task("t3")]

    results = runtime.run_parallel(tasks)

    assert [result.success for result in results] == [True, True, True]


def test_run_parallel_executes_tasks_concurrently() -> None:
    """M4-T06/ADR-0023: `run_parallel()`이 실제로 동시에 실행됨을 시간으로
    증명한다 — 순차 실행이라면 3 * delay 이상 걸리지만, 실제 동시 실행이면
    delay 1회 분량에 가깝게 끝난다."""
    delay_seconds = 0.2
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("slow", SlowParallelEngineAdapter(delay_seconds))
    tasks = [make_task("t1"), make_task("t2"), make_task("t3")]

    started = time.monotonic()
    results = runtime.run_parallel(tasks)
    elapsed = time.monotonic() - started

    assert [result.success for result in results] == [True, True, True]
    assert elapsed < delay_seconds * 2  # 순차였다면 0.6초 이상, 동시면 0.2초 근처


def test_run_parallel_preserves_input_order_even_with_uneven_delays() -> None:
    """작업마다 소요 시간이 달라도(먼저 제출된 것이 늦게 끝나도) 반환
    목록은 입력 순서를 그대로 따른다(완료 순서가 아님, EngineRuntime
    계약 그대로)."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("slow", SlowParallelEngineAdapter(0.05))
    tasks = [make_task("t1"), make_task("t2"), make_task("t3")]

    results = runtime.run_parallel(tasks)

    assert runtime.status("t1") == EngineSessionStatus.COMPLETED
    assert runtime.status("t2") == EngineSessionStatus.COMPLETED
    assert runtime.status("t3") == EngineSessionStatus.COMPLETED
    assert len(results) == 3


def test_run_parallel_independent_failure_does_not_block_others() -> None:
    """한 Task의 실행이 실패(예외)해도 다른 Task는 이미 동시에 제출되어
    독립적으로 실행이 끝난다 — `ThreadPoolExecutor`의 `with` 블록이
    종료되며 모든 제출된 작업의 완료를 기다리기 때문에, 예외가 전파될
    시점에는 다른 Task들도 이미 완료 상태다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("selective", SelectivelyFailingEngineAdapter(failing_task_id="t2"))
    tasks = [make_task("t1"), make_task("t2"), make_task("t3")]

    with pytest.raises(EngineExecutionError):
        runtime.run_parallel(tasks)

    assert runtime.status("t1") == EngineSessionStatus.COMPLETED
    assert runtime.status("t2") == EngineSessionStatus.FAILED
    assert runtime.status("t3") == EngineSessionStatus.COMPLETED


def test_run_parallel_empty_list_returns_empty_list() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())

    assert runtime.run_parallel([]) == []
