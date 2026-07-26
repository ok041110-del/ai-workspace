from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    XAI = "xai"


class LLMEffort(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class LLMModel:
    provider: LLMProvider
    name: str


@dataclass(frozen=True)
class LLMPolicyDecision:
    model: LLMModel
    effort: LLMEffort


INITIAL_MODELS: tuple[LLMModel, ...] = (
    LLMModel(LLMProvider.ANTHROPIC, "opus"),
    LLMModel(LLMProvider.ANTHROPIC, "sonnet"),
    LLMModel(LLMProvider.ANTHROPIC, "haiku"),
    LLMModel(LLMProvider.OPENAI, "gpt"),
    LLMModel(LLMProvider.GOOGLE, "gemini"),
    LLMModel(LLMProvider.XAI, "grok"),
)

_PROVIDER_ENGINE_CAPABILITY: dict[LLMProvider, str] = {
    LLMProvider.ANTHROPIC: "claude_code",
    LLMProvider.OPENAI: "codex",
    LLMProvider.GOOGLE: "gemini",
    LLMProvider.XAI: "xai",
}


def required_capabilities(decision: LLMPolicyDecision | None) -> frozenset[str]:
    """M6-T02: `LLMPolicyDecision`을 `EngineRuntime.run()`에 넘길
    `required_capabilities`로 변환한다(ManagedEngineRuntime의 다중 Adapter
    등록·선택은 M6-T01에서 이미 지원됨). 정책이 없으면(Role에 규칙이
    없거나 LLMPolicyEngine이 아예 주입되지 않은 경우) 빈 집합을 반환해
    "제약 없음"이라는 기존 동작과 완전히 하위 호환된다. `LLMProvider.XAI`
    처럼 대응하는 EngineAdapter가 아직 없는 Provider는 태그만 반환하고,
    실제로 매칭되는 Adapter가 없으면 `EngineRuntime.run()`이
    `NoSuitableEngineError`를 던지는 것이 의도된 동작이다."""
    if decision is None:
        return frozenset()
    return frozenset({_PROVIDER_ENGINE_CAPABILITY[decision.model.provider]})


def model_name(decision: LLMPolicyDecision | None) -> str | None:
    """M14-T03: `LLMPolicyDecision`을 `EngineRuntime.run()`에 넘길
    `model`로 변환한다. 정책이 없으면(Role에 규칙이 없거나
    LLMPolicyEngine이 아예 주입되지 않은 경우) `None`을 반환해 "제약
    없음"이라는 기존 동작과 완전히 하위 호환된다."""
    if decision is None:
        return None
    return decision.model.name
