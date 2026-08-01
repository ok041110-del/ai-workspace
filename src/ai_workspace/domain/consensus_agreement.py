from __future__ import annotations

from dataclasses import dataclass
from typing import Final

_MIN_SAMPLE_SIZE_FOR_RECOMMENDATION: Final[int] = 3


@dataclass(frozen=True)
class ConsensusAgreementStat:
    """엔진의 과거 Ensemble 투표가 최종 합의(다수 의견)와 일치했는지를
    누적하는 값 객체(Milestone 70, ADR-0088).

    M69의 `EngineExecutionMemoryStat`은 "태스크 실행 자체의 성공/실패"를
    추적하지만, 이 값 객체는 "엔진의 투표가 Ensemble 합의에서 다수 의견에
    속했는지"만 추적한다 — 실행은 성공했지만 소수 의견(dissenting)이었을
    수도 있으므로 서로 다른 신호다. 그래서 `(required_capabilities,
    engine_name)` 키는 `EngineExecutionMemoryStat`과 같은 형태를 재사용하되,
    별도의 도메인 값 객체로 분리한다(M65가 `ExperienceStat` 대신
    `EngineReliabilityStat`을 새로 만든 것과 같은 이유 — layering 분리)."""

    total: int = 0
    agree_count: int = 0
    disagree_count: int = 0

    def record(self, agreed: bool) -> ConsensusAgreementStat:
        return ConsensusAgreementStat(
            total=self.total + 1,
            agree_count=self.agree_count + (1 if agreed else 0),
            disagree_count=self.disagree_count + (0 if agreed else 1),
        )

    def agreement_rate(self) -> float | None:
        if self.total < _MIN_SAMPLE_SIZE_FOR_RECOMMENDATION:
            return None
        return self.agree_count / self.total
