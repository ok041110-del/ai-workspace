from fastapi.testclient import TestClient

from ai_workspace.web.server import build_app


def test_build_app_produces_a_working_health_endpoint() -> None:
    app = build_app(project_name="AI Workspace")
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200


def test_build_app_wires_dashboard_service_with_project_name() -> None:
    app = build_app(project_name="AI Workspace")

    status = app.state.dashboard_service.workspace_status()

    assert status.project_name == "AI Workspace"


def test_build_app_wires_automation_service_and_scheduler() -> None:
    app = build_app(project_name="AI Workspace")

    assert app.state.automation_service.list_rules() == []
    assert app.state.automation_scheduler is not None


def test_build_app_lifespan_starts_and_shuts_down_cleanly() -> None:
    app = build_app(project_name="AI Workspace")

    with TestClient(app) as client:
        response = client.get("/api/automation")
        assert response.status_code == 200


def test_build_app_wires_production_layer() -> None:
    app = build_app(project_name="AI Workspace")

    assert app.state.production_config.host == "127.0.0.1"
    assert app.state.lifecycle_manager is not None
    assert app.state.health_monitor is not None


def test_build_app_lifespan_transitions_lifecycle_to_running() -> None:
    app = build_app(project_name="AI Workspace")

    with TestClient(app) as client:
        response = client.get("/api/status")

    assert response.status_code == 200
    assert response.json()["lifecycle_state"] == "running"


def test_build_app_accepts_explicit_config() -> None:
    from ai_workspace.runtime.production.config import ProductionConfig

    app = build_app(config=ProductionConfig(host="0.0.0.0", port=9090))

    assert app.state.production_config.host == "0.0.0.0"
    assert app.state.production_config.port == 9090
