from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.workflow_flow import WorkflowFlowReport
from ai_workspace.intelligence.workflow_service import (
    WorkflowIntelligenceService,
    render_markdown,
)


def _make_vault_adapter(tmp_path: Path) -> VaultAdapter:
    return VaultAdapter(tmp_path)


def test_generate_returns_empty_when_no_tasks(tmp_path: Path) -> None:
    service = WorkflowIntelligenceService(_make_vault_adapter(tmp_path))

    report = service.generate()

    assert report.milestones == []


def test_generate_reflects_created_vault_tasks(tmp_path: Path) -> None:
    vault_adapter = _make_vault_adapter(tmp_path)
    vault_adapter.create_task(
        "M34-T01",
        "설계",
        status="done",
        priority="high",
        milestone="M34",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    vault_adapter.create_task(
        "M34-T02",
        "구현",
        status="todo",
        priority="high",
        milestone="M34",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    service = WorkflowIntelligenceService(vault_adapter)

    report = service.generate()

    assert len(report.milestones) == 1
    milestone = report.milestones[0]
    assert milestone.milestone == "M34"
    assert milestone.next_task_ids == ["M34-T02"]


def test_generate_excludes_fully_completed_milestone(tmp_path: Path) -> None:
    vault_adapter = _make_vault_adapter(tmp_path)
    vault_adapter.create_task(
        "M34-T01",
        "설계",
        status="done",
        priority="high",
        milestone="M34",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    service = WorkflowIntelligenceService(vault_adapter)

    report = service.generate()

    assert report.milestones == []


def test_render_markdown_shows_empty_state_when_no_milestones() -> None:
    markdown = render_markdown(WorkflowFlowReport(milestones=[]))

    assert "현재 진행 중인 Milestone 없음" in markdown
    assert "미완료 Task가 없거나" in markdown


def test_render_markdown_lists_task_flow_per_milestone(tmp_path: Path) -> None:
    vault_adapter = _make_vault_adapter(tmp_path)
    vault_adapter.create_task(
        "M34-T01",
        "설계",
        status="done",
        priority="high",
        milestone="M34",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    vault_adapter.create_task(
        "M34-T02",
        "구현",
        status="todo",
        priority="high",
        milestone="M34",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    service = WorkflowIntelligenceService(vault_adapter)

    markdown = render_markdown(service.generate())

    assert "## M34" in markdown
    assert "M34-T02(구현)" in markdown
    assert "Next(다음 실행 가능)" in markdown


def test_publish_writes_workflow_intelligence_file(tmp_path: Path) -> None:
    vault_adapter = _make_vault_adapter(tmp_path)
    vault_adapter.create_task(
        "M34-T01",
        "설계",
        status="todo",
        priority="high",
        milestone="M34",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    service = WorkflowIntelligenceService(vault_adapter)

    report, path = service.publish()

    assert path == tmp_path / "15 Project Intelligence" / "Workflow Intelligence.md"
    assert path.exists()
    assert report.milestones[0].next_task_ids == ["M34-T01"]
    assert "Workflow Intelligence" in path.read_text(encoding="utf-8")
