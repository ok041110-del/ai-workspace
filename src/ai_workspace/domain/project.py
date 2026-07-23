from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProjectStatus(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


@dataclass
class Project:
    project_id: str
    name: str
    goal: str
    status: ProjectStatus = ProjectStatus.ACTIVE
    priority: int = 0

    def archive(self) -> None:
        self.status = ProjectStatus.ARCHIVED

    def activate(self) -> None:
        self.status = ProjectStatus.ACTIVE
