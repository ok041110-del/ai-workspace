from __future__ import annotations

import asyncio
import time
from datetime import UTC, datetime
from enum import Enum

from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService

DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT_SECONDS = 30.0
DEFAULT_GRACEFUL_SHUTDOWN_POLL_INTERVAL_SECONDS = 0.5


class LifecycleState(Enum):
    STARTUP = "startup"
    RUNNING = "running"
    SHUTDOWN = "shutdown"


def _utc_now() -> datetime:
    return datetime.now(UTC)


class LifecycleManager:
    """Workspace Server의 Startup/Running/Shutdown 생명주기만
    관리한다(M22-T03, 사용자 승인 조건 2 — **생성이 아닌 생명주기만**
    관리한다). `AutomationScheduler`/`DashboardService`는 이미
    `web/server.py`가 조립해 둔 것을 그대로 주입받는다 — 이 클래스는
    컴포넌트를 만들거나 `EventBus`/Engine을 초기화하지 않는다.

    **Startup**: `AutomationScheduler.start()`(Startup Trigger 1회
    평가)를 호출하고 `started_at`을 기록한다.

    **Graceful Shutdown**: 강제 종료를 수행하지 않는다(사용자 DoD).
    `DashboardService.workspace_status()`(M20이 이미 Event로
    추적하는 실행 중 여부)를 폴링해 실행 중인 Task가 끝나기를
    기다리되, `graceful_shutdown_timeout_seconds`를 넘기면 그 이상
    강제로 개입하지 않고 그대로 진행한다 — `ExecutionDispatcher`를
    직접 참조하지 않으므로 Core Domain은 이 클래스의 존재를 전혀
    모른다."""

    def __init__(
        self,
        *,
        automation_scheduler: AutomationScheduler | None = None,
        dashboard_service: DashboardService | None = None,
        graceful_shutdown_timeout_seconds: float = DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT_SECONDS,
        graceful_shutdown_poll_interval_seconds: float = (
            DEFAULT_GRACEFUL_SHUTDOWN_POLL_INTERVAL_SECONDS
        ),
    ) -> None:
        self._automation_scheduler = automation_scheduler
        self._dashboard_service = dashboard_service
        self._graceful_shutdown_timeout_seconds = graceful_shutdown_timeout_seconds
        self._graceful_shutdown_poll_interval_seconds = graceful_shutdown_poll_interval_seconds
        self._state = LifecycleState.STARTUP
        self._started_at: str | None = None

    @property
    def state(self) -> LifecycleState:
        return self._state

    @property
    def started_at(self) -> str | None:
        return self._started_at

    def startup(self, *, now: datetime | None = None) -> None:
        moment = now or _utc_now()
        self._started_at = moment.isoformat()
        if self._automation_scheduler is not None:
            self._automation_scheduler.start(now=moment)
        self._state = LifecycleState.RUNNING

    async def shutdown(self) -> None:
        self._state = LifecycleState.SHUTDOWN
        await self._wait_for_running_tasks()

    async def _wait_for_running_tasks(self) -> None:
        if self._dashboard_service is None:
            return
        deadline = time.monotonic() + self._graceful_shutdown_timeout_seconds
        while time.monotonic() < deadline:
            if self._dashboard_service.workspace_status().status != "running":
                return
            await asyncio.sleep(self._graceful_shutdown_poll_interval_seconds)
