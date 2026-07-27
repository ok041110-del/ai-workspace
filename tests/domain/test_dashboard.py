from ai_workspace.domain.dashboard import (
    EngineStatus,
    ExecutionRecord,
    ExecutionStats,
    ReliabilityStats,
    WorkspaceStatus,
)


def test_engine_status_covers_expected_states() -> None:
    assert {status.value for status in EngineStatus} == {
        "ready",
        "running",
        "auth_required",
        "error",
    }


def test_workspace_status_holds_given_fields() -> None:
    status = WorkspaceStatus(
        project_name="AI Workspace",
        current_task_title="로그인 기능 구현하기",
        status="running",
        started_at="2026-07-27T10:00:00Z",
    )

    assert status.project_name == "AI Workspace"
    assert status.current_task_title == "로그인 기능 구현하기"
    assert status.status == "running"
    assert status.started_at == "2026-07-27T10:00:00Z"


def test_workspace_status_allows_no_running_task() -> None:
    status = WorkspaceStatus(
        project_name=None, current_task_title=None, status="idle", started_at=None
    )

    assert status.started_at is None


def test_execution_record_holds_given_fields() -> None:
    record = ExecutionRecord(
        executed_at="2026-07-27T10:05:00Z",
        engine="claude_code",
        success=True,
        cancelled=False,
        timed_out=False,
        retry_count=1,
        error=None,
    )

    assert record.engine == "claude_code"
    assert record.success is True
    assert record.retry_count == 1


def test_execution_stats_holds_given_fields() -> None:
    stats = ExecutionStats(total=10, success=7, failure=1, cancelled=1, timed_out=1)

    assert stats.total == 10
    assert stats.success == 7
    assert stats.failure == 1
    assert stats.cancelled == 1
    assert stats.timed_out == 1


def test_reliability_stats_holds_given_fields() -> None:
    stats = ReliabilityStats(
        retry_count=5, timeout_count=2, cancelled_count=1, authentication_failure_count=3
    )

    assert stats.retry_count == 5
    assert stats.timeout_count == 2
    assert stats.cancelled_count == 1
    assert stats.authentication_failure_count == 3
