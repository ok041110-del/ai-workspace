from __future__ import annotations

from pathlib import Path

import yaml

from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMEffort, LLMModel, LLMPolicyDecision, LLMProvider


class InvalidLLMPolicyRuleError(ValueError):
    """YAML 규칙의 role/provider/effort 값이 알려진 값과 일치하지 않을 때
    발생한다."""


_ROLE_BY_VALUE = {role.value: role for role in AgentRole}


def load_llm_policy_rules(path: str | Path) -> dict[AgentRole, LLMPolicyDecision]:
    """YAML 파일(`docs/llm_policy.example.yaml` 형식)을 읽어 AgentRole별
    `LLMPolicyDecision` 규칙을 만든다. `LLMPolicyEngine`/
    `InMemoryLLMPolicyEngine`은 이 함수(또는 이 파일 자체)를 전혀 알지
    못한다 — PyYAML 의존은 이 로더 계층 안에만 있다(M5-T01, 사용자 지시).

    최상위 key는 `AgentRole.value`와 정확히 일치해야 한다(예: "planner",
    "coding", "reviewer", "documentation", "research"). 일치하지 않는
    key나 알 수 없는 provider/effort 값은 조용히 넘어가지 않고
    InvalidLLMPolicyRuleError로 명확히 실패한다."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    rules: dict[AgentRole, LLMPolicyDecision] = {}
    for role_key, rule in data.items():
        if role_key not in _ROLE_BY_VALUE:
            raise InvalidLLMPolicyRuleError(f"알 수 없는 role입니다: {role_key}")
        try:
            provider = LLMProvider(rule["provider"])
            effort = LLMEffort(rule["effort"])
        except ValueError as exc:
            raise InvalidLLMPolicyRuleError(f"{role_key} 규칙이 올바르지 않습니다: {exc}") from exc
        rules[_ROLE_BY_VALUE[role_key]] = LLMPolicyDecision(
            model=LLMModel(provider=provider, name=rule["model"]), effort=effort
        )
    return rules
