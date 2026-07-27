---
tags: [system]
---

# Tasks 사용법

이 폴더는 Task 1건당 문서 1개(`{task_id}.md`, 예: `T27-01.md`)를
담는다. GitHub `.ai/TASKS.md`의 Task List/DoD/완료 write-up을
대체하지 않는다 — 그 원문은 여전히 `.ai/TASKS.md`다. 이 폴더의
문서는 Obsidian 안에서 Task의 **현재 상태**(Status/Priority/
Checklist)를 바로 보고 갱신하기 위한 것으로, Milestone 27
(Obsidian Workspace Templates)에서 도입됐다.

새 Task 문서는 [[Template - Task]]를 복사해 만들거나
`vault.engine.VaultSaveEngine`에 `VaultDocumentKind.TASK` Request를
전달해 생성한다(`vault/router.py`가 `fields["task_id"]`로 파일명을
결정).

상태 변경(Todo→In Progress→Review→Done→Archived)은 Frontmatter를
직접 고치지 않고 `vault.task_lifecycle.transition_task_status()`
를 통해서 한다(Milestone 28-T01) — 허용되지 않은 전이를 막고
`updated`를 자동 갱신한다. `Archived`로 전이하면 문서가 `Archive/
{task_id}.md`로 옮겨진다(같은 파일명이라 Wikilink는 유지).

## 관련 문서

- [[Template - Task]]
- [[TASK_TEMPLATE]]
- [[Milestones Index]]
- [[Overview]]

## 원문

- `.ai/TASKS.md`
