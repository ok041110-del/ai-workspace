from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.integration.workflow_adapter import WorkflowAdapter


def _make_adapter() -> WorkflowAdapter:
    return WorkflowAdapter(InMemoryWorkflowEngine(), InMemoryTaskEngine())


def test_create_workflow_builds_domain_workflow() -> None:
    adapter = _make_adapter()

    workflow = adapter.create_workflow(
        "wf-1", "mission-1", ["a", "b"], {"b": {"a"}}
    )

    assert workflow.workflow_id == "wf-1"
    assert workflow.task_ids == ["a", "b"]


def test_plan_delegates_to_workflow_engine() -> None:
    adapter = _make_adapter()
    workflow = adapter.create_workflow("wf-1", "mission-1", ["a", "b"], {"b": {"a"}})

    order = adapter.plan(workflow)

    assert order == ["a", "b"]


def test_create_and_transition_task_delegates_to_task_engine() -> None:
    adapter = _make_adapter()

    task = adapter.create_task("project-1", "로그인 기능 구현")
    transitioned = adapter.transition_task(task, TaskStatus.IN_PROGRESS)

    assert transitioned.status is TaskStatus.IN_PROGRESS
    assert adapter.get_task(task.task_id).status is TaskStatus.IN_PROGRESS
