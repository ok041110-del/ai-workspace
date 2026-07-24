from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus


def test_agent_defaults_to_idle() -> None:
    agent = Agent(agent_id="a1", role=AgentRole.CODING)

    assert agent.status == AgentStatus.IDLE
    assert agent.capabilities == frozenset()


def test_agent_can_hold_multiple_capabilities_including_coordination() -> None:
    agent = Agent(
        agent_id="a1",
        role=AgentRole.COORDINATOR,
        capabilities=frozenset({AgentCapability.COORDINATION, AgentCapability.PLANNING}),
    )

    assert AgentCapability.COORDINATION in agent.capabilities
    assert AgentCapability.PLANNING in agent.capabilities
