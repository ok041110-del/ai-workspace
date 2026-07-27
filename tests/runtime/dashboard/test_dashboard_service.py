from ai_workspace.domain.dashboard import EngineStatus
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import KNOWN_ENGINES, DashboardService
from ai_workspace.runtime.execution.events import ENGINE_EXECUTION_STARTED


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
