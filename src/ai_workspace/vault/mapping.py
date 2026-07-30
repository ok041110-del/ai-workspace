"""ADR-0035 결정 2: Vault Directory Mapping — kind → 대상 Vault 파일."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.vault.models import VaultDocumentKind

#: Vault 실제 콘텐츠가 있는 최상위 디렉터리 16종(Milestone 26,
#: Obsidian Vault Root Refactoring 이후 vault_root == 저장소 root이므로
#: `src/`/`tests/`/`docs/`/`.claude/`/`.agents/` 등 Vault가 아닌 나머지
#: 저장소 콘텐츠와 스캔 범위를 분리하는 데 쓰인다). `14 Tasks`는
#: Milestone 27(Obsidian Workspace Templates)에서 추가됨.
VAULT_CONTENT_DIRECTORIES: tuple[str, ...] = (
    "00 System",
    "01 Overview",
    "02 Architecture",
    "03 ADR",
    "04 Backend",
    "05 API",
    "06 Dashboard",
    "07 Automation",
    "08 Production",
    "09 iOS",
    "10 Android",
    "11 Milestones",
    "12 Decisions",
    "13 Daily",
    "14 Tasks",
    "15 Project Intelligence",
    "99 Templates",
)


@dataclass(frozen=True)
class VaultMappingEntry:
    relative_path: str
    mode: str  # "append" | "create"


VAULT_DIRECTORY_MAP: dict[VaultDocumentKind, VaultMappingEntry] = {
    VaultDocumentKind.ADR: VaultMappingEntry("03 ADR/ADR Index.md", "append"),
    VaultDocumentKind.DECISION: VaultMappingEntry("12 Decisions/Decisions Index.md", "append"),
    VaultDocumentKind.BACKEND: VaultMappingEntry("04 Backend/Backend Index.md", "append"),
    VaultDocumentKind.API: VaultMappingEntry("05 API/API Catalog.md", "append"),
    VaultDocumentKind.DASHBOARD: VaultMappingEntry("06 Dashboard/Dashboard Index.md", "append"),
    VaultDocumentKind.AUTOMATION: VaultMappingEntry("07 Automation/Automation Index.md", "append"),
    VaultDocumentKind.PRODUCTION: VaultMappingEntry("08 Production/Production Index.md", "append"),
    VaultDocumentKind.IOS: VaultMappingEntry("09 iOS/iOS Design.md", "append"),
    VaultDocumentKind.ANDROID: VaultMappingEntry("10 Android/Android Placeholder.md", "append"),
    VaultDocumentKind.MILESTONE: VaultMappingEntry("11 Milestones/Milestones Index.md", "append"),
    VaultDocumentKind.DAILY: VaultMappingEntry("13 Daily/{date}.md", "create"),
    VaultDocumentKind.ARCHITECTURE: VaultMappingEntry(
        "02 Architecture/Architecture Overview.md", "append"
    ),
    VaultDocumentKind.TASK: VaultMappingEntry("14 Tasks/{task_id}.md", "create"),
}
