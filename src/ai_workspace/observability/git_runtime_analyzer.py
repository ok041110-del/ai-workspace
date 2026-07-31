"""Observability Layer — Git Runtime Analyzer (ADR-0063, Milestone 45 확장).

로컬 `git` 실행 파일을 읽기 전용 하위 명령(`rev-parse`/`status --porcelain`/
`rev-list --left-right --count`/`log -1`)으로만 호출하는 순수 Analyzer.
쓰기 명령(`add`/`commit`/`push`/`fetch` 등)은 절대 실행하지 않는다 —
`fetch`를 하지 않으므로 `ahead`/`behind`는 마지막으로 로컬에 캐시된
원격 추적 브랜치 기준이며, 최신 원격 상태를 보장하지 않는다(Phase 1
한계, 네트워크 호출 없음 원칙 유지). 각 하위 명령은 타임아웃을 두어
StatusLine이 멈추지 않도록 한다 — 실패/타임아웃 시 해당 필드만
`None`으로 남기고 다른 필드는 계속 시도한다."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ai_workspace.observability.snapshot import GitRuntimeInfo

_TIMEOUT_SECONDS = 1.5


class GitRuntimeAnalyzer:
    def analyze(self, project_root: Path) -> GitRuntimeInfo:
        """
        입력: project_root(git 저장소로 간주할 경로)
        출력: `GitRuntimeInfo`
        예외: 없음
        보장: 쓰기 명령을 실행하지 않는다(`fetch` 포함). 명령이
              실패/타임아웃하면 해당 필드만 `None`.
        """
        if not _is_git_repo(project_root):
            return GitRuntimeInfo(
                current_branch=None,
                working_tree_dirty=None,
                ahead=None,
                behind=None,
                last_commit_summary=None,
            )

        ahead, behind = _read_ahead_behind(project_root)
        return GitRuntimeInfo(
            current_branch=_run(project_root, ["git", "rev-parse", "--abbrev-ref", "HEAD"]),
            working_tree_dirty=_read_dirty(project_root),
            ahead=ahead,
            behind=behind,
            last_commit_summary=_run(project_root, ["git", "log", "-1", "--format=%h %s"]),
        )


def _is_git_repo(project_root: Path) -> bool:
    return _run(project_root, ["git", "rev-parse", "--is-inside-work-tree"]) == "true"


def _read_dirty(project_root: Path) -> bool | None:
    output = _run(project_root, ["git", "status", "--porcelain"])
    if output is None:
        return None
    return len(output) > 0


def _read_ahead_behind(project_root: Path) -> tuple[int | None, int | None]:
    upstream = _run(
        project_root, ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]
    )
    if upstream is None:
        return None, None
    counts = _run(
        project_root, ["git", "rev-list", "--left-right", "--count", "@{u}...HEAD"]
    )
    if counts is None:
        return None, None
    parts = counts.split()
    if len(parts) != 2:
        return None, None
    behind, ahead = parts
    return int(ahead), int(behind)


def _run(project_root: Path, command: list[str]) -> str | None:
    try:
        result = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()
