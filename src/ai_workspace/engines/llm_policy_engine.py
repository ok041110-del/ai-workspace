from __future__ import annotations

from dataclasses import replace

from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import INITIAL_MODELS, LLMModel, LLMPolicyDecision
from ai_workspace.domain.llm_policy_reliability import LLMPolicyReliabilityStat
from ai_workspace.interfaces.llm_policy_engine import LLMPolicyEngine


class InMemoryLLMPolicyEngine(LLMPolicyEngine):
    """생성 시 주어진 규칙 목록으로 AgentRole별 LLM 정책을 조회하는 최소
    구현체(M5-T01). 규칙을 어디서 읽어왔는지는 알지 못한다 — YAML 파일
    등에서 규칙을 불러오는 것은 `storage/llm_policy_loader.py`의 책임이며,
    이 클래스는 이미 구성된 `dict[AgentRole, LLMPolicyDecision]`만 받는다.

    **Self Optimization(Milestone 67, ADR-0085)**: `record_outcome()`으로
    누적한 `(role, model)`별 `LLMPolicyReliabilityStat`이
    `is_unreliable()`(M65/ADR-0083과 동일한 "성공 0건 + 표본 3건 이상"
    임계값)이 되면, 그 role의 다음 `select()`가 `domain.llm_policy.
    INITIAL_MODELS` 순서상 다음 모델로 자동 전환된 `LLMPolicyDecision`을
    반환한다(effort는 원래 rule 값을 유지). 마지막 모델까지 전환했는데도
    다시 신뢰 불가로 판정되면 더 이상 전환하지 않는다 — 이미 순서상
    끝에 도달했고, 되돌아가 봤자 이미 실패한 모델을 다시 쓰게 될 뿐이다
    (Probe/자동 복구는 이번 범위 밖, 별도 Milestone 후보로 남긴다).
    `record_outcome()`을 한 번도 호출하지 않으면 이 클래스의 동작은
    M5-T01과 100% 동일하다."""

    def __init__(self, rules: dict[AgentRole, LLMPolicyDecision]) -> None:
        self._rules = dict(rules)
        self._active_decisions: dict[AgentRole, LLMPolicyDecision] = {}
        self._stats: dict[tuple[AgentRole, LLMModel], LLMPolicyReliabilityStat] = {}

    def select(self, role: AgentRole) -> LLMPolicyDecision | None:
        base_decision = self._rules.get(role)
        if base_decision is None:
            return None
        decision = self._active_decisions.get(role, base_decision)
        stat = self._stats.get((role, decision.model), LLMPolicyReliabilityStat())
        if stat.is_unreliable():
            next_model = _next_model(decision.model)
            if next_model is not None:
                decision = replace(decision, model=next_model)
                self._active_decisions[role] = decision
        return decision

    def record_outcome(
        self, role: AgentRole, decision: LLMPolicyDecision, success: bool
    ) -> None:
        key = (role, decision.model)
        stat = self._stats.get(key, LLMPolicyReliabilityStat())
        self._stats[key] = stat.record(success)


def _next_model(model: LLMModel) -> LLMModel | None:
    """`INITIAL_MODELS` 순서상 `model` 바로 다음 모델을 반환한다.
    `model`이 목록에 없거나 이미 마지막이면 `None`(더 이상 전환할 곳이
    없음)."""
    try:
        index = INITIAL_MODELS.index(model)
    except ValueError:
        return None
    if index + 1 >= len(INITIAL_MODELS):
        return None
    return INITIAL_MODELS[index + 1]
