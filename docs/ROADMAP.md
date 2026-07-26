# ROADMAP — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.13.0 |
| 작성일 | 2026-07-25 |
| 상태 | Draft (Milestone 1~6 완료, v0.5.0 아키텍처 기준선 선언, Milestone 7 구현+Review 완료 — 사용자 승인 대기) |

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
| M1. 기반 구축 (Foundation) | 문서 체계 + 핵심 도메인(Mission/Step/WorkspaceSession/Agent 포함) + 전체 Interfaces(16종) + Workspace Core 골격 | **완료 (2026-07-25 사용자 승인)** |
| M2. 멀티 에이전트 코어 (Multi-Agent Core) | Agent Runtime·Event Store·기본 Agent, Core Engines & Context Manager 구현 | **완료 (2026-07-25 사용자 승인)** |
| M3. 실행 엔진 연동 & 상호작용 (Engine Integration & Interaction) | Engine Runtime & Engine Adapter(Claude Code 우선) 구현 | **완료 (2026-07-25 사용자 승인)** — Interaction Layer·Coding Agent 실제 경로 통합은 M4로 공식 이관 |
| M4. 자동화 및 확장 (Automation & Scale) | 다중 프로젝트, 메모리 고도화, 자동화 시나리오 | **완료 (2026-07-26 사용자 승인)** — v0.5.0 아키텍처 기준선 선언(ADR-0024) |
| M5. 실제 개발 수행 (Real Development Execution) | LLM Policy Engine, DevelopmentContext+Agent 강화, ShellAgent, Multi-Engine(Codex/Gemini), Workflow 조건부 분기 | **완료 (2026-07-26 사용자 승인)** |
| M6. Policy 기반 실행 라우팅 (Policy-Driven Engine Routing) | `LLMPolicyDecision`에 따라 실제 등록된 `EngineAdapter`(Claude Code/Codex/Gemini CLI)를 자동 선택해 실행 — RULES §7 로드맵의 "Policy Engine 자동 선택" 단계 완성 | **완료 (2026-07-26 사용자 승인)** |
| M7. Memory 요약 (Memory Summarization) | `DocumentationAgent`의 Engine 실행 결과를 Memory Snapshot 요약으로 저장 — PRD 7.4 "검색/요약" 갭 완성 | **구현+Review 완료 (2026-07-26) — 사용자 승인 대기** |

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

**진행 상태**: T1-01~T1-28 전체 완료. **2026-07-25 사용자 승인으로 Milestone 1
종료.** 다음은 Milestone 2 목표/DoD 확정 후 `T2-01`부터 착수 (세부 Task는
착수 시점에 정의).
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

**구성**: T2-01~T2-08 (8개 Task. 2026-07-25 Milestone 1 완료 승인 직후
T2-01~T2-07(7개)로 확정했으나, T2-01 실제 착수 시 범위가 좁아져(아래 참고)
T2-01~T2-08로 재분해)

**진행 상태**: T2-01~T2-08 전체 완료. **2026-07-25 사용자 승인으로
Milestone 2 종료.** Retrospective(목표 달성 여부/설계 원칙 적용/기술
부채/M3 과제/유지 결정)는 `.ai/TASKS.md`의 T2-08 항목 참고. 다음은
Milestone 3 착수 — 세부 Task는 착수 시점에 `T3-01`부터 정의.

> **설계 판단 (T2-01 재분해)**: 원래 T2-01은 Registry/Scheduler/Manager/
> EventBus 4종을 한 Task로 묶고 있었으나, 실제 착수 시 "AgentRuntime
> 파사드 + AgentSession + Lifecycle"만 다루고 Scheduler/EventBus는
> 배제하기로 재정의됨(T1-22가 보류했던 AgentRuntime 파사드 도입을 지금
> 재검토하는 결정). Scheduler/EventBus는 신규 **T2-02**로 분리하고 이하
> Task를 T2-03~T2-08로 순연했다.
>
> **설계 판단 (T2-05, 구 T2-04)**: `docs/ARCHITECTURE.md` §7 표는
> `EngineRuntime`/`EngineAdapter`의 구체 구현을 Milestone 3로 표시하지만,
> 위 Milestone DoD 3번("Mock EngineAdapter 위에서 시나리오 통과")을
> 만족하려면 최소한의 `EngineRuntime` 구현과 `MockEngineAdapter`(실제 LLM
> 호출 없이 즉시 성공 반환)가 필요하다. 이를 M2로 앞당기고, M3에서는
> `MockEngineAdapter`를 실제 Claude Code 등 어댑터로 교체하되
> `EngineRuntime` 구조는 그대로 재사용한다.

T2-01~T2-05는 서로 독립적이며 순서 무관(병렬 진행 가능, T2-02는 T2-01의
`AgentRuntime`에 붙는 구조라 T2-01 이후 진행을 권장), T2-06(능력별 Agent
골격)은 다섯 Task 모두에 의존, T2-07(통합 시나리오 테스트)·T2-08
(Milestone 2 Review)은 순차 진행한다.

| Task | 내용 | DoD | 의존성 | 상태 |
|---|---|---|---|---|
| T2-01 | AgentRuntime + AgentSession 구현 (`runtime/agent/agent_runtime.py`, `domain/agent_session.py` — `AgentManager`+`AgentRegistry`만 사용) | Lifecycle(시작/중지/종료)·상태 조회가 단위 테스트로 검증, 배제 범위(Scheduler/EventBus 등) 미import 확인 | T1-18 | **DONE** |
| T2-02 | Agent Scheduler + Event Bus 구현 (`runtime/agent/`: `InMemoryAgentScheduler`, `events/`: `InMemoryEventBus`) | 두 구현체 계약 테스트 통과 + Capability 기준 선택/다중 구독자 전달 검증 | T1-18, T2-01(권장) | **DONE** |
| T2-03 | Core Engines 구현 (`engines/`: `InMemoryTaskEngine`/`WorkflowEngine`/`ApprovalEngine`/`AutomationEngine`) | 4개 구현체 계약 테스트 통과 + ApprovalEngine이 4대 승인 행위(ADR-0003) 차단 검증 | T1-15 | **DONE** |
| T2-04 | Memory 계열 구현 (`memory/`: `InMemoryMemoryEngine`, `InMemoryContextManager`) | Snapshot 생성→복원 왕복 일치 + 의존 방향(ARCHITECTURE §8 규칙 7) 준수 확인 | T1-20 | **DONE** |
| T2-05 | Engine Runtime 최소 구현 + Mock Adapter (`runtime/engine/`: `InMemoryEngineRuntime`, `adapters/`: `MockEngineAdapter`) | `EngineRuntime.run()`이 Mock Adapter로 Task를 "실행"해 `EngineResult(success=True)` 반환 검증 | T1-19 | **DONE** |
| T2-06 | 능력별 Agent 골격 (`agents/`: Planning/Coding/Review/Documentation(+Coordination), EventBus 구독/발행) | `MissionPlanned`→`CodeCompleted`→`ReviewCompleted`→`DocumentationCompleted` 자동 진행 검증 | T2-01~T2-05 | **DONE** |
| T2-07 | 통합 시나리오 테스트 (전체 스위트 점검 + Event Store Replay + 승인 게이트 차단 시나리오) | `ruff`/`mypy`/`pytest` 전체 통과 + Milestone DoD 3개 항목이 각각 테스트로 매핑 | T2-01~T2-06 | **DONE** |
| T2-08 | Milestone 2 Review | 위 전부 DONE + 테스트 통과 상태에서 사용자 승인 | T2-01~T2-07 | TODO |

---

## Milestone 3 — 실행 엔진 연동 & 상호작용 (Engine Integration & Interaction)

**목표**: 실제 구현 엔진(Claude Code 우선)에 Task를 위임하고, 다양한 표면을
통합하는 Interaction Layer를 구현한다.

> **M2 Retrospective와의 관계**(`.ai/TASKS.md` T2-08 참고): **M3는 M2에서
> 이월된 기술 부채를 해결하는 것이 목표가 아니라, 실제 Engine Runtime과
> Engine Adapter 구현이 목표다.** 다만 M3 진행 중 자연스럽게 해결 가능한
> Deferred by Design 부채(`InMemoryAgentManager`/`AgentRegistry` 프로덕션
> 구현, CLI-WorkspaceCore 완전 연동, 실제 병렬 EngineAdapter 도입 시
> `run_parallel` 동시성 재검증)는 별도 Task로 포함할 수 있다. M3의 목표가
> "부채 청산"으로 변질되지 않도록, 착수 시점에 Task를 정의할 때 이 목표
> 우선순위를 그대로 유지한다.

**Milestone Definition of Done**(원문, 2026-07-25 이전 작성)
1. 세션 생명주기 계약을 만족하는 ClaudeCodeAdapter로 Coding Agent가 실제 Task를
   end-to-end(create_session→run→결과 수집→destroy_session) 수행한다.
2. Interaction Layer가 CLI/API 등 표면 입력을 표준 요청으로 정규화한다.

> **2026-07-25 Milestone 3 Review(M3-T08)에서 재확정**: 실제 착수 시
> 사용자가 정의한 M3-T01~T08 8개 Task 범위에는 위 DoD 2번(Interaction
> Layer)과 1번의 "Coding Agent가 실제로 수행" 부분이 처음부터 포함되지
> 않았다(1번 중 ClaudeCodeAdapter의 세션 생명주기 자체는 M3-T02/T03/T07
> 에서 실증됨). 사용자 승인으로 두 항목은 M3 미완료가 아니라 **Milestone
> 4로 공식 이관**되었다 — 아래 "진행 상태"와 Milestone 4 절 참고.

**진행 상태**: M3-T01(Engine Runtime)~M3-T08(Milestone Review) **완료
(2026-07-25 사용자 승인 — Milestone 3 Completed)**.

**Task 개요 — Engine Adapter & Execution** (M3-T01~M3-T08)
1. M3-T01 Managed Engine Runtime — **완료**
2. M3-T02 Claude Code Adapter — **완료**
3. M3-T03 Process Management — **완료**
4. M3-T04 Session & Workspace Integration — **완료**: WorkspaceCore↔
   ManagedEngineRuntime 연결, EngineSession 생명주기, 실행 기록, EventBus
   완전 연동. Deferred by Design 부채(#1 AgentManager/Registry, #2 CLI
   통합, #5 병렬성 검증)는 이번 Task 범위와 무관해 다루지 않음 — 계속
   이월.
5. M3-T05 Approval Pipeline — **완료**: `EngineApprovalPipeline` 신규 —
   ApprovalRequest 생성/사용자 승인 대기/승인·거부 Event/Runtime Resume
   (`run_approved()`). 기존 `ApprovalEngine`(T2-03)·`EngineRuntime`
   그대로 재사용, 새 상태 머신 없음.
6. M3-T06 Runtime Recovery — **완료**: `RecoveringEngineRuntime`(내부
   `EngineRuntime`을 감싸는 데코레이터) + `RetryPolicy` 신규. 실패/예외
   시 재시도, 재시도 소진 시 결과는 그대로 반환하되 예외는 계약대로
   그대로 재전파. 새 상태 저장소 없이 내부 Runtime 상태만 진실로 유지.
7. M3-T07 End-to-End Integration — **완료**: `ClaudeCodeEngineAdapter`→
   `ManagedEngineRuntime`→`RecoveringEngineRuntime`→`EngineApprovalPipeline`
   →`WorkspaceCore`를 실제 구현으로 조립(FakeProcessRunner만 대체)한
   `tests/integration/test_m3_end_to_end.py`. 승인→실행/거부→차단 경로와
   Event 발행 순서까지 검증.
8. M3-T08 Milestone Review — **완료**: 사용자 제공 8개 Task 체크리스트
   기준 7항목 전부 충족, 새 Interface 0개 추가(Interface First 실증),
   `pytest` 281개/`ruff`/`mypy` 클린. 원래 이 문서의 M3 DoD 2개 항목 중
   "Interaction Layer" 미구현, "Coding Agent 실제 경로 사용" 미검증을
   발견해 보고했고, **사용자 승인으로 두 항목을 Milestone 4로 공식
   이관하며 Milestone 3 Completed 확정**. 상세 Review는 `.ai/TASKS.md`의
   "Milestone 3 Review" 참고.

> M3 목표는 M2 이월 부채 청산이 아니라 실제 Engine Runtime/Adapter
> 구현이다(위 안내 유지). Deferred by Design 부채(#1 AgentManager/
> Registry, #2 CLI 통합, #5 병렬성 검증)는 자연스럽게 해결 가능한 Task
> (예: M3-T04)에 자연히 포함될 수 있다.

---

## Milestone 4 — 자동화 및 확장 (Automation & Scale)

**목표**: Automation Engine 기반 자동화, 다중 프로젝트 운용, Memory Engine
고도화. **사용자 강조: M4는 "기반 프레임워크"에서 "사용 가능한
워크스페이스"로 넘어가는 전환점이다** — Milestone 종료 시 v0.5.0 아키텍처
기준선(Baseline)을 확정해, M5 이후는 구조 변경보다 기능 확장에 집중한다.

**Milestone Definition of Done**
- 자동화 시나리오 1건 이상 동작(Automation Engine이 조건/일정 기반으로
  Workflow/Mission을 실제로 트리거) — **충족(M4-T07)**
- 다중 프로젝트 조회(2개 이상 프로젝트를 동시에 운용) — **충족(M4-T05)**
- 메모리 검색이 확인됨(Memory Engine이 핵심 컨텍스트를 검색/요약) —
  **검색만 충족(M4-T08)**. 요약(summarization)은 M4-T08 Analysis
  단계에서 사용자 승인 하에 범위를 좁혀 LLM Policy/Router 준비 이후
  Milestone으로 공식 이관(LLM 없이는 실질적인 요약을 구현할 수 없음)
- (필요 시 파일→DB 전환은 별도 ADR)

**Task List**(2026-07-26 확정, 상세는 `.ai/TASKS.md`의 "Milestone 4" 참고)

| Task | 내용 | 근거/출처 |
|---|---|---|
| M4-T01 | `AgentManager`/`AgentRegistry` 프로덕션 구현 — **완료** | M2 이월 부채 #1 |
| M4-T02 | CLI ↔ WorkspaceCore 완전 연동 — **완료** | M2 이월 부채 #2 |
| M4-T03 | Interaction Layer 구현 — **완료** | M3 Review에서 공식 이관 |
| M4-T04 | `CodingAgent` 실제 Engine 통합 + E2E — **완료** | M3 Review에서 공식 이관 |
| M4-T05 | 다중 프로젝트 운용 검증 — **완료** | M4 DoD |
| M4-T06 | `run_parallel` 실제 동시성 검증 — **완료** | M2 이월 부채 #5 |
| M4-T07 | Automation Engine 구현 — **완료**: `bind_workflow`/`fire` 추가, AutomationEngine은 연결 관리만 담당(WorkflowEngine 미의존) | M4 DoD |
| M4-T08 | Memory Engine 고도화 — **완료**: `search()`/`find_snapshots()` 추가(검색만, 요약은 LLM Router 이후로 이관) | M4 DoD |
| M4-T09 | Milestone 4 Review + v0.5.0 아키텍처 기준선 확정 — **완료**: `pyproject.toml` 버전 0.5.0 상향, ADR-0024 신규 | 관례 + 사용자 신규 제안 |

**Milestone 3에서 공식 이관된 항목**(M3-T08 Milestone 3 Review, 2026-07-25
사용자 승인, 위 M4-T03/T04에 반영됨): 이 문서의 원래 Milestone 3 DoD에는
포함되어 있었으나 실제 M3-T01~T08 Task 범위에는 없었던 항목 — M3
미완료가 아니라 M4로 재배치된 것으로 확정됨(`.ai/TASKS.md`의 "Milestone 3
Review" 7절 참고).
1. Interaction Layer 구현 — CLI/API 등 표면 입력을 표준 요청으로 정규화
2. `CodingAgent`(M2)의 실제 Engine 실행 경로(EngineApprovalPipeline→
   RecoveringEngineRuntime→ManagedEngineRuntime→ClaudeCodeEngineAdapter)
   통합 및 End-to-End 검증 — M3-T07 E2E는 Task를 Pipeline에 직접
   넘겼을 뿐 실제 Agent를 경유하지 않았음

---

## Milestone 5 — 실제 개발 수행 (Real Development Execution)

**목표**: v0.5.0 아키텍처 기준선(ADR-0024) 이후 첫 Milestone. Agent가
실제 개발 작업을 수행하도록 만든다 — 구조 변경보다 기능 확장에 집중한다.

> **`.ai/RULES.md` §7(Temporary LLM Policy) 로드맵과의 관계**: 원래
> 로드맵은 "M2 Rule 기반 선택 → M3 Agent Policy 참조 → M4 Policy Engine
> 자동 선택 → M5 Self Optimizer"였으나, M2~M4 내내 Domain 정의(T1-16)
> 이후 실제 선택 로직이 전혀 구현되지 않았다. M5-T01/T02가 M2/M3 단계를
> 소급 구현하며, Self Optimizer(M5 원래 목표)는 M6 이후로 미룬다.

**진행 상태**: M5-T01(LLM Policy Engine)~M5-T07(Milestone Review) **완료
(2026-07-26 사용자 승인)**. Milestone 6는 아직 목표/DoD/Task List가
정의되지 않았다(`.ai/TASKS.md`의 "Milestone 5 Review" 참고).

**Task List**(2026-07-26 확정, 상세는 `.ai/TASKS.md`의 "Milestone 5" 참고)

| Task | 내용 | 근거/출처 |
|---|---|---|
| M5-T01 | Rule 기반 `LLMPolicyEngine` 구현 — **완료**: `pyyaml` 최초 외부 의존성 추가, PolicyLoader 계층 분리 | RULES §7 M2 단계 소급 |
| M5-T02 | Agent Runtime이 `LLMPolicyEngine`을 통해 정책을 조회·기록하도록 연결 — **완료**(실제 Engine/Adapter 선택 반영은 M5-T05 이후) | RULES §7 M3 단계 소급 |
| M5-T03 | `DevelopmentContext` 도입 + 기존 Coding/Review Agent 강화 — **완료**: Coding→Review 산출물 전달, 원본 Task 불변 | 사용자 지시 — M5 핵심 목표 |
| M5-T04 | `ShellAgent` 신규(실제 쉘 명령 실행 능력) — **완료**: 화이트리스트 고정 명령, 명령어 삽입 방지 | 사용자 지시 — M5 핵심 목표 |
| M5-T05 | Codex/Gemini CLI Engine Adapter(가능한 범위) — **완료**: `CLIEngineAdapter`+`CLIProvider` 프레임워크 신규, ClaudeCodeEngineAdapter는 별도 유지(M6+ 통합 검토) | PRD 7.8 Multi-Engine 지원 |
| M5-T06 | Workflow 조건부 분기 + 필요 범위의 `Step` Domain 반영(M2 이월 부채 #6) — **완료**: `CoordinatorAgent`(ADR-0019 최초 구현) 신규, `ReviewAgent` 트리거 재배선, `TaskEngine`에 Step 이력 추가 | PRD 7.3 갭 + M2 이월 부채 #6 |
| M5-T07 | Milestone 5 Review — **완료**: 새 Interface 1개(`LLMPolicyEngine`) 추가를 투명하게 보고, 정책→실행 연결 미완성을 부채로 기록 | 관례 |

**M5 착수 전 사전 정리 — 조사 결과 조치 불필요로 종결**: Event ID 생성
방식 불일치(M2 이월 부채 #4)를 조사한 결과, `src/ai_workspace/`의 모든
Event 생성 지점이 이미 `uuid.uuid4()`로 일관되어 있어(M3에서 자연히
해소됨) 코드 변경 없이 부채 항목만 해소로 종결했다.

---

## Milestone 6 — Policy 기반 실행 라우팅 (Policy-Driven Engine Routing)

**목표**: `.ai/RULES.md` §7(Temporary LLM Policy) 로드맵의 "M4 단계: Policy
Engine이 자동으로 Provider/Model/Effort를 선택한다"를 완성한다. M5-T01/T02가
정책을 조회·기록하는 데까지만 연결했던 것을, 이번에는 실제로
`LLMPolicyDecision`에 따라 서로 다른 등록된 `EngineAdapter`가 선택되어
실행되도록 만든다 — M5 Review가 남긴 "정책→실행 연결 미완성" 갭을 해소하는
것이 핵심이다.

> **2026-07-26 사용자 확정**: 범위를 좁게 유지한다. Adapter 계열 통합
> (`ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 흡수), Codex/Gemini CLI
> 실제 재검증, 소규모 이월 부채(`run_parallel` 개별 재시도/
> `MemoryEngine.search` 성능/`ShellAgent` 화이트리스트 외부화 등)는 이번
> Milestone 범위에서 명시적으로 제외하고 계속 이월한다.

**Milestone Definition of Done**
1. `LLMPolicyDecision.model.provider`에 따라 `CodingAgent`/`ReviewAgent`/
   `DocumentationAgent`가 실제로 서로 다른 등록된 `EngineAdapter`를 선택해
   실행함이 통합 테스트로 검증된다.
2. `ManagedEngineRuntime`이 2개 이상의 `EngineAdapter`를 동시에 등록할 수
   있고, `required_capabilities`로 올바른 Adapter를 선택하며, 만족하는
   Adapter가 없으면 `NoSuitableEngineError`를 던진다.
3. `EngineRuntime`/`EngineAdapter` 인터페이스 계약은 변경되지 않는다
   (Interface First).
4. 기존 `pytest` 전체 스위트 + 신규 테스트 모두 통과, `ruff`/`mypy` 클린.
5. Adapter 계열 통합, Codex/Gemini CLI 실제 재검증, 소규모 이월 부채는
   이번 범위에서 제외되며 계속 이월된다.

**Task List**(2026-07-26 확정, 상세는 `.ai/TASKS.md`의 "Milestone 6" 참고)

| Task | 내용 | 근거/출처 |
|---|---|---|
| M6-T01 | `ManagedEngineRuntime` 다중 Adapter 등록 지원 — **완료** | M5 Review 이월 갭 #1 |
| M6-T02 | `LLMProvider` → Engine Capability 매핑 + Agent 3종(Coding/Review/Documentation) 라우팅 반영 — **완료** | RULES §7 M4 단계(자동 선택) |
| M6-T03 | 다중 Adapter 조립 + End-to-End 검증 — **완료** | Milestone DoD |
| M6-T04 | Milestone 6 Review — 완료 | 관례 |

**진행 상태**: M6-T01~T04 전체 완료. **2026-07-26 사용자 승인으로
Milestone 6 종료.** Retrospective(Model/Effort 수준 라우팅 미완성을
M7+ 논의 대상으로 명시)는 `.ai/TASKS.md`의 "Milestone 6 Review" 참고.

---

## Milestone 7 — Memory 요약 (Memory Summarization)

**목표**: PRD 7.4(장기 메모리)와 M4 DoD가 원래 요구했던 "검색/요약" 중
"요약"만 M4-T08에서 "LLM 없이는 구현 불가"로 이관됐던 항목을 완성한다.
M6에서 실제 LLM 호출 인프라(`EngineRuntime`→`EngineAdapter`)가 완성되어
이 차단 사유가 해소됐다.

> **2026-07-26 사용자 확정**: 요약 트리거는 **파이프라인 종료
> 시점**(`DocumentationAgent`)으로 좁힌다. 온디맨드 트리거는 범위 제외.

**Milestone Definition of Done**
1. `DocumentationAgent`가 `engine_runtime.run()` 결과를 캡처해
   `context_manager.create_snapshot(session, summary=...)`로 전달한다.
2. `ContextManager.create_snapshot()`이 선택적 `summary` 파라미터를 받아
   Snapshot에 포함시키며, 기존 무인자 호출과 하위 호환된다.
3. 저장된 요약을 `restore_snapshot()`/`assemble_context()`로 조회,
   `find_snapshots(query)`로 검색할 수 있다(PRD 7.4 완전 충족).
4. `MemoryEngine` 인터페이스는 변경되지 않는다(ADR-0017 경계 유지).
5. 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린.
6. Adapter 통합/CLI 실제 재검증/Model·Effort 라우팅/소규모 이월 부채는
   범위 밖으로 유지된다.

**Task List**(2026-07-26 확정, 상세는 `.ai/TASKS.md`의 "Milestone 7" 참고)

| Task | 내용 | 근거/출처 |
|---|---|---|
| M7-T01 | `ContextManager.create_snapshot()`에 선택적 `summary` 파라미터 추가 — **완료** | PRD 7.4 갭 |
| M7-T02 | `DocumentationAgent`가 버려지던 engine 결과를 요약으로 전달 — **완료** | PRD 7.4 갭 |
| M7-T03 | End-to-End 검증 — **완료** | Milestone DoD |
| M7-T04 | Milestone 7 Review — 리뷰 작성 완료, 사용자 승인 대기 | 관례 |

**진행 상태**: M7-T01~T03 전체 완료(2026-07-26). Milestone DoD 1~5번
충족 확인됨(6번은 범위 제외 확정 그대로 유지). Milestone 7 Review 작성
완료(`.ai/TASKS.md`의 "Milestone 7 Review" 참고) — 사용자 승인 대기.

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
| P1-6 | T1-18~T1-21 | (2026-07-24 ADR-0022로 4개 Task로 재분해 — 아래 표 참고) | DONE |
| P1-7 | T1-22 | Workspace Core 골격 구현 (Agent Runtime 위임형) | DONE |
| P1-8 | T1-23 | 파일 기반 저장소 구현 (ProjectRepository + AgentRepository + EventStore) | DONE |
| P1-9 | T1-24 | CLI 진입점 구성 | DONE |
| P1-10 | T1-25 | 기본 테스트 환경 구축 및 테스트 작성 | DONE |
| P1-11 | T1-26 | `docs/ARCHITECTURE.md` 최종 정합성 확인 | DONE |
| P1-12 | T1-27 | ADR 상태 갱신 (ADR-0002, ADR-0004) | DONE |
| P1-13 | T1-28 | Milestone 1 완료 승인 요청 (구 "Phase 1 완료 승인 요청") | DONE |

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
