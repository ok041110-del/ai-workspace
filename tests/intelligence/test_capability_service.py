from pathlib import Path

from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_service import (
    CapabilityIntelligenceService,
    render_markdown,
)
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler


def _make_agent_adapter() -> AgentAdapter:
    return AgentAdapter(InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler())


def _make_vault(tmp_path: Path) -> Path:
    (tmp_path / "11 Milestones").mkdir(parents=True)
    (tmp_path / "11 Milestones" / "Milestones Index.md").write_text(
        "# Milestones Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    return tmp_path


def test_generate_combines_snapshot_and_gap_report() -> None:
    agent_adapter = _make_agent_adapter()
    agent_adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    service = CapabilityIntelligenceService(agent_adapter)

    report = service.generate()

    assert report.snapshot.total_active_agents == 1
    assert report.snapshot.by_capability["coding"] == 1
    assert "coding" not in {gap.capability for gap in report.gap_report.gaps}


def test_generate_reports_gap_when_no_active_agents() -> None:
    service = CapabilityIntelligenceService(_make_agent_adapter())

    report = service.generate()

    assert report.snapshot.total_active_agents == 0
    assert len(report.gap_report.gaps) == len(report.snapshot.known_capabilities)


def test_publish_raises_without_vault_adapter() -> None:
    service = CapabilityIntelligenceService(_make_agent_adapter())

    try:
        service.publish()
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError를 기대했지만 발생하지 않음")


def test_publish_writes_markdown_to_vault(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    agent_adapter = _make_agent_adapter()
    agent_adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    service = CapabilityIntelligenceService(agent_adapter, VaultAdapter(vault_root))

    report, path = service.publish()

    assert path == vault_root / "15 Project Intelligence" / "Capability Intelligence.md"
    content = path.read_text(encoding="utf-8")
    assert "# Capability Intelligence" in content
    assert report.snapshot.total_active_agents == 1


def test_render_markdown_includes_all_sections() -> None:
    service = CapabilityIntelligenceService(_make_agent_adapter())
    report = service.generate()

    markdown = render_markdown(report)

    assert "## Snapshot" in markdown
    assert "### Role별" in markdown
    assert "### Capability별" in markdown
    assert "## Coverage" in markdown
    assert "## Gap" in markdown
