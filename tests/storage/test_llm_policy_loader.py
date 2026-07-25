from pathlib import Path

import pytest

from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMEffort, LLMProvider
from ai_workspace.storage.llm_policy_loader import InvalidLLMPolicyRuleError, load_llm_policy_rules

_EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "docs" / "llm_policy.example.yaml"


def test_loads_real_example_yaml_file() -> None:
    """저장소의 실제 docs/llm_policy.example.yaml이 항상 로드 가능한
    유효한 형식으로 유지됨을 보장한다(회귀 방지)."""
    rules = load_llm_policy_rules(_EXAMPLE_YAML)

    assert rules[AgentRole.CODING].model.provider == LLMProvider.ANTHROPIC
    assert rules[AgentRole.CODING].effort == LLMEffort.HIGH
    assert AgentRole.COORDINATOR not in rules


def test_parses_rules_keyed_by_agent_role_value(tmp_path: Path) -> None:
    yaml_path = tmp_path / "policy.yaml"
    yaml_path.write_text(
        "planner:\n  provider: openai\n  model: gpt\n  effort: high\n", encoding="utf-8"
    )

    rules = load_llm_policy_rules(yaml_path)

    assert rules[AgentRole.PLANNER].model.name == "gpt"
    assert rules[AgentRole.PLANNER].model.provider == LLMProvider.OPENAI
    assert rules[AgentRole.PLANNER].effort == LLMEffort.HIGH


def test_unknown_role_key_raises_error(tmp_path: Path) -> None:
    yaml_path = tmp_path / "policy.yaml"
    yaml_path.write_text(
        "typo-role:\n  provider: openai\n  model: gpt\n  effort: high\n", encoding="utf-8"
    )

    with pytest.raises(InvalidLLMPolicyRuleError):
        load_llm_policy_rules(yaml_path)


def test_unknown_provider_raises_error(tmp_path: Path) -> None:
    yaml_path = tmp_path / "policy.yaml"
    yaml_path.write_text(
        "planner:\n  provider: unknown-provider\n  model: gpt\n  effort: high\n", encoding="utf-8"
    )

    with pytest.raises(InvalidLLMPolicyRuleError):
        load_llm_policy_rules(yaml_path)


def test_empty_file_returns_empty_rules(tmp_path: Path) -> None:
    yaml_path = tmp_path / "empty.yaml"
    yaml_path.write_text("", encoding="utf-8")

    assert load_llm_policy_rules(yaml_path) == {}
