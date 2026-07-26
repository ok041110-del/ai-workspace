from __future__ import annotations

from typing import Any

from tests.adapters.test_claude_code_engine_adapter import error_result, success_result
from tests.agents.test_shell_agent import FakeProcessRunner as FakeShellProcessRunner
from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
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
from ai_workspace.domain.retry_policy import RetryPolicy
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.memory.context_manager import InMemoryContextManager
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime
from ai_workspace.runtime.engine.managed_engine_runtime import ManagedEngineRuntime
from ai_workspace.runtime.engine.recovering_engine_runtime import RecoveringEngineRuntime


class FlakyProcessRunner:
    """미리 정해진 결과를 호출 순서대로 반환하는 테스트 더블 — 실제 `claude`
    프로세스는 띄우지 않되(비용·비결정성 회피, M3-T07과 동일 원칙),
    `RecoveringEngineRuntime`의 재시도가 실제 Agent 파이프라인 안에서
    의미 있게 동작함을 증명하기 위해 첫 실행을 의도적으로 실패시킨다."""

    def __init__(self, results: list[ProcessResult]) -> None:
        self._results = list(results)
        self.call_count = 0

    def run(
        self,
        process_id: str,
        command: list[str],
        *,
        cwd: str | None = None,
        timeout: float | None = None,
    ) -> ProcessResult:
        result = self._results[self.call_count]
        self.call_count += 1
        return result

    def cancel(self, process_id: str) -> None:
        pass


def build_pipeline() -> dict[str, Any]:
    """M2의 Planning→Coding→Review→Documentation 파이프라인을 T2-06처럼
    `MockEngineAdapter`가 아니라 M3의 실제 Engine 스택(`ClaudeCodeEngineAdapter`
    + `ManagedEngineRuntime` + `RecoveringEngineRuntime`)으로 조립한다.
    Coding 단계의 첫 실행만 실패시켜(`FlakyProcessRunner`) 재시도가 실제로
    발생하고 복구됨을 증명한다. M5-T06으로 `ShellAgent`(항상 성공하는
    `FakeShellProcessRunner` 주입)+`CoordinatorAgent`가 Coding과 Review
    사이에 추가되었다 — `ClaudeCodeEngineAdapter`용 `FlakyProcessRunner`와는
    완전히 별개의 프로세스 실행 경로다."""
    process_runner = FlakyProcessRunner(
        [
            error_result("일시 오류"),
            success_result("완료(coding)"),
            success_result("완료(review)"),
            success_result("완료(documentation)"),
        ]
    )
    adapter = ClaudeCodeEngineAdapter(process_runner=process_runner)
    event_bus = InMemoryEventBus()
    managed_runtime = ManagedEngineRuntime(event_bus=event_bus)
    managed_runtime.register_engine("claude_code", adapter)
    engine_runtime = RecoveringEngineRuntime(
        inner=managed_runtime, retry_policy=RetryPolicy(max_attempts=2)
    )

    agent_registry = FakeAgentRegistry()
    agent_runtime = AgentRuntime(agent_manager=FakeAgentManager(), agent_registry=agent_registry)
    task_engine = InMemoryTaskEngine()
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
    CoordinatorAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
    )
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
        "event_bus": event_bus,
        "task_engine": task_engine,
        "planning_agent": planning_agent,
        "process_runner": process_runner,
    }


def test_full_pipeline_completes_with_real_engine_stack() -> None:
    pipeline = build_pipeline()

    task = pipeline["planning_agent"].plan_mission("p1", "구현하기")

    assert pipeline["task_engine"].get_task(task.task_id).status == TaskStatus.DONE
    # Coding 1차 실패 + 재시도 성공(2) + Review(1) + Documentation(1) = 4회 실제 실행
    assert pipeline["process_runner"].call_count == 4


def test_retry_actually_recovers_a_failed_first_attempt() -> None:
    """RecoveringEngineRuntime의 존재 이유를 실제 Agent 흐름 안에서 검증한다
    — Coding 단계의 첫 실행이 실패해도 CodingAgent는 예외를 보지 못하고
    최종적으로 성공한 결과만 받는다(재시도가 Agent에게 투명함)."""
    pipeline = build_pipeline()
    received: list[Event] = []
    pipeline["event_bus"].subscribe(received.append)

    pipeline["planning_agent"].plan_mission("p1", "구현하기")

    event_types = [event.event_type for event in received]
    assert event_types.count("engine_task_failed") == 1
    assert event_types.count("engine_task_completed") == 3
    assert CODE_COMPLETED in event_types  # 재시도 실패가 CodingAgent까지 전파되지 않음


def test_engine_and_agent_events_interleave_in_expected_nested_order() -> None:
    """`InMemoryEventBus`는 핸들러 내부에서 재귀적으로 publish()가 호출되면
    가장 안쪽에서 발행된 이벤트를 먼저 관측한다(M2 Retrospective
    Implementation Observation #3). 이번 파이프라인은 Coding→Shell→
    Coordinator→Review→Documentation이 서로의 핸들러 안에서 중첩
    호출되므로(M5-T06으로 Shell/Coordinator 추가), 이 특성이 정확히 아래
    순서를 만들어낸다는 것까지 명시적으로 검증한다. `ShellAgent`는
    `EngineRuntime`을 쓰지 않아 자체적으로는 `engine_task_*` Event를
    발행하지 않는다."""
    pipeline = build_pipeline()
    received: list[Event] = []
    pipeline["event_bus"].subscribe(received.append)

    pipeline["planning_agent"].plan_mission("p1", "구현하기")

    event_types = [event.event_type for event in received]
    assert event_types == [
        "engine_task_started",  # Coding 1차 시도
        "engine_task_failed",  # Coding 1차 실패
        "engine_task_started",  # Coding 재시도
        "engine_task_completed",  # Coding 재시도 성공
        "engine_task_started",  # Review
        "engine_task_completed",
        "engine_task_started",  # Documentation
        "engine_task_completed",
        DOCUMENTATION_COMPLETED,  # 가장 안쪽(Documentation)이 가장 먼저 관측됨
        REVIEW_COMPLETED,
        CODE_VERIFIED,
        SHELL_COMPLETED,
        CODE_COMPLETED,
        MISSION_PLANNED,  # 가장 바깥쪽 트리거가 가장 마지막에 관측됨
    ]
