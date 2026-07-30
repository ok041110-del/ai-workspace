"""Intelligence Layer — Context Intelligence Service (ADR-0044, Milestone 30-T04/T05).

`context.ContextAnalyzer`(M30-T02)와 `context_quality.
ContextFreshnessGapAnalyzer`(M30-T03)를 순서대로 실행해 하나의
`ProjectContextReport`로 묶는다(T04). `render_markdown()`/`publish()`
(T05)는 그 결과를 Markdown으로 렌더링해 Vault에 노출한다 — 여기서도
새 판단 기준을 만들지 않는다."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_workspace.integration.knowledge_adapter import KnowledgeAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.context import ContextAnalyzer, ProjectContext
from ai_workspace.intelligence.context_quality import ContextFreshnessGapAnalyzer, ContextQuality

_KIND_LABELS = {
    "adr": "관련 ADR",
    "task": "관련 Task",
    "architecture": "관련 Architecture",
    "rule": "관련 Rules",
    "project": "관련 Roadmap/PRD",
}
_FRESHNESS_LABELS = {"healthy": "Healthy", "warning": "Warning"}


@dataclass(frozen=True)
class ProjectContextReport:
    context: ProjectContext
    quality: ContextQuality


class ContextIntelligenceService:
    """Context → Freshness/Gap을 순서대로 실행해
    `ProjectContextReport`를 만든다(`generate()`). `VaultAdapter`가
    주입돼 있으면 Markdown으로 렌더링해 Vault에 노출한다
    (`publish()`). `KnowledgeAdapter`(필수)/`VaultAdapter`(선택,
    미주입 시 `publish()` 호출 불가)만 생성자로 주입받는다."""

    def __init__(
        self,
        knowledge_adapter: KnowledgeAdapter,
        vault_adapter: VaultAdapter | None = None,
        *,
        milestone_distance_threshold: int = 3,
    ) -> None:
        self._analyzer = ContextAnalyzer(knowledge_adapter)
        self._quality_analyzer = ContextFreshnessGapAnalyzer(
            milestone_distance_threshold=milestone_distance_threshold
        )
        self._vault_adapter = vault_adapter

    def generate(
        self, subject: str, *, current_milestone: int | None = None
    ) -> ProjectContextReport:
        """
        입력: subject(Task/Milestone 식별자), current_milestone(선택,
              Freshness 비교 기준)
        출력: `ProjectContextReport`(Context + Quality)
        예외: 없음
        보장: side-effect 없음(read-only) — Vault/Knowledge에 쓰지
              않는다. 쓰기가 필요하면 `publish()`를 쓴다.
        """
        context = self._analyzer.analyze(subject)
        quality = self._quality_analyzer.analyze(context, current_milestone=current_milestone)
        return ProjectContextReport(context=context, quality=quality)

    def publish(
        self, subject: str, *, current_milestone: int | None = None
    ) -> tuple[ProjectContextReport, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_project_context()`에 위임).

        예외: 생성자에 `vault_adapter`를 주입하지 않았으면
              `ValueError`.
        보장: `15 Project Intelligence/Project Context.md`가 이번
              결과로 완전히 덮어써진다(누적 append 아님).
        """
        if self._vault_adapter is None:
            raise ValueError("publish()를 쓰려면 생성자에 vault_adapter를 주입해야 합니다")
        report = self.generate(subject, current_milestone=current_milestone)
        markdown = render_markdown(report)
        path = self._vault_adapter.publish_project_context(markdown)
        return report, path


def render_markdown(report: ProjectContextReport) -> str:
    """`ProjectContextReport`를 Vault 문서 Markdown으로 렌더링한다.
    순수 함수(입출력 문자열 변환만, I/O 없음)."""
    context = report.context
    quality = report.quality

    lines = [
        "---",
        "tags: [project-context]",
        "type: project-context",
        f"subject: {context.subject}",
        "---",
        "",
        "# Project Context",
        "",
        "> Milestone 30(Context Intelligence)이 계산한 읽기 전용 "
        "리포트다(ADR-0044). 매 생성 시 이 문서 전체가 덮어써진다.",
        "",
        "## 현재 작업",
        "",
        f"- {context.subject}",
        "",
    ]

    for kind, label in _KIND_LABELS.items():
        entries = context.by_kind(kind)
        lines.extend([f"## {label}", ""])
        if entries:
            lines.extend(f"- {entry.heading}" for entry in entries)
        else:
            lines.append("- (없음)")
        lines.append("")

    lines.extend(
        [
            "## Freshness",
            "",
            f"**{_FRESHNESS_LABELS.get(quality.freshness.level, quality.freshness.level)}**",
            "",
        ]
    )
    if quality.freshness.reasons:
        lines.extend(f"- {reason}" for reason in quality.freshness.reasons)
    else:
        lines.append("- 오래된 참조 없음")

    lines.extend(["", "## Gap", ""])
    if quality.gaps:
        lines.extend(f"- [{gap.kind}] {gap.detail}" for gap in quality.gaps)
    else:
        lines.append("- 없음")

    lines.extend(
        [
            "",
            f"## Context Quality Score: {quality.score:.0%}",
            "",
            "## 관련 문서",
            "",
            "- [[Milestones Index]]",
            "- [[Project Intelligence]]",
            "",
            "## 원문",
            "",
            "- `.ai/TASKS.md`의 \"Milestone 30 — Context Intelligence\" 절",
            "- `src/ai_workspace/intelligence/`",
            "",
        ]
    )
    return "\n".join(lines)
