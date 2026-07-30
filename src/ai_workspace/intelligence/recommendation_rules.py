"""Intelligence Layer — Recommendation Rule Analyzer (ADR-0049, Milestone 35-T02).

새로운 Intelligence를 계산하지 않는다 — M29 `ProjectRecommendation`
(`intelligence/recommendation.py`), M31 `CapabilityGapReport`
(`intelligence/capability_gap.py`), M33 `CurrentWork`
(`intelligence/session_resume.py`), M34 `WorkflowFlowReport`
(`intelligence/workflow_flow.py`)가 이미 계산해 둔 값만 읽어, 순서대로
확인하다 첫 번째로 해당하는 조건에서 멈추는 5단계 Priority Rule
하나로 단일 `NextAction`을 고른다. 새 지표·점수·AI 추론 없음."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.intelligence.capability_gap import CapabilityGapReport
from ai_workspace.intelligence.recommendation import ProjectRecommendation
from ai_workspace.intelligence.session_resume import CurrentWork
from ai_workspace.intelligence.workflow_flow import WorkflowFlowReport

SOURCE_CURRENT_WORK = "current_work"
SOURCE_NEXT_TASK = "next_task"
SOURCE_BLOCKED_TASK = "blocked_task"
SOURCE_CAPABILITY_GAP = "capability_gap"
SOURCE_PROJECT_RECOMMENDATION = "project_recommendation"

ACTION_CONTINUE_CURRENT_WORK = "continue_current_work"
ACTION_START_NEXT_TASK = "start_next_task"
ACTION_RESOLVE_BLOCKER = "resolve_blocker"
ACTION_IMPROVE_CAPABILITY = "improve_capability"

#: M29 `ProjectRecommendation.priority` 정렬 순서(낮을수록 우선).
_PROJECT_PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


@dataclass(frozen=True)
class NextAction:
    """5단계 Priority Rule이 고른 단일 다음 행동."""

    source: str
    action: str
    target: str
    reason: str


class RecommendationRuleAnalyzer:
    """Current Work/Workflow Flow/Capability Gap/Project Recommendation
    을 순서대로 확인해 단일 `NextAction`을 고르는 Rule 기반 Analyzer.
    새 판단 기준이 아니라, 이미 계산된 4개 Intelligence 출력 중 무엇을
    지금 보여줄지 고르는 것뿐이다(ADR-0049)."""

    def analyze(
        self,
        *,
        current_work: CurrentWork | None,
        workflow_report: WorkflowFlowReport,
        capability_gap_report: CapabilityGapReport,
        project_recommendations: list[ProjectRecommendation],
    ) -> NextAction | None:
        """
        입력: M33 `CurrentWork`(또는 없음), M34 `WorkflowFlowReport`,
              M31 `CapabilityGapReport`, M29 `ProjectRecommendation`
              목록
        출력: 5단계 Priority 중 첫 번째로 해당하는 `NextAction`. 다섯
              조건 모두 해당 없으면 `None`.
        예외: 없음
        보장: side-effect 없음(read-only), 입력을 변경하지 않는다.
        """
        if current_work is not None:
            return NextAction(
                source=SOURCE_CURRENT_WORK,
                action=ACTION_CONTINUE_CURRENT_WORK,
                target=current_work.task_id,
                reason=f"현재 진행 중인 Task {current_work.task_id}({current_work.title})가 있음",
            )

        next_task = self._find_next_task(workflow_report)
        if next_task is not None:
            milestone, task_id, title = next_task
            return NextAction(
                source=SOURCE_NEXT_TASK,
                action=ACTION_START_NEXT_TASK,
                target=task_id,
                reason=f"{milestone}의 선행 Task가 모두 완료돼 {task_id}({title})를 시작 가능",
            )

        blocked_task = self._find_blocked_task(workflow_report)
        if blocked_task is not None:
            milestone, task_id, title = blocked_task
            return NextAction(
                source=SOURCE_BLOCKED_TASK,
                action=ACTION_RESOLVE_BLOCKER,
                target=task_id,
                reason=f"{milestone}의 {task_id}({title})가 선행 Task 미완료로 진행 불가",
            )

        if capability_gap_report.gaps:
            gap = capability_gap_report.gaps[0]
            return NextAction(
                source=SOURCE_CAPABILITY_GAP,
                action=ACTION_IMPROVE_CAPABILITY,
                target=gap.capability,
                reason=gap.detail,
            )

        if project_recommendations:
            top = min(
                project_recommendations,
                key=lambda r: (_PROJECT_PRIORITY_RANK.get(r.priority, 99), r.target),
            )
            return NextAction(
                source=SOURCE_PROJECT_RECOMMENDATION,
                action=top.action,
                target=top.target,
                reason=top.reason,
            )

        return None

    def _find_next_task(self, workflow_report: WorkflowFlowReport) -> tuple[str, str, str] | None:
        for milestone in workflow_report.milestones:
            for task in milestone.tasks:
                if task.flow_state == "next":
                    return milestone.milestone, task.task_id, task.title
        return None

    def _find_blocked_task(
        self, workflow_report: WorkflowFlowReport
    ) -> tuple[str, str, str] | None:
        for milestone in workflow_report.milestones:
            for task in milestone.tasks:
                if task.flow_state == "blocked":
                    return milestone.milestone, task.task_id, task.title
        return None
