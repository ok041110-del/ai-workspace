from pathlib import Path

from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_service import CapabilityIntelligenceService
from ai_workspace.intelligence.experience_rules import ExperienceReport, ExperienceStat
from ai_workspace.intelligence.recommendation_rules import (
    ACTION_CONTINUE_CURRENT_WORK,
    ACTION_IMPROVE_CAPABILITY,
    ACTION_START_NEXT_TASK,
    SOURCE_CAPABILITY_GAP,
    SOURCE_CURRENT_WORK,
    SOURCE_NEXT_TASK,
)
from ai_workspace.intelligence.recommendation_service import (
    RecommendationIntelligenceService,
    render_markdown,
)
from ai_workspace.intelligence.report import ProjectIntelligenceService
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler


def _make_agent_adapter() -> AgentAdapter:
    return AgentAdapter(InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler())


def _make_service(vault_root: Path) -> RecommendationIntelligenceService:
    vault_adapter = VaultAdapter(vault_root)
    return RecommendationIntelligenceService(
        vault_adapter,
        ProjectIntelligenceService(vault_adapter),
        CapabilityIntelligenceService(_make_agent_adapter()),
    )


def test_generate_falls_back_to_capability_gap_when_nothing_else_applies(tmp_path: Path) -> None:
    # 활성 Agent가 0명인 이 저장소의 "워크숍 단계" 현실(M31과 동일)에서는
    # Capability Gap이 항상 존재해 Priority 4가 항상 걸린다 — Priority
    # 1~3(Current Work/Next/Blocked Task)이 전부 해당 없을 때의 정상 동작.
    service = _make_service(tmp_path)

    report = service.generate(today="2026-07-30")

    assert report.next_action is not None
    assert report.next_action.source == SOURCE_CAPABILITY_GAP
    assert report.next_action.action == ACTION_IMPROVE_CAPABILITY
    assert report.current_work is None
    assert report.workflow_report.milestones == []
    assert report.project_recommendations == []


def test_generate_recommends_continuing_current_work(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M35-T02",
        "Analyzer",
        status="in-progress",
        priority="high",
        milestone="M35",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    service = RecommendationIntelligenceService(
        vault_adapter,
        ProjectIntelligenceService(vault_adapter),
        CapabilityIntelligenceService(_make_agent_adapter()),
    )

    report = service.generate(today="2026-07-30")

    assert report.next_action is not None
    assert report.next_action.source == SOURCE_CURRENT_WORK
    assert report.next_action.action == ACTION_CONTINUE_CURRENT_WORK
    assert report.next_action.target == "M35-T02"


def test_generate_recommends_next_task_when_no_current_work(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M35-T01",
        "설계",
        status="done",
        priority="high",
        milestone="M35",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    vault_adapter.create_task(
        "M35-T02",
        "Analyzer",
        status="todo",
        priority="high",
        milestone="M35",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    service = RecommendationIntelligenceService(
        vault_adapter,
        ProjectIntelligenceService(vault_adapter),
        CapabilityIntelligenceService(_make_agent_adapter()),
    )

    report = service.generate(today="2026-07-30")

    assert report.next_action is not None
    assert report.next_action.source == SOURCE_NEXT_TASK
    assert report.next_action.action == ACTION_START_NEXT_TASK
    assert report.next_action.target == "M35-T02"


def test_render_markdown_shows_next_action_and_evidence(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M35-T02",
        "Analyzer",
        status="in-progress",
        priority="high",
        milestone="M35",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    service = RecommendationIntelligenceService(
        vault_adapter,
        ProjectIntelligenceService(vault_adapter),
        CapabilityIntelligenceService(_make_agent_adapter()),
    )

    markdown = render_markdown(service.generate(today="2026-07-30"))

    assert "## 다음 행동" in markdown
    assert "현재 작업 계속 수행" in markdown
    assert "M35-T02" in markdown
    assert "## 근거 — Capability" in markdown


def test_publish_writes_recommendation_intelligence_file(tmp_path: Path) -> None:
    service = _make_service(tmp_path)

    report, path = service.publish(today="2026-07-30")

    assert path == tmp_path / "15 Project Intelligence" / "Recommendation Intelligence.md"
    assert path.exists()
    assert report.next_action is not None
    assert "Recommendation Intelligence" in path.read_text(encoding="utf-8")


def test_generate_is_identical_to_m35_when_experience_report_is_none(tmp_path: Path) -> None:
    # Milestone 42 DoD(사용자 조건): experience_report=None이면 M35와
    # 100% 동일 동작 — Adjustment가 전혀 개입하지 않는다.
    service = _make_service(tmp_path)

    without_param = service.generate(today="2026-07-30")
    with_none = service.generate(today="2026-07-30", experience_report=None)

    assert without_param == with_none
    assert without_param.adjusted is False
    assert without_param.adjustment_reason is None


def test_generate_withholds_next_action_when_experience_shows_only_failures(
    tmp_path: Path,
) -> None:
    service = _make_service(tmp_path)
    baseline = service.generate(today="2026-07-30")
    assert baseline.next_action is not None
    target = baseline.next_action.target

    experience_report = ExperienceReport(
        stats=[
            ExperienceStat(
                task_id=target,
                total=1,
                success_count=0,
                failure_count=1,
                last_result="failure",
                last_timestamp="2026-07-30T00:00:00",
            )
        ]
    )

    report = service.generate(today="2026-07-30", experience_report=experience_report)

    assert report.next_action is None
    assert report.adjusted is True
    assert report.adjustment_reason is not None
    assert target in report.adjustment_reason


def test_render_markdown_shows_adaptation_section(tmp_path: Path) -> None:
    service = _make_service(tmp_path)

    markdown = render_markdown(service.generate(today="2026-07-30"))

    assert "## Adaptation(Milestone 42)" in markdown
    assert "조정 없음" in markdown
