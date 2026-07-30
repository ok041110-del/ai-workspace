from pathlib import Path

from tests.interfaces.fakes import FakeKnowledgeRepository

from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.knowledge_adapter import KnowledgeAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_service import CapabilityIntelligenceService
from ai_workspace.intelligence.context_service import ContextIntelligenceService
from ai_workspace.intelligence.report import ProjectIntelligenceService
from ai_workspace.intelligence.synthesis_service import (
    IntelligenceSynthesisService,
    render_markdown,
)
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler

_ADR_CONTENT = """# DECISIONS

## ADR-0046: Intelligence Synthesis 설계 (Milestone 32-T01)

내용.
"""


def _make_vault(tmp_path: Path) -> Path:
    (tmp_path / "11 Milestones").mkdir(parents=True)
    (tmp_path / "11 Milestones" / "Milestones Index.md").write_text(
        "# Milestones Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    (tmp_path / "12 Decisions").mkdir(parents=True)
    (tmp_path / "12 Decisions" / "Decisions Index.md").write_text(
        "# Decisions Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    return tmp_path


def _make_agent_adapter() -> AgentAdapter:
    return AgentAdapter(InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler())


def _make_knowledge_adapter() -> KnowledgeAdapter:
    repository = FakeKnowledgeRepository(
        [
            KnowledgeDocument(
                document_id="decisions",
                kind=KnowledgeKind.ADR,
                title="DECISIONS",
                content=_ADR_CONTENT,
                source_path=".ai/DECISIONS.md",
            )
        ]
    )
    return KnowledgeAdapter(repository)


def _make_service(vault_root: Path, agent_adapter: AgentAdapter) -> IntelligenceSynthesisService:
    vault_adapter = VaultAdapter(vault_root)
    return IntelligenceSynthesisService(
        ProjectIntelligenceService(vault_adapter),
        ContextIntelligenceService(_make_knowledge_adapter()),
        CapabilityIntelligenceService(agent_adapter),
        vault_adapter,
    )


def test_generate_combines_all_three_services(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    agent_adapter = _make_agent_adapter()
    agent_adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    service = _make_service(vault_root, agent_adapter)

    overview = service.generate("M32-T01", today="2026-07-30")

    assert overview.project_health_level == "healthy"
    assert overview.context_freshness_level == "healthy"
    assert overview.capability_coverage_level == "partial"


def test_publish_raises_without_vault_adapter() -> None:
    service = IntelligenceSynthesisService(
        ProjectIntelligenceService(VaultAdapter(Path("/does-not-matter"))),
        ContextIntelligenceService(_make_knowledge_adapter()),
        CapabilityIntelligenceService(_make_agent_adapter()),
    )

    try:
        service.publish("M32-T01")
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError를 기대했지만 발생하지 않음")


def test_publish_writes_markdown_to_vault(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    service = _make_service(vault_root, _make_agent_adapter())

    overview, path = service.publish("M32-T01", today="2026-07-30")

    assert path == vault_root / "15 Project Intelligence" / "Intelligence Overview.md"
    content = path.read_text(encoding="utf-8")
    assert "# Intelligence Overview" in content
    assert overview.total_findings == len(overview.findings)


def test_render_markdown_includes_summary_and_findings_sections() -> None:
    vault_root_placeholder = Path("/does-not-matter-for-generate")
    agent_adapter = _make_agent_adapter()
    vault_adapter = VaultAdapter(vault_root_placeholder)
    service = IntelligenceSynthesisService(
        ProjectIntelligenceService(vault_adapter),
        ContextIntelligenceService(_make_knowledge_adapter()),
        CapabilityIntelligenceService(agent_adapter),
    )
    # generate() only reads from Vault via VaultAdapter.list_tasks(), which
    # tolerates a missing "14 Tasks" directory (empty task list) — no real
    # vault_root needs to exist for this render-only assertion.
    overview = service.generate("M32-T01")

    markdown = render_markdown(overview)

    assert "## 요약" in markdown
    assert "## Findings" in markdown
    assert "Project Health" in markdown
    assert "Context Freshness" in markdown
    assert "Capability Coverage" in markdown
