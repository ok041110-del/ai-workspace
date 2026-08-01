from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ai_workspace.interfaces.engine_adapter import EngineResult


@dataclass(frozen=True)
class AggregatedResult:
    output: str
    success: bool
    agreeing_engines: tuple[str, ...]
    dissenting_engines: tuple[str, ...]
    failed_engines: tuple[str, ...]
    agreement_ratio: float


class ResultAggregator(ABC):
    """`EngineRuntime.run_ensemble()`(Milestone 62)이 반환한
    `dict[str, EngineResult]`를 입력받아 다수결로 대표 결과 하나를 고르는
    계약(Milestone 63, ADR-0081). ADR-0080에서 "결과를 투표/합치는 로직은
    포함하지 않는다(YAGNI) — 호출자가 직접 비교·선택한다"고 명시했던 부분을
    이 인터페이스로 구현한다.

    이 인터페이스는 `EngineResult.output`의 **정확한 문자열 일치**만
    비교한다 — 의미(semantic) 비교나 LLM 기반 심사는 하지 않는다.
    `EngineRuntime`/`run_ensemble()`은 이 인터페이스의 존재를 알지 못한다 —
    호출자가 `run_ensemble()`의 반환값을 이 인터페이스에 넘기는 별도
    단계로만 사용된다(자동으로 연결되지 않는다)."""

    @abstractmethod
    def aggregate(self, results: dict[str, EngineResult]) -> AggregatedResult:
        """
        입력: results (`run_ensemble()`이 반환한, 엔진 이름을 key로 하는
              EngineResult dict)
        출력: AggregatedResult
              - output: 다수결로 선택된 대표 출력(동점이면 results의 순회
                순서상 가장 먼저 그 출력을 낸 엔진의 출력)
              - success: 성공한(success=True) 결과가 하나 이상 있으면 True
              - agreeing_engines: 선택된 output과 정확히 같은 출력을 낸,
                성공한 엔진 이름들(입력 순서 유지)
              - dissenting_engines: 성공했지만 선택된 output과 다른 출력을
                낸 엔진 이름들(입력 순서 유지)
              - failed_engines: success=False였던 엔진 이름들(입력 순서 유지)
              - agreement_ratio: len(agreeing_engines) / len(results).
                results가 비어 있으면 0.0
        예외: 없음
        보장: results가 비어 있거나 성공한 결과가 하나도 없으면
              AggregatedResult(output="", success=False, agreeing_engines=(),
              dissenting_engines=(), failed_engines=<전체 실패 이름들>,
              agreement_ratio=0.0)을 반환한다 — 예외를 던지지 않는다.
        """
        raise NotImplementedError
