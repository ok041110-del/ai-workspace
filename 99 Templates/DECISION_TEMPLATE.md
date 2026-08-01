---
tags: [system]
type: documentation
---

# DECISION_TEMPLATE

ADR로 승격하기엔 가벼운 판단(설계 회의 중 나온 "왜?"에 대한 답)을
기록할 때 쓴다. 결과물을 Vault [[Decisions Index]]에 항목으로
추가할 때는 이 구조를 그대로 옮기거나 [[Template - Decision]](개별
문서로 분리할 만큼 커진 경우)을 쓴다 — 이 템플릿은 판단 과정을
정리하는 용도이고, 최종 위치는 Vault다(GitHub 쪽 별도 원문 없음).

## 구조

```
### {{질문 — 예: "왜 X를 Y 방식으로 했는가"}}

- Status: 확정 | 미정 | 재검토 필요
- 질문: {{정확히 무엇이 애매했는가}}
- 답/현재 상태: {{결론 또는 아직 결론이 없다면 그 상태}}
- 관련 문서: {{[[ADR Index]] 등 근거가 되는 문서}}
```

## 사용 방법

1. 대화/설계 중 "왜?" 질문이 반복되면 이 구조로 즉시 기록한다 —
   ADR처럼 무겁게 만들지 않는다.
2. 나중에 이 판단이 구조적으로 중요해지면(예: 새 Interface로
   이어짐) [[ADR_TEMPLATE]]로 승격한다.
3. [[Decisions Index]]에 이 항목을 추가하고 Status를 정직하게
   기록한다("미정"도 유효한 상태다).

## 관련 문서

- [[Template - Decision]]
- [[Decisions Index]]
- [[ADR_TEMPLATE]]

## 원문

- 없음(Vault 전용 — 결정이 공식화되면 `.ai/DECISIONS.md`의 ADR로
  이동한다)
