import pytest

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.engine_selection import EngineSelectionDecision
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.interfaces.authentication_manager import AuthenticationRequiredError
from ai_workspace.interfaces.engine_registry import EngineNotRegisteredError
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher


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
