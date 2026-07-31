"""Observability Layer — Workspace Info Analyzer (ADR-0062, Milestone 45).

`pyproject.toml`(Project 이름)과 `11 Milestones/Milestones Index.md`
(가장 큰 번호의 Milestone 행)만 읽는 순수 Analyzer. `current_workflow`
는 Phase 1 범위 밖이라 항상 `None`이다(§13.2 Workflow와 혼동을
피하기 위해 근거 없이 값을 채우지 않는다, ADR-0062 결정 4)."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from ai_workspace.observability.snapshot import WorkspaceInfo

_MILESTONE_ROW = re.compile(r"^\|\s*M(\d+)\s*\|\s*([^|]+?)\s*\|")
_UNKNOWN = "Unknown"


class WorkspaceInfoAnalyzer:
    def analyze(self, project_root: Path) -> WorkspaceInfo:
        """
        입력: project_root(저장소 루트로 간주할 경로)
        출력: `WorkspaceInfo`
        예외: 없음
        보장: 파일이 없으면 추정하지 않고 "Unknown"을 반환한다.
        """
        return WorkspaceInfo(
            project_name=_read_project_name(project_root),
            milestone=_read_latest_milestone(project_root),
        )


def _read_project_name(project_root: Path) -> str:
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        return _UNKNOWN
    with pyproject_path.open("rb") as file:
        data = tomllib.load(file)
    return str(data.get("project", {}).get("name", _UNKNOWN))


def _read_latest_milestone(project_root: Path) -> str:
    index_path = project_root / "11 Milestones" / "Milestones Index.md"
    if not index_path.exists():
        return _UNKNOWN

    latest_number = -1
    latest_name = _UNKNOWN
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = _MILESTONE_ROW.match(line)
        if match is None:
            continue
        number = int(match.group(1))
        if number > latest_number:
            latest_number = number
            latest_name = match.group(2).strip()

    if latest_number == -1:
        return _UNKNOWN
    return f"M{latest_number} {latest_name}"
