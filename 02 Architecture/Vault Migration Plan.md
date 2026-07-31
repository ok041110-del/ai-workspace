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

## Phase 1 — Recommendation Hub 생성(다음 PR 후보)

- `15 Project Intelligence/Recommendation Hub.md` 신규 생성
  ([[Map of Content Guide]] 참고).
- 기존 3개 리포트(`Recommendation Intelligence.md`/`Recommendation
  Execution.md`/`Recommendation Explanation.md`)는 **수정하지
  않는다** — 이들은 매번 재계산되어 덮어써지는 AI 생성 파일이라
  수동 편집이 다음 실행 때 사라진다(§1.2 기존 규칙 재확인). Hub가
  단방향으로 이들을 가리킨다.
- 별도 승인 없이 진행 가능(신규 파일 추가뿐, 기존 파일 무변경).

## Phase 2 — Concept 문서 8종 생성(별도 제안·승인 필요)

§13.2/13.3의 8개 Domain Vocabulary(Intelligence/Memory/Execution/
Guardian/Adaptation/Orchestration/Explainability/Observability)를
`02 Architecture/Concepts/*.md`로 만든다. 내용은 `docs/
ARCHITECTURE.md` §13 정의를 요약 인용 + 원문 링크만 — 새로 쓰지
않는다. `Concept Index.md`(Hub)도 함께 생성.

**별도 승인이 필요한 이유**: 8개 신규 파일 + PROJECT_INDEX 재수정
+ 새 `type: concept` 값 도입이라 이번 Milestone 46 PR 하나에
묶기에는 검토 범위가 커진다 — Domain 정의를 요약하는 과정에서
미묘한 표현 차이가 §13 원문과 어긋날 위험을 사용자가 직접 확인하는
것이 안전하다.

## Phase 3 — Metadata(`type`) 점진 추가(Boy Scout Rule)

T01 기준 36/49 문서에 `type`이 없다. **일괄 추가하지 않는다** —
해당 문서를 다른 이유로 수정할 PR에서 `type` 필드를 함께 추가한다
(ADR-0057 Boy Scout Rule과 동일 절차, [[Metadata Standard]] 참고).
예외적으로 이번 Milestone에서 만드는 5개 신규 문서는 처음부터
`type: architecture`를 갖는다(Phase 0에 포함, 이미 완료).

## Phase 4 — Roadmap Hub 생성(별도 제안·승인 필요)

`01 Overview/Roadmap.md` 신규 — `docs/ROADMAP.md` 요약 + 링크.
`Overview.md`/`Milestones Index.md`와 상호 링크 추가. Phase 2와
마찬가지로 원문 요약의 정확성을 사용자가 확인해야 하므로 별도
승인.

## Phase 5 — Color Migration(Desktop 검증 대기, 이번에 실행 안 함)

[[Document Type Color Strategy#Color Migration 절차(적용은 보류)]]
참고 — `.obsidian/graph.json` 실제 수정은 Desktop 검증 완료 후
별도 트리거로만 진행한다.

## 요약 — 무엇이 "지금" 실행되고 무엇이 "제안만" 되는가

| Phase | 내용 | 이번 PR 포함 여부 |
|---|---|---|
| 0 | IA 문서 5개 생성 + PROJECT_INDEX 진입점 추가 | ✅ 포함 |
| 1 | Recommendation Hub 생성 | 제안만(다음 PR 후보, 별도 승인 불필요할 만큼 작음) |
| 2 | Concept 문서 8종 | 제안만(별도 승인 필요) |
| 3 | 기존 문서 `type` 점진 추가 | 제안만(Boy Scout Rule, 트리거 시 진행) |
| 4 | Roadmap Hub | 제안만(별도 승인 필요) |
| 5 | Color Migration 실제 적용 | 제안만(Desktop 검증 대기) |
