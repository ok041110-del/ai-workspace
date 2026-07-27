from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.domain.dashboard import (
    EngineStatus,
    ExecutionRecord,
    ExecutionStats,
    ReliabilityStats,
    WorkspaceStatus,
)
from ai_workspace.interfaces.dashboard_repository import DashboardRepository

KNOWN_ENGINES: tuple[str, ...] = ("claude_code", "gemini_cli", "codex_cli", "ollama")
"""Dashboard "엔진 현황" 영역에 항상 표시할 Engine 식별자 목록(M20 DoD).
`DashboardRepository`는 실제로 실행된 적 있는 Engine만 알고 있으므로,
아직 한 번도 실행되지 않은 Engine은 이 목록을 기준으로 기본 상태
(READY)를 채운다."""


@dataclass(frozen=True)
class DashboardSnapshot:
    """5개 Dashboard 영역을 한 번에 담는 조합 결과(M20-T03). `/api/dashboard`
    처럼 전체를 한 번에 내려줘야 하는 진입점을 위한 것이고, 개별 영역만
    필요하면 `DashboardService`의 개별 메서드를 쓰면 된다."""

    workspace_status: WorkspaceStatus
    engine_statuses: dict[str, EngineStatus]
    execution_stats: ExecutionStats
    recent_executions: list[ExecutionRecord]
    reliability_stats: ReliabilityStats


class DashboardService:
    """`DashboardRepository`의 Read Model을 조합해 Dashboard 조회
    요청에 응답하는 서비스(M20-T03). **UI를 전혀 모른다** — `web/`
    계층(API/WebSocket/Web UI)을 import하지 않는다(M20-T06에서
    Architecture 의존성 검증으로 증명). 통계를 스스로 계산하지 않고
    `DashboardRepository`가 이미 계산해 둔 값을 그대로 전달한다."""

    def __init__(self, *, dashboard_repository: DashboardRepository) -> None:
        self._dashboard_repository = dashboard_repository

    def snapshot(self) -> DashboardSnapshot:
        return DashboardSnapshot(
            workspace_status=self.workspace_status(),
            engine_statuses=self.engine_statuses(),
            execution_stats=self.execution_stats(),
            recent_executions=self.recent_executions(),
            reliability_stats=self.reliability_stats(),
        )

    def workspace_status(self) -> WorkspaceStatus:
        return self._dashboard_repository.workspace_status()

    def engine_statuses(self) -> dict[str, EngineStatus]:
        recorded = self._dashboard_repository.engine_statuses()
        return {name: recorded.get(name, EngineStatus.READY) for name in KNOWN_ENGINES}

    def recent_executions(self, limit: int = 20) -> list[ExecutionRecord]:
        return self._dashboard_repository.recent_executions(limit)

    def execution_stats(self) -> ExecutionStats:
        return self._dashboard_repository.execution_stats()

    def reliability_stats(self) -> ReliabilityStats:
        return self._dashboard_repository.reliability_stats()
