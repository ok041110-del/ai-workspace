---
tags: [system]
type: documentation
---

# Template - Project Workspace

새 Project가 생길 때 이 Vault 안에 만들어야 하는 표준 폴더 구조를
정의한다(M25 요청 "Workspace Template"). 현재 이 Vault는 **단일
Project("AI Workspace" 자신)**만 다루므로, 이 구조를 별도
`Projects/<이름>/` 하위 트리로 지금 만들지 않는다 — 대신 그
구조가 이미 Vault Root 최상위 디렉터리(00 System~14 Tasks/99
Templates)로 1:1 대응돼 있음을 아래 표로 명시하고, **두 번째
Project가 실제로 생기는 시점**(`ProjectRepository`/`domain/
project.py`가 Vault와 연결되는 시점)에 이 템플릿을 그대로
`Projects/<이름>/` 아래 인스턴스화한다.

## 표준 구조

```
Projects/<Project 이름>/
  README.md       # Overview — 목적, 범위, 현재 상태
  Tasks/          # Task 1건당 문서 1개 ([[Template - Task]])
  Notes/          # 자유 형식 작업 메모
  Meetings/       # 회의록 (frontmatter: tags: [meeting])
  Decisions/      # 가벼운 판단 기록 ([[Template - Decision]])
  Archive/        # 종료된 Task/Note 보관
```

## 현재 Vault(단일 Project)와의 대응

| 표준 구조 | 이 Vault의 현재 디렉터리 |
|---|---|
| `README.md` | [[Overview]] |
| `Tasks/` | `14 Tasks/` |
| `Notes/` | `00 System/` |
| `Meetings/` | (아직 없음 — 필요해지면 `15 Meetings/` 신설, `#meeting` 태그) |
| `Decisions/` | `12 Decisions/` |
| `Archive/` | (아직 없음 — 종료 문서가 쌓이면 신설) |

## 사용 방법

1. 지금은 이 표를 참고 자료로만 쓴다 — 새 폴더를 미리 만들지
   않는다(YAGNI, [[AI_RULES]]).
2. 두 번째 Project를 실제로 이 Vault에서 관리해야 하는 시점에,
   위 "표준 구조"를 `Projects/<이름>/`로 그대로 만들고 이 문서를
   갱신해 인스턴스화 이력을 남긴다.

## 관련 문서

- [[Template - Task]]
- [[Template - Decision]]
- [[PROJECT_INDEX]]
- [[Overview]]

## 원문

- `workspace/README.md` (Phase 1 Project 도메인 계획)
- `docs/ROADMAP.md`
