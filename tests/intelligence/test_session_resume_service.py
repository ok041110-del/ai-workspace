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
from ai_workspace.intelligence.session_resume_service import (
    SessionResumeService,
    render_markdown,
)
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler

_ADR_CONTENT = """# DECISIONS

## ADR-0047: Session Resume 설계 (Milestone 33-T01)

내용.
"""

_TASK_CONTENT = """# TASKS

### M33-T02: Current Work Selector

내용.
"""

_ARCHITECTURE_CONTENT = """# ARCHITECTURE

### 3.26 Session Resume (Milestone 33-T01)

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
            ),
            KnowledgeDocument(
                document_id="tasks",
                kind=KnowledgeKind.TASK,
                title="TASKS",
                content=_TASK_CONTENT,
                source_path=".ai/TASKS.md",
            ),
            KnowledgeDocument(
                document_id="architecture",
                kind=KnowledgeKind.ARCHITECTURE,
                title="ARCHITECTURE",
                content=_ARCHITECTURE_CONTENT,
                source_path="docs/ARCHITECTURE.md",
            ),
        ]
    )
    return KnowledgeAdapter(repository)


def _make_service(vault_root: Path, agent_adapter: AgentAdapter) -> SessionResumeService:
    vault_adapter = VaultAdapter(vault_root)
    return SessionResumeService(
        vault_adapter,
        ProjectIntelligenceService(vault_adapter),
        ContextIntelligenceService(_make_knowledge_adapter()),
        CapabilityIntelligenceService(agent_adapter),
    )


def test_generate_reports_no_current_work_when_no_active_tasks(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    service = _make_service(vault_root, _make_agent_adapter())

    report = service.generate(today="2026-07-30")

    assert report.current_work is None
    assert report.context_report.context.subject == ""
    # 빈 subject를 ContextAnalyzer에 그대로 넘기면 모든 문서가
    # 매칭돼 버리는 회귀를 막는다 — 현재 작업이 없으면 Context
    # Intelligence를 아예 호출하지 않아야 한다.
    assert report.context_report.context.entries == []
    assert report.context_report.quality.gaps == []


def test_generate_picks_current_work_and_matching_context(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    vault_adapter = VaultAdapter(vault_root)
    vault_adapter.create_task(
        "M33-T02",
        "Current Work Selector",
        status="todo",
        priority="high",
        milestone="M33",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    vault_adapter.transition_task("M33-T02", "in-progress", today="2026-07-30")
    agent_adapter = _make_agent_adapter()
    agent_adapter.create_agent(AgentRole.CODING, frozenset({AgentCapability.CODING}))
    service = _make_service(vault_root, agent_adapter)

    report = service.generate(today="2026-07-30")

    assert report.current_work is not None
    assert report.current_work.task_id == "M33-T02"
    assert report.context_report.context.subject == "M33-T02"
    assert any(entry.kind == "task" for entry in report.context_report.context.entries)
    assert report.overview.project_health_level in ("healthy", "warning", "critical")


def test_publish_writes_markdown_to_vault(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    service = _make_service(vault_root, _make_agent_adapter())

    report, path = service.publish(today="2026-07-30")

    assert path == vault_root / "15 Project Intelligence" / "Session Resume.md"
    content = path.read_text(encoding="utf-8")
    assert "# Session Resume" in content
    assert report.current_work is None


def test_render_markdown_includes_all_sections() -> None:
    service = _make_service(Path("/does-not-matter-for-generate"), _make_agent_adapter())
    report = service.generate()

    markdown = render_markdown(report)

    assert "## 현재 작업" in markdown
    assert "## Project 상태" in markdown
    assert "## 관련 Context" in markdown
    assert "## Capability 상태" in markdown
    assert "## 다음 작업" in markdown
