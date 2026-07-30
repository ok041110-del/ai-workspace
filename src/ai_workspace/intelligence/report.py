"""Intelligence Layer — Project Intelligence Report (ADR-0043, Milestone 29-T05).

`snapshot`/`health_risk`/`recommendation`(M29-T02~T04)을 순서대로
조합해 하나의 `ProjectIntelligenceReport`를 만들고, Vault에 Markdown
으로 노출한다. 이 모듈 자신은 새 판단 기준을 만들지 않는다 — 이미
만든 세 Analyzer를 호출 순서대로 배열하고 결과를 묶을 뿐이다
(Orchestrating Connector와 같은 성격의 조합 책임, ADR-0041 원칙을
Intelligence Layer에도 적용). `VaultAdapter`에만 의존하고 `domain`/
`interfaces`/`engines`/`vault`를 직접 참조하지 않는다(§8 규칙 21)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.health_risk import ProjectHealthReport, ProjectHealthRiskAnalyzer
from ai_workspace.intelligence.recommendation import (
    ProjectRecommendation,
    ProjectRecommendationEngine,
)
from ai_workspace.intelligence.snapshot import ProjectSnapshot, ProjectSnapshotAnalyzer

_HEALTH_LABELS = {"healthy": "Healthy", "warning": "Warning", "critical": "Critical"}


@dataclass(frozen=True)
class ProjectIntelligenceReport:
    snapshot: ProjectSnapshot
    health_report: ProjectHealthReport
    recommendations: list[ProjectRecommendation]


class ProjectIntelligenceService:
    """Snapshot → Health/Risk → Recommendation을 순서대로 실행해
    `ProjectIntelligenceReport`를 만들고, 필요하면 Vault에 Markdown
    으로 노출(publish)한다. `VaultAdapter`(필수)/`AgentAdapter`(선택)
    만 생성자로 주입받는다."""

    def __init__(
        self,
        vault_adapter: VaultAdapter,
        agent_adapter: AgentAdapter | None = None,
        *,
        stagnant_days_threshold: int = 7,
        owner_overload_threshold: int = 3,
        low_progress_threshold: float = 0.3,
    ) -> None:
        self._snapshot_analyzer = ProjectSnapshotAnalyzer(vault_adapter, agent_adapter)
        self._health_risk_analyzer = ProjectHealthRiskAnalyzer(
            stagnant_days_threshold=stagnant_days_threshold,
            owner_overload_threshold=owner_overload_threshold,
        )
        self._recommendation_engine = ProjectRecommendationEngine(
            low_progress_threshold=low_progress_threshold
        )
        self._vault_adapter = vault_adapter

    def generate(
        self, *, include_archived: bool = True, today: str | None = None
    ) -> ProjectIntelligenceReport:
        """
        입력: include_archived(기본 True), today(고정 날짜 주입용)
        출력: `ProjectIntelligenceReport`(Snapshot + Health/Risk +
              Recommendation)
        예외: 없음
        보장: side-effect 없음(read-only) — Vault에 쓰지 않는다.
              쓰기가 필요하면 `publish()`를 쓴다.
        """
        snapshot_result = self._snapshot_analyzer.analyze(
            include_archived=include_archived, today=today
        )
        health_report = self._health_risk_analyzer.analyze(snapshot_result, today=today)
        recommendations = self._recommendation_engine.recommend(snapshot_result, health_report)
        return ProjectIntelligenceReport(
            snapshot=snapshot_result.snapshot,
            health_report=health_report,
            recommendations=recommendations,
        )

    def publish(
        self, *, include_archived: bool = True, today: str | None = None
    ) -> tuple[ProjectIntelligenceReport, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_intelligence_report()`에 위임).

        보장: `15 Project Intelligence/Project Intelligence.md`가
              이번 결과로 완전히 덮어써진다(누적 append 아님).
        """
        report = self.generate(include_archived=include_archived, today=today)
        markdown = render_markdown(report)
        path = self._vault_adapter.publish_intelligence_report(markdown)
        return report, path


def render_markdown(report: ProjectIntelligenceReport) -> str:
    """`ProjectIntelligenceReport`를 Vault 문서 Markdown으로 렌더링한다.
    순수 함수(입출력 문자열 변환만, I/O 없음)."""
    snapshot = report.snapshot
    health = report.health_report.health

    lines = [
        "---",
        "tags: [project-intelligence]",
        "type: project-intelligence",
        f"generated: {snapshot.generated_at}",
        "---",
        "",
        "# Project Intelligence",
        "",
        "> Milestone 29(Project Intelligence)가 계산한 읽기 전용 리포트다"
        "(ADR-0043). 매 생성 시 이 문서 전체가 덮어써진다 — 편집해도"
        " 다음 생성 때 사라진다.",
        "",
        "## Snapshot",
        "",
        f"- 전체 Task: {snapshot.total_tasks}",
        f"- Todo/In Progress/Review/Done/Archived: "
        f"{snapshot.todo_count}/{snapshot.in_progress_count}/{snapshot.review_count}/"
        f"{snapshot.done_count}/{snapshot.archived_count}",
        f"- 진행률: {snapshot.progress_ratio:.0%}",
        f"- 활성 Agent 수: {snapshot.active_agent_count}",
        "",
        "### Milestone별",
        "",
    ]
    if snapshot.by_milestone:
        lines.extend(
            f"- {milestone}: {count}건" for milestone, count in snapshot.by_milestone.items()
        )
    else:
        lines.append("- (없음)")

    lines.extend(["", "### Owner별", ""])
    if snapshot.by_owner:
        lines.extend(f"- {owner}: {count}건" for owner, count in snapshot.by_owner.items())
    else:
        lines.append("- (없음)")

    lines.extend(
        [
            "",
            "## Health",
            "",
            f"**{_HEALTH_LABELS.get(health.level, health.level)}**",
            "",
        ]
    )
    if health.reasons:
        lines.extend(f"- {reason}" for reason in health.reasons)
    else:
        lines.append("- 감지된 Risk 없음")

    lines.extend(["", "## Risk", ""])
    if report.health_report.risks:
        for risk in report.health_report.risks:
            lines.append(f"- [{risk.severity}] `{risk.kind}` {risk.target}: {risk.detail}")
    else:
        lines.append("- (없음)")

    lines.extend(["", "## Recommendation", ""])
    if report.recommendations:
        for recommendation in report.recommendations:
            lines.append(
                f"- [{recommendation.priority}] `{recommendation.action}` "
                f"{recommendation.target}: {recommendation.reason}"
            )
    else:
        lines.append("- (없음)")

    lines.extend(
        [
            "",
            "## 관련 문서",
            "",
            "- [[Milestones Index]]",
            "- [[Dashboard Index]]",
            "",
            "## 원문",
            "",
            "- `.ai/TASKS.md`의 \"Milestone 29 — Project Intelligence\" 절",
            "- `src/ai_workspace/intelligence/`",
            "",
        ]
    )
    return "\n".join(lines)
