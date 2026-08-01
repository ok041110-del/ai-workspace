---
tags: [system]
type: documentation
---

# DESIGN_TEMPLATE

새 Milestone/기능을 설계할 때 이 구조를 복사해서 채운다(Template
First). 이 프로젝트가 지금까지의 모든 Milestone Kickoff에서 실제로
사용해 온 구조(목표/설계 원칙/DoD/Out of Scope)를 템플릿화한 것이다.

## {{기능/Milestone 이름}}

### 목표

{{이 작업으로 무엇을 달성하는가. 1~3문장}}

### 배경

{{왜 지금 이 작업이 필요한가. 관련 기존 컴포넌트/ADR이 있으면
[[ADR Index]] 링크}}

### 설계 원칙

- {{원칙 1}}
- {{원칙 2}}

### 범위(구현할 것)

- {{항목 1}}
- {{항목 2}}

### Out of Scope(하지 않을 것)

- {{항목 1}}

### Definition of Done

| # | 항목 |
|---|---|
| 1 | {{}} |
| 2 | {{}} |

### 관련 문서

- [[PROJECT_INDEX]]
- {{관련 Index 문서}}

## 사용 방법

1. 위 섹션을 복사해 새 문서 또는 프롬프트에 붙여넣는다.
2. `{{}}` 자리만 채운다 — 나머지 구조는 그대로 유지한다.
3. 채운 내용을 승인받은 뒤에만 구현을 시작한다(TASKS.md의 Task
   Driven Development 원칙, [[AI_RULES]] 참고).

## 관련 문서

- [[PROJECT_INDEX]]
- [[PROMPT_PROFILE]]
- [[AI_RULES]]

## 원문

- 없음(이 문서 자체가 Vault 전용 템플릿이며 GitHub에 대응 원문이
  없다)
