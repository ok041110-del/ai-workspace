from pathlib import Path

import pytest
from tests.interfaces.fakes import (
    FakeAgentManager,
    FakeAgentRegistry,
    FakeAgentScheduler,
    FakeEngineRuntime,
    FakeEventBus,
    FakeWorkflowEngine,
)

from ai_workspace.core.workspace_core import WorkspaceCore
from ai_workspace.domain.project import Project, ProjectStatus
from ai_workspace.interfaces.project_repository import ProjectNotFoundError
from ai_workspace.storage.file_project_repository import FileProjectRepository


def test_save_then_load_returns_same_project(tmp_path: Path) -> None:
    repo = FileProjectRepository(tmp_path)
    project = Project(
        project_id="p1", name="Demo", goal="목표", status=ProjectStatus.ACTIVE, priority=2
    )

    repo.save(project)
    loaded = repo.load("p1")

    assert loaded == project


def test_load_missing_raises_error(tmp_path: Path) -> None:
    repo = FileProjectRepository(tmp_path)

    with pytest.raises(ProjectNotFoundError):
        repo.load("unknown")


def test_save_overwrites_existing_project(tmp_path: Path) -> None:
    repo = FileProjectRepository(tmp_path)
    repo.save(Project(project_id="p1", name="Demo", goal="목표"))
    repo.save(Project(project_id="p1", name="Updated", goal="목표"))

    assert repo.load("p1").name == "Updated"


def test_list_projects_returns_all_saved_projects(tmp_path: Path) -> None:
    repo = FileProjectRepository(tmp_path)
    repo.save(Project(project_id="p1", name="A", goal="목표"))
    repo.save(Project(project_id="p2", name="B", goal="목표"))

    projects = repo.list_projects()

    assert {p.project_id for p in projects} == {"p1", "p2"}


def test_list_projects_empty_when_no_projects(tmp_path: Path) -> None:
    repo = FileProjectRepository(tmp_path)

    assert repo.list_projects() == []


def test_creates_base_dir_if_missing(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "dir"

    FileProjectRepository(target)

    assert target.exists()


def test_project_persists_across_new_repository_instance(tmp_path: Path) -> None:
    FileProjectRepository(tmp_path).save(Project(project_id="p1", name="Demo", goal="목표"))

    reopened = FileProjectRepository(tmp_path)

    assert reopened.load("p1").name == "Demo"


def test_workspace_core_accepts_file_project_repository_without_core_changes(
    tmp_path: Path,
) -> None:
    repo = FileProjectRepository(tmp_path)
    repo.save(Project(project_id="p1", name="Demo", goal="목표"))
    core = WorkspaceCore(
        project_repository=repo,
        workflow_engine=FakeWorkflowEngine(),
        agent_registry=FakeAgentRegistry(),
        agent_scheduler=FakeAgentScheduler(),
        agent_manager=FakeAgentManager(),
        event_bus=FakeEventBus(),
        engine_runtime=FakeEngineRuntime(),
    )

    assert core.load_project("p1").name == "Demo"
