from ai_workspace.intelligence.health_risk import (
    HEALTH_CRITICAL,
    HEALTH_HEALTHY,
    HEALTH_WARNING,
    RISK_MILESTONE_STALL,
    RISK_OWNER_OVERLOAD,
    RISK_STAGNANT_TASK,
    ProjectHealthRiskAnalyzer,
)
from ai_workspace.intelligence.snapshot import (
    ProjectSnapshot,
    ProjectSnapshotWithTasks,
    TaskSnapshotEntry,
)

_TODAY = "2026-07-30"


def _entry(
    task_id: str,
    *,
    status: str = "in-progress",
    milestone: str = "",
    owner: str = "AI",
    updated: str = "2026-07-30",
    title: str = "",
) -> TaskSnapshotEntry:
    return TaskSnapshotEntry(
        task_id=task_id,
        title=title or task_id,
        status=status,
        priority="medium",
        milestone=milestone,
        owner=owner,
        updated=updated,
    )


def _snapshot_with(tasks: list[TaskSnapshotEntry]) -> ProjectSnapshotWithTasks:
    snapshot = ProjectSnapshot(
        generated_at=_TODAY,
        total_tasks=len(tasks),
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
    return ProjectSnapshotWithTasks(snapshot=snapshot, tasks=tasks)


def test_analyze_returns_healthy_when_no_tasks() -> None:
    analyzer = ProjectHealthRiskAnalyzer()

    report = analyzer.analyze(_snapshot_with([]), today=_TODAY)

    assert report.health.level == HEALTH_HEALTHY
    assert report.risks == []


def test_analyze_flags_stagnant_task_after_threshold() -> None:
    analyzer = ProjectHealthRiskAnalyzer(stagnant_days_threshold=7)
    tasks = [_entry("T29-05", status="in-progress", updated="2026-07-15")]

    report = analyzer.analyze(_snapshot_with(tasks), today=_TODAY)

    assert len(report.risks) == 1
    risk = report.risks[0]
    assert risk.kind == RISK_STAGNANT_TASK
    assert risk.target == "T29-05"
    assert report.health.level in (HEALTH_WARNING, HEALTH_CRITICAL)


def test_analyze_does_not_flag_recently_updated_active_task() -> None:
    analyzer = ProjectHealthRiskAnalyzer(stagnant_days_threshold=7)
    tasks = [_entry("T29-05", status="in-progress", updated="2026-07-28")]

    report = analyzer.analyze(_snapshot_with(tasks), today=_TODAY)

    assert report.risks == []
    assert report.health.level == HEALTH_HEALTHY


def test_analyze_does_not_flag_done_task_as_stagnant() -> None:
    analyzer = ProjectHealthRiskAnalyzer(stagnant_days_threshold=7)
    tasks = [_entry("T29-05", status="done", updated="2026-01-01")]

    report = analyzer.analyze(_snapshot_with(tasks), today=_TODAY)

    assert report.risks == []


def test_analyze_escalates_to_critical_when_very_stagnant() -> None:
    analyzer = ProjectHealthRiskAnalyzer(stagnant_days_threshold=7)
    tasks = [_entry("T29-05", status="in-progress", updated="2026-06-01")]

    report = analyzer.analyze(_snapshot_with(tasks), today=_TODAY)

    assert report.risks[0].severity == "critical"
    assert report.health.level == HEALTH_CRITICAL


def test_analyze_flags_owner_overload() -> None:
    analyzer = ProjectHealthRiskAnalyzer(owner_overload_threshold=3)
    tasks = [
        _entry(f"T29-0{i}", status="in-progress", owner="AI", updated=_TODAY) for i in range(3)
    ]

    report = analyzer.analyze(_snapshot_with(tasks), today=_TODAY)

    overload_risks = [risk for risk in report.risks if risk.kind == RISK_OWNER_OVERLOAD]
    assert len(overload_risks) == 1
    assert overload_risks[0].target == "AI"


def test_analyze_flags_milestone_stall_when_nothing_completed() -> None:
    analyzer = ProjectHealthRiskAnalyzer(stagnant_days_threshold=7)
    tasks = [
        _entry("T29-01", status="todo", milestone="M29", updated="2026-07-01"),
        _entry("T29-02", status="in-progress", milestone="M29", updated="2026-07-10"),
    ]

    report = analyzer.analyze(_snapshot_with(tasks), today=_TODAY)

    stall_risks = [risk for risk in report.risks if risk.kind == RISK_MILESTONE_STALL]
    assert len(stall_risks) == 1
    assert stall_risks[0].target == "M29"


def test_analyze_does_not_flag_milestone_stall_when_a_task_is_done() -> None:
    analyzer = ProjectHealthRiskAnalyzer(stagnant_days_threshold=7)
    tasks = [
        _entry("T29-01", status="done", milestone="M29", updated="2026-07-01"),
        _entry("T29-02", status="in-progress", milestone="M29", updated="2026-07-01"),
    ]

    report = analyzer.analyze(_snapshot_with(tasks), today=_TODAY)

    stall_risks = [risk for risk in report.risks if risk.kind == RISK_MILESTONE_STALL]
    assert stall_risks == []
