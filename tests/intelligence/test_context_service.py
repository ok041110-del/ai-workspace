from tests.interfaces.fakes import FakeKnowledgeRepository

from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind
from ai_workspace.integration.knowledge_adapter import KnowledgeAdapter
from ai_workspace.intelligence.context_service import ContextIntelligenceService

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


def _make_service(**kwargs) -> ContextIntelligenceService:
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
    return ContextIntelligenceService(KnowledgeAdapter(repository), **kwargs)


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
