from __future__ import annotations

import json
from pathlib import Path

from ai_workspace.domain.project import Project, ProjectStatus
from ai_workspace.interfaces.project_repository import ProjectNotFoundError, ProjectRepository


class FileProjectRepository(ProjectRepository):
    """Project를 프로젝트당 JSON 파일 하나로 저장하는 파일 기반 구현체
    (ARCHITECTURE.md §11, ADR-0004)."""

    def __init__(self, base_dir: str | Path) -> None:
        self._base_dir = Path(base_dir)
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, project_id: str) -> Path:
        return self._base_dir / f"{project_id}.json"

    def load(self, project_id: str) -> Project:
        path = self._path(project_id)
        if not path.exists():
            raise ProjectNotFoundError(project_id)
        data = json.loads(path.read_text(encoding="utf-8"))
        return Project(
            project_id=data["project_id"],
            name=data["name"],
            goal=data["goal"],
            status=ProjectStatus(data["status"]),
            priority=data["priority"],
        )

    def save(self, project: Project) -> None:
        data = {
            "project_id": project.project_id,
            "name": project.name,
            "goal": project.goal,
            "status": project.status.value,
            "priority": project.priority,
        }
        self._path(project.project_id).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def list_projects(self) -> list[Project]:
        return [self.load(path.stem) for path in sorted(self._base_dir.glob("*.json"))]
