from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind


def test_knowledge_kind_covers_expected_categories() -> None:
    assert {kind.value for kind in KnowledgeKind} == {
        "architecture",
        "adr",
        "rule",
        "task",
        "project",
    }


def test_knowledge_document_holds_given_fields() -> None:
    document = KnowledgeDocument(
        document_id="architecture",
        kind=KnowledgeKind.ARCHITECTURE,
        title="ARCHITECTURE",
        content="# ARCHITECTURE\n...",
        source_path="docs/ARCHITECTURE.md",
    )

    assert document.document_id == "architecture"
    assert document.kind == KnowledgeKind.ARCHITECTURE
    assert document.title == "ARCHITECTURE"
    assert document.content == "# ARCHITECTURE\n..."
    assert document.source_path == "docs/ARCHITECTURE.md"
