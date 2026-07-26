from __future__ import annotations

import uuid

from ai_workspace.adapters.process_runner import ProcessRunner
from ai_workspace.agents.events import CODE_COMPLETED, SHELL_COMPLETED
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime

_WHITELISTED_COMMANDS: dict[str, list[str]] = {
    "test": ["pytest"],
    "lint": ["ruff", "check", "."],
}


class UnknownShellCommandKindError(Exception):
    """화이트리스트에 없는 command_kind로 ShellAgent를 생성하려 할 때
    발생한다."""


class ShellAgent:
    """`CodeCompleted` Event를 구독해 실제 쉘 명령을 실행하고
    `ShellCompleted` Event를 발행하는 Agent(ARCHITECTURE.md §3.6, M5-T04).

    **명령어 삽입 방지**: Task 제목이나 LLM 출력(`DevelopmentContext`,
    `EngineResult.output` 등) 어디에서도 실행할 명령을 유도하지 않는다.
    생성 시 지정한 `command_kind`가 내부 화이트리스트(`_WHITELISTED_COMMANDS`)
    에 있는 고정 명령으로만 매핑되며, 외부에는 명령 배열 자체를 노출하지
    않는다. 실제 프로세스 실행은 `ProcessRunner`(M3-T03)에 위임한다 —
    `EngineRuntime`/`EngineAdapter`는 LLM 엔진 호출 전용이라 여기서는
    쓰지 않는다."""

    def __init__(
        self,
        *,
        agent_runtime: AgentRuntime,
        event_bus: EventBus,
        command_kind: str,
        process_runner: ProcessRunner | None = None,
    ) -> None:
        if command_kind not in _WHITELISTED_COMMANDS:
            raise UnknownShellCommandKindError(command_kind)
        self._command = _WHITELISTED_COMMANDS[command_kind]
        self._event_bus = event_bus
        self._process_runner = process_runner if process_runner is not None else ProcessRunner()
        self._session = agent_runtime.start_agent(
            AgentRole.SHELL, frozenset({AgentCapability.SHELL})
        )
        event_bus.subscribe(self._on_code_completed)

    def _on_code_completed(self, event: Event) -> None:
        if event.event_type != CODE_COMPLETED:
            return
        task_id = event.payload["task_id"]
        process_id = str(uuid.uuid4())
        result = self._process_runner.run(process_id, self._command)
        success = result.returncode == 0 and not result.timed_out and not result.cancelled
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=SHELL_COMPLETED,
                payload={
                    "task_id": task_id,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.returncode,
                    "success": success,
                },
                source_agent_id=self._session.agent_id,
            )
        )
