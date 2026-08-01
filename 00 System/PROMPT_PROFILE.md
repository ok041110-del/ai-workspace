---
tags: [system]
type: system
---

# PROMPT_PROFILE

Short Prompt Workflow의 실제 패턴 모음. [[AI_RULES]]의 Prompt
Rules가 원칙이고, 이 문서는 그 원칙을 반복 작업 유형별 짧은
프롬프트 예시로 구체화한다.

## 원칙

- 문서를 다시 붙여넣지 말고 `[[문서 제목]]`으로 참조한다.
- "무엇을 바꿀지"만 짧게 쓰고, "왜 이 프로젝트가 이런 구조인지"는
  다시 설명하지 않는다(이미 Vault에 있다).
- 새 설계는 자유 서술 대신 [[DESIGN_TEMPLATE]] 형식을 요청한다.

## 패턴별 예시

| 작업 유형 | 짧은 프롬프트 예시 |
|---|---|
| 새 Milestone/기능 설계 | "[[DESIGN_TEMPLATE]] 형식으로 <기능명> 설계해줘" |
| 기존 영역 확장 | "[[Dashboard Index]] 기준으로 <확장 내용> 추가 설계해줘" |
| 버그 수정 | "<증상> 발생. 관련 영역은 [[Automation Index]] 참고해서 원인 파악해줘" |
| 문서만 갱신 | "[[Production Index]] 갱신 — <바뀐 내용>만 반영" |
| 과거 결정 확인 | "[[ADR Index]]에서 <주제> 관련 ADR 찾아서 요약해줘" |
| Milestone 이력 확인 | "[[Milestones Index]]에서 <Milestone 번호> 요약 보여줘" |
| 새 Task 착수 | "TASKS.md에 <Task ID> DoD 작성하고 승인 요청해줘" |

## Template Mapping(만들려는 것 → 쓸 템플릿)

작업 종류가 아니라 **지금 만들려는 산출물 종류**로 템플릿을
고를 때는 이 표를 쓴다(작업 종류→문서 라우팅은
[[PROJECT_INDEX]]의 Template Index 참고).

| 만들려는 것 | 쓸 템플릿 | 용도 |
|---|---|---|
| 새 Milestone/기능 설계 착수 | [[DESIGN_TEMPLATE]] | 목표/DoD 정의 |
| Task DoD 등록·완료 기록(TASKS.md) | [[TASK_TEMPLATE]] | GitHub 원문 작성 |
| 구현 결과 정리(커밋 전) | [[IMPLEMENTATION_TEMPLATE]] | 보고 전 체크리스트 |
| 새 ADR 원문 작성(DECISIONS.md) | [[ADR_TEMPLATE]] | GitHub 원문 작성 |
| ADR을 Vault Index에 요약 등록 | [[Template - ADR Summary]] | Vault 요약 등록 |
| 새 API 엔드포인트 설계 | [[API_TEMPLATE]] | 구현 전 계약 정리 |
| API를 Vault Catalog에 등록 | [[Template - API]] | Vault 요약 등록 |
| 가벼운 "왜?" 판단 기록 | [[DECISION_TEMPLATE]] | 판단 정리 |
| 판단을 Vault Index에 등록 | [[Template - Decision]] | Vault 요약 등록 |
| Milestone을 Vault Index에 등록 | [[Template - Milestone]] | Vault 요약 등록 |
| Daily Note 작성 | [[Template - Daily]] | 일일 기록 |

**구분 원칙**: `_TEMPLATE.md`(대문자, 밑줄)는 GitHub 원문/실제
구현물을 작성하기 **전** 계약을 정리하는 용도, `Template - X.md`
(공백, `-`)는 그 결과를 Vault Index에 요약으로 **등록**할 때
쓰는 용도다. 둘은 역할이 다르며 서로 대체하지 않는다.

## Reading Profile 연계

패턴별 짧은 프롬프트 예시는 "무엇을 요청할지"를 정한다. 요청을
받은 AI가 "구체적으로 어떤 문서를 어떤 순서로 읽을지"는
[[READING_PROFILES]]가 작업 유형별로(Architecture Design/Feature
Design/API Design/Backend·Frontend·Mobile Implementation/Dashboard·
Automation Development/ADR·Decision 작성/Bug Fix/Refactoring/
Documentation/Milestone Planning/Daily 기록) 필수/선택/제외 문서로
미리 정해 둔다. 프롬프트에 "[[READING_PROFILES]]의 <Profile 이름>
기준으로"라고만 덧붙이면 위 표의 예시 프롬프트에 Retrieval 범위까지
명시적으로 고정할 수 있다(예: "[[READING_PROFILES]]의 Bug Fix
기준으로 <증상> 원인 파악해줘").

## Execution Profile 연계

이 문서가 다루는 "어떻게 짧게 물어볼지"는 요청 단계까지다. 요청을
받은 뒤 AI가 실제로 수행하는 절차(Context Retrieval → Template
Selection → 구현 → 문서 갱신 → 검증 → 보고)는 [[EXECUTION_PROFILE]]
의 Standard Workflow 7단계를 따른다 — 이 표의 각 프롬프트 예시는
결국 그 7단계 중 1단계(Task Start)의 입력일 뿐이다.

## 안티패턴(피할 것)

- GitHub 파일 전체 내용을 프롬프트에 복사해 붙여넣기 — 대신
  경로/문서 제목만 언급.
- 이미 Vault에 정리된 배경 설명을 매번 다시 요청 — [[PROJECT_INDEX]]
  라우팅 표를 먼저 따른다.
- 템플릿 없이 새 설계 문서를 자유 형식으로 요청 — [[DESIGN_TEMPLATE]]
  를 우선 사용한다.

## 관련 문서

- [[PROJECT_INDEX]]
- [[AI_RULES]]
- [[DESIGN_TEMPLATE]]
- [[EXECUTION_PROFILE]]
- [[READING_PROFILES]]

## 원문

- 없음(이 문서 자체가 Vault 전용 프롬프트 가이드이며 GitHub에
  대응 원문이 없다)
