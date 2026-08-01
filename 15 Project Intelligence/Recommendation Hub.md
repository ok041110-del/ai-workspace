---
tags: [architecture, recommendation]
type: concept
---

# Recommendation Hub

> Map of Content(Milestone 47, [[Map of Content Guide]]에서 제안,
> 이번에 실제 생성). Recommendation 파이프라인(M35→M42→M43→M36→M44)
> 이 만드는 산출물을 한 곳에서 연결한다 — 이 파이프라인의 3개 Vault
> 리포트가 서로 전혀 링크되지 않았던 문제([[Vault Information Architecture]] T01 §1.3)를 해결한다. 아래 리포트 파일은 **직접
> 수정하지 않는다** — 매번 재계산되어 덮어써지는 AI 생성 파일이다
> (`15 Project Intelligence/README.md` 규칙 그대로).

## Recommendation 파이프라인 5단계

| 단계 | Milestone | Vault 산출물 |
|---|---|---|
| 1. 판단 | M35 — Recommendation Intelligence | [[Recommendation Intelligence]] |
| 2. 조정 | M42 — Recommendation Adaptation | 별도 Vault 산출물 없음(Adjustment 결과는 3단계 흐름 제어 안에 포함) |
| 3. 흐름 제어 | M43 — Recommendation Orchestration | 별도 Vault 산출물 없음(`RecommendationOrchestrationService`가 아래 실행/설명 산출물을 만들어냄) |
| 4. 실행 | M36 — Execution | [[Recommendation Execution]] |
| 5. 설명 | M44 — Recommendation Explainability | [[Recommendation Explanation]] |

## 관련 Concept

- [[Recommendation]]
- [[Execution]]
- [[Memory]]

## 관련 문서

- [[Knowledge Hub]]
- [[Architecture Overview]]
- [[Experience Intelligence]]
