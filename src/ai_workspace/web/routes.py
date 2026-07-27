from __future__ import annotations

from fastapi import APIRouter, Request

from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.web.dashboard_viewmodel import (
    DashboardViewModel,
    EngineStatusViewModel,
    ExecutionHistoryEntryViewModel,
    build_dashboard_view_model,
    build_engine_view_models,
    build_history_view_models,
    build_workspace_view_model,
)

router = APIRouter(prefix="/api", tags=["dashboard"])


def _dashboard_service(request: Request) -> DashboardService:
    service: DashboardService = request.app.state.dashboard_service
    return service


@router.get("/dashboard", response_model=DashboardViewModel)
def get_dashboard(request: Request) -> DashboardViewModel:
    """5개 Dashboard 영역 전체를 한 번에 반환한다."""
    return build_dashboard_view_model(_dashboard_service(request).snapshot())


@router.get("/summary")
def get_summary(request: Request) -> dict[str, object]:
    """"Workspace 현황" + "실행 현황" + "안정성 현황" 요약(목록류 제외)."""
    service = _dashboard_service(request)
    return {
        "workspace": build_workspace_view_model(service.workspace_status()),
        "execution_stats": service.execution_stats(),
        "reliability_stats": service.reliability_stats(),
        "automation_status": service.automation_status(),
        "production_status": service.production_status(),
    }


@router.get("/history", response_model=list[ExecutionHistoryEntryViewModel])
def get_history(request: Request, limit: int = 20) -> list[ExecutionHistoryEntryViewModel]:
    """"최근 실행 내역" 영역."""
    return build_history_view_models(_dashboard_service(request).recent_executions(limit))


@router.get("/engines", response_model=list[EngineStatusViewModel])
def get_engines(request: Request) -> list[EngineStatusViewModel]:
    """"엔진 현황" 영역."""
    return build_engine_view_models(_dashboard_service(request).engine_statuses())
