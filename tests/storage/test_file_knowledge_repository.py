from pathlib import Path

import pytest

from ai_workspace.domain.knowledge import KnowledgeKind
from ai_workspace.interfaces.knowledge_repository import KnowledgeDocumentNotFoundError
from ai_workspace.storage.file_knowledge_repository import FileKnowledgeRepository


def _write(base_dir: Path, relative_path: str, content: str) -> None:
    path = base_dir / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_list_all_returns_only_existing_files(tmp_path: Path) -> None:
    _write(tmp_path, "docs/ARCHITECTURE.md", "# ARCHITECTURE\n내용")
    repo = FileKnowledgeRepository(
        tmp_path, file_map={"docs/ARCHITECTURE.md": KnowledgeKind.ARCHITECTURE}
    )

    documents = repo.list_all()

    assert len(documents) == 1
    assert documents[0].document_id == "architecture"
    assert documents[0].kind == KnowledgeKind.ARCHITECTURE
    assert documents[0].source_path == "docs/ARCHITECTURE.md"


def test_list_all_skips_missing_files(tmp_path: Path) -> None:
    repo = FileKnowledgeRepository(
        tmp_path,
        file_map={
            "docs/ARCHITECTURE.md": KnowledgeKind.ARCHITECTURE,
            ".ai/RULES.md": KnowledgeKind.RULE,
        },
    )

    assert repo.list_all() == []


def test_title_is_extracted_from_first_non_empty_line(tmp_path: Path) -> None:
    _write(tmp_path, ".ai/RULES.md", "\n\n# RULES 문서\n본문")
    repo = FileKnowledgeRepository(tmp_path, file_map={".ai/RULES.md": KnowledgeKind.RULE})

    document = repo.get("rules")

    assert document.title == "RULES 문서"


def test_get_returns_matching_document(tmp_path: Path) -> None:
    _write(tmp_path, ".ai/TASKS.md", "# TASKS\n내용")
    repo = FileKnowledgeRepository(tmp_path, file_map={".ai/TASKS.md": KnowledgeKind.TASK})

    document = repo.get("tasks")

    assert document.content == "# TASKS\n내용"


def test_get_unknown_document_raises_not_found(tmp_path: Path) -> None:
    repo = FileKnowledgeRepository(tmp_path, file_map={})

    with pytest.raises(KnowledgeDocumentNotFoundError):
        repo.get("unknown")


def test_default_file_map_reads_this_projects_real_documents() -> None:
    """M16-T01 DoD: 실제 프로젝트 문서를 읽어 문서 목록을 반환함을
    확인한다(기본 매핑, 실제 저장소 루트)."""
    project_root = Path(__file__).resolve().parents[2]
    repo = FileKnowledgeRepository(project_root)

    documents = repo.list_all()

    document_ids = {document.document_id for document in documents}
    assert "architecture" in document_ids
    assert "decisions" in document_ids
    assert "rules" in document_ids
    assert "tasks" in document_ids
