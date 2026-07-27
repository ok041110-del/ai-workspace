from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.domain.dashboard import (
    AutomationStatus,
    EngineStatus,
    ExecutionRecord,
    ExecutionStats,
    ReliabilityStats,
    WorkspaceStatus,
)
from ai_workspace.interfaces.dashboard_repository import DashboardRepository
from ai_workspace.runtime.automation.automation_service import AutomationService

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
    automation_status: AutomationStatus | None = None


class DashboardService:
    """`DashboardRepository`의 Read Model을 조합해 Dashboard 조회
    요청에 응답하는 서비스(M20-T03). **UI를 전혀 모른다** — `web/`
    계층(API/WebSocket/Web UI)을 import하지 않는다(M20-T06에서
    Architecture 의존성 검증으로 증명). 통계를 스스로 계산하지 않고
    `DashboardRepository`가 이미 계산해 둔 값을 그대로 전달한다.

    `automation_service`는 선택적으로 주입한다(M21-T05, M15
    `budget_policy_engine`/M16 `knowledge_provider`와 동일한 선택적
    DI 패턴) — Automation Rule 개수/마지막·다음 실행 시각을 조회해
    표시하기 위함이다. `AutomationService.list_rules()`(읽기 전용)만
    호출하고 Automation을 제어하지 않는다(사용자 승인 조건 4).
    미주입 시 `automation_status()`는 `None`을 반환한다."""

    def __init__(
        self,
        *,
        dashboard_repository: DashboardRepository,
        automation_service: AutomationService | None = None,
    ) -> None:
        self._dashboard_repository = dashboard_repository
        self._automation_service = automation_service

    def snapshot(self) -> DashboardSnapshot:
        return DashboardSnapshot(
            workspace_status=self.workspace_status(),
            engine_statuses=self.engine_statuses(),
            execution_stats=self.execution_stats(),
            recent_executions=self.recent_executions(),
            reliability_stats=self.reliability_stats(),
            automation_status=self.automation_status(),
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

    def automation_status(self) -> AutomationStatus | None:
        if self._automation_service is None:
            return None
        rules = self._automation_service.list_rules()
        enabled_rules = [rule for rule in rules if rule.enabled]
        last_executions = [rule.last_executed_at for rule in rules if rule.last_executed_at]
        next_executions = [
            rule.next_execution_at for rule in enabled_rules if rule.next_execution_at
        ]
        return AutomationStatus(
            registered_rule_count=len(rules),
            enabled_rule_count=len(enabled_rules),
            last_execution_at=max(last_executions) if last_executions else None,
            next_execution_at=min(next_executions) if next_executions else None,
        )
