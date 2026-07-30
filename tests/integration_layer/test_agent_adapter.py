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
