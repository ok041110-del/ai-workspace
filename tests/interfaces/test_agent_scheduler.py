from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole

from .fakes import FakeAgentScheduler


def test_select_returns_only_agents_with_capability() -> None:
    scheduler = FakeAgentScheduler()
    matching = Agent(
        agent_id="a1", role=AgentRole.CODING, capabilities=frozenset({AgentCapability.CODING})
    )
    other = Agent(
        agent_id="a2", role=AgentRole.REVIEWER, capabilities=frozenset({AgentCapability.REVIEW})
    )

    selected = scheduler.select([matching, other], AgentCapability.CODING)

    assert selected == [matching]


def test_select_respects_max_count() -> None:
    scheduler = FakeAgentScheduler()
    agents = [
        Agent(
            agent_id=f"a{i}",
            role=AgentRole.CODING,
            capabilities=frozenset({AgentCapability.CODING}),
        )
        for i in range(3)
    ]

    selected = scheduler.select(agents, AgentCapability.CODING, max_count=2)

    assert len(selected) == 2


def test_select_returns_empty_list_when_no_match() -> None:
    scheduler = FakeAgentScheduler()
    agent = Agent(agent_id="a1", role=AgentRole.CODING, capabilities=frozenset())

    selected = scheduler.select([agent], AgentCapability.CODING)

    assert selected == []
