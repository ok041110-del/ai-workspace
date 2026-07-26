from __future__ import annotations

from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry, FakeTaskEngine

from ai_workspace.agents.coding_agent import CodingAgent
from ai_workspace.agents.events import CODE_COMPLETED, MISSION_PLANNED
from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMEffort, LLMModel, LLMPolicyDecision, LLMProvider
from ai_workspace.domain.task import Task
from ai_workspace.engines.llm_policy_engine import InMemoryLLMPolicyEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.engine_adapter import EngineResult
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.llm_policy_engine import LLMPolicyEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class RecordingEngineRuntime(EngineRuntime):
    """실제로 넘어온 Task(특히 title)와 required_capabilities(M6-T02)를
    기록하는 테스트 더블."""

    def __init__(self, result: EngineResult) -> None:
        self._result = result
        self.received_tasks: list[Task] = []
        self.received_required_capabilities: list[frozenset[str]] = []

    def register_engine(self, name, adapter) -> None:
        raise NotImplementedError

    def run(self, task: Task, required_capabilities: frozenset[str] = frozenset()) -> EngineResult:
        self.received_tasks.append(task)
        self.received_required_capabilities.append(required_capabilities)
        return self._result

    def run_parallel(self, tasks, required_capabilities: frozenset[str] = frozenset()):
        raise NotImplementedError

    def cancel(self, task_id: str) -> None:
        raise NotImplementedError

    def status(self, task_id: str):
        raise NotImplementedError


def build_coding_agent(
    engine_runtime: RecordingEngineRuntime,
    *,
    llm_policy_engine: LLMPolicyEngine | None = None,
) -> tuple[CodingAgent, InMemoryEventBus, FakeTaskEngine]:
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        llm_policy_engine=llm_policy_engine,
    )
    event_bus = InMemoryEventBus()
    task_engine = FakeTaskEngine()
    agent = CodingAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
    )
    return agent, event_bus, task_engine


def test_coding_agent_passes_task_title_as_instructions_when_no_prior_context() -> None:
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="완료"))
    _agent, event_bus, task_engine = build_coding_agent(engine_runtime)
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    assert len(engine_runtime.received_tasks) == 1
    assert engine_runtime.received_tasks[0].title == "로그인 기능 구현하기"


def test_coding_agent_includes_rework_reason_as_prior_output() -> None:
    """M5-T06: `CoordinatorAgent`가 테스트 실패 후 재발행한 MissionPlanned
    (payload에 rework_reason 포함)을 받으면, 이전에 무엇이 실패했는지
    프롬프트에 반영한다."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="완료"))
    _agent, event_bus, task_engine = build_coding_agent(engine_runtime)
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=MISSION_PLANNED,
            payload={"task_id": task.task_id, "rework_reason": "AssertionError: 로그인 실패"},
        )
    )

    prompt = engine_runtime.received_tasks[0].title
    assert "로그인 기능 구현하기" in prompt
    assert "AssertionError: 로그인 실패" in prompt


def test_coding_agent_does_not_mutate_original_task_title() -> None:
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="완료"))
    _agent, event_bus, task_engine = build_coding_agent(engine_runtime)
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    assert task_engine.get_task(task.task_id).title == "로그인 기능 구현하기"


def test_coding_agent_publishes_output_and_success_in_event_payload() -> None:
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="def login(): ..."))
    _agent, event_bus, task_engine = build_coding_agent(engine_runtime)
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    code_completed = next(e for e in received if e.event_type == CODE_COMPLETED)
    assert code_completed.payload["output"] == "def login(): ..."
    assert code_completed.payload["success"] is True


def test_coding_agent_passes_no_required_capabilities_when_no_policy_engine() -> None:
    """M6-T02: LLMPolicyEngine이 주입되지 않으면(기존 모든 조립 코드)
    required_capabilities는 빈 집합이어야 한다 — 기존 동작과 완전히
    하위 호환."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="완료"))
    _agent, event_bus, task_engine = build_coding_agent(engine_runtime)
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    assert engine_runtime.received_required_capabilities == [frozenset()]


def test_coding_agent_passes_required_capabilities_from_llm_policy_decision() -> None:
    """M6-T02: LLMPolicyEngine이 CODING Role에 ANTHROPIC 정책을 주면,
    실제로 `required_capabilities={"claude_code"}`가 engine_runtime.run()에
    전달된다 — Policy→Execution 라우팅의 핵심 경로."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="완료"))
    policy_engine = InMemoryLLMPolicyEngine(
        {
            AgentRole.CODING: LLMPolicyDecision(
                LLMModel(LLMProvider.ANTHROPIC, "opus"), LLMEffort.HIGH
            )
        }
    )
    _agent, event_bus, task_engine = build_coding_agent(
        engine_runtime, llm_policy_engine=policy_engine
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    assert engine_runtime.received_required_capabilities == [frozenset({"claude_code"})]
