from __future__ import annotations

import ast
from pathlib import Path

from fastapi.testclient import TestClient
from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.domain.automation import Action, ActionKind, Trigger, TriggerKind
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.execution_environment import ExecutionResult
from ai_workspace.runtime.automation.automation_action_executor import AutomationActionExecutor
from ai_workspace.runtime.automation.automation_repository import InMemoryAutomationRepository
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.automation.automation_service import AutomationService
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher
from ai_workspace.web.app import create_app

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _assemble_full_stack() -> tuple[
    AutomationService, AutomationScheduler, InMemoryEventBus, FakeExecutionEnvironment, TestClient
]:
    """M21 DoD: `AutomationRule` -> `AutomationRepository` ->
    `AutomationService`/`AutomationScheduler` -> `ExecutionDispatcher`
    -> `EventBus` -> `Dashboard`까지 이어지는 실제 구성 요소를 하나로
    조립한다(Fake Automation 컴포넌트 없이, M18/M19/M20과 동일하게
    실제 `ClaudeCodeEngineAdapter`를 사용)."""
    event_bus = InMemoryEventBus()
    execution_environment = FakeExecutionEnvironment()
    execution_environment.result = ExecutionResult(returncode=0, stdout="ok", stderr="")
    registry = InMemoryEngineRegistry()
    registry.register(
        "claude_code",
        ClaudeCodeEngineAdapter(
            execution_environment=execution_environment, subprocess_timeout_seconds=5.0
        ),
    )
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    execution_dispatcher = ExecutionDispatcher(
        engine_registry=registry, authentication_manager=auth, event_bus=event_bus
    )

    automation_repository = InMemoryAutomationRepository()
    automation_service = AutomationService(automation_repository=automation_repository)
    action_executor = AutomationActionExecutor(
        engine_registry=registry,
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
        execution_dispatcher=execution_dispatcher,
    )
    automation_scheduler = AutomationScheduler(
        automation_repository=automation_repository, action_executor=action_executor
    )
    automation_scheduler.bind_event_bus(event_bus)

    dashboard_repository = InMemoryDashboardRepository(event_bus=event_bus)
    dashboard_service = DashboardService(
        dashboard_repository=dashboard_repository, automation_service=automation_service
    )
    app = create_app(
        dashboard_service=dashboard_service,
        event_bus=event_bus,
        automation_service=automation_service,
        automation_scheduler=automation_scheduler,
    )
    client = TestClient(app)
    return automation_service, automation_scheduler, event_bus, execution_environment, client


def test_event_trigger_causes_real_task_execution_via_execution_dispatcher() -> None:
    """"Task Completed -> Automation Rule 확인 -> 조건 만족 ->
    ExecutionDispatcher -> 새 Task 실행" 흐름(사용자 Architecture
    다이어그램)을 실제 컴포넌트로 증명한다. Trigger의 event_type을
    `ExecutionDispatcher`가 발행하는 이벤트와 다른 값으로 둬서, 이
    Rule 자신의 실행 결과가 스스로를 재귀적으로 재발동시키지 않게
    한다(외부 신호에 반응하는 전형적 사용 사례)."""
    automation_service, _scheduler, event_bus, execution_environment, _client = (
        _assemble_full_stack()
    )
    automation_service.create_rule(
        name="외부 신호 대응",
        description="외부 승인 이벤트 발생 시 후속 Task 실행",
        trigger=Trigger(kind=TriggerKind.EVENT, event_type="external_approval_granted"),
        action=Action(kind=ActionKind.RUN_TASK, project_id="p1", task_title="후속 작업"),
    )

    event_bus.publish(
        Event(event_id="e1", event_type="external_approval_granted", payload={})
    )

    assert len(execution_environment.executed_commands) == 1


def test_run_now_via_rest_api_updates_dashboard_automation_status() -> None:
    """REST API(`POST /api/automation`, `POST /{id}/run`)로 만들고
    즉시 실행한 Rule이 `/api/dashboard`의 Automation 현황에 그대로
    반영됨을 실제 HTTP 요청으로 증명한다."""
    _service, _scheduler, _event_bus, _env, client = _assemble_full_stack()

    created = client.post(
        "/api/automation",
        json={
            "name": "즉시 실행 테스트",
            "description": "설명",
            "trigger": {"kind": "startup"},
            "action": {"kind": "dashboard_refresh"},
        },
    )
    rule_id = created.json()["rule_id"]

    run_response = client.post(f"/api/automation/{rule_id}/run")
    assert run_response.status_code == 202

    dashboard = client.get("/api/dashboard").json()
    automation_status = dashboard["automation_status"]
    assert automation_status["registered_rule_count"] == 1
    assert automation_status["last_execution_at"] is not None


def _imported_module_names(module_path: Path) -> set[str]:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
    return names


def test_automation_core_modules_do_not_import_web_layer() -> None:
    """M21 설계 원칙: Automation Domain은 FastAPI를 알지 못한다.
    `domain`/`interfaces`/`runtime/automation`의 Automation 관련
    모듈이 `web/`이나 `fastapi`/`uvicorn`을 import하지 않음을 실제
    import 그래프로 확인한다."""
    for relative_path in (
        "src/ai_workspace/domain/automation.py",
        "src/ai_workspace/interfaces/automation_repository.py",
        "src/ai_workspace/runtime/automation/automation_repository.py",
        "src/ai_workspace/runtime/automation/automation_service.py",
        "src/ai_workspace/runtime/automation/automation_scheduler.py",
        "src/ai_workspace/runtime/automation/trigger_evaluator.py",
        "src/ai_workspace/runtime/automation/automation_action_executor.py",
    ):
        module_names = _imported_module_names(_PROJECT_ROOT / relative_path)
        assert not any(name.startswith("ai_workspace.web") for name in module_names)
        assert not any(name in ("fastapi", "uvicorn") for name in module_names)


def test_automation_scheduler_does_not_import_dashboard_layer() -> None:
    """`AutomationScheduler`/`AutomationActionExecutor`는 Dashboard와
    독립적인 Domain이다(사용자 확정) — `runtime.dashboard`나 `web`을
    직접 참조하지 않는다."""
    for relative_path in (
        "src/ai_workspace/runtime/automation/automation_scheduler.py",
        "src/ai_workspace/runtime/automation/automation_action_executor.py",
    ):
        module_names = _imported_module_names(_PROJECT_ROOT / relative_path)
        assert not any(name.startswith("ai_workspace.runtime.dashboard") for name in module_names)
        assert not any(name.startswith("ai_workspace.web") for name in module_names)


def test_execution_dispatcher_does_not_import_automation_layer() -> None:
    """`ExecutionDispatcher`는 Automation의 존재를 전혀 모른다 —
    Automation이 Event를 구독해 `ExecutionDispatcher`를 호출하는
    방향으로만 결합된다(단방향)."""
    module_names = _imported_module_names(
        _PROJECT_ROOT / "src/ai_workspace/runtime/execution/execution_dispatcher.py"
    )
    assert not any(name.startswith("ai_workspace.runtime.automation") for name in module_names)
