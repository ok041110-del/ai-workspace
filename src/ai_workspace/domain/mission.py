from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Mission:
    mission_id: str
    project_id: str
    goal: str
