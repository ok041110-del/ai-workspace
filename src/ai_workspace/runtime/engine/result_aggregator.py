from __future__ import annotations

from ai_workspace.interfaces.engine_adapter import EngineResult
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
