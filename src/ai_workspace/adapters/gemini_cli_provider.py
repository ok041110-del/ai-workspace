from __future__ import annotations

import json

from ai_workspace.adapters.cli_provider import CLIProvider
from ai_workspace.adapters.process_runner import ProcessResult
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import EngineResult


class GeminiCliProvider(CLIProvider):
    """Google Gemini CLI(`gemini`)용 `CLIProvider`(M5-T05).

    **미검증 경고**: 이 저장소 환경에는 `gemini` CLI가 설치되어 있지
    않아 실제 실행으로 플래그를 검증하지 못했다. 아래 명령 구성은 공개
    문서(Gemini CLI Headless Mode/Configuration, 2026-07 기준 웹 검색)를
    근거로 했다 — 실제 사용 전 `gemini --help`로 재확인을 권장한다.

    - `gemini -p "<prompt>" --output-format json`: 비대화형 프롬프트 +
      JSON 출력(`{"response": ..., "stats": {...}}` 형태)
    - `--non-interactive`: 프롬프트가 파이프라인을 막지 않게 함
    - `--yolo`: 모든 도구 실행을 자동 승인(헤드리스 환경에서 승인 대기로
      멈추지 않게 함, `ClaudeCodeEngineAdapter`의
      `--permission-mode acceptEdits`에 대응)
    """

    def __init__(self, model: str | None = None) -> None:
        self._model = model

    def build_command(self, session_id: str, task: Task) -> list[str]:
        command = [
            "gemini",
            "-p",
            task.title,
            "--output-format",
            "json",
            "--non-interactive",
            "--yolo",
        ]
        if self._model is not None:
            command.extend(["--model", self._model])
        return command

    def parse_result(self, process_result: ProcessResult) -> EngineResult:
        data = self._parse_json(process_result.stdout)
        if data is not None and "response" in data:
            return EngineResult(
                success=process_result.returncode == 0, output=str(data["response"])
            )
        if process_result.returncode == 0:
            return EngineResult(success=True, output=process_result.stdout)
        return EngineResult(
            success=False,
            output=process_result.stdout,
            error=process_result.stderr or process_result.stdout,
        )

    @staticmethod
    def _parse_json(stdout: str) -> dict[str, object] | None:
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None

    def capabilities(self) -> frozenset[str]:
        return frozenset({"code_generation", "gemini"})

    def supports_parallel(self) -> bool:
        return True
