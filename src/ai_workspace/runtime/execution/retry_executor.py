from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

from ai_workspace.domain.retry_policy import RetryPolicy

T = TypeVar("T")


class RetryExecutor:
    """`RetryPolicy`에 따라 실행을 반복하는 최소 구현체(M19-T01).
    `ExecutionDispatcher`는 재시도 로직을 직접 구현하지 않고 이
    클래스에 위임한다(Reliability는 Execution 위에서 동작한다, 사용자
    설계 원칙 1). `attempt`가 반환하는 값의 타입에 대해서는 알지
    못한다(`TypeVar`) — `ExecutionDispatcher`가 `EngineExecutionResult`
    를 반환하는 콜러블을 넘기지만, 이 클래스 자체는 그 사실을 모른다."""

    def __init__(self, *, retry_policy: RetryPolicy) -> None:
        self._retry_policy = retry_policy

    def execute(self, attempt: Callable[[], T]) -> T:
        last_exception: BaseException | None = None
        for attempt_number in range(1, self._retry_policy.max_attempts + 1):
            try:
                return attempt()
            except BaseException as exc:
                last_exception = exc
                decision = self._retry_policy.decide(exc)
                if not decision.should_retry:
                    raise
                if attempt_number == self._retry_policy.max_attempts:
                    raise
                if self._retry_policy.retry_delay_seconds > 0:
                    time.sleep(self._retry_policy.retry_delay_seconds)
        assert last_exception is not None
        raise last_exception
