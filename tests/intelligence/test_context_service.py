from pathlib import Path

from tests.interfaces.fakes import FakeKnowledgeRepository

from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind
from ai_workspace.integration.knowledge_adapter import KnowledgeAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.context_service import ContextIntelligenceService, render_markdown

_ADR_CONTENT = """# DECISIONS

## ADR-0044: Context Intelligence 설계 (Milestone 30-T01)

내용.
"""

_TASK_CONTENT = """# TASKS

### M30-T04: Integration 구현

내용.
"""

_ARCHITECTURE_CONTENT = """# ARCHITECTURE

### 3.23 Context Intelligence (Milestone 30-T01)

내용.
"""


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


def _make_service(
    vault_adapter: VaultAdapter | None = None, **kwargs
) -> ContextIntelligenceService:
    return ContextIntelligenceService(_make_knowledge_adapter(), vault_adapter, **kwargs)


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


def test_generate_combines_context_and_quality() -> None:
    service = _make_service()

    report = service.generate("M30-T04")

    assert report.context.subject == "M30-T04"
    assert any(entry.kind == "task" for entry in report.context.entries)
    assert report.quality.gaps == [] or all(
        gap.kind != "task" for gap in report.quality.gaps
    )


def test_generate_reports_gap_when_subject_not_mentioned() -> None:
    service = _make_service()

    report = service.generate("M99-T99")

    assert report.context.entries == []
    gap_kinds = {gap.kind for gap in report.quality.gaps}
    assert gap_kinds == {"adr", "task", "architecture"}


def test_generate_applies_freshness_with_current_milestone() -> None:
    service = _make_service(milestone_distance_threshold=1)

    report = service.generate("M30-T04", current_milestone=30)

    assert report.quality.freshness.level == "healthy"


def test_publish_raises_without_vault_adapter() -> None:
    service = _make_service()

    try:
        service.publish("M30-T04")
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError를 기대했지만 발생하지 않음")


def test_publish_writes_markdown_to_vault(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    service = _make_service(VaultAdapter(vault_root))

    report, path = service.publish("M30-T04", current_milestone=30)

    assert path == vault_root / "15 Project Intelligence" / "Project Context.md"
    content = path.read_text(encoding="utf-8")
    assert "# Project Context" in content
    assert "M30-T04" in content
    assert report.context.subject == "M30-T04"


def test_render_markdown_includes_all_sections() -> None:
    service = _make_service()
    report = service.generate("M30-T04", current_milestone=30)

    markdown = render_markdown(report)

    assert "## 관련 ADR" in markdown
    assert "## 관련 Task" in markdown
    assert "## 관련 Architecture" in markdown
    assert "## 관련 Rules" in markdown
    assert "## 관련 Roadmap/PRD" in markdown
    assert "## Freshness" in markdown
    assert "## Gap" in markdown
    assert "Context Quality Score" in markdown
