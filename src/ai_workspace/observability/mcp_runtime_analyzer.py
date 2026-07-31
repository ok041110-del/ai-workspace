"""Observability Layer — MCP Runtime Analyzer (ADR-0063, Milestone 45 확장).

Claude Code 공식 문서(`code.claude.com/docs/en/mcp`)가 확인해 주는
두 가지 경로만 사용한다:

1. **`.mcp.json`(프로젝트 범위 설정 파일, 공식 문서화된 스키마)** —
   `mcpServers` 키를 그대로 읽어 "어떤 서버가 설정돼 있는가"만
   확인한다. 파일이 없으면 `mcp_enabled=False`.
2. **`claude mcp list`(공식 CLI 하위 명령)** — 서버별 연결 상태를
   사람이 읽는 텍스트로 출력한다(JSON 옵션 없음, 공식 문서 확인).
   문서가 확인해 준 상태 기호(`✔`=Connected, `✘`=Failed/Connection
   error, `!`=Needs auth, `⏸`=Pending approval)만 그대로 매칭한다 —
   기호가 안 보이거나 출력 형식이 예상과 다르면 추측하지 않고
   `connected_servers=None`(Not Available)으로 남긴다. 이 명령은
   `claude` 바이너리를 하위 프로세스로 실행하므로 짧은 타임아웃을
   두고, 실패/타임아웃 시 전체를 Not Available로 되돌린다.

**Phase 1에서 Not Available로 남기는 항목(이유 명시)**:
- `active_server`: 정적 조회로는 "지금 이 순간" 호출 중인 서버를
  알 수 없다 — 실시간 계측(Hook)이 필요하며 Phase 2 후보.
- `available_tools`: `claude mcp list`/`get` 출력에 도구 개수가
  보장된 형식으로 없어 안전하게 파싱할 수 없다.
- `last_mcp_call`/`last_mcp_error`: Claude Code가 공식적으로 로그
  파일을 문서화하지 않는다. Hook(`PostToolUse`)으로 직접 기록하는
  방법은 있지만, 이는 새로운 기록 메커니즘(Hook 추가)을 도입하는
  것이라 이번 Phase 1(순수 읽기, 새 메커니즘 추가 없음) 범위 밖으로
  남기고 별도 승인 대상인 Phase 2 후보로 문서화한다(ADR-0063)."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from ai_workspace.observability.snapshot import McpRuntimeInfo

_MCP_CONFIG_FILENAME = ".mcp.json"
_TIMEOUT_SECONDS = 2.0
_SERVER_LINE = re.compile(r"^\s*([\w.\-]+)\s*[:\-]?.*(✔|✘|!|⏸)")


class McpRuntimeAnalyzer:
    def analyze(self, project_root: Path) -> McpRuntimeInfo:
        """
        입력: project_root
        출력: `McpRuntimeInfo`
        예외: 없음
        보장: MCP 서버에 어떤 명령도 실행하지 않는다(조회만). 형식이
              불확실하면 추측 대신 `None`(Not Available)을 반환한다.
        """
        configured_servers = _read_configured_servers(project_root)
        return McpRuntimeInfo(
            mcp_enabled=len(configured_servers) > 0,
            configured_servers=configured_servers,
            connected_servers=_read_connected_servers(project_root, configured_servers),
            active_server=None,
            available_tools=None,
            last_mcp_call=None,
            last_mcp_error=None,
        )


def _read_configured_servers(project_root: Path) -> tuple[str, ...]:
    config_path = project_root / _MCP_CONFIG_FILENAME
    if not config_path.exists():
        return ()
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ()
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        return ()
    return tuple(servers.keys())


def _read_connected_servers(
    project_root: Path, configured_servers: tuple[str, ...]
) -> tuple[str, ...] | None:
    if not configured_servers:
        return ()

    try:
        result = subprocess.run(
            ["claude", "mcp", "list"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None

    connected = []
    for line in result.stdout.splitlines():
        match = _SERVER_LINE.match(line)
        if match is None:
            continue
        name, symbol = match.group(1), match.group(2)
        if symbol == "✔" and name in configured_servers:
            connected.append(name)
    return tuple(connected)
