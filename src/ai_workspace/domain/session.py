from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WorkspaceSession:
    session_id: str
    current_project_id: str | None = None
    current_mission_id: str | None = None
    active_workflow_id: str | None = None
    active_agent_ids: list[str] = field(default_factory=list)
    memory_snapshot_id: str | None = None
    engine_session_id: str | None = None
