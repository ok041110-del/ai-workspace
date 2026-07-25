import pytest

from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMEffort, LLMModel, LLMPolicyDecision, LLMProvider
from ai_workspace.interfaces.llm_policy_engine import PolicyNotFoundError

from .fakes import FakeLLMPolicyEngine


def test_select_returns_configured_decision() -> None:
    decision = LLMPolicyDecision(
        model=LLMModel(LLMProvider.ANTHROPIC, "opus"), effort=LLMEffort.HIGH
    )
    engine = FakeLLMPolicyEngine({AgentRole.CODING: decision})

    assert engine.select(AgentRole.CODING) == decision


def test_select_unknown_role_raises_policy_not_found() -> None:
    engine = FakeLLMPolicyEngine()

    with pytest.raises(PolicyNotFoundError):
        engine.select(AgentRole.COORDINATOR)
