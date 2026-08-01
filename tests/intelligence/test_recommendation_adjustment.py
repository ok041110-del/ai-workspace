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
                total=3,
                success_count=0,
                failure_count=3,
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


def test_analyze_passes_through_when_only_failures_but_sample_too_small() -> None:
    """M49-T03(ADR-0066) — 실패 1~2건만으로는 표본이 부족해 보류하지
    않는다(최소 표본 3건 미만)."""
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

    assert result.next_action == _NEXT_ACTION
    assert result.adjusted is False


def test_analyze_withholds_when_recent_failure_streak_meets_threshold() -> None:
    """M51-T03(ADR-0068) — 전체 이력에 성공이 섞여 있어도 최근 5회
    연속 실패면 보류한다."""
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M42-T01",
                total=8,
                success_count=3,
                failure_count=5,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
                recent_failure_streak=5,
            )
        ]
    )

    result = analyzer.analyze(_NEXT_ACTION, report)

    assert result.next_action is None
    assert result.adjusted is True
    assert result.reason is not None
    assert "M51" in result.reason
    assert "M49" not in result.reason


def test_analyze_passes_through_when_combined_score_below_threshold() -> None:
    """M52-T03(ADR-0070) — 두 신호 모두 낮으면(실패율 1/8, 최근 연속
    실패 1회) 가중치 결합 점수가 threshold(0.6) 미만이라 보류하지
    않는다."""
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M42-T01",
                total=8,
                success_count=7,
                failure_count=1,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
                recent_failure_streak=1,
            )
        ]
    )

    result = analyzer.analyze(_NEXT_ACTION, report)

    assert result.next_action == _NEXT_ACTION
    assert result.adjusted is False


def test_analyze_withholds_on_combined_signals_below_individual_thresholds() -> None:
    """M52-T03(ADR-0070) — 실패율 50%(표본 8건) + 최근 4회 연속 실패는
    개별 규칙(M49 실패율 100%, M51 연속 5회)은 어느 쪽도 충족하지
    않지만, 가중치 결합 점수(0.6*0.5 + 0.6*0.8=0.78)가 threshold(0.6)
    이상이라 보류한다."""
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M42-T01",
                total=8,
                success_count=4,
                failure_count=4,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
                recent_failure_streak=4,
            )
        ]
    )

    result = analyzer.analyze(_NEXT_ACTION, report)

    assert result.next_action is None
    assert result.adjusted is True
    assert result.reason is not None
    assert "M52" in result.reason
    assert "M49" not in result.reason
    assert "M51" not in result.reason


def test_analyze_reason_tags_both_rules_when_both_triggered() -> None:
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M42-T01",
                total=5,
                success_count=0,
                failure_count=5,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
                recent_failure_streak=5,
            )
        ]
    )

    result = analyzer.analyze(_NEXT_ACTION, report)

    assert result.adjusted is True
    assert result.reason is not None
    assert "M49" in result.reason
    assert "M51" in result.reason


def test_analyze_reason_tags_m49_only_when_only_overall_rule_triggered() -> None:
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M42-T01",
                total=3,
                success_count=0,
                failure_count=3,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
                recent_failure_streak=3,
            )
        ]
    )

    result = analyzer.analyze(_NEXT_ACTION, report)

    assert result.adjusted is True
    assert result.reason is not None
    assert "M49" in result.reason
    assert "M51" not in result.reason


def test_analyze_withholds_when_only_overall_signal_is_full_and_recent_streak_zero() -> None:
    """M52-T03(ADR-0070) — 회귀 없음 증명: recent_failure_streak=0이라
    최근 신호가 전혀 없어도, 전체 실패율 신호 하나만으로
    score=0.6*1.0+0.6*0.0=0.6이 threshold(0.6)를 정확히 충족해 여전히
    보류한다(기존 M49 단일 규칙이 그대로 보존됨)."""
    analyzer = RecommendationAdjustmentAnalyzer()
    report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M42-T01",
                total=3,
                success_count=0,
                failure_count=3,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
                recent_failure_streak=0,
            )
        ]
    )

    result = analyzer.analyze(_NEXT_ACTION, report)

    assert result.next_action is None
    assert result.adjusted is True
    assert result.reason is not None
    assert "M49" in result.reason


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
