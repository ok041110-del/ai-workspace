"""Observability Layer — Runtime Snapshot Service (ADR-0062, Milestone 45).

3개 Analyzer(`ClaudeRuntimeAnalyzer`/`PipelineStageAnalyzer`/
`WorkspaceInfoAnalyzer`) 호출만 조합하는 얇은 Service(§13.6
`*Service` 역할 — `RecommendationExplanationService`와 동일한
뼈대). 판정 로직을 전혀 갖지 않는다."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.observability.claude_runtime_analyzer import ClaudeRuntimeAnalyzer
from ai_workspace.observability.pipeline_stage_analyzer import PipelineStageAnalyzer
from ai_workspace.observability.snapshot import WorkspaceRuntimeSnapshot
from ai_workspace.observability.workspace_info_analyzer import WorkspaceInfoAnalyzer


class RuntimeSnapshotService:
    def __init__(self, vault_adapter: VaultAdapter, project_root: Path) -> None:
        self._vault_adapter = vault_adapter
        self._project_root = project_root
        self._claude_runtime_analyzer = ClaudeRuntimeAnalyzer()
        self._pipeline_stage_analyzer = PipelineStageAnalyzer()
        self._workspace_info_analyzer = WorkspaceInfoAnalyzer()

    def build(self, statusline_payload: Mapping[str, Any]) -> WorkspaceRuntimeSnapshot:
        """
        입력: statusline_payload(Claude Code StatusLine stdin JSON)
        출력: `WorkspaceRuntimeSnapshot`(읽기 전용, side-effect 없음)
        예외: 없음
        보장: Vault에 쓰지 않는다. 기존 Domain(Recommendation/Adaptation/
              Explainability/Orchestration/Execution/Memory/Experience)의
              책임을 바꾸지 않는다 — 그 산출물을 읽기만 한다.
        """
        return WorkspaceRuntimeSnapshot(
            workspace=self._workspace_info_analyzer.analyze(self._project_root),
            claude_runtime=self._claude_runtime_analyzer.analyze(statusline_payload),
            pipeline=self._pipeline_stage_analyzer.analyze(self._vault_adapter),
        )
