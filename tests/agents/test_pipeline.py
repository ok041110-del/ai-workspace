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


def build_pipeline(
    *,
    event_bus: InMemoryEventBus | None = None,
    context_manager: InMemoryContextManager | None = None,
    session_id: str = "s1",
) -> dict[str, Any]:
    """M5-T06: `ShellAgent`(테스트 실행)+`CoordinatorAgent`(테스트 통과
    여부에 따라 Review로 보내거나 재작업시킴)가 Coding과 Review 사이에
    추가되었다. 여기서는 `ShellAgent`가 항상 성공하도록
    `FakeProcessRunner`를 주입해(실제 `pytest`를 재귀 호출하지 않음) 기존
    T2-06 시나리오와 동일하게 한 번에 Documentation까지 도달하는 흐름을
    검증한다.

    `context_manager`/`session_id`(M8-T04)를 선택적으로 받을 수 있다 —
    같은 `ContextManager`를 공유하는 **별도의 새 세션**으로 두 번째
    파이프라인을 조립해 "세션 연속성"(다른 세션이 이전 세션의 Snapshot을
    자동으로 이어받음)을 증명하기 위함이다."""
    agent_registry = FakeAgentRegistry()
    agent_scheduler = InMemoryAgentScheduler()
    agent_runtime = AgentRuntime(agent_manager=FakeAgentManager(), agent_registry=agent_registry)
    event_bus = event_bus or InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    engine_runtime = InMemoryEngineRuntime()
    engine_runtime.register_engine("mock", MockEngineAdapter())
    context_manager = context_manager or InMemoryContextManager(InMemoryMemoryEngine())
    workspace_session = WorkspaceSession(session_id=session_id, current_project_id="p1")

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


def test_pipeline_stores_documentation_summary_searchable_via_memory() -> None:
    """M7-T03: 전체 파이프라인이 끝나면 DocumentationAgent가 Engine
    실행 결과를 요약으로 저장하고, MemoryEngine.search()(M4-T08)를 통해
    실제로 검색·복원 가능함을 증명한다 — PRD 7.4 "검색/요약" 완전 충족을
    End-to-End로 검증."""
    pipeline = build_pipeline()

    task = pipeline["planning_agent"].plan_mission("p1", "구현하기")

    expected_summary = f"{task.task_id} 완료(Mock)"
    snapshot_ids = pipeline["context_manager"].find_snapshots(expected_summary)
    assert snapshot_ids != []
    restored = pipeline["context_manager"].restore_snapshot(snapshot_ids[0])
    assert restored["summary"] == expected_summary


def test_second_mission_in_same_session_sees_prior_summary_in_context() -> None:
    """M8-T04: Milestone DoD 4번(같은 세션) — 첫 번째 Mission이 끝나면
    두 번째 Mission이 시작되기 전에 이미 `assemble_context()`가 첫
    번째 요약을 반영하고 있다(M8-T02가 세션에 되먹인 결과). 같은
    세션이므로 `memory_snapshot_id`가 이미 채워져 있어 M8-T03의 자동
    복원 로직은 트리거되지 않는다(이미 채워진 값을 그대로 이어갈 뿐)."""
    pipeline = build_pipeline()

    first_task = pipeline["planning_agent"].plan_mission("p1", "첫 번째 작업")
    context_before_second_mission = pipeline["context_manager"].assemble_context(
        pipeline["workspace_session"]
    )
    assert context_before_second_mission["summary"] == f"{first_task.task_id} 완료(Mock)"

    pipeline["planning_agent"].plan_mission("p1", "두 번째 작업")

    assert pipeline["workspace_session"].memory_snapshot_id is not None


def test_new_session_inherits_previous_session_summary_via_planning_agent() -> None:
    """M8-T04: Milestone DoD 4번(새 세션) — 완전히 새로운
    `WorkspaceSession`(같은 project_id, `memory_snapshot_id=None`)이
    실제 `InMemoryContextManager`/`InMemoryMemoryEngine`을 통해 이전
    세션이 만든 요약을 자동으로 이어받는다. 두 번째 세션에는 일부러
    `DocumentationAgent`를 연결하지 않는다 — 연결하면 그 세션의 새
    Mission이 끝나자마자 자신의 새 요약으로 즉시 덮어써서(M8-T02, "누적이
    아니라 최신 하나만 유지") 이어받은 상태를 관찰할 수 없게 되기
    때문이다(그 "덮어쓰기" 자체는
    test_documentation_agent_second_mission_overwrites_session_snapshot_id
    가 별도로 이미 검증했다)."""
    first_pipeline = build_pipeline()
    task = first_pipeline["planning_agent"].plan_mission("p1", "첫 번째 작업")
    expected_summary = f"{task.task_id} 완료(Mock)"

    new_session = WorkspaceSession(session_id="s2", current_project_id="p1")
    new_planning_agent = PlanningAgent(
        agent_runtime=AgentRuntime(
            agent_manager=FakeAgentManager(), agent_registry=FakeAgentRegistry()
        ),
        event_bus=InMemoryEventBus(),
        task_engine=InMemoryTaskEngine(),
        context_manager=first_pipeline["context_manager"],
        workspace_session=new_session,
    )

    new_planning_agent.plan_mission("p1", "두 번째 세션의 작업")

    assert new_session.memory_snapshot_id == first_pipeline["workspace_session"].memory_snapshot_id
    inherited_context = first_pipeline["context_manager"].assemble_context(new_session)
    assert inherited_context["summary"] == expected_summary


def test_reset_mission_does_not_inherit_previous_session_summary() -> None:
    """M9-T04: Milestone DoD — 새 `WorkspaceSession`이 `reset=True`로
    Mission을 시작하면, 이전 세션이 만든 요약이 있어도 이어받지 않는다
    (M9-T03). `test_new_session_inherits_previous_session_summary_via_
    planning_agent`(reset 없음, 자동 복원됨)와 대비되는 시나리오다."""
    first_pipeline = build_pipeline()
    first_pipeline["planning_agent"].plan_mission("p1", "첫 번째 작업")

    new_session = WorkspaceSession(session_id="s2", current_project_id="p1")
    new_planning_agent = PlanningAgent(
        agent_runtime=AgentRuntime(
            agent_manager=FakeAgentManager(), agent_registry=FakeAgentRegistry()
        ),
        event_bus=InMemoryEventBus(),
        task_engine=InMemoryTaskEngine(),
        context_manager=first_pipeline["context_manager"],
        workspace_session=new_session,
    )

    new_planning_agent.plan_mission("p1", "리셋된 두 번째 세션의 작업", reset=True)

    assert new_session.memory_snapshot_id is None


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
