from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMEffort, LLMModel, LLMPolicyDecision, LLMProvider
from ai_workspace.engines.llm_policy_engine import InMemoryLLMPolicyEngine


def test_select_returns_configured_decision() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    engine = InMemoryLLMPolicyEngine({AgentRole.CODING: decision})

    assert engine.select(AgentRole.CODING) == decision


def test_select_unknown_role_returns_none() -> None:
    engine = InMemoryLLMPolicyEngine({})

    assert engine.select(AgentRole.RESEARCH) is None


def test_rules_are_copied_defensively() -> None:
    decision = LLMPolicyDecision(model=LLMModel(LLMProvider.OPENAI, "gpt"), effort=LLMEffort.LOW)
    rules = {AgentRole.DOCUMENTATION: decision}
    engine = InMemoryLLMPolicyEngine(rules)
    rules[AgentRole.RESEARCH] = decision

    assert engine.select(AgentRole.RESEARCH) is None


def test_record_outcome_alone_does_not_change_selection() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    engine = InMemoryLLMPolicyEngine({AgentRole.CODING: decision})

    engine.record_outcome(AgentRole.CODING, decision, True)
    engine.record_outcome(AgentRole.CODING, decision, False)

    assert engine.select(AgentRole.CODING) == decision


def test_select_falls_back_to_next_model_when_unreliable() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    engine = InMemoryLLMPolicyEngine({AgentRole.CODING: decision})

    for _ in range(3):
        engine.record_outcome(AgentRole.CODING, decision, False)

    fallback = engine.select(AgentRole.CODING)

    assert fallback == LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "sonnet"), effort=LLMEffort.HIGH
    )


def test_select_does_not_fall_back_with_insufficient_failures() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    engine = InMemoryLLMPolicyEngine({AgentRole.CODING: decision})

    for _ in range(2):
        engine.record_outcome(AgentRole.CODING, decision, False)

    assert engine.select(AgentRole.CODING) == decision


def test_select_does_not_fall_back_with_at_least_one_success() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    engine = InMemoryLLMPolicyEngine({AgentRole.CODING: decision})

    engine.record_outcome(AgentRole.CODING, decision, True)
    for _ in range(5):
        engine.record_outcome(AgentRole.CODING, decision, False)

    assert engine.select(AgentRole.CODING) == decision


def test_fallback_can_advance_multiple_times_along_initial_models() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    engine = InMemoryLLMPolicyEngine({AgentRole.CODING: decision})

    for _ in range(3):
        engine.record_outcome(AgentRole.CODING, decision, False)
    sonnet_decision = engine.select(AgentRole.CODING)
    assert sonnet_decision is not None
    for _ in range(3):
        engine.record_outcome(AgentRole.CODING, sonnet_decision, False)

    haiku_decision = engine.select(AgentRole.CODING)

    assert haiku_decision == LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "haiku"), effort=LLMEffort.HIGH
    )


def test_fallback_stops_at_last_initial_model() -> None:
    decision = LLMPolicyDecision(model=LLMModel(LLMProvider.XAI, "grok"), effort=LLMEffort.LOW)
    engine = InMemoryLLMPolicyEngine({AgentRole.CODING: decision})

    for _ in range(3):
        engine.record_outcome(AgentRole.CODING, decision, False)

    assert engine.select(AgentRole.CODING) == decision


def test_other_roles_are_unaffected_by_a_role_becoming_unreliable() -> None:
    coding_decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    review_decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.MEDIUM
    )
    engine = InMemoryLLMPolicyEngine(
        {AgentRole.CODING: coding_decision, AgentRole.REVIEWER: review_decision}
    )

    for _ in range(3):
        engine.record_outcome(AgentRole.CODING, coding_decision, False)

    assert engine.select(AgentRole.REVIEWER) == review_decision
