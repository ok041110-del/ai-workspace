"""Observability Layer — Guardian Runtime Analyzer (ADR-0063/ADR-0065,
Milestone 45 확장/Milestone 48).

`guardian.checker.evaluate()`(M41, ADR-0056)는 AST 기반 순수 평가라
StatusLine 갱신마다 다시 호출해도 비용이 작다 — 그대로 재사용한다
(새 판단 로직 추가 아님, Guardian의 기존 계약을 읽기만 함).

`pytest`/`ruff`/`mypy`/Coverage는 전체 실행 자체가 수 초 이상 걸려
StatusLine 갱신마다 다시 실행하면 지연·타임아웃 위험이 크다 —
매번 재실행하지 않고, `pytest`가 로컬에 남긴 `.pytest_cache/v/cache/
lastfailed`(pytest 공식 캐시 파일)만 읽어 "마지막으로 로컬에서 실행한
결과"를 반영한다. `ruff`/`mypy`는 이 저장소에 그런 캐시된 pass/fail
요약이 없어(캐시 디렉터리는 있지만 최종 판정을 담지 않음) Phase 1에서
`None`(Not Available)으로 남긴다. Coverage는 `pytest-cov`가 이
저장소에 설정돼 있지 않아 `.coverage` 파일 자체가 없다 — 마찬가지로
`None`.

**Automation Gate 이력(M48, ADR-0065)**: `RecommendationOrchestrationService`
(M43)가 Guardian을 Execution 직전에 평가한 결과는 새 Vault
산출물이 아니라 이미 존재하는 `15 Project Intelligence/
Recommendation Execution.md`(M36)의 "이유" 줄에 그대로 기록된다
(`ExecutionGate`, ADR-0065). 이 Analyzer는 Vault Root == Repository
Root(ADR-0037)라는 이미 확립된 전제를 그대로 이용해, `.pytest_cache`
를 읽는 것과 같은 방식으로 그 문서를 직접 읽는다 — 새 `VaultAdapter`
메서드를 추가하지 않는다. 문서가 없으면(Automation이 한 번도
실행되지 않음) `AutomationGateStatus.UNKNOWN`으로 정직하게 남긴다
(추정 금지)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from ai_workspace.guardian.checker import evaluate
from ai_workspace.guardian.models import GUARDIAN_BLOCK_REASON_PREFIX
from ai_workspace.guardian.rules import GUARDIAN_RULES
from ai_workspace.observability.snapshot import AutomationGateStatus, GuardianRuntimeInfo

_SRC_ROOT = ("src", "ai_workspace")
_PYTEST_LASTFAILED = (".pytest_cache", "v", "cache", "lastfailed")
_EXECUTION_REPORT = ("15 Project Intelligence", "Recommendation Execution.md")
_REASON_LINE_PATTERN = re.compile(r"^- 이유: (.+)$", re.MULTILINE)


class GuardianRuntimeAnalyzer:
    def analyze(self, project_root: Path) -> GuardianRuntimeInfo:
        """
        입력: project_root
        출력: `GuardianRuntimeInfo`
        예외: 없음
        보장: `pytest`/`ruff`/`mypy`를 실행하지 않는다(재실행 없음) —
              Guardian만 그 자리에서 평가하고, 나머지는 이미 존재하는
              캐시 파일/Vault 문서만 읽는다.
        """
        gate_status, gate_reason = _read_last_automation_gate(project_root)
        return GuardianRuntimeInfo(
            guardian_all_passed=_read_guardian_status(project_root),
            pytest_failed_count=_read_pytest_last_known_failed_count(project_root),
            ruff_status=None,
            mypy_status=None,
            coverage_percentage=None,
            last_automation_gate_status=gate_status,
            last_automation_gate_reason=gate_reason,
        )


def _read_guardian_status(project_root: Path) -> bool | None:
    src_root = project_root.joinpath(*_SRC_ROOT)
    if not src_root.exists():
        return None
    report = evaluate(GUARDIAN_RULES, src_root)
    return report.all_passed


def _read_pytest_last_known_failed_count(project_root: Path) -> int | None:
    lastfailed_path = project_root.joinpath(*_PYTEST_LASTFAILED)
    if not lastfailed_path.exists():
        return None
    try:
        data = json.loads(lastfailed_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    return len(data)


def _read_last_automation_gate(
    project_root: Path,
) -> tuple[AutomationGateStatus, str | None]:
    report_path = project_root.joinpath(*_EXECUTION_REPORT)
    if not report_path.exists():
        return AutomationGateStatus.UNKNOWN, None
    text = report_path.read_text(encoding="utf-8")
    match = _REASON_LINE_PATTERN.search(text)
    if match is None:
        return AutomationGateStatus.UNKNOWN, None
    reason = match.group(1)
    if reason.startswith(GUARDIAN_BLOCK_REASON_PREFIX):
        return AutomationGateStatus.BLOCKED, reason
    return AutomationGateStatus.PASS, None
