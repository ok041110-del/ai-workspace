from ai_workspace.domain.llm_policy_reliability import LLMPolicyReliabilityStat


def test_record_success_increments_total_and_success_count() -> None:
    stat = LLMPolicyReliabilityStat().record(True)

    assert stat == LLMPolicyReliabilityStat(total=1, success_count=1, failure_count=0)


def test_record_failure_increments_total_and_failure_count() -> None:
    stat = LLMPolicyReliabilityStat().record(False)

    assert stat == LLMPolicyReliabilityStat(total=1, success_count=0, failure_count=1)


def test_is_unreliable_false_when_no_records() -> None:
    assert LLMPolicyReliabilityStat().is_unreliable() is False


def test_is_unreliable_false_when_sample_size_insufficient() -> None:
    stat = LLMPolicyReliabilityStat()
    for _ in range(2):
        stat = stat.record(False)

    assert stat.is_unreliable() is False


def test_is_unreliable_true_when_all_failed_with_sufficient_sample() -> None:
    stat = LLMPolicyReliabilityStat()
    for _ in range(3):
        stat = stat.record(False)

    assert stat.is_unreliable() is True


def test_is_unreliable_false_when_at_least_one_success() -> None:
    stat = LLMPolicyReliabilityStat()
    stat = stat.record(True)
    for _ in range(5):
        stat = stat.record(False)

    assert stat.is_unreliable() is False
