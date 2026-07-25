from __future__ import annotations

import pytest
from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry

from ai_workspace.domain.agent import AgentCapability, AgentRole, AgentStatus
from ai_workspace.interfaces.agent_registry import AgentNotRegisteredError
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime, AgentSessionNotFoundError


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
