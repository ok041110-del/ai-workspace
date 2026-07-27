from fastapi.testclient import TestClient

from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.web.app import create_app


def _build_client() -> TestClient:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)
    service = DashboardService(dashboard_repository=repository)
    app = create_app(dashboard_service=service)
    return TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    client = _build_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_dashboard_service_is_stored_on_app_state() -> None:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)
    service = DashboardService(dashboard_repository=repository)

    app = create_app(dashboard_service=service)

    assert app.state.dashboard_service is service
