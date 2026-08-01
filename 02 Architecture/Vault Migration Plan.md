---
tags: [architecture]
type: architecture
---

# Vault Migration Plan

> [[Vault Information Architecture]] T04의 상세. 기존 문서를
> **삭제하지 않는다** — Rename/Move/Metadata 추가/Wiki Link 추가/
> MOC 생성만 제안한다. Backward Compatibility를 최대한 유지한다
> (사용자 조건, Milestone 46).

## 관련 문서

- [[Vault Information Architecture]]
- [[Metadata Standard]]
- [[Document Type Color Strategy]]
- [[Map of Content Guide]]

---

## 원칙

- 기존 파일 **삭제 0건**.
- 기존 [[WikiLink]]를 깨는 Rename **0건**(Rename이 필요하면 Obsidian
  의 자동 링크 갱신 기능을 전제로 하고, 이번 Milestone에서는
  Rename 자체를 제안하지 않는다 — 전부 "추가"만 제안).
  실행 시점에 실제로 Rename이 필요한 항목이 나오면 별도 승인.
- **모든 변경은 이번 Milestone에서 즉시 실행하지 않는다** — 이
  문서는 Proposal이다. 실제 실행은 T04 DoD("Migration Plan 완료")
  가 요구하는 "계획 수립"까지이며, 대규모 일괄 편집 자체는 Boy
  Scout Rule(ADR-0057 정신)과 동일하게 **후속 Milestone/PR에서
  실제로 그 문서를 건드릴 때 점진 적용**한다.

## Phase 0 — 이번 Milestone에서 실제로 생성하는 것(즉시 실행)

이번 PR로 아래 5개 신규 문서만 생성한다(기존 파일 무변경):

1. `02 Architecture/Vault Information Architecture.md`
2. `02 Architecture/Metadata Standard.md`
3. `02 Architecture/Document Type Color Strategy.md`
4. `02 Architecture/Map of Content Guide.md`
5. `02 Architecture/Vault Migration Plan.md`(이 문서)

`00 System/PROJECT_INDEX.md`에 위 5개 문서로 가는 진입점 1줄을
추가한다(기존 구조·순서 변경 없음, 항목 추가만).

## Phase 1 — Recommendation Hub 생성 ✅ 완료(Milestone 47)

- `15 Project Intelligence/Recommendation Hub.md` 생성 완료.
- 기존 리포트(`Recommendation Intelligence.md`/`Recommendation
  Execution.md`/`Recommendation Explanation.md`)는 **수정하지
  않았다** — 이들은 매번 재계산되어 덮어써지는 AI 생성 파일이라
  수동 편집이 다음 실행 때 사라진다(§1.2 기존 규칙 재확인). Hub가
  단방향으로 이들을 가리킨다.

## Phase 2 — Concept 문서 생성 ✅ 완료(Milestone 47, 7종)

`02 Architecture/Concepts/*.md` 7개 생성: Recommendation/Execution/
Memory/Guardian/Observability/Automation/Runtime. `Concept
Index.md`(Hub)도 함께 생성. 내용은 `docs/ARCHITECTURE.md` §13 정의를
요약 인용만 하고 새로 쓰지 않았다. **Adaptation/Orchestration/
Explainability는 별도 Concept으로 만들지 않았다** — Recommendation
파이프라인의 단계일 뿐 독립된 Domain Vocabulary가 아니므로
[[Recommendation Hub]]에서 흐름으로 표현한다(M46이 열거한 8종
전부를 기계적으로 만들지 않고, 실제 재사용 가치를 판단해 7종으로
정리).

## Phase 3 — Metadata(`type`) 백필 ✅ 완료(Milestone 47, 전수 적용)

M46 T04는 이 Phase를 Boy Scout Rule(점진 적용)로 남겼으나, M47은
사용자가 "Metadata Backfill 완료"를 DoD로 명시해 **전수 백필로
승격**했다 — 기존 36개 문서 전부에 `type`을 추가해 54/54(100%)
커버리지를 달성했다(스크립트 기반 일괄 처리, 각 문서의 실제 성격에
따라 [[Metadata Standard]]의 Document Type 표를 그대로 적용 —
04 Backend~10 Android/99 Templates류는 `documentation`으로 통일).

## Phase 4 — Roadmap Hub 생성(계속 보류, 이번 범위 아님)

`01 Overview/Roadmap.md` 신규 — `docs/ROADMAP.md` 요약 + 링크.
`Overview.md`/`Milestones Index.md`와 상호 링크 추가. Phase 2와
마찬가지로 원문 요약의 정확성을 사용자가 확인해야 하므로 별도
승인.

## Phase 5 — Color Migration(계속 Pending, Desktop 검증 대기)

[[Document Type Color Strategy#Color Migration 절차(적용은 보류)]]
참고 — `.obsidian/graph.json` 실제 수정은 Milestone 47에서도
**하지 않는다**. 2026-07-30 사용자 결정으로 동결된 Pending
Verification 상태가 그대로 유지된다 — 이번 Migration으로 Desktop
검증이 필요 없어지는 것이 아니라, 검증이 풀리는 즉시 [[Metadata Standard]]의 `type` 필드(이미 54/54 완료)를 그대로 태그 기반 Color
쿼리에 쓸 수 있는 상태로 대비를 마쳤다는 의미다.

## Migration 검증(Milestone 47)

Graph View 자체(Desktop UI)는 검증할 수 없지만, Graph의 **구조적
근거**(Metadata + Wiki Link)는 스크립트로 실측 검증했다.

| 지표 | M46 이전 | M47 이후 |
|---|---|---|
| `type` Frontmatter 커버리지 | 13/49(27%) | 54/54(100%) |
| Orphan 문서(0 backlink) | 4 | 3(전부 사용법 안내 README) |
| Recommendation 파이프라인 리포트의 inbound 링크 | 0건(6개 리포트 전부) | 1~4건씩(Recommendation Hub 경유) |
| Concept 문서 | 0 | 7 |
| Hub(MOC) 문서 | 4(비공식, 이름 없음) | 9(4개 재확인 + 5개 신규: Recommendation/Architecture/Runtime/Knowledge/Decision Hub) |
| `find_broken_backlinks()` 미확인 오류 | 0(당시 기준) | 0(신규 문서 전수 검증 통과) |
| Vault Content Directory | 16종 | 17종(`16 Lessons` 추가) |

`.obsidian/graph.json` 실제 색상 적용은 이 표에 포함되지 않는다 —
Desktop 검증 완료 후 별도로 검증한다(Phase 5).

## 요약 — 무엇이 "지금" 실행되고 무엇이 "제안만" 되는가

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | IA 문서 5개 생성 + PROJECT_INDEX 진입점 추가 | ✅ 완료(Milestone 46) |
| 1 | Recommendation Hub 생성 | ✅ 완료(Milestone 47) |
| 2 | Concept 문서 7종 + Concept Index | ✅ 완료(Milestone 47) |
| 3 | 기존 문서 `type` 전수 백필 | ✅ 완료(Milestone 47) |
| 4 | Roadmap Hub | 제안만(이번 범위 아님, 별도 승인 필요) |
| 5 | Color Migration 실제 적용 | Pending(Desktop 검증 대기, 계속 보류) |
