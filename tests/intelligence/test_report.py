from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.report import ProjectIntelligenceService, render_markdown


def _make_vault(tmp_path: Path) -> Path:
    (tmp_path / "11 Milestones").mkdir(parents=True)
    (tmp_path / "11 Milestones" / "Milestones Index.md").write_text(
        "# Milestones Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    (tmp_path / "12 Decisions").mkdir(parents=True)
    (tmp_path / "12 Decisions" / "Decisions Index.md").write_text(
        "# Decisions Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    return tmp_path


def test_generate_returns_empty_report_when_no_tasks(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(_make_vault(tmp_path))
    service = ProjectIntelligenceService(vault_adapter)

    report = service.generate(today="2026-07-30")

    assert report.snapshot.total_tasks == 0
    assert report.health_report.health.level == "healthy"
    assert report.health_report.risks == []
    assert report.recommendations == []


def test_generate_produces_recommendations_for_stagnant_task(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    vault_adapter = VaultAdapter(vault_root)
    vault_adapter.create_task(
        "T29-05",
        "정체된 Task",
        status="todo",
        priority="high",
        milestone="M29",
        owner="AI",
        created="2026-07-01",
        updated="2026-07-01",
    )
    vault_adapter.transition_task("T29-05", "in-progress", today="2026-07-01")
    service = ProjectIntelligenceService(vault_adapter, stagnant_days_threshold=7)

    report = service.generate(today="2026-07-30")

    assert report.health_report.health.level in ("warning", "critical")
    assert any(risk.target == "T29-05" for risk in report.health_report.risks)
    assert any(rec.target == "T29-05" for rec in report.recommendations)


def test_publish_writes_markdown_to_vault(tmp_path: Path) -> None:
    vault_root = _make_vault(tmp_path)
    vault_adapter = VaultAdapter(vault_root)
    vault_adapter.create_task(
        "T29-01",
        "설계",
        status="todo",
        priority="high",
        milestone="M29",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    service = ProjectIntelligenceService(vault_adapter)

    report, path = service.publish(today="2026-07-30")

    assert path == vault_root / "15 Project Intelligence" / "Project Intelligence.md"
    content = path.read_text(encoding="utf-8")
    assert "# Project Intelligence" in content
    assert "T29-01" not in content  # Task 개별 내역이 아니라 집계만 노출
    assert "전체 Task: 1" in content
    assert report.snapshot.total_tasks == 1


def test_render_markdown_includes_all_sections() -> None:
    from ai_workspace.intelligence.health_risk import ProjectHealth, ProjectHealthReport
    from ai_workspace.intelligence.report import ProjectIntelligenceReport
    from ai_workspace.intelligence.snapshot import ProjectSnapshot

    snapshot = ProjectSnapshot(
        generated_at="2026-07-30",
        total_tasks=0,
        by_status={},
        by_milestone={},
        by_owner={},
        todo_count=0,
        in_progress_count=0,
        review_count=0,
        done_count=0,
        archived_count=0,
        progress_ratio=0.0,
        active_agent_count=0,
    )
    health = ProjectHealth(level="healthy", reasons=[])
    report = ProjectIntelligenceReport(
        snapshot=snapshot,
        health_report=ProjectHealthReport(health=health, risks=[]),
        recommendations=[],
    )

    markdown = render_markdown(report)

    assert "## Snapshot" in markdown
    assert "## Health" in markdown
    assert "## Risk" in markdown
    assert "## Recommendation" in markdown
