import pytest

from ai_workspace.domain.task import InvalidTaskTransitionError, TaskStatus
from ai_workspace.interfaces.task_engine import TaskNotFoundError

from .fakes import FakeTaskEngine


def test_create_task_starts_in_todo() -> None:
    engine = FakeTaskEngine()

    task = engine.create_task(project_id="p1", title="첫 Task")

    assert task.status == TaskStatus.TODO
    assert engine.get_task(task.task_id) == task


def test_create_task_rejects_empty_title() -> None:
    engine = FakeTaskEngine()

    with pytest.raises(ValueError):
        engine.create_task(project_id="p1", title="")


def test_transition_updates_status() -> None:
    engine = FakeTaskEngine()
    task = engine.create_task(project_id="p1", title="Task")

    updated = engine.transition(task, TaskStatus.IN_PROGRESS)

    assert updated.status == TaskStatus.IN_PROGRESS


def test_transition_rejects_invalid_move_without_mutating_task() -> None:
    engine = FakeTaskEngine()
    task = engine.create_task(project_id="p1", title="Task")

    with pytest.raises(InvalidTaskTransitionError):
        engine.transition(task, TaskStatus.DONE)

    assert task.status == TaskStatus.TODO


def test_get_unknown_task_raises_not_found() -> None:
    engine = FakeTaskEngine()

    with pytest.raises(TaskNotFoundError):
        engine.get_task("unknown")


def test_record_step_appears_in_get_steps() -> None:
    engine = FakeTaskEngine()
    task = engine.create_task(project_id="p1", title="Task")

    step = engine.record_step(task.task_id, "1차 시도 실패")

    assert engine.get_steps(task.task_id) == [step]


def test_get_steps_preserves_recording_order() -> None:
    engine = FakeTaskEngine()
    task = engine.create_task(project_id="p1", title="Task")

    first = engine.record_step(task.task_id, "1차")
    second = engine.record_step(task.task_id, "2차")

    assert engine.get_steps(task.task_id) == [first, second]


def test_get_steps_returns_empty_list_when_no_steps_recorded() -> None:
    engine = FakeTaskEngine()
    task = engine.create_task(project_id="p1", title="Task")

    assert engine.get_steps(task.task_id) == []


def test_record_step_unknown_task_raises_not_found() -> None:
    engine = FakeTaskEngine()

    with pytest.raises(TaskNotFoundError):
        engine.record_step("unknown", "설명")


def test_get_steps_unknown_task_raises_not_found() -> None:
    engine = FakeTaskEngine()

    with pytest.raises(TaskNotFoundError):
        engine.get_steps("unknown")


def test_get_steps_returns_defensive_copy() -> None:
    engine = FakeTaskEngine()
    task = engine.create_task(project_id="p1", title="Task")
    engine.record_step(task.task_id, "1차")

    steps = engine.get_steps(task.task_id)
    steps.clear()

    assert len(engine.get_steps(task.task_id)) == 1
