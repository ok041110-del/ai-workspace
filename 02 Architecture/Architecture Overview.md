---
tags: [architecture]
---

# Architecture Overview

## 요약

AI Workspace는 위(UI)에서 아래(구현 엔진)로만 의존하는 계층형
구조다. Agent 간 협업만 EventBus를 통한 수평 결합이고, 나머지는
전부 단방향 의존이다. Milestone 20부터는 Dashboard/Automation/
Production이라는 Infrastructure 계층이 추가됐지만, Core
Domain(`domain`/`interfaces`/`engines`)은 이 계층들의 존재를
전혀 모른다.

## Layer 구조

```
UI Surfaces (CLI, Web Dashboard)
  → Interaction Layer
  → Workspace Core (오케스트레이터)
  → Agent Runtime (Registry/Scheduler/Manager/EventBus)
  → Agents (Coordination/Planning/Coding/Review/Documentation …)
  → Core Engines / Context Manager+Memory Engine / Engine Runtime→Engine Adapter→구현 엔진
```

병렬로 존재하는 Infrastructure 계층(Core Domain과 독립):

```
ExecutionDispatcher → EventBus → Dashboard(Read Model)
                              ↘ Automation(Scheduler, EventBus 구독)
Production(Configuration/Lifecycle/Health) → web/(FastAPI, 유일하게 프레임워크를 아는 계층)
```

## 핵심 컴포넌트

| 컴포넌트 | 역할 | 관련 문서 |
|---|---|---|
| Workspace Core | 최상위 오케스트레이터, Task를 직접 실행하지 않고 Agent Runtime에 위임 | |
| Agent Runtime | Registry/Scheduler/Manager, Capability 기준으로 Agent 선택 | |
| EventBus | Agent/Engine/Workspace Core 사이 pub/sub. Event Store는 독립 구독자 | 아래 EventBus 절 |
| Engine Runtime → Engine Adapter | 구현 엔진(Claude Code/Codex/Gemini CLI) 호출 경로 | |
| ExecutionDispatcher | `EngineSelectionDecision` → 실제 실행. 유일한 실행 진입점(M18) | [[Automation Index]] |
| DashboardService | CQRS Read Model, Task를 실행하지 않고 조회만 | [[Dashboard Index]] |
| AutomationScheduler | 조건/일정에 따라 Task 자동 실행. Dashboard와 독립적인 Domain | [[Automation Index]] |
| LifecycleManager / HealthMonitor | Server Runtime의 생명주기/상태(비즈니스 로직 없음) | [[Production Index]] |

## CQRS

Dashboard/Automation Read 경로는 CQRS를 따른다 — 쓰기(Event 발행)
와 읽기(Service 조회)가 분리돼 있고, Writer(`ExecutionDispatcher`)
는 Reader(`DashboardRepository`)를 전혀 모른다. 단, **Reader가 다른
Reader를 참조하는 것은 CQRS 위반이 아니다** — `DashboardService`가
`AutomationService`/`HealthMonitor`를 선택적으로 참조하는 것이 그
예(M21/M22).

## EventBus

인메모리 pub/sub(`InMemoryEventBus`). `ExecutionDispatcher`가
`ENGINE_EXECUTION_STARTED`/`ENGINE_EXECUTION_COMPLETED`/
`ENGINE_AUTHENTICATION_FAILED`를 발행하고, `DashboardRepository`와
`AutomationScheduler`가 각자 독립적으로 구독한다. Event Store는
이 Bus의 **독립 구독자**일 뿐 특별한 전달 경로를 갖지 않는다.

## Repository 패턴

`ProjectRepository`/`AgentRepository`/`EventStore`/
`KnowledgeRepository`/`DashboardRepository`/`AutomationRepository`
등 — 전부 `load`/`get` + `save`(upsert) + `list_*`(방어적 복사)
스타일을 공유한다. 파일 기반 구현체(`storage/`)와 인메모리
구현체(`runtime/*/`)가 같은 Interface를 만족한다.

## Interface 개수

**총 27종**(2026-07-27 기준, ADR-0034 시점). Milestone 21에서
`AutomationRepository`가 27번째로 추가된 뒤 Milestone 22·23(T02)
모두 새 Interface를 추가하지 않았다. 전체 목록은 GitHub `docs/
ARCHITECTURE.md` §7 참고.

## Vault Integration Layer(Milestone 23, ADR-0035, 설계만)

Core Domain·`web/` 양쪽 모두 모르는 독립 계층 `vault/`가 GitHub
원문과 이 Vault 사이의 문서 동기화(Markdown 생성/저장)를
자동화한다. 아직 미구현이며, 설계 상세는
[[Vault Integration Architecture]] 참고.

## Obsidian Workspace Templates(Milestone 27, ADR-0038)

`vault/`에 `VaultDocumentKind.TASK`(개별 Task 문서, `14 Tasks/
{task_id}.md`)가 추가돼, Task 1건마다 Status/Priority/Milestone/
Owner/Checklist/Notes/Related Documents/Decision을 담은 문서를
Obsidian 안에서 직접 관리할 수 있다. [[Template - Task]] 참고.

## Workspace Adapter Layer(Milestone 28-T03, ADR-0039)

Core Domain과 `vault/`는 여전히 서로를 모른다(ADR-0035 유지) —
그 경계를 넘는 유일한 통로가 새 최상위 패키지 `integration/`이다.
"Adapter 3개"가 아니라, 외부 관심사마다 하나씩 늘어나는 확장
가능한 계층(Vault/Workflow/Agent, 향후 Runtime/Service/
Notification/Sync 등)으로 정의했다. 각 Adapter는 연결·변환·위임만
하고 비즈니스 로직을 갖지 않는다. `ast` 기반 테스트가 이 경계를
자동으로 강제한다.

## Adapter vs Connector(Milestone 28-T05, ADR-0040)

Integration Layer 안에서 두 종류를 구분한다: **Adapter**(외부
시스템 하나와의 연결만, `VaultAdapter`/`WorkflowAdapter`/
`AgentAdapter`)와 **Connector**(여러 Adapter를 조합해 유스케이스
하나를 오케스트레이션, `WorkflowTaskLink`/`WorkflowAgentLink`).
Connector도 자체 비즈니스 로직은 갖지 않고 항상 Adapter가 감싼
Core Domain Engine에 위임한다. Connector끼리도 서로 참조하지
않는다 — Agent 배정은 `WorkflowTaskLink`가 아니라 별도
`WorkflowAgentLink`가 담당한다.

## 관련 문서

- [[Overview]]
- [[ADR Index]]
- [[Backend Index]]
- [[Dashboard Index]]
- [[Automation Index]]
- [[Production Index]]
- [[Architecture Map]]
- [[Vault Integration Architecture]]

## 원문

- docs/ARCHITECTURE.md
