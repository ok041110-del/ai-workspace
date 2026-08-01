from __future__ import annotations

from dataclasses import dataclass
from typing import Final

_MIN_SAMPLE_SIZE_FOR_EXCLUSION: Final[int] = 3
_PROBE_INTERVAL: Final[int] = 5


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
    범위로 한정"과 동일한 판단 — 영속화는 이번 범위 밖).

    `skip_count`(Milestone 66, ADR-0084)는 `is_unreliable()`이 참인 채로
    후보에서 제외된 횟수를 센다 — M65는 한번 제외되면 영구히 후보에서
    빠지는 공백이 있었다(성공이 없으면 total만 계속 늘어 success_count는
    0에 머무르므로 다시 선택될 길이 없었다). `_PROBE_INTERVAL`번 연속으로
    제외되면 `is_probe_eligible()`이 참이 되어 다음 선택에서 한 번 더
    후보로 포함된다 — 실제로 실행되어 `record()`가 호출되면 성공 여부와
    무관하게 `skip_count`는 0으로 초기화된다(다음 탐색까지 다시 카운트)."""

    total: int = 0
    success_count: int = 0
    failure_count: int = 0
    skip_count: int = 0

    def record(self, success: bool) -> EngineReliabilityStat:
        return EngineReliabilityStat(
            total=self.total + 1,
            success_count=self.success_count + (1 if success else 0),
            failure_count=self.failure_count + (0 if success else 1),
            skip_count=0,
        )

    def skip(self) -> EngineReliabilityStat:
        """`is_unreliable()`인 채로 후보에서 제외될 때마다 호출된다."""
        return EngineReliabilityStat(
            total=self.total,
            success_count=self.success_count,
            failure_count=self.failure_count,
            skip_count=self.skip_count + 1,
        )

    def is_unreliable(self) -> bool:
        """M49(ADR-0066)의 Recommendation Adaptation 임계값 규칙(`success_count
        == 0 and total >= 3`)을 엔진 신뢰도에도 그대로 재사용한다 — 실패
        1~2건만으로 성급하게 제외하지 않고, 성공이 단 한 번도 없이 3건
        이상 쌓였을 때만 "신뢰할 수 없음"으로 판정한다."""
        return self.success_count == 0 and self.total >= _MIN_SAMPLE_SIZE_FOR_EXCLUSION

    def is_probe_eligible(self) -> bool:
        """`_PROBE_INTERVAL`번 연속 제외됐다면 다음 선택에서 다시 후보로
        포함해 "탐색(probe)" 기회를 준다(Milestone 66, ADR-0084)."""
        return self.skip_count >= _PROBE_INTERVAL
