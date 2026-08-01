---
tags: [automation]
type: automation
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

> **Platform 계층(2026-07-30, 사용자 확정)**: M21(이 Milestone)은
> M36~M38과 함께 **Execution Platform**(실행·상태 전이·스케줄링)에
> 속한다 — M29~M35 **Intelligence Platform**(관찰·분석·추천,
> Read Only)과 책임이 다르다. "Automation Core"라는 이름은 Memory
> Engine/Architecture Guardian/Learning Engine이 갖춰진 뒤로
> 보류됐다. 상세는 `docs/ARCHITECTURE.md` §2.1 참고.

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

**RUN_RECOMMENDATION(Milestone 38, ADR-0052)**: `RecommendationExecutionService`
(M36/M37)를 `manual_trigger=True`로 호출해 M35 `source=next_task`
추천을 그대로 실행한다 — `ExecutionGate`는 손대지 않는다(여전히
`source=next_task`만 승인). `web/server.py`의 `build_app()`이
`VaultAdapter`/`AgentAdapter`/Recommendation 파이프라인 전체를
최초로 실배선해, `AutomationScheduler`의 TIME/INTERVAL Trigger로
실제 자동 실행이 가능해졌다.

**Architecture Guardian Gate(Milestone 48, ADR-0065)**:
`RecommendationOrchestrationService`가 `execution_service.execute()`
를 호출하기 직전에(주입된 경우) `ArchitectureGuardianService.
generate()`(M41, Read Only)를 호출한다 — Guardian 위반이 있으면
Recommendation/Adaptation/Explainability는 그대로 생성하되 Execution
만 차단한다(Override 없음). M45 StatusLine에 `AutomationGateStatus`
(PASS/BLOCKED/UNKNOWN)로 최근 1건의 결과가 노출된다.

**Adaptation 규칙 정교화(Milestone 49, ADR-0066)**:
`RecommendationAdjustmentAnalyzer`(M42)의 추천 보류 조건이 "성공
0건 + 실패 1건 이상"에서 "실패율 100% + 표본 3건 이상"으로
정교화됐다 — 표본이 부족한 상태(실패 1~2건)에서 성급하게 보류하지
않도록 최소 표본 조건을 추가했다. Guardian 다건 이력 축적·영속
저장소 도입은 이번 Milestone Scope에서 명시적으로 배제됐다(향후
별도 Milestone 대상).

**Learning Persistence(Milestone 50, ADR-0067)**: `ExecutionMemory
Store`(M39)가 쓰는 `MemoryEngine` 구현체가 `InMemoryMemoryEngine`
에서 `FileMemoryEngine`(신규, `storage/`)으로 교체됐다 —
`<vault_root>/.ai-workspace-data/`에 단일 JSON 파일로 key-value를
영속화해, 서버 재시작 후에도 학습 이력이 유지된다. 새 Interface/
Service 없이 기존 `MemoryEngine` 계약을 구현만 했고, `web/server.py`
Composition Root 1곳만 교체됐다. StatusLine이 이 파일을 읽는
Observability 배선은 이번 Scope 밖(향후 별도 Milestone 대상).

**Learning Evolution(Milestone 51, ADR-0068)**: M49/M50 규칙(실패율
100% + 표본 3건 이상, 전체 이력 기반)에 최근 추세 기반 규칙이
보완으로 추가됐다 — `ExperienceStat.recent_failure_streak`(가장
최근 기록부터 거슬러 올라간 연속 실패 횟수)가 5 이상이면, 전체
이력에 성공이 섞여 있어도 추천을 보류한다(기존 규칙 무변경, OR
병존). 어느 규칙이 발동했는지는 `reason` 텍스트에 "(M49 규칙)"/
"(M51 규칙)"/"(M49+M51 규칙)"로 태깅돼 Explainability(M44)가 그대로
노출한다.

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
