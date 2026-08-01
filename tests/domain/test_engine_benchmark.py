from ai_workspace.domain.engine_benchmark import EngineBenchmarkProfile


def test_success_rate_none_when_no_executions() -> None:
    profile = EngineBenchmarkProfile(
        engine_name="claude",
        execution_count=0,
        success_count=0,
        failure_count=0,
        latency_sample_count=0,
        total_latency_seconds=0.0,
    )

    assert profile.success_rate() is None
    assert profile.failure_rate() is None


def test_success_rate_and_failure_rate_computed_from_execution_count() -> None:
    profile = EngineBenchmarkProfile(
        engine_name="claude",
        execution_count=4,
        success_count=3,
        failure_count=1,
        latency_sample_count=0,
        total_latency_seconds=0.0,
    )

    assert profile.success_rate() == 0.75
    assert profile.failure_rate() == 0.25


def test_average_latency_seconds_none_when_no_latency_samples() -> None:
    profile = EngineBenchmarkProfile(
        engine_name="claude",
        execution_count=2,
        success_count=2,
        failure_count=0,
        latency_sample_count=0,
        total_latency_seconds=0.0,
    )

    assert profile.average_latency_seconds() is None


def test_average_latency_seconds_averages_recorded_latency_samples() -> None:
    profile = EngineBenchmarkProfile(
        engine_name="claude",
        execution_count=2,
        success_count=2,
        failure_count=0,
        latency_sample_count=2,
        total_latency_seconds=3.0,
    )

    assert profile.average_latency_seconds() == 1.5
