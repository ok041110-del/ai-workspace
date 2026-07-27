from __future__ import annotations

from ai_workspace.domain.dashboard import (
    EngineStatus,
    ExecutionRecord,
    ExecutionStats,
    ReliabilityStats,
    WorkspaceStatus,
)
from ai_workspace.interfaces.dashboard_repository import DashboardRepository
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.runtime.execution.events import (
    ENGINE_AUTHENTICATION_FAILED,
    ENGINE_EXECUTION_COMPLETED,
    ENGINE_EXECUTION_STARTED,
)

_RECENT_EXECUTIONS_KEPT = 100


class InMemoryDashboardRepository(DashboardRepository):
    """`EventBus`를 구독해 `ExecutionDispatcher`(M20-T02)가 발행하는
    Event로 Read Model을 갱신하는 최소 구현체. `ExecutionDispatcher`
    는 이 클래스를 전혀 알지 못한다 — 구독은 이 클래스가 스스로 한다
    (CQRS: 쓰기는 Event를 통해서만, 읽기는 이 클래스의 조회 메서드를
    통해서만). 통계는 조회 시점에 계산하지 않고 매 Event마다
    미리 갱신해 둔다("Dashboard는 통계를 계산하지 않는다", 사용자
    설계 원칙)."""

    def __init__(self, *, event_bus: EventBus, project_name: str | None = None) -> None:
        self._workspace_status = WorkspaceStatus(
            project_name=project_name, current_task_title=None, status="idle", started_at=None
        )
        self._engine_statuses: dict[str, EngineStatus] = {}
        self._recent_executions: list[ExecutionRecord] = []
        self._execution_stats = ExecutionStats(
            total=0, success=0, failure=0, cancelled=0, timed_out=0
        )
        self._reliability_stats = ReliabilityStats(
            retry_count=0, timeout_count=0, cancelled_count=0, authentication_failure_count=0
        )
        event_bus.subscribe(self._on_event)

    def _on_event(self, event: Event) -> None:
        if event.event_type == ENGINE_EXECUTION_STARTED:
            self.record_execution_started(
                engine_name=str(event.payload["engine"]),
                task_title=str(event.payload["task_title"]),
                started_at=str(event.payload["started_at"]),
            )
        elif event.event_type == ENGINE_EXECUTION_COMPLETED:
            self.record_execution_completed(
                ExecutionRecord(
                    executed_at=str(event.payload["completed_at"]),
                    engine=str(event.payload["engine"]),
                    success=bool(event.payload["success"]),
                    cancelled=bool(event.payload["cancelled"]),
                    timed_out=bool(event.payload["timed_out"]),
                    retry_count=int(event.payload["retry_count"]),
                    error=event.payload["error"],
                )
            )
        elif event.event_type == ENGINE_AUTHENTICATION_FAILED:
            self.record_authentication_failure(engine_name=str(event.payload["engine"]))

    def record_execution_started(
        self, *, engine_name: str, task_title: str, started_at: str
    ) -> None:
        self._workspace_status = WorkspaceStatus(
            project_name=self._workspace_status.project_name,
            current_task_title=task_title,
            status="running",
            started_at=started_at,
        )
        self._engine_statuses[engine_name] = EngineStatus.RUNNING

    def record_execution_completed(self, record: ExecutionRecord) -> None:
        self._recent_executions.insert(0, record)
        del self._recent_executions[_RECENT_EXECUTIONS_KEPT:]

        self._engine_statuses[record.engine] = (
            EngineStatus.READY if record.success else EngineStatus.ERROR
        )
        self._workspace_status = WorkspaceStatus(
            project_name=self._workspace_status.project_name,
            current_task_title=None,
            status="idle",
            started_at=None,
        )

        stats = self._execution_stats
        self._execution_stats = ExecutionStats(
            total=stats.total + 1,
            success=stats.success + (1 if record.success else 0),
            failure=stats.failure
            + (1 if (not record.success and not record.cancelled and not record.timed_out) else 0),
            cancelled=stats.cancelled + (1 if record.cancelled else 0),
            timed_out=stats.timed_out + (1 if record.timed_out else 0),
        )
        reliability = self._reliability_stats
        self._reliability_stats = ReliabilityStats(
            retry_count=reliability.retry_count + record.retry_count,
            timeout_count=reliability.timeout_count + (1 if record.timed_out else 0),
            cancelled_count=reliability.cancelled_count + (1 if record.cancelled else 0),
            authentication_failure_count=reliability.authentication_failure_count,
        )

    def record_authentication_failure(self, *, engine_name: str) -> None:
        self._engine_statuses[engine_name] = EngineStatus.AUTH_REQUIRED
        reliability = self._reliability_stats
        self._reliability_stats = ReliabilityStats(
            retry_count=reliability.retry_count,
            timeout_count=reliability.timeout_count,
            cancelled_count=reliability.cancelled_count,
            authentication_failure_count=reliability.authentication_failure_count + 1,
        )
        self._workspace_status = WorkspaceStatus(
            project_name=self._workspace_status.project_name,
            current_task_title=None,
            status="idle",
            started_at=None,
        )

    def workspace_status(self) -> WorkspaceStatus:
        return self._workspace_status

    def engine_statuses(self) -> dict[str, EngineStatus]:
        return dict(self._engine_statuses)

    def recent_executions(self, limit: int = 20) -> list[ExecutionRecord]:
        return list(self._recent_executions[:limit])

    def execution_stats(self) -> ExecutionStats:
        return self._execution_stats

    def reliability_stats(self) -> ReliabilityStats:
        return self._reliability_stats
