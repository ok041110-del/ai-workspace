from ai_workspace.runtime.execution.recommendation_task_lifecycle import TaskLifecycleTransitioner


def test_decide_start_returns_in_progress_when_todo() -> None:
    transitioner = TaskLifecycleTransitioner()

    assert transitioner.decide_start("todo") == "in-progress"


def test_decide_start_returns_none_when_not_todo() -> None:
    transitioner = TaskLifecycleTransitioner()

    assert transitioner.decide_start("in-progress") is None
    assert transitioner.decide_start("review") is None
    assert transitioner.decide_start("done") is None


def test_decide_completion_returns_review_on_success_when_in_progress() -> None:
    transitioner = TaskLifecycleTransitioner()

    assert transitioner.decide_completion("in-progress", success=True) == "review"


def test_decide_completion_returns_todo_on_failure_when_in_progress() -> None:
    transitioner = TaskLifecycleTransitioner()

    assert transitioner.decide_completion("in-progress", success=False) == "todo"


def test_decide_completion_returns_none_when_not_in_progress() -> None:
    transitioner = TaskLifecycleTransitioner()

    assert transitioner.decide_completion("todo", success=True) is None
    assert transitioner.decide_completion("review", success=True) is None
    assert transitioner.decide_completion("done", success=False) is None
