"""Observability Layer — Claude Runtime Analyzer (ADR-0062, Milestone 45).

Claude Code StatusLine이 stdin으로 넘기는 JSON(공식 문서 `model`/
`effort`/`context_window` 필드)을 그대로 옮겨 담는 순수 Analyzer.
`*Analyzer` 명명 규칙(§13.6)대로 부작용 없음, 생성자 인자 없이
`analyze()`만 제공한다. 필드가 없으면 값을 지어내지 않고 `None`을
그대로 반환한다."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ai_workspace.observability.snapshot import ClaudeRuntimeInfo


class ClaudeRuntimeAnalyzer:
    def analyze(self, payload: Mapping[str, Any]) -> ClaudeRuntimeInfo:
        """
        입력: payload(Claude Code StatusLine stdin JSON을 `json.loads`한 dict)
        출력: `ClaudeRuntimeInfo`
        예외: 없음
        보장: payload에 없는 필드는 추정하지 않고 `None`으로 남긴다.
        """
        model = payload.get("model") or {}
        effort = payload.get("effort") or {}
        context_window = payload.get("context_window") or {}

        return ClaudeRuntimeInfo(
            model_display_name=model.get("display_name"),
            effort_level=effort.get("level"),
            context_used_tokens=context_window.get("total_input_tokens"),
            context_total_tokens=context_window.get("context_window_size"),
            context_used_percentage=context_window.get("used_percentage"),
            input_tokens=context_window.get("total_input_tokens"),
            output_tokens=context_window.get("total_output_tokens"),
        )
