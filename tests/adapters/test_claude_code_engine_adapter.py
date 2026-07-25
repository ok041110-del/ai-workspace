from __future__ import annotations

import json

import pytest

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.adapters.process_runner import ProcessResult
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import (
    EngineExecutionError,
    EngineSessionStatus,
    SessionNotFoundError,
)


class FakeProcessRunner:
    """`ProcessRunner`를 대체하는 테스트 더블 — 실제 프로세스를 띄우지
    않고 미리 준비된 결과/예외를 반환한다. `ProcessRunner`와 동일한
    `run`/`cancel` 시그니처만 덕 타이핑으로 만족시킨다."""

    def __init__(self) -> None:
        self.result: ProcessResult | None = None
        self.exception: BaseException | None = None
        self.received_commands: list[list[str]] = []
        self.cancelled_ids: list[str] = []

    def run(
        self,
        process_id: str,
        command: list[str],
        *,
        cwd: str | None = None,
        timeout: float | None = None,
    ) -> ProcessResult:
        self.received_commands.append(command)
        if self.exception is not None:
            raise self.exception
        assert self.result is not None
        return self.result

    def cancel(self, process_id: str) -> None:
        self.cancelled_ids.append(process_id)


def make_task(title: str = "구현하기") -> Task:
    return Task(task_id="t1", project_id="p1", title=title, status=TaskStatus.TODO)


def success_result(result: str = "42") -> ProcessResult:
    stdout = json.dumps({"is_error": False, "result": result, "session_id": "s1"})
    return ProcessResult(returncode=0, stdout=stdout, stderr="")


def error_result(result: str = "실패했습니다") -> ProcessResult:
    stdout = json.dumps({"is_error": True, "result": result})
    return ProcessResult(returncode=1, stdout=stdout, stderr="")


def test_manual_permission_mode_rejected_at_construction() -> None:
    with pytest.raises(ValueError):
        ClaudeCodeEngineAdapter(permission_mode="manual")


def test_run_unknown_session_raises_not_found() -> None:
    adapter = ClaudeCodeEngineAdapter(process_runner=FakeProcessRunner())

    with pytest.raises(SessionNotFoundError):
        adapter.run("unknown", make_task())


def test_run_parses_successful_json_result() -> None:
    fake = FakeProcessRunner()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is True
    assert result.output == "42"


def test_run_parses_error_json_result_without_raising() -> None:
    fake = FakeProcessRunner()
    fake.result = error_result()
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "실패했습니다"


def test_run_falls_back_to_raw_stdout_when_not_json() -> None:
    fake = FakeProcessRunner()
    fake.result = ProcessResult(returncode=0, stdout="완료", stderr="")
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is True
    assert result.output == "완료"


def test_run_nonzero_exit_without_json_returns_failure_not_exception() -> None:
    fake = FakeProcessRunner()
    fake.result = ProcessResult(returncode=1, stdout="", stderr="boom")
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "boom"


def test_run_missing_claude_binary_raises_engine_execution_error() -> None:
    fake = FakeProcessRunner()
    fake.exception = FileNotFoundError()
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())


def test_run_timeout_raises_engine_execution_error() -> None:
    fake = FakeProcessRunner()
    fake.result = ProcessResult(returncode=-1, stdout="", stderr="", timed_out=True)
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())


def test_run_timeout_marks_status_failed() -> None:
    fake = FakeProcessRunner()
    fake.result = ProcessResult(returncode=-1, stdout="", stderr="", timed_out=True)
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())

    assert adapter.status(session_id) == EngineSessionStatus.FAILED


def test_run_reflects_cancellation_from_process_runner() -> None:
    fake = FakeProcessRunner()
    fake.result = ProcessResult(returncode=-1, stdout="일부 출력", stderr="", cancelled=True)
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "cancelled"
    assert adapter.status(session_id) == EngineSessionStatus.CANCELLED


def test_status_reflects_completed_after_successful_run() -> None:
    fake = FakeProcessRunner()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    adapter.run(session_id, make_task())

    assert adapter.status(session_id) == EngineSessionStatus.COMPLETED


def test_status_reflects_failed_after_unsuccessful_run() -> None:
    fake = FakeProcessRunner()
    fake.result = error_result()
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    adapter.run(session_id, make_task())

    assert adapter.status(session_id) == EngineSessionStatus.FAILED


def test_cancel_marks_status_cancelled_and_notifies_process_runner() -> None:
    fake = FakeProcessRunner()
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    adapter.cancel(session_id)

    assert adapter.status(session_id) == EngineSessionStatus.CANCELLED
    assert session_id in fake.cancelled_ids


def test_cancel_after_completion_preserves_completed_status() -> None:
    """M3-T03에서 발견한 계약 위반 수정: EngineAdapter.cancel()은 이미
    COMPLETED/FAILED로 끝난 세션을 CANCELLED로 덮어써서는 안 된다
    (interfaces/engine_adapter.py의 cancel() 계약 — "이미 COMPLETED/
    FAILED로 끝난 세션은 상태가 유지된다")."""
    fake = FakeProcessRunner()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()
    adapter.run(session_id, make_task())

    adapter.cancel(session_id)

    assert adapter.status(session_id) == EngineSessionStatus.COMPLETED
    assert session_id not in fake.cancelled_ids


def test_destroy_session_then_status_raises_not_found() -> None:
    adapter = ClaudeCodeEngineAdapter(process_runner=FakeProcessRunner())
    session_id = adapter.create_session()

    adapter.destroy_session(session_id)

    with pytest.raises(SessionNotFoundError):
        adapter.status(session_id)


def test_capabilities_include_claude_code() -> None:
    adapter = ClaudeCodeEngineAdapter(process_runner=FakeProcessRunner())

    assert "claude_code" in adapter.capabilities()


def test_build_command_includes_model_when_given() -> None:
    fake = FakeProcessRunner()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(model="sonnet", process_runner=fake)
    session_id = adapter.create_session()

    adapter.run(session_id, make_task())

    assert "--model" in fake.received_commands[0]
    assert "sonnet" in fake.received_commands[0]


def test_build_command_never_uses_manual_permission_mode() -> None:
    fake = FakeProcessRunner()
    fake.result = success_result()
    adapter = ClaudeCodeEngineAdapter(process_runner=fake)
    session_id = adapter.create_session()

    adapter.run(session_id, make_task())

    assert "manual" not in fake.received_commands[0]


def test_estimate_cost_returns_nonzero_tokens_for_nonempty_title() -> None:
    adapter = ClaudeCodeEngineAdapter(process_runner=FakeProcessRunner())

    estimate = adapter.estimate_cost(make_task("아주 긴 제목의 구현 작업입니다"))

    assert estimate.estimated_tokens > 0
