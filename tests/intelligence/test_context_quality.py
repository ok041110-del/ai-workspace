from ai_workspace.intelligence.context import ContextEntry, ProjectContext
from ai_workspace.intelligence.context_quality import (
    FRESHNESS_HEALTHY,
    FRESHNESS_WARNING,
    ContextFreshnessGapAnalyzer,
)


def _entry(kind: str, heading: str = "", milestone: str | None = None) -> ContextEntry:
    return ContextEntry(
        kind=kind,
        heading=heading or f"{kind} heading",
        source_path=f"{kind}.md",
        milestone=milestone,
    )


def test_analyze_flags_gap_for_missing_adr_task_architecture() -> None:
    analyzer = ContextFreshnessGapAnalyzer()
    context = ProjectContext(subject="M30-T03", entries=[])

    quality = analyzer.analyze(context)

    gap_kinds = {gap.kind for gap in quality.gaps}
    assert gap_kinds == {"adr", "task", "architecture"}
    assert quality.score == 0.0


def test_analyze_no_gap_when_all_three_kinds_present() -> None:
    analyzer = ContextFreshnessGapAnalyzer()
    context = ProjectContext(
        subject="M30-T03",
        entries=[_entry("adr"), _entry("task"), _entry("architecture")],
    )

    quality = analyzer.analyze(context)

    assert quality.gaps == []
    assert quality.score == 1.0


def test_analyze_ignores_rule_and_project_for_gap() -> None:
    analyzer = ContextFreshnessGapAnalyzer()
    context = ProjectContext(
        subject="M30-T03",
        entries=[_entry("adr"), _entry("task"), _entry("architecture")],
    )

    quality = analyzer.analyze(context)

    # rule/project 미언급은 Gap이 아니므로 gaps는 여전히 비어있어야 한다.
    assert all(gap.kind not in ("rule", "project") for gap in quality.gaps)


def test_analyze_freshness_healthy_without_current_milestone() -> None:
    analyzer = ContextFreshnessGapAnalyzer()
    context = ProjectContext(subject="M30-T03", entries=[_entry("adr", milestone="M1")])

    quality = analyzer.analyze(context)

    assert quality.freshness.level == FRESHNESS_HEALTHY


def test_analyze_freshness_warns_for_distant_milestone() -> None:
    analyzer = ContextFreshnessGapAnalyzer(milestone_distance_threshold=3)
    context = ProjectContext(
        subject="M30-T03", entries=[_entry("adr", heading="ADR-0001", milestone="M1")]
    )

    quality = analyzer.analyze(context, current_milestone=30)

    assert quality.freshness.level == FRESHNESS_WARNING
    assert any("ADR-0001" in reason for reason in quality.freshness.reasons)


def test_analyze_freshness_healthy_for_nearby_milestone() -> None:
    analyzer = ContextFreshnessGapAnalyzer(milestone_distance_threshold=3)
    context = ProjectContext(
        subject="M30-T03", entries=[_entry("adr", heading="ADR-0043", milestone="M29")]
    )

    quality = analyzer.analyze(context, current_milestone=30)

    assert quality.freshness.level == FRESHNESS_HEALTHY


def test_analyze_score_penalized_when_freshness_warning() -> None:
    analyzer = ContextFreshnessGapAnalyzer(milestone_distance_threshold=3)
    context = ProjectContext(
        subject="M30-T03",
        entries=[
            _entry("adr", heading="ADR-0001", milestone="M1"),
            _entry("task"),
            _entry("architecture"),
        ],
    )

    quality = analyzer.analyze(context, current_milestone=30)

    assert quality.gaps == []
    assert quality.score < 1.0
