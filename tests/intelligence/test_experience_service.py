from pathlib import Path

from ai_workspace.domain.execution_memory import ExecutionMemory
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.experience_service import (
    ExperienceIntelligenceService,
    render_markdown,
)
from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine


def _make_service(vault_root: Path) -> tuple[ExperienceIntelligenceService, ExecutionMemoryStore]:
    store = ExecutionMemoryStore(InMemoryMemoryEngine())
    service = ExperienceIntelligenceService(VaultAdapter(vault_root), store)
    return service, store


def test_generate_returns_empty_report_when_no_execution_memory(tmp_path: Path) -> None:
    service, _store = _make_service(tmp_path)

    report = service.generate()

    assert report.stats == []


def test_generate_aggregates_stored_execution_memory(tmp_path: Path) -> None:
    service, store = _make_service(tmp_path)
    store.record(
        ExecutionMemory(
            task_id="M40-T01",
            action="Gate",
            result="success",
            timestamp="2026-07-30T00:00:00+00:00",
        )
    )
    store.record(
        ExecutionMemory(
            task_id="M40-T01",
            action="Gate",
            result="failure",
            timestamp="2026-07-30T01:00:00+00:00",
            reason="boom",
        )
    )

    report = service.generate()

    assert len(report.stats) == 1
    assert report.stats[0].task_id == "M40-T01"
    assert report.stats[0].total == 2
    assert report.stats[0].success_count == 1
    assert report.stats[0].failure_count == 1
    assert report.stats[0].last_result == "failure"


def test_publish_writes_experience_intelligence_file(tmp_path: Path) -> None:
    service, store = _make_service(tmp_path)
    store.record(
        ExecutionMemory(
            task_id="M40-T01",
            action="Gate",
            result="success",
            timestamp="2026-07-30T00:00:00+00:00",
        )
    )

    report, path = service.publish()

    assert path == tmp_path / "15 Project Intelligence" / "Experience Intelligence.md"
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Experience Intelligence" in content
    assert "M40-T01" in content
    assert report.stats[0].task_id == "M40-T01"


def test_render_markdown_shows_no_records_message_when_empty() -> None:
    from ai_workspace.intelligence.experience_rules import ExperienceReport

    markdown = render_markdown(ExperienceReport(stats=[]))

    assert "기록된 실행 경험 없음" in markdown
