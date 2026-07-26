from __future__ import annotations

from tests.interfaces.fakes import (
    FakeAgentManager,
    FakeAgentRegistry,
    FakeContextManager,
    FakeTaskEngine,
)

from ai_workspace.agents.events import MISSION_PLANNED
from ai_workspace.agents.planning_agent import PlanningAgent
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


def build_planning_agent(
    workspace_session: WorkspaceSession, context_manager: FakeContextManager
) -> tuple[PlanningAgent, InMemoryEventBus, FakeTaskEngine]:
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(), agent_registry=FakeAgentRegistry()
    )
    event_bus = InMemoryEventBus()
    task_engine = FakeTaskEngine()
    agent = PlanningAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        context_manager=context_manager,
        workspace_session=workspace_session,
    )
    return agent, event_bus, task_engine


def test_plan_mission_restores_latest_snapshot_when_session_has_none() -> None:
    """M8-T03: 세션 연속성의 핵심 — memory_snapshot_id가 비어 있는(예:
    새로 만든) 세션으로 Mission을 시작하면, 그 project의 최신 Snapshot을
    자동으로 이어받는다."""
    context_manager = FakeContextManager()
    prior_snapshot_id = context_manager.create_snapshot(
        WorkspaceSession(session_id="prior", current_project_id="p1")
    )
    workspace_session = WorkspaceSession(session_id="s1", current_project_id="p1")
    agent, _event_bus, _task_engine = build_planning_agent(workspace_session, context_manager)

    agent.plan_mission("p1", "구현하기")

    assert workspace_session.memory_snapshot_id == prior_snapshot_id


def test_plan_mission_does_not_overwrite_existing_snapshot_id() -> None:
    """같은 세션에서 이어지는 Mission이라면(memory_snapshot_id가 이미
    있으면) 자동 복원 로직이 이를 덮어쓰지 않는다."""
    context_manager = FakeContextManager()
    context_manager.create_snapshot(WorkspaceSession(session_id="prior", current_project_id="p1"))
    workspace_session = WorkspaceSession(
        session_id="s1", current_project_id="p1", memory_snapshot_id="existing-snapshot"
    )
    agent, _event_bus, _task_engine = build_planning_agent(workspace_session, context_manager)

    agent.plan_mission("p1", "구현하기")

    assert workspace_session.memory_snapshot_id == "existing-snapshot"


def test_plan_mission_leaves_snapshot_id_none_when_no_prior_snapshot() -> None:
    context_manager = FakeContextManager()
    workspace_session = WorkspaceSession(session_id="s1", current_project_id="p1")
    agent, _event_bus, _task_engine = build_planning_agent(workspace_session, context_manager)

    agent.plan_mission("p1", "구현하기")

    assert workspace_session.memory_snapshot_id is None


def test_plan_mission_only_restores_for_matching_project() -> None:
    """다른 project의 최신 Snapshot을 잘못 이어받지 않는다(project별
    독립성, M8-T01의 latest_snapshot_id 스코프 재확인)."""
    context_manager = FakeContextManager()
    context_manager.create_snapshot(WorkspaceSession(session_id="prior", current_project_id="p2"))
    workspace_session = WorkspaceSession(session_id="s1", current_project_id="p1")
    agent, _event_bus, _task_engine = build_planning_agent(workspace_session, context_manager)

    agent.plan_mission("p1", "구현하기")

    assert workspace_session.memory_snapshot_id is None


def test_plan_mission_still_publishes_mission_planned_event() -> None:
    context_manager = FakeContextManager()
    workspace_session = WorkspaceSession(session_id="s1", current_project_id="p1")
    agent, event_bus, task_engine = build_planning_agent(workspace_session, context_manager)
    received: list[Event] = []
    event_bus.subscribe(received.append)

    task = agent.plan_mission("p1", "구현하기")

    assert len(received) == 1
    assert received[0].event_type == MISSION_PLANNED
    assert received[0].payload["task_id"] == task.task_id
