import pytest

from ai_workspace.domain.retry_policy import RetryPolicy
from ai_workspace.runtime.execution.retry_executor import RetryExecutor


class _NonRetryableError(Exception):
    pass


def test_execute_returns_result_on_first_success() -> None:
    executor = RetryExecutor(retry_policy=RetryPolicy(max_attempts=3))
    calls = []

    def attempt() -> str:
        calls.append(1)
        return "ok"

    result = executor.execute(attempt)

    assert result == "ok"
    assert len(calls) == 1


def test_execute_retries_until_success() -> None:
    """M19 DoD 9번: Retry 횟수가 정책대로 동작함을 증명한다."""
    executor = RetryExecutor(retry_policy=RetryPolicy(max_attempts=3))
    calls = []

    def attempt() -> str:
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("transient")
        return "ok"

    result = executor.execute(attempt)

    assert result == "ok"
    assert len(calls) == 3


def test_execute_stops_at_max_attempts_and_reraises_last_exception() -> None:
    executor = RetryExecutor(retry_policy=RetryPolicy(max_attempts=3))
    calls = []

    def attempt() -> str:
        calls.append(1)
        raise RuntimeError(f"failure {len(calls)}")

    with pytest.raises(RuntimeError, match="failure 3"):
        executor.execute(attempt)

    assert len(calls) == 3


def test_execute_does_not_retry_non_retryable_exception() -> None:
    """M19 DoD 6/7/8번: 재시도 불가 오류는 첫 시도에서 즉시 실패한다."""
    executor = RetryExecutor(
        retry_policy=RetryPolicy(max_attempts=5, non_retryable_exceptions=(_NonRetryableError,))
    )
    calls = []

    def attempt() -> str:
        calls.append(1)
        raise _NonRetryableError("no retry")

    with pytest.raises(_NonRetryableError):
        executor.execute(attempt)

    assert len(calls) == 1


def test_execute_applies_delay_between_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr(
        "ai_workspace.runtime.execution.retry_executor.time.sleep", sleeps.append
    )
    executor = RetryExecutor(retry_policy=RetryPolicy(max_attempts=3, retry_delay_seconds=0.5))
    calls = []

    def attempt() -> str:
        calls.append(1)
        if len(calls) < 2:
            raise RuntimeError("transient")
        return "ok"

    executor.execute(attempt)

    assert sleeps == [0.5]
