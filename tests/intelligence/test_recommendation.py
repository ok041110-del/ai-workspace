from ai_workspace.intelligence.health_risk import (
    RISK_MILESTONE_STALL,
    RISK_OWNER_OVERLOAD,
    RISK_STAGNANT_TASK,
    SEVERITY_CRITICAL,
    SEVERITY_WARNING,
    ProjectHealth,
    ProjectHealthReport,
    ProjectRisk,
)
from ai_workspace.intelligence.recommendation import (
    ACTION_ADVANCE_MILESTONE,
    ACTION_IMPROVE_PROGRESS,
    ACTION_PRIORITIZE_TASK,
    ACTION_REASSIGN_OWNER,
    ACTION_UNBLOCK_TASK,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    ProjectRecommendationEngine,
)
from ai_workspace.intelligence.snapshot import ProjectSnapshot, ProjectSnapshotWithTasks


def _snapshot(total_tasks: int = 0, progress_ratio: float = 0.0) -> ProjectSnapshotWithTasks:
    snapshot = ProjectSnapshot(
        generated_at="2026-07-30",
        total_tasks=total_tasks,
        by_status={},
        by_milestone={},
        by_owner={},
        todo_count=0,
        in_progress_count=0,
        review_count=0,
        done_count=0,
        archived_count=0,
        progress_ratio=progress_ratio,
        active_agent_count=0,
    )
    return ProjectSnapshotWithTasks(snapshot=snapshot, tasks=[])


def _health_report(risks: list[ProjectRisk]) -> ProjectHealthReport:
    level = "healthy" if not risks else "warning"
    return ProjectHealthReport(
        health=ProjectHealth(level=level, reasons=[risk.detail for risk in risks]), risks=risks
    )


def test_recommend_returns_empty_when_no_risks_and_healthy_progress() -> None:
    engine = ProjectRecommendationEngine()

    recommendations = engine.recommend(
        _snapshot(total_tasks=5, progress_ratio=0.8), _health_report([])
    )

    assert recommendations == []


def test_recommend_maps_critical_stagnant_task_to_unblock() -> None:
    engine = ProjectRecommendationEngine()
    risk = ProjectRisk(
        kind=RISK_STAGNANT_TASK, target="T29-05", detail="정체", severity=SEVERITY_CRITICAL
    )

    recommendations = engine.recommend(_snapshot(), _health_report([risk]))

    assert len(recommendations) == 1
    assert recommendations[0].action == ACTION_UNBLOCK_TASK
    assert recommendations[0].target == "T29-05"
    assert recommendations[0].priority == PRIORITY_HIGH


def test_recommend_maps_warning_stagnant_task_to_prioritize() -> None:
    engine = ProjectRecommendationEngine()
    risk = ProjectRisk(
        kind=RISK_STAGNANT_TASK, target="T29-05", detail="정체", severity=SEVERITY_WARNING
    )

    recommendations = engine.recommend(_snapshot(), _health_report([risk]))

    assert recommendations[0].action == ACTION_PRIORITIZE_TASK
    assert recommendations[0].priority == PRIORITY_MEDIUM


def test_recommend_maps_owner_overload_to_reassign() -> None:
    engine = ProjectRecommendationEngine()
    risk = ProjectRisk(
        kind=RISK_OWNER_OVERLOAD, target="AI", detail="과부하", severity=SEVERITY_WARNING
    )

    recommendations = engine.recommend(_snapshot(), _health_report([risk]))

    assert recommendations[0].action == ACTION_REASSIGN_OWNER
    assert recommendations[0].target == "AI"


def test_recommend_maps_milestone_stall_to_advance() -> None:
    engine = ProjectRecommendationEngine()
    risk = ProjectRisk(
        kind=RISK_MILESTONE_STALL, target="M29", detail="정체", severity=SEVERITY_WARNING
    )

    recommendations = engine.recommend(_snapshot(), _health_report([risk]))

    assert recommendations[0].action == ACTION_ADVANCE_MILESTONE
    assert recommendations[0].target == "M29"


def test_recommend_adds_project_level_recommendation_for_low_progress() -> None:
    engine = ProjectRecommendationEngine(low_progress_threshold=0.3)

    recommendations = engine.recommend(
        _snapshot(total_tasks=10, progress_ratio=0.1), _health_report([])
    )

    assert len(recommendations) == 1
    assert recommendations[0].action == ACTION_IMPROVE_PROGRESS
    assert recommendations[0].target == "project"


def test_recommend_skips_project_level_recommendation_when_no_tasks() -> None:
    engine = ProjectRecommendationEngine(low_progress_threshold=0.3)

    recommendations = engine.recommend(
        _snapshot(total_tasks=0, progress_ratio=0.0), _health_report([])
    )

    assert recommendations == []


def test_recommend_combines_risk_and_project_level_recommendations() -> None:
    engine = ProjectRecommendationEngine(low_progress_threshold=0.3)
    risk = ProjectRisk(
        kind=RISK_MILESTONE_STALL, target="M29", detail="정체", severity=SEVERITY_WARNING
    )

    recommendations = engine.recommend(
        _snapshot(total_tasks=10, progress_ratio=0.1), _health_report([risk])
    )

    actions = {recommendation.action for recommendation in recommendations}
    assert actions == {ACTION_ADVANCE_MILESTONE, ACTION_IMPROVE_PROGRESS}
