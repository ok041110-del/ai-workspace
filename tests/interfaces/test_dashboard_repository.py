from ai_workspace.domain.dashboard import EngineStatus, ExecutionRecord

from .fakes import FakeDashboardRepository


def test_record_execution_started_updates_workspace_status_and_engine_status() -> None:
    repository = FakeDashboardRepository()

    repository.record_execution_started(
        engine_name="claude_code", task_title="구현하기", started_at="2026-07-27T10:00:00Z"
    )

    status = repository.workspace_status()
    assert status.current_task_title == "구현하기"
    assert status.started_at == "2026-07-27T10:00:00Z"
    assert repository.engine_statuses()["claude_code"] == EngineStatus.RUNNING


def test_record_execution_completed_appends_to_recent_executions() -> None:
    repository = FakeDashboardRepository()
    record = ExecutionRecord(
        executed_at="2026-07-27T10:05:00Z",
        engine="claude_code",
        success=True,
        cancelled=False,
        timed_out=False,
        retry_count=0,
        error=None,
    )

    repository.record_execution_completed(record)

    assert repository.recent_executions() == [record]
    assert repository.engine_statuses()["claude_code"] == EngineStatus.READY
    assert repository.workspace_status().started_at is None


def test_record_authentication_failure_marks_engine_status() -> None:
    repository = FakeDashboardRepository()

    repository.record_authentication_failure(engine_name="claude_code")

    assert repository.engine_statuses()["claude_code"] == EngineStatus.AUTH_REQUIRED
    assert repository.reliability_stats().authentication_failure_count == 1


def test_execution_stats_reflect_recorded_executions() -> None:
    repository = FakeDashboardRepository()
    repository.record_execution_completed(
        ExecutionRecord("t1", "claude_code", True, False, False, 0, None)
    )
    repository.record_execution_completed(
        ExecutionRecord("t2", "claude_code", False, True, False, 0, "cancelled")
    )
    repository.record_execution_completed(
        ExecutionRecord("t3", "claude_code", False, False, True, 1, "timeout")
    )

    stats = repository.execution_stats()

    assert stats.total == 3
    assert stats.success == 1
    assert stats.cancelled == 1
    assert stats.timed_out == 1


def test_recent_executions_respects_limit() -> None:
    repository = FakeDashboardRepository()
    for i in range(5):
        repository.record_execution_completed(
            ExecutionRecord(f"t{i}", "claude_code", True, False, False, 0, None)
        )

    assert len(repository.recent_executions(limit=2)) == 2
