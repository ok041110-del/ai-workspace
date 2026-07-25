import pytest

from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.interfaces.task_engine import TaskNotFoundError


def test_create_task_starts_as_todo() -> None:
    engine = InMemoryTaskEngine()

    task = engine.create_task("p1", "구현하기")

    assert task.status == TaskStatus.TODO


def test_create_task_rejects_empty_project_id() -> None:
    engine = InMemoryTaskEngine()

    with pytest.raises(ValueError):
        engine.create_task("", "구현하기")


def test_create_task_rejects_empty_title() -> None:
    engine = InMemoryTaskEngine()

    with pytest.raises(ValueError):
        engine.create_task("p1", "")


def test_transition_updates_status() -> None:
    engine = InMemoryTaskEngine()
    task = engine.create_task("p1", "구현하기")

    engine.transition(task, TaskStatus.IN_PROGRESS)

    assert task.status == TaskStatus.IN_PROGRESS


def test_get_task_returns_latest_state() -> None:
    engine = InMemoryTaskEngine()
    task = engine.create_task("p1", "구현하기")
    engine.transition(task, TaskStatus.IN_PROGRESS)

    fetched = engine.get_task(task.task_id)

    assert fetched.status == TaskStatus.IN_PROGRESS


def test_get_task_unknown_raises_error() -> None:
    engine = InMemoryTaskEngine()

    with pytest.raises(TaskNotFoundError):
        engine.get_task("unknown")
