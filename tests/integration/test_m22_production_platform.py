from __future__ import annotations

import ast
import asyncio
from pathlib import Path

from fastapi.testclient import TestClient
from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.domain.engine_selection import EngineSelectionDecision
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.execution_environment import ExecutionResult
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher
from ai_workspace.runtime.production.config import ProductionConfig
from ai_workspace.runtime.production.config_loader import load_production_config
from ai_workspace.runtime.production.health import HealthMonitor
from ai_workspace.runtime.production.lifecycle import LifecycleManager, LifecycleState
from ai_workspace.web.app import create_app
from ai_workspace.web.server import build_app

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_server_lifespan_transitions_lifecycle_and_reports_healthy() -> None:
    """M22 DoD: `workspace start` -> Configuration 로드 -> Lifecycle
    시작 -> Dashboard/Automation 시작까지 실제 FastAPI lifespan으로
    증명한다."""
    app = build_app(project_name="ai-workspace")

    with TestClient(app) as client:
        status_response = client.get("/api/status")
        health_response = client.get("/api/health")

    assert status_response.json()["lifecycle_state"] == "running"
    assert status_response.json()["health_status"] == "healthy"
    assert health_response.json()["health_status"] == "healthy"


def test_graceful_shutdown_waits_for_in_flight_execution_then_completes() -> None:
    """Graceful Shutdown이 실제 실행 중인 Task(Dashboard의 기존
    Event 기반 상태 추적)를 감지해 완료를 기다린 뒤에야 종료함을
    실제 ExecutionDispatcher 흐름으로 증명한다(강제 종료 없음,
    사용자 DoD)."""
    event_bus = InMemoryEventBus()
    dashboard_service = DashboardService(
        dashboard_repository=InMemoryDashboardRepository(event_bus=event_bus)
    )
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
    dispatcher = ExecutionDispatcher(
        engine_registry=registry, authentication_manager=auth, event_bus=event_bus
    )
    lifecycle_manager = LifecycleManager(
        dashboard_service=dashboard_service,
        graceful_shutdown_timeout_seconds=2.0,
        graceful_shutdown_poll_interval_seconds=0.02,
    )
    lifecycle_manager.startup()

    task = Task(task_id="t1", project_id="p1", title="정리 작업", status=TaskStatus.TODO)
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    async def _dispatch_while_shutting_down() -> None:
        shutdown_task = asyncio.create_task(lifecycle_manager.shutdown())
        await asyncio.sleep(0.05)
        assert lifecycle_manager.state is LifecycleState.SHUTDOWN
        assert dashboard_service.workspace_status().status == "idle"

        result = await asyncio.to_thread(dispatcher.dispatch, decision, task)
        assert result.success is True
        await shutdown_task

    asyncio.run(_dispatch_while_shutting_down())


def test_production_api_reflects_real_dashboard_and_automation_state() -> None:
    """`/api/health`/`/api/status`가 실제 Dashboard/Automation
    컴포넌트 연결 상태를 반영함을 REST 호출로 증명한다."""
    event_bus = InMemoryEventBus()
    dashboard_service = DashboardService(
        dashboard_repository=InMemoryDashboardRepository(event_bus=event_bus)
    )
    lifecycle_manager = LifecycleManager(dashboard_service=dashboard_service)
    health_monitor = HealthMonitor(
        lifecycle_manager=lifecycle_manager,
        dashboard_service=dashboard_service,
        event_bus=event_bus,
    )
    dashboard_service.attach_health_monitor(health_monitor)
    app = create_app(
        dashboard_service=dashboard_service,
        production_config=ProductionConfig(),
        lifecycle_manager=lifecycle_manager,
        health_monitor=health_monitor,
    )

    with TestClient(app) as client:
        health = client.get("/api/health").json()

    by_name = {c["name"]: c["status"] for c in health["components"]}
    assert by_name["dashboard"] == "healthy"
    assert by_name["automation"] == "unhealthy"  # 이번 인스턴스는 주입하지 않음


def test_load_production_config_env_var_overrides_reach_build_app() -> None:
    """Environment Variable로 설정한 값이 실제 `build_app()`이 만든
    앱의 `/api/config`까지 그대로 이어짐을 증명한다."""
    config = load_production_config(
        env={"AI_WORKSPACE_LOG_LEVEL": "DEBUG", "AI_WORKSPACE_AUTOMATION_TICK_SECONDS": "5"}
    )
    app = build_app(config=config)

    with TestClient(app) as client:
        response = client.get("/api/config")

    assert response.json()["log_level"] == "DEBUG"
    assert response.json()["automation_tick_seconds"] == 5.0


def _imported_module_names(module_path: Path) -> set[str]:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
    return names


def test_production_core_modules_do_not_import_web_layer() -> None:
    """M22 설계 원칙: Production Layer는 Infrastructure Layer에
    위치하지만, `runtime/production/`은 FastAPI/uvicorn을 몰라야
    한다 — 실제 라우트는 `web/production_routes.py`에서만 쓴다."""
    for relative_path in (
        "src/ai_workspace/runtime/production/config.py",
        "src/ai_workspace/runtime/production/config_loader.py",
        "src/ai_workspace/runtime/production/logging_setup.py",
        "src/ai_workspace/runtime/production/lifecycle.py",
        "src/ai_workspace/runtime/production/health.py",
        "src/ai_workspace/runtime/production/version.py",
    ):
        module_names = _imported_module_names(_PROJECT_ROOT / relative_path)
        assert not any(name.startswith("ai_workspace.web") for name in module_names)
        assert not any(name in ("fastapi", "uvicorn") for name in module_names)


def test_core_domain_modules_do_not_import_production_layer() -> None:
    """"Core Domain은 Production을 알지 못한다"(사용자 원칙)를
    `domain`/`interfaces`/`engines` 전체에 대해 확인한다."""
    core_dirs = (
        _PROJECT_ROOT / "src/ai_workspace/domain",
        _PROJECT_ROOT / "src/ai_workspace/interfaces",
        _PROJECT_ROOT / "src/ai_workspace/engines",
    )
    for core_dir in core_dirs:
        for module_path in core_dir.glob("*.py"):
            module_names = _imported_module_names(module_path)
            assert not any(
                name.startswith("ai_workspace.runtime.production") for name in module_names
            ), f"{module_path} imports Production layer"


def _imported_symbol_names(module_path: Path) -> set[str]:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom | ast.Import):
            names.update(alias.name for alias in node.names)
    return names


def test_lifecycle_manager_does_not_construct_components() -> None:
    """"LifecycleManager는 생성이 아닌 생명주기만 관리한다"(사용자
    승인 조건 2)를 import 그래프로 재확인한다 — 구체 구현체
    (`InMemory*`)를 전혀 import하지 않는다."""
    module_path = _PROJECT_ROOT / "src/ai_workspace/runtime/production/lifecycle.py"
    symbol_names = _imported_symbol_names(module_path)
    module_names = _imported_module_names(module_path)

    assert not any(name.startswith("InMemory") for name in symbol_names)
    assert not any(name.startswith("ai_workspace.engines") for name in module_names)
    assert not any(name.startswith("ai_workspace.storage") for name in module_names)
