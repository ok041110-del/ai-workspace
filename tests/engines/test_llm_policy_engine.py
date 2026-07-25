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
