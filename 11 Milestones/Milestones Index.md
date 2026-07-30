---
tags: [milestone]
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
| M31 | Capability Intelligence | 정의된 `AgentCapability`(11종) 대비 활성 Agent가 실제로 커버하는 Capability를 정리하는 Read Only Capability Intelligence. T01(설계)~T05(Presentation) 전체 완료 — 신규 Adapter 없이 기존 `AgentAdapter` 확장만(새 메서드 2개), 새 Core Domain Interface 없음(27종 유지), LLM 추론/새 지식 생성 없음, 결과는 [[Capability Intelligence]]에 노출. **Milestone Review 완료 — 사용자 승인 대기** | ADR-0045 |

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
