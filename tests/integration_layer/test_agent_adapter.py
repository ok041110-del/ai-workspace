from ai_workspace.domain.agent import AgentCapability, AgentRole, AgentStatus
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler


def _make_adapter() -> AgentAdapter:
    return AgentAdapter(InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler())


def test_create_agent_registers_it() -> None:
    adapter = _make_adapter()

    agent = adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))

    assert agent in adapter.list_active_agents()


def test_select_agent_matches_capability() -> None:
    adapter = _make_adapter()
    coding_agent = adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    adapter.create_agent(AgentRole.REVIEWER, frozenset({AgentCapability.REVIEW}))

    selected = adapter.select_agent(AgentCapability.CODING)

    assert selected == [coding_agent]


def test_transition_agent_delegates_to_manager() -> None:
    adapter = _make_adapter()
    agent = adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))

    transitioned = adapter.transition_agent(agent, AgentStatus.RUNNING)

    assert transitioned.status is AgentStatus.RUNNING


def test_list_active_agent_capabilities_returns_views() -> None:
    adapter = _make_adapter()
    agent = adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))

    views = adapter.list_active_agent_capabilities()

    assert len(views) == 1
    view = views[0]
    assert view.agent_id == agent.agent_id
    assert view.role == "coding"
    assert view.capabilities == frozenset({"coding"})
    assert view.status == "idle"


def test_list_active_agent_capabilities_empty_when_no_agents() -> None:
    adapter = _make_adapter()

    assert adapter.list_active_agent_capabilities() == []


def test_known_capabilities_returns_all_domain_values() -> None:
    adapter = _make_adapter()

    known = adapter.known_capabilities()

    assert known == frozenset(capability.value for capability in AgentCapability)
