---
tags: [ios]
type: documentation
---

# iOS Design

> Mobile Experience(Milestone 번호 미정 — 2026-07-27 M23이 "Obsidian
> Integration & Auto Save"로 재정의되며 이월, [[Decisions Index]]
> 참고) 설계 메모. **아직 구현하지
> 않는다** — 서버(Production Platform, M22)가 이미 필요한 API를
> 제공하므로 이 Milestone은 그 API를 소비하는 Client를 만드는
> 작업이다.

## 범위(계획)

- **Home Screen Widget**: `/api/status`(경량 4필드: health_status/
  version/started_at/uptime_seconds)를 주기적으로 폴링해 워크스페이스
  상태를 홈 화면에 표시.
- **Lock Screen Widget**: 동일 API를 더 축약된 형태로 표시.
- **Live Activity**: 실행 중인 Task/Automation Rule의 진행 상황을
  실시간으로 보여줌(WebSocket `/ws/dashboard` 또는 Push 연동 검토
  필요 — 미결정).
- **Push Notification**: Execution 실패/Automation 발동 등 주요
  Event를 푸시로 전달. 서버(`ok041110-del/ai-workspace`)가 Push를
  생성·관리하고, 실제 전송은 FCM/APNs를 통해 수행한다(2026-07-27
  Start Criteria 확정, [[PREPARATION_SUMMARY]] 참고).

## 사용할 서버 API

[[API Catalog]]의 기존 엔드포인트를 그대로 사용한다(서버 쪽 Mobile
전용 로직 추가 없음, [[Overview]] 참고):

- `/api/status`, `/api/health` — Production 상태
- `/api/dashboard`, `/api/summary` — Workspace 현황
- `/api/automation` — Automation Rule 조회
- `/ws/dashboard` — 실시간 갱신(Live Activity 후보)

## 기술 스택(제안, 미확정)

SwiftUI + WidgetKit(Home/Lock Screen Widget) + ActivityKit(Live
Activity) + APNs(Push). 해당 Milestone kickoff 시 정식 확정 필요.

## Start Criteria 확정 사항(2026-07-27)

- Client(iOS/Android) 코드는 이 Python 저장소(`ok041110-del/
  ai-workspace`)와 분리된 별도 저장소에 둔다([[Overview]]의
  "저장소 목록" 참고, 저장소 자체는 아직 생성 전).
- 이 저장소는 Server(API)까지만 담당하며 Mobile Client는 포함하지
  않는다.
- Push는 이 저장소의 Server가 생성·관리하고, 실제 전송은 FCM/APNs를
  이용한다.

## 남은 미결정 사항

- 기술 스택(SwiftUI/WidgetKit/ActivityKit)은 여전히 제안 단계 —
  별도 Client 저장소 kickoff 시 확정.
- Live Activity의 실시간 갱신 경로(`/ws/dashboard` 직접 구독 vs
  Push 경유)는 미정.

## 관련 문서

- [[Overview]]
- [[API Catalog]]
- [[Production Index]]
- [[Android Placeholder]]

## 원문

- (착수 전 — 아직 GitHub에 구현 코드 없음)
