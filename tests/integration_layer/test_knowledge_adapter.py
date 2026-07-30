from tests.interfaces.fakes import FakeKnowledgeRepository

from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind
from ai_workspace.engines.knowledge_search import InMemoryKnowledgeSearch
from ai_workspace.integration.knowledge_adapter import KnowledgeAdapter

_ARCHITECTURE_DOC = KnowledgeDocument(
    document_id="architecture",
    kind=KnowledgeKind.ARCHITECTURE,
    title="ARCHITECTURE",
    content="# ARCHITECTURE\n\n### 3.22 Intelligence Layer(Milestone 29)\n\n내용",
    source_path="docs/ARCHITECTURE.md",
)
_ADR_DOC = KnowledgeDocument(
    document_id="decisions",
    kind=KnowledgeKind.ADR,
    title="DECISIONS",
    content="# DECISIONS\n\n## ADR-0043: Intelligence Layer 도입(Milestone 29-T01)\n\n내용",
    source_path=".ai/DECISIONS.md",
)


def test_list_all_returns_views_for_all_documents() -> None:
    repository = FakeKnowledgeRepository([_ARCHITECTURE_DOC, _ADR_DOC])
    adapter = KnowledgeAdapter(repository)

    documents = adapter.list_all()

    assert {document.document_id for document in documents} == {"architecture", "decisions"}
    architecture = next(
        document for document in documents if document.document_id == "architecture"
    )
    assert architecture.kind == "architecture"
    assert architecture.title == "ARCHITECTURE"
    assert architecture.source_path == "docs/ARCHITECTURE.md"


def test_search_delegates_to_injected_search() -> None:
    repository = FakeKnowledgeRepository([_ARCHITECTURE_DOC, _ADR_DOC])
    adapter = KnowledgeAdapter(repository, InMemoryKnowledgeSearch(repository))

    results = adapter.search("ADR-0043")

    assert [document.document_id for document in results] == ["decisions"]


def test_search_returns_empty_when_no_search_injected() -> None:
    repository = FakeKnowledgeRepository([_ARCHITECTURE_DOC])
    adapter = KnowledgeAdapter(repository)

    assert adapter.search("ARCHITECTURE") == []
