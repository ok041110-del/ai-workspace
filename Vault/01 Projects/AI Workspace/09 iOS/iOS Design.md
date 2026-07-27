---
tags: [ios]
---

# iOS Design

> Milestone 23(Mobile Experience) 설계 메모. **아직 구현하지
> 않는다** — 서버(Production Platform, M22)가 이미 필요한 API를
> 제공하므로 M23은 이 API를 소비하는 Client를 만드는 작업이다.

## 범위(계획)

- **Home Screen Widget**: `/api/status`(경량 4필드: health_status/
  version/started_at/uptime_seconds)를 주기적으로 폴링해 워크스페이스
  상태를 홈 화면에 표시.
- **Lock Screen Widget**: 동일 API를 더 축약된 형태로 표시.
- **Live Activity**: 실행 중인 Task/Automation Rule의 진행 상황을
  실시간으로 보여줌(WebSocket `/ws/dashboard` 또는 Push 연동 검토
  필요 — 미결정).
- **Push Notification**: Execution 실패/Automation 발동 등 주요
  Event를 푸시로 전달(서버 쪽 Push 발송 주체는 미정 — M23 본 작업에서
  결정 필요).

## 사용할 서버 API

[[API Catalog]]의 기존 엔드포인트를 그대로 사용한다(서버 쪽 Mobile
전용 로직 추가 없음, [[Overview]] 참고):

- `/api/status`, `/api/health` — Production 상태
- `/api/dashboard`, `/api/summary` — Workspace 현황
- `/api/automation` — Automation Rule 조회
- `/ws/dashboard` — 실시간 갱신(Live Activity 후보)

## 기술 스택(제안, 미확정)

SwiftUI + WidgetKit(Home/Lock Screen Widget) + ActivityKit(Live
Activity) + APNs(Push). M23 kickoff 시 정식 확정 필요.

## 미결정 사항

- 이 Python 저장소(`ok041110-del/ai-workspace`)와 iOS 앱 코드가
  같은 저장소에 있을지, 별도 저장소로 분리할지 아직 결정되지 않음
  ([[Overview]]의 "저장소 목록" 참고).
- Push 발송을 서버가 담당할지, 별도 서비스가 담당할지 미정.

## 관련 문서

- [[Overview]]
- [[API Catalog]]
- [[Production Index]]
- [[Android Placeholder]]

## 원문

- (M23 착수 전 — 아직 GitHub에 구현 코드 없음)
