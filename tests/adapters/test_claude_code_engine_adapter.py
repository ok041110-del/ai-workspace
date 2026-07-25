from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

import pytest

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import (
    EngineExecutionError,
    EngineSessionStatus,
    SessionNotFoundError,
)


def make_task(title: str = "구현하기") -> Task:
    return Task(task_id="t1", project_id="p1", title=title, status=TaskStatus.TODO)


def make_completed_process(
    *, stdout: str, returncode: int = 0, stderr: str = ""
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=["claude"], returncode=returncode, stdout=stdout, stderr=stderr
    )


def success_json(result: str = "42") -> str:
    return json.dumps({"is_error": False, "result": result, "session_id": "s1"})


def error_json(result: str = "실패했습니다") -> str:
    return json.dumps({"is_error": True, "result": result})


def test_manual_permission_mode_rejected_at_construction() -> None:
    with pytest.raises(ValueError):
        ClaudeCodeEngineAdapter(permission_mode="manual")


def test_run_unknown_session_raises_not_found() -> None:
    adapter = ClaudeCodeEngineAdapter()

    with pytest.raises(SessionNotFoundError):
        adapter.run("unknown", make_task())


def test_run_parses_successful_json_result() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()

    with patch("subprocess.run", return_value=make_completed_process(stdout=success_json())):
        result = adapter.run(session_id, make_task())

    assert result.success is True
    assert result.output == "42"


def test_run_parses_error_json_result_without_raising() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()

    with patch(
        "subprocess.run",
        return_value=make_completed_process(stdout=error_json(), returncode=1),
    ):
        result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "실패했습니다"


def test_run_falls_back_to_raw_stdout_when_not_json() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()

    with patch("subprocess.run", return_value=make_completed_process(stdout="완료")):
        result = adapter.run(session_id, make_task())

    assert result.success is True
    assert result.output == "완료"


def test_run_nonzero_exit_without_json_returns_failure_not_exception() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()

    with patch(
        "subprocess.run",
        return_value=make_completed_process(stdout="", returncode=1, stderr="boom"),
    ):
        result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "boom"


def test_run_missing_claude_binary_raises_engine_execution_error() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()

    with patch("subprocess.run", side_effect=FileNotFoundError()):
        with pytest.raises(EngineExecutionError):
            adapter.run(session_id, make_task())


def test_run_timeout_raises_engine_execution_error() -> None:
    adapter = ClaudeCodeEngineAdapter(subprocess_timeout_seconds=1.0)
    session_id = adapter.create_session()

    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="claude", timeout=1.0)):
        with pytest.raises(EngineExecutionError):
            adapter.run(session_id, make_task())


def test_status_reflects_completed_after_successful_run() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()

    with patch("subprocess.run", return_value=make_completed_process(stdout=success_json())):
        adapter.run(session_id, make_task())

    assert adapter.status(session_id) == EngineSessionStatus.COMPLETED


def test_status_reflects_failed_after_unsuccessful_run() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()

    with patch(
        "subprocess.run",
        return_value=make_completed_process(stdout=error_json(), returncode=1),
    ):
        adapter.run(session_id, make_task())

    assert adapter.status(session_id) == EngineSessionStatus.FAILED


def test_cancel_marks_status_cancelled() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()

    adapter.cancel(session_id)

    assert adapter.status(session_id) == EngineSessionStatus.CANCELLED


def test_destroy_session_then_status_raises_not_found() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()

    adapter.destroy_session(session_id)

    with pytest.raises(SessionNotFoundError):
        adapter.status(session_id)


def test_capabilities_include_claude_code() -> None:
    adapter = ClaudeCodeEngineAdapter()

    assert "claude_code" in adapter.capabilities()


def test_build_command_includes_model_when_given() -> None:
    adapter = ClaudeCodeEngineAdapter(model="sonnet")
    session_id = adapter.create_session()
    captured: dict[str, list[str]] = {}

    def _fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        captured["command"] = command
        return make_completed_process(stdout=success_json())

    with patch("subprocess.run", side_effect=_fake_run):
        adapter.run(session_id, make_task())

    assert "--model" in captured["command"]
    assert "sonnet" in captured["command"]


def test_build_command_never_uses_manual_permission_mode() -> None:
    adapter = ClaudeCodeEngineAdapter()
    session_id = adapter.create_session()
    captured: dict[str, list[str]] = {}

    def _fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        captured["command"] = command
        return make_completed_process(stdout=success_json())

    with patch("subprocess.run", side_effect=_fake_run):
        adapter.run(session_id, make_task())

    assert "manual" not in captured["command"]


def test_estimate_cost_returns_nonzero_tokens_for_nonempty_title() -> None:
    adapter = ClaudeCodeEngineAdapter()

    estimate = adapter.estimate_cost(make_task("아주 긴 제목의 구현 작업입니다"))

    assert estimate.estimated_tokens > 0
