"""Observability Layer — Runtime Snapshot Service (ADR-0062/ADR-0063/
ADR-0072, Milestone 45 + 확장).

8개 Analyzer(`ClaudeRuntimeAnalyzer`/`PipelineStageAnalyzer`/
`WorkspaceInfoAnalyzer`/`GitRuntimeAnalyzer`/`GuardianRuntimeAnalyzer`/
`VaultRuntimeAnalyzer`/`McpRuntimeAnalyzer`/`LearningRuntimeAnalyzer`)
호출만 조합하는 얇은 Service(§13.6 `*Service` 역할 —
`RecommendationExplanationService`와 동일한 뼈대). 판정 로직을 전혀
갖지 않는다."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.observability.claude_runtime_analyzer import ClaudeRuntimeAnalyzer
from ai_workspace.observability.git_runtime_analyzer import GitRuntimeAnalyzer
from ai_workspace.observability.guardian_runtime_analyzer import GuardianRuntimeAnalyzer
from ai_workspace.observability.learning_runtime_analyzer import LearningRuntimeAnalyzer
from ai_workspace.observability.mcp_runtime_analyzer import McpRuntimeAnalyzer
from ai_workspace.observability.pipeline_stage_analyzer import PipelineStageAnalyzer
from ai_workspace.observability.snapshot import WorkspaceRuntimeSnapshot
from ai_workspace.observability.vault_runtime_analyzer import VaultRuntimeAnalyzer
from ai_workspace.observability.workspace_info_analyzer import WorkspaceInfoAnalyzer


class RuntimeSnapshotService:
    def __init__(self, vault_adapter: VaultAdapter, project_root: Path) -> None:
        self._vault_adapter = vault_adapter
        self._project_root = project_root
        self._claude_runtime_analyzer = ClaudeRuntimeAnalyzer()
        self._pipeline_stage_analyzer = PipelineStageAnalyzer()
        self._workspace_info_analyzer = WorkspaceInfoAnalyzer()
        self._git_runtime_analyzer = GitRuntimeAnalyzer()
        self._guardian_runtime_analyzer = GuardianRuntimeAnalyzer()
        self._vault_runtime_analyzer = VaultRuntimeAnalyzer()
        self._mcp_runtime_analyzer = McpRuntimeAnalyzer()
        self._learning_runtime_analyzer = LearningRuntimeAnalyzer()

    def build(self, statusline_payload: Mapping[str, Any]) -> WorkspaceRuntimeSnapshot:
        """
        입력: statusline_payload(Claude Code StatusLine stdin JSON)
        출력: `WorkspaceRuntimeSnapshot`(읽기 전용, side-effect 없음)
        예외: 없음
        보장: Vault에 쓰지 않는다. 기존 Domain(Recommendation/Adaptation/
              Explainability/Orchestration/Execution/Memory/Experience)의
              책임을 바꾸지 않는다 — 그 산출물을 읽기만 한다.
        """
        learning_runtime = self._learning_runtime_analyzer.analyze(self._project_root)
        return WorkspaceRuntimeSnapshot(
            workspace=self._workspace_info_analyzer.analyze(self._project_root),
            claude_runtime=self._claude_runtime_analyzer.analyze(statusline_payload),
            pipeline=self._pipeline_stage_analyzer.analyze(
                self._vault_adapter,
                has_learning_records=learning_runtime.tracked_task_count > 0,
            ),
            git_runtime=self._git_runtime_analyzer.analyze(self._project_root),
            guardian_runtime=self._guardian_runtime_analyzer.analyze(self._project_root),
            vault_runtime=self._vault_runtime_analyzer.analyze(
                self._vault_adapter, self._project_root
            ),
            mcp_runtime=self._mcp_runtime_analyzer.analyze(self._project_root),
            learning_runtime=learning_runtime,
        )
