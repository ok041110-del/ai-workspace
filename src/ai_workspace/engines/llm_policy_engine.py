from __future__ import annotations

from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMPolicyDecision
from ai_workspace.interfaces.llm_policy_engine import LLMPolicyEngine, PolicyNotFoundError


class InMemoryLLMPolicyEngine(LLMPolicyEngine):
    """생성 시 주어진 규칙 목록으로 AgentRole별 LLM 정책을 조회하는 최소
    구현체(M5-T01). 규칙을 어디서 읽어왔는지는 알지 못한다 — YAML 파일
    등에서 규칙을 불러오는 것은 `storage/llm_policy_loader.py`의 책임이며,
    이 클래스는 이미 구성된 `dict[AgentRole, LLMPolicyDecision]`만 받는다."""

    def __init__(self, rules: dict[AgentRole, LLMPolicyDecision]) -> None:
        self._rules = dict(rules)

    def select(self, role: AgentRole) -> LLMPolicyDecision:
        if role not in self._rules:
            raise PolicyNotFoundError(role)
        return self._rules[role]
