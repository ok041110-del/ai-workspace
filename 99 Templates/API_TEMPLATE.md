---
tags: [system]
type: documentation
---

# API_TEMPLATE

새 REST/WebSocket 엔드포인트를 **설계/구현**할 때 이 구조로 계약을
먼저 정리한다. 이 템플릿은 구현 전 설계용이고, 구현이 끝난 뒤
Vault [[API Catalog]]에 등록할 때는 [[Template - API]](완료된
엔드포인트의 회고적 카탈로그 항목)를 대신 쓴다.

## 구조

```
### {{METHOD}} {{/api/path}}

- 목적: {{이 엔드포인트가 왜 필요한가}}
- Request: {{path/query/body 파라미터}}
- Response: {{필드와 타입}}
- 에러 처리: {{4xx/5xx 상황과 응답}}
- 관련 ViewModel/DTO: {{타입 이름}}
- CQRS 분류: {{조회 전용(Read) / 쓰기(Write) — 대부분 Read Model,
  Write는 ExecutionDispatcher 경로로만}}
- 테스트 계획: {{TestClient로 검증할 시나리오}}
```

## 사용 방법

1. 구현 전 이 구조로 계약을 정리해 [[DESIGN_TEMPLATE]]의 "범위"
   절에 포함시킨다.
2. 구현/테스트가 끝나면 [[Template - API]]로 [[API Catalog]]에
   회고적으로 등록한다 — 이 설계 템플릿 자체를 Vault에 남기지
   않는다(임시 작업 문서).

## 관련 문서

- [[Template - API]]
- [[API Catalog]]
- [[DESIGN_TEMPLATE]]

## 원문

- `src/ai_workspace/web/`
