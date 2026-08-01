from ai_workspace.interfaces.engine_adapter import EngineResult
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime
from ai_workspace.runtime.engine.result_aggregator import (
    AdaptiveConsensusAggregator,
    MajorityVoteAggregator,
)


def test_aggregate_picks_output_with_most_votes() -> None:
    aggregator = MajorityVoteAggregator()
    results = {
        "claude": EngineResult(success=True, output="42"),
        "codex": EngineResult(success=True, output="42"),
        "gemini": EngineResult(success=True, output="7"),
    }

    aggregated = aggregator.aggregate(results)

    assert aggregated.output == "42"
    assert aggregated.success is True
    assert aggregated.agreeing_engines == ("claude", "codex")
    assert aggregated.dissenting_engines == ("gemini",)
    assert aggregated.failed_engines == ()
    assert aggregated.agreement_ratio == 2 / 3


def test_aggregate_breaks_tie_by_first_engine_in_input_order() -> None:
    aggregator = MajorityVoteAggregator()
    results = {
        "claude": EngineResult(success=True, output="A"),
        "codex": EngineResult(success=True, output="B"),
    }

    aggregated = aggregator.aggregate(results)

    assert aggregated.output == "A"
    assert aggregated.agreeing_engines == ("claude",)
    assert aggregated.dissenting_engines == ("codex",)


def test_aggregate_isolates_failed_engines_from_voting() -> None:
    aggregator = MajorityVoteAggregator()
    results = {
        "claude": EngineResult(success=True, output="ok"),
        "codex": EngineResult(success=False, output="", error="boom"),
    }

    aggregated = aggregator.aggregate(results)

    assert aggregated.output == "ok"
    assert aggregated.success is True
    assert aggregated.agreeing_engines == ("claude",)
    assert aggregated.failed_engines == ("codex",)
    assert aggregated.agreement_ratio == 1 / 2


def test_aggregate_all_failed_returns_unsuccessful_with_no_output() -> None:
    aggregator = MajorityVoteAggregator()
    results = {
        "claude": EngineResult(success=False, output="", error="boom"),
        "codex": EngineResult(success=False, output="", error="bang"),
    }

    aggregated = aggregator.aggregate(results)

    assert aggregated.output == ""
    assert aggregated.success is False
    assert aggregated.agreeing_engines == ()
    assert aggregated.dissenting_engines == ()
    assert aggregated.failed_engines == ("claude", "codex")
    assert aggregated.agreement_ratio == 0.0


def test_aggregate_empty_results_returns_unsuccessful_default() -> None:
    aggregator = MajorityVoteAggregator()

    aggregated = aggregator.aggregate({})

    assert aggregated.output == ""
    assert aggregated.success is False
    assert aggregated.agreeing_engines == ()
    assert aggregated.dissenting_engines == ()
    assert aggregated.failed_engines == ()
    assert aggregated.agreement_ratio == 0.0


def test_aggregate_unanimous_agreement_ratio_is_one() -> None:
    aggregator = MajorityVoteAggregator()
    results = {
        "claude": EngineResult(success=True, output="same"),
        "codex": EngineResult(success=True, output="same"),
        "gemini": EngineResult(success=True, output="same"),
    }

    aggregated = aggregator.aggregate(results)

    assert aggregated.agreement_ratio == 1.0
    assert aggregated.agreeing_engines == ("claude", "codex", "gemini")
    assert aggregated.dissenting_engines == ()


def test_adaptive_consensus_matches_majority_vote_when_no_history() -> None:
    runtime = InMemoryEngineRuntime()
    aggregator = AdaptiveConsensusAggregator(runtime, frozenset({"code"}))
    results = {
        "claude": EngineResult(success=True, output="42"),
        "codex": EngineResult(success=True, output="42"),
        "gemini": EngineResult(success=True, output="7"),
    }

    aggregated = aggregator.aggregate(results)

    assert aggregated.output == "42"
    assert aggregated.agreeing_engines == ("claude", "codex")
    assert aggregated.dissenting_engines == ("gemini",)
    assert aggregated.agreement_ratio == 2 / 3


def test_adaptive_consensus_prefers_proven_reliable_engine_over_bare_majority() -> None:
    """M70(ADR-0088): 표 개수는 적어도(1표), 과거 합의 일치율이 높은
    엔진의 표가, 표는 많지만(3표) 과거에 계속 소수 의견이었던 엔진들의
    표보다 우선한다."""
    runtime = InMemoryEngineRuntime()
    caps = frozenset({"code"})
    for _ in range(3):
        runtime.record_consensus_outcome(caps, ("good",), ())
    for _ in range(3):
        runtime.record_consensus_outcome(caps, (), ("bad1", "bad2", "bad3"))

    aggregator = AdaptiveConsensusAggregator(runtime, caps)
    results = {
        "good": EngineResult(success=True, output="A"),
        "bad1": EngineResult(success=True, output="B"),
        "bad2": EngineResult(success=True, output="B"),
        "bad3": EngineResult(success=True, output="B"),
    }

    aggregated = aggregator.aggregate(results)

    assert aggregated.output == "A"
    assert aggregated.agreeing_engines == ("good",)
    assert aggregated.dissenting_engines == ("bad1", "bad2", "bad3")


def test_adaptive_consensus_records_outcome_for_future_weighting() -> None:
    runtime = InMemoryEngineRuntime()
    caps = frozenset({"code"})
    aggregator = AdaptiveConsensusAggregator(runtime, caps)
    results = {
        "claude": EngineResult(success=True, output="ok"),
        "codex": EngineResult(success=True, output="different"),
    }

    for _ in range(3):
        aggregator.aggregate(results)

    assert runtime.consensus_weight(caps, "claude") == 1.0
    assert runtime.consensus_weight(caps, "codex") == 0.0


def test_adaptive_consensus_all_failed_does_not_record_outcome() -> None:
    runtime = InMemoryEngineRuntime()
    caps = frozenset({"code"})
    aggregator = AdaptiveConsensusAggregator(runtime, caps)
    results = {
        "claude": EngineResult(success=False, output="", error="boom"),
    }

    aggregated = aggregator.aggregate(results)

    assert aggregated.success is False
    assert runtime.consensus_weight(caps, "claude") == 0.5
