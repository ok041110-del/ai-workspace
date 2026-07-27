from tests.interfaces.fakes import FakeKnowledgeRepository

from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind
from ai_workspace.engines.knowledge_search import InMemoryKnowledgeSearch


def _document(document_id: str, title: str, content: str) -> KnowledgeDocument:
    return KnowledgeDocument(
        document_id=document_id,
        kind=KnowledgeKind.ARCHITECTURE,
        title=title,
        content=content,
        source_path=f"docs/{document_id}.md",
    )


def test_search_matches_by_title() -> None:
    repository = FakeKnowledgeRepository(
        [_document("a", "ExecutionEnvironment 설계", "본문"), _document("b", "다른 문서", "본문")]
    )
    search = InMemoryKnowledgeSearch(repository)

    results = search.search("ExecutionEnvironment")

    assert [document.document_id for document in results] == ["a"]


def test_search_matches_by_content() -> None:
    repository = FakeKnowledgeRepository(
        [
            _document("a", "제목", "BudgetPolicyEngine 관련 내용"),
            _document("b", "제목", "무관한 내용"),
        ]
    )
    search = InMemoryKnowledgeSearch(repository)

    results = search.search("BudgetPolicyEngine")

    assert [document.document_id for document in results] == ["a"]


def test_search_returns_empty_list_when_no_match() -> None:
    repository = FakeKnowledgeRepository([_document("a", "제목", "내용")])
    search = InMemoryKnowledgeSearch(repository)

    assert search.search("존재하지 않는 검색어") == []
