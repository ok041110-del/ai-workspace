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
