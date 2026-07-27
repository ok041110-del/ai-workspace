from tests.interfaces.fakes import FakeKnowledgeRepository

from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind
from ai_workspace.engines.knowledge_provider import InMemoryKnowledgeProvider
from ai_workspace.engines.knowledge_search import InMemoryKnowledgeSearch


def test_provide_delegates_to_search() -> None:
    document = KnowledgeDocument(
        document_id="a",
        kind=KnowledgeKind.RULE,
        title="RULES",
        content="Budget 정책 관련 규칙",
        source_path="docs/a.md",
    )
    repository = FakeKnowledgeRepository([document])
    provider = InMemoryKnowledgeProvider(InMemoryKnowledgeSearch(repository))

    results = provider.provide("Budget")

    assert results == [document]


def test_provide_returns_empty_list_when_no_match() -> None:
    repository = FakeKnowledgeRepository([])
    provider = InMemoryKnowledgeProvider(InMemoryKnowledgeSearch(repository))

    assert provider.provide("아무거나") == []
