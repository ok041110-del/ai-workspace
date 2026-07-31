from ai_workspace.observability.snapshot import (
    ClaudeRuntimeInfo,
    PipelineStageState,
    PipelineStageStatus,
    WorkspaceInfo,
    WorkspaceRuntimeSnapshot,
)
from ai_workspace.observability.statusline_renderer import StatusLineRenderer

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
    )

    text = StatusLineRenderer().render(snapshot)

    assert "N/A" in text
