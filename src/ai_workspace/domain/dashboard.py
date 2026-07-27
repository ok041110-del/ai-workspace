from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EngineStatus(Enum):
    """Dashboard가 표시하는 Engine 상태(M20-T01). Provider 독립 — 상태
    문자열의 한국어 라벨은 이 계층이 아니라 `DashboardViewModel`
    (`web/` 계층)의 책임이다."""

    READY = "ready"
    RUNNING = "running"
    AUTH_REQUIRED = "auth_required"
    ERROR = "error"


@dataclass(frozen=True)
class WorkspaceStatus:
    """"Workspace 현황" 영역의 Read Model(M20-T01). `started_at`이
    `None`이 아니면 현재 실행 중인 작업이 있다는 뜻이다 — 경과 시간은
    브라우저가 `현재 시각 - started_at`으로 직접 계산한다(Dashboard가
    계산하지 않음, Polling 없음)."""

    project_name: str | None
    current_task_title: str | None
    status: str
    started_at: str | None


@dataclass(frozen=True)
class ExecutionRecord:
    """"최근 실행 내역" 영역의 항목 하나(M20-T01). `EngineExecutionResult`
    (M18/M19)를 그대로 참조하지 않고 Dashboard가 필요한 필드만
    옮겨 담는다 — Dashboard는 Execution 계층에 대한 쓰기 접근이 없는
    순수 Read Model이다(CQRS)."""

    executed_at: str
    engine: str
    success: bool
    cancelled: bool
    timed_out: bool
    retry_count: int
    error: str | None


@dataclass(frozen=True)
class ExecutionStats:
    """"실행 현황" 영역의 Read Model(M20-T01). Dashboard는 이 값을
    직접 계산하지 않고 `DashboardRepository`가 제공하는 값을 그대로
    쓴다."""

    total: int
    success: int
    failure: int
    cancelled: int
    timed_out: int


@dataclass(frozen=True)
class ReliabilityStats:
    """"안정성 현황" 영역의 Read Model(M20-T01, M19 Reliability Layer의
    결과를 집계)."""

    retry_count: int
    timeout_count: int
    cancelled_count: int
    authentication_failure_count: int
