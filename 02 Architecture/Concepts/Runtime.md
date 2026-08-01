---
tags: [architecture, observability]
type: concept
---

# Runtime (Concept)

> Evergreen Concept 문서(Milestone 47, [[Vault Information Architecture]]
> T02-6). "Runtime"은 Observability가 관찰하는 **대상**(Claude Code
> 세션 상태 + 실행 환경 상태)을 가리키는 보조 개념이다 — Observability
> (관찰 행위) 자체와는 구분한다. 실시간 값 자체는 Vault Node로
> 존재하지 않는다(M46 T03 Node Definition 결정 — 휘발성, 영속 문서
> 아님) — 이 문서는 그 **범주**만 정의한다.

## 정의

Runtime은 두 축으로 구성된다(§3.37~3.38, ADR-0062/ADR-0063).

1. **AI Workspace Runtime**: Claude Code 자체 상태(Model/Effort/
   Context 사용량) + Recommendation 파이프라인 7단계
   (Recommendation→Adaptation→Explainability→Orchestration→
   Execution→Memory→Experience)의 관찰 가능 여부
2. **Execution Environment**: Git(브랜치/dirty 여부/ahead-behind),
   Guardian(아키텍처 준수), Vault(최신 문서 상태), MCP(연결 상태)

관측 불가능한 값(`ruff`/`mypy`/Coverage 실시간 상태, MCP 상세 호출
이력, GitHub PR 상태, 현재 실행 중인 Task)은 추정하지 않고 정직하게
Not Available로 표시한다는 원칙이 이 범주 전체에 적용된다.

## 이 개념을 구현하는 Milestone

| Milestone | 책임 |
|---|---|
| M45 — Workspace Observability | AI Workspace Runtime 관찰(Phase 1) |
| M45 확장 | Execution Environment Runtime 관찰 |

## 관련 문서

- [[Runtime Hub]]
- [[Observability]]
- [[Guardian]]

## 원문

- `docs/ARCHITECTURE.md` §3.37~3.38
