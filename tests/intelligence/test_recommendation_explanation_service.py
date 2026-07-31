from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_gap import CapabilityCoverage, CapabilityGapReport
from ai_workspace.intelligence.experience_rules import ExperienceReport
from ai_workspace.intelligence.recommendation_explanation_service import (
    RecommendationExplanationService,
    render_markdown,
)
from ai_workspace.intelligence.recommendation_rules import (
    ACTION_IMPROVE_CAPABILITY,
    SOURCE_CAPABILITY_GAP,
    NextAction,
)
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceReport
from ai_workspace.intelligence.workflow_flow import WorkflowFlowReport

_REPORT = RecommendationIntelligenceReport(
    next_action=NextAction(
        source=SOURCE_CAPABILITY_GAP,
        action=ACTION_IMPROVE_CAPABILITY,
        target="테스트 커버리지",
        reason="Capability Gap 존재",
    ),
    current_work=None,
    workflow_report=WorkflowFlowReport(milestones=[]),
    capability_gap_report=CapabilityGapReport(
        coverage=CapabilityCoverage(level="none", ratio=0.0), gaps=[]
    ),
    project_recommendations=[],
)


def test_generate_delegates_to_analyzer(tmp_path: Path) -> None:
    service = RecommendationExplanationService(VaultAdapter(tmp_path))

    explanation = service.generate(_REPORT)

    assert explanation.next_action_target == "테스트 커버리지"


def test_publish_writes_recommendation_explanation_file(tmp_path: Path) -> None:
    service = RecommendationExplanationService(VaultAdapter(tmp_path))

    explanation, path = service.publish(_REPORT)

    assert path == tmp_path / "15 Project Intelligence" / "Recommendation Explanation.md"
    assert path.exists()
    assert "Recommendation Explanation" in path.read_text(encoding="utf-8")
    assert explanation.next_action_target == "테스트 커버리지"


def test_render_markdown_shows_next_action_and_reason() -> None:
    service = RecommendationExplanationService(VaultAdapter(Path(".")))
    explanation = service.generate(_REPORT, ExperienceReport(stats=[]))

    markdown = render_markdown(explanation)

    assert "## Next Action" in markdown
    assert "테스트 커버리지" in markdown
    assert "## Reason" in markdown
    assert "Priority Rule #4 선택" in markdown
    assert "Adaptation 적용 안 됨" in markdown
