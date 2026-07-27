---
tags: [decision]
---

# ADR Index

> ADR 전문은 복사하지 않는다. 각 항목은 목적/결정/영향만 4줄로
> 요약하고, 전문이 필요하면 "원문"의 GitHub 링크를 연다.
> ([[AI_RULES]]의 GitHub Link Rule)

## ADR-0001: 문서 구조 3계층

- 목적: PRD/ARCHITECTURE/TASKS 문서 역할 분리 기준 확립
- 결정: PRD(무엇/왜)-ARCHITECTURE(어떻게)-TASKS(언제/누가) 3계층으로 문서를 나눈다
- 영향: 이후 모든 Milestone 문서화가 이 3계층 구조를 따름

## ADR-0002: EngineAdapter Adapter 패턴

- 목적: Claude Code/Codex/Gemini CLI 등 구현 엔진을 동일 계약으로 호출
- 결정: `EngineAdapter` 인터페이스를 도입해 엔진별 구현을 어댑터 뒤로 숨긴다
- 영향: Engine Runtime 계층(ADR-0016)의 기반이 됨

## ADR-0003: Approval Engine 분리 (상태: 제안)

- 목적: 승인 로직을 Workspace Core에서 분리할지 검토
- 결정: 별도 `ApprovalEngine`으로 분리(제안 상태로 기록)
- 영향: 이후 ApprovalPipeline 데코레이터 설계(ADR-0024 언급)의 초기 논의

## ADR-0004: 파일 기반 저장

- 목적: 초기 단계 저장소 구현 방식 결정
- 결정: DB 대신 파일 기반(JSON 등) Repository 구현체로 시작한다
- 영향: `storage/` 계층의 파일 기반 구현체 전반의 근거

## ADR-0005: Workspace Core 순수 오케스트레이터 + Interfaces 분리

- 목적: Workspace Core가 비즈니스 로직을 직접 갖지 않도록 경계 설정
- 결정: Workspace Core는 조율만 하고, 실제 계약은 `interfaces/`로 분리한다
- 영향: 이후 모든 계층이 Interface 우선 설계 원칙을 따르는 기반이 됨

## ADR-0006: Multi-Agent First 전환

- 목적: 단일 실행기 구조에서 멀티 에이전트 구조로 전환
- 결정: Multi-Agent 협업을 선택 기능이 아닌 기본 구조로 채택한다
- 영향: Agent Runtime(ADR-0010), Capability 중심 설계(ADR-0012)의 출발점

## ADR-0007: Event Bus 도입

- 목적: Agent/Engine/Workspace Core 사이 결합도를 낮춘다
- 결정: pub/sub 방식의 EventBus를 도입해 수평 결합을 이벤트로 대체한다
- 영향: Event Store(ADR-0014), Dashboard/Automation의 이벤트 구독 구조(M20/M21)의 기반

## ADR-0008: Conversation Layer (ADR-0013으로 대체됨)

- 목적: 대화형 인터페이스 계층 도입 검토
- 결정: Conversation Layer 도입(이후 Interaction Layer로 재정의됨)
- 영향: ADR-0013에서 "Interaction Layer"로 확장 대체됨(폐기 아님, 발전)

## ADR-0009: EngineAdapter 확장 실행 계약

- 목적: EngineAdapter의 실행 계약을 더 세분화
- 결정: 세션/실행 단위 계약을 EngineAdapter에 추가한다
- 영향: ADR-0015(세션 생명주기)로 추가 확장됨

## ADR-0010: Agent Runtime 계층 + WorkspaceSession

- 목적: Multi-Agent First(ADR-0006)를 실제 계층으로 구체화
- 결정: Agent Runtime(Registry/Scheduler/Manager/EventBus)과 WorkspaceSession을 도입
- 영향: 이후 모든 Agent 관련 기능이 이 계층 위에 구축됨

## ADR-0011: Mission→Workflow→Task→Step 4단 계층

- 목적: 작업 단위의 계층 구조 확립
- 결정: Mission-Workflow-Task-Step 4단 모델을 도메인 표준으로 채택
- 영향: 이후 모든 실행/자동화 도메인 모델의 기준 단위가 됨

## ADR-0012: Capability 중심 Agent, Memory/Automation은 Engine

- 목적: Agent와 Engine의 책임 경계 정리
- 결정: Agent는 Capability로 선택되고, Memory/Automation 등은 Engine으로 분리한다
- 영향: Agent Runtime과 Core Engines의 역할이 명확히 분리됨

## ADR-0013: Interaction Layer로 확장 (ADR-0008 대체)

- 목적: Conversation Layer(ADR-0008)를 더 넓은 개념으로 재정의
- 결정: Voice/Slack/REST 등 다양한 진입점을 포괄하는 Interaction Layer로 확장
- 영향: UI Surfaces(CLI/Web)와 Workspace Core 사이의 표준 진입 계층이 됨

## ADR-0014: Event Store 도입

- 목적: EventBus(ADR-0007)를 통과한 이벤트의 영속 기록 필요
- 결정: Event Store를 도입해 이벤트를 영속 저장한다
- 영향: ADR-0018에서 "독립 구독자" 위치로 보완됨

## ADR-0015: EngineAdapter 세션 생명주기 (ADR-0009 확장)

- 목적: EngineAdapter 세션의 시작/종료 생명주기 명세 필요
- 결정: 세션 생명주기 계약을 EngineAdapter 인터페이스에 추가
- 영향: Engine Runtime(ADR-0016) 구현체가 이 계약을 따름

## ADR-0016: Engine Runtime 계층

- 목적: EngineAdapter 위에 실행 관리 계층 필요
- 결정: EngineRuntime을 도입해 EngineAdapter 호출을 관리한다
- 영향: `run_parallel()` 책임 경계는 이후 ADR-0023에서 확정됨

## ADR-0017: Context Manager 도입

- 목적: Agent 실행에 필요한 컨텍스트 관리 분리
- 결정: ContextManager를 도입해 MemoryEngine과 역할을 분리한다
- 영향: Memory 계열 인터페이스(ADR-0020 T1-20)의 기반

## ADR-0018: Event Store 독립 Subscriber로 위치 조정 (ADR-0014 보완)

- 목적: Event Store가 특별한 전달 경로를 갖는 것처럼 보이는 오해 해소
- 결정: Event Store는 EventBus의 여러 구독자 중 하나일 뿐임을 명확히 한다
- 영향: Dashboard/Automation과 동일한 구독 방식이라는 원칙이 확립됨(M20/M21에서도 재사용)

## ADR-0019: Coordination Capability 추가

- 목적: Agent 간 조율을 위한 Capability 필요
- 결정: Coordination을 Capability 목록에 추가한다
- 영향: Agent Scheduler의 선택 기준이 확장됨

## ADR-0020: Task.workflow_id 선택 필드

- 목적: Task가 Workflow에 속하지 않는 경우도 지원해야 함
- 결정: `Task.workflow_id`를 필수가 아닌 선택 필드로 정의
- 영향: 독립 Task와 Workflow 소속 Task를 모두 같은 모델로 표현 가능해짐

## ADR-0021: Phase 계층 폐지, Milestone→Task 2단 전환

- 목적: 기존 Phase 단위 계획 방식의 비효율 해소
- 결정: Phase를 폐지하고 Milestone→Task 2단 구조로 개발 계획을 전환한다. Task는 "하나의 구현 목표 + 하나의 Commit + 하나의 구현 사이클"로 정의
- 영향: 이후 모든 개발이 Milestone/Task 체계로 진행됨(Task Driven Development의 시작점)

## ADR-0022: Task 분해 원칙 — "한 Task = 하나의 아키텍처 책임 경계"

- 목적: 서로 무관한 컴포넌트가 하나의 Task에 뭉치는 문제 해결
- 결정: Task 분해 기준을 `docs/ARCHITECTURE.md` §3의 컴포넌트 경계로 명문화. 서로 import하지 않는 컴포넌트는 별도 Task로 분리하고, "정의→구현→테스트"는 한 Task 안에서 완결한다
- 영향: T1-18을 T1-18~T1-21 4개로 재분해, 이후 모든 Task 설계의 표준 기준이 됨

## ADR-0023: `run_parallel()` 병렬 실행 책임 경계 확정 (AgentScheduler vs EngineRuntime)

- 목적: AgentScheduler와 EngineRuntime 양쪽에서 "병렬 실행"을 자신의 책임으로 서술해 경계가 불명확했던 문제 해결
- 결정: AgentScheduler는 "동시에 활동할 후보를 고르는" 선택 책임만 갖고, EngineRuntime의 `run_parallel()`이 실제 동시 실행(ThreadPoolExecutor)을 책임진다
- 영향: `ManagedEngineRuntime.run_parallel()`이 순차 반복에서 실제 동시 실행으로 재구현됨

## ADR-0024: v0.5.0 아키텍처 기준선(Baseline) 선언

- 목적: Milestone 1~4로 구조(16종 Interface 등)가 실제 구현으로 채워진 시점을 공식화
- 결정: `pyproject.toml` version을 0.1.0→0.5.0으로 상향. M5 이후는 기존 Interface·계층을 기본적으로 유지하고 새 기능은 그 위에 조립한다
- 영향: 이후 모든 Milestone Review에서 "새 Interface 추가 여부"를 확인하는 관행의 근거가 됨

## ADR-0025: ExecutionEnvironment를 EngineAdapter 하위 인터페이스로 도입

- 목적: 실행 환경(로컬/컨테이너 등) 추상화 필요
- 결정: `ExecutionEnvironment`를 EngineAdapter 하위 인터페이스로 도입
- 영향: 엔진 실행 환경이 EngineAdapter 계약과 분리되어 독립적으로 교체 가능해짐

## ADR-0026: EngineAdapter/EngineRuntime 계약에 model 파라미터 확장 (M14)

- 목적: 엔진 호출 시 모델을 지정할 수 있어야 함
- 결정: EngineAdapter/EngineRuntime 계약에 `model` 파라미터를 추가
- 영향: 이후 EngineSelectionPolicy(ADR-0029) 등 모델 선택 기능의 기반이 됨

## ADR-0027: EngineRuntime.estimate_cost() + BudgetPolicyEngine 신설 (M15)

- 목적: 실행 비용을 사전에 추정하고 예산을 통제할 필요
- 결정: `EngineRuntime.estimate_cost()`를 추가하고 `BudgetPolicyEngine`을 신설
- 영향: Budget/Cost 관리가 Core Domain의 정식 관심사로 편입됨

## ADR-0028: Project Knowledge System 도입 (M16, MemoryEngine과 분리)

- 목적: 프로젝트 지식(문서/결정 이력 등)을 MemoryEngine과 별도로 관리
- 결정: Project Knowledge System을 신설하고 MemoryEngine과 책임을 분리
- 영향: `KnowledgeRepository` 등 새 Interface 도입

## ADR-0029: Intelligent Engine Selection (EngineRegistry+EngineSelectionPolicy, M17)

- 목적: 여러 구현 엔진 중 적합한 엔진을 자동 선택할 필요
- 결정: `EngineRegistry`와 `EngineSelectionPolicy`를 도입해 지능적 엔진 선택을 구현
- 영향: ExecutionDispatcher(ADR-0030)가 이 선택 결과를 소비하는 구조로 이어짐

## ADR-0030: Execution Layer 도입 (ExecutionDispatcher+AuthenticationManager, M18)

- 목적: 엔진 선택 결과를 실제 실행으로 연결하는 단일 진입점 필요
- 결정: `ExecutionDispatcher`와 `AuthenticationManager`를 도입, 유일한 실행 진입점으로 확정
- 영향: Dashboard/Automation이 구독하는 이벤트(ENGINE_EXECUTION_STARTED 등)의 발행 주체가 됨

## ADR-0031: Reliability Layer 도입 (RetryPolicy 확장+RetryExecutor, M19)

- 목적: 실행 실패에 대한 재시도 정책 필요
- 결정: RetryPolicy를 확장하고 `RetryExecutor`를 도입(timed_out 판정은 휴리스틱, 기술 부채로 기록)
- 영향: ExecutionDispatcher 위에 재시도 계층이 추가됨

## ADR-0032: Real-time Dashboard Platform 도입 (M20)

- 목적: 시스템 상태를 실시간으로 조회할 Read Model 필요
- 결정: `DashboardRepository`를 도입(첫 외부 런타임 의존성 — FastAPI/uvicorn 채택)
- 영향: Core Domain과 독립된 Infrastructure 계층(Dashboard)이 처음 생김

## ADR-0033: Automation Engine 도입 (M21)

- 목적: 조건/일정에 따른 Task 자동 실행 필요
- 결정: `AutomationRepository`를 도입, 기존 M4-T07의 AutomationEngine과 다른 개념이므로 이름을 분리
- 영향: AutomationScheduler가 EventBus를 독립적으로 구독하는 두 번째 Infrastructure 계층이 됨

## ADR-0034: Production Platform 도입 (M22)

- 목적: 운영에 필요한 설정/생명주기/헬스체크 표준화
- 결정: `ProductionConfig`/`LifecycleManager`/`HealthMonitor`를 도입. DashboardService와의 순환 의존은 `TYPE_CHECKING`으로 해결, 조립 순서 문제는 `attach_health_monitor()`로 해결
- 영향: M23에서 재사용할 `uptime`/`started_at`/`version`/`health_status` 표준 필드가 확정됨

## ADR-0035: Vault Integration Layer 도입 (M23-T02)

- 목적: GitHub 원문 ↔ Vault 문서 동기화를 수작업 대신 표준 계층으로 자동화
- 결정: 신규 `vault/` 패키지(Path Map/Document Router/Markdown Generator/Vault Writer), Core Domain·`web/` 양쪽 모두 모르는 완전 독립 계층으로 설계(새 Interface 없음, 설계만·미구현)
- 영향: 상세 설계는 [[Vault Integration Architecture]], 실제 구현은 M23-T03(Vault Save Engine)부터

## ADR-0036: Real Obsidian Vault Integration 도입 (Milestone 24)

- 목적: `vault/`가 실제 Obsidian Vault에 안전하게 연결·저장하도록 Mock/tmp_path 의존을 제거
- 결정: `connection.py`(실제 Vault 탐색·연결 검증)/`filesystem.py`(Create/Read/Update/Delete/Exists/Rename/Move Adapter)/`atomic.py`(원자적 쓰기) 신규, Auto Save Validation을 Vault 전체 스캔에서 저장한 파일만 검사하는 Incremental 방식으로 전환
- 영향: `tests/vault/`(Mock, 38개) 무변경 유지 + `tests/integration/test_m24_real_vault_e2e.py`(신규, 5개)가 실제 Vault 대상으로 Connect/CRUD/Rename/Auto Save 왕복 검증. 상세는 [[Vault Integration Architecture]]

## ADR-0037: Obsidian Vault Root Refactoring (Milestone 26)

- 목적: Git Vault Sync/Obsidian Mobile·macOS가 요구하는 "Vault == Repository Root" 조건 충족
- 결정: `Vault/01 Projects/AI Workspace/`의 15개 디렉터리를 `git mv`로 저장소 root로 승격, PARA 뼈대(Inbox/Resources/Archives) 제거. `connection.py`는 표식 파일(`00 System/PROJECT_INDEX.md`) 기준으로 Vault Root를 찾도록 변경, `mapping.py`는 무변경(처음부터 상대 경로), `validation.py`/`sync.py`는 스캔 범위를 Vault 콘텐츠 15개 디렉터리로 제한
- 영향: Wikilink는 파일명 기준이라 전혀 깨지지 않음(마크다운 상대경로 링크는 Vault 안에 0건). 상세는 [[Vault Integration Architecture]]

## 관련 문서

- [[Architecture Overview]]
- [[Milestones Index]]
- [[Decisions Index]]

## 원문

- `.ai/DECISIONS.md`
