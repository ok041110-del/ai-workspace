from ai_workspace.domain.project import Project, ProjectStatus


def test_project_defaults_to_active() -> None:
    project = Project(project_id="p1", name="AI Workspace", goal="오케스트레이션 플랫폼 구축")

    assert project.status == ProjectStatus.ACTIVE
    assert project.priority == 0


def test_project_archive_and_activate() -> None:
    project = Project(project_id="p1", name="AI Workspace", goal="목표")

    project.archive()
    assert project.status == ProjectStatus.ARCHIVED

    project.activate()
    assert project.status == ProjectStatus.ACTIVE
