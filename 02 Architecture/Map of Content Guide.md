---
tags: [architecture]
type: architecture
---

# Map of Content Guide

> [[Vault Information Architecture]] T02-2의 상세. MOC(Map of
> Content)는 Graphify/Second Brain의 핵심 개념 — "여러 Node를 주제로
> 묶어 보여주는 진입점"이다. 이 저장소에 이미 존재하는 성공 패턴
> (`00 System/PROJECT_INDEX.md`)을 공식화하고 확장한다.

## 관련 문서

- [[Vault Information Architecture]]
- [[Metadata Standard]]

---

## 이미 존재하는 MOC(재확인만, 신규 아님)

| MOC | 현재 상태 | 이번 변경 |
|---|---|---|
| `00 System/PROJECT_INDEX.md` | 이미 Vault 전체 진입점, backlink 2위(45) | 변경 없음 — 이미 최선의 형태 |
| `02 Architecture/Architecture Overview.md` | backlink 1위(62) | Architecture Hub로 역할 명명(내용 변경 없음) |
| `03 ADR/ADR Index.md` | backlink 3위(36) | ADR Hub로 역할 명명(내용 변경 없음) |
| `11 Milestones/Milestones Index.md` | backlink 6위(27) | Milestone Hub로 역할 명명(내용 변경 없음) |

이 4개는 이미 Hub 역할을 하고 있었다 — "MOC"라는 이름이 없었을
뿐이다. 이번 Milestone은 이 사실을 문서화하는 것으로 충분하고,
구조를 다시 만들 필요가 없다(Reuse First).

## 신규 제안 — Recommendation Hub

**문제(T01 §1.3)**: `Recommendation Intelligence.md`/`Recommendation
Execution.md`/`Recommendation Explanation.md`(M35/M36/M44가 만드는
3개 리포트)가 서로 전혀 링크되지 않는다 — Adaptation(M42)/
Orchestration(M43)은 별도 Vault 산출물조차 없다. 하지만 이 5개
Milestone은 하나의 파이프라인(§3.34~3.36)이다.

**제안**: `15 Project Intelligence/Recommendation Hub.md`(신규,
[[Vault Migration Plan]] Phase 1에서 생성) — Recommendation 파이프
라인 5단계(M35→M42→M43→M36→M44)를 순서대로 나열하고 각 단계의
Vault Node(있는 것만)를 [[WikiLink]]로 연결한다. 리포트 3개의
Frontmatter는 그대로 두고(자동 생성 파일 수정 금지 원칙 유지), Hub
문서만 신규로 추가한다 — 기존 파일 수정 0건.

## 신규 제안 — Concept Hub

**문제**: §13.2/13.3의 8개 Domain Vocabulary가 Vault에 전혀 존재하지
않는다(T01 §1.6-7). 개별 Concept 문서(T02-6)를 만들면 이들을 한
곳에서 찾을 수 있는 진입점도 필요하다.

**제안**: `02 Architecture/Concepts/Concept Index.md`(신규) — 8개
Concept 문서를 한 줄 요약과 함께 나열. `PROJECT_INDEX.md`에서
"Domain Vocabulary가 궁금하면 여기" 1줄만 추가해 연결한다(기존
PROJECT_INDEX 구조는 유지, 항목만 추가).

## 신규 제안 — Roadmap Hub

**문제**: `docs/ROADMAP.md`(GitHub 원문)를 가리키는 Vault Node가
없다 — 전체 로드맵을 Vault 안에서 조망할 진입점이 없다.

**제안**: `01 Overview/Roadmap.md`(신규, 얇은 포인터 문서) —
`docs/ROADMAP.md` 요약 3~5줄 + "원문" 링크(GitHub Link Rule, §9
원칙 재사용, 신규 규칙 아님). Milestone Hub와 상호 링크.

## MOC 설계 원칙(공통)

1. **Hub는 원본을 복제하지 않는다** — 요약 + Wiki Link 나열만.
2. **Hub 자체도 Frontmatter `type: architecture`(또는 해당 Type)를
   가진 일반 Node다** — MOC라고 특별 취급하지 않는다(Graphify는
   MOC를 별도 Node 타입으로 정의하지만, 이 저장소는 최소 Metadata
   원칙상 **기각** — 기존 `type` 값 재사용으로 충분).
3. **§14.4 Linking Rules(완전 연결 그래프 금지)를 그대로 적용** —
   Hub도 관련된 것만 링크하지, 해당 Domain의 모든 문서를 나열하지
   않는다.
