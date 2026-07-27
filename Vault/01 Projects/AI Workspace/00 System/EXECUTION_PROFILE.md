---
tags: [system]
---

# EXECUTION_PROFILE

[[PROJECT_INDEX]](무엇을 읽을지)와 [[PROMPT_PROFILE]](어떻게
물어볼지)이 "탐색·요청" 단계를 다룬다면, 이 문서는 요청을 받은
뒤 AI가 실제로 작업을 수행하는 **표준 절차(Standard Execution
Workflow)**를 정의한다. GitHub `.ai/RULES.md`의 Task Driven
Development 원칙(승인 필요 항목·완료 전 테스트·문서 동기화 등)을
Vault 레벨에서 실행 가능한 7단계로 정리한 것이다.

## Standard Workflow

### 1. Task Start

요청을 받으면 바로 구현하지 않는다. 요청이 이미 승인된 DoD를
가리키는지(예: "TASKS의 DoD에 따라 구현") 확인하고, 없다면 목표/
DoD를 먼저 정리해 승인을 받는다(GitHub `.ai/RULES.md`의 승인
필요 원칙 — 이 문서가 그 원칙을 대체하지 않는다).

### 2. Context Retrieval

[[PROJECT_INDEX]]의 "Retrieval First" 표에서 작업과 가장 가까운
행을 찾는다. 그 작업 유형이 [[READING_PROFILES]]에 정의돼 있으면
(Architecture Design/Feature Design/API Design/Backend·Frontend·
Mobile Implementation/Dashboard·Automation Development/ADR·Decision
작성/Bug Fix/Refactoring/Documentation/Milestone Planning/Daily
기록) 해당 Profile의 "필수 문서"만 그 순서대로 읽는다 — "선택
문서"는 필수 문서만으로 판단이 서지 않을 때만 추가하고, "읽지
않는 문서"는 임의로 읽지 않는다(Minimum Retrieval). 해당하는
Profile이 없으면 기존대로 [[PROJECT_INDEX]] 라우팅 표의 문서만
읽는다. 전체 Vault나 GitHub 코드베이스를 처음부터 훑지 않는다
([[AI_RULES]]의 Context Retrieval Rule).

### 3. Template Selection

만들려는 산출물 종류를 [[PROJECT_INDEX]]의 "Template Index",
[[PROMPT_PROFILE]]의 "Template Mapping", 또는 2단계에서 이미 확인한
[[READING_PROFILES]] Profile의 "쓸 Template"에서 찾아 해당
템플릿으로 시작한다(Template First) — 세 출처는 서로 일치하도록
유지되므로 어느 쪽에서 찾아도 같은 템플릿에 도달한다. 해당하는
템플릿이 없으면 가장 가까운 기존 문서의 구조를 따른다 — 새 템플릿을
즉흥적으로 만들지 않는다.

### 4. Task Execution

승인된 DoD 항목만 구현한다. 범위 밖 리팩터링/정리를 함께 하지
않는다("변경된 파일만 수정" 원칙). 구현 중 새로운 설계 판단이
필요하면 [[DECISION_TEMPLATE]]로 즉시 기록한다.

### 5. Document Update

구현이 끝나면 같은 커밋 안에서 관련 문서를 갱신한다 — GitHub
`.ai/TASKS.md`([[TASK_TEMPLATE]] 형식)와 필요 시 `docs/
ARCHITECTURE.md`/`.ai/DECISIONS.md`(GitHub 원문), 그리고 관련
Vault Index([[PROJECT_INDEX]]가 가리키는 문서, `Template - X.md`
형식). Vault는 GitHub 원문을 복제하지 않는다([[AI_RULES]]). GitHub
원문 갱신 내용을 `VaultDocumentRequest`(kind/title/summary/
related_docs/fields)로 정리할 수 있으면(ADR/Decision 등),
`vault.auto_save.run_auto_save()`(M23-T03~T05,
[[Vault Integration Architecture]] 참고)를 호출해 저장까지 코드로
수행한다 — 손으로 여러 Vault 파일을 열어 고치는 대신 이 함수
하나로 끝낸다.

### 6. Validation

- Vault 문서라면: `run_auto_save()`가 돌려주는 `AutoSaveReport`로
  Backlink Rule(실제 문서를 가리키는지)/Tag Rule(신규 문서
  frontmatter)을 자동 확인한다(`AutoSaveReport.ok`가 `False`면
  `summary()`의 실패 목록부터 고친다). `run_auto_save()`를 쓰지
  않고 Vault 문서를 직접 수정했다면(예: 표 구조 변경처럼 Auto
  Save가 다루지 않는 편집), Backlink/Tag/원문 섹션을 수동으로
  확인한다([[AI_RULES]]의 GitHub Link Rule/Backlink Rule/Tag Rule).
- GitHub 코드 변경이라면: 관련 테스트/`ruff`/`mypy` 실행(GitHub
  `.ai/RULES.md` 기준, 이 문서 범위 밖).

## Execution Engine — 자연어 명령 라우팅(M23-T06)

사용자의 짧은 명령 하나가 위 7단계 전체를 어떻게 통과하는지
보여주는 흐름이다. 이 절 자체는 새 프로그램이 아니라 **AI(이
세션)가 항상 따르는 절차**를 명시적으로 적어 둔 것이다 — 자연어
해석은 AI의 역할이고, 그 이후 단계(Retrieval/Template/저장/검증)는
이미 코드([[READING_PROFILES]], `vault/`)로 뒷받침된다.

```
사용자 명령
  → PROJECT_INDEX(Retrieval First 표에서 작업 종류 확인)
  → AI_CONTEXT(현재 상태·다음 Task 확인, "다음 Task 진행"류일 때)
  → TASKS.md(승인된 DoD가 있는지 확인 — 1단계 Task Start)
  → READING_PROFILES(작업 유형의 Reading Profile 선택 — 2단계
    Context Retrieval)
  → Retrieval(Profile의 필수 문서만)
  → Template 선택(3단계 Template Selection)
  → 작업 수행(4단계 Task Execution)
  → Vault 저장(5단계, `vault.auto_save.run_auto_save()`)
  → Validation(6단계, `AutoSaveReport`)
  → 완료 보고(7단계)
```

### 지원 명령 예시

| 명령 | 해석 | 적용 Reading Profile |
|---|---|---|
| "다음 Task 진행" / "다음 작업 진행" | `.ai/TASKS.md`에서 진행 중 Milestone의 다음 미완료 Task를 찾아 그 DoD로 Task Start | 해당 Task 내용에 따라 결정 |
| "M23-T05 진행" (특정 Task ID) | 그 Task ID의 DoD를 `.ai/TASKS.md`에서 확인 후 Task Start | 해당 Task 내용에 따라 결정 |
| "ADR 작성" | 새 아키텍처 결정 기록 요청 | [[READING_PROFILES]]의 "ADR 작성" |
| "Bug Fix" | 증상 기반 원인 파악·수정 요청 | [[READING_PROFILES]]의 "Bug Fix" |
| "Feature Design" | 새 기능/Milestone 설계 착수 요청 | [[READING_PROFILES]]의 "Feature Design" |
| "API 설계" | 새 엔드포인트 계약 설계 요청 | [[READING_PROFILES]]의 "API Design" |

명령이 이 표에 없어도 절차는 같다 — [[READING_PROFILES]]의
Profile Index에서 가장 가까운 작업 유형을 고르고, 없으면
[[PROJECT_INDEX]] Retrieval First 표로 내려간다.

### 7. Completion Report

요청자가 지정한 보고 형식을 그대로 따른다(형식을 지정하지 않았으면
[[TASK_TEMPLATE]]의 완료 write-up 형식). 이 단계에서 처음으로
결과를 커밋·푸시한다.

## 관련 문서

- [[PROJECT_INDEX]]
- [[PROMPT_PROFILE]]
- [[READING_PROFILES]]
- [[TASK_TEMPLATE]]
- [[AI_RULES]]
- [[Vault Integration Architecture]]

## 원문

- `.ai/RULES.md`(Task Driven Development 8단계 원칙의 GitHub 원문)
