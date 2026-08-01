---
tags: [architecture, recommendation]
type: concept
---

# Recommendation (Concept)

> Evergreen Concept 문서(Milestone 47, [[Vault Information Architecture]]
> T02-6) — Milestone과 무관하게 유지된다. 내용은 `docs/ARCHITECTURE.md`
> §13.3 정의를 그대로 요약 인용한다(새로 쓰지 않음).

## 정의(ADR-0060 확정)

> The domain concept responsible for determining the most
> appropriate Next Action from the current project state. It
> represents an actionable recommendation, not a mandatory
> decision.

Intelligence가 계산한 "다음에 무엇을 해야 하는가"라는 단일하고
근거(`reason`) 있는 판단(`NextAction`)이다. **비구속적**이다 —
실제 실행 여부는 별도의 `ExecutionGate`가 최종 결정한다
(§13.3, ADR-0049/ADR-0060).

## 이 개념을 구현하는 Milestone

| Milestone | 책임 |
|---|---|
| M35 — Recommendation Intelligence | 5단계 Priority Rule로 `NextAction` 결정 |
| M42 — Recommendation Adaptation | 과거 Experience로 사후 조정(Adjustment) |
| M43 — Recommendation Orchestration | Experience→Recommendation→Execution 흐름 제어 |
| M44 — Recommendation Explainability | 결정 근거를 구조적으로 재구성 |

## 관련 문서

- [[Recommendation Hub]]
- [[Architecture Overview]]
- [[Execution]]

Adaptation/Orchestration/Explainability는 별도 Concept 문서를 두지
않는다 — Recommendation 파이프라인의 단계일 뿐 독립된 Domain
Vocabulary가 아니므로([[Vault Information Architecture]] T02-6),
[[Recommendation Hub]]에서 흐름으로 확인한다.

## 원문

- `docs/ARCHITECTURE.md` §13.3(Recommendation 정의), §3.34~3.36(M42~M44)
