# ARCHITECTURE — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.6.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft (Milestone 1 / Phase 1 — 아키텍처 확정, 구현 재개 대기) |

이 문서는 `docs/PRD.md`에 정의된 요구사항을 바탕으로 AI Workspace의 구조를 설계한다.
실제 구현이 진행됨에 따라 이 문서와 실제 구조가 항상 일치하도록 갱신한다
(Documentation First 원칙).

> **v0.6.0 변경 사항 (안정화 보완 — ADR-0016 ~ ADR-0019)**
> v0.5.0 구조에 장기 확장을 위한 네 가지 보완을 반영했다.
> 1. **Engine Runtime 계층**을 Agent Runtime과 Engine Adapter 사이에 추가했다.
>    엔진 선택·세션 풀 관리·병렬 실행을 담당한다 (ADR-0016).
> 2. **Context Manager**를 도입해 **Memory Snapshot 관리 역할을 분리**했다.
>    Memory Engine은 저장/검색만, Context Manager는 Context 조립과 Snapshot
>    생명주기를 담당한다 (ADR-0017).
> 3. **Event Store**를 Event Bus의 하위(전달 경로)에서 **독립 Subscriber**로
>    위치를 조정했다. 이벤트 전달을 게이팅하지 않고 기록만 담당한다 (ADR-0018).
> 4. **Coordination Capability**를 추가해 조정 역할을 명시했다 (ADR-0019).
> ADR-0005(Interface 우선), ADR-0010~0015(Multi-Agent First 심화)는 유지한다.

---

## 1. 아키텍처 원칙

1. **멀티 에이전트 우선 (Multi-Agent First)** — 모든 작업은 능력을 가진 Agent들이
   협업하여 수행한다.
2. **관리자와 구현자의 분리** — AI Workspace는 조율만 하고, 실제 코드 작성은 구현
   엔진의 책임이다.
3. **엔진 비종속성** — Agent/도메인 로직은 구현 엔진을 알지 못하며, Engine Runtime
   → Engine Adapter를 통해서만 통신한다.
4. **인터페이스 우선 설계 (ADR-0005 유지)** — 컴포넌트 간 협력은 구체 클래스가
   아니라 인터페이스(계약: 입력/출력/예외/보장사항)를 통한다.
5. **느슨한 결합 / Event 우선** — Agent는 서로 직접 호출하지 않고 Event Bus로
   협업한다. Event Store는 **독립 구독자**로서 모든 이벤트를 기록하여 Replay/Audit이
   가능하다.
6. **Capability 중심 선택** — Agent는 역할뿐 아니라 **능력(Capability)**으로
   선택된다. 조정 역할은 **Coordination Capability**로 명시된다.
7. **런타임 계층의 대칭성** — Agent 실행은 **Agent Runtime**이, 엔진 실행은
   **Engine Runtime**이 관리한다. Runtime은 각각 Agent/Engine의 선택·생명주기·
   병렬성을 책임진다.
8. **역할 분리** — 저장/검색(Memory Engine)과 Context 조립/Snapshot(Context
   Manager)을 분리하고, 세션 상태(WorkspaceSession)를 명시적으로 관리한다.
9. **승인 지점의 명시적 분리 / 기록 우선 / 단순한 것에서 시작** — 승인은 게이트로
   강제하고, 상태/결정은 문서와 동기화하며, Voice·Event Store·확장 표면은 구조에
   포함하되 구현은 뒤로 미룬다.

## 2. 전체 구조 개요 (Architecture Diagram)

의존 방향은 항상 **위(사용자)에서 아래(구현 엔진)로만** 향한다. Agent 협업만
Event Bus를 통한 수평 결합이며, Event Store는 Bus의 독립 구독자다.

```
┌────────────────────────────────────────────────────────────────────────┐
│  UI Surfaces   CLI · Dashboard · Mobile · Voice · REST API · Slack · …    │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Interaction Layer               (InteractionEngine)                     │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Workspace Core   (최상위 오케스트레이터)                                │
│  프로젝트/설정 로드 · 서비스 초기화 · WorkspaceSession 관리 ·             │
│  Agent Runtime & Engine Runtime 초기화 · Workflow 시작 · 종료            │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Agent Runtime                                                          │
│  Agent Registry · Agent Scheduler · Agent Manager · Event Bus ──┐        │
└─────────────────────────────────────────────────────────────────┼──────┘
                                   │                               │ 구독
                                   ▼                    ┌──────────▼─────────┐
┌────────────────────────────────────────────────┐     │  Event Store        │
│  Agents (Capability 중심)                       │◀───▶│  (독립 Subscriber)  │
│  Coordination · Planning · Coding · Review ·    │Event│  기록/Replay/Audit  │
│  Documentation · Research · Vision · Voice ·    │ Bus └────────────────────┘
│  Git · MCP …                                    │
└────────────────────────────────────────────────┘
         │  (Agent는 아래 세 축을 사용한다)
   ┌─────┼───────────────────────┬───────────────────────────────┐
   ▼     ▼                       ▼                               ▼
┌──────────────┐  ┌────────────────────────────┐  ┌──────────────────────────┐
│ Core Engines  │  │ Context Manager             │  │ Engine Runtime           │
│ Task·Workflow │  │ Context 조립 / Memory       │  │ 엔진 선택 · 세션 풀 관리 │
│ ·Approval·    │  │ Snapshot 생명주기           │  │ · 병렬 실행              │
│ Automation    │  │        │                    │  │        │                 │
│               │  │        ▼                    │  │        ▼                 │
│               │  │ Memory Engine (저장/검색)   │  │ Engine Adapter           │
│               │  │                             │  │ (per-engine 세션 계약)   │
└──────────────┘  └────────────────────────────┘  └───────────┬──────────────┘
                                                               ▼
                                          ┌──────────────────────────────────┐
                                          │  Implementation Engines (외부)     │
                                          │  Claude Code · Codex · Gemini CLI  │
                                          └──────────────────────────────────┘
```

## 3. 핵심 컴포넌트

### 3.1 UI Surfaces
- **책임**: 사용자와의 접점(CLI/Dashboard/Mobile/Voice/REST API/Slack/Discord/
  Webhook). 입력을 Interaction Layer로 전달.
- **의존 방향**: Interaction Layer만 호출.

### 3.2 Interaction Layer (InteractionEngine)
- **책임**: 다양한 입력 표면을 표준 요청으로 정규화하고 응답을 표면에 맞게 변환
  (ADR-0013). Voice는 이 계층에 붙는 표면이다.
- **의존 방향**: UI Surfaces로부터 호출받음 / Workspace Core를 호출.

### 3.3 Workspace Core (최상위 오케스트레이터)
- **책임 (ADR-0010)**: 프로젝트/설정 로드, 서비스 초기화, **WorkspaceSession
  관리**, **Agent Runtime 및 Engine Runtime 초기화**, Workflow 시작, 종료.
  Task 실행은 Agent Runtime에 위임한다.
- **의존 방향**: Interaction Layer로부터 호출받음 / Agent Runtime, Engine Runtime,
  Interfaces에 의존. 구체 클래스를 직접 참조하지 않는다.

### 3.4 Agent Runtime
Agent의 실행을 담당하는 계층.
- **Agent Registry** (`AgentRegistry`): Agent 등록/조회/제거.
- **Agent Scheduler** (`AgentScheduler`): **Capability 기준** 실행 가능 Agent
  선택, 병렬 실행 관리, 우선순위·순서 결정.
- **Agent Manager** (`AgentManager`): Agent 생성/생명주기/상태 관리.
- **Event Bus** (`EventBus`): Event 발행/구독/Agent 간 통신.

### 3.5 Event Store (EventStore 인터페이스) — 독립 Subscriber
- **책임**: Event Bus를 **구독하는 독립 구독자**로서 모든 이벤트를 기록한다.
  다른 구독자(Agent 등)로의 전달 경로에 끼어들지 않으며(게이팅 없음), Replay/
  Audit/Debugging/Workflow 복구를 제공한다 (ADR-0018).
- **의존 방향**: Event Bus를 구독. 다른 구독자와 동등한 위치.
- **구현 시점**: 인터페이스만 Phase 1, 구현은 이후 Phase.

### 3.6 Agents (Capability 중심)
- **책임**: 각 Agent는 하나 이상의 **Capability**를 가진다: **Coordination**,
  Planning, Coding, Review, Documentation, Research, Vision, Voice, Git, MCP …
  Agent Scheduler는 엔진 종류가 아니라 Capability로 Agent를 선택한다.
- **Coordination Capability (ADR-0019)**: 여러 Agent의 협업을 조정하는 역할을
  명시한다. Coordination 능력을 가진 Agent(Coordinator)는 Event 흐름을 조율하되,
  다른 Agent를 직접 호출하지 않고 Event 기반 협업 규칙을 따른다.
- **협업**: Agent끼리 직접 호출하지 않고 Event 기반으로 협업(§5).
- **실행**: 실제 일은 **Engine Runtime**을 통해 구현 엔진에 위임하고, Context는
  **Context Manager**로, 도메인 작업은 **Core Engines**로 처리한다.

### 3.7 Core Engines (Services)
Task · Workflow · Approval · Automation Engine. Agent가 사용하는 능력 서비스.
- **Workflow Engine**: Mission→Workflow→Task→Step 협업 흐름 계획/실행(§4).
- **Approval Engine**: 승인 대상 4행위 판별/차단.
- **Automation Engine**: 조건/일정 트리거. (Agent가 아니라 서비스, ADR-0012.)
- Task Engine: Task 생성/상태 전이.

### 3.8 Memory 계열 — Context Manager + Memory Engine (역할 분리, ADR-0017)
- **Context Manager** (`ContextManager`): Agent에게 제공할 **Context를 조립**하고,
  **Memory Snapshot의 생명주기**(생성/복원)를 관리한다. WorkspaceSession의
  Memory Snapshot은 Context Manager가 소유·관리한다.
- **Memory Engine** (`MemoryEngine`): **저장/검색**만 담당하는 하위 서비스.
  Context Manager가 이를 사용한다.
- **의존 방향**: Agent → Context Manager → Memory Engine.

### 3.9 Engine Runtime (EngineRuntime 인터페이스, ADR-0016)
Agent Runtime과 Engine Adapter 사이의 계층. 엔진 실행을 관리한다.
- **책임**: **엔진 선택**(capabilities/estimate_cost/supports_parallel 기반),
  **엔진 세션 풀 관리**(Engine Adapter의 create_session/destroy_session 활용),
  **병렬 실행 관리**.
- **의존 방향**: Agent로부터 호출받음 / `EngineAdapter`(구체 구현체)를 통해 실제
  엔진과 통신. Agent는 Engine Adapter를 직접 부르지 않고 Engine Runtime을 거친다.

### 3.10 Engine Adapter (per-engine 세션 계약, ADR-0015)
개별 구현 엔진이 구현하는 계약. Engine Runtime이 호출한다.

| 메서드 | 의미 |
|---|---|
| `create_session()` | 엔진 세션 생성 |
| `run(...)` | 세션 위 실행 요청 |
| `cancel(...)` | 실행 취소 |
| `status(...)` | 실행 상태 조회 |
| `destroy_session()` | 세션 정리/종료 |
| `capabilities()` | 엔진 능력 목록 |
| `supports_parallel()` | 병렬 실행 지원 여부 |
| `estimate_cost(...)` | 실행 전 비용/토큰 추정 |

### 3.11 Implementation Engines (외부)
Claude Code · Codex · Gemini CLI 등.

## 4. Mission → Workflow → Task → Step 계층 (ADR-0011)

```
Mission (사용자 목표) → Workflow (협업 흐름) → Task (Agent 할당 작업) → Step (세부 실행)
```

## 5. Agent 협업 구조 (Event Driven)

Agent는 직접 호출하지 않고 Event로 협업한다. Event Store는 Bus의 독립 구독자로
모든 이벤트를 기록한다. Coordination Capability를 가진 Agent가 흐름을 조정할 수 있다.

```
Planner Agent
   │  MissionPlanned Event
   ▼
Coding Agent
   │  CodeCompleted Event
   ▼
Review Agent
   │  ReviewCompleted Event
   ▼
Documentation Agent
   │  DocumentationCompleted Event
   ▼
Context Manager → Memory Engine 갱신 (Memory는 Agent가 아니라 서비스)

  ※ 모든 Event는 Event Bus의 독립 구독자인 Event Store에 함께 기록된다.
```

## 6. 도메인 모델

| 모델 | 설명 |
|---|---|
| `Project` | 프로젝트 |
| `Mission` | 사용자 목표(최상위 단위) |
| `Workflow` | Mission 수행 협업 흐름 |
| `Task` | Agent에게 할당되는 작업 |
| `Step` | Task 내부 세부 실행 단위 |
| `WorkspaceSession` | 현재 실행 상태(현재 프로젝트/Mission/활성 Workflow/활성 Agent/Memory Snapshot/Engine Session) |
| `Agent` | 능력을 가진 실행 주체 |
| `AgentRole` | Agent 역할 유형 |
| `AgentCapability` | Coordination/Planning/Coding/Review/Documentation/Research/Vision/Voice/Git/MCP … |
| `AgentStatus` | 생명주기 상태 |

## 7. Interfaces (추상 계약, 총 16종)

| Interface | 계약 책임 | 구현 시점 | 상태 |
|---|---|---|---|
| `ProjectRepository` | 프로젝트 조회/저장 | Phase 1 | 기존 |
| `WorkflowEngine` | Mission→…→Step 협업 흐름 | 이후 | 기존 |
| `TaskEngine` | Task 생성/상태 전이 | 이후 | 기존 |
| `MemoryEngine` | Memory 저장/검색 (Snapshot 제외) | 이후 | 기존(축소) |
| `ApprovalEngine` | 승인 대상 판별/차단 | 이후 | 기존 |
| `AutomationEngine` | 조건/일정 트리거 | 이후 | 기존 |
| `EngineAdapter` | per-engine 세션 계약 | Phase 4 | 기존 |
| `AgentManager` | Agent 생성/생명주기/상태 | 이후 | 기존 |
| `AgentRepository` | Agent 조회/저장 | 이후 | 기존 |
| `AgentRegistry` | Agent 등록/조회/제거 | 이후 | 기존 |
| `AgentScheduler` | Capability 기준 선택/병렬/우선순위 | 이후 | 기존 |
| `InteractionEngine` | 입력 표면 정규화 | 이후 | 기존 |
| `EventBus` | 이벤트 발행/구독 | 이후 | 기존 |
| `EventStore` | 이벤트 기록(독립 구독자)/Replay/Audit | 이후 | 기존(위치 조정) |
| `EngineRuntime` | 엔진 선택/세션 풀/병렬 실행 | 이후 | **신규** |
| `ContextManager` | Context 조립 / Memory Snapshot 생명주기 | 이후 | **신규** |

## 8. 의존성 규칙 (Dependency Rules)

1. UI Surfaces → Interaction Layer만 호출.
2. Interaction Layer → Workspace Core만 호출.
3. Workspace Core → Agent Runtime, Engine Runtime, Interfaces에만 의존. Task를
   직접 실행하지 않고 Agent Runtime에 위임.
4. Agent Runtime 컴포넌트는 서로 및 해당 인터페이스, `AgentRepository`에 의존.
5. Agent는 **Core Engines, Context Manager, Engine Runtime, Event Bus**에 의존.
   Agent끼리 직접 호출 금지(Event Bus만).
6. **Engine 호출은 Agent → Engine Runtime → Engine Adapter → 구현 엔진** 순서로만
   이루어진다. Agent가 Engine Adapter를 직접 부르지 않는다.
7. **Memory 접근은 Agent → Context Manager → Memory Engine** 순서로만 이루어진다.
   Memory Snapshot은 Context Manager가 관리한다.
8. **Event Store는 Event Bus의 독립 구독자**다. 다른 구독자로의 전달을 가로막지
   않는다.
9. Memory/Automation은 Agent가 아니라 Core Engine(서비스)이다.
10. Persistence는 `ProjectRepository`/`AgentRepository`/`EventStore` 인터페이스를
    통해서만 접근한다.

## 9. 디렉터리 구조와 컴포넌트 매핑

```
src/ai_workspace/
├── domain/            # Project, Mission, Workflow, Task, Step,
│                       #   WorkspaceSession, Agent, AgentRole, AgentCapability, AgentStatus
├── interfaces/         # 추상 계약 (16종, §7)
├── core/              # Workspace Core (WorkspaceSession 관리, Runtime 초기화)
├── runtime/           # (이후 Phase)
│   ├── agent/         #   Agent Runtime: registry, scheduler, manager
│   └── engine/        #   Engine Runtime: 선택/세션 풀/병렬
├── agents/            # 능력별 Agent 구현체 (이후 Phase)
├── engines/           # Core Engines 구현 (Task/Workflow/Approval/Automation, 이후 Phase)
├── memory/            # Context Manager + Memory Engine 구현 (이후 Phase)
├── events/            # Event Bus + Event Store 구현 (이후 Phase)
├── interaction/        # Interaction Layer 구현 (이후 Phase)
├── adapters/          # EngineAdapter 구현 (Phase 4: claude_code.py, codex.py, gemini_cli.py)
├── storage/           # ProjectRepository/AgentRepository/EventStore 파일 구현
└── cli/               # CLI 진입점 (UI Surface의 하나)
```

## 10. 확장성 고려사항

- **신규 Agent/Capability**: Registry에 등록 + Event 구독만 추가. Scheduler가
  Capability로 선택. 조정이 필요하면 Coordination Capability를 부여한다.
- **신규 구현 엔진**: `EngineAdapter` 구현체를 추가하면 Engine Runtime이 선택
  대상으로 편입한다.
- **신규 UI 표면(Voice/Slack)**: Interaction Layer에 어댑터만 추가.
- **감사/복구**: Event Store의 독립 기록을 Replay하여 상태를 재구성.
- **Context 전략 변경**: Context Manager만 교체하면 되며 Memory Engine(저장/검색)은
  영향받지 않는다.

## 11. 기술 스택 (제안 — 각 Phase에서 ADR로 확정)

| 영역 | 제안 | 이유 |
|---|---|---|
| 언어 | Python 3.11+ | 프로젝트 규칙(PEP 8, type hint) |
| 데이터 모델 | `dataclasses` (필요 시 `pydantic`) | 명시적 스키마 |
| 인터페이스 | `abc.ABC` / `typing.Protocol` | 표준 계약 강제 |
| Event Bus/Store | 인메모리 pub/sub + append-only 파일 로그 | 단순 시작, 이후 확장 |
| 저장 (Phase 1) | 파일 기반 (Markdown/JSON) | 별도 인프라 없이 시작 |
| UI (Phase 1) | CLI | 가장 단순한 표면 |
| 테스트 | `pytest` | Python 표준 관행 |

## 12. 대안 및 트레이드오프 (v0.6.0 신규 결정)

| 대안 | 장점 | 단점 | 채택 |
|---|---|---|---|
| Agent가 Engine Adapter를 직접 호출 | 계층 단순 | 엔진 선택/세션 풀/병렬을 Agent마다 중복 | 기각 |
| **Engine Runtime 계층 분리** | 엔진 선택·세션·병렬을 한 곳에서 관리, Agent 단순화 | 계층 추가 | **채택** |
| Memory Engine이 Snapshot까지 담당 | 컴포넌트 적음 | 저장/검색과 Context/Snapshot 책임 혼재 | 기각 |
| **Context Manager로 Snapshot 분리** | 저장과 Context 책임 분리, Context 전략 교체 용이 | 컴포넌트 추가 | **채택** |
| Event Store를 Bus 하위(전달 경로)에 배치 | 기록 보장 직관적 | 전달 게이팅·단일 장애점 위험 | 기각 |
| **Event Store를 독립 Subscriber로** | 전달 비간섭, 장애 격리, 확장 용이 | 기록 누락 방지 설계 필요 | **채택** |
| 조정 역할을 암묵적으로 처리 | 별도 정의 불필요 | 조정 책임이 흐릿함 | 기각 |
| **Coordination Capability 명시** | 조정 역할이 선택/추적 가능 | Capability 하나 추가 | **채택** |
