"""Architecture Guardian — 결과 모델(ADR-0056, Milestone 41-T01).

Guardian은 규칙을 정의하지 않는다(§8이 여전히 규칙의 소유자다) —
이미 선언된 규칙을 평가하고 그 결과를 공표할 뿐이다. 이 모듈은 그
"평가 결과"를 표현하는 순수 값 객체만 담는다. 메서드가 있는
`all_passed`는 판단이 아니라 이미 계산된 `passed` 값들의 단순
논리곱이다(새 판정 로직 아님).

`GUARDIAN_BLOCK_REASON_PREFIX`(M48, ADR-0065)는 Guardian 위반으로
Execution이 차단됐을 때 `ExecutionGate`(`runtime/execution/`)가
Vault Execution 리포트에 남기는 이유 문자열의 접두어다. Guardian이
이 문자열의 정본 소유자다 — `observability/guardian_runtime_
analyzer.py`가 같은 리포트를 읽어 Guardian 차단 여부를 구분할 때도
이 상수를 그대로 재사용한다(문자열 중복 정의 금지)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

GUARDIAN_BLOCK_REASON_PREFIX: Final[str] = "Architecture Guardian 위반으로 실행 차단"


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
