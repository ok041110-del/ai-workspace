from __future__ import annotations

import json

from ai_workspace.adapters.cli_provider import CLIProvider
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import EngineResult
from ai_workspace.interfaces.execution_environment import ExecutionResult


class CodexProvider(CLIProvider):
    """OpenAI Codex CLI(`codex exec`)용 `CLIProvider`(M5-T05).

    **미검증 경고**: 이 저장소 환경에는 `codex` CLI가 설치되어 있지 않아
    실제 실행으로 플래그를 검증하지 못했다(`ClaudeCodeEngineAdapter`가
    M3-T02에서 `claude --help` + 실제 호출로 검증한 것과 다름). 아래 명령
    구성은 공개 문서(OpenAI Developers `codex exec`/Non-interactive mode,
    2026-07 기준 웹 검색)를 근거로 했다 — 실제 사용 전 `codex --help`로
    재확인을 권장한다.

    - `codex exec "<prompt>"`: 비대화형 1회 실행
    - `--json`: 상태 변화마다 한 줄씩 JSON 이벤트를 stdout에 출력
    - `--full-auto`: `--approval-mode never` + `--sandbox workspace-write`를
      묶은 축약 플래그 — 헤드리스 환경에서 승인 대기로 멈추지 않게 함
      (`ClaudeCodeEngineAdapter`의 `--permission-mode acceptEdits`에 대응)
    """

    def __init__(self, model: str | None = None) -> None:
        self._model = model

    def build_command(self, session_id: str, task: Task) -> list[str]:
        command = ["codex", "exec", task.title, "--json", "--full-auto"]
        if self._model is not None:
            command.extend(["--model", self._model])
        return command

    def parse_result(self, execution_result: ExecutionResult) -> EngineResult:
        text = self._extract_text_from_ndjson(execution_result.stdout)
        if text is not None:
            return EngineResult(success=execution_result.returncode == 0, output=text)
        if execution_result.returncode == 0:
            return EngineResult(success=True, output=execution_result.stdout)
        return EngineResult(
            success=False,
            output=execution_result.stdout,
            error=execution_result.stderr or execution_result.stdout,
        )

    @staticmethod
    def _extract_text_from_ndjson(stdout: str) -> str | None:
        """`--json`은 상태 변화마다 한 줄씩 JSON 이벤트를 출력하므로,
        뒤에서부터 훑어 텍스트로 보이는 필드(content/message/text)를 가진
        첫 유효한 JSON 줄을 최종 결과로 취급한다."""
        for line in reversed(stdout.splitlines()):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(data, dict):
                continue
            for key in ("content", "message", "text"):
                if key in data:
                    return str(data[key])
        return None

    def capabilities(self) -> frozenset[str]:
        return frozenset({"code_generation", "codex"})

    def supports_parallel(self) -> bool:
        return True
