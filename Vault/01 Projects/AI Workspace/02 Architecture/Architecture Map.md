---
tags: [architecture]
---

# Architecture Map

> [[Architecture Overview]]의 요약을 읽은 뒤, 특정 영역을 더 깊이
> 봐야 할 때 이 지도를 통해 이동한다. AI Reading Rule([[AI_RULES]])
> 대로 필요한 노드만 열어본다.

```
Overview
   │
   ▼
Architecture Overview
   │
   ├── Backend Index ──────► API Catalog
   │
   ├── Dashboard Index
   ├── Automation Index
   ├── Production Index
   │
   ├── iOS Design (M23, 설계만)
   ├── Android Placeholder (M23)
   │
   ├── ADR Index ──────────► (개별 ADR 필요 시 GitHub 원문)
   └── Milestones Index
```

## 영역별 진입점

| 영역 | 진입 문서 |
|---|---|
| 서버 전체 구조 | [[Architecture Overview]] |
| Backend/Engine 구현 | [[Backend Index]] |
| REST/WebSocket API | [[API Catalog]] |
| 실시간 상태 조회 | [[Dashboard Index]] |
| 자동 실행 규칙 | [[Automation Index]] |
| 운영(설정/생명주기/상태) | [[Production Index]] |
| 의사결정 이력 | [[ADR Index]], [[Decisions Index]] |
| Milestone 이력 | [[Milestones Index]] |
| Mobile(M23) | [[iOS Design]], [[Android Placeholder]] |

## 관련 문서

- [[Architecture Overview]]
- [[Overview]]

## 원문

- docs/ARCHITECTURE.md
