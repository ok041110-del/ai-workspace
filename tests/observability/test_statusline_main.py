from __future__ import annotations

import io

from ai_workspace.observability import statusline_main


def _run(monkeypatch, capsys, tmp_path, stdin_text: str) -> str:
    monkeypatch.setattr("sys.stdin", io.StringIO(stdin_text))
    monkeypatch.setattr(statusline_main, "_DEBUG_LOG_PATH", tmp_path / "statusline.log")
    exit_code = statusline_main.main()
    assert exit_code == 0
    return capsys.readouterr().out


def test_main_never_raises_and_always_prints_one_line_for_valid_payload(
    monkeypatch, capsys, tmp_path
):
    output = _run(monkeypatch, capsys, tmp_path, '{"cwd": "."}')
    assert output.strip() != ""


def test_main_never_raises_on_malformed_json(monkeypatch, capsys, tmp_path):
    output = _run(monkeypatch, capsys, tmp_path, "not json")
    assert output.strip() != ""


def test_main_never_raises_on_empty_stdin(monkeypatch, capsys, tmp_path):
    output = _run(monkeypatch, capsys, tmp_path, "")
    assert output.strip() != ""


def test_debug_log_not_written_on_normal_success(monkeypatch, capsys, tmp_path):
    monkeypatch.delenv(statusline_main._DEBUG_ENV_VAR, raising=False)
    _run(monkeypatch, capsys, tmp_path, '{"cwd": "."}')
    assert not (tmp_path / "statusline.log").exists()


def test_debug_log_written_when_json_parse_fails(monkeypatch, capsys, tmp_path):
    monkeypatch.delenv(statusline_main._DEBUG_ENV_VAR, raising=False)
    _run(monkeypatch, capsys, tmp_path, "not json")
    log_path = tmp_path / "statusline.log"
    assert log_path.exists()
    assert "stdin JSON 파싱 실패" in log_path.read_text(encoding="utf-8")


def test_debug_env_var_forces_raw_stdin_capture_even_on_success(monkeypatch, capsys, tmp_path):
    monkeypatch.setenv(statusline_main._DEBUG_ENV_VAR, "1")
    _run(monkeypatch, capsys, tmp_path, '{"cwd": "."}')
    log_path = tmp_path / "statusline.log"
    assert log_path.exists()
    assert "디버그 캡처(정상 동작)" in log_path.read_text(encoding="utf-8")
