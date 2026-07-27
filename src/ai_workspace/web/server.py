from __future__ import annotations

import uvicorn
from fastapi import FastAPI

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

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080


def build_app(*, project_name: str | None = None) -> FastAPI:
    """`workspace start`가 실행할 FastAPI 앱을 조립한다(M20-T04,
    M21-T05). `EventBus`/`InMemoryDashboardRepository`/
    `DashboardService`/Automation 컴포넌트를 이 함수 하나로 조립해,
    실제 서버 기동(`uvicorn.run`)과 분리한다 — 이렇게 하면 실제
    소켓을 열지 않고도 `TestClient`로 테스트할 수 있다.

    `EngineRegistry`/`AuthenticationManager`/`ExecutionDispatcher`는
    Automation의 RUN_TASK Action이 사용할 실행 파이프라인이다(M21
    사용자 승인 조건 5 — `ExecutionDispatcher`가 유일한 실행
    진입점). 이 시점에는 아직 어떤 `EngineAdapter`도 등록돼 있지
    않다 — 실제 Engine 등록·인증은 Workspace Core(CLI 경로)의
    책임이고, 이 Dashboard/Automation 서버 모듈은 그 등록을 대신하지
    않는다(Out of Scope). 그 상태에서 RUN_TASK가 발동하면
    `EngineNotRegisteredError`가 발생하지만, `AutomationScheduler`
    가 이를 삼켜(swallow) 다른 Rule 평가에 영향을 주지 않는다."""
    event_bus = InMemoryEventBus()
    dashboard_repository = InMemoryDashboardRepository(
        event_bus=event_bus, project_name=project_name
    )

    engine_registry = InMemoryEngineRegistry()
    authentication_manager = InMemoryAuthenticationManager()
    execution_dispatcher = ExecutionDispatcher(
        engine_registry=engine_registry,
        authentication_manager=authentication_manager,
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
    automation_scheduler.bind_event_bus(event_bus)

    dashboard_service = DashboardService(
        dashboard_repository=dashboard_repository, automation_service=automation_service
    )
    return create_app(
        dashboard_service=dashboard_service,
        event_bus=event_bus,
        automation_service=automation_service,
        automation_scheduler=automation_scheduler,
    )


def run_server(
    *, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, project_name: str | None = None
) -> None:
    """`workspace start`의 실제 진입점 — `uvicorn.run()`을 호출해
    상시 실행되는 서버를 띄운다. 기존 CLI 명령(1회성 실행)에는 전혀
    영향을 주지 않는다 — 서버는 이 함수가 호출될 때만 실행된다."""
    app = build_app(project_name=project_name)
    uvicorn.run(app, host=host, port=port)
