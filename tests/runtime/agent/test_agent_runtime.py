from __future__ import annotations

from pathlib import Path

import pytest
from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry, FakeLLMPolicyEngine

from ai_workspace.domain.agent import AgentCapability, AgentRole, AgentStatus
from ai_workspace.domain.llm_policy import LLMEffort, LLMModel, LLMPolicyDecision, LLMProvider
from ai_workspace.engines.llm_policy_engine import InMemoryLLMPolicyEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.agent_registry import AgentNotRegisteredError
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.remote_agent_dispatcher import AgentUnreachableError
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime, AgentSessionNotFoundError
from ai_workspace.runtime.agent.remote_agent_dispatcher import LoopbackAgentDispatcher
from ai_workspace.storage.llm_policy_loader import load_llm_policy_rules

_EXAMPLE_YAML = Path(__file__).resolve().parents[3] / "docs" / "llm_policy.example.yaml"


def make_runtime(
    agent_registry: FakeAgentRegistry | None = None,
) -> AgentRuntime:
    return AgentRuntime(
        agent_manager=FakeAgentManager(), agent_registry=agent_registry or FakeAgentRegistry()
    )


def test_start_agent_creates_registers_and_runs_agent() -> None:
    runtime = make_runtime()

    session = runtime.start_agent(AgentRole.CODING)

    assert runtime.get_agent_state(session.session_id) == AgentStatus.RUNNING


def test_start_agent_keeps_given_capabilities() -> None:
    agent_registry = FakeAgentRegistry()
    runtime = make_runtime(agent_registry)

    session = runtime.start_agent(
        AgentRole.CODING, capabilities=frozenset({AgentCapability.CODING})
    )

    agent = agent_registry.get(session.agent_id)
    assert AgentCapability.CODING in agent.capabilities


def test_start_agent_returns_unique_session_ids() -> None:
    runtime = make_runtime()

    session1 = runtime.start_agent(AgentRole.CODING)
    session2 = runtime.start_agent(AgentRole.CODING)

    assert session1.session_id != session2.session_id
    assert session1.agent_id != session2.agent_id


def test_stop_agent_transitions_to_stopped_and_removes_from_registry() -> None:
    agent_registry = FakeAgentRegistry()
    runtime = make_runtime(agent_registry)
    session = runtime.start_agent(AgentRole.CODING)

    runtime.stop_agent(session.session_id)

    with pytest.raises(AgentNotRegisteredError):
        agent_registry.get(session.agent_id)


def test_stop_agent_removes_session() -> None:
    runtime = make_runtime()
    session = runtime.start_agent(AgentRole.CODING)

    runtime.stop_agent(session.session_id)

    with pytest.raises(AgentSessionNotFoundError):
        runtime.get_session(session.session_id)


def test_stop_agent_unknown_session_raises_error() -> None:
    runtime = make_runtime()

    with pytest.raises(AgentSessionNotFoundError):
        runtime.stop_agent("unknown")


def test_get_session_unknown_raises_error() -> None:
    runtime = make_runtime()

    with pytest.raises(AgentSessionNotFoundError):
        runtime.get_session("unknown")


def test_get_agent_state_unknown_session_raises_error() -> None:
    runtime = make_runtime()

    with pytest.raises(AgentSessionNotFoundError):
        runtime.get_agent_state("unknown")


def test_shutdown_stops_all_active_sessions() -> None:
    runtime = make_runtime()
    session1 = runtime.start_agent(AgentRole.CODING)
    session2 = runtime.start_agent(AgentRole.REVIEWER)

    runtime.shutdown()

    with pytest.raises(AgentSessionNotFoundError):
        runtime.get_session(session1.session_id)
    with pytest.raises(AgentSessionNotFoundError):
        runtime.get_session(session2.session_id)


def test_shutdown_with_no_active_sessions_does_nothing() -> None:
    runtime = make_runtime()

    runtime.shutdown()  # 예외 없이 종료되어야 한다


def test_stop_agent_twice_raises_session_not_found_on_second_call() -> None:
    runtime = make_runtime()
    session = runtime.start_agent(AgentRole.CODING)
    runtime.stop_agent(session.session_id)

    with pytest.raises(AgentSessionNotFoundError):
        runtime.stop_agent(session.session_id)


def test_start_agent_without_llm_policy_engine_leaves_decision_none() -> None:
    runtime = make_runtime()

    session = runtime.start_agent(AgentRole.CODING)

    assert session.llm_policy_decision is None


def test_start_agent_records_llm_policy_decision_when_engine_provided() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    llm_policy_engine = FakeLLMPolicyEngine({AgentRole.CODING: decision})
    runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        llm_policy_engine=llm_policy_engine,
    )

    session = runtime.start_agent(AgentRole.CODING)

    assert session.llm_policy_decision == decision


def test_start_agent_records_none_when_role_has_no_policy() -> None:
    llm_policy_engine = FakeLLMPolicyEngine({})
    runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        llm_policy_engine=llm_policy_engine,
    )

    session = runtime.start_agent(AgentRole.COORDINATOR)

    assert session.llm_policy_decision is None


def test_start_agent_reflects_real_policy_loaded_from_example_yaml() -> None:
    """M5-T02: 실제 `InMemoryLLMPolicyEngine`을 실제 `docs/llm_policy.
    example.yaml`로 구성해 AgentRuntime에 연결하면, start_agent() 시점에
    해당 Role의 실제 정책이 세션에 기록됨을 증명한다(가짜가 아닌 전체
    조립으로 "연결"을 검증)."""
    llm_policy_engine = InMemoryLLMPolicyEngine(load_llm_policy_rules(_EXAMPLE_YAML))
    runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        llm_policy_engine=llm_policy_engine,
    )

    session = runtime.start_agent(AgentRole.CODING)

    assert session.llm_policy_decision == LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )


def test_record_llm_policy_outcome_forwards_to_engine() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    llm_policy_engine = FakeLLMPolicyEngine({AgentRole.CODING: decision})
    runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        llm_policy_engine=llm_policy_engine,
    )
    session = runtime.start_agent(AgentRole.CODING)

    runtime.record_llm_policy_outcome(session.session_id, True)

    assert llm_policy_engine.recorded_outcomes == [(AgentRole.CODING, decision, True)]


def test_record_llm_policy_outcome_without_engine_is_noop() -> None:
    runtime = make_runtime()
    session = runtime.start_agent(AgentRole.CODING)

    runtime.record_llm_policy_outcome(session.session_id, True)


def test_record_llm_policy_outcome_without_decision_is_noop() -> None:
    llm_policy_engine = FakeLLMPolicyEngine({})
    runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        llm_policy_engine=llm_policy_engine,
    )
    session = runtime.start_agent(AgentRole.COORDINATOR)

    runtime.record_llm_policy_outcome(session.session_id, True)

    assert llm_policy_engine.recorded_outcomes == []


def test_start_agent_without_location_leaves_agent_location_none() -> None:
    agent_registry = FakeAgentRegistry()
    runtime = make_runtime(agent_registry)

    session = runtime.start_agent(AgentRole.CODING)

    assert agent_registry.get(session.agent_id).location is None


def test_start_agent_with_location_records_it_on_agent() -> None:
    agent_registry = FakeAgentRegistry()
    runtime = make_runtime(agent_registry)

    session = runtime.start_agent(AgentRole.CODING, location="worker-1")

    assert agent_registry.get(session.agent_id).location == "worker-1"


def test_dispatch_event_does_nothing_for_local_agent() -> None:
    """location이 없는(로컬) Agent는 dispatch_event()가 개입하지 않는다 —
    remote_agent_dispatcher가 없어도 예외 없이 조용히 반환한다."""
    runtime = make_runtime()
    session = runtime.start_agent(AgentRole.CODING)

    runtime.dispatch_event(session.session_id, Event(event_id="e1", event_type="x"))  # no raise


def test_dispatch_event_without_dispatcher_raises_for_remote_agent() -> None:
    runtime = make_runtime()
    session = runtime.start_agent(AgentRole.CODING, location="worker-1")

    with pytest.raises(ValueError):
        runtime.dispatch_event(session.session_id, Event(event_id="e1", event_type="x"))


def test_dispatch_event_forwards_to_remote_location_event_bus() -> None:
    dispatcher = LoopbackAgentDispatcher()
    remote_bus = InMemoryEventBus()
    dispatcher.register_location("worker-1", remote_bus)
    received: list[Event] = []
    remote_bus.subscribe(received.append)
    runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        remote_agent_dispatcher=dispatcher,
    )
    session = runtime.start_agent(AgentRole.CODING, location="worker-1")
    event = Event(event_id="e1", event_type="mission_planned")

    runtime.dispatch_event(session.session_id, event)

    assert received == [event]


def test_dispatch_event_unreachable_location_raises() -> None:
    dispatcher = LoopbackAgentDispatcher()
    runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        remote_agent_dispatcher=dispatcher,
    )
    session = runtime.start_agent(AgentRole.CODING, location="unknown-worker")

    with pytest.raises(AgentUnreachableError):
        runtime.dispatch_event(session.session_id, Event(event_id="e1", event_type="x"))
