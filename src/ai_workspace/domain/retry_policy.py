from __future__ import annotations

from dataclasses import dataclass, field


class InvalidRetryPolicyError(ValueError):
    pass


@dataclass(frozen=True)
class RetryDecision:
    """`RetryPolicy.decide()`의 결과(M19-T01). `allow`가 아니라
    `should_retry`인 이유: 이미 사용 중인 `EngineSelectionDecision`/
    `BudgetDecision`과 이름 패턴을 맞추기 위함."""

    should_retry: bool
    reason: str


@dataclass(frozen=True)
class RetryPolicy:
    """실행 재시도 정책(M3, M10-T03에서 `RecoveringEngineRuntime`이
    "무조건 재시도"로 처음 사용). M19-T01에서 `retry_delay_seconds`/
    `non_retryable_exceptions`을 추가해 확장했다 — 둘 다 기본값이
    있어 기존 `RecoveringEngineRuntime` 호출부(모두 `max_attempts`만
    지정)는 전혀 영향받지 않는다. `non_retryable_exceptions`은 도메인
    계층이 특정 구체 예외 타입을 알 필요가 없도록 `type[BaseException]`
    튜플만 받는다 — 실제로 어떤 예외가 재시도 불가인지는 이 정책을
    구성하는 호출자(예: `ExecutionDispatcher`)가 결정한다."""

    max_attempts: int = 3
    retry_delay_seconds: float = 0.0
    non_retryable_exceptions: tuple[type[BaseException], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise InvalidRetryPolicyError(
                f"max_attempts는 1 이상이어야 합니다: {self.max_attempts}"
            )

    def decide(self, exception: BaseException) -> RetryDecision:
        """
        입력: exception (실행 중 발생한 예외)
        출력: RetryDecision(should_retry, reason) — side-effect 없음,
              시도 횟수를 스스로 추적하지 않는다(호출자인
              `RetryExecutor`가 시도 횟수와 `max_attempts`를 비교한다)
        """
        if isinstance(exception, self.non_retryable_exceptions):
            return RetryDecision(
                should_retry=False,
                reason=f"{type(exception).__name__}은(는) 재시도 불가 목록에 있음",
            )
        return RetryDecision(should_retry=True, reason="재시도 가능한 예외")
