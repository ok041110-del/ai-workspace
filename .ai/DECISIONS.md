# DECISIONS — Architecture Decision Record (ADR)

이 문서는 AI Workspace 프로젝트의 주요 설계 결정을 기록한다. 각 ADR은 결정
내용뿐 아니라 **배경, 대안, 이유, 결과**를 함께 남겨 이후 재검토가 가능하도록 한다.

시스템 아키텍처가 아니라 **AI 세션 운영 절차(DX 트랙)**에 대한 결정은 ADR
번호를 소비하지 않고 `## DX-01: 제목` 형식(형식은 ADR과 동일)으로 이 문서에
함께 기록한다 — ADR 번호 체계는 실제 아키텍처 결정만을 위해 순번을 유지한다.

형식은 다음을 따른다.

```
## ADR-000X: 제목
- 상태: 제안 / 승인됨 / 반려됨 / 폐기됨
- 날짜: YYYY-MM-DD
- 배경: 왜 이 결정이 필요했는가
- 결정: 무엇을 결정했는가
- 대안: 검토했던 다른 선택지와 그 장단점
- 이유: 왜 이 대안을 선택했는가
- 결과/영향: 이 결정이 프로젝트에 미치는 영향
```

---

## ADR-0001: 문서 구조를 README / docs / .ai 3계층으로 구성

- 상태: 승인됨 (2026-07-23, Phase 0 완료 승인)
- 날짜: 2026-07-23
- 배경: AI Workspace는 "문서 우선" 원칙을 따르며, 사람과 AI 구현 엔진이 모두
  읽을 수 있는 일관된 문서 체계가 필요했다.
- 결정: 문서를 세 계층으로 분리한다.
  - `README.md`: 프로젝트 소개 및 진입점
  - `docs/`: 사람 중심의 제품/구조/계획 문서 (PRD, ARCHITECTURE, ROADMAP)
  - `.ai/`: AI 구현 엔진이 작업 시 참조하는 운영 문서 (RULES, TASKS, MEMORY,
    DECISIONS)
- 대안:
  - 단일 `docs/` 폴더에 모두 모아두는 방식 — 단순하지만 "사람을 위한 설명 문서"와
    "AI가 매 세션 참조해야 하는 운영 문서"의 성격이 섞여 관리가 어려움.
  - 각 컴포넌트별로 별도 하위 문서 폴더를 만드는 방식 — 초기 단계에는 과도한
    세분화로 판단.
- 이유: 문서의 "독자"와 "갱신 빈도"가 다르다. `docs/`는 상대적으로 안정적인 제품
  정의, `.ai/`는 작업할 때마다 갱신되는 살아있는 문서다. 이를 분리하면 AI 구현
  엔진이 매 세션 시작 시 `.ai/`만 우선 참조해도 충분하도록 만들 수 있다.
- 결과/영향: 이후 모든 Task는 `.ai/TASKS.md`를 갱신하고, 아키텍처/요구사항
  변경은 `docs/`를 갱신하는 것으로 책임이 명확히 나뉜다.

## ADR-0002: 구현 엔진을 Adapter 패턴으로 추상화

- 상태: 승인됨 (2026-07-25, T1-27에서 ADR-0009·ADR-0015의 세션 생명주기
  계약 확장을 포함해 재확정)
- 날짜: 2026-07-23 (확정: 2026-07-25)
- 배경: Claude Code, Codex, Gemini CLI는 호출 방식과 능력이 서로 다르다. 이를
  Orchestration Layer가 직접 알게 하면 엔진 추가/교체 시마다 핵심 로직을 수정해야
  한다.
- 결정: 모든 구현 엔진은 공통 `EngineAdapter` 인터페이스를 구현하고,
  Orchestration Layer(Engine Runtime)는 이 인터페이스에만 의존한다. 최초
  제안된 `run_task()` 단일 메서드는 ADR-0009(확장 실행 계약)와 ADR-0015
  (세션 생명주기)를 거쳐 다음 최종 계약으로 확정되었다: `create_session()`,
  `run(...)`, `cancel(...)`, `status(...)`, `destroy_session()`,
  `capabilities()`, `supports_parallel()`, `estimate_cost(...)`(T1-19에서
  `src/ai_workspace/interfaces/engine_adapter.py`로 구현).
- 대안:
  - 엔진별로 별도 파이프라인을 만드는 방식 — 초기 구현은 빠르지만 엔진이
    늘어날수록 중복과 불일치가 커짐 (기각).
  - 엔진 호출을 설정 파일 기반 스크립트로 느슨하게 연결하는 방식 — 유연하지만
    타입 안전성과 테스트 용이성이 떨어짐 (기각).
- 이유: Open-Closed Principle을 따라, 신규 엔진 추가가 기존 코드 변경 없이
  Adapter 하나를 새로 작성하는 것만으로 가능하도록 하기 위함.
- 결과/영향: Milestone 3에서 `EngineAdapter` 계약의 구체 구현체(Claude Code
  어댑터를 1차 구현체로)를 작성한다. 계약 자체는 T1-19에서 이미 확정·구현
  완료됨(Fake 기반 계약 테스트 포함).

## ADR-0003: 승인 절차를 별도 Approval Engine 컴포넌트로 분리

- 상태: 제안 (Phase 2 착수 시 재확인 및 확정 예정)
- 날짜: 2026-07-23
- 배경: 아키텍처 변경, 신규 기능, 리팩토링, Phase 완료는 반드시 사용자 승인을
  거쳐야 한다는 요구사항이 있다. 이를 Workflow 로직 곳곳에 조건문으로 흩어 넣으면
  우회 경로가 생기기 쉽고 정책 변경 시 여러 곳을 고쳐야 한다.
- 결정: 승인이 필요한 행위 유형을 열거형으로 정의하고, 모든 승인 판단과 대기
  상태 관리를 단일 컴포넌트인 Approval Engine에 위임한다.
- 대안:
  - Workflow Engine 내부에 승인 체크 로직을 인라인으로 작성 — 구현은 빠르지만
    누락/우회 위험이 크고 감사(audit)가 어려움 (기각).
- 이유: 승인은 시스템의 "안전 장치"에 해당하므로, 단일 지점에서 강제되어야
  누락 없이 일관되게 적용된다.
- 결과/영향: Phase 2에서 Approval Engine을 구현하며, 승인/반려 이력은
  `.ai/DECISIONS.md`와 연동해 기록한다.

## ADR-0004: Phase 1 저장 방식은 파일 기반(Markdown/JSON)으로 시작

- 상태: 승인됨 (2026-07-25, T1-27에서 확정)
- 날짜: 2026-07-23 (확정: 2026-07-25)
- 배경: 데이터베이스 도입은 초기 단계에서 불필요한 복잡도를 추가할 수 있다
  (YAGNI). 동시에 문서 우선 철학상, 저장된 데이터도 사람이 직접 읽을 수 있으면
  유리하다.
- 결정: Phase 1에서는 프로젝트/Task 데이터를 파일 기반(Markdown 및/또는 JSON)으로
  저장한다.
- 대안:
  - SQLite 등 경량 DB 도입 — 쿼리와 동시성 처리에 유리하지만 Phase 1 범위(단일
    사용자, 소규모 데이터)에는 과함 (기각, Phase 5에서 재검토 예정).
- 이유: 초기 단계의 단순성과 "사람이 직접 확인 가능한 저장 형식"이라는 문서
  우선 철학에 부합한다.
- 결과/영향: T1-23에서 `FileProjectRepository`/`FileAgentRepository`/
  `FileEventStore`로 구현되며 실제로는 **JSON만** 채택되었다(Markdown은
  쓰이지 않음 — Enum/frozenset 등 구조화된 도메인 값을 다루기에 JSON이 더
  적합했기 때문). Milestone 4에서 다중 프로젝트/장기 메모리 고도화 시 DB
  전환 필요성을 재검토하며, 그 경우 별도 ADR을 작성한다.

## ADR-0005: Workspace Core를 순수 오케스트레이터로 한정하고 Interfaces 계층을 명시적으로 분리

- 상태: 승인됨 (2026-07-23, Phase 1 진행 중 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: 기존 설계(v0.2.0)는 Workspace Core가 "프로젝트 등록/조회/보관"과 "다중
  프로젝트 관리"까지 직접 포함하고, Core Engine을 구체적으로 호출하는 형태였다.
  이 경우 Workspace Core가 점점 비대해지고, 실제 Workflow/Task/Memory/Approval/
  Automation 처리 로직과 뒤섞일 위험이 있었다. 또한 Phase별로 구현 순서가
  다른 컴포넌트(Engine은 Phase 2, Adapter는 Phase 3)를 Workspace Core가 조기에
  구체적으로 알게 되면, Phase 1 시점에 존재하지 않는 구현체 때문에 설계가
  막히는 문제가 있었다.
- 결정:
  1. Workspace Core의 책임을 **프로젝트 로드, 설정 로드, 서비스 초기화, Engine
     등록 및 관리, Task 실행 요청, 애플리케이션 종료** 6가지로 한정한다.
     Workflow/Task/Memory/Approval/Automation 처리, 구현 엔진 직접 호출, 파일
     저장 세부 구현은 Workspace Core에 포함하지 않는다.
  2. Workspace Core와 그 협력 대상 사이에 **Interfaces(추상 계약)** 계층을
     명시적으로 둔다: `ProjectRepository`, `WorkflowEngine`, `TaskEngine`,
     `MemoryEngine`, `ApprovalEngine`, `AutomationEngine`, `EngineAdapter`.
  3. Phase 1에서는 이 7개 Interface **정의만** 하고, `ProjectRepository`의
     구체 구현체(`FileProjectRepository`)만 함께 구현한다. 나머지 5개 Engine의
     구체 구현체는 Phase 2, `EngineAdapter`의 구체 구현체(Claude Code/Codex/
     Gemini CLI)는 Phase 3에서 구현한다.
- 대안:
  - Workspace Core가 각 Engine의 로직을 직접 포함하는 방식 — 초기 구현은
    간단하지만 책임이 섞이고, Phase별로 순차 구현하기 어려움 (기각).
  - Interfaces 없이 구체 클래스에 바로 의존하는 방식 — 인터페이스 계층 설계
    비용은 없지만, 구체 구현체가 아직 없는 Phase 1 시점에 Workspace Core를
    완성할 수 없고, 이후 구현체 교체 시 Workspace Core 수정이 불가피함 (기각).
- 이유: Interfaces를 먼저 정의하면 Workspace Core를 Phase 1에서 완성할 수
  있고(구체 구현체는 아직 없어도 됨), 각 Engine/Adapter를 이후 Phase에서 독립적으로
  구현·테스트할 수 있다. 이는 ADR-0002(Adapter 패턴)의 정신을 Engine
  전반으로 확장한 것이다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.3.0에 반영됨. Phase 1 Task 목록
  (`.ai/TASKS.md`)이 "도메인 모델 → Interfaces 정의 → Workspace Core 골격 →
  ProjectRepository 구현 → CLI → 테스트" 순서로 재구성됨.
- 후속: ADR-0006에서 Workspace Core의 책임이 "Engine 오케스트레이터"에서
  "Agent 최상위 오케스트레이터"로 재정의된다. 다만 "Interfaces에만 의존하는
  순수 오케스트레이터"라는 본 ADR의 핵심 원칙은 그대로 유지된다.

## ADR-0006: Multi-Agent First 아키텍처로 전환 (Workspace Core 재정의 · Agent Manager · Agent 도메인)

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: 프로젝트 방향이 "필요 시 다중 에이전트를 사용할 수 있는 Workspace"에서
  **"상시 멀티 에이전트(Multi-Agent First) Workspace"**로 변경되었다. 멀티
  에이전트가 선택 기능이 아니라 시스템의 기본 구조가 되어야 하므로, Engine
  오케스트레이션만 전제한 기존 구조(v0.3.0)로는 부적합하다. 구현을 더 진행하기
  전에 아키텍처를 먼저 이 방향에 맞게 바꾸는 것이 재작업 비용을 최소화한다.
- 결정:
  1. **Workspace Core를 Agent 최상위 오케스트레이터로 재정의한다.** 책임:
     프로젝트 로드 / 설정 로드 / 서비스 초기화 / Agent 등록 및 관리 / Workflow
     시작 / Task 분배 / Engine 선택 및 위임 / 종료. **Task를 직접 실행하지 않고
     Agent에게 위임한다.**
  2. Workspace Core 아래에 **Agent Manager**를 추가한다. 책임: Agent 생성 /
     생명주기 관리 / 선택 / 협업 / 상태 관리.
  3. **Agent 도메인을 추가한다**: `Agent`, `AgentRole`(PLANNER/CODING/REVIEW/
     RESEARCH/MEMORY/AUTOMATION), `AgentStatus`. Agent는 Workspace의 핵심
     도메인 모델이 된다.
  4. **Workflow를 협업 흐름으로 재정의한다**: Task 생성 → Agent 할당 → Agent 간
     협업 → 결과 통합.
  5. Interfaces에 `AgentManager`, `AgentRepository`를 추가한다.
- 대안:
  - 멀티 에이전트를 계속 선택 기능으로 두는 방식 — 초기에는 단순하지만, 방향과
    어긋나고 나중에 핵심 구조를 대수술해야 함 (기각).
  - Agent 없이 Engine을 직접 다중 실행하는 방식 — 역할 분리/협업/상태 관리를
    표현하지 못함 (기각).
- 이유: 멀티 에이전트를 기본 구조로 삼으면 이후 기능이 자연스럽게 확장되고,
  Workspace Core는 "누가(Agent) 무엇을 할지" 조율에만 집중해 책임이 명확해진다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.4.0 반영. Phase 재구성(로드맵 갱신).
  기존 P1-2(도메인), P1-3(Interfaces)는 유지하되 Agent 도메인/신규 Interface를
  더하는 후속 Task가 추가된다.

## ADR-0007: Event 기반 Agent 협업 구조 (Event Bus) 도입

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: 멀티 에이전트 환경에서 Agent가 서로를 직접 호출하면 강한 결합이 생겨
  Agent 추가/교체/테스트가 어렵고, 협업 흐름이 코드 곳곳에 흩어진다.
- 결정: Agent 간 협업을 **Event Bus 기반의 발행/구독**으로 처리한다. 예:
  Planner 완료 → `TaskCreated` → Coding Agent 실행 → `ReviewRequested` →
  Review Agent 실행. `EventBus` 인터페이스를 Phase 1에서 정의하되, 구현은 이후
  Phase(멀티 에이전트 코어)에서 진행한다.
- 대안: Agent 간 직접 메서드 호출 — 직관적이지만 강결합·낮은 확장성 (기각).
- 이유: 느슨한 결합으로 Agent를 독립적으로 추가·교체·테스트할 수 있고, 협업
  흐름을 이벤트로 명시적으로 추적할 수 있다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.4.0 §3.6, §4에 반영. `events/` 패키지와
  `EventBus` 인터페이스가 계획에 포함된다.

## ADR-0008: Conversation Layer 도입 (입력 표면 통합 · Voice 대비)

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: 향후 CLI 외에 Dashboard/Mobile/Voice/API 등 다양한 입력 표면을 지원해야
  한다. 각 표면을 Workspace Core에 직접 연결하면 표면이 늘어날 때마다 Core를
  수정해야 한다.
- 결정: UI 표면과 Workspace Core 사이에 **Conversation Layer**를 둔다. 모든
  표면의 입력을 표준 요청으로 정규화하고 응답을 표면에 맞게 변환한다. Voice는
  Workspace Core가 아니라 **Conversation Layer에 연결되는 UI**로 취급한다.
  `ConversationEngine` 인터페이스를 Phase 1에서 정의하되 구현은 이후로 미룬다
  (지금 구현하지 않음).
- 대안: 표면을 Workspace Core에 직접 연결 — 경로는 짧지만 표면 추가마다 Core
  수정 필요 (기각).
- 이유: 입력 정규화를 한 곳에 모으면, 새 표면(특히 Voice) 추가가 어댑터 추가로
  끝나고 Core는 변경되지 않는다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.4.0 §3.1~3.2에 반영. UI Surfaces →
  Conversation Layer → Workspace Core 계층이 확정된다.

## ADR-0009: EngineAdapter를 확장 실행 계약으로 확대

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: 기존 `EngineAdapter`는 `run_task()` 단일 메서드였다. 멀티 에이전트
  환경에서는 여러 Agent가 동시에 엔진을 사용하므로 취소/상태/병렬/비용 같은
  운영 제어가 필요하다.
- 결정: `EngineAdapter`를 모든 Agent가 공유하는 확장 실행 계약으로 넓힌다:
  `run(...)`, `cancel(...)`, `status(...)`, `capabilities(...)`,
  `supports_parallel()`, `estimate_cost()`. 구체 구현(Claude Code/Codex/Gemini)은
  Phase 3(엔진 연동)에서 진행한다. ADR-0002(Adapter 패턴)를 계승·확장한다.
- 대안: `run_task()` 단일 계약 유지 — 단순하지만 멀티 에이전트 운영에 필요한
  제어를 제공하지 못함 (기각).
- 이유: Engine 선택 정책(비용/병렬 지원 기반)과 실행 제어(취소/상태)를 계약에
  포함해야 멀티 에이전트 오케스트레이션이 가능하다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.4.0 §3.8에 반영. 기존 P1-3에서 정의한
  `EngineAdapter` 인터페이스는 Phase 1 재개 시 확장 계약으로 갱신한다
  (ADR-0002 상태는 이 확장을 포함해 재확정).
- 후속: ADR-0015에서 세션 생명주기(`create_session`/`destroy_session`)를 더해
  실행 계약을 재확장한다.

## ADR-0010: Agent Runtime 계층 도입 및 Workspace Core 재정의 (+ WorkspaceSession)

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: v0.4.0에서 Workspace Core가 Agent 등록/관리, Task 분배, Engine 선택을
  직접 수행했다. 멀티 에이전트를 기본 구조로 심화하면서, 병렬 실행·스케줄링·
  생명주기 관리를 Core에 두면 Core가 비대해지고 책임이 섞인다.
- 결정:
  1. Workspace Core의 책임을 **프로젝트/설정 로드, 서비스 초기화,
     WorkspaceSession 관리, Agent Runtime 초기화, Workflow 시작, 종료**로 좁힌다.
     Task 실행은 **모두 Agent Runtime에 위임**한다.
  2. Workspace Core 아래 **Agent Runtime 계층**을 둔다: **Agent Registry**(등록/
     조회/제거), **Agent Scheduler**(선택/병렬/우선순위), **Agent Manager**(생성/
     생명주기/상태), **Event Bus**(발행/구독/통신).
  3. **WorkspaceSession** 도메인을 추가한다(현재 프로젝트/Mission/활성 Workflow/
     활성 Agent/Memory Snapshot/Engine Session 등 실행 상태).
- 대안: Workspace Core가 Agent를 직접 제어 — 계층은 단순하나 병렬/스케줄링/
  생명주기가 Core에 혼재 (기각).
- 이유: 실행 관심사(등록·스케줄·생명주기·통신)를 Runtime으로 분리하면 Core는
  세션과 조율에만 집중하고, 각 Runtime 컴포넌트를 독립적으로 확장·테스트할 수 있다.
- 결과/영향: ADR-0006에서 Workspace Core 직속이던 Agent Manager가 Agent Runtime
  내부로 이동한다. `docs/ARCHITECTURE.md` v0.5.0 §3.3~3.4 반영. Interfaces에
  `AgentRegistry`, `AgentScheduler` 추가.

## ADR-0011: Mission → Workflow → Task → Step 4단 계층 도입

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: 기존 Workflow→Task 2단으로는 "사용자 목표(무엇을)"와 "세부 실행 단위"를
  함께 표현하기 어렵다.
- 결정: **Mission(목표) → Workflow(협업 흐름) → Task(Agent 할당 작업) →
  Step(세부 실행 단위)** 4단 계층을 기본 모델로 삼는다. 도메인에 `Mission`,
  `Step`을 추가한다.
- 대안: Workflow=Task 2단 유지 — 단순하나 목표/세부 실행 표현 부족 (기각).
- 이유: 목표부터 세부 실행까지 일관된 단위로 추적·분배·검증할 수 있다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.5.0 §4, §6 반영. Workflow 도메인을 이
  계층 안에서 재정의.

## ADR-0012: Capability 중심 Agent 설계 (Memory/Automation은 Engine)

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: 역할(Role)만으로 Agent를 선택하면 엔진 능력과의 매칭이 부정확하고,
  Memory/Automation처럼 모든 Agent가 공유하는 기능을 Agent로 두면 중복이 생긴다.
- 결정:
  1. Agent를 **Capability 중심**으로 설계한다(Planning/Coding/Review/
     Documentation/Research/Vision/Voice/Git/MCP …). Scheduler는 엔진 종류가
     아니라 **Capability로** Agent를 선택한다. 도메인에 `AgentCapability` 추가.
  2. **Memory와 Automation은 Agent가 아니라 Core Engine(서비스)**로 유지한다.
     Memory Engine은 Context 생성/검색/저장/Snapshot 관리를 담당하며 모든 Agent가
     사용한다.
- 대안: 역할만으로 선택 + Memory Agent 도입 — 단순해 보이나 매칭 부정확·공용
  기능 중복 (기각).
- 이유: Capability 기반이면 엔진에 비종속적으로 정확히 Agent를 선택할 수 있고,
  공용 기능(Memory/Automation)은 서비스로 재사용된다.
- 결과/영향: ADR-0006의 "Memory Agent"는 폐기되고 Memory는 Engine으로 확정.
  `docs/ARCHITECTURE.md` v0.5.0 §3.6~3.7 반영.

## ADR-0013: Conversation Layer를 Interaction Layer로 확장

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정). ADR-0008을 대체.
- 날짜: 2026-07-23
- 배경: 입력 표면이 CLI/Voice를 넘어 Dashboard/Mobile/REST API/Slack/Discord/
  Webhook 등으로 확장될 예정이다.
- 결정: 기존 Conversation Layer를 **Interaction Layer**로 확장하고,
  `ConversationEngine` 인터페이스를 **`InteractionEngine`**으로 대체한다. Voice는
  Workspace Core가 아니라 Interaction Layer에 추가되는 표면으로 유지한다.
- 대안: Conversation Layer 명칭 유지 — 텍스트 대화에 국한된 인상 (기각).
- 이유: 다양한 상호작용 표면을 일관되게 수용하는 계층임을 이름과 계약에 반영.
- 결과/영향: `docs/ARCHITECTURE.md` v0.5.0 §3.2 반영. ADR-0008은 본 ADR로 대체됨.

## ADR-0014: Event Store 도입 (Event Bus와 분리)

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: Event Bus만으로는 이벤트가 소비되면 사라져 Replay/Audit/복구가 불가능하다.
- 결정: Event Bus와 별도로 **Event Store**를 둔다. 구조는 `Event Bus → Event
  Store → Subscribers`. 목적은 Event 기록/Replay/Audit/Debugging/Workflow 복구.
  `EventStore` 인터페이스를 Phase 1에서 정의하고 구현은 이후 Phase.
- 대안: Event Bus만 사용 — 단순하나 기록/복구 불가 (기각).
- 이유: 이벤트 기반 협업의 추적성과 복구력을 확보한다 (기록 우선 원칙과 부합).
- 결과/영향: `docs/ARCHITECTURE.md` v0.5.0 §3.5 반영. Interfaces에 `EventStore`
  추가.

## ADR-0015: EngineAdapter를 세션 생명주기 포함 계약으로 확장

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정). ADR-0009를 확장.
- 날짜: 2026-07-23
- 배경: 구현 엔진은 상태 있는 세션(연속 대화/작업 맥락)을 갖는다. 무상태 `run`
  만으로는 세션 생성/정리를 표현할 수 없다.
- 결정: `EngineAdapter` 계약에 **`create_session()`**, **`destroy_session()`**을
  추가한다. 최종 계약: `create_session`, `run`, `cancel`, `status`,
  `destroy_session`, `capabilities`, `supports_parallel`, `estimate_cost`.
  구체 구현은 Phase 3(엔진 연동).
- 대안: 무상태 `run`만 유지 — 단순하나 세션 있는 엔진 제어 불가 (기각).
- 이유: 세션 생명주기를 계약에 포함해야 상태 있는 실행/취소/정리를 일관되게
  다룰 수 있다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.5.0 §3.8 반영. ADR-0009의 계약을 이
  ADR로 확장·대체.

## ADR-0016: Engine Runtime 계층 도입 (Agent Runtime과 Engine Adapter 사이)

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: v0.5.0에서 Agent가 Engine Adapter를 직접 호출했다. 멀티 에이전트가 여러
  엔진을 동시에 쓰는 환경에서 엔진 선택·세션 풀·병렬 실행 로직이 각 Agent에
  중복·산재될 위험이 있다.
- 결정: Agent Runtime과 Engine Adapter 사이에 **Engine Runtime** 계층을 둔다.
  책임: 엔진 선택(capabilities/estimate_cost/supports_parallel 기반), 엔진 세션
  풀 관리(Engine Adapter의 create_session/destroy_session 활용), 병렬 실행 관리.
  Agent는 Engine Adapter를 직접 호출하지 않고 **Engine Runtime을 거친다**.
  `EngineRuntime` 인터페이스를 추가한다.
- 대안: Agent가 Engine Adapter 직접 호출 — 단순하나 선택/세션/병렬 로직 중복 (기각).
- 이유: Agent Runtime(Agent 실행 관리)과 대칭으로 Engine Runtime(엔진 실행 관리)을
  두면 책임이 명확해지고, 엔진 관련 정책을 한 곳에서 관리·테스트할 수 있다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.6.0 §3.9 반영. 의존 순서가 Agent →
  Engine Runtime → Engine Adapter → 구현 엔진으로 확정. Interfaces에 `EngineRuntime`
  추가(총 16종).

## ADR-0017: Context Manager 도입 (Memory Snapshot 관리 역할 분리)

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: v0.5.0의 Memory Engine이 저장/검색과 Context 생성/Snapshot 관리를 모두
  담당해 책임이 혼재했다.
- 결정: **Context Manager**를 도입해 역할을 분리한다. Context Manager는 Agent에게
  제공할 **Context 조립**과 **Memory Snapshot 생명주기**(생성/복원)를 담당하고,
  Memory Engine은 **저장/검색만** 담당한다. WorkspaceSession의 Memory Snapshot은
  Context Manager가 소유·관리한다. Memory 접근 순서는 Agent → Context Manager →
  Memory Engine. `ContextManager` 인터페이스를 추가한다.
- 대안: Memory Engine이 Snapshot까지 담당 — 컴포넌트는 적으나 책임 혼재 (기각).
- 이유: 저장(Memory Engine)과 Context/Snapshot(Context Manager)을 분리하면 Context
  전략을 독립적으로 교체·테스트할 수 있다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.6.0 §3.8 반영. `MemoryEngine` 계약에서
  Snapshot 책임을 제거하고 `ContextManager`로 이관.

## ADR-0018: Event Store를 독립 Subscriber로 위치 조정

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정). ADR-0014를 보완.
- 날짜: 2026-07-23
- 배경: ADR-0014는 `Event Bus → Event Store → Subscribers` 구조로 Event Store를
  전달 경로에 두었다. 이 경우 Event Store가 전달을 게이팅하고 단일 장애점이 될
  수 있다.
- 결정: Event Store를 Event Bus의 **독립 Subscriber**로 위치 조정한다. 다른
  구독자(Agent 등)와 동등하게 Bus를 구독하여 모든 이벤트를 기록하되, 다른
  구독자로의 전달에 끼어들지 않는다. 목적(기록/Replay/Audit/복구)은 유지한다.
- 대안: Event Store를 전달 경로(Bus 하위)에 유지 — 기록 보장은 직관적이나 전달
  게이팅·단일 장애점 위험 (기각).
- 이유: 기록 관심사를 전달 경로에서 분리하면 장애가 격리되고 전달 성능/신뢰성이
  기록에 종속되지 않는다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.6.0 §3.5, §5, §8 반영. ADR-0014의 구조를
  본 ADR로 보완.

## ADR-0019: Coordination Capability 추가

- 상태: 승인됨 (2026-07-23, 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: 여러 Agent의 협업을 조정하는 역할이 암묵적이면 조정 책임이 흐릿해지고
  선택·추적이 어렵다.
- 결정: `AgentCapability`에 **Coordination**을 추가한다. Coordination 능력을 가진
  Agent(Coordinator)는 협업 흐름을 조정하되, 다른 Agent를 직접 호출하지 않고
  Event 기반 협업 규칙(ADR-0007)을 따른다.
- 대안: 조정 역할을 암묵적으로 처리 — 별도 정의는 불필요하나 책임이 흐릿함 (기각).
- 이유: 조정 역할을 Capability로 명시하면 Scheduler가 이를 선택 기준으로 삼고,
  조정 책임을 추적할 수 있다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.6.0 §3.6 반영. Capability 목록에
  Coordination 추가.

## ADR-0020: Task-Workflow 관계 필드(`workflow_id`)를 선택 필드로 추가

- 상태: 승인됨 (2026-07-23, P1-5 진행 중 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: P1-4에서 `Workflow.mission_id`(필수), `Step.task_id`(필수)를 추가해
  Mission→Workflow→Task→Step 계층에서 하위 개체가 상위 개체를 참조하는 패턴을
  마련했지만, `Task`에는 자신이 속한 `Workflow`를 가리키는 필드가 없어 이 패턴이
  Task 단계에서 끊겨 있었다. P1-5에서 이 관계를 재검토해 필드를 보완하기로 했다.
- 결정: `Task`에 `workflow_id: str | None = None`을 추가한다. `Workflow.
  mission_id`/`Step.task_id`와 달리 **선택 필드(기본값 None)**로 둔다.
- 대안:
  - `workflow_id`를 필수 필드로 추가 — 계층의 일관성은 완벽해지지만, 현재
    `TaskEngine.create_task(project_id, title)` 인터페이스 계약(P1-3에서 확정)이
    `workflow_id`를 받지 않으므로, 필수로 만들려면 Interface 계약도 함께
    변경해야 한다. 이번 P1-5는 "Domain만 다루고 Interface는 손대지 않는다"는
    범위 지시를 받았으므로 기각.
  - 필드를 추가하지 않고 다음 Phase로 미룸 — 계층 참조 패턴이 Task 단계에서
    끊긴 채로 남아 Workflow 실행/조회 로직 설계 시 혼란을 야기할 수 있어 기각.
- 이유: 선택 필드로 두면 (1) Task가 아직 어떤 Workflow에도 배정되지 않은
  상태(예: 백로그성 Task)를 자연스럽게 표현할 수 있고, (2) 기존 `TaskEngine`
  Interface 계약을 변경하지 않고도 관계를 표현할 수 있다. 이후 Phase(Interface
  확장·TaskEngine 구현)에서 필요하면 필수화 여부를 다시 검토한다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.6.1 §6 반영. `domain/task.py`,
  `tests/domain/test_task.py` 갱신.

## ADR-0021: Phase 계층 폐지, `Milestone → Task` 2단 관리 체계로 전환

- 상태: 승인됨 (2026-07-24, 사용자 지시로 확정 — Migration Task)
- 날짜: 2026-07-24
- 배경: 기존 프로젝트 관리 체계는 `Milestone → Phase → Task` 4단 계층이었다.
  Milestone 1(Phase 0 + Phase 1)을 실제로 운영해 본 결과 다음 문제가 드러났다.
  1. Phase 완료 승인과 Milestone 완료 승인이 사실상 같은 성격의 게이트였는데도
     별도로 존재해, 승인 지점이 필요 이상으로 늘어났다(문서화 단계에서 "Phase 0
     완료 승인"을 받고, 구현 단계 끝에서 다시 "Phase 1 완료 승인"을 받는 식).
  2. Task 하나하나가 이미 "하나의 구현 목표 + 하나의 커밋 + 하나의 구현
     사이클"로 충분히 독립적이었다. 실제 커밋 이력(`git log`)도 Task 단위로
     정확히 1:1 대응되어 있었다 — Phase는 그 위에 존재하는 그룹 라벨일
     뿐이었다.
  3. Milestone 2~4는 애초에 Phase 단위로만 목표가 서술되어 있었고 개별 Task가
     정의된 적이 없었다. 즉 Phase는 "이미 진행 중인 작업의 실제 관리 단위"라기
     보다 "아직 오지 않은 작업의 목표 그룹 설명"에 더 가까웠다.
- 결정: Phase 계층을 폐지하고 `Milestone → Task` 2단 계층으로 단순화한다.
  1. Task ID 형식을 `T{Milestone 번호}-{일련번호}`(예 `T1-01`)로 표준화한다.
  2. 기존 Phase 0(P0-1~P0-11)과 Phase 1(P1-0~P1-13), 총 25개 Task를 Milestone 1
     소속 `T1-01`~`T1-25`로 번호만 재부여한다. **내용·완료 상태·이력(진행
     로그, ADR 참조)은 그대로 보존**하며, 대응표(Migration Table)를
     `docs/ROADMAP.md`에 영구 기록한다.
  3. 승인 지점은 **Milestone 완료 승인**으로 일원화한다. (과거에 이미 완료된
     "Phase 0 완료 승인", "Phase 1 착수 승인"은 역사적 사실로서 Task 설명에
     그대로 남긴다 — 다시 승인받지 않는다.)
  4. Milestone 2~4처럼 아직 Task로 분해되지 않은 영역은 목표만 "예정 작업
     영역"으로 서술하고, 실제 착수 시점에 `T2-01`, `T3-01`, `T4-01`부터 개별
     Task를 정의한다(Task Driven Development — 너무 이른 시점에 세부 Task를
     확정하지 않는다).
- 대안:
  - 현행 4단 계층 유지 — 이미 익숙하고 문서 변경 비용이 없음. 그러나 위에서
    지적한 이중 승인·불필요한 그룹핑 문제가 계속 남는다 (기각).
  - Phase는 유지하되 승인만 Milestone 단위로 통합 — 절충안이지만, Task가 이미
    충분히 독립적인 단위인 상황에서 Phase라는 그룹 개념 자체가 실질적인 정보
    가치를 더하지 못해 완전 폐지가 더 단순하다 (기각).
  - 기존 Task ID(P0-x, P1-x)를 그대로 두고 Phase "라벨"만 문서에서 지움 — ID
    형식 자체가 Phase 번호(`P{phase}-{seq}`)에 묶여 있어 미봉책이 된다. 새
    Milestone에 진입할 때 ID 체계가 다시 애매해진다 (기각).
- 이유: Task 자체가 이미 "구현 목표+커밋+사이클"의 최소 완결 단위이므로, 그 위에
  불필요한 중간 계층을 두지 않는 것이 실제 운영 방식과 가장 잘 맞는다. 승인
  지점을 Milestone 단위로 좁히면 승인 피로도를 줄이면서도 "아키텍처 변경/신규
  기능/리팩토링/Phase(→Milestone) 완료" 4대 승인 원칙(RULES.md §1.4)의 취지는
  그대로 유지된다.
- 기대 효과:
  - 관리 계층이 하나 줄어 상태 추적이 단순해진다("Milestone 1의 몇 번째
    Task인지"만 보면 됨, "어느 Phase의 몇 번째 Task인지"를 이중으로 추적할
    필요 없음).
  - Task ID가 Milestone에만 종속되므로, Milestone이 늘어나도(M5, M6, …) ID
    체계가 자연스럽게 확장된다.
  - Milestone 완료 승인 1회로 게이트가 명확해져 "언제 사용자 승인이 필요한가"에
    대한 혼선이 줄어든다.
- Commit 전략 변경: 기존에도 Task 1개 = Commit 1개 원칙은 지켜지고 있었으므로
  실질적인 커밋 전략 변경은 없다. 다만 커밋 메시지 접두어를 `[PhaseN][Pn-x]`
  형식에서 `[Mn][Tn-xx]` 형식으로 변경한다 (`.ai/RULES.md` §5.3 갱신).
- 개발 방식 변경: Task 착수 전 별도의 "Phase 착수 승인"이 필요했던 흐름을
  없애고, Milestone 착수 시 한 번의 승인 이후에는 각 Task를 "구현 → 테스트 →
  보고" 흐름으로 연속 진행한다. Milestone 완료 시점에만 종합 승인을 받는다.
- 결과/영향: `docs/ROADMAP.md`(Migration Table 포함), `docs/ARCHITECTURE.md`
  §0(신설), `.ai/TASKS.md`(전면 재구성), `.ai/MEMORY.md`, `.ai/RULES.md`
  (승인 항목·커밋 메시지 예시), `README.md`에 반영됨. 적용 대상 코드는 없음
  (순수 프로젝트 관리 체계 변경).

## ADR-0022: Task 분해 원칙 — "한 Task = 하나의 아키텍처 책임 경계", 정의·구현·테스트는 한 Task 안에서 완결

- 상태: 승인됨 (2026-07-24, 사용자 지시로 확정 — 설계 검토 후 결정)
- 날짜: 2026-07-24
- 배경: ADR-0021은 Task를 "하나의 구현 목표 + 하나의 Commit + 하나의 구현
  사이클"로 정의했다. 그런데 계획 중이던 T1-18("신규 Interface 정의 및
  EngineAdapter 세션 계약 확장, 총 16종")을 실제로 검토해 보니, 서로 참조하지
  않는 4개의 독립적인 아키텍처 하위 계층 — Agent Runtime(§3.4, AgentManager/
  Registry/Scheduler/Repository/EventBus/EventStore), Engine Runtime(§3.9,
  EngineRuntime + EngineAdapter 확장), Memory 계열(§3.8, ContextManager +
  MemoryEngine), Interaction Layer(§3.2, InteractionEngine) — 가 하나의 Task에
  뭉쳐 있었다. 이는 ADR-0021이 정의한 "하나의 구현 목표"라는 기준에 부합하지
  않았다.
- 결정:
  1. **Task 분해 기준을 "아키텍처 책임 경계(= `docs/ARCHITECTURE.md` §3의 컴포넌트
     절 경계)"로 명문화한다.** 서로 의존하지 않는(= 서로 import하지 않는) 컴포넌트
     그룹은 별도 Task로 분리하고, 서로 강하게 의존하는 컴포넌트(예: EngineRuntime과
     EngineAdapter, ContextManager와 MemoryEngine)는 같은 Task로 묶는다.
  2. T1-18을 4개 Task로 분리한다: **T1-18 Agent Runtime Interfaces**,
     **T1-19 Engine Runtime Interfaces**, **T1-20 Memory Interfaces**,
     **T1-21 Interaction Interfaces**. 이에 맞춰 이후 Task를 T1-22(Workspace
     Core Skeleton) ~ T1-28(Milestone 1 Review)로 순연한다(구 T1-19~T1-25).
  3. **"인터페이스 정의 → 구현 → 테스트"는 계속 한 Task 안에서 완결한다.** 이를
     Task별로 더 잘게(예: "정의만 하는 Task"와 "테스트만 하는 Task"를 분리)
     쪼개지 않는다.
- 대안:
  - 현행 유지(T1-18을 하나의 Task로) — Commit 1개로 16종 계약을 한 번에 볼 수
    있다는 장점은 있으나, diff가 서로 무관한 4개 하위 계층에 걸쳐 흩어져
    리뷰·롤백 단위가 모호해짐 (기각).
  - "정의 → 구현 → 테스트"까지 Task 단위로 잘게 분리 — 더 잘게 쪼갤수록 각
    Task의 책임은 명확해지지만, Milestone 1처럼 아직 구체 구현이 없는 계약
    전용 단계에서는 Task 수만 불필요하게 늘어나고 오히려 흐름이 끊긴다 (기각).
  - Task 분해 기준을 "파일 개수" 등 기계적 기준으로 정함 — 아키텍처 의미와
    무관한 분해가 되어 Commit이 여전히 "하나의 설계 의도"를 나타내지 못함
    (기각).
- 이유: 아키텍처 책임 경계로 Task를 나누면 (1) Commit 하나가 항상 하나의 설계
  의도를 표현하고, (2) 리뷰어가 diff만 보고도 어떤 컴포넌트가 바뀌었는지 즉시
  파악할 수 있으며, (3) 향후 자동화된 Task 생성 도구("Task Analyzer")가 "한
  Task = 한 책임"이라는 동일한 규칙으로 Task를 기계적으로 생성할 수 있다. 반면
  정의·구현·테스트를 Task 단위로 추가 분리하면 계약 전용 단계에서 Task 수 증가
  대비 얻는 이점이 적어, 균형을 위해 이 층위의 분해는 하지 않는다.
- 부가 발견 (설계 검토 과정에서 확인, 이번 결정과는 별개):
  - `memory_engine.py`는 현재도 `remember`/`recall`만 가지고 있어 "Snapshot
    책임 제거"라는 문구가 실제로는 변경할 코드가 없는 상태(No-Op)임을 확인함
    (T1-20에 반영).
  - `AgentRegistry`(런타임 등록부)와 `AgentRepository`(영속 저장소)는 이름이
    유사해 혼동 우려가 있어, 각 인터페이스 docstring에 역할 차이를 명시하기로
    함(T1-18에 반영).
  - `AgentRuntime` 파사드 인터페이스 도입, `EngineAdapter.run()`의 입력 단위를
    `Task`에서 `Step`으로 낮출지 여부, LLM Policy Domain과 EngineRuntime의
    연동 시점은 지금 결정하지 않고 각각 자연스러운 시점(T1-22, Milestone 2,
    Milestone 3~4)에 재검토하기로 함(YAGNI).
- 결과/영향: `.ai/TASKS.md`의 T1-18~T1-28 재구성, `docs/ROADMAP.md`의 진행
  상태·Migration Table 주석 갱신에 반영됨. 적용 대상 코드는 없음(설계 검토 및
  계획 문서 변경).

## DX-01: Stage Checkpoint + Smart Model Router 통합 (Manual Recommendation Executor)

- 상태: 승인됨 (2026-07-25, 사용자 지시로 확정)
- 날짜: 2026-07-25
- 배경: Claude Code 세션에서 Task를 진행하는 동안 Model/Effort가 다음 작업에
  적합한지 재판단하는 표준 절차가 없어, 매번 사람의 감에 의존했다. 이미
  `.claude/skills/smart-model-router`(Task Type/Difficulty/Effort/Scope/
  토큰/Reasoning/Project Stage 7개 항목 기반 판단 프레임워크)가 존재했으나
  세션 중 수동 호출로만 쓰이고 있었고, 사용자에게 보이는 세션 메시지의
  언어(한국어/영어 혼용)도 표준화되어 있지 않았다.
- 결정:
  1. `.ai/RULES.md`에 §2.4 Stage Checkpoint를 신규 추가한다. Task 내부 4개
     작업 단계 경계(Analysis/Implementation/Validation/Task 완료)마다 Smart
     Model Router를 실행해 Recommendation(model/effort/confidence/reason)을
     산출한다. 4개 경계는 `.ai/skills/Task-Planning.md`(Analysis)와
     `.ai/skills/Task-Implementation.md` §5.1~5.6(Implementation/
     Validation/Task 완료)의 기존 절차 경계에 그대로 대응시킨다(신규 SOP를
     만들지 않음).
  2. **"Phase"라는 이름은 쓰지 않는다.** ADR-0021에서 `Milestone → Phase →
     Task` 관리 계층의 "Phase"가 이미 폐지되었으므로, 이름 충돌로 인한 혼동을
     피하기 위해 Task 내부 작업 단계는 **"Stage"**로 부른다.
  3. Recommendation은 지금 단계에서 실행 로직이 없는 순수 판단 결과이며,
     **Manual Recommendation Executor**(사용자에게 한국어 UI로 보여주고
     선택받아 `/model` 전환을 안내만 하는 방식)로 소비한다. Model/Effort는
     동일/상향/하향 어떤 경우에도 **자동 전환하지 않는다** — Claude Code
     세션에는 이를 프로그램적으로 전환하는 도구가 없음을 확인했다(방금 도구
     목록에서 재확인).
  4. 세션 중 사용자에게 보이는 모든 메시지(진행 상황/질문/완료 보고/추천
     결과/오류 안내/승인 요청)를 한국어로 통일한다(§5.1 확장). Model,
     Effort, pytest, ruff, mypy, Commit Message, 클래스/함수/파일명, API 등
     기술 용어는 원문을 유지한다.
  5. 불필요한 중단을 막기 위해 Skip Rule을 둔다 — 직전 Stage와 동일한
     Recommendation이거나 현재 설정이 이미 추천과 일치하면 박스 UI 없이 한
     줄만 출력하고 자동 진행한다.
  6. `Recommendation`의 실제 Python 구현(`domain/llm_policy.py` 확장 등)은
     지금 하지 않는다. Task Driven Development 원칙(RULES.md §2.1)과 §7
     Temporary LLM Policy의 M2 이후 로드맵에 따라, 실제 제품 코드 반영은
     Milestone 2 이후 별도 Task로 다룬다. 지금은 §2.4 안의 개념적 스키마로만
     정의한다.
- 대안:
  - 신규 `CLAUDE.md` 생성 후 그곳에 규칙 정의 — 이 저장소는 이미
    `.ai/RULES.md`를 AI 운영 규칙의 단일 원천으로 쓰고 있어(README.md,
    §3.1 Context Loading Rules), `CLAUDE.md`를 추가하면 두 문서가 같은
    역할로 공존하게 되어 Context Loading Rules와 충돌한다 (기각).
  - "Phase Checkpoint"라는 원래 요청 명칭 유지 — ADR-0021에서 이미 폐지한
    프로젝트 관리 용어 "Phase"와 이름이 겹쳐 향후 문서 독해 시 혼동 위험이
    크다. "Stage"로 대체해도 요청하신 UI 문구·흐름은 그대로 유지 가능하다
    (기각, 사용자 승인).
  - 지금 바로 `Recommendation`을 Python 도메인 객체로 구현 — Milestone 2
    (§7 M2 "Rule 기반 선택")를 앞지르는 구현이 되어 Task Driven Development
    원칙과 어긋난다. 지금은 RULES.md 문서 안의 스키마로만 정의하고, 실제
    코드는 해당 Milestone에서 별도 Task로 다룬다 (기각, 사용자 설계에도
    "미래" 경로로 명시됨).
- 결과/영향: `.ai/RULES.md`(v0.3.0, §2.4 신규·§5.1 확장·§7 상호 참조),
  `.ai/skills/Task-Planning.md`·`.ai/skills/Task-Implementation.md`(Stage
  경계 상호 참조 4곳), `.ai/TASKS.md`(DX-01 진행 로그) 갱신. `README.md`,
  `docs/ARCHITECTURE.md`는 변경하지 않음 — 시스템 아키텍처가 아니라 AI 세션
  운영 절차이기 때문이다. 적용 대상 소스 코드(`src/`, `tests/`)는 없다.

## DX-02: 설계 철학(Architecture First 강화·최소 복잡성·YAGNI·점진적 확장·응집도·기존 코드 존중)을 RULES.md 영구 규칙으로 승격

- 상태: 승인됨 (2026-07-25, 사용자 지시로 확정)
- 날짜: 2026-07-25
- 배경: Milestone 2 T2-07 착수 직전, 사용자가 Stage Checkpoint 질문에 대한
  답으로 별도의 설계 철학 문서를 제시했다("AI Workspace 설계 철학" —
  Architecture First/최소 복잡성/YAGNI/응집도/점진적 확장/기존 코드 존중).
  T2-07은 이 철학을 실제로 한 번 적용해 효과를 확인했다(기존 테스트 점검 후
  실제 빈틈 2곳만 채움, 새 파일 없음). 사용자가 이를 일회성 제안이 아니라
  프로젝트의 공식·영구 규칙으로 채택할 것을 요청했다.
- 결정:
  1. `.ai/RULES.md`에 **새 섹션을 만들지 않고** 기존 규칙에 통합한다
     (v0.4.0). 대조 결과 상당 부분이 이미 기존 규칙과 중복되었다:
     - §1.2 Architecture First — 이미 있던 "아키텍처 의존성 규칙 위반
       금지"에 **핵심 아키텍처 자산 명시 보호 목록**(`EngineAdapter`,
       `AgentRegistry`, `WorkflowEngine`, `ProjectRepository`, Workspace
       Core, Agent Runtime)과 **"아키텍처 vs 단순함 충돌 시 아키텍처
       우선"** 우선순위 규칙, "AI Workspace는 프레임워크 프로젝트"라는
       프레이밍을 추가.
     - §4.2 Simplicity First — 이미 있던 YAGNI 관련 항목(불필요한
       추상화 금지, 미래 확장성 금지 등)은 유지하되, **최소 복잡성**
       (새 Class/Interface/Manager 등을 만들기 전 기존 구조 검토),
       **점진적 확장**(패턴이 명확해질 때까지 중복 허용, 조기 추상화
       금지), **새 컴포넌트를 만들기 전 자문 질문 6개**, **금지 사항
       목록**을 추가로 통합.
     - §4.3 Surgical Changes — "기존 코드 존중"(새 코드 작성 전 기존
       구현을 먼저 검토, 확장/수정을 신규 작성보다 우선)을 추가.
     - 신규 **§4.5 Cohesion**(응집도 우선) — "하나의 컴포넌트는 하나의
       책임만" 원칙은 기존 규칙에 없던 내용이라 새로 추가. §2.1/
       ADR-0022의 "한 Task = 하나의 책임" 원칙과 명시적으로 연결.
     - §4 도입부에 **구현 순서**(기존 구현 검토 → 단순 해결책 탐색 →
       아키텍처 준수 확인 → 최소 구현 → 검증)를 추가해 4.1~4.5를 하나의
       절차로 연결.
  2. YAGNI는 별도 절을 만들지 않는다 — 기존 §4.2 내용과 대부분 중복되어
     그 안에서 소제목으로만 명시적으로 재확인한다(사용자 지시: "중복되는
     규칙은 제거하고 하나의 명확한 규칙으로 정리").
  3. ADR 번호는 소비하지 않는다 — 시스템 아키텍처 결정이 아니라 코딩
     원칙/프로세스 정리이므로 DX-01과 동일하게 `DX-02`로 기록한다
     (`.ai/DECISIONS.md` 상단 안내 참고). ADR 최신 번호는 ADR-0022로
     유지된다.
- 대안:
  - 별도의 새 섹션(예: "§8 설계 철학")을 만들어 통째로 붙여넣기 — 가장
    빠르지만 §1.2/§4.2와 내용이 상당 부분 겹쳐 RULES.md 전체의 일관성이
    깨지고 "어느 규칙이 최종본인가"를 알기 어려워짐 (기각, 사용자 지시:
    "단순 복사나 추가가 아니라 프로젝트 전체 규칙으로 승격").
  - 기존 §1.2/§4.2/§4.3을 전면 재작성 — 통합 효과는 같지만 기존 문서의
    구조와 문장을 불필요하게 많이 바꿔 변경 이력 추적이 어려워짐 (기각,
    사용자 지시: "기존 RULES의 구조와 의도를 유지하면서 리팩터링").
- 이유: 기존 RULES.md는 이미 Architecture First(§1.2)와 Simplicity
  First(§4.2)라는 이름으로 유사한 원칙을 갖고 있었다. 사용자가 제시한
  철학은 이를 대체하는 새 규칙이 아니라 **더 구체적인 체크리스트로
  보강**하는 성격이 강했으므로, 기존 절 제목과 의도를 유지한 채 내용만
  풍부하게 하는 편이 "일관성 있게 통합"이라는 사용자 요구에 가장
  부합한다.
- 결과/영향: `.ai/RULES.md`(v0.4.0, §1.2/§4.2/§4.3 확장, §4.5 신규,
  §4 도입부에 구현 순서 추가). 앞으로 모든 Task의 설계 판단·구현·
  리팩터링은 이 통합된 규칙을 기준으로 한다. 소스 코드(`src/`, `tests/`)
  변경 없음.
