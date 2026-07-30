"""Intelligence Layer — Project Health & Risk Analyzer (ADR-0043, Milestone 29-T03).

`snapshot.ProjectSnapshotWithTasks`(M29-T02 산출물)만 입력으로 받는
순수 Rule 기반 판단 계층이다 — Adapter를 직접 호출하지 않는다(이미
Snapshot 단계에서 읽어온 값만 재사용, 새로운 데이터 접근 경로 없음).
AI 추론/LLM 호출은 하지 않는다(사용자 지시 — Rule 기반만, AI 추론은
M33 이후)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date as date_cls

from ai_workspace.intelligence.snapshot import ProjectSnapshotWithTasks, TaskSnapshotEntry

#: 활성 작업으로 취급하는 Vault Task 상태(ADR-0043 — Vault에는
#: Core Domain TaskStatus.BLOCKED에 대응하는 값이 없어, 이 상태로
#: 오래 머무는 것을 "정체(Stagnant)"로 근사한다).
_ACTIVE_STATUSES = frozenset({"in-progress", "review"})
_COMPLETED_STATUSES = frozenset({"done", "archived"})

#: Risk 종류(Interface/Domain Enum이 아니라 이 모듈 안의 문자열
#: 상수 — intelligence/는 domain을 직접 참조하지 않는다).
RISK_STAGNANT_TASK = "stagnant_task"
RISK_OWNER_OVERLOAD = "owner_overload"
RISK_MILESTONE_STALL = "milestone_stall"

HEALTH_HEALTHY = "healthy"
HEALTH_WARNING = "warning"
HEALTH_CRITICAL = "critical"

SEVERITY_WARNING = "warning"
SEVERITY_CRITICAL = "critical"


@dataclass(frozen=True)
class ProjectRisk:
    kind: str
    target: str
    detail: str
    severity: str


@dataclass(frozen=True)
class ProjectHealth:
    level: str
    reasons: list[str]


@dataclass(frozen=True)
class ProjectHealthReport:
    health: ProjectHealth
    risks: list[ProjectRisk]


def _parse_date(value: str) -> date_cls | None:
    try:
        return date_cls.fromisoformat(value)
    except ValueError:
        return None


class ProjectHealthRiskAnalyzer:
    """Project Snapshot을 입력으로 Health/Risk를 계산하는 Rule 기반
    Analyzer. 임계값은 생성자 파라미터로 조정 가능하다(기본값은 이
    프로젝트의 하루~1주 단위 작업 리듬을 가정한 보수적인 값)."""

    def __init__(
        self,
        *,
        stagnant_days_threshold: int = 7,
        owner_overload_threshold: int = 3,
    ) -> None:
        self._stagnant_days_threshold = stagnant_days_threshold
        self._owner_overload_threshold = owner_overload_threshold

    def analyze(
        self, result: ProjectSnapshotWithTasks, *, today: str | None = None
    ) -> ProjectHealthReport:
        """
        입력: `ProjectSnapshotWithTasks`(M29-T02 산출물), today(고정
              날짜 주입용, 기본값은 오늘 날짜)
        출력: `ProjectHealthReport`(Health 판정 + Risk 목록)
        예외: 없음 — `updated` 필드가 없거나 파싱 불가능한 Task는
              정체 판정에서 조용히 건너뛴다(방어적, 판단 중단하지
              않음).
        보장: side-effect 없음(read-only), Snapshot을 변경하지 않는다.
        """
        today_date = _parse_date(today) if today else date_cls.today()
        if today_date is None:
            today_date = date_cls.today()

        risks: list[ProjectRisk] = []
        risks.extend(self._stagnant_task_risks(result.tasks, today_date))
        risks.extend(self._owner_overload_risks(result.tasks))
        risks.extend(self._milestone_stall_risks(result.tasks, today_date))

        health = self._determine_health(risks)
        return ProjectHealthReport(health=health, risks=risks)

    def _stagnant_task_risks(
        self, tasks: list[TaskSnapshotEntry], today_date: date_cls
    ) -> list[ProjectRisk]:
        risks: list[ProjectRisk] = []
        for task in tasks:
            if task.status not in _ACTIVE_STATUSES:
                continue
            updated_date = _parse_date(task.updated)
            if updated_date is None:
                continue
            idle_days = (today_date - updated_date).days
            if idle_days < self._stagnant_days_threshold:
                continue
            severity = (
                SEVERITY_CRITICAL
                if idle_days >= self._stagnant_days_threshold * 2
                else SEVERITY_WARNING
            )
            risks.append(
                ProjectRisk(
                    kind=RISK_STAGNANT_TASK,
                    target=task.task_id,
                    detail=(
                        f"{task.task_id}({task.title})가 {task.status} 상태로 "
                        f"{idle_days}일째 정체(Blocked/장기 미진행 근사)"
                    ),
                    severity=severity,
                )
            )
        return risks

    def _owner_overload_risks(self, tasks: list[TaskSnapshotEntry]) -> list[ProjectRisk]:
        active_counts: dict[str, int] = {}
        for task in tasks:
            if task.status not in _ACTIVE_STATUSES or not task.owner:
                continue
            active_counts[task.owner] = active_counts.get(task.owner, 0) + 1

        risks: list[ProjectRisk] = []
        for owner, count in active_counts.items():
            if count < self._owner_overload_threshold:
                continue
            severity = (
                SEVERITY_CRITICAL
                if count >= self._owner_overload_threshold * 2
                else SEVERITY_WARNING
            )
            risks.append(
                ProjectRisk(
                    kind=RISK_OWNER_OVERLOAD,
                    target=owner,
                    detail=f"{owner}에게 진행 중(in-progress/review) Task {count}건 배정",
                    severity=severity,
                )
            )
        return risks

    def _milestone_stall_risks(
        self, tasks: list[TaskSnapshotEntry], today_date: date_cls
    ) -> list[ProjectRisk]:
        by_milestone: dict[str, list[TaskSnapshotEntry]] = {}
        for task in tasks:
            if not task.milestone:
                continue
            by_milestone.setdefault(task.milestone, []).append(task)

        risks: list[ProjectRisk] = []
        for milestone, milestone_tasks in by_milestone.items():
            if any(task.status in _COMPLETED_STATUSES for task in milestone_tasks):
                continue
            updated_dates = [
                parsed
                for task in milestone_tasks
                if (parsed := _parse_date(task.updated)) is not None
            ]
            if not updated_dates:
                continue
            most_recent = max(updated_dates)
            idle_days = (today_date - most_recent).days
            if idle_days < self._stagnant_days_threshold:
                continue
            risks.append(
                ProjectRisk(
                    kind=RISK_MILESTONE_STALL,
                    target=milestone,
                    detail=(
                        f"{milestone}에 완료(done/archived)된 Task가 없고 "
                        f"{idle_days}일째 갱신 없음(Workflow 정체 근사)"
                    ),
                    severity=SEVERITY_WARNING,
                )
            )
        return risks

    def _determine_health(self, risks: list[ProjectRisk]) -> ProjectHealth:
        if any(risk.severity == SEVERITY_CRITICAL for risk in risks):
            level = HEALTH_CRITICAL
        elif risks:
            level = HEALTH_WARNING
        else:
            level = HEALTH_HEALTHY
        reasons = [risk.detail for risk in risks]
        return ProjectHealth(level=level, reasons=reasons)
