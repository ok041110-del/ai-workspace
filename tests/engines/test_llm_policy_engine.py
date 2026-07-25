import pytest

from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMEffort, LLMModel, LLMPolicyDecision, LLMProvider
from ai_workspace.engines.llm_policy_engine import InMemoryLLMPolicyEngine
from ai_workspace.interfaces.llm_policy_engine import PolicyNotFoundError


def test_select_returns_configured_decision() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    engine = InMemoryLLMPolicyEngine({AgentRole.CODING: decision})

    assert engine.select(AgentRole.CODING) == decision


def test_select_unknown_role_raises_policy_not_found() -> None:
    engine = InMemoryLLMPolicyEngine({})

    with pytest.raises(PolicyNotFoundError):
        engine.select(AgentRole.RESEARCH)


def test_rules_are_copied_defensively() -> None:
    decision = LLMPolicyDecision(model=LLMModel(LLMProvider.OPENAI, "gpt"), effort=LLMEffort.LOW)
    rules = {AgentRole.DOCUMENTATION: decision}
    engine = InMemoryLLMPolicyEngine(rules)
    rules[AgentRole.RESEARCH] = decision

    with pytest.raises(PolicyNotFoundError):
        engine.select(AgentRole.RESEARCH)
