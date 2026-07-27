from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

WORKSPACE_VERSION = "1.0.0"
"""제품 릴리스 버전(M22-T04). `pyproject.toml`의 `version`(ADR-0024가
관리하는 아키텍처 기준선 버전)과는 다른 개념이다 — 이 값이 Production
Version API가 실제로 노출하는 값이다(2026-07-27 사용자 승인, M22
kickoff 논의)."""


@dataclass(frozen=True)
class VersionInfo:
    version: str
    commit_hash: str | None


def get_git_commit_hash(*, cwd: str | Path | None = None) -> str | None:
    """현재 HEAD의 Git Commit Hash를 조회한다(사용자 DoD — "Git Commit
    Hash를 함께 제공할 수 있다", 선택 항목). git 저장소가 아니거나
    `git` 실행 파일이 없거나 실패하면 `None`을 반환한다 — Version
    API가 이 값 없이도 항상 동작해야 한다."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    commit_hash = result.stdout.strip()
    return commit_hash or None


def get_version_info(*, repo_path: str | Path | None = None) -> VersionInfo:
    return VersionInfo(version=WORKSPACE_VERSION, commit_hash=get_git_commit_hash(cwd=repo_path))
