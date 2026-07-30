from tests.interfaces.fakes import FakeKnowledgeRepository

from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind
from ai_workspace.integration.knowledge_adapter import KnowledgeAdapter
from ai_workspace.intelligence.context import ContextAnalyzer

_ADR_CONTENT = """# DECISIONS

## ADR-0043: Intelligence Layer 도입 (Milestone 29-T01)

Snapshot/Health/Risk/Recommendation 설계.

## ADR-0044: Context Intelligence 설계 (Milestone 30-T01)

KnowledgeAdapter 신규.
"""

_TASK_CONTENT = """# TASKS

## Milestone 29 — Project Intelligence

### M29-T01: Project Intelligence Architecture 설계

설계 완료.

## Milestone 30 — Context Intelligence

### M30-T01: Context Intelligence Architecture

설계 완료.
"""

_RULE_CONTENT = """# RULES

## 1. Architecture First

원칙 설명.
"""


def _make_adapter() -> KnowledgeAdapter:
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
                document_id="rules",
                kind=KnowledgeKind.RULE,
                title="RULES",
                content=_RULE_CONTENT,
                source_path=".ai/RULES.md",
            ),
        ]
    )
    return KnowledgeAdapter(repository)


def test_analyze_finds_entries_mentioning_subject() -> None:
    analyzer = ContextAnalyzer(_make_adapter())

    context = analyzer.analyze("M30-T01")

    assert context.subject == "M30-T01"
    headings = {entry.heading for entry in context.entries}
    assert "ADR-0044: Context Intelligence 설계 (Milestone 30-T01)" in headings
    assert "M30-T01: Context Intelligence Architecture" in headings


def test_analyze_does_not_match_unrelated_sections() -> None:
    analyzer = ContextAnalyzer(_make_adapter())

    context = analyzer.analyze("M30-T01")

    headings = {entry.heading for entry in context.entries}
    assert "ADR-0043: Intelligence Layer 도입 (Milestone 29-T01)" not in headings
    assert "1. Architecture First" not in headings


def test_analyze_extracts_milestone_from_matched_entries() -> None:
    analyzer = ContextAnalyzer(_make_adapter())

    context = analyzer.analyze("M30-T01")

    adr_entry = next(entry for entry in context.entries if entry.kind == "adr")
    assert adr_entry.milestone == "M30"


def test_analyze_returns_empty_when_subject_not_mentioned() -> None:
    analyzer = ContextAnalyzer(_make_adapter())

    context = analyzer.analyze("M99-T99")

    assert context.entries == []


def test_by_kind_filters_entries() -> None:
    analyzer = ContextAnalyzer(_make_adapter())

    context = analyzer.analyze("M30-T01")

    adr_entries = context.by_kind("adr")
    assert len(adr_entries) == 1
    assert all(entry.kind == "adr" for entry in adr_entries)
