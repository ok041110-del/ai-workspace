from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.knowledge import KnowledgeDocument


class KnowledgeDocumentNotFoundError(Exception):
    """존재하지 않는 document_id를 조회하려 할 때 발생한다."""


class KnowledgeRepository(ABC):
    """프로젝트 Knowledge 문서의 조회 계약(M16-T01). 문서를 어디서
    읽어오는지(Markdown 파일 등)는 이 계약이 알지 못한다 — 실제 출처는
    구체 구현체(`FileKnowledgeRepository`)의 책임이다. `ProjectRepository`
    와 동일한 설계(순수 조회, side-effect 없음)를 따르되, Knowledge는
    Workspace가 소유한 읽기 전용 문서라 `save()`가 없다."""

    @abstractmethod
    def list_all(self) -> list[KnowledgeDocument]:
        """
        입력: 없음
        출력: 저장된 모든 KnowledgeDocument 목록(없으면 빈 리스트)
        예외: 없음
        보장: side-effect 없음(read-only). 반환된 리스트를 호출자가
              수정해도 내부 상태는 변하지 않는다(방어적 복사).
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, document_id: str) -> KnowledgeDocument:
        """
        입력: document_id
        출력: document_id에 해당하는 KnowledgeDocument
        예외: 해당 document_id가 없으면 KnowledgeDocumentNotFoundError
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError
