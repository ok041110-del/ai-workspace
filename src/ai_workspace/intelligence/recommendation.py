"""Intelligence Layer — Project Recommendation (ADR-0043, Milestone 29-T04).

`snapshot.ProjectSnapshotWithTasks`/`health_risk.ProjectHealthReport`
(M29-T02/T03 산출물)만 입력으로 받는 순수 Rule 기반 추천 계층이다.
Adapter를 직접 호출하지 않는다 — 새로운 데이터 접근 경로 없음. **AI
추론이나 LLM 호출은 포함하지 않는다**(사용자 지시 — Rule 기반만,
AI 추론은 M33(Planning Intelligence) 이후)."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.intelligence.health_risk import (
    RISK_MILESTONE_STALL,
    RISK_OWNER_OVERLOAD,
    RISK_STAGNANT_TASK,
    SEVERITY_CRITICAL,
    ProjectHealthReport,
    ProjectRisk,
)
from ai_workspace.intelligence.snapshot import ProjectSnapshotWithTasks

ACTION_UNBLOCK_TASK = "unblock_task"
ACTION_PRIORITIZE_TASK = "prioritize_task"
ACTION_REASSIGN_OWNER = "reassign_owner"
ACTION_ADVANCE_MILESTONE = "advance_milestone"
ACTION_IMPROVE_PROGRESS = "improve_progress"

PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"


@dataclass(frozen=True)
class ProjectRecommendation:
    action: str
    target: str
    reason: str
    priority: str


class ProjectRecommendationEngine:
    """Snapshot/Health/Risk를 입력으로 다음 행동을 추천하는 Rule 기반
    Engine. Risk 하나당 추천 하나를 1:1로 만들고(새 판단 기준을 따로
    만들지 않음), 전체 진행률이 낮을 때만 project 단위 추천을
    추가한다."""

    def __init__(self, *, low_progress_threshold: float = 0.3) -> None:
        self._low_progress_threshold = low_progress_threshold

    def recommend(
        self,
        snapshot_result: ProjectSnapshotWithTasks,
        health_report: ProjectHealthReport,
    ) -> list[ProjectRecommendation]:
        """
        입력: `ProjectSnapshotWithTasks`(T02), `ProjectHealthReport`(T03)
        출력: `ProjectRecommendation` 목록(우선순위 순서 보장 없음 —
              호출자가 `priority`로 정렬한다)
        예외: 없음
        보장: side-effect 없음(read-only), LLM 호출 없음.
        """
        recommendations = [
            recommendation
            for risk in health_report.risks
            if (recommendation := self._recommendation_for_risk(risk)) is not None
        ]

        snapshot = snapshot_result.snapshot
        if snapshot.total_tasks > 0 and snapshot.progress_ratio < self._low_progress_threshold:
            recommendations.append(
                ProjectRecommendation(
                    action=ACTION_IMPROVE_PROGRESS,
                    target="project",
                    reason=(
                        f"전체 진행률이 {snapshot.progress_ratio:.0%}로 임계값 "
                        f"{self._low_progress_threshold:.0%} 미만"
                    ),
                    priority=PRIORITY_MEDIUM,
                )
            )
        return recommendations

    def _recommendation_for_risk(self, risk: ProjectRisk) -> ProjectRecommendation | None:
        if risk.kind == RISK_STAGNANT_TASK:
            if risk.severity == SEVERITY_CRITICAL:
                return ProjectRecommendation(
                    action=ACTION_UNBLOCK_TASK,
                    target=risk.target,
                    reason=risk.detail,
                    priority=PRIORITY_HIGH,
                )
            return ProjectRecommendation(
                action=ACTION_PRIORITIZE_TASK,
                target=risk.target,
                reason=risk.detail,
                priority=PRIORITY_MEDIUM,
            )
        if risk.kind == RISK_OWNER_OVERLOAD:
            return ProjectRecommendation(
                action=ACTION_REASSIGN_OWNER,
                target=risk.target,
                reason=risk.detail,
                priority=PRIORITY_HIGH if risk.severity == SEVERITY_CRITICAL else PRIORITY_MEDIUM,
            )
        if risk.kind == RISK_MILESTONE_STALL:
            return ProjectRecommendation(
                action=ACTION_ADVANCE_MILESTONE,
                target=risk.target,
                reason=risk.detail,
                priority=PRIORITY_MEDIUM,
            )
        return None
