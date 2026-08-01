from __future__ import annotations

from dataclasses import dataclass
from typing import Final

_MIN_SAMPLE_SIZE_FOR_EXCLUSION: Final[int] = 3


@dataclass(frozen=True)
class EngineReliabilityStat:
    """엔진 이름 하나에 대한 `EngineRuntime`의 in-process 누적 실행
    결과(Milestone 65, ADR-0083). `intelligence/experience_rules.py`의
    `ExperienceStat`(task_id별 집계)와 같은 필드 구성(total/
    success_count/failure_count)을 의도적으로 재사용한다 — 계층만
    다를 뿐(이쪽은 domain, `EngineRuntime`이 직접 갱신) 같은 "누적
    성공/실패 카운트" 개념이기 때문이다. `intelligence/` 계층에
    의존하지 않기 위해 별도 타입으로 둔다(`runtime/engine/`이
    `intelligence/`를 참조하면 계층 위반).

    서버 프로세스가 살아있는 동안에만 유지된다(M49/M50의 "in-process
    범위로 한정"과 동일한 판단 — 영속화는 이번 범위 밖)."""

    total: int = 0
    success_count: int = 0
    failure_count: int = 0

    def record(self, success: bool) -> EngineReliabilityStat:
        return EngineReliabilityStat(
            total=self.total + 1,
            success_count=self.success_count + (1 if success else 0),
            failure_count=self.failure_count + (0 if success else 1),
        )

    def is_unreliable(self) -> bool:
        """M49(ADR-0066)의 Recommendation Adaptation 임계값 규칙(`success_count
        == 0 and total >= 3`)을 엔진 신뢰도에도 그대로 재사용한다 — 실패
        1~2건만으로 성급하게 제외하지 않고, 성공이 단 한 번도 없이 3건
        이상 쌓였을 때만 "신뢰할 수 없음"으로 판정한다."""
        return self.success_count == 0 and self.total >= _MIN_SAMPLE_SIZE_FOR_EXCLUSION
