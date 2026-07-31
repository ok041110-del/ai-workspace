"""Architecture Guardian — 순수 평가기(ADR-0056, Milestone 41-T01).

`GUARDIAN_RULES`(`guardian/rules.py`)를 소스 트리(`src/ai_workspace`)
에 대해 평가해 `ArchitectureHealthReport`를 만든다. **`pytest`를
전혀 알지 못한다** — `import pytest`도 `assert`도 이 파일 어디에도
없다(사용자 조건). `pytest` 테스트는 이 모듈의 결과를 보고 자기
스스로 `assert`할 뿐, 평가 로직 자체는 여기 있다."""

from __future__ import annotations

import ast
from collections.abc import Sequence
from pathlib import Path

from ai_workspace.guardian.models import (
    ArchitectureCheckResult,
    ArchitectureHealthReport,
    ArchitectureViolation,
)
from ai_workspace.guardian.rules import (
    AllowedImportPrefixRule,
    ArchitectureRule,
    ForbiddenPackageImportRule,
    ServiceRoleGatedImportRule,
)


def evaluate(rules: Sequence[ArchitectureRule], src_root: Path) -> ArchitectureHealthReport:
    """
    입력: rules(평가할 `ArchitectureRule` 목록), src_root
          (`src/ai_workspace` 디렉터리)
    출력: 규칙별 `ArchitectureCheckResult`를 담은 `ArchitectureHealthReport`
    예외: 알 수 없는 Rule 타입이 섞여 있으면 `TypeError`
    보장: side-effect 없음(read-only) — 소스 트리를 읽기만 한다.
    """
    results = tuple(_evaluate_rule(rule, src_root) for rule in rules)
    return ArchitectureHealthReport(results=results)


def _evaluate_rule(rule: ArchitectureRule, src_root: Path) -> ArchitectureCheckResult:
    if isinstance(rule, ForbiddenPackageImportRule):
        return _evaluate_forbidden_package_import(rule, src_root)
    if isinstance(rule, AllowedImportPrefixRule):
        return _evaluate_allowed_import_prefix(rule, src_root)
    if isinstance(rule, ServiceRoleGatedImportRule):
        return _evaluate_service_role_gated_import(rule, src_root)
    raise TypeError(f"알 수 없는 ArchitectureRule 타입: {type(rule)!r}")  # pragma: no cover


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _defines_class_with_suffix(path: Path, suffix: str) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return any(
        isinstance(node, ast.ClassDef) and node.name.endswith(suffix) for node in ast.walk(tree)
    )


def _matches_any_package(module: str, packages: tuple[str, ...]) -> bool:
    return any(
        module == f"ai_workspace.{package}" or module.startswith(f"ai_workspace.{package}.")
        for package in packages
    )


def _evaluate_forbidden_package_import(
    rule: ForbiddenPackageImportRule, src_root: Path
) -> ArchitectureCheckResult:
    violations: list[ArchitectureViolation] = []
    for package in rule.source_packages:
        for path in (src_root / package).rglob("*.py"):
            for module in _imported_modules(path):
                if _matches_any_package(module, rule.forbidden_packages):
                    violations.append(
                        ArchitectureViolation(
                            file=str(path.relative_to(src_root)), detail=f"imports {module}"
                        )
                    )
    return ArchitectureCheckResult(
        rule_name=rule.name, passed=not violations, violations=tuple(violations)
    )


def _evaluate_allowed_import_prefix(
    rule: AllowedImportPrefixRule, src_root: Path
) -> ArchitectureCheckResult:
    violations: list[ArchitectureViolation] = []
    for package in rule.source_packages:
        for path in (src_root / package).rglob("*.py"):
            for module in _imported_modules(path):
                if module.startswith(f"{rule.restricted_package}.") and not module.startswith(
                    rule.allowed_prefixes
                ):
                    violations.append(
                        ArchitectureViolation(
                            file=str(path.relative_to(src_root)),
                            detail=f"imports disallowed {module}",
                        )
                    )
    return ArchitectureCheckResult(
        rule_name=rule.name, passed=not violations, violations=tuple(violations)
    )


def _evaluate_service_role_gated_import(
    rule: ServiceRoleGatedImportRule, src_root: Path
) -> ArchitectureCheckResult:
    violations: list[ArchitectureViolation] = []
    for package in rule.source_packages:
        for path in (src_root / package).rglob("*.py"):
            modules = _imported_modules(path)
            imports_gated = any(
                module == rule.gated_package or module.startswith(f"{rule.gated_package}.")
                for module in modules
            )
            if imports_gated and not _defines_class_with_suffix(path, rule.role_suffix):
                violations.append(
                    ArchitectureViolation(
                        file=str(path.relative_to(src_root)),
                        detail=(
                            f"imports {rule.gated_package} without defining a "
                            f"*{rule.role_suffix} class"
                        ),
                    )
                )
    return ArchitectureCheckResult(
        rule_name=rule.name, passed=not violations, violations=tuple(violations)
    )
