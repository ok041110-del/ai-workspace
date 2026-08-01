---
tags: [architecture, guardian]
type: concept
---

# Guardian (Concept)

> Evergreen Concept 문서(Milestone 47, [[Vault Information Architecture]]
> T02-6). 내용은 `docs/ARCHITECTURE.md` §13.2 정의를 그대로 요약
> 인용한다.

## 정의(§13.2, 핵심 4개 용어 중 하나, ADR-0056)

> Guardian owns the executable representation of architectural
> rules. Architecture documentation defines the rules; Guardian
> encodes them, evaluates conformance, and publishes architectural
> health.

규칙을 **정의하지 않는다** — §8이 여전히 규칙의 소유자다. 이미
선언된 규칙을 `ArchitectureRule`(순수 값 객체)로 인코딩하고, 소스
트리에 대해 평가(`checker.evaluate()`)해 결과를 공표한다.

- **범위(Scope)**: `guardian/` 패키지. 소스 트리(`src/ai_workspace`)
  를 읽기만 한다(Read Only). `VaultAdapter`(Presentation)만 의존
- **대표 산출물**: `ArchitectureHealthReport`, Vault Markdown
  ([[Architecture Guardian]])
- **대표 소비자**: 사람(Vault 열람), 기존 `pytest` 기반 boundary
  테스트

## 이 개념을 구현하는 Milestone

| Milestone | 책임 |
|---|---|
| M41 — Architecture Guardian | `tests/` 5곳에 중복됐던 `ast` 경계 검사를 `GUARDIAN_RULES`로 통합 |
| M45 확장 — Execution Environment Observability | `guardian.checker.evaluate()`를 StatusLine에서 재사용(재실행 없이) |

## 관련 문서

- [[Architecture Hub]]
- [[Architecture Overview]]
- [[Runtime]]

## 원문

- `docs/ARCHITECTURE.md` §13.2(Guardian 정의), §3.33(M41)
