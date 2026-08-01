---
tags: [system]
type: system
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
| Vault 구조/Metadata/Color/Link 원칙이 궁금하다(Information Architecture) | [[Vault Information Architecture]] |
| Vault 전체 Hub/Concept 지도가 필요하다(Knowledge Graph 탐색) | [[Knowledge Hub]] |
| Recommendation 파이프라인(M35~M44) 산출물이 궁금하다 | [[Recommendation Hub]] |
| 회고/교훈(Lesson)을 남기고 싶다 | [[Lessons]] |
| 개별 Task 진행 상태를 Obsidian에서 관리하고 싶다 | [[Template - Task]] → [[Milestones Index]] |
| Mobile(M23) 관련 작업 | [[iOS Design]] / [[Android Placeholder]] |
| 프롬프트를 어떻게 짧게 쓸지 모르겠다 | [[PROMPT_PROFILE]] |
| Vault 운영 규칙 자체가 궁금하다 | [[AI_RULES]] |

## Reading Profiles Index — 작업 유형별 표준 Retrieval

위 표가 작업 종류 → 문서 1줄 라우팅이라면, 작업 유형별로 필수/
선택/제외 문서와 Template·Retrieval 순서·예상 출력까지 정해진
표준 절차가 필요할 때는 [[READING_PROFILES]]를 먼저 연다(Backend
Implementation/API Design/ADR 작성/Bug Fix 등 15종 정의). 이 표와
[[READING_PROFILES]]는 같은 원칙(Retrieval First/Minimum Retrieval)
을 다른 세밀도로 적용한 것이며, 서로 대체하지 않는다.

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
| 개별 Task 문서(Obsidian 안에서 진행/상태 관리) | [[Template - Task]] |
| 새 Project(다중 Project 확장 시) 폴더 구조 | [[Template - Project Workspace]] |

산출물별 선택 기준과 "원문 작성용 vs Vault 등록용" 구분은
[[PROMPT_PROFILE]]의 Template Mapping 절 참고.

## Execution Flow — 요청부터 완료까지

이 문서(Retrieval)와 [[PROMPT_PROFILE]](요청 방식)로 "무엇을
어떻게 물을지"를 정했다면, 그 다음 "AI가 실제로 어떻게 처리하는가"
는 [[EXECUTION_PROFILE]]의 표준 절차를 따른다:

```
Task Start → Context Retrieval(이 문서) → Template Selection
  (Template Index) → Task Execution → Document Update
  → Validation → Completion Report
```

각 단계의 상세 규칙은 [[EXECUTION_PROFILE]] 참고.

## Preparation Status

**M23-Preparation(Obsidian Knowledge Base 구축) 완료**(T01~T07 +
T01A~T01D, 2026-07-27). 이 Vault 자체가 그 산출물이다. 전체 결과·
Baseline·M23 착수 조건은 [[PREPARATION_SUMMARY]] 참고 — 새 세션은
이 Vault를 쓰기 전에 그 문서의 "M23 Start Criteria"부터 확인한다.

## 관련 문서

- [[AI_CONTEXT]]
- [[AI_RULES]]
- [[PROMPT_PROFILE]]
- [[EXECUTION_PROFILE]]
- [[READING_PROFILES]]
- [[PREPARATION_SUMMARY]]

## 원문

- 없음(이 문서 자체가 Vault 진입점이며 GitHub에 대응 원문이 없다)
