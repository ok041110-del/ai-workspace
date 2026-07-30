from ai_workspace.domain.execution_memory import ExecutionMemory


def test_execution_memory_holds_given_fields() -> None:
    memory = ExecutionMemory(
        task_id="M36-T01",
        action="설계 문서 작성",
        result="success",
        timestamp="2026-07-30T00:00:00+00:00",
    )

    assert memory.task_id == "M36-T01"
    assert memory.action == "설계 문서 작성"
    assert memory.result == "success"
    assert memory.timestamp == "2026-07-30T00:00:00+00:00"
    assert memory.reason is None


def test_execution_memory_can_represent_failure_with_reason() -> None:
    memory = ExecutionMemory(
        task_id="M36-T02",
        action="배포",
        result="failure",
        timestamp="2026-07-30T00:00:00+00:00",
        reason="authentication required",
    )

    assert memory.result == "failure"
    assert memory.reason == "authentication required"
