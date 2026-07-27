from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING

from ai_workspace.interfaces.engine_registry import EngineRegistry
from ai_workspace.interfaces.event_bus import EventBus
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.production.lifecycle import LifecycleManager, LifecycleState
from ai_workspace.runtime.production.version import WORKSPACE_VERSION

if TYPE_CHECKING:
    # DashboardService가 이 모듈을 선택적으로 참조할 수 있어(M22-T06,
    # Reader→Reader) 런타임 순환 import를 피한다 — `_dashboard_health()`
    # 는 `DashboardService`의 메서드를 전혀 호출하지 않고 주입 여부만
    # 확인하므로, 타입 힌트 목적의 지연 import만으로 충분하다.
    from ai_workspace.runtime.dashboard.dashboard_service import DashboardService


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


_SEVERITY_ORDER = (HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY)


@dataclass(frozen=True)
class ComponentHealth:
    name: str
    status: HealthStatus
    detail: str | None = None


@dataclass(frozen=True)
class ProductionStatus:
    """M22의 표준 상태 정보(사용자 승인 조건 5 — `uptime`/
    `started_at`/`version`/`health_status`를 M23이 그대로 재사용할
    수 있도록 제공)."""

    health_status: HealthStatus
    version: str
    started_at: str | None
    uptime_seconds: float | None
    components: tuple[ComponentHealth, ...]


class HealthMonitor:
    """Workspace Server 구성 요소의 상태를 조회만 하는 Read
    Model(M22-T04, 사용자 승인 조건 3 — 상태를 바꾸지 않는다). 이미
    조립된 컴포넌트를 선택적으로 주입받아 "연결돼 있는가/정상
    범위인가"만 확인한다 — `LifecycleManager`와 마찬가지로 컴포넌트를
    스스로 만들지 않는다.

    **Engine 항목**: 이번 Milestone은 `EngineRegistry` Interface를
    확장하지 않기로 했다(M22 kickoff 승인 논의) — 등록된 Engine
    개수를 세지 않고, `EngineRegistry`가 구조적으로 연결돼 있는지만
    확인한다."""

    def __init__(
        self,
        *,
        lifecycle_manager: LifecycleManager,
        dashboard_service: DashboardService | None = None,
        automation_scheduler: AutomationScheduler | None = None,
        event_bus: EventBus | None = None,
        engine_registry: EngineRegistry | None = None,
    ) -> None:
        self._lifecycle_manager = lifecycle_manager
        self._dashboard_service = dashboard_service
        self._automation_scheduler = automation_scheduler
        self._event_bus = event_bus
        self._engine_registry = engine_registry

    def status(self, *, now: datetime | None = None) -> ProductionStatus:
        components = (
            self._server_health(),
            self._dashboard_health(),
            self._automation_health(),
            self._event_bus_health(),
            self._engine_health(),
        )
        return ProductionStatus(
            health_status=_aggregate(components),
            version=WORKSPACE_VERSION,
            started_at=self._lifecycle_manager.started_at,
            uptime_seconds=self._compute_uptime(now),
            components=components,
        )

    def _compute_uptime(self, now: datetime | None) -> float | None:
        started_at = self._lifecycle_manager.started_at
        if started_at is None:
            return None
        moment = now or datetime.now(UTC)
        return (moment - datetime.fromisoformat(started_at)).total_seconds()

    def _server_health(self) -> ComponentHealth:
        state = self._lifecycle_manager.state
        if state is LifecycleState.RUNNING:
            return ComponentHealth(name="server", status=HealthStatus.HEALTHY)
        if state is LifecycleState.STARTUP:
            return ComponentHealth(
                name="server", status=HealthStatus.DEGRADED, detail="아직 시작 중입니다"
            )
        return ComponentHealth(
            name="server", status=HealthStatus.UNHEALTHY, detail="종료 처리 중입니다"
        )

    def _dashboard_health(self) -> ComponentHealth:
        if self._dashboard_service is None:
            return ComponentHealth(
                name="dashboard", status=HealthStatus.UNHEALTHY, detail="연결되지 않음"
            )
        return ComponentHealth(name="dashboard", status=HealthStatus.HEALTHY)

    def _automation_health(self) -> ComponentHealth:
        if self._automation_scheduler is None:
            return ComponentHealth(
                name="automation", status=HealthStatus.UNHEALTHY, detail="연결되지 않음"
            )
        return ComponentHealth(name="automation", status=HealthStatus.HEALTHY)

    def _event_bus_health(self) -> ComponentHealth:
        if self._event_bus is None:
            return ComponentHealth(
                name="event_bus", status=HealthStatus.UNHEALTHY, detail="연결되지 않음"
            )
        return ComponentHealth(name="event_bus", status=HealthStatus.HEALTHY)

    def _engine_health(self) -> ComponentHealth:
        if self._engine_registry is None:
            return ComponentHealth(
                name="engine", status=HealthStatus.UNHEALTHY, detail="연결되지 않음"
            )
        return ComponentHealth(
            name="engine",
            status=HealthStatus.HEALTHY,
            detail="EngineRegistry 연결됨(개별 Engine 상태 조회는 범위 밖)",
        )


def _aggregate(components: tuple[ComponentHealth, ...]) -> HealthStatus:
    worst = HealthStatus.HEALTHY
    for component in components:
        if _SEVERITY_ORDER.index(component.status) > _SEVERITY_ORDER.index(worst):
            worst = component.status
    return worst
