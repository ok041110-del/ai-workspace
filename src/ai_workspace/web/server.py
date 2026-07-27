from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.web.app import create_app

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080


def build_app(*, project_name: str | None = None) -> FastAPI:
    """`workspace start`가 실행할 FastAPI 앱을 조립한다(M20-T04).
    `EventBus`/`InMemoryDashboardRepository`/`DashboardService`를
    이 함수 하나로 조립해, 실제 서버 기동(`uvicorn.run`)과 분리한다
    — 이렇게 하면 실제 소켓을 열지 않고도 `TestClient`로 테스트할 수
    있다. 반환된 `event_bus`는 아직 어떤 Agent/`ExecutionDispatcher`
    와도 연결돼 있지 않다 — Dashboard 컴포넌트 자체의 조립까지만
    이번 Milestone의 책임이다."""
    event_bus = InMemoryEventBus()
    dashboard_repository = InMemoryDashboardRepository(
        event_bus=event_bus, project_name=project_name
    )
    dashboard_service = DashboardService(dashboard_repository=dashboard_repository)
    return create_app(dashboard_service=dashboard_service, event_bus=event_bus)


def run_server(
    *, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, project_name: str | None = None
) -> None:
    """`workspace start`의 실제 진입점 — `uvicorn.run()`을 호출해
    상시 실행되는 서버를 띄운다. 기존 CLI 명령(1회성 실행)에는 전혀
    영향을 주지 않는다 — 서버는 이 함수가 호출될 때만 실행된다."""
    app = build_app(project_name=project_name)
    uvicorn.run(app, host=host, port=port)
