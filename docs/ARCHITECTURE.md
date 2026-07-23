# ARCHITECTURE — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.4.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft (Milestone 1 / Phase 1 — 아키텍처 재설계 완료, 구현 재개 대기) |

이 문서는 `docs/PRD.md`에 정의된 요구사항을 바탕으로 AI Workspace의 구조를 설계한다.
실제 구현이 진행됨에 따라 이 문서와 실제 구조가 항상 일치하도록 갱신한다
(Documentation First 원칙).

> **v0.4.0 변경 사항 (Multi-Agent First 전환 — ADR-0006 ~ ADR-0009)**
> AI Workspace의 방향을 "필요 시 다중 에이전트를 사용할 수 있는 Workspace"에서
> **"상시 멀티 에이전트(Multi-Agent First) Workspace"**로 변경했다. 멀티 에이전트는
> 더 이상 선택 기능이 아니라 시스템의 **기본 구조**다. 주요 변경:
> 1. **Workspace Core**를 Engine 오케스트레이터에서 **Agent 최상위
>    오케스트레이터**로 재정의했다. Task를 직접 실행하지 않고 Agent에 위임한다.
> 2. **Agent Manager**와 **Agent 도메인**(Agent, AgentRole, AgentStatus)을 추가했다.
> 3. **Workflow**를 단순 실행 순서에서 **협업 흐름**(Task 생성 → Agent 할당 →
>    Agent 간 협업 → 결과 통합)으로 재정의했다.
> 4. **Conversation Layer**를 도입했다 (CLI/Dashboard/Mobile/Voice/API를 통합하는
>    입력 계층). Voice는 이 계층에 연결되는 UI로 취급한다.
> 5. **Event Bus** 기반의 느슨한 결합 구조를 도입했다 (Agent 간 직접 호출 대신
>    Event 우선).
> 6. **EngineAdapter**를 `run_task()` 단일 계약에서 모든 Agent가 공유하는 확장
>    실행 계약(run/cancel/status/capabilities/supports_parallel/estimate_cost)으로
>    확장했다.
> v0.3.0에서 확정한 "Interface 우선 설계"(ADR-0005)는 그대로 유지·확장한다.

---

## 1. 아키텍처 원칙

1. **멀티 에이전트 우선 (Multi-Agent First)**
   Workspace의 모든 작업은 역할(Role)을 가진 Agent들이 협업하여 수행한다.
   단일 실행 경로는 특수 케이스이며, 기본 구조는 항상 다중 Agent 협업이다.

2. **관리자와 구현자의 분리 (Separation of Orchestration and Implementation)**
   AI Workspace(관리자)는 "어떤 Agent가, 무엇을, 언제, 어떤 Engine으로" 할지
   결정한다. "어떻게 코드를 작성하는가"는 전적으로 구현 엔진(Claude Code, Codex,
   Gemini CLI 등)의 책임이다.

3. **엔진 비종속성 (Engine Agnosticism)**
   Agent와 도메인 로직은 특정 구현 엔진의 API/CLI 형식을 알지 못한다. 엔진과의
   통신은 반드시 Engine Adapter를 통해서만 이루어진다 (의존성 역전).

4. **인터페이스 우선 설계 (Interface-Driven Design, ADR-0005 유지)**
   모든 컴포넌트 간 협력은 구체 클래스가 아니라 **Interfaces(추상 계약)**를 통해
   이루어진다. 구체 구현체는 각 Phase에서 순차적으로 채워진다.

5. **느슨한 결합 / Event 우선 (Loose Coupling, Event-First)**
   Agent는 서로를 직접 호출하지 않고, **Event Bus**를 통해 이벤트를 발행/구독하여
   협업한다. 이로써 Agent를 독립적으로 추가·교체·테스트할 수 있다.

6. **승인 지점의 명시적 분리 (Explicit Approval Boundaries)**
   아키텍처 변경, 신규 기능, 리팩토링, Phase 완료는 별도의 승인 상태를 가지는
   명시적 게이트(Approval Engine)로 모델링한다. 우회 경로는 존재하지 않는다.

7. **기록 우선 (Traceability by Design)**
   Task/Agent 상태 변화, 승인/반려, 주요 설계 결정은 사람이 읽을 수 있는 문서
   (`.ai/TASKS.md`, `.ai/DECISIONS.md`, `.ai/MEMORY.md`)와 항상 동기화된다.

8. **단순한 것에서 시작 (Start Simple, Extend Later)**
   Phase 1은 단일 사용자, 로컬 파일 기반 저장을 가정한다. 다중 사용자, 원격 저장,
   동시성 제어 등은 이후 Phase에서 필요할 때 확장한다 (YAGNI). Voice/Event Bus
   등은 **구조에는 포함하되 구현은 뒤로 미룬다.**

## 2. 전체 구조 개요

의존 방향은 항상 **위(사용자와 가까운 쪽)에서 아래(구현 엔진과 가까운 쪽)로만**
향한다. Agent 간 협업만은 예외적으로 **Event Bus를 통한 수평적 느슨한 결합**으로
이루어진다.

```
┌──────────────────────────────────────────────────────────────┐
│  UI Surfaces                                                   │
│  CLI · Dashboard · Mobile · Voice · API                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Conversation Layer         (ConversationEngine 인터페이스)     │
│  모든 입력 표면을 표준 요청으로 정규화 / 응답을 표면에 맞게 변환   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Workspace Core             (최상위 오케스트레이터)             │
│  프로젝트/설정 로드 · 서비스 초기화 · Agent 등록/관리 ·          │
│  Workflow 시작 · Task 분배 · Engine 선택/위임 · 종료             │
│  ※ Task를 직접 실행하지 않고 Agent에게 위임한다                 │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Agent Manager              (AgentManager 인터페이스)          │
│  Agent 생성 · 생명주기 · 선택 · 협업 조율 · 상태 관리            │
└──────────────────────────────────────────────────────────────┘
             │                                      ▲
             ▼                                      │
┌───────────────────────────────────┐     ┌──────────────────────┐
│  Agents                            │◀───▶│  Event Bus            │
│  Planner · Coding · Review ·       │     │  발행/구독 기반        │
│  Research · Memory · Automation     │     │  느슨한 결합           │
└───────────────────────────────────┘     └──────────────────────┘
             │  (Agent는 아래 두 축을 사용한다)
   ┌─────────┴───────────────────────────────┐
   ▼                                          ▼
┌──────────────────────────────┐   ┌──────────────────────────────┐
│  Domain Services (Core Engines)│   │  Engine Adapter              │
│  Task · Workflow · Memory ·    │   │  run · cancel · status ·     │
│  Approval · Automation Engine  │   │  capabilities ·              │
│                                │   │  supports_parallel ·         │
│                                │   │  estimate_cost               │
└──────────────────────────────┘   └──────────────────────────────┘
                                                │
                                                ▼
                              ┌──────────────────────────────────┐
                              │  Implementation Engines (외부)     │
                              │  Claude Code · Codex · Gemini CLI  │
                              └──────────────────────────────────┘
```

**핵심 관계 요약**
- **Agent가 시스템의 주체(actor)**다. 실제 일은 Agent가 수행하되, 직접 코드를
  작성하지 않고 Engine Adapter를 통해 구현 엔진에 위임한다.
- **Core Engines는 능력(capability) 서비스**다. Agent와 Workspace Core가
  Task/Workflow/Memory/Approval/Automation 기능을 사용할 때 호출하는 도메인
  서비스이며, 그 자체가 Agent는 아니다. (예: Memory Agent는 MemoryEngine
  서비스를 사용해 메모리를 큐레이션하는 Agent다.)
- **Event Bus는 Agent 협업의 기본 통로**다. Planner가 Task를 만들면
  `TaskCreated` 이벤트가 발행되고, 이를 구독한 Coding Agent가 실행되는 식이다.

## 3. 핵심 컴포넌트

각 컴포넌트마다 **책임**과 **의존 방향**을 명시한다.

### 3.1 UI Surfaces (CLI · Dashboard · Mobile · Voice · API)
- **책임**: 사용자와의 물리적 접점. 입력을 받아 Conversation Layer로 전달하고,
  응답을 사용자에게 표시한다.
- **의존 방향**: Conversation Layer만 호출한다. Workspace Core 이하를 직접
  알지 못한다.
- **Voice 취급**: Voice는 Workspace Core가 아니라 **Conversation Layer에
  연결되는 하나의 UI**다. 지금은 구현하지 않으나, 다른 표면과 동일하게
  ConversationEngine을 통해 붙는 구조로 설계한다.

### 3.2 Conversation Layer (ConversationEngine 인터페이스)
- **책임**
  - 여러 UI 표면(텍스트/음성/API 호출 등)의 입력을 **표준 요청(canonical
    request)**으로 정규화한다.
  - Workspace Core의 응답을 각 표면에 맞는 형태로 변환한다.
  - 향후 Voice/멀티모달 입력을 추가할 때, 이 계층에만 어댑터를 붙이면 되도록
    한다.
- **의존 방향**: UI Surfaces로부터 호출받음(→ 위) / Workspace Core를 호출(→ 아래).
- **구현 시점**: 인터페이스는 Phase 1에서 정의하고, 구체 구현은 이후 Phase에서
  진행한다 (지금 구현하지 않아도 되지만 구조에는 포함).

### 3.3 Workspace Core (최상위 오케스트레이터)
Workspace Core는 **Agent를 관리하는 최상위 오케스트레이터**다. Task를 직접
실행하지 않고 Agent에게 위임한다.
- **책임 (포함)**
  1. **프로젝트 로드** (`ProjectRepository` 통해)
  2. **설정(Config) 로드**
  3. **서비스 초기화** (등록된 Interfaces 구현체 초기화·연결)
  4. **Agent 등록 및 관리** (`AgentManager` 통해)
  5. **Workflow 시작** (`WorkflowEngine` 통해 협업 흐름을 착수)
  6. **Task 분배** (생성된 Task를 직접 처리하지 않고 적절한 Agent에 분배)
  7. **Engine 선택 및 위임** (Agent가 사용할 구현 엔진을 정책에 따라 선택)
  8. **종료(Shutdown)**
- **책임 (제외)**: Task 자체의 실행, Agent 내부 로직, 구현 엔진 직접 호출,
  파일 저장 세부 구현. 이들은 각각 Agent / Engine Adapter / 구체 Repository의
  몫이다.
- **의존 방향**: Conversation Layer로부터 호출받음(→ 위) / `AgentManager`,
  `WorkflowEngine`, `ProjectRepository` 등 **Interfaces에만** 의존(→ 아래).
  어떤 구체 클래스도 직접 알지 못한다.

### 3.4 Agent Manager (AgentManager 인터페이스)
- **책임**
  1. **Agent 생성** (역할별 Agent 인스턴스 생성)
  2. **Agent 생명주기 관리** (생성 → 준비 → 실행 → 대기 → 종료)
  3. **Agent 선택** (Task의 성격/역할/능력에 맞는 Agent 선정)
  4. **Agent 간 협업** (Event Bus를 통한 협업 흐름 조율)
  5. **Agent 상태 관리** (`AgentStatus` 추적)
- **의존 방향**: Workspace Core로부터 호출받음(→ 위) / `AgentRepository`(Agent
  영속화), `EventBus`(협업), 개별 Agent를 관리(→ 아래).

### 3.5 Agents (Planner · Coding · Review · Research · Memory · Automation)
각 Agent는 하나의 `AgentRole`을 가지며, Event 기반으로 동작한다.
- **Planner Agent**: 사용자의 목표를 Task로 분해하고 Workflow를 구성한다
  (`WorkflowEngine`, `TaskEngine` 사용). 완료 시 `TaskCreated` 이벤트 발행.
- **Coding Agent**: 실제 구현을 구현 엔진에 위임한다 (`EngineAdapter` 사용).
  `TaskCreated`를 구독하여 실행, 완료 시 `ReviewRequested` 발행.
- **Review Agent**: 산출물을 검토한다. `ReviewRequested`를 구독, 결과에 따라
  `ReviewApproved` / `ReworkRequested` 발행.
- **Research Agent**: 필요한 정보를 조사한다 (구현 엔진 또는 외부 소스 활용).
- **Memory Agent**: `MemoryEngine`을 사용해 장기 메모리를 큐레이션한다.
- **Automation Agent**: `AutomationEngine`을 사용해 조건/일정 기반 작업을
  트리거한다.
- **의존 방향**: Agent Manager가 생성/관리(→ 위) / `EngineAdapter`, Core
  Engines, `EventBus`를 사용(→ 아래·수평). Agent끼리 **직접 호출하지 않고**
  Event Bus를 통해서만 협업한다.

### 3.6 Event Bus
- **책임**: 이벤트 발행(publish)과 구독(subscribe)을 제공하여 Agent 간 느슨한
  결합을 실현한다. 예: `TaskCreated`, `ReviewRequested`, `ReviewApproved`,
  `ReworkRequested`, `ResultIntegrated`.
- **의존 방향**: Agent Manager와 Agent들이 사용하는 수평적 인프라. 특정 Agent에
  의존하지 않는다.
- **구현 시점**: 구조에는 포함하되 구현은 이후 Phase(멀티 에이전트 코어)에서
  진행한다. Phase 1에서는 `EventBus` 인터페이스만 정의한다.

### 3.7 Domain Services / Core Engines
Task · Workflow · Memory · Approval · Automation Engine. Agent와 Workspace
Core가 사용하는 **능력 서비스**다. (ADR-0005에서 정의한 인터페이스들을 유지한다.)
- **Workflow Engine**: 이제 단순 실행 순서가 아니라 **협업 흐름**을 다룬다
  (§4 참고).
- 나머지 Engine(Task/Memory/Approval/Automation)의 책임은 v0.3.0과 동일하되,
  호출 주체가 "Workspace Core"에서 "Agent 및 Workspace Core"로 확장된다.
- **의존 방향**: Agent/Workspace Core로부터 호출받음(→ 위) / 필요 시
  `EngineAdapter`, 저장소 인터페이스를 사용(→ 아래).

### 3.8 Engine Adapter (확장된 실행 계약)
모든 Agent가 공통으로 사용하는 **실행 계약**이다. `run_task()` 단일 메서드에서
아래와 같은 확장 계약으로 넓힌다 (구체 구현은 Phase 3/엔진 연동 단계).

| 메서드 | 의미 |
|---|---|
| `run(request)` | 구현 엔진에 실행 요청. 실행 핸들/결과를 반환 |
| `cancel(execution_id)` | 진행 중인 실행 취소 |
| `status(execution_id)` | 실행 상태 조회 |
| `capabilities()` | 이 엔진이 지원하는 능력 목록(예: 코드 편집, 검색) |
| `supports_parallel()` | 병렬 실행 지원 여부 (멀티 에이전트 동시 실행 판단용) |
| `estimate_cost(request)` | 실행 전 비용/토큰 추정 (Engine 선택 정책에 사용) |

- **의존 방향**: Agent로부터 호출받음(→ 위) / 실제 구현 엔진을 호출(→ 아래).
- **확장 이유**: 멀티 에이전트 환경에서는 여러 Agent가 동시에 엔진을 사용하므로,
  취소·상태·병렬 지원·비용 추정 같은 운영 계약이 필수다 (ADR-0009).

### 3.9 Implementation Engines (외부)
Claude Code · Codex · Gemini CLI 등. AI Workspace 범위 밖의 실제 실행 주체.

## 4. Workflow 재정의 — 협업 흐름

Workflow는 더 이상 "Task 실행 순서"만을 뜻하지 않는다. 이제 다음을 포함하는
**Agent 협업 흐름**이다.

1. **Task 생성**: Planner Agent가 목표를 Task로 분해한다.
2. **Agent 할당**: 각 Task에 적합한 역할의 Agent를 할당한다 (Agent Manager).
3. **Agent 간 협업**: 할당된 Agent들이 Event Bus를 통해 협업한다.
4. **결과 통합**: 각 Agent의 산출물을 통합하여 최종 결과를 만든다.

### 예시 협업 흐름 (Event 기반)

```
사용자 목표
   │
   ▼
Planner Agent  ──▶  [TaskCreated Event]
                        │
                        ▼
                   Coding Agent  ──(EngineAdapter)──▶ Claude Code
                        │
                        ▼
                   [ReviewRequested Event]
                        │
                        ▼
                   Review Agent
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
     [ReviewApproved]       [ReworkRequested]
             │                     │
             ▼                     ▼
     결과 통합(Workflow)      Coding Agent 재실행
```

## 5. Interfaces (추상 계약)

Phase 1에서 아래 인터페이스를 **계약(추상 클래스/Protocol)으로만** 정의한다.
v0.3.0의 기존 7개를 유지하고, Multi-Agent First를 위해 4개를 추가한다.

| Interface | 계약 책임 | 구체 구현 시점 | 상태 |
|---|---|---|---|
| `ProjectRepository` | 프로젝트 조회/저장 | Phase 1 (FileProjectRepository) | 기존 |
| `WorkflowEngine` | **협업 흐름** 계획/실행 | 이후 Phase | 기존(재정의) |
| `TaskEngine` | Task 생성/상태 전이 | 이후 Phase | 기존 |
| `MemoryEngine` | 장기 메모리 조회/기록 | 이후 Phase | 기존 |
| `ApprovalEngine` | 승인 대상 판별/차단 | 이후 Phase | 기존 |
| `AutomationEngine` | 조건/일정 트리거 | 이후 Phase | 기존 |
| `EngineAdapter` | **확장 실행 계약**(run/cancel/status/…) | Phase 3 | 기존(확장) |
| `AgentManager` | Agent 생성/생명주기/선택/협업/상태 | 이후 Phase | **신규** |
| `AgentRepository` | Agent 조회/저장 | 이후 Phase | **신규** |
| `ConversationEngine` | 입력 표면 정규화(Voice/CLI/API 통합) | 이후 Phase | **신규** |
| `EventBus` | 이벤트 발행/구독 | 이후 Phase | **신규** |

## 6. 도메인 모델

기존 Project / Task / Workflow 에 더해 Agent 관련 모델을 추가한다. Agent는
Workspace의 **핵심 도메인 모델**이다.

| 모델 | 설명 |
|---|---|
| `Project` | 프로젝트 (기존) |
| `Task` | 작업 단위 (기존) |
| `Workflow` | **협업 흐름** (재정의: Task 생성/Agent 할당/협업/결과 통합 포함) |
| `Agent` | 역할과 상태를 가진 실행 주체. `agent_id`, `role`, `status` 등 |
| `AgentRole` | 열거형: `PLANNER`, `CODING`, `REVIEW`, `RESEARCH`, `MEMORY`, `AUTOMATION` |
| `AgentStatus` | 열거형(생명주기): 예) `IDLE`, `RUNNING`, `WAITING`, `PAUSED`, `STOPPED`, `ERROR` |

## 7. 의존성 규칙 (Dependency Rules)

1. UI Surfaces는 **Conversation Layer만** 호출한다.
2. Conversation Layer는 **Workspace Core만** 호출한다.
3. Workspace Core는 §5의 **Interfaces에만** 의존한다 (구체 클래스 직접 참조
   금지). Task를 직접 실행하지 않고 Agent Manager를 통해 Agent에 위임한다.
4. Agent Manager는 `AgentRepository`, `EventBus`, 개별 Agent 인터페이스에
   의존한다.
5. Agent는 `EngineAdapter`, Core Engines, `EventBus`에 의존한다. **Agent끼리
   직접 호출하지 않고 Event Bus를 통해서만 협업한다.**
6. 구현 엔진 호출은 오직 `EngineAdapter`(의 구체 구현체)를 통해서만 이루어진다.
7. Persistence(파일 저장)는 `ProjectRepository` / `AgentRepository` 인터페이스를
   통해서만 접근한다. 저장 형식 변경이 상위 로직에 영향을 주지 않아야 한다.

## 8. 디렉터리 구조와 컴포넌트 매핑

```
src/ai_workspace/
├── domain/            # Project, Task, Workflow, Agent, AgentRole, AgentStatus
├── interfaces/         # 추상 계약 (기존 7 + AgentManager, AgentRepository,
│                       #             ConversationEngine, EventBus)
├── core/              # Workspace Core — 최상위 오케스트레이터 (Interfaces에만 의존)
├── agents/            # Agent Manager + 역할별 Agent 구현체 (이후 Phase)
│   ├── manager.py
│   ├── planner_agent.py
│   ├── coding_agent.py
│   ├── review_agent.py
│   ├── research_agent.py
│   ├── memory_agent.py
│   └── automation_agent.py
├── engines/           # Core Engines 구현체 (Task/Workflow/Memory/Approval/Automation, 이후 Phase)
├── events/            # Event Bus 구현체 + 이벤트 정의 (이후 Phase)
├── conversation/       # Conversation Layer 구현체 (이후 Phase)
├── adapters/          # EngineAdapter 구현체 (Phase 3: claude_code.py, codex.py, gemini_cli.py)
├── storage/           # ProjectRepository/AgentRepository 구체 구현체 (Phase 1~: file 기반)
└── cli/               # CLI 진입점 (UI Surface의 하나)
```

## 9. 확장성 고려사항

- **신규 Agent 추가**: 새 `AgentRole`과 Agent 구현체를 추가하고 Event 구독만
  등록하면 되며, 기존 Agent나 Workspace Core 변경은 필요 없다 (Event 우선).
- **신규 UI 표면 추가 (예: Voice)**: Conversation Layer에 표면 어댑터만
  추가한다. Workspace Core 이하는 변경되지 않는다.
- **신규 구현 엔진 추가**: `EngineAdapter` 계약을 구현하는 클래스를 `adapters/`에
  추가한다.
- **저장소 교체**: `ProjectRepository`/`AgentRepository` 구현체 교체로 충분하다.

## 10. 기술 스택 (제안 — 확정은 각 Phase에서 ADR로)

| 영역 | 제안 | 이유 |
|---|---|---|
| 언어 | Python 3.11+ | 프로젝트 규칙(PEP 8, type hint)과 AI 생태계 친화성 |
| 데이터 모델 | `dataclasses` (필요 시 `pydantic`) | 명시적 스키마와 검증 |
| 인터페이스 | `abc.ABC` / `typing.Protocol` | 표준 방식으로 계약 강제 |
| Event Bus | 인메모리 pub/sub (초기) | 단순 시작, 이후 외부 브로커로 확장 가능 |
| 저장 (Phase 1) | 파일 기반 (Markdown/JSON) | 별도 인프라 없이 시작, 사람이 직접 읽기 용이 |
| UI (Phase 1) | CLI | 가장 단순한 표면, 이후 Dashboard/API/Voice로 확장 |
| 테스트 | `pytest` | Python 표준 관행 |

## 11. 대안 및 트레이드오프

| 대안 | 장점 | 단점 | 채택 여부 |
|---|---|---|---|
| 멀티 에이전트를 선택 기능으로 유지 | 초기 단순 | 나중에 핵심 구조 대수술 필요, 방향과 불일치 | 기각 |
| **멀티 에이전트를 기본 구조로 채택 (Multi-Agent First)** | 방향과 일치, 확장이 자연스러움 | 초기 설계 비용 증가 | **채택** |
| Workspace Core가 Task를 직접 실행 | 경로 단순 | Core 비대·책임 혼재, 멀티 에이전트 불가 | 기각 |
| **Workspace Core는 Agent에 위임하는 오케스트레이터** | 책임 분리, 멀티 에이전트 자연 지원 | 위임 계층 추가 | **채택** |
| Agent 간 직접 호출 | 구현 직관적 | 강결합, Agent 추가/교체 어려움 | 기각 |
| **Event Bus 기반 느슨한 결합** | Agent 독립 추가/교체/테스트, 확장성 | 이벤트 흐름 추적 필요 | **채택** |
| Voice를 Workspace Core에 직접 연결 | 경로 짧음 | 표면마다 Core 수정, 재사용 불가 | 기각 |
| **Voice를 Conversation Layer의 UI로 취급** | 표면 추가가 어댑터 추가로 끝남 | 입력 정규화 계층 필요 | **채택** |
| EngineAdapter를 run_task 단일 계약 유지 | 단순 | 멀티 에이전트 운영(취소/병렬/비용) 불가 | 기각 |
| **EngineAdapter 확장 실행 계약** | 멀티 에이전트 운영에 필요한 제어 확보 | 계약이 커짐 | **채택** |
