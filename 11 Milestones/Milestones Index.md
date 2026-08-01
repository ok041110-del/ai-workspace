---
tags: [milestone]
type: milestone
---

# Milestones Index

> Milestone 1~22 전체 이력 요약. 상세 Task 목록/Review는 GitHub
> `.ai/TASKS.md` 원문 참고. [[ADR Index]]와 교차 참고하면 각 결정의
> 배경을 알 수 있다.

> **Task 변경 로그(Milestone 28-T02)**: 이 문서에 "## Task 변경
> 로그" 절이 보인다면 `vault/task_sync.py`가 Task 상태 변경 때마다
> 자동으로 추가한 것이다 — `docs/ROADMAP.md`는 GitHub 원문이라
> Vault가 직접 쓰지 않으므로, 그 대신 이 Vault 쪽 대응 문서에
> Task와 Milestone을 잇는 연결 로그를 남긴다(각 줄이 해당 Task
> 문서로의 Wikilink다).

| Milestone | 이름 | 핵심 결과 | 관련 ADR |
|---|---|---|---|
| M1 | 기반 구축(Foundation) | 27종 중 다수 Interface 최초 정의, 도메인 모델 확립, Multi-Agent First 구조 확정 | ADR-0006, 0010~0013 |
| M2 | 멀티 에이전트 코어(Multi-Agent Core) | Agent Runtime 실제 구현, Capability 기반 선택 | ADR-0012, 0019 |
| M3 | 실행 엔진 연동 & 상호작용 | EngineAdapter 실제 구현, Interaction Layer 구현 | ADR-0002, 0013, 0015 |
| M4 | 자동화 및 확장 | AutomationEngine(T1-07), `run_parallel()` 실제 동시성. v0.5.0 아키텍처 기준선 선언 | ADR-0023, 0024 |
| M5 | 실제 개발 수행 | LLMPolicyEngine 구현, 실제 코드 작성 파이프라인 검증 | — |
| M6 | Policy 기반 실행 라우팅 | Policy Rule 기반 Provider/Model/Effort 결정 고도화 | — |
| M7 | Memory 요약 | Memory 요약 기능 도입 | — |
| M8 | 세션 연속성 | WorkspaceSession 연속성 보강 | — |
| M9 | 세션 견고성 | 세션 실패 복구 검증 | — |
| M10 | 실행 복원력 | 실행 실패에 대한 초기 복원력 확보 | — |
| M11 | Execution Environment | `ExecutionEnvironment` Interface 도입, `LocalExecutionEnvironment` 구현 | ADR-0025 |
| M12 | Workflow Automation | `WorkflowRunner` 구현, End-to-End 워크플로 자동화 검증 | — |
| M13 | Multi-Agent Collaboration | Scheduler 가드(`is_agent_selected()`) 도입 | — |
| M14 | LLM Routing(Model 수준 라우팅) | EngineAdapter/EngineRuntime 계약에 `model` 파라미터 확장 | ADR-0026 |
| M15 | Token & Cost Optimization | `EngineRuntime.estimate_cost()` + `BudgetPolicyEngine` 신설 | ADR-0027 |
| M16 | Project Knowledge System | `KnowledgeRepository`/`KnowledgeSearch`/`KnowledgeProvider` 도입(MemoryEngine과 분리) | ADR-0028 |
| M17 | Intelligent Engine Selection | `EngineRegistry` + `EngineSelectionPolicy` 도입 | ADR-0029 |
| M18 | Multi-Engine Execution Integration | `ExecutionDispatcher` + `AuthenticationManager` 도입, 유일한 실행 진입점 확정 | ADR-0030 |
| M19 | Reliability Layer | `RetryPolicy` 확장 + `RetryExecutor` 도입 | ADR-0031 |
| M20 | Real-time Dashboard Platform | `DashboardRepository`(26번째 Interface) 도입, 첫 외부 런타임 의존성(FastAPI/uvicorn) | ADR-0032 |
| M21 | Automation Engine | `AutomationRepository`(27번째 Interface) 도입, AutomationScheduler | ADR-0033 |
| M22 | Production Platform | `ProductionConfig`/`LifecycleManager`/`HealthMonitor` 도입, 새 Interface 없음 | ADR-0034 |
| M27 | Obsidian Workspace Templates(M25 요청) | `VaultDocumentKind.TASK` 신규(개별 Task 문서), Daily/Decision Template 확장, Project Workspace Template 정의(설계만) | ADR-0038 |
| M28 | Live Task Management & Integration | Task Lifecycle/자동 문서 갱신(Vault 내부), 신규 `integration/` 패키지(Workspace Adapter Layer) — Vault/Workflow/Agent Adapter, Peer Connector(WorkflowTaskLink/WorkflowAgentLink), Orchestrating Connector(ConversationConnector). Core Domain↔vault 직접 의존 금지를 `ast` 테스트로 강제, Domain 모델 무변경. **Architecture Freeze 완료**(Peer Connector 상호 참조 위반 1건 발견·수정) | ADR-0039, 0040, 0041, 0042 |
| M29 | Project Intelligence | Project/Workflow/Task/Agent/Event/Vault 데이터로 Project Snapshot/Health/Risk/Recommendation을 만드는 Read Only Intelligence Layer(`intelligence/`, 신규). T01(설계)~T05(Integration & Presentation) 전체 완료, Vault Task 문서를 단일 데이터 소스로 채택, 새 Core Domain Interface 없음(27종 유지), 결과는 [[Project Intelligence]]에 노출. "의존성 위험"은 Deferred by Design. **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0043 |
| M30 | Context Intelligence | Knowledge Layer(M16)/Intelligence Layer(M29)를 종합해 지금 작업(Task/Milestone)과 관련된 맥락을 정리하는 Read Only Context Intelligence. T01(설계)~T05(Presentation) 전체 완료 — `KnowledgeAdapter` 신규(기존 Knowledge Interface만 감쌈), 새 Core Domain Interface 없음(27종 유지), LLM 추론/새 지식 생성 없음, 결과는 [[Project Context]]에 노출. **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0044 |
| M31 | Capability Intelligence | 정의된 `AgentCapability`(11종) 대비 활성 Agent가 실제로 커버하는 Capability를 정리하는 Read Only Capability Intelligence. T01(설계)~T05(Presentation) 전체 완료 — 신규 Adapter 없이 기존 `AgentAdapter` 확장만(새 메서드 2개), 새 Core Domain Interface 없음(27종 유지), LLM 추론/새 지식 생성 없음, 결과는 [[Capability Intelligence]]에 노출. **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0045 |
| M32 | Intelligence Synthesis | M29(Project)/M30(Context)/M31(Capability) Intelligence 리포트를 새 데이터 소스·판단 기준 없이 하나의 `IntelligenceOverview`로 합성하는 통합 계층. T01(설계)~T04(E2E+문서화+Review) 전체 완료 — 신규 Adapter/Interface 없이 기존 3개 Service만 조합, `VaultAdapter` 확장 1건(`publish_intelligence_overview()`), 새 Core Domain Interface 없음(27종 유지), LLM 추론/새 지식 생성 없음, 결과는 [[Intelligence Overview]]에 노출. **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0046 |
| M33 | Session Resume | 새 세션 시작 시 "지금 무엇을 하고 있었는가"를 자동 복원하는 Read Only Session Resume. M29~M32 Intelligence를 그대로 재사용하고 "현재 작업" 선택 규칙 1개만 추가. T01(설계)~T04(Presentation+E2E+문서화+Review) 전체 완료 — 신규 Adapter/Interface 없음(`VaultAdapter` 확장 1건), 새 Core Domain Interface 없음(27종 유지), LLM 추론/새 Intelligence 생성 없음, 결과는 [[Session Resume]]에 노출. **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0047 |
| M34 | Workflow Intelligence | Vault Task 문서의 Milestone별 Task 실행 흐름을 분석하는 Read Only Workflow Intelligence. "Workflow"는 `domain.Workflow`(영속 저장소 없는 휘발성 값 객체)가 아니라 Milestone 안의 Task 실행 순서로 재정의(사용자 승인 조건). Blocked/Next Rule 1개를 `WorkflowFlowAnalyzer`(순수 Analyzer)에 캡슐화하고 `WorkflowIntelligenceService`는 조합만 담당. T01(설계)~T04(Presentation+E2E+문서화+Review) 전체 완료 — 신규 Adapter/Interface 없음(`VaultAdapter` 확장 1건), 새 Core Domain Interface 없음(27종 유지), `domain.Workflow`/`WorkflowEngine`/`WorkflowAdapter` 무변경(사용하지 않음), 결과는 [[Workflow Intelligence]]에 노출. **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0048 |
| M35 | Recommendation Intelligence | M29(Project)/M31(Capability)/M33(Session Resume)/M34(Workflow) Intelligence를 그대로 조합해 "지금 무엇을 하는 것이 가장 적절한가"를 결정하는 Read Only Decision Layer. 5단계 Priority Rule(Current Work→Workflow Next→Workflow Blocked→Capability Gap→Project Recommendation) 1개를 `RecommendationRuleAnalyzer`(순수 Analyzer)에 캡슐화, `RecommendationIntelligenceService`는 조합만 담당. Execution Layer 이전의 마지막 Decision Layer — 자동 실행 없음(Automation은 M36 이후). T01(설계+MDD Review)~T04(Presentation+E2E+문서화+Review) 전체 완료 — 신규 Adapter/Interface 없음(`VaultAdapter` 확장 1건), 새 Core Domain Interface 없음(27종 유지), 결과는 [[Recommendation Intelligence]]에 노출. **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0049 |
| M36 | Execution | M35 `NextAction`의 `source=next_task` 추천만, 수동 트리거로만, 기존 `ExecutionDispatcher`(M18)/`EngineRegistry`/`EngineSelectionPolicy`(M17) 파이프라인에 연결해 실제로 실행하고 결과를 Vault에 보고. `ExecutionGate`(판정)/`ActionBuilder`(변환) 책임 분리, `AutomationActionExecutor`(M21)를 감싸지 않고 그 내부와 동일한 3단계 직접 재사용. **M29~M35 Read Only Intelligence를 실제 실행으로 연결한 첫 side-effecting Milestone.** T01(설계+MDD Review)~T04(Presentation+E2E+문서화+Review) 전체 완료 — 신규 Adapter/Interface 없음(`VaultAdapter` 확장 1건), 새 Core Domain Interface 없음(27종 유지), Task 상태 자동 전이 없음, 결과는 [[Recommendation Execution]]에 노출. **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0050 |
| M37 | Task Lifecycle | M36 Execution 결과(Gate 승인/실행 성공·실패)를 이미 존재하는 Task 상태 전이 기계(`_ALLOWED_TRANSITIONS`, M28)에 연결. 실행 시작 시 `todo→in-progress`, 성공 시 `in-progress→review`, 실패 시 `in-progress→todo`만 자동화(`review→done`은 사람 검토로 남김). `TaskLifecycleTransitioner`(현재 상태 확인 후 유효한 전이만 결정)가 방어적으로 판정. Presentation을 Execution 결과/Task Status 이력으로 분리. T01(설계+MDD Review)~T04(Presentation 분리+E2E+문서화+Review) 전체 완료 — 새 상태·새 전이 규칙·새 Adapter 없음(`VaultAdapter` 확장도 없음), 새 Core Domain Interface 없음(27종 유지), 결과는 [[Recommendation Execution]]의 "Task Status 이력" 섹션에 노출. **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0051 |
| M38 | AutomationScheduler 연결 | M21 `AutomationScheduler`와 M35~M37 Recommendation Execution 파이프라인을 `web/server.py`의 `build_app()`(Composition Root)에서 실제로 연결. `VaultAdapter`/`AgentAdapter`/`RecommendationIntelligenceService`/`RecommendationExecutionService`가 `tests/`에서만 조립되던 "워크숍 단계" 한계를 해소해 최초로 실배선. 새 `ActionKind.RUN_RECOMMENDATION`(추가 필드 없음)이 `AutomationActionExecutor`를 거쳐 `RecommendationExecutionService.publish(manual_trigger=True)`를 호출 — `ExecutionGate`는 M36과 동일하게 `source=next_task`만 승인(새 정책 없음). `done→archived` 자동화·재시도 정책·`review→done` 자동화·CLI·Hook은 범위 밖(YAGNI). 새 Core Domain Interface/Adapter 없음(27종 유지). **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0052 |
| M39 | Execution Memory | M38 Review가 M39 이후로 미룬 세 Engine(Memory Engine/Architecture Guardian/Learning Engine) 중 Memory Engine 착수. Execution 결과를 새 Interface 없이 기존 `MemoryEngine`(M1)에 자동 저장하고 `ExecutionMemoryStore`(신규 Service)로 조회만 제공 — `ExecutionMemory`(task_id/action/result/timestamp/reason)에 embedding/score/vector/confidence 없음. `RecommendationExecutionService`에 선택적 의존성으로 주입(미주입 시 M38 이전과 동일). 영속화(Vault 파일)는 `MemoryEngine`(M1 기초 계약)이 `vault/`(M28+ Layer)에 하향 결합되는 문제로 범위 제외, Learning(Rule 반영)은 M40 이후로 이관(사용자 조건부 승인). 새 Core Domain Interface/Adapter 없음(27종 유지). **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0053 |
| M40 | Experience Intelligence | `ExecutionMemoryStore`(M39)에 쌓인 실행 기록을 task_id별 성공/실패 집계로 바꾸는 Read Only Intelligence — Scope는 (a)Read-Only Reporting만(Recommendation 판정 로직 미반영, Learning 없음). `ExperienceAnalyzer`(`intelligence/experience_rules.py`)는 외부 패키지 import 0개로 완전히 순수(Deterministic+Immutable Input, 사용자 조건). 구현 중 `ExecutionMemoryStore.query()`가 domain 타입을 그대로 반환해 `intelligence/`의 domain 참조 금지 규칙과 충돌함을 발견 — `ExecutionMemoryEntry`(신규 View 타입, `TaskDocumentView`와 동일 패턴)로 해결. §8 규칙 21을 특정 클래스명 나열 대신 **Role 기반**(`*Service` 클래스 정의 모듈만 `memory/` 접근 허용)으로 재정의(사용자 조건부 승인). 결과는 [[Experience Intelligence]]에 노출. 새 Core Domain Interface/Adapter 없음(27종 유지). **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0055 |
| M41 | Architecture Guardian | `docs/ARCHITECTURE.md` §13.2가 예약해 둔 Guardian Domain의 내용을 채움 — "Guardian owns the executable representation of architectural rules... evaluates conformance, and publishes architectural health." Reuse First로 `tests/` 5곳에 중복 구현돼 있던 `ast` 경계 검사를 발견해 새로 만들지 않고 통합. `ArchitectureRule`은 ABC가 아니라 메서드 없는 `frozen dataclass` 3종의 Union(`ForbiddenPackageImportRule`/`AllowedImportPrefixRule`/`ServiceRoleGatedImportRule`), `GUARDIAN_RULES`는 `Final`+`tuple`(불변 Registry). `guardian/checker.py`는 `pytest`를 모르는 순수 평가기, `ArchitectureGuardianService.publish()`가 핵심 진입점(Vault 발행이 부가 기능 아님). 3개 Rule 형태에 맞는 5개 규칙만 이전, Connector 그룹 규칙 2개는 억지로 일반화하지 않고 범위 제외(사용자 조건). 결과는 [[Architecture Guardian]]에 노출. 새 Core Domain Interface/Adapter 없음(27종 유지), 새 Layer 1개(`guardian/`). **Milestone Review 완료 — 사용자 승인(2026-07-30)** | ADR-0056 |
| M42 | Recommendation Adaptation | M39(Execution Memory)가 Non-goal로 명시적으로 미뤄뒀던 "과거 실행 결과로 판단 기준을 조정한다"는 책임을 처음 다룸. T02 Domain Analysis로 §13.4가 이미 배제해둔 `Learning`/`Insight` 대신 `Adaptation` 용어를 채택(재사용 사례 1건뿐이라 1급 Domain 승격은 보류, §13.3 Behavioral Concept로만 정의). `RecommendationAdjustmentAnalyzer`(신규)는 M35 `RecommendationRuleAnalyzer`의 `NextAction`을 새로 생성하지 않고 M40 `ExperienceReport`를 근거로 사후 조정(Adjustment)만 함 — 대상의 과거 실행이 전부 실패일 때만 추천 보류. `RecommendationIntelligenceService.generate()/publish()`에 `experience_report` 선택적 인자 추가, `None`이면 M35와 100% 동일 동작(사용자 조건 5개 전부 반영). 새 Core Domain Interface/Adapter 없음(27종 유지), `web/server.py` 자동 배선 없음(Non-goal). **Milestone Review 완료 — 사용자 승인(2026-07-31)** | ADR-0058 |
| M43 | Recommendation Orchestration | M42가 Non-goal로 남겨둔 `web/server.py` 자동 배선을 완성 — M35(Recommendation)→M42(Adaptation)→M36(Execution)→M39(Memory)→M40(Experience)로 이어지는 실행 흐름을 명시적으로 연결. T02 Domain Analysis로 `Workflow`(M34, 다른 의미) 재사용을 배제하고, 이미 확립된 `Orchestrating Connector`(ADR-0041)/`Orchestrating 패턴`(M32, M40)과 같은 의미인 `Orchestration`을 §13.3에 최초 등재(1급 Domain 아님). `RecommendationOrchestrationService`(신규)가 Experience 조회 → Recommendation 계산(Adaptation 포함) → Execution 위임을 판단 로직 없이 순서대로 호출. MDD Review 중 사용자 재검토 요청으로 `RecommendationExecutionService`(M36)의 Recommendation 의존성을 아예 제거해 결합도 개선(Composition Root/Analyzer/Orchestration Service/Execution Service 네 책임 명시적 분리). `AutomationActionExecutor`/`web/server.py` 배선 교체로 M42 Non-goal 완성. 새 Core Domain Interface/Adapter 없음(27종 유지), `build_app()` 실제 조립 스모크 테스트 통과. **Milestone Review 완료 — 사용자 승인(2026-07-31)** | ADR-0059 |
| M44 | Recommendation Explainability | M43로 완성된 내부 루프(Recommendation→Adaptation→Orchestration→Execution→Memory→Experience) 위에서 Recommendation이 "무엇을 할 것인가"뿐 아니라 "왜 그렇게 결정했는가"를 공식 Domain Concept로 만듦(사용자가 상세 제안서 직접 작성). Domain Analysis로 Recommendation(무엇을)과 Explainability(왜)의 책임 차이를 확인. `RecommendationExplanationAnalyzer`(신규)가 `RecommendationIntelligenceReport`(M35/M42) + `ExperienceReport`(M40)를 읽어 5단계 Priority Rule 평가 흔적 + Experience 성공률 + Adaptation 적용 여부를 재구성 — Recommendation 자체는 바꾸지 않음(새 AI 판단 없음). `RecommendationExplanationService`(신규)가 Vault [[Recommendation Explanation]]에 발행. `Explainability`는 §13.3 Behavioral Concept로 등재(`Adaptation`과 동일 급, 1급 Domain 승격 보류). `RecommendationOrchestrationService`(M43)에 선택적 주입으로 Recommendation→Explainability→Execution 순서 연결(미주입 시 M43과 100% 동일 동작). 새 Core Domain Interface/Adapter 없음(27종 유지). **Milestone Review 완료 — 사용자 승인(2026-07-31)** | ADR-0061 |
| M45 | Workspace Observability | M44까지 완성된 Recommendation 계열 파이프라인(Recommendation→Adaptation→Explainability→Orchestration→Execution→Memory→Experience)은 사후(Vault 문서/pytest)로만 확인 가능했다 — 새 AI 판단·자동화를 추가하지 않고, Claude Code 세션 안에서 이 과정과 Claude Code 자체 Runtime(Model/Effort/Context 사용량)을 실시간 StatusLine으로 반영하는 Observability Phase 1(Claude Code 내부 표시만, Dashboard/Web UI/Automation 제외)을 구축. T01 Domain Analysis로 §13.2 4개 핵심 Domain 어디에도 해당하지 않음을 확인해 `Observability`를 §13.3 Behavioral Concept로 신규 등재(1급 Domain 승격 보류). `observability/`(신규 패키지) — `WorkspaceRuntimeSnapshot`(읽기 전용 Runtime 모델) + 3개 Analyzer(`ClaudeRuntimeAnalyzer`/`PipelineStageAnalyzer`/`WorkspaceInfoAnalyzer`) + `RuntimeSnapshotService` + `StatusLineRenderer`. 7단계 중 Adaptation/Orchestration은 별도 Vault 산출물 없어 `STRUCTURAL_INCLUDED`, Memory는 `InMemoryMemoryEngine` 비영속이라 `NOT_OBSERVABLE`로 정직하게 표시(추정값 사용 안 함). `VaultAdapter.report_last_modified()` 1개 메서드만 확장(새 Adapter 없음), `.claude/settings.json`에 StatusLine 실배선. 새 Core Domain Interface/Adapter 없음(27종 유지). **Milestone Review 완료 — 사용자 승인(2026-07-31)** | ADR-0062 |
| M45 확장 | Workspace Observability — Execution Environment | M45(Claude Runtime + Pipeline)를 "실행 환경"(Git/Guardian/Vault/MCP, 특히 Obsidian MCP)까지 확장 관찰. 새 Domain/Behavioral Concept 아님 — 기존 `Observability`(§13.3) 그대로 확장. 공식 문서 조사 결과 StatusLine JSON에 MCP 필드 없음을 확인, `.mcp.json`(설정 목록)/`claude mcp list`(공식 CLI, 문서화된 기호만 매칭)만 사용. `GitRuntimeAnalyzer`/`GuardianRuntimeAnalyzer`/`VaultRuntimeAnalyzer`/`McpRuntimeAnalyzer`(신규 4개) — Git은 `git` 하위 명령만(fetch 없음), Guardian은 `guardian.checker.evaluate()` 재사용 + `.pytest_cache` 마지막 결과만(재실행 없음), Vault는 `VaultAdapter.report_last_modified()`만. `ruff`/`mypy`/Coverage/MCP `active_server`·`available_tools`·`last_mcp_call`·`last_mcp_error`/Vault `current_pr`/Workspace `current_task`는 공식적으로 안전하게 관측할 방법이 없어 전부 Not Available로 정직하게 표시(Phase 2 후보). 새 Core Domain Interface/Adapter 없음(27종 유지). **Milestone Review 완료 — 사용자 승인(2026-07-31)** | ADR-0063 |
| M46 | Vault Information Architecture | M39~M45로 기능 아키텍처가 안정화된 시점에 Vault를 "문서 저장소"가 아니라 "AI Workspace의 Long-term Memory Layer"로 재정의. 기능 변경 금지. T01에서 Vault 49개 문서 전수 실측 — `type` Frontmatter 13/49만 존재, Tag 대부분 1회성, `ADR Index`/`Milestones Index`가 관련 문서를 Wiki Link가 아닌 백틱 텍스트로만 언급(핵심 발견). T02에서 Graphify/Second Brain 7개 항목마다 채택·수정·기각 판단(Dataview는 Plugin 미설치 확인 후 기각). T03에서 Node/Relationship Definition 확정(PR·Runtime은 Node 아님). Document Type Color Strategy는 §14.2(ADR-0054) Domain Cluster를 폐기하지 않고 확장 — `.obsidian/graph.json` 실제 적용은 Desktop 검증 대기로 계속 보류. T04 Migration Plan은 삭제 없는 증분 방식(Phase 0만 이번에 실행). `02 Architecture/`에 5개 문서 신규 생성, 코드 변경 없음(`pytest`/Guardian 기존 상태 유지). **Milestone Review 완료 — 사용자 승인(2026-07-31)** | ADR-0064 |
| M47 | Knowledge Graph Migration | M46이 Phase 0까지만 실행하고 Deferred로 남긴 Metadata Backfill/Wiki Link Migration/Concept Notes/Hub/Graph Color Migration을 실제 Vault 전체에 적용(새 ADR 아님, ADR-0064 구현 단계). 기능 변경 금지 유지. `type` Frontmatter를 기존 36개 문서에 전수 백필해 Vault 54개 문서 100%(13/49→54/54) 커버리지 달성. `[[Recommendation Hub]]`(신규)로 Recommendation 파이프라인(M35~M44) 리포트 3개의 orphan 문제 해소(inbound 링크 0건→1~4건씩). Concept 문서 7종(Recommendation/Execution/Memory/Guardian/Observability/Automation/Runtime, Adaptation/Orchestration/Explainability는 파이프라인 단계로 판단해 제외) + Concept Index 신규. Architecture/Runtime/Decision/Knowledge Hub 4종 신규(기존 Index 대체 아님). `16 Lessons/` 신규(`VAULT_CONTENT_DIRECTORIES` 17종으로 확장, 실제 Lesson 데이터는 아직 없음 — 허위 생성 금지). `.obsidian/graph.json` 실제 적용은 이번에도 하지 않음(Desktop 검증 대기, 2026-07-30 동결 유지). 코드 변경은 `vault/mapping.py` 상수 목록 1건뿐(8개 보호 기능 전부 무변경). **Milestone Review 완료 — 사용자 승인(2026-07-31)** | ADR-0064 |
| M48 | Automation Foundation | 원래 "Automation Core" 3대 Engine(Memory/Guardian/Learning) 중 마지막 Learning Engine 구현으로 시작할 계획이었으나, M35~M47 구현 완료 후 사용자 지시로 T01 Domain Analysis를 실제 코드 기준으로 재수행 — `RecommendationOrchestrationService`(M43)가 Automation Trigger마다 자동 실행되고 있음에도 Architecture Guardian(M41)만 이 경로 어디에도 연결돼 있지 않음을 확인(테스트/StatusLine에서만 평가됨). Learning이 관찰할 신호(Guardian 위반 이력)가 자동으로 쌓이지 않는 상태에서 Learning Engine을 먼저 설계하는 것은 YAGNI 위반 소지가 크다고 판단해, M48을 "Automation Foundation"(Guardian↔Automation 연결)으로 재정의. Guardian 실행 시점 = Execution 직전(Pre-flight for Execution), 실패 정책 = Recommendation은 그대로 생성하고 Execution만 차단(Override 없음). `ExecutionGate`에 선택적 `guardian_report` 파라미터 추가, M45 StatusLine에 `AutomationGateStatus`(PASS/BLOCKED/UNKNOWN) 신규 노출. 새 Core Domain Interface/Adapter/Service/Layer/File 없음(27종 유지, 기존 6개 파일의 선택적 의존성 확장만). Learning Engine은 M49 이후로 명시적으로 분리. **Milestone Review 완료 — 사용자 승인(2026-08-01)** | ADR-0065 |
| M49 | Learning Engine | ADR-0065가 분리해 둔 Learning Engine 착수. T01 Domain Analysis(코드 전수 조사)로 `ExperienceStat`(M40)의 성공/실패 누적 카운트, `RecommendationAdjustmentAnalyzer`(M42)의 이진 규칙(성공 0건+실패 1건 이상이면 보류), `AutomationGateStatus`(M48)의 최근 1건짜리 Guardian Gate 상태를 인벤토리하고, Guardian 위반 다건 이력·영속 저장소 부재를 Gap으로 확인. 사용자가 학습 대상을 "기존 Adaptation 규칙 정교화"로 한정하고 Guardian 다건 이력 축적·영속 저장소 도입은 이번 Scope에서 명시적으로 배제. `RecommendationAdjustmentAnalyzer`의 보류 조건을 `success_count == 0 and failure_count > 0`(표본 1건부터 보류)에서 `success_count == 0 and total >= 3`(실패율 100% + 표본 3건 이상)으로 교체 — 표본 부족으로 성급하게 보류하던 한계를 최소로 고쳤다(기존 규칙의 상위 집합, 회귀 없음). 새 Domain/Service/Interface/Adapter/Layer/File 없음 — 기존 파일 1개 내부 조건식만 교체. **Milestone Review 완료 — 사용자 승인(2026-08-01)** | ADR-0066 |
| M50 | Learning Persistence | M49가 in-process 범위로 한정했던 `ExecutionMemoryStore`의 저장 엔진을 파일 영속화로 교체. T01 코드 전수 조사로 `MemoryEngine` Interface는 이미 존재하고 구현체는 `InMemoryMemoryEngine` 하나뿐이며 사용처는 `web/server.py` 1곳뿐임을 확인, `storage/`의 기존 File 기반 영속화 패턴(`File*Repository`)을 재사용 가능함을 인벤토리. 사용자가 저장 위치를 "vault_root 하위 전용 디렉터리"로, T02에서 단일 JSON key-value 파일 설계를 승인. 새 Interface/Service 없이 `MemoryEngine`을 구현하는 `FileMemoryEngine`(`storage/`) 신설 — `<vault_root>/.ai-workspace-data/`에 영속화. `web/server.py` Composition Root 1곳만 교체, 다른 사용처(테스트 픽스처·`InMemoryContextManager`) 무변경. StatusLine Observability 배선(별도 프로세스 읽기 경로)은 이번 Scope 밖으로 명시적 분리. **Milestone Review 완료 — 사용자 승인(2026-08-01)** | ADR-0067 |

## Post-M43: Recommendation Vocabulary Review

**Domain Vocabulary Migration 절차로 "Recommendation" 용어 재검토**(ADR-0060).
Milestone 번호가 아닌 M43 완료 후 정리 단계. `src/ai_workspace/`
전수 검색으로 `Suggest`/`Selection`/`Decision`/`Proposal` 4개
대안과 비교 — `Selection`/`Decision`/`Proposal`은 기존 확립된 의미
(각각 `EngineSelectionPolicy`, 6개 `*Decision` 패턴, "Milestone
Proposal" 프로세스 용어)와 충돌하고 `Suggest`는 실질적 이득 없는
동의어일 뿐이라 4개 모두 기각. `Recommendation`을 공식 Domain
Vocabulary로 유지 확정하고 정의를 한 문장으로 고정("현재 프로젝트
상태를 분석해 Next Action을 결정하는 Domain 개념, 비구속적").
문서화 전용 작업 — 코드/클래스/파일명 변경 없음. 상세는 GitHub
`.ai/DECISIONS.md`의 "ADR-0060" 절 참고.

## Pre-M40: Domain Vocabulary & Naming Convention

**프로젝트 전체 명명 규칙 및 Obsidian Graph 규칙 확립**(ADR-0054).
Milestone 번호가 아닌 M40 착수 전 준비 단계. Intelligence/Memory/
Execution/Guardian을 1급 Domain 어휘로 정의하고, Milestone 이름은
`{Domain} {Responsibility}` 형식만 쓰도록 명문화했다. Obsidian Graph
Cluster도 폴더가 아니라 Domain 기준으로 재정의(`docs/ARCHITECTURE.md`
§13/§14). 문서화 전용 작업 — 기존 Milestone/클래스/파일명 변경 없음.
상세는 GitHub `.ai/DECISIONS.md`의 "ADR-0054" 절 참고.

## M23-Preparation

**Obsidian Knowledge Base 구축**(이 Vault 자체). Milestone 번호가
아닌 M23 착수 전 준비 단계. 상세는 GitHub `.ai/TASKS.md`의
"M23-Preparation" 절 참고.

## 관련 문서

- [[ADR Index]]
- [[Architecture Overview]]
- [[Overview]]

## 원문

- `.ai/TASKS.md`
- `docs/ROADMAP.md`
