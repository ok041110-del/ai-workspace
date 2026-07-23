# AI Workspace

Claude Code, Codex, Gemini CLI와 같은 **AI 구현 엔진(Implementation Engine)**을
관리하는 **오케스트레이션 플랫폼**입니다.

AI Workspace는 또 하나의 코딩 AI가 아닙니다. 실제 코드 작성은 구현 엔진이
수행하고, AI Workspace는 다음을 관리하고 연결하는 역할을 담당합니다.

- 프로젝트 관리 (Project Management)
- Task 관리 (Task Management)
- Workflow 관리 (Workflow Orchestration)
- 장기 메모리 (Long-term Memory)
- 승인 (Approval)
- 자동화 (Automation)
- 다중 프로젝트 관리 (Multi Project)
- 구현 엔진(Claude Code, Codex 등) 관리

> **현재 상태**: Phase 0 (문서화 및 구조 설계) 진행 중입니다. 아직 애플리케이션
> 코드는 존재하지 않습니다. 자세한 계획은 [`docs/ROADMAP.md`](docs/ROADMAP.md)를
> 참고하세요.

## 시작 방법

Phase 0에서는 문서 체계만 존재하며, 실행 가능한 코드는 Phase 1부터 추가됩니다.
현재 시점에는 아래 문서를 순서대로 읽어보는 것을 권장합니다.

1. [`docs/PRD.md`](docs/PRD.md) — 이 프로젝트가 왜 필요한지, 무엇을 목표로 하는지
2. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — 전체 구조와 컴포넌트
3. [`docs/ROADMAP.md`](docs/ROADMAP.md) — Phase별 개발 계획
4. [`.ai/RULES.md`](.ai/RULES.md) — 이 저장소에서 작업할 때 지켜야 하는 규칙
5. [`.ai/TASKS.md`](.ai/TASKS.md) — 현재 진행 중인 Task와 전체 진행 상태

Phase 1부터는 이 섹션에 실제 설치/실행 방법이 추가될 예정입니다.

## 디렉터리 구조

```
ai-workspace/
├── README.md              # 프로젝트 소개 (본 문서)
├── docs/                   # 사람을 위한 제품/구조/계획 문서
│   ├── PRD.md              # 목표, 요구사항, 기능 목록, 성공 기준
│   ├── ARCHITECTURE.md     # 전체 구조, 컴포넌트, 데이터 흐름, 의존성 규칙
│   └── ROADMAP.md          # Phase 계획, 마일스톤, 우선순위
├── .ai/                     # AI 구현 엔진을 위한 운영 문서
│   ├── RULES.md            # AI 개발 규칙, 코딩 규칙, 작업 원칙
│   ├── TASKS.md            # 전체 Task, 진행 상태, 체크리스트
│   ├── MEMORY.md           # 프로젝트 장기 메모리, 중요한 결정, 컨텍스트
│   └── DECISIONS.md        # Architecture Decision Record (ADR)
├── workspace/               # 프로젝트별 실제 작업 공간 (Phase 1 이후 구체화)
└── tests/                   # 테스트 코드 (Phase 1 이후 구체화)
```

## 개발 철학

이 프로젝트는 다음 원칙을 따릅니다. 자세한 내용은 [`.ai/RULES.md`](.ai/RULES.md)를
참고하세요.

1. 모든 문서/설명/주석/커밋 메시지는 한국어로, 코드 식별자는 Python 표준에 따라
   영어로 작성한다.
2. Documentation First — 구현보다 문서를 먼저 작성한다.
3. Architecture First — 구현 전에 구조를 먼저 설계한다.
4. Task Driven Development — 항상 Task 단위로 개발한다.
5. One Task At A Time — 한 번에 하나의 Task만 수행한다.
6. Test Before Complete — Task 완료 전 반드시 테스트한다.
7. Approval Required — 아키텍처 변경/신규 기능/리팩토링/Phase 완료는 사용자
   승인 후 진행한다.
8. 항상 이유(선택 이유, 설계 이유, 장단점, 대안)를 설명한다.

## 문서 링크

| 문서 | 설명 |
|---|---|
| [docs/PRD.md](docs/PRD.md) | 제품 요구사항 정의서 |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | 아키텍처 설계 문서 |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Phase별 로드맵 |
| [.ai/RULES.md](.ai/RULES.md) | AI 개발 규칙 |
| [.ai/TASKS.md](.ai/TASKS.md) | Task 목록 및 진행 상태 |
| [.ai/MEMORY.md](.ai/MEMORY.md) | 장기 메모리 |
| [.ai/DECISIONS.md](.ai/DECISIONS.md) | 설계 결정 기록 (ADR) |
