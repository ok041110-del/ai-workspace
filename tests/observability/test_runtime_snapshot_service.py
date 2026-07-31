from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.observability.runtime_snapshot_service import RuntimeSnapshotService

_PAYLOAD = {
    "model": {"display_name": "Sonnet 5"},
    "effort": {"level": "high"},
    "context_window": {
        "total_input_tokens": 1000,
        "total_output_tokens": 200,
        "context_window_size": 200000,
        "used_percentage": 0.5,
    },
}


def test_build_composes_all_analyzers(tmp_path: Path) -> None:
    service = RuntimeSnapshotService(VaultAdapter(tmp_path), tmp_path)

    snapshot = service.build(_PAYLOAD)

    assert snapshot.claude_runtime.model_display_name == "Sonnet 5"
    assert snapshot.workspace.project_name == "Unknown"
    assert len(snapshot.pipeline) == 7
    assert snapshot.git_runtime.current_branch is None
    assert snapshot.guardian_runtime.guardian_all_passed is None
    assert snapshot.vault_runtime.vault_connected is False
    assert snapshot.mcp_runtime.mcp_enabled is False


def test_build_does_not_write_to_vault(tmp_path: Path) -> None:
    service = RuntimeSnapshotService(VaultAdapter(tmp_path), tmp_path)

    service.build(_PAYLOAD)

    assert not (tmp_path / "15 Project Intelligence").exists()
