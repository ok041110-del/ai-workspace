import pytest

from ai_workspace.domain.retry_policy import InvalidRetryPolicyError, RetryPolicy


class _AuthError(Exception):
    pass


class _TransientError(Exception):
    pass


def test_default_max_attempts_is_three() -> None:
    assert RetryPolicy().max_attempts == 3


def test_max_attempts_below_one_raises_error() -> None:
    with pytest.raises(InvalidRetryPolicyError):
        RetryPolicy(max_attempts=0)


def test_default_has_no_delay_and_no_non_retryable_exceptions() -> None:
    policy = RetryPolicy()

    assert policy.retry_delay_seconds == 0.0
    assert policy.non_retryable_exceptions == ()


def test_decide_allows_retry_for_unknown_exception() -> None:
    policy = RetryPolicy()

    decision = policy.decide(_TransientError("boom"))

    assert decision.should_retry is True


def test_decide_denies_retry_for_configured_exception_type() -> None:
    policy = RetryPolicy(non_retryable_exceptions=(_AuthError,))

    decision = policy.decide(_AuthError("no auth"))

    assert decision.should_retry is False
    assert "_AuthError" in decision.reason


def test_decide_allows_retry_for_exception_not_in_non_retryable_list() -> None:
    policy = RetryPolicy(non_retryable_exceptions=(_AuthError,))

    decision = policy.decide(_TransientError("boom"))

    assert decision.should_retry is True
