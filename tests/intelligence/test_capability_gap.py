from ai_workspace.intelligence.capability import AgentCapabilitySnapshot
from ai_workspace.intelligence.capability_gap import (
    COVERAGE_FULL,
    COVERAGE_NONE,
    COVERAGE_PARTIAL,
    CapabilityGapAnalyzer,
)


def test_analyze_reports_full_coverage_when_no_gaps() -> None:
    snapshot = AgentCapabilitySnapshot(
        total_active_agents=1,
        by_capability={"coding": 1, "review": 1},
        by_role={"coding": 1},
        known_capabilities=frozenset({"coding", "review"}),
    )
    analyzer = CapabilityGapAnalyzer()

    report = analyzer.analyze(snapshot)

    assert report.gaps == []
    assert report.coverage.level == COVERAGE_FULL
    assert report.coverage.ratio == 1.0


def test_analyze_reports_partial_coverage_with_gap_list() -> None:
    snapshot = AgentCapabilitySnapshot(
        total_active_agents=1,
        by_capability={"coding": 1, "review": 0},
        by_role={"coding": 1},
        known_capabilities=frozenset({"coding", "review"}),
    )
    analyzer = CapabilityGapAnalyzer()

    report = analyzer.analyze(snapshot)

    assert [gap.capability for gap in report.gaps] == ["review"]
    assert report.coverage.level == COVERAGE_PARTIAL
    assert report.coverage.ratio == 0.5


def test_analyze_reports_no_coverage_when_no_active_agents() -> None:
    snapshot = AgentCapabilitySnapshot(
        total_active_agents=0,
        by_capability={"coding": 0, "review": 0},
        by_role={},
        known_capabilities=frozenset({"coding", "review"}),
    )
    analyzer = CapabilityGapAnalyzer()

    report = analyzer.analyze(snapshot)

    assert {gap.capability for gap in report.gaps} == {"coding", "review"}
    assert report.coverage.level == COVERAGE_NONE
    assert report.coverage.ratio == 0.0


def test_analyze_gaps_sorted_by_capability_name() -> None:
    snapshot = AgentCapabilitySnapshot(
        total_active_agents=0,
        by_capability={"voice": 0, "coding": 0, "git": 0},
        by_role={},
        known_capabilities=frozenset({"voice", "coding", "git"}),
    )
    analyzer = CapabilityGapAnalyzer()

    report = analyzer.analyze(snapshot)

    assert [gap.capability for gap in report.gaps] == ["coding", "git", "voice"]
