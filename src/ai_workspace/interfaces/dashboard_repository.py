from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.dashboard import (
    EngineStatus,
    ExecutionRecord,
    ExecutionStats,
    ReliabilityStats,
    WorkspaceStatus,
)


class DashboardRepository(ABC):
    """Dashboard의 Read Model을 저장·조회하는 계약(M20-T01, CQRS).
    이 계약은 `EventBus`를 알지 못한다 — Event를 구독해 이 계약의
    쓰기 메서드를 호출하는 것은 구체 구현체(`InMemoryDashboardRepository`,
    M20-T02)의 책임이다. `DashboardService`(M20-T03)는 조회 메서드만
    사용한다."""

    @abstractmethod
    def record_execution_started(
        self, *, engine_name: str, task_title: str, started_at: str
    ) -> None:
        """
        입력: engine_name, task_title(현재 실행 중인 작업), started_at
              (ISO 8601 문자열)
        출력: 없음
        예외: 없음
        보장: 호출 이후 `workspace_status()`가 이 정보를 반영하고,
              `engine_statuses()`의 해당 engine_name이 RUNNING이 된다.
        """
        raise NotImplementedError

    @abstractmethod
    def record_execution_completed(self, record: ExecutionRecord) -> None:
        """
        입력: record (완료된 실행 하나)
        출력: 없음
        예외: 없음
        보장: 호출 이후 `recent_executions()`/`execution_stats()`/
              `reliability_stats()`에 반영된다. 진행 중이던
              `workspace_status()`는 해제된다(started_at=None).
        """
        raise NotImplementedError

    @abstractmethod
    def record_authentication_failure(self, *, engine_name: str) -> None:
        """
        입력: engine_name (인증 실패로 실행되지 못한 Engine)
        출력: 없음
        예외: 없음
        보장: 호출 이후 `engine_statuses()`의 해당 engine_name이
              AUTH_REQUIRED가 되고, `reliability_stats().
              authentication_failure_count`가 증가한다.
        """
        raise NotImplementedError

    @abstractmethod
    def workspace_status(self) -> WorkspaceStatus:
        """
        입력: 없음
        출력: 현재 Workspace 현황
        예외: 없음
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError

    @abstractmethod
    def engine_statuses(self) -> dict[str, EngineStatus]:
        """
        입력: 없음
        출력: engine_name -> EngineStatus 매핑(기록된 적 없는 Engine은
              포함되지 않는다)
        예외: 없음
        보장: side-effect 없음(read-only). 반환된 dict를 호출자가
              수정해도 내부 상태는 변하지 않는다(방어적 복사).
        """
        raise NotImplementedError

    @abstractmethod
    def recent_executions(self, limit: int = 20) -> list[ExecutionRecord]:
        """
        입력: limit (반환할 최대 개수)
        출력: 가장 최근 실행부터 최대 limit개(없으면 빈 리스트)
        예외: 없음
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError

    @abstractmethod
    def execution_stats(self) -> ExecutionStats:
        """
        입력: 없음
        출력: 누적 실행 통계
        예외: 없음
        보장: side-effect 없음(read-only). 통계는 미리 계산돼 있으며
              이 메서드는 계산하지 않고 그대로 반환한다.
        """
        raise NotImplementedError

    @abstractmethod
    def reliability_stats(self) -> ReliabilityStats:
        """
        입력: 없음
        출력: 누적 안정성 통계
        예외: 없음
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError
