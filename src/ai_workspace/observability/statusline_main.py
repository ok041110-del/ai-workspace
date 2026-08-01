"""Observability Layer — StatusLine 진입점 (ADR-0062, Milestone 45 / M45-1
Integration Fix, ADR-0069).

`.claude/settings.json`의 `statusLine.command`가 실행하는 스크립트.
stdin으로 Claude Code StatusLine JSON을 받아 `RuntimeSnapshotService`
로 `WorkspaceRuntimeSnapshot`을 만들고 `StatusLineRenderer`로 출력한다.
StatusLine은 실패 시 빈 줄로 사라지므로(공식 문서), 어떤 예외도
바깥으로 내보내지 않고 항상 사람이 읽을 수 있는 한 줄을 출력한다 —
`ai_workspace.*` import 자체가 실패하는 경우(PYTHONPATH 미설정,
의존성 미설치된 `python3` 사용 등)도 포함하기 위해 import를 `main()`
안으로 옮겼다(M45-1에서 발견된 실제 원인: 기존 코드는 import가
try/except 바깥에 있어 import 실패 시 아무 출력 없이 프로세스가 죽고
StatusLine이 조용히 사라졌다).

디버그 로그(`/tmp/statusline.log`)는 실패했을 때만 남긴다(정상 동작
시 로그 없음). 실제 Runtime JSON Schema를 한 번 확인하고 싶을 때는
`AI_WORKSPACE_STATUSLINE_DEBUG=1` 환경 변수로 원본 stdin을 강제로
기록할 수 있다(추측 대신 실제 payload로 검증하기 위함)."""

from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path

_DEBUG_LOG_PATH = Path("/tmp/statusline.log")
_DEBUG_ENV_VAR = "AI_WORKSPACE_STATUSLINE_DEBUG"


def _append_log(stage: str, raw_stdin: str, detail: str) -> None:
    try:
        with _DEBUG_LOG_PATH.open("a", encoding="utf-8") as log_file:
            log_file.write(f"--- StatusLine {stage} ---\n")
            log_file.write(f"raw stdin: {raw_stdin!r}\n")
            log_file.write(f"{detail}\n\n")
    except OSError:
        pass  # 로그조차 남길 수 없어도 StatusLine 출력 자체는 계속되어야 한다.


def main() -> int:
    raw_stdin = sys.stdin.read()

    if os.environ.get(_DEBUG_ENV_VAR):
        _append_log("디버그 캡처(정상 동작)", raw_stdin, "AI_WORKSPACE_STATUSLINE_DEBUG=1 요청")

    try:
        payload = json.loads(raw_stdin or "{}")
    except json.JSONDecodeError as error:
        _append_log("stdin JSON 파싱 실패", raw_stdin, "".join(traceback.format_exception(error)))
        payload = {}

    workspace = payload.get("workspace") or {}
    project_root = Path(workspace.get("project_dir") or payload.get("cwd") or ".")

    try:
        from ai_workspace.integration.vault_adapter import VaultAdapter
        from ai_workspace.observability.runtime_snapshot_service import RuntimeSnapshotService
        from ai_workspace.observability.statusline_renderer import StatusLineRenderer

        vault_adapter = VaultAdapter(project_root)
        service = RuntimeSnapshotService(vault_adapter, project_root)
        snapshot = service.build(payload)
        print(StatusLineRenderer().render(snapshot))
    except Exception as error:  # StatusLine은 절대 죽으면 안 됨(공식 문서 권고)
        _append_log(
            "Snapshot 생성/렌더링 실패", raw_stdin, "".join(traceback.format_exception(error))
        )
        print(f"AI Workspace Observability: 초기화 실패 ({error})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
