# ARCHITECTURE — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.43.0 |
| 작성일 | 2026-07-30 |
| 상태 | Draft (Milestone 1~22 완료. Milestone 23(Obsidian Integration & Auto Save) — Completed. Milestone 24(Real Obsidian Vault Integration) — Completed(ADR-0036). Milestone 25(Production Vault Activation) — Completed. Milestone 26(Obsidian Vault Root Refactoring) — Completed(ADR-0037, Vault == Repository Root). Milestone 27(Obsidian Workspace Templates, 사용자 요청 "M25") — Completed(ADR-0038, `VaultDocumentKind.TASK` 신규). Milestone 28(Live Task Management & Integration) — Completed(T01~T06 전체, ADR-0039~0041). Architecture Freeze(ADR-0042) — 사용자 승인 완료. Milestone 29(Project Intelligence) 완료 — 사용자 승인 완료(2026-07-30)(ADR-0043, `intelligence/` 신규 Layer, 결과는 Vault `15 Project Intelligence/Project Intelligence.md`에 노출, "의존성 위험" Deferred by Design). 새 Core Domain Interface 없음, 27종 유지. Milestone 30(Context Intelligence) 완료 — 사용자 승인 완료(2026-07-30)(ADR-0044, `intelligence/context*.py`, 결과는 Vault `15 Project Intelligence/Project Context.md`에 노출). 새 Core Domain Interface 없음, 27종 유지. Milestone 31(Capability Intelligence) 완료 — 사용자 승인 완료(2026-07-30)(ADR-0045, `intelligence/capability*.py`, `AgentAdapter` 확장, 결과는 Vault `15 Project Intelligence/Capability Intelligence.md`에 노출). 새 Core Domain Interface 없음, 27종 유지. Milestone 32(Intelligence Synthesis) 완료 — 사용자 승인 완료(2026-07-30)(ADR-0046, `intelligence/synthesis*.py`, M29~M31 Service 3개를 조합해 결과는 Vault `15 Project Intelligence/Intelligence Overview.md`에 노출). 새 Core Domain Interface/Adapter 없음(`VaultAdapter` 확장 1건), 27종 유지. M29~M32로 Intelligence Layer 기반 완성(Project/Context/Capability/Synthesis). **Milestone 33(Session Resume) 완료 — 사용자 승인 완료(2026-07-30)**(ADR-0047, `intelligence/session_resume*.py`, "현재 작업" 선택 규칙 1개 + M29~M32 재사용, 결과는 Vault `15 Project Intelligence/Session Resume.md`에 공식 확정). 새 Core Domain Interface/Adapter 없음(`VaultAdapter` 확장 1건), 27종 유지. **Intelligence Layer를 실제 사용 시나리오(세션 시작)에 처음 연결한 Execution 쪽 첫 기능**. **Milestone 34(Workflow Intelligence) 완료 — 사용자 승인 완료(2026-07-30)**(ADR-0048, `intelligence/workflow_flow.py`/`workflow_service.py`, "Workflow"를 `domain.Workflow`가 아니라 Milestone Task 실행 흐름으로 재정의하고 Blocked/Next Rule 1개 + `WorkflowFlowAnalyzer` 캡슐화로 구현, 결과는 Vault `15 Project Intelligence/Workflow Intelligence.md`에 공식 확정). 새 Core Domain Interface/Adapter 없음(`VaultAdapter` 확장 1건), 27종 유지, `domain.Workflow`/`WorkflowEngine`/`WorkflowAdapter` 무변경(사용하지 않음). **Milestone 35(Recommendation Intelligence) 완료 — 사용자 승인 완료(2026-07-30)**(ADR-0049, `intelligence/recommendation_rules.py`/`recommendation_service.py`, M29/M31/M33/M34 Intelligence를 그대로 조합한 5단계 Priority Rule 1개로 단일 Next Action을 결정, 결과는 Vault `15 Project Intelligence/Recommendation Intelligence.md`에 공식 확정). 새 Core Domain Interface/Adapter 없음(`VaultAdapter` 확장 1건), 27종 유지 — Execution Layer 이전의 마지막 Decision Layer, 자동 실행 없음. **Milestone 36(Execution) 완료 — 사용자 승인 완료(2026-07-30)**(ADR-0050, `runtime/execution/recommendation_execution_gate.py`/`recommendation_action_builder.py`/`recommendation_execution_service.py`, M35 `NextAction`의 `source=next_task`만·수동 트리거로만 기존 `ExecutionDispatcher`/`EngineRegistry`/`EngineSelectionPolicy`(M17/M18)에 연결해 실행, 결과는 Vault `15 Project Intelligence/Recommendation Execution.md`에 공식 확정). 새 Core Domain Interface/Adapter 없음(`VaultAdapter` 확장 1건), 27종 유지, `AutomationActionExecutor`/`AutomationScheduler`/`ExecutionDispatcher` 무변경(그대로 재사용) — **M29~M35 Read Only Intelligence를 실제 실행으로 연결한 첫 side-effecting Milestone**. **Milestone 37(Task Lifecycle) 완료 — 사용자 승인 완료(2026-07-30)**(ADR-0051, `runtime/execution/recommendation_task_lifecycle.py`, M36 Execution 결과를 기존 Task 상태 전이 기계(`_ALLOWED_TRANSITIONS`, M28)에 연결 — 실행 시작 시 `todo→in-progress`, 성공 시 `in-progress→review`, 실패 시 `in-progress→todo`만 자동화하고 `review→done`은 사람 검토로 남김, 결과는 Vault `15 Project Intelligence/Recommendation Execution.md`의 "Task Status 이력" 섹션에 공식 확정). 새 상태·새 전이 규칙·새 Adapter 없음(`VaultAdapter` 확장도 없음, 기존 `transition_task()` 그대로 재사용), 27종 유지. **Milestone 38(AutomationScheduler 연결) 완료 — 사용자 승인 완료(2026-07-30)**(ADR-0052, `web/server.py`의 `build_app()`에 `VaultAdapter`/`AgentAdapter`/`RecommendationIntelligenceService`/`RecommendationExecutionService`를 최초로 실배선하고, `AutomationActionExecutor`에 신설 `ActionKind.RUN_RECOMMENDATION`을 연결해 `AutomationScheduler`의 TIME/INTERVAL Trigger로 M35 `source=next_task` 추천이 자동 실행되게 함). 새 정책 없음 — `ExecutionGate`는 M36과 동일하게 `source=next_task`만 승인. 새 Core Domain Interface/Adapter 없음(27종 유지), `ExecutionGate`/`ActionBuilder`/`TaskLifecycleTransitioner` 무변경. **M29(Project Intelligence)~M38(AutomationScheduler 연결)로 Intelligence→Execution→Automation 기본 폐쇄 루프 완성**. **Milestone 39(Execution Memory) 완료 — 사용자 승인 완료(2026-07-30)**(ADR-0053, `domain/execution_memory.py`/`memory/execution_memory_store.py` 신규, `RecommendationExecutionService`에 `execution_memory_store` 선택적 주입으로 Execution 결과가 기존 `MemoryEngine`(M1)에 자동 저장, `ExecutionMemoryStore.query()`로 조회만 제공하고 Learning/영속화/Rule 반영은 범위 밖). 새 Core Domain Interface 없음(27종 유지, `MemoryEngine` interface 무변경). **Milestone 40(Experience Intelligence) 완료 — 사용자 승인 완료(2026-07-30)**(ADR-0055, `intelligence/experience_rules.py`/`experience_service.py` 신규, `ExecutionMemoryStore.query()`가 domain 타입 대신 `ExecutionMemoryEntry`를 반환하도록 변경(M39 확장), §8 규칙 21을 Adapter 이름 나열 대신 Role(`*Service` 클래스 유무) 기반으로 재정의해 `memory/` 접근을 Service 계층에만 허용. Scope는 (a)Read-Only Reporting만(Recommendation 미반영), Analyzer는 Deterministic+Immutable Input 조건 충족(사용자 조건부 승인), 결과는 Vault `15 Project Intelligence/Experience Intelligence.md`에 노출). 새 Core Domain Interface/Adapter 없음(27종 유지). **Milestone 41(Architecture Guardian) 완료 — 사용자 승인 완료(2026-07-30)**(ADR-0056, `guardian/` 신규 패키지 — `tests/` 5곳에 중복 구현돼 있던 `ast` 기반 경계 검사 중 3개 형태에 맞는 5개 규칙을 `GUARDIAN_RULES`(Final tuple)로 통합, `ArchitectureRule`은 메서드 없는 순수 값 객체 3종의 Union, `guardian/checker.py`는 pytest를 모르는 순수 평가기, `ArchitectureGuardianService.publish()`가 핵심 진입점으로 Vault `15 Project Intelligence/Architecture Guardian.md`에 결과 공표. Connector 그룹 규칙 2개는 억지로 일반화하지 않고 범위 제외(사용자 조건)). 새 Core Domain Interface/Adapter 없음(27종 유지), 새 Layer 1개(`guardian/`, §13.2가 이미 예약해 둔 자리) — 다음은 M42이며 착수 시점에 별도 제안·승인. **Milestone 42(Recommendation Adaptation) 완료 — 사용자 승인 완료(2026-07-31)**(ADR-0058, `intelligence/recommendation_adjustment.py` 신규 `RecommendationAdjustmentAnalyzer`, M40 `ExperienceReport`를 근거로 M35 `NextAction`을 새로 생성하지 않고 사후 조정(Adjustment)만 함 — 대상의 과거 실행이 전부 실패일 때만 추천 보류. `RecommendationIntelligenceService.generate()/publish()`에 `experience_report` 선택적 인자 추가, `experience_report=None`이면 M35와 100% 동일 동작(사용자 조건). `Adaptation`은 §13.3 Behavioral Concept로만 기록 — 1급 Domain 승격은 재사용 사례 축적 시 별도 ADR로 보류). 새 Core Domain Interface/Adapter 없음(27종 유지), `web/server.py`/`RecommendationExecutionService` 자동 배선 없음(Non-goal). **Milestone 43(Recommendation Orchestration) 완료 — 사용자 승인 완료(2026-07-31)**(ADR-0059, `runtime/execution/recommendation_orchestration_service.py` 신규 `RecommendationOrchestrationService` — M40 Experience 조회 → M35/M42 Recommendation(Adaptation 포함) 계산 → M36 Execution 위임까지 전체 흐름을 판단 로직 없이 순서대로 호출만 함. `Orchestration`은 ADR-0041 Orchestrating Connector와 같은 의미로 §13.3에 구조적 관행으로 최초 등재(1급 Domain 아님). MDD Review 재검토로 `RecommendationExecutionService`가 `RecommendationIntelligenceService` 의존성을 아예 제거하고 `RecommendationIntelligenceReport`를 파라미터로 받도록 결합도 개선(사용자 제안). `AutomationActionExecutor`/`web/server.py` 배선을 Orchestration Service로 교체해 M42의 Non-goal(자동 배선)을 완성). 새 Core Domain Interface/Adapter 없음(27종 유지). **Milestone 44(Recommendation Explainability) 완료 — 사용자 승인 완료(2026-07-31)**(ADR-0061, `intelligence/recommendation_explanation.py` 신규 `RecommendationExplanationAnalyzer` — M35/M42 `RecommendationIntelligenceReport` + M40 `ExperienceReport`를 읽어 5단계 Priority Rule 평가 흔적·Experience 성공률·Adaptation 적용 여부를 재구성. Recommendation 자체는 바꾸지 않음(새 AI 판단 없음). `intelligence/recommendation_explanation_service.py` 신규 `RecommendationExplanationService`가 Vault `15 Project Intelligence/Recommendation Explanation.md`에 발행. `Explainability`는 §13.3 Behavioral Concept로 등재(1급 Domain 아님, `Adaptation`과 동일 급). `RecommendationOrchestrationService`(M43)에 `explanation_service` 선택적 주입으로 Recommendation→Explainability→Execution 순서 연결(`web/server.py` 실배선), 미주입 시 M43 이전과 100% 동일 동작). 새 Core Domain Interface/Adapter 없음(27종 유지). **Milestone 45(Workspace Observability) 완료 — 사용자 승인 완료(2026-07-31)**(ADR-0062, `observability/` 신규 패키지 — `WorkspaceRuntimeSnapshot`(읽기 전용 Runtime 모델) + 3개 Analyzer(`ClaudeRuntimeAnalyzer`/`PipelineStageAnalyzer`/`WorkspaceInfoAnalyzer`) + `RuntimeSnapshotService` + `StatusLineRenderer`. Claude Code StatusLine stdin JSON을 그대로 옮기고, Recommendation→Adaptation→Explainability→Orchestration→Execution→Memory→Experience 7단계 상태를 Vault 산출물 존재 여부로만 재구성(Adaptation/Orchestration은 별도 산출물 없어 `STRUCTURAL_INCLUDED`, Memory는 `InMemoryMemoryEngine` 비영속이라 `NOT_OBSERVABLE`로 정직하게 표시). `VaultAdapter.report_last_modified()` 1개 메서드만 확장(새 Adapter 없음). `Observability`는 §13.3 Behavioral Concept로 등재(1급 Domain 아님). `.claude/settings.json`에 `statusLine.command`로 배선. 새 Core Domain Interface/Adapter 없음(27종 유지), Dashboard/Web UI/Telemetry/기존 Domain 판단 로직 변경 없음(Non-goal)). **Milestone 45 확장(Execution Environment Observability) 완료 — 사용자 승인 완료(2026-07-31)**(ADR-0063, `GitRuntimeAnalyzer`/`GuardianRuntimeAnalyzer`/`VaultRuntimeAnalyzer`/`McpRuntimeAnalyzer`(신규 4개) — Git/Guardian/Vault/MCP(Obsidian MCP 포함) 실행 환경을 읽기 전용으로 추가 관찰. `Observability`는 §13.3 Behavioral Concept를 그대로 확장(새 Domain 어휘 없음). `.mcp.json`/`claude mcp list`(공식 문서화된 경로만 사용), `.pytest_cache/lastfailed`(재실행 없이 마지막 로컬 결과만), `guardian.checker.evaluate()`(그대로 재사용) — `ruff`/`mypy`/Coverage/MCP `active_server`·`available_tools`·`last_mcp_call`·`last_mcp_error`/Vault `current_pr`은 공식적으로 안전하게 관측할 방법이 없어 전부 `None`(Not Available)으로 정직하게 표시(Phase 2 후보로만 문서화). 새 Core Domain Interface/Adapter 없음(27종 유지)) |

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

### 2.1 Intelligence Platform / Execution Platform 계층 구조 (2026-07-30 사용자 확정)

M29~M38(§3.22~§3.31)은 위 §2 다이어그램의 `Core Engines`(Task·
Workflow·Approval·Automation) 축 위에 얹힌 별도 계층이며, 책임에
따라 두 그룹으로 재해석한다 — **새 컴포넌트나 코드 변경 없이 기존
10개 Milestone을 문서상으로 재구성**한 것뿐이다(M38 완료 논의 중
사용자 제안, ADR 없음 — 코드/Interface/의존성 규칙에 영향을 주지
않는 순수 문서 재구성이라 별도 ADR을 만들지 않는다).

```
Intelligence Platform (M29~M35) — 관찰·분석·추천
├── M29 Project Intelligence         (ADR-0043)
├── M30 Context Intelligence         (ADR-0044)
├── M31 Capability Intelligence      (ADR-0045)
├── M32 Intelligence Synthesis       (ADR-0046)
├── M33 Session Resume               (ADR-0047)
├── M34 Workflow Intelligence        (ADR-0048)
└── M35 Recommendation Intelligence  (ADR-0049)

Execution Platform (M36~M38) — 실행·상태 전이·스케줄링
├── M36 Execution                    (ADR-0050)
├── M37 Task Lifecycle               (ADR-0051)
└── M38 AutomationScheduler 연결      (ADR-0052)
```

- **Intelligence Platform(M29~M35)**: `VaultAdapter`/`AgentAdapter`를
  읽기만 해서(Read Only) Project/Context/Capability/Synthesis/Session
  Resume/Workflow 상태를 계산하고, M35 `RecommendationRuleAnalyzer`가
  이를 입력으로 단일 `NextAction`을 고른다. side-effect가 없다 — 추천만
  하고 Task를 실행하거나 상태를 바꾸지 않는다.
- **Execution Platform(M36~M38)**: `ExecutionGate`/`ActionBuilder`
  (M36)가 `source=next_task`만 승인해 기존 `ExecutionDispatcher`
  (M18)로 실제 실행하고, `TaskLifecycleTransitioner`(M37)가 그
  결과를 기존 Task 상태 전이 기계(M28)에 연결하며,
  `AutomationScheduler`(M21) 연결(M38)로 이 전체를 주기적 Trigger
  에서도 실행 가능하게 만든다 — **처음으로 실제 부작용(AI Engine
  실행, Task 상태 변경)을 일으키는 계층**이다.
- **"Automation Core" 명명 보류(사용자 판단, 2026-07-30)**: M36~M38은
  "생각하고 실행"할 수 있을 뿐, 아직 스스로 기억하고(Memory Engine)
  설계를 감시하고(Architecture Guardian) 학습하는(Learning Engine)
  단계가 아니다 — 그래서 지금은 "Automation Core v1.0"이라는 이름을
  붙이지 않는다. 이 세 Engine이 실제로 설계·구현·승인된 뒤(M39 이후,
  각각 별도 제안·승인 대상)에야 M29~그 시점까지의 전체를 묶어
  "Automation Core"로 명명하는 것이 아키텍처적으로 더 일관된다. 이
  문단은 향후 방향에 대한 사용자 의견 기록일 뿐, 세 Engine 자체를
  설계하거나 구현을 확정하는 것이 아니다(§1.4 Approval Required —
  각 Engine은 별도 승인 절차를 거친다).
- **M39 Execution Memory — 완료(2026-07-30, ADR-0053)**: 위 세 Engine 중
  Memory Engine을 M39로 착수해 완료했다 — Execution 결과(`ExecutionMemory`)
  를 기존 `MemoryEngine`(M1)에 저장하고 `ExecutionMemoryStore`로
  조회만 제공한다(§3.8, §8 규칙 22). Learning(Rule/추천 반영)·
  영속화·Architecture Guardian은 여전히 범위 밖 — "Automation Core"
  명명 여부는 이 셋(Architecture Guardian/Learning Engine 포함)이
  모두 결정된 뒤 다시 논의한다.
- **M41 Architecture Guardian — 완료(2026-07-30, ADR-0056)**: 위 세
  Engine 중 Architecture Guardian을 M41로 착수해 완료했다 — §13.2가
  정의한 역할(규칙을 정의하지 않고 평가·공표만) 그대로, 이미 `tests/`
  5곳에 흩어져 중복 구현돼 있던 `ast` 기반 경계 검사를 `guardian/`
  패키지 하나로 통합했다(§3.33). Learning Engine만 남아 "Automation
  Core" 명명 여부는 여전히 논의 대상이다.

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
- **Execution Memory(M39, ADR-0053)**: `ExecutionMemoryStore`
  (`memory/execution_memory_store.py`)는 Agent 경로(위 규칙 7)와는
  **완전히 별도의 경로**로 `MemoryEngine`을 재사용한다(§8 규칙 14) —
  `RecommendationExecutionService`(Execution Platform)가 실행 결과를
  `ExecutionMemory`(task_id/action/result/timestamp/reason만 있는
  순수 기록, embedding/score 없음)로 자동 기록한다. Context Manager가
  관리하는 Snapshot과는 다른 개념(세션 Context 복원 vs. Execution
  이력 축적)이며, `MemoryEngine` interface는 그대로다(remember/
  recall/search 3개 그대로, 새 메서드 없음). 저장·조회만 제공하고
  Learning(과거 기록으로 추천/판단을 바꾸는 것)은 하지 않는다 —
  Learning Engine(M40 이후, 별도 승인 대상)의 책임이다.

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

Obsidian Vault(Milestone 26부터 이 저장소 root 자체 — Vault ==
Repository Root)로의 문서 저장을 자동화하는 계층. **Core
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
    저장소 root(= Vault Root, git-tracked Markdown)
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
- **구현 상태(M23-T06, Execution Engine)**: 새 코드가 아니라
  절차 문서로 구현 — 자연어 해석은 AI 고유 역할이라 결정적
  프로그램 대상이 아니다. Vault `EXECUTION_PROFILE`에 "Execution
  Engine — 자연어 명령 라우팅" 절 추가(흐름도 + 지원 명령 예시
  표), 5~6단계(Document Update/Validation)가 `vault.auto_save.
  run_auto_save()`를 구체적으로 가리키도록 갱신.
- **구현 상태(M23-T07, Execution Environment Integration)**:
  `tests/integration/test_m23_vault_environment_integration.py`
  신규 — 이 실행 환경(Claude Code CLI + 로컬 Filesystem)에서
  실제 `Vault/`에 접근 가능한지, 실제 문서 트리에서
  `find_broken_backlinks()`가 알려진 프롬프트 예시 텍스트 외에
  새로운 깨진 링크가 없는지, `run_auto_save()`가 실제 Vault 트리
  복사본 위에서 저장→검증 왕복에 성공하는지 확인한다. 검증 과정
  에서 `EXECUTION_PROFILE.md`/`Backend Index.md`에 줄바꿈으로
  깨진 `[[..]]` 링크 2건(M23 작업 중 도입 1건, 그 이전부터 있던
  1건)을 실제로 찾아 함께 수정 — 이 계층이 실제로 가치가 있음을
  증명. Obsidian MCP를 통한 실시간 연동은 범위 밖으로 유지
  (M23-Prep-T08 Optional, Claude Code 도입 시점으로 이월 유지).
  GitHub Repository 연동은 M23-T01~T07 매 Task의 커밋·푸시 성공
  으로 이미 검증됨.

**Milestone 23(Obsidian Integration & Auto Save) 전체 완료
(T01~T07).**

- **구현 상태(Milestone 24, ADR-0036, Real Obsidian Vault
  Integration)**: `vault/connection.py`(`resolve_default_vault_root()`
  로 이 저장소 상위에서 실제 `Vault/01 Projects/AI Workspace`를
  탐색, `connect()`가 존재/디렉터리/쓰기 권한을 검증해
  `VaultConnection` 반환 또는 `VaultConnectionError`), `vault/
  filesystem.py`(`VaultFileSystem` — Create/Read/Update/Delete/
  Exists/Rename/Move 7개 연산을 명시적으로 노출하는 얇은 Adapter),
  `vault/atomic.py`(`atomic_write_text()` — 임시 파일 + `os.replace()`
  로 원자적 저장, `VaultWriter`가 내부적으로 사용). `run_auto_save()`
  의 Validation을 Vault 전체 스캔에서 **이번 호출이 저장한 파일만
  검사하는 Incremental 방식**으로 전환(`find_broken_backlinks()`에
  `only_paths` 파라미터 추가, 생략 시 기존과 동일한 전체 스캔).
  `run_auto_save_on_default_vault()`(신규)가 `vault_root` 생략 시
  실제 Vault에 자동 연결한다. `tests/vault/`(Mock/`tmp_path`, 38개)
  는 전부 무변경 통과, `tests/integration/test_m24_real_vault_e2e.py`
  (신규, 5개)가 `tmp_path` 없이 이 저장소의 실제 `Vault/`를 대상으로
  Connect/Create/Update/Rename/Delete/Auto Save 왕복을 검증하고
  종료 시 스스로 정리한다(기존 문서 영구 변경 없음).

- **구현 상태(Milestone 26, ADR-0037, Obsidian Vault Root
  Refactoring)**: 위 M24 서술의 `Vault/`(`Vault/01 Projects/
  AI Workspace/`)는 **이 시점 이후 저장소 root로 승격**됐다 — Git
  Vault Sync/Obsidian Mobile·macOS가 요구하는 "Vault == Repository
  Root" 조건을 만족시키기 위해 `00 System`~`13 Daily`/`99
  Templates` 15개 디렉터리를 `git mv`로 저장소 root로 이동하고,
  더 이상 필요 없는 PARA 뼈대(`Vault/00 Inbox`/`02 Resources`/
  `03 Archives`)는 제거했다. `vault/connection.py`의
  `resolve_default_vault_root()`는 이제 `00 System/PROJECT_INDEX.md`
  표식 파일이 있는 조상 디렉터리를 찾고(이전처럼 `Vault/01
  Projects/AI Workspace` 하위 경로를 찾지 않는다), `vault/mapping.py`
  의 상대 경로는 처음부터 `vault_root` 기준이라 변경이 필요 없었다.
  `vault_root`가 저장소 root와 같아짐에 따라 `vault/validation.py`/
  `vault/sync.py`의 문서 스캔 범위를 `VAULT_CONTENT_DIRECTORIES`
  (Vault 콘텐츠 15개 디렉터리)로 명시적으로 제한해 `docs/`/
  `.claude/`/`.agents/` 등 Vault가 아닌 마크다운이 Validation에
  섞이지 않게 했다. `[[Wikilink]]`는 파일명 기준이라 이동으로
  전혀 깨지지 않았고, 마크다운 스타일 상대경로 링크는 Vault 안에
  하나도 없었다(검증 완료). `tests/vault/`(Mock, 46개 중 9개
  fixture를 새 스캔 범위에 맞춰 조정) 전부 통과, `tests/integration/
  test_m23_vault_environment_integration.py`/`test_m24_real_vault_e2e.py`
  는 저장소 root를 직접 Vault Root로 사용하도록 갱신.

- **구현 상태(Milestone 27, ADR-0038, Obsidian Workspace
  Templates — 사용자 요청 "M25 - Obsidian Workspace Integration")**:
  Obsidian을 "Task 생성 → 문서 생성 → 진행 관리 → 상태 변경"이
  Obsidian 안에서 이뤄지는 Workspace로 확장했다. `vault/models.py`
  에 `VaultDocumentKind.TASK` 신규(`DAILY`와 같은 create 방식,
  대상 파일은 `fields["task_id"]` 기준), `vault/mapping.py`에
  `14 Tasks` 디렉터리 + `"14 Tasks/{task_id}.md"` 매핑 추가(
  `VAULT_CONTENT_DIRECTORIES` 15종 → 16종), `vault/router.py`가
  `task_id` 치환을 처리(누락 시 `MissingVaultFieldError`),
  `vault/markdown_generator.py`에 `render_task_file()` 신규
  (frontmatter `tags`/`type`/`status`/`priority`/`milestone`/
  `owner`/`created`/`updated` + Status/Priority/Milestone/Owner/
  Created/Updated/Checklist/Notes/Related Documents/Decision
  섹션), `render_daily_file()`에 진행중/완료/결정사항 구분 추가.
  `99 Templates/Template - Task.md`/`Template - Project
  Workspace.md`(신규), `Template - Daily.md`/`Template -
  Decision.md`(갱신). `AI_RULES`에 `#task`/`#meeting`/`#bug`/
  `#feature`/`#research`/`#daily` Tag 추가 + 신규 Frontmatter Rule
  절(`type`/`status`/`priority`/`milestone`/`created`/`updated`).
  Workspace(다중 Project 폴더) Template은 이 Vault가 아직 단일
  Project라 지금 인스턴스화하지 않고 `Template - Project
  Workspace.md`에 설계만 남긴다(YAGNI). `tests/vault/` 신규 6개
  (`render_task_file`/Router TASK 라우팅/`VaultSaveEngine` TASK
  저장 + Daily 확장 섹션) 전부 통과, 기존 테스트 무변경 통과. 새
  Interface 없음(27종 그대로) — `vault/`는 Interface 계층이 아니라
  데이터/함수 계층(ADR-0035)이라는 성격을 유지한다.

**Milestone 27(Obsidian Workspace Templates) 완료.**

- **구현 상태(Milestone 28-T01, Task Lifecycle)**: `vault/
  task_lifecycle.py`(신규) — `TaskStatus`(Todo/In Progress/Review/
  Done/Archived) + `transition_task_status()`가 Task 문서의 상태
  전이·`updated` 자동 갱신·Archive 이동(`14 Tasks/Archive/
  {task_id}.md`)을 처리한다. `sync.py`(Rename/Delete)와 같은 "문서
  생성 이후 관리" 계층으로 배치했고, Task 생성 자체(Router→
  Generator→Writer→Engine)는 그대로다. Core Domain 참조 없음, 새
  Interface 없음 — Milestone 28의 나머지 Task(자동 문서 갱신/
  Integration Layer/Workflow·Agent 연동/Conversation Layer)는
  진행 중이며 각 Task 완료마다 이 절에 추가한다.

- **구현 상태(Milestone 28-T02, Automatic Document
  Synchronization)**: `vault/task_sync.py`(신규) — `sync_task_change()`
  가 Task 상태 변경을 Daily Note("오늘 작업"/"진행중"/"완료" 섹션에
  Backlink 줄 추가, 없으면 생성)/`11 Milestones/Milestones
  Index.md`("## Task 변경 로그" — `docs/ROADMAP.md`는 GitHub 원문
  이라 Vault가 직접 못 쓰므로 이 Vault 대응 문서로 대신함)/`12
  Decisions/Decisions Index.md`("## Task 연결", Task의 `## Decision`
  절에 실제 Wikilink가 있을 때만)에 반영한다. 신규 헬퍼
  `_upsert_bullet_section()`은 `writer.upsert_section()`(섹션
  전체 치환)과 달리 누적 로그용으로 "중복 없는 줄 추가"를
  구현한다(서로 다른 저장 전략을 하나로 억지로 합치지 않음).
  `transition_and_sync()`가 `task_lifecycle.transition_task_status()`
  + `sync_task_change()`를 잇는 단일 진입점. 모든 신규 링크는
  파일명/기존 문서 제목만 가리켜 Wiki Link/Backlink가 깨지지
  않는다(`find_broken_backlinks()` 통합 테스트로 확인). Core Domain
  참조 없음, 새 Interface 없음.

### Workspace Adapter Layer(Milestone 28-T03, ADR-0039)

`vault/`(§3.21)와 Core Domain(§3.4~3.21의 `domain`/`interfaces`/
`engines`)은 서로 직접 참조하지 않는다(ADR-0035) — 이 절은 그
경계를 넘는 유일한 통로인 신규 최상위 패키지 `integration/`을
설명한다.

- **Workspace Adapter Layer**: `integration/`이 구현하는 계층
  이름(ADR-0039). "Adapter 3개"가 아니라, 외부 관심사(Vault,
  Workflow, Agent, 그리고 향후 Runtime/Service/Notification/Sync
  등)마다 하나씩 늘어나는 확장 가능한 계층으로 정의한다. 각
  Adapter는 **연결·변환·위임만** 담당하고 비즈니스 로직이나
  Workspace Intelligence(자연어 해석, 계획 수립 등)를 갖지 않는다.
- **구성원(Milestone 28-T03)**:
  - `vault_adapter.VaultAdapter` — `vault/`를 아는 유일한 Integration
    Layer 구성원. `create_task()`/`transition_task()`가 `vault.
    engine`/`vault.task_lifecycle`/`vault.task_sync`를 그대로
    호출한다. vault 내부 타입(`TaskStatus` 등)은 바깥에 노출하지
    않고 문자열로만 주고받는다.
  - `workflow_adapter.WorkflowAdapter` — `WorkflowEngine`/`TaskEngine`
    **Interface**에만 의존(Interface First, 구체 구현은 생성자로
    주입). `plan()`/`transition_task()`는 각각 Core Domain Engine을
    그대로 호출한다.
  - `agent_adapter.AgentAdapter` — `AgentManager`/`AgentRegistry`/
    `AgentScheduler` Interface에만 의존. `create_agent()`가
    `AgentManager.create()` + `AgentRegistry.register()`를 잇는다.
  - 세 Adapter는 서로를 참조하지 않는다 — Task↔Workflow 연결
    (M28-T04)/Workflow↔Agent 연결(M28-T05)은 이들을 조합해 쓰는
    상위 호출자(Conversation Layer, M28-T06)의 책임으로 남겨뒀다.
- **공유 기반 클래스를 두지 않은 이유**: 세 Adapter의 메서드
  시그니처가 서로 다른 관심사를 다뤄 억지로 공통 Interface를 뽑으면
  Speculative Generality가 된다(ADR-0039 결정 3). "Layer"는
  패키지 경계 + `XxxAdapter` 이름 규칙 + 이 문서로 정의하고,
  실제로 여러 Adapter가 공유해야 하는 필요가 생기면 그때 Interface를
  뽑는다.
- **경계 강제**: `tests/integration_layer/test_architecture_boundary.py`
  가 `ast` 모듈로 `src/ai_workspace/` 전체 import 문을 파싱해
  (a) Core Domain이 `vault`를 import하지 않는지, (b) `vault`가
  Core Domain을 import하지 않는지, (c) `integration/` 밖의 어떤
  파일도 둘을 동시에 import하지 않는지 확인한다 — §8 규칙 18을
  코드로 강제한다.
- 새 Core Domain Interface 없음(27종 그대로) — Integration Layer는
  기존 Interface에 의존만 하고 새 계약을 추가하지 않는다.

**구현 상태(Milestone 28-T04, Workflow Engine Integration)**:
`integration/workflow_task_link.py`의 `WorkflowTaskLink` — Vault
Task와 Core Domain `Workflow`/`Task`를 잇는다. 사용자가 T04 승인 시
제시한 4개 원칙을 그대로 지켰다:

1. Workflow↔Vault 직접 의존 없음 — 이 파일은 `vault`를 import하지
   않고 `VaultAdapter`/`WorkflowAdapter`만 조합한다.
2. 모든 연결이 Integration Layer 안에서만 이뤄진다 — `WorkflowTaskLink`
   자체가 `integration/`에 있고, 밖의 어떤 모듈도 두 Adapter를
   동시에 쓰지 않는다(경계 테스트가 계속 보장).
3. Domain 객체 오염 없음 — `Task`/`Workflow`에 새 필드를 추가하지
   않았다. 대신 Vault task_id와 Core Domain task_id(서로 다른
   문자열 공간 — Vault는 사람이 붙인 ID, Core Domain은 `TaskEngine`
   발급 ID)를 잇는 매핑은 이 파일의 `WorkflowLink` 값 객체가
   별도로 든다. 기존 `Task.workflow_id` 필드(원래부터 있던 Workflow
   소속 정보)를 그대로 채워 재사용했다.
4. Adapter는 연결·변환·위임만 — `WorkflowTaskLink`는 ID 변환과
   호출 순서 조합만 하고, 상태 전이 규칙은 여전히 `TaskEngine`/
   `vault.task_lifecycle`에 위임한다. `transition_and_reflect()`는
   Core Domain `TaskStatus`를 Vault 상태 문자열로 매핑(`BLOCKED`/
   `CANCELLED`는 대응 상태가 없어 의도적으로 Vault에 반영하지
   않음)하고, `is_workflow_complete()`는 Workflow 자체에 없는
   "종료" 개념을 Task 전체가 `DONE`인지로 파생 계산한다(Domain
   모델을 건드리지 않기 위함) — 둘 다 판단이 아니라 조회/변환이다.

`create_workflow_from_vault_tasks()`가 "Task → Workflow 생성",
`transition_and_reflect()`가 "Workflow 상태 변경 → Task 상태 반영",
`is_workflow_complete()`가 "Workflow 종료"에 대응한다(M25 요청
원문의 흐름 그대로). 새 Core Domain Interface 없음, `domain.Task`/
`domain.Workflow` 필드 추가 없음.

**Adapter vs Connector(Milestone 28-T05, ADR-0040)**: T04에서
`VaultAdapter`/`WorkflowAdapter`(외부 시스템 하나만 연결)와
`WorkflowTaskLink`(둘을 조합)가 서로 다른 책임임이 드러나, T05
(Agent Assignment) 착수 시 이를 공식 분류로 확정했다.

- **Adapter** — 외부 시스템 하나와의 연결만. 다른 Adapter를
  참조하지 않는다(ADR-0039 유지).
- **Connector** — 여러 Adapter를 조합해 유스케이스 하나를
  오케스트레이션한다. 자체 비즈니스 로직은 갖지 않고 Adapter가
  감싼 Core Domain Engine에 위임만 한다. **Connector도 유스케이스
  하나만 책임진다** — Connector끼리 서로 참조하지 않는다.

`integration/workflow_agent_link.py`의 `WorkflowAgentLink`(신규
Connector)가 이 원칙에 따라 Agent 배정 책임을 `WorkflowTaskLink`에
얹지 않고 분리됐다:

- `AgentAssignment`(값 객체) — `WorkflowLink` + `Agent`. `domain.
  Task`/`domain.Agent` 어느 쪽에도 필드를 추가하지 않는다(Domain
  오염 금지, T04와 동일 원칙) — 배정 관계는 `WorkflowAgentLink`가
  내부 상태로만 든다.
- `assign_agent()` — `AgentAdapter.select_agent()`(→
  `AgentScheduler`)로 고른 Agent를 Task에 배정한다("Agent
  Assignment"). 후보가 없으면 `NoAvailableAgentError`.
- `transition_agent_status()` — 배정된 Agent의 상태를 `AgentAdapter.
  transition_agent()`(→ `AgentManager`)에 위임해 전이한다("Agent
  Status" 추적). 배정 전이면 `AgentNotAssignedError`.
- `agent_progress()` — 해당 Agent에게 배정된 Task 중 Core Domain
  기준 `DONE` 비율("Agent Progress"). `Agent`에 진행률 필드가
  없으므로 배정 목록에서 매번 파생 계산한다.
- `AgentAdapter`(T03)를 그대로 재사용하므로 "Agent Registry 연동"/
  "Agent Manager 연동"은 추가 코드 없이 이미 충족된다(위임 자체가
  그 연동이다).

**Conversation Layer 연동 — Orchestrating Connector(Milestone
28-T06, ADR-0041)**: M28의 마지막 Task. Conversation Layer(사용자
입력 해석/요청 라우팅/결과 조합만 담당 — 자연어 해석 자체는
코드가 아니라 AI의 역할, M23-T06과 같은 전제)가 Task/Workflow/
Agent 요청을 처리하는 유일한 진입점으로
`integration/conversation_workflow_link.py`의
`ConversationConnector`를 도입했다.

- **Peer Connector vs Orchestrating Connector**(ADR-0040 확장):
  `WorkflowTaskLink`/`WorkflowAgentLink`는 유스케이스 하나만
  책임지고 서로 참조하지 않는 **Peer Connector**다.
  `ConversationConnector`는 여러 Peer Connector/Adapter를 조합해
  더 상위 유스케이스를 라우팅·조합하는 것 자체가 존재 이유인
  **Orchestrating Connector**로, ADR-0040 "Connector끼리 서로
  참조하지 않는다" 원칙의 명시적 예외다.
- `handle_task_request()` — "Task 생성 → Workflow 생성 → Agent
  Assignment → Vault 반영"(M25 요청 예시 흐름)을 `VaultAdapter.
  create_task()` → `WorkflowTaskLink.create_workflow_from_vault_tasks()`
  → `WorkflowAgentLink.assign_agent()` 순서로 그대로 호출한다.
- `advance_task()` — `WorkflowTaskLink.transition_and_reflect()`에
  그대로 위임(요청 라우팅).
- `report_status()` — `WorkflowTaskLink.get_task_status()`(신규,
  `WorkflowAdapter.get_task()` 위임)/`is_workflow_complete()`
  결과를 묶기만 한다("결과 조합").
- **Boundary**: Conversation Layer(호출자)와 `ConversationConnector`
  자신 둘 다 `vault`/`WorkflowEngine`/`TaskEngine`/`AgentManager`
  (및 구체 구현)를 직접 import하지 않는다 — `VaultAdapter`/
  `WorkflowTaskLink`/`WorkflowAgentLink`만 통해서 접근한다.
  `tests/integration_layer/test_conversation_connector_boundary.py`
  가 `ast`로 이를 강제한다. Domain 값 타입(`Task`/`Workflow`/
  `Agent`/`TaskStatus`/`AgentCapability`)은 메서드 시그니처에
  그대로 쓴다 — T03부터 Adapter가 이미 노출해 온 값이라 새로운
  경계 위반이 아니다.
- 새 비즈니스 로직 없음, 새 Core Domain Interface 없음, `domain.
  Task`/`domain.Workflow`/`domain.Agent` 필드 추가 없음.

**Milestone 28(Live Task Management & Integration) 전체 완료
(T01~T06).** Architecture Freeze(ADR-0042) 사용자 승인 완료. 다음은
Milestone 29(Project Intelligence).

### 3.22 Intelligence Layer (Milestone 29, ADR-0043, 설계: M29-T01)

Project/Workflow/Task/Agent 데이터를 종합해 **Project Snapshot/
Health/Risk/Recommendation**을 산출하는 **Read Only Query Layer**.
`integration/`(Integration Layer)과 같은 층위에서 그 위에 얹히는
신규 최상위 패키지 `intelligence/`로 만든다 — Integration Layer가
Core Domain↔Vault 경계를 잇는 것과 달리, Intelligence Layer는 아무
경계도 잇지 않고 Integration Layer가 이미 노출한 값만 읽어 **집계·
판단**한다(쓰기 없음, 새 비즈니스 로직 없음).

- **설계 결론(ADR-0043)**: Core Domain 27종 Interface에는 project
  단위 전체 목록 조회(`TaskEngine.list_tasks()` 등)가 없어 새
  Interface 없이는 Snapshot 자체가 불가능하다. 대신 `vault/`의
  `14 Tasks/*.md` 문서(M27/M28)가 파일 열거만으로 project 소속
  Task 전체를 이미 제공하므로, **Vault Task 문서를 M29의 단일
  데이터 소스로 채택**했다 — 새 Core Domain Interface를 추가하지
  않는다(27종 그대로).
- **데이터 접근 경로**(모두 기존 또는 소규모 확장, Interface
  아님):
  - `vault/task_query.py`(신규) — `14 Tasks/*.md`를 열거해
    frontmatter를 파싱한 `TaskDocument` 목록 반환. `vault/`
    안이라 Core Domain을 모른다(ADR-0035와 동일 원칙).
  - `VaultAdapter.list_tasks()`(신규 메서드, 기존 Adapter 클래스
    확장 — Interface 변경 아님) — 위 함수를 Integration Layer에
    노출.
  - `AgentAdapter.list_active_agents()`(기존, M28-T03) — Agent
    데이터는 신규 메서드 없이 그대로 재사용.
  - Event(EventStore)는 M29에서 데이터 소스로 쓰지 않는다(Adapter
    미존재, YAGNI — Vault `updated` 필드만으로 정체 판단이
    충분하다고 판단).
  - Workflow 단위 집계는 Vault Task의 `milestone` 필드로 근사한다
    (Vault에 Workflow 전용 문서 종류가 없음).
- **Blocked Task 근사**: Vault `TaskStatus`(todo/in-progress/
  review/done/archived)에는 Core Domain `TaskStatus.BLOCKED`에
  대응하는 값이 없다(두 enum은 ADR-0035에 따라 원래 독립). M29은
  "정체(Stagnant) = IN_PROGRESS/REVIEW 상태이면서 `updated`가
  임계일 이상 지난 Task"라는 Risk 규칙으로 "Blocked/장기 미진행"을
  근사한다(임계값은 M29-T03에서 확정).
- **경계 규칙(§8 규칙 21)**: `intelligence/`의 Analyzer는 오직
  `integration/`의 `VaultAdapter`/`AgentAdapter`에만 의존하고,
  `domain`/`interfaces`/`engines`/`vault`를 직접 import하지 않는다
  — `tests/intelligence/test_intelligence_layering.py`(M29-T02
  작성 예정)가 `ast` 기반으로 강제한다.
- **범위**: Snapshot(M29-T02, 완료)/Health·Risk(M29-T03)/
  Recommendation(M29-T04, Rule 기반, LLM 호출 없음)/Dashboard 또는
  Vault 노출(M29-T05). 새 Core Domain Interface 없음, `domain.
  Project`/`domain.Task` 필드 추가 없음.
- **M29-T02 구현 완료**: `vault/task_query.py`(신규,
  `list_task_documents()`) → `VaultAdapter.list_tasks()`(신규
  메서드) → `intelligence/snapshot.py`의 `ProjectSnapshotAnalyzer`
  (`ProjectSnapshot`: 상태별/Milestone별/Owner별 집계, progress_ratio,
  active_agent_count). `tests/intelligence/
  test_intelligence_layering.py`가 §8 규칙 21을 `ast` 기반으로
  강제.
- **M29-T03 구현 완료**: `intelligence/health_risk.py`의
  `ProjectHealthRiskAnalyzer`가 `ProjectSnapshotWithTasks`만 입력
  받아(Adapter 직접 호출 없음) Health(Healthy/Warning/Critical)와
  Risk(`stagnant_task`/`owner_overload`/`milestone_stall`, 전부
  Rule 기반)를 계산한다. "의존성 위험"은 Vault에 의존관계 필드가
  없고 필요한 Workflow 전체 열거 Interface도 없어(T01에서 확인한
  공백) M29 범위 밖으로 명시적으로 남긴다.
- **M29-T04 구현 완료**: `intelligence/recommendation.py`의
  `ProjectRecommendationEngine`이 Snapshot/Health/Risk만 입력으로
  받아(Adapter 미참조) Risk 하나당 추천 하나를 1:1로 매핑하고,
  전체 진행률이 낮을 때 project 단위 추천을 더한다. AI 추론/LLM
  호출 없음(M33 이후로 미룸).
- **M29-T05 구현 완료(Milestone 29 전체 완료)**: `intelligence/
  report.py`의 `ProjectIntelligenceService`가 세 Analyzer를
  Snapshot→Health/Risk→Recommendation 순서로 실행해
  `ProjectIntelligenceReport`를 만들고(`generate()`), Markdown으로
  렌더링해(`render_markdown()`) `VaultAdapter.
  publish_intelligence_report()`로 Vault에 노출한다(`publish()`).
  `vault/intelligence_report.py`(신규)가 `15 Project Intelligence/
  Project Intelligence.md`에 원자적으로 전체 교체(overwrite)한다
  — 기존 `VaultDocumentKind` 체계(Index append)를 쓰지 않는
  "생성된 리포트" 전용 경로다. Dashboard(`web/`) 연동 대신 Vault
  노출을 선택했다(DoD가 "Dashboard 또는 Vault" 중 하나를 요구,
  FastAPI 서버 통합은 범위 확장이라 YAGNI로 보류). `intelligence/`
  경계(§8 규칙 21)는 그대로 유지 — `report.py`도 `VaultAdapter`/
  `AgentAdapter`에만 의존한다.

### 3.23 Context Intelligence (Milestone 30, ADR-0044, 설계: M30-T01)

Milestone 16의 Knowledge Layer(§3.14)와 Milestone 29의 Intelligence
Layer(§3.22)를 종합해, 지금 진행 중인 작업(Task/Milestone)과 관련된
**맥락(Context)**을 모아 `ProjectContext`로 정리하는 Read Only 계층.
새 지식을 만들지 않고, LLM 추론도 하지 않는다 — 이미 있는 Knowledge
문서를 구조적으로 파싱·필터링할 뿐이다.

- **설계 결론(ADR-0044)**: `KnowledgeRepository`/`KnowledgeSearch`
  (M16, 27종 Interface 중 2종)를 그대로 재사용한다 — 새 Core Domain
  Interface를 추가하지 않는다. 대신 신규 Integration Layer Adapter
  `KnowledgeAdapter`(`integration/knowledge_adapter.py`)가 이 두
  Interface만 감싸고, `intelligence/context.py`의 `ContextAnalyzer`
  가 `KnowledgeAdapter.list_all()`이 반환한 문서 전체 텍스트를
  Markdown 제목(`#`/`##`/`###`) 단위로 쪼개 subject(Task/Milestone
  식별자)가 언급된 항목만 `ContextEntry`로 채택한다 — 이 저장소가
  제목에 ADR/Milestone 번호를 담는 실제 작성 관례를 그대로
  이용한다.
- **Freshness/Gap**(`intelligence/context_quality.py`): Freshness는
  제목에서 추출한 Milestone 번호와 현재 Milestone의 거리로
  판단한다(파일 mtime은 이 저장소가 매 세션 fresh clone이라
  무의미, git log 조회는 Adapter의 "외부 시스템 하나만" 원칙과
  충돌해 채택하지 않음). Gap은 ADR/TASK/ARCHITECTURE 3종에서 subject
  언급이 0건일 때만 판정한다(RULE/PROJECT는 범용 문서라 제외).
- **경계**: `intelligence/context*.py`는 오직 `integration/`의
  `KnowledgeAdapter`에만 의존한다(§8 규칙 21 그대로 적용, 새 규칙
  추가 없음).
- **범위**: Context Analyzer(M30-T02, 완료)/Freshness & Gap Analyzer
  (M30-T03)/Integration(M30-T04, `ContextIntelligenceService`)/
  Presentation(M30-T05, Vault 노출). 새 Core Domain Interface
  없음, `domain/` 필드 추가 없음.
- **M30-T02 구현 완료**: `integration/knowledge_adapter.py`(신규
  Adapter, `KnowledgeRepository`/`KnowledgeSearch`만 감쌈) →
  `intelligence/context.py`의 `ContextAnalyzer`(Markdown 제목 단위
  평면 분할 + subject 표기 변형 대조로 `ProjectContext` 생성).
- **M30-T03 구현 완료**: `intelligence/context_quality.py`의
  `ContextFreshnessGapAnalyzer`가 `ProjectContext`만 입력으로
  받아(Adapter 미참조) Gap(ADR/TASK/ARCHITECTURE 언급 0건)과
  Freshness(Milestone 번호 거리, `current_milestone` 생략 시 항상
  Healthy)를 계산한다.
- **M30-T04 구현 완료**: `intelligence/context_service.py`의
  `ContextIntelligenceService`가 `KnowledgeAdapter`만 생성자로
  받아 `ContextAnalyzer`→`ContextFreshnessGapAnalyzer` 순서로
  실행해 `ProjectContextReport`를 만든다.
- **M30-T05 구현 완료(Milestone 30 전체 완료)**: `context_service.py`
  에 `render_markdown()`/`publish()`를 추가해 `VaultAdapter.
  publish_project_context()`로 `15 Project Intelligence/Project
  Context.md`에 노출한다(M29-T05와 동일 패턴, 같은 폴더 재사용).
  실제 검증 중 Milestone 추출이 본문 "첫 언급"을 잘못 고르는
  버그를 발견해 "subject와 위치가 가장 가까운 언급"으로
  수정했다(`context.py`).

### 3.24 Capability Intelligence (Milestone 31, ADR-0045, 설계: M31-T01)

Milestone 28의 Agent Adapter(§3.19류)가 노출한 활성 Agent 정보를
종합해, 정의된 `AgentCapability`(11종) 대비 지금 실제로 커버되는
Capability가 무엇인지 `CapabilityIntelligenceReport`로 정리하는
Read Only 계층. 새 데이터를 만들지 않고, LLM 추론도 하지 않는다 —
이미 있는 `AgentAdapter`가 노출한 값만 집계·판단할 뿐이다.

- **설계 결론(ADR-0045)**: `AgentManager`/`AgentRegistry`/
  `AgentScheduler`(M28, 27종 Interface 중 3종)를 이미 감싸는 기존
  `AgentAdapter`를 그대로 재사용한다 — 새 Adapter/Core Domain
  Interface를 추가하지 않는다. `AgentAdapter`에 `list_active_agent_
  capabilities()`(활성 Agent를 `AgentCapabilityView`로 열거)/
  `known_capabilities()`(정의된 `AgentCapability` 전체를 문자열
  카탈로그로 노출) 두 메서드만 추가했다(M30이 `VaultAdapter`에
  `publish_project_context()`를 추가한 것과 같은 방식 — 새 Adapter가
  아니라 기존 Adapter 확장).
- **Coverage/Gap**(`intelligence/capability_gap.py`): Gap은 "정의된
  Capability 중 활성 Agent가 0명인 것"으로 판정한다. Coverage
  등급은 M29/M30의 healthy/warning/critical과 달리 중립적인
  none/partial/full을 쓴다 — 활성 Agent 0명은 이 저장소가 아직
  Agent 프로세스를 상시 구동하지 않는 워크숍 단계의 자연스러운
  상태이지 시스템 이상이 아니기 때문이다(M29 `active_agent_count`도
  항상 0으로 관찰됨, 같은 한계를 M31도 그대로 인정하고 넘어간다).
- **경계**: `intelligence/capability*.py`는 오직 `integration/`의
  `AgentAdapter`에만 의존한다(§8 규칙 21 그대로 적용, 새 규칙 추가
  없음).
- **범위**: Capability Snapshot Analyzer(M31-T02)/Coverage & Gap
  Analyzer(M31-T03)/Integration(M31-T04, `CapabilityIntelligenceService`)/
  Presentation(M31-T05, Vault 노출). 새 Core Domain Interface 없음,
  `domain/` 필드 추가 없음.
- **M31-T02 구현 완료**: `integration/agent_adapter.py`에
  `list_active_agent_capabilities()`/`known_capabilities()` 추가 →
  `intelligence/capability.py`의 `CapabilitySnapshotAnalyzer`가
  활성 Agent를 Capability/Role별로 집계해 `AgentCapabilitySnapshot`
  을 만든다.
- **M31-T03 구현 완료**: `intelligence/capability_gap.py`의
  `CapabilityGapAnalyzer`가 `AgentCapabilitySnapshot`만 입력으로
  받아(Adapter 미참조) Coverage(none/partial/full)와 Gap(Capability
  별 활성 Agent 0명 여부)을 계산한다.
- **M31-T04 구현 완료**: `intelligence/capability_service.py`의
  `CapabilityIntelligenceService`가 `AgentAdapter`만 생성자로 받아
  `CapabilitySnapshotAnalyzer`→`CapabilityGapAnalyzer` 순서로 실행해
  `CapabilityIntelligenceReport`를 만든다.
- **M31-T05 구현 완료(Milestone 31 전체 완료)**: `capability_service.py`
  에 `render_markdown()`/`publish()`를 추가해 `VaultAdapter.
  publish_capability_report()`로 `15 Project Intelligence/
  Capability Intelligence.md`에 노출한다(M29-T05/M30-T05와 동일
  패턴, 같은 폴더 재사용).

### 3.25 Intelligence Synthesis (Milestone 32, ADR-0046, 설계: M32-T01)

M29(Project Intelligence, §3.22)/M30(Context Intelligence, §3.23)/
M31(Capability Intelligence, §3.24)이 각각 독립적으로 계산한 리포트를
새로운 데이터 소스나 판단 기준 없이 하나의 `IntelligenceOverview`로
합성하는 Read Only 계층. 세 Milestone을 잇는 통합 계층(Integration
at the Intelligence Layer)으로, M29~M31 위에 새 기능을 얹는 것이
아니라 이미 있는 것을 조합해 마무리하는 성격의 Milestone이다.

- **설계 결론(ADR-0046)**: 새 Adapter/Interface를 만들지 않는다.
  `intelligence/synthesis.py`의 `IntelligenceSynthesisAnalyzer`는
  이미 생성된 세 리포트(`ProjectIntelligenceReport`/
  `ProjectContextReport`/`CapabilityIntelligenceReport`)만 입력으로
  받는 순수 함수 계층이다 — Adapter를 전혀 참조하지 않는다.
- **§8 규칙 21과의 관계**: 규칙 21("`intelligence/`의 Analyzer는
  `integration/`의 Adapter에만 의존")은 변경 없이 그대로 적용된다.
  `IntelligenceSynthesisAnalyzer`/`IntelligenceSynthesisService`는
  Adapter가 아니라 **같은 `intelligence/` 계층의 다른 Service**
  (`report.py`/`context_service.py`/`capability_service.py`)를
  조합하므로 애초에 이 규칙이 금지하는 대상이 아니다 —
  `tests/intelligence/test_intelligence_layering.py`를 코드 변경
  없이 그대로 실행해 위반이 없음을 확인했다.
- **집계와 조합의 분리(M29/M30/M31과 동일한 2단 구조)**:
  `intelligence/synthesis.py`의 `IntelligenceSynthesisAnalyzer`는
  세 리포트의 등급(Health/Freshness/Coverage)과 Risk/Gap을 하나의
  `SynthesizedFinding` 목록으로 모으기만 한다(target 기준 정렬 외
  새 우선순위 알고리즘·새 임계값 없음). `intelligence/
  synthesis_service.py`의 `IntelligenceSynthesisService`가 세
  Service(`ProjectIntelligenceService`/`ContextIntelligenceService`/
  `CapabilityIntelligenceService`)를 생성자로 받아 순서대로 실행한
  뒤 Analyzer에 넘기는 조합 책임만 진다(M29-T05 `report.py`와 동일한
  Orchestrating 패턴을 Service 3개 조합 층위로 한 단계 더 얹음).
- **경계**: `intelligence/synthesis*.py`는 `intelligence/report.py`/
  `context_service.py`/`capability_service.py`(같은 계층의 Service)
  에만 의존하고, `integration/`/`domain/`/`interfaces/`/`engines/`/
  `vault`를 직접 import하지 않는다.
- **범위**: Synthesis Analyzer(M32-T02, 완료)/Integration(M32-T03,
  `IntelligenceSynthesisService`)/Presentation(M32-T03, Vault 노출)/
  E2E 검증·문서화(M32-T04). 새 Core Domain Interface 없음, `domain/`
  필드 추가 없음.
- **M32-T02 구현 완료**: `intelligence/synthesis.py`의
  `IntelligenceSynthesisAnalyzer`(`SynthesizedFinding`/
  `IntelligenceOverview` 신규 값 객체)가 세 리포트를 조합한다.
- **M32-T03 구현 완료**: `intelligence/synthesis_service.py`의
  `IntelligenceSynthesisService`가 세 Service를 조합해
  `generate()`/`publish()`를 제공하고, `vault/
  intelligence_overview.py`(신규) → `VaultAdapter.
  publish_intelligence_overview()`(신규 메서드)로 `15 Project
  Intelligence/Intelligence Overview.md`에 노출한다.
- **M32-T04 구현 완료(Milestone 32 전체 완료)**: 전체 스택 통합
  테스트로 Vault 노출까지 검증, 문서화 완료. `docs/ARCHITECTURE.md`/
  `.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones
  Index) 갱신 확인.

### 3.26 Session Resume (Milestone 33, ADR-0047, 설계: M33-T01)

새 세션 시작 시 "지금 무엇을 하고 있었는가"를 자동 복원하는 Read
Only 계층. M29(Project Intelligence)/M30(Context Intelligence)/
M31(Capability Intelligence)/M32(Intelligence Synthesis)를 그대로
재사용하고, "현재 작업(Current Work)" 판정 규칙 1개만 새로 더한다
— Intelligence Layer를 처음으로 실제 사용 시나리오(세션 시작)에
연결하는 Execution 쪽 첫 기능이다.

- **M8 세션 연속성과의 구분**: M8(`PlanningAgent`의
  `memory_snapshot_id` 자동 복원)은 Agent 실행 컨텍스트(LLM에
  넘길 요약 텍스트)를 `ContextManager`/`MemoryEngine`으로 복원하는
  내부 메커니즘이다. M33 Session Resume은 사람이 읽는 보고서를
  Intelligence Layer에서 만드는 Read Only Query Layer로, Interface·
  Layer가 M8과 겹치지 않는다.
- **설계 결론(ADR-0047)**: 새 Adapter/Interface를 만들지 않는다.
  "현재 작업" 판정은 `VaultAdapter.list_tasks()`(M29부터 존재)가
  이미 노출한 `status`/`updated` 값에서 "활성 상태(in-progress/
  review) Task 중 `updated`가 가장 최근인 1건"을 고르는 순수
  선택 로직(`intelligence/session_resume.py`의
  `CurrentWorkSelector`)일 뿐, 새 지표·점수가 아니다.
- **조합 방식**: `intelligence/session_resume_service.py`의
  `SessionResumeService`가 `VaultAdapter` + `ProjectIntelligenceService`/
  `ContextIntelligenceService`/`CapabilityIntelligenceService`(M29~M31)
  + `IntelligenceSynthesisAnalyzer`(M32, Overview 합성 로직 재사용)를
  조합한다. M32 `IntelligenceSynthesisService`를 감싸지 않고
  Analyzer만 재사용하는 이유는 M29 `ProjectIntelligenceReport.
  recommendations`("다음 작업")가 Overview 밖에 있어 직접 필요하기
  때문이다 — 세 리포트를 어차피 손에 쥐고 있어야 한다.
- **"다음 작업"은 새로 만들지 않는다**: M29-T04가 이미 계산해 둔
  `ProjectRecommendation`을 그대로 옮겨 담는다(DRY, AI 추론 없음).
- **경계**: `intelligence/session_resume*.py`는 `integration/`의
  `VaultAdapter`(기존 허용 Adapter)와 `intelligence/`의 기존
  Service/Analyzer에만 의존한다(§8 규칙 21 그대로 적용, 새 규칙
  추가 없음).
- **범위**: Current Work Selector(M33-T02, 완료)/Integration
  (M33-T03, `SessionResumeService`)/Presentation(M33-T04, Vault
  노출). CLI 노출·자동 트리거(세션 시작 Hook/Automation Engine
  연결)는 범위 밖(M29~M32와 동일하게 Vault 노출까지만, YAGNI). 새
  Core Domain Interface 없음, `domain/` 필드 추가 없음.
- **M33-T02 구현 완료**: `intelligence/session_resume.py`의
  `CurrentWork`/`CurrentWorkSelector`(활성 Task 중 `updated` 최신
  1건 선택, 동률이면 `task_id`가 더 큰 쪽, 활성 Task 없으면
  `None`).
- **M33-T03 구현 완료**: `intelligence/session_resume_service.py`의
  `SessionResumeService`가 Current Work 판정 → subject/milestone
  결정 → Project/Context/Capability 리포트 생성 → Overview 합성을
  한 번에 실행해 `SessionResumeReport`를 만든다.
- **M33-T04 구현 완료(Milestone 33 전체 완료)**: `session_resume_
  service.py`에 `render_markdown()`/`publish()`를 추가해
  `VaultAdapter.publish_session_resume()`(신규 메서드)로 `15
  Project Intelligence/Session Resume.md`에 노출한다(M29~M32와
  동일 패턴, 같은 폴더 재사용).

### 3.27 Workflow Intelligence (Milestone 34, ADR-0048, 설계: M34-T01)

Vault Task 문서의 Milestone별 Task 실행 흐름을 분석하는 Read Only
계층. **여기서 "Workflow"는 `domain.Workflow`(§4의 `Workflow` 값
객체, 휘발성 in-memory DAG, 영속 저장소 없음)가 아니라 Milestone
안의 Task 실행 순서를 가리킨다** — 착수 전 조사로 `domain.Workflow`
인스턴스를 조회할 수 있는 기존 데이터 소스가 이 저장소에 없음을
확인했고(`WorkflowAdapter`에 `list_workflows()`류 메서드 없음), M29
Project Intelligence조차 `domain.Workflow`를 참조하지 않는다는 점을
근거로 "Workflow"의 의미를 이 저장소의 실제 데이터 현실(Milestone
Task 실행 순서)에 맞게 재정의했다.

- **`domain.Workflow`/`WorkflowEngine`/`WorkflowAdapter`와의 구분**:
  이번 Milestone에서 전혀 사용하지 않는다. 새 영속 계층을 만들어
  `Workflow` 인스턴스를 저장하기 시작하는 것은 Scope를 크게 키우는
  선택이라 채택하지 않았다(YAGNI, ADR-0048).
- **Blocked/Next 판정 Rule(ADR-0048)**: Task ID(`M{n}-T{nn}`)의
  T-번호로 같은 Milestone 내 Task를 정렬했을 때, `status`가 `todo`
  이면서 선행 Task 중 완료(`done`/`archived`)가 아닌 것이 하나라도
  있으면 Blocked, 선행이 전부 완료된 `todo` Task는 Next다.
  `in-progress`/`review`는 진행 중, `done`/`archived`는 완료로
  그대로 노출한다 — 새 상태 분류를 만들지 않는다.
- **Analyzer/Service 책임 분리**: 판정 규칙은
  `intelligence/workflow_flow.py`의 `WorkflowFlowAnalyzer`(순수
  Analyzer, `VaultAdapter.list_tasks()`가 반환하는 `TaskDocumentView`
  목록만 입력)에 전부 캡슐화하고, `intelligence/workflow_service.py`
  의 `WorkflowIntelligenceService`는 `VaultAdapter` 조회 + Analyzer
  실행 조합·오케스트레이션만 담당한다(M29
  `ProjectSnapshotAnalyzer`/`HealthRiskAnalyzer`와 Service를 분리해
  온 기존 패턴과 동일) — M35(Recommendation)/M36(Automation)이
  `WorkflowFlowAnalyzer`를 그대로 재사용할 수 있게 하기 위함이다.
- **경계**: `intelligence/workflow_flow.py`/`workflow_service.py`는
  `integration/`의 `VaultAdapter`(기존 허용 Adapter)에만 의존한다
  (§8 규칙 21 그대로 적용, 새 규칙 추가 없음).
- **범위**: Workflow Flow Analyzer(M34-T02, 완료)/Integration
  (M34-T03, `WorkflowIntelligenceService`)/Presentation(M34-T04,
  Vault 노출). CLI 노출·자동 트리거·M35 Recommendation·M36
  Automation 연동은 범위 밖(M29~M33과 동일하게 Vault 노출까지만,
  YAGNI). 새 Core Domain Interface 없음, `domain/` 필드 추가 없음.
- **M34-T02 구현 완료**: `intelligence/workflow_flow.py`의
  `WorkflowFlowAnalyzer.analyze()` — Milestone별로 Task를 T-번호
  순으로 정렬하고 Blocked/Next/진행 중/완료를 판정한 `MilestoneFlow`
  목록(`WorkflowFlowReport`)을 만든다. 미완료 Task가 없는(이미 끝난)
  Milestone은 결과에서 제외한다.
- **M34-T03 구현 완료**: `intelligence/workflow_service.py`의
  `WorkflowIntelligenceService.generate()`가 `VaultAdapter.
  list_tasks()` 조회 → `WorkflowFlowAnalyzer.analyze()` 실행을
  그대로 위임한다.
- **M34-T04 구현 완료(Milestone 34 전체 완료)**:
  `workflow_service.py`에 `render_markdown()`/`publish()`를 추가해
  `VaultAdapter.publish_workflow_intelligence()`(신규 메서드)로 `15
  Project Intelligence/Workflow Intelligence.md`에 노출한다
  (M29~M33과 동일 패턴, 같은 폴더 재사용).

### 3.28 Recommendation Intelligence (Milestone 35, ADR-0049, 설계: M35-T01)

M29(Project)/M31(Capability)/M33(Session Resume)/M34(Workflow)
Intelligence를 그대로 조합해 "지금 무엇을 하는 것이 가장 적절한가"를
결정하는 Read Only Decision Layer. **Execution Layer 이전의 마지막
Decision Layer**이며, 자동으로 실행하지 않고 추천만 제공한다 —
Task 상태 전이·Workflow 수정·Task 생성을 수행하지 않는다(Automation은
M36 이후).

- **5단계 Priority Rule(ADR-0049)**: 순서대로 첫 번째로 해당하는
  조건에서 멈추고 단일 `NextAction`을 고른다 — ① Current Work(M33
  `CurrentWorkSelector`)가 있으면 계속 수행 ② Workflow Intelligence
  (M34)의 Next Task가 있으면 시작 추천 ③ Blocked Task가 있으면 해소
  추천 ④ Capability Gap(M31)이 있으면 보완 추천 ⑤ M29
  `ProjectRecommendation` 중 priority(high>medium>low, 동률이면
  target 사전순)가 가장 높은 것을 그대로 노출. 다섯 조건 모두 해당
  없으면 `next_action=None`("추천할 다음 행동 없음").
- **새로운 Intelligence를 계산하지 않는다**: M29
  `ProjectIntelligenceService.generate().recommendations`, M31
  `CapabilityIntelligenceService.generate().gap_report`, M33
  `CurrentWorkSelector`(Analyzer만 재사용, M33 Service 전체를 감싸지
  않음 — Context Intelligence까지 포함된 `SessionResumeService`는
  M35에서 불필요), M34 `WorkflowFlowAnalyzer`(Analyzer만 재사용)를
  입력으로 그대로 소비한다. 새 지표·점수·Health/Risk 분류가 없다.
- **Analyzer/Service 책임 분리**: 판정 규칙은
  `intelligence/recommendation_rules.py`의
  `RecommendationRuleAnalyzer`(순수 Analyzer)에 전부 캡슐화하고,
  `intelligence/recommendation_service.py`의
  `RecommendationIntelligenceService`는 `VaultAdapter.list_tasks()`
  1회 조회 + `ProjectIntelligenceService`/`CapabilityIntelligenceService`
  (주입) 실행 + `CurrentWorkSelector`/`WorkflowFlowAnalyzer`(같은
  tasks 목록 재사용) 실행 + Analyzer 호출을 조합만 담당한다(M29/M34
  Analyzer/Service 분리 패턴과 동일) — Automation(M36 이후)이
  `RecommendationRuleAnalyzer`를 그대로 재사용할 수 있게 하기 위함이다.
- **경계**: `intelligence/recommendation_rules.py`/
  `recommendation_service.py`는 `integration/`의 `VaultAdapter`(기존
  허용 Adapter)와 `intelligence/`의 기존 Service/Analyzer에만
  의존한다(§8 규칙 21 그대로 적용, 새 규칙 추가 없음).
- **범위**: RecommendationRuleAnalyzer(M35-T02, 완료)/Integration
  (M35-T03, `RecommendationIntelligenceService`)/Presentation
  (M35-T04, Vault 노출). Task 우선순위 재계산·AI 추론·점수 계산·
  Workflow 수정·Task 생성·Automation·CLI·Hook은 범위 밖(YAGNI). 새
  Core Domain Interface 없음, `domain/` 필드 추가 없음.
- **M35-T02 구현 완료**: `intelligence/recommendation_rules.py`의
  `RecommendationRuleAnalyzer.analyze()` — Current Work/Workflow
  Next/Workflow Blocked/Capability Gap/Project Recommendation을
  순서대로 확인해 단일 `NextAction`(또는 `None`)을 반환한다.
- **M35-T03 구현 완료**: `intelligence/recommendation_service.py`의
  `RecommendationIntelligenceService.generate()`가 Task 목록 1회
  조회 → Current Work/Workflow Flow 계산 → Project/Capability
  리포트 생성 → Rule Analyzer 실행을 한 번에 수행해
  `RecommendationIntelligenceReport`를 만든다.
- **M35-T04 구현 완료(Milestone 35 전체 완료)**:
  `recommendation_service.py`에 `render_markdown()`/`publish()`를
  추가해 `VaultAdapter.publish_recommendation_intelligence()`(신규
  메서드)로 `15 Project Intelligence/Recommendation Intelligence.md`
  에 노출한다(M29~M34와 동일 패턴, 같은 폴더 재사용).

### 3.29 Execution (Milestone 36, ADR-0050, 설계: M36-T01)

M35 `NextAction`의 `source=next_task` 추천만, 수동 트리거로만,
이미 존재하는 `ExecutionDispatcher`(M18)/`EngineRegistry`/
`EngineSelectionPolicy`(M17) 파이프라인에 연결해 실제로 실행하고
결과를 Vault에 보고한다. **M29~M35와 달리 Read Only가 아니라 실제
부작용(AI Engine 실행)을 일으키는 첫 Milestone**이며, 그 위험을
반영해 범위를 최소로 좁혔다.

- **위치**: `intelligence/`(Read Only, §8 규칙 21)에 두지 않고
  `runtime/execution/`(기존 Layer, `execution_dispatcher.py`와 같은
  디렉터리)에 신규 파일만 추가했다 — 새 top-level 패키지·새 Layer
  없음. `runtime/execution/recommendation_execution_service.py`는
  `intelligence/recommendation_service.py`(M35, NextAction 계산)와
  `integration/vault_adapter.py`(결과 보고)를 모두 참조하는 첫
  `runtime/` 모듈이다 — `tests/integration_layer/
  test_architecture_boundary.py`(§8 규칙 18)는 `ai_workspace.vault`
  직접 import만 금지하므로 `VaultAdapter`(Integration Layer의
  사용 허가된 통로)를 통한 이 참조는 위반이 아니다(실제로 pytest로
  확인).
- **실행 대상 범위(ADR-0050)**: `NextAction`의 5가지 source 중
  `next_task`만 실행 대상이다. `current_work`/`blocked_task`/
  `capability_gap`/`project_recommendation`은 "지원하지 않음(Not
  Supported)"으로 명시적으로 표현한다 — 오류가 아니라 Scope 밖이라는
  뜻이다.
- **수동 트리거만**: `AutomationScheduler`(M21)에 연결하지 않는다.
  `ExecutionGate.check(next_action, *, manual_trigger)`가
  `manual_trigger=True`를 호출자가 명시적으로 전달했을 때만
  승인한다 — 사람 개입 없는 완전 자동화는 범위 밖(YAGNI, 위험
  최소화).
- **Gate/Builder 책임 분리**: `runtime/execution/
  recommendation_execution_gate.py`의 `ExecutionGate`는 source/
  manual_trigger/next_task 여부만 확인해 `GateDecision(approved,
  reason)`을 반환한다(판정만). `runtime/execution/
  recommendation_action_builder.py`의 `ActionBuilder`는 승인된
  `NextAction`을 `domain.automation.Action(kind=RUN_TASK, ...)`로
  변환만 한다(변환만). 다음 Milestone에서 `blocked_task`용 새 Gate
  Rule을 추가하기 쉽도록 두 책임을 분리했다.
- **`AutomationActionExecutor`(M21)를 감싸지 않고 재사용**:
  `EngineRegistry.list_candidates()` → `EngineSelectionPolicy.
  select()` → `ExecutionDispatcher.dispatch()` 3단계를
  `RecommendationExecutionService`가 직접 재사용한다.
  `AutomationActionExecutor.__call__()`은 `EngineExecutionResult`를
  버리는 `Callable[[AutomationRule], None]` 계약(`AutomationScheduler`
  가 의존)이라 실행 결과를 Vault에 보고할 수 없어, 그 계약을 바꾸지
  않고 같은 3개 기존 컴포넌트만 재사용했다(새 Interface/Engine/
  Dispatcher 없음).
- **Task 상태 자동 전이 없음**: 실행 성공 시에도 Vault Task를
  자동으로 `done`으로 전이하지 않는다 — 실패 처리 정책까지 함께
  설계해야 해 Scope가 커지기 때문이다. `VaultAdapter.
  transition_task()`(기존)로 이미 가능한 능력이라 필요성이 확인되면
  다음 Milestone에서 추가한다. M36은 실행 결과를 새 Vault 문서에
  보고만 한다.
- **경계**: `runtime/execution/recommendation_execution_service.py`
  는 `intelligence/recommendation_service.py`(M35)와
  `integration/vault_adapter.py`(기존 허용 Adapter) +
  `interfaces/engine_registry.py`/`interfaces/
  engine_selection_policy.py`/`runtime/execution/
  execution_dispatcher.py`(M17/M18, 기존)에만 의존한다.
- **범위**: ExecutionGate + ActionBuilder(M36-T02, 완료)/Integration
  (M36-T03, `RecommendationExecutionService`)/Presentation(M36-T04,
  Vault 노출). `current_work`/`blocked_task`/`capability_gap`/
  `project_recommendation`의 실행·`AutomationScheduler` 자동 트리거
  연결·Task 상태 자동 전이·CLI·Hook은 범위 밖(YAGNI). 새 Core Domain
  Interface 없음, `domain/` 필드 추가 없음.
- **M36-T02 구현 완료**: `ExecutionGate.check()`/`ActionBuilder.
  build()` — 판정과 변환을 각각 순수 함수로 분리 구현.
- **M36-T03 구현 완료**: `recommendation_execution_service.py`의
  `RecommendationExecutionService.execute()`가 `NextAction` 계산 →
  Gate 판정 → (승인 시) Action 변환 → `ExecutionDispatcher.
  dispatch()`를 한 번에 수행해 `RecommendationExecutionOutcome`을
  만든다.
- **M36-T04 구현 완료(Milestone 36 전체 완료)**:
  `recommendation_execution_service.py`에 `render_markdown()`/
  `publish()`를 추가해 `VaultAdapter.
  publish_recommendation_execution()`(신규 메서드)로 `15 Project
  Intelligence/Recommendation Execution.md`에 노출한다(M29~M35와
  동일 패턴, 같은 폴더 재사용).

### 3.30 Task Lifecycle (Milestone 37, ADR-0051, 설계: M37-T01)

M36 Execution 결과(Gate 승인/실행 성공·실패)를 이미 존재하는 Task
상태 전이 기계(`vault/task_lifecycle.py`의 `_ALLOWED_TRANSITIONS`,
M28)에 연결한다. **새 상태·새 전이 규칙·새 Adapter를 전혀 만들지
않는다** — M36 ADR-0050 결정 5가 미뤄 둔 "Task 상태 자동 전이"를
이번에 구현하되, 이미 검증된 상태 전이 기계 그대로만 사용한다.

- **전이 규칙(ADR-0051)**: 실행 시작 시 `todo→in-progress`, 실행
  성공 시 `in-progress→review`(사람 검토 대기), 실행 실패 시
  `in-progress→todo`(되돌려 재시도 가능하게). **`review→done`은
  자동화하지 않는다** — `_ALLOWED_TRANSITIONS`상 허용돼 있지만, 이
  프로젝트 전체가 항상 사람이 Review를 거쳐 Done을 확정해 온 실제
  작업 흐름(M29~M36 모든 Milestone Review도 사용자 최종 승인을
  거침)과 어긋나기 때문이다.
- **방어적 판정**: `runtime/execution/recommendation_task_lifecycle.py`
  의 `TaskLifecycleTransitioner`는 현재 상태를 먼저 확인하고, 예상과
  다르면 전이하지 않는다(`decide_start()`/`decide_completion()`
  둘 다 조건에 맞지 않으면 `None` 반환) — Gate 승인 시점과 실제
  전이 시점 사이에 Task 상태가 이미 바뀌어 있어도
  `InvalidTaskTransitionError`를 던지는 대신 조용히 건너뛴다(사용자
  권고).
- **현재 상태 재조회 없음**: `RecommendationExecutionService.
  execute()`는 새 Vault 읽기 경로를 만들지 않고, 이미 계산된
  `report.workflow_report`의 `TaskFlowEntry.status`(M34)를
  `ActionBuilder.find_entry()`(M37을 위해 공개 메서드로 확장,
  ADR-0051 결정 3)로 재사용한다.
- **Presentation 분리**(사용자 권고): `recommendation_execution_service.py`
  의 `render_markdown()`을 `_render_execution_section()`(M36의
  Gate/Action/실행 결과)과 `_render_lifecycle_section()`(신규, Task
  Status 이력)으로 나눠 각각 다른 책임만 갖게 한다. 같은 Vault 문서
  (`Recommendation Execution.md`) 안에 별도 섹션(`## Task Status
  이력`)으로 노출한다 — 새 Vault 파일은 만들지 않는다(YAGNI).
- **경계**: `runtime/execution/recommendation_task_lifecycle.py`는
  `vault.task_lifecycle.TaskStatus`를 직접 import하지 않고 문자열
  status 값만 주고받는다 — `VaultAdapter.transition_task()`가 이미
  문자열 인터페이스이기 때문이다(§8 규칙 18/19 경계를 넘지 않음).
- **범위**: `TaskLifecycleTransitioner`(M37-T02, 완료)/Integration
  (M37-T03, `RecommendationExecutionService` 확장)/Presentation
  분리(M37-T04, `render_markdown()` 리팩터). `done→archived` 자동화·
  재시도 정책·`review→done` 자동화·`AutomationScheduler` 연결·
  CLI·Hook은 범위 밖(YAGNI). 새 Core Domain Interface/Adapter 없음,
  `_ALLOWED_TRANSITIONS` 무변경.
- **M37-T02 구현 완료**: `TaskLifecycleTransitioner.decide_start()`/
  `decide_completion()` — 현재 상태를 확인하고 유효한 전이만 결정
  하는 순수 함수 2개.
- **M37-T03 구현 완료**: `RecommendationExecutionService.execute()`
  가 Gate 승인 → `decide_start()` → (전이 시) `VaultAdapter.
  transition_task()` → `ExecutionDispatcher.dispatch()` →
  `decide_completion()` → (전이 시) `VaultAdapter.transition_task()`
  순서로 호출해 `RecommendationExecutionOutcome.
  lifecycle_transitions`(신규 필드)에 전이 이력을 담는다.
- **M37-T04 구현 완료(Milestone 37 전체 완료)**: `render_markdown()`
  을 `_render_execution_section()`/`_render_lifecycle_section()`으로
  분리해 `Recommendation Execution.md`에 "Task Status 이력" 섹션을
  추가 노출한다. `VaultAdapter` 확장 없음(M35/M36과 달리 새 메서드
  추가도 없음 — `transition_task()`가 이미 있었음).

### 3.31 AutomationScheduler 연결 (Milestone 38, ADR-0052, 설계: M38-T01)

M21 `AutomationScheduler`와 M35~M37 Recommendation Execution 파이프라인을
`web/server.py`의 `build_app()`(Composition Root)에서 실제로 연결한다.
**새 기능이 아니라 배선(Wiring) Milestone이다** — M29~M37이 만든
`VaultAdapter`/`AgentAdapter`/`RecommendationIntelligenceService`/
`RecommendationExecutionService`는 이 Milestone 전까지 `tests/`에서만
조립됐고 실제 서버에는 한 번도 연결된 적이 없었다("워크숍 단계" 한계,
M37 완료 노트).

- **새 정책 없음**: `ExecutionGate`(M36, ADR-0050)는 손대지 않는다 —
  여전히 `source=next_task`만 승인하고, `current_work`/`blocked_task`/
  `capability_gap`/`project_recommendation`은 계속 Not Supported다.
  M38은 "기존 정책을 주기적으로 호출"만 하지 새 정책을 만들지 않는다
  (MDD/YAGNI/Reuse First).
- **`RUN_RECOMMENDATION` Action(신규, 추가 필드 없음)**:
  `domain.automation.ActionKind`에 1개 추가. `AutomationActionExecutor`
  가 선택적 `recommendation_execution_service` 의존성을 받아, 발동
  시 `RecommendationExecutionService.publish(manual_trigger=True)`를
  호출한다. 의존성이 주입되지 않으면(예: 기존 단위 테스트) 기존
  `RUN_WORKFLOW`와 동일하게 `AutomationActionNotSupportedError`를
  던진다.
- **`manual_trigger=True` 고정 전달**: `ExecutionGate`는 자동/주기적
  Trigger가 실수로 승인되는 것을 막기 위해 `manual_trigger`에 기본값을
  두지 않는다(ADR-0050). M38은 이 판정 로직을 바꾸지 않고, 대신 "사용자가
  `AutomationRule`을 명시적으로 만들고 활성화했다"는 사실 자체를 수동
  승인으로 해석한다 — Rule 생성/활성화가 이미 `AutomationService`(M21)
  의 CRUD 진입점을 거친 사용자 행위이기 때문이다.
- **Composition Root 배선**: `build_app()`이 `VaultAdapter(Path(config.
  vault_root))` + `AgentAdapter(InMemoryAgentManager(),
  InMemoryAgentRegistry(), InMemoryAgentScheduler())` +
  `RecommendationIntelligenceService` + `RecommendationExecutionService`
  를 `tests/runtime/execution/test_recommendation_execution_service.py`
  와 동일한 생성자 조합으로 조립해 `AutomationActionExecutor`에 주입한다.
  `EngineRegistry`/`EngineSelectionPolicy`/`ExecutionDispatcher`는 기존
  RUN_TASK 배선과 동일 인스턴스를 공유한다.
- **`ProductionConfig.vault_root`(신규 필드, 기본값 `"."`)**: ADR-0037
  "Vault == Repository Root"를 그대로 따라, 서버가 저장소 루트에서
  기동된다는 기존 전제를 설정값으로 명시했을 뿐이다. `AI_WORKSPACE_
  VAULT_ROOT` Env Var로 오버라이드할 수 있다(기존 Env Var 우선순위
  규칙과 동일).
- **범위**: `AutomationScheduler`↔Recommendation Execution 연결만.
  `done→archived` 자동화·재시도 정책·`review→done` 자동화·CLI·Hook은
  M37과 동일하게 범위 밖(YAGNI) — 다음 Milestone 이후 논의 대상으로
  남는다. 새 Core Domain Interface/Adapter 없음(27종 유지),
  `ExecutionGate`/`ActionBuilder`/`TaskLifecycleTransitioner` 무변경.

### 3.32 Experience Intelligence (Milestone 40, ADR-0055, 설계: M40-T01)

`ExecutionMemoryStore`(M39)에 쌓인 실행 기록을 task_id별 성공/실패
집계로 바꾸는 Read Only Intelligence 계층. M29~M35와 같은 뼈대
(Analyzer + Service + Vault Presentation)를 그대로 따르되, 데이터
소스가 처음으로 `integration/`의 Adapter가 아니라 `memory/`라는
점이 다르다 — 이를 위해 §8 규칙 21을 이름 나열이 아닌 **Role 기반**
으로 재정의했다(위 참고).

- **Scope(사용자 승인)**: (a) Read-Only Experience Reporting만 —
  `RecommendationRuleAnalyzer`(M35)의 판정 로직에는 관여하지 않는다.
  (b)Experience-Informed Recommendation(판단 기준 자체를 바꾸는 것)
  은 명시적으로 범위 밖 — Learning은 여전히 M40 이후 과제다.
- **`ExperienceRecord`/`ExperienceAnalyzer`(`intelligence/
  experience_rules.py`)**: `memory/`를 포함해 이 파일 밖 어떤
  패키지도 import하지 않는 순수 Analyzer. `ExecutionMemoryEntry`
  (`memory/`)를 그대로 받지 않고, `intelligence/`가 스스로 정의한
  `ExperienceRecord`로 변환된 값만 받는다 — Analyzer 순수성을
  Import 경계로도 강제하기 위함이다.
- **Deterministic + Immutable Input(사용자 조건, DoD)**: `ExperienceAnalyzer.
  analyze()`는 현재 시각·난수·외부 상태를 참조하지 않아 같은 입력에
  항상 같은 결과를 낸다(`stats`도 task_id 오름차순으로 고정). 입력
  `ExperienceRecord`는 `@dataclass(frozen=True)`라 구조적으로
  불변이고, Analyzer는 쓰기 메서드를 전혀 호출하지 않는다.
- **`ExperienceIntelligenceService`(`intelligence/experience_service.py`)**:
  `VaultAdapter` + `ExecutionMemoryStore`를 조합해 `ExecutionMemoryEntry`
  →`ExperienceRecord` 변환 + Analyzer 호출 + Vault 노출(`publish()`
  →`VaultAdapter.publish_experience_intelligence()`)까지 담당하는
  얇은 조합 계층 — `RecommendationIntelligenceService`(M35)와 동일한
  패턴. `*Service`로 끝나는 이름이라 §8 규칙 21의 Role 판정에서
  `memory/` 접근이 허용된다.
- **`ExecutionMemoryEntry`(M39 `memory/execution_memory_store.py`
  확장)**: `ExecutionMemoryStore.query()`의 반환 타입을 domain의
  `ExecutionMemory`에서 `memory/`가 스스로 정의하는
  `ExecutionMemoryEntry`로 바꿨다 — `integration/vault_adapter.py`가
  `TaskDocumentView`로 `domain.Task`를 감싸 노출하는 것과 같은
  이유(경계를 넘는 자리에서는 domain 타입을 그대로 흘려보내지
  않는다). `record()`는 여전히 domain의 `ExecutionMemory`를 받는다
  (쓰기 쪽 호출자인 `runtime/execution/`은 domain 참조 제약이 없다).
- **결과 노출**: `15 Project Intelligence/Experience Intelligence.md`
  (M29~M35와 동일한 1-파일-1-리포트 관례). 매 `publish()` 호출마다
  전체가 덮어써진다.
- **범위 밖(YAGNI)**: 영속화(ADR-0053 유지, `InMemoryMemoryEngine`
  그대로), embedding/score 등 Learning 전용 필드, Composition Root
  (`web/server.py`) 배선 — M29~M34의 다른 순수 Intelligence Service
  (Context/Session Resume/Workflow/Synthesis)와 동일하게, 실제
  프로덕션 실행 경로에 자동 연결되는 것은 `RecommendationIntelligenceService`
  가 필요로 하는 것들뿐이라는 기존 관례를 그대로 따른다. 새 Core
  Domain Interface/Adapter 없음(27종 유지).

### 3.33 Architecture Guardian (Milestone 41, ADR-0056, 설계: M41-T01)

**역할 정의(§13.2에 그대로 반영)**: *Guardian owns the executable
representation of architectural rules. Architecture documentation
defines the rules; Guardian encodes them, evaluates conformance, and
publishes architectural health.* — Guardian은 규칙을 만들지 않는다
(§8이 여전히 규칙의 소유자다), 이미 선언된 규칙을 평가하고 공표할
뿐이다.

- **Reuse First로 발견한 것**: 아키텍처 경계 검사가 이미 `tests/`
  5곳(`test_architecture_boundary.py`/`test_connector_layering.py`/
  `test_conversation_connector_boundary.py`/`test_intelligence_
  layering.py` 등)에 개별 구현·중복돼 있었다. M41은 새 감시 로직을
  만드는 Milestone이 아니라 **이미 존재하던 로직을 하나로 통합**하는
  Milestone이다.
- **`ArchitectureRule`(`guardian/rules.py`, 메서드 없는 순수 값
  객체)**: 다형적 `evaluate()`를 갖는 ABC가 아니라, 필드만 있는
  `frozen dataclass` 3종의 Union이다 — `ForbiddenPackageImportRule`
  (패키지 A는 B를 import 금지)/`AllowedImportPrefixRule`(특정
  패키지 아래는 화이트리스트만 허용)/`ServiceRoleGatedImportRule`
  (Role 기반 허용, M40/ADR-0055 패턴 재사용). 평가 로직은 전부
  `guardian/checker.py`가 타입별로 분기해서 담당한다 — Rule은 항상
  순수 데이터로 남는다.
- **`GUARDIAN_RULES`(`Final[tuple[ArchitectureRule, ...]]`)**: 실행
  중 변경 불가능한 정본 규칙 목록(Registry). 기존 5곳 중 3개 형태에
  자연스럽게 맞는 5개 규칙만 이전했다 — `test_architecture_boundary.py`
  의 2개(Core Domain↔vault 개별 금지) + `test_intelligence_layering.py`
  의 3개(금지 패키지/Adapter 화이트리스트/Role 기반 Memory 접근).
- **의도적으로 제외한 것**: `test_connector_layering.py`(Adapter/
  Peer Connector/Orchestrating Connector 그룹 화이트리스트)와
  `test_conversation_connector_boundary.py`(단일 파일 기준 규칙)는
  위 3개 Rule 형태로 자연스럽게 표현되지 않는다 — 억지로 일반화하지
  않고(사용자 조건) 이번 범위에서 제외했다. 두 파일은 각자의 기존
  `ast` 검사를 그대로 유지한다(회귀 없음, Guardian 미경유).
- **`guardian/checker.py`(순수 평가기)**: `pytest`를 전혀 알지
  못한다 — `import pytest`/`assert` 없음(사용자 조건). 기존 5개
  boundary 테스트(그중 이전된 5개 규칙에 한해)는 이 평가기의 결과를
  받아 자기 스스로 `assert`하는 얇은 wrapper로 재작성됐다 — 각
  테스트가 잡아내는 위반 내용은 100% 동일하게 유지(회귀 없음).
- **`ArchitectureCheckResult`/`ArchitectureHealthReport`
  (`guardian/models.py`)**: 평가 결과를 표현하는 Domain Model(사용자
  조건) — `ArchitectureViolation`(위반 1건) 목록을 규칙별로 묶고,
  `all_passed`(전체 통과 여부)는 이미 계산된 `passed` 값들의 단순
  논리곱일 뿐 새 판정 로직이 아니다.
- **`ArchitectureGuardianService`(`guardian/service.py`)**: `checker.
  evaluate()` 호출 + Vault 발행을 조합하는 얇은 계층
  (`RecommendationIntelligenceService`, M35와 동일 뼈대). **Vault
  발행(`publish()`)이 부가 기능이 아니라 핵심 진입점**(사용자 조건)
  — Guardian의 목적("공표한다")은 평가만으로 완수되지 않는다.
  `VaultAdapter.publish_architecture_guardian()`(신규 메서드 1개)이
  `15 Project Intelligence/Architecture Guardian.md`에 원자적으로
  덮어쓴다.
- **범위 밖(YAGNI)**: CI 강제 게이트 신설 — 이미 `pytest` 통과가
  §8.6 Merge 조건에 포함돼 있어 새로 만들 것이 없다(위반하면 이미
  병합이 막힌다). Connector 그룹 규칙의 Guardian 편입, Composition
  Root(`web/server.py`) 배선. 새 Core Domain Interface/Adapter 없음
  (27종 유지).

### 3.34 Recommendation Adaptation (Milestone 42, ADR-0058, 설계: M42-T02~T04)

**책임(Responsibility)**: `RecommendationRuleAnalyzer`(M35)의 5단계
Priority Rule은 지금까지 고정돼 있었다. M42는 그 고정 순서를
재설계하지 않고, M40 `ExperienceReport`(과거 실행 성공/실패 집계)를
근거로 **이미 결정된 `NextAction`을 사후 조정(Adjustment)**한다 —
새 Recommendation을 생성하는 것이 아니다(사용자 조건 1).

- **`Adaptation`은 Behavioral Concept(§13.3)이지 1급 Domain이 아니다**
  (사용자 조건 4, 보류 결정): 재사용 사례가 이번 1건뿐이므로 §13.2로
  승격하지 않는다. Workflow/Agent/Capability Adaptation 등으로 개념이
  반복되면 그 시점에 별도 ADR로 승격을 재검토한다.
- **`RecommendationAdjustmentAnalyzer`(`intelligence/recommendation_adjustment.py`,
  신규)**: 입력을 `NextAction`(M35이 이미 고른 단일 후보) +
  `ExperienceReport`(M40) 두 값으로 단순화했다(사용자 조건 2) — 여러
  후보를 다시 순위 매기지 않는다. 대상(`target`)의 과거 실행 기록이
  전부 실패(성공 0건)일 때만 추천을 보류(`next_action=None`)하고,
  그 밖의 모든 경우(기록 없음/일부 성공/`experience_report=None`)는
  `NextAction`을 그대로 통과시킨다. Deterministic + Immutable Input
  (M40과 동일 조건) — side-effect 없음, 두 입력 모두 수정하지 않는다.
- **`ExperienceReport` 생성은 M40의 책임(Non-goal, 사용자 조건 3)**:
  이 Analyzer는 `ExperienceReport`를 만들지 않고 소비만 한다 —
  `ExperienceIntelligenceService.generate()`(M40)가 호출자 책임으로
  남는다.
- **`RecommendationIntelligenceService`(M35) 확장**: `generate()`/
  `publish()`에 `experience_report: ExperienceReport | None = None`
  선택적 인자 추가. **`experience_report=None`이면 M35와 100% 동일
  동작**(사용자 조건 5, DoD) — Adjustment가 전혀 개입하지 않는다.
  `RecommendationIntelligenceReport`에 `adjusted`/`adjustment_reason`
  필드 추가(기본값 `False`/`None`), Vault
  `15 Project Intelligence/Recommendation Intelligence.md`에
  "Adaptation(Milestone 42)" 섹션 추가.
- **범위 밖(Non-goals)**: 5단계 Priority Rule 순서 자체의 재설계,
  점수화(scoring)/가중치 학습, `web/server.py`(Composition Root)·
  `RecommendationExecutionService`(M36)·`AutomationScheduler`(M38)에
  자동 배선(향후 필요 시 별도 승인). `Adaptation`의 1급 Domain 승격.
  새 Core Domain Interface/Adapter 없음(27종 유지).

### 3.35 Recommendation Orchestration (Milestone 43, ADR-0059, 설계: M43-T02~T04)

**책임(Responsibility)**: M42가 Non-goal로 남겨둔 `web/server.py`
자동 배선을 완성한다 — M35(Recommendation)→M42(Adaptation)→M36
(Execution)→M39(Memory)→M40(Experience)로 이어지는 하나의 실행
흐름을 명시적으로 연결한다. 새 판단 로직을 추가하지 않는다 — 이미
존재하는 Service들을 정해진 순서로 호출만 한다.

- **Domain Analysis(T02)**: 책임이 기존 `Workflow`(M34, Read-Only
  Task 상태 분석)에 포함되지 않음을 확인 — Workflow/Runtime/
  Coordination 등은 이미 다른 의미로 쓰이는 `Workflow`를 접두어로
  재사용해 §13.4가 배제한 `Learning`/`Insight`와 같은 유형의 충돌을
  일으킨다. 대신 이 저장소에 이미 확립된 `Orchestrating Connector`
  (ADR-0041)/`Orchestrating 패턴`(M32, M40)과 정확히 같은 의미임을
  확인하고 `Orchestration`을 재사용(§13.3에 구조적 관행으로 최초
  등재, 1급 Domain 승격 아님).
- **네 가지 책임 분리(사용자 결정)**: Composition Root(`web/server.py`,
  조립) / Analyzer(`RecommendationRuleAnalyzer`/
  `RecommendationAdjustmentAnalyzer`, 판단) / `RecommendationOrchestrationService`
  (이 Milestone, 실행 흐름 제어) / `RecommendationExecutionService`
  (실행). 각 책임을 명확히 분리해 향후 Automation·Multi-Agent가
  같은 Orchestration Service를 재사용할 수 있는 기반을 마련한다.
- **`RecommendationExecutionService`(M36)의 Recommendation 의존성
  제거(ADR-0059)**: 최초 제안(T04)은 `experience_report`를 이
  Service에 선택적으로 threading하는 것이었으나, MDD Review 재검토
  결과 더 낮은 결합도를 위해 이 Service가 `RecommendationIntelligenceService`
  를 생성자로 아예 쥐지 않도록 변경했다 — `execute()`/`publish()`가
  이미 계산된 `RecommendationIntelligenceReport`를 파라미터로 받는다.
  이 Service는 이제 "Recommendation을 어떻게 얻는지" 전혀 모른다 —
  순수하게 "주어진 실행 대상을 실행"만 한다.
- **`RecommendationOrchestrationService`(신규,
  `runtime/execution/recommendation_orchestration_service.py`)**:
  `ExperienceIntelligenceService.generate()`(M40)로 `ExperienceReport`
  를 얻고, `RecommendationIntelligenceService.generate(experience_report=...)`
  (M35, Adaptation은 M42)로 최종 Report를 만든 뒤,
  `RecommendationExecutionService.execute()/publish()`에 그대로
  전달한다. 판단 로직 0줄 — 순서대로 호출만 한다.
- **`AutomationActionExecutor`(M21) 배선 교체**: 주입받는 의존성을
  `RecommendationExecutionService`에서 `RecommendationOrchestrationService`
  로 교체(파라미터명도 함께 갱신) — `AutomationScheduler`의
  `RUN_RECOMMENDATION` Action이 이제 Experience/Adaptation까지 반영된
  흐름으로 실행된다.
- **`web/server.py`(Composition Root) 갱신**: `ExperienceIntelligenceService`
  +`RecommendationOrchestrationService`를 조립해 `AutomationActionExecutor`
  에 주입 — M42가 미뤄뒀던 자동 배선을 이 Milestone에서 완성한다.
- **범위 밖(Non-goals)**: Multi-Agent 조율(향후 재사용 후보로만
  문서화), `Orchestration`의 1급 Domain(§13.2) 승격, Gate/Builder/
  Lifecycle/Memory 기록 로직 자체의 변경(내부는 그대로). 새 Core
  Domain Interface/Adapter 없음(27종 유지).

### 3.36 Recommendation Explainability (Milestone 44, ADR-0061, 설계: M44-T02~T04)

**책임(Responsibility)**: Recommendation은 "무엇을 할 것인가"를
결정한다(M35/M42/M43). Explainability는 "왜 그렇게 결정했는가"를
이미 계산된 값들로부터 **구조적으로 재구성**한다 — Recommendation
자체를 바꾸지 않는다. 새 AI 판단·새 지표를 만들지 않는다.

- **`RecommendationExplanationAnalyzer`(신규,
  `intelligence/recommendation_explanation.py`)**: `RecommendationIntelligenceReport`
  (M35, Adaptation 반영 시 M42) + `ExperienceReport`(M40, 선택)를
  입력받아 5단계 Priority Rule의 평가 흔적(`PriorityStepTrace`,
  각 단계의 존재 여부와 선택 여부), 선택된 대상의 Experience 성공률
  요약, Adaptation 적용 여부/사유를 `RecommendationExplanationReport`
  로 재구성하는 순수 Analyzer. Deterministic + Immutable Input(M40/M42
  와 동일 조건) — 두 입력 모두 수정하지 않는다.
- **`RecommendationExplanationService`(신규,
  `intelligence/recommendation_explanation_service.py`)**: Analyzer
  호출 + Vault 발행만 조합하는 얇은 계층(`ExperienceIntelligenceService`
  와 같은 뼈대). `VaultAdapter.publish_recommendation_explanation()`
  (신규)이 `15 Project Intelligence/Recommendation Explanation.md`에
  원자적으로 덮어쓴다.
- **`Explainability`는 §13.3 Behavioral Concept로 등재**(`Adaptation`
  과 동일한 급) — 재사용 사례가 이번 1건뿐이라 1급 Domain(§13.2)
  승격은 보류.
- **`RecommendationOrchestrationService`(M43) 연결**: `explanation_service`
  를 선택적으로 주입하면 Recommendation 계산 직후(Execution 위임
  전) `RecommendationExplanationService.publish()`를 호출해 근거를
  Vault에 함께 기록한다 — Recommendation→Explainability→Execution
  순서(사용자 제안 다이어그램과 일치). 미주입 시 M43 이전과 완전히
  동일하게 동작(하위 호환).
- **`web/server.py`(Composition Root) 갱신**: `RecommendationExplanationService`
  를 조립해 `RecommendationOrchestrationService`에 주입 — 매 추천
  실행마다 실제로 근거가 Vault에 기록된다.
- **범위 밖(Non-goals)**: Dashboard/API/CLI/Multi-Agent Reviewer 연동
  (향후 재사용 후보로만 문서화), 5단계 Priority Rule/Adaptation 판단
  로직 자체의 변경(그대로 재사용). 새 Core Domain Interface/Adapter
  없음(27종 유지).

### 3.37 Workspace Observability (Milestone 45, ADR-0062, 설계: M45-T01~T04)

**책임(Responsibility)**: Claude Code 세션 안에서 AI Workspace의
Recommendation→Adaptation→Explainability→Orchestration→Execution→
Memory→Experience 파이프라인이 지금 어떤 상태인지, 그리고 Claude
Code 자체의 Runtime(Model/Effort/Context 사용량)이 어떤지를 **실시간
StatusLine으로 반영**한다. 새 AI 판단·새 자동화·새 지표를 만들지
않는다 — 이미 있는 상태를 읽기만 한다.

- **`observability/snapshot.py`(신규)**: `WorkspaceRuntimeSnapshot`
  (읽기 전용 Runtime 모델, 가칭이었던 이름 그대로 채택) +
  `ClaudeRuntimeInfo`/`WorkspaceInfo`/`PipelineStageState`/
  `PipelineStageStatus`. 전부 메서드 없는 `frozen dataclass`(§13.6
  `*Rule`과 동일 원칙) — StatusLine뿐 아니라 향후 Dashboard/CLI/Web
  UI가 같은 Snapshot을 재사용할 수 있는 공통 타입.
- **3개 Analyzer(신규, `observability/`)**: `ClaudeRuntimeAnalyzer`
  (StatusLine stdin JSON을 그대로 옮김), `PipelineStageAnalyzer`
  (Vault 산출물 존재 여부로 7단계 상태 재구성), `WorkspaceInfoAnalyzer`
  (`pyproject.toml`/`Milestones Index.md`만 읽음). 셋 다 생성자
  인자 없이 `analyze()`만 제공하는 순수 Analyzer(§13.6).
- **`RuntimeSnapshotService`(신규, `observability/runtime_snapshot_service.py`)**:
  3개 Analyzer 호출만 조합하는 얇은 Service — `VaultAdapter`만
  의존한다(Intelligence와 동일한 의존 규칙, §13.2).
- **`StatusLineRenderer`(신규, `observability/statusline_renderer.py`)**:
  `WorkspaceRuntimeSnapshot` → StatusLine 평문 문자열 변환만 하는
  순수 함수형 Renderer(`render_markdown()`류와 동일한 원칙, 대상만
  Markdown이 아니라 터미널 한 줄).
- **`VaultAdapter.report_last_modified()`(확장)**: Vault 문서의
  마지막 수정 시각(epoch seconds)을 읽기 전용으로 조회하는 메서드
  1개 추가 — 새 Adapter를 만들지 않고 기존 Adapter를 재사용(MDD
  Review Adapter Reuse 단계 통과).
- **Phase 1의 정직한 한계(ADR-0062 결정 3)**: Adaptation/Orchestration
  은 별도 Vault 산출물이 없어(M42/M43에서 이미 확인된 사실) 다른
  단계의 산출물에 구조적으로 포함된 것으로 표시(`STRUCTURAL_INCLUDED`).
  Memory(M39)는 `InMemoryMemoryEngine` 기반이라 영속화되지 않아
  별도 프로세스인 StatusLine에서 조회할 수 없음(`NOT_OBSERVABLE`) —
  실제로 관측 가능한 것만 관측했다고 표시하고, 안 되는 것은 왜
  안 되는지 명시한다(값을 지어내지 않음).
- **`.claude/settings.json`(신규)**: `statusLine.command`로
  `observability/statusline_main.py`를 실행 — Claude Code가 세션
  이벤트마다 stdin으로 Runtime JSON을 넘기고, 이 스크립트가 그 JSON을
  파싱해 Snapshot을 만들고 렌더링해 표준출력에 찍는다.
- **범위 밖(Non-goals)**: Dashboard/Web UI/Remote Monitoring/Metrics
  Server/Telemetry(향후 재사용 후보로만 문서화), 기존 Domain의
  판단 로직 변경, Recommendation/Adaptation/Explainability/
  Orchestration/Execution/Memory/Experience에 새 자동화나 새 상태
  기록(Instrumentation) 추가(Phase 2 후보, 이번 범위 아님). 새 Core
  Domain Interface/Adapter 없음(27종 유지).

### 3.38 Workspace Observability 확장 — Execution Environment (Milestone 45 확장, ADR-0063)

**책임(Responsibility)**: §3.37이 다루지 못한 "AI Workspace가 실행되는
환경" 자체를 관찰 대상에 추가한다 — Git 저장소 상태, Guardian
아키텍처 준수 여부, Vault 문서 상태, MCP 실행 환경(Obsidian MCP
포함). `Observability`는 §13.3에 이미 등재된 Behavioral Concept를
그대로 확장한 것이며, 새 Domain 어휘를 추가하지 않는다(T01 Domain
Analysis 결론).

- **`GitRuntimeAnalyzer`(신규, `observability/git_runtime_analyzer.py`)**:
  `git` 하위 명령(`rev-parse`/`status --porcelain`/`rev-list
  --left-right --count`/`log -1`)만 읽기 전용으로 호출. `fetch`를
  하지 않으므로 `ahead`/`behind`는 마지막으로 로컬에 캐시된 원격
  추적 브랜치 기준(네트워크 호출 없음 원칙 유지). 각 하위 명령은
  1.5초 타임아웃 — 실패/타임아웃 시 해당 필드만 `None`.
- **`GuardianRuntimeAnalyzer`(신규, `observability/guardian_runtime_analyzer.py`)**:
  `guardian.checker.evaluate()`(M41)를 그대로 재사용(AST 기반 순수
  평가라 갱신마다 다시 호출해도 저비용) — Guardian의 판정 로직을
  전혀 바꾸지 않는다. `pytest`는 재실행하지 않고 `.pytest_cache/v/
  cache/lastfailed`(pytest 공식 캐시 파일)만 읽어 "마지막 로컬 실행
  결과"를 반영한다. `ruff`/`mypy`/Coverage는 캐시된 pass/fail 요약이
  없고 매 갱신마다 재실행하면 지연 위험이 커 Phase 1은 `None`(Not
  Available).
- **`VaultRuntimeAnalyzer`(신규, `observability/vault_runtime_analyzer.py`)**:
  `VaultAdapter.report_last_modified()`(M45)만 재사용(새 Adapter
  없음). `Current Milestone`은 `WorkspaceInfoAnalyzer`(M45)를 그대로
  호출해 재사용. `Current PR`은 GitHub API 조회(네트워크+인증)가
  필요해 Phase 1은 `None`(Not Available) — 로컬에서 확인 가능한
  대안은 `GitRuntimeInfo.current_branch`.
- **`McpRuntimeAnalyzer`(신규, `observability/mcp_runtime_analyzer.py`)**:
  공식 문서가 확인해 준 두 경로만 사용 — ① `.mcp.json`(프로젝트
  범위 설정 파일)을 읽어 "설정된 서버 목록"만 확인, ② `claude mcp
  list`(공식 CLI, JSON 옵션 없음)를 2초 타임아웃으로 실행해 문서화된
  상태 기호(`✔`/`✘`/`!`/`⏸`)만 그대로 매칭 — 기호가 안 보이거나
  형식이 예상과 다르면 추측하지 않고 `None`. `active_server`/
  `available_tools`/`last_mcp_call`/`last_mcp_error`는 정적 조회로
  확인할 공식 경로가 없어 Phase 1은 `None`(Not Available) — Hook
  기반 기록은 새로운 기록 메커니즘 도입이라 별도 승인이 필요한
  Phase 2 후보로만 문서화한다.
- **`WorkspaceInfo.current_task`(신규 필드)**: Phase 1은 항상 `None`
  — 이 저장소의 Recommendation 계열 코드는 상시 실행 프로세스가
  아니라 요청-응답형 함수 호출이라, "지금 실행 중인 Task"를 관찰하려면
  기존 Domain 코드에 상태 기록을 추가해야 한다(Domain 책임 변경
  금지 원칙과 충돌).
- **`RuntimeSnapshotService`/`StatusLineRenderer`(확장)**: 4개
  Analyzer를 추가로 조합하고, StatusLine에 Git/Guardian/Vault/MCP
  줄을 추가로 렌더링한다. 값이 `None`이면 "N/A"만 찍는다(추정 없음).
- **범위 밖(Non-goals)**: Dashboard/Web UI/Telemetry, `ruff`/`mypy`/
  Coverage 실시간 측정(재실행 비용 문제), MCP Hook 기반 호출 이력
  기록, GitHub API 기반 PR 조회 — 전부 Phase 2 후보로만 문서화. 새
  Core Domain Interface/Adapter 없음(27종 유지).

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
18. **Core Domain(`domain`/`interfaces`/`engines`)과 `vault/`는
    서로 직접 참조하지 않는다**(ADR-0035, Milestone 28-T03로
    ADR-0039에서 강제 방식 추가). 이 경계를 넘는 통신은 반드시
    `integration/`의 Workspace Adapter Layer(`VaultAdapter`/
    `WorkflowAdapter`/`AgentAdapter`)를 통해서만 이뤄진다.
    `integration/`을 제외한 어떤 모듈도 `vault`와 `domain`/
    `interfaces`/`engines`를 동시에 import할 수 없다 —
    `tests/integration_layer/test_architecture_boundary.py`가
    `ast` 기반으로 이를 테스트 실패로 강제한다.
19. **`integration/` 내부 참조 규칙**(ADR-0040/ADR-0041, Milestone
    28-T05/T06 Architecture Freeze에서 §8로 명문화): Adapter
    (`VaultAdapter`/`WorkflowAdapter`/`AgentAdapter`)는 다른
    Adapter를 참조하지 않는다. Peer Connector(`WorkflowTaskLink`/
    `WorkflowAgentLink`)는 Adapter만 조합하고 다른 Peer Connector를
    참조하지 않는다. Orchestrating Connector(`ConversationConnector`)
    만 예외적으로 Peer Connector와 Adapter를 함께 조합할 수 있다
    (그 반대로 Peer Connector나 Adapter가 Orchestrating Connector를
    참조하는 것은 금지). 즉 참조 방향은 항상 **Orchestrating
    Connector → (Peer Connector | Adapter) → Core**이며 위로
    거슬러 올라가지 않는다.
20. **Conversation Layer는 `vault`/`WorkflowEngine`/`TaskEngine`/
    `AgentManager`(및 그 구체 구현)를 직접 참조하지 않는다**
    (ADR-0041, Milestone 28-T06) — 모든 요청은
    `ConversationConnector`(Orchestrating Connector)를 통해서만
    전달한다. `tests/integration_layer/
    test_conversation_connector_boundary.py`가 `ConversationConnector`
    자신의 import를 `ast` 기반으로 검증한다(Conversation Layer
    자체는 별도 코드 패키지가 아니라 이 Connector의 호출자이므로,
    이 규칙은 실제로는 "`ConversationConnector` 밖에 이 접근 경로를
    또 만들지 않는다"는 의미로 강제된다 — §9 참고).
21. **`intelligence/`(Intelligence Layer, ADR-0043, Milestone 29;
    Role 기반으로 재정의 — ADR-0055, Milestone 40)는 `domain`/
    `interfaces`/`engines`/`vault`를 직접 참조하지 않는다**(무변경).
    Read-Only 데이터 제공자 접근은 **역할(Role)**로 나뉜다 —
    이름을 규칙에 나열하는 대신 "이 모듈이 무엇을 하는가"로
    판단한다:
    - `integration/`의 Adapter(`VaultAdapter`/`AgentAdapter`/
      `KnowledgeAdapter`)는 패키지 전체에 계속 허용된다(M29부터의
      기존 관례, M40에서 넓히지 않음).
    - `memory/`(Memory Domain — §13.2, 저장/검색만 하고 판단하지
      않는 컴포넌트)는 **`*Service`로 끝나는 클래스를 정의하는
      모듈(오케스트레이션 역할)에만** 새로 허용한다(M40) —
      `ExecutionMemoryStore` 같은 특정 클래스 이름을 규칙에 박아
      넣지 않고, 앞으로 `memory/`에 무엇이 추가되든 "Service
      역할인가"만으로 자동 적용되게 한다. `*Service` 클래스가 없는
      모듈(Analyzer/값 객체)은 여전히 `memory/`를 import할 수 없다
      — Analyzer의 순수성(Deterministic, 부작용 없음)을 그대로
      강제한다.
    Intelligence Layer는 쓰기를 하지 않는 Read Only Query Layer이며,
    Integration/Memory Layer가 이미 노출한 값을 읽어 집계·판단만
    한다(새 비즈니스 로직 없음). `tests/intelligence/
    test_intelligence_layering.py`가 `ast` 기반으로 이를 강제한다 —
    금지 패키지 검사(도메인 4종)와 Adapter 화이트리스트 검사에
    더해, `memory/`를 import하는 모듈은 반드시 `*Service` 클래스를
    가져야 한다는 검사가 추가됐다(M40).
22. **Execution 결과의 Memory 기록은 `RecommendationExecutionService`
    → `ExecutionMemoryStore` → `MemoryEngine`** 순서로만 이루어진다
    (Milestone 39, ADR-0053) — §8 규칙 7(Agent → Context Manager →
    Memory Engine)과는 완전히 별도의 경로다(§8 규칙 11이 Knowledge
    접근을 규칙 7과 별도 경로로 둔 것과 동일한 패턴). `MemoryEngine`
    interface 자체는 바뀌지 않는다. `ExecutionMemoryStore`는
    Learning(과거 기록으로 판단을 바꾸는 것)을 하지 않는다 — 저장과
    조회만 제공한다.

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
│                       #   + execution_memory_store.py (ExecutionMemoryStore,
│                       #   Execution 결과 저장/조회, Milestone 39;
│                       #   query()는 ExecutionMemoryEntry 반환, Milestone 40)
├── guardian/          # Architecture Guardian(Milestone 41) — rules.py(GUARDIAN_RULES)
│                       #   + checker.py(순수 평가기) + service.py(ArchitectureGuardianService)
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
│                       #   + connection.py/filesystem.py/atomic.py
│                       #   (Real Vault Connection/Adapter/Atomic
│                       #   Write, M24, ADR-0036) + task_lifecycle.py
│                       #   (Status Transition/Archive, Milestone 28-T01)
│                       #   + task_sync.py(Automatic Document
│                       #   Synchronization, Milestone 28-T02)
│                       #   — Core Domain·web/을 모두 모름, Milestone 23~24
├── integration/       # Workspace Adapter Layer(ADR-0039, Milestone
│                       #   28-T03) — vault_adapter.py/workflow_adapter.py/
│                       #   agent_adapter.py(Adapter: 외부 시스템 1개만
│                       #   연결). Core Domain↔vault 경계를 넘는 유일한
│                       #   통로, 연결·변환·위임만 담당
│                       #   + workflow_task_link.py(WorkflowTaskLink,
│                       #   Milestone 28-T04)/workflow_agent_link.py
│                       #   (WorkflowAgentLink, Milestone 28-T05,
│                       #   ADR-0040) — Peer Connector: 유스케이스
│                       #   하나씩 오케스트레이션, 서로 참조하지 않음
│                       #   + conversation_workflow_link.py
│                       #   (ConversationConnector, Milestone 28-T06,
│                       #   ADR-0041) — Orchestrating Connector: 위
│                       #   Peer Connector 2개 + VaultAdapter를 조합해
│                       #   Conversation Layer 요청을 처리(예외적으로
│                       #   Connector를 참조하는 유일한 구성원)
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

## 13. Domain Vocabulary & Naming Convention (ADR-0054, 2026-07-30)

### 13.1 배경 및 목적

M1~M39를 거치며 Milestone 이름과 컴포넌트 이름이 각 시점의 필요에 따라
독립적으로 만들어졌다 — Intelligence(M29~M35)/Memory(M1, M39)/Engine
(M1의 Core Engines)/Guardian(§2.1에서 예약만 됨)/Resume(M33)/Lifecycle
(M37) 등이 서로 다른 시점에 서로 다른 맥락에서 도입됐다. 프로젝트가
커질수록 이 용어들이 같은 뜻인지 다른 뜻인지 매 Milestone마다 다시
판단해야 하는 비용이 커진다.

이 절은 **M40 이후의 모든 Milestone/Engine/Service 이름이 재사용해야
할 단일 어휘(Vocabulary)**를 정의한다. 새 코드를 만들기 전에
Reuse First를 검증하는 MDD Review Gate(§2.1.1, `.ai/RULES.md`)와
같은 정신을 **이름**에도 적용한 것이다 — "이 개념을 표현할 기존
용어가 있는가?"를 먼저 확인하고, 없을 때만 새 용어를 만든다.

### 13.2 Domain Vocabulary — 핵심 4개 용어

아래 4개는 이후 Milestone이 이름을 지을 때 최우선으로 재사용해야 할
1급 어휘다. 각 용어는 **Read/Write 여부와 소비 대상이 명확히 다른
서로 배타적인 책임**을 가리킨다.

| 용어 | 정의 | 책임(Responsibility) | 범위(Scope) | 대표 산출물(Typical Outputs) | 대표 소비자(Typical Consumers) |
|---|---|---|---|---|---|
| **Intelligence** | 여러 데이터 소스를 읽어 "지금 상황이 어떤가"를 분석·요약·판단하는 **Read Only** 계층(ADR-0043) | 관찰·집계·판단만 한다. 절대 쓰지 않고, 절대 실행하지 않는다(side-effect 없음) | `intelligence/` 패키지. `VaultAdapter`/`AgentAdapter`(Integration Layer)만 읽기 의존, `domain`/`interfaces`/`engines`/`vault`는 직접 참조하지 않는다(§8 규칙 21) | Vault Markdown 리포트(`15 Project Intelligence/*.md`), 값 객체(`ProjectSnapshot`/`NextAction` 등) | 사람(Vault 열람), Execution(M36 이후, `NextAction`만 예외적으로 소비) |
| **Memory** | 시스템이 무언가를 **저장하고 다시 꺼내 쓸 수 있게** 하는 계층. 판단(Learning)은 하지 않는다 | key-value 저장/검색만 담당(`MemoryEngine.remember`/`recall`/`search`, M1). 무엇을 저장할지는 호출자가 결정 | `memory/` 패키지. `MemoryEngine` interface(M1)와 그 재사용 계층(`ContextManager`/`ExecutionMemoryStore`) | 저장된 key-value 레코드(Session/Mission Snapshot, `ExecutionMemory`) | Context Manager(Snapshot), Execution Platform(자기 실행 결과 기록, M39) |
| **Execution** | 실제 부작용(Task 실행, 상태 변경)을 일으키는 계층. 이 저장소에서 "생각(Intelligence)"과 "행동(Execution)"을 가르는 경계선이다 | `EngineAdapter`를 통한 실제 실행, Task 상태 전이. 유일한 실행 진입점은 `ExecutionDispatcher`(M18) | `runtime/execution/`, `runtime/automation/` | `EngineExecutionResult`, Task 상태 전이, Vault 실행 리포트(`Recommendation Execution.md`) | 사람(Vault 열람), Memory(M39, 실행 결과를 `ExecutionMemory`로 기록) |
| **Guardian** | Guardian owns the executable representation of architectural rules. Architecture documentation defines the rules; Guardian encodes them, evaluates conformance, and publishes architectural health.(Milestone 41, ADR-0056) | 규칙을 **정의하지 않는다** — §8이 여전히 규칙의 소유자다. 이미 선언된 규칙을 `ArchitectureRule`(순수 값 객체)로 인코딩하고, 소스 트리에 대해 평가(`checker.evaluate()`)해 결과를 공표한다 | `guardian/` 패키지. 소스 트리(`src/ai_workspace`)를 읽기만 한다(Read Only). `VaultAdapter`(Presentation)만 의존 | `ArchitectureHealthReport`(규칙별 통과/위반 목록), Vault Markdown(`15 Project Intelligence/Architecture Guardian.md`) | 사람(Vault 열람), 기존 `pytest` 기반 boundary 테스트(결과를 `assert`) |

### 13.3 이미 확립된 보조 용어

아래 용어들은 4개 핵심 어휘만큼 범용적이지는 않지만, 이미 특정
의미로 정착되어 있으므로 **다른 뜻으로 재사용하지 않는다**. 새
Milestone에서 비슷한 개념이 필요하면 새 단어를 만들기 전에 먼저 이
표를 확인한다.

| 용어 | 확립된 의미 | 근거 |
|---|---|---|
| **Engine** | Core Domain의 상태 없는(또는 최소 상태) 서비스 계층(Task/Workflow/Approval/Automation/Memory Engine 등). "생각하는 상위 개념"이 아니라 Agent가 사용하는 하위 서비스를 가리킨다 | ADR-0012, §3.7 |
| **Lifecycle** | 상태 기계(State Machine)를 통한 전이 관리. `TaskLifecycleTransitioner`(M37)처럼 "허용된 상태→상태 전이만 수행"하는 컴포넌트에만 쓴다 | ADR-0051, §3.30 |
| **Resume** | 세션/작업 재개 — "지금 무엇을 하고 있었는가"를 자동 복원하는 것(M33)에만 쓴다. Memory의 저장/검색과는 다른, Intelligence의 판단(어떤 것이 "현재 작업"인지 규칙으로 고르는 것) | ADR-0047 |
| **Scheduler** | 주기/조건 Trigger로 무언가를 반복 발동시키는 컴포넌트(`AgentScheduler`, `AutomationScheduler`)에만 쓴다 | ADR-0033 |
| **Recommendation**(정의 확정, ADR-0060, 2026-07-31) | *The domain concept responsible for determining the most appropriate Next Action from the current project state. It represents an actionable recommendation, not a mandatory decision.* — Intelligence가 계산한 "다음에 무엇을 해야 하는가"라는 단일하고 근거(`reason`) 있는 판단(`NextAction`, M35)에만 쓴다. **비구속적**이다 — 실제 실행 여부는 별도의 `ExecutionGate`(M36)가 최종 결정한다. Recommendation 자체는 Intelligence(Read Only)지만, `Recommendation Execution`(M36)/`Recommendation Adaptation`(M42)/`Recommendation Orchestration`(M43)처럼 뒤에 다른 Domain이 붙으면 그 Recommendation을 실행/조정/흐름 제어하는 별도 컴포넌트를 가리킨다. M43 완료 후 `Suggest`/`Selection`/`Decision`/`Proposal` 4개 대안과 비교 검토했으나, 기존 의미와 충돌하거나(`Selection`/`Decision`/`Proposal`) 실질적 이득이 없어(`Suggest`) 유지하기로 확정(ADR-0060) | ADR-0049, ADR-0050, ADR-0060 |
| **Automation** | 조건/일정 Trigger로 Action을 자동 발동시키는 계층(`AutomationEngine`/`AutomationScheduler`)에만 쓴다. Automation은 스스로 "무엇을 할지" 판단하지 않는다 — 그 판단은 Intelligence/Recommendation의 책임이다 | ADR-0033 |
| **Adaptation**(Behavioral Concept, 1급 Domain 아님) | 과거 실행 결과(M40 `ExperienceReport`)를 근거로 **이미 결정된 판단을 사후 조정(Adjustment)**하는 행동 유형. 새 Recommendation을 생성하지 않는다 — `RecommendationRuleAnalyzer`(M35)가 이미 고른 `NextAction`을 그대로 받아 통과시키거나 보류할 뿐이다. Intelligence(1차 판단)와 구분되는 별도 개념이지만, 아직 재사용 사례가 1건(M42)뿐이므로 §13.2의 1급 Domain으로 승격하지 않는다 — Workflow/Agent/Capability Adaptation 등으로 개념이 반복 재사용되면 그 시점에 별도 ADR로 승격을 재검토한다(2026-07-30 사용자 결정) | ADR-0058 |
| **Orchestration**(구조적 관행, 1급 Domain 아님) | 여러 Service를 **새 판단 로직 없이 정해진 순서로 호출·조합**하는 것. ADR-0041의 Orchestrating Connector(`ConversationConnector`), M32/M40의 "Orchestrating 패턴"이 이미 이 의미로 써왔다 — M43에서 이 관행을 처음 §13.3에 정식 등재한다. `Workflow`(M34, Read-Only Task 상태 분석)와는 다른 개념 — Orchestration은 side-effecting Service들의 실행 순서를 제어한다(§8 규칙 21에 따라 `intelligence/`가 아니라 `runtime/execution/` 등 Execution Domain에 위치) | ADR-0041, ADR-0059 |
| **Explainability**(Behavioral Concept, 1급 Domain 아님) | Recommendation이 "무엇을 할 것인가"(M35/M42/M43)를 결정한 뒤, **"왜 그렇게 결정했는가"를 이미 계산된 값으로부터 구조적으로 재구성**하는 행동 유형(M44). Recommendation 자체를 바꾸지 않는다 — 새 AI 판단·새 지표를 만들지 않고, 5단계 Priority Rule 평가 흔적·Experience 통계·Adaptation 적용 여부를 사람이 읽을 수 있는 근거(Evidence)로 펼쳐 보일 뿐이다. `Adaptation`(M42)과 같은 급의 Behavioral Concept — 재사용 사례가 쌓이면(예: Guardian Explainability) 그 시점에 1급 Domain 승격을 재검토한다 | ADR-0061 |
| **Observability**(Behavioral Concept, 1급 Domain 아님) | 이미 존재하는 상태(Claude Code 세션 정보, Vault에 이미 발행된 산출물의 존재/최신 여부)를 **그대로 반영해 사람이 실시간으로 볼 수 있게** 만드는 행동 유형(M45). Intelligence처럼 "지금 상황이 어떤가"를 새로 판단하지 않는다 — Recommendation/Adaptation/Explainability/Orchestration/Execution/Memory/Experience 어느 것의 판단 로직도 바꾸지 않고, 그 산출물이 이미 있는지 없는지만 확인한다. Read Only라는 점은 Intelligence와 같지만 소비 대상(터미널 StatusLine)과 트리거(Claude Code 세션 이벤트)가 달라 별도 개념으로 둔다. 재사용 사례가 쌓이면(예: Dashboard/CLI Observability) 1급 Domain 승격을 재검토한다 | ADR-0062 |

### 13.4 Milestone Naming Convention — "Domain + Responsibility"

**규칙**: Milestone 이름은 항상 `{Domain} {Responsibility}` 형태를
따른다. `{Domain}`은 §13.2/§13.3의 기존 용어 중 하나여야 하고,
`{Responsibility}`는 그 Domain이 무엇에 대해 작동하는지를 명사로
표현한다.

**예시**(기존 Milestone 이름 재확인)

| Milestone 이름 | Domain | Responsibility |
|---|---|---|
| Project Intelligence(M29) | Intelligence | Project(상태 관찰 대상) |
| Workflow Intelligence(M34) | Intelligence | Workflow(상태 관찰 대상) |
| Recommendation Execution(M36) | Execution | Recommendation(실행 대상) |
| Execution Memory(M39) | Memory | Execution(저장 대상) |
| Architecture Guardian(M41) | Guardian | Architecture(평가 대상) |
| Recommendation Adaptation(M42) | Adaptation(§13.3 Behavioral Concept) | Recommendation(조정 대상) |
| Recommendation Orchestration(M43) | Orchestration(§13.3 구조적 관행) | Recommendation(제어 대상 흐름) |
| Recommendation Explainability(M44) | Explainability(§13.3 Behavioral Concept) | Recommendation(설명 대상) |
| Workspace Observability(M45) | Observability(§13.3 Behavioral Concept) | Workspace(관측 대상 — Claude Runtime + Pipeline 전체) |

**이 규칙이 존재하는 이유**: `{Domain}`을 고정하면 이름만 보고도 그
컴포넌트가 Read Only인지(Intelligence) side-effect를 일으키는지
(Execution) 저장만 하는지(Memory)를 즉시 알 수 있다 — §8 의존성
규칙과 1:1로 대응하는 이름 체계다. `{Responsibility}`가 자유롭게
바뀌어도 `{Domain}`이 그대로면 그 컴포넌트가 지켜야 할 아키텍처
제약(예: Intelligence는 절대 쓰지 않는다)이 이름만으로 드러난다.

**새 용어 도입이 허용되는 경우**: §13.2/§13.3의 어떤 용어로도 그
개념의 핵심 책임(Read Only 판단 / 저장 / 실행 / 감시 등)을 정확히
표현할 수 없을 때만 새 Domain 용어를 만든다. 이 경우에도 §1.4
Approval Required에 따라 사용자 승인을 받아야 하며, 승인 시 그
새 용어를 본 절(§13.2)에 즉시 추가해 다음 Milestone부터 재사용
가능하게 한다.

**기존 어휘를 재사용해야 하는 경우**: 다음처럼 이미 존재하는 개념과
본질적으로 같다면 새 단어를 만들지 않는다.

- `Knowledge` — 이미 Project Knowledge System(M16, `KnowledgeSearch`/
  `KnowledgeProvider`)이라는 확립된 의미가 있다. "정보를 찾아 준다"는
  개념이 필요하면 Knowledge를 재사용하거나 Intelligence로 표현한다.
- `Insight`/`Learning` — Intelligence(관찰·판단, Read Only)와
  경계가 흐릿한 동의어다. "판단한다"는 Intelligence, "과거 기록으로
  판단 기준 자체를 바꾼다"는 아직 이름이 정해지지 않은 별도
  개념이며(ADR-0053이 M40 이후로 명시적으로 미룸), 임의로
  Insight/Learning이라는 새 이름을 붙이지 않고 착수 시점에 §13.2에
  정식으로 추가한다.
- `Analyzer`/`Manager` — 이미 내부 클래스 이름 접미사로 널리 쓰인다
  (`RecommendationRuleAnalyzer`, `ContextManager`). Milestone/Domain
  이름(위 Naming Convention의 `{Domain}`)으로는 쓰지 않는다 — 이들은
  "무엇을 하는 클래스인지"를 나타내는 구현 세부사항이지, 이
  저장소의 아키텍처 층위를 가리키는 Domain 어휘가 아니다.

### 13.5 신규 용어 도입 전 확인 절차 (영구 규칙)

다음을 새로 도입하기 전에는 **반드시** 먼저 이 개념이 §13.2/§13.3의
기존 어휘로 표현 가능한지 확인한다.

- 새 Milestone 이름
- 새 Engine
- 새 Service
- 새 아키텍처 개념(Layer/Adapter/Runtime 등)

기존 어휘로 정확히 표현할 수 없는 경우에만 새 어휘를 만든다(§13.4
"새 용어 도입이 허용되는 경우" 참고). 이 규칙은 `.ai/RULES.md`
§1.5(Vocabulary Reuse First)에도 동일하게 반영되어 있다.

### 13.6 Class/File Naming Standard (ADR-0057, 2026-07-30)

M39~M41 이후 "Repository Naming Consistency Review"(사용자 요청,
2026-07-30)가 실제 저장소(300개 클래스, 160여 개 모듈)를 전수
조사했다. 이 절은 **새 규칙을 만드는 것이 아니라, 그 조사에서 이미
일관되게 지켜지고 있음이 확인된 관행을 공식 문서로 승격**한다 —
M42 이후에도 계속 지켜야 할 기준선이다.

**클래스 접미사별 역할(전부 실측 확인됨)**

| 접미사 | 역할 | 근거 |
|---|---|---|
| `*Analyzer` | 순수 Read Only 판정 — 부작용 없음, 대부분 생성자 인자 없이 `analyze()`만 제공 | `intelligence/`의 9개 Analyzer(`RecommendationRuleAnalyzer`/`CapabilityGapAnalyzer`/`WorkflowFlowAnalyzer` 등) 전수 확인 |
| `*Service` | 여러 Analyzer/Adapter/Store를 조합하는 얇은 계층. Vault 발행처럼 "공표"가 핵심이면 `publish()`를 기본 진입점으로 삼는다(M41 Guardian 선례) | `intelligence/`의 8개 `*_service.py` 파일 전수 확인(예외 없이 `*Service` 클래스 정의) |
| `*Store` | **시간순/로그성 데이터**(추가되기만 하고 개별 항목을 갱신하지 않는 기록) | `EventStore`(M1)/`ExecutionMemoryStore`(M39) — 2건뿐이라 관찰에 가깝지만 방향은 일관됨 |
| `*Repository` | **단일 Aggregate에 대한 CRUD**(생성/조회/갱신/삭제 대상이 명확한 하나의 엔티티) | `AgentRepository`/`ProjectRepository`/`AutomationRepository`/`DashboardRepository`/`KnowledgeRepository` 등 27종 Interface의 다수 |
| `*Adapter` | Integration Layer의 유일한 진입점 — Core Domain(domain/interfaces/engines)과 외부 자원(Vault/Agent Runtime/Knowledge) 사이의 유일한 통로 | `VaultAdapter`/`AgentAdapter`/`KnowledgeAdapter`/`WorkflowAdapter` |
| `*View` | Adapter가 domain 타입을 감싸 외부(주로 `intelligence/`)에 노출하는 읽기 전용 투영 — domain 타입을 그대로 흘려보내지 않기 위함(§8 규칙 18/21) | `TaskDocumentView`/`KnowledgeDocumentView`/`AgentCapabilityView`, M40의 `ExecutionMemoryEntry`(같은 역할, 이름만 `Entry`) |
| `*Record` | 로그성 개별 기록 1건(발생 시점이 있는 사실) | `ExecutionRecord`/`ExperienceRecord` |
| `*Report` | 여러 `Result`/`Record`/판단을 모은 집계 산출물. Service의 `generate()` 반환 타입 | `ArchitectureHealthReport`/`ProjectHealthReport`/`WorkflowFlowReport` 등 12건 |
| `*Result` | 단일 연산 1회 호출의 결과(성공/실패 포함) | `EngineExecutionResult`/`TaskSyncResult`/`ArchitectureCheckResult` 등 11건 |
| `*Rule` | 메서드 없는 순수 값 객체(평가 로직을 갖지 않는다 — 평가는 별도 함수/클래스가 담당) | `guardian/rules.py`의 3종(M41, ADR-0056) |
| `*Manager` | 클래스 접미사로만 허용, Milestone/Domain 이름으로는 쓰지 않는다(§13.4에 이미 명시) | `AgentManager`/`ContextManager`/`LifecycleManager` |
| `*Engine` | **두 가지 의미로만 한정**: ① Core Engine(§3.7, Agent가 쓰는 상태 없는 서비스 — `TaskEngine`/`WorkflowEngine`/`MemoryEngine` 등 27종 Interface 소속) ② 구현 엔진 실행 관리(§3.9, `EngineAdapter`/`EngineRuntime`/`EngineRegistry`) — 이 두 의미 **밖에서는 새로 쓰지 않는다** | 리뷰에서 `ProjectRecommendationEngine`(①·②도 아닌 사실상 Analyzer)이 위반 사례로 발견됨 — 개선 여지로 기록(아래) |

**파일명 ↔ 클래스명 대응 원칙**

- `{name}_service.py`는 반드시 `{Name}Service`로 끝나는 클래스를
  정의해야 한다 — `guardian/`의 Role 기반 접근 규칙(M40/ADR-0055,
  M41/ADR-0056)이 이를 실제로 `ast`로 강제한다.
- `{name}_rules.py`는 순수 Rule/Analyzer(부작용 없음)만 담는다 —
  Adapter/Store를 참조하면 안 된다(M40의 "Analyzer 순수성" 강제와
  동일 원칙).
- 파일명과 핵심 클래스명이 일치하지 않는 예외(`report.py`→
  `ProjectIntelligenceService`, `recommendation.py`→
  `ProjectRecommendationEngine`)는 M29(§13 확립 이전) 시절 파일이다
  — 새 파일에서는 반복하지 않는다. 기존 파일 개선은 별도 논의
  (아래 "개선 여지").

**디렉터리명 ↔ Domain 대응 원칙**

- `guardian/`/`intelligence/`/`memory/`/`runtime/execution/`은
  §13.2 4개 1급 Domain과 정확히 1:1 대응한다 — 새 최상위 디렉터리를
  만들 때도 이 대응을 우선 확인한다(§13.5와 동일한 절차).
- `domain/`(Core Domain Model 패키지, ADR-0001)은 §13.2의 "Domain
  Vocabulary"와 **이름만 같고 완전히 다른 개념**이다 — 착수하는
  사람은 어느 쪽 "Domain"인지 문맥으로 구분해야 한다(동음이의어,
  이번 리뷰에서 처음 명시적으로 기록됨).

**Naming Technical Debt Ledger(공식 기술 부채 목록, 2026-07-30
사용자 결정)** — 아래 표는 §13.6 위반이 발견될 때마다 항목을
추가하는 이 프로젝트의 **공식** 기술 부채 목록이다. 즉시 실행하지
않는다(Boy Scout Rule, 아래 참고).

| 현재 | 제안 | 사유 | 상태 |
|---|---|---|---|
| `ProjectRecommendationEngine` | `ProjectRecommendationAnalyzer` | 위 Engine 표의 두 의미 어디에도 속하지 않음 | 미해결 |
| `intelligence/recommendation.py` | `intelligence/project_recommendation.py` | `recommendation_rules.py`/`recommendation_service.py`(M35, 더 넓은 의미)와 구별 | 미해결 |
| `tests/integration_layer/` | (이름 유지) §9에 "`tests/integration/`과의 명칭 충돌 회피" 주석만 추가 | 이름 변경보다 문서화가 더 안전 | 미해결 |

이 4건을 한꺼번에 처리하는 대규모 Rename PR은 만들지 않는다 —
대신 다음 3원칙을 유지한다(2026-07-30 사용자 결정, `.ai/RULES.md`
§1.6에 영구 반영):

1. **신규 코드는 §13.6을 예외 없이 100% 준수한다** — "이번만 예외"는
   허용하지 않는다.
2. **기존 코드는 Boy Scout Rule로 정리한다** — 해당 파일을 **기능
   변경이 발생한 PR에서만** 함께 Rename한다. Rename만을 목적으로 한
   별도 PR(Cleanup Sprint 포함)은 만들지 않는다.
3. **이 표는 공식 기술 부채 목록으로 유지한다** — 새 위반이
   발견되면 이 표에 행을 추가한다. 항목이 해결되면 행을 **지우지
   않고** "현재"/"제안" 칸에 취소선(`~~이전 이름~~`)을 긋고, "상태"
   칸에 해결 일자와 처리한 PR/커밋을 짧게 남긴다(예: "해결
   2026-08-05, PR #40") — 표 자체가 언제 무엇이 왜 바뀌었는지의
   변경 이력이 된다.

이 방식으로 대규모 일괄 Rename 없이도 저장소가 점진적으로 표준에
수렴하며, 별도 Cleanup Sprint를 편성할 필요가 없다.

## 14. Obsidian Graph Convention (ADR-0054, 2026-07-30)

### 14.1 목적

Obsidian Graph View가 폴더 구조(`00 System`~`15 Project
Intelligence`)를 그대로 반영하는 무의미한 그물망이 되지 않고, **§13의
아키텍처 어휘(Domain)를 시각적으로 드러내는 지도**가 되도록 한다.
폴더는 "문서가 어디 저장돼 있는가"만 나타내지만, 이 절이 정의하는
Cluster는 "이 문서가 아키텍처적으로 무엇인가"를 나타낸다 — 같은
폴더(`15 Project Intelligence/`) 안에 있어도 `Recommendation
Execution.md`는 Intelligence가 아니라 Execution Cluster에 속한다.

### 14.2 Graph Cluster 정의

| Cluster | 색상(제안) | 포함 대상(§13 Domain 기준) |
|---|---|---|
| 🔵 Intelligence | Blue | Project Intelligence, Context Intelligence, Capability Intelligence, Workflow Intelligence, Recommendation Intelligence, Intelligence Overview, Session Resume |
| 🟢 Execution | Green | Recommendation Execution, Task Status 이력(Task Lifecycle), AutomationScheduler 관련 문서 |
| 🟡 Memory | Yellow | Execution Memory 관련 문서(향후 Vault 노출 시), Session/Mission Summary(장기 Memory) |
| 🟣 Architecture | Purple | ADR Index 및 개별 ADR, Architecture Overview, Architecture Guardian(M41, `.obsidian/graph.json` Cluster 반영은 별도 검증 대기 — Pending Verification 상태) |
| 🔴 Domain | Red | Agent, Task, Workflow, Project를 다루는 개별 문서(예: `14 Tasks/*.md`) |
| 🟠 Documentation | Orange | README, ROADMAP, PRD, Overview, Templates |

이 매핑은 §13.2/§13.3의 Domain 어휘와 1:1로 대응한다 — 새 Cluster를
만들기 전에 먼저 새 Domain 어휘가 §13에 추가되어 있는지 확인한다
(Cluster는 Vocabulary의 파생물이지 독립적인 분류 체계가 아니다).

### 14.3 현재 Vault 문서 → Cluster 매핑 (참고)

| Vault 위치 | Cluster |
|---|---|
| `15 Project Intelligence/Project Intelligence.md`, `Project Context.md`, `Capability Intelligence.md`, `Workflow Intelligence.md`, `Recommendation Intelligence.md`, `Intelligence Overview.md`, `Session Resume.md` | 🔵 Intelligence |
| `15 Project Intelligence/Recommendation Execution.md`("Task Status 이력" 섹션 포함) | 🟢 Execution |
| `03 ADR/ADR Index.md` 및 `12 Decisions/` | 🟣 Architecture |
| `11 Milestones/Milestones Index.md` | 🟣 Architecture(Milestone은 아키텍처 결정의 진행 기록이므로 ADR과 같은 Cluster) |
| `14 Tasks/*.md` | 🔴 Domain |
| `01 Overview/`, `99 Templates/`, 저장소 루트 `README.md` | 🟠 Documentation |
| `13 Daily/` | 🟠 Documentation(운영 기록, 특정 Domain에 속하지 않음) |
| `04 Backend/`, `05 API/`, `06 Dashboard/`, `07 Automation/`, `08 Production/`, `09 iOS/`, `10 Android/` | 해당 문서가 다루는 Domain에 따라 개별 판단(예: `07 Automation/Automation Index.md`는 🟢 Execution) — 폴더 자체가 Cluster를 결정하지 않는다(§14.1) |

### 14.4 Linking Rules

- **의미 있는 아키텍처 관계만 링크한다.** "같은 Milestone에서 만들어졌다"는
  이유만으로 링크하지 않는다 — 실제 의존 관계(§8 Dependency Rules)나
  같은 Cluster 내 참조 관계일 때만 링크한다.
- **불필요한 Cross-Cluster 링크를 피한다.** Intelligence 문서가
  Execution 문서를 링크하는 것은 실제 소비 관계(§13.2의 "대표
  소비자")가 있을 때만 허용한다 — 예: `Recommendation
  Intelligence.md` → `Recommendation Execution.md`(M35 Recommendation을
  M36이 실행)는 허용, 무관한 Intelligence 문서 간 임의 링크는
  지양한다.
- **계층적 링크를 우선한다.** Index 문서(`ADR Index`, `Milestones
  Index`)가 개별 문서를 링크하는 방향을 기본으로 하고, 개별 문서끼리
  직접 링크하는 것은 실제 참조가 있을 때만 추가한다.
- **완전 연결 그래프(Mesh)를 막는다.** 한 문서가 같은 Cluster 안의
  모든 문서를 링크할 필요는 없다 — Index를 거쳐 탐색 가능하면
  충분하다. Graph View에서 한 문서의 링크 수가 비정상적으로 많다면
  (예: 10개 초과) 그 문서가 실제로는 Index 역할을 하고 있는 것은
  아닌지 재검토한다.

### 14.5 적용 계획

이번 문서화에서는 §14.2~14.4의 **규칙만 정의**한다. 기존 Vault
문서에 Domain Cluster를 나타내는 새 Tag(예: `#cluster/intelligence`)를
일괄 추가하는 작업과 `.obsidian/graph.json`의 실제 Group/Color 설정은
**별도 후속 작업**으로 남긴다 — 수십 개 문서의 Frontmatter를 한 번에
바꾸는 것은 "문서화만" 범위를 벗어나는 별도 변경이며, §1.4 Approval
Required(리팩토링/새 기능 해당)에 따라 별도 제안·승인이 필요하다.
