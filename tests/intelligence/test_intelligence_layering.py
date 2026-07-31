"""M29-T02: Intelligence Layer 경계 검증(docs/ARCHITECTURE.md §8 규칙 21,
ADR-0043, M40에서 Role 기반으로 재정의 — ADR-0055). `intelligence/`의
어떤 모듈도 `domain`/`interfaces`/`engines`/`vault`를 직접 import하지
않는다. Read-Only 데이터 제공자 접근은 역할(Role)로 나뉜다 —
`integration/`의 Adapter(`VaultAdapter`/`AgentAdapter`/
`KnowledgeAdapter`)는 패키지 전체에 계속 허용되고(M29부터의 기존
관례, 이번에 넓히지 않음), `memory/`(Memory Domain — §13.2, 저장/
검색만 하고 판단하지 않는 컴포넌트)는 **`*Service`로 끝나는 클래스를
정의하는 모듈(오케스트레이션 역할)에만** 새로 허용한다(M40) — 특정
클래스 이름을 규칙에 나열하지 않고 "Service 역할인가"로 판단한다.
`*Service` 클래스가 없는 모듈(Analyzer/값 객체)은 여전히 `memory/`를
import할 수 없다 — Analyzer의 순수성을 그대로 강제한다."""

from __future__ import annotations

import ast
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "ai_workspace"
_INTELLIGENCE_DIR = _SRC_ROOT / "intelligence"
_FORBIDDEN_PACKAGES = ("domain", "interfaces", "engines", "vault")


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _defines_service_class(path: Path) -> bool:
    """모듈이 이름이 `Service`로 끝나는 클래스를 정의하는지 — 이
    저장소의 기존 관례(`ProjectIntelligenceService`/
    `RecommendationIntelligenceService` 등, 예외 없음)를 그대로
    Role 판정 기준으로 쓴다."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return any(
        isinstance(node, ast.ClassDef) and node.name.endswith("Service")
        for node in ast.walk(tree)
    )


def test_intelligence_does_not_import_forbidden_packages() -> None:
    offenders: list[str] = []
    for path in _INTELLIGENCE_DIR.rglob("*.py"):
        modules = _imported_modules(path)
        for module in modules:
            if any(
                module == f"ai_workspace.{package}" or module.startswith(f"ai_workspace.{package}.")
                for package in _FORBIDDEN_PACKAGES
            ):
                offenders.append(f"{path.relative_to(_SRC_ROOT)} -> {module}")
    assert offenders == [], f"intelligence/가 금지된 패키지를 직접 import합니다: {offenders}"


def test_intelligence_only_depends_on_integration_adapters() -> None:
    allowed_prefixes = (
        "ai_workspace.integration.vault_adapter",
        "ai_workspace.integration.agent_adapter",
        "ai_workspace.integration.knowledge_adapter",
    )
    offenders: list[str] = []
    for path in _INTELLIGENCE_DIR.rglob("*.py"):
        modules = _imported_modules(path)
        for module in modules:
            if module.startswith("ai_workspace.integration.") and not module.startswith(
                allowed_prefixes
            ):
                offenders.append(f"{path.relative_to(_SRC_ROOT)} -> {module}")
    assert offenders == [], (
        f"intelligence/가 Adapter가 아닌 integration 모듈을 참조합니다: {offenders}"
    )


def test_intelligence_memory_access_is_limited_to_service_role_modules() -> None:
    """`memory/`를 import하는 모듈은 반드시 `*Service` 클래스를 정의해야
    한다(Role 기반 허용, M40/ADR-0055) — Analyzer/값 객체 모듈이
    `memory/`를 직접 참조하면 안 된다."""
    offenders: list[str] = []
    for path in _INTELLIGENCE_DIR.rglob("*.py"):
        modules = _imported_modules(path)
        imports_memory = any(
            module == "ai_workspace.memory" or module.startswith("ai_workspace.memory.")
            for module in modules
        )
        if imports_memory and not _defines_service_class(path):
            offenders.append(str(path.relative_to(_SRC_ROOT)))
    assert offenders == [], (
        f"intelligence/에서 memory/를 참조하지만 *Service 클래스가 없는 모듈"
        f"(Analyzer 순수성 위반): {offenders}"
    )
