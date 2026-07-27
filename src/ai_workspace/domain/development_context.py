from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DevelopmentContext:
    """Agent 간에 실제 개발 산출물을 이어받아 전달하는 구조화된 컨텍스트
    (M5-T03). 필드 자체가 진실의 원천이며, `to_prompt()`는 그 내용을 LLM
    텍스트 프롬프트로 렌더링하는 여러 표현 방식 중 하나일 뿐이다 — 이후
    다른 렌더링(예: 구조화된 dict, 요약본)이 필요해지면 이 dataclass는
    그대로 두고 렌더링 메서드만 추가하면 된다."""

    task_id: str
    instructions: str
    prior_output: str | None = None
    related_knowledge: list[str] | None = None

    def to_prompt(self) -> str:
        prompt = self.instructions
        if self.prior_output is not None:
            prompt = f"{prompt}\n\n이전 단계 결과:\n{self.prior_output}"
        if self.related_knowledge:
            knowledge_text = "\n\n".join(self.related_knowledge)
            prompt = f"{prompt}\n\n관련 프로젝트 지식:\n{knowledge_text}"
        return prompt
