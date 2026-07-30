from ai_workspace.integration.vault_adapter import TaskDocumentView
from ai_workspace.intelligence.session_resume import CurrentWorkSelector


def _task(
    task_id: str,
    *,
    status: str = "in-progress",
    updated: str = "2026-07-30",
    archived: bool = False,
    milestone: str = "M33",
    owner: str = "AI",
) -> TaskDocumentView:
    return TaskDocumentView(
        task_id=task_id,
        title=f"{task_id} 제목",
        status=status,
        priority="high",
        milestone=milestone,
        owner=owner,
        created="2026-07-01",
        updated=updated,
        archived=archived,
    )


def test_select_returns_none_when_no_active_tasks() -> None:
    selector = CurrentWorkSelector()

    result = selector.select([_task("T33-01", status="done"), _task("T33-02", status="todo")])

    assert result is None


def test_select_picks_most_recently_updated_active_task() -> None:
    selector = CurrentWorkSelector()
    tasks = [
        _task("T33-01", status="in-progress", updated="2026-07-20"),
        _task("T33-02", status="review", updated="2026-07-30"),
        _task("T33-03", status="done", updated="2026-08-01"),
    ]

    result = selector.select(tasks)

    assert result is not None
    assert result.task_id == "T33-02"
    assert result.status == "review"


def test_select_breaks_ties_by_task_id() -> None:
    selector = CurrentWorkSelector()
    tasks = [
        _task("T33-02", status="in-progress", updated="2026-07-30"),
        _task("T33-01", status="in-progress", updated="2026-07-30"),
    ]

    result = selector.select(tasks)

    assert result is not None
    assert result.task_id == "T33-02"


def test_select_ignores_archived_tasks() -> None:
    selector = CurrentWorkSelector()
    tasks = [_task("T33-01", status="in-progress", updated="2026-07-30", archived=True)]

    result = selector.select(tasks)

    assert result is None
