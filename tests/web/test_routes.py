from fastapi.testclient import TestClient

from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.execution.events import (
    ENGINE_EXECUTION_COMPLETED,
    ENGINE_EXECUTION_STARTED,
)
from ai_workspace.web.app import create_app


def _build_client_with_repository() -> tuple[TestClient, InMemoryEventBus]:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus, project_name="ai-workspace")
    service = DashboardService(dashboard_repository=repository)
    app = create_app(dashboard_service=service, event_bus=event_bus)
    return TestClient(app), event_bus


def _publish_completed_execution(event_bus: InMemoryEventBus) -> None:
    event_bus.publish(
        Event(
            event_id="e1",
            event_type=ENGINE_EXECUTION_STARTED,
            payload={"engine": "claude_code", "task_title": "테스트 작업", "started_at": "t0"},
        )
    )
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


def test_get_dashboard_returns_all_sections() -> None:
    client, event_bus = _build_client_with_repository()
    _publish_completed_execution(event_bus)

    response = client.get("/api/dashboard")

    assert response.status_code == 200
    body = response.json()
    assert body["workspace"]["project_name"] == "ai-workspace"
    assert any(engine["name"] == "Claude Code" for engine in body["engines"])
    assert body["execution_stats"]["total"] == 1
    assert body["recent_history"][0]["result_label"] == "성공"
    assert body["reliability_stats"]["retry_count"] == 0


def test_get_summary_excludes_list_fields() -> None:
    client, event_bus = _build_client_with_repository()
    _publish_completed_execution(event_bus)

    response = client.get("/api/summary")

    assert response.status_code == 200
    body = response.json()
    assert "workspace" in body
    assert "execution_stats" in body
    assert "reliability_stats" in body
    assert "engines" not in body
    assert "recent_history" not in body


def test_get_history_respects_limit() -> None:
    client, event_bus = _build_client_with_repository()
    _publish_completed_execution(event_bus)
    _publish_completed_execution(event_bus)

    response = client.get("/api/history", params={"limit": 1})

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_engines_returns_known_engines_with_defaults() -> None:
    client, _event_bus = _build_client_with_repository()

    response = client.get("/api/engines")

    assert response.status_code == 200
    names = {engine["name"] for engine in response.json()}
    assert "Claude Code" in names
    assert all(engine["status_label"] == "준비 완료" for engine in response.json())
