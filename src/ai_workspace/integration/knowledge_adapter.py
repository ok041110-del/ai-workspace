"""Workspace Adapter Layer — Knowledge Adapter (ADR-0044, Milestone 30-T02).

Core Domain의 `KnowledgeRepository`/`KnowledgeSearch` **Interface**에만
의존한다(Interface First, `.ai/RULES.md` §1.3) — 구체 구현체
(`FileKnowledgeRepository`/`InMemoryKnowledgeSearch` 등)는 생성자로
주입받는다. Knowledge 조회/검색 로직은 여기서 새로 만들지 않고 전부
Core Domain Engine에 위임한다(연결·변환·위임만, ADR-0039)."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.domain.knowledge import KnowledgeDocument
from ai_workspace.interfaces.knowledge_repository import KnowledgeRepository
from ai_workspace.interfaces.knowledge_search import KnowledgeSearch


@dataclass(frozen=True)
class KnowledgeDocumentView:
    """`KnowledgeAdapter`가 반환하는 문서 하나의 읽기 전용 뷰. 호출자는
    `domain.knowledge.KnowledgeDocument`/`KnowledgeKind`를 직접 import
    하지 않는다(다른 Adapter와 동일한 원칙) — `kind`는 `KnowledgeKind`의
    `.value` 문자열이다."""

    document_id: str
    kind: str
    title: str
    content: str
    source_path: str


class KnowledgeAdapter:
    """Knowledge 문서 조회/검색을 Core Domain Engine에 위임하는 Adapter.
    `KnowledgeRepository`(필수)/`KnowledgeSearch`(선택, 미주입 시
    `search()`는 빈 목록)만 생성자로 주입받는다."""

    def __init__(
        self,
        repository: KnowledgeRepository,
        search: KnowledgeSearch | None = None,
    ) -> None:
        self._repository = repository
        self._search = search

    def list_all(self) -> list[KnowledgeDocumentView]:
        """모든 Knowledge 문서를 반환한다(side-effect 없음)."""
        return [self._to_view(document) for document in self._repository.list_all()]

    def search(self, query: str) -> list[KnowledgeDocumentView]:
        """`KnowledgeSearch`가 주입돼 있으면 위임하고, 없으면 빈 목록을
        반환한다(side-effect 없음, LLM 호출 없음)."""
        if self._search is None:
            return []
        return [self._to_view(document) for document in self._search.search(query)]

    @staticmethod
    def _to_view(document: KnowledgeDocument) -> KnowledgeDocumentView:
        return KnowledgeDocumentView(
            document_id=document.document_id,
            kind=document.kind.value,
            title=document.title,
            content=document.content,
            source_path=document.source_path,
        )
