from __future__ import annotations

from ai_workspace.domain.knowledge import KnowledgeDocument
from ai_workspace.interfaces.knowledge_repository import KnowledgeRepository
from ai_workspace.interfaces.knowledge_search import KnowledgeSearch


class InMemoryKnowledgeSearch(KnowledgeSearch):
    """생성 시 주어진 `KnowledgeRepository`의 문서를 대상으로 Keyword
    포함 검색을 수행하는 최소 구현체(M16-T02). 매 호출마다
    `repository.list_all()`을 다시 훑는다 — 문서 수가 적어(프로젝트
    문서 6개 안팎) 영속 Index 없이도 충분하다(YAGNI, `KnowledgeIndexer`
    는 이번 범위에서 제외)."""

    def __init__(self, repository: KnowledgeRepository) -> None:
        self._repository = repository

    def search(self, query: str) -> list[KnowledgeDocument]:
        return [
            document
            for document in self._repository.list_all()
            if query in document.title or query in document.content
        ]
