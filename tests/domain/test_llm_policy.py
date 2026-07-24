from ai_workspace.domain.llm_policy import INITIAL_MODELS, LLMEffort, LLMModel, LLMProvider


def test_llm_model_pairs_provider_and_name() -> None:
    model = LLMModel(provider=LLMProvider.ANTHROPIC, name="opus")

    assert model.provider == LLMProvider.ANTHROPIC
    assert model.name == "opus"


def test_initial_models_cover_all_providers() -> None:
    providers_in_initial_models = {model.provider for model in INITIAL_MODELS}

    assert providers_in_initial_models == set(LLMProvider)


def test_llm_effort_has_three_levels() -> None:
    assert {effort.value for effort in LLMEffort} == {"low", "medium", "high"}
