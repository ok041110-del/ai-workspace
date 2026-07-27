import pytest

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.engine_selection import EngineSelectionDecision
from ai_workspace.domain.retry_policy import RetryPolicy
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.authentication_manager import AuthenticationRequiredError
from ai_workspace.interfaces.engine_adapter import EngineExecutionError, EngineResult
from ai_workspace.interfaces.engine_registry import EngineNotRegisteredError
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.events import (
    ENGINE_AUTHENTICATION_FAILED,
    ENGINE_EXECUTION_COMPLETED,
    ENGINE_EXECUTION_STARTED,
)
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher


class _FlakyThenSucceedsAdapter(MockEngineAdapter):
    def __init__(self, fail_times: int) -> None:
        super().__init__()
        self._fail_times = fail_times
        self.call_count = 0

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        self.call_count += 1
        if self.call_count <= self._fail_times:
            raise EngineExecutionError("process error")
        return super().run(session_id, task, model=model)


class _AlwaysTimingOutAdapter(MockEngineAdapter):
    def __init__(self) -> None:
        super().__init__()
        self.call_count = 0

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        self.call_count += 1
        raise EngineExecutionError("claude CLI가 5.0초 내에 응답하지 않았습니다.")


class _CancelledAdapter(MockEngineAdapter):
    def __init__(self) -> None:
        super().__init__()
        self.call_count = 0

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        self.call_count += 1
        return EngineResult(success=False, output="", error="cancelled")


class _AlwaysFailingAuthAdapter(MockEngineAdapter):
    """인증 실패는 EngineAdapter까지 도달하면 안 되므로, 도달하면
    호출 횟수를 기록해 테스트가 실패를 감지할 수 있게 한다."""

    def __init__(self) -> None:
        super().__init__()
        self.call_count = 0

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        self.call_count += 1
        return super().run(session_id, task, model=model)


def make_task() -> Task:
    return Task(task_id="t1", project_id="p1", title="구현하기", status=TaskStatus.TODO)


class SpyEngineRegistry(InMemoryEngineRegistry):
    def __init__(self) -> None:
        super().__init__()
        self.get_calls: list[str] = []

    def get(self, name: str):  # type: ignore[override]
        self.get_calls.append(name)
        return super().get(name)


def test_dispatch_executes_the_decided_engine_when_authenticated() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("claude_code", MockEngineAdapter())
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(engine_registry=registry, authentication_manager=auth)
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is True
    assert result.engine == "claude_code"
    assert result.execution_time >= 0.0


def test_dispatch_raises_authentication_required_when_not_authenticated() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("claude_code", MockEngineAdapter())
    auth = InMemoryAuthenticationManager()  # 아무것도 인증되지 않음
    dispatcher = ExecutionDispatcher(engine_registry=registry, authentication_manager=auth)
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    with pytest.raises(AuthenticationRequiredError):
        dispatcher.dispatch(decision, make_task())


def test_dispatch_returns_failure_result_when_no_decision() -> None:
    """M18 DoD 11번: SelectionDecision이 없으면 실행되지 않는다 —
    EngineRegistry/AuthenticationManager 어디도 호출되지 않음을
    Spy로 직접 증명한다."""
    registry = SpyEngineRegistry()
    registry.register("claude_code", MockEngineAdapter())
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(engine_registry=registry, authentication_manager=auth)

    result = dispatcher.dispatch(None, make_task())

    assert result.success is False
    assert result.engine is None
    assert result.error is not None
    assert registry.get_calls == []


def test_dispatch_only_executes_the_selected_engine_not_others() -> None:
    """M18 DoD 1번: 여러 Engine이 등록돼 있어도 선택된 하나만 실행된다."""
    registry = InMemoryEngineRegistry()
    selected = MockEngineAdapter()
    other = MockEngineAdapter()
    registry.register("selected", selected)
    registry.register("other", other)
    auth = InMemoryAuthenticationManager(frozenset({"selected", "other"}))
    dispatcher = ExecutionDispatcher(engine_registry=registry, authentication_manager=auth)
    decision = EngineSelectionDecision(engine_name="selected", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.engine == "selected"


def test_dispatch_unregistered_engine_raises_not_found() -> None:
    registry = InMemoryEngineRegistry()
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(engine_registry=registry, authentication_manager=auth)
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    with pytest.raises(EngineNotRegisteredError):
        dispatcher.dispatch(decision, make_task())


def test_dispatch_retries_on_engine_execution_error_and_eventually_succeeds() -> None:
    """M19 DoD 2/3번: EngineExecutionError는 재시도 가능하고, 정책 내에서
    성공하면 그 결과를 반환한다."""
    registry = InMemoryEngineRegistry()
    adapter = _FlakyThenSucceedsAdapter(fail_times=2)
    registry.register("claude_code", adapter)
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(
        engine_registry=registry,
        authentication_manager=auth,
        retry_policy=RetryPolicy(max_attempts=3),
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is True
    assert result.retry_count == 2
    assert adapter.call_count == 3


def test_dispatch_returns_failed_result_with_timed_out_after_exhausting_retries() -> None:
    """M19 DoD 3/5/10번: Timeout으로 재시도를 소진하면 예외 대신
    timed_out=True인 실패 결과를 반환한다(휴리스틱 기반)."""
    registry = InMemoryEngineRegistry()
    adapter = _AlwaysTimingOutAdapter()
    registry.register("claude_code", adapter)
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(
        engine_registry=registry,
        authentication_manager=auth,
        retry_policy=RetryPolicy(max_attempts=3),
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is False
    assert result.timed_out is True
    assert result.retry_count == 2
    assert adapter.call_count == 3


def test_dispatch_reflects_cancelled_result_without_retrying() -> None:
    """M19 DoD 4/11번: 취소는 예외가 아니라 결과이므로 재시도 루프를
    타지 않고 즉시 cancelled=True로 반영된다."""
    registry = InMemoryEngineRegistry()
    adapter = _CancelledAdapter()
    registry.register("claude_code", adapter)
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(
        engine_registry=registry,
        authentication_manager=auth,
        retry_policy=RetryPolicy(max_attempts=3),
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is False
    assert result.cancelled is True
    assert result.retry_count == 0
    assert adapter.call_count == 1


def test_dispatch_does_not_retry_authentication_required() -> None:
    """M19 DoD 6/8번: 인증 실패는 첫 시도에서 즉시 예외로 전파되고
    재시도되지 않는다."""
    registry = InMemoryEngineRegistry()
    adapter = _AlwaysFailingAuthAdapter()
    registry.register("claude_code", adapter)
    auth = InMemoryAuthenticationManager()  # 아무것도 인증되지 않음
    dispatcher = ExecutionDispatcher(
        engine_registry=registry,
        authentication_manager=auth,
        retry_policy=RetryPolicy(max_attempts=5),
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    with pytest.raises(AuthenticationRequiredError):
        dispatcher.dispatch(decision, make_task())

    assert adapter.call_count == 0


def test_dispatch_does_not_retry_unregistered_engine() -> None:
    """M19 DoD 7/8번: 등록되지 않은 Engine 조회 실패도 재시도되지
    않는다."""
    registry = InMemoryEngineRegistry()
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(
        engine_registry=registry,
        authentication_manager=auth,
        retry_policy=RetryPolicy(max_attempts=5),
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    with pytest.raises(EngineNotRegisteredError):
        dispatcher.dispatch(decision, make_task())


def test_dispatch_source_delegates_to_retry_executor_not_a_manual_loop() -> None:
    """M19 DoD 12번: ExecutionDispatcher는 RetryPolicy를 직접 구현하지
    않는다 - 소스 코드 검사로 RetryExecutor에 위임하고 있음을
    확인한다."""
    import inspect

    from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher as ED

    source = inspect.getsource(ED)
    assert "RetryExecutor" in source
    assert "for " not in inspect.getsource(ED.dispatch)


def test_dispatch_without_event_bus_behaves_like_before_m20() -> None:
    """M20 DoD: event_bus 미주입 시 기존과 완전히 동일하게 동작한다."""
    registry = InMemoryEngineRegistry()
    registry.register("claude_code", MockEngineAdapter())
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(engine_registry=registry, authentication_manager=auth)
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is True


def test_dispatch_publishes_started_and_completed_events_on_success() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("claude_code", MockEngineAdapter())
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    event_bus = InMemoryEventBus()
    received: list[Event] = []
    event_bus.subscribe(received.append)
    dispatcher = ExecutionDispatcher(
        engine_registry=registry, authentication_manager=auth, event_bus=event_bus
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    dispatcher.dispatch(decision, make_task())

    event_types = [event.event_type for event in received]
    assert event_types == [ENGINE_EXECUTION_STARTED, ENGINE_EXECUTION_COMPLETED]
    started = received[0]
    assert started.payload["engine"] == "claude_code"
    assert started.payload["task_title"] == "구현하기"
    completed = received[1]
    assert completed.payload["success"] is True
    assert completed.payload["cancelled"] is False


def test_dispatch_publishes_no_events_when_no_decision() -> None:
    registry = InMemoryEngineRegistry()
    auth = InMemoryAuthenticationManager()
    event_bus = InMemoryEventBus()
    received: list[Event] = []
    event_bus.subscribe(received.append)
    dispatcher = ExecutionDispatcher(
        engine_registry=registry, authentication_manager=auth, event_bus=event_bus
    )

    dispatcher.dispatch(None, make_task())

    assert received == []


def test_dispatch_publishes_authentication_failed_event() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("claude_code", MockEngineAdapter())
    auth = InMemoryAuthenticationManager()  # 미인증
    event_bus = InMemoryEventBus()
    received: list[Event] = []
    event_bus.subscribe(received.append)
    dispatcher = ExecutionDispatcher(
        engine_registry=registry, authentication_manager=auth, event_bus=event_bus
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    with pytest.raises(AuthenticationRequiredError):
        dispatcher.dispatch(decision, make_task())

    event_types = [event.event_type for event in received]
    assert event_types == [ENGINE_EXECUTION_STARTED, ENGINE_AUTHENTICATION_FAILED]
    assert received[1].payload["engine"] == "claude_code"
