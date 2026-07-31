import json
from pathlib import Path

from ai_workspace.observability.mcp_runtime_analyzer import McpRuntimeAnalyzer


def test_analyze_disabled_when_no_mcp_config(tmp_path: Path) -> None:
    info = McpRuntimeAnalyzer().analyze(tmp_path)

    assert info.mcp_enabled is False
    assert info.configured_servers == ()
    assert info.connected_servers == ()
    assert info.active_server is None
    assert info.available_tools is None
    assert info.last_mcp_call is None
    assert info.last_mcp_error is None


def test_analyze_reads_configured_servers_from_mcp_json(tmp_path: Path) -> None:
    (tmp_path / ".mcp.json").write_text(
        json.dumps(
            {
                "mcpServers": {
                    "filesystem": {"type": "stdio", "command": "npx"},
                    "obsidian": {"type": "http", "url": "https://example.com/mcp"},
                }
            }
        ),
        encoding="utf-8",
    )

    info = McpRuntimeAnalyzer().analyze(tmp_path)

    assert info.mcp_enabled is True
    assert set(info.configured_servers) == {"filesystem", "obsidian"}


def test_analyze_handles_malformed_mcp_json_without_guessing(tmp_path: Path) -> None:
    (tmp_path / ".mcp.json").write_text("not valid json", encoding="utf-8")

    info = McpRuntimeAnalyzer().analyze(tmp_path)

    assert info.mcp_enabled is False
    assert info.configured_servers == ()
