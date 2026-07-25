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
    관리라는 본래 책임에만 집중할 수 있게 한다)."""

    @abstractmethod
    def select(self, role: AgentRole) -> LLMPolicyDecision | None:
        """
        입력: role (정책을 조회할 AgentRole)
        출력: 해당 role에 대해 결정된 LLMPolicyDecision(model, effort),
              규칙이 없으면 None
        예외: 없음
        보장: side-effect 없음(read-only). Engine 실행이나 실제 Adapter
              선택은 하지 않는다 — 정책 결정만 담당한다.
        """
        raise NotImplementedError
