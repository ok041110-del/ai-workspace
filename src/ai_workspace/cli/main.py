from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ai_workspace.domain.project import Project
from ai_workspace.interfaces.project_repository import ProjectNotFoundError
from ai_workspace.storage.file_project_repository import FileProjectRepository

DEFAULT_DATA_DIR = str(Path("workspace") / "projects")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-workspace", description="AI Workspace CLI")
    parser.add_argument(
        "--data-dir", default=DEFAULT_DATA_DIR, help="Project 데이터를 저장할 디렉터리"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    project_parser = subparsers.add_parser("project", help="Project 관리")
    project_subparsers = project_parser.add_subparsers(dest="project_command", required=True)

    create_parser = project_subparsers.add_parser("create", help="Project 생성")
    create_parser.add_argument("project_id")
    create_parser.add_argument("name")
    create_parser.add_argument("goal")
    create_parser.add_argument("--priority", type=int, default=0)

    show_parser = project_subparsers.add_parser("show", help="Project 조회")
    show_parser.add_argument("project_id")

    return parser


def _create_project(repository: FileProjectRepository, args: argparse.Namespace) -> int:
    project = Project(
        project_id=args.project_id, name=args.name, goal=args.goal, priority=args.priority
    )
    repository.save(project)
    print(f"Project가 생성되었습니다: {project.project_id}")
    return 0


def _show_project(repository: FileProjectRepository, args: argparse.Namespace) -> int:
    try:
        project = repository.load(args.project_id)
    except ProjectNotFoundError:
        print(f"Project를 찾을 수 없습니다: {args.project_id}", file=sys.stderr)
        return 1
    print(f"project_id: {project.project_id}")
    print(f"name: {project.name}")
    print(f"goal: {project.goal}")
    print(f"status: {project.status.value}")
    print(f"priority: {project.priority}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    repository = FileProjectRepository(args.data_dir)

    if args.project_command == "create":
        return _create_project(repository, args)
    return _show_project(repository, args)


if __name__ == "__main__":
    raise SystemExit(main())
