from __future__ import annotations

import json
from pathlib import Path

from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.domain.engine_selection import EngineSelectionDecision
from ai_workspace.domain.retry_policy import RetryPolicy
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.interfaces.execution_environment import ExecutionResult
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def make_task() -> Task:
    return Task(
        task_id="t1", project_id="p1", title="로그인 기능 구현하기", status=TaskStatus.TODO
    )


def _assemble(*, execution_result: ExecutionResult, max_attempts: int = 3):
    execution_environment = FakeExecutionEnvironment()
    execution_environment.result = execution_result
    registry = InMemoryEngineRegistry()
    registry.register(
        "claude_code",
        ClaudeCodeEngineAdapter(
            execution_environment=execution_environment, subprocess_timeout_seconds=5.0
        ),
    )
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(
        engine_registry=registry,
        authentication_manager=auth,
        retry_policy=RetryPolicy(max_attempts=max_attempts),
    )
    return dispatcher, execution_environment


def test_timeout_is_retried_and_final_result_marks_timed_out() -> None:
    """M19 DoD 10번: 실제 ClaudeCodeEngineAdapter + ExecutionEnvironment
    조합에서 Timeout이 정책에 따라 재시도되고, 소진 후 timed_out=True
    실패 결과로 반영됨을 증명한다."""
    dispatcher, execution_environment = _assemble(
        execution_result=ExecutionResult(returncode=0, stdout="", stderr="", timed_out=True),
        max_attempts=3,
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is False
    assert result.timed_out is True
    assert result.retry_count == 2
    assert len(execution_environment.executed_commands) == 3


def test_cancellation_is_reflected_and_not_retried() -> None:
    """M19 DoD 11번: 실제 ClaudeCodeEngineAdapter + ExecutionEnvironment
    조합에서 취소가 EngineExecutionResult.cancelled에 반영되고
    재시도되지 않음을 증명한다."""
    dispatcher, execution_environment = _assemble(
        execution_result=ExecutionResult(returncode=0, stdout="", stderr="", cancelled=True),
        max_attempts=3,
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is False
    assert result.cancelled is True
    assert result.retry_count == 0
    assert len(execution_environment.executed_commands) == 1


def test_transient_process_error_recovers_within_retry_budget() -> None:
    """실행 파일을 찾지 못하는 경우(EngineExecutionError의 다른
    발생 경로)도 동일한 재시도 정책을 탄다 - 다만 이 시나리오는
    항상 실패하므로 소진 후 실패 결과를 반환함을 확인한다."""
    execution_environment = FakeExecutionEnvironment()
    execution_environment.exception = FileNotFoundError("claude not found")
    registry = InMemoryEngineRegistry()
    registry.register(
        "claude_code", ClaudeCodeEngineAdapter(execution_environment=execution_environment)
    )
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(
        engine_registry=registry,
        authentication_manager=auth,
        retry_policy=RetryPolicy(max_attempts=2),
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is False
    assert result.retry_count == 1
    assert len(execution_environment.executed_commands) == 2


def test_successful_execution_still_works_after_reliability_changes() -> None:
    """M18에서 검증했던 정상 실행 경로가 M19 이후에도 회귀 없이
    그대로 동작함을 재확인한다."""
    dispatcher, execution_environment = _assemble(
        execution_result=ExecutionResult(
            returncode=0,
            stdout=json.dumps({"is_error": False, "result": "claude 실행 결과"}),
            stderr="",
        )
    )
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is True
    assert result.output == "claude 실행 결과"
    assert result.retry_count == 0
    assert result.cancelled is False
    assert result.timed_out is False
    assert len(execution_environment.executed_commands) == 1
