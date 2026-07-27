from ai_workspace.domain.execution_result import EngineExecutionResult


def test_engine_execution_result_holds_given_fields() -> None:
    result = EngineExecutionResult(
        success=True,
        output="완료",
        error=None,
        engine="claude_code",
        execution_time=1.5,
    )

    assert result.success is True
    assert result.output == "완료"
    assert result.error is None
    assert result.engine == "claude_code"
    assert result.execution_time == 1.5


def test_engine_execution_result_can_represent_failure() -> None:
    result = EngineExecutionResult(
        success=False, output="", error="authentication required", engine=None, execution_time=0.0
    )

    assert result.success is False
    assert result.error == "authentication required"
    assert result.engine is None
