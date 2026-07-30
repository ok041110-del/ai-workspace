from ai_workspace.intelligence.capability import AgentCapabilitySnapshot
from ai_workspace.intelligence.capability_gap import (
    CapabilityCoverage,
    CapabilityGap,
    CapabilityGapReport,
)
from ai_workspace.intelligence.capability_service import CapabilityIntelligenceReport
from ai_workspace.intelligence.context import ProjectContext
from ai_workspace.intelligence.context_quality import ContextFreshness, ContextGap, ContextQuality
from ai_workspace.intelligence.context_service import ProjectContextReport
from ai_workspace.intelligence.health_risk import ProjectHealth, ProjectHealthReport, ProjectRisk
from ai_workspace.intelligence.report import ProjectIntelligenceReport
from ai_workspace.intelligence.snapshot import ProjectSnapshot
from ai_workspace.intelligence.synthesis import IntelligenceSynthesisAnalyzer


def _project_report(*, risks: list[ProjectRisk] | None = None) -> ProjectIntelligenceReport:
    risks = risks or []
    health_level = "critical" if any(r.severity == "critical" for r in risks) else (
        "warning" if risks else "healthy"
    )
    snapshot = ProjectSnapshot(
        generated_at="2026-07-30",
        total_tasks=0,
        by_status={},
        by_milestone={},
        by_owner={},
        todo_count=0,
        in_progress_count=0,
        review_count=0,
        done_count=0,
        archived_count=0,
        progress_ratio=0.0,
        active_agent_count=0,
    )
    return ProjectIntelligenceReport(
        snapshot=snapshot,
        health_report=ProjectHealthReport(
            health=ProjectHealth(level=health_level, reasons=[r.detail for r in risks]),
            risks=risks,
        ),
        recommendations=[],
    )


def _context_report(*, gaps: list[ContextGap] | None = None) -> ProjectContextReport:
    gaps = gaps or []
    return ProjectContextReport(
        context=ProjectContext(subject="M32-T02", entries=[]),
        quality=ContextQuality(
            freshness=ContextFreshness(level="healthy", reasons=[]),
            gaps=gaps,
            score=1.0,
        ),
    )


def _capability_report(*, gaps: list[CapabilityGap] | None = None) -> CapabilityIntelligenceReport:
    gaps = gaps or []
    return CapabilityIntelligenceReport(
        snapshot=AgentCapabilitySnapshot(
            total_active_agents=0, by_role={}, by_capability={}, known_capabilities=[]
        ),
        gap_report=CapabilityGapReport(
            coverage=CapabilityCoverage(level="none", ratio=0.0), gaps=gaps
        ),
    )


def test_analyze_combines_levels_from_all_three_reports() -> None:
    analyzer = IntelligenceSynthesisAnalyzer()

    overview = analyzer.analyze(_project_report(), _context_report(), _capability_report())

    assert overview.project_health_level == "healthy"
    assert overview.context_freshness_level == "healthy"
    assert overview.capability_coverage_level == "none"
    assert overview.findings == []
    assert overview.total_findings == 0


def test_analyze_merges_findings_from_all_three_reports() -> None:
    analyzer = IntelligenceSynthesisAnalyzer()
    project_report = _project_report(
        risks=[
            ProjectRisk(
                kind="stagnant_task", target="T29-05", detail="정체됨", severity="warning"
            )
        ]
    )
    context_report = _context_report(
        gaps=[ContextGap(kind="adr", detail="ADR 언급 없음")]
    )
    capability_report = _capability_report(
        gaps=[CapabilityGap(capability="coding", detail="활성 Agent 없음")]
    )

    overview = analyzer.analyze(project_report, context_report, capability_report)

    assert overview.total_findings == 3
    sources = {finding.source for finding in overview.findings}
    assert sources == {"project", "context", "capability"}
    project_finding = next(f for f in overview.findings if f.source == "project")
    assert project_finding.kind == "stagnant_task"
    assert project_finding.target == "T29-05"
    context_finding = next(f for f in overview.findings if f.source == "context")
    assert context_finding.kind == "context_adr"
    assert context_finding.target == "M32-T02"
    capability_finding = next(f for f in overview.findings if f.source == "capability")
    assert capability_finding.kind == "capability_gap"
    assert capability_finding.target == "coding"


def test_analyze_reflects_critical_project_health() -> None:
    analyzer = IntelligenceSynthesisAnalyzer()
    project_report = _project_report(
        risks=[
            ProjectRisk(
                kind="owner_overload", target="AI", detail="과부하", severity="critical"
            )
        ]
    )

    overview = analyzer.analyze(project_report, _context_report(), _capability_report())

    assert overview.project_health_level == "critical"
