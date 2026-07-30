"""Intelligence Layer — Session Resume Service (ADR-0047, Milestone 33-T03).

새 세션이 시작될 때 "지금 무엇을 하고 있었는가"를 자동 복원하는
Read Only 조합 계층. `CurrentWorkSelector`(M33-T02)로 "현재 작업"을
고른 뒤, 이미 있는 M29~M32 Intelligence(`ProjectIntelligenceService`/
`ContextIntelligenceService`/`CapabilityIntelligenceService`/
`IntelligenceSynthesisAnalyzer`)를 그대로 실행해 조합한다. 새로운
지표·점수·추천 로직을 만들지 않는다 — "현재 작업 선택" 규칙 하나만
더할 뿐이다."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_service import (
    CapabilityIntelligenceReport,
    CapabilityIntelligenceService,
)
from ai_workspace.intelligence.context import ProjectContext
from ai_workspace.intelligence.context_quality import (
    FRESHNESS_HEALTHY,
    ContextFreshness,
    ContextQuality,
)
from ai_workspace.intelligence.context_service import (
    ContextIntelligenceService,
    ProjectContextReport,
)
from ai_workspace.intelligence.report import ProjectIntelligenceReport, ProjectIntelligenceService
from ai_workspace.intelligence.session_resume import CurrentWork, CurrentWorkSelector
from ai_workspace.intelligence.synthesis import IntelligenceOverview, IntelligenceSynthesisAnalyzer

_HEALTH_LABELS = {"healthy": "Healthy", "warning": "Warning", "critical": "Critical"}
_FRESHNESS_LABELS = {"healthy": "Healthy", "warning": "Warning"}
_COVERAGE_LABELS = {"none": "None", "partial": "Partial", "full": "Full"}


@dataclass(frozen=True)
class SessionResumeReport:
    current_work: CurrentWork | None
    project_report: ProjectIntelligenceReport
    context_report: ProjectContextReport
    capability_report: CapabilityIntelligenceReport
    overview: IntelligenceOverview


def _parse_milestone(milestone: str) -> int | None:
    try:
        return int(milestone.lstrip("Mm"))
    except ValueError:
        return None


class SessionResumeService:
    """"현재 작업" 판정(`CurrentWorkSelector`) + Project/Context/
    Capability Intelligence(M29~M31) + Intelligence Overview 합성
    (M32 `IntelligenceSynthesisAnalyzer` 재사용)을 한 번에 실행해
    `SessionResumeReport`를 만든다(`generate()`). `VaultAdapter`가
    주입돼 있으면 Markdown으로 렌더링해 Vault에 노출한다
    (`publish()`)."""

    def __init__(
        self,
        vault_adapter: VaultAdapter,
        project_service: ProjectIntelligenceService,
        context_service: ContextIntelligenceService,
        capability_service: CapabilityIntelligenceService,
    ) -> None:
        self._vault_adapter = vault_adapter
        self._project_service = project_service
        self._context_service = context_service
        self._capability_service = capability_service
        self._selector = CurrentWorkSelector()
        self._synthesizer = IntelligenceSynthesisAnalyzer()

    def generate(
        self, *, include_archived: bool = True, today: str | None = None
    ) -> SessionResumeReport:
        """
        입력: include_archived(기본 True), today(고정 날짜 주입용)
        출력: `SessionResumeReport`(현재 작업 + Project/Context/
              Capability 리포트 + Overview)
        예외: 없음 — 활성 Task가 없으면 `current_work=None`으로
              방어적으로 반환한다(판단 중단하지 않음).
        보장: side-effect 없음(read-only) — Vault에 쓰지 않는다.
              쓰기가 필요하면 `publish()`를 쓴다.
        """
        tasks = self._vault_adapter.list_tasks(include_archived=include_archived)
        current_work = self._selector.select(tasks)

        project_report = self._project_service.generate(
            include_archived=include_archived, today=today
        )
        if current_work is not None:
            context_report = self._context_service.generate(
                current_work.task_id, current_milestone=_parse_milestone(current_work.milestone)
            )
        else:
            # ContextAnalyzer.analyze()는 빈 subject를 허용하지 않는다
            # (모든 문서를 매칭시켜 버림) — 현재 작업이 없으면 Context
            # Intelligence를 아예 호출하지 않고 "해당 없음"으로 반환한다.
            context_report = ProjectContextReport(
                context=ProjectContext(subject="", entries=[]),
                quality=ContextQuality(
                    freshness=ContextFreshness(level=FRESHNESS_HEALTHY, reasons=[]),
                    gaps=[],
                    score=1.0,
                ),
            )
        capability_report = self._capability_service.generate()
        overview = self._synthesizer.analyze(project_report, context_report, capability_report)

        return SessionResumeReport(
            current_work=current_work,
            project_report=project_report,
            context_report=context_report,
            capability_report=capability_report,
            overview=overview,
        )

    def publish(
        self, *, include_archived: bool = True, today: str | None = None
    ) -> tuple[SessionResumeReport, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_session_resume()`에 위임).

        보장: `15 Project Intelligence/Session Resume.md`가 이번
              결과로 완전히 덮어써진다(누적 append 아님).
        """
        report = self.generate(include_archived=include_archived, today=today)
        markdown = render_markdown(report)
        path = self._vault_adapter.publish_session_resume(markdown)
        return report, path


def render_markdown(report: SessionResumeReport) -> str:
    """`SessionResumeReport`를 Vault 문서 Markdown으로 렌더링한다.
    순수 함수(입출력 문자열 변환만, I/O 없음)."""
    lines = [
        "---",
        "tags: [session-resume]",
        "type: session-resume",
        "---",
        "",
        "# Session Resume",
        "",
        "> Milestone 33(Session Resume)이 M29~M32 Intelligence를 조합해 "
        "만든 읽기 전용 문서다(ADR-0047). 매 생성 시 이 문서 전체가 "
        "덮어써진다 — 편집해도 다음 생성 때 사라진다.",
        "",
        "## 현재 작업",
        "",
    ]
    current_work = report.current_work
    if current_work is not None:
        lines.extend(
            [
                f"- Task: {current_work.task_id}({current_work.title})",
                f"- 상태: {current_work.status}",
                f"- Milestone: {current_work.milestone}",
                f"- Owner: {current_work.owner}",
                f"- 마지막 갱신: {current_work.updated}",
            ]
        )
    else:
        lines.append("- 현재 진행 중인 Task 없음(활성 상태 Task 0건)")

    snapshot = report.project_report.snapshot
    health = report.project_report.health_report.health
    lines.extend(
        [
            "",
            "## Project 상태",
            "",
            f"- 진행률: {snapshot.progress_ratio:.0%}",
            f"- Health: {_HEALTH_LABELS.get(health.level, health.level)}",
            "",
            "## 관련 Context",
            "",
        ]
    )
    if report.context_report.context.entries:
        lines.extend(
            f"- [{entry.kind}] {entry.heading}" for entry in report.context_report.context.entries
        )
    else:
        lines.append("- (없음)")

    coverage = report.capability_report.gap_report.coverage
    lines.extend(
        [
            "",
            "## Capability 상태",
            "",
            f"- Coverage: {_COVERAGE_LABELS.get(coverage.level, coverage.level)} "
            f"({coverage.ratio:.0%})",
            "",
            "## 다음 작업",
            "",
        ]
    )
    if report.project_report.recommendations:
        for recommendation in report.project_report.recommendations:
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
            "- [[Project Intelligence]]",
            "- [[Project Context]]",
            "- [[Capability Intelligence]]",
            "- [[Intelligence Overview]]",
            "",
            "## 원문",
            "",
            "- `.ai/TASKS.md`의 \"Milestone 33 — Session Resume\" 절",
            "- `src/ai_workspace/intelligence/`",
            "",
        ]
    )
    return "\n".join(lines)
