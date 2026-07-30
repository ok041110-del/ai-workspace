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


def test_automation_scheduler_run_now_wires_run_recommendation_to_vault(tmp_path) -> None:
    """M38 — AutomationScheduler가 RUN_RECOMMENDATION Action을 실제로
    RecommendationExecutionService까지 연결하는지 확인한다(빈
    Vault라 Gate는 승인하지 않지만, publish()가 호출돼 결과 문서는
    쓰여진다 — Composition Root 배선 자체를 검증한다)."""
    from ai_workspace.domain.automation import Action, ActionKind, Trigger, TriggerKind
    from ai_workspace.runtime.production.config import ProductionConfig

    app = build_app(config=ProductionConfig(vault_root=str(tmp_path)))
    automation_service = app.state.automation_service
    automation_scheduler = app.state.automation_scheduler

    rule = automation_service.create_rule(
        name="추천 자동 실행",
        description="M38 next_task 자동 실행",
        trigger=Trigger(kind=TriggerKind.INTERVAL, interval_seconds=3600),
        action=Action(kind=ActionKind.RUN_RECOMMENDATION),
    )

    automation_scheduler.run_now(rule.rule_id)

    published_path = tmp_path / "15 Project Intelligence" / "Recommendation Execution.md"
    assert published_path.exists()
