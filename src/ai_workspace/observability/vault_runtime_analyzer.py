"""Observability Layer — Vault Runtime Analyzer (ADR-0063, Milestone 45 확장).

`VaultAdapter.report_last_modified()`(M45)만 재사용해 Vault 산출물의
존재/최신 여부를 읽는다 — 새 Adapter 없음. `Current Milestone`은
`WorkspaceInfoAnalyzer`(M45)를 그대로 호출해 재사용하고 값을 새로
계산하지 않는다. `Current PR`은 GitHub API 조회(네트워크 호출 +
인증)가 필요해 Read-Only/저지연 StatusLine 원칙과 맞지 않아 Phase 1
에서 `None`(Not Available)으로 남긴다 — 로컬에서 확인 가능한
대안(현재 브랜치명)은 `GitRuntimeInfo.current_branch`로 이미
노출된다."""

from __future__ import annotations

import re
from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.observability.snapshot import VaultRuntimeInfo
from ai_workspace.observability.workspace_info_analyzer import WorkspaceInfoAnalyzer

_MILESTONES_INDEX = ("11 Milestones", "Milestones Index.md")
_ADR_INDEX = ("03 ADR", "ADR Index.md")
_ADR_HEADING = re.compile(r"^##\s*ADR-(\d+):\s*(.+)$")
_UNKNOWN = "Unknown"


class VaultRuntimeAnalyzer:
    def analyze(self, vault_adapter: VaultAdapter, project_root: Path) -> VaultRuntimeInfo:
        """
        입력: vault_adapter(읽기 전용), project_root
        출력: `VaultRuntimeInfo`
        예외: 없음
        보장: Vault에 쓰지 않는다.
        """
        milestones_mtime = vault_adapter.report_last_modified(*_MILESTONES_INDEX)
        adr_mtime = vault_adapter.report_last_modified(*_ADR_INDEX)
        report_mtimes = _known_report_mtimes(vault_adapter)

        candidates = [m for m in (milestones_mtime, adr_mtime, *report_mtimes) if m is not None]

        return VaultRuntimeInfo(
            vault_connected=milestones_mtime is not None,
            current_milestone=WorkspaceInfoAnalyzer().analyze(project_root).milestone,
            current_adr=_read_latest_adr(project_root),
            current_pr=None,
            last_modified_epoch=max(candidates) if candidates else None,
        )


def _known_report_mtimes(vault_adapter: VaultAdapter) -> list[float | None]:
    known_reports = (
        ("15 Project Intelligence", "Recommendation Intelligence.md"),
        ("15 Project Intelligence", "Recommendation Explanation.md"),
        ("15 Project Intelligence", "Recommendation Execution.md"),
        ("15 Project Intelligence", "Experience Intelligence.md"),
    )
    return [vault_adapter.report_last_modified(*path_parts) for path_parts in known_reports]


def _read_latest_adr(project_root: Path) -> str:
    index_path = project_root.joinpath(*_ADR_INDEX)
    if not index_path.exists():
        return _UNKNOWN

    latest_number = -1
    latest_title = _UNKNOWN
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = _ADR_HEADING.match(line)
        if match is None:
            continue
        number = int(match.group(1))
        if number > latest_number:
            latest_number = number
            latest_title = match.group(2).strip()

    if latest_number == -1:
        return _UNKNOWN
    return f"ADR-{latest_number:04d} {latest_title}"
