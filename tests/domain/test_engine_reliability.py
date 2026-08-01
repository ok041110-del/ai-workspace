from ai_workspace.domain.engine_reliability import EngineReliabilityStat


def test_record_success_increments_total_and_success_count() -> None:
    stat = EngineReliabilityStat().record(True)

    assert stat == EngineReliabilityStat(total=1, success_count=1, failure_count=0)


def test_record_failure_increments_total_and_failure_count() -> None:
    stat = EngineReliabilityStat().record(False)

    assert stat == EngineReliabilityStat(total=1, success_count=0, failure_count=1)


def test_is_unreliable_false_when_no_records() -> None:
    assert EngineReliabilityStat().is_unreliable() is False


def test_is_unreliable_false_when_sample_size_insufficient() -> None:
    stat = EngineReliabilityStat()
    for _ in range(2):
        stat = stat.record(False)

    assert stat.is_unreliable() is False


def test_is_unreliable_true_when_all_failed_with_sufficient_sample() -> None:
    stat = EngineReliabilityStat()
    for _ in range(3):
        stat = stat.record(False)

    assert stat.is_unreliable() is True


def test_is_unreliable_false_when_at_least_one_success() -> None:
    stat = EngineReliabilityStat()
    stat = stat.record(True)
    for _ in range(5):
        stat = stat.record(False)

    assert stat.is_unreliable() is False


def test_is_probe_eligible_false_before_probe_interval_reached() -> None:
    stat = EngineReliabilityStat()
    for _ in range(4):
        stat = stat.skip()

    assert stat.is_probe_eligible() is False


def test_is_probe_eligible_true_once_probe_interval_reached() -> None:
    stat = EngineReliabilityStat()
    for _ in range(5):
        stat = stat.skip()

    assert stat.is_probe_eligible() is True


def test_skip_does_not_affect_reliability_counts() -> None:
    stat = EngineReliabilityStat(total=3, success_count=0, failure_count=3)

    stat = stat.skip()

    assert stat == EngineReliabilityStat(total=3, success_count=0, failure_count=3, skip_count=1)


def test_record_resets_skip_count() -> None:
    stat = EngineReliabilityStat()
    for _ in range(5):
        stat = stat.skip()

    stat = stat.record(False)

    assert stat.skip_count == 0
