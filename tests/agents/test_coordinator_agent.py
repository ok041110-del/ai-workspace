from __future__ import annotations

from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry, FakeTaskEngine

from ai_workspace.agents.coordinator_agent import CoordinatorAgent
from ai_workspace.agents.events import (
    CODE_VERIFIED,
    MISSION_PLANNED,
    REWORK_EXHAUSTED,
    SHELL_COMPLETED,
)
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


def build_coordinator(
    max_rework_attempts: int = 3,
) -> tuple[CoordinatorAgent, InMemoryEventBus, FakeTaskEngine]:
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(), agent_registry=FakeAgentRegistry()
    )
    event_bus = InMemoryEventBus()
    task_engine = FakeTaskEngine()
    agent = CoordinatorAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        max_rework_attempts=max_rework_attempts,
    )
    return agent, event_bus, task_engine


def test_successful_shell_result_publishes_code_verified() -> None:
    _agent, event_bus, task_engine = build_coordinator()
    task = task_engine.create_task("p1", "구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=SHELL_COMPLETED,
            payload={"task_id": task.task_id, "success": True, "code_output": "def f(): ..."},
        )
    )

    verified = next(e for e in received if e.event_type == CODE_VERIFIED)
    assert verified.payload == {"task_id": task.task_id, "output": "def f(): ..."}


def test_failed_shell_result_republishes_mission_planned_with_reason() -> None:
    _agent, event_bus, task_engine = build_coordinator()
    task = task_engine.create_task("p1", "구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=SHELL_COMPLETED,
            payload={"task_id": task.task_id, "success": False, "stderr": "1 failed"},
        )
    )

    replanned = [e for e in received if e.event_type == MISSION_PLANNED]
    assert len(replanned) == 1
    assert replanned[0].payload == {"task_id": task.task_id, "rework_reason": "1 failed"}


def test_failed_shell_result_records_step_via_task_engine() -> None:
    """Step의 소유권은 CoordinatorAgent가 아니라 실행 컨텍스트(TaskEngine)
    에 있다 — CoordinatorAgent는 자체적으로 이력을 보관하지 않는다."""
    _agent, event_bus, task_engine = build_coordinator()
    task = task_engine.create_task("p1", "구현하기")

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=SHELL_COMPLETED,
            payload={"task_id": task.task_id, "success": False, "stderr": "1 failed"},
        )
    )

    steps = task_engine.get_steps(task.task_id)
    assert len(steps) == 1
    assert "1 failed" in steps[0].description


def test_exceeding_max_rework_attempts_publishes_rework_exhausted() -> None:
    _agent, event_bus, task_engine = build_coordinator(max_rework_attempts=2)
    task = task_engine.create_task("p1", "구현하기")

    failure = Event(
        event_id="e1",
        event_type=SHELL_COMPLETED,
        payload={"task_id": task.task_id, "success": False, "stderr": "실패"},
    )
    event_bus.publish(failure)
    event_bus.publish(failure)
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(failure)

    exhausted = next(e for e in received if e.event_type == REWORK_EXHAUSTED)
    assert exhausted.payload["task_id"] == task.task_id
    assert not any(e.event_type == MISSION_PLANNED for e in received)
    assert len(task_engine.get_steps(task.task_id)) == 3


def test_ignores_unrelated_event_types() -> None:
    _agent, event_bus, task_engine = build_coordinator()
    task = task_engine.create_task("p1", "구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type="unrelated", payload={"task_id": task.task_id})
    )

    assert [e.event_type for e in received] == ["unrelated"]
    assert task_engine.get_steps(task.task_id) == []
