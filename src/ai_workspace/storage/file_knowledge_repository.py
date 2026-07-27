from __future__ import annotations

from pathlib import Path

from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind
from ai_workspace.interfaces.knowledge_repository import (
    KnowledgeDocumentNotFoundError,
    KnowledgeRepository,
)

DEFAULT_KNOWLEDGE_FILE_MAP: dict[str, KnowledgeKind] = {
    "docs/ARCHITECTURE.md": KnowledgeKind.ARCHITECTURE,
    ".ai/DECISIONS.md": KnowledgeKind.ADR,
    ".ai/RULES.md": KnowledgeKind.RULE,
    ".ai/TASKS.md": KnowledgeKind.TASK,
    "docs/ROADMAP.md": KnowledgeKind.PROJECT,
    "docs/PRD.md": KnowledgeKind.PROJECT,
}


class FileKnowledgeRepository(KnowledgeRepository):
    """프로젝트 문서 파일을 통째로 `KnowledgeDocument`로 노출하는 최소
    구현체(M16-T01). 문단 단위로 쪼개지 않고 파일 하나 = 문서 하나로
    다룬다(YAGNI) — `document_id`↔`KnowledgeKind` 매핑은 고정 설정
    (`DEFAULT_KNOWLEDGE_FILE_MAP`)이며, 실제로 존재하는 파일만 노출한다."""

    def __init__(
        self,
        base_dir: str | Path,
        file_map: dict[str, KnowledgeKind] | None = None,
    ) -> None:
        self._base_dir = Path(base_dir)
        self._file_map = dict(file_map) if file_map is not None else dict(
            DEFAULT_KNOWLEDGE_FILE_MAP
        )

    def list_all(self) -> list[KnowledgeDocument]:
        documents = []
        for relative_path, kind in self._file_map.items():
            path = self._base_dir / relative_path
            if path.exists():
                documents.append(self._load(relative_path, kind))
        return documents

    def get(self, document_id: str) -> KnowledgeDocument:
        for document in self.list_all():
            if document.document_id == document_id:
                return document
        raise KnowledgeDocumentNotFoundError(document_id)

    def _load(self, relative_path: str, kind: KnowledgeKind) -> KnowledgeDocument:
        content = (self._base_dir / relative_path).read_text(encoding="utf-8")
        return KnowledgeDocument(
            document_id=Path(relative_path).stem.lower(),
            kind=kind,
            title=self._extract_title(content, relative_path),
            content=content,
            source_path=relative_path,
        )

    @staticmethod
    def _extract_title(content: str, relative_path: str) -> str:
        for line in content.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped.lstrip("#").strip() or relative_path
        return relative_path
