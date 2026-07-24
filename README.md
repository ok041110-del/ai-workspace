# AI Workspace

Claude Code, Codex, Gemini CLI와 같은 **AI 구현 엔진(Implementation Engine)**을
**멀티 에이전트(Multi-Agent First)**로 오케스트레이션하는 플랫폼입니다.

AI Workspace는 또 하나의 코딩 AI가 아닙니다. 실제 코드 작성은 구현 엔진이
수행하고, AI Workspace는 역할을 가진 **Agent들의 협업**으로 다음을 관리하고
연결하는 역할을 담당합니다.

- 멀티 에이전트 협업 (Multi-Agent Orchestration) — 능력(Capability) 기반 Agent
  (Planning / Coding / Review / Documentation / Research / …)를 Agent Runtime이
  조율
- 프로젝트 관리 (Project Management)
- Task 관리 (Task Management)
- Workflow 관리 (협업 흐름 Orchestration)
- 장기 메모리 (Long-term Memory)
- 승인 (Approval)
- 자동화 (Automation)
- 다중 프로젝트 관리 (Multi Project)
- 구현 엔진(Claude Code, Codex 등) 관리

> **현재 상태**: Milestone 1 / Phase 1 진행 중입니다. Multi-Agent First 구조를
> Agent Runtime·Engine Runtime·Context Manager·Event Store·Interaction Layer·
> Mission→Workflow→Task→Step 계층까지 확정(ADR-0006~0019)했으며, 도메인 모델과
> 인터페이스 계약을 구현하는 중입니다. 자세한 계획은
> [`docs/ROADMAP.md`](docs/ROADMAP.md)와
> [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)를 참고하세요.

## 시작 방법

현재는 도메인 모델과 인터페이스 계약을 구현하는 단계(Phase 1)입니다. 아래
문서를 순서대로 읽어보는 것을 권장합니다.

1. [`docs/PRD.md`](docs/PRD.md) — 이 프로젝트가 왜 필요한지, 무엇을 목표로 하는지
2. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — 전체 구조와 컴포넌트 (Multi-Agent First)
3. [`docs/ROADMAP.md`](docs/ROADMAP.md) — Milestone/Phase별 개발 계획
4. [`.ai/RULES.md`](.ai/RULES.md) — 이 저장소에서 작업할 때 지켜야 하는 규칙
5. [`.ai/TASKS.md`](.ai/TASKS.md) — 현재 진행 중인 Task와 전체 진행 상태

테스트는 저장소 루트에서 `python3 -m pytest`로 실행합니다. 실제 설치/실행
방법은 CLI 진입점이 구현되면 이 섹션에 추가됩니다.

## 디렉터리 구조

```
ai-workspace/
├── README.md              # 프로젝트 소개 (본 문서)
├── pyproject.toml         # 패키지/테스트 설정
├── docs/                   # 사람을 위한 제품/구조/계획 문서
│   ├── PRD.md              # 목표, 요구사항, 기능 목록, 성공 기준
│   ├── ARCHITECTURE.md     # 전체 구조, 컴포넌트, 데이터 흐름, 의존성 규칙
│   └── ROADMAP.md          # Milestone/Phase 계획, 우선순위
├── .ai/                     # AI 운영 문서
│   ├── RULES.md            # AI 개발 규칙, 코딩 규칙, 작업 원칙
│   ├── TASKS.md            # 전체 Task, 진행 상태, 체크리스트
│   ├── MEMORY.md           # 프로젝트 장기 메모리, 중요한 결정, 컨텍스트
│   └── DECISIONS.md        # Architecture Decision Record (ADR)
├── src/ai_workspace/        # 애플리케이션 코드
│   ├── domain/             # Project, Mission, Workflow, Task, Step,
│   │                       #   WorkspaceSession, Agent 등 핵심 모델
│   ├── interfaces/          # 추상 계약 14종 (Repository, Engine, AgentRuntime, EventBus/Store 등)
│   ├── core/               # Workspace Core (최상위 오케스트레이터, WorkspaceSession)
│   ├── runtime/            # Agent Runtime (Registry/Scheduler/Manager) (이후 Phase)
│   ├── agents/             # 능력별 Agent (이후 Phase)
│   ├── engines/            # Core Engines 구현 (이후 Phase)
│   ├── events/             # Event Bus + Event Store (이후 Phase)
│   ├── interaction/         # Interaction Layer (이후 Phase)
│   ├── adapters/           # Engine Adapter 구현 (이후 Phase)
│   ├── storage/            # 파일 기반 저장소 구현
│   └── cli/                # CLI 진입점
├── workspace/               # 프로젝트별 실제 작업 공간 (이후 구체화)
└── tests/                   # 테스트 코드
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
