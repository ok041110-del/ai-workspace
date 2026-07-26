from __future__ import annotations

import pytest
from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry

from ai_workspace.adapters.process_runner import ProcessResult
from ai_workspace.agents.events import CODE_COMPLETED, SHELL_COMPLETED
from ai_workspace.agents.shell_agent import ShellAgent, UnknownShellCommandKindError
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class FakeProcessRunner:
    """`ProcessRunner`를 대체하는 테스트 더블 — 실제 프로세스를 띄우지
    않고 미리 준비된 결과를 반환한다. 어떤 명령이 실제로 전달됐는지
    기록해, ShellAgent가 이벤트 payload가 아니라 화이트리스트로만
    명령을 정한다는 것을 검증한다."""

    def __init__(self, result: ProcessResult) -> None:
        self._result = result
        self.received_commands: list[list[str]] = []

    def run(self, process_id, command, *, cwd=None, timeout=None) -> ProcessResult:
        self.received_commands.append(command)
        return self._result

    def cancel(self, process_id: str) -> None:
        pass


def build_shell_agent(
    command_kind: str, process_runner: FakeProcessRunner
) -> tuple[ShellAgent, InMemoryEventBus]:
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(), agent_registry=FakeAgentRegistry()
    )
    event_bus = InMemoryEventBus()
    agent = ShellAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        command_kind=command_kind,
        process_runner=process_runner,
    )
    return agent, event_bus


def test_unknown_command_kind_raises_error() -> None:
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(), agent_registry=FakeAgentRegistry()
    )

    with pytest.raises(UnknownShellCommandKindError):
        ShellAgent(
            agent_runtime=agent_runtime,
            event_bus=InMemoryEventBus(),
            command_kind="rm -rf /",
        )


def test_runs_whitelisted_command_for_test_kind() -> None:
    process_runner = FakeProcessRunner(ProcessResult(returncode=0, stdout="ok", stderr=""))
    _agent, event_bus = build_shell_agent("test", process_runner)

    event_bus.publish(Event(event_id="e1", event_type=CODE_COMPLETED, payload={"task_id": "t1"}))

    assert process_runner.received_commands == [["pytest"]]


def test_runs_whitelisted_command_for_lint_kind() -> None:
    process_runner = FakeProcessRunner(ProcessResult(returncode=0, stdout="", stderr=""))
    _agent, event_bus = build_shell_agent("lint", process_runner)

    event_bus.publish(Event(event_id="e1", event_type=CODE_COMPLETED, payload={"task_id": "t1"}))

    assert process_runner.received_commands == [["ruff", "check", "."]]


def test_command_is_not_influenced_by_event_payload() -> None:
    """이벤트 payload에 무엇이 들어있든(예: 악의적인 문자열) 실행되는
    명령은 화이트리스트로 고정되어 절대 바뀌지 않는다(명령어 삽입 방지)."""
    process_runner = FakeProcessRunner(ProcessResult(returncode=0, stdout="", stderr=""))
    _agent, event_bus = build_shell_agent("test", process_runner)

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=CODE_COMPLETED,
            payload={"task_id": "t1; rm -rf /", "output": "$(malicious command)"},
        )
    )

    assert process_runner.received_commands == [["pytest"]]


def test_publishes_success_event_with_stdout_stderr_exit_code() -> None:
    process_runner = FakeProcessRunner(
        ProcessResult(returncode=0, stdout="3 passed", stderr="")
    )
    _agent, event_bus = build_shell_agent("test", process_runner)
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(Event(event_id="e1", event_type=CODE_COMPLETED, payload={"task_id": "t1"}))

    shell_completed = next(e for e in received if e.event_type == SHELL_COMPLETED)
    assert shell_completed.payload == {
        "task_id": "t1",
        "stdout": "3 passed",
        "stderr": "",
        "exit_code": 0,
        "success": True,
    }


def test_publishes_failure_event_when_command_exits_nonzero() -> None:
    process_runner = FakeProcessRunner(
        ProcessResult(returncode=1, stdout="", stderr="1 failed")
    )
    _agent, event_bus = build_shell_agent("test", process_runner)
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(Event(event_id="e1", event_type=CODE_COMPLETED, payload={"task_id": "t1"}))

    shell_completed = next(e for e in received if e.event_type == SHELL_COMPLETED)
    assert shell_completed.payload["success"] is False
    assert shell_completed.payload["exit_code"] == 1


def test_ignores_unrelated_event_types() -> None:
    process_runner = FakeProcessRunner(ProcessResult(returncode=0, stdout="", stderr=""))
    _agent, event_bus = build_shell_agent("test", process_runner)

    event_bus.publish(Event(event_id="e1", event_type="unrelated_event", payload={}))

    assert process_runner.received_commands == []
