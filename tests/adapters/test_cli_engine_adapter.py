from __future__ import annotations

import pytest
from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.cli_engine_adapter import CLIEngineAdapter
from ai_workspace.adapters.cli_provider import CLIProvider
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import (
    EngineExecutionError,
    EngineResult,
    EngineSessionStatus,
    SessionNotFoundError,
)
from ai_workspace.interfaces.execution_environment import ExecutionResult


class FakeCLIProvider(CLIProvider):
    """CLIEngineAdapter가 Provider에 정확히 위임하는지 검증하기 위한
    테스트 더블 — 고정된 명령/결과만 반환한다."""

    def __init__(self, command: list[str], result: EngineResult) -> None:
        self._command = command
        self._result = result
        self.parsed_execution_results: list[ExecutionResult] = []

    def build_command(self, session_id: str, task: Task) -> list[str]:
        return self._command

    def parse_result(self, execution_result: ExecutionResult) -> EngineResult:
        self.parsed_execution_results.append(execution_result)
        return self._result

    def capabilities(self) -> frozenset[str]:
        return frozenset({"code_generation"})

    def supports_parallel(self) -> bool:
        return True


def make_task(title: str = "구현하기") -> Task:
    return Task(task_id="t1", project_id="p1", title=title, status=TaskStatus.TODO)


def test_run_delegates_command_building_and_result_parsing_to_provider() -> None:
    fake_environment = FakeExecutionEnvironment()
    fake_environment.result = ExecutionResult(returncode=0, stdout="output", stderr="")
    provider = FakeCLIProvider(
        ["codex", "exec", "구현하기"], EngineResult(success=True, output="완료")
    )
    adapter = CLIEngineAdapter(provider=provider, execution_environment=fake_environment)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result == EngineResult(success=True, output="완료")
    assert fake_environment.executed_commands == [["codex", "exec", "구현하기"]]
    assert provider.parsed_execution_results == [fake_environment.result]


def test_run_unknown_session_raises_not_found() -> None:
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, execution_environment=FakeExecutionEnvironment())

    with pytest.raises(SessionNotFoundError):
        adapter.run("unknown", make_task())


def test_run_missing_executable_raises_engine_execution_error() -> None:
    fake_environment = FakeExecutionEnvironment()
    fake_environment.exception = FileNotFoundError()
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, execution_environment=fake_environment)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())
    assert adapter.status(session_id) == EngineSessionStatus.FAILED


def test_run_timeout_raises_engine_execution_error() -> None:
    fake_environment = FakeExecutionEnvironment()
    fake_environment.result = ExecutionResult(returncode=0, stdout="", stderr="", timed_out=True)
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, execution_environment=fake_environment)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())
    assert adapter.status(session_id) == EngineSessionStatus.FAILED


def test_run_cancelled_process_returns_failed_result_without_calling_provider() -> None:
    fake_environment = FakeExecutionEnvironment()
    fake_environment.result = ExecutionResult(returncode=-1, stdout="", stderr="", cancelled=True)
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output="이건 안 쓰임"))
    adapter = CLIEngineAdapter(provider=provider, execution_environment=fake_environment)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "cancelled"
    assert provider.parsed_execution_results == []
    assert adapter.status(session_id) == EngineSessionStatus.CANCELLED


def test_cancel_after_completion_preserves_completed_status() -> None:
    fake_environment = FakeExecutionEnvironment()
    fake_environment.result = ExecutionResult(returncode=0, stdout="", stderr="")
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output="완료"))
    adapter = CLIEngineAdapter(provider=provider, execution_environment=fake_environment)
    session_id = adapter.create_session()
    adapter.run(session_id, make_task())

    adapter.cancel(session_id)

    assert adapter.status(session_id) == EngineSessionStatus.COMPLETED


def test_destroy_session_then_run_raises_session_not_found() -> None:
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, execution_environment=FakeExecutionEnvironment())
    session_id = adapter.create_session()

    adapter.destroy_session(session_id)

    with pytest.raises(SessionNotFoundError):
        adapter.run(session_id, make_task())


def test_capabilities_and_supports_parallel_delegate_to_provider() -> None:
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, execution_environment=FakeExecutionEnvironment())

    assert adapter.capabilities() == frozenset({"code_generation"})
    assert adapter.supports_parallel() is True


def test_new_execution_environment_extends_adapter_without_code_changes() -> None:
    """Milestone 11 DoD 4번: 새 ExecutionEnvironment 구현체(여기서는
    FakeExecutionEnvironment)를 주입하는 것만으로 EngineAdapter가 정상
    동작한다 — Adapter 코드를 전혀 수정하지 않고도 실행 환경을 교체할 수
    있음을 증명한다(OCP)."""
    fake_environment = FakeExecutionEnvironment()
    fake_environment.result = ExecutionResult(returncode=0, stdout="output", stderr="")
    provider = FakeCLIProvider(["gemini"], EngineResult(success=True, output="완료"))

    adapter = CLIEngineAdapter(provider=provider, execution_environment=fake_environment)
    session_id = adapter.create_session()
    result = adapter.run(session_id, make_task())

    assert result.success is True
    assert fake_environment.executed_commands == [["gemini"]]
