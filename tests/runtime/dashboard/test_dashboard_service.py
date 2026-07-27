from ai_workspace.domain.automation import Action, ActionKind, Trigger, TriggerKind
from ai_workspace.domain.dashboard import EngineStatus
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.automation.automation_repository import InMemoryAutomationRepository
from ai_workspace.runtime.automation.automation_service import AutomationService
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import KNOWN_ENGINES, DashboardService
from ai_workspace.runtime.execution.events import ENGINE_EXECUTION_STARTED
from ai_workspace.runtime.production.health import HealthMonitor, HealthStatus
from ai_workspace.runtime.production.lifecycle import LifecycleManager


def _build_service() -> tuple[DashboardService, InMemoryEventBus]:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)
    return DashboardService(dashboard_repository=repository), event_bus


def test_engine_statuses_defaults_unknown_engines_to_ready() -> None:
    service, _event_bus = _build_service()

    statuses = service.engine_statuses()

    assert set(statuses.keys()) == set(KNOWN_ENGINES)
    assert all(status == EngineStatus.READY for status in statuses.values())


def test_engine_statuses_reflects_recorded_status() -> None:
    service, event_bus = _build_service()
    event_bus.publish(
        Event(
            event_id="e1",
            event_type=ENGINE_EXECUTION_STARTED,
            payload={"engine": "claude_code", "task_title": "구현하기", "started_at": "t"},
        )
    )

    statuses = service.engine_statuses()

    assert statuses["claude_code"] == EngineStatus.RUNNING
    assert statuses["gemini_cli"] == EngineStatus.READY


def test_snapshot_combines_all_five_areas() -> None:
    service, _event_bus = _build_service()

    snapshot = service.snapshot()

    assert snapshot.workspace_status is not None
    assert set(snapshot.engine_statuses.keys()) == set(KNOWN_ENGINES)
    assert snapshot.execution_stats.total == 0
    assert snapshot.recent_executions == []
    assert snapshot.reliability_stats.retry_count == 0


def test_automation_status_is_none_without_automation_service() -> None:
    service, _event_bus = _build_service()

    assert service.automation_status() is None


def test_production_status_is_none_without_health_monitor() -> None:
    service, _event_bus = _build_service()

    assert service.production_status() is None


def test_production_status_reflects_attached_health_monitor() -> None:
    service, _event_bus = _build_service()
    lifecycle_manager = LifecycleManager()
    lifecycle_manager.startup()
    health_monitor = HealthMonitor(lifecycle_manager=lifecycle_manager)

    service.attach_health_monitor(health_monitor)

    status = service.production_status()
    assert status is not None
    server = next(c for c in status.components if c.name == "server")
    assert server.status == HealthStatus.HEALTHY


def test_automation_status_aggregates_rule_counts_and_timestamps() -> None:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)
    automation_repository = InMemoryAutomationRepository()
    automation_service = AutomationService(automation_repository=automation_repository)
    service = DashboardService(
        dashboard_repository=repository, automation_service=automation_service
    )
    rule1 = automation_service.create_rule(
        name="A",
        description="A",
        trigger=Trigger(kind=TriggerKind.TIME, time_of_day="09:00"),
        action=Action(kind=ActionKind.DASHBOARD_REFRESH),
    )
    rule1.last_executed_at = "2026-07-27T09:00:00"
    rule1.next_execution_at = "2026-07-28T09:00:00"
    automation_repository.save(rule1)
    automation_service.create_rule(
        name="B",
        description="B",
        trigger=Trigger(kind=TriggerKind.STARTUP),
        action=Action(kind=ActionKind.DASHBOARD_REFRESH),
        enabled=False,
    )

    status = service.automation_status()

    assert status is not None
    assert status.registered_rule_count == 2
    assert status.enabled_rule_count == 1
    assert status.last_execution_at == "2026-07-27T09:00:00"
    assert status.next_execution_at == "2026-07-28T09:00:00"


def test_dashboard_service_module_has_no_web_import() -> None:
    """M20 DoD 11번(사전 준비): dashboard_service 모듈이 web 계층을
    import하지 않음을 미리 확인한다(전체 검증은 M20-T06 통합
    테스트에서)."""
    import ast
    import inspect

    import ai_workspace.runtime.dashboard.dashboard_service as module

    tree = ast.parse(inspect.getsource(module))
    imported_modules = [
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
        for alias in node.names
    ] + [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]

    assert not any(name.startswith("ai_workspace.web") for name in imported_modules if name)
