from __future__ import annotations

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
