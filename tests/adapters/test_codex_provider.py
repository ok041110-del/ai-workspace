from __future__ import annotations

import json

from ai_workspace.adapters.codex_provider import CodexProvider
from ai_workspace.adapters.process_runner import ProcessResult
from ai_workspace.domain.task import Task, TaskStatus


def make_task(title: str = "구현하기") -> Task:
    return Task(task_id="t1", project_id="p1", title=title, status=TaskStatus.TODO)


def test_build_command_uses_codex_exec_with_json_and_full_auto() -> None:
    provider = CodexProvider()

    command = provider.build_command("s1", make_task("로그인 구현"))

    assert command == ["codex", "exec", "로그인 구현", "--json", "--full-auto"]


def test_build_command_appends_model_when_given() -> None:
    provider = CodexProvider(model="gpt-5.3-codex")

    command = provider.build_command("s1", make_task())

    assert command[-2:] == ["--model", "gpt-5.3-codex"]


def test_parse_result_extracts_content_field_from_last_ndjson_line() -> None:
    provider = CodexProvider()
    stdout = "\n".join(
        [
            json.dumps({"type": "state", "content": "시작"}),
            json.dumps({"type": "final", "content": "완료된 결과"}),
        ]
    )
    process_result = ProcessResult(returncode=0, stdout=stdout, stderr="")

    result = provider.parse_result(process_result)

    assert result.success is True
    assert result.output == "완료된 결과"


def test_parse_result_falls_back_to_raw_stdout_when_not_json() -> None:
    provider = CodexProvider()
    process_result = ProcessResult(returncode=0, stdout="일반 텍스트 출력", stderr="")

    result = provider.parse_result(process_result)

    assert result.success is True
    assert result.output == "일반 텍스트 출력"


def test_parse_result_returns_failure_for_nonzero_exit_without_json() -> None:
    provider = CodexProvider()
    process_result = ProcessResult(returncode=1, stdout="", stderr="에러 발생")

    result = provider.parse_result(process_result)

    assert result.success is False
    assert result.error == "에러 발생"


def test_capabilities_and_supports_parallel() -> None:
    provider = CodexProvider()

    assert "codex" in provider.capabilities()
    assert provider.supports_parallel() is True
