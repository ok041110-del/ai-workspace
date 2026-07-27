# ARCHITECTURE — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.28.0 |
| 작성일 | 2026-07-27 |
| 상태 | Draft (Milestone 1~22 완료, Milestone 23은 "Obsidian Integration & Auto Save"로 재정의(M23-T01/T02 완료) — ADR-0035로 신규 §3.21 Vault Integration Layer 도입. 새 Interface 없이 27종 유지. **M23-T03 완료**: `vault/` 패키지(Path Map/Document Router/Markdown Generator/Vault Writer/VaultSaveEngine) 실제 구현. **M23-T04 완료**: `vault/validation.py`+`vault/auto_save.py`로 저장→Validation→완료 보고를 한 번에 묶는 Auto Save Workflow 추가. **M23-T05 완료**: `vault/sync.py`로 Rename/Delete/Conflict Handling 추가, Version Strategy는 git 기반 유지로 결정) |

이 문서는 `docs/PRD.md`에 정의된 요구사항을 바탕으로 AI Workspace의 구조를 설계한다.
실제 구현이 진행됨에 따라 이 문서와 실제 구조가 항상 일치하도록 갱신한다
(Documentation First 원칙).

> **v0.7.0 변경 사항 (T1-26, 실제 구현과의 정합성 확인)**
> T1-22~T1-25 구현 완료에 따라 문서 상단 상태 표기를 갱신하고, §7 Interface
> 표에서 `ProjectRepository`/`AgentRepository`/`EventStore`가 T1-23에서
> `FileProjectRepository`/`FileAgentRepository`/`FileEventStore`로 실제
> 구현되었음을 반영했다. §9 디렉터리 구조에서 이미 구현된 `core/`/`storage/`/
> `cli/`에 완료 표시를 추가했다. 시스템 구조(컴포넌트·의존성) 자체는 변경
> 없음 — 실제 구현이 기존 설계와 정확히 일치함을 확인한 결과다.
>
> **v0.6.3 변경 사항 (T1-18 설계 검토 및 재분해, ADR-0022)**
> 구 `T1-18`(신규 Interface 16종 정의 및 EngineAdapter 세션 계약 확장)의
> 설계를 검토한 결과, Interface 계약 내용 자체(§3.4~3.10, ADR-0010~0019)는
> 변경할 근거가 없어 그대로 유지하되, 서로 독립적인 4개 하위 계층을 한 Task로
> 묶은 것은 ADR-0021의 "Task = 하나의 구현 목표" 원칙에 맞지 않아 `T1-18`~
> `T1-21`(Agent Runtime / Engine Runtime / Memory / Interaction Interfaces)로
> 분리하기로 함. 이하 Task는 `T1-22`~`T1-28`로 순연됨. 시스템 구조 자체는
> 변경 없음 — §0 참고.
>
> **v0.6.2 변경 사항 (Phase 체계 폐지 → Task 기반 체계, ADR-0021)**
> 프로젝트 관리 체계를 `Milestone → Phase → Task` 4단 계층에서
> `Milestone → Task` 2단 계층으로 전환했다. 이는 소프트웨어 구조 변경이
> 아니라 **개발 프로세스(거버넌스) 변경**이며, §0에 별도로 기술한다. 본
> 문서의 컴포넌트·의존성·디렉터리 구조는 이 변경으로 영향받지 않는다. 기존에
> "Phase 1", "Phase 4" 등으로 표기하던 시점 참조는 이제 해당 작업이 속한
> Milestone과 Task ID로 표기한다 (예: "Phase 1" → "Milestone 1(T1-XX)").
>
> **v0.6.1 변경 사항 (P1-5 — Task-Workflow 관계 보완, ADR-0020)**
> `Task` 도메인 모델에 `workflow_id`(선택 필드)를 추가해 Mission→Workflow→
> Task→Step 계층에서 각 하위 개체가 상위 개체를 참조하는 패턴
> (`Workflow.mission_id`, `Step.task_id`와 동일)을 완성했다. Agent Domain의
> Provider 비의존성과 LLM Domain의 확장 가능한 `LLMModel` 구조(Provider + name
> 조합)는 P1-4 구현이 이미 만족함을 재확인했다 (코드 변경 없음).
>
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

## 0. 개발 프로세스 (Governance — Milestone → Task, ADR-0021)

AI Workspace 저장소 자체의 **개발 관리 체계**는 다음 2단 계층을 따른다 (시스템
아키텍처와는 별개의 프로젝트 관리 개념이다).

```
Roadmap
  └─ Milestone   (프로젝트의 큰 목표. 완료 시 사용자 승인 필요)
       └─ Task    (실제 구현 단위. T{Milestone 번호}-{일련번호}, 예: T1-01)
```

- **Task**는 "하나의 구현 목표 + 하나의 Commit + 하나의 구현 사이클"이 되도록
  설계한다. Task 완료 전 반드시 테스트를 수행한다 (Test Before Complete).
- 예전에는 Milestone과 Task 사이에 **Phase**라는 중간 계층이 있었으나,
  2026-07-24 폐지되었다 (ADR-0021). Phase 완료마다 별도로 요구되던 승인은
  Milestone 완료 승인으로 일원화된다. 기존 Phase 0/Phase 1의 모든 Task는
  Milestone 1의 `T1-01`~`T1-25`로 번호만 이어졌으며 내용·상태·이력은 보존된다
  (`docs/ROADMAP.md`의 Migration Table 참고). 이후 2026-07-24 설계 검토에서
  구 `T1-18`(단일 Task)이 서로 독립적인 4개 하위 계층을 묶고 있음이 확인되어
  `T1-18`~`T1-21`로 추가 분해되었고, 이하 Task가 `T1-22`~`T1-28`로 순연되었다
  (ADR-0022).
- Milestone 2~4처럼 아직 세부 Task로 분해되지 않은 영역은 "예정 작업 영역"으로
  서술하고, 착수 시점에 `T2-01`, `T3-01`, `T4-01`부터 개별 Task를 정의한다
  (Task Driven Development — 너무 이른 시점에 세부 Task를 미리 확정하지 않는다).
- **Task 분해 기준 (ADR-0022)**: Task는 §3의 컴포넌트 절 경계(아키텍처 책임
  경계)를 따라 나눈다. 서로 의존하지 않는 컴포넌트 그룹은 별도 Task로 분리하고,
  서로 강하게 의존하는 컴포넌트(예: EngineRuntime과 EngineAdapter, ContextManager와
  MemoryEngine)는 같은 Task로 묶는다. 다만 "정의 → 구현 → 테스트"는 계속 한
  Task 안에서 완결하며, 이 층위를 Task 단위로 추가 분리하지 않는다.
- 세부 Task 목록/상태는 `.ai/TASKS.md`, Milestone 개요는 `docs/ROADMAP.md`,
  거버넌스 변경 근거는 `.ai/DECISIONS.md`(ADR-0021, ADR-0022)를 참고한다.

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
- **예외(CLI, M4-T03)**: CLI는 argparse로 이미 구조화된 입력(서브커맨드+
  타입 지정 인자)을 제공하므로 자유 텍스트 정규화가 필요 없다. 따라서
  CLI는 Interaction Layer를 거치지 않고 `WorkspaceCore`를 직접 호출하는
  예외적인 Surface다(`cli/main.py`). Voice/Slack/REST API처럼 자유
  텍스트를 받는 Surface가 실제로 추가될 때 이 계층을 거친다.

### 3.2 Interaction Layer (InteractionEngine)
- **책임**: 다양한 입력 표면을 표준 요청(`NormalizedRequest`)으로 정규화하고
  응답을 표면에 맞게 변환(ADR-0013). Voice는 이 계층에 붙는 표면이다.
  모든 Surface(Voice/Slack/REST/Dashboard 등)가 동일한 `NormalizedRequest`
  DTO를 통해 Workspace Core에 전달되어야 이 계층의 가치가 성립한다 — 위
  3.1의 예외(CLI)를 제외하고는 항상 이 계층을 거쳐야 한다.
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
  선택, 병렬 실행 관리, 우선순위·순서 결정. **"병렬 실행 관리"의 의미
  (ADR-0023)**: `select(candidates, capability, max_count)`로 **동시에
  활동할 Agent 후보를 최대 max_count개 선택**하는 정책 결정만 한다 —
  선택된 Agent를 실제로 동시에 실행시키는 메커니즘은 갖지 않는다(그
  메커니즘은 3.9 Engine Runtime의 `run_parallel()` 책임).
  **선택이 실제로 개입을 가르는 자가 확인 가드(Milestone 13)**: M1~M12
  내내 `select()`는 정의만 되어 있고 실제 협업 흐름에서 "선택되지 않은
  Agent는 개입하지 않는다"가 실제로 검증된 적이 없었다. 새 중앙
  디스패처를 두지 않고, `agents/scheduling.py`의
  `is_agent_selected(agent_registry, agent_scheduler, capability,
  agent_id)`로 각 Agent가 처리 직전 스스로 "내가 선택됐나"를 확인하는
  방식을 택했다 — `select()`가 결정적(같은 candidates에 항상 같은 결과)
  이라는 전제 하에, 같은 Capability의 Agent가 여러 개 Event를
  구독하고 있어도 전부 같은 결론에 도달해 실제로는 선택된 하나만
  일한다. `CodingAgent`가 이 가드를 최초로 채택했다(생성자에
  `agent_registry`/`agent_scheduler`를 **선택적**으로 주입 — 기본값
  `None`이면 이 확인을 건너뛰어 기존 동작과 완전히 동일).
- **Agent Manager** (`AgentManager`): Agent 생성/생명주기/상태 관리.
- **Event Bus** (`EventBus`): Event 발행/구독/Agent 간 통신.

### 3.5 Event Store (EventStore 인터페이스) — 독립 Subscriber
- **책임**: Event Bus를 **구독하는 독립 구독자**로서 모든 이벤트를 기록한다.
  다른 구독자(Agent 등)로의 전달 경로에 끼어들지 않으며(게이팅 없음), Replay/
  Audit/Debugging/Workflow 복구를 제공한다 (ADR-0018).
- **의존 방향**: Event Bus를 구독. 다른 구독자와 동등한 위치.
- **구현 시점**: 인터페이스만 Milestone 1, 구현은 이후 Milestone.

### 3.6 Agents (Capability 중심)
- **책임**: 각 Agent는 하나 이상의 **Capability**를 가진다: **Coordination**,
  Planning, Coding, Review, Documentation, Research, Vision, Voice, Git, MCP …
  Agent Scheduler는 엔진 종류가 아니라 Capability로 Agent를 선택한다.
- **Coordination Capability (ADR-0019)**: 여러 Agent의 협업을 조정하는 역할을
  명시한다. Coordination 능력을 가진 Agent(Coordinator)는 Event 흐름을 조율하되,
  다른 Agent를 직접 호출하지 않고 Event 기반 협업 규칙을 따른다. **M5-T06에서
  `CoordinatorAgent`로 최초 구현됨** — `ShellCompleted`(테스트 결과)를 보고
  `ReviewAgent`로 진행시키거나(`CodeVerified`) 실패 시 `CodingAgent`로 되돌리는
  (`MissionPlanned` 재발행) 조건부 분기를 담당한다. Task의 실행 이력(Step,
  ADR-0011)은 Coordinator가 직접 보관하지 않고 `TaskEngine.record_step()`을
  통해 실행 컨텍스트(TaskEngine)에 기록한다.
- **협업**: Agent끼리 직접 호출하지 않고 Event 기반으로 협업(§5).
- **실행**: 실제 일은 **Engine Runtime**을 통해 구현 엔진에 위임하고, Context는
  **Context Manager**로, 도메인 작업은 **Core Engines**로 처리한다.
- **세션 연속성(M8-T03)**: `PlanningAgent`(파이프라인 진입점)는
  `context_manager`/`workspace_session`을 생성자로 주입받는다.
  `plan_mission()` 호출 시 `workspace_session.memory_snapshot_id`가
  비어 있으면 `context_manager.latest_snapshot_id(project_id)`로 그
  project의 최신 Snapshot을 자동 복원한다(이미 값이 있으면 덮어쓰지
  않음). §8 규칙 5(Agent → Context Manager)로 해결하며, Workspace
  Core는 이 로직에 관여하지 않는다(§8 규칙 3·7 무변경).
- **세션 리셋 옵션(M9-T03)**: `plan_mission(..., reset=True)`는 위 자동
  복원을 건너뛴다 — 사용자가 이전 프로젝트 요약을 이어받지 않고 완전히
  새로 시작하고 싶을 때 쓴다. 같은 세션에 이미 있는 `memory_snapshot_id`
  (이어지는 Mission)는 건드리지 않는다 — "새 세션 자동 복원"만 막는
  좁은 범위다.
- **Token & Cost Optimization(M15)**: `CodingAgent`는 선택적으로
  `budget_policy_engine`(§3.13)을 주입받는다. 주입되어 있으면 실행
  직전 예상 비용을 확인해 예산 초과 시 Task를 `BLOCKED`로 전환하고
  실행하지 않는다.
- **Project Knowledge System(M16)**: `CodingAgent`는 선택적으로
  `knowledge_provider`(§3.14)를 주입받는다. 주입되어 있으면
  `task.title`로 관련 Knowledge를 검색해 실행 프롬프트에 반영한다.

### 3.7 Core Engines (Services)
Task · Workflow · Approval · Automation Engine. Agent가 사용하는 능력 서비스.
- **Workflow Engine**: Mission→Workflow→Task→Step 협업 흐름의 실행
  **순서 계획만** 담당한다(`plan()`, side-effect 없는 순수 함수, §4).
  **계획된 순서를 실제로 실행하는 책임은 이 Engine에 없다** — Core
  Engine이 EventBus에 의존하면 Agent → Core Engine 의존 방향(§8)이
  뒤집히기 때문이다. 실행은 §3.12 `WorkflowRunner`가 맡는다
  (Milestone 12).
- **Approval Engine**: 승인 대상 4행위 판별/차단.
- **Automation Engine**: 조건/일정 트리거를 Workflow와 연결(bind)·발동
  (fire)한다(M4-T07). **연결 관리만** 담당하고 `WorkflowEngine`에
  의존하지 않는다 — 언제 발동할지(조건/일정 평가)와 발동된 Workflow의
  실제 실행은 호출자 책임이다. (Agent가 아니라 서비스, ADR-0012.)
- Task Engine: Task 생성/상태 전이.

### 3.8 Memory 계열 — Context Manager + Memory Engine (역할 분리, ADR-0017)
- **Context Manager** (`ContextManager`): Agent에게 제공할 **Context를 조립**하고,
  **Memory Snapshot의 생명주기**(생성/복원)를 관리한다. WorkspaceSession의
  Memory Snapshot은 Context Manager가 소유·관리한다.
- **Memory Engine** (`MemoryEngine`): **저장/검색**만 담당하는 하위 서비스.
  Context Manager가 이를 사용한다.
- **Memory 요약(M7-T01)**: `ContextManager.create_snapshot(session, summary=...)`가
  선택적 `summary` 문자열을 받아 Snapshot 내용에 포함시킨다. **Context
  Manager와 Memory Engine 둘 다 요약을 생성하지 않는다** — 이미 만들어진
  요약 문자열을 전달받아 저장할 뿐이다. 요약을 실제로 만드는 것(LLM 호출)은
  `EngineRuntime`에 접근할 수 있는 Agent 계층의 책임이다(§3.6 Agents,
  `DocumentationAgent` 참고). 저장된 요약은 `MemoryEngine.search()`(M4-T08)
  로도 검색되므로 별도 구현 없이 PRD 7.4 "검색/요약"을 함께 충족한다.
- **세션 연속성(M8-T01)**: `ContextManager.latest_snapshot_id(project_id)`가
  그 project로 가장 최근에 생성된 snapshot_id를 반환한다. 이 "최신"
  포인터는 **`MemoryEngine`을 거치지 않고 Context Manager 내부에서만**
  관리한다 — `MemoryEngine.search()`는 값의 substring 일치로 동작해
  정렬 순서를 계약하지 않으므로, 포인터까지 그 경로로 저장하면 검색
  결과가 오염될 위험이 있다(`memory/context_manager.py` 클래스 docstring
  참고). `PlanningAgent`가 Mission 시작 시 이를 이용해 세션 연속성을
  복원한다(§3.6 Agents 참고) — **Workspace Core는 이 메서드를 호출하지
  않는다**(§8 규칙 7 유지, Memory 접근은 Agent 계층에서만).
- **의존 방향**: Agent → Context Manager → Memory Engine.

### 3.9 Engine Runtime (EngineRuntime 인터페이스, ADR-0016)
Agent Runtime과 Engine Adapter 사이의 계층. 엔진 실행을 관리한다.
- **책임**: **엔진 선택**(capabilities/estimate_cost/supports_parallel 기반),
  **엔진 세션 풀 관리**(Engine Adapter의 create_session/destroy_session 활용),
  **병렬 실행 관리**. **"병렬 실행 관리"의 의미(ADR-0023)**:
  `run_parallel(tasks)`로 **여러 Engine Task 실행을 실제로 동시에
  수행**하는 메커니즘 자체를 책임진다(`ManagedEngineRuntime`은
  `ThreadPoolExecutor` 기반, M4-T06) — 3.4 Agent Scheduler의 "후보 선택"
  과는 다른 층위다: Scheduler는 누구를 동시에 활동시킬지 고르고,
  Engine Runtime은 실제로 여러 실행을 동시에 수행한다.
- **다중 Adapter 등록·선택(M6-T01)**: `ManagedEngineRuntime`은 이름별로
  여러 `EngineAdapter`를 동시에 등록할 수 있다(`register_engine`은 같은
  이름을 재등록할 때만 `DuplicateEngineError`). `run()`/`run_parallel()`은
  `required_capabilities`를 만족하는 등록된 어댑터 중 하나(등록 순서상 첫
  매칭)를 선택해 실행한다 — 복수 매칭 시 우선순위 정책(비용 기반 선택
  등)은 필요성이 증명되지 않아 도입하지 않는다(YAGNI). 이 방식으로
  `LLMPolicyDecision.model.provider`에 따라 Agent가 서로 다른 등록된
  Adapter(capability 태그 기준 `claude_code`/`codex`/`gemini`)를 실행
  시점에 고를 수 있는 기반이 마련된다.
- **Policy→Execution 라우팅(M6-T02)**: `domain/llm_policy.py`의
  `required_capabilities(decision)` 순수 함수가 `LLMProvider`(ANTHROPIC/
  OPENAI/GOOGLE/XAI)를 위 capability 태그로 매핑한다(ANTHROPIC→
  `claude_code`, OPENAI→`codex`, GOOGLE→`gemini`; XAI는 대응 Adapter가
  없어 매칭 실패 시 `NoSuitableEngineError`가 자연히 발생하는 것이 의도된
  동작). `CodingAgent`/`ReviewAgent`/`DocumentationAgent` 3개 Agent가
  `AgentSession.llm_policy_decision`을 이 함수에 넘겨 `engine_runtime.
  run()`의 `required_capabilities`로 전달한다 — 정책이 없으면 빈 집합이
  되어 기존 동작과 하위 호환된다.
- **`run_parallel()` 개별 Task 실패 격리 + 재시도(M10)**: `EngineRuntime.
  run_parallel()` 계약에 "개별 Task 실패는 다른 Task 결과에 영향을 주지
  않는다"는 보장이 명시됐다(M10-T01, 시그니처 불변·docstring 보강).
  `ManagedEngineRuntime`은 `future.result()`를 개별적으로 캐치해 실패한
  Task만 `EngineResult(success=False)`로 변환한다(M10-T02) — 이전에는
  한 Task의 예외가 이미 완료된 다른 Task의 결과까지 통째로 날렸다.
  `RecoveringEngineRuntime.run_parallel()`은 첫 병렬 패스 후 실패한
  Task만 골라 `self.run()`의 기존 재시도 루프로 재실행한다(M10-T03,
  새 재시도 로직 없이 재사용). 요구 Capability를 만족하는 엔진이 아예
  없는 경우(`NoSuitableEngineError`)는 이 격리 대상이 아니라 여전히
  Task 실행 전에 즉시 전파되는 Runtime 자체의 치명적 오류다.
- **Model 라우팅(M14, ADR-0026)**: `run(task, required_capabilities, *,
  model=None)`/`run_parallel(...)`이 `model`을 새 선택 로직 없이 다음
  계층까지 그대로 전달한다(`ManagedEngineRuntime`/
  `RecoveringEngineRuntime`/`InMemoryEngineRuntime` 전부 동일). Provider
  선택(M6, `required_capabilities`)과 달리 **Model은 어떤 Adapter를
  고를지에 관여하지 않고**, 이미 선택된 Adapter에 "이번 호출에서 어떤
  모델을 쓸지"만 전달한다 — 두 축(Provider 선택 vs Model 지정)은 서로
  다른 층위다.
- **비용 사전 조회(M15, ADR-0027)**: `estimate_cost(task,
  required_capabilities=frozenset()) -> CostEstimate`를 계약에 추가했다.
  `EngineAdapter.estimate_cost()`는 M3부터 존재했지만 `EngineRuntime`도
  Agent도 호출한 적이 없었다 — `run()`과 동일한 엔진 선택 규칙으로
  Adapter를 고른 뒤 세션을 만들지 않고 그 Adapter의 `estimate_cost()`
  결과만 반환한다(read-only). `RecoveringEngineRuntime`은 재시도 로직
  없이 내부 Runtime에 순수 위임한다(추정은 side-effect가 없어 재시도할
  이유가 없다). `CodingAgent`가 이를 §3.13 `BudgetPolicyEngine`과
  함께 사용해 실행 전 예산을 확인한다.
- **의존 방향**: Agent로부터 호출받음 / `EngineAdapter`(구체 구현체)를 통해 실제
  엔진과 통신. Agent는 Engine Adapter를 직접 부르지 않고 Engine Runtime을 거친다.

### 3.10 Engine Adapter (per-engine 세션 계약, ADR-0015)
개별 구현 엔진이 구현하는 계약. Engine Runtime이 호출한다.

| 메서드 | 의미 |
|---|---|
| `create_session()` | 엔진 세션 생성 |
| `run(..., model=None)` | 세션 위 실행 요청(Milestone 14: 선택적 model 파라미터) |
| `cancel(...)` | 실행 취소 |
| `status(...)` | 실행 상태 조회 |
| `destroy_session()` | 세션 정리/종료 |
| `capabilities()` | 엔진 능력 목록 |
| `supports_parallel()` | 병렬 실행 지원 여부 |
| `estimate_cost(...)` | 실행 전 비용/토큰 추정 |

**구현체 계열(M5-T05)**: `ClaudeCodeEngineAdapter`(M3-T02, Claude Code 전용,
자체 명령 조립·파싱 보유)와 `CLIEngineAdapter`+`CLIProvider`(Codex/Gemini
CLI 등 여러 CLI 기반 엔진이 공유하는 프레임워크 — `CLIEngineAdapter`가
`EngineAdapter` 계약과 세션 생명주기를 담당하고, `CodexProvider`/
`GeminiCliProvider`가 CLI별 명령 조립·결과 파싱만 다르게 구현) 두 계열이
공존한다. `CLIProvider`는 `adapters/` 내부에서만 쓰이는 협력자로,
`interfaces/`의 보호 자산 목록에는 포함되지 않는다(Agent/WorkspaceCore는
`EngineAdapter`만 알고 `CLIProvider`를 알지 못함). `ClaudeCodeEngineAdapter`
를 이 프레임워크로 통합하는 것은 의도적으로 미룸(기존 안정성 유지) —
`CLIEngineAdapter`가 충분히 검증된 뒤 재검토(M6+).

**ExecutionEnvironment (Milestone 11, ADR-0025)**: `EngineAdapter`가
"무엇을 실행할지"(엔진별 명령 조립·결과 파싱)와 "어디서 실행할지"(로컬
프로세스/향후 원격 컨테이너)를 분리하기 위한 `EngineAdapter` 하위(내부)
인터페이스. `ClaudeCodeEngineAdapter`/`CLIEngineAdapter` 둘 다 구체
구현체를 직접 생성하지 않고 생성자 주입(Dependency Injection)으로
`ExecutionEnvironment`를 받는다(기본값 `LocalExecutionEnvironment`).
`execute(execution_id, command, ...)`/`cancel(execution_id)` 계약이며,
`execution_id`는 특정 실행 방식(OS 프로세스 등)을 가정하지 않는
이름이다. 현재는 기존 `ProcessRunner`(M3-T03)를 그대로 감싸는
`LocalExecutionEnvironment`만 구현되어 있다. `CodespacesExecutionEnvironment`
/`ReplitExecutionEnvironment`/`DockerExecutionEnvironment` 등은 실제
요구사항이 생길 때까지 구현하지 않는다(YAGNI) — 새 구현체를 추가할 때
`EngineAdapter` 코드를 전혀 수정할 필요가 없도록 설계되었다(OCP).
`ExecutionEnvironment`는 `CLIProvider`처럼 `adapters/`·`interfaces/`
내부에서만 쓰이는 협력자이며, Agent/Engine Runtime은 이 인터페이스의
존재를 알지 못한다 — Task→Agent→Engine Runtime→Engine Adapter라는
기존 최상위 흐름(§2)은 그대로 유지된다.

**Model 라우팅(Milestone 14, ADR-0026)**: `run()`의 `model` 인자는
Provider 선택(위 M6-T02 라우팅)과 다른 층위다 — Provider는 "어떤
Adapter를 쓸지"를 정하고, Model은 "이미 정해진 Adapter에게 어떤
모델을 쓰라고 지시할지"를 정한다. 지금은 `ClaudeCodeEngineAdapter`만
`model`을 실제로 `--model` 실행 인자에 반영한다(`run()`에 전달된
값이 생성자의 고정 `model`보다 우선) — `MockEngineAdapter`/
`CLIEngineAdapter`(Codex/Gemini)는 받되 사용하지 않는다(Codex/Gemini
는 이 환경에 CLI가 없어 검증 불가, M5-T05/M10에서 반복 확인). Effort
(low/medium/high)는 대응하는 실제 실행 지점이 아직 없어 이번
Milestone 범위에서 뺐다 — 실제 대응 지점이 생기면 재검토한다.

### 3.11 Implementation Engines (외부)
Claude Code · Codex · Gemini CLI 등.

### 3.12 Workflow Runner (Milestone 12, Workflow Automation)
`Workflow`에 속한 여러 Task를 `WorkflowEngine.plan()`이 계산한 순서대로
사람 개입 없이 순차 실행하는 조율자(`WorkflowRunner`). Agent도 아니고
Core Engine도 아닌 별도 컴포넌트다.
- **Agent가 아닌 이유**: Multi-Agent 선택/조정(ADR-0019 Coordination
  Capability)과는 다른 관심사다 — `AgentRuntime`/`AgentScheduler`를
  전혀 사용하지 않는다. 이번 Milestone은 의도적으로 Multi-Agent
  선택·Routing·병렬 실행·Retry·Approval을 범위 밖에 둔다.
- **Core Engine이 아닌 이유**: `WorkflowEngine`은 Agent보다 하위 계층
  서비스라 EventBus를 알면 안 된다(§8). `WorkflowRunner`는 그 위에서
  `WorkflowEngine.plan()` + `EventBus` + `TaskEngine` 세 Interface를
  조합할 뿐인 조율자다(`EngineApprovalPipeline`, M3-T05와 같은 패턴).
- **동작**: `plan()`이 반환한 순서대로 각 task_id에 `MissionPlanned`
  Event를 발행한다. `EventBus.publish()`는 계약상 예외를 던지지 않으므로
  (구독자 예외는 Bus가 내부에서 격리, §7), 실패 감지는 오직
  `TaskEngine.get_task(task_id).status`가 `DONE`인지로만 판단한다 —
  `DONE`에 도달하지 못하면(예: 재작업 소진) 그 자리에서 Workflow 실행을
  중단하고 이후 Task는 실행하지 않는다.
- **전제 조건**: `workflow.task_ids`의 모든 Task는 호출 전에 이미
  `TaskEngine.create_task()`로 생성되어 있어야 한다 — `WorkflowRunner`
  는 Task를 새로 만들지 않는다.

### 3.13 Budget Policy (BudgetPolicyEngine 인터페이스, Milestone 15, ADR-0027)
`EngineAdapter.estimate_cost()`가 계산한 예상 비용/토큰을 Workspace
차원의 예산과 대조해 실행 허용 여부를 결정하는 계약. `LLMPolicyEngine`
(§3.9 Policy→Execution 라우팅)과 동일한 설계 원칙을 따른다 — 규칙
기반, side-effect 없음, 정책이 없으면(`Budget` 미설정) 예외가 아니라
항상 허용으로 표현해 정책 부재가 정상 상태임을 나타낸다.
- **domain 객체**: `Budget(max_tokens, max_cost_usd)`(둘 다 선택적,
  Provider 독립) / `BudgetDecision(allowed, reason)`.
- **구현체**: `InMemoryBudgetPolicyEngine` — 생성 시 주어진 단일
  `Budget` 하나로 `CostEstimate`를 검사한다. 여러 Task에 걸친 누적
  소비량 추적은 하지 않는다(Task 단위 개별 확인만, YAGNI).
- **연동 지점**: `CodingAgent`에 `budget_policy_engine`을 선택적으로
  주입하면, `MissionPlanned`를 처리하기 직전 `engine_runtime.
  estimate_cost()` → `BudgetPolicyEngine.check()`를 거친다. 예산을
  초과하면 Approval 요청이나 재시도 없이 Task를 `BLOCKED`로 전환하고
  실행하지 않는다(M15 MVP — 승인 흐름은 범위 밖). 주입하지 않으면
  (기본값 `None`) 이 확인 자체를 건너뛰어 M15 이전과 완전히 동일하게
  동작한다.
- **Provider 독립**: 이 Interface와 `Budget`/`BudgetDecision` 어디에도
  특정 LLM Provider나 Engine 개념이 등장하지 않는다 — Claude/GPT/
  Gemini 어떤 조합이든 동일하게 동작한다.

### 3.14 Knowledge Layer — Project Knowledge System (Milestone 16, ADR-0028)
프로젝트의 기존 문서(ARCHITECTURE/DECISIONS/RULES/TASKS/ROADMAP/PRD)를
Workspace 전용 Knowledge로 노출하고, Agent가 Keyword 기반으로 검색해
실행 컨텍스트에 참고하게 하는 계층. **§3.8 Memory 계열(`MemoryEngine`)
과는 완전히 다른 개념**이다 — `MemoryEngine`은 Mission 요약/세션
연속성(대화·세션 기억)을 다루고, Knowledge Layer는 **프로젝트가 이미
갖고 있는 정적 문서**를 다룬다. 이름과 역할을 섞지 않기 위해 별도
컴포넌트 계열로 신설했다(ADR-0028).
- **저장(`KnowledgeRepository`)**: 문서를 어디서 읽어오는지 아는
  유일한 계층. `FileKnowledgeRepository`(M16-T01)는 고정 파일→
  `KnowledgeKind` 매핑(`docs/ARCHITECTURE.md`→ARCHITECTURE,
  `.ai/DECISIONS.md`→ADR, `.ai/RULES.md`→RULE, `.ai/TASKS.md`→TASK,
  `docs/ROADMAP.md`/`docs/PRD.md`→PROJECT)으로 파일 하나를
  `KnowledgeDocument` 하나로 노출한다(문단 단위 파싱 없음, YAGNI).
- **검색(`KnowledgeSearch`)**: `KnowledgeRepository`의 문서를 대상으로
  Keyword(포함) 검색만 한다(`InMemoryKnowledgeSearch`, 기존
  `MemoryEngine.search()`와 동일한 단순성). Vector/Embedding/Semantic
  Search는 다루지 않는다. 문서 수가 적어 영속 `KnowledgeIndexer`는
  이번 범위에서 제외했다(YAGNI) — 필요해지면 `KnowledgeSearch` 계약은
  그대로 두고 구현체만 교체하면 된다(OCP).
- **제공(`KnowledgeProvider`)**: **Agent가 Knowledge에 접근하는 유일한
  진입점**(`InMemoryKnowledgeProvider`가 `KnowledgeSearch`에 위임).
  `ContextManager`가 `MemoryEngine`을 감싸 Agent에게 노출하는 것과
  동일한 패턴 — Agent는 `KnowledgeRepository`/`KnowledgeSearch`를
  직접 호출하지 않는다.
- **연동 지점**: `CodingAgent`에 `knowledge_provider`를 선택적으로
  주입하면, `task.title`로 `KnowledgeProvider.provide()`를 호출해
  검색 결과를 `DevelopmentContext.related_knowledge`에 실어 실행
  프롬프트에 반영한다. 미주입 시(기본값 `None`) 검색 자체를
  건너뛰어 M16 이전과 완전히 동일하게 동작한다.
- **Memory는 LLM을 호출하지 않는다**: `KnowledgeSearch`/
  `KnowledgeProvider` 어디도 LLM을 호출하지 않는다 — Keyword 검색
  결과를 그대로 반환/전달할 뿐이다.
- **의존 방향**: Agent → Knowledge Provider → Knowledge Search →
  Knowledge Repository(§8 의존성 규칙에 신규 추가).

### 3.15 Intelligent Engine Selection (Milestone 17, ADR-0029)
Task + Budget(§3.13) + Project Knowledge(§3.14) + 등록된 Engine들의
Capability/비용을 종합해 **최적 Engine 후보를 결정**만 하는 계층.
**Decision Only Milestone** — 이 계층의 결정은 실제 실행(어떤 Engine
으로 `engine_runtime.run()`을 호출할지)에 전혀 연결되지 않는다. 실행
연결은 Milestone 18의 책임이다.
- **`EngineRegistry`(신규, `AgentRegistry`와 동일 설계)**: 등록된
  `EngineAdapter`가 무엇인지 조회하는 계약(`register`/`get`/
  `list_candidates`). **`EngineRuntime`의 실행 계약(run/
  estimate_cost)은 전혀 확장하지 않았다** — `EngineRuntime`은
  `list_candidates()` 이전부터 이미 자체 dict로 Adapter를
  등록·관리하고 있었고, 이번에도 그 내부 구현은 손대지 않는다.
  대신 후보 조회가 필요한 쪽이 같은 Adapter를 조립 시점에
  `EngineRegistry`에도 등록해 별도로 조회한다(같은 Adapter를 두
  곳에 등록하는 약간의 중복은 있으나, `EngineRuntime`의 실행 경로를
  전혀 건드리지 않아 회귀 위험이 0이다).
- **`list_candidates(task, required_capabilities)`**: `required_
  capabilities`를 만족하는 **등록된 모든** Engine을 `EngineCandidate`
  (engine_name/capabilities/estimated_tokens/estimated_cost_usd/
  supports_parallel)로 나열한다. `EngineRuntime.run()`/
  `estimate_cost()`가 "첫 매칭 하나"만 고르는 것과 달리, 이 계층은
  "비교 가능한 후보 여럿"을 제공하는 것이 존재 이유다. 세션을 생성
  하지 않는다(각 Adapter의 `estimate_cost(task)`만 호출).
- **`EngineSelectionPolicy`(신규)**: `Task`/`EngineCandidate` 목록/
  선택적 `BudgetPolicyEngine`/선택적 Knowledge 목록을 받아 규칙
  기반으로 판단만 하는 계약(`LLMPolicyEngine`/`BudgetPolicyEngine`과
  동일한 설계 원칙 — side-effect 없음, LLM 호출 없음). 후보가 어디서
  왔는지(`EngineRegistry`)는 알지 못한다 — 조회(Registry)와 판단
  (Policy)의 책임을 분리했다(SRP, 사용자 승인 조건).
- **`InMemoryEngineSelectionPolicy`(최소 구현)**: `budget_policy_
  engine`이 주어지면 각 후보의 `estimated_tokens`/`estimated_cost_usd`
  로 `CostEstimate`를 만들어 `BudgetPolicyEngine.check()`에 그대로
  위임(M15 재사용, 예산 비교 로직을 중복 구현하지 않음) — 예산 내
  후보 중 `estimated_cost_usd`(동률이면 `estimated_tokens`)가 가장
  낮은 후보를 선택한다. Knowledge는 결정 사유(`reason`)에만 참고로
  반영하고 후보를 걸러내는 데는 쓰지 않는다(MVP 범위, Model 수준
  결정도 범위 밖 — 계속 M14의 정적 정책이 담당).
- **결정과 실행의 분리(핵심 경계, 통합 테스트로 증명됨)**: `CodingAgent`
  는 `EngineSelectionPolicy`/`EngineRegistry`를 전혀 모른다 — 생성자에
  해당 파라미터가 없다. `EngineSelectionPolicy`가 다른 Engine을
  추천하더라도, 실제 `EngineRuntime`에 등록된 Adapter와 기존
  "첫 매칭" 규칙(§3.9)이 실행을 그대로 결정한다.
- **의존 방향**: 이 계층을 호출하는 주체(현재는 §3.16
  `ExecutionDispatcher`와 통합 테스트) → `EngineRegistry`(후보 조회) +
  `EngineSelectionPolicy`(판단). `EngineRuntime`과는 독립적인 경로다.

### 3.16 Execution Layer — ExecutionDispatcher / Authentication (Milestone 18, ADR-0030)
M17의 `EngineSelectionDecision`을 실제 실행으로 연결하는 계층.
`Task → Selection Policy → EngineSelectionDecision → ExecutionDispatcher
→ AuthenticationManager → EngineRegistry → EngineAdapter →
ExecutionEnvironment → AI Engine 실행 → EngineExecutionResult`가
Workspace가 실제로 수행할 수 있는 첫 End-to-End 실행 경로다(M11
ExecutionEnvironment/M15 Budget/M16 Knowledge/M17 Selection이 실행까지
연결됨).
- **`ExecutionDispatcher`(구체 클래스, Interface 아님)**: `EngineRegistry`
  /`EngineAdapter`/`AuthenticationManager` **Interface만** 사용해
  특정 Provider(Claude/Gemini/Codex/GPT/Ollama)를 직접 분기하지
  않는다(OCP — 새 Engine 추가 시 `EngineRegistry`/`EngineAdapter`/
  Authentication 구현체만 추가하면 되고 이 클래스는 수정하지 않는다).
  `dispatch(decision, task) -> EngineExecutionResult`가 유일한
  진입점이다. `ExecutionEnvironment`를 직접 생성하지 않는다 —
  `EngineAdapter`(예: `ClaudeCodeEngineAdapter`)가 이미 M11부터
  생성자 주입으로 갖고 있다.
- **Decision과 Execution의 완전한 분리**: `ExecutionDispatcher`는
  `EngineSelectionDecision`만 입력받고 `EngineSelectionPolicy`를
  전혀 참조하지 않는다. 반대로 `EngineSelectionPolicy`도
  `ExecutionDispatcher`를 전혀 모른다(코드 검증됨, M18-T03). `decision`
  이 `None`이면 `EngineRegistry`/`AuthenticationManager` 어느 쪽도
  호출하지 않고 즉시 `EngineExecutionResult(success=False, ...)`를
  반환한다 — "선택된 것이 없다"는 정상 입력으로 취급한다.
- **`AuthenticationManager`(신규 Interface)**: "실행 가능한 인증
  상태인지 **확인**"만 담당한다 — `is_authenticated(engine_name)`/
  `authentication_status(engine_name)`만 제공하고 `login()`/`logout()`
  은 이 계약에 없다. 이미 인증되어 있으면 `ExecutionDispatcher`가
  즉시 실행하고, 인증되어 있지 않으면 `AuthenticationRequiredError`
  를 던진다(정상 실패로 취급하는 "Decision 없음"과 달리, 인증 실패는
  전제조건 위반이라 예외로 표현). `InMemoryAuthenticationManager`는
  실제 로그인/OAuth/API Key/Credential 저장/Token Refresh를 전혀
  다루지 않는다 — 생성 시 주어진 "인증된 것으로 간주할 Engine 이름"
  집합만 보관한다. Workspace는 CLI 로그인 명령을 직접 실행하지
  않는다(실제 로그인 기능은 후속 Milestone).
- **`EngineExecutionResult`(domain, Provider 독립)**: success/output/
  error/engine/execution_time(+ M19에서 retry_count/cancelled/
  timed_out 확장, §3.17). `interfaces/execution_environment.py`의
  `ExecutionResult`(OS 프로세스 결과 — returncode/stdout/stderr)와는
  이름·개념이 다르다 — 혼동 방지를 위해 별도로 명명했다.
- **`CodingAgent`는 수정하지 않는다**: M18은 `ExecutionDispatcher`를
  독립적으로 구현·검증했다(사용자 확정). Agent 파이프라인 연결은
  후속 Milestone의 책임이다.
- **의존 방향**: (현재는 호출 주체 없음, 통합 테스트가 직접
  호출) `ExecutionDispatcher` → `RetryExecutor`(§3.17) →
  `AuthenticationManager` + `EngineRegistry` → `EngineAdapter` →
  `ExecutionEnvironment`(기존 M11 경로 그대로).

### 3.17 Reliability — Retry / Timeout / Cancellation (Milestone 19, ADR-0031)
`ExecutionDispatcher`(§3.16)의 안정성을 확보하는 계층. Reliability는
Execution 위에서 동작한다 — `ExecutionDispatcher`는 재시도 로직을
직접 구현하지 않고 `RetryExecutor`에 위임한다(사용자 설계 원칙 1).
- **`RetryPolicy`(M3부터 존재, M19에서 확장)**: `max_attempts`(M3)
  에 `retry_delay_seconds`/`non_retryable_exceptions`(둘 다 기본값
  있음)를 추가했다 — 이름을 새로 만들지 않고 **같은 개념을
  확장**했다(M16 `MemoryEngine`/M18 `ExecutionResult`가 겪은 "다른
  개념인데 이름이 겹침"과는 반대로, 이번엔 실제로 같은 개념이라
  확장이 맞는 선택이었다). `RecoveringEngineRuntime`(M3/M10, 무조건
  재시도)은 새 필드를 쓰지 않아 전혀 영향받지 않는다.
  `decide(exception) -> RetryDecision`이 재시도 가능 여부를
  판단한다(도메인 계층은 구체 예외 타입을 몰라도 되도록
  `type[BaseException]` 튜플만 다룬다).
- **`RetryExecutor`(신규, 구체 클래스)**: `Callable[[], T]`를 받아
  `RetryPolicy`대로 재시도하는 범용 메커니즘 — `EngineExecutionResult`
  를 전혀 알지 못한다(제네릭). `ExecutionDispatcher`는 "인증 확인→
  Registry 조회→Adapter 실행" 전체를 한 번의 시도로 묶어 넘긴다
  (사용자 Architecture 다이어그램대로 `RetryExecutor`가
  `AuthenticationManager`보다 앞에 위치) — 그래서
  `AuthenticationRequiredError`/`EngineNotRegisteredError`/
  `NoSuitableEngineError`도 재시도 루프 "안"에 있지만,
  `RetryPolicy.non_retryable_exceptions`에 기본 포함되어 있어 첫
  시도에서 즉시 실패한다(재시도 없음).
- **`NoSuitableEngineError`는 이 경로에 실제로 나타나지 않는다**:
  `EngineRuntime` 시절 예외인데, `ExecutionDispatcher`는
  `EngineRuntime`을 건너뛰고 `EngineRegistry`를 직접 쓴다(M18) —
  실제로 발생하는 것은 `EngineNotRegisteredError`다. 둘 다 기본
  재시도 불가 목록에 포함해 뒀다(전방 호환, 해가 없음).
- **취소(Cancellation)**: `EngineAdapter`(예: `ClaudeCodeEngineAdapter`)
  가 이미 쓰는 sentinel(`EngineResult.error == "cancelled"` —
  `ExecutionEnvironment.ExecutionResult.cancelled`이 Adapter 내부에서
  이미 이 값으로 인코딩됨)을 그대로 재사용해 판정한다(사용자 승인
  조건 — 새 문자열 규칙을 만들지 않음). 취소는 예외가 아니라 정상
  반환값이므로 재시도 루프를 타지 않고 즉시
  `EngineExecutionResult.cancelled=True`로 반영된다.
- **⚠️ 기술 부채: `timed_out`은 완전한 구분이 불가능한 휴리스틱이다**:
  `ClaudeCodeEngineAdapter.run()`은 Timeout과 다른 실행 오류(예: CLI
  파일 없음)를 **모두 같은 예외 타입**(`EngineExecutionError`)으로
  던지고, 메시지 텍스트로만 구분된다. 이번 Milestone은 "`EngineAdapter`
  인터페이스를 변경하지 않는다"는 제약이 있어 이 문제를 근본적으로
  고칠 수 없다 — `_looks_like_timeout()`이 Timeout 메시지의 한국어
  마커 문자열("응답하지 않았습니다")을 찾는 방식으로만 판정한다.
  Adapter가 메시지 문구를 바꾸면 이 판정은 깨진다. 근본 해결은
  `EngineAdapter`(또는 `EngineExecutionError`)에 Timeout 여부를
  구조적으로 표현하는 후속 Milestone이 필요하다(ADR-0031에 정식
  기록).
- **의존 방향**: `ExecutionDispatcher` → `RetryExecutor`(순수 재시도
  메커니즘, `EngineExecutionResult`를 모름) → (인증 확인→Registry
  조회→Adapter 실행을 하나의 시도로 묶은 클로저).

### 3.18 Real-time Dashboard Platform (Milestone 20, ADR-0032)
CQRS Read Model — Dashboard는 Task를 실행하지 않고 오직 조회만
한다. Workspace 현황/엔진 현황/실행 현황/최근 실행 내역/안정성
현황 5개 영역을 실시간으로 보여준다(Event 기반 갱신, Polling 없음).
- **`domain/dashboard.py`**: `EngineStatus`(READY/RUNNING/
  AUTH_REQUIRED/ERROR), `WorkspaceStatus`, `ExecutionRecord`,
  `ExecutionStats`, `ReliabilityStats`. `EngineExecutionResult`
  (M18/M19)를 그대로 참조하지 않고 필요한 필드만 옮겨 담는다 —
  Dashboard는 Execution 계층에 대한 쓰기 접근이 없다.
- **Event(`runtime/execution/events.py`)**: `ExecutionDispatcher`
  (§3.16)가 `ENGINE_EXECUTION_STARTED`/`ENGINE_EXECUTION_COMPLETED`/
  `ENGINE_AUTHENTICATION_FAILED`를 발행한다. `ExecutionDispatcher`는
  `event_bus: EventBus | None = None`을 선택적으로 주입받고,
  Event를 발행할 뿐 Dashboard의 존재를 전혀 모른다(§8 규칙 12).
- **`DashboardRepository`(Interface, 신규 26번째)**: 쓰기
  (`record_execution_started`/`record_execution_completed`/
  `record_authentication_failure`, Event 구독 경로 전용)와 읽기
  (`workspace_status`/`engine_statuses`/`recent_executions`/
  `execution_stats`/`reliability_stats`, `DashboardService` 경로
  전용)를 한 Interface에 함께 정의한다(ADR-0032 — 구현체가 하나뿐이라
  분리는 과설계로 판단).
- **`InMemoryDashboardRepository`(`runtime/dashboard/`)**: 생성자에서
  스스로 `event_bus.subscribe()`한다. 통계는 조회 시점에 계산하지
  않고 매 Event마다 미리 갱신해 둔다("Dashboard는 통계를 계산하지
  않는다", 사용자 설계 원칙). 최근 실행 이력은 100건으로 제한한다.
- **`DashboardService`(`runtime/dashboard/`)**: `DashboardRepository`를
  조합해 조회에 응답하는 순수 서비스. **`web/`을 전혀 import하지
  않는다**(M20-T06에서 `ast` 기반 검증으로 증명) — 동일한 Read
  Model을 향후 다른 Presentation(M23 Mobile 등)이 재사용할 수 있게
  한다. `KNOWN_ENGINES` 목록으로 아직 실행되지 않은 Engine도 기본
  상태(`READY`)로 채운다.
- **`web/`(신규 최상위 패키지, Infrastructure 계층, 이 프로젝트
  최초의 서버/외부 런타임 의존성)**: `DashboardViewModel`(한국어
  라벨 DTO — Engine 이름만 예외로 영어 유지) +
  `DashboardBroadcaster`(WebSocket 연결 관리, `EventBus` 구독,
  연결 시점에 캡처한 `asyncio.get_running_loop()`에
  `loop.call_soon_threadsafe()`로 동기 이벤트 콜백→비동기 전송 경계를
  넘김) + FastAPI `routes.py`(`/api/dashboard`, `/api/summary`,
  `/api/history`, `/api/engines`) + `app.py`(`create_app`, `/health`,
  `/ws/dashboard`, `StaticFiles` 정적 마운트) + `server.py`
  (`build_app`/`run_server`, 앱 조립과 실제 소켓 기동을 분리해
  `TestClient`로 테스트 가능) + `static/`(`index.html`/`style.css`/
  `app.js`, 빌드 도구 없는 Vanilla JS). 현재 시각·경과 시간
  (`현재 시각 - started_at`)은 브라우저가 1초마다 직접 계산한다 —
  서버는 Polling하지 않는다.
- **`cli/main.py`의 `start` 서브커맨드**: `--host`/`--port`로
  `web.server.run_server`를 지연 import해 호출한다 — 기존 CLI
  명령은 FastAPI/uvicorn 설치 여부와 무관하게 그대로 동작한다.
- **의존 방향**: `ExecutionDispatcher` → (Event 발행, `EventBus`만
  앎) ⇢ `InMemoryDashboardRepository`(스스로 구독) →
  `DashboardService` → `web/`(REST/WebSocket/정적 UI). Core 계층
  (`domain`/`interfaces`/`engines`/`runtime`, `runtime/dashboard/`
  포함)은 FastAPI/uvicorn을 모른다 — 오직 `web/`만 안다(ADR-0032).

### 3.19 Automation Engine (Milestone 21, ADR-0033)
사용자의 명시적 요청 없이 조건/일정에 따라 Task를 자동 실행하는
시스템. Dashboard와 독립적인 Domain이며, `ExecutionDispatcher`를
통해서만 Task를 실행하고 `EventBus`/Dashboard는 그대로 재사용한다.

> **M4-T07 `AutomationEngine`과의 관계**: 이름이 비슷하지만 다른
> 개념이다. `AutomationEngine`(`interfaces/automation_engine.py`)은
> "trigger_id가 어떤 Workflow와 연결돼 있는가"만 관리하는 연결
> 관리 계약이고, trigger가 **언제** 발동해야 하는지 판단(조건/일정
> 평가)과 실제 실행은 원래부터 호출자 책임으로 명시돼 있었다. M21은
> 그 떠넘겨진 책임을 처음 구현한다 — `AutomationEngine`은 수정 없이
> 그대로 유지된다(M16 `KnowledgeRepository`/M18 `EngineExecutionResult`
> 와 같은 "이름은 유사하지만 다른 개념" 패턴).

```text
AutomationRule
    │
    ▼
AutomationRepository
    │
    ▼
AutomationService (CRUD 유일 진입점)
    │
    ▼
AutomationScheduler (Trigger 평가 오케스트레이션, Infrastructure)
    │
    ▼
AutomationActionExecutor → ExecutionDispatcher (유일한 실행 진입점)
    │
    ▼
EventBus → Dashboard (Reader → Reader)
```

- **`domain/automation.py`**: `TriggerKind`(TIME/INTERVAL/EVENT/
  STARTUP)/`Trigger`, `ActionKind`(RUN_TASK/RUN_WORKFLOW/
  DASHBOARD_REFRESH/NOTIFICATION)/`Action` — 둘 다 kind로 태그된
  Flat 구조(`ExecutionRecord`(M20)와 동일 스타일). `AutomationRule`
  은 `last_executed_at`/`next_execution_at`을 포함하는 가변
  엔티티(`Task`와 동일 패턴, `enable()`/`disable()`) — M23 Mobile
  Experience가 그대로 재사용할 수 있도록 이 필드를 도메인에 내장해
  둔다.
- **`AutomationRepository`(Interface, 신규 27번째)**: `get`/`save`
  (upsert)/`delete`/`list_rules` — `ProjectRepository`와 동일한
  스타일. `InMemoryAutomationRepository`가 최소 구현체.
- **`AutomationService`(`runtime/automation/`)**: Rule CRUD의 유일한
  진입점(사용자 승인 조건 3) — Action을 실제로 실행하지 않는다.
- **`TriggerEvaluator` 계층(`runtime/automation/trigger_evaluator.py`)**:
  "지금 발동해야 하는가"/"다음 예정 시각"을 전담(사용자 승인 조건
  1 — Scheduler와 Trigger 책임 분리). `TimeTriggerEvaluator`(요일/
  일자 제약, 같은 날 중복 발동 방지)/`IntervalTriggerEvaluator`
  (`last_executed_at` 또는 `created_at` 기준 경과 시간)/
  `StartupTriggerEvaluator`(`last_executed_at is None`으로 최초
  1회만)/`EventTriggerEvaluator`(사전 필터링된 뒤 호출되므로 항상
  발동).
- **`AutomationScheduler`(`runtime/automation/`, Infrastructure
  Layer)**: Rule을 별도로 등록/보관하지 않고 매 `tick()`/`start()`
  /Event 수신마다 `AutomationRepository`를 다시 조회한다 —
  `AutomationService`가 같은 Repository로 CRUD하면 자동 반영되어
  별도 동기화가 필요 없다. `start()`(Startup Trigger 1회), `tick(now)`
  (Time/Interval Trigger, 순수 함수라 고정 시각으로 결정적 테스트
  가능), `bind_event_bus(event_bus)`(Event Trigger 구독),
  `run_now(rule_id)`(Trigger 조건 무시, 즉시 발동 — API의 `/run`이
  위임). Action 실행 실패는 `InMemoryEventBus.publish()`와 동일한
  원칙으로 삼켜(swallow) 다른 Rule 평가에 영향을 주지 않는다.
- **`AutomationActionExecutor`(`runtime/automation/`)**: RUN_TASK를
  M17/M18 파이프라인(`EngineSelectionPolicy.select()` →
  `ExecutionDispatcher.dispatch()`)에 그대로 실어 실행한다(사용자
  승인 조건 5 — 새 실행 경로를 만들지 않음). DASHBOARD_REFRESH/
  NOTIFICATION은 실행할 Task가 없어 아무것도 하지 않는다.
  RUN_WORKFLOW는 이번 Milestone이 Task 단위 실행 경로만 다뤄
  `AutomationActionNotSupportedError`로 아직 지원하지 않는다(후속
  Milestone 이월).
- **Dashboard 연계(Reader → Reader)**: `DashboardService`가 선택적
  으로 `automation_service`를 주입받아(M15/M16과 동일한 선택적 DI
  패턴) `AutomationService.list_rules()`(읽기 전용)만 호출해
  `AutomationStatus`(등록/활성 Rule 수, 마지막/다음 실행 시각)를
  집계한다. Dashboard는 Automation을 제어하지 않는다(사용자 승인
  조건 4) — `ExecutionDispatcher`(Writer)가 Dashboard를 직접
  참조하는 것은 여전히 금지되지만, 두 Reader(`DashboardService`/
  `AutomationService`)가 서로 참조하는 것은 CQRS 위반이 아니다.
- **`web/automation_routes.py`**: Automation REST API 8종(목록/
  조회/생성/수정/삭제/활성화/비활성화/즉시 실행). Web UI(정적
  HTML/CSS/Vanilla JS)는 이 API만 사용해 Rule을 생성·수정·삭제·
  활성화한다.
- **Server Runtime 연동**: `web/app.py`의 `create_app()`이
  `lifespan` Context Manager로 서버 기동 시 `AutomationScheduler.
  start()`를 호출하고, 서버가 살아 있는 동안 `automation_tick_seconds`
  (기본 30초)마다 `tick()`을 도는 백그라운드 asyncio Task를 두어
  종료 시 정리한다 — "Scheduler는 Server Runtime과 함께 실행된다".
- **의존 방향**: `AutomationScheduler`(EventBus 구독) →
  `AutomationActionExecutor` → `ExecutionDispatcher`(Automation을
  전혀 모름, 단방향) → `EventBus` → `InMemoryDashboardRepository`
  (기존 M20 경로 그대로). `DashboardService` → `AutomationService`
  (읽기 전용). Automation Core(`domain`/`interfaces`/`runtime/
  automation/`)는 `web/`이나 FastAPI/uvicorn을 모른다(ADR-0033).

### 3.20 Production Platform (Milestone 22, ADR-0034)
Server Runtime의 생명주기(Lifecycle)/설정(Configuration)/상태
(Health)/Logging을 담당한다. 비즈니스 로직을 추가하지 않는다 —
Execution/Dashboard/Automation은 그대로 유지한다. **새 최상위
Interface를 추가하지 않는다** — 아래 3개 컴포넌트 전부 구체
클래스/dataclass다.

```text
                    Workspace Server
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
Configuration      Lifecycle Manager      Health Monitor
      │                    │                    │
      └──────────────┬─────┴──────────────┬─────┘
                     ▼                    ▼
               Dashboard             Automation
                     │                    │
                     ▼                    ▼
               ExecutionDispatcher    EventBus
```

- **`ProductionConfig`(`runtime/production/config.py`)**: `host`/
  `port`/`log_level`/`dashboard_enabled`/`automation_enabled`/
  `automation_tick_seconds`/`engine_settings`를 담는 **Immutable**
  객체(frozen dataclass, 사용자 승인 조건 1 — Infrastructure
  Layer). `load_production_config()`(`config_loader.py`)가
  기본값→설정 파일(YAML)→Environment Variable(`AI_WORKSPACE_`
  접두사) 순으로 겹쳐 쓴다 — `storage/llm_policy_loader.py`와
  동일하게 로더만 PyYAML/`os.environ`을 안다.
- **Production Logging(`logging_setup.py`)**: `ProductionConfig.
  log_level`로 표준 `logging.Logger`(`ai_workspace`)를 설정한다
  (Console 항상, File 선택). `domain`/`interfaces`/`engines`는
  이 모듈을 참조하지 않는다 — Logging은 Domain에 침투하지 않는다.
- **`LifecycleManager`(`lifecycle.py`)**: `STARTUP`/`RUNNING`/
  `SHUTDOWN` 상태만 관리하고 **컴포넌트를 생성하지 않는다**
  (사용자 승인 조건 2 — 조립은 `web/server.py`의 `build_app()`
  책임). `startup()`이 `started_at`을 기록하고
  `AutomationScheduler.start()`를 호출한다. `shutdown()`은
  `DashboardService.workspace_status()`(M20이 이미 Event로 추적)를
  폴링해 실행 중 Task 완료를 기다리되, 타임아웃을 넘겨도 **강제로
  개입하지 않는다**(Graceful Shutdown, 강제 종료 없음).
- **`HealthMonitor`(`health.py`)**: **조회 전용**(사용자 승인
  조건 3, Read Model) — Server(`LifecycleManager.state` 기반)/
  Dashboard/Automation/EventBus/Engine 5개 컴포넌트를 "연결돼
  있는가"로 판정하고 가장 나쁜 상태로 전체 `health_status`
  (HEALTHY/DEGRADED/UNHEALTHY)를 집계한다. Engine 항목은
  `EngineRegistry` Interface를 확장하지 않고 구조적 연결 여부만
  본다(실제 Engine 등록 여부는 범위 밖, M21부터의 알려진 한계).
  `ProductionStatus`가 사용자 승인 조건 5의 4개 표준 필드
  (`health_status`/`version`/`started_at`/`uptime_seconds`)를
  담아 M23이 그대로 재사용할 수 있게 한다.
- **`WORKSPACE_VERSION`(`version.py`)**: 제품 릴리스 버전 —
  `pyproject.toml`의 `version`(ADR-0024의 아키텍처 기준선 버전)과
  별개 개념이다. `get_git_commit_hash()`는 실패해도 `None`을
  반환해 Version API가 항상 동작한다.
- **Dashboard Health(Reader→Reader 확장)**: **기존
  `DashboardService`를 확장**해 구현한다(사용자 승인 조건 4) —
  선택적 `health_monitor` DI + `production_status()`(M21
  `automation_service`와 동일한 패턴). `HealthMonitor`/
  `LifecycleManager`는 `TYPE_CHECKING` 가드로 `DashboardService`를
  타입 힌트로만 참조해 런타임 순환 import를 피한다. `HealthMonitor`
  생성에는 이미 만들어진 `DashboardService`가 필요하므로,
  `DashboardService.attach_health_monitor()`(생성 후 연결)로 조립
  순서 문제를 푼다 — 실제 순환 의존은 아니다.
- **Production API(`web/production_routes.py`)**: `GET /api/health`
  (컴포넌트별 상세)/`GET /api/config`(비밀값 없어 그대로 노출)/
  `GET /api/version`/`GET /api/status`(4개 표준 필드만 담은 경량
  요약, `/api/health`의 상세와 분리). `web/app.py`의
  `create_app()`은 `production_config`/`lifecycle_manager`/
  `health_monitor` 3개 모두 주입해야만 이 라우터를 등록한다.
- **Server Runtime 연동**: `web/server.py`의 `build_app()`이
  `config` 미지정 시 `load_production_config()`로 채우고
  `LifecycleManager`/`HealthMonitor`까지 조립한다. `run_server()`
  는 CLI `host`/`port`가 주어지면 Configuration보다 우선하고,
  `configure_logging()` 호출 뒤 `uvicorn.run()`한다.
- **의존 방향**: Core Domain(`domain`/`interfaces`/`engines`)은
  Production을 전혀 모른다. `runtime/production/`은 `web/`이나
  FastAPI/uvicorn을 모른다 — 실제 라우트는 `web/production_routes.py`
  에서만 조립한다(ADR-0034).

### 3.21 Vault Integration Layer (Milestone 23, ADR-0035, M23-T02 설계 + M23-T03 구현)

Obsidian Vault(`Vault/`)로의 문서 저장을 자동화하는 계층. **Core
Domain·`web/` 양쪽 모두 이 계층을 모르고, 이 계층도 Core Domain에
의존하지 않는다** — Production Platform(§3.20)이 지킨 "위 계층이
아래 계층을 모른다"는 원칙과 반대 방향으로 완전히 독립된, AI
Workspace 개발 과정을 돕는 도구 계층이다(제품 기능이 아님).

```text
GitHub 원문(.ai/TASKS.md, .ai/DECISIONS.md, .ai/MEMORY.md,
             docs/ARCHITECTURE.md, docs/ROADMAP.md)
        │  구조화 입력(kind, title, summary, related_docs, source_paths)
        ▼
  Document Router  ──►  Vault Directory Mapping(kind → 대상 파일)
        │
        ▼
  Markdown Generator  ──►  99 Templates/의 해당 Template로 렌더링
        │
        ▼
  Vault Writer  ──►  File Creator(신규) / File Updater(기존 파일의
                      대상 섹션만 치환, 전체 재작성 금지)
        │
        ▼
        Vault/ (git-tracked Markdown)
```

- **패키지 위치**: `vault/`(신규, `storage/`와 나란히 존재하되
  대상이 다름 — `storage/`는 도메인 객체 JSON 영속성, `vault/`는
  Task/ADR/Decision/Design/Implementation/API 등 산출물의 Markdown
  동기화).
- **Vault Directory Mapping**: `AI_RULES`의 Tag Rule 11종과 1:1
  대응하는 kind→디렉터리 고정 매핑(코드가 아니라 데이터). 상세
  매핑표는 ADR-0035 참고.
- **File Strategy**: 신규 문서는 전체 생성, 기존 Index 문서는
  대상 섹션만 치환 — 과거 수작업으로 채운 내용을 보존한다. 내용이
  실제로 바뀔 때만 파일을 쓴다.
- **구현 상태(M23-T03)**: `vault/models.py`(`VaultDocumentKind`/
  `VaultDocumentRequest`), `vault/mapping.py`(`VAULT_DIRECTORY_MAP`),
  `vault/router.py`(`DocumentRouter`), `vault/markdown_generator.py`
  (`render_section`/`render_daily_file`), `vault/writer.py`
  (`VaultWriter` — 신규 파일 생성/기존 섹션 upsert), `vault/
  engine.py`(`VaultSaveEngine`, Save Flow 전체를 잇는 진입점)로
  구현 완료.
- **구현 상태(M23-T04, Auto Save Workflow)**: `vault/validation.py`
  (`find_broken_backlinks`/`find_missing_tags` — AI_RULES의 Backlink
  Rule/Tag Rule을 코드로 확인), `vault/auto_save.py`(`run_auto_save`
  — 여러 `VaultDocumentRequest`를 저장하고 Vault 전체 Backlink +
  새로 만든 파일의 Tag를 검증해 `AutoSaveReport`(저장/미변경/
  Validation 실패 목록 + `summary()` 완료 보고 문구)를 돌려줌)로
  구현 완료. `pytest` 27개(T03 18 + T04 9), `ruff`/`mypy` 클린.
- **구현 상태(M23-T05, Vault Synchronization)**: `vault/sync.py`
  — `rename_document()`(파일명 변경 + Vault 전체 Backlink `[[..]]`/
  `[[..|별칭]]`/`[[..#절]]` 일괄 갱신), `delete_document()`(다른
  문서가 아직 참조 중이면 기본적으로 거부, `force=True`일 때만
  삭제 — Orphan Backlink 방지), `content_hash()`+`VaultWriter.
  upsert_section(expected_hash=...)`(Conflict Handling — 저장
  시점 사이 파일이 바뀌면 `VaultConflictError`로 실패, 조용히
  덮어쓰지 않음). **Version Strategy**: 별도 버전 관리 시스템을
  새로 만들지 않고 `Vault/`가 이미 git으로 버전 관리되는 사실을
  그대로 쓰기로 결정(최소 복잡성 원칙). Link/Backlink Validation은
  M23-T04의 `find_broken_backlinks()`를 그대로 재사용.
- **범위 밖(계속)**: 자연어 명령 라우팅(M23-T06), 실행 환경 연동
  검증(M23-T07).

## 4. Mission → Workflow → Task → Step 계층 (ADR-0011)

```
Mission (사용자 목표) → Workflow (협업 흐름) → Task (Agent 할당 작업) → Step (세부 실행)
```

**Step의 실질 반영(M5-T06)**: `Step`은 T1-16에서 도메인만 정의된 채 오래
쓰이지 않았으나(M2 Retrospective 이월 부채 #6), 이제 `TaskEngine.
record_step()`/`get_steps()`로 Task의 실행 시도 이력(예: 재작업 시도)을
기록하는 데 실제로 쓰인다. 별도 StepEngine/Repository는 두지 않고(YAGNI),
Task를 소유하는 `TaskEngine`이 Step도 함께 관리한다.

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
| `Workflow` | Mission 수행 협업 흐름 (`mission_id`로 상위 Mission 참조) |
| `Task` | Agent에게 할당되는 작업 (`workflow_id`로 상위 Workflow 참조, 선택 필드) |
| `Step` | Task 내부 세부 실행 단위 (`task_id`로 상위 Task 참조) |
| `WorkspaceSession` | 현재 실행 상태(현재 프로젝트/Mission/활성 Workflow/활성 Agent/Memory Snapshot/Engine Session) |
| `Agent` | 능력을 가진 실행 주체 |
| `AgentRole` | Agent 역할 유형 |
| `AgentCapability` | Coordination/Planning/Coding/Review/Documentation/Research/Vision/Voice/Git/MCP … |
| `AgentStatus` | 생명주기 상태 |

## 7. Interfaces (추상 계약, 총 27종)

| Interface | 계약 책임 | 구현 시점 | 상태 |
|---|---|---|---|
| `AutomationRepository` | `AutomationRule` 저장/조회(CRUD는 `AutomationService`가 유일하게 사용) | Milestone 21 (M21-T01 계약, `InMemoryAutomationRepository` 구현) | **완료(계약+구현)** |
| `DashboardRepository` | Execution 결과를 Event로 받아 Dashboard Read Model에 기록 + 조회 | Milestone 20 (M20-T01 계약, `InMemoryDashboardRepository` 구현) | **완료(계약+구현)** |
| `LLMPolicyEngine` | AgentRole별 LLM Provider/Model/Effort Rule 기반 결정 | Milestone 5 (M5-T01) | **완료(계약+구현)** |
| `BudgetPolicyEngine` | `CostEstimate` vs `Budget` 대조로 실행 허용 여부 결정 | Milestone 15 (M15-T01 계약, `InMemoryBudgetPolicyEngine` 구현) | **완료(계약+구현)** |
| `KnowledgeRepository` | 프로젝트 문서를 `KnowledgeDocument`로 조회 | Milestone 16 (M16-T01 계약, `FileKnowledgeRepository` 구현) | **완료(계약+구현)** |
| `KnowledgeSearch` | `KnowledgeRepository` 문서의 Keyword 검색 | Milestone 16 (M16-T02 계약, `InMemoryKnowledgeSearch` 구현) | **완료(계약+구현)** |
| `KnowledgeProvider` | Agent가 Knowledge에 접근하는 유일한 진입점 | Milestone 16 (M16-T02 계약, `InMemoryKnowledgeProvider` 구현) | **완료(계약+구현)** |
| `EngineRegistry` | 등록된 `EngineAdapter` 조회 + Capability 만족 후보 나열 | Milestone 17 (M17-T01 계약, `InMemoryEngineRegistry` 구현) | **완료(계약+구현)** |
| `EngineSelectionPolicy` | Task/Budget/Knowledge/후보를 종합해 최적 Engine 판단(Decision Only) | Milestone 17 (M17-T02 계약, `InMemoryEngineSelectionPolicy` 구현) | **완료(계약+구현)** |
| `AuthenticationManager` | Engine별 실행 가능한 인증 상태 확인(`login`/`logout` 없음) | Milestone 18 (M18-T01 계약, `InMemoryAuthenticationManager` 구현) | **완료(계약+구현)** |
| `ProjectRepository` | 프로젝트 조회/저장 | Milestone 1 (T1-15 계약, T1-23 `FileProjectRepository` 구현) | **완료(계약+구현)** |
| `WorkflowEngine` | Mission→…→Step 협업 흐름 | 이후 | 기존 |
| `TaskEngine` | Task 생성/상태 전이 + Step 실행 이력(M5-T06) | 이후 | 기존 |
| `MemoryEngine` | Memory 저장/검색 (Snapshot 제외) | Milestone 1 (T1-15, T1-20 재확인) | 기존(축소, 변경 없음) |
| `ApprovalEngine` | 승인 대상 판별/차단 | 이후 | 기존 |
| `AutomationEngine` | trigger_id↔Workflow 연결 관리(`bind_workflow`/`fire`, M4-T07) — §3.19 Automation Engine(M21)과는 다른 개념, 그대로 유지 | Milestone 1 (T1-15), M4-T07 확장 | **완료(계약+구현)** |
| `EngineAdapter` | per-engine 세션 계약 (create_session/run/cancel/status/destroy_session/capabilities/supports_parallel/estimate_cost) | Milestone 1 (T1-19) 계약, Milestone 3 구현 | **완료(계약)** |
| `AgentManager` | Agent 생성/생명주기/상태 | Milestone 1 (T1-18) | **완료(계약)** |
| `AgentRepository` | Agent 조회/저장 | Milestone 1 (T1-18 계약, T1-23 `FileAgentRepository` 구현) | **완료(계약+구현)** |
| `AgentRegistry` | Agent 등록/조회/제거 | Milestone 1 (T1-18) | **완료(계약)** |
| `AgentScheduler` | Capability 기준 선택/병렬/우선순위 | Milestone 1 (T1-18) | **완료(계약)** |
| `InteractionEngine` | 입력 표면 정규화/응답 변환 (기존 ConversationEngine 대체) | Milestone 1 (T1-21) 계약, Milestone 3 구현 | **완료(계약)** |
| `EventBus` | 이벤트 발행/구독 | Milestone 1 (T1-18) | **완료(계약)** |
| `EventStore` | 이벤트 기록(독립 구독자)/Replay/Audit | Milestone 1 (T1-18 계약, T1-23 `FileEventStore` 구현) | **완료(계약+구현)** |
| `EngineRuntime` | 엔진 선택/세션 풀/병렬 실행/비용 사전 조회(M15) | Milestone 1 (T1-19) | **완료(계약)** |
| `ContextManager` | Context 조립 / Memory Snapshot 생명주기 | Milestone 1 (T1-20) | **완료(계약)** |
| `ExecutionEnvironment` | `EngineAdapter` 하위(내부): 명령을 실제로 실행할 장소 추상화 (execute/cancel) | Milestone 11 (M11-T01 계약, M11-T02 `LocalExecutionEnvironment` 구현) | **완료(계약+구현)** |

> **참고**: "완료(계약)"은 Interface 정의와 Fake 기반 계약 테스트만 존재하고
> 실제 서비스에 쓰일 구체 구현체는 아직 없다는 뜻이다(각 컴포넌트의 계획된
> Milestone에서 구현 예정). "완료(계약+구현)"은 `storage/`의 파일 기반
> 구현체까지 존재해 CLI 등에서 실제로 쓰이고 있다는 뜻이다.

## 8. 의존성 규칙 (Dependency Rules)

1. UI Surfaces → Interaction Layer만 호출.
2. Interaction Layer → Workspace Core만 호출.
3. Workspace Core → Agent Runtime, Engine Runtime, Interfaces에만 의존. Task를
   직접 실행하지 않고 Agent Runtime에 위임.
4. Agent Runtime 컴포넌트는 서로 및 해당 인터페이스, `AgentRepository`에 의존.
5. Agent는 **Core Engines, Context Manager, Engine Runtime, Event Bus,
   Knowledge Provider**에 의존. Agent끼리 직접 호출 금지(Event Bus만).
6. **Engine 호출은 Agent → Engine Runtime → Engine Adapter → 구현 엔진** 순서로만
   이루어진다. Agent가 Engine Adapter를 직접 부르지 않는다.
7. **Memory 접근은 Agent → Context Manager → Memory Engine** 순서로만 이루어진다.
   Memory Snapshot은 Context Manager가 관리한다.
8. **Event Store는 Event Bus의 독립 구독자**다. 다른 구독자로의 전달을 가로막지
   않는다.
9. Memory/Automation은 Agent가 아니라 Core Engine(서비스)이다.
10. Persistence는 `ProjectRepository`/`AgentRepository`/`EventStore` 인터페이스를
    통해서만 접근한다.
11. **Project Knowledge 접근은 Agent → Knowledge Provider → Knowledge Search →
    Knowledge Repository** 순서로만 이루어진다(Milestone 16). Agent는
    Knowledge Search/Knowledge Repository를 직접 호출하지 않는다 — §8
    규칙 7(Memory 접근)과 같은 층위이나 완전히 별도의 경로다.
12. **Dashboard 갱신은 `ExecutionDispatcher` → Event Bus → `DashboardRepository`
    (구독)** 순서로만 이루어진다(Milestone 20). `ExecutionDispatcher`는
    `DashboardRepository`를 직접 참조하지 않는다(CQRS 쓰기측 독립).
    `web/`(API/WebSocket/Web UI)은 오직 `DashboardService`(읽기)만
    호출하고, `domain`/`interfaces`/`engines`/`runtime`(Core 계층)은
    `web/`이나 FastAPI/uvicorn을 참조하지 않는다 — 이 프로젝트에서
    프레임워크를 아는 유일한 계층은 `web/`이다.
13. **Automation Rule 실행은 `AutomationScheduler` → `AutomationActionExecutor`
    → `ExecutionDispatcher`** 순서로만 이루어진다(Milestone 21).
    `AutomationScheduler`는 `EventBus`를 구독할 뿐 Dashboard를 직접
    참조하지 않는다. Automation CRUD는 `AutomationService`(API 전용
    진입점)를 통해서만 이루어진다 — `AutomationScheduler`는 Rule을
    직접 생성/수정/삭제하지 않고 조회만 한다.
14. **Dashboard의 Automation 조회는 `DashboardService` → `AutomationService`
    (읽기 전용)** 순서로만 이루어진다(Milestone 21) — Reader가 다른
    Reader를 참조하는 것은 CQRS 위반이 아니다(§8 규칙 12의 "쓰기측이
    읽기측을 모른다"는 방향성만 유지하면 된다). Dashboard는
    `AutomationService`의 조회 메서드만 호출하고 Automation을
    제어하지 않는다.
15. **Core Domain(`domain`/`interfaces`/`engines`)은 Production을
    전혀 모른다**(Milestone 22). `runtime/production/`(Configuration
    /Lifecycle Manager/Health Monitor/Logging)은 `web/`이나
    FastAPI/uvicorn을 참조하지 않는다 — 실제 REST 엔드포인트는
    `web/production_routes.py`에서만 조립한다.
16. **Dashboard Health 조회는 `DashboardService` → `HealthMonitor`
    (읽기 전용)** 순서로만 이루어진다(Milestone 22) — §8 규칙 14와
    동일한 Reader→Reader 패턴. `HealthMonitor`/`LifecycleManager`는
    `DashboardService`를 타입 힌트로만 참조해(`TYPE_CHECKING`)
    런타임 순환 import를 만들지 않는다.
17. **`LifecycleManager`는 컴포넌트를 생성하지 않는다**(Milestone
    22) — 조립은 항상 `web/server.py`의 `build_app()`이 전담하고,
    `LifecycleManager`는 이미 조립된 컴포넌트의 Startup/Shutdown
    순서만 조율한다.

## 9. 디렉터리 구조와 컴포넌트 매핑

```
src/ai_workspace/
├── domain/            # Project, Mission, Workflow, Task, Step,
│                       #   WorkspaceSession, Agent, AgentRole, AgentCapability, AgentStatus
│                       #   (구현됨, T1-14~T1-17)
├── interfaces/         # 추상 계약 (27종, §7) (구현됨, T1-15~T1-21, M11-T01, M15-T01/T02, M16-T01/T02, M17-T01/T02, M18-T01, M20-T01, M21-T01)
├── core/              # Workspace Core (WorkspaceSession 관리, Runtime 초기화)
│                       #   (구현됨, T1-22)
├── runtime/           # (Milestone 2 이후)
│   ├── agent/         #   Agent Runtime: registry, scheduler, manager
│   ├── engine/        #   Engine Runtime: 선택/세션 풀/병렬
│   │                   #   + engine_registry.py (InMemoryEngineRegistry, Milestone 17)
│   ├── execution/     #   ExecutionDispatcher: Decision -> Execution 연결 (Milestone 18)
│   │                   #   + retry_executor.py (RetryExecutor, Milestone 19)
│   │                   #   + events.py (Dashboard Event 상수, Milestone 20)
│   ├── dashboard/     #   InMemoryDashboardRepository + DashboardService
│   │                   #   (Read Model, Core 계층, web/을 모름, Milestone 20)
│   │                   #   + 선택적 AutomationService DI (Milestone 21)
│   ├── automation/    #   InMemoryAutomationRepository + AutomationService
│   │                   #   + trigger_evaluator.py(TriggerEvaluator 계층)
│   │                   #   + AutomationScheduler + AutomationActionExecutor
│   │                   #   (Dashboard와 독립적인 Domain, web/을 모름, Milestone 21)
│   ├── production/    #   ProductionConfig/config_loader.py/logging_setup.py
│   │                   #   + LifecycleManager + HealthMonitor + version.py
│   │                   #   (Infrastructure Layer, web/을 모름, Milestone 22)
│   └── workflow/      #   WorkflowRunner: Workflow 순차 자동 실행 (Milestone 12)
├── agents/            # 능력별 Agent 구현체 (Milestone 2 이후)
├── engines/           # Core Engines 구현 (Task/Workflow/Approval/Automation, Milestone 2 이후)
│                       #   + knowledge_search.py/knowledge_provider.py
│                       #   (InMemoryKnowledgeSearch/InMemoryKnowledgeProvider, Milestone 16)
│                       #   + engine_selection_policy.py
│                       #   (InMemoryEngineSelectionPolicy, Milestone 17)
│                       #   + authentication_manager.py
│                       #   (InMemoryAuthenticationManager, Milestone 18)
├── memory/            # Context Manager + Memory Engine 구현 (Milestone 2 이후)
├── events/            # Event Bus + Event Store 구현 (Milestone 2 이후)
├── interaction/        # Interaction Layer 구현 (Milestone 3 이후)
├── adapters/          # EngineAdapter 구현 (Milestone 3: claude_code.py, codex.py, gemini_cli.py)
│                       #   + local_execution_environment.py (ExecutionEnvironment
│                       #   구현, Milestone 11)
├── storage/           # FileProjectRepository/FileAgentRepository/FileEventStore
│                       #   (구현됨, T1-23) + FileKnowledgeRepository (Milestone 16)
├── vault/             # Vault Directory Mapping/Document Router/
│                       #   Markdown Generator/Vault Writer/
│                       #   VaultSaveEngine (구현됨, M23-T02/T03,
│                       #   ADR-0035) + validation.py/auto_save.py
│                       #   (Auto Save Workflow, M23-T04) +
│                       #   sync.py(Rename/Delete/Conflict, M23-T05)
│                       #   — Core Domain·web/을 모두 모름, Milestone 23
├── web/               # Infrastructure 계층 — FastAPI/uvicorn을 아는 유일한 곳
│                       #   (Milestone 20): dashboard_viewmodel.py, routes.py,
│                       #   dashboard_broadcaster.py, app.py, server.py,
│                       #   static/(index.html/style.css/app.js, 빌드 도구 없음)
│                       #   + automation_routes.py(Automation REST API 8종,
│                       #   Milestone 21) — static/에 Automation 화면 추가
│                       #   + production_routes.py(Production API 4종,
│                       #   Milestone 22) — static/에 Production 현황 추가
└── cli/               # CLI 진입점 (UI Surface의 하나) — main.py (구현됨, T1-24)
│                       #   + start 서브커맨드로 web.server.run_server 지연 import (Milestone 20)
│                       #   + --host/--port 기본값 None(미지정 시 Configuration 값 사용, Milestone 22)
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

## 11. 기술 스택 (제안 — 각 Milestone에서 ADR로 확정)

| 영역 | 제안 | 이유 |
|---|---|---|
| 언어 | Python 3.11+ | 프로젝트 규칙(PEP 8, type hint) |
| 데이터 모델 | `dataclasses` (필요 시 `pydantic`) | 명시적 스키마 |
| 인터페이스 | `abc.ABC` / `typing.Protocol` | 표준 계약 강제 |
| Event Bus/Store | 인메모리 pub/sub + append-only 파일 로그 | 단순 시작, 이후 확장 |
| 저장 (Milestone 1) | 파일 기반 (Markdown/JSON) | 별도 인프라 없이 시작 |
| UI (Milestone 1) | CLI | 가장 단순한 표면 |
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
