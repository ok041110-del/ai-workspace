from ai_workspace.interfaces.engine_adapter import EngineResult
from ai_workspace.runtime.engine.result_aggregator import MajorityVoteAggregator


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
