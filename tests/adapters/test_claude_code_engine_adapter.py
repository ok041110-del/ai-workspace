from __future__ import annotations

import json

import pytest
from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import (
    EngineExecutionError,
    EngineSessionStatus,
    SessionNotFoundError,
)
from ai_workspace.interfaces.execution_environment import ExecutionResult


def make_task(title: str = "구현하기") -> Task:
    return Task(task_id="t1", project_id="p1", title=title, status=TaskStatus.TODO)


def success_result(result: str = "42") -> ExecutionResult:
    stdout = json.dumps({"is_error": False, "result": result, "session_id": "s1"})
    return ExecutionResult(returncode=0, stdout=stdout, stderr="")


def error_result(result: str = "실패했습니다") -> ExecutionResult:
    stdout = json.dumps({"is_error": True, "result": result})
    return ExecutionResult(returncode=1, stdout=stdout, stderr="")


def test_manual_permission_mode_rejected_at_construction() -> None:
    with pytest.raises(ValueError):
        ClaudeCodeEngineAdapter(permission_mode="manual")


def test_run_unknown_session_raises_not_found() -> None:
    adapter = ClaudeCodeEngineAdapter(execution_environment=FakeExecutionEnvironment())

    with pytest.raises(SessionNotFoundError):
        adapter.run("unknown", make_task())


def test_run_parses_successful_json_result() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is True
    assert result.output == "42"


def test_run_parses_error_json_result_without_raising() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = error_result()
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "실패했습니다"


def test_run_falls_back_to_raw_stdout_when_not_json() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = ExecutionResult(returncode=0, stdout="완료", stderr="")
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is True
    assert result.output == "완료"


def test_run_nonzero_exit_without_json_returns_failure_not_exception() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = ExecutionResult(returncode=1, stdout="", stderr="boom")
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "boom"


def test_run_missing_claude_binary_raises_engine_execution_error() -> None:
    fake = FakeExecutionEnvironment()
    fake.exception = FileNotFoundError()
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())


def test_run_timeout_raises_engine_execution_error() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = ExecutionResult(returncode=-1, stdout="", stderr="", timed_out=True)
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())


def test_run_timeout_marks_status_failed() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = ExecutionResult(returncode=-1, stdout="", stderr="", timed_out=True)
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())

    assert adapter.status(session_id) == EngineSessionStatus.FAILED


def test_run_reflects_cancellation_from_execution_environment() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = ExecutionResult(returncode=-1, stdout="일부 출력", stderr="", cancelled=True)
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "cancelled"
    assert adapter.status(session_id) == EngineSessionStatus.CANCELLED


def test_status_reflects_completed_after_successful_run() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    adapter.run(session_id, make_task())

    assert adapter.status(session_id) == EngineSessionStatus.COMPLETED


def test_status_reflects_failed_after_unsuccessful_run() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = error_result()
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    adapter.run(session_id, make_task())

    assert adapter.status(session_id) == EngineSessionStatus.FAILED


def test_cancel_before_execution_marks_status_cancelled() -> None:
    """실행이 시작되기 전(run() 호출 전)에는 ExecutionEnvironment에 아무
    것도 등록되어 있지 않으므로 environment.cancel()은 ExecutionNotFoundError
    를 던지지만, Adapter는 이를 삼키고 자신의 세션 상태만 CANCELLED로
    바꾼다(EngineAdapter.cancel() 계약은 environment 쪽 성공 여부와 무관하게
    상태 전이를 보장한다)."""
    fake = FakeExecutionEnvironment()
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    adapter.cancel(session_id)

    assert adapter.status(session_id) == EngineSessionStatus.CANCELLED


def test_cancel_after_completion_preserves_completed_status() -> None:
    """M3-T03에서 발견한 계약 위반 수정: EngineAdapter.cancel()은 이미
    COMPLETED/FAILED로 끝난 세션을 CANCELLED로 덮어써서는 안 된다
    (interfaces/engine_adapter.py의 cancel() 계약 — "이미 COMPLETED/
    FAILED로 끝난 세션은 상태가 유지된다")."""
    fake = FakeExecutionEnvironment()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()
    adapter.run(session_id, make_task())

    adapter.cancel(session_id)

    assert adapter.status(session_id) == EngineSessionStatus.COMPLETED
    assert session_id not in fake.cancelled_ids


def test_destroy_session_then_status_raises_not_found() -> None:
    adapter = ClaudeCodeEngineAdapter(execution_environment=FakeExecutionEnvironment())
    session_id = adapter.create_session()

    adapter.destroy_session(session_id)

    with pytest.raises(SessionNotFoundError):
        adapter.status(session_id)


def test_capabilities_include_claude_code() -> None:
    adapter = ClaudeCodeEngineAdapter(execution_environment=FakeExecutionEnvironment())

    assert "claude_code" in adapter.capabilities()


def test_build_command_includes_model_when_given() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(model="sonnet", execution_environment=fake)
    session_id = adapter.create_session()

    adapter.run(session_id, make_task())

    assert "--model" in fake.executed_commands[0]
    assert "sonnet" in fake.executed_commands[0]


def test_build_command_never_uses_manual_permission_mode() -> None:
    fake = FakeExecutionEnvironment()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(execution_environment=fake)
    session_id = adapter.create_session()

    adapter.run(session_id, make_task())

    assert "manual" not in fake.executed_commands[0]


def test_estimate_cost_returns_nonzero_tokens_for_nonempty_title() -> None:
    adapter = ClaudeCodeEngineAdapter(execution_environment=FakeExecutionEnvironment())

    estimate = adapter.estimate_cost(make_task("아주 긴 제목의 구현 작업입니다"))

    assert estimate.estimated_tokens > 0
