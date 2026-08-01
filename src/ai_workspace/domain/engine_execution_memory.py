from __future__ import annotations

from dataclasses import dataclass
from typing import Final

_MIN_SAMPLE_SIZE_FOR_RECOMMENDATION: Final[int] = 3


@dataclass(frozen=True)
class EngineExecutionMemoryStat:
    """Milestone 69(Execution Memory & Context Routing, ADR-0087)가 "같은
    종류의 Task"(`required_capabilities` 조합)에서 어떤 Engine이 실제로
    더 잘 수행했는지 기억하는 최소 단위. `domain.engine_reliability.
    EngineReliabilityStat`(M65)과 필드 구성은 같지만 집계 키가 다르다 —
    `EngineReliabilityStat`은 엔진 이름 단독 키(모든 Task를 통틀은 전반적
    신뢰도)인 반면, 이 타입은 `(required_capabilities, engine_name)` 조합
    키로 "같은 종류의 Task에서만" 비교한다. `domain.execution_memory.
    ExecutionMemory`(M39)와도 이름이 비슷하지만 완전히 별개 타입이다 —
    M39는 Recommendation Execution Platform 전용 범용 기록(action/result/
    reason, `MemoryEngine`에 영속)이고, 이 타입은 `EngineRuntime` 전용
    in-process 통계(latency 포함)다(ARCHITECTURE.md §8 규칙 14가 두 경로를
    이미 완전히 분리해 뒀다 — 이 타입은 그 경계를 그대로 유지한다).

    `latency_seconds`는 기록만 한다 — 추천 랭킹(`success_rate()`)에는
    반영하지 않는다(YAGNI, 새 가중치 공식을 설계하지 않는다)."""

    total: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_latency_seconds: float = 0.0

    def record(self, success: bool, latency_seconds: float) -> EngineExecutionMemoryStat:
        return EngineExecutionMemoryStat(
            total=self.total + 1,
            success_count=self.success_count + (1 if success else 0),
            failure_count=self.failure_count + (0 if success else 1),
            total_latency_seconds=self.total_latency_seconds + latency_seconds,
        )

    def success_rate(self) -> float | None:
        """표본이 `_MIN_SAMPLE_SIZE_FOR_RECOMMENDATION`(M49/M65와 동일한
        "3건") 미만이면 `None`(추천 근거로 쓰기엔 성급함)을 반환한다."""
        if self.total < _MIN_SAMPLE_SIZE_FOR_RECOMMENDATION:
            return None
        return self.success_count / self.total

    def average_latency_seconds(self) -> float | None:
        if self.total == 0:
            return None
        return self.total_latency_seconds / self.total
