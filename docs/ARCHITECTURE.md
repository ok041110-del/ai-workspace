# ARCHITECTURE — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.5.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft (Milestone 1 / Phase 1 — 아키텍처 재설계 완료, 구현 재개 대기) |

이 문서는 `docs/PRD.md`에 정의된 요구사항을 바탕으로 AI Workspace의 구조를 설계한다.
실제 구현이 진행됨에 따라 이 문서와 실제 구조가 항상 일치하도록 갱신한다
(Documentation First 원칙).

> **v0.5.0 변경 사항 (Multi-Agent First 심화 — ADR-0010 ~ ADR-0015)**
> v0.4.0에서 도입한 Multi-Agent First를 실행 계층까지 구체화했다.
> 1. **Workspace Core**의 책임을 더 좁혔다. 이제 Agent 등록·Task 분배·Engine
>    선택을 직접 하지 않고, **Agent Runtime**에 위임한다. Core는 프로젝트/설정
>    로드, 서비스 초기화, **WorkspaceSession 관리**, Agent Runtime 초기화,
>    Workflow 시작, 종료만 담당한다.
> 2. **Agent Runtime 계층**을 추가했다(Agent Registry / Agent Scheduler /
>    Agent Manager / Event Bus).
> 3. 도메인에 **WorkspaceSession, AgentCapability, Step**을 추가하고,
>    **Mission → Workflow → Task → Step** 4단 계층을 기본 모델로 삼았다.
> 4. Agent를 **Capability 중심**으로 설계했다(엔진 종류와 무관하게 능력으로 선택).
>    **Memory/Automation은 Agent가 아니라 Core Engine(서비스)**임을 명확히 했다.
> 5. **Conversation Layer → Interaction Layer**로 확장(입력 표면 다양화).
> 6. **Event Store**를 Event Bus와 별도로 추가(기록/Replay/Audit/복구).
> 7. **EngineAdapter**를 세션 생명주기를 포함한 실행 계약으로 확장
>    (create_session/run/cancel/status/destroy_session/capabilities/
>    supports_parallel/estimate_cost).
> ADR-0005(Interface 우선 설계)는 그대로 유지·확장한다.

---

## 1. 아키텍처 원칙

1. **멀티 에이전트 우선 (Multi-Agent First)** — 모든 작업은 능력을 가진 Agent들이
   협업하여 수행한다. 단일 실행은 특수 케이스다.
2. **관리자와 구현자의 분리** — AI Workspace는 조율만 하고, 실제 코드 작성은 구현
   엔진의 책임이다.
3. **엔진 비종속성** — Agent/도메인 로직은 구현 엔진을 알지 못하며, Engine
   Adapter를 통해서만 통신한다.
4. **인터페이스 우선 설계 (ADR-0005 유지)** — 컴포넌트 간 협력은 구체 클래스가
   아니라 인터페이스(계약: 입력/출력/예외/보장사항)를 통한다.
5. **느슨한 결합 / Event 우선** — Agent는 서로 직접 호출하지 않고 Event Bus로
   협업한다. 모든 이벤트는 Event Store에 기록되어 Replay/Audit이 가능하다.
6. **Capability 중심 선택** — Agent는 역할뿐 아니라 **능력(Capability)**으로
   선택된다. 엔진 종류에 종속되지 않는다.
7. **세션 중심 실행 (Session-Centric)** — Workspace의 현재 실행 상태는
   `WorkspaceSession` 도메인으로 명시적으로 관리된다.
8. **승인 지점의 명시적 분리** — 아키텍처 변경 등 4가지 행위는 Approval Engine
   게이트로 강제되며 우회 경로가 없다.
9. **기록 우선 / 단순한 것에서 시작** — 상태/결정은 문서와 동기화하고, Voice·Event
   Store·Interaction 확장 표면 등은 **구조에는 포함하되 구현은 뒤로 미룬다**.

## 2. 전체 구조 개요 (Architecture Diagram)

의존 방향은 항상 **위(사용자)에서 아래(구현 엔진)로만** 향한다. Agent 협업만
Event Bus/Event Store를 통한 수평 결합이다.

```
┌────────────────────────────────────────────────────────────────────────┐
│  UI Surfaces                                                            │
│  CLI · Dashboard · Mobile · Voice · REST API · Slack · Discord · Webhook │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Interaction Layer               (InteractionEngine 인터페이스)          │
│  모든 입력 표면을 표준 요청으로 정규화 / 응답을 표면에 맞게 변환           │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Workspace Core                  (최상위 오케스트레이터)                 │
│  프로젝트/설정 로드 · 서비스 초기화 · WorkspaceSession 관리 ·             │
│  Agent Runtime 초기화 · Workflow 시작 · 종료                             │
│  ※ Task를 직접 실행하지 않고 Agent Runtime에 위임한다                    │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Agent Runtime                                                          │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌─────────────┐ │
│  │ Agent Registry │ │ Agent Scheduler│ │ Agent Manager  │ │  Event Bus  │ │
│  │ 등록/조회/제거  │ │ 선택/병렬/순서 │ │ 생성/생명주기/  │ │ 발행/구독/  │ │
│  │               │ │               │ │ 상태           │ │ 통신        │ │
│  └───────────────┘ └───────────────┘ └───────────────┘ └──────┬──────┘ │
│                                                                │        │
│                                                         ┌──────▼──────┐ │
│                                                         │ Event Store │ │
│                                                         │ 기록/Replay/│ │
│                                                         │ Audit/복구  │ │
│                                                         └─────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Agents (Capability 중심)                                               │
│  Planning · Coding · Review · Documentation · Research · Vision ·        │
│  Voice · Git · MCP …  (능력으로 선택, 엔진 비종속)                        │
└────────────────────────────────────────────────────────────────────────┘
                 │  (Agent는 아래 두 축을 사용한다)
     ┌───────────┴─────────────────────────────────┐
     ▼                                              ▼
┌──────────────────────────────┐        ┌──────────────────────────────────┐
│  Core Engines (Services)      │        │  Engine Adapter                  │
│  Task · Workflow · Memory ·   │        │  create_session · run · cancel · │
│  Approval · Automation Engine │        │  status · destroy_session ·      │
│  (Memory/Automation은 Agent가 │        │  capabilities · supports_parallel│
│   아니라 서비스다)             │        │  · estimate_cost                 │
└──────────────────────────────┘        └──────────────────────────────────┘
                                                       │
                                                       ▼
                                    ┌──────────────────────────────────┐
                                    │  Implementation Engines (외부)     │
                                    │  Claude Code · Codex · Gemini CLI  │
                                    └──────────────────────────────────┘
```

## 3. 핵심 컴포넌트

### 3.1 UI Surfaces
- **책임**: 사용자와의 물리적 접점(CLI/Dashboard/Mobile/Voice/REST API/Slack/
  Discord/Webhook). 입력을 Interaction Layer로 전달하고 응답을 표시한다.
- **의존 방향**: Interaction Layer만 호출한다.
- **Voice 취급**: Voice는 Workspace Core에 직접 연결되지 않는다. **Interaction
  Layer에 추가되는 표면**이다.

### 3.2 Interaction Layer (InteractionEngine 인터페이스)
- **책임**: 다양한 입력 표면을 **표준 요청**으로 정규화하고, 응답을 표면에 맞게
  변환한다. (기존 Conversation Layer의 확장 — ADR-0013.)
- **의존 방향**: UI Surfaces로부터 호출받음 / Workspace Core를 호출.
- **구현 시점**: 인터페이스는 Phase 1에서 정의, 구현은 이후 Phase.

### 3.3 Workspace Core (최상위 오케스트레이터)
- **책임 (포함, ADR-0010)**
  1. 프로젝트 로드 (`ProjectRepository`)
  2. 설정(Config) 로드
  3. 서비스 초기화
  4. **WorkspaceSession 관리** (현재 실행 상태의 생성/갱신/종료)
  5. **Agent Runtime 초기화** (Registry/Scheduler/Manager/Event Bus 준비)
  6. Workflow 시작 (`WorkflowEngine`)
  7. 종료(Shutdown)
- **책임 (제외)**: Task 실행, Agent 직접 제어, Engine 직접 호출, 파일 저장 세부.
  Task 실행은 **모두 Agent Runtime에 위임**한다.
- **의존 방향**: Interaction Layer로부터 호출받음 / Agent Runtime과 Interfaces에
  의존. 구체 클래스를 직접 참조하지 않는다.

### 3.4 Agent Runtime
Workspace Core 아래에서 Agent의 실제 실행을 담당하는 계층. 네 컴포넌트로 구성된다.

- **3.4.1 Agent Registry** (`AgentRegistry`): Agent 등록 / 조회 / 제거.
- **3.4.2 Agent Scheduler** (`AgentScheduler`): 실행 가능한 Agent 선택,
  **병렬 실행 관리**, 우선순위·실행 순서 결정.
- **3.4.3 Agent Manager** (`AgentManager`): Agent 생성 / 생명주기 관리 /
  상태 관리.
- **3.4.4 Event Bus** (`EventBus`): Event 발행 / 구독 / Agent 간 통신. 모든
  이벤트는 Event Store에 함께 기록된다.
- **의존 방향**: Workspace Core로부터 호출받음 / `AgentRegistry`,
  `AgentScheduler`, `AgentManager`, `AgentRepository`, `EventBus`, `EventStore`,
  개별 Agent 인터페이스에 의존.

### 3.5 Event Store (EventStore 인터페이스)
- **책임**: Event Bus를 흐르는 이벤트를 **기록(persist)**한다. 이로써 Replay,
  Audit, Debugging, Workflow 복구가 가능하다 (ADR-0014).
- **구조**: `Event Bus → Event Store → Subscribers`. 구독자는 Event Store를
  통해 과거 이벤트를 재생할 수 있다.
- **의존 방향**: Event Bus가 기록을 위해 호출. 특정 Agent에 의존하지 않는다.
- **구현 시점**: 인터페이스만 Phase 1, 구현은 이후 Phase.

### 3.6 Agents (Capability 중심)
- **책임**: 각 Agent는 하나 이상의 **Capability**(Planning, Coding, Review,
  Documentation, Research, Vision, Voice, Git, MCP …)를 가진다. Agent Scheduler는
  **엔진 종류가 아니라 Capability를 기준으로** Agent를 선택한다.
- **협업**: Agent끼리 직접 호출하지 않고 **Event 기반**으로 협업한다(§5).
- **실행**: 실제 일은 `EngineAdapter`를 통해 구현 엔진에 위임하며, 필요 시 Core
  Engines(Task/Workflow/Memory/Approval/Automation)를 서비스로 사용한다.
- **의존 방향**: Agent Runtime이 생성/관리 / `EngineAdapter`, Core Engines,
  `EventBus`를 사용.

### 3.7 Core Engines (Services)
Task · Workflow · Memory · Approval · Automation Engine. Agent와 Workspace
Core가 사용하는 **능력 서비스**다. (Agent가 아니다.)
- **Memory Engine (ADR-0012)**: **Agent가 아니라 서비스**다. Context 생성 /
  Memory 검색 / Memory 저장 / Snapshot 관리를 담당하며, 모든 Agent가 사용한다.
- **Automation Engine**: 조건/일정 트리거를 담당하는 서비스. (Agent가 아니다.)
- **Workflow Engine**: **Mission → Workflow → Task → Step** 계층(§4)의 협업
  흐름을 계획/실행한다.
- Task/Approval Engine의 책임은 v0.4.0과 동일.

### 3.8 Engine Adapter (세션 생명주기 포함 실행 계약)
모든 구현 엔진이 공통으로 구현하는 실행 계약 (ADR-0015). 구체 구현은 Phase 3.

| 메서드 | 의미 |
|---|---|
| `create_session()` | 구현 엔진과의 세션 생성 (상태 있는 실행의 시작점) |
| `run(...)` | 세션 위에서 실행 요청. 실행 핸들/결과 반환 |
| `cancel(...)` | 진행 중 실행 취소 |
| `status(...)` | 실행 상태 조회 |
| `destroy_session()` | 세션 정리/종료 |
| `capabilities()` | 이 엔진이 지원하는 능력 목록 |
| `supports_parallel()` | 병렬 실행 지원 여부 |
| `estimate_cost(...)` | 실행 전 비용/토큰 추정 |

### 3.9 Implementation Engines (외부)
Claude Code · Codex · Gemini CLI 등. AI Workspace 범위 밖의 실제 실행 주체.

## 4. Mission → Workflow → Task → Step 계층 (ADR-0011)

Workflow를 다음 4단 계층 안에서 재정의한다.

```
Mission     사용자의 목표를 나타내는 최상위 단위
   │
   ▼
Workflow    Mission을 수행하기 위한 협업 흐름 (Agent 협업)
   │
   ▼
Task        Agent에게 할당되는 작업
   │
   ▼
Step        Task 내부의 세부 실행 단위
```

- **Mission**: "무엇을 이루고자 하는가" (사용자 목표).
- **Workflow**: Mission을 이루기 위한 Agent 협업 흐름(Task 생성 → Agent 할당 →
  협업 → 결과 통합).
- **Task**: 특정 Agent에게 할당되는 실행 단위.
- **Step**: Task를 구성하는 세부 실행 단위.

## 5. Agent 협업 구조 (Event Driven)

Agent는 서로 직접 호출하지 않고 Event로 협업한다. 모든 이벤트는 Event Store에
기록된다.

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
Memory Engine Update   (Memory는 Agent가 아니라 서비스; 이벤트를 받아 갱신)
```

## 6. 도메인 모델

| 모델 | 설명 |
|---|---|
| `Project` | 프로젝트 (기존) |
| `Mission` | 사용자 목표를 나타내는 최상위 단위 (**신규**) |
| `Workflow` | Mission 수행을 위한 협업 흐름 (재정의) |
| `Task` | Agent에게 할당되는 작업 (기존) |
| `Step` | Task 내부의 세부 실행 단위 (**신규**) |
| `WorkspaceSession` | Workspace의 현재 실행 상태 (**신규 핵심**): 현재 프로젝트/현재 Mission/활성 Workflow/활성 Agent/Memory Snapshot/Engine Session |
| `Agent` | 능력을 가진 실행 주체 (**신규**) |
| `AgentRole` | Agent의 역할 유형 (**신규**) |
| `AgentCapability` | Agent 능력 (Planning/Coding/Review/Documentation/Research/Vision/Voice/Git/MCP …) (**신규**) |
| `AgentStatus` | Agent 생명주기 상태 (**신규**) |

## 7. Interfaces (추상 계약)

기존 인터페이스를 유지하고, Agent Runtime·Interaction·Event Store를 위한
인터페이스를 추가한다. `ConversationEngine`은 `InteractionEngine`으로 대체한다.

| Interface | 계약 책임 | 구현 시점 | 상태 |
|---|---|---|---|
| `ProjectRepository` | 프로젝트 조회/저장 | Phase 1 | 기존 |
| `WorkflowEngine` | Mission→Workflow→Task→Step 협업 흐름 | 이후 | 기존(재정의) |
| `TaskEngine` | Task 생성/상태 전이 | 이후 | 기존 |
| `MemoryEngine` | Context 생성/검색/저장/Snapshot | 이후 | 기존(확장) |
| `ApprovalEngine` | 승인 대상 판별/차단 | 이후 | 기존 |
| `AutomationEngine` | 조건/일정 트리거 | 이후 | 기존 |
| `EngineAdapter` | 세션 생명주기 포함 실행 계약 | Phase 3 | 기존(확장) |
| `AgentManager` | Agent 생성/생명주기/상태 | 이후 | 기존 |
| `AgentRepository` | Agent 조회/저장 | 이후 | 기존 |
| `AgentRegistry` | Agent 등록/조회/제거 | 이후 | **신규** |
| `AgentScheduler` | Agent 선택/병렬/우선순위 | 이후 | **신규** |
| `InteractionEngine` | 입력 표면 정규화 (Voice/CLI/API/Slack …) | 이후 | **신규(대체)** |
| `EventBus` | 이벤트 발행/구독 | 이후 | 기존 |
| `EventStore` | 이벤트 기록/Replay/Audit | 이후 | **신규** |

## 8. 의존성 규칙 (Dependency Rules)

1. UI Surfaces는 **Interaction Layer만** 호출한다.
2. Interaction Layer는 **Workspace Core만** 호출한다.
3. Workspace Core는 Agent Runtime과 Interfaces에만 의존한다. **Task를 직접
   실행하지 않고 Agent Runtime에 위임한다.**
4. Agent Runtime(Registry/Scheduler/Manager/Event Bus)은 서로 및 해당
   인터페이스, `AgentRepository`, `EventStore`에 의존한다.
5. Agent는 `EngineAdapter`, Core Engines, `EventBus`에 의존한다. **Agent끼리
   직접 호출하지 않고 Event Bus를 통해서만 협업한다.**
6. 구현 엔진 호출은 오직 `EngineAdapter`(구체 구현체)를 통해서만 이루어진다.
7. **Memory/Automation은 Agent가 아니라 Core Engine(서비스)**이다. Agent가
   이들을 서비스로 사용한다.
8. Persistence는 `ProjectRepository`/`AgentRepository`/`EventStore` 인터페이스를
   통해서만 접근한다.

## 9. 디렉터리 구조와 컴포넌트 매핑

```
src/ai_workspace/
├── domain/            # Project, Mission, Workflow, Task, Step,
│                       #   WorkspaceSession, Agent, AgentRole, AgentCapability, AgentStatus
├── interfaces/         # 추상 계약 (14종, §7)
├── core/              # Workspace Core (WorkspaceSession 관리, Agent Runtime 초기화)
├── runtime/           # Agent Runtime (registry.py, scheduler.py, manager.py) (이후 Phase)
├── agents/            # 능력별 Agent 구현체 (이후 Phase)
├── engines/           # Core Engines 구현 (Task/Workflow/Memory/Approval/Automation, 이후 Phase)
├── events/            # Event Bus + Event Store 구현 (이후 Phase)
├── interaction/        # Interaction Layer 구현 (이후 Phase)
├── adapters/          # EngineAdapter 구현 (Phase 3: claude_code.py, codex.py, gemini_cli.py)
├── storage/           # ProjectRepository/AgentRepository/EventStore 파일 구현
└── cli/               # CLI 진입점 (UI Surface의 하나)
```

## 10. 확장성 고려사항

- **신규 Agent/Capability 추가**: 새 Agent를 Registry에 등록하고 Event 구독만
  더하면 되며, Scheduler는 Capability로 자동 선택한다.
- **신규 UI 표면(Voice/Slack 등)**: Interaction Layer에 표면 어댑터만 추가한다.
- **신규 구현 엔진**: `EngineAdapter` 계약을 구현하는 클래스를 `adapters/`에 추가.
- **Workflow 복구/감사**: Event Store의 Replay로 과거 상태를 재구성한다.
- **저장소 교체**: Repository/EventStore 구현체 교체로 충분하다.

## 11. 기술 스택 (제안 — 각 Phase에서 ADR로 확정)

| 영역 | 제안 | 이유 |
|---|---|---|
| 언어 | Python 3.11+ | 프로젝트 규칙(PEP 8, type hint) |
| 데이터 모델 | `dataclasses` (필요 시 `pydantic`) | 명시적 스키마 |
| 인터페이스 | `abc.ABC` / `typing.Protocol` | 표준 계약 강제 |
| Event Bus/Store | 인메모리 pub/sub + append-only 파일 로그 (초기) | 단순 시작, 이후 확장 |
| 저장 (Phase 1) | 파일 기반 (Markdown/JSON) | 별도 인프라 없이 시작 |
| UI (Phase 1) | CLI | 가장 단순한 표면 |
| 테스트 | `pytest` | Python 표준 관행 |

## 12. 대안 및 트레이드오프 (v0.5.0 신규 결정)

| 대안 | 장점 | 단점 | 채택 |
|---|---|---|---|
| Workspace Core가 Agent를 직접 제어 | 계층 단순 | Core 비대·병렬/스케줄링 혼재 | 기각 |
| **Agent Runtime 계층 분리** | Registry/Scheduler/Manager 책임 분리, 병렬·우선순위 관리 용이 | 계층 추가 | **채택** |
| Workflow=Task 2단 | 단순 | 목표·세부 실행 표현 부족 | 기각 |
| **Mission→Workflow→Task→Step 4단** | 목표부터 세부 실행까지 표현 | 모델 수 증가 | **채택** |
| 역할(Role)만으로 Agent 선택 | 단순 | 엔진/능력 매칭 부정확 | 기각 |
| **Capability 중심 선택** | 엔진 비종속, 정확한 매칭 | Capability 정의 필요 | **채택** |
| Event Bus만 사용 | 단순 | Replay/Audit/복구 불가 | 기각 |
| **Event Store 분리** | 기록/Replay/Audit/복구 | 저장 계층 추가 | **채택** |
| Memory를 Agent로 | 일관돼 보임 | 모든 Agent가 쓰는 공용 서비스에 부적합 | 기각 |
| **Memory를 Core Engine으로** | 공용 서비스로 재사용 | — | **채택** |
| EngineAdapter 무상태 run만 | 단순 | 세션 있는 엔진 제어 불가 | 기각 |
| **세션 생명주기 포함 계약** | 상태 있는 실행/취소/정리 가능 | 계약 확대 | **채택** |
