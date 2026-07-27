from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.knowledge import KnowledgeDocument


class KnowledgeSearch(ABC):
    """`KnowledgeRepository`가 노출하는 문서를 Keyword 기반으로 검색하는
    계약(M16-T02). 저장(Repository)과 검색(Search) 역할을 분리한다 —
    이 계약은 문서를 어디서 읽어오는지 알지 못하고, 주어진(생성자로
    주입된) `KnowledgeRepository`의 결과만 검색한다. 기존
    `MemoryEngine.search()`와 동일하게 단순 포함(substring) 검색
    수준이며, Vector/Embedding/Semantic Search는 다루지 않는다."""

    @abstractmethod
    def search(self, query: str) -> list[KnowledgeDocument]:
        """
        입력: query (검색어)
        출력: title 또는 content에 query가 부분 문자열로 포함된
              KnowledgeDocument 목록(없으면 빈 리스트)
        예외: 없음
        보장: side-effect 없음(read-only, LLM을 호출하지 않는다).
        """
        raise NotImplementedError
