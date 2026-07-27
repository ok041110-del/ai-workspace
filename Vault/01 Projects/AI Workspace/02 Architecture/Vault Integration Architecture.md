---
tags: [architecture]
---

# Vault Integration Architecture

## 요약

GitHub 원문(`.ai/TASKS.md`/`.ai/DECISIONS.md`/`.ai/MEMORY.md`/
`docs/ARCHITECTURE.md`/`docs/ROADMAP.md`)이 갱신된 뒤, 관련 Vault
문서(Index류)를 자동으로 만들거나 갱신하는 계층(M23-T02 설계,
ADR-0035). Core Domain·`web/`을 전혀 모르는 독립 계층이며, AI
Workspace 제품 기능이 아니라 이 프로젝트의 **개발 과정 자체를
돕는 도구**다.

## Layer 구조

`storage/`(도메인 객체 JSON 영속성)와 나란히 존재하는 새 최상위
패키지 `vault/`. 아래로도 위로도 의존하지 않는다 — Core
Domain(`domain`/`interfaces`/`engines`)이 `vault/`를 모르고,
`vault/`도 Core Domain 타입을 가져오지 않는다(구조화 입력은
`kind`/`title`/`summary`/`related_docs`/`source_paths`로 구성된
독립 스키마).

## 핵심 컴포넌트

| 이름 | 역할 |
|---|---|
| Vault Directory Mapping | 문서 종류(kind, Tag Rule 11종과 1:1) → 대상 Vault 파일 고정 매핑 |
| Document Router | kind로 대상 파일 결정 + append(기존 Index) vs create(신규 파일, 예: Daily) 판단 |
| Markdown Generator | `99 Templates/`의 해당 Template로 렌더링(frontmatter tags/Backlink/"원문" 섹션 고정 포함) |
| Vault Writer | File Creator(신규 파일 생성) / File Updater(기존 파일의 대상 섹션만 치환) |

## Execution Flow

```
GitHub 원문 갱신(Standard Workflow 5단계, Document Update)
  → 구조화 입력 작성(kind/title/summary/related_docs/source_paths)
  → Document Router(대상 파일 결정)
  → Markdown Generator(Template 렌더링)
  → Vault Writer(파일 생성 또는 대상 섹션만 치환, 실제 변경 시에만 저장)
```

## Vault Directory Mapping

| kind | 대상 문서 | 방식 |
|---|---|---|
| adr | [[ADR Index]] | append |
| decision | [[Decisions Index]] | append |
| backend | [[Backend Index]] | append |
| api | [[API Catalog]] | append |
| dashboard | [[Dashboard Index]] | append |
| automation | [[Automation Index]] | append |
| production | [[Production Index]] | append |
| ios | [[iOS Design]] | append |
| android | [[Android Placeholder]] | append |
| milestone | [[Milestones Index]] | append |
| daily | `13 Daily/{{YYYY-MM-DD}}.md` | create |
| architecture | [[Architecture Overview]] | append |
| system | `00 System/` | 수동(자동 대상 아님) |

## File Strategy

- 신규 문서(Daily 등): File Creator가 전체 파일 생성.
- 기존 Index 문서: File Updater가 **대상 섹션만** 문자열 치환하거나
  말미에 추가 — 과거 수작업으로 채운 내용을 보존한다.
- 실제 내용이 바뀔 때만 파일을 쓴다(불필요한 diff 방지).

## 범위 밖(이 설계 시점, M23-T02)

- 실제 코드 구현 — [[READING_PROFILES]] 기준 Backend Implementation
  대상, M23-T03(Vault Save Engine).
- Task 완료 시 자동 트리거 — M23-T04(Auto Save Workflow).
- Rename/Delete/Conflict/Version 정책 — M23-T05(Vault
  Synchronization).
- 자연어 명령 라우팅 — M23-T06(Execution Engine).
- Claude Code/Filesystem/MCP/GitHub 실제 연동 검증 — M23-T07
  (Execution Environment Integration).

## 관련 문서

- [[Architecture Overview]]
- [[ADR Index]]
- [[READING_PROFILES]]
- [[EXECUTION_PROFILE]]

## 원문

- `.ai/DECISIONS.md` (ADR-0035)
- `docs/ARCHITECTURE.md` (§3.21)
