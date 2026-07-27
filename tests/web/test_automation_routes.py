from fastapi.testclient import TestClient

from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.runtime.automation.automation_action_executor import AutomationActionExecutor
from ai_workspace.runtime.automation.automation_repository import InMemoryAutomationRepository
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.automation.automation_service import AutomationService
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher
from ai_workspace.web.app import create_app

_CREATE_BODY = {
    "name": "매일 정리",
    "description": "매일 09:00 정리 작업 실행",
    "trigger": {"kind": "time", "time_of_day": "09:00"},
    "action": {"kind": "dashboard_refresh"},
}


def _build_client() -> TestClient:
    event_bus = InMemoryEventBus()
    dashboard_repository = InMemoryDashboardRepository(event_bus=event_bus)
    engine_registry = InMemoryEngineRegistry()
    execution_dispatcher = ExecutionDispatcher(
        engine_registry=engine_registry,
        authentication_manager=InMemoryAuthenticationManager(),
        event_bus=event_bus,
    )
    automation_repository = InMemoryAutomationRepository()
    automation_service = AutomationService(automation_repository=automation_repository)
    action_executor = AutomationActionExecutor(
        engine_registry=engine_registry,
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
        execution_dispatcher=execution_dispatcher,
    )
    automation_scheduler = AutomationScheduler(
        automation_repository=automation_repository, action_executor=action_executor
    )
    dashboard_service = DashboardService(
        dashboard_repository=dashboard_repository, automation_service=automation_service
    )
    app = create_app(
        dashboard_service=dashboard_service,
        automation_service=automation_service,
        automation_scheduler=automation_scheduler,
    )
    return TestClient(app)


def test_list_rules_starts_empty() -> None:
    client = _build_client()

    response = client.get("/api/automation")

    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_rule() -> None:
    client = _build_client()

    created = client.post("/api/automation", json=_CREATE_BODY)
    assert created.status_code == 201
    rule_id = created.json()["rule_id"]

    fetched = client.get(f"/api/automation/{rule_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "매일 정리"


def test_get_unknown_rule_returns_404() -> None:
    client = _build_client()

    response = client.get("/api/automation/missing")

    assert response.status_code == 404


def test_update_rule_changes_only_given_fields() -> None:
    client = _build_client()
    rule_id = client.post("/api/automation", json=_CREATE_BODY).json()["rule_id"]

    response = client.put(f"/api/automation/{rule_id}", json={"description": "새 설명"})

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "매일 정리"
    assert body["description"] == "새 설명"


def test_update_unknown_rule_returns_404() -> None:
    client = _build_client()

    response = client.put("/api/automation/missing", json={"description": "새 설명"})

    assert response.status_code == 404


def test_delete_rule() -> None:
    client = _build_client()
    rule_id = client.post("/api/automation", json=_CREATE_BODY).json()["rule_id"]

    response = client.delete(f"/api/automation/{rule_id}")
    assert response.status_code == 204

    assert client.get(f"/api/automation/{rule_id}").status_code == 404


def test_delete_unknown_rule_returns_404() -> None:
    client = _build_client()

    response = client.delete("/api/automation/missing")

    assert response.status_code == 404


def test_enable_and_disable_rule() -> None:
    client = _build_client()
    rule_id = client.post("/api/automation", json=_CREATE_BODY).json()["rule_id"]

    disabled = client.post(f"/api/automation/{rule_id}/disable")
    assert disabled.status_code == 200
    assert disabled.json()["enabled"] is False

    enabled = client.post(f"/api/automation/{rule_id}/enable")
    assert enabled.status_code == 200
    assert enabled.json()["enabled"] is True


def test_run_rule_executes_immediately() -> None:
    client = _build_client()
    rule_id = client.post("/api/automation", json=_CREATE_BODY).json()["rule_id"]

    response = client.post(f"/api/automation/{rule_id}/run")

    assert response.status_code == 202
    assert client.get(f"/api/automation/{rule_id}").json()["last_executed_at"] is not None


def test_run_unknown_rule_returns_404() -> None:
    client = _build_client()

    response = client.post("/api/automation/missing/run")

    assert response.status_code == 404


def test_automation_routes_absent_without_automation_wiring() -> None:
    event_bus = InMemoryEventBus()
    dashboard_repository = InMemoryDashboardRepository(event_bus=event_bus)
    dashboard_service = DashboardService(dashboard_repository=dashboard_repository)
    app = create_app(dashboard_service=dashboard_service)
    client = TestClient(app)

    response = client.get("/api/automation")

    assert response.status_code == 404
