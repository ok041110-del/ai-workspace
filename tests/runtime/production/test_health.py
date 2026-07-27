from datetime import datetime

from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.runtime.automation.automation_repository import InMemoryAutomationRepository
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.production.health import HealthMonitor, HealthStatus
from ai_workspace.runtime.production.lifecycle import LifecycleManager
from ai_workspace.runtime.production.version import WORKSPACE_VERSION


def test_status_before_startup_reports_degraded_server() -> None:
    monitor = HealthMonitor(lifecycle_manager=LifecycleManager())

    status = monitor.status(now=datetime(2026, 7, 27, 9, 0))

    server = next(c for c in status.components if c.name == "server")
    assert server.status == HealthStatus.DEGRADED
    assert status.started_at is None
    assert status.uptime_seconds is None


def test_status_after_startup_with_no_components_wired_is_unhealthy() -> None:
    lifecycle = LifecycleManager()
    lifecycle.startup(now=datetime(2026, 7, 27, 9, 0))
    monitor = HealthMonitor(lifecycle_manager=lifecycle)

    status = monitor.status(now=datetime(2026, 7, 27, 9, 5))

    assert status.health_status == HealthStatus.UNHEALTHY
    assert status.version == WORKSPACE_VERSION
    assert status.started_at == datetime(2026, 7, 27, 9, 0).isoformat()
    assert status.uptime_seconds == 300.0


def test_status_healthy_when_all_components_wired() -> None:
    event_bus = InMemoryEventBus()
    lifecycle = LifecycleManager()
    lifecycle.startup(now=datetime(2026, 7, 27, 9, 0))
    dashboard_service = DashboardService(
        dashboard_repository=InMemoryDashboardRepository(event_bus=event_bus)
    )
    automation_scheduler = AutomationScheduler(
        automation_repository=InMemoryAutomationRepository(), action_executor=lambda rule: None
    )
    monitor = HealthMonitor(
        lifecycle_manager=lifecycle,
        dashboard_service=dashboard_service,
        automation_scheduler=automation_scheduler,
        event_bus=event_bus,
        engine_registry=InMemoryEngineRegistry(),
    )

    status = monitor.status(now=datetime(2026, 7, 27, 9, 1))

    assert status.health_status == HealthStatus.HEALTHY
    assert {c.name for c in status.components} == {
        "server",
        "dashboard",
        "automation",
        "event_bus",
        "engine",
    }
    assert all(c.status == HealthStatus.HEALTHY for c in status.components)


def test_overall_health_status_is_the_worst_component() -> None:
    lifecycle = LifecycleManager()
    lifecycle.startup(now=datetime(2026, 7, 27, 9, 0))
    monitor = HealthMonitor(lifecycle_manager=lifecycle, event_bus=InMemoryEventBus())

    status = monitor.status(now=datetime(2026, 7, 27, 9, 1))

    assert status.health_status == HealthStatus.UNHEALTHY  # dashboard/automation/engine unwired


def test_status_reflects_shutdown_state() -> None:
    import asyncio

    lifecycle = LifecycleManager()
    lifecycle.startup()
    asyncio.run(lifecycle.shutdown())
    monitor = HealthMonitor(lifecycle_manager=lifecycle)

    status = monitor.status()

    server = next(c for c in status.components if c.name == "server")
    assert server.status == HealthStatus.UNHEALTHY
