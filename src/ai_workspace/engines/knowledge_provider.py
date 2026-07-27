from __future__ import annotations

from ai_workspace.domain.knowledge import KnowledgeDocument
from ai_workspace.interfaces.knowledge_provider import KnowledgeProvider
from ai_workspace.interfaces.knowledge_search import KnowledgeSearch


class InMemoryKnowledgeProvider(KnowledgeProvider):
    """생성 시 주어진 `KnowledgeSearch`에 그대로 위임하는 최소
    구현체(M16-T02). Agent 입장에서는 `KnowledgeRepository`/
    `KnowledgeSearch`가 어떻게 조합됐는지 알 필요가 없다 — 이 클래스가
    그 조합을 감추는 경계다."""

    def __init__(self, search: KnowledgeSearch) -> None:
        self._search = search

    def provide(self, query: str) -> list[KnowledgeDocument]:
        return self._search.search(query)
