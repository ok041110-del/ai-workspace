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
