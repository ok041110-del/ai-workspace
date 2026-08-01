---
tags: [architecture, observability]
type: concept
---

# Observability (Concept)

> Evergreen Concept 문서(Milestone 47, [[Vault Information Architecture]]
> T02-6). 내용은 `docs/ARCHITECTURE.md` §13.3 정의를 그대로 요약
> 인용한다.

## 정의(§13.3, Behavioral Concept, ADR-0062)

Claude Code 세션 안에서 이미 계산된 값의 **존재 여부만** 실시간으로
반영하는 것 — Intelligence와 비슷하게 Read Only지만, 새로운 판단
(분석·요약)을 하지 않는다는 점이 다르다. §13.2 4개 핵심 Domain 중
어디에도 정확히 해당하지 않아 **Behavioral Concept**로 분류한다
(1급 Domain 승격 보류).

- **범위(Scope)**: `observability/` 패키지. StatusLine stdin JSON +
  `git`/`guardian.checker`/`VaultAdapter`/`.mcp.json`을 읽기 전용
  으로만 조회
- **대표 산출물**: `WorkspaceRuntimeSnapshot`, StatusLine 출력 문자열
  (Vault Node 아님 — 휘발성 표시)
- **대표 소비자**: 사람(Claude Code 세션 안에서 실시간 확인)

## 이 개념을 구현하는 Milestone

| Milestone | 책임 |
|---|---|
| M45 — Workspace Observability(Phase 1) | Claude Runtime + Recommendation 파이프라인 7단계를 StatusLine으로 반영 |
| M45 확장 | Git/Guardian/Vault/MCP 실행 환경까지 확장 관찰(Not Available 항목은 정직하게 표시) |

## 관련 문서

- [[Runtime Hub]]
- [[Runtime]]
- [[Guardian]]

## 원문

- `docs/ARCHITECTURE.md` §13.3(Observability 정의), §3.37~3.38(M45)
