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
행을 찾아 그 문서만 읽는다. 전체 Vault나 GitHub 코드베이스를
처음부터 훑지 않는다([[AI_RULES]]의 Context Retrieval Rule).

### 3. Template Selection

만들려는 산출물 종류를 [[PROJECT_INDEX]]의 "Template Index" 또는
[[PROMPT_PROFILE]]의 "Template Mapping"에서 찾아 해당 템플릿으로
시작한다(Template First). 해당하는 템플릿이 없으면 가장 가까운
기존 문서의 구조를 따른다 — 새 템플릿을 즉흥적으로 만들지 않는다.

### 4. Task Execution

승인된 DoD 항목만 구현한다. 범위 밖 리팩터링/정리를 함께 하지
않는다("변경된 파일만 수정" 원칙). 구현 중 새로운 설계 판단이
필요하면 [[DECISION_TEMPLATE]]로 즉시 기록한다.

### 5. Document Update

구현이 끝나면 같은 커밋 안에서 관련 문서를 갱신한다 — GitHub
`.ai/TASKS.md`([[TASK_TEMPLATE]] 형식)와 필요 시 `docs/
ARCHITECTURE.md`/`.ai/DECISIONS.md`(GitHub 원문), 그리고 관련
Vault Index([[PROJECT_INDEX]]가 가리키는 문서, `Template - X.md`
형식). Vault는 GitHub 원문을 복제하지 않는다([[AI_RULES]]).

### 6. Validation

- Vault 문서라면: Backlink가 실제로 존재하는 문서를 가리키는지,
  Tag Rule을 따르는지, Index류 문서에 "원문" 섹션이 있는지 확인
  ([[AI_RULES]]의 GitHub Link Rule/Backlink Rule/Tag Rule).
- GitHub 코드 변경이라면: 관련 테스트/`ruff`/`mypy` 실행(GitHub
  `.ai/RULES.md` 기준, 이 문서 범위 밖).

### 7. Completion Report

요청자가 지정한 보고 형식을 그대로 따른다(형식을 지정하지 않았으면
[[TASK_TEMPLATE]]의 완료 write-up 형식). 이 단계에서 처음으로
결과를 커밋·푸시한다.

## 관련 문서

- [[PROJECT_INDEX]]
- [[PROMPT_PROFILE]]
- [[TASK_TEMPLATE]]
- [[AI_RULES]]

## 원문

- `.ai/RULES.md`(Task Driven Development 8단계 원칙의 GitHub 원문)
