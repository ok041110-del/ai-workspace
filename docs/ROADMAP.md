# ROADMAP — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.6.1 |
| 작성일 | 2026-07-24 |
| 상태 | Draft (Task 기반 체계, T1-18 설계 검토 후 T1-18~T1-28로 재분해, ADR-0022) |

## 계층 구조 (Task 기반 체계, ADR-0021)

AI Workspace의 계획은 다음 3단계 계층으로 관리한다. **기존의 Phase 계층은
폐지되었다.**

```
Roadmap
  └─ Milestone   (프로젝트의 큰 목표)
       └─ Task    (실제 구현 단위)
```

> **v0.6.0 변경 (Phase → Task 마이그레이션, ADR-0021)**
> 기존에는 `Milestone → Phase → Task` 4단 계층을 사용했다. Phase는 Milestone과
> Task 사이의 중간 그룹핑이었지만, 실제 운영에서는 다음과 같은 문제가 있었다.
> - Phase 완료 승인이 Milestone 완료 승인과 중복되어 승인 지점이 불필요하게
>   늘어남.
> - Task 하나하나가 이미 "하나의 구현 목표 + 하나의 Commit + 하나의 구현
>   사이클"로 충분히 독립적인데, Phase라는 그룹이 그 위에 한 겹 더 있어 상태
>   추적(어느 Phase의 몇 번째 Task인지)이 이중으로 필요했음.
> - Milestone 2~4는 애초에 Phase 단위로만 목표가 서술되어 있고 개별 Task가
>   정의되지 않아, Phase가 "실제 작업 단위"라기보다 "목표 그룹 설명"에 가까웠음.
>
> 이에 따라 Phase를 폐지하고 `Milestone → Task` 2단 계층으로 단순화한다. 각
> Milestone 안에서 Task는 `T{Milestone 번호}-{일련번호}` 형식으로 일련번호가
> 매겨진다 (예: `T1-01`, `T1-02`, …). 기존 Phase 0/Phase 1의 모든 Task(P0-1~
> P0-11, P1-0~P1-13)는 Milestone 1 소속 `T1-01`~`T1-25`로 그대로 이어진다
> (내용·상태·이력 손실 없음). 마이그레이션 대응표는 `.ai/TASKS.md` 상단과
> 본 문서 하단(§Migration Table)에 기록한다.

각 **Milestone 완료**는 `.ai/RULES.md`의 Approval Required 원칙에 따라 **사용자
승인**을 받아야 다음 Milestone으로 진행한다. (기존에 있었던 "Phase 완료 승인"은
폐지되고, Milestone 완료 승인으로 일원화된다. 단, 이미 지나간 Phase 0/Phase 1
승인 이력은 아래 §Migration Table에 그대로 보존한다.)

## Milestone 개요

| Milestone | 핵심 목표 | 상태 |
|---|---|---|
| M1. 기반 구축 (Foundation) | 문서 체계 + 핵심 도메인(Mission/Step/WorkspaceSession/Agent 포함) + 전체 Interfaces(16종) + Workspace Core 골격 | 진행 중 |
| M2. 멀티 에이전트 코어 (Multi-Agent Core) | Agent Runtime·Event Store·기본 Agent, Core Engines & Context Manager 구현 | 예정 |
| M3. 실행 엔진 연동 & 상호작용 (Engine Integration & Interaction) | Engine Runtime & Engine Adapter(Claude Code 우선) 구현, Interaction Layer 구현 | 예정 |
| M4. 자동화 및 확장 (Automation & Scale) | 다중 프로젝트, 메모리 고도화, 자동화 시나리오 | 예정 |

---

## Milestone 1 — 기반 구축 (Foundation)

**목표**: 문서 체계를 완성하고, Multi-Agent First 구조의 토대가 되는 핵심 도메인
(Project/Mission/Workflow/Task/Step + WorkspaceSession + Agent/AgentRole/
AgentCapability/AgentStatus), 전체 Interfaces(16종), 그리고 Agent Runtime에
위임하는 Workspace Core 골격과 최소 CLI를 확보한다.

**구성**: 문서화 작업(T1-01~T1-11, 구 Phase 0) + 구현 작업(T1-12~T1-28, 구
Phase 1)

**Milestone Definition of Done**
1. `docs/`, `.ai/` 문서 체계가 작성·승인되었다 (T1-01~T1-11).
2. 확장된 도메인 모델, 전체 Interfaces(16종), 세션 생명주기 EngineAdapter 계약,
   Agent Runtime·Engine Runtime 위임형 Workspace Core 골격(WorkspaceSession 관리
   포함), 파일 저장소, 최소 CLI가 동작하며 테스트를 통과한다 (T1-12~T1-28).
3. Multi-Agent First 관련 아키텍처 결정(ADR-0006~0022)이 문서로 확정되어 있다.

**진행 상태**: T1-01~T1-17 완료, T1-18~T1-20 및 T1-21 완료, T1-22~T1-28 진행 예정 (다음 Task: T1-22).
세부 Task 목록/DoD/상태는 `.ai/TASKS.md`의 "Milestone 1" 섹션 참고.

> **2026-07-24 Task 재분해(ADR-0022)**: 설계 검토 결과 원래 하나의 Task였던
> "신규 Interface 정의 및 EngineAdapter 확장"(구 T1-18)이 서로 독립적인 4개
> 아키텍처 하위 계층을 묶고 있어 "Task = 하나의 구현 목표" 원칙에 맞지 않는다고
> 판단, T1-18~T1-21(Agent Runtime / Engine Runtime / Memory / Interaction
> Interfaces) 4개로 분리하고 이후 Task를 T1-22~T1-28로 순연했다.

---

## Milestone 2 — 멀티 에이전트 코어 (Multi-Agent Core)

**목표**: Agent Runtime(Registry/Scheduler/Manager/Event Bus)과 Event Store,
능력별 Agent를 구현하여 실제 멀티 에이전트 협업이 동작하게 하고, Agent가
사용하는 Core Engines를 구현한다.

**Milestone Definition of Done**
1. Agent Runtime이 Agent를 등록/선택(Capability 기준)/스케줄링/생명주기 관리하고,
   Event Bus+Event Store로 Agent 간 협업과 이벤트 기록이 이루어진다.
2. Core Engines(Task/Workflow/Memory/Approval/Automation)가 구현되고, Workflow가
   Mission→Workflow→Task→Step 협업 흐름을 실행한다.
3. Mock EngineAdapter 위에서 Planner→Coding→Review→Documentation 협업 시나리오가
   통과한다.

**예정 작업 영역** (Milestone 1 완료 후 착수 시점에 `T2-01`부터 개별 Task로 정의)
- Agent Runtime & Event Store & 기본 Agent: AgentRegistry/AgentScheduler/
  AgentManager/EventBus/EventStore 구현, Planning·Coding·Review·Documentation
  등 능력별 Agent 골격을 Event 기반으로 동작(실행은 Mock EngineAdapter).
  Scheduler는 Capability로 Agent 선택. DoD: `MissionPlanned`→`CodeCompleted`→
  `ReviewCompleted`→`DocumentationCompleted` 이벤트 흐름이 테스트로 검증되고,
  이벤트가 Event Store에 기록·Replay됨.
- Core Engines & Context Manager 구현: Task/Workflow/Approval/Automation
  Engine 구현. Memory 계열은 **Memory Engine(저장/검색) + Context
  Manager(Context 조립/Snapshot 생명주기)**로 구현. Approval Engine으로 승인
  대상 4행위 차단(ADR-0003 확정). DoD: Mission→…→Step 협업 Workflow가 실제
  Engine 위에서 동작하고, Context Manager가 Snapshot을 생성/복원하며, 승인
  게이트 차단이 테스트로 확인됨.

---

## Milestone 3 — 실행 엔진 연동 & 상호작용 (Engine Integration & Interaction)

**목표**: 실제 구현 엔진(Claude Code 우선)에 Task를 위임하고, 다양한 표면을
통합하는 Interaction Layer를 구현한다.

**Milestone Definition of Done**
1. 세션 생명주기 계약을 만족하는 ClaudeCodeAdapter로 Coding Agent가 실제 Task를
   end-to-end(create_session→run→결과 수집→destroy_session) 수행한다.
2. Interaction Layer가 CLI/API 등 표면 입력을 표준 요청으로 정규화한다.

**예정 작업 영역** (Milestone 2 완료 후 착수 시점에 `T3-01`부터 개별 Task로 정의)
- Engine Runtime & Engine Adapter 구현(Claude Code 우선): **Engine Runtime**
  (엔진 선택/세션 풀/병렬) 구현과, 세션 생명주기 계약(create_session/run/
  cancel/status/destroy_session/capabilities/supports_parallel/estimate_cost)을
  만족하는 ClaudeCodeAdapter 구현, 이후 Codex/Gemini CLI. DoD: Coding Agent가
  Engine Runtime을 거쳐 ClaudeCodeAdapter로 최소 1개 Task를 실제 수행하고
  결과를 통합함.
- Interaction Layer 구현: InteractionEngine 구현으로 CLI/API를 통합.
  Voice/Slack/Webhook 등 추가 표면 대비 구조 확정(표면 자체 구현은 이후). DoD:
  최소 2개 표면(CLI, API)의 입력이 동일한 표준 요청으로 정규화되어 Workspace
  Core에 전달됨.

---

## Milestone 4 — 자동화 및 확장 (Automation & Scale)

**목표**: Automation Engine 기반 자동화, 다중 프로젝트 운용, Memory Engine
고도화.

**예정 작업 영역** (Milestone 3 완료 후 착수 시점에 `T4-01`부터 개별 Task로 정의)
- 자동화·다중 프로젝트·메모리 고도화: Automation Engine이 조건/일정 기반으로
  협업 Workflow(Mission)를 트리거하고, 2개 이상 프로젝트를 동시에 운용하며,
  Memory Engine이 핵심 컨텍스트를 검색/요약/Snapshot 관리한다. DoD: 자동화
  시나리오 1건 이상 동작, 다중 프로젝트 조회, 메모리 검색이 확인됨. (필요 시
  파일→DB 전환은 별도 ADR.)

---

## 우선순위 원칙

1. 기반이 되는 도메인·인터페이스(Milestone 1)를 가장 먼저 확정한다.
2. Multi-Agent First 방향에 따라 Agent 협업 코어(Milestone 2)를 그 다음으로
   우선하고, 실제 엔진 연동과 상호작용 계층(Milestone 3)을 잇는다.
3. 자동화·다중 프로젝트 고도화(Milestone 4)는 핵심 오케스트레이션이 안정화된
   이후에 진행한다.

---

## Migration Table (Phase → Task, 2026-07-24)

Phase 체계 폐지에 따라 기존 Phase 0/Phase 1의 모든 Task를 Milestone 1의 Task로
재번호한다. **내용·완료 상태·이력은 전혀 변경되지 않았으며, ID만 변경되었다.**
세부 내용은 `.ai/TASKS.md`를 참고한다.

| 기존 ID (Phase) | 신규 ID (Task) | 제목 | 상태 |
|---|---|---|---|
| P0-1 | T1-01 | 프로젝트 비전/철학 분석 및 문서 구조 설계 | DONE |
| P0-2 | T1-02 | 디렉터리 구조 생성 | DONE |
| P0-3 | T1-03 | `docs/PRD.md` 작성 | DONE |
| P0-4 | T1-04 | `docs/ARCHITECTURE.md` 작성 | DONE |
| P0-5 | T1-05 | `docs/ROADMAP.md` 작성 | DONE |
| P0-6 | T1-06 | `.ai/RULES.md` 작성 | DONE |
| P0-7 | T1-07 | `.ai/MEMORY.md` 작성 | DONE |
| P0-8 | T1-08 | `.ai/DECISIONS.md` 초기 ADR 작성 | DONE |
| P0-9 | T1-09 | `.ai/TASKS.md` 작성 | DONE |
| P0-10 | T1-10 | `README.md` 작성 | DONE |
| P0-11 | T1-11 | 문서화 완료 승인 요청 (구 "Phase 0 완료 승인 요청") | DONE |
| P1-0 | T1-12 | 구현 착수 승인 요청 (구 "Phase 1 착수 승인 요청") | DONE |
| P1-1 | T1-13 | `src/ai_workspace/` 디렉터리 구조 생성 | DONE |
| P1-2 | T1-14 | 공통 도메인 모델 정의 (Project, Task, Workflow) | DONE |
| P1-3 | T1-15 | Interfaces 정의 (7개) | DONE |
| P1-4 | T1-16 | 도메인 확장 (Mission/Workflow 재정의/Step, WorkspaceSession, Agent 계열, LLM Policy 초안) | DONE |
| P1-5 | T1-17 | Core/Agent/LLM Domain 마무리 및 코드 품질 도구(Ruff/MyPy) 도입 | DONE |
| P1-6 | T1-18~T1-21 | (2026-07-24 ADR-0022로 4개 Task로 재분해 — 아래 표 참고) | TODO |
| P1-7 | T1-22 | Workspace Core 골격 구현 (Agent Runtime 위임형) | TODO |
| P1-8 | T1-23 | 파일 기반 저장소 구현 (ProjectRepository + AgentRepository + EventStore) | TODO |
| P1-9 | T1-24 | CLI 진입점 구성 | TODO |
| P1-10 | T1-25 | 기본 테스트 환경 구축 및 테스트 작성 | TODO |
| P1-11 | T1-26 | `docs/ARCHITECTURE.md` 최종 정합성 확인 | TODO |
| P1-12 | T1-27 | ADR 상태 갱신 (ADR-0002, ADR-0004) | TODO |
| P1-13 | T1-28 | Milestone 1 완료 승인 요청 (구 "Phase 1 완료 승인 요청") | TODO |

Milestone 2~4는 아직 개별 Task로 분해되지 않았으므로(과거에도 "Phase 2 상세
Task는 착수 시점에 정의"였음), 대응표에 포함하지 않는다. 각 Milestone 착수 시점에
`T2-01`, `T3-01`, `T4-01`부터 새로 정의한다.

### 세부 재분해 (ADR-0022, 2026-07-24) — 구 T1-18(단일 Task) → T1-18~T1-21

Phase→Task 이관 직후 `T1-18`은 "신규 Interface 정의 및 EngineAdapter 세션 계약
확장(총 16종)"이라는 단일 Task였다. 설계 검토 결과 서로 의존하지 않는 4개
아키텍처 하위 계층을 묶고 있어 "Task = 하나의 구현 목표"(ADR-0021) 원칙에
어긋난다고 판단해 아래와 같이 재분해했다. **내용은 그대로이며 Task 경계만
나뉘었다.**

| 신규 Task | 포함 Interface | 대응 ARCHITECTURE 절 |
|---|---|---|
| T1-18 Agent Runtime Interfaces | AgentManager, AgentRegistry, AgentScheduler, AgentRepository, EventBus, EventStore | §3.4, §3.5 |
| T1-19 Engine Runtime Interfaces | EngineRuntime, EngineAdapter(확장) | §3.9, §3.10 |
| T1-20 Memory Interfaces | ContextManager, MemoryEngine(재확인, No-Op) | §3.8 |
| T1-21 Interaction Interfaces | InteractionEngine | §3.2 |
