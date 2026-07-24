from ai_workspace.domain.step import Step


def test_step_holds_task_reference_and_description() -> None:
    step = Step(step_id="s1", task_id="t1", description="파일 읽기")

    assert step.task_id == "t1"
    assert step.description == "파일 읽기"
