import pytest

from ai_workspace.domain.project import Project
from ai_workspace.interfaces.project_repository import ProjectNotFoundError

from .fakes import FakeProjectRepository


def test_save_then_load_returns_same_project() -> None:
    repository = FakeProjectRepository()
    project = Project(project_id="p1", name="AI Workspace", goal="목표")

    repository.save(project)

    assert repository.load("p1") == project


def test_load_unknown_project_raises_not_found() -> None:
    repository = FakeProjectRepository()

    with pytest.raises(ProjectNotFoundError):
        repository.load("unknown")


def test_list_projects_returns_defensive_copy() -> None:
    repository = FakeProjectRepository()
    repository.save(Project(project_id="p1", name="A", goal="목표"))

    projects = repository.list_projects()
    projects.append(Project(project_id="p2", name="B", goal="목표"))

    assert len(repository.list_projects()) == 1
