"""Intelligence Layer — Cross-Intelligence Synthesis (ADR-0046, Milestone 32-T02).

M29(Project)/M30(Context)/M31(Capability) Intelligence Layer가 이미
만든 세 리포트(`ProjectIntelligenceReport`/`ProjectContextReport`/
`CapabilityIntelligenceReport`)만 입력으로 받는 순수 함수 계층이다 —
Adapter를 전혀 참조하지 않는다(이미 계산된 리포트만 재사용, 새로운
데이터 접근 경로 없음). 세 리포트 중 어느 것의 판단 로직도 재계산
하지 않는다 — 이미 만들어진 Risk/Gap을 그대로 옮겨 담아 하나의
Finding 목록으로 합칠 뿐이다. AI 추론/LLM 호출은 하지 않는다."""

from __future__ import annotations

from dataclasses import dataclass, field

from ai_workspace.intelligence.capability_service import CapabilityIntelligenceReport
from ai_workspace.intelligence.context_service import ProjectContextReport
from ai_workspace.intelligence.report import ProjectIntelligenceReport


@dataclass(frozen=True)
class SynthesizedFinding:
    source: str
    kind: str
    target: str
    detail: str


@dataclass(frozen=True)
class IntelligenceOverview:
    project_health_level: str
    context_freshness_level: str
    capability_coverage_level: str
    findings: list[SynthesizedFinding] = field(default_factory=list)

    @property
    def total_findings(self) -> int:
        return len(self.findings)


class IntelligenceSynthesisAnalyzer:
    """`ProjectIntelligenceReport`/`ProjectContextReport`/
    `CapabilityIntelligenceReport`를 조합해 `IntelligenceOverview`를
    만드는 Rule 기반 Analyzer. 새 임계값·새 판단 기준을 두지 않는다
    — 세 리포트가 이미 계산해 둔 등급/Risk/Gap을 그대로 모을 뿐이다."""

    def analyze(
        self,
        project_report: ProjectIntelligenceReport,
        context_report: ProjectContextReport,
        capability_report: CapabilityIntelligenceReport,
    ) -> IntelligenceOverview:
        """
        입력: 이미 생성된 세 Intelligence 리포트(M29/M30/M31
              `generate()`의 결과)
        출력: `IntelligenceOverview`(세 리포트의 등급 + 합쳐진 Finding
              목록, target 기준 정렬)
        예외: 없음
        보장: side-effect 없음(read-only), 입력 리포트를 변경하지
              않는다.
        """
        findings: list[SynthesizedFinding] = []
        findings.extend(
            SynthesizedFinding(
                source="project", kind=risk.kind, target=risk.target, detail=risk.detail
            )
            for risk in project_report.health_report.risks
        )
        findings.extend(
            SynthesizedFinding(
                source="context",
                kind=f"context_{gap.kind}",
                target=context_report.context.subject,
                detail=gap.detail,
            )
            for gap in context_report.quality.gaps
        )
        findings.extend(
            SynthesizedFinding(
                source="capability",
                kind="capability_gap",
                target=gap.capability,
                detail=gap.detail,
            )
            for gap in capability_report.gap_report.gaps
        )
        findings.sort(key=lambda finding: (finding.source, finding.target))

        return IntelligenceOverview(
            project_health_level=project_report.health_report.health.level,
            context_freshness_level=context_report.quality.freshness.level,
            capability_coverage_level=capability_report.gap_report.coverage.level,
            findings=findings,
        )
