"""Observability Layer — StatusLine 진입점 (ADR-0062, Milestone 45).

`.claude/settings.json`의 `statusLine.command`가 실행하는 스크립트.
stdin으로 Claude Code StatusLine JSON을 받아 `RuntimeSnapshotService`
로 `WorkspaceRuntimeSnapshot`을 만들고 `StatusLineRenderer`로 출력한다.
StatusLine은 실패 시 빈 줄로 사라지므로(공식 문서), 어떤 예외도
바깥으로 내보내지 않고 항상 사람이 읽을 수 있는 한 줄을 출력한다."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.observability.runtime_snapshot_service import RuntimeSnapshotService
from ai_workspace.observability.statusline_renderer import StatusLineRenderer


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        payload = {}

    workspace = payload.get("workspace") or {}
    project_root = Path(workspace.get("project_dir") or payload.get("cwd") or ".")

    try:
        vault_adapter = VaultAdapter(project_root)
        service = RuntimeSnapshotService(vault_adapter, project_root)
        snapshot = service.build(payload)
        print(StatusLineRenderer().render(snapshot))
    except Exception as error:  # StatusLine은 절대 죽으면 안 됨(공식 문서 권고)
        print(f"AI Workspace Observability: 초기화 실패 ({error})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
