from ai_workspace.intelligence.capability_gap import (
    CapabilityCoverage,
    CapabilityGap,
    CapabilityGapReport,
)
from ai_workspace.intelligence.experience_rules import ExperienceReport, ExperienceStat
from ai_workspace.intelligence.recommendation_explanation import (
    RecommendationExplanationAnalyzer,
)
from ai_workspace.intelligence.recommendation_rules import (
    ACTION_IMPROVE_CAPABILITY,
    SOURCE_CAPABILITY_GAP,
    NextAction,
)
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceReport
from ai_workspace.intelligence.workflow_flow import WorkflowFlowReport

_EMPTY_WORKFLOW_REPORT = WorkflowFlowReport(milestones=[])
_EMPTY_CAPABILITY_GAP_REPORT = CapabilityGapReport(
    coverage=CapabilityCoverage(level="none", ratio=0.0), gaps=[]
)


def _make_report(
    *,
    next_action: NextAction | None,
    capability_gap_report: CapabilityGapReport = _EMPTY_CAPABILITY_GAP_REPORT,
    adjusted: bool = False,
    adjustment_reason: str | None = None,
) -> RecommendationIntelligenceReport:
    return RecommendationIntelligenceReport(
        next_action=next_action,
        current_work=None,
        workflow_report=_EMPTY_WORKFLOW_REPORT,
        capability_gap_report=capability_gap_report,
        project_recommendations=[],
        adjusted=adjusted,
        adjustment_reason=adjustment_reason,
    )


def test_analyze_marks_selected_source_as_matched() -> None:
    analyzer = RecommendationExplanationAnalyzer()
    next_action = NextAction(
        source=SOURCE_CAPABILITY_GAP,
        action=ACTION_IMPROVE_CAPABILITY,
        target="테스트 커버리지",
        reason="Capability Gap 존재",
    )
    report = _make_report(
        next_action=next_action,
        capability_gap_report=CapabilityGapReport(
            coverage=CapabilityCoverage(level="none", ratio=0.0),
            gaps=[CapabilityGap(capability="테스트 커버리지", detail="Capability Gap 존재")],
        ),
    )

    explanation = analyzer.analyze(report)

    assert explanation.next_action_target == "테스트 커버리지"
    matched = [step for step in explanation.trace if step.matched]
    assert len(matched) == 1
    assert matched[0].source == SOURCE_CAPABILITY_GAP
    assert matched[0].rank == 4
    assert explanation.adaptation_applied is False
    assert explanation.experience_summary is None


def test_analyze_shows_no_step_matched_when_next_action_is_none() -> None:
    analyzer = RecommendationExplanationAnalyzer()
    report = _make_report(next_action=None)

    explanation = analyzer.analyze(report)

    assert explanation.next_action_target is None
    assert all(not step.matched for step in explanation.trace)


def test_analyze_reports_adaptation_reason_when_applied() -> None:
    analyzer = RecommendationExplanationAnalyzer()
    report = _make_report(
        next_action=None, adjusted=True, adjustment_reason="M44-T01이(가) 반복 실패해 추천을 보류함"
    )

    explanation = analyzer.analyze(report)

    assert explanation.adaptation_applied is True
    assert explanation.adaptation_reason == "M44-T01이(가) 반복 실패해 추천을 보류함"


def test_analyze_includes_experience_summary_when_available() -> None:
    analyzer = RecommendationExplanationAnalyzer()
    next_action = NextAction(
        source=SOURCE_CAPABILITY_GAP,
        action=ACTION_IMPROVE_CAPABILITY,
        target="M44-T01",
        reason="Capability Gap 존재",
    )
    report = _make_report(next_action=next_action)
    experience_report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id="M44-T01",
                total=5,
                success_count=4,
                failure_count=1,
                last_result="success",
                last_timestamp="2026-07-31T00:00:00",
            )
        ]
    )

    explanation = analyzer.analyze(report, experience_report)

    assert explanation.experience_summary == "성공률 80%(5건 중 4건 성공)"


def test_analyze_is_deterministic() -> None:
    analyzer = RecommendationExplanationAnalyzer()
    next_action = NextAction(
        source=SOURCE_CAPABILITY_GAP,
        action=ACTION_IMPROVE_CAPABILITY,
        target="M44-T01",
        reason="Capability Gap 존재",
    )
    report = _make_report(next_action=next_action)

    first = analyzer.analyze(report)
    second = analyzer.analyze(report)

    assert first == second
