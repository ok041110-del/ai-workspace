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


def _build_client() -> tuple[TestClient, InMemoryEventBus]:
    event_bus = InMemoryEventBus()
    repository = InMemoryDashboardRepository(event_bus=event_bus)
    service = DashboardService(dashboard_repository=repository)
    app = create_app(dashboard_service=service, event_bus=event_bus)
    return TestClient(app), event_bus


def test_websocket_sends_initial_snapshot_on_connect() -> None:
    client, _event_bus = _build_client()

    with client.websocket_connect("/ws/dashboard") as websocket:
        message = websocket.receive_json()

    assert "workspace" in message
    assert "engines" in message
    assert message["execution_stats"]["total"] == 0


def test_websocket_pushes_update_after_execution_event() -> None:
    client, event_bus = _build_client()

    with client.websocket_connect("/ws/dashboard") as websocket:
        websocket.receive_json()

        event_bus.publish(
            Event(
                event_id="e1",
                event_type=ENGINE_EXECUTION_STARTED,
                payload={
                    "engine": "claude_code",
                    "task_title": "테스트 작업",
                    "started_at": "t0",
                },
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

        started_message = websocket.receive_json()
        completed_message = websocket.receive_json()

    assert started_message["workspace"]["status_label"] == "실행 중"
    assert completed_message["execution_stats"]["total"] == 1


def test_websocket_ignores_irrelevant_events() -> None:
    client, event_bus = _build_client()

    with client.websocket_connect("/ws/dashboard") as websocket:
        websocket.receive_json()
        event_bus.publish(Event(event_id="e1", event_type="unrelated_event", payload={}))

        event_bus.publish(
            Event(
                event_id="e2",
                event_type=ENGINE_EXECUTION_STARTED,
                payload={"engine": "claude_code", "task_title": "테스트", "started_at": "t0"},
            )
        )
        message = websocket.receive_json()

    assert message["workspace"]["status_label"] == "실행 중"
