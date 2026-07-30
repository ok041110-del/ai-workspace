"""Intelligence Layer — Recommendation Intelligence Service (ADR-0049, Milestone 35-T03).

`VaultAdapter.list_tasks()`(기존) 1회 조회 + `ProjectIntelligenceService`
/`CapabilityIntelligenceService`(M29/M31, 주입) 실행 +
`CurrentWorkSelector`(M33)/`WorkflowFlowAnalyzer`(M34, 같은 tasks
목록 재사용) 실행 + `RecommendationRuleAnalyzer`(M35-T02) 호출을
조합만 하는 Read Only 계층이다. 판정 규칙 자체는 여기 두지 않는다 —
전부 Analyzer의 책임이다(ADR-0049 결정 3)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_gap import CapabilityGapReport
from ai_workspace.intelligence.capability_service import CapabilityIntelligenceService
from ai_workspace.intelligence.recommendation import ProjectRecommendation
from ai_workspace.intelligence.recommendation_rules import NextAction, RecommendationRuleAnalyzer
from ai_workspace.intelligence.report import ProjectIntelligenceService
from ai_workspace.intelligence.session_resume import CurrentWork, CurrentWorkSelector
from ai_workspace.intelligence.workflow_flow import (
    WorkflowFlowAnalyzer,
    WorkflowFlowReport,
)

_SOURCE_LABELS = {
    "current_work": "현재 작업 계속 수행",
    "next_task": "다음 Task 시작",
    "blocked_task": "Blocked 해소",
    "capability_gap": "Capability 보완",
    "project_recommendation": "Project Recommendation",
}
_COVERAGE_LABELS = {"none": "None", "partial": "Partial", "full": "Full"}


@dataclass(frozen=True)
class RecommendationIntelligenceReport:
    next_action: NextAction | None
    current_work: CurrentWork | None
    workflow_report: WorkflowFlowReport
    capability_gap_report: CapabilityGapReport
    project_recommendations: list[ProjectRecommendation]


class RecommendationIntelligenceService:
    """`VaultAdapter`(Task 조회) + `ProjectIntelligenceService`/
    `CapabilityIntelligenceService`(M29/M31) + `CurrentWorkSelector`
    (M33)/`WorkflowFlowAnalyzer`(M34) + `RecommendationRuleAnalyzer`
    (M35-T02)를 조합해 `RecommendationIntelligenceReport`를 만든다."""

    def __init__(
        self,
        vault_adapter: VaultAdapter,
        project_service: ProjectIntelligenceService,
        capability_service: CapabilityIntelligenceService,
    ) -> None:
        self._vault_adapter = vault_adapter
        self._project_service = project_service
        self._capability_service = capability_service
        self._current_work_selector = CurrentWorkSelector()
        self._workflow_analyzer = WorkflowFlowAnalyzer()
        self._rule_analyzer = RecommendationRuleAnalyzer()

    def generate(
        self, *, include_archived: bool = True, today: str | None = None
    ) -> RecommendationIntelligenceReport:
        """
        입력: include_archived(기본 True), today(고정 날짜 주입용)
        출력: `RecommendationIntelligenceReport`(단일 `NextAction`
              + 근거가 된 하위 리포트 전체)
        예외: 없음 — 5단계 Priority 모두 해당 없으면
              `next_action=None`으로 방어적으로 반환한다.
        보장: side-effect 없음(read-only) — Vault에 쓰지 않는다.
              쓰기가 필요하면 `publish()`를 쓴다.
        """
        tasks = self._vault_adapter.list_tasks(include_archived=include_archived)
        current_work = self._current_work_selector.select(tasks)
        workflow_report = self._workflow_analyzer.analyze(tasks)

        project_report = self._project_service.generate(
            include_archived=include_archived, today=today
        )
        capability_report = self._capability_service.generate()

        next_action = self._rule_analyzer.analyze(
            current_work=current_work,
            workflow_report=workflow_report,
            capability_gap_report=capability_report.gap_report,
            project_recommendations=project_report.recommendations,
        )

        return RecommendationIntelligenceReport(
            next_action=next_action,
            current_work=current_work,
            workflow_report=workflow_report,
            capability_gap_report=capability_report.gap_report,
            project_recommendations=project_report.recommendations,
        )

    def publish(
        self, *, include_archived: bool = True, today: str | None = None
    ) -> tuple[RecommendationIntelligenceReport, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_recommendation_intelligence()`에 위임).

        보장: `15 Project Intelligence/Recommendation Intelligence.md`
              가 이번 결과로 완전히 덮어써진다(누적 append 아님).
        """
        report = self.generate(include_archived=include_archived, today=today)
        markdown = render_markdown(report)
        path = self._vault_adapter.publish_recommendation_intelligence(markdown)
        return report, path


def render_markdown(report: RecommendationIntelligenceReport) -> str:
    """`RecommendationIntelligenceReport`를 Vault 문서 Markdown으로
    렌더링한다. 순수 함수(입출력 문자열 변환만, I/O 없음)."""
    lines = [
        "---",
        "tags: [recommendation-intelligence]",
        "type: recommendation-intelligence",
        "---",
        "",
        "# Recommendation Intelligence",
        "",
        "> Milestone 35(Recommendation Intelligence)가 M29/M31/M33/M34 "
        "Intelligence를 조합해 만든 읽기 전용 문서다(ADR-0049). "
        "자동으로 실행하지 않고 추천만 제공한다. 매 생성 시 이 문서 "
        "전체가 덮어써진다 — 편집해도 다음 생성 때 사라진다.",
        "",
        "## 다음 행동",
        "",
    ]
    next_action = report.next_action
    if next_action is not None:
        lines.extend(
            [
                f"- 근거: {_SOURCE_LABELS.get(next_action.source, next_action.source)}",
                f"- 행동: `{next_action.action}`",
                f"- 대상: {next_action.target}",
                f"- 이유: {next_action.reason}",
            ]
        )
    else:
        lines.append("- 추천할 다음 행동 없음")

    lines.extend(["", "## 근거 — 현재 작업", ""])
    if report.current_work is not None:
        lines.append(
            f"- {report.current_work.task_id}({report.current_work.title}), "
            f"상태: {report.current_work.status}"
        )
    else:
        lines.append("- 현재 진행 중인 Task 없음")

    lines.extend(["", "## 근거 — Workflow", ""])
    if report.workflow_report.milestones:
        for milestone in report.workflow_report.milestones:
            lines.append(
                f"- {milestone.milestone}: 진행률 {milestone.completion_ratio:.0%}, "
                f"Blocked {milestone.blocked_count}건, "
                f"Next: {', '.join(milestone.next_task_ids) or '없음'}"
            )
    else:
        lines.append("- 진행 중인 Milestone 없음")

    coverage = report.capability_gap_report.coverage
    lines.extend(
        [
            "",
            "## 근거 — Capability",
            "",
            f"- Coverage: {_COVERAGE_LABELS.get(coverage.level, coverage.level)} "
            f"({coverage.ratio:.0%})",
        ]
    )

    lines.extend(["", "## 근거 — Project Recommendation", ""])
    if report.project_recommendations:
        lines.extend(
            f"- [{recommendation.priority}] `{recommendation.action}` "
            f"{recommendation.target}: {recommendation.reason}"
            for recommendation in report.project_recommendations
        )
    else:
        lines.append("- (없음)")

    lines.append("")
    return "\n".join(lines)
