from __future__ import annotations

from dataclasses import dataclass
from typing import Final

_MIN_SAMPLE_SIZE_FOR_EXCLUSION: Final[int] = 3


@dataclass(frozen=True)
class LLMPolicyReliabilityStat:
    """`(AgentRole, LLMModel)` 조합 하나에 대한 `LLMPolicyEngine`의
    in-process 누적 실행 결과(Milestone 67, ADR-0085).
    `domain/engine_reliability.py`의 `EngineReliabilityStat`(Milestone 65)
    과 필드 구성(total/success_count/failure_count)과 임계값 규칙을
    그대로 재사용한다 — "엔진 이름"이 아니라 "Role+Model 조합" 단위로
    같은 개념(누적 성공/실패 카운트)을 추적할 뿐이다. `skip_count`/
    Probe(Milestone 66)는 이번 범위에서 명시적으로 제외한다(ADR-0084가
    별도 Milestone 후보로 남긴 "LLMPolicyEngine Self Optimizer" 범위를
    사용자가 "관측 + 자동 대체"로 좁혔다 — 자동 복구는 범위 밖).

    서버 프로세스가 살아있는 동안에만 유지된다(M49/M50/M65와 동일하게
    영속화는 이번 범위 밖, YAGNI)."""

    total: int = 0
    success_count: int = 0
    failure_count: int = 0

    def record(self, success: bool) -> LLMPolicyReliabilityStat:
        return LLMPolicyReliabilityStat(
            total=self.total + 1,
            success_count=self.success_count + (1 if success else 0),
            failure_count=self.failure_count + (0 if success else 1),
        )

    def is_unreliable(self) -> bool:
        """M49(ADR-0066)/M65(ADR-0083)와 동일한 임계값 규칙
        (`success_count == 0 and total >= 3`)을 재사용한다 — 실패
        1~2건만으로 성급하게 대체하지 않고, 성공이 단 한 번도 없이
        3건 이상 쌓였을 때만 "신뢰할 수 없음"으로 판정한다."""
        return self.success_count == 0 and self.total >= _MIN_SAMPLE_SIZE_FOR_EXCLUSION
