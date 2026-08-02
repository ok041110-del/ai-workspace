from pathlib import Path

import pytest

from ai_workspace.cli.main import main


def test_start_command_delegates_to_run_server(monkeypatch: pytest.MonkeyPatch) -> None:
    """M20 DoD 12번: `workspace start`는 서버를 실행하고, 기존 명령
    (project create/show/list)은 그대로 유지된다 - 실제 소켓을 열지
    않도록 `run_server`를 대체해 호출 인자만 확인한다."""
    calls: list[dict[str, object]] = []

    def fake_run_server(*, host: str, port: int) -> None:
        calls.append({"host": host, "port": port})

    monkeypatch.setattr("ai_workspace.web.server.run_server", fake_run_server)

    exit_code = main(["start", "--host", "0.0.0.0", "--port", "9000"])

    assert exit_code == 0
    assert calls == [{"host": "0.0.0.0", "port": 9000}]


def test_create_then_show_end_to_end(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    data_dir = str(tmp_path)

    assert main(["--data-dir", data_dir, "project", "create", "p1", "Demo", "목표"]) == 0
    assert main(["--data-dir", data_dir, "project", "show", "p1"]) == 0

    output = capsys.readouterr().out
    assert "project_id: p1" in output
    assert "name: Demo" in output
    assert "goal: 목표" in output


def test_create_uses_given_priority(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data_dir = str(tmp_path)
    main(["--data-dir", data_dir, "project", "create", "p1", "Demo", "목표", "--priority", "3"])
    capsys.readouterr()

    main(["--data-dir", data_dir, "project", "show", "p1"])

    assert "priority: 3" in capsys.readouterr().out


def test_create_defaults_priority_to_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data_dir = str(tmp_path)
    main(["--data-dir", data_dir, "project", "create", "p1", "Demo", "목표"])
    capsys.readouterr()

    main(["--data-dir", data_dir, "project", "show", "p1"])

    assert "priority: 0" in capsys.readouterr().out


def test_show_missing_project_returns_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data_dir = str(tmp_path)

    exit_code = main(["--data-dir", data_dir, "project", "show", "unknown"])

    assert exit_code == 1
    assert "unknown" in capsys.readouterr().err


def test_project_persists_across_separate_main_invocations(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data_dir = str(tmp_path)
    main(["--data-dir", data_dir, "project", "create", "p1", "Demo", "목표"])
    capsys.readouterr()

    exit_code = main(["--data-dir", data_dir, "project", "show", "p1"])

    assert exit_code == 0


def test_list_shows_multiple_projects_end_to_end(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """M4-T05: `project list`가 실제 `FileProjectRepository`(파일 시스템)를
    거쳐 여러 Project를 동시에 조회할 수 있음을 증명한다(다중 프로젝트
    운용 검증, 실제 Repository를 사용하는 통합 경로)."""
    data_dir = str(tmp_path)
    main(["--data-dir", data_dir, "project", "create", "p1", "Alpha", "목표A"])
    main(["--data-dir", data_dir, "project", "create", "p2", "Beta", "목표B"])
    capsys.readouterr()

    exit_code = main(["--data-dir", data_dir, "project", "list"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "p1\tAlpha\tactive" in output
    assert "p2\tBeta\tactive" in output


def test_list_reports_when_no_projects_exist(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data_dir = str(tmp_path)

    exit_code = main(["--data-dir", data_dir, "project", "list"])

    assert exit_code == 0
    assert "등록된 Project가 없습니다." in capsys.readouterr().out


def test_learning_state_persists_across_separate_workspace_core_builds(tmp_path: Path) -> None:
    """M83(ADR-0101): `_build_workspace_core()`가 조립하는 `WorkspaceCore`는
    `FileLearningStateStore`를 통해 EngineRuntime 학습 상태(M65/M69)를
    Workspace 종료(`shutdown()`) 시 저장하고, 다음 번 조립(`__init__`)
    시 자동으로 복원한다."""
    from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
    from ai_workspace.cli.main import _build_workspace_core
    from ai_workspace.domain.task import Task, TaskStatus

    data_dir = str(tmp_path / "projects")

    first = _build_workspace_core(data_dir)
    first.engine_runtime.register_engine("engine-a", MockEngineAdapter())
    for i in range(3):
        first.engine_runtime.run(
            Task(task_id=f"t{i}", project_id="p1", title="구현하기", status=TaskStatus.TODO)
        )
    assert first.engine_runtime.benchmark_profile("engine-a").execution_count == 3
    first.shutdown()

    second = _build_workspace_core(data_dir)

    assert second.engine_runtime.benchmark_profile("engine-a").execution_count == 3


def test_learning_state_absent_on_first_build_without_error(tmp_path: Path) -> None:
    """M83(ADR-0101): 저장된 학습 상태가 아직 없어도(첫 실행) 조립이
    예외 없이 성공하고, 빈 in-process 상태로 시작한다."""
    from ai_workspace.cli.main import _build_workspace_core

    core = _build_workspace_core(str(tmp_path / "projects"))

    assert core.engine_runtime.export_learning_state() == {
        "engine_reliability": {},
        "execution_memory": [],
        "consensus_agreement": [],
        "reflections": {},
    }
