"""Workspace Observability — 읽기 전용 Runtime 값 객체 (ADR-0062, Milestone 45).

`Observability`(§13.3 Behavioral Concept)가 다루는 모든 산출물은 이미
존재하는 상태(Claude Code 세션 정보, Vault 산출물의 존재/최신 여부)를
그대로 반영할 뿐 새 판단을 만들지 않는다 — 이 파일은 그 반영 결과를
담는 순수 값 객체만 정의한다(메서드 없음, `guardian/rules.py`의
`*Rule`과 동일한 원칙)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ClaudeRuntimeInfo:
    """Claude Code StatusLine stdin JSON에서 그대로 옮겨온 필드만 담는다.
    Claude Code가 제공하지 않는 값은 `None`으로 남기고 추정하지 않는다
    (`effort_level`은 모델이 effort 파라미터를 지원하지 않으면 부재)."""

    model_display_name: str | None
    effort_level: str | None
    context_used_tokens: int | None
    context_total_tokens: int | None
    context_used_percentage: float | None
    input_tokens: int | None
    output_tokens: int | None


class PipelineStageStatus(Enum):
    """Pipeline Stage 하나의 관측 상태(ADR-0062 결정 3 — Phase 1은
    있는 그대로의 한계를 숨기지 않는다)."""

    OBSERVED_DONE = "observed_done"
    OBSERVED_NOT_YET = "observed_not_yet"
    STRUCTURAL_INCLUDED = "structural_included"
    NOT_OBSERVABLE = "not_observable"


@dataclass(frozen=True)
class PipelineStageState:
    """Pipeline 7단계(Recommendation→Adaptation→Explainability→
    Orchestration→Execution→Memory→Experience) 중 하나의 상태.
    `note`는 그 판정의 근거(어떤 Vault 산출물을 봤는지, 혹은 왜
    관측할 수 없는지)를 사람이 읽을 수 있게 남긴다."""

    name: str
    status: PipelineStageStatus
    note: str


@dataclass(frozen=True)
class WorkspaceInfo:
    """Vault/저장소 자체에서 읽은 Workspace 식별 정보. `current_workflow`
    는 Phase 1 범위 밖(§13.2 Workflow와 혼동 방지를 위해 근거 없는
    추정을 하지 않음) — 항상 `None`이다."""

    project_name: str
    milestone: str
    current_workflow: str | None = None


@dataclass(frozen=True)
class WorkspaceRuntimeSnapshot:
    """StatusLine(및 향후 Dashboard/CLI/Web UI 재사용 후보)이 표시만
    하는 단일 읽기 전용 Runtime 모델(ADR-0062). 이 객체 자체는 아무
    것도 계산하지 않는다 — `RuntimeSnapshotService`가 이미 계산한
    값을 조립해서 넘겨줄 뿐이다."""

    workspace: WorkspaceInfo
    claude_runtime: ClaudeRuntimeInfo
    pipeline: tuple[PipelineStageState, ...]
