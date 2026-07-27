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
from ai_workspace.runtime.dashboard.dashboard_service import DashboardSnapshot

_ENGINE_DISPLAY_NAMES: dict[str, str] = {
    "claude_code": "Claude Code",
    "gemini_cli": "Gemini CLI",
    "codex_cli": "Codex CLI",
    "ollama": "Ollama",
}

_ENGINE_STATUS_LABELS: dict[EngineStatus, str] = {
    EngineStatus.READY: "준비 완료",
    EngineStatus.RUNNING: "실행 중",
    EngineStatus.AUTH_REQUIRED: "인증 필요",
    EngineStatus.ERROR: "오류",
}

_WORKSPACE_STATUS_LABELS: dict[str, str] = {
    "idle": "대기 중",
    "running": "실행 중",
}


def _engine_display_name(engine_name: str) -> str:
    return _ENGINE_DISPLAY_NAMES.get(engine_name, engine_name)


def _execution_result_label(record: ExecutionRecord) -> str:
    if record.success:
        return "성공"
    if record.cancelled:
        return "취소"
    if record.timed_out:
        return "시간 초과"
    return "실패"


@dataclass(frozen=True)
class WorkspaceStatusViewModel:
    """"Workspace 현황" 영역의 API 응답 전용 DTO(M20-T03). 표시 언어는
    한국어를 기본으로 한다(사용자 설계 원칙) — Engine 이름만 예외로
    영어를 유지한다. `started_at`은 그대로 넘긴다 — 경과 시간은
    브라우저가 `현재 시각 - started_at`으로 계산한다(이 계층은
    계산하지 않는다)."""

    project_name: str | None
    current_task_title: str | None
    status_label: str
    started_at: str | None


@dataclass(frozen=True)
class EngineStatusViewModel:
    name: str
    status_label: str


@dataclass(frozen=True)
class ExecutionHistoryEntryViewModel:
    executed_at: str
    engine: str
    result_label: str


@dataclass(frozen=True)
class DashboardViewModel:
    """`DashboardService`가 반환한 `DashboardSnapshot`(Provider 독립,
    영어/Enum 중심)을 API/WebSocket/Web UI가 그대로 내려줄 수 있는
    한국어 라벨 DTO로 변환한 결과(M20-T03). `DashboardService`는 이
    타입을 전혀 모른다 — 변환은 `web/` 계층의 책임이다."""

    workspace: WorkspaceStatusViewModel
    engines: list[EngineStatusViewModel]
    execution_stats: ExecutionStats
    recent_history: list[ExecutionHistoryEntryViewModel]
    reliability_stats: ReliabilityStats
    automation_status: AutomationStatus | None


def build_workspace_view_model(status: WorkspaceStatus) -> WorkspaceStatusViewModel:
    return WorkspaceStatusViewModel(
        project_name=status.project_name,
        current_task_title=status.current_task_title,
        status_label=_WORKSPACE_STATUS_LABELS.get(status.status, status.status),
        started_at=status.started_at,
    )


def build_engine_view_models(
    engine_statuses: dict[str, EngineStatus],
) -> list[EngineStatusViewModel]:
    return [
        EngineStatusViewModel(
            name=_engine_display_name(engine_name), status_label=_ENGINE_STATUS_LABELS[status]
        )
        for engine_name, status in engine_statuses.items()
    ]


def build_history_view_models(
    records: list[ExecutionRecord],
) -> list[ExecutionHistoryEntryViewModel]:
    return [
        ExecutionHistoryEntryViewModel(
            executed_at=record.executed_at,
            engine=_engine_display_name(record.engine),
            result_label=_execution_result_label(record),
        )
        for record in records
    ]


def build_dashboard_view_model(snapshot: DashboardSnapshot) -> DashboardViewModel:
    return DashboardViewModel(
        workspace=build_workspace_view_model(snapshot.workspace_status),
        engines=build_engine_view_models(snapshot.engine_statuses),
        execution_stats=snapshot.execution_stats,
        recent_history=build_history_view_models(snapshot.recent_executions),
        reliability_stats=snapshot.reliability_stats,
        automation_status=snapshot.automation_status,
    )
