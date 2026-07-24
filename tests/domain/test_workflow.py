import pytest

from ai_workspace.domain.workflow import Workflow, WorkflowCycleError


def test_workflow_accepts_valid_dependencies() -> None:
    workflow = Workflow(
        workflow_id="w1",
        mission_id="m1",
        task_ids=["t1", "t2", "t3"],
        dependencies={"t2": {"t1"}, "t3": {"t2"}},
    )

    assert workflow.mission_id == "m1"
    assert workflow.task_ids == ["t1", "t2", "t3"]


def test_workflow_rejects_unknown_task_reference() -> None:
    with pytest.raises(ValueError):
        Workflow(
            workflow_id="w1",
            mission_id="m1",
            task_ids=["t1"],
            dependencies={"t1": {"unknown"}},
        )


def test_workflow_detects_direct_cycle() -> None:
    with pytest.raises(WorkflowCycleError):
        Workflow(
            workflow_id="w1",
            mission_id="m1",
            task_ids=["t1", "t2"],
            dependencies={"t1": {"t2"}, "t2": {"t1"}},
        )


def test_workflow_detects_self_cycle() -> None:
    with pytest.raises(WorkflowCycleError):
        Workflow(
            workflow_id="w1",
            mission_id="m1",
            task_ids=["t1"],
            dependencies={"t1": {"t1"}},
        )
