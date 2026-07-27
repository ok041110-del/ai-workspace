---
tags: [production]
---

# Production Index

> Production Platform(Milestone 22, ADR-0034). Server Runtime의
> 생명주기/설정/상태/Logging을 담당한다. 새 최상위 Interface는
> 추가하지 않는다 — 전부 구체 클래스/dataclass.

## Configuration

`ProductionConfig`(Immutable, frozen dataclass): `host`/`port`/
`log_level`/`dashboard_enabled`/`automation_enabled`/
`automation_tick_seconds`/`engine_settings`. `load_production_config()`
가 기본값→YAML 설정 파일→Environment Variable(`AI_WORKSPACE_` 접두사)
순으로 겹쳐 쓴다.

## Lifecycle

`LifecycleManager`는 `STARTUP`/`RUNNING`/`SHUTDOWN` 상태만 관리하고
컴포넌트를 생성하지 않는다(조립은 `web/server.py`의 `build_app()`
책임). `startup()`이 `started_at`을 기록하고 Automation Startup
Trigger를 발동시킨다. `shutdown()`은 `DashboardService.
workspace_status()`를 폴링해 실행 중 Task 완료를 기다리되, 타임아웃을
넘겨도 강제 종료하지 않는다(Graceful Shutdown).

## Logging

`ProductionConfig.log_level`로 표준 `logging.Logger`(`ai_workspace`)
를 설정(Console 항상, File 선택). `domain`/`interfaces`/`engines`는
이 모듈을 모른다 — Logging은 Domain에 침투하지 않는다.

## Health

`HealthMonitor`는 조회 전용(Read Model) — Server/Dashboard/
Automation/EventBus/Engine 5개 컴포넌트를 "연결돼 있는가"로 판정해
가장 나쁜 상태로 `health_status`(HEALTHY/DEGRADED/UNHEALTHY)를
집계한다. `ProductionStatus`가 `health_status`/`version`/
`started_at`/`uptime_seconds` 4개 표준 필드를 담아 M23이 그대로
재사용한다.

`HealthMonitor`/`LifecycleManager`는 `TYPE_CHECKING` 가드로
`DashboardService`를 타입 힌트로만 참조해 순환 import를 피하고,
`DashboardService.attach_health_monitor()`로 조립 순서 문제를
해결한다(실제 순환 의존은 아님).

## Version

`WORKSPACE_VERSION`(`version.py`)은 제품 릴리스 버전 —
`pyproject.toml`의 `version`(ADR-0024 아키텍처 기준선)과 별개 개념.
`get_git_commit_hash()`는 실패해도 `None`을 반환해 Version API가
항상 동작한다.

## 배포 계획

아직 별도 배포 파이프라인 문서는 없다(CLI `start` 서브커맨드로
`uvicorn.run()` 직접 기동). M23 Mobile Experience가 이 Production
API(`uptime`/`started_at`/`version`/`health_status`)를 그대로
소비할 예정이다.

## 관련 GitHub 문서

- `docs/ARCHITECTURE.md` §3.20
- `src/ai_workspace/runtime/production/`
- `src/ai_workspace/web/production_routes.py`

## 관련 문서

- [[ADR Index]] — ADR-0034
- [[Dashboard Index]]
- [[Automation Index]]
- [[API Catalog]]

## 원문

- `docs/ARCHITECTURE.md` §3.20
