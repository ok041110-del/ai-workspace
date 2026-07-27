---
tags: [automation]
---

# Automation Index

> Automation Engine(Milestone 21, ADR-0033). 사용자의 명시적 요청
> 없이 조건/일정에 따라 Task를 자동 실행한다. Dashboard와 독립적인
> Domain.

> **이름 주의**: M4-T07의 `AutomationEngine`(Interface)과는 다른
> 개념이다 — `AutomationEngine`은 trigger_id↔Workflow 연결 관리만
> 하고, "언제 발동해야 하는가" 판단과 실제 실행은 이번 Milestone이
> 새로 구현한다. 두 개념 모두 그대로 유지된다. ([[ADR Index]]
> ADR-0033)

## Rule

`AutomationRule`은 `last_executed_at`/`next_execution_at`을 포함하는
가변 엔티티(`enable()`/`disable()`). `AutomationRepository`(신규
27번째 Interface)에 저장되고, `AutomationService`가 CRUD의 유일한
진입점이다(Action을 직접 실행하지 않음).

## Trigger

`TriggerKind`: TIME/INTERVAL/EVENT/STARTUP. `TriggerEvaluator` 계층이
"지금 발동해야 하는가"만 전담(Scheduler와 책임 분리) —
`TimeTriggerEvaluator`/`IntervalTriggerEvaluator`/
`StartupTriggerEvaluator`/`EventTriggerEvaluator`.

## Scheduler

`AutomationScheduler`(Infrastructure)는 Rule을 별도 보관하지 않고
매 `tick()`/`start()`/Event 수신마다 `AutomationRepository`를 다시
조회한다 — `AutomationService`의 CRUD가 자동 반영됨. Server Runtime이
`automation_tick_seconds`(기본 30초)마다 백그라운드로 `tick()`을
돈다([[Production Index]]).

## Execution Flow

```
AutomationRule → AutomationRepository → AutomationService(CRUD)
  → AutomationScheduler(Trigger 평가) → AutomationActionExecutor
  → ExecutionDispatcher(유일한 실행 진입점) → EventBus → Dashboard
```

`AutomationActionExecutor`는 RUN_TASK를 기존 M17/M18 파이프라인
(`EngineSelectionPolicy.select()` → `ExecutionDispatcher.dispatch()`)
에 그대로 실어 실행한다 — 새 실행 경로를 만들지 않는다. RUN_WORKFLOW는
아직 미지원(`AutomationActionNotSupportedError`).

## 관련 GitHub 문서

- `docs/ARCHITECTURE.md` §3.19
- `src/ai_workspace/runtime/automation/`
- `src/ai_workspace/web/automation_routes.py`

## 관련 문서

- [[ADR Index]] — ADR-0033
- [[Dashboard Index]]
- [[API Catalog]]

## 원문

- `docs/ARCHITECTURE.md` §3.19
