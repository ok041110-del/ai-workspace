from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMPolicyDecision


class LLMPolicyEngine(ABC):
    """Agent의 Role에 따라 어떤 LLM Provider/Model/Effort를 쓸지 Rule 기반으로
    결정하는 계약(M5-T01, `.ai/RULES.md` §7 "Temporary LLM Policy" M2 단계
    소급 구현). 규칙의 출처(YAML 파일 등)는 이 계약이 알지 못한다 — 규칙을
    실제로 어디서 읽어오는지는 별도 로더(예: `storage/llm_policy_loader.py`)
    의 책임이며, 이 Engine은 이미 구성된 규칙을 조회만 한다.

    규칙이 없는 role은 예외가 아니라 `None`으로 표현한다(M5-T02에서
    조정 — 정책 부재는 "이 컴포넌트의 실패"가 아니라 "정책이 아직 없다"는
    정상적인 상태이며, 호출자(예: Agent Runtime)가 예외 처리 없이 생명주기
    관리라는 본래 책임에만 집중할 수 있게 한다).

    `record_outcome()`(Milestone 67, ADR-0085)은 실행 결과를 정책에
    되먹이는 별도의 명시적 진입점이다 — `select()` 자체의 "side-effect
    없음(read-only)" 계약은 그대로 유지하고, 결과 기록은 항상 이
    메서드를 통해서만 이루어진다."""

    @abstractmethod
    def select(self, role: AgentRole) -> LLMPolicyDecision | None:
        """
        입력: role (정책을 조회할 AgentRole)
        출력: 해당 role에 대해 결정된 LLMPolicyDecision(model, effort),
              규칙이 없으면 None
        예외: 없음
        보장: side-effect 없음(read-only). Engine 실행이나 실제 Adapter
              선택은 하지 않는다 — 정책 결정만 담당한다. 과거
              `record_outcome()` 호출 이력에 따라 반환값이 달라질 수는
              있다(Self Optimization) — 이 호출 자체가 상태를 바꾸지는
              않는다는 뜻이다.
        """
        raise NotImplementedError

    @abstractmethod
    def record_outcome(
        self, role: AgentRole, decision: LLMPolicyDecision, success: bool
    ) -> None:
        """
        입력: role, 실제로 사용된 decision(select()가 반환했던 값),
              success(해당 실행의 성공 여부)
        출력: 없음
        예외: 없음
        보장: 이 role+decision 조합의 누적 성공/실패 이력을 갱신한다.
              구현체는 이 이력을 바탕으로 이후 select(role) 호출의
              결과를 스스로 조정할 수 있다(Self Optimization) — 조정
              여부/방식은 구현체 재량이며, 아무 것도 하지 않아도 계약을
              위반하지 않는다(no-op 허용).
        """
        raise NotImplementedError
