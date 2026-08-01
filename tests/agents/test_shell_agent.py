from __future__ import annotations

import pytest
from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry, FakeAgentScheduler

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

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=CODE_COMPLETED,
            payload={"task_id": "t1", "output": "def f(): ..."},
        )
    )

    shell_completed = next(e for e in received if e.event_type == SHELL_COMPLETED)
    assert shell_completed.payload == {
        "task_id": "t1",
        "code_output": "def f(): ...",
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


def test_both_instances_run_when_max_parallel_agents_is_two() -> None:
    """M58(ADR-0076) — max_parallel_agents=2를 두 인스턴스 모두에 주면
    같은 Event를 병렬로 처리한다."""
    shared_registry = FakeAgentRegistry()
    shared_manager = FakeAgentManager()
    shared_scheduler = FakeAgentScheduler()
    event_bus = InMemoryEventBus()
    process_runner = FakeProcessRunner(ProcessResult(returncode=0, stdout="ok", stderr=""))

    first_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    ShellAgent(
        agent_runtime=first_agent_runtime,
        event_bus=event_bus,
        command_kind="test",
        process_runner=process_runner,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
        max_parallel_agents=2,
    )
    second_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    ShellAgent(
        agent_runtime=second_agent_runtime,
        event_bus=event_bus,
        command_kind="test",
        process_runner=process_runner,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
        max_parallel_agents=2,
    )

    event_bus.publish(Event(event_id="e1", event_type=CODE_COMPLETED, payload={"task_id": "t1"}))

    assert process_runner.received_commands == [["pytest"], ["pytest"]]


def test_ignores_code_completed_when_not_selected_by_scheduler() -> None:
    """M56(ADR-0074) — CodingAgent(M13)와 동일한 패턴: 같은 SHELL
    Capability를 가진 다른 ShellAgent 인스턴스가 Scheduler에게
    선택되면, 선택되지 않은 인스턴스는 아무것도 하지 않는다."""
    shared_registry = FakeAgentRegistry()
    shared_manager = FakeAgentManager()
    shared_scheduler = FakeAgentScheduler()
    event_bus = InMemoryEventBus()
    process_runner = FakeProcessRunner(ProcessResult(returncode=0, stdout="ok", stderr=""))

    selected_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    ShellAgent(
        agent_runtime=selected_agent_runtime,
        event_bus=event_bus,
        command_kind="test",
        process_runner=process_runner,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
    )
    unselected_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    ShellAgent(
        agent_runtime=unselected_agent_runtime,
        event_bus=event_bus,
        command_kind="test",
        process_runner=process_runner,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
    )

    event_bus.publish(Event(event_id="e1", event_type=CODE_COMPLETED, payload={"task_id": "t1"}))

    assert process_runner.received_commands == [["pytest"]]
