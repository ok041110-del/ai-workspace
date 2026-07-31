---
tags: [architecture]
type: architecture
---

# Document Type Color Strategy

> [[Vault Information Architecture]] T02-7의 상세. 기존 Graph Color
> 문제(폴더 경로 기준)를 Document Type 기준으로 재설계한다. **이
> 문서는 설계(Design)만 다룬다 — `.obsidian/graph.json`은 이번
> Milestone에서 수정하지 않는다**(Desktop 검증 대기 동결 유지,
> [[Vault Information Architecture#1.4 Graph View 설정(`.obsidian/graph.json`)]]
> 참고).

## 관련 문서

- [[Vault Information Architecture]]
- [[Metadata Standard]]

---

## 현재 문제(T01 실측)

`.obsidian/graph.json`의 6개 `colorGroups`는 전부 `path:"..."`(폴더
경로 또는 파일명 문자열) 기준이다. 예: `path:"02 Architecture" OR
path:"03 ADR" OR path:"11 Milestones" OR path:"12 Decisions" OR
path:"04 Backend" OR path:"05 API" OR path:"08 Production"`가 한
색으로 묶여 있다 — Architecture 문서와 ADR과 Milestone과 API
Catalog가 "성격이 전혀 다른데도" 같은 색이다.

## §14(ADR-0054)와의 관계 — 재사용, 폐기 아님

`docs/ARCHITECTURE.md` §14.2는 이미 **Domain 기반** 6-Cluster
(Intelligence/Execution/Memory/Architecture/Domain/Documentation)를
정의해뒀다. 이 Milestone은 그 축을 없애지 않는다 — 대신 **Document
Type이라는 새 1차 축을 추가**하고, Domain Cluster는 "같은 Document
Type 안에서 더 세분화하고 싶을 때" 쓰는 2차 참고 자료로 격을
낮춘다. 이유: 실제 T01 문제(§14가 못 잡아낸 것)는 "ADR과 Milestone
과 API Catalog가 같은 색"이라는 Document Type 혼동이지, Domain
혼동이 아니다.

## Document Type Color Palette(제안)

| Document Type | 색(제안) | 근거 |
|---|---|---|
| Architecture | 보라(Purple) | §14.2가 이미 Architecture=Purple로 정의 — 그대로 재사용(신규 발명 금지) |
| ADR | 진보라(Deep Purple, Architecture와 구분되는 인접색) | Architecture와 개념적으로 가깝지만(결정↔구조) Node 성격이 다름(ADR은 시점 고정 결정, Architecture는 현재 상태) — 인접색으로 관계는 유지하되 구분 |
| Milestone | 남색(Indigo) | ADR과 같은 "결정 기록" 계열이지만 시간 축(진행 이력)이 강함 — ADR보다 시간성이 강조되는 색 계열 선택 |
| Decision(비공식) | 연보라(Light Purple) | ADR의 가벼운 버전이라는 §1.2의 의도적 위계를 색 명도로 표현(ADR보다 옅게) |
| Concept(Evergreen) | 청록(Teal) | Milestone/시간과 무관하다는 성격을 Architecture 계열(보라)과 확실히 구분되는 색으로 표현 — "영구히 남는 것"이라는 의미 부여 |
| Project Intelligence(생성 리포트) | 파랑(Blue) | §14.2의 기존 Intelligence=Blue를 그대로 재사용 |
| Execution 계열(Recommendation Execution 등) | 초록(Green) | §14.2의 기존 Execution=Green을 그대로 재사용 |
| Automation | 주황(Orange) | §14.2 Documentation=Orange와 계열은 같지만, Automation은 "운영 절차 문서"라는 점에서 재사용 — 신규 색 최소화 |
| Memory | 노랑(Yellow) | §14.2의 기존 Memory=Yellow를 그대로 재사용 |
| Runtime(Observability) | 회색(Gray) | 아직 Vault Node가 없어(T01/T03) 배정만 해 두고 실사용은 없음 — "휘발성/비영속" 성격을 무채색으로 표현 |
| System/Documentation | 주황(Orange) | §14.2의 기존 Documentation=Orange를 그대로 재사용(System 문서도 이 계열로 통합 — 별도 색 신설 안 함) |

**색 선택 원칙**: 이미 §14.2가 정의한 색(Intelligence=Blue/
Execution=Green/Memory=Yellow/Architecture=Purple/Documentation=
Orange)은 전부 그대로 재사용한다. 신규 색은 Document Type이
§14.2에 없던 경우(ADR/Milestone/Decision/Concept)에만 Purple
계열의 명도·색상 변주로 최소 추가한다 — 완전히 새로운 색상 팔레트를
발명하지 않는다(Vocabulary Reuse First와 동일 정신을 색상에도
적용).

## Color Migration 절차(적용은 보류)

1. **지금(Milestone 46)**: 팔레트 설계 + Frontmatter `type` 표준
   정의(→ [[Metadata Standard]])까지만 완료.
2. **Desktop 검증 완료 후(별도 트리거)**: 사용자가 실제 Desktop
   Obsidian에서 Graph Groups 렌더링을 확인 — 이번 Milestone이 새로
   만드는 정보가 아니라 이미 존재하던 Pending Verification 절차를
   그대로 따른다.
3. **검증 통과 시**: `.obsidian/graph.json`의 `colorGroups`를
   `path:"..."` 대신 `tag:"#type/adr"` 같은 태그 기반(또는 Obsidian
   버전이 지원하면 Property 기반) 쿼리로 교체 — 이때 [[Metadata Standard]]
   의 `type` 필드가 이미 채워져 있어야 하므로, [[Vault Migration Plan]]
   의 Metadata 추가 단계가 선행돼야 한다.
4. **검증 실패 시**: 기존 6-Cluster(§14.2, 경로 기준) 그대로
   유지하고 이 문서는 설계 참고 자료로만 남는다 — graph.json을
   다시 임의로 건드리지 않는다(기존 동결 원칙 유지).
