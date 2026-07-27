from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from ai_workspace.interfaces.event_bus import EventBus
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.web.dashboard_broadcaster import DashboardBroadcaster
from ai_workspace.web.routes import router as dashboard_router

_STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app(
    *, dashboard_service: DashboardService, event_bus: EventBus | None = None
) -> FastAPI:
    """Dashboard API의 FastAPI 앱을 조립한다(M20-T04/T05). `Core`
    계층(domain/interfaces/engines/runtime)은 FastAPI를 전혀 모른다
    — FastAPI는 이 `web/` 디렉터리(Infrastructure 계층)에서만 쓴다.
    `DashboardService`를 `app.state`에 실어 라우터가
    `request.app.state.dashboard_service`로 꺼내 쓴다.

    `event_bus`를 주입하면(M20-T05) `DashboardBroadcaster`가 구독해
    Dashboard 관련 Event 발생 시 연결된 WebSocket 전부에 최신 스냅샷을
    민다(Polling 없음). 미주입 시(기본값 `None`) WebSocket 엔드포인트
    는 등록되지만 자동 갱신은 일어나지 않는다 — REST API만으로도
    Dashboard는 정상 동작한다."""

    app = FastAPI(title="AI Workspace Dashboard API")
    app.state.dashboard_service = dashboard_service
    app.include_router(dashboard_router)

    broadcaster = DashboardBroadcaster(dashboard_service=dashboard_service)
    if event_bus is not None:
        broadcaster.register_event_bus(event_bus)
    app.state.dashboard_broadcaster = broadcaster

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.websocket("/ws/dashboard")
    async def dashboard_websocket(websocket: WebSocket) -> None:
        await broadcaster.handle_connection(websocket)

    if _STATIC_DIR.is_dir():
        app.mount("/", StaticFiles(directory=str(_STATIC_DIR), html=True), name="static")

    return app
