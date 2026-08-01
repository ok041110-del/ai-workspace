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


def test_build_app_wires_execution_memory_store(tmp_path) -> None:
    """M39 — RUN_RECOMMENDATION이 실제로 승인·실행되면 그 결과가
    `app.state.execution_memory_store`에 자동 기록되는지 확인한다
    (Composition Root 배선 검증, ADR-0053)."""
    from ai_workspace.domain.automation import Action, ActionKind, Trigger, TriggerKind
    from ai_workspace.integration.vault_adapter import VaultAdapter
    from ai_workspace.runtime.production.config import ProductionConfig

    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M39-T04",
        "Integration",
        status="todo",
        priority="high",
        milestone="M39",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )

    app = build_app(config=ProductionConfig(vault_root=str(tmp_path)))
    automation_service = app.state.automation_service
    automation_scheduler = app.state.automation_scheduler
    rule = automation_service.create_rule(
        name="추천 자동 실행",
        description="M39 Memory 기록 확인",
        trigger=Trigger(kind=TriggerKind.INTERVAL, interval_seconds=3600),
        action=Action(kind=ActionKind.RUN_RECOMMENDATION),
    )

    automation_scheduler.run_now(rule.rule_id)

    records = app.state.execution_memory_store.query(task_id="M39-T04")
    assert len(records) == 1
    # build_app()은 아직 어떤 EngineAdapter도 등록하지 않으므로(Out of
    # Scope, docstring 참고) 실행 자체는 실패하지만, 그 결과가
    # Memory에 자동 기록되는지가 이 테스트의 검증 대상이다.
    assert records[0].result == "failure"


def test_build_app_wires_architecture_guardian_and_blocks_execution_on_violation(tmp_path) -> None:
    """M48 — `build_app()`이 `ArchitectureGuardianService`를 실제
    자동 실행 경로에 조립해, `RUN_RECOMMENDATION`이 발동될 때 소스
    트리에 Guardian 위반이 있으면 Execution만 차단되는지 확인한다
    (ADR-0065). Recommendation 자체는 계속 계산돼 Vault Execution
    리포트가 여전히 발행된다."""
    from ai_workspace.domain.automation import Action, ActionKind, Trigger, TriggerKind
    from ai_workspace.integration.vault_adapter import VaultAdapter
    from ai_workspace.runtime.production.config import ProductionConfig

    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M48-T03",
        "Guardian 연결",
        status="todo",
        priority="high",
        milestone="M48",
        owner="AI",
        created="2026-08-01",
        updated="2026-08-01",
    )
    # core_domain_does_not_import_vault 규칙을 의도적으로 위반하는
    # 파일을 배치한다(GUARDIAN_RULES, guardian/rules.py).
    domain_dir = tmp_path / "src" / "ai_workspace" / "domain"
    domain_dir.mkdir(parents=True)
    (domain_dir / "bad.py").write_text("import ai_workspace.vault\n", encoding="utf-8")

    app = build_app(config=ProductionConfig(vault_root=str(tmp_path)))
    automation_service = app.state.automation_service
    automation_scheduler = app.state.automation_scheduler
    rule = automation_service.create_rule(
        name="추천 자동 실행",
        description="M48 Guardian Gate 확인",
        trigger=Trigger(kind=TriggerKind.INTERVAL, interval_seconds=3600),
        action=Action(kind=ActionKind.RUN_RECOMMENDATION),
    )

    automation_scheduler.run_now(rule.rule_id)

    execution_report = (
        tmp_path / "15 Project Intelligence" / "Recommendation Execution.md"
    ).read_text(encoding="utf-8")
    assert "Architecture Guardian 위반으로 실행 차단" in execution_report
    assert app.state.execution_memory_store.query(task_id="M48-T03") == []
