import asyncio
from datetime import datetime

from ai_workspace.domain.automation import Action, ActionKind, Trigger, TriggerKind
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.automation.automation_repository import InMemoryAutomationRepository
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.execution.events import (
    ENGINE_EXECUTION_COMPLETED,
    ENGINE_EXECUTION_STARTED,
)
from ai_workspace.runtime.production.lifecycle import LifecycleManager, LifecycleState


def make_scheduler() -> tuple[AutomationScheduler, InMemoryAutomationRepository, list]:
    repository = InMemoryAutomationRepository()
    fired: list = []
    scheduler = AutomationScheduler(automation_repository=repository, action_executor=fired.append)
    return scheduler, repository, fired


def make_dashboard_service(event_bus: InMemoryEventBus) -> DashboardService:
    repository = InMemoryDashboardRepository(event_bus=event_bus)
    return DashboardService(dashboard_repository=repository)


def test_initial_state_is_startup() -> None:
    manager = LifecycleManager()

    assert manager.state == LifecycleState.STARTUP
    assert manager.started_at is None


def test_startup_transitions_to_running_and_records_started_at() -> None:
    manager = LifecycleManager()

    manager.startup(now=datetime(2026, 7, 27, 9, 0))

    assert manager.state == LifecycleState.RUNNING
    assert manager.started_at == datetime(2026, 7, 27, 9, 0).isoformat()


def test_startup_fires_automation_startup_trigger() -> None:
    scheduler, repository, fired = make_scheduler()
    from ai_workspace.domain.automation import AutomationRule

    repository.save(
        AutomationRule(
            rule_id="r1",
            name="시작 시 실행",
            description="설명",
            trigger=Trigger(kind=TriggerKind.STARTUP),
            action=Action(kind=ActionKind.DASHBOARD_REFRESH),
            created_at="2026-07-27T00:00:00",
            updated_at="2026-07-27T00:00:00",
        )
    )
    manager = LifecycleManager(automation_scheduler=scheduler)

    manager.startup(now=datetime(2026, 7, 27, 9, 0))

    assert len(fired) == 1


def test_shutdown_transitions_state() -> None:
    manager = LifecycleManager()
    manager.startup()

    asyncio.run(manager.shutdown())

    assert manager.state == LifecycleState.SHUTDOWN


def test_shutdown_returns_immediately_without_dashboard_service() -> None:
    manager = LifecycleManager()
    manager.startup()

    asyncio.run(manager.shutdown())  # should not hang

    assert manager.state == LifecycleState.SHUTDOWN


def test_shutdown_waits_while_workspace_is_running_then_completes() -> None:
    event_bus = InMemoryEventBus()
    dashboard_service = make_dashboard_service(event_bus)
    manager = LifecycleManager(
        dashboard_service=dashboard_service,
        graceful_shutdown_timeout_seconds=2.0,
        graceful_shutdown_poll_interval_seconds=0.05,
    )
    manager.startup()

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=ENGINE_EXECUTION_STARTED,
            payload={"engine": "claude_code", "task_title": "작업", "started_at": "t0"},
        )
    )
    assert dashboard_service.workspace_status().status == "running"

    async def _shutdown_then_complete() -> None:
        shutdown_task = asyncio.create_task(manager.shutdown())
        await asyncio.sleep(0.15)
        event_bus.publish(
            Event(
                event_id="e2",
                event_type=ENGINE_EXECUTION_COMPLETED,
                payload={
                    "completed_at": "t1",
                    "engine": "claude_code",
                    "success": True,
                    "cancelled": False,
                    "timed_out": False,
                    "retry_count": 0,
                    "error": None,
                },
            )
        )
        await shutdown_task

    asyncio.run(_shutdown_then_complete())

    assert manager.state == LifecycleState.SHUTDOWN
    assert dashboard_service.workspace_status().status == "idle"


def test_shutdown_gives_up_after_timeout_without_forcing() -> None:
    event_bus = InMemoryEventBus()
    dashboard_service = make_dashboard_service(event_bus)
    manager = LifecycleManager(
        dashboard_service=dashboard_service,
        graceful_shutdown_timeout_seconds=0.1,
        graceful_shutdown_poll_interval_seconds=0.02,
    )
    manager.startup()

    event_bus.publish(
        Event(
            event_id="e1",
            event_type=ENGINE_EXECUTION_STARTED,
            payload={"engine": "claude_code", "task_title": "작업", "started_at": "t0"},
        )
    )

    asyncio.run(manager.shutdown())

    assert manager.state == LifecycleState.SHUTDOWN
    assert dashboard_service.workspace_status().status == "running"
