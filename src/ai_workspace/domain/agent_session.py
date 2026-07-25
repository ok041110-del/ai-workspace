from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.domain.llm_policy import LLMPolicyDecision


@dataclass
class AgentSession:
    session_id: str
    agent_id: str
    llm_policy_decision: LLMPolicyDecision | None = None
