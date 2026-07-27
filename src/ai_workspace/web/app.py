from __future__ import annotations

from fastapi import FastAPI

from ai_workspace.runtime.dashboard.dashboard_service import DashboardService


def create_app(*, dashboard_service: DashboardService) -> FastAPI:
    """Dashboard API의 FastAPI 앱 골격을 조립한다(M20-T04). `Core`
    계층(domain/interfaces/engines/runtime)은 FastAPI를 전혀 모른다
    — FastAPI는 이 `web/` 디렉터리(Infrastructure 계층)에서만 쓴다.
    `DashboardService`를 `app.state`에 실어 라우터(M20-T05)가
    `request.app.state.dashboard_service`로 꺼내 쓴다. 실제 Dashboard
    라우터/WebSocket 등록은 M20-T05의 책임이다 — 이 Task는 서버가
    실제로 뜨고 헬스 체크에 응답하는 최소 골격까지만 다룬다."""

    app = FastAPI(title="AI Workspace Dashboard API")
    app.state.dashboard_service = dashboard_service

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
