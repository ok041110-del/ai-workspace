from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.knowledge import KnowledgeDocument


class KnowledgeProvider(ABC):
    """Agent가 Project Knowledge에 접근하는 유일한 진입점(M16-T02).
    `ContextManager`가 `MemoryEngine`을 감싸 Agent에게 노출하는 것과
    동일한 패턴 — Agent는 이 계약만 알고 `KnowledgeRepository`/
    `KnowledgeSearch`를 직접 호출하지 않는다(§8 의존성 규칙에 신규
    추가). Memory는 LLM을 호출하지 않고, Knowledge를 검색해 제공하는
    역할만 수행한다."""

    @abstractmethod
    def provide(self, query: str) -> list[KnowledgeDocument]:
        """
        입력: query (Agent가 참고하고 싶은 주제/검색어)
        출력: query와 관련된 KnowledgeDocument 목록(없으면 빈 리스트)
        예외: 없음
        보장: side-effect 없음(read-only, LLM을 호출하지 않는다).
        """
        raise NotImplementedError
