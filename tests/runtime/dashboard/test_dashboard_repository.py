from ai_workspace.domain.dashboard import EngineStatus
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.execution.events import (
    ENGINE_AUTHENTICATION_FAILED,
    ENGINE_EXECUTION_COMPLETED,
    ENGINE_EXECUTION_STARTED,
)


def test_started_event_updates_workspace_and_engine_status() -> None:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=ENGINE_EXECUTION_STARTED,
            payload={
                "engine": "claude_code",
                "task_title": "구현하기",
                "started_at": "2026-07-27T10:00:00Z",
            },
        )
    )

    status = repository.workspace_status()
    assert status.current_task_title == "구현하기"
    assert status.started_at == "2026-07-27T10:00:00Z"
    assert repository.engine_statuses()["claude_code"] == EngineStatus.RUNNING


def test_completed_event_updates_stats_and_history() -> None:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=ENGINE_EXECUTION_COMPLETED,
            payload={
                "engine": "claude_code",
                "success": True,
                "cancelled": False,
                "timed_out": False,
                "retry_count": 2,
                "error": None,
                "completed_at": "2026-07-27T10:05:00Z",
            },
        )
    )

    assert repository.engine_statuses()["claude_code"] == EngineStatus.READY
    assert repository.workspace_status().started_at is None
    assert len(repository.recent_executions()) == 1
    stats = repository.execution_stats()
    assert stats.total == 1
    assert stats.success == 1
    reliability = repository.reliability_stats()
    assert reliability.retry_count == 2


def test_authentication_failed_event_updates_engine_status_and_stats() -> None:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=ENGINE_AUTHENTICATION_FAILED,
            payload={"engine": "claude_code"},
        )
    )

    assert repository.engine_statuses()["claude_code"] == EngineStatus.AUTH_REQUIRED
    assert repository.reliability_stats().authentication_failure_count == 1


def test_failed_execution_marks_engine_error_and_updates_failure_stats() -> None:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=ENGINE_EXECUTION_COMPLETED,
            payload={
                "engine": "claude_code",
                "success": False,
                "cancelled": False,
                "timed_out": True,
                "retry_count": 3,
                "error": "timeout",
                "completed_at": "2026-07-27T10:05:00Z",
            },
        )
    )

    assert repository.engine_statuses()["claude_code"] == EngineStatus.ERROR
    stats = repository.execution_stats()
    assert stats.timed_out == 1
    assert stats.failure == 0  # timed_out으로 분류되므로 failure는 아님
    reliability = repository.reliability_stats()
    assert reliability.timeout_count == 1


def test_recent_executions_are_ordered_newest_first() -> None:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)

    for i in range(3):
        event_bus.publish(
            Event(
                event_id=f"e{i}",
                event_type=ENGINE_EXECUTION_COMPLETED,
                payload={
                    "engine": "claude_code",
                    "success": True,
                    "cancelled": False,
                    "timed_out": False,
                    "retry_count": 0,
                    "error": None,
                    "completed_at": f"2026-07-27T10:0{i}:00Z",
                },
            )
        )

    history = repository.recent_executions()
    assert [record.executed_at for record in history] == [
        "2026-07-27T10:02:00Z",
        "2026-07-27T10:01:00Z",
        "2026-07-27T10:00:00Z",
    ]


def test_unrelated_events_are_ignored() -> None:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)

    event_bus.publish(Event(event_id="e1", event_type="mission_planned", payload={}))

    assert repository.recent_executions() == []
    assert repository.engine_statuses() == {}
