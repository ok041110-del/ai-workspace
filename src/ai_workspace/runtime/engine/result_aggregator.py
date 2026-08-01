from __future__ import annotations

from ai_workspace.interfaces.engine_adapter import EngineResult
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.result_aggregator import AggregatedResult, ResultAggregator


class MajorityVoteAggregator(ResultAggregator):
    """`EngineResult.output`의 정확한 문자열 일치로 다수결 투표하는 최소
    구현(Milestone 63, ADR-0081)."""

    def aggregate(self, results: dict[str, EngineResult]) -> AggregatedResult:
        failed_engines = tuple(
            name for name, result in results.items() if not result.success
        )
        successful = {
            name: result for name, result in results.items() if result.success
        }

        if not successful:
            return AggregatedResult(
                output="",
                success=False,
                agreeing_engines=(),
                dissenting_engines=(),
                failed_engines=failed_engines,
                agreement_ratio=0.0,
            )

        votes: dict[str, list[str]] = {}
        for name, result in successful.items():
            votes.setdefault(result.output, []).append(name)

        winning_output = max(
            votes,
            key=lambda output: len(votes[output]),
        )
        agreeing_engines = tuple(votes[winning_output])
        dissenting_engines = tuple(
            name for name in successful if name not in agreeing_engines
        )

        return AggregatedResult(
            output=winning_output,
            success=True,
            agreeing_engines=agreeing_engines,
            dissenting_engines=dissenting_engines,
            failed_engines=failed_engines,
            agreement_ratio=len(agreeing_engines) / len(results),
        )


class AdaptiveConsensusAggregator(ResultAggregator):
    """과거 Consensus 합의 이력(Milestone 70, ADR-0088)으로 가중치를 매겨
    투표하는 `ResultAggregator` 구현체. `MajorityVoteAggregator`(M63)가
    표 개수만 세는 것과 달리, 같은 `required_capabilities` 조합에서
    과거에 최종 합의와 자주 일치했던 엔진의 표를 더 무겁게 반영한다.

    `ResultAggregator.aggregate()`의 계약(시그니처·반환 타입·빈 입력/
    전원 실패 처리)은 전혀 바꾸지 않는다 — `EngineRuntime`에 이미
    Milestone 70에서 추가된 `consensus_weight()`(조회)/
    `record_consensus_outcome()`(기록) 두 메서드만 이 클래스 생성자로
    주입받아 사용한다. `MajorityVoteAggregator`를 포함한 기존
    `ResultAggregator` 구현체는 전혀 영향받지 않는다(100% 하위 호환)."""

    def __init__(
        self, engine_runtime: EngineRuntime, required_capabilities: frozenset[str] = frozenset()
    ) -> None:
        self._engine_runtime = engine_runtime
        self._required_capabilities = required_capabilities

    def aggregate(self, results: dict[str, EngineResult]) -> AggregatedResult:
        failed_engines = tuple(
            name for name, result in results.items() if not result.success
        )
        successful = {
            name: result for name, result in results.items() if result.success
        }

        if not successful:
            return AggregatedResult(
                output="",
                success=False,
                agreeing_engines=(),
                dissenting_engines=(),
                failed_engines=failed_engines,
                agreement_ratio=0.0,
            )

        votes: dict[str, list[str]] = {}
        for name, result in successful.items():
            votes.setdefault(result.output, []).append(name)

        weight_sums = {
            output: sum(
                self._engine_runtime.consensus_weight(self._required_capabilities, name)
                for name in names
            )
            for output, names in votes.items()
        }
        winning_output = max(
            votes,
            key=lambda output: (weight_sums[output], len(votes[output])),
        )
        agreeing_engines = tuple(votes[winning_output])
        dissenting_engines = tuple(
            name for name in successful if name not in agreeing_engines
        )

        self._engine_runtime.record_consensus_outcome(
            self._required_capabilities, agreeing_engines, dissenting_engines
        )

        return AggregatedResult(
            output=winning_output,
            success=True,
            agreeing_engines=agreeing_engines,
            dissenting_engines=dissenting_engines,
            failed_engines=failed_engines,
            agreement_ratio=len(agreeing_engines) / len(results),
        )
