from __future__ import annotations

import json
from pathlib import Path

from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus
from ai_workspace.interfaces.agent_repository import AgentNotFoundError, AgentRepository


class FileAgentRepository(AgentRepository):
    """Agent를 Agent당 JSON 파일 하나로 저장하는 파일 기반 구현체
    (ARCHITECTURE.md §11)."""

    def __init__(self, base_dir: str | Path) -> None:
        self._base_dir = Path(base_dir)
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, agent_id: str) -> Path:
        return self._base_dir / f"{agent_id}.json"

    def load(self, agent_id: str) -> Agent:
        path = self._path(agent_id)
        if not path.exists():
            raise AgentNotFoundError(agent_id)
        data = json.loads(path.read_text(encoding="utf-8"))
        return Agent(
            agent_id=data["agent_id"],
            role=AgentRole(data["role"]),
            capabilities=frozenset(AgentCapability(c) for c in data["capabilities"]),
            status=AgentStatus(data["status"]),
        )

    def save(self, agent: Agent) -> None:
        data = {
            "agent_id": agent.agent_id,
            "role": agent.role.value,
            "capabilities": sorted(c.value for c in agent.capabilities),
            "status": agent.status.value,
        }
        self._path(agent.agent_id).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def list_agents(self) -> list[Agent]:
        return [self.load(path.stem) for path in sorted(self._base_dir.glob("*.json"))]
