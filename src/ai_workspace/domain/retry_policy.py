from __future__ import annotations

from dataclasses import dataclass


class InvalidRetryPolicyError(ValueError):
    pass


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise InvalidRetryPolicyError(
                f"max_attempts는 1 이상이어야 합니다: {self.max_attempts}"
            )
