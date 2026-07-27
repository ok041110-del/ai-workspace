---
tags: [system]
---

# AI_RULES

이 Vault를 다루는(읽는/쓰는) 모든 AI와 사람이 지켜야 하는 규칙.

## 이 Vault가 아닌 것

- 코드 저장소가 아니다 — Python/Swift 코드나 테스트 코드를 저장하지
  않는다.
- GitHub를 대체하지 않는다.
- GitHub 문서를 수정하지 않는다(이 Vault의 문서를 고쳐도 GitHub의
  `docs/ARCHITECTURE.md` 등은 전혀 바뀌지 않는다 — 반대 방향으로
  동기화되는 장치도 없다).
- GitHub 문서를 복사하지 않는다 — ADR 전문, Architecture 전문을
  그대로 붙여넣지 않는다.

## 이 Vault가 하는 것

- 원문 대신 **요약 + 링크**를 제공한다.
- AI의 장기 메모리(Long-term Memory) 역할을 한다 — 매번 GitHub
  전체를 다시 읽지 않고, 이 Vault의 압축된 Index만 읽고도 맥락을
  파악할 수 있게 한다.

## Backlink Rule

모든 문서는 관련 문서를 `[[이중 대괄호]]` 링크로 적극적으로
연결한다. 예:

```
[[Architecture Overview]]
[[Automation Index]]
[[Dashboard Index]]
[[Production Index]]
[[ADR Index]]
[[API Catalog]]
[[Milestones Index]]
```

새 문서를 쓸 때 관련된 기존 문서 최소 1개 이상을 backlink로 건다.
관련 문서가 없으면(예: 완전히 새 영역) [[Overview]]에 연결한다.

## Tag Rule

문서 상단 frontmatter에 아래 태그 중 해당하는 것을 붙인다.

```
#backend
#ios
#android
#dashboard
#automation
#production
#architecture
#decision
#api
#milestone
#system
```

한 문서에 여러 태그를 붙여도 된다(예: Dashboard API 문서는
`#dashboard #api`).

## GitHub Link Rule

Index 성격의 문서는 **마지막 섹션**에 반드시 "원문"을 둔다. 예:

```markdown
## 원문

- docs/ARCHITECTURE.md
- docs/ROADMAP.md
- docs/PRD.md
- .ai/DECISIONS.md (ADR-0034)
```

경로만 적고 URL 전체를 매번 쓰지 않는다(저장소가 이동해도 깨지지
않도록) — 필요하면 저장소 루트 기준 상대 경로로 표기한다.

## AI Reading Rule

AI는 Vault 전체를 읽지 않는다. 작업별로 최소 문서만 읽는다.

예: "Dashboard 코드를 수정해야 한다"

```
[[Overview]] → [[Architecture Overview]] → [[Dashboard Index]]
  → [[API Catalog]](관련 엔드포인트만) → 필요하면 GitHub 원문
  (예: src/ai_workspace/runtime/dashboard/dashboard_service.py)
```

Vault 문서를 읽고도 판단이 서지 않으면(예: 정확한 필드명, 정확한
함수 시그니처) 반드시 GitHub 원문을 확인한다 — 이 Vault의 요약은
근사치이지 계약(Contract)이 아니다.

## Context Retrieval Rule(Retrieval First)

작업을 시작하기 전, GitHub 전체를 다시 훑거나 코드베이스를 처음부터
탐색하지 않는다. 항상 [[PROJECT_INDEX]]의 라우팅 표에서 작업과 가장
가까운 문서를 먼저 찾고, 그 문서(들)만 읽은 뒤에도 판단이 서지
않을 때만 GitHub 원문으로 내려간다(AI Reading Rule과 동일한 순서,
[[PROJECT_INDEX]]가 그 진입점을 표로 명시한 것뿐이다). 이미 같은
세션에서 읽은 문서는 다시 읽지 않는다.

## Prompt Rules(Short Prompt Workflow)

- 문서 내용을 프롬프트에 다시 붙여넣지 않는다 — 문서 제목(`[[링크]]`
  형태)이나 경로만 언급한다.
- 새 설계를 요청/작성할 때는 자유 서술 대신 [[DESIGN_TEMPLATE]]의
  섹션 구조를 따른다(Template First).
- 반복되는 요청 패턴(새 Milestone 시작/버그 수정/문서 갱신 등)은
  [[PROMPT_PROFILE]]에 정리된 짧은 형식을 우선 사용한다.
- 자세한 예시는 [[PROMPT_PROFILE]] 참고.

## 관련 문서

- [[PROJECT_INDEX]]
- [[PROMPT_PROFILE]]
- [[AI_CONTEXT]]
- [[Overview]]

## 원문

- 없음(이 문서 자체가 이 Vault의 운영 규칙이다)
