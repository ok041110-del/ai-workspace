"""Observability Layer — Guardian Runtime Analyzer (ADR-0063, Milestone 45 확장).

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
`None`."""

from __future__ import annotations

import json
from pathlib import Path

from ai_workspace.guardian.checker import evaluate
from ai_workspace.guardian.rules import GUARDIAN_RULES
from ai_workspace.observability.snapshot import GuardianRuntimeInfo

_SRC_ROOT = ("src", "ai_workspace")
_PYTEST_LASTFAILED = (".pytest_cache", "v", "cache", "lastfailed")


class GuardianRuntimeAnalyzer:
    def analyze(self, project_root: Path) -> GuardianRuntimeInfo:
        """
        입력: project_root
        출력: `GuardianRuntimeInfo`
        예외: 없음
        보장: `pytest`/`ruff`/`mypy`를 실행하지 않는다(재실행 없음) —
              Guardian만 그 자리에서 평가하고, 나머지는 이미 존재하는
              캐시 파일만 읽는다.
        """
        return GuardianRuntimeInfo(
            guardian_all_passed=_read_guardian_status(project_root),
            pytest_failed_count=_read_pytest_last_known_failed_count(project_root),
            ruff_status=None,
            mypy_status=None,
            coverage_percentage=None,
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
