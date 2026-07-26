from __future__ import annotations

from pathlib import Path
from typing import Any

from tests.agents.test_shell_agent import FakeProcessRunner
from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
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
from ai_workspace.agents.scheduling import find_agent_by_capability
from ai_workspace.agents.shell_agent import ShellAgent
from ai_workspace.domain.agent import AgentCapability
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.memory.context_manager import InMemoryContextManager
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime
from ai_workspace.storage.file_event_store import FileEventStore


def build_pipeline(*, event_bus: InMemoryEventBus | None = None) -> dict[str, Any]:
    """M5-T06: `ShellAgent`(테스트 실행)+`CoordinatorAgent`(테스트 통과
    여부에 따라 Review로 보내거나 재작업시킴)가 Coding과 Review 사이에
    추가되었다. 여기서는 `ShellAgent`가 항상 성공하도록
    `FakeProcessRunner`를 주입해(실제 `pytest`를 재귀 호출하지 않음) 기존
    T2-06 시나리오와 동일하게 한 번에 Documentation까지 도달하는 흐름을
    검증한다."""
    agent_registry = FakeAgentRegistry()
    agent_scheduler = InMemoryAgentScheduler()
    agent_runtime = AgentRuntime(agent_manager=FakeAgentManager(), agent_registry=agent_registry)
    event_bus = event_bus or InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    engine_runtime = InMemoryEngineRuntime()
    engine_runtime.register_engine("mock", MockEngineAdapter())
    context_manager = InMemoryContextManager(InMemoryMemoryEngine())
    workspace_session = WorkspaceSession(session_id="s1", current_project_id="p1")

    planning_agent = PlanningAgent(
        agent_runtime=agent_runtime, event_bus=event_bus, task_engine=task_engine
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
        process_runner=FakeProcessRunner(ProcessResult(returncode=0, stdout="1 passed", stderr="")),
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
        "agent_registry": agent_registry,
        "agent_scheduler": agent_scheduler,
        "event_bus": event_bus,
        "task_engine": task_engine,
        "planning_agent": planning_agent,
        "context_manager": context_manager,
        "workspace_session": workspace_session,
    }


def test_mission_planned_triggers_full_event_chain() -> None:
    """T2-06 DoD(M5-T06으로 확장): MissionPlanned→CodeCompleted→
    ShellCompleted→CodeVerified→ReviewCompleted→DocumentationCompleted
    Event 체인이 Agent 간 협업으로 자동 진행된다. InMemoryEventBus는
    핸들러 내부에서 재귀적으로 publish()가 호출되면 수신 순서가
    뒤집히므로(가장 안쪽에서 발행된 이벤트를 먼저 관측), 순서가 아니라
    수신된 이벤트 타입의 집합과 최종 Task 상태로 체인 완주를 검증한다."""
    pipeline = build_pipeline()
    received_types: set[str] = set()
    pipeline["event_bus"].subscribe(lambda event: received_types.add(event.event_type))

    task = pipeline["planning_agent"].plan_mission("p1", "구현하기")

    assert received_types == {
        MISSION_PLANNED,
        CODE_COMPLETED,
        SHELL_COMPLETED,
        CODE_VERIFIED,
        REVIEW_COMPLETED,
        DOCUMENTATION_COMPLETED,
    }
    assert pipeline["task_engine"].get_task(task.task_id).status == TaskStatus.DONE


def test_documentation_agent_creates_context_snapshot_on_completion() -> None:
    pipeline = build_pipeline()

    pipeline["planning_agent"].plan_mission("p1", "구현하기")

    context = pipeline["context_manager"].assemble_context(pipeline["workspace_session"])
    assert context["project_id"] == "p1"


def test_agent_scheduler_finds_coding_agent_by_capability() -> None:
    pipeline = build_pipeline()

    found = find_agent_by_capability(
        pipeline["agent_registry"], pipeline["agent_scheduler"], AgentCapability.CODING
    )

    assert found is not None
    assert AgentCapability.CODING in found.capabilities


def test_agent_scheduler_returns_none_for_missing_capability() -> None:
    pipeline = build_pipeline()

    found = find_agent_by_capability(
        pipeline["agent_registry"], pipeline["agent_scheduler"], AgentCapability.VISION
    )

    assert found is None


def test_each_agent_registered_with_distinct_capability() -> None:
    pipeline = build_pipeline()

    agents = pipeline["agent_registry"].list_active()

    assert len(agents) == 6
    capabilities = {capability for agent in agents for capability in agent.capabilities}
    assert capabilities == {
        AgentCapability.PLANNING,
        AgentCapability.CODING,
        AgentCapability.SHELL,
        AgentCapability.COORDINATION,
        AgentCapability.REVIEW,
        AgentCapability.DOCUMENTATION,
    }


def test_event_store_records_full_pipeline_event_chain(tmp_path: Path) -> None:
    """T2-07: Milestone 2 DoD 1번("Event Bus+Event Store로 협업과 이벤트
    기록이 이루어진다")을 증명한다. EventStore는 EventBus의 독립
    구독자다(ADR-0018) — 다른 Agent 구독자와 동일한 subscribe() 경로로
    등록한다."""
    event_bus = InMemoryEventBus()
    event_store = FileEventStore(tmp_path)
    event_bus.subscribe(event_store.record)
    pipeline = build_pipeline(event_bus=event_bus)

    pipeline["planning_agent"].plan_mission("p1", "구현하기")

    recorded_types = {event.event_type for event in event_store.replay()}
    assert recorded_types == {
        MISSION_PLANNED,
        CODE_COMPLETED,
        SHELL_COMPLETED,
        CODE_VERIFIED,
        REVIEW_COMPLETED,
        DOCUMENTATION_COMPLETED,
    }
