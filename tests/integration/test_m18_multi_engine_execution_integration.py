from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest
from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.domain.budget import Budget
from ai_workspace.domain.engine_selection import EngineSelectionDecision
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.engines.budget_policy_engine import InMemoryBudgetPolicyEngine
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.interfaces.authentication_manager import AuthenticationRequiredError
from ai_workspace.interfaces.execution_environment import ExecutionResult
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def make_task() -> Task:
    return Task(
        task_id="t1", project_id="p1", title="로그인 기능 구현하기", status=TaskStatus.TODO
    )


def _assemble(*, authenticated: bool):
    execution_environment = FakeExecutionEnvironment()
    execution_environment.result = ExecutionResult(
        returncode=0,
        stdout=json.dumps({"is_error": False, "result": "claude 실행 결과"}),
        stderr="",
    )
    registry = InMemoryEngineRegistry()
    registry.register(
        "claude_code", ClaudeCodeEngineAdapter(execution_environment=execution_environment)
    )
    auth = InMemoryAuthenticationManager(
        frozenset({"claude_code"}) if authenticated else frozenset()
    )
    dispatcher = ExecutionDispatcher(engine_registry=registry, authentication_manager=auth)
    return dispatcher, registry, execution_environment


def test_decision_is_actually_executed_via_claude_code_adapter_and_execution_environment() -> None:
    """M18 DoD 10번: 실제 ClaudeCodeEngineAdapter가 실제
    ExecutionEnvironment를 통해 실행됨을 증명한다."""
    dispatcher, registry, execution_environment = _assemble(authenticated=True)
    policy = InMemoryEngineSelectionPolicy()
    candidates = registry.list_candidates(make_task())
    decision = policy.select(make_task(), candidates)
    assert decision is not None

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is True
    assert result.engine == "claude_code"
    assert result.output == "claude 실행 결과"
    assert len(execution_environment.executed_commands) == 1
    assert execution_environment.executed_commands[0][0] == "claude"


def test_unauthenticated_engine_never_touches_execution_environment() -> None:
    """M18 DoD 4/5번: 미인증 상태면 실제 실행 환경까지 도달하지 않는다."""
    dispatcher, _registry, execution_environment = _assemble(authenticated=False)
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    with pytest.raises(AuthenticationRequiredError):
        dispatcher.dispatch(decision, make_task())

    assert execution_environment.executed_commands == []


def test_full_pipeline_from_registry_and_budget_through_selection_to_dispatch() -> None:
    """Registry 조회 -> Budget 반영 Selection -> Dispatch 전체 경로를
    실제 컴포넌트로 조립해 확인한다(Task->...->ExecutionResult)."""
    dispatcher, registry, _execution_environment = _assemble(authenticated=True)
    policy = InMemoryEngineSelectionPolicy()
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_tokens=10_000))
    task = make_task()

    candidates = registry.list_candidates(task)
    decision = policy.select(task, candidates, budget_policy_engine=budget_policy_engine)
    assert decision is not None

    result = dispatcher.dispatch(decision, task)

    assert result.success is True
    assert result.engine == "claude_code"


def test_engine_selection_policy_source_has_no_reference_to_execution_dispatcher() -> None:
    """M18 DoD 12번: SelectionPolicy는 ExecutionDispatcher를 참조하지
    않는다 - 실제 소스 코드를 읽어 Architecture 의존성을 직접
    검증한다."""
    policy_sources = [
        Path(inspect.getfile(InMemoryEngineSelectionPolicy)).read_text(encoding="utf-8"),
    ]
    interface_path = (
        _PROJECT_ROOT
        / "src"
        / "ai_workspace"
        / "interfaces"
        / "engine_selection_policy.py"
    )
    policy_sources.append(interface_path.read_text(encoding="utf-8"))

    for source in policy_sources:
        assert "ExecutionDispatcher" not in source
        assert "execution_dispatcher" not in source
