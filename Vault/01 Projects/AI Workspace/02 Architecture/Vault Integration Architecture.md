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

## 구현 상태(M23-T03, Vault Save Engine)

`src/ai_workspace/vault/`에 `VaultDocumentKind`/`VaultDocumentRequest`
(models.py), `VAULT_DIRECTORY_MAP`(mapping.py), `DocumentRouter`
(router.py), `render_section`/`render_daily_file`
(markdown_generator.py), `VaultWriter`(writer.py, 신규 파일 생성 +
기존 섹션 upsert), `VaultSaveEngine`(engine.py, Save Flow 전체를
잇는 진입점)로 구현 완료.

## 구현 상태(M23-T04, Auto Save Workflow)

`vault/validation.py`(`find_broken_backlinks`/`find_missing_tags` —
`AI_RULES`의 Backlink Rule/Tag Rule을 코드로 확인), `vault/
auto_save.py`(`run_auto_save` — 여러 `VaultDocumentRequest`를 한
번에 저장한 뒤 Vault 전체 Backlink와 새로 만든 파일의 Tag를 검증해
`AutoSaveReport`를 돌려줌. `AutoSaveReport.summary()`가 "저장됨 N개/
변경 없음 N개/Validation 통과(또는 실패 목록)" 형태의 완료 보고
문구를 만든다)로 구현 완료. `tests/vault/` 27개(T03 18 + T04 9),
`ruff`/`mypy` 클린.

## 구현 상태(M23-T05, Vault Synchronization)

`vault/sync.py`(신규): `rename_document()`가 파일명을 바꾸고
Vault 전체에서 그 문서를 가리키는 `[[..]]`/`[[..|별칭]]`/
`[[..#절]]`을 일괄 갱신한다. `delete_document()`는 다른 문서가
아직 참조 중이면 기본적으로 삭제를 거부하고 참조 목록을 돌려준다
(Orphan Backlink 방지, `force=True`로 강제 가능). `content_hash()`
+ `VaultWriter.upsert_section(expected_hash=...)`로 Conflict
Handling을 구현 — 저장 시점 사이 파일이 다른 경로로 바뀌면
`VaultConflictError`. **Version Strategy**: 별도 버전 관리를 새로
만들지 않고 이미 git으로 관리되는 `Vault/`를 그대로 쓴다(최소
복잡성). Link/Backlink Validation은 M23-T04의
`find_broken_backlinks()`를 재사용. `tests/vault/` 38개(T03 18 +
T04 9 + T05 11), `ruff`/`mypy` 클린.

## 구현 상태(M23-T06, Execution Engine)

새 Python 코드가 아니라 **절차 문서**로 구현됐다 — 자연어 해석은
AI(이 세션) 고유의 역할이라 결정적 프로그램으로 대체할 대상이
아니고, 그 이후 단계(Retrieval/Template/저장/검증)는 이미
[[READING_PROFILES]]와 `vault/`(M23-T03~T05)가 코드로 뒷받침하기
때문이다. [[EXECUTION_PROFILE]]에 "Execution Engine — 자연어 명령
라우팅" 절을 추가해 "사용자 명령 → PROJECT_INDEX → AI_CONTEXT →
TASKS → READING_PROFILES → Retrieval → Template 선택 → 작업 수행 →
Vault 저장(`run_auto_save()`) → Validation → 완료 보고" 흐름과
지원 명령 예시("다음 Task 진행"/"M23-T05 진행"/"ADR 작성"/
"Bug Fix"/"Feature Design"/"API 설계")를 표로 명시했다.
[[EXECUTION_PROFILE]] 5~6단계(Document Update/Validation)도
`run_auto_save()`를 구체적으로 가리키도록 갱신.

## 구현 상태(M23-T07, Execution Environment Integration)

`tests/integration/test_m23_vault_environment_integration.py`
신규 — 실제 `Vault/`를 대상으로 (1) Filesystem 접근(디렉터리·
`PROJECT_INDEX.md` 존재 확인), (2) 실제 문서 트리 전체
`find_broken_backlinks()`가 알려진 프롬프트 예시 텍스트 외 새
문제가 없는지, (3) 실제 Vault 복사본 위에서 `run_auto_save()`
저장→검증 왕복이 성공하는지 확인한다. **검증 중 실제로
`EXECUTION_PROFILE.md`/`Backend Index.md`에서 줄바꿈 때문에 깨진
`[[..]]` Backlink 2건을 발견해 함께 고쳤다** — Validation 계층이
실제로 문제를 잡아낸 첫 사례. Obsidian MCP 실시간 연동은 범위
밖으로 유지(M23-Prep-T08 Optional). GitHub 연동은 M23-T01~T07
매 Task의 커밋·푸시로 이미 검증됨.

**Milestone 23(Obsidian Integration & Auto Save) 전체 완료
(T01~T07).**

## 관련 문서

- [[Architecture Overview]]
- [[ADR Index]]
- [[READING_PROFILES]]
- [[EXECUTION_PROFILE]]

## 원문

- `.ai/DECISIONS.md` (ADR-0035)
- `docs/ARCHITECTURE.md` (§3.21)
