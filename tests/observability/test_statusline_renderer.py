from ai_workspace.observability.snapshot import (
    ClaudeRuntimeInfo,
    GitRuntimeInfo,
    GuardianRuntimeInfo,
    McpRuntimeInfo,
    PipelineStageState,
    PipelineStageStatus,
    VaultRuntimeInfo,
    WorkspaceInfo,
    WorkspaceRuntimeSnapshot,
)
from ai_workspace.observability.statusline_renderer import StatusLineRenderer

_GIT_RUNTIME = GitRuntimeInfo(
    current_branch="feature/m45",
    working_tree_dirty=False,
    ahead=1,
    behind=0,
    last_commit_summary="abc1234 커밋 메시지",
)
_GUARDIAN_RUNTIME = GuardianRuntimeInfo(
    guardian_all_passed=True,
    pytest_failed_count=0,
    ruff_status=None,
    mypy_status=None,
    coverage_percentage=None,
)
_VAULT_RUNTIME = VaultRuntimeInfo(
    vault_connected=True,
    current_milestone="M44 Recommendation Explainability",
    current_adr="ADR-0061 Recommendation Explainability",
    current_pr=None,
    last_modified_epoch=1234567890.0,
)
_MCP_RUNTIME = McpRuntimeInfo(
    mcp_enabled=True,
    configured_servers=("filesystem", "obsidian"),
    connected_servers=("filesystem",),
    active_server=None,
    available_tools=None,
    last_mcp_call=None,
    last_mcp_error=None,
)

_SNAPSHOT = WorkspaceRuntimeSnapshot(
    workspace=WorkspaceInfo(project_name="ai-workspace", milestone="M45 Workspace Observability"),
    claude_runtime=ClaudeRuntimeInfo(
        model_display_name="Sonnet 5",
        effort_level="high",
        context_used_tokens=137000,
        context_total_tokens=200000,
        context_used_percentage=68.5,
        input_tokens=137000,
        output_tokens=1200,
    ),
    pipeline=(
        PipelineStageState("Recommendation", PipelineStageStatus.OBSERVED_DONE, "존재"),
        PipelineStageState("Adaptation", PipelineStageStatus.STRUCTURAL_INCLUDED, "포함"),
        PipelineStageState("Explainability", PipelineStageStatus.OBSERVED_NOT_YET, "없음"),
        PipelineStageState("Orchestration", PipelineStageStatus.STRUCTURAL_INCLUDED, "포함"),
        PipelineStageState("Execution", PipelineStageStatus.OBSERVED_DONE, "존재"),
        PipelineStageState("Memory", PipelineStageStatus.NOT_OBSERVABLE, "관측 불가"),
        PipelineStageState("Experience", PipelineStageStatus.OBSERVED_NOT_YET, "없음"),
    ),
    git_runtime=_GIT_RUNTIME,
    guardian_runtime=_GUARDIAN_RUNTIME,
    vault_runtime=_VAULT_RUNTIME,
    mcp_runtime=_MCP_RUNTIME,
)


def test_render_includes_workspace_and_claude_runtime_line() -> None:
    text = StatusLineRenderer().render(_SNAPSHOT)

    assert "ai-workspace" in text
    assert "M45 Workspace Observability" in text
    assert "Sonnet 5" in text
    assert "Effort high" in text
    assert "137K/200K (68%)" in text


def test_render_includes_pipeline_line_with_symbols() -> None:
    text = StatusLineRenderer().render(_SNAPSHOT)

    assert "✓ Recommendation" in text
    assert "· Adaptation" in text
    assert "□ Explainability" in text
    assert "? Memory" in text


def test_render_includes_git_line() -> None:
    text = StatusLineRenderer().render(_SNAPSHOT)

    assert "Git feature/m45 (clean, +1/-0)" in text
    assert "abc1234 커밋 메시지" in text


def test_render_includes_guardian_line() -> None:
    text = StatusLineRenderer().render(_SNAPSHOT)

    assert "Guardian OK" in text
    assert "pytest 0 failed" in text
    assert "ruff N/A" in text
    assert "mypy N/A" in text
    assert "Coverage N/A" in text


def test_render_includes_vault_line() -> None:
    text = StatusLineRenderer().render(_SNAPSHOT)

    assert "Vault Connected" in text
    assert "ADR-0061 Recommendation Explainability" in text
    assert "PR N/A" in text


def test_render_includes_mcp_line() -> None:
    text = StatusLineRenderer().render(_SNAPSHOT)

    assert "MCP Enabled" in text
    assert "Configured [filesystem, obsidian]" in text
    assert "Connected [filesystem]" in text


def test_render_handles_missing_claude_runtime_fields_without_guessing() -> None:
    snapshot = WorkspaceRuntimeSnapshot(
        workspace=WorkspaceInfo(project_name="ai-workspace", milestone="Unknown"),
        claude_runtime=ClaudeRuntimeInfo(
            model_display_name=None,
            effort_level=None,
            context_used_tokens=None,
            context_total_tokens=None,
            context_used_percentage=None,
            input_tokens=None,
            output_tokens=None,
        ),
        pipeline=(),
        git_runtime=GitRuntimeInfo(
            current_branch=None,
            working_tree_dirty=None,
            ahead=None,
            behind=None,
            last_commit_summary=None,
        ),
        guardian_runtime=GuardianRuntimeInfo(
            guardian_all_passed=None,
            pytest_failed_count=None,
            ruff_status=None,
            mypy_status=None,
            coverage_percentage=None,
        ),
        vault_runtime=VaultRuntimeInfo(
            vault_connected=False,
            current_milestone="Unknown",
            current_adr="Unknown",
            current_pr=None,
            last_modified_epoch=None,
        ),
        mcp_runtime=McpRuntimeInfo(
            mcp_enabled=False,
            configured_servers=(),
            connected_servers=None,
            active_server=None,
            available_tools=None,
            last_mcp_call=None,
            last_mcp_error=None,
        ),
    )

    text = StatusLineRenderer().render(snapshot)

    assert "N/A" in text
