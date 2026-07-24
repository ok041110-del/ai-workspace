import pytest

from ai_workspace.domain.task import InvalidTaskTransitionError, Task, TaskStatus


def make_task(status: TaskStatus = TaskStatus.TODO) -> Task:
    return Task(task_id="t1", project_id="p1", title="테스트 Task", status=status)


def test_task_defaults_to_todo() -> None:
    task = make_task()
    assert task.status == TaskStatus.TODO


def test_task_workflow_id_defaults_to_none() -> None:
    task = make_task()
    assert task.workflow_id is None


def test_task_can_be_linked_to_a_workflow() -> None:
    task = Task(
        task_id="t1", project_id="p1", title="테스트 Task", workflow_id="w1"
    )
    assert task.workflow_id == "w1"


def test_allowed_transition_succeeds() -> None:
    task = make_task()
    task.transition_to(TaskStatus.IN_PROGRESS)
    assert task.status == TaskStatus.IN_PROGRESS

    task.transition_to(TaskStatus.REVIEW)
    assert task.status == TaskStatus.REVIEW

    task.transition_to(TaskStatus.DONE)
    assert task.status == TaskStatus.DONE


def test_disallowed_transition_is_rejected() -> None:
    task = make_task(status=TaskStatus.DONE)

    with pytest.raises(InvalidTaskTransitionError):
        task.transition_to(TaskStatus.IN_PROGRESS)


def test_todo_cannot_jump_to_done() -> None:
    task = make_task(status=TaskStatus.TODO)

    with pytest.raises(InvalidTaskTransitionError):
        task.transition_to(TaskStatus.DONE)
