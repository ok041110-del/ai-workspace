from __future__ import annotations

from tests.agents.test_coding_agent import RecordingEngineRuntime
from tests.interfaces.fakes import (
    FakeAgentManager,
    FakeAgentRegistry,
    FakeAgentScheduler,
    FakeTaskEngine,
)

from ai_workspace.agents.events import CODE_VERIFIED, REVIEW_COMPLETED
from ai_workspace.agents.review_agent import ReviewAgent
from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMEffort, LLMModel, LLMPolicyDecision, LLMProvider
from ai_workspace.engines.llm_policy_engine import InMemoryLLMPolicyEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.engine_adapter import EngineResult
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.llm_policy_engine import LLMPolicyEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


def build_review_agent(
    engine_runtime: RecordingEngineRuntime,
    *,
    llm_policy_engine: LLMPolicyEngine | None = None,
) -> tuple[ReviewAgent, InMemoryEventBus, FakeTaskEngine]:
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        llm_policy_engine=llm_policy_engine,
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
            event_type=CODE_VERIFIED,
            payload={"task_id": task.task_id, "output": "def login(): ...", "success": True},
        )
    )

    assert len(engine_runtime.received_tasks) == 1
    prompt = engine_runtime.received_tasks[0].title
    assert "로그인 기능 구현하기" in prompt
    assert "def login(): ..." in prompt


def test_review_agent_handles_missing_prior_output() -> None:
    """CoordinatorAgent 없이 CodeVerified가 직접 발행되는 등, output이
    없는 경우에도 예외 없이 동작해야 한다(prior_output=None으로 처리)."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="검토 완료"))
    _agent, event_bus, task_engine = build_review_agent(engine_runtime)
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(event_id="e1", event_type=CODE_VERIFIED, payload={"task_id": task.task_id})
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
            event_type=CODE_VERIFIED,
            payload={"task_id": task.task_id, "output": "def login(): ...", "success": True},
        )
    )

    review_completed = next(e for e in received if e.event_type == REVIEW_COMPLETED)
    assert review_completed.payload["output"] == "문제 발견"
    assert review_completed.payload["success"] is False


def test_review_agent_passes_required_capabilities_from_llm_policy_decision() -> None:
    """M6-T02: REVIEWER Role에 OPENAI 정책이 있으면 실제로
    required_capabilities={"codex"}가 전달된다."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="검토 완료"))
    policy_engine = InMemoryLLMPolicyEngine(
        {
            AgentRole.REVIEWER: LLMPolicyDecision(
                LLMModel(LLMProvider.OPENAI, "gpt"), LLMEffort.MEDIUM
            )
        }
    )
    _agent, event_bus, task_engine = build_review_agent(
        engine_runtime, llm_policy_engine=policy_engine
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=CODE_VERIFIED,
            payload={"task_id": task.task_id, "output": "def login(): ...", "success": True},
        )
    )

    assert engine_runtime.received_required_capabilities == [frozenset({"codex"})]


def test_review_agent_passes_model_from_llm_policy_decision() -> None:
    """M14-T03: REVIEWER Role에 gpt 모델 정책이 있으면 실제로
    model="gpt"가 전달된다."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="검토 완료"))
    policy_engine = InMemoryLLMPolicyEngine(
        {
            AgentRole.REVIEWER: LLMPolicyDecision(
                LLMModel(LLMProvider.OPENAI, "gpt"), LLMEffort.MEDIUM
            )
        }
    )
    _agent, event_bus, task_engine = build_review_agent(
        engine_runtime, llm_policy_engine=policy_engine
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=CODE_VERIFIED,
            payload={"task_id": task.task_id, "output": "def login(): ...", "success": True},
        )
    )

    assert engine_runtime.received_models == ["gpt"]


def test_review_agent_both_instances_run_when_max_parallel_agents_is_two() -> None:
    """M58(ADR-0076) — max_parallel_agents=2를 두 인스턴스 모두에 주면
    같은 Event를 병렬로 처리한다."""
    shared_registry = FakeAgentRegistry()
    shared_manager = FakeAgentManager()
    shared_scheduler = FakeAgentScheduler()
    event_bus = InMemoryEventBus()
    task_engine = FakeTaskEngine()
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="검토 완료"))

    first_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    ReviewAgent(
        agent_runtime=first_agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
        max_parallel_agents=2,
    )
    second_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    ReviewAgent(
        agent_runtime=second_agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
        max_parallel_agents=2,
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=CODE_VERIFIED,
            payload={"task_id": task.task_id, "output": "def login(): ...", "success": True},
        )
    )

    assert len(engine_runtime.received_tasks) == 2


def test_review_agent_ignores_code_verified_when_not_selected_by_scheduler() -> None:
    """M56(ADR-0074) — CodingAgent(M13)와 동일한 패턴: 같은 REVIEW
    Capability를 가진 다른 ReviewAgent 인스턴스가 Scheduler에게
    선택되면, 선택되지 않은 인스턴스는 아무것도 하지 않는다."""
    shared_registry = FakeAgentRegistry()
    shared_manager = FakeAgentManager()
    shared_scheduler = FakeAgentScheduler()
    event_bus = InMemoryEventBus()
    task_engine = FakeTaskEngine()
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="검토 완료"))

    selected_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    ReviewAgent(
        agent_runtime=selected_agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
    )
    unselected_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    ReviewAgent(
        agent_runtime=unselected_agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=CODE_VERIFIED,
            payload={"task_id": task.task_id, "output": "def login(): ...", "success": True},
        )
    )

    assert len(engine_runtime.received_tasks) == 1
