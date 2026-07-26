from __future__ import annotations

import pytest

from ai_workspace.adapters.cli_engine_adapter import CLIEngineAdapter
from ai_workspace.adapters.cli_provider import CLIProvider
from ai_workspace.adapters.process_runner import ProcessResult
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.interfaces.engine_adapter import (
    EngineExecutionError,
    EngineResult,
    EngineSessionStatus,
    SessionNotFoundError,
)


class FakeProcessRunner:
    """`ProcessRunner`를 대체하는 테스트 더블(M3-T02/T03과 동일 패턴)."""

    def __init__(self) -> None:
        self.result: ProcessResult | None = None
        self.exception: BaseException | None = None
        self.received_commands: list[list[str]] = []

    def run(self, process_id, command, *, cwd=None, timeout=None) -> ProcessResult:
        self.received_commands.append(command)
        if self.exception is not None:
            raise self.exception
        assert self.result is not None
        return self.result

    def cancel(self, process_id: str) -> None:
        pass


class FakeCLIProvider(CLIProvider):
    """CLIEngineAdapter가 Provider에 정확히 위임하는지 검증하기 위한
    테스트 더블 — 고정된 명령/결과만 반환한다."""

    def __init__(self, command: list[str], result: EngineResult) -> None:
        self._command = command
        self._result = result
        self.parsed_process_results: list[ProcessResult] = []

    def build_command(self, session_id: str, task: Task) -> list[str]:
        return self._command

    def parse_result(self, process_result: ProcessResult) -> EngineResult:
        self.parsed_process_results.append(process_result)
        return self._result

    def capabilities(self) -> frozenset[str]:
        return frozenset({"code_generation"})

    def supports_parallel(self) -> bool:
        return True


def make_task(title: str = "구현하기") -> Task:
    return Task(task_id="t1", project_id="p1", title=title, status=TaskStatus.TODO)


def test_run_delegates_command_building_and_result_parsing_to_provider() -> None:
    fake_runner = FakeProcessRunner()
    fake_runner.result = ProcessResult(returncode=0, stdout="output", stderr="")
    provider = FakeCLIProvider(
        ["codex", "exec", "구현하기"], EngineResult(success=True, output="완료")
    )
    adapter = CLIEngineAdapter(provider=provider, process_runner=fake_runner)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result == EngineResult(success=True, output="완료")
    assert fake_runner.received_commands == [["codex", "exec", "구현하기"]]
    assert provider.parsed_process_results == [fake_runner.result]


def test_run_unknown_session_raises_not_found() -> None:
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, process_runner=FakeProcessRunner())

    with pytest.raises(SessionNotFoundError):
        adapter.run("unknown", make_task())


def test_run_missing_executable_raises_engine_execution_error() -> None:
    fake_runner = FakeProcessRunner()
    fake_runner.exception = FileNotFoundError()
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, process_runner=fake_runner)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())
    assert adapter.status(session_id) == EngineSessionStatus.FAILED


def test_run_timeout_raises_engine_execution_error() -> None:
    fake_runner = FakeProcessRunner()
    fake_runner.result = ProcessResult(returncode=0, stdout="", stderr="", timed_out=True)
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, process_runner=fake_runner)
    session_id = adapter.create_session()

    with pytest.raises(EngineExecutionError):
        adapter.run(session_id, make_task())
    assert adapter.status(session_id) == EngineSessionStatus.FAILED


def test_run_cancelled_process_returns_failed_result_without_calling_provider() -> None:
    fake_runner = FakeProcessRunner()
    fake_runner.result = ProcessResult(returncode=-1, stdout="", stderr="", cancelled=True)
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output="이건 안 쓰임"))
    adapter = CLIEngineAdapter(provider=provider, process_runner=fake_runner)
    session_id = adapter.create_session()

    result = adapter.run(session_id, make_task())

    assert result.success is False
    assert result.error == "cancelled"
    assert provider.parsed_process_results == []
    assert adapter.status(session_id) == EngineSessionStatus.CANCELLED


def test_cancel_after_completion_preserves_completed_status() -> None:
    fake_runner = FakeProcessRunner()
    fake_runner.result = ProcessResult(returncode=0, stdout="", stderr="")
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output="완료"))
    adapter = CLIEngineAdapter(provider=provider, process_runner=fake_runner)
    session_id = adapter.create_session()
    adapter.run(session_id, make_task())

    adapter.cancel(session_id)

    assert adapter.status(session_id) == EngineSessionStatus.COMPLETED


def test_destroy_session_then_run_raises_session_not_found() -> None:
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, process_runner=FakeProcessRunner())
    session_id = adapter.create_session()

    adapter.destroy_session(session_id)

    with pytest.raises(SessionNotFoundError):
        adapter.run(session_id, make_task())


def test_capabilities_and_supports_parallel_delegate_to_provider() -> None:
    provider = FakeCLIProvider(["codex"], EngineResult(success=True, output=""))
    adapter = CLIEngineAdapter(provider=provider, process_runner=FakeProcessRunner())

    assert adapter.capabilities() == frozenset({"code_generation"})
    assert adapter.supports_parallel() is True
