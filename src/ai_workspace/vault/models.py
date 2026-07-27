"""ADR-0035(Vault Integration Layer)의 구조화 입력 스키마.

`vault/`는 Core Domain을 알지 못하므로, 이 모듈은 `domain/`의 어떤
타입도 참조하지 않는다 — kind/title/summary 등 독립된 값만 담는다."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class VaultDocumentKind(Enum):
    """Vault Directory Mapping의 kind. `AI_RULES`의 Tag Rule 11종 중
    자동 저장 대상과 1:1 대응한다(`system`은 수동 문서라 제외)."""

    ADR = "adr"
    DECISION = "decision"
    BACKEND = "backend"
    API = "api"
    DASHBOARD = "dashboard"
    AUTOMATION = "automation"
    PRODUCTION = "production"
    IOS = "ios"
    ANDROID = "android"
    MILESTONE = "milestone"
    DAILY = "daily"
    ARCHITECTURE = "architecture"


@dataclass(frozen=True)
class VaultDocumentRequest:
    """Markdown Generator/Vault Writer에 전달하는 구조화 입력. AI가 GitHub
    원문을 수정한 직후 이미 결정된 값을 채워 넘긴다(자연어 생성이 아니라
    고정 스키마 값 전달, ADR-0035 결정 3)."""

    kind: VaultDocumentKind
    title: str
    summary: str
    related_docs: tuple[str, ...] = ()
    source_paths: tuple[str, ...] = ()
    fields: dict[str, str] = field(default_factory=dict)
    date: str | None = None
