from ai_workspace.observability.claude_runtime_analyzer import ClaudeRuntimeAnalyzer

_FULL_PAYLOAD = {
    "model": {"id": "claude-sonnet-5", "display_name": "Sonnet 5"},
    "effort": {"level": "high"},
    "context_window": {
        "total_input_tokens": 137000,
        "total_output_tokens": 1200,
        "context_window_size": 200000,
        "used_percentage": 68.5,
    },
}


def test_analyze_reads_documented_fields() -> None:
    info = ClaudeRuntimeAnalyzer().analyze(_FULL_PAYLOAD)

    assert info.model_display_name == "Sonnet 5"
    assert info.effort_level == "high"
    assert info.context_used_tokens == 137000
    assert info.context_total_tokens == 200000
    assert info.context_used_percentage == 68.5
    assert info.input_tokens == 137000
    assert info.output_tokens == 1200


def test_analyze_leaves_missing_fields_as_none_without_guessing() -> None:
    info = ClaudeRuntimeAnalyzer().analyze({"model": {"display_name": "Sonnet 5"}})

    assert info.model_display_name == "Sonnet 5"
    assert info.effort_level is None
    assert info.context_used_tokens is None
    assert info.context_total_tokens is None
    assert info.context_used_percentage is None


def test_analyze_handles_empty_payload() -> None:
    info = ClaudeRuntimeAnalyzer().analyze({})

    assert info.model_display_name is None
    assert info.effort_level is None
