---
tags: [architecture, memory]
type: concept
---

# Memory (Concept)

> Evergreen Concept 문서(Milestone 47, [[Vault Information Architecture]]
> T02-6). 내용은 `docs/ARCHITECTURE.md` §13.2 정의를 그대로 요약
> 인용한다.

## 정의(§13.2, 핵심 4개 용어 중 하나)

시스템이 무언가를 **저장하고 다시 꺼내 쓸 수 있게** 하는 계층.
판단(Learning)은 하지 않는다 — key-value 저장/검색만 담당한다
(`MemoryEngine.remember`/`recall`/`search`, M1). 무엇을 저장할지는
호출자가 결정한다.

- **범위(Scope)**: `memory/` 패키지. `MemoryEngine` interface(M1)와
  그 재사용 계층(`ContextManager`/`ExecutionMemoryStore`)
- **대표 산출물**: 저장된 key-value 레코드(Session/Mission Snapshot,
  `ExecutionMemory`)
- **대표 소비자**: Context Manager(Snapshot), Execution Platform
  (자기 실행 결과 기록, M39)

## 이 개념을 구현하는 Milestone

| Milestone | 책임 |
|---|---|
| M1 — Memory Engine | key-value 저장/검색 기본 계약 |
| M39 — Execution Memory | Execution 결과를 `ExecutionMemory`로 자동 기록 |
| M40 — Experience Intelligence | Memory에 쌓인 기록을 성공/실패로 집계(Read Only) |

## 관련 문서

- [[Recommendation Hub]]
- [[Architecture Overview]]
- [[Execution]]

## 원문

- `docs/ARCHITECTURE.md` §13.2(Memory 정의), §3.x(M1/M39/M40)
