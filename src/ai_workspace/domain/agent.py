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
    """`priority`(Milestone 57, ADR-0075): `AgentScheduler.select()`가
    같은 Capability의 여러 후보 중 우선순위를 매길 때 쓴다 — 낮을수록
    우선(숫자가 작을수록 먼저 선택). 기본값 0이라 기존 코드는 모두
    동점이며, 동점 시 `select()`의 안정 정렬이 `candidates` 원래
    순서를 그대로 보존해 M13/M56이 검증한 "첫 매치" 동작과 100%
    동일하다(회귀 없음)."""

    agent_id: str
    role: AgentRole
    capabilities: frozenset[AgentCapability] = field(default_factory=frozenset)
    status: AgentStatus = AgentStatus.IDLE
    priority: int = 0
