---
tags: [task]
type: task
status: todo
priority: medium
milestone:
owner:
created:
updated:
---

# {{title}}

## Status

`todo` | `in-progress` | `review` | `done` | `archived`

Status Transition(Milestone 28, `vault/task_lifecycle.py`
`transition_task_status()`)이 허용하는 경로만 유효하다:

```
todo → in-progress → review → done → archived
         ↑______________|
```

`archived`로 전이하면 문서가 `14 Tasks/Archive/{{task_id}}.md`로
이동한다(파일명은 그대로라 Wikilink는 깨지지 않음).

## Priority

`low` | `medium` | `high`

## Milestone

<!-- 예: M27 -->

## Owner

<!-- 담당자/담당 Agent -->

## Created

<!-- YYYY-MM-DD -->

## Updated

<!-- YYYY-MM-DD -->

## Checklist

-

## Notes

<!-- 진행 중 메모, 발견한 문제 -->

## Related Documents

- [[Milestones Index]]

## Decision

<!-- 이 Task 중 내려진 판단. 무거워지면 [[Template - Decision]]로 승격 -->

## 관련 문서

- [[Template - Decision]]
- [[TASK_TEMPLATE]]
- [[Milestones Index]]

## 원문

- 없음(Vault 전용 — GitHub 원문 Task 기록은 `.ai/TASKS.md`)
