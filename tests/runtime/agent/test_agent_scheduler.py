from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler


def make_agent(agent_id: str, capabilities: frozenset[AgentCapability] = frozenset()) -> Agent:
    return Agent(agent_id=agent_id, role=AgentRole.CODING, capabilities=capabilities)


def test_select_returns_agents_with_matching_capability() -> None:
    scheduler = InMemoryAgentScheduler()
    matching = make_agent("a1", frozenset({AgentCapability.CODING}))
    other = make_agent("a2", frozenset({AgentCapability.REVIEW}))

    selected = scheduler.select([matching, other], AgentCapability.CODING)

    assert selected == [matching]


def test_select_respects_max_count() -> None:
    scheduler = InMemoryAgentScheduler()
    agents = [
        make_agent("a1", frozenset({AgentCapability.CODING})),
        make_agent("a2", frozenset({AgentCapability.CODING})),
        make_agent("a3", frozenset({AgentCapability.CODING})),
    ]

    selected = scheduler.select(agents, AgentCapability.CODING, max_count=2)

    assert selected == agents[:2]


def test_select_returns_empty_list_when_no_match() -> None:
    scheduler = InMemoryAgentScheduler()
    agent = make_agent("a1", frozenset({AgentCapability.REVIEW}))

    selected = scheduler.select([agent], AgentCapability.CODING)

    assert selected == []
