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

## ADR-0038: Obsidian Workspace Templates 도입 (Milestone 27, M25 요청)

- 목적: Task 생성 → 문서 생성 → 진행 관리 → 상태 변경이 Obsidian 안에서 이뤄지도록 Task 전용 Template/kind 도입
- 결정: `VaultDocumentKind.TASK` 신규(개별 Task 문서, `14 Tasks/{task_id}.md`), `render_task_file()`(Status/Priority/Milestone/Owner/Checklist/Notes/Related Documents/Decision + frontmatter), `render_daily_file()`에 진행중/완료 구분 추가, `AI_RULES` Tag/Frontmatter Rule 확장, Project Workspace Template은 설계만(단일 Project 유지, YAGNI)
- 영향: [[Template - Task]]/[[Template - Project Workspace]] 신규, [[Template - Daily]]/[[Template - Decision]] 갱신. 상세는 [[Vault Integration Architecture]]

## ADR-0039: Workspace Adapter Layer 도입 (Milestone 28-T03)

- 목적: Core Domain↔vault 직접 의존 없이 Task Lifecycle을 Workflow/Agent와 연결할 통로 마련
- 결정: 신규 최상위 패키지 `integration/`(Vault/Workflow/Agent Adapter 3종)을 "Adapter 3개"가 아니라 향후 Runtime/Service/Notification/Sync까지 확장 가능한 Workspace Adapter Layer로 정의. 공유 기반 클래스는 두지 않음(Speculative Generality 회피). Core Domain↔vault 직접 import 금지를 `ast` 기반 테스트로 강제
- 영향: `docs/ARCHITECTURE.md` §8 규칙 18 신설, §3 Workspace Adapter Layer 절 추가. 상세는 [[Architecture Overview]]

## ADR-0040: Integration Layer 내부 분류 — Adapter vs Connector (Milestone 28-T05)

- 목적: Integration Layer 안에서 "외부 시스템 연결"과 "여러 Adapter를 조합하는 오케스트레이션"을 명확히 구분
- 결정: Adapter(Vault/Workflow/Agent, 외부 시스템 1개만 연결) vs Connector(WorkflowTaskLink/WorkflowAgentLink, 여러 Adapter 조합, 유스케이스 1개만 책임). Connector끼리도 서로 참조하지 않음 — Agent 배정을 WorkflowTaskLink에 얹지 않고 별도 WorkflowAgentLink로 분리
- 영향: `integration/__init__.py`에 분류 명시, `docs/ARCHITECTURE.md` §3에 반영. 상세는 [[Architecture Overview]]

## ADR-0041: Conversation Layer 연동 — Conversation Connector 도입, Orchestrating Connector 개념 추가 (Milestone 28-T06)

- 목적: Conversation Layer가 Task/Workflow/Agent 요청을 처리할 유일한 진입점 마련, M28 마지막 Task
- 결정: `ConversationConnector`(Peer Connector `WorkflowTaskLink`/`WorkflowAgentLink` + `VaultAdapter` 조합)를 **Orchestrating Connector**로 도입 — ADR-0040 "Connector끼리 참조 금지" 원칙의 명시적 예외. Conversation Layer는 Vault/Core Domain Engine/AgentManager를 직접 참조하지 않고 이 Connector만 거침(`ast` 테스트로 강제). 새 비즈니스 로직·새 Domain 필드 없음
- 영향: `integration/conversation_workflow_link.py` 신규. **Milestone 28(Live Task Management & Integration) 전체 완료**, Architecture Freeze 예정. 상세는 [[Architecture Overview]]

## ADR-0042: M28 Architecture Freeze — Baseline 선언

- 목적: M28이 만든 구조(Layer/Integration Layer/Boundary/Domain/Public Interface/ADR 정합성)를 새 기능 없이 검증·확정
- 결정: Layer 구조·Integration Layer 구성(Adapter/Peer Connector/Orchestrating Connector)을 그대로 기준선으로 확정. 검증 중 Peer Connector 상호 참조 위반 1건 발견(`WorkflowAgentLink`→`WorkflowTaskLink`) 즉시 수정 — `WorkflowLink`를 신규 중립 모듈 `integration/models.py`로 이동. `docs/ARCHITECTURE.md` §8에 규칙 19/20 추가. 개선 후보 7건은 목록만 작성, 리팩토링하지 않음
- 영향: `tests/integration_layer/test_connector_layering.py` 신규(위반 검출 테스트), `pytest` 851개·ruff·mypy 전부 클린. **M29(Project Intelligence) 진행 가능 — 사용자 승인 완료(2026-07-30)**. 상세는 [[Architecture Overview]], 전문은 GitHub `.ai/TASKS.md`의 "Milestone 28 — Architecture Freeze" 절

## ADR-0043: Intelligence Layer 도입 — `intelligence/` 신규 최상위 패키지, Vault Task 문서를 Project 단위 조회의 단일 데이터 소스로 채택 (Milestone 29-T01)

- 목적: Project Snapshot/Health/Risk/Recommendation을 만들 Read Only Query Layer의 데이터 소스와 위치를 결정, 신규 Interface 필요 여부 판단
- 결정: Core Domain 27종 Interface에는 project 단위 전체 목록 조회가 없어 새 Interface 없이는 Snapshot이 불가능함을 확인. 대신 **Vault Task 문서(`14 Tasks/*.md`)를 단일 데이터 소스**로 채택(새 Interface 미추가, 27종 유지) — `vault/task_query.py`(신규)→`VaultAdapter.list_tasks()`(신규 메서드)로 노출. Agent 데이터는 기존 `AgentAdapter.list_active_agents()` 재사용. Event는 제외(YAGNI). "Blocked Task"는 Vault에 대응 상태가 없어 "IN_PROGRESS/REVIEW + `updated` 임계일 초과" Rule로 근사. 신규 최상위 패키지 `intelligence/`를 만들고 `integration/`의 Adapter에만 의존하게 제한(§8 규칙 21 신설)
- 영향: `docs/ARCHITECTURE.md` §3.22(신규)/§8 규칙 21 추가, `.ai/TASKS.md` Milestone 29 절 신규. 코드 변경 없음(설계 Task, 구현은 M29-T02부터). 상세는 [[Architecture Overview]]

## ADR-0044: Context Intelligence 설계 — `KnowledgeAdapter` 신규(Integration Layer), Markdown 제목 단위 파싱으로 `ProjectContext` 구성 (Milestone 30-T01)

- 목적: 지금 하는 작업(Task/Milestone)과 관련된 맥락을 기존 Knowledge Layer(M16)/Intelligence Layer(M29) 정보로 모아 정리할 방법과 위치를 결정, 신규 Interface 필요 여부 판단
- 결정: `KnowledgeRepository`/`KnowledgeSearch`(M16, 기존 27종 Interface 중 2종)만 재사용하고 새 Interface는 추가하지 않는다. 신규 Integration Layer Adapter `KnowledgeAdapter`가 이 두 Interface만 감싸고, `intelligence/context.py`의 `ContextAnalyzer`가 반환된 문서 텍스트를 Markdown 제목 단위로 쪼개 subject(Task/Milestone 식별자)가 언급된 항목만 채택한다(이 저장소의 실제 제목 작성 관례 활용, 새 지식 생성 없음). Freshness는 파일 mtime/git log 대신 제목에서 추출한 Milestone 번호 거리로 판단(mtime은 fresh clone 환경이라 무의미, git log는 Adapter "외부 시스템 하나만" 원칙과 충돌). Gap은 ADR/TASK/ARCHITECTURE 3종에서 subject 언급 0건일 때만 판정
- 영향: `docs/ARCHITECTURE.md` §3.23(신규) 갱신, `.ai/TASKS.md` Milestone 30 절 신규. 코드 변경 없음(설계 Task, 구현은 M30-T02부터). 상세는 [[Architecture Overview]]

## ADR-0045: Capability Intelligence 설계 — `AgentAdapter` 확장(신규 Adapter 아님), "정의된 Capability 대비 활성 Agent 커버리지"로 Gap 판정 (Milestone 31-T01~T05)

- 목적: 정의된 `AgentCapability`(11종) 대비 실제 활성 Agent가 커버하는 Capability를 정리할 방법과 위치를 결정, 신규 Adapter/Interface 필요 여부 판단
- 결정: 새 Adapter를 만들지 않고 기존 `AgentAdapter`(M28)를 확장한다 — `list_active_agent_capabilities()`(활성 Agent를 Adapter 전용 DTO로 열거)/`known_capabilities()`(정의된 Capability 카탈로그 노출) 두 메서드만 추가(새 Core Domain Interface 아님, 27종 유지). `intelligence/capability.py`(Snapshot 집계)→`intelligence/capability_gap.py`(Coverage/Gap 판단, Snapshot만 입력)의 2단 Analyzer로 M29/M30과 동일한 구조를 따른다. Coverage 등급은 healthy/warning/critical이 아니라 none/partial/full을 쓴다 — 활성 Agent 0명은 이 저장소가 아직 Agent 프로세스를 상시 구동하지 않는 워크숍 단계의 자연스러운 상태이지 시스템 이상이 아니기 때문. Vault Task `owner`(자유 텍스트)는 Capability 수요 신호로 매핑하지 않는다(고정 명명 규칙 없음, 새 관례 발명 금지)
- 영향: `docs/ARCHITECTURE.md` §3.24(신규) 갱신, `.ai/TASKS.md` Milestone 31 절 신규. `integration/agent_adapter.py`(확장)/`intelligence/capability*.py`(신규)/`vault/capability_report.py`(신규)/`VaultAdapter.publish_capability_report()`(신규) 구현 완료, `pytest` 947개·ruff·mypy 전부 클린. 새 Core Domain Interface 없음(27종 유지). 상세는 [[Architecture Overview]]

## ADR-0046: Intelligence Synthesis 도입 — 새 Analyzer/Adapter 없이 M29~M31 Service 3개를 조합해 `IntelligenceOverview` 생성 (Milestone 32-T01~T04)

- 목적: M29/M30/M31이 각각 만든 리포트를 교차로 보려면 파일 3개를 열어야 하는 문제 해결
- 결정: 새 Adapter/Interface 없이 `intelligence/synthesis.py`(Analyzer)/`synthesis_service.py`(조합)가 기존 3개 Service의 `generate()` 결과만 합성. §8 규칙 21은 변경 없이 그대로 적용(Adapter가 아니라 같은 계층의 Service를 조합하므로 애초에 금지 대상 아님)
- 영향: `docs/ARCHITECTURE.md` §3.25(신규) 갱신, `.ai/TASKS.md` Milestone 32 절 신규. `integration/vault_adapter.py`(확장 1건)/`intelligence/synthesis*.py`(신규)/`vault/intelligence_overview.py`(신규) 구현 완료, `pytest` 954개·ruff·mypy 전부 클린. 새 Core Domain Interface 없음(27종 유지). 상세는 [[Architecture Overview]]

## ADR-0047: Session Resume 도입 — Current Work Selector 1개 + M29~M32 재사용으로 세션 시작 시 자동 복원 문서 생성 (Milestone 33-T01~T04)

- 목적: 세션을 새로 시작할 때 "지금 무엇을 하고 있었는가"를 알려면 리포트 3~4개를 직접 열어야 하는 문제 해결
- 결정: 새 Adapter/Interface 없이 `intelligence/session_resume.py`(Current Work Selector)/`session_resume_service.py`(조합)가 `VaultAdapter.list_tasks()` + M29~M31 Service 3개 + M32 `IntelligenceSynthesisAnalyzer`만 재사용. "현재 작업" 판정은 이미 있는 status/updated 값을 고르는 Rule 1개뿐, 새 지표 없음. M8 세션 연속성(Agent 실행 컨텍스트 복원)과는 별개 계층
- 영향: `docs/ARCHITECTURE.md` §3.26(신규) 갱신, `.ai/TASKS.md` Milestone 33 절 신규. `integration/vault_adapter.py`(확장 1건)/`intelligence/session_resume*.py`(신규)/`vault/session_resume.py`(신규) 구현 완료, `pytest` 962개·ruff·mypy 전부 클린. 새 Core Domain Interface 없음(27종 유지). 상세는 [[Architecture Overview]]

## ADR-0048: Workflow Intelligence 도입 — "Workflow" = Milestone Task 실행 흐름(domain.Workflow 아님), Blocked Rule 1개 + WorkflowFlowAnalyzer 캡슐화 (Milestone 34-T01~T04)

- 목적: `domain.Workflow`가 영속 저장소 없는 휘발성 값 객체라 조회할 데이터가 없는 상황에서, "Workflow Intelligence"가 실제로 무엇을 분석할지 정의
- 결정: "Workflow"를 `domain.Workflow`가 아니라 Milestone 안의 Task 실행 순서로 재정의. Blocked = Task ID T-번호 순으로 정렬했을 때 선행 Task 중 미완료가 있는 `todo` Task, 선행이 모두 완료된 `todo`는 Next. 판정 규칙은 `intelligence/workflow_flow.py`의 `WorkflowFlowAnalyzer`(순수 Analyzer)에 전부 캡슐화하고, `workflow_service.py`의 `WorkflowIntelligenceService`는 `VaultAdapter` 조회 + Analyzer 실행 조합만 담당(사용자 3가지 권고 반영). 새 Adapter/Interface 없이 `VaultAdapter` 확장 1건만 추가
- 영향: `docs/ARCHITECTURE.md` §3.27(신규) 갱신, `.ai/TASKS.md` Milestone 34 절 신규. `integration/vault_adapter.py`(확장 1건)/`intelligence/workflow_flow.py`(신규)/`intelligence/workflow_service.py`(신규)/`vault/workflow_intelligence.py`(신규) 구현 완료, `pytest` 976개·ruff·mypy 전부 클린. 새 Core Domain Interface 없음(27종 유지), `domain.Workflow`/`WorkflowEngine`/`WorkflowAdapter` 무변경(사용하지 않음). 상세는 [[Architecture Overview]]

## ADR-0049: Recommendation Intelligence 도입 — 5단계 Priority Rule 1개로 M29~M34 Intelligence를 그대로 소비하는 Decision Layer (Milestone 35-T01~T04)

- 목적: M29 Recommendation이 Project Snapshot/Health/Risk만 보고 Session Resume(현재 작업)이나 Workflow Intelligence(Blocked/Next)는 고려하지 않아, "지금 무엇을 하는 것이 가장 적절한가"에 답하는 단일 창구가 없는 문제 해결
- 결정: 새 Intelligence를 계산하지 않고, M29 `ProjectRecommendation`/M31 `CapabilityGapReport`/M33 `CurrentWorkSelector`(Analyzer만 재사용)/M34 `WorkflowFlowAnalyzer`(Analyzer만 재사용)를 입력으로 5단계 Priority Rule(Current Work→Workflow Next→Workflow Blocked→Capability Gap→Project Recommendation) 1개로 단일 `NextAction`을 고른다. 판정 로직은 `intelligence/recommendation_rules.py`의 `RecommendationRuleAnalyzer`(순수 Analyzer)에 캡슐화하고 `recommendation_service.py`의 `RecommendationIntelligenceService`는 조합만 담당. 자동 실행하지 않는다(Automation은 M36 이후)
- 영향: `docs/ARCHITECTURE.md` §3.28(신규) 갱신, `.ai/TASKS.md` Milestone 35 절 신규. `integration/vault_adapter.py`(확장 1건)/`intelligence/recommendation_rules.py`(신규)/`intelligence/recommendation_service.py`(신규)/`vault/recommendation_intelligence.py`(신규) 구현 완료, `pytest` 988개·ruff·mypy 전부 클린. 새 Core Domain Interface 없음(27종 유지). 상세는 [[Architecture Overview]]

## ADR-0050: Execution 도입 — next_task Recommendation만, 수동 트리거로만, 새 실행 경로 없이 기존 ExecutionDispatcher/EngineRegistry/EngineSelectionPolicy 재사용 (Milestone 36-T01~T04)

- 목적: M35 NextAction은 추천만 하고 실행하지 않아, 이미 존재하는 ExecutionDispatcher(M18)/AutomationActionExecutor(M21) 파이프라인과 연결되지 않는 문제 해결 — M29~M35와 달리 실제 부작용(AI Engine 실행)을 일으키는 첫 Milestone이라 범위를 최소로 좁힘
- 결정: NextAction의 5가지 source 중 next_task만 실행 대상(나머지는 "지원하지 않음(Not Supported)"), 자동 트리거 없이 manual_trigger=True 수동 호출로만 실행. `runtime/execution/recommendation_execution_gate.py`의 `ExecutionGate`(판정만)와 `recommendation_action_builder.py`의 `ActionBuilder`(변환만)로 책임 분리. `AutomationActionExecutor`를 감싸지 않고 그 내부와 동일한 `EngineRegistry`→`EngineSelectionPolicy`→`ExecutionDispatcher` 3단계를 `recommendation_execution_service.py`가 직접 재사용(반환값을 버리지 않기 위함). Task 상태 자동 전이 없음 — 실행 결과만 Vault에 보고
- 영향: `docs/ARCHITECTURE.md` §3.29(신규) 갱신, `.ai/TASKS.md` Milestone 36 절 신규. `integration/vault_adapter.py`(확장 1건)/`runtime/execution/recommendation_execution_gate.py`(신규)/`recommendation_action_builder.py`(신규)/`recommendation_execution_service.py`(신규)/`vault/recommendation_execution.py`(신규) 구현 완료, `pytest` 998개·ruff·mypy 전부 클린. 새 Core Domain Interface 없음(27종 유지), `AutomationActionExecutor`/`AutomationScheduler`/`ExecutionDispatcher` 무변경. 상세는 [[Architecture Overview]]

## ADR-0051: Task Lifecycle 도입 — M36 Execution 결과를 기존 Task 상태 전이 기계(_ALLOWED_TRANSITIONS)에 연결, 새 상태·새 전이 규칙 없음 (Milestone 37-T01~T04)

- 목적: M36 ADR-0050 결정 5가 미뤄 둔 "Task 상태 자동 전이"를 이미 존재하는 검증된 상태 전이 기계(`_ALLOWED_TRANSITIONS`, M28)로 구현
- 결정: 실행 시작 시 `todo→in-progress`, 성공 시 `in-progress→review`, 실패 시 `in-progress→todo`만 자동화(`review→done`은 사람 검토로 남김). `runtime/execution/recommendation_task_lifecycle.py`의 `TaskLifecycleTransitioner`는 현재 상태를 먼저 확인하고 예상과 다르면 전이하지 않는다(방어적, 사용자 권고). Presentation을 `_render_execution_section()`/`_render_lifecycle_section()`으로 분리(사용자 권고). `VaultAdapter` 확장 없이 기존 `transition_task()` 그대로 재사용
- 영향: `docs/ARCHITECTURE.md` §3.30(신규) 갱신, `.ai/TASKS.md` Milestone 37 절 신규. `runtime/execution/recommendation_task_lifecycle.py`(신규)/`recommendation_execution_service.py`(확장) 구현 완료, `pytest` 1005개·ruff·mypy 전부 클린. 새 Core Domain Interface/Adapter 없음(27종 유지), `_ALLOWED_TRANSITIONS` 무변경. 상세는 [[Architecture Overview]]

## ADR-0052: AutomationScheduler 연결 — M21~M37 Composition Root 실배선, 새 정책 없음, source=next_task만 그대로 유지 (Milestone 38)

- 목적: M37 완료 시 "M38 이후"로 미룬 6개 항목 중 `AutomationScheduler` 연결을 처리. M29~M37이 만든 `VaultAdapter`/`AgentAdapter`/`RecommendationIntelligenceService`/`RecommendationExecutionService`가 `tests/`에서만 조립되고 실제 서버(`web/server.py`의 `build_app()`)에는 한 번도 배선된 적이 없었던 "워크숍 단계" 한계(M37 완료 노트)를 해소해, `AutomationScheduler`의 주기 Trigger(TIME/INTERVAL)로 M35 Recommendation이 실제로 실행되게 한다
- 결정: 새 실행 정책/Gate 변경 없음 — `ExecutionGate`는 M36과 동일하게 `source=next_task`만 승인하고 나머지 4개 source는 계속 Not Supported로 남는다. `domain.automation.ActionKind`에 `RUN_RECOMMENDATION`(추가 필드 없음) 1개만 신설하고, `AutomationActionExecutor`에 선택적 `recommendation_execution_service` 의존성을 주입받아 발동 시 `RecommendationExecutionService.publish(manual_trigger=True)`를 호출한다 — `manual_trigger=True`는 사용자가 Rule을 명시적으로 만들고 활성화했다는 사실 자체를 수동 승인으로 간주한 것이며(ExecutionGate가 막으려는 "실수로 자동 승인" 상황이 아님), Gate 내부 판정 로직은 손대지 않는다. `web/server.py`의 `build_app()`에 `VaultAdapter`/`AgentAdapter`(`InMemoryAgentManager`/`InMemoryAgentRegistry`/`InMemoryAgentScheduler`)/`RecommendationIntelligenceService`/`RecommendationExecutionService`를 `tests/runtime/execution/test_recommendation_execution_service.py`와 동일한 생성자 조합으로 최초 조립(Composition Root 배선만, 새 클래스 없음). `ProductionConfig`에 `vault_root`(기본값 `"."`, ADR-0037 "Vault == Repository Root") 필드 1개만 추가하고 `AI_WORKSPACE_VAULT_ROOT` Env Var로 오버라이드 가능하게 한다
- 영향: `docs/ARCHITECTURE.md` §3.31(신규) 갱신, `.ai/TASKS.md` Milestone 38 절 신규. `domain/automation.py`(확장 1건)/`runtime/automation/automation_action_executor.py`(확장 1건)/`runtime/production/config.py`·`config_loader.py`(확장 1건)/`web/server.py`(Composition Root 배선) 구현 완료, `pytest` 1010개·ruff·mypy 전부 클린. 새 Core Domain Interface/Adapter 없음(27종 유지), `ExecutionGate`/`ActionBuilder`/`TaskLifecycleTransitioner` 무변경. `done→archived` 자동화·재시도 정책·`review→done` 자동화·CLI·Hook은 계속 범위 밖(YAGNI, 다음 Milestone 이후 논의). 상세는 [[Architecture Overview]]

## ADR-0053: Execution Memory 도입 — Execution 결과를 기존 MemoryEngine에 저장만, 조회 API 제공, Learning 없음 (Milestone 39)

- 목적: M38 Review가 M39 이후로 미룬 세 Engine(Memory Engine/Architecture Guardian/Learning Engine) 중 Memory Engine을 착수 — M36~M38(Execution Platform)이 실제 부작용을 일으키기 시작했음에도 그 결과를 아무도 기억하지 않는 공백을 해소
- 결정: 새 Interface 없이 기존 `MemoryEngine`(M1, remember/recall/search)을 그대로 재사용. `ExecutionMemory`(신규 dataclass — task_id/action/result/timestamp/reason 5개만, embedding·score·vector·confidence 금지)를 `ExecutionMemoryStore`(신규, `MemoryEngine`을 감싸는 얇은 Service)가 JSON 직렬화해 저장/조회. `RecommendationExecutionService`에 `execution_memory_store` 선택적 의존성을 추가해 실행 결과를 자동 기록(미주입 시 M38 이전과 동일). 영속화(Vault 파일 등)는 `MemoryEngine`(M1 기초 계약) 구현체가 `vault/`(M28+ Layer)에 하향 결합되는 문제를 발견해 범위에서 제외 — `InMemoryMemoryEngine`만 사용. `RecommendationRuleAnalyzer` 반영(Learning)은 M40 이후로 명시적으로 이관(사용자 조건부 승인)
- 영향: `docs/ARCHITECTURE.md` §3.8/§8 규칙 22(신규)/§2.1 갱신, `.ai/TASKS.md` Milestone 39 절 신규. `domain/execution_memory.py`(신규)/`memory/execution_memory_store.py`(신규)/`runtime/execution/recommendation_execution_service.py`(확장)/`web/server.py`·`web/app.py`(Composition Root 배선) 구현 완료, `pytest` 1021개·ruff·mypy(194 source files) 전부 클린. 새 Core Domain Interface/Adapter 없음(27종 유지), `MemoryEngine`/`ExecutionGate`/`ActionBuilder`/`TaskLifecycleTransitioner` 무변경. 영속화·Learning·REST 엔드포인트는 계속 범위 밖(YAGNI, M40 이후 논의). 상세는 [[Architecture Overview]]

## ADR-0054: Domain Vocabulary & Naming Convention 확립 — Milestone 이름은 "{Domain} {Responsibility}", 신규 용어보다 재사용 우선 (Pre-M40)

- 목적: M1~M39를 거치며 Intelligence/Memory/Engine/Guardian/Resume/Lifecycle 등의 용어가 각 시점 필요에 따라 독립적으로 도입돼 어휘가 발산. M40 착수 전 이름을 짓는 규칙 자체를 먼저 확립
- 결정: `docs/ARCHITECTURE.md` 신규 §13에서 Intelligence/Memory/Execution/Guardian을 1급 Domain 어휘로, Engine/Lifecycle/Resume/Scheduler/Recommendation/Automation을 보조 어휘로 정의. Milestone 이름은 `{Domain} {Responsibility}` 형식만 사용(예: Project Intelligence, Execution Memory). `Knowledge`/`Insight`/`Learning`/`Analyzer`/`Manager` 등 기존 어휘와 겹치는 동의어 신설 금지. 신규 §14에서 Obsidian Graph Cluster를 폴더가 아니라 Domain 기준(🔵Intelligence/🟢Execution/🟡Memory/🟣Architecture/🔴Domain/🟠Documentation)으로 재정의하고 Linking Rules 명문화. `.ai/RULES.md` 신규 §1.5(Vocabulary Reuse First)로 영구 규칙화. 이번 작업은 문서화 전용 — 기존 Milestone/클래스/파일명 변경 없음, Vault Tag 일괄 추가·`.obsidian/graph.json` 설정은 별도 후속 작업으로 이관
- 영향: `docs/ARCHITECTURE.md` §13/§14(신규) 추가, `.ai/RULES.md` §1.5(신규, v0.9.0) 추가. 코드 변경 없음(`pytest` 1021개 그대로 유지). **T01 적용 완료**(2026-07-30): `.obsidian/graph.json` 신규 — 새 Frontmatter Tag 없이 기존 Tag/경로만으로 6개 Cluster를 상호 배타적으로 분류(41개 문서 시뮬레이션 검증). 상세는 [[Architecture Overview]]

## 관련 문서

- [[Architecture Overview]]
- [[Milestones Index]]
- [[Decisions Index]]

## 원문

- `.ai/DECISIONS.md`
