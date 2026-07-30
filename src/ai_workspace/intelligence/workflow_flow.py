"""Intelligence Layer — Workflow Flow Analyzer (ADR-0048, Milestone 34-T02).

여기서 "Workflow"는 `domain.Workflow`(휘발성 in-memory DAG, 영속
저장소 없음)가 아니라 **Milestone 안의 Task 실행 순서**를 가리킨다
(ADR-0048) — `VaultAdapter.list_tasks()`(M29부터 존재)가 이미
노출한 `task_id`/`status`/`milestone` 값만 읽는 순수 함수 계층이다.
새로운 데이터 접근 경로도, 새로운 지표·점수도 만들지 않는다."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ai_workspace.integration.vault_adapter import TaskDocumentView

#: "완료"로 취급하는 상태(다른 Intelligence 모듈과 동일한 집합을
#: 재사용 — 새 상태 분류를 만들지 않는다).
_COMPLETED_STATUSES = frozenset({"done", "archived"})
#: "진행 중"으로 취급하는 상태.
_IN_PROGRESS_STATUSES = frozenset({"in-progress", "review"})

_ORDER_PATTERN = re.compile(r"-T(\d+)$")


def _task_order(task_id: str) -> int:
    """Task ID(`M{n}-T{nn}`)에서 T-번호를 추출한다. 형식이 다르면
    정렬 시 맨 뒤로 밀리도록 매우 큰 값을 반환한다."""
    match = _ORDER_PATTERN.search(task_id)
    if match is None:
        return 1 << 30
    return int(match.group(1))


@dataclass(frozen=True)
class TaskFlowEntry:
    """Milestone 흐름 안에서 Task 한 건의 읽기 전용 뷰."""

    task_id: str
    title: str
    status: str
    flow_state: str  # "done" | "in_progress" | "blocked" | "next"


@dataclass(frozen=True)
class MilestoneFlow:
    """하나의 Milestone에 속한 Task들의 실행 흐름."""

    milestone: str
    tasks: list[TaskFlowEntry]

    @property
    def blocked_count(self) -> int:
        return sum(1 for task in self.tasks if task.flow_state == "blocked")

    @property
    def next_task_ids(self) -> list[str]:
        return [task.task_id for task in self.tasks if task.flow_state == "next"]

    @property
    def completion_ratio(self) -> float:
        if not self.tasks:
            return 0.0
        done = sum(1 for task in self.tasks if task.flow_state == "done")
        return done / len(self.tasks)


@dataclass(frozen=True)
class WorkflowFlowReport:
    """전체 Milestone 흐름 분석 결과. 미완료 Task가 하나도 없는(=이미
    완전히 끝난) Milestone은 포함하지 않는다 — "진행 중" 흐름만
    보여준다."""

    milestones: list[MilestoneFlow]


class WorkflowFlowAnalyzer:
    """Vault Task 목록에서 Milestone별 Task 실행 흐름(Blocked/Next
    판정 포함)을 계산하는 Read Only Analyzer. 새 판단 기준이 아니라,
    이미 있는 `task_id`/`status`/`milestone` 값에서 흐름을 재구성할
    뿐이다(ADR-0048)."""

    def analyze(self, tasks: list[TaskDocumentView]) -> WorkflowFlowReport:
        """
        입력: `VaultAdapter.list_tasks()`가 반환한 Task 목록
        출력: 미완료 Task가 있는 Milestone만 모은 `WorkflowFlowReport`
              (각 Milestone은 T-번호 순으로 정렬된 Task 목록 포함)
        예외: 없음
        보장: side-effect 없음(read-only), 입력 목록을 변경하지 않는다.
        """
        by_milestone: dict[str, list[TaskDocumentView]] = {}
        for task in tasks:
            if not task.milestone or task.archived:
                continue
            by_milestone.setdefault(task.milestone, []).append(task)

        milestones: list[MilestoneFlow] = []
        for milestone in sorted(by_milestone):
            ordered = sorted(by_milestone[milestone], key=lambda task: _task_order(task.task_id))
            if all(task.status in _COMPLETED_STATUSES for task in ordered):
                continue

            entries: list[TaskFlowEntry] = []
            blocked_by_predecessor = False
            for task in ordered:
                if task.status in _COMPLETED_STATUSES:
                    flow_state = "done"
                elif task.status in _IN_PROGRESS_STATUSES:
                    flow_state = "in_progress"
                elif blocked_by_predecessor:
                    flow_state = "blocked"
                else:
                    flow_state = "next"
                entries.append(
                    TaskFlowEntry(
                        task_id=task.task_id,
                        title=task.title,
                        status=task.status,
                        flow_state=flow_state,
                    )
                )
                if task.status not in _COMPLETED_STATUSES:
                    blocked_by_predecessor = True

            milestones.append(MilestoneFlow(milestone=milestone, tasks=entries))

        return WorkflowFlowReport(milestones=milestones)
