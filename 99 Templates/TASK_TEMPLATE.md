---
tags: [system]
type: documentation
---

# TASK_TEMPLATE

GitHub `.ai/TASKS.md`에 새 Task를 등록/완료 기록할 때 이 구조를
그대로 따른다. Vault Index 작성용이 아니라 **GitHub 원문(TASKS.md)
작성용** 템플릿이다 — Milestone 요약을 Vault에 남길 때는
[[Template - Milestone]]을 대신 쓴다.

## Task List 행

```
| {{Task ID}} | {{한 줄 내용}} | {{상태: 진행 예정/완료}} |
```

## Task 착수 전 DoD

```
**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | {{}} | |
| 2 | {{}} | |
```

## Task 완료 write-up

```
#### {{Task ID}}: {{제목}}
- 상태: **DONE ({{날짜}})** — {{구현 내용을 한 문단으로. 무엇을
  만들었고 무엇을 바꿨는지}}. 다음 Task: **{{다음 Task ID}}**
  ({{다음 Task 이름}}).
- 의존성: {{선행 Task ID 또는 "없음"}}.
```

## 사용 방법

1. Task 착수 전: "Task List 행" + "DoD"를 먼저 채워 승인받는다
   (승인 없이 구현하지 않는다, [[AI_RULES]]).
2. 구현 완료 후: "Task 완료 write-up"으로 TASKS.md에 기록한다.
   상세 구현 서술이 필요하면 [[IMPLEMENTATION_TEMPLATE]]을 이어서
   쓴다.

## 관련 문서

- [[IMPLEMENTATION_TEMPLATE]]
- [[DESIGN_TEMPLATE]]
- [[PROJECT_INDEX]]

## 원문

- `.ai/TASKS.md`
