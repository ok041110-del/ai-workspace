"""M24-T01: Real Vault Connection.

M23까지 `vault_root`는 항상 호출자가 넘겨주는 `Path`였다(단위 테스트의
`tmp_path`, 통합 테스트가 직접 계산한 실제 경로). 이 모듈은 "실제
Obsidian Vault"를 안정적으로 찾고, 연결 가능 여부(존재/디렉터리 여부/
쓰기 권한)를 검증하는 표준 진입점을 제공한다.

Milestone 26(Obsidian Vault Root Refactoring)부터 **Vault Root == 이
Git 저장소의 Root**다(Git Vault Sync/Obsidian Mobile·macOS가 요구하는
"Vault == Repository Root" 조건). 그래서 별도 하위 경로를 찾는 대신,
Vault Root에만 존재하는 표식 파일(`00 System/PROJECT_INDEX.md`)이 있는
첫 조상 디렉터리를 Vault Root로 판단한다."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

_VAULT_ROOT_MARKER = Path("00 System") / "PROJECT_INDEX.md"


class VaultConnectionError(RuntimeError):
    """Vault 연결에 실패했을 때(찾지 못함/디렉터리 아님/쓰기 권한 없음)
    발생한다."""


@dataclass(frozen=True)
class VaultConnection:
    root: Path


def resolve_default_vault_root(start: Path | None = None) -> Path:
    """`start`(기본값: 현재 작업 디렉터리)에서 상위로 올라가며
    `00 System/PROJECT_INDEX.md`(Vault Root 표식)가 실제로 존재하는
    첫 조상 경로를 찾는다. 이 저장소의 루트 위치를 가정하지 않는다."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / _VAULT_ROOT_MARKER).is_file():
            return candidate
    raise VaultConnectionError(
        f"'{current}'의 상위 경로 어디에서도 "
        f"'{_VAULT_ROOT_MARKER}'를 찾지 못했습니다."
    )


def connect(root: Path | None = None) -> VaultConnection:
    """`root`(생략 시 `resolve_default_vault_root()`)가 실제로 존재하는
    디렉터리이고 쓰기 가능한지 검증한 뒤 `VaultConnection`을 돌려준다.
    실패하면 `VaultConnectionError`를 낸다(Permission Validation +
    존재 여부 확인 + 연결 실패 예외 처리)."""
    resolved = (root if root is not None else resolve_default_vault_root()).resolve()

    if not resolved.exists():
        raise VaultConnectionError(f"Vault 경로가 존재하지 않습니다: {resolved}")
    if not resolved.is_dir():
        raise VaultConnectionError(f"Vault 경로가 디렉터리가 아닙니다: {resolved}")
    if not os.access(resolved, os.W_OK):
        raise VaultConnectionError(f"Vault 경로에 쓰기 권한이 없습니다: {resolved}")

    return VaultConnection(root=resolved)
