from __future__ import annotations

import ast
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
from ai_workspace.web.app import create_app

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def make_task() -> Task:
    return Task(
        task_id="t1", project_id="p1", title="대시보드 통합 테스트 작업", status=TaskStatus.TODO
    )


def _assemble_full_stack() -> tuple[ExecutionDispatcher, TestClient]:
    """M20 DoD: Event(`ExecutionDispatcher`) -> `InMemoryDashboardRepository`
    -> `DashboardService` -> REST API/WebSocket까지 이어지는 실제
    구성 요소들을 하나로 조립한다(가짜 Dashboard 컴포넌트 없이 실제
    `ClaudeCodeEngineAdapter`를 사용해 진짜 실행 결과가 Dashboard에
    반영됨을 검증한다)."""
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
    dispatcher = ExecutionDispatcher(
        engine_registry=registry, authentication_manager=auth, event_bus=event_bus
    )

    repository = InMemoryDashboardRepository(event_bus=event_bus, project_name="ai-workspace")
    service = DashboardService(dashboard_repository=repository)
    app = create_app(dashboard_service=service, event_bus=event_bus)
    client = TestClient(app)
    return dispatcher, client


def test_real_execution_updates_rest_api_dashboard() -> None:
    """실제 실행(`ExecutionDispatcher.dispatch`)이 발행한 Event가
    `InMemoryDashboardRepository`를 거쳐 `/api/dashboard` REST 응답에
    그대로 반영됨을 증명한다(Event -> Repository -> Service -> API)."""
    dispatcher, client = _assemble_full_stack()
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    result = dispatcher.dispatch(decision, make_task())

    assert result.success is True
    response = client.get("/api/dashboard")
    body = response.json()
    assert body["execution_stats"]["total"] == 1
    assert body["execution_stats"]["success"] == 1
    assert body["recent_history"][0]["result_label"] == "성공"
    assert any(
        engine["name"] == "Claude Code" and engine["status_label"] == "준비 완료"
        for engine in body["engines"]
    )


def test_real_execution_pushes_websocket_updates() -> None:
    """동일한 실제 실행 흐름이 WebSocket으로도 최신 스냅샷을 밀어줌을
    증명한다(Event -> Repository -> Service -> WebSocket, Polling 없음)."""
    dispatcher, client = _assemble_full_stack()
    decision = EngineSelectionDecision(engine_name="claude_code", model=None, reason="test")

    with client.websocket_connect("/ws/dashboard") as websocket:
        websocket.receive_json()  # 최초 연결 시 보내는 스냅샷

        dispatcher.dispatch(decision, make_task())

        started_message = websocket.receive_json()
        completed_message = websocket.receive_json()

    assert started_message["workspace"]["status_label"] == "실행 중"
    assert completed_message["execution_stats"]["total"] == 1
    assert completed_message["workspace"]["status_label"] == "대기 중"


def _imported_module_names(module_path: Path) -> set[str]:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
    return names


def test_dashboard_service_and_repository_do_not_import_web_layer() -> None:
    """M20 설계 원칙: `DashboardService`/`InMemoryDashboardRepository`
    (Core 계층)는 `web/`(Infrastructure 계층, FastAPI)을 전혀 모른다
    — Event 기반 CQRS 경계를 실제 import 그래프로 재확인한다."""
    for relative_path in (
        "src/ai_workspace/runtime/dashboard/dashboard_service.py",
        "src/ai_workspace/runtime/dashboard/dashboard_repository.py",
    ):
        module_names = _imported_module_names(_PROJECT_ROOT / relative_path)
        assert not any(name.startswith("ai_workspace.web") for name in module_names)
        assert not any(name in ("fastapi", "uvicorn") for name in module_names)


def test_execution_dispatcher_does_not_import_dashboard_layer() -> None:
    """`ExecutionDispatcher`는 이벤트만 발행할 뿐, Dashboard 관련
    모듈(`runtime.dashboard`/`web`)을 직접 참조하지 않는다(CQRS 쓰기측
    독립성)."""
    module_names = _imported_module_names(
        _PROJECT_ROOT / "src/ai_workspace/runtime/execution/execution_dispatcher.py"
    )
    assert not any(name.startswith("ai_workspace.runtime.dashboard") for name in module_names)
    assert not any(name.startswith("ai_workspace.web") for name in module_names)
