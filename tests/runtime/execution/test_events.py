from ai_workspace.runtime.execution.events import (
    ENGINE_AUTHENTICATION_FAILED,
    ENGINE_EXECUTION_COMPLETED,
    ENGINE_EXECUTION_STARTED,
)


def test_event_type_constants_are_distinct_strings() -> None:
    assert ENGINE_EXECUTION_STARTED == "engine_execution_started"
    assert ENGINE_EXECUTION_COMPLETED == "engine_execution_completed"
    assert ENGINE_AUTHENTICATION_FAILED == "engine_authentication_failed"
    all_types = {ENGINE_EXECUTION_STARTED, ENGINE_EXECUTION_COMPLETED, ENGINE_AUTHENTICATION_FAILED}
    assert len(all_types) == 3
