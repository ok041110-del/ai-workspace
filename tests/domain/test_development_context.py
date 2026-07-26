from ai_workspace.domain.development_context import DevelopmentContext


def test_to_prompt_returns_instructions_when_no_prior_output() -> None:
    context = DevelopmentContext(task_id="t1", instructions="구현하기")

    assert context.to_prompt() == "구현하기"


def test_to_prompt_includes_prior_output_when_present() -> None:
    context = DevelopmentContext(task_id="t1", instructions="검토하기", prior_output="def f(): ...")

    prompt = context.to_prompt()

    assert "검토하기" in prompt
    assert "def f(): ..." in prompt
