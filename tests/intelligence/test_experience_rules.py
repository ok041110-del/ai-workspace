import pytest

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


def test_recent_failure_streak_counts_consecutive_failures_from_latest() -> None:
    """M51(ADR-0068) — 가장 최근 기록부터 거슬러 올라가며 연속 실패를
    센다. 도중에 성공을 만나면 멈춘다."""
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T01", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "failure", "2026-07-30T01:00:00+00:00"),
        _record("M40-T01", "failure", "2026-07-30T02:00:00+00:00"),
    ]

    report = analyzer.analyze(records)

    assert report.stats[0].recent_failure_streak == 2


def test_recent_failure_streak_is_zero_when_latest_is_success() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T01", "failure", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T01:00:00+00:00"),
    ]

    report = analyzer.analyze(records)

    assert report.stats[0].recent_failure_streak == 0


def test_recent_failure_streak_ignores_input_order() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T01", "failure", "2026-07-30T02:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "failure", "2026-07-30T01:00:00+00:00"),
    ]

    report = analyzer.analyze(records)

    assert report.stats[0].recent_failure_streak == 2


def test_decayed_failure_rate_is_exactly_one_when_all_records_are_failures() -> None:
    """M53(ADR-0071) — 전체가 실패면 Decay 가중치와 무관하게 항상
    정확히 1.0(M49 조건과의 호환성 보장)."""
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T01", "failure", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "failure", "2026-07-30T01:00:00+00:00"),
        _record("M40-T01", "failure", "2026-07-30T02:00:00+00:00"),
    ]

    report = analyzer.analyze(records)

    assert report.stats[0].decayed_failure_rate == pytest.approx(1.0)


def test_decayed_failure_rate_is_zero_when_all_records_are_successes() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T01", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T01:00:00+00:00"),
    ]

    report = analyzer.analyze(records)

    assert report.stats[0].decayed_failure_rate == pytest.approx(0.0)


def test_decayed_failure_rate_weighs_recent_failure_more_than_old_failure() -> None:
    """M53(ADR-0071) — 실패 1건/성공 2건으로 실패 개수는 같아도, 그
    실패가 가장 최근 기록이면 오래된 기록일 때보다 decayed_failure_rate
    가 더 높다(지수 Decay가 최근 기록에 더 큰 비중을 준다는 증거)."""
    analyzer = ExperienceAnalyzer()
    recent_failure_records = [
        _record("M40-T01", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T01:00:00+00:00"),
        _record("M40-T01", "failure", "2026-07-30T02:00:00+00:00"),
    ]
    old_failure_records = [
        _record("M40-T02", "failure", "2026-07-30T00:00:00+00:00"),
        _record("M40-T02", "success", "2026-07-30T01:00:00+00:00"),
        _record("M40-T02", "success", "2026-07-30T02:00:00+00:00"),
    ]

    report = analyzer.analyze(recent_failure_records + old_failure_records)

    recent_rate = next(s for s in report.stats if s.task_id == "M40-T01").decayed_failure_rate
    old_rate = next(s for s in report.stats if s.task_id == "M40-T02").decayed_failure_rate
    assert recent_rate > old_rate
    assert recent_rate == pytest.approx(1 / 2.44)
    assert old_rate == pytest.approx(0.64 / 2.44)


def test_decayed_failure_rate_ignores_input_order() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T01", "failure", "2026-07-30T02:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T01:00:00+00:00"),
    ]
    shuffled = [records[2], records[0], records[1]]

    report_in_order = analyzer.analyze(records)
    report_shuffled = analyzer.analyze(shuffled)

    assert report_in_order.stats[0].decayed_failure_rate == pytest.approx(
        report_shuffled.stats[0].decayed_failure_rate
    )


def test_analyze_does_not_mutate_input_list() -> None:
    analyzer = ExperienceAnalyzer()
    records = [
        _record("M40-T02", "success", "2026-07-30T00:00:00+00:00"),
        _record("M40-T01", "success", "2026-07-30T01:00:00+00:00"),
    ]
    original_order = list(records)

    analyzer.analyze(records)

    assert records == original_order
