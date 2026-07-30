from ai_workspace.intelligence.capability_gap import (
    CapabilityCoverage,
    CapabilityGap,
    CapabilityGapReport,
)
from ai_workspace.intelligence.recommendation import ProjectRecommendation
from ai_workspace.intelligence.recommendation_rules import (
    ACTION_CONTINUE_CURRENT_WORK,
    ACTION_IMPROVE_CAPABILITY,
    ACTION_RESOLVE_BLOCKER,
    ACTION_START_NEXT_TASK,
    SOURCE_BLOCKED_TASK,
    SOURCE_CAPABILITY_GAP,
    SOURCE_CURRENT_WORK,
    SOURCE_NEXT_TASK,
    SOURCE_PROJECT_RECOMMENDATION,
    RecommendationRuleAnalyzer,
)
from ai_workspace.intelligence.session_resume import CurrentWork
from ai_workspace.intelligence.workflow_flow import MilestoneFlow, TaskFlowEntry, WorkflowFlowReport

_EMPTY_WORKFLOW = WorkflowFlowReport(milestones=[])
_EMPTY_CAPABILITY = CapabilityGapReport(
    coverage=CapabilityCoverage(level="full", ratio=1.0), gaps=[]
)


def _current_work() -> CurrentWork:
    return CurrentWork(
        task_id="M35-T02",
        title="RecommendationRuleAnalyzer",
        status="in-progress",
        milestone="M35",
        owner="AI",
        updated="2026-07-30",
    )


def _workflow_with(*, flow_state: str) -> WorkflowFlowReport:
    return WorkflowFlowReport(
        milestones=[
            MilestoneFlow(
                milestone="M35",
                tasks=[
                    TaskFlowEntry(
                        task_id="M35-T01", title="설계", status="done", flow_state="done"
                    ),
                    TaskFlowEntry(
                        task_id="M35-T02", title="Analyzer", status="todo", flow_state=flow_state
                    ),
                ],
            )
        ]
    )


def test_priority1_current_work_wins_over_everything() -> None:
    analyzer = RecommendationRuleAnalyzer()

    result = analyzer.analyze(
        current_work=_current_work(),
        workflow_report=_workflow_with(flow_state="next"),
        capability_gap_report=CapabilityGapReport(
            coverage=CapabilityCoverage(level="none", ratio=0.0),
            gaps=[CapabilityGap(capability="coding", detail="없음")],
        ),
        project_recommendations=[
            ProjectRecommendation(action="unblock_task", target="X", reason="r", priority="high")
        ],
    )

    assert result is not None
    assert result.source == SOURCE_CURRENT_WORK
    assert result.action == ACTION_CONTINUE_CURRENT_WORK
    assert result.target == "M35-T02"


def test_priority2_next_task_when_no_current_work() -> None:
    analyzer = RecommendationRuleAnalyzer()

    result = analyzer.analyze(
        current_work=None,
        workflow_report=_workflow_with(flow_state="next"),
        capability_gap_report=_EMPTY_CAPABILITY,
        project_recommendations=[],
    )

    assert result is not None
    assert result.source == SOURCE_NEXT_TASK
    assert result.action == ACTION_START_NEXT_TASK
    assert result.target == "M35-T02"


def test_priority3_blocked_task_when_no_current_work_or_next() -> None:
    analyzer = RecommendationRuleAnalyzer()

    result = analyzer.analyze(
        current_work=None,
        workflow_report=_workflow_with(flow_state="blocked"),
        capability_gap_report=_EMPTY_CAPABILITY,
        project_recommendations=[],
    )

    assert result is not None
    assert result.source == SOURCE_BLOCKED_TASK
    assert result.action == ACTION_RESOLVE_BLOCKER
    assert result.target == "M35-T02"


def test_priority4_capability_gap_when_workflow_has_nothing_actionable() -> None:
    analyzer = RecommendationRuleAnalyzer()

    result = analyzer.analyze(
        current_work=None,
        workflow_report=_EMPTY_WORKFLOW,
        capability_gap_report=CapabilityGapReport(
            coverage=CapabilityCoverage(level="none", ratio=0.0),
            gaps=[CapabilityGap(capability="coding", detail="coding Capability 없음")],
        ),
        project_recommendations=[
            ProjectRecommendation(action="unblock_task", target="X", reason="r", priority="high")
        ],
    )

    assert result is not None
    assert result.source == SOURCE_CAPABILITY_GAP
    assert result.action == ACTION_IMPROVE_CAPABILITY
    assert result.target == "coding"


def test_priority5_project_recommendation_picks_highest_priority() -> None:
    analyzer = RecommendationRuleAnalyzer()

    result = analyzer.analyze(
        current_work=None,
        workflow_report=_EMPTY_WORKFLOW,
        capability_gap_report=_EMPTY_CAPABILITY,
        project_recommendations=[
            ProjectRecommendation(
                action="prioritize_task", target="B", reason="r2", priority="medium"
            ),
            ProjectRecommendation(action="unblock_task", target="A", reason="r1", priority="high"),
        ],
    )

    assert result is not None
    assert result.source == SOURCE_PROJECT_RECOMMENDATION
    assert result.action == "unblock_task"
    assert result.target == "A"


def test_priority5_breaks_ties_by_target() -> None:
    analyzer = RecommendationRuleAnalyzer()

    result = analyzer.analyze(
        current_work=None,
        workflow_report=_EMPTY_WORKFLOW,
        capability_gap_report=_EMPTY_CAPABILITY,
        project_recommendations=[
            ProjectRecommendation(action="unblock_task", target="B", reason="r", priority="high"),
            ProjectRecommendation(action="unblock_task", target="A", reason="r", priority="high"),
        ],
    )

    assert result is not None
    assert result.target == "A"


def test_returns_none_when_nothing_applies() -> None:
    analyzer = RecommendationRuleAnalyzer()

    result = analyzer.analyze(
        current_work=None,
        workflow_report=_EMPTY_WORKFLOW,
        capability_gap_report=_EMPTY_CAPABILITY,
        project_recommendations=[],
    )

    assert result is None
