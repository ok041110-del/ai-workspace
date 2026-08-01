---
tags: [api]
type: documentation
---

# API Catalog

> [[Backend Index]]의 하위 문서. REST/WebSocket 엔드포인트 목록만
> 정리한다. 요청/응답 스키마 전문은 원문(FastAPI 라우터 코드) 참고.

## Dashboard API (`web/routes.py`, prefix `/api`)

| Method | Path | 설명 |
|---|---|---|
| GET | `/api/dashboard` | 전체 DashboardViewModel 조회 |
| GET | `/api/summary` | 요약 상태 |
| GET | `/api/history` | Execution 이력 목록 |
| GET | `/api/engines` | Engine 상태 목록 |

## Automation API (`web/automation_routes.py`, prefix `/api/automation`)

| Method | Path | 설명 |
|---|---|---|
| GET | `/api/automation` | AutomationRule 목록 |
| GET | `/api/automation/{rule_id}` | 단일 Rule 조회 |
| POST | `/api/automation` | Rule 생성(201) |
| PUT | `/api/automation/{rule_id}` | Rule 수정 |
| DELETE | `/api/automation/{rule_id}` | Rule 삭제(204) |
| POST | `/api/automation/{rule_id}/enable` | Rule 활성화 |
| POST | `/api/automation/{rule_id}/disable` | Rule 비활성화 |
| POST | `/api/automation/{rule_id}/run` | Rule 즉시 실행(202) |

## Production API (`web/production_routes.py`, prefix `/api`)

| Method | Path | 설명 |
|---|---|---|
| GET | `/api/health` | ProductionStatus(컴포넌트별 Health 포함 전체 조회) |
| GET | `/api/config` | ProductionConfig 요약 |
| GET | `/api/version` | VersionInfo(버전/Git commit hash) |
| GET | `/api/status` | 경량 4필드 요약(health_status/version/started_at/uptime_seconds) |

## WebSocket

| Path | 설명 |
|---|---|
| `/ws/dashboard` | Dashboard 관련 Event 발생 시 연결된 클라이언트 전체에 최신 스냅샷 push(Polling 없음). `DashboardBroadcaster`가 처리 |

## 설계 원칙

- `/api/health`(전체 컴포넌트 breakdown)와 `/api/status`(경량 요약)는
  의도적으로 분리돼 있다 — Mobile Client(M23)는 주로 `/api/status`를
  가볍게 폴링하고, 운영 대시보드는 `/api/health`로 상세를 본다.
- 모든 API는 DashboardService/AutomationService/HealthMonitor 등
  **조회 전용(Read Model)**에서만 응답을 만든다 — API 계층에서 직접
  Task를 실행하지 않는다([[Architecture Overview]]의 CQRS 절 참고).

## 관련 문서

- [[Backend Index]]
- [[Dashboard Index]]
- [[Automation Index]]
- [[Production Index]]

## 원문

- `src/ai_workspace/web/routes.py`
- `src/ai_workspace/web/automation_routes.py`
- `src/ai_workspace/web/production_routes.py`
- `src/ai_workspace/web/app.py`
