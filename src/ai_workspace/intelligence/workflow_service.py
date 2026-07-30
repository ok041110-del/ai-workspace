"""Intelligence Layer — Workflow Intelligence Service (ADR-0048, Milestone 34-T03~T04).

`VaultAdapter.list_tasks()`(기존) 조회와 `WorkflowFlowAnalyzer`
(M34-T02) 실행을 조합만 하는 Read Only 계층이다. Blocked/Next 판정
규칙 자체는 여기 두지 않는다 — 전부 Analyzer의 책임이다(ADR-0048
결정 3, M35/M36 재사용을 위한 분리)."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.workflow_flow import (
    MilestoneFlow,
    WorkflowFlowAnalyzer,
    WorkflowFlowReport,
)

_FLOW_STATE_LABELS = {
    "done": "완료",
    "in_progress": "진행 중",
    "blocked": "Blocked",
    "next": "Next(다음 실행 가능)",
}


class WorkflowIntelligenceService:
    """`VaultAdapter`(Task 조회) + `WorkflowFlowAnalyzer`(흐름 분석)를
    조합해 `WorkflowFlowReport`를 만든다."""

    def __init__(self, vault_adapter: VaultAdapter) -> None:
        self._vault_adapter = vault_adapter
        self._analyzer = WorkflowFlowAnalyzer()

    def generate(self, *, include_archived: bool = True) -> WorkflowFlowReport:
        """
        입력: include_archived(기본 True, `Archive/`의 완료 Task도
              조회 대상에 포함 — Analyzer가 이미 완료된 Milestone은
              스스로 걸러낸다)
        출력: `WorkflowFlowReport`(진행 중인 Milestone들의 Task 흐름)
        예외: 없음 — 진행 중인 Milestone이 없으면 빈 목록을 반환한다.
        보장: side-effect 없음(read-only).
        """
        tasks = self._vault_adapter.list_tasks(include_archived=include_archived)
        return self._analyzer.analyze(tasks)

    def publish(self, *, include_archived: bool = True) -> tuple[WorkflowFlowReport, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_workflow_intelligence()`에 위임).

        보장: `15 Project Intelligence/Workflow Intelligence.md`가
              이번 결과로 완전히 덮어써진다(누적 append 아님).
        """
        report = self.generate(include_archived=include_archived)
        markdown = render_markdown(report)
        path = self._vault_adapter.publish_workflow_intelligence(markdown)
        return report, path


def _render_milestone(milestone: MilestoneFlow) -> list[str]:
    lines = [
        f"## {milestone.milestone}",
        "",
        f"- 진행률: {milestone.completion_ratio:.0%}",
        f"- Blocked: {milestone.blocked_count}건",
        f"- Next(다음 실행 가능): {', '.join(milestone.next_task_ids) or '없음'}",
        "",
        "| Task | 상태 | 흐름 |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| {task.task_id}({task.title}) | {task.status} | "
        f"{_FLOW_STATE_LABELS.get(task.flow_state, task.flow_state)} |"
        for task in milestone.tasks
    )
    lines.append("")
    return lines


def render_markdown(report: WorkflowFlowReport) -> str:
    """`WorkflowFlowReport`를 Vault 문서 Markdown으로 렌더링한다.
    순수 함수(입출력 문자열 변환만, I/O 없음)."""
    lines = [
        "---",
        "tags: [workflow-intelligence]",
        "type: workflow-intelligence",
        "---",
        "",
        "# Workflow Intelligence",
        "",
        "> Milestone 34(Workflow Intelligence)가 Vault Task 문서의 "
        "Milestone별 실행 흐름을 분석해 만든 읽기 전용 문서다(ADR-0048). "
        "여기서 \"Workflow\"는 `domain.Workflow`가 아니라 Milestone 안의 "
        "Task 실행 순서를 가리킨다. 매 생성 시 이 문서 전체가 "
        "덮어써진다 — 편집해도 다음 생성 때 사라진다.",
        "",
    ]
    if not report.milestones:
        lines.append("현재 진행 중인 Milestone 없음(미완료 Task가 없거나 추적 중인 Task가 없음).")
        lines.append("")
        return "\n".join(lines)

    for milestone in report.milestones:
        lines.extend(_render_milestone(milestone))
    return "\n".join(lines)
