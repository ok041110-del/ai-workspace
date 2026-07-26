from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AgentRole(Enum):
    COORDINATOR = "coordinator"
    PLANNER = "planner"
    CODING = "coding"
    REVIEWER = "reviewer"
    DOCUMENTATION = "documentation"
    RESEARCH = "research"
    SHELL = "shell"


class AgentCapability(Enum):
    COORDINATION = "coordination"
    PLANNING = "planning"
    CODING = "coding"
    REVIEW = "review"
    DOCUMENTATION = "documentation"
    RESEARCH = "research"
    VISION = "vision"
    VOICE = "voice"
    GIT = "git"
    MCP = "mcp"
    SHELL = "shell"


class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class Agent:
    agent_id: str
    role: AgentRole
    capabilities: frozenset[AgentCapability] = field(default_factory=frozenset)
    status: AgentStatus = AgentStatus.IDLE
