---
tags: [backend]
---

# Backend Index

> [[Architecture Overview]]를 먼저 읽는다. 이 문서는 Backend
> 구현(디렉터리/Interface 구성)만 별도로 정리한 진입점이다.

## 구성

| 영역 | 디렉터리 | 설명 |
|---|---|---|
| Domain | `src/ai_workspace/domain/` | Task/Workflow/Agent 등 순수 도메인 모델 |
| Interfaces | `src/ai_workspace/interfaces/` | 27종 추상 계약(구현에 의존하지 않음) |
| Core Engines | `src/ai_workspace/engines/` | LLMPolicyEngine/BudgetPolicyEngine/AutomationEngine 등 |
| Agent Runtime | `src/ai_workspace/runtime/agent/` | Registry/Scheduler/Manager/EventBus |
| Engine Runtime | `src/ai_workspace/runtime/engine/` | EngineRuntime → EngineAdapter 호출 경로 |
| Execution Layer | `src/ai_workspace/runtime/execution/` | ExecutionDispatcher, AuthenticationManager(M18) |
| Reliability | `src/ai_workspace/runtime/reliability/` | RetryPolicy/RetryExecutor(M19) |
| Dashboard | `src/ai_workspace/runtime/dashboard/` | DashboardService/DashboardRepository(M20) |
| Automation | `src/ai_workspace/runtime/automation/` | AutomationScheduler/AutomationRepository(M21) |
| Production | `src/ai_workspace/runtime/production/` | Configuration/Lifecycle/Health/Logging/Version(M22) |
| Storage | `src/ai_workspace/storage/` | 파일 기반 Repository 구현체 |
| Web | `src/ai_workspace/web/` | FastAPI 앱, 유일하게 프레임워크를 아는 계층 |
| CLI | `src/ai_workspace/cli/` | 커맨드라인 진입점 |

## Interface 목록(27종, ADR-0034 기준)

전체 표는 GitHub `docs/ARCHITECTURE.md` §7 참고. 최근 3개
Milestone에서 도입된 것만 요약:

| Interface | 도입 Milestone | 관련 ADR |
|---|---|---|
| `DashboardRepository` | M20 | ADR-0032 |
| `AutomationRepository` | M21 | ADR-0033 |
| (M22는 새 Interface 없음 — `ProductionConfig` 등은 Interface가 아닌 값 객체/서비스) | M22 | ADR-0034 |

## Core Engines vs Runtime 구분

- **Core Engines**(`engines/`): Core Domain 내부에서 순수 정책/판단
  로직을 담당(LLMPolicyEngine, BudgetPolicyEngine, EngineSelectionPolicy 등).
- **Runtime**(`runtime/*/`): 실제 실행/조립/생명주기를 담당하는
  Infrastructure에 가까운 계층. `dashboard`/`automation`/`production`은
  Core Domain을 모르는 상태로 EventBus만 구독한다([[Architecture
  Overview]]의 CQRS 절 참고).

## 관련 문서

- [[Architecture Overview]]
- [[API Catalog]]
- [[Dashboard Index]]
- [[Automation Index]]
- [[Production Index]]

## 원문

- `docs/ARCHITECTURE.md` §3, §7, §9
