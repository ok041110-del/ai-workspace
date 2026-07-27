from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Budget:
    """M15-T01: Workspace 차원의 Token/Cost 상한을 표현하는 순수 domain
    객체. 어떤 Provider(Claude/GPT/Gemini)에도 속하지 않는다 — Budget은
    실행 정책이지 특정 엔진의 속성이 아니다. 둘 다 선택적이며, 지정된
    항목만 검사 대상이 된다(둘 다 None이면 사실상 무제한).

    Task 단위로 개별 확인만 한다 — 여러 Task에 걸친 누적 소비량 추적은
    이번 범위 밖이다(YAGNI, M15 Non-goal)."""

    max_tokens: int | None = None
    max_cost_usd: float | None = None


@dataclass(frozen=True)
class BudgetDecision:
    """`BudgetPolicyEngine.check()`의 결과. `allowed=False`일 때만
    `reason`이 사람이 읽을 수 있는 근거를 담는다."""

    allowed: bool
    reason: str | None = None
