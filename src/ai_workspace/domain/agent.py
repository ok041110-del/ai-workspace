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
    동일하다(회귀 없음).

    `location`(Milestone 61, ADR-0079): 이 Agent가 Event를 처리하는
    위치를 가리키는 불투명한 식별자. 기본값 `None`은 "같은 프로세스"를
    뜻하며(기존 동작과 100% 동일 — 모든 기존 Agent는 EventBus.publish()로
    방송되는 Event를 직접 구독해 처리한다), `None`이 아니면 다른
    프로세스/호스트에 있다고 선언하는 것이다. 이 필드 자체는 아무 것도
    강제하지 않는다 — 실제 원격 전달은 `RemoteAgentDispatcher`
    구현체(interfaces/remote_agent_dispatcher.py)가 이 값을 해석해
    수행한다."""

    agent_id: str
    role: AgentRole
    capabilities: frozenset[AgentCapability] = field(default_factory=frozenset)
    status: AgentStatus = AgentStatus.IDLE
    priority: int = 0
    location: str | None = None
