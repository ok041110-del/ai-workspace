import pytest

from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.workflow_repository import WorkflowNotFoundError
from ai_workspace.runtime.workflow.workflow_repository import InMemoryWorkflowRepository


def make_workflow(workflow_id: str = "w1") -> Workflow:
    return Workflow(workflow_id=workflow_id, mission_id="m1", task_ids=["t1", "t2"])


def test_save_then_get_returns_same_workflow() -> None:
    repository = InMemoryWorkflowRepository()
    workflow = make_workflow()

    repository.save(workflow)

    assert repository.get("w1") == workflow


def test_save_is_idempotent_upsert() -> None:
    repository = InMemoryWorkflowRepository()
    repository.save(make_workflow())

    updated = Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1"])
    repository.save(updated)

    assert repository.get("w1").task_ids == ["t1"]


def test_get_unknown_workflow_raises() -> None:
    repository = InMemoryWorkflowRepository()

    with pytest.raises(WorkflowNotFoundError):
        repository.get("missing")


def test_list_workflows_returns_all_saved_workflows() -> None:
    repository = InMemoryWorkflowRepository()
    repository.save(make_workflow("w1"))
    repository.save(make_workflow("w2"))

    workflows = repository.list_workflows()

    assert {workflow.workflow_id for workflow in workflows} == {"w1", "w2"}


def test_list_workflows_returns_defensive_copy() -> None:
    repository = InMemoryWorkflowRepository()
    repository.save(make_workflow())

    workflows = repository.list_workflows()
    workflows.clear()

    assert len(repository.list_workflows()) == 1
