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
import할 수 없다 — Analyzer의 순수성을 그대로 강제한다.

Milestone 41(Architecture Guardian, ADR-0056)부터 이 3개 규칙의
평가 로직은 `guardian/rules.py`의 `GUARDIAN_RULES` + `guardian/
checker.py`로 이전됐다 — 여기서는 그 결과를 `assert`만 한다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.guardian.checker import evaluate
from ai_workspace.guardian.rules import GUARDIAN_RULES

_SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "ai_workspace"

_INTELLIGENCE_RULE_NAMES = (
    "intelligence_does_not_import_forbidden_packages",
    "intelligence_only_depends_on_integration_adapters",
    "intelligence_memory_access_is_limited_to_service_role_modules",
)


def test_intelligence_does_not_import_forbidden_packages() -> None:
    rules = [
        rule
        for rule in GUARDIAN_RULES
        if rule.name == "intelligence_does_not_import_forbidden_packages"
    ]
    result = evaluate(rules, _SRC_ROOT).results[0]
    assert result.passed, f"intelligence/가 금지된 패키지를 직접 import합니다: {result.violations}"


def test_intelligence_only_depends_on_integration_adapters() -> None:
    rules = [
        rule
        for rule in GUARDIAN_RULES
        if rule.name == "intelligence_only_depends_on_integration_adapters"
    ]
    result = evaluate(rules, _SRC_ROOT).results[0]
    assert result.passed, (
        f"intelligence/가 Adapter가 아닌 integration 모듈을 참조합니다: {result.violations}"
    )


def test_intelligence_memory_access_is_limited_to_service_role_modules() -> None:
    """`memory/`를 import하는 모듈은 반드시 `*Service` 클래스를 정의해야
    한다(Role 기반 허용, M40/ADR-0055) — Analyzer/값 객체 모듈이
    `memory/`를 직접 참조하면 안 된다."""
    rules = [
        rule
        for rule in GUARDIAN_RULES
        if rule.name == "intelligence_memory_access_is_limited_to_service_role_modules"
    ]
    result = evaluate(rules, _SRC_ROOT).results[0]
    assert result.passed, (
        f"intelligence/에서 memory/를 참조하지만 *Service 클래스가 없는 모듈"
        f"(Analyzer 순수성 위반): {result.violations}"
    )


def test_all_intelligence_rules_are_registered_in_guardian() -> None:
    """이 파일이 검증하는 3개 규칙이 `GUARDIAN_RULES`에서 사라지지
    않았는지 확인한다 — Registry에서 실수로 규칙이 빠지면 이 파일의
    나머지 테스트가 조용히 빈 목록(`rules == []`)을 평가해 항상
    통과해버리는 것을 막는다."""
    registered = {rule.name for rule in GUARDIAN_RULES}
    missing = set(_INTELLIGENCE_RULE_NAMES) - registered
    assert missing == set(), f"GUARDIAN_RULES에서 누락된 규칙: {missing}"
