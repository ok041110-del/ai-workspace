from __future__ import annotations

import itertools
import threading
import time

import pytest
from tests.interfaces.fakes import FailingFakeEngineAdapter

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.budget import Budget
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.budget_policy_engine import InMemoryBudgetPolicyEngine
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
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


class CostedEngineAdapter(MockEngineAdapter):
    """M64: `estimate_cost()`가 고정 비용을 반환하고 `run()` 호출 여부를
    기록하는 테스트용 Adapter — 비용 기반 선택을 테스트에서 재현할 수
    있게 한다. M65: `succeed=False`면 계속 실패해 신뢰도 추적을
    재현할 수 있다."""

    def __init__(
        self,
        estimated_cost_usd: float,
        capabilities: frozenset[str] = frozenset(),
        *,
        succeed: bool = True,
    ) -> None:
        super().__init__(capabilities)
        self._estimated_cost_usd = estimated_cost_usd
        self._succeed = succeed
        self.run_count = 0

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        self.run_count += 1
        if not self._succeed:
            if session_id not in self._sessions:
                raise ValueError("unknown session")
            self._sessions[session_id] = EngineSessionStatus.COMPLETED
            return EngineResult(success=False, output="", error="mock failure")
        return super().run(session_id, task, model=model)

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=self._estimated_cost_usd)


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

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
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

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
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

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
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


class RecordingEngineAdapter(EngineAdapter):
    """호출 횟수를 기록하는 테스트 전용 Adapter(M6-T01) — 여러 어댑터가
    등록되어 있을 때 실제로 어느 어댑터가 선택·실행되었는지 증명하기
    위함(`MockEngineAdapter`는 어느 인스턴스가 실행됐는지 구분할 방법이
    없어 별도로 둔다)."""

    def __init__(self, capabilities: frozenset[str]) -> None:
        self._capabilities = capabilities
        self._sessions: dict[str, EngineSessionStatus] = {}
        self._id_generator = itertools.count(1)
        self.run_count = 0

    def create_session(self) -> str:
        session_id = f"recording-session-{next(self._id_generator)}"
        self._sessions[session_id] = EngineSessionStatus.RUNNING
        return session_id

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        self.run_count += 1
        self._sessions[session_id] = EngineSessionStatus.COMPLETED
        return EngineResult(success=True, output=f"{task.task_id} 완료(Recording)")

    def cancel(self, session_id: str) -> None:
        self._sessions[session_id] = EngineSessionStatus.CANCELLED

    def status(self, session_id: str) -> EngineSessionStatus:
        return self._sessions[session_id]

    def destroy_session(self, session_id: str) -> None:
        del self._sessions[session_id]

    def capabilities(self) -> frozenset[str]:
        return self._capabilities

    def supports_parallel(self) -> bool:
        return False

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=0.0)


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="구현하기", status=TaskStatus.TODO)


class RecordingModelEngineAdapter(MockEngineAdapter):
    """`run()`에 전달된 model을 기록하는 테스트 전용 Adapter(M14-T02) —
    `ManagedEngineRuntime`이 model을 그대로 전달만 하는지 확인하는 데
    쓰인다."""

    def __init__(self) -> None:
        super().__init__()
        self.received_models: list[str | None] = []

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        self.received_models.append(model)
        return super().run(session_id, task, model=model)


def test_run_forwards_model_to_the_adapter() -> None:
    adapter = RecordingModelEngineAdapter()
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", adapter)

    runtime.run(make_task(), model="opus")

    assert adapter.received_models == ["opus"]


def test_run_parallel_forwards_model_to_the_adapter() -> None:
    adapter = RecordingModelEngineAdapter()
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", adapter)

    runtime.run_parallel([make_task("t1"), make_task("t2")], model="opus")

    assert adapter.received_models == ["opus", "opus"]


def test_run_executes_task_via_mock_adapter_and_returns_success() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())

    result = runtime.run(make_task())

    assert result.success is True


def test_register_engine_same_name_twice_raises_duplicate_error() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())

    with pytest.raises(DuplicateEngineError):
        runtime.register_engine("mock", MockEngineAdapter())


def test_register_engine_with_different_names_both_succeed() -> None:
    """M6-T01: 서로 다른 이름이면 여러 EngineAdapter를 동시에 등록할 수
    있다 — 이전에는 두 번째 register_engine() 호출부터 무조건
    DuplicateEngineError였다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock1", MockEngineAdapter(frozenset({"claude_code"})))
    runtime.register_engine("mock2", MockEngineAdapter(frozenset({"codex"})))

    assert runtime.run(make_task(), required_capabilities=frozenset({"claude_code"})).success
    assert runtime.run(make_task("t2"), required_capabilities=frozenset({"codex"})).success


def test_run_selects_matching_adapter_among_multiple_registered() -> None:
    """M6-T01: 여러 어댑터가 등록되어 있을 때 required_capabilities를
    만족하는 어댑터가 실제로 선택되어 실행됨을 증명한다(다른 어댑터는
    호출되지 않음)."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    claude_adapter = RecordingEngineAdapter(frozenset({"claude_code"}))
    codex_adapter = RecordingEngineAdapter(frozenset({"codex"}))
    runtime.register_engine("claude_code", claude_adapter)
    runtime.register_engine("codex", codex_adapter)

    result = runtime.run(make_task(), required_capabilities=frozenset({"codex"}))

    assert result.success is True
    assert codex_adapter.run_count == 1
    assert claude_adapter.run_count == 0


def test_run_no_matching_adapter_among_multiple_raises_no_suitable_engine() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("claude_code", MockEngineAdapter(frozenset({"claude_code"})))
    runtime.register_engine("codex", MockEngineAdapter(frozenset({"codex"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task(), required_capabilities=frozenset({"gemini_cli"}))


def test_run_without_registered_engine_raises_no_suitable_engine() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task())


def test_run_capability_mismatch_raises_no_suitable_engine() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task(), required_capabilities=frozenset({"vision"}))


def test_estimate_cost_selects_matching_adapter_without_creating_a_session() -> None:
    """M15-T02: estimate_cost()는 run()과 같은 선택 규칙을 쓰되, 세션을
    만들거나 실제로 실행하지 않는다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    claude_adapter = RecordingEngineAdapter(frozenset({"claude_code"}))
    codex_adapter = RecordingEngineAdapter(frozenset({"codex"}))
    runtime.register_engine("claude_code", claude_adapter)
    runtime.register_engine("codex", codex_adapter)

    estimate = runtime.estimate_cost(make_task(), required_capabilities=frozenset({"codex"}))

    assert estimate == codex_adapter.estimate_cost(make_task())
    assert codex_adapter.run_count == 0
    assert claude_adapter.run_count == 0


def test_estimate_cost_raises_no_suitable_engine_when_capability_unmatched() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.estimate_cost(make_task(), required_capabilities=frozenset({"vision"}))


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


def test_run_parallel_independent_failure_does_not_lose_other_results() -> None:
    """M10-T02: 한 Task의 실행이 실패(예외)해도 다른 Task의 결과는
    유실되지 않는다 — 이전에는 예외가 run_parallel() 밖으로 그대로
    전파되어 이미 완료된 다른 Task의 결과까지 전부 잃었다(M10 이전
    버그). 이제는 실패한 Task만 EngineResult(success=False)로 변환되고
    나머지는 정상 결과를 그대로 반환한다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("selective", SelectivelyFailingEngineAdapter(failing_task_id="t2"))
    tasks = [make_task("t1"), make_task("t2"), make_task("t3")]

    results = runtime.run_parallel(tasks)

    assert len(results) == 3
    assert results[0].success is True
    assert results[1].success is False
    assert results[2].success is True
    assert runtime.status("t1") == EngineSessionStatus.COMPLETED
    assert runtime.status("t2") == EngineSessionStatus.FAILED
    assert runtime.status("t3") == EngineSessionStatus.COMPLETED


def test_run_parallel_without_suitable_engine_raises_before_any_execution() -> None:
    """M10-T01 계약: 개별 Task 실패는 삼키지만, Runtime 자체의 치명적
    오류(요구 Capability를 만족하는 엔진이 아예 없음)는 여전히
    NoSuitableEngineError로 즉시 전파된다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"claude_code"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.run_parallel([make_task()], required_capabilities=frozenset({"codex"}))


def test_run_parallel_empty_list_returns_empty_list() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())

    assert runtime.run_parallel([]) == []


def test_run_ensemble_runs_same_task_via_each_named_engine() -> None:
    """M62(ADR-0080): 같은 Task를 여러 등록된 엔진 이름으로 동시에 돌려
    이름별로 비교 가능한 결과를 얻는다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("claude", MockEngineAdapter())
    runtime.register_engine("codex", MockEngineAdapter())
    runtime.register_engine("gemini", MockEngineAdapter())

    results = runtime.run_ensemble(make_task(), ["claude", "codex", "gemini"])

    assert set(results) == {"claude", "codex", "gemini"}
    assert all(result.success for result in results.values())


def test_run_ensemble_executes_engines_concurrently() -> None:
    """`run_parallel()`이 여러 Task를 동시에 돌리듯, `run_ensemble()`도
    같은 Task를 여러 엔진에서 실제로 동시에 실행함을 시간으로 증명한다."""
    delay_seconds = 0.2
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("a", SlowParallelEngineAdapter(delay_seconds))
    runtime.register_engine("b", SlowParallelEngineAdapter(delay_seconds))
    runtime.register_engine("c", SlowParallelEngineAdapter(delay_seconds))

    started = time.monotonic()
    results = runtime.run_ensemble(make_task(), ["a", "b", "c"])
    elapsed = time.monotonic() - started

    assert all(result.success for result in results.values())
    assert elapsed < delay_seconds * 2


def test_run_ensemble_isolates_individual_engine_failure() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("ok", MockEngineAdapter())
    runtime.register_engine("broken", FailingFakeEngineAdapter())

    results = runtime.run_ensemble(make_task(), ["ok", "broken"])

    assert results["ok"].success is True
    assert results["broken"].success is False


def test_run_ensemble_unregistered_name_yields_failed_result_not_exception() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("ok", MockEngineAdapter())

    results = runtime.run_ensemble(make_task(), ["ok", "missing"])

    assert results["ok"].success is True
    assert results["missing"].success is False


def test_run_ensemble_empty_names_returns_empty_dict() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())

    assert runtime.run_ensemble(make_task(), []) == {}


def test_run_ensemble_does_not_affect_run_task_status_tracking() -> None:
    """`run_ensemble()`은 `status(task_id)`(1개 task_id당 1개 상태만
    추적)와 의미가 충돌하므로 이 추적에 전혀 관여하지 않는다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("a", MockEngineAdapter())
    task = make_task()

    runtime.run_ensemble(task, ["a"])

    with pytest.raises(EngineTaskNotFoundError):
        runtime.status(task.task_id)


def test_run_without_policy_picks_first_registered_matching_adapter() -> None:
    """M64 이전과 100% 동일 동작(회귀 확인): policy 미주입 시 등록 순서상
    첫 매칭을 그대로 고른다 — 비용이 더 낮은 두 번째 엔진을 무시한다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    expensive_first = CostedEngineAdapter(10.0)
    cheap_second = CostedEngineAdapter(1.0)
    runtime.register_engine("expensive", expensive_first)
    runtime.register_engine("cheap", cheap_second)

    runtime.run(make_task())

    assert expensive_first.run_count == 1
    assert cheap_second.run_count == 0


def test_run_with_policy_selects_cheapest_registered_adapter() -> None:
    """M64(ADR-0082): engine_selection_policy를 주입하면 등록 순서와
    무관하게 예상 비용이 가장 낮은 엔진이 선택된다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
    )
    expensive_first = CostedEngineAdapter(10.0)
    cheap_second = CostedEngineAdapter(1.0)
    runtime.register_engine("expensive", expensive_first)
    runtime.register_engine("cheap", cheap_second)

    runtime.run(make_task())

    assert expensive_first.run_count == 0
    assert cheap_second.run_count == 1


def test_run_with_policy_and_budget_excludes_over_budget_candidate() -> None:
    """M64: budget_policy_engine을 함께 주입하면 예산을 초과하는 후보는
    선택 대상에서 제외된다."""
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=5.0))
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
        budget_policy_engine=budget_policy_engine,
    )
    over_budget = CostedEngineAdapter(10.0)
    cheapest_within_budget = CostedEngineAdapter(1.0)
    pricier_within_budget = CostedEngineAdapter(4.0)
    runtime.register_engine("over_budget", over_budget)
    runtime.register_engine("pricier_within_budget", pricier_within_budget)
    runtime.register_engine("cheapest_within_budget", cheapest_within_budget)

    runtime.run(make_task())

    assert over_budget.run_count == 0
    assert pricier_within_budget.run_count == 0
    assert cheapest_within_budget.run_count == 1


def test_run_raises_no_suitable_engine_when_no_candidate_within_budget() -> None:
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=1.0))
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
        budget_policy_engine=budget_policy_engine,
    )
    runtime.register_engine("too_expensive", CostedEngineAdapter(5.0))

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task())


def test_run_parallel_with_policy_selects_cheapest_adapter_for_batch() -> None:
    """M64: run_parallel()의 사전 검사도 비용 기반 선택을 거친다 —
    각 Task는 여전히 self.run()을 통해 개별적으로 비용 평가·선택된다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
    )
    expensive = CostedEngineAdapter(10.0)
    cheap = CostedEngineAdapter(1.0)
    runtime.register_engine("expensive", expensive)
    runtime.register_engine("cheap", cheap)
    tasks = [make_task("t1"), make_task("t2")]

    results = runtime.run_parallel(tasks)

    assert [result.success for result in results] == [True, True]
    assert expensive.run_count == 0
    assert cheap.run_count == 2


def test_run_with_policy_excludes_engine_after_repeated_failures() -> None:
    """M65(ADR-0083): 성공 0건 + 표본 3건 이상(M49와 동일한 임계값) 쌓인
    엔진은 비용이 가장 싸도 더 이상 선택되지 않는다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
    )
    failing_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("failing_cheap", failing_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    for i in range(3):
        runtime.run(make_task(f"warmup-{i}"))

    assert failing_cheap.run_count == 3
    assert reliable_expensive.run_count == 0

    runtime.run(make_task("after-exclusion"))

    assert failing_cheap.run_count == 3
    assert reliable_expensive.run_count == 1


def test_run_with_policy_does_not_exclude_engine_with_insufficient_sample() -> None:
    """실패가 1~2건뿐이면(표본 부족) 아직 제외되지 않는다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
    )
    failing_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("failing_cheap", failing_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    runtime.run(make_task("warmup-0"))
    runtime.run(make_task("warmup-1"))

    assert failing_cheap.run_count == 2
    assert reliable_expensive.run_count == 0


def test_run_with_policy_reprobes_excluded_engine_after_probe_interval() -> None:
    """M66(ADR-0084): 제외된 엔진도 `_PROBE_INTERVAL`(5)번 연속 건너뛰면
    다음 선택에서 다시 후보로 포함되어 복구 여부를 재확인한다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
    )
    failing_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("failing_cheap", failing_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    for i in range(3):
        runtime.run(make_task(f"warmup-{i}"))
    assert failing_cheap.run_count == 3

    for i in range(5):
        runtime.run(make_task(f"skip-{i}"))
    assert failing_cheap.run_count == 3
    assert reliable_expensive.run_count == 5

    runtime.run(make_task("probe"))

    assert failing_cheap.run_count == 4


def test_run_with_policy_recovers_after_successful_probe() -> None:
    """M66: probe 실행이 성공하면 `is_unreliable()`이 거짓이 되어 이후
    다시 정상적으로 선택된다(비용이 가장 싸므로)."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
    )
    recovering_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("recovering_cheap", recovering_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    for i in range(3):
        runtime.run(make_task(f"warmup-{i}"))
    for i in range(5):
        runtime.run(make_task(f"skip-{i}"))

    recovering_cheap._succeed = True
    runtime.run(make_task("probe"))

    assert recovering_cheap.run_count == 4

    runtime.run(make_task("after-recovery"))

    assert recovering_cheap.run_count == 5
    assert reliable_expensive.run_count == 5


def test_run_without_policy_does_not_apply_reliability_exclusion() -> None:
    """M65 이전과 100% 동일 동작(회귀 확인): policy 미주입 시 계속 실패하는
    엔진도 그대로 계속 선택된다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    failing_only = CostedEngineAdapter(1.0, succeed=False)
    runtime.register_engine("failing_only", failing_only)

    for i in range(5):
        runtime.run(make_task(f"t{i}"))

    assert failing_only.run_count == 5


def test_run_ensemble_auto_without_policy_picks_first_n_matching_registered_order() -> None:
    """M68: policy 미주입 시 등록 순서상 조건을 만족하는 첫 top_n개를
    고른다 — run()의 정책 미주입 동작과 동일한 원칙."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("first", MockEngineAdapter())
    runtime.register_engine("second", MockEngineAdapter())
    runtime.register_engine("third", MockEngineAdapter())

    results = runtime.run_ensemble_auto(make_task(), top_n=2)

    assert set(results) == {"first", "second"}


def test_run_ensemble_auto_with_policy_selects_cheapest_n_candidates() -> None:
    """M68(ADR-0086): engine_selection_policy를 주입하면 비용이 낮은
    순서로 top_n개를 동적으로 고른다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(), engine_selection_policy=InMemoryEngineSelectionPolicy()
    )
    runtime.register_engine("expensive", CostedEngineAdapter(10.0))
    runtime.register_engine("cheapest", CostedEngineAdapter(1.0))
    runtime.register_engine("middle", CostedEngineAdapter(5.0))

    results = runtime.run_ensemble_auto(make_task(), top_n=2)

    assert set(results) == {"cheapest", "middle"}


def test_run_ensemble_auto_filters_by_required_capabilities() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("vision", MockEngineAdapter(frozenset({"vision"})))
    runtime.register_engine("code", MockEngineAdapter(frozenset({"code_generation"})))

    results = runtime.run_ensemble_auto(
        make_task(), required_capabilities=frozenset({"code_generation"}), top_n=5
    )

    assert set(results) == {"code"}


def test_run_ensemble_auto_returns_fewer_than_top_n_when_not_enough_candidates() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("only", MockEngineAdapter())

    results = runtime.run_ensemble_auto(make_task(), top_n=5)

    assert set(results) == {"only"}


def test_run_ensemble_auto_raises_no_suitable_engine_when_no_candidate_matches() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.run_ensemble_auto(make_task(), required_capabilities=frozenset({"vision"}))


def test_run_ensemble_auto_with_top_n_below_one_returns_empty_dict() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    runtime.register_engine("mock", MockEngineAdapter())

    assert runtime.run_ensemble_auto(make_task(), top_n=0) == {}


def test_run_ensemble_auto_excludes_unreliable_engine_with_policy() -> None:
    """M68이 M65/M66의 신뢰도 기반 제외 규칙을 그대로 적용받는지 확인한다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(), engine_selection_policy=InMemoryEngineSelectionPolicy()
    )
    failing_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("failing_cheap", failing_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    for i in range(3):
        runtime.run(make_task(f"t{i}"))
    assert failing_cheap.run_count == 3

    results = runtime.run_ensemble_auto(make_task("after"), top_n=2)

    assert set(results) == {"reliable_expensive"}


def test_run_with_policy_prefers_proven_success_over_untested_on_cost_tie() -> None:
    """M69(ADR-0087): 같은 비용(tie)에서, 이미 같은 required_capabilities
    조합으로 3회 이상 성공한 "검증된" 엔진이 아직 한 번도 실행된 적
    없는 "미검증" 엔진보다 tie-break에서 우선한다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(), engine_selection_policy=InMemoryEngineSelectionPolicy()
    )
    proven = CostedEngineAdapter(1.0)
    runtime.register_engine("proven", proven)
    for i in range(3):
        runtime.run(make_task(f"seed-{i}"))
    assert proven.run_count == 3

    untested = CostedEngineAdapter(1.0)
    runtime.register_engine("untested", untested)

    runtime.run(make_task("tie"))

    assert proven.run_count == 4
    assert untested.run_count == 0


def test_run_with_policy_prefers_untested_over_proven_failure_on_cost_tie() -> None:
    """M69(ADR-0087): 반대로, 같은 비용(tie)에서 검증된 이력이 "전량
    실패"라면 아직 미검증인 엔진이 오히려 우선한다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(), engine_selection_policy=InMemoryEngineSelectionPolicy()
    )
    proven_bad = CostedEngineAdapter(1.0, succeed=False)
    runtime.register_engine("proven_bad", proven_bad)
    for i in range(2):
        runtime.run(make_task(f"seed-{i}"))
    assert proven_bad.run_count == 2

    untested = CostedEngineAdapter(1.0)
    runtime.register_engine("untested", untested)

    runtime.run(make_task("still-unknown"))
    assert proven_bad.run_count == 3
    assert untested.run_count == 0

    runtime.run(make_task("now-known-bad"))
    assert proven_bad.run_count == 3
    assert untested.run_count == 1


def test_consensus_weight_defaults_to_neutral_when_no_history() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())

    assert runtime.consensus_weight(frozenset({"code"}), "claude") == 0.5


def test_consensus_weight_reflects_agreement_rate_once_sample_sufficient() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    caps = frozenset({"code"})

    for _ in range(3):
        runtime.record_consensus_outcome(caps, ("claude",), ())
    runtime.record_consensus_outcome(caps, (), ("claude",))

    assert runtime.consensus_weight(caps, "claude") == 0.75


def test_record_consensus_outcome_only_updates_named_engines() -> None:
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    caps = frozenset({"code"})

    for _ in range(3):
        runtime.record_consensus_outcome(caps, ("claude",), ("codex",))

    assert runtime.consensus_weight(caps, "claude") == 1.0
    assert runtime.consensus_weight(caps, "codex") == 0.0
    assert runtime.consensus_weight(caps, "gemini") == 0.5


class CountingSlowEngineAdapter(SlowParallelEngineAdapter):
    """M74(ADR-0092) 테스트용 — `SlowParallelEngineAdapter`에 호출 횟수
    카운터를 더한다. `run_parallel()`은 각 Task마다 별도 스레드에서
    `run()`을 호출하므로 카운터 증가도 Lock으로 보호한다."""

    def __init__(self, delay_seconds: float) -> None:
        super().__init__(delay_seconds)
        self._count_lock = threading.Lock()
        self.run_count = 0

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        with self._count_lock:
            self.run_count += 1
        return super().run(session_id, task, model=model)


def test_run_parallel_falls_back_to_other_engine_when_provider_at_capacity() -> None:
    """M74(ADR-0092): engine-a에 `max_concurrency=1`을 지정하면, 실제
    `ThreadPoolExecutor`로 동시에 제출된 두 Task 중 하나만 engine-a를
    쓰고 나머지는 자동으로 engine-b로 fallback한다 — 둘 다 실패 없이
    완료된다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    engine_a = CountingSlowEngineAdapter(delay_seconds=0.2)
    engine_b = CountingSlowEngineAdapter(delay_seconds=0.05)
    runtime.register_engine("engine-a", engine_a, max_concurrency=1)
    runtime.register_engine("engine-b", engine_b)
    tasks = [make_task("t1"), make_task("t2")]

    results = runtime.run_parallel(tasks)

    assert [result.success for result in results] == [True, True]
    assert engine_a.run_count == 1
    assert engine_b.run_count == 1


def test_run_parallel_uses_only_engine_when_capacity_allows_both() -> None:
    """M74 이전과 100% 동일 동작(회귀 확인): `max_concurrency`가 두 Task를
    모두 수용할 만큼 넉넉하면(또는 지정하지 않으면), 등록 순서상 첫
    후보가 그대로 두 Task 모두에 선택된다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    engine_a = CountingSlowEngineAdapter(delay_seconds=0.05)
    engine_b = CountingSlowEngineAdapter(delay_seconds=0.05)
    runtime.register_engine("engine-a", engine_a, max_concurrency=2)
    runtime.register_engine("engine-b", engine_b)
    tasks = [make_task("t1"), make_task("t2")]

    results = runtime.run_parallel(tasks)

    assert [result.success for result in results] == [True, True]
    assert engine_a.run_count == 2
    assert engine_b.run_count == 0


def test_run_parallel_fails_individual_task_when_all_providers_at_capacity() -> None:
    """M74(ADR-0092): 대체 후보가 전혀 없고 유일한 엔진마저 capacity를
    초과하면, 기존 개별 Task 실패 격리 정책(M10-T01/T02)대로 그 Task만
    `EngineResult(success=False)`가 되고 다른 Task의 결과에는 영향이
    없다."""
    runtime = ManagedEngineRuntime(event_bus=InMemoryEventBus())
    engine_a = CountingSlowEngineAdapter(delay_seconds=0.2)
    runtime.register_engine("engine-a", engine_a, max_concurrency=1)
    tasks = [make_task("t1"), make_task("t2")]

    results = runtime.run_parallel(tasks)

    successes = [result.success for result in results]
    assert successes.count(True) == 1
    assert successes.count(False) == 1
    assert engine_a.run_count == 1


class CostedSlowEngineAdapter(CountingSlowEngineAdapter):
    """M75(ADR-0093) 테스트용 — `CountingSlowEngineAdapter`(고유 세션 ID +
    Lock 보호 호출 횟수)에 고정 비용을 더한다."""

    def __init__(self, delay_seconds: float, estimated_cost_usd: float = 0.0) -> None:
        super().__init__(delay_seconds)
        self._estimated_cost_usd = estimated_cost_usd

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=self._estimated_cost_usd)


def test_run_parallel_diversity_spreads_across_engines_on_full_tie() -> None:
    """M75(ADR-0093): `max_concurrency` 제한이 전혀 없어도(M74와 무관),
    비용·신뢰도가 완전히 동률이면 실제 병렬 실행 중인(`ThreadPoolExecutor`)
    두 Task가 같은 엔진에 몰리지 않고 각각 다른 엔진으로 분산된다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(), engine_selection_policy=InMemoryEngineSelectionPolicy()
    )
    engine_a = CostedSlowEngineAdapter(delay_seconds=0.2)
    engine_b = CostedSlowEngineAdapter(delay_seconds=0.05)
    runtime.register_engine("engine-a", engine_a)
    runtime.register_engine("engine-b", engine_b)
    tasks = [make_task("t1"), make_task("t2")]

    results = runtime.run_parallel(tasks)

    assert [result.success for result in results] == [True, True]
    assert engine_a.run_count == 1
    assert engine_b.run_count == 1


def test_run_parallel_diversity_does_not_override_lower_cost() -> None:
    """M75(ADR-0093): engine-a가 더 바쁘더라도(느려서 오래 점유) 비용이
    더 낮으면 다양성이 이를 뒤집지 않는다 — 두 병렬 Task 모두 그대로
    engine-a로 몰린다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(), engine_selection_policy=InMemoryEngineSelectionPolicy()
    )
    engine_a = CostedSlowEngineAdapter(delay_seconds=0.2, estimated_cost_usd=0.0)
    engine_b = CostedSlowEngineAdapter(delay_seconds=0.05, estimated_cost_usd=5.0)
    runtime.register_engine("engine-a", engine_a)
    runtime.register_engine("engine-b", engine_b)
    tasks = [make_task("t1"), make_task("t2")]

    results = runtime.run_parallel(tasks)

    assert [result.success for result in results] == [True, True]
    assert engine_a.run_count == 2
    assert engine_b.run_count == 0


class CapableCostedSlowEngineAdapter(CostedSlowEngineAdapter):
    """M76(ADR-0094) 테스트용 — `CostedSlowEngineAdapter`에 커스텀
    capabilities를 더해, `required_capabilities`로 특정 엔진에만 선택적으로
    부하를 재현할 수 있게 한다(다른 엔진은 그 capability를 만족하지
    못해 자동으로 후보에서 제외됨)."""

    def __init__(
        self,
        delay_seconds: float,
        estimated_cost_usd: float = 0.0,
        capabilities: frozenset[str] = frozenset({"code_generation"}),
    ) -> None:
        super().__init__(delay_seconds, estimated_cost_usd)
        self._capabilities = capabilities

    def capabilities(self) -> frozenset[str]:
        return self._capabilities


def test_load_balancing_prefers_lower_relative_load_over_raw_in_flight_count() -> None:
    """M76(ADR-0094): 실제 `ThreadPoolExecutor` 없이도 여러 `threading.Thread`
    가 `ManagedEngineRuntime.run()`을 동시에 호출하는 상황에서, engine-a
    (max_concurrency=10, 지금 3건 실행 중 → 부하율 0.3)와 engine-b
    (max_concurrency=2, 지금 1건 실행 중 → 부하율 0.5)가 비용·성공률
    완전 동률이면, raw in-flight 개수(3 > 1)가 아니라 상대 부하율이 더
    낮은 engine-a가 선택된다."""
    runtime = ManagedEngineRuntime(
        event_bus=InMemoryEventBus(), engine_selection_policy=InMemoryEngineSelectionPolicy()
    )
    engine_a = CapableCostedSlowEngineAdapter(
        delay_seconds=0.2, capabilities=frozenset({"cap_a"})
    )
    engine_b = CapableCostedSlowEngineAdapter(
        delay_seconds=0.2, capabilities=frozenset({"cap_b"})
    )
    runtime.register_engine("engine-a", engine_a, max_concurrency=10)
    runtime.register_engine("engine-b", engine_b, max_concurrency=2)

    threads = [
        threading.Thread(
            target=runtime.run, args=(make_task(f"busy-a-{i}"), frozenset({"cap_a"}))
        )
        for i in range(3)
    ]
    threads.append(
        threading.Thread(target=runtime.run, args=(make_task("busy-b"), frozenset({"cap_b"})))
    )
    for thread in threads:
        thread.start()
    time.sleep(0.05)  # engine-a in-flight=3(부하율 0.3), engine-b in-flight=1(부하율 0.5)

    runtime.run(make_task("tie"))

    for thread in threads:
        thread.join()

    assert engine_a.run_count == 4
    assert engine_b.run_count == 1
