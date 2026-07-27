---
tags: [system]
---

# ADR_TEMPLATE

GitHub `.ai/DECISIONS.md`에 **새 ADR 원문**을 작성할 때 이 구조를
쓴다. Vault에 그 ADR의 3줄 요약을 남길 때는(전문을 복사하지 않고)
[[Template - ADR Summary]]를 대신 쓴다 — 이 템플릿은 원문 작성용,
그것은 Vault Index 등록용으로 역할이 다르다.

## 구조(`.ai/DECISIONS.md` 실제 ADR 형식)

```markdown
## ADR-{{number}}: {{title}}

- 상태: 승인됨 ({{날짜}}, 사용자 지시로 확정)
- 날짜: {{날짜}}
- 배경: {{왜 이 결정이 필요했는가}}
- 결정: {{무엇을 하기로 했는가}}
- 대안:
  - {{기각한 대안 1}} — {{기각 이유}} (기각).
- 이유: {{왜 이 결정이 대안보다 나은가}}
- 결과/영향: {{코드/문서/향후 작업에 미치는 영향}}
```

## 사용 방법

1. 새 최상위 Interface를 추가하거나, Interface 추가 없이도 사용자가
   명시적으로 ADR 작성을 요청한 경우에만 쓴다(기존 원칙 유지).
2. ADR 원문을 `.ai/DECISIONS.md`에 작성한 뒤, Vault
   [[ADR Index]]에 [[Template - ADR Summary]] 형식으로 3줄 요약
   (목적/결정/영향)을 추가한다 — 전문을 Vault에 복사하지 않는다.

## 관련 문서

- [[Template - ADR Summary]]
- [[ADR Index]]
- [[IMPLEMENTATION_TEMPLATE]]

## 원문

- `.ai/DECISIONS.md`
