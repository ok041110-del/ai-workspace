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
    """Vault/저장소 자체에서 읽은 Workspace 식별 정보. `current_workflow`/
    `current_task`는 Phase 1 범위 밖 — 이 저장소의 Recommendation 계열
    코드는 상시 실행되는 프로세스가 아니라 요청-응답형 함수 호출이라,
    별도 프로세스인 StatusLine이 "지금 실행 중인 Workflow/Task"를
    알려면 기존 Domain 코드에 상태 기록을 추가해야 한다 — Domain
    책임 변경 금지 원칙과 충돌해 항상 `None`(ADR-0063 Phase 2 후보)."""

    project_name: str
    milestone: str
    current_workflow: str | None = None
    current_task: str | None = None


@dataclass(frozen=True)
class GitRuntimeInfo:
    """`git` 하위 명령(읽기 전용)만으로 채운다. `ahead`/`behind`는
    `git fetch`를 하지 않으므로 마지막으로 로컬에 캐시된 원격 추적
    브랜치 기준 — 최신 원격 상태를 보장하지 않는다(ADR-0063)."""

    current_branch: str | None
    working_tree_dirty: bool | None
    ahead: int | None
    behind: int | None
    last_commit_summary: str | None


class AutomationGateStatus(Enum):
    """가장 최근 Automation 실행(`RecommendationOrchestrationService`
    경유)에서 Guardian이 Execution을 막았는지를 나타내는 상태(M48,
    ADR-0065). `guardian_all_passed`(라이브 재평가, M45)와는 다른
    질문에 답한다 — "지금 소스가 통과하는가"가 아니라 "가장 최근
    Automation 실행이 Guardian 때문에 막혔는가"(이력)."""

    PASS = "pass"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class GuardianRuntimeInfo:
    """`guardian.checker.evaluate()`(M41)만 재사용해 `guardian_all_passed`
    를 채운다. `pytest_failed_count`는 `.pytest_cache`의 마지막 로컬
    실행 결과(재실행 아님)다. `ruff_status`/`mypy_status`/
    `coverage_percentage`는 이 저장소에 캐시된 pass/fail 요약이 없고
    매 갱신마다 재실행하면 지연 위험이 커 Phase 1은 항상 `None`
    (Not Available, ADR-0063). `last_automation_gate_status`/
    `last_automation_gate_reason`은 M48에서 추가 — Vault
    `Recommendation Execution.md`(M36)에 이미 기록되는 Gate 판정
    이유를 재사용해 채우며, 그 문서가 아직 없으면(Automation이 한
    번도 실행되지 않음) `UNKNOWN`/`None`으로 정직하게 남긴다."""

    guardian_all_passed: bool | None
    pytest_failed_count: int | None
    ruff_status: str | None
    mypy_status: str | None
    coverage_percentage: float | None
    last_automation_gate_status: AutomationGateStatus = AutomationGateStatus.UNKNOWN
    last_automation_gate_reason: str | None = None


@dataclass(frozen=True)
class VaultRuntimeInfo:
    """`VaultAdapter.report_last_modified()`(M45)만 재사용한다.
    `current_pr`은 GitHub API 조회(네트워크 호출 + 인증)가 필요해
    Phase 1은 항상 `None`(Not Available) — 로컬에서 확인 가능한 대안은
    `GitRuntimeInfo.current_branch`."""

    vault_connected: bool
    current_milestone: str
    current_adr: str
    current_pr: str | None
    last_modified_epoch: float | None


@dataclass(frozen=True)
class McpRuntimeInfo:
    """`.mcp.json`(공식 문서화된 설정 파일)과 `claude mcp list`(공식
    CLI, 문서화된 상태 기호만 매칭)로만 채운다. `active_server`/
    `available_tools`/`last_mcp_call`/`last_mcp_error`는 정적 조회로
    확인할 공식 경로가 없어 Phase 1은 항상 `None`(Not Available,
    ADR-0063 Phase 2 후보 — Hook 기반 기록은 새 메커니즘 추가라 별도
    승인 필요)."""

    mcp_enabled: bool
    configured_servers: tuple[str, ...]
    connected_servers: tuple[str, ...] | None
    active_server: str | None
    available_tools: int | None
    last_mcp_call: str | None
    last_mcp_error: str | None


@dataclass(frozen=True)
class WorkspaceRuntimeSnapshot:
    """StatusLine(및 향후 Dashboard/CLI/Web UI 재사용 후보)이 표시만
    하는 단일 읽기 전용 Runtime 모델(ADR-0062/ADR-0063). 이 객체
    자체는 아무 것도 계산하지 않는다 — `RuntimeSnapshotService`가
    이미 계산한 값을 조립해서 넘겨줄 뿐이다."""

    workspace: WorkspaceInfo
    claude_runtime: ClaudeRuntimeInfo
    pipeline: tuple[PipelineStageState, ...]
    git_runtime: GitRuntimeInfo
    guardian_runtime: GuardianRuntimeInfo
    vault_runtime: VaultRuntimeInfo
    mcp_runtime: McpRuntimeInfo
