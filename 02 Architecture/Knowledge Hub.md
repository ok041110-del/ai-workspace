---
tags: [architecture]
type: concept
---

# Knowledge Hub

> Map of Content(Milestone 47) — Vault 전체 Knowledge Graph의
> 최상위 진입점. [[PROJECT_INDEX]]가 "무엇을 읽어야 하는가"의
> Router라면, 이 문서는 "이 Vault에 어떤 Hub들이 있는가"의 지도다.

## Hub 목록

| Hub | 다루는 것 |
|---|---|
| [[Architecture Hub]] | 구조/Concept/설계 표준/Guardian 평가 |
| [[Recommendation Hub]] | Recommendation 파이프라인(M35~M44) 산출물 |
| [[Runtime Hub]] | Observability/Runtime(M45) |
| [[Decision Hub]] | ADR/Decision/Milestone 결정 기록 |

## Concept Index

- [[Concept Index]] — Recommendation/Execution/Memory/Guardian/
  Observability/Automation/Runtime 7종 Evergreen 문서

## Knowledge Graph 원칙([[Vault Information Architecture]] T02)

1. GitHub 원문을 대표하는 얇은 Vault Node + Wiki Link(순수 Graphify
   전체 Node화는 기각)
2. Index→Hub→개별 Node 계층 탐색(완전 연결 그래프 금지, §14.4)
3. Document Type이 Graph Color의 1차 축([[Document Type Color Strategy]])

## 관련 문서

- [[PROJECT_INDEX]]
- [[Architecture Overview]]
