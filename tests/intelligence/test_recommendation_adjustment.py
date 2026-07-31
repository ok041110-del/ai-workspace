from ai_workspace.intelligence.experience_rules import ExperienceReport, ExperienceStat
from ai_workspace.intelligence.recommendation_adjustment import (
    RecommendationAdjustment,
    RecommendationAdjustmentAnalyzer,
)
from ai_workspace.intelligence.recommendation_rules import (
    ACTION_START_NEXT_TASK,
    SOURCE_NEXT_TASK,
    NextAction,
)

_NEXT_ACTION = NextAction(
    source=SOURCE_NEXT_TASK,
    action=ACTION_START_NEXT_TASK,
    target="M42-T01",
    reason="선행 Task 완료",
)


def test_analyze_passes_through_when_experience_report_is_none() -> None:
    analyzer = RecommendationAdjustmentAnalyzer()

    result = analyzer.analyze(_NEXT_ACTION, None)

    assert result == RecommendationAdjustment(
        next_action=_NEXT_ACTION, adjusted=False, reason=None
    )


def test_analyze_passes_through_when_next_action_is_none() -> None:
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(stats=[])

    result = analyzer.analyze(None, report)

    assert result == RecommendationAdjustment(next_action=None, adjusted=False, reason=None)


def test_analyze_passes_through_when_target_has_no_matching_experience() -> None:
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="OTHER-T01",
                total=1,
                success_count=0,
                failure_count=1,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
            )
        ]
    )

    result = analyzer.analyze(_NEXT_ACTION, report)

    assert result.next_action == _NEXT_ACTION
    assert result.adjusted is False


def test_analyze_passes_through_when_target_has_at_least_one_success() -> None:
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M42-T01",
                total=2,
                success_count=1,
                failure_count=1,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
            )
        ]
    )

    result = analyzer.analyze(_NEXT_ACTION, report)

    assert result.next_action == _NEXT_ACTION
    assert result.adjusted is False


def test_analyze_withholds_recommendation_when_target_has_only_failures() -> None:
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M42-T01",
                total=2,
                success_count=0,
                failure_count=2,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
            )
        ]
    )

    result = analyzer.analyze(_NEXT_ACTION, report)

    assert result.next_action is None
    assert result.adjusted is True
    assert result.reason is not None
    assert "M42-T01" in result.reason


def test_analyze_is_deterministic() -> None:
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M42-T01",
                total=1,
                success_count=0,
                failure_count=1,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
            )
        ]
    )

    first = analyzer.analyze(_NEXT_ACTION, report)
    second = analyzer.analyze(_NEXT_ACTION, report)

    assert first == second
