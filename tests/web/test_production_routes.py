from fastapi.testclient import TestClient

from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.production.config import ProductionConfig
from ai_workspace.runtime.production.health import HealthMonitor
from ai_workspace.runtime.production.lifecycle import LifecycleManager
from ai_workspace.runtime.production.version import WORKSPACE_VERSION
from ai_workspace.web.app import create_app


def _build_client() -> TestClient:
    event_bus = InMemoryEventBus()
    dashboard_service = DashboardService(
        dashboard_repository=InMemoryDashboardRepository(event_bus=event_bus)
    )
    lifecycle_manager = LifecycleManager(dashboard_service=dashboard_service)
    health_monitor = HealthMonitor(
        lifecycle_manager=lifecycle_manager, dashboard_service=dashboard_service
    )
    app = create_app(
        dashboard_service=dashboard_service,
        production_config=ProductionConfig(),
        lifecycle_manager=lifecycle_manager,
        health_monitor=health_monitor,
    )
    return TestClient(app)


def test_get_health_returns_component_breakdown() -> None:
    client = _build_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert "components" in body
    assert {c["name"] for c in body["components"]} == {
        "server",
        "dashboard",
        "automation",
        "event_bus",
        "engine",
    }


def test_get_config_returns_production_config() -> None:
    client = _build_client()

    response = client.get("/api/config")

    assert response.status_code == 200
    assert response.json()["host"] == "127.0.0.1"
    assert response.json()["port"] == 8080


def test_get_version_returns_workspace_version() -> None:
    client = _build_client()

    response = client.get("/api/version")

    assert response.status_code == 200
    assert response.json()["version"] == WORKSPACE_VERSION


def test_get_status_returns_standard_fields() -> None:
    client = _build_client()

    response = client.get("/api/status")

    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "lifecycle_state",
        "health_status",
        "version",
        "started_at",
        "uptime_seconds",
    }


def test_production_routes_absent_without_production_wiring() -> None:
    event_bus = InMemoryEventBus()
    dashboard_service = DashboardService(
        dashboard_repository=InMemoryDashboardRepository(event_bus=event_bus)
    )
    app = create_app(dashboard_service=dashboard_service)
    client = TestClient(app)

    response = client.get("/api/health")

    assert response.status_code == 404
