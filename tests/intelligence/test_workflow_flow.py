from ai_workspace.integration.vault_adapter import TaskDocumentView
from ai_workspace.intelligence.workflow_flow import WorkflowFlowAnalyzer


def _task(
    task_id: str,
    *,
    status: str = "todo",
    milestone: str = "M34",
    archived: bool = False,
) -> TaskDocumentView:
    return TaskDocumentView(
        task_id=task_id,
        title=f"{task_id} 제목",
        status=status,
        priority="high",
        milestone=milestone,
        owner="AI",
        created="2026-07-01",
        updated="2026-07-30",
        archived=archived,
    )


def test_analyze_returns_no_milestones_when_no_tasks() -> None:
    analyzer = WorkflowFlowAnalyzer()

    report = analyzer.analyze([])

    assert report.milestones == []


def test_analyze_excludes_fully_completed_milestone() -> None:
    analyzer = WorkflowFlowAnalyzer()
    tasks = [_task("M34-T01", status="done"), _task("M34-T02", status="archived")]

    report = analyzer.analyze(tasks)

    assert report.milestones == []


def test_analyze_marks_earliest_incomplete_task_as_next() -> None:
    analyzer = WorkflowFlowAnalyzer()
    tasks = [
        _task("M34-T01", status="done"),
        _task("M34-T02", status="todo"),
        _task("M34-T03", status="todo"),
    ]

    report = analyzer.analyze(tasks)

    assert len(report.milestones) == 1
    milestone = report.milestones[0]
    assert milestone.milestone == "M34"
    states = {entry.task_id: entry.flow_state for entry in milestone.tasks}
    assert states == {"M34-T01": "done", "M34-T02": "next", "M34-T03": "blocked"}
    assert milestone.next_task_ids == ["M34-T02"]
    assert milestone.blocked_count == 1


def test_analyze_marks_all_tasks_after_predecessor_not_done_as_blocked() -> None:
    analyzer = WorkflowFlowAnalyzer()
    tasks = [
        _task("M34-T01", status="done"),
        _task("M34-T02", status="in-progress"),
        _task("M34-T03", status="todo"),
        _task("M34-T04", status="todo"),
    ]

    report = analyzer.analyze(tasks)

    milestone = report.milestones[0]
    states = {entry.task_id: entry.flow_state for entry in milestone.tasks}
    assert states == {
        "M34-T01": "done",
        "M34-T02": "in_progress",
        "M34-T03": "blocked",
        "M34-T04": "blocked",
    }
    assert milestone.next_task_ids == []


def test_analyze_orders_tasks_by_task_number_regardless_of_input_order() -> None:
    analyzer = WorkflowFlowAnalyzer()
    tasks = [_task("M34-T03", status="todo"), _task("M34-T01", status="todo")]

    report = analyzer.analyze(tasks)

    milestone = report.milestones[0]
    assert [entry.task_id for entry in milestone.tasks] == ["M34-T01", "M34-T03"]


def test_analyze_ignores_archived_tasks() -> None:
    analyzer = WorkflowFlowAnalyzer()
    tasks = [_task("M34-T01", status="todo", archived=True)]

    report = analyzer.analyze(tasks)

    assert report.milestones == []


def test_analyze_computes_completion_ratio() -> None:
    analyzer = WorkflowFlowAnalyzer()
    tasks = [
        _task("M34-T01", status="done"),
        _task("M34-T02", status="done"),
        _task("M34-T03", status="todo"),
    ]

    report = analyzer.analyze(tasks)

    milestone = report.milestones[0]
    assert milestone.completion_ratio == 2 / 3


def test_analyze_groups_multiple_milestones_independently() -> None:
    analyzer = WorkflowFlowAnalyzer()
    tasks = [
        _task("M34-T01", status="todo", milestone="M34"),
        _task("M35-T01", status="todo", milestone="M35"),
    ]

    report = analyzer.analyze(tasks)

    assert [milestone.milestone for milestone in report.milestones] == ["M34", "M35"]
    assert report.milestones[0].next_task_ids == ["M34-T01"]
    assert report.milestones[1].next_task_ids == ["M35-T01"]
