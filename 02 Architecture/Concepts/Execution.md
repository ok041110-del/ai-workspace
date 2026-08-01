---
tags: [architecture, execution]
type: concept
---

# Execution (Concept)

> Evergreen Concept 문서(Milestone 47, [[Vault Information Architecture]]
> T02-6). 내용은 `docs/ARCHITECTURE.md` §13.2 정의를 그대로 요약
> 인용한다.

## 정의(§13.2, 핵심 4개 용어 중 하나)

실제 부작용(Task 실행, 상태 변경)을 일으키는 계층. 이 저장소에서
"생각(Intelligence)"과 "행동(Execution)"을 가르는 경계선이다.
`EngineAdapter`를 통한 실제 실행, Task 상태 전이를 담당하며, 유일한
실행 진입점은 `ExecutionDispatcher`(M18)다.

- **범위(Scope)**: `runtime/execution/`, `runtime/automation/`
- **대표 산출물**: `EngineExecutionResult`, Task 상태 전이, Vault
  실행 리포트([[Recommendation Execution]])
- **대표 소비자**: 사람(Vault 열람), Memory(M39, 실행 결과를
  `ExecutionMemory`로 기록)

## 이 개념을 구현하는 Milestone

| Milestone | 책임 |
|---|---|
| M36 — Execution | `NextAction`을 `ExecutionGate`/`ActionBuilder`로 변환해 실행 |
| M37 — Task Lifecycle | 실행 결과를 Task 상태 전이 기계에 연결 |
| M43 — Recommendation Orchestration | Recommendation 의존성을 제거해 순수 실행 계층으로 정제 |

## 관련 문서

- [[Recommendation Hub]]
- [[Architecture Overview]]
- [[Recommendation]]
- [[Memory]]

## 원문

- `docs/ARCHITECTURE.md` §13.2(Execution 정의), §3.x(M36/M37/M43)
