"""Architecture Guardian — 결과 모델(ADR-0056, Milestone 41-T01).

Guardian은 규칙을 정의하지 않는다(§8이 여전히 규칙의 소유자다) —
이미 선언된 규칙을 평가하고 그 결과를 공표할 뿐이다. 이 모듈은 그
"평가 결과"를 표현하는 순수 값 객체만 담는다. 메서드가 있는
`all_passed`는 판단이 아니라 이미 계산된 `passed` 값들의 단순
논리곱이다(새 판정 로직 아님)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitectureViolation:
    """규칙 하나를 어긴 구체적인 사례 1건."""

    file: str
    detail: str


@dataclass(frozen=True)
class ArchitectureCheckResult:
    """규칙 하나에 대한 평가 결과."""

    rule_name: str
    passed: bool
    violations: tuple[ArchitectureViolation, ...]


@dataclass(frozen=True)
class ArchitectureHealthReport:
    """전체 규칙에 대한 평가 결과 모음 — Guardian의 핵심 Output."""

    results: tuple[ArchitectureCheckResult, ...]

    @property
    def all_passed(self) -> bool:
        return all(result.passed for result in self.results)
