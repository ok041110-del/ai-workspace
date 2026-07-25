from pathlib import Path

import pytest

from ai_workspace.cli.main import main


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
