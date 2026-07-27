from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator
from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from ai_workspace.interfaces.event_bus import EventBus
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.automation.automation_service import AutomationService
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.web.automation_routes import router as automation_router
from ai_workspace.web.dashboard_broadcaster import DashboardBroadcaster
from ai_workspace.web.routes import router as dashboard_router

_STATIC_DIR = Path(__file__).resolve().parent / "static"
DEFAULT_AUTOMATION_TICK_SECONDS = 30.0


def create_app(
    *,
    dashboard_service: DashboardService,
    event_bus: EventBus | None = None,
    automation_service: AutomationService | None = None,
    automation_scheduler: AutomationScheduler | None = None,
    automation_tick_seconds: float = DEFAULT_AUTOMATION_TICK_SECONDS,
) -> FastAPI:
    """Dashboard/Automation API의 FastAPI 앱을 조립한다(M20-T04/T05,
    M21-T05). `Core` 계층(domain/interfaces/engines/runtime)은
    FastAPI를 전혀 모른다 — FastAPI는 이 `web/` 디렉터리
    (Infrastructure 계층)에서만 쓴다. `DashboardService`를
    `app.state`에 실어 라우터가 `request.app.state.dashboard_service`
    로 꺼내 쓴다.

    `event_bus`를 주입하면(M20-T05) `DashboardBroadcaster`가 구독해
    Dashboard 관련 Event 발생 시 연결된 WebSocket 전부에 최신 스냅샷을
    민다(Polling 없음). 미주입 시(기본값 `None`) WebSocket 엔드포인트
    는 등록되지만 자동 갱신은 일어나지 않는다 — REST API만으로도
    Dashboard는 정상 동작한다.

    `automation_service`/`automation_scheduler`를 함께 주입해야만
    Automation API(`/api/automation/...`)가 등록된다(M21-T05) — 둘 다
    없으면(기본값) Dashboard API만 있던 M20 시절과 동일하게 동작한다
    (기존 호출부 무영향). `automation_scheduler`가 주어지면 서버
    기동(`lifespan`) 시 Startup Trigger를 1회 평가하고, 서버가 살아
    있는 동안 `automation_tick_seconds`마다 Time/Interval Trigger를
    평가하는 백그라운드 Task를 띄운다 — 종료 시 Task를 취소해 정리한다
    ("Scheduler는 Server Runtime과 함께 실행된다", 사용자 DoD)."""

    @contextlib.asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        tick_task: asyncio.Task[None] | None = None
        if automation_scheduler is not None:
            automation_scheduler.start()

            async def _tick_loop() -> None:
                while True:
                    await asyncio.sleep(automation_tick_seconds)
                    automation_scheduler.tick()

            tick_task = asyncio.create_task(_tick_loop())
        try:
            yield
        finally:
            if tick_task is not None:
                tick_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await tick_task

    app = FastAPI(title="AI Workspace Dashboard API", lifespan=lifespan)
    app.state.dashboard_service = dashboard_service
    app.include_router(dashboard_router)

    if automation_service is not None and automation_scheduler is not None:
        app.state.automation_service = automation_service
        app.state.automation_scheduler = automation_scheduler
        app.include_router(automation_router)

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
