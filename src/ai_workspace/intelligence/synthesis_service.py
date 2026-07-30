"""Intelligence Layer — Intelligence Synthesis Service (ADR-0046, Milestone 32-T03).

`ProjectIntelligenceService`(M29)/`ContextIntelligenceService`(M30)/
`CapabilityIntelligenceService`(M31)를 순서대로 실행해 그 결과를
`IntelligenceSynthesisAnalyzer`(M32-T02)로 합성한다. 이 모듈 자신은
Adapter를 전혀 참조하지 않는다 — 이미 있는 세 Service만 조립한다
(`report.py`(M29-T05)/`context_service.py`(M30-T04/T05)/
`capability_service.py`(M31-T04/T05)와 동일한 "Analyzer 조합" 패턴을
Service 3개를 조합하는 층위로 한 단계 더 얹었을 뿐이다, ADR-0041의
Orchestrating 원칙을 Intelligence Layer 안에서 재사용)."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_service import CapabilityIntelligenceService
from ai_workspace.intelligence.context_service import ContextIntelligenceService
from ai_workspace.intelligence.report import ProjectIntelligenceService
from ai_workspace.intelligence.synthesis import IntelligenceOverview, IntelligenceSynthesisAnalyzer

_HEALTH_LABELS = {"healthy": "Healthy", "warning": "Warning", "critical": "Critical"}
_FRESHNESS_LABELS = {"healthy": "Healthy", "warning": "Warning"}
_COVERAGE_LABELS = {"none": "None", "partial": "Partial", "full": "Full"}
_SOURCE_LABELS = {"project": "Project", "context": "Context", "capability": "Capability"}


class IntelligenceSynthesisService:
    """Project/Context/Capability Intelligence Service 3개를 순서대로
    실행해 `IntelligenceOverview`를 만든다(`generate()`). `VaultAdapter`가
    주입돼 있으면 Markdown으로 렌더링해 Vault에 노출한다(`publish()`).
    새 Adapter는 주입받지 않는다 — 각 하위 Service가 이미 필요한
    Adapter를 갖고 있다."""

    def __init__(
        self,
        project_service: ProjectIntelligenceService,
        context_service: ContextIntelligenceService,
        capability_service: CapabilityIntelligenceService,
        vault_adapter: VaultAdapter | None = None,
    ) -> None:
        self._project_service = project_service
        self._context_service = context_service
        self._capability_service = capability_service
        self._synthesizer = IntelligenceSynthesisAnalyzer()
        self._vault_adapter = vault_adapter

    def generate(
        self,
        subject: str,
        *,
        current_milestone: int | None = None,
        include_archived: bool = True,
        today: str | None = None,
    ) -> IntelligenceOverview:
        """
        입력: subject(Context 리포트가 요구하는 Task/Milestone
              식별자), current_milestone/include_archived/today(각
              하위 Service의 `generate()`에 그대로 전달)
        출력: `IntelligenceOverview`
        예외: 없음
        보장: side-effect 없음(read-only) — Vault에 쓰지 않는다.
              쓰기가 필요하면 `publish()`를 쓴다.
        """
        project_report = self._project_service.generate(
            include_archived=include_archived, today=today
        )
        context_report = self._context_service.generate(
            subject, current_milestone=current_milestone
        )
        capability_report = self._capability_service.generate()
        return self._synthesizer.analyze(project_report, context_report, capability_report)

    def publish(
        self,
        subject: str,
        *,
        current_milestone: int | None = None,
        include_archived: bool = True,
        today: str | None = None,
    ) -> tuple[IntelligenceOverview, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_intelligence_overview()`에 위임).

        예외: 생성자에 `vault_adapter`를 주입하지 않았으면
              `ValueError`.
        보장: `15 Project Intelligence/Intelligence Overview.md`가
              이번 결과로 완전히 덮어써진다(누적 append 아님).
        """
        if self._vault_adapter is None:
            raise ValueError("publish()를 쓰려면 생성자에 vault_adapter를 주입해야 합니다")
        overview = self.generate(
            subject,
            current_milestone=current_milestone,
            include_archived=include_archived,
            today=today,
        )
        markdown = render_markdown(overview)
        path = self._vault_adapter.publish_intelligence_overview(markdown)
        return overview, path


def render_markdown(overview: IntelligenceOverview) -> str:
    """`IntelligenceOverview`를 Vault 문서 Markdown으로 렌더링한다.
    순수 함수(입출력 문자열 변환만, I/O 없음)."""
    health_label = _HEALTH_LABELS.get(overview.project_health_level, overview.project_health_level)
    freshness_label = _FRESHNESS_LABELS.get(
        overview.context_freshness_level, overview.context_freshness_level
    )
    coverage_label = _COVERAGE_LABELS.get(
        overview.capability_coverage_level, overview.capability_coverage_level
    )

    lines = [
        "---",
        "tags: [intelligence-overview]",
        "type: intelligence-overview",
        "---",
        "",
        "# Intelligence Overview",
        "",
        "> Milestone 32(Intelligence Synthesis)가 Project/Context/"
        "Capability Intelligence(M29~M31) 리포트를 합성한 읽기 전용 "
        "문서다(ADR-0046). 매 생성 시 이 문서 전체가 덮어써진다 — "
        "편집해도 다음 생성 때 사라진다.",
        "",
        "## 요약",
        "",
        f"- Project Health: {health_label}",
        f"- Context Freshness: {freshness_label}",
        f"- Capability Coverage: {coverage_label}",
        f"- 통합 Finding 수: {overview.total_findings}",
        "",
        "## Findings",
        "",
    ]
    if overview.findings:
        for finding in overview.findings:
            source_label = _SOURCE_LABELS.get(finding.source, finding.source)
            lines.append(
                f"- [{source_label}] `{finding.kind}` {finding.target}: {finding.detail}"
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
            "- [[Milestones Index]]",
            "",
            "## 원문",
            "",
            "- `.ai/TASKS.md`의 \"Milestone 32 — Intelligence Synthesis\" 절",
            "- `src/ai_workspace/intelligence/`",
            "",
        ]
    )
    return "\n".join(lines)
