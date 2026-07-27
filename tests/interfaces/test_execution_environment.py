import pytest

from ai_workspace.interfaces.execution_environment import ExecutionNotFoundError, ExecutionResult

from .fakes import FakeExecutionEnvironment


def test_execute_returns_configured_result() -> None:
    environment = FakeExecutionEnvironment()
    environment.result = ExecutionResult(returncode=0, stdout="hello", stderr="")

    result = environment.execute("e1", ["echo", "hello"])

    assert result == ExecutionResult(returncode=0, stdout="hello", stderr="")


def test_execute_defaults_to_success_when_no_result_configured() -> None:
    environment = FakeExecutionEnvironment()

    result = environment.execute("e1", ["echo", "hello"])

    assert result.returncode == 0
    assert result.timed_out is False
    assert result.cancelled is False


def test_execute_records_command_for_verification() -> None:
    environment = FakeExecutionEnvironment()

    environment.execute("e1", ["claude", "-p", "hi"])

    assert environment.executed_commands == [["claude", "-p", "hi"]]


def test_execute_raises_configured_exception() -> None:
    environment = FakeExecutionEnvironment()
    environment.exception = FileNotFoundError("claude 실행 파일을 찾을 수 없습니다.")

    with pytest.raises(FileNotFoundError):
        environment.execute("e1", ["claude"])


def test_cancel_unknown_execution_id_raises_not_found() -> None:
    environment = FakeExecutionEnvironment()

    with pytest.raises(ExecutionNotFoundError):
        environment.cancel("unknown")
