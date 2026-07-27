---
tags: [system]
---

# PROJECT_INDEX

이 문서는 Vault에서 **가장 먼저 여는 문서**다(`AI_CONTEXT`보다도
먼저) — "무엇을 읽어야 하는가"를 작업 종류별로 즉시 알려주는
Router 역할만 한다. 프로젝트 설명은 [[AI_CONTEXT]], 운영 규칙은
[[AI_RULES]] 참고.

## Retrieval First — 작업 종류 → 읽을 문서

전체 Vault를 읽지 않는다. 아래 표에서 작업과 가장 가까운 행 하나만
따라간다.

| 작업 종류 | 읽을 문서(순서대로) |
|---|---|
| 지금 프로젝트가 어떤 상태인지 모르겠다 | [[AI_CONTEXT]] → [[Overview]] |
| 새 Milestone/기능을 설계해야 한다 | [[DESIGN_TEMPLATE]] → [[Overview]] → [[Architecture Overview]] |
| Dashboard 관련 작업 | [[Dashboard Index]] → 필요 시 [[API Catalog]] |
| Automation 관련 작업 | [[Automation Index]] → 필요 시 [[API Catalog]] |
| Production/운영 관련 작업 | [[Production Index]] → 필요 시 [[API Catalog]] |
| Backend/Interface 구조가 궁금하다 | [[Backend Index]] → [[Architecture Overview]] |
| REST/WebSocket 엔드포인트가 궁금하다 | [[API Catalog]] |
| 과거 결정("왜 이렇게 했는가")이 궁금하다 | [[Decisions Index]] → 더 상세하면 [[ADR Index]] |
| 특정 ADR 전문이 필요하다 | [[ADR Index]]에서 항목 확인 → GitHub `.ai/DECISIONS.md` 원문 |
| 과거 Milestone 이력이 궁금하다 | [[Milestones Index]] |
| Mobile(M23) 관련 작업 | [[iOS Design]] / [[Android Placeholder]] |
| 프롬프트를 어떻게 짧게 쓸지 모르겠다 | [[PROMPT_PROFILE]] |
| Vault 운영 규칙 자체가 궁금하다 | [[AI_RULES]] |

## Short Prompt Workflow

이 표로 문서를 먼저 찾은 뒤에는, 그 문서의 제목/경로만 프롬프트에
넣고 내용을 다시 붙여넣지 않는다. 예: "Dashboard Index 기준으로
Automation 연동 부분 확인해줘"(O) vs GitHub 파일 전체를 프롬프트에
복사(X). 자세한 패턴은 [[PROMPT_PROFILE]] 참고.

## Template First

새 문서/새 설계를 시작할 때는 자유 형식보다 `99 Templates/`의
템플릿을 먼저 사용한다. 설계 착수는 [[DESIGN_TEMPLATE]]을 복사하는
것으로 시작한다.

## Template Index — 만들려는 산출물 → 쓸 템플릿

| 산출물 | 템플릿 |
|---|---|
| Milestone/기능 설계 착수 | [[DESIGN_TEMPLATE]] |
| Task DoD/완료 기록 | [[TASK_TEMPLATE]] |
| 구현 결과 정리 | [[IMPLEMENTATION_TEMPLATE]] |
| 새 ADR 원문 | [[ADR_TEMPLATE]] |
| 새 API 엔드포인트 설계 | [[API_TEMPLATE]] |
| 가벼운 판단 기록 | [[DECISION_TEMPLATE]] |
| ADR/API/Milestone/Decision을 Vault Index에 요약 등록 | [[Template - ADR Summary]] / [[Template - API]] / [[Template - Milestone]] / [[Template - Decision]] |
| Daily Note | [[Template - Daily]] |

산출물별 선택 기준과 "원문 작성용 vs Vault 등록용" 구분은
[[PROMPT_PROFILE]]의 Template Mapping 절 참고.

## 관련 문서

- [[AI_CONTEXT]]
- [[AI_RULES]]
- [[PROMPT_PROFILE]]

## 원문

- 없음(이 문서 자체가 Vault 진입점이며 GitHub에 대응 원문이 없다)
