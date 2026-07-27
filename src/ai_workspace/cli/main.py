from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ai_workspace.core.workspace_core import WorkspaceCore
from ai_workspace.domain.project import Project
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.project_repository import ProjectNotFoundError
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler
from ai_workspace.runtime.engine.managed_engine_runtime import ManagedEngineRuntime
from ai_workspace.storage.file_project_repository import FileProjectRepository

DEFAULT_DATA_DIR = str(Path("workspace") / "projects")


def _build_workspace_core(data_dir: str) -> WorkspaceCore:
    """CLI의 유일한 진입점인 `WorkspaceCore`를 조립한다. `ClaudeCodeEngineAdapter`
    (M3)가 기본 채택 Engine이지만, 현재 CLI 명령 중 실제로 Engine 실행을
    요구하는 것이 없어 등록하지 않는다(지연 초기화) — Task 실행이 필요한
    명령이 추가되는 시점에 `engine_runtime.register_engine("claude_code",
    ClaudeCodeEngineAdapter())`를 호출한다. 그전까지 CLI는 `claude` 실행
    파일 설치 여부에 의존하지 않는다."""
    event_bus = InMemoryEventBus()
    return WorkspaceCore(
        project_repository=FileProjectRepository(data_dir),
        workflow_engine=InMemoryWorkflowEngine(),
        agent_registry=InMemoryAgentRegistry(),
        agent_scheduler=InMemoryAgentScheduler(),
        agent_manager=InMemoryAgentManager(),
        event_bus=event_bus,
        engine_runtime=ManagedEngineRuntime(event_bus=event_bus),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-workspace", description="AI Workspace CLI")
    parser.add_argument(
        "--data-dir", default=DEFAULT_DATA_DIR, help="Project 데이터를 저장할 디렉터리"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser(
        "start", help="Dashboard 서버 실행(M20) — 상시 실행, 기존 명령과 독립"
    )
    start_parser.add_argument("--host", default="127.0.0.1")
    start_parser.add_argument("--port", type=int, default=8080)

    project_parser = subparsers.add_parser("project", help="Project 관리")
    project_subparsers = project_parser.add_subparsers(dest="project_command", required=True)

    create_parser = project_subparsers.add_parser("create", help="Project 생성")
    create_parser.add_argument("project_id")
    create_parser.add_argument("name")
    create_parser.add_argument("goal")
    create_parser.add_argument("--priority", type=int, default=0)

    show_parser = project_subparsers.add_parser("show", help="Project 조회")
    show_parser.add_argument("project_id")

    project_subparsers.add_parser("list", help="Project 목록 조회")

    return parser


def _create_project(core: WorkspaceCore, args: argparse.Namespace) -> int:
    project = Project(
        project_id=args.project_id, name=args.name, goal=args.goal, priority=args.priority
    )
    core.save_project(project)
    print(f"Project가 생성되었습니다: {project.project_id}")
    return 0


def _show_project(core: WorkspaceCore, args: argparse.Namespace) -> int:
    try:
        project = core.load_project(args.project_id)
    except ProjectNotFoundError:
        print(f"Project를 찾을 수 없습니다: {args.project_id}", file=sys.stderr)
        return 1
    print(f"project_id: {project.project_id}")
    print(f"name: {project.name}")
    print(f"goal: {project.goal}")
    print(f"status: {project.status.value}")
    print(f"priority: {project.priority}")
    return 0


def _list_projects(core: WorkspaceCore, args: argparse.Namespace) -> int:
    projects = core.list_projects()
    if not projects:
        print("등록된 Project가 없습니다.")
        return 0
    for project in projects:
        print(f"{project.project_id}\t{project.name}\t{project.status.value}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "start":
        # 서버 실행은 FastAPI/uvicorn을 요구한다(M20) — 다른 CLI 명령은
        # 웹 프레임워크를 몰라도 되므로 지연 import로 분리한다.
        from ai_workspace.web.server import run_server

        run_server(host=args.host, port=args.port)
        return 0

    core = _build_workspace_core(args.data_dir)

    if args.project_command == "create":
        return _create_project(core, args)
    if args.project_command == "list":
        return _list_projects(core, args)
    return _show_project(core, args)


if __name__ == "__main__":
    raise SystemExit(main())
