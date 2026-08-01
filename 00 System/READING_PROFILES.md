---
tags: [system]
type: system
---

# READING_PROFILES

[[PROJECT_INDEX]]의 "Retrieval First" 표가 작업 종류 → 문서 1줄
라우팅이라면, 이 문서는 그 라우팅을 15개 **작업 유형별 표준
Retrieval 절차(Reading Profile)**로 세분화한 것이다. 각 Profile은
목적/필수 문서/선택 문서/읽지 않는 문서/쓸 Template/예상 Retrieval
순서/예상 출력 문서 7항목을 고정 형식으로 제공해, AI가 매번 무엇을
읽을지 새로 판단하지 않고 이 표만 따르게 한다.

## 사용 원칙

- **Retrieval First**: 코드베이스나 Vault를 처음부터 훑지 않고,
  먼저 이 문서에서 작업과 일치하는 Profile을 찾는다.
- **Minimum Retrieval**: Profile의 "필수 문서"만 우선 읽는다.
  "선택 문서"는 필수 문서만으로 판단이 서지 않을 때만 추가로
  읽는다. "읽지 않는 문서"는 해당 작업에서 의도적으로 제외한
  것이므로 임의로 읽지 않는다.
- **Short Prompt Workflow**: Profile을 확인한 뒤에는 문서 내용을
  프롬프트에 복사하지 않고 `[[문서 제목]]`으로만 참조한다
  ([[PROMPT_PROFILE]]).
- **Template First**: "쓸 Template" 열이 가리키는 템플릿으로
  산출물을 시작한다. 자유 형식으로 새로 만들지 않는다.
- **Standard Execution Workflow**: Profile 선택은
  [[EXECUTION_PROFILE]] Standard Workflow의 2단계(Context
  Retrieval)를 대체하지 않고 구체화한다 — 순서는 동일하게
  Task Start → Context Retrieval(이 문서로 Profile 선택 후 Retrieval)
  → Template Selection → Task Execution → Document Update →
  Validation → Completion Report를 따른다.

## Profile Index

| # | Profile | 핵심 필수 문서 |
|---|---|---|
| 1 | [Architecture Design](#1-architecture-design) | [[Architecture Overview]] |
| 2 | [Feature Design](#2-feature-design) | [[Overview]] |
| 3 | [API Design](#3-api-design) | [[API Catalog]] |
| 4 | [Backend Implementation](#4-backend-implementation) | [[Backend Index]] |
| 5 | [Frontend Implementation](#5-frontend-implementation) | [[Dashboard Index]] |
| 6 | [Mobile(iOS/Android) Implementation](#6-mobileiosandroid-implementation) | [[iOS Design]] / [[Android Placeholder]] |
| 7 | [Dashboard Development](#7-dashboard-development) | [[Dashboard Index]] |
| 8 | [Automation Development](#8-automation-development) | [[Automation Index]] |
| 9 | [ADR 작성](#9-adr-작성) | [[ADR Index]] |
| 10 | [Decision 작성](#10-decision-작성) | [[Decisions Index]] |
| 11 | [Bug Fix](#11-bug-fix) | [[PROJECT_INDEX]] 라우팅 표 |
| 12 | [Refactoring](#12-refactoring) | [[Architecture Overview]] |
| 13 | [Documentation](#13-documentation) | [[PROJECT_INDEX]] |
| 14 | [Milestone Planning](#14-milestone-planning) | [[Milestones Index]] |
| 15 | [Daily 기록](#15-daily-기록) | [[Template - Daily]] |

---

## 1. Architecture Design

- **목적**: 새 아키텍처 계층/컴포넌트 경계를 설계하거나 기존
  구조를 변경한다.
- **필수 문서**: [[Architecture Overview]], [[Architecture Map]]
- **선택 문서**: [[ADR Index]](과거 유사 결정 확인), [[Backend Index]]
  (영향받는 구현 영역 확인)
- **읽지 않는 문서**: [[Dashboard Index]], [[Automation Index]],
  [[iOS Design]], [[Android Placeholder]](아키텍처 경계 설계 자체와
  무관)
- **쓸 Template**: [[DESIGN_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[Architecture Overview]]
  → [[Architecture Map]] → (필요 시) [[ADR Index]]
- **예상 출력 문서**: `docs/ARCHITECTURE.md`(GitHub 원문 갱신),
  필요 시 [[Template - Architecture]]로 Vault 반영, 큰 결정이면
  ADR([[ADR_TEMPLATE]])

## 2. Feature Design

- **목적**: 새 기능/Milestone 착수를 위해 목표와 DoD를 정의한다.
- **필수 문서**: [[Overview]], [[DESIGN_TEMPLATE]]
- **선택 문서**: 기능이 속한 영역의 Index([[Dashboard Index]] /
  [[Automation Index]] / [[Production Index]] 중 해당하는 것)
- **읽지 않는 문서**: 관련 없는 영역 Index 전부, [[ADR Index]]
  (신규 설계 판단에 과거 ADR이 직접 필요할 때만 예외)
- **쓸 Template**: [[DESIGN_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[Overview]] →
  (해당 영역 Index)
- **예상 출력 문서**: `.ai/TASKS.md`의 Task List/DoD([[TASK_TEMPLATE]]),
  필요 시 `docs/ROADMAP.md`

## 3. API Design

- **목적**: 새 REST/WebSocket 엔드포인트 계약을 설계한다.
- **필수 문서**: [[API Catalog]], [[Backend Index]]
- **선택 문서**: [[Architecture Overview]](영향 범위가 계층을
  넘어설 때)
- **읽지 않는 문서**: [[iOS Design]], [[Android Placeholder]]
  (Client 소비 방식은 API 계약 확정 후 별도 Profile), [[Dashboard Index]]
  (Dashboard 전용 API가 아닌 이상)
- **쓸 Template**: [[API_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[API Catalog]] →
  [[Backend Index]]
- **예상 출력 문서**: API 계약 정리([[API_TEMPLATE]]), 구현 후
  [[Template - API]]로 [[API Catalog]] 등록

## 4. Backend Implementation

- **목적**: 서버/Interface/Adapter 등 백엔드 코드를 구현한다.
- **필수 문서**: [[Backend Index]], [[Architecture Overview]]
- **선택 문서**: [[API Catalog]](API 계약이 관련될 때)
- **읽지 않는 문서**: [[iOS Design]], [[Android Placeholder]],
  [[Dashboard Index]](프론트엔드 코드가 아닌 이상)
- **쓸 Template**: [[TASK_TEMPLATE]](DoD) → [[IMPLEMENTATION_TEMPLATE]]
  (구현 정리)
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[Backend Index]] →
  [[Architecture Overview]] → (필요 시) [[API Catalog]]
- **예상 출력 문서**: `src/ai_workspace/` 코드, `.ai/TASKS.md`
  write-up, 필요 시 `docs/ARCHITECTURE.md`

## 5. Frontend Implementation

- **목적**: 웹 프론트엔드(Dashboard 등 브라우저 UI) 코드를 구현한다.
- **필수 문서**: [[Dashboard Index]], [[API Catalog]]
- **선택 문서**: [[Architecture Overview]](Client-Server 경계 확인
  필요 시)
- **읽지 않는 문서**: [[Backend Index]](API 계약만 있으면 충분,
  서버 내부 구현 세부는 불필요), [[iOS Design]], [[Android Placeholder]]
- **쓸 Template**: [[TASK_TEMPLATE]] → [[IMPLEMENTATION_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[Dashboard Index]]
  → [[API Catalog]](소비할 엔드포인트만)
- **예상 출력 문서**: 프론트엔드 코드, `.ai/TASKS.md` write-up,
  필요 시 [[Dashboard Index]] 갱신

## 6. Mobile(iOS/Android) Implementation

- **목적**: iOS/Android 클라이언트 코드를 설계·구현한다.
- **필수 문서**: [[iOS Design]](iOS) 또는 [[Android Placeholder]]
  (Android)
- **선택 문서**: [[API Catalog]](서버 API 소비 방식), [[Production Index]]
  (Health/Version 등 M22 표준 필드 재사용 확인)
- **읽지 않는 문서**: [[Backend Index]](서버 내부 구현 세부는
  불필요, API 계약만 필요), [[Automation Index]]
- **쓸 Template**: [[DESIGN_TEMPLATE]](신규 설계) 또는
  [[IMPLEMENTATION_TEMPLATE]](이미 승인된 설계의 구현)
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[iOS Design]] /
  [[Android Placeholder]] → (필요 시) [[API Catalog]]
- **예상 출력 문서**: Client 코드(저장소 위치는 M23 Start Criteria
  #1 확정 후), `.ai/TASKS.md` write-up, [[iOS Design]]/
  [[Android Placeholder]] 갱신

## 7. Dashboard Development

- **목적**: Dashboard 기능(화면/위젯/실시간 갱신)을 추가·수정한다.
- **필수 문서**: [[Dashboard Index]]
- **선택 문서**: [[API Catalog]](신규 데이터 소스 필요 시),
  [[Automation Index]](Automation 연동 화면일 때)
- **읽지 않는 문서**: [[iOS Design]], [[Android Placeholder]],
  [[ADR Index]](신규 아키텍처 판단이 필요할 때만 예외)
- **쓸 Template**: [[TASK_TEMPLATE]] → [[IMPLEMENTATION_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[Dashboard Index]]
  → (필요 시) [[API Catalog]]
- **예상 출력 문서**: Dashboard 코드, `.ai/TASKS.md` write-up,
  [[Dashboard Index]] 갱신

## 8. Automation Development

- **목적**: 자동화 워크플로/스케줄링 기능을 추가·수정한다.
- **필수 문서**: [[Automation Index]]
- **선택 문서**: [[API Catalog]](Automation이 노출/소비하는 API가
  있을 때)
- **읽지 않는 문서**: [[Dashboard Index]](Automation 결과를 보여줄
  화면 작업이 아닌 이상), [[iOS Design]], [[Android Placeholder]]
- **쓸 Template**: [[TASK_TEMPLATE]] → [[IMPLEMENTATION_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[Automation Index]]
  → (필요 시) [[API Catalog]]
- **예상 출력 문서**: Automation 코드, `.ai/TASKS.md` write-up,
  [[Automation Index]] 갱신

## 9. ADR 작성

- **목적**: 되돌리기 어렵거나 구조에 영향을 주는 결정을 정식
  ADR로 기록한다.
- **필수 문서**: [[ADR Index]]
- **선택 문서**: [[Architecture Overview]](구조 영향 확인),
  [[Decisions Index]](경량 판단으로 이미 다뤄졌는지 확인)
- **읽지 않는 문서**: [[Dashboard Index]]/[[Automation Index]]/
  [[Production Index]](결정 대상 영역이 아닌 이상)
- **쓸 Template**: [[ADR_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[ADR Index]] →
  (필요 시) [[Architecture Overview]]
- **예상 출력 문서**: `.ai/DECISIONS.md`(GitHub 원문, ADR 번호
  발급), [[Template - ADR Summary]]로 [[ADR Index]] 등록

## 10. Decision 작성

- **목적**: ADR로 남길 정도는 아닌 가벼운 "왜 이렇게 했는가"
  판단을 기록한다.
- **필수 문서**: [[Decisions Index]]
- **선택 문서**: 판단이 속한 영역 Index(해당하는 경우)
- **읽지 않는 문서**: [[ADR Index]](ADR과 Decision은 별개 트랙 —
  ADR로 격상할지는 별도 판단), [[Architecture Map]]
- **쓸 Template**: [[DECISION_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[Decisions Index]]
- **예상 출력 문서**: 판단 기록(필요 시 GitHub 원문),
  [[Template - Decision]]로 [[Decisions Index]] 등록

## 11. Bug Fix

- **목적**: 증상이 보고된 결함을 원인 분석 후 수정한다.
- **필수 문서**: [[PROJECT_INDEX]] Retrieval First 표에서 증상이
  속한 영역의 Index 1개(예: [[Dashboard Index]], [[Backend Index]])
- **선택 문서**: [[ADR Index]](의도된 설계인지 실제 버그인지
  구분이 필요할 때)
- **읽지 않는 문서**: [[DESIGN_TEMPLATE]](신규 설계 아님),
  [[Milestones Index]]
- **쓸 Template**: [[TASK_TEMPLATE]](경량 DoD — "증상 재현 →
  원인 → 수정 → 회귀 테스트")
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → 증상 영역 Index →
  (필요 시) GitHub 원문 코드
- **예상 출력 문서**: 코드 수정 + 회귀 테스트, `.ai/TASKS.md`
  write-up

## 12. Refactoring

- **목적**: 동작 변경 없이 코드 구조/품질을 개선한다.
- **필수 문서**: [[Architecture Overview]], 대상 영역 Index
- **선택 문서**: [[ADR Index]](현재 구조가 의도된 결정인지 확인)
- **읽지 않는 문서**: [[DESIGN_TEMPLATE]](신규 기능 설계 아님)
- **쓸 Template**: [[TASK_TEMPLATE]] → [[IMPLEMENTATION_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[Architecture Overview]]
  → 대상 영역 Index
- **예상 출력 문서**: 코드 변경(동작 동일), `.ai/TASKS.md`
  write-up, 필요 시 `docs/ARCHITECTURE.md`

## 13. Documentation

- **목적**: GitHub 원문 문서(`docs/`, `.ai/`) 또는 Vault Index
  문서 자체를 작성·갱신한다.
- **필수 문서**: [[PROJECT_INDEX]], [[AI_RULES]]
- **선택 문서**: 갱신 대상 문서와 연결된 Index([[Backend Index]] 등)
- **읽지 않는 문서**: 갱신 대상과 무관한 코드 영역 Index 전부
- **쓸 Template**: 대상 산출물에 따라 [[PROMPT_PROFILE]]의
  "Template Mapping" 표에서 선택
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[AI_RULES]] →
  갱신 대상 문서
- **예상 출력 문서**: 갱신된 문서 자체(GitHub 원문 및/또는 Vault
  Index)

## 14. Milestone Planning

- **목적**: 새 Milestone의 목표를 정하고 Task로 분해한다.
- **필수 문서**: [[Milestones Index]], [[Overview]]
- **선택 문서**: [[ADR Index]], [[Decisions Index]](과거 유사
  Milestone의 판단 재확인)
- **읽지 않는 문서**: 세부 구현 Index([[Backend Index]],
  [[API Catalog]] 등 — Task 분해 이전 단계에는 불필요, 분해 후
  개별 Task Profile에서 다룬다)
- **쓸 Template**: [[DESIGN_TEMPLATE]]
- **예상 Retrieval 순서**: [[PROJECT_INDEX]] → [[Milestones Index]]
  → [[Overview]]
- **예상 출력 문서**: `.ai/TASKS.md` Task List, `docs/ROADMAP.md`,
  [[Template - Milestone]]로 [[Milestones Index]] 등록

## 15. Daily 기록

- **목적**: 하루 작업 내역을 짧게 기록한다.
- **필수 문서**: [[Template - Daily]]
- **선택 문서**: 그날 작업한 영역 Index(요약에 링크할 때만)
- **읽지 않는 문서**: 그 외 전체 Vault
- **쓸 Template**: [[Template - Daily]]
- **예상 Retrieval 순서**: [[Template - Daily]](Router 경유 없이
  바로 사용 — 형식이 고정적이므로 [[PROJECT_INDEX]] 확인이 필수는
  아니다)
- **예상 출력 문서**: `13 Daily/{{날짜}}.md`

## 관련 문서

- [[PROJECT_INDEX]]
- [[PROMPT_PROFILE]]
- [[EXECUTION_PROFILE]]
- [[AI_RULES]]

## 원문

- 없음(이 문서 자체가 Vault 전용 Retrieval 표준이며 GitHub에
  대응 원문이 없다)
