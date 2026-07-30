from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator
from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from ai_workspace.interfaces.event_bus import EventBus
from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.automation.automation_service import AutomationService
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.production.config import ProductionConfig
from ai_workspace.runtime.production.health import HealthMonitor
from ai_workspace.runtime.production.lifecycle import LifecycleManager
from ai_workspace.web.automation_routes import router as automation_router
from ai_workspace.web.dashboard_broadcaster import DashboardBroadcaster
from ai_workspace.web.production_routes import router as production_router
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
    production_config: ProductionConfig | None = None,
    lifecycle_manager: LifecycleManager | None = None,
    health_monitor: HealthMonitor | None = None,
    execution_memory_store: ExecutionMemoryStore | None = None,
) -> FastAPI:
    """Dashboard/Automation/Production API의 FastAPI 앱을
    조립한다(M20-T04/T05, M21-T05, M22-T05). `Core` 계층(domain/
    interfaces/engines/runtime)은 FastAPI를 전혀 모른다 — FastAPI는
    이 `web/` 디렉터리(Infrastructure 계층)에서만 쓴다.
    `DashboardService`를 `app.state`에 실어 라우터가
    `request.app.state.dashboard_service`로 꺼내 쓴다.

    `event_bus`를 주입하면(M20-T05) `DashboardBroadcaster`가 구독해
    Dashboard 관련 Event 발생 시 연결된 WebSocket 전부에 최신 스냅샷을
    민다(Polling 없음). 미주입 시(기본값 `None`) WebSocket 엔드포인트
    는 등록되지만 자동 갱신은 일어나지 않는다 — REST API만으로도
    Dashboard는 정상 동작한다.

    `automation_service`/`automation_scheduler`를 함께 주입해야만
    Automation API(`/api/automation/...`)가 등록된다(M21-T05) — 둘 다
    없으면(기본값) Dashboard API만 있던 M20 시절과 동일하게 동작한다
    (기존 호출부 무영향).

    `production_config`/`lifecycle_manager`/`health_monitor`를 모두
    주입해야만 Production API(`/api/health`, `/api/config`,
    `/api/version`, `/api/status`)가 등록된다(M22-T05, 기존 호출부
    무영향). `lifecycle_manager`가 주어지면 서버 기동 시
    `lifecycle_manager.startup()`이 `automation_scheduler.start()`를
    대신 호출하고, 종료 시 `await lifecycle_manager.shutdown()`이
    Graceful Shutdown(실행 중 Task 완료 대기, 강제 종료 없음)을
    수행한 뒤에야 주기적 tick Task를 취소한다 — `lifecycle_manager`
    미주입 시(기존 M20/M21 호출부)는 이전과 동일하게 즉시
    `automation_scheduler.start()`를 호출하고 대기 없이 tick Task를
    취소한다.

    `execution_memory_store`를 주입하면(M39) `app.state.
    execution_memory_store`로 노출한다 — 새 REST 엔드포인트는
    추가하지 않는다(YAGNI, ADR-0053). 미주입 시(기본값 `None`)
    `app.state`에 아무것도 실리지 않는다."""

    @contextlib.asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        tick_task: asyncio.Task[None] | None = None
        if automation_scheduler is not None:
            if lifecycle_manager is not None:
                lifecycle_manager.startup()
            else:
                automation_scheduler.start()

            async def _tick_loop() -> None:
                while True:
                    await asyncio.sleep(automation_tick_seconds)
                    automation_scheduler.tick()

            tick_task = asyncio.create_task(_tick_loop())
        try:
            yield
        finally:
            if lifecycle_manager is not None:
                await lifecycle_manager.shutdown()
            if tick_task is not None:
                tick_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await tick_task

    app = FastAPI(title="AI Workspace Dashboard API", lifespan=lifespan)
    app.state.dashboard_service = dashboard_service
    if execution_memory_store is not None:
        app.state.execution_memory_store = execution_memory_store
    app.include_router(dashboard_router)

    if automation_service is not None and automation_scheduler is not None:
        app.state.automation_service = automation_service
        app.state.automation_scheduler = automation_scheduler
        app.include_router(automation_router)

    if (
        production_config is not None
        and lifecycle_manager is not None
        and health_monitor is not None
    ):
        app.state.production_config = production_config
        app.state.lifecycle_manager = lifecycle_manager
        app.state.health_monitor = health_monitor
        app.include_router(production_router)

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
