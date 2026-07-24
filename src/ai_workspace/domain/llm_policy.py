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


INITIAL_MODELS: tuple[LLMModel, ...] = (
    LLMModel(LLMProvider.ANTHROPIC, "opus"),
    LLMModel(LLMProvider.ANTHROPIC, "sonnet"),
    LLMModel(LLMProvider.ANTHROPIC, "haiku"),
    LLMModel(LLMProvider.OPENAI, "gpt"),
    LLMModel(LLMProvider.GOOGLE, "gemini"),
    LLMModel(LLMProvider.XAI, "grok"),
)
