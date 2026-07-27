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
