from __future__ import annotations

from tests.agents.test_coding_agent import RecordingEngineRuntime
from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry, FakeTaskEngine

from ai_workspace.agents.events import CODE_COMPLETED, REVIEW_COMPLETED
from ai_workspace.agents.review_agent import ReviewAgent
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.engine_adapter import EngineResult
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


def build_review_agent(
    engine_runtime: RecordingEngineRuntime,
) -> tuple[ReviewAgent, InMemoryEventBus, FakeTaskEngine]:
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(), agent_registry=FakeAgentRegistry()
    )
    event_bus = InMemoryEventBus()
    task_engine = FakeTaskEngine()
    agent = ReviewAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
    )
    return agent, event_bus, task_engine


def test_review_agent_includes_coding_output_as_prior_output_in_prompt() -> None:
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="검토 완료"))
    _agent, event_bus, task_engine = build_review_agent(engine_runtime)
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=CODE_COMPLETED,
            payload={"task_id": task.task_id, "output": "def login(): ...", "success": True},
        )
    )

    assert len(engine_runtime.received_tasks) == 1
    prompt = engine_runtime.received_tasks[0].title
    assert "로그인 기능 구현하기" in prompt
    assert "def login(): ..." in prompt


def test_review_agent_handles_missing_prior_output() -> None:
    """CodingAgent 없이 CodeCompleted가 직접 발행되는 등, output이 없는
    경우에도 예외 없이 동작해야 한다(prior_output=None으로 처리)."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="검토 완료"))
    _agent, event_bus, task_engine = build_review_agent(engine_runtime)
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(event_id="e1", event_type=CODE_COMPLETED, payload={"task_id": task.task_id})
    )

    assert engine_runtime.received_tasks[0].title == "로그인 기능 구현하기"


def test_review_agent_publishes_output_and_success_in_event_payload() -> None:
    engine_runtime = RecordingEngineRuntime(EngineResult(success=False, output="문제 발견"))
    _agent, event_bus, task_engine = build_review_agent(engine_runtime)
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=CODE_COMPLETED,
            payload={"task_id": task.task_id, "output": "def login(): ...", "success": True},
        )
    )

    review_completed = next(e for e in received if e.event_type == REVIEW_COMPLETED)
    assert review_completed.payload["output"] == "문제 발견"
    assert review_completed.payload["success"] is False
