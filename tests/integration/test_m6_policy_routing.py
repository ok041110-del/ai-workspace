from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tests.agents.test_shell_agent import FakeProcessRunner as FakeShellProcessRunner
from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.adapters.cli_engine_adapter import CLIEngineAdapter
from ai_workspace.adapters.codex_provider import CodexProvider
from ai_workspace.adapters.gemini_cli_provider import GeminiCliProvider
from ai_workspace.adapters.process_runner import ProcessResult
from ai_workspace.agents.coding_agent import CodingAgent
from ai_workspace.agents.coordinator_agent import CoordinatorAgent
from ai_workspace.agents.documentation_agent import DocumentationAgent
from ai_workspace.agents.events import (
    CODE_COMPLETED,
    CODE_VERIFIED,
    DOCUMENTATION_COMPLETED,
    MISSION_PLANNED,
    REVIEW_COMPLETED,
    SHELL_COMPLETED,
)
from ai_workspace.agents.planning_agent import PlanningAgent
from ai_workspace.agents.review_agent import ReviewAgent
from ai_workspace.agents.shell_agent import ShellAgent
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.llm_policy_engine import InMemoryLLMPolicyEngine
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.execution_environment import ExecutionEnvironment, ExecutionResult
from ai_workspace.memory.context_manager import InMemoryContextManager
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime
from ai_workspace.runtime.engine.managed_engine_runtime import ManagedEngineRuntime
from ai_workspace.storage.llm_policy_loader import load_llm_policy_rules

_EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "docs" / "llm_policy.example.yaml"


class SwitchingFakeExecutionEnvironment(ExecutionEnvironment):
    """command[0](CLI 실행 파일 이름)에 따라 서로 다른 결과를 반환하는
    테스트 더블(M6-T03, M11-T03에서 `ExecutionEnvironment` 계약으로 전환)
    — `ClaudeCodeEngineAdapter`/`CLIEngineAdapter`(Codex)/`CLIEngineAdapter`
    (Gemini)가 하나의 `ManagedEngineRuntime`에 동시에 등록되어도, 실제로
    정책에 맞는 어댑터만 호출됐음을 실행 파일 이름으로 구분해 증명한다
    (세 어댑터 모두 실제 프로세스 대신 이 환경을 공유해서 주입받는다)."""

    def __init__(self, stdout_by_executable: dict[str, str]) -> None:
        self._stdout_by_executable = stdout_by_executable
        self.executed_commands: list[list[str]] = []

    def execute(
        self,
        execution_id: str,
        command: list[str],
        *,
        cwd: str | None = None,
        timeout: float | None = None,
    ) -> ExecutionResult:
        self.executed_commands.append(command)
        return ExecutionResult(
            returncode=0, stdout=self._stdout_by_executable[command[0]], stderr=""
        )

    def cancel(self, execution_id: str) -> None:
        pass


def assemble() -> dict[str, Any]:
    """M6 전체를 실제 구현으로 조립한다: `ManagedEngineRuntime`(M6-T01)에
    3개 EngineAdapter(`claude_code`/`codex`/`gemini`)를 동시에 등록하고,
    저장소의 실제 `docs/llm_policy.example.yaml`을 로드한 진짜
    `InMemoryLLMPolicyEngine`을 `AgentRuntime`에 주입한다(M5-T02와 동일한
    "진짜 정책 파일" 검증 방식). Coding/Review/Documentation 3개 Agent가
    각자 Role에 배정된 Provider의 Adapter로 실제 라우팅되는지(M6-T02)를
    End-to-End로 증명하는 것이 이 통합 테스트의 목적이다. 세 Adapter
    모두 실제 CLI 프로세스 대신 `SwitchingFakeExecutionEnvironment`를
    공유 주입받는다(명령 조립·결과 파싱 등 실제 코드 경로는 그대로
    거친다)."""
    event_bus = InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    execution_environment = SwitchingFakeExecutionEnvironment(
        {
            "claude": json.dumps({"is_error": False, "result": "claude 실행 결과"}),
            "codex": json.dumps({"content": "codex 실행 결과"}),
            "gemini": json.dumps({"response": "gemini 실행 결과"}),
        }
    )

    engine_runtime = ManagedEngineRuntime(event_bus=event_bus)
    engine_runtime.register_engine(
        "claude_code", ClaudeCodeEngineAdapter(execution_environment=execution_environment)
    )
    engine_runtime.register_engine(
        "codex",
        CLIEngineAdapter(provider=CodexProvider(), execution_environment=execution_environment),
    )
    engine_runtime.register_engine(
        "gemini",
        CLIEngineAdapter(
            provider=GeminiCliProvider(), execution_environment=execution_environment
        ),
    )

    llm_policy_engine = InMemoryLLMPolicyEngine(load_llm_policy_rules(_EXAMPLE_YAML))
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        llm_policy_engine=llm_policy_engine,
    )
    context_manager = InMemoryContextManager(InMemoryMemoryEngine())
    workspace_session = WorkspaceSession(session_id="s1", current_project_id="p1")

    planning_agent = PlanningAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        context_manager=context_manager,
        workspace_session=workspace_session,
    )
    CodingAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
    )
    ShellAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        command_kind="test",
        process_runner=FakeShellProcessRunner(
            ProcessResult(returncode=0, stdout="1 passed", stderr="")
        ),
    )
    CoordinatorAgent(agent_runtime=agent_runtime, event_bus=event_bus, task_engine=task_engine)
    ReviewAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
    )
    DocumentationAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        context_manager=context_manager,
        workspace_session=workspace_session,
    )

    return {
        "planning_agent": planning_agent,
        "task_engine": task_engine,
        "event_bus": event_bus,
        "execution_environment": execution_environment,
    }


def test_full_pipeline_completes_with_multiple_registered_adapters() -> None:
    """여러 EngineAdapter가 동시에 등록되어 있어도(M6-T01) 기존 전체
    파이프라인(M5-T06 DoD)이 그대로 완주함을 확인한다 — 회귀 없음."""
    pipeline = assemble()
    received: list[Event] = []
    pipeline["event_bus"].subscribe(received.append)

    task = pipeline["planning_agent"].plan_mission("p1", "구현하기")

    assert pipeline["task_engine"].get_task(task.task_id).status == TaskStatus.DONE
    event_types = {event.event_type for event in received}
    # ManagedEngineRuntime(M6-T01)은 InMemoryEngineRuntime(T2-05, 기존
    # test_pipeline.py가 쓰던 구현)과 달리 engine_task_started/completed
    # 같은 자체 생명주기 Event도 같은 EventBus에 발행하므로(ARCHITECTURE.md
    # §3.9) 정확히 일치가 아니라 Agent 파이프라인 Event가 전부 포함되는지만
    # 확인한다.
    assert event_types >= {
        MISSION_PLANNED,
        CODE_COMPLETED,
        SHELL_COMPLETED,
        CODE_VERIFIED,
        REVIEW_COMPLETED,
        DOCUMENTATION_COMPLETED,
    }


def test_policy_routes_each_role_to_distinct_registered_engine_adapter() -> None:
    """Milestone 6 DoD 1번: `docs/llm_policy.example.yaml`의 실제 정책
    (coding→anthropic, reviewer→openai, documentation→google)에 따라
    Coding/Review/Documentation 3개 Agent가 각각 claude/codex/gemini
    CLI를 실제로 호출했음을 증명한다."""
    pipeline = assemble()

    pipeline["planning_agent"].plan_mission("p1", "구현하기")

    invoked_executables = [
        command[0] for command in pipeline["execution_environment"].executed_commands
    ]
    assert sorted(invoked_executables) == ["claude", "codex", "gemini"]


def test_coding_agent_result_reflects_claude_code_adapter_output() -> None:
    pipeline = assemble()
    received: list[Event] = []
    pipeline["event_bus"].subscribe(received.append)

    pipeline["planning_agent"].plan_mission("p1", "구현하기")

    code_completed = next(e for e in received if e.event_type == CODE_COMPLETED)
    assert code_completed.payload["output"] == "claude 실행 결과"


def test_review_agent_result_reflects_codex_adapter_output() -> None:
    pipeline = assemble()
    received: list[Event] = []
    pipeline["event_bus"].subscribe(received.append)

    pipeline["planning_agent"].plan_mission("p1", "구현하기")

    review_completed = next(e for e in received if e.event_type == REVIEW_COMPLETED)
    assert review_completed.payload["output"] == "codex 실행 결과"
