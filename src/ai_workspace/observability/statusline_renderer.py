"""Observability Layer — StatusLine Renderer (ADR-0062, Milestone 45).

`WorkspaceRuntimeSnapshot`을 Claude Code StatusLine에 그대로 찍을
평문 문자열로 바꾸는 순수 함수형 Renderer — 입출력 변환만 하고
I/O를 하지 않는다(`render_markdown()`류의 Vault 렌더링 함수와 동일한
원칙, 다만 대상이 Markdown이 아니라 터미널 한 줄이라는 점만 다르다).
Dashboard/CLI/Web UI가 같은 `WorkspaceRuntimeSnapshot`을 다른
Renderer로 재사용할 수 있도록, 이 모듈은 StatusLine 전용 포맷에만
책임을 진다."""

from __future__ import annotations

from ai_workspace.observability.snapshot import (
    ClaudeRuntimeInfo,
    PipelineStageState,
    PipelineStageStatus,
    WorkspaceRuntimeSnapshot,
)

_STAGE_SYMBOL = {
    PipelineStageStatus.OBSERVED_DONE: "✓",
    PipelineStageStatus.OBSERVED_NOT_YET: "□",
    PipelineStageStatus.STRUCTURAL_INCLUDED: "·",
    PipelineStageStatus.NOT_OBSERVABLE: "?",
}


class StatusLineRenderer:
    def render(self, snapshot: WorkspaceRuntimeSnapshot) -> str:
        """
        입력: snapshot(`RuntimeSnapshotService.build()`의 결과)
        출력: StatusLine에 그대로 출력할 평문 문자열(여러 줄 가능)
        예외: 없음
        보장: side-effect 없음(print/파일쓰기 안 함) — 문자열만 만든다.
        """
        lines = [
            _render_workspace_line(snapshot),
            _render_pipeline_line(snapshot.pipeline),
        ]
        return "\n".join(lines)


def _render_workspace_line(snapshot: WorkspaceRuntimeSnapshot) -> str:
    workspace = snapshot.workspace
    parts = [workspace.project_name, workspace.milestone]
    if workspace.current_workflow:
        parts.append(workspace.current_workflow)
    parts.append(_render_claude_runtime(snapshot.claude_runtime))
    return " · ".join(parts)


def _render_claude_runtime(info: ClaudeRuntimeInfo) -> str:
    model = info.model_display_name or "N/A"
    effort = info.effort_level or "N/A"
    context = _render_context(info)
    return f"{model} · Effort {effort} · Context {context}"


def _render_context(info: ClaudeRuntimeInfo) -> str:
    if info.context_used_tokens is None or info.context_total_tokens is None:
        return "N/A"
    used = _format_tokens(info.context_used_tokens)
    total = _format_tokens(info.context_total_tokens)
    if info.context_used_percentage is None:
        return f"{used}/{total}"
    return f"{used}/{total} ({info.context_used_percentage:.0f}%)"


def _format_tokens(count: int) -> str:
    if count < 1000:
        return str(count)
    return f"{count / 1000:.0f}K"


def _render_pipeline_line(pipeline: tuple[PipelineStageState, ...]) -> str:
    return "  ".join(f"{_STAGE_SYMBOL[stage.status]} {stage.name}" for stage in pipeline)
