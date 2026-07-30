"""Execution Layer — Recommendation Action Builder (ADR-0050, Milestone 36-T02).

승인된 M35 `NextAction`(`source=next_task`)을 `domain.automation.
Action(kind=RUN_TASK, ...)`으로 변환만 한다 — 승인 여부 판정은
`ExecutionGate`의 책임이다(ADR-0050 결정 3). M34 `WorkflowFlowReport`
가 이미 갖고 있는 Task 제목/Milestone 값만 재사용하고 새로운 데이터
접근 경로를 만들지 않는다."""

from __future__ import annotations

from ai_workspace.domain.automation import Action, ActionKind
from ai_workspace.intelligence.recommendation_rules import NextAction
from ai_workspace.intelligence.workflow_flow import WorkflowFlowReport


class NextTaskNotFoundError(ValueError):
    """`next_action.target`이 `workflow_report`에 없을 때 발생한다
    (Gate 승인과 Builder 호출 사이에 상태가 바뀐 방어적 경우)."""


class ActionBuilder:
    """승인된 `NextAction`을 `Action(kind=RUN_TASK)`로 변환하는 순수
    변환기. Milestone(Vault Task의 `milestone` 필드)을 `project_id`로
    그대로 재사용한다 — 이 저장소에 별도 project_id 데이터 소스가
    없기 때문(새 필드 추가 없음)."""

    def build(self, next_action: NextAction, workflow_report: WorkflowFlowReport) -> Action:
        """
        입력: `ExecutionGate`가 승인한 `NextAction`(`source=next_task`),
              같은 시점에 계산된 `WorkflowFlowReport`
        출력: `Action(kind=RUN_TASK, project_id=milestone,
              task_title=title)`
        예외: `NextTaskNotFoundError` — `next_action.target`이
              `workflow_report`에 없는 경우
        보장: side-effect 없음(read-only), 실행하지 않는다.
        """
        for milestone in workflow_report.milestones:
            for task in milestone.tasks:
                if task.task_id == next_action.target:
                    return Action(
                        kind=ActionKind.RUN_TASK,
                        project_id=milestone.milestone,
                        task_title=task.title,
                    )
        raise NextTaskNotFoundError(next_action.target)
