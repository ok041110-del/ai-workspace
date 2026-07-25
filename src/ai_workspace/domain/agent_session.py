from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentSession:
    session_id: str
    agent_id: str
