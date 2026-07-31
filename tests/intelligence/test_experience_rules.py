from ai_workspace.intelligence.experience_rules import ExperienceAnalyzer, ExperienceRecord


def _record(
    task_id: str, result: str, timestamp: str, action: str = "실행", reason: str | None = None
) -> ExperienceRecord:
    return ExperienceRecord(
        task_id=task_id, action=action, result=result, timestamp=timestamp, reason=reason
    )


def test_analyze_returns_empty_report_for_no_records() -> None:
    analyzer = ExperienceAnalyzer()

    report = analyzer.analyze([])

    assert report.stats == []


def test_analyze_aggregates_success_and_failure_counts_per_task() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T01", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "failure", "2026-07-30T01:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T02:00:00+00:00"),
    ]

    report = analyzer.analyze(records)

    assert len(report.stats) == 1
    stat = report.stats[0]
    assert stat.task_id == "M40-T01"
    assert stat.total == 3
    assert stat.success_count == 2
    assert stat.failure_count == 1


def test_analyze_reports_latest_result_by_timestamp_not_input_order() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T01", "failure", "2026-07-30T02:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T01:00:00+00:00"),
    ]

    report = analyzer.analyze(records)

    assert report.stats[0].last_result == "failure"
    assert report.stats[0].last_timestamp == "2026-07-30T02:00:00+00:00"


def test_analyze_sorts_stats_by_task_id_regardless_of_input_order() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T02", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T00:00:00+00:00"),
    ]

    report = analyzer.analyze(records)

    assert [stat.task_id for stat in report.stats] == ["M40-T01", "M40-T02"]


def test_analyze_is_deterministic_for_the_same_input() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T02", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "failure", "2026-07-30T01:00:00+00:00", reason="boom"),
    ]

    first = analyzer.analyze(records)
    second = analyzer.analyze(records)

    assert first == second


def test_analyze_does_not_mutate_input_list() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T02", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T01:00:00+00:00"),
    ]
    original_order = list(records)

    analyzer.analyze(records)

    assert records == original_order
