---
tags: [architecture, automation]
type: concept
---

# Automation (Concept)

> Evergreen Concept 문서(Milestone 47, [[Vault Information Architecture]]
> T02-6). 내용은 `docs/ARCHITECTURE.md` §13.3 정의를 그대로 요약
> 인용한다.

## 정의(§13.3, 보조 용어, ADR-0033)

조건/일정 Trigger로 Action을 자동 발동시키는 계층(`AutomationEngine`/
`AutomationScheduler`)에만 쓴다. Automation은 스스로 "무엇을 할지"
판단하지 않는다 — 그 판단은 Intelligence/Recommendation의 책임이다.

## 이 개념을 구현하는 Milestone

| Milestone | 책임 |
|---|---|
| M21 — Automation Scheduler | `AutomationRule`/`AutomationScheduler` 기본 계약 |
| M38 — AutomationScheduler 연결 | `RUN_RECOMMENDATION` Action으로 M35 추천을 자동 실행 |
| M43 — Recommendation Orchestration | `AutomationActionExecutor`가 Orchestration Service를 거치도록 배선 교체 |

## 관련 문서

- [[Automation Index]]
- [[Recommendation Hub]]
- [[Execution]]

## 원문

- `docs/ARCHITECTURE.md` §13.3(Automation 정의), §3.x(M21/M38/M43)
