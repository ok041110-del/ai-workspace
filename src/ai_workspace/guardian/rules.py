"""Architecture Guardian — 실행 가능한 규칙 명세(ADR-0056, Milestone
41-T01). "Guardian owns the executable representation of
architectural rules. Architecture documentation defines the rules;
Guardian encodes them, evaluates conformance, and publishes
architectural health." — `docs/ARCHITECTURE.md` §8이 규칙을 정의하고,
이 모듈은 그중 이미 `tests/`에 개별 구현돼 있던 것들을 데이터로
인코딩할 뿐이다(새 규칙 발명 없음).

**메서드 없는 순수 값 객체(사용자 조건)**: 아래 3개 Rule 타입은 전부
필드만 있는 `frozen` dataclass다 — 평가 로직(`evaluate()`)을 갖지
않는다. 평가는 `guardian/checker.py`가 타입별로 분기해서 한다(Rule을
다형적 客体가 아니라 순수 데이터로 유지하기 위함).

**의도적으로 제외한 것**: `test_connector_layering.py`(Adapter/Peer
Connector/Orchestrating Connector 그룹 화이트리스트)와 `test_
conversation_connector_boundary.py`(파일 단위 규칙)는 아래 3개
Rule 형태로 자연스럽게 표현되지 않는다 — 억지로 일반화하면 Rule
타입 자체가 특수 사례에 맞춰 뒤틀린다(사용자 조건: 무리한 일반화
금지). 두 파일은 이번 범위에서 제외하고 각자의 기존 `ast` 검사를
그대로 유지한다 — 후속 Milestone에서 그룹 기반 Rule 형태가 필요해
지면 그때 새 Rule 타입을 추가한다."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class ForbiddenPackageImportRule:
    """`source_packages`(각각 `src/ai_workspace/` 아래 top-level
    패키지) 안의 어떤 파일도 `forbidden_packages`를 import하면 안
    된다(양방향 개별 선언 — A가 B를 금지한다고 B도 A를 금지하는 건
    아니다, 명시적으로 둘 다 선언)."""

    name: str
    source_packages: tuple[str, ...]
    forbidden_packages: tuple[str, ...]


@dataclass(frozen=True)
class AllowedImportPrefixRule:
    """`source_packages` 안의 파일이 `restricted_package`(예:
    `ai_workspace.integration`) 아래 무언가를 import한다면, 반드시
    `allowed_prefixes` 중 하나로 시작해야 한다(화이트리스트)."""

    name: str
    source_packages: tuple[str, ...]
    restricted_package: str
    allowed_prefixes: tuple[str, ...]


@dataclass(frozen=True)
class ServiceRoleGatedImportRule:
    """`source_packages` 안의 파일이 `gated_package`(예:
    `ai_workspace.memory`)를 import한다면, 그 파일은 반드시
    `role_suffix`(기본 `"Service"`)로 끝나는 클래스를 정의해야
    한다 — Analyzer/값 객체 모듈은 여전히 접근 금지(Role 기반,
    Milestone 40/ADR-0055)."""

    name: str
    source_packages: tuple[str, ...]
    gated_package: str
    role_suffix: str = "Service"


ArchitectureRule = ForbiddenPackageImportRule | AllowedImportPrefixRule | ServiceRoleGatedImportRule

#: Guardian의 정본 규칙 목록(Registry). 실행 중 변경되지 않는다
#: (사용자 조건 — `Final` + `tuple`). 새 규칙은 이 목록에 항목을
#: 추가하는 것만으로 등록된다 — Guardian 평가 로직은 손대지 않는다.
GUARDIAN_RULES: Final[tuple[ArchitectureRule, ...]] = (
    ForbiddenPackageImportRule(
        name="core_domain_does_not_import_vault",
        source_packages=("domain", "interfaces", "engines"),
        forbidden_packages=("vault",),
    ),
    ForbiddenPackageImportRule(
        name="vault_does_not_import_core_domain",
        source_packages=("vault",),
        forbidden_packages=("domain", "interfaces", "engines"),
    ),
    ForbiddenPackageImportRule(
        name="intelligence_does_not_import_forbidden_packages",
        source_packages=("intelligence",),
        forbidden_packages=("domain", "interfaces", "engines", "vault"),
    ),
    AllowedImportPrefixRule(
        name="intelligence_only_depends_on_integration_adapters",
        source_packages=("intelligence",),
        restricted_package="ai_workspace.integration",
        allowed_prefixes=(
            "ai_workspace.integration.vault_adapter",
            "ai_workspace.integration.agent_adapter",
            "ai_workspace.integration.knowledge_adapter",
        ),
    ),
    ServiceRoleGatedImportRule(
        name="intelligence_memory_access_is_limited_to_service_role_modules",
        source_packages=("intelligence",),
        gated_package="ai_workspace.memory",
        role_suffix="Service",
    ),
)
