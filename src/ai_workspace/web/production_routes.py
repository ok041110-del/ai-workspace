from __future__ import annotations

from fastapi import APIRouter, Request

from ai_workspace.runtime.production.config import ProductionConfig
from ai_workspace.runtime.production.health import HealthMonitor, ProductionStatus
from ai_workspace.runtime.production.lifecycle import LifecycleManager
from ai_workspace.runtime.production.version import VersionInfo, get_version_info

router = APIRouter(prefix="/api", tags=["production"])


def _health_monitor(request: Request) -> HealthMonitor:
    monitor: HealthMonitor = request.app.state.health_monitor
    return monitor


def _production_config(request: Request) -> ProductionConfig:
    config: ProductionConfig = request.app.state.production_config
    return config


def _lifecycle_manager(request: Request) -> LifecycleManager:
    manager: LifecycleManager = request.app.state.lifecycle_manager
    return manager


@router.get("/health", response_model=ProductionStatus)
def get_health(request: Request) -> ProductionStatus:
    """Health Monitor의 컴포넌트별 상세 상태(사용자 DoD)."""
    return _health_monitor(request).status()


@router.get("/config", response_model=ProductionConfig)
def get_config(request: Request) -> ProductionConfig:
    """현재 적용된 `ProductionConfig`를 그대로 노출한다 — 비밀값을
    담지 않는 순수 운영 설정이라 읽기 전용으로 공개해도 안전하다."""
    return _production_config(request)


@router.get("/version", response_model=VersionInfo)
def get_version(_request: Request) -> VersionInfo:
    return get_version_info()


@router.get("/status")
def get_status(request: Request) -> dict[str, object]:
    """사용자 승인 조건 5의 표준 상태 정보(`uptime`/`started_at`/
    `version`/`health_status`)만 담은 경량 요약 — M23이 그대로
    재사용할 수 있도록 `/api/health`(컴포넌트별 상세)와 분리해
    둔다."""
    status = _health_monitor(request).status()
    return {
        "lifecycle_state": _lifecycle_manager(request).state.value,
        "health_status": status.health_status.value,
        "version": status.version,
        "started_at": status.started_at,
        "uptime_seconds": status.uptime_seconds,
    }
