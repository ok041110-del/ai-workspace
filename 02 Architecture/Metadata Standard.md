---
tags: [architecture]
type: architecture
---

# Metadata Standard

> [[Vault Information Architecture]] T02-4/T03의 Metadata Standard
> 상세. 최소 Metadata 원칙(사용자 조건, Milestone 46) — 과도한
> 필드를 추가하지 않는다.

## 관련 문서

- [[Vault Information Architecture]]
- [[Document Type Color Strategy]]

---

## Frontmatter 표준(4개 필드만)

| 필드 | 필수 여부 | 값 | 목적 |
|---|---|---|---|
| `type` | **필수**(신규 문서), 기존 문서는 [[Vault Migration Plan]] Phase에 따라 점진 추가 | [[Document Type Color Strategy]]의 Document Type 목록 중 1개 | Graph Color, 향후 Dataview 질의의 기준 축 |
| `tags` | 필수(기존과 동일, 이미 100% 커버리지) | §13.2/13.3 Domain Vocabulary(Intelligence/Memory/Execution/Guardian/Adaptation/Orchestration/Explainability/Observability) 중 0개 이상 + 구조적 태그(`system`/`architecture`/`concept`) | Domain 축 — T01에서 확인한 "1회성 Tag" 재발 방지를 위해 **자유 Tag 신설 금지** |
| `project` | 선택 | Milestone 번호(예: `M44`) | 어느 Milestone에서 만들어졌는지(Concept 문서처럼 Milestone 무관 문서는 생략) |
| `related` | 선택 | Wiki Link 배열 | Frontmatter 안에서 명시적 관계를 선언하고 싶을 때만(대부분은 본문 "관련 문서" 절로 충분 — 중복 방지) |

**기각한 필드**(Graphify 원안에는 있으나 채택하지 않음): `status`/
`priority`/`owner`/`reviewed`/`created`/`updated`/`version` — 전부
GitHub(`.ai/TASKS.md`/`.ai/DECISIONS.md`)에 이미 있는 원본을
Vault에서 중복 관리하게 만든다. Vault는 파생 뷰라는 기존 원칙(§9)
을 지킨다.

## `type` 값 목록(Document Type)

[[Document Type Color Strategy]]의 팔레트와 1:1 대응한다.

| `type` 값 | 대상 |
|---|---|
| `architecture` | `02 Architecture/*` |
| `adr` | ADR 관련 문서(`ADR Index.md` 포함) |
| `decision` | `12 Decisions/Decisions Index.md` |
| `milestone` | `Milestones Index.md` |
| `concept` | Evergreen Concept 문서(신규, T02-6) |
| `project-intelligence` | `15 Project Intelligence/*`(이미 세분화된 값 사용 중인 문서는 유지 — 마이그레이션 강제 안 함, [[Vault Migration Plan]] 참고) |
| `runtime` | Observability 관련(현재 Vault Node 없음, 향후 대비만) |
| `automation` | `07 Automation/*` |
| `task` | `14 Tasks/*`(설계는 있으나 아직 실제 문서 없음) |
| `system` | `00 System/*` |
| `documentation` | README/Overview/Template류 |

## Project / Label / Tag 재정의(T02-5)

- **Project = Milestone**: Graphify의 "Project" 개념을 새로 만들지
  않고 이 저장소의 기존 `Milestone`(§13.4)과 동일시한다.
- **Label = Domain Vocabulary**: §13.2/13.3의 8개 어휘를 그대로
  Label(Tag)로 재사용한다 — 신규 Label 발명 금지(§1.5 Vocabulary
  Reuse First와 동일 정신).
- **Tag 신설 절차**: 새 Domain Vocabulary가 §13에 추가될 때만 그와
  동일한 이름의 Tag가 자동으로 허용된다. Tag만 먼저 만들고 §13에
  나중에 반영하는 순서는 금지(선후관계 고정).

## 이번에 기존 문서를 일괄 수정하지 않는 이유

T01 실측 기준 36/49 문서에 `type`이 없다. 49개를 한 번에 고치는
것은 "Information Architecture 설계"가 아니라 "대규모 일괄
편집"이며, Boy Scout Rule(ADR-0057 정신)과 동일하게 **실제로 그
문서를 건드릴 이유가 생겼을 때 함께 추가**하는 점진적 적용을
원칙으로 한다. 상세 순서는 [[Vault Migration Plan]] 참고.
