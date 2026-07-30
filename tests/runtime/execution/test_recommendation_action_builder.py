import pytest

from ai_workspace.domain.automation import ActionKind
from ai_workspace.intelligence.recommendation_rules import (
    ACTION_START_NEXT_TASK,
    SOURCE_NEXT_TASK,
    NextAction,
)
from ai_workspace.intelligence.workflow_flow import MilestoneFlow, TaskFlowEntry, WorkflowFlowReport
from ai_workspace.runtime.execution.recommendation_action_builder import (
    ActionBuilder,
    NextTaskNotFoundError,
)

_WORKFLOW_REPORT = WorkflowFlowReport(
    milestones=[
        MilestoneFlow(
            milestone="M36",
            tasks=[
                TaskFlowEntry(task_id="M36-T01", title="설계", status="done", flow_state="done"),
                TaskFlowEntry(task_id="M36-T02", title="Gate", status="todo", flow_state="next"),
            ],
        )
    ]
)


def test_build_converts_next_task_action_to_run_task_action() -> None:
    builder = ActionBuilder()
    next_action = NextAction(
        source=SOURCE_NEXT_TASK, action=ACTION_START_NEXT_TASK, target="M36-T02", reason="r"
    )

    action = builder.build(next_action, _WORKFLOW_REPORT)

    assert action.kind == ActionKind.RUN_TASK
    assert action.project_id == "M36"
    assert action.task_title == "Gate"


def test_build_raises_when_target_not_found() -> None:
    builder = ActionBuilder()
    next_action = NextAction(
        source=SOURCE_NEXT_TASK, action=ACTION_START_NEXT_TASK, target="M99-T01", reason="r"
    )

    with pytest.raises(NextTaskNotFoundError):
        builder.build(next_action, _WORKFLOW_REPORT)
