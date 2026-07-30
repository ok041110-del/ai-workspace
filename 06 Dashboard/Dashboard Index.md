---
tags: [dashboard]
---

# Dashboard Index

> Real-time Dashboard Platform(Milestone 20, ADR-0032). CQRS Read
> Model — Task를 실행하지 않고 조회만 한다.

## Health

`workspace_status`/`engine_statuses`(READY/RUNNING/AUTH_REQUIRED/
ERROR)/`recent_executions`(최근 100건)/`execution_stats`/
`reliability_stats` 5개 영역을 실시간으로 제공한다. `KNOWN_ENGINES`
목록으로 아직 실행되지 않은 Engine도 기본 상태(READY)로 채운다.
M22부터는 `production_status()`(HealthMonitor 위임)도 함께 제공한다
([[Production Index]] 참고).

## Automation(Reader → Reader)

`DashboardService`가 선택적으로 `automation_service`를 주입받아
`AutomationService.list_rules()`(읽기 전용)만 호출해
`AutomationStatus`(등록/활성 Rule 수, 마지막/다음 실행 시각)를
집계한다. Dashboard는 Automation을 제어하지 않는다 —
[[Architecture Overview]]의 CQRS 절 참고([[Automation Index]]).

## Execution

`ExecutionDispatcher`(§3.16, [[Backend Index]])가 발행하는
`ENGINE_EXECUTION_STARTED`/`ENGINE_EXECUTION_COMPLETED`/
`ENGINE_AUTHENTICATION_FAILED` 이벤트를 `InMemoryDashboardRepository`
가 스스로 구독해 기록한다. 통계는 조회 시점이 아니라 매 Event마다
미리 갱신한다("Dashboard는 통계를 계산하지 않는다").

## ViewModel

`web/dashboard_viewmodel.py`의 `DashboardViewModel`이 한국어 라벨
DTO를 만든다(Engine 이름만 예외로 영어 유지). `DashboardBroadcaster`
가 `/ws/dashboard` WebSocket으로 Event 발생 시 최신 스냅샷을
push한다(Polling 없음). 자세한 REST/WebSocket 목록은
[[API Catalog]] 참고.

## Project Intelligence(Milestone 29)

`DashboardRepository`(§Health/Execution)와는 별도로, Milestone
29(Project Intelligence)가 Vault Task 문서를 집계한 Snapshot/
Health/Risk/Recommendation 리포트를 [[Project Intelligence]]에
노출한다(ADR-0043) — `intelligence.report.ProjectIntelligenceService
.publish()`가 실행될 때마다 문서 전체를 덮어쓴다. 이 Dashboard
Read Model(Event 기반 실시간)과 달리 호출 시점에 Vault를 다시
읽어 계산하는 On-demand 리포트다.

## 관련 ADR

- [[ADR Index]] — ADR-0032(Real-time Dashboard Platform 도입)

## 관련 Architecture

- [[Architecture Overview]] §CQRS
- [[Backend Index]]

## 원문

- `docs/ARCHITECTURE.md` §3.18
- `src/ai_workspace/runtime/dashboard/`
- `src/ai_workspace/web/routes.py`
