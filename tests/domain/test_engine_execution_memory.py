from ai_workspace.domain.engine_execution_memory import EngineExecutionMemoryStat


def test_record_success_increments_total_and_success_count_and_latency() -> None:
    stat = EngineExecutionMemoryStat().record(True, 1.5)

    assert stat == EngineExecutionMemoryStat(
        total=1, success_count=1, failure_count=0, total_latency_seconds=1.5
    )


def test_record_failure_increments_total_and_failure_count_and_latency() -> None:
    stat = EngineExecutionMemoryStat().record(False, 2.0)

    assert stat == EngineExecutionMemoryStat(
        total=1, success_count=0, failure_count=1, total_latency_seconds=2.0
    )


def test_success_rate_none_when_no_records() -> None:
    assert EngineExecutionMemoryStat().success_rate() is None


def test_success_rate_none_when_sample_size_insufficient() -> None:
    stat = EngineExecutionMemoryStat()
    for _ in range(2):
        stat = stat.record(True, 0.1)

    assert stat.success_rate() is None


def test_success_rate_computed_once_sample_size_sufficient() -> None:
    stat = EngineExecutionMemoryStat()
    for _ in range(3):
        stat = stat.record(True, 0.1)
    stat = stat.record(False, 0.1)

    assert stat.success_rate() == 0.75


def test_average_latency_seconds_none_when_no_records() -> None:
    assert EngineExecutionMemoryStat().average_latency_seconds() is None


def test_average_latency_seconds_averages_recorded_latency() -> None:
    stat = EngineExecutionMemoryStat()
    stat = stat.record(True, 1.0)
    stat = stat.record(True, 3.0)

    assert stat.average_latency_seconds() == 2.0
