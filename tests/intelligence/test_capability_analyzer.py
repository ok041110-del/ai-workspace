from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.intelligence.capability import CapabilitySnapshotAnalyzer
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler


def _make_adapter() -> AgentAdapter:
    return AgentAdapter(InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler())


def test_analyze_counts_active_agents_by_capability_and_role() -> None:
    adapter = _make_adapter()
    adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING, AgentCapability.GIT}))
    adapter.create_agent(AgentRole.REVIEWER, frozenset({AgentCapability.REVIEW}))
    analyzer = CapabilitySnapshotAnalyzer(adapter)

    snapshot = analyzer.analyze()

    assert snapshot.total_active_agents == 2
    assert snapshot.by_role == {"coding": 1, "reviewer": 1}
    assert snapshot.by_capability["coding"] == 1
    assert snapshot.by_capability["git"] == 1
    assert snapshot.by_capability["review"] == 1
    assert snapshot.by_capability["voice"] == 0


def test_analyze_known_capabilities_includes_all_domain_values() -> None:
    adapter = _make_adapter()
    analyzer = CapabilitySnapshotAnalyzer(adapter)

    snapshot = analyzer.analyze()

    assert snapshot.known_capabilities == frozenset(c.value for c in AgentCapability)
    assert set(snapshot.by_capability) == snapshot.known_capabilities


def test_analyze_empty_when_no_active_agents() -> None:
    adapter = _make_adapter()
    analyzer = CapabilitySnapshotAnalyzer(adapter)

    snapshot = analyzer.analyze()

    assert snapshot.total_active_agents == 0
    assert snapshot.by_role == {}
    assert all(count == 0 for count in snapshot.by_capability.values())
