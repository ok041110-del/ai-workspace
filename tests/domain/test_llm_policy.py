from ai_workspace.domain.llm_policy import (
    INITIAL_MODELS,
    LLMEffort,
    LLMModel,
    LLMPolicyDecision,
    LLMProvider,
    required_capabilities,
)


def test_llm_model_pairs_provider_and_name() -> None:
    model = LLMModel(provider=LLMProvider.ANTHROPIC, name="opus")

    assert model.provider == LLMProvider.ANTHROPIC
    assert model.name == "opus"


def test_initial_models_cover_all_providers() -> None:
    providers_in_initial_models = {model.provider for model in INITIAL_MODELS}

    assert providers_in_initial_models == set(LLMProvider)


def test_llm_effort_has_three_levels() -> None:
    assert {effort.value for effort in LLMEffort} == {"low", "medium", "high"}


def test_required_capabilities_returns_empty_set_when_no_decision() -> None:
    """M6-T02: 정책이 없으면(Role 규칙 없음/LLMPolicyEngine 미주입) 빈
    집합을 반환해 EngineRuntime.run()의 기존 동작(제약 없음)과 하위
    호환된다."""
    assert required_capabilities(None) == frozenset()


def test_required_capabilities_maps_anthropic_to_claude_code() -> None:
    decision = LLMPolicyDecision(LLMModel(LLMProvider.ANTHROPIC, "opus"), LLMEffort.HIGH)

    assert required_capabilities(decision) == frozenset({"claude_code"})


def test_required_capabilities_maps_openai_to_codex() -> None:
    decision = LLMPolicyDecision(LLMModel(LLMProvider.OPENAI, "gpt"), LLMEffort.MEDIUM)

    assert required_capabilities(decision) == frozenset({"codex"})


def test_required_capabilities_maps_google_to_gemini() -> None:
    decision = LLMPolicyDecision(LLMModel(LLMProvider.GOOGLE, "gemini"), LLMEffort.LOW)

    assert required_capabilities(decision) == frozenset({"gemini"})


def test_required_capabilities_maps_all_providers_without_error() -> None:
    """모든 LLMProvider 값에 대해 매핑이 정의되어 있어야 한다(XAI처럼
    대응 EngineAdapter가 아직 없는 Provider도 태그 자체는 반환하고,
    실제 매칭 실패는 EngineRuntime.run()의 NoSuitableEngineError로
    처리하는 것이 의도된 동작)."""
    for provider in LLMProvider:
        decision = LLMPolicyDecision(LLMModel(provider, "model"), LLMEffort.LOW)

        assert len(required_capabilities(decision)) == 1
