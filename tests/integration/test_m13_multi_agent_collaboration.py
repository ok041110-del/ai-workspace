from __future__ import annotations

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.agents.coding_agent import CodingAgent
from ai_workspace.agents.events import CODE_COMPLETED, MISSION_PLANNED
from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime


def test_only_scheduler_selected_coding_agent_processes_mission_planned() -> None:
    """Milestone 13 DoD 2·3번: 실제 InMemoryAgentManager/InMemoryAgentRegistry
    /InMemoryAgentScheduler(Fake 아님)로 같은 CODING Capability의
    CodingAgent 2개를 등록해도, MissionPlanned 하나에 대해 Scheduler가
    고른 1개만 Task를 처리하고 CodeCompleted를 발행한다."""
    agent_manager = InMemoryAgentManager()
    agent_registry = InMemoryAgentRegistry()
    agent_scheduler = InMemoryAgentScheduler()
    event_bus = InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    engine_runtime = InMemoryEngineRuntime()
    engine_runtime.register_engine("mock", MockEngineAdapter())

    first_runtime = AgentRuntime(agent_manager=agent_manager, agent_registry=agent_registry)
    CodingAgent(
        agent_runtime=first_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        agent_registry=agent_registry,
        agent_scheduler=agent_scheduler,
    )
    second_runtime = AgentRuntime(agent_manager=agent_manager, agent_registry=agent_registry)
    CodingAgent(
        agent_runtime=second_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        agent_registry=agent_registry,
        agent_scheduler=agent_scheduler,
    )

    task = task_engine.create_task("p1", "구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    code_completed_events = [e for e in received if e.event_type == CODE_COMPLETED]
    assert len(code_completed_events) == 1
    assert task_engine.get_task(task.task_id).status == TaskStatus.REVIEW


def test_single_registered_coding_agent_still_works_with_guard_enabled() -> None:
    """가드가 켜져 있어도(agent_registry/agent_scheduler 주입) 등록된
    CodingAgent가 하나뿐이면 항상 자기 자신이 선택되어 정상 동작한다."""
    agent_manager = InMemoryAgentManager()
    agent_registry = InMemoryAgentRegistry()
    agent_scheduler = InMemoryAgentScheduler()
    event_bus = InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    engine_runtime = InMemoryEngineRuntime()
    engine_runtime.register_engine("mock", MockEngineAdapter())

    agent_runtime = AgentRuntime(agent_manager=agent_manager, agent_registry=agent_registry)
    CodingAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        agent_registry=agent_registry,
        agent_scheduler=agent_scheduler,
    )
    task = task_engine.create_task("p1", "구현하기")

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    assert task_engine.get_task(task.task_id).status == TaskStatus.REVIEW
