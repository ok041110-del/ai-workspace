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

## ADR-0023: `run_parallel()` 병렬 실행 책임 경계 확정 (AgentScheduler vs EngineRuntime)

- 상태: 승인됨 (2026-07-26, 사용자 지시로 확정)
- 날짜: 2026-07-26
- 배경: M4-T06(`run_parallel` 실제 동시성 검증) 착수 중,
  `docs/ARCHITECTURE.md` §3.4(Agent Scheduler)와 §3.9(Engine Runtime)
  양쪽 모두 "병렬 실행"을 자신의 책임으로 서술하고 있어(§3.4 "병렬 실행
  관리", §3.9/ADR-0016 "병렬 실행을 담당") 두 컴포넌트 사이의 책임 경계가
  불명확했다. 실제 구현(`AgentScheduler.select()` vs
  `EngineRuntime.run_parallel()`)의 시그니처를 대조해 경계를 확정한다.
- 결정: 두 컴포넌트의 "병렬"은 서로 다른 층위의 책임이며 충돌하지 않는다.
  - **AgentScheduler(선택/할당 책임)**: `select(candidates, capability,
    max_count)`로 **동시에 활동할 수 있는 Agent 후보를 최대 max_count개
    선택**하는 정책 결정만 한다. 선택된 Agent들을 실제로 동시에
    실행시키는 메커니즘은 갖지 않는다 — 각 Agent가 이후 독립적으로
    Event를 구독·처리하면서 결과적으로 동시에 활동하게 될 뿐이다.
  - **EngineRuntime(실행 책임)**: `run_parallel(tasks)`로 **여러 Engine
    Task 실행을 실제로 동시에 수행**하는 메커니즘 자체를 책임진다. 이번
    ADR로 `ManagedEngineRuntime.run_parallel()`을 `ThreadPoolExecutor`
    기반 실제 동시 실행으로 구현한다(기존에는 순차 반복 호출).
  - 요약: **"누구를 동시에 활동시킬지 고르는 것"은 AgentScheduler,
    "실제로 여러 실행을 동시에 수행하는 것"은 EngineRuntime.**
- 대안:
  - AgentScheduler에도 실행 메커니즘을 두는 방안 — Agent 실행과 Engine
    실행이라는 서로 다른 층위의 동시성을 한 컴포넌트가 떠안게 되어
    ARCHITECTURE.md §8 의존 방향(Agent Runtime → Engine Runtime)과
    책임 분리 원칙에 어긋남 (기각).
  - 두 컴포넌트 문서에서 "병렬" 표현을 아예 제거 — 실제로 둘 다 병렬성과
    관련이 있으므로 표현 자체를 지우기보다 의미를 구체화하는 편이
    맞다고 판단 (기각).
- 이유: 시그니처가 이미 답을 말하고 있다 — `select()`는 `list[Agent]`를
  반환하는 순수 선택 함수이고, `run_parallel()`은 `list[EngineResult]`를
  반환하는 실행 함수다. 문서의 "병렬" 표현이 겹쳐 보였을 뿐, 실제
  책임은 처음부터 겹치지 않았다.
- 결과/영향: `docs/ARCHITECTURE.md` §3.4/§3.9에 위 경계를 명시하는 문장
  추가. `runtime/engine/managed_engine_runtime.py`의 `run_parallel()`을
  `ThreadPoolExecutor`로 재구현(입력 순서 보장 계약은 그대로 유지).
  `RecoveringEngineRuntime.run_parallel()`은 이번 ADR 범위에서 수정하지
  않음 — 여전히 `inner.run_parallel()`에 그대로 위임하므로, 병렬 배치
  안의 개별 Task 재시도는 지원하지 않는다(M4-T06에서 테스트로 확인·
  기록, 필요 시 이후 Task로 이월).

## ADR-0024: v0.5.0 아키텍처 기준선(Baseline) 선언

> **표기 주의(M5-T07 Review에서 발견)**: 이 ADR의 "v0.5.0"은
> `pyproject.toml`의 **프로젝트 패키지 버전**을 가리킨다.
> `docs/ARCHITECTURE.md` 등 개별 문서 자체의 "문서 버전"(예:
> ARCHITECTURE.md는 현재 v0.12.0)과는 별개의 숫자 체계이며, 우연히
> ADR-0006~0012 시절 ARCHITECTURE.md의 문서 버전이 "v0.5.0"이었던
> 적이 있어 `.ai/DECISIONS.md`의 오래된 ADR 본문에도 같은 문자열이
> 등장하지만 서로 무관하다(과거 기록이라 수정하지 않음).

- 상태: 승인됨 (2026-07-26, 사용자 지시로 확정)
- 날짜: 2026-07-26
- 배경: M4-T09(Milestone 4 Review) 진행 중, 사용자가 "M4는 AI Workspace가
  '기반 프레임워크'에서 '사용 가능한 워크스페이스'로 넘어가는 전환점"이라고
  규정하며, Milestone 2·3처럼 단순 Review로 끝내지 말고 아키텍처
  기준선(Baseline)을 공식 선언할 것을 제안했다.
- 결정: **`pyproject.toml`의 `version`을 `0.1.0` → `0.5.0`으로 상향해
  아키텍처 기준선을 표시한다.** 근거:
  1. Milestone 1~4를 거치며 ARCHITECTURE.md가 그리는 전체 구조(16종
     Interface, 도메인 모델, Workspace Core, Agent Runtime, Engine
     Runtime과 그 위의 Recovering/ApprovalPipeline 데코레이터, Core
     Engines 4종, Memory 계열, Interaction Layer, CLI)가 실제 구현으로
     모두 채워졌다.
  2. Milestone 2·3·4 세 Milestone 내내 **새 최상위 Interface가 한 번도
     추가되지 않았다** — 매 Milestone Review(T2-08/M3-T08/M4-T09)에서
     반복 확인된 사실이며, M1의 Interface 설계가 구조적으로 안정적임을
     뜻한다.
  3. 기준선 선언 이후 원칙: M5 이후 작업은 기존 Interface·계층 구조를
     변경하지 않는 것을 기본값으로 하고 새 기능은 기존 구조 위에
     조립한다. 구조 자체를 바꿔야 하는 경우(Interface 추가/계층 변경)는
     지금까지와 동일하게 "Interface 변경 여부 우선 검토" 절차를 거쳐
     명시적 승인을 받는다 — 기준선 선언이 구조 변경을 영구히 금지하는
     것은 아니다.
- 대안:
  - 버전을 올리지 않고 문서(MEMORY.md 등)에만 "기준선"이라고 서술 —
    선언의 무게감이 약하고, 이후 세션이 프로젝트 상태를 빠르게 파악할
    표준 지표(버전 번호)가 없어짐 (기각).
  - `1.0.0`으로 상향 — 아직 Interaction Layer의 실제 표면(Voice/Slack/
    REST 등) 연동, Memory 요약, LLM Policy Engine 자동화 등 PRD의 핵심
    기능이 다수 남아 있어 "1.0"이 의미하는 완성도에는 이르지 못했다고
    판단 (기각, 사용자가 제시한 `0.5.0`을 그대로 채택).
- 이유: 버전 번호는 "구조적 완성도"와 "기능적 완성도"를 구분해 전달할
  수 있는 가장 간단한 신호다. `0.5.0`은 구조(Architecture)는 안정
  기준선에 도달했지만 기능(Feature)은 아직 절반 수준이라는 의미를
  정확히 전달한다.
- 결과/영향: `pyproject.toml`(`version = "0.5.0"`), `.ai/TASKS.md`의
  "Milestone 4 Review" 6절에 선언 근거 기록. `docs/ARCHITECTURE.md`/
  `docs/ROADMAP.md`/`README.md`는 이 ADR을 참고해 M4 완료 상태와 함께
  갱신한다. 소스 코드(`src/`, `tests/`) 변경 없음(문서·버전 메타데이터
  변경만).

## ADR-0025: ExecutionEnvironment를 EngineAdapter 하위(내부) 인터페이스로 도입

- 상태: 승인됨 (2026-07-26, 사용자 최종 승인)
- 날짜: 2026-07-26
- 배경: `ClaudeCodeEngineAdapter`/`CLIEngineAdapter`가 명령을 "무엇을
  실행할지"(엔진별 명령 조립·결과 파싱)뿐 아니라 "어디서 실행할지"까지
  떠안고 있었다 — 둘 다 생성자에서 `ProcessRunner`(M3-T03, 로컬 프로세스
  실행 전용 구체 클래스)를 직접 생성해 사용했다. GitHub Codespaces,
  Replit, Docker 같은 원격/컨테이너 실행 환경을 지원해야 할 때 이
  구조로는 매 Adapter 코드를 직접 고쳐야 한다. 설계 검토 단계에서
  두 가지 선택지를 비교했다: (1) Task→Agent→Engine 사이에
  `ExecutionEnvironment`를 새로운 최상위 Layer로 추가, (2)
  `EngineAdapter` 하위(내부) 인터페이스로 두고 DI로 주입.
- 결정:
  1. `ExecutionEnvironment`를 새 최상위 Layer로 만들지 않는다. Agent나
     Engine Runtime이 "어디서 실행되는지"를 알아야 할 이유가 없고,
     `EngineAdapter`가 이미 세션 생명주기 계약(ADR-0015)을 갖고 있어
     그 내부 협력자로 두는 것이 최소 복잡성 원칙(§4.2)에 맞는다.
  2. `interfaces/execution_environment.py`에 `ExecutionEnvironment`
     (ABC, `execute`/`cancel`), `ExecutionResult`, `ExecutionNotFoundError`
     를 신규 정의한다(총 18종 Interface). `execution_id`는 특정 실행
     방식(OS 프로세스 등)을 가정하지 않는 이름으로, 로컬 프로세스든
     향후 원격 컨테이너 세션이든 동일하게 다룰 수 있게 한다.
  3. `adapters/local_execution_environment.py`에 `LocalExecutionEnvironment`
     를 구현한다 — 새 프로세스 관리 로직을 만들지 않고 기존
     `ProcessRunner`(M3-T03)를 그대로 감싸는 얇은 위임 클래스로 둔다
     (Surgical Changes, `ProcessRunner`는 무변경).
  4. `ClaudeCodeEngineAdapter`/`CLIEngineAdapter`는 이제 구체 구현체를
     직접 생성하지 않고 **생성자 주입(Dependency Injection)**으로
     `ExecutionEnvironment`를 받는다(기본값 `LocalExecutionEnvironment()`
     — 호출자가 아무것도 지정하지 않아도 기존과 동일하게 동작하되,
     항상 다른 구현체로 교체 가능하다).
  5. Codespaces/Replit/Docker 실행 환경은 실제 요구사항이 생길 때까지
     구현하지 않는다(YAGNI) — 지금은 `LocalExecutionEnvironment`만
     존재한다.
- 대안:
  - 새 최상위 Layer(Task→Agent→Engine→EngineAdapter→ExecutionEnvironment
    →LLM)로 도입 — Agent/Engine Runtime이 실행 환경을 알아야 할
    이유가 없는데도 의존 경로에 계층이 하나 더 늘어나 오히려 책임
    경계가 흐려짐 (기각).
  - 아무 추상화도 두지 않고 필요할 때 리팩터링 — `ClaudeCodeEngineAdapter`
    와 `CLIEngineAdapter` 두 곳에 이미 같은 로직(`ProcessRunner` 직접
    생성)이 중복돼 있어, 나중에 실행 환경이 늘어나면 두 곳을 동시에
    고쳐야 하는 문제를 지금 막을 수 있음에도 방치하는 셈 (기각).
- 이유: `EngineAdapter`의 세션 생명주기 계약(ADR-0015)은 이미 "이
  Adapter가 실행을 어떻게 관리하는가"를 캡슐화하는 경계였다.
  `ExecutionEnvironment`를 그 경계 안쪽에 두면 Open-Closed Principle을
  만족한다 — 새 실행 환경이 추가되어도 `EngineAdapter`/`Agent`/`Engine
  Runtime` 어느 코드도 수정할 필요가 없다. DI를 기본 방향으로 삼은
  것은 Adapter가 협력자를 스스로 생성(`new`)하지 않아야 테스트 가능성과
  교체 가능성이 함께 확보되기 때문이다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.13.0 §3.10/§7/§9에 반영.
  `CLIProvider.parse_result()`(및 `CodexProvider`/`GeminiCliProvider`)
  시그니처도 `ProcessResult` → `ExecutionResult`로 함께 갱신(같은 이유로
  항상 함께 바뀌는 강결합). `ShellAgent`가 쓰는 `ProcessRunner`
  (M5-T04, EngineAdapter와 무관한 별도 경로)는 이번 변경 범위 밖.
  새 `ExecutionEnvironment` 구현체(예: 향후 Codespaces) 추가 시
  `EngineAdapter` 코드를 전혀 수정하지 않고 확장 가능함을
  `test_new_execution_environment_extends_adapter_without_code_changes`
  로 직접 증명(M11-T03).

## ADR-0026: EngineAdapter/EngineRuntime 계약에 `model` 파라미터 확장 (Milestone 14)

- 상태: 승인됨 (2026-07-26, 사용자 승인)
- 날짜: 2026-07-26
- 배경: M6(ADR 미부여, M6-T01/T02)에서 완성한 것은 **Provider 단위**
  라우팅(Claude Code/Codex/Gemini 중 어떤 CLI를 쓸지)뿐이었다.
  `LLMPolicyDecision`은 `model`(opus/sonnet/haiku 등)과 `effort`(low/
  medium/high)도 담고 있었지만, `EngineAdapter.run(session_id, task)`
  와 `EngineRuntime.run(task, required_capabilities)` 어디에도 이 값을
  전달할 자리가 없어 지금까지 한 번도 실제 실행에 반영된 적이 없었다
  (M6 Review 최초 이월, M10에서 "Interface 변경이 필요한 무거운
  작업"으로 재확인·재이월). `EngineAdapter`는 `.ai/RULES.md` §1.2가
  명시하는 핵심 아키텍처 보호 자산이라, 계약을 확장하는 이번 결정을
  ADR-0009/ADR-0015(과거 `EngineAdapter` 계약 확장)와 동일하게
  정식 기록한다.
- 결정:
  1. `interfaces/engine_adapter.py`의 `run(session_id, task)`에
     `model: str | None = None`(키워드 전용)을 추가한다.
  2. `interfaces/engine_runtime.py`의 `run(task, required_capabilities)`
     와 `run_parallel(tasks, required_capabilities)`에도 동일하게
     `model: str | None = None`을 추가한다.
  3. **Model만** 다루고 **Effort는 이번 범위에서 뺀다** —
     `ClaudeCodeEngineAdapter`는 이미 `--model` CLI 플래그와 연결된
     `model` 생성자 필드가 있어(M3-T02) 실제로 연결할 지점이 있지만,
     `effort`는 Claude Code CLI에 대응하는 플래그가 없어 지금 연결하면
     검증 불가능한 상태가 된다.
  4. **적용 대상은 `ClaudeCodeEngineAdapter`만** — Codex/Gemini
     (`CLIProvider` 계열)는 이 환경에 CLI가 없어 검증이 불가능해
     (M5-T05/M10에서 반복 확인) 계약만 만족하도록(받되 무시) 남겨둔다.
     `MockEngineAdapter`도 동일하게 무시한다(실제 엔진을 호출하지
     않아 모델 구분이 의미 없음).
  5. `ManagedEngineRuntime`/`RecoveringEngineRuntime`/
     `InMemoryEngineRuntime`은 `model`에 대해 새로운 선택·우선순위
     로직을 두지 않고 다음 계층까지 그대로 전달만 한다.
  6. `CodingAgent`/`ReviewAgent`/`DocumentationAgent`가
     `domain/llm_policy.py`의 신규 `model_name()`(기존
     `required_capabilities()`와 동일한 패턴)으로 정책의 model을
     꺼내 `engine_runtime.run()`에 함께 전달한다.
- 대안:
  - Effort까지 함께 라우팅 — 기각. 대응하는 실행 지점이 없어
    "정책 결정은 있으나 검증할 방법이 없는" 상태가 되고, 이는
    M5-T02/T07 Review가 이미 경계했던 문제("정책 결정≠실제 LLM 호출
    서비스")를 반복하는 것이다.
  - Codex/Gemini까지 함께 적용 — 기각. 이 환경에 CLI 바이너리가 없어
    실제 검증이 불가능하고(M5-T05/M10 재확인), 검증 없이 "구현됨"으로
    표시하는 것은 프로젝트 관례(Repository-Analysis SOP의 "1차 자료
    확인")에 어긋난다.
  - `create_session()`이 model을 받는 방식(세션 단위 고정) — 기각.
    `run()`이 세션 단위로 model을 매번 다르게 지정할 수 있는 유연성이
    없어지고(예: 같은 세션에서 재시도 시 다른 모델로 재시도하는
    미래 시나리오를 막음), 기존 세션 생명주기 계약(ADR-0015)의 의미도
    "세션=고정 모델"로 좁아진다.
- 이유: `model`을 `run()` 호출 단위로 전달하면 세션 생성 이후에도
  호출마다 다른 모델을 지정할 수 있어 유연하고, 새 선택 로직 없이
  기존 데코레이터 체인(`RecoveringEngineRuntime`→`ManagedEngineRuntime`
  →`EngineAdapter`)을 그대로 통과시키기만 하면 되어 최소 복잡성
  원칙에도 맞는다. 새 최상위 Interface를 추가하지 않고 기존 두
  Interface(`EngineAdapter`/`EngineRuntime`)의 계약만 확장해
  Interface First 원칙(불필요한 신규 컴포넌트 지양)을 지켰다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.16.0 §3.9/§3.10에 반영.
  `EngineAdapter` 구현체 4종, `EngineRuntime` 구현체 3종 전부 새
  시그니처를 받도록 갱신(M14-T01). `ClaudeCodeEngineAdapter`만 실제
  반영, 나머지는 받되 무시(M14-T02). `CodingAgent`/`ReviewAgent`/
  `DocumentationAgent` 3개 Agent가 정책의 model을 실제로 전달함을
  실제 `docs/llm_policy.example.yaml` 기반 통합 테스트로 증명
  (M14-T03). 이월 부채(Effort 라우팅, Codex/Gemini 실연동)는
  실제 대응 지점이 생기기 전까지 계속 이월한다.

## ADR-0027: `EngineRuntime`에 `estimate_cost()` 추가 + `BudgetPolicyEngine` 신설 (Milestone 15)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: `EngineAdapter.estimate_cost(task) -> CostEstimate`는 M3부터
  존재했지만, `EngineRuntime`도 어떤 Agent도 이를 호출한 적이 없었다
  (M12의 `WorkflowEngine.plan()`, M13의 `AgentScheduler.select()`와
  동일한 "만들어졌지만 쓰인 적 없는 기능" 패턴). `EngineRuntime`은
  `.ai/RULES.md` §1.2가 보호하는 핵심 아키텍처 자산(`EngineAdapter`와
  같은 층위)이라, 계약을 확장하는 이번 결정을 ADR-0009/ADR-0015/
  ADR-0026(과거 `EngineAdapter`/`EngineRuntime` 계약 확장)과 동일하게
  정식 기록한다.
- 결정:
  1. `interfaces/engine_runtime.py`에 `estimate_cost(task,
     required_capabilities=frozenset()) -> CostEstimate`를 추가한다.
     `run()`과 동일한 엔진 선택 규칙(등록 순서상 첫 매칭)을 따르되,
     세션을 만들지 않는다(read-only, side-effect 없음).
  2. `InMemoryEngineRuntime`/`ManagedEngineRuntime`은 각자의 기존
     어댑터 선택 로직(`_select`/`_require_adapter`)을 재사용해
     구현한다 — 새 선택 로직을 추가하지 않는다.
  3. `RecoveringEngineRuntime`은 재시도 로직 없이 내부 Runtime에 순수
     위임한다 — 추정은 실패할 side-effect가 없어 재시도할 이유가 없다.
  4. `domain/budget.py`에 `Budget(max_tokens, max_cost_usd)`/
     `BudgetDecision(allowed, reason)`을 신설한다. 둘 다 Provider/
     Engine 개념을 전혀 참조하지 않는 순수 domain 객체다.
  5. `interfaces/budget_policy_engine.py`에 `BudgetPolicyEngine`
     Interface(`check(estimate) -> BudgetDecision`)를 신설한다.
     `LLMPolicyEngine`(M5-T01)과 동일한 설계 원칙 — 정책이 없으면
     예외가 아니라 항상 허용으로 표현.
  6. `CodingAgent`에 선택적 `budget_policy_engine` DI를 추가한다.
     주입되어 있으면 실행 직전 `estimate_cost()` → `check()`를 거쳐
     초과 시 Task를 `BLOCKED`로 전환하고 실행하지 않는다(Approval/
     Retry 없음, M15 MVP).
- 대안:
  - `EngineAdapter.estimate_cost()`를 Agent가 직접 호출 — 기각.
    `.ai/RULES.md` §8 규칙 6("Engine 호출은 Agent → Engine Runtime →
    Engine Adapter 순서로만")을 정면으로 위반한다.
  - Budget을 `LLMPolicyEngine`에 병합(정책 하나로 통합) — 기각.
    `LLMPolicyEngine`은 AgentRole→Provider/Model/Effort를 결정하는
    책임이고, Budget은 Task 단위 CostEstimate를 검사하는 책임이라
    서로 다른 관심사다(SRP) — `LLMPolicyDecision`에 예산 필드를
    추가하면 "정책 하나가 두 가지 다른 질문에 답하는" 결합이 생긴다.
  - 예산 초과 시 Approval Engine으로 승인 요청 — 기각(사용자 확정
    범위 밖). Approval 비동기 처리는 기존에도 이월된 부채이며, 이번
    Milestone에서 함께 처리하면 범위가 걷잡을 수 없이 커진다.
  - 여러 Task에 걸친 누적 소비량 추적(Workspace 전체 잔여 예산) —
    기각(YAGNI). 실제 필요성이 증명되지 않았고, Task 단위 개별 확인만
    으로도 M15 목표("실행 전에 확인하고 초과하면 막는다")는 충족된다.
- 이유: `estimate_cost()`를 `run()`과 동일한 위치(`EngineRuntime`
  계약)에 두면 Agent가 이미 알고 있는 `required_capabilities`를 그대로
  재사용할 수 있고, 실제로 선택될 Adapter와 항상 같은 Adapter의
  추정치를 얻는다는 보장이 자연스럽게 성립한다. `BudgetPolicyEngine`을
  별도 Interface로 분리하면 Provider 독립성이 타입 수준에서 보장된다
  (`CostEstimate`만 알고 어떤 Provider/Engine인지 전혀 모름).
- 결과/영향: `docs/ARCHITECTURE.md` v0.17.0 §3.9/§3.13/§7(19종)에 반영.
  `EngineRuntime` 구현체 3종(`InMemoryEngineRuntime`/
  `ManagedEngineRuntime`/`RecoveringEngineRuntime`) 및 기존
  `EngineRuntime` 테스트 더블(`FakeEngineRuntime` 등) 전부 새 추상
  메서드를 구현하도록 갱신(M15-T02). `CodingAgent`가 예산 초과 시
  실행을 막음을 실제 `ManagedEngineRuntime`+`ClaudeCodeEngineAdapter`
  조합으로 증명(M15-T03). Effort/Model 기반 비용 차등, 여러 Task
  누적 예산 추적, 실시간 API 과금 조회는 실제 필요성이 생기기 전까지
  이월한다.

## ADR-0028: Project Knowledge System 도입 (KnowledgeRepository/KnowledgeSearch/KnowledgeProvider, 기존 MemoryEngine과 분리) (Milestone 16)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: 사용자가 "AI가 프로젝트의 구조와 설계 의도를 이해할 수 있는
  Workspace 전용 Knowledge Layer"를 요청했다(M16 킥오프 프롬프트).
  설계 검토 결과, `interfaces/memory_engine.py`의 `MemoryEngine`은
  M1부터 이미 존재하지만 `ContextManager`가 감싸서 **Mission 요약/
  세션 연속성**(M8-T03)에 쓰는 완전히 다른 개념임을 확인했다. 이름을
  재사용하면 "세션 기억"(사용자가 명시적으로 범위 밖이라 한 Chat
  History/Conversation Memory와 가까운 개념)과 "프로젝트 지식"이
  섞인다고 판단해, 새 이름의 컴포넌트 계열로 분리하기로 사용자가
  최종 승인했다.
- 결정:
  1. `domain/knowledge.py`에 `KnowledgeDocument`(document_id/kind/
     title/content/source_path)/`KnowledgeKind`(ARCHITECTURE/ADR/
     RULE/TASK/PROJECT 5종)를 신설한다. 어떤 Provider/Engine도
     참조하지 않는다.
  2. `interfaces/knowledge_repository.py`에 `KnowledgeRepository`
     (`list_all`/`get`, 읽기 전용)를 신설한다.
     `storage/file_knowledge_repository.py`의 `FileKnowledgeRepository`
     가 고정 파일→kind 매핑으로 파일 하나를 문서 하나로 노출한다
     (문단 단위 파싱 없음, YAGNI).
  3. `interfaces/knowledge_search.py`에 `KnowledgeSearch`(Keyword
     포함 검색)를 신설한다. `KnowledgeIndexer`(영속 Index 자료구조)는
     문서 수가 적어(6개 안팎) 성능 문제가 없어 이번 범위에서
     제외한다(YAGNI, 사용자 승인) — 필요해지면 `KnowledgeSearch`
     계약은 그대로 두고 구현체만 교체 가능(OCP).
  4. `interfaces/knowledge_provider.py`에 `KnowledgeProvider`(Agent가
     의존하는 유일한 진입점)를 신설한다. `ContextManager`가
     `MemoryEngine`을 감싸는 것과 동일한 패턴이다.
  5. `CodingAgent`에 선택적 `knowledge_provider` DI를 추가한다.
     주입 시 `task.title`로 검색한 결과를 `DevelopmentContext.
     related_knowledge`에 실어 프롬프트에 반영하고, 미주입 시
     기존과 완전히 동일하게 동작한다.
  6. `docs/ARCHITECTURE.md` §8 의존성 규칙에 "Agent → Knowledge
     Provider → Knowledge Search → Knowledge Repository" 경로를
     신규 추가한다(기존 규칙 7 "Agent → Context Manager → Memory
     Engine"과 나란히, 완전히 별도의 경로).
- 대안:
  - 기존 `MemoryEngine`을 확장해 Project Knowledge까지 다루게 함 —
    기각. `MemoryEngine.search()`는 세션 요약을 위한 key-value 저장소
    계약이라, 파일 기반 정적 문서(Markdown)를 다루기엔 계약 자체가
    맞지 않고, 두 개념을 섞으면 SRP를 위반한다.
  - `KnowledgeRepository`/`KnowledgeSearch`를 하나의 Interface로
    통합 — 기각(사용자 명시적 요청: "저장/검색/제공 역할을 명확히
    분리해야 합니다"). 저장은 "문서가 어디 있는지", 검색은 "어떻게
    찾는지"로 관심사가 다르며, 향후 검색 알고리즘(예: Semantic
    Search)만 교체하고 싶을 때 Repository는 그대로 둘 수 있어야
    한다.
  - `KnowledgeIndexer`까지 포함해 4개 컴포넌트 전부 구현 — 기각
    (YAGNI). 현재 문서 수로는 매 검색 시 전체를 훑어도 성능 문제가
    없고, 증명되지 않은 성능 요구를 앞서 처리하는 것은 프로젝트
    원칙(YAGNI)에 어긋난다.
  - Vector/Embedding 기반 Semantic Search 도입 — 기각(사용자 명시적
    범위 밖). 초기 구현은 Markdown/Keyword/Index 기반으로 충분하며,
    추후 확장 가능하도록 Interface(`KnowledgeSearch`)만 설계해 둔다.
- 이유: 저장(Repository)/검색(Search)/제공(Provider) 역할을 분리하면
  각 역할을 독립적으로 교체할 수 있다(SOLID의 OCP/SRP) — 예를 들어
  나중에 Semantic Search가 필요해지면 `KnowledgeSearch` 구현체만
  바꾸면 되고, `KnowledgeRepository`나 Agent 쪽 코드는 전혀 손대지
  않는다. `KnowledgeProvider`를 Agent의 유일한 의존 지점으로 두면
  `ContextManager`/`MemoryEngine`과 동일한 패턴이 되어 프로젝트
  전체의 "Agent는 façade Interface만 안다"는 일관된 설계를 유지한다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.18.0 §3.14(신규)/§7(Interfaces
  19→22종)/§8(의존성 규칙 11번 신규)/§9에 반영. `CodingAgent`가
  `knowledge_provider` 주입 시 실제 프로젝트 문서(`docs/
  ARCHITECTURE.md` 등)의 내용을 검색해 프롬프트에 반영함을 실제
  `FileKnowledgeRepository` 기반 통합 테스트로 증명(M16-T03).
  Review/Documentation Agent로의 확장, `KnowledgeIndexer` 도입,
  Semantic Search는 실제 필요성이 증명되기 전까지 이월한다.

## ADR-0029: Intelligent Engine Selection 도입 (EngineRegistry + EngineSelectionPolicy, Decision Only, `EngineRuntime` 계약 미확장) (Milestone 17)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: 사용자가 "Task + Budget(M15) + Project Knowledge(M16) +
  Engine Capability + Selection Policy → 최적 Engine 선택"이라는
  목표로 M17을 요청했다. 설계 검토 결과, `EngineRuntime.run()`/
  `estimate_cost()`는 `required_capabilities`를 만족하는 등록된
  Engine 중 **첫 번째 매칭만** 고르며, 여러 후보를 나열·비교하는
  방법 자체가 없었다 — "선택"이라 부를 로직이 지금까지 없었다.
  사용자는 최종 승인에서 세 조건을 명시했다: (1) M17은 Decision
  Only Milestone으로 유지, (2) `EngineSelectionDecision`에 선택
  이유(`reason`) 포함, (3) 가능하다면 `EngineRuntime.list_candidates()`
  대신 기존 Engine 관리 계층(Registry/Manager)의 조회 기능을
  활용해 조회(Registry)와 판단(Policy)의 책임을 분리. 조사 결과,
  `AgentRegistry`에 대응하는 **Engine Registry는 이 저장소에 존재하지
  않았다**(Engine 등록은 `EngineRuntime.register_engine()` 내부
  dict가 전부였음) — 그래서 "기존 계층 활용"이 아니라 `AgentManager`/
  `AgentRegistry` 분리와 동일한 패턴으로 **신규 계층을 도입**하는
  결정이 됐다.
- 결정:
  1. `domain/engine_selection.py`에 `EngineCandidate`(engine_name/
     capabilities/estimated_tokens/estimated_cost_usd/
     supports_parallel)/`EngineSelectionDecision`(engine_name/model/
     reason)을 신설한다. `CostEstimate`(interfaces 계층)를 그대로
     참조하지 않고 값만 옮겨 담아 domain이 interfaces에 의존하지
     않는 기존 원칙을 유지한다.
  2. `interfaces/engine_registry.py`에 `EngineRegistry`(`register`/
     `get`/`list_candidates`)를 신설한다. **`EngineRuntime`의 실행
     계약(run/estimate_cost)은 전혀 확장하지 않는다** — 기존 3개
     구현체(`InMemoryEngineRuntime`/`ManagedEngineRuntime`/
     `RecoveringEngineRuntime`)의 내부 구현은 손대지 않는다. 후보
     조회가 필요한 쪽이 같은 Adapter를 조립 시점에 `EngineRegistry`
     에도 등록해 별도로 조회한다.
  3. `interfaces/engine_selection_policy.py`에
     `EngineSelectionPolicy`(`select(task, candidates, *,
     budget_policy_engine=None, knowledge=None) ->
     EngineSelectionDecision | None`)를 신설한다. 후보가 어디서
     왔는지는 알지 못한다(조회와 판단의 책임 분리, 사용자 승인
     조건).
  4. `InMemoryEngineSelectionPolicy`는 `budget_policy_engine`이
     주어지면 각 후보로 `CostEstimate`를 만들어 `BudgetPolicyEngine.
     check()`에 위임(M15 재사용, 예산 비교 로직 중복 없음)하고,
     예산 내 최저 비용 후보를 선택한다. `knowledge`는 `reason`에만
     참고로 반영한다(후보를 걸러내지 않음, MVP).
  5. **결정과 실행을 연결하지 않는다** — `CodingAgent`는
     `EngineSelectionPolicy`/`EngineRegistry`를 이번 Milestone에서
     전혀 모른다(생성자 파라미터 없음). 이 경계를 통합 테스트로
     직접 증명한다(다른 Engine을 추천해도 실제 실행은 영향받지
     않음 + `inspect.signature()`로 파라미터 부재 확인).
- 대안:
  - `EngineRuntime.list_candidates()`를 추가 — 사용자가 "가능하다면
    피하라"고 명시. `EngineRuntime`을 M14(model)/M15(estimate_cost)
    에 이어 세 번째로 확장하는 대신, 이번엔 완전히 별도 계층으로
    분리해 `EngineRuntime`의 책임(실행)과 `EngineRegistry`의 책임
    (조회)을 더 명확히 나눴다.
  - `EngineSelectionPolicy`가 직접 `EngineRegistry`를 주입받아 후보를
    스스로 조회 — 기각. Policy가 "어디서 후보를 가져오는지"까지
    알게 되면 조회와 판단의 책임이 다시 섞인다. 호출자가 먼저
    `EngineRegistry.list_candidates()`로 후보를 조회한 뒤 Policy에
    넘기는 2단계 흐름을 유지한다.
  - M17에서 곧바로 `CodingAgent`에 연결해 실제 실행까지 바꿈 —
    기각(사용자 확정 범위 밖, "Decision Only"). 결정 로직과 실행
    로직을 같은 Milestone에서 함께 바꾸면 두 책임이 다시 섞이고,
    "M17=Decision, M18=Execution"이라는 사용자의 책임 분리 의도가
    깨진다.
- 이유: 조회(Registry)/판단(Policy)/실행(Runtime) 세 책임을 분리하면
  각각 독립적으로 교체·검증할 수 있다(SRP). `EngineRuntime`을 건드리지
  않아 기존 3개 실행 구현체에 회귀 위험이 전혀 없다(Surgical
  Changes). Decision과 Execution을 Milestone 단위로 분리하면, M18에서
  "어떻게 연결할지"(예: `CodingAgent`에 선택적 DI로 추가할지, 별도
  조율자를 둘지)를 M17의 판단 로직 변경 없이 독립적으로 검토할 수
  있다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.19.0 신규 §3.15/§7(Interfaces
  22→24종)/§9에 반영. 실제 여러 Engine이 등록된 상태에서 Budget 내
  최저 비용 후보 선택, 예산 초과 후보 제외, 전체 초과 시 `None`,
  실제 `FileKnowledgeRepository` 기반 Knowledge 반영을 통합 테스트로
  증명(M17-T03). "결정과 실행의 분리" 경계는 실제 `CodingAgent`
  파이프라인 실행 결과로 직접 검증했다. Model 수준 결정, ML/휴리스틱
  기반 고급 판단, `EngineRuntime`↔`EngineRegistry` 통합(중복 등록
  제거)은 실제 필요성이 증명되기 전까지 이월한다.

## ADR-0030: Execution Layer 도입 (`ExecutionDispatcher` 구체 클래스 + `AuthenticationManager` Interface), Decision-Execution 완전 분리 (Milestone 18)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: M17의 `EngineSelectionDecision`은 결정만 하고 실제 실행에는
  전혀 연결되지 않았다(의도된 Decision Only 경계). 사용자가 "Task →
  Selection Policy → EngineSelectionDecision → ExecutionDispatcher →
  AuthenticationManager → EngineRegistry → EngineAdapter →
  ExecutionEnvironment → AI Engine 실행 → ExecutionResult" 흐름으로
  M18을 요청했다. 설계 검토 결과, 요청한 새 "ExecutionResult" Domain
  (success/output/error/engine/execution_time)이 M11의
  `interfaces/execution_environment.py`가 이미 쓰고 있는
  `ExecutionResult`(returncode/stdout/stderr — OS 프로세스 결과)와
  이름이 겹친다는 사실을 확인했다. 사용자는 최종 승인에서 네 가지를
  확정했다: (1) 새 Domain은 `EngineExecutionResult`로 명명해 기존
  `ExecutionResult`와 분리, (2) `ExecutionDispatcher`는 Interface가
  아닌 구체 클래스로 구현, (3) 인증 실패는
  `AuthenticationRequiredError` 예외, `SelectionDecision` 부재는
  `EngineExecutionResult(success=False)`로 구분, (4) 이번
  Milestone은 `CodingAgent`를 수정하지 않고 `ExecutionDispatcher`를
  독립적으로 구현·검증.
- 결정:
  1. `domain/execution_result.py`에 `EngineExecutionResult`(success/
     output/error/engine/execution_time, Provider 독립)를 신설한다.
  2. `interfaces/authentication_manager.py`에
     `AuthenticationStatus`(AUTHENTICATED/UNAUTHENTICATED)/
     `AuthenticationRequiredError`/`AuthenticationManager`(`is_
     authenticated`/`authentication_status`만 — `login`/`logout`은
     의도적으로 이 계약에 없음)를 신설한다. "로그인을 수행"하는
     것이 아니라 "실행 가능한 인증 상태인지 확인"만 한다.
     `InMemoryAuthenticationManager`는 생성 시 주어진 "인증된 것으로
     간주할 Engine 이름" 집합만 보관하고, 실제 로그인/OAuth/API Key/
     Credential 저장/Token Refresh는 전혀 다루지 않는다.
  3. `runtime/execution/execution_dispatcher.py`에
     `ExecutionDispatcher`(구체 클래스, M12 `WorkflowRunner`와 동일
     패턴)를 신설한다. `dispatch(decision, task) ->
     EngineExecutionResult`: `decision`이 `None`이면
     `EngineRegistry`/`AuthenticationManager` 어느 쪽도 호출하지
     않고 즉시 실패 결과를 반환하고, 인증되지 않았으면
     `AuthenticationRequiredError`를 던지며, 인증됐으면
     `EngineRegistry.get(decision.engine_name)`으로 정확히 하나의
     `EngineAdapter`만 얻어 실행한다.
  4. `ExecutionDispatcher`는 `EngineRegistry`/`EngineAdapter`/
     `AuthenticationManager` **Interface만** 사용하고 구현체를 직접
     참조하지 않는다(OCP). `EngineSelectionPolicy`는 전혀 참조하지
     않는다(Decision과 Execution의 완전한 분리) — 반대 방향도
     마찬가지로, `EngineSelectionPolicy`의 실제 소스 코드에
     `ExecutionDispatcher` 참조가 없음을 통합 테스트가 직접
     검증한다(M18-T03).
  5. `ExecutionDispatcher`는 `ExecutionEnvironment`를 직접 생성하지
     않는다 — `ClaudeCodeEngineAdapter`가 M11부터 이미 생성자
     주입으로 갖고 있으므로 `EngineAdapter.run()`만 호출하면 된다.
  6. 이번 Milestone은 `CodingAgent`를 수정하지 않는다.
     `ExecutionDispatcher`는 독립적으로 구현·검증하며, Agent
     파이프라인 연결은 후속 Milestone의 책임이다.
- 대안:
  - 새 Domain을 그대로 `ExecutionResult`로 명명 — 기각(이름 충돌).
    M11의 `ExecutionResult`(프로세스 결과)와 이번 `EngineExecutionResult`
    (Engine 실행 결과)는 서로 다른 추상화 층위라, 같은 이름을 쓰면
    "무엇의 결과인지" 코드만 봐서는 알 수 없게 된다.
  - `ExecutionDispatcher`를 Interface로 정의하고 여러 구현체를 허용 —
    기각(사용자 명시적 요청, YAGNI). 이 Dispatcher는 조합 로직
    (Registry 조회 → 인증 확인 → 실행)만 담당하고 교체 가능한 정책이
    아니다 — `WorkflowRunner`가 Interface가 아닌 것과 같은 이유.
  - 인증 실패도 `EngineExecutionResult(success=False)`로 통일 —
    기각. "Decision 없음"은 정상적인 입력(아무것도 선택되지 않음)
    이지만, "선택은 됐는데 인증이 안 됨"은 실행 전제조건 위반이라
    이 저장소가 일관되게 써온 예외 기반 패턴(`NoSuitableEngineError`,
    `SessionNotFoundError` 등)과 맞춘다.
  - M18에서 `CodingAgent`에 바로 연결 — 기각(사용자 확정 범위 밖).
    Decision Only였던 M17에 이어, M18도 "Execution Layer 완성"에만
    집중해 범위를 명확히 유지한다.
- 이유: `ExecutionDispatcher`가 세 Interface(Registry/Adapter/
  Authentication)만 의존하면 새 Engine 추가 시 이 클래스를 전혀
  수정하지 않아도 된다(OCP). Decision과 Execution을 물리적으로
  분리된 두 컴포넌트로 유지하면(서로가 서로를 모름) 어느 한쪽만
  교체·재검증할 수 있다. 인증을 "상태 확인"으로 좁히면 이번
  Milestone은 실행 파이프라인 연결에만 집중할 수 있고, 실제
  로그인/OAuth라는 훨씬 큰 관심사는 후속 Milestone(Authentication
  Layer)으로 명확히 미룰 수 있다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.20.0 신규 §3.16/§7(Interfaces
  24→25종)/§9에 반영. 실제 `ClaudeCodeEngineAdapter`+
  `ExecutionEnvironment`로 실행됨을 통합 테스트로 증명(M18-T03,
  `ExecutionEnvironment.executed_commands`에 실제 명령 기록 확인).
  Task → Selection Policy → Decision → Dispatcher →
  Authentication → Registry → Adapter → ExecutionEnvironment →
  EngineExecutionResult로 이어지는 첫 End-to-End 실행 경로가 완성됐다
  (M11/M15/M16/M17이 실행까지 연결됨). 실제 로그인/OAuth/Credential
  관리/Token Refresh, `CodingAgent` 연결, Retry/Timeout/Recovery/
  Approval/병렬 실행은 실제 필요성이 생기기 전까지 이월한다.

## ADR-0031: Reliability Layer 도입 (`RetryPolicy` 확장 + `RetryExecutor`), `timed_out` 휴리스틱 기술 부채 명시 (Milestone 19)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: M18로 완성된 Execution Layer는 실패를 감지·복구하는 능력이
  없었다. 사용자가 "Task → Selection Policy → Decision →
  ExecutionDispatcher → RetryExecutor → AuthenticationManager →
  EngineRegistry → EngineAdapter → ExecutionEnvironment →
  EngineExecutionResult" 흐름으로 M19를 요청했다. 설계 검토 결과
  세 가지를 확인했다: (1) `domain/retry_policy.py`의 `RetryPolicy`
  (M3)가 이미 존재하고 `RecoveringEngineRuntime`이 "무조건 재시도"
  에 쓰고 있다 — 이번엔 M16/M18과 달리 **같은 개념의 확장**이라
  판단해 새 이름 대신 기존 클래스에 필드를 추가하기로 했다. (2)
  `ClaudeCodeEngineAdapter.run()`은 Timeout과 다른 실행 오류를 모두
  같은 `EngineExecutionError`로 던지고 메시지 텍스트로만 구분되는데,
  "`EngineAdapter` 인터페이스는 변경하지 않는다"는 이번 Milestone의
  제약과 정면으로 부딪힌다 — 완전한 구분이 불가능하다. (3) DoD가
  언급한 `NoSuitableEngineError`(`EngineRuntime` 시절 예외)는 이
  경로에 실제로 나타나지 않는다 — M18이 `EngineRuntime`을 건너뛰고
  `EngineRegistry`를 직접 쓰기 때문에 실제로는
  `EngineNotRegisteredError`가 발생한다. 사용자는 최종 승인에서
  두 조건을 확정했다: `timed_out`은 휴리스틱임을 이 ADR과
  ARCHITECTURE.md에 기술 부채로 명시할 것, `cancelled`는 새 문자열
  규칙을 만들지 않고 `EngineAdapter`가 이미 쓰는 sentinel을 그대로
  이어받을 것.
- 결정:
  1. `domain/retry_policy.py`의 기존 `RetryPolicy`에
     `retry_delay_seconds: float = 0.0`/`non_retryable_exceptions:
     tuple[type[BaseException], ...] = ()`(둘 다 기본값)와
     `decide(exception) -> RetryDecision`을 추가한다. 도메인
     계층은 구체 예외 타입을 몰라도 되도록 `type[BaseException]`
     튜플만 받는다 — 실제 재시도 불가 예외 목록은 호출자
     (`ExecutionDispatcher`)가 구성한다. `RecoveringEngineRuntime`
     의 기존 호출부(모두 `max_attempts`만 지정)는 전혀 영향받지
     않는다.
  2. `RetryDecision`(should_retry/reason)을 신설한다 —
     `EngineSelectionDecision`/`BudgetDecision`과 동일한 명명
     패턴.
  3. `runtime/execution/retry_executor.py`에 `RetryExecutor`(구체
     클래스, 제네릭 `Callable[[], T]`를 받아 재시도)를 신설한다.
     `EngineExecutionResult`를 전혀 알지 못하는 순수 재시도
     메커니즘이다.
  4. `ExecutionDispatcher`는 "인증 확인→`EngineRegistry` 조회→
     `EngineAdapter` 실행" 전체를 한 번의 시도로 묶어
     `RetryExecutor.execute()`에 위임한다(재시도 로직을 직접
     구현하지 않음). 기본 `RetryPolicy`는
     `non_retryable_exceptions=(AuthenticationRequiredError,
     EngineNotRegisteredError, NoSuitableEngineError)`로 구성한다
     — `NoSuitableEngineError`는 이 경로에 실제로 발생하지 않지만
     전방 호환을 위해 포함해 뒀다(해가 없음).
  5. `domain/execution_result.py`의 `EngineExecutionResult`에
     `retry_count: int = 0`/`cancelled: bool = False`/`timed_out:
     bool = False`(전부 기본값, M18 호출부 무영향)를 추가한다.
  6. `EngineExecutionError`가 재시도를 소진하면 예외를 그대로
     전파하는 대신 `EngineExecutionResult(success=False,
     timed_out=<휴리스틱>)`로 변환한다 — `_looks_like_timeout()`이
     Timeout 메시지의 한국어 마커("응답하지 않았습니다") 문자열
     매칭으로만 판정한다. **이것은 알려진 기술 부채다** — Adapter가
     메시지 문구를 바꾸면 이 판정은 깨진다.
  7. 취소는 `EngineResult.error == "cancelled"`(`EngineAdapter`가
     이미 쓰는 sentinel)로 판정하고, 재시도 루프를 타지 않고 즉시
     `cancelled=True`로 반영한다.
- 대안:
  - `RetryPolicy`를 새 이름(예: `ExecutionRetryPolicy`)으로 분리 —
    기각. M16(`MemoryEngine`/Knowledge)·M18(`ExecutionResult`)의
    이름 충돌과 달리, 이번엔 "실행 재시도 정책"이라는 **같은
    개념**을 다루므로 확장이 SRP를 지키면서도 더 단순하다
    (YAGNI — 불필요하게 유사 개념을 두 이름으로 쪼개지 않음).
  - `EngineAdapter` 인터페이스를 확장해 Timeout을 구조적으로 표현
    (예: `EngineExecutionTimeoutError` 서브타입 도입) — 기각(사용자
    확정 범위 밖, "이번 Milestone에서는 EngineAdapter 인터페이스를
    변경하지 않는다"). 근본 해결은 후속 Milestone으로 이월하고,
    이번엔 메시지 기반 휴리스텍으로 최소 기능만 제공하며 한계를
    투명하게 기록한다.
  - `cancelled` 판정에 새로운 전용 필드나 예외 타입 도입 — 기각
    (사용자 확정 조건). `EngineAdapter`가 이미 `error="cancelled"`
    라는 값으로 취소를 인코딩하고 있으므로, 새 규칙을 만들지 않고
    그 값을 그대로 이어받는 것이 최소 변경 원칙에 맞는다.
  - 모든 실행 실패(성공하지 못한 `EngineResult`)를 자동 재시도 —
    기각. DoD의 재시도 대상은 전부 예외 기반(Timeout/Process
    Error)이라, 정상적으로 반환된 실패 결과(예: LLM이 "이 작업은
    할 수 없습니다"라고 응답한 경우)까지 재시도하면 의미 없는
    반복 호출만 늘어난다 — 이번 MVP는 인프라 수준 실패만 재시도
    대상으로 좁혔다.
- 이유: `RetryExecutor`를 제네릭·독립 컴포넌트로 두면
  `ExecutionDispatcher` 외의 다른 곳에서도 재시도가 필요해질 때
  재사용할 수 있다. 재시도 판단을 예외 타입 기반으로 구성 가능하게
  하면(`non_retryable_exceptions`) `ExecutionDispatcher`가 판단
  로직을 직접 갖지 않아도 되고, 정책만 교체하면 재시도 대상을
  바꿀 수 있다(OCP). Timeout 휴리스틱의 한계를 숨기지 않고 ADR과
  ARCHITECTURE.md에 명시적으로 기록해, 향후 `EngineAdapter` 개선
  Milestone에서 이 부채를 해소할 근거를 남긴다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.21.0 신규 §3.17(Reliability)에
  반영(§7 Interfaces는 새 Interface가 없어 25종 그대로 — `RetryExecutor`
  는 구체 클래스, `RetryPolicy`/`RetryDecision`은 domain 확장).
  실제 `ClaudeCodeEngineAdapter`+`ExecutionEnvironment` 조합으로
  Timeout 재시도·소진 후 `timed_out` 반영, Cancellation 즉시 반영을
  통합 테스트로 증명(M19-T03). `EngineAdapter` 구조적 Timeout 신호,
  Backoff 전략 고도화, 다른 컴포넌트(예: `KnowledgeRepository`)로의
  `RetryExecutor` 재사용은 실제 필요성이 생기기 전까지 이월한다.

## ADR-0032: Real-time Dashboard Platform 도입 — `DashboardRepository` Interface, 첫 외부 런타임 의존성(FastAPI/uvicorn), Core-Web 계층 분리 (Milestone 20)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: M11~M19로 완성된 Execution/Reliability 계층은 실행 상태를
  확인할 방법이 CLI 로그뿐이었다. 사용자가 "Task 실행/엔진/안정성
  현황을 실시간으로 보여주는 Dashboard"를 CQRS Read Model로
  요청했다 — Dashboard는 Task를 실행하지 않고 오직 조회만 한다.
  사용자의 3단계 승인으로 설계가 확정됐다: (1) `workspace start`
  서버 런타임 도입, 기존 CLI는 변경 없음. (2)
  `ExecutionDispatcher`에 `event_bus: EventBus | None = None`을
  선택적으로 주입 — `ExecutionDispatcher`는 이벤트만 발행하고
  Dashboard를 직접 참조하지 않으며, `DashboardRepository`가 이벤트를
  구독해 스스로 Read Model을 갱신한다. API/WebSocket/Web UI는
  `DashboardService`만 사용한다. (3) Task 구조를 사용자가 직접
  T01~T07로 확정하고, "Core 계층은 웹 프레임워크를 모르도록
  유지하고, FastAPI는 Infrastructure 계층에서만 사용한다"는 원칙을
  명시했다. AskUserQuestion으로 웹 프레임워크(FastAPI+uvicorn)와
  Web UI 방식(정적 HTML/CSS/Vanilla JS, 빌드 도구 없음)을 확인했다.
- 결정:
  1. `domain/dashboard.py`에 `EngineStatus`(READY/RUNNING/
     AUTH_REQUIRED/ERROR)/`WorkspaceStatus`/`ExecutionRecord`/
     `ExecutionStats`/`ReliabilityStats`를 신설한다. `EngineExecutionResult`
     (M18/M19)를 그대로 참조하지 않고 Dashboard가 필요한 필드만
     옮겨 담는다 — Dashboard는 Execution 계층에 대한 쓰기 접근이
     없는 순수 Read Model이다.
  2. `runtime/execution/events.py`에 `ENGINE_EXECUTION_STARTED`/
     `ENGINE_EXECUTION_COMPLETED`/`ENGINE_AUTHENTICATION_FAILED`
     Event 타입 상수를 신설한다. `ExecutionDispatcher`는 이 Event를
     발행하기만 하고 누가 구독하는지 모른다.
  3. `interfaces/dashboard_repository.py`에 `DashboardRepository`
     Interface(신규 26번째 Interface)를 신설한다 —
     `record_execution_started`/`record_execution_completed`/
     `record_authentication_failure`(쓰기, Event 구독 경로 전용)와
     `workspace_status`/`engine_statuses`/`recent_executions`/
     `execution_stats`/`reliability_stats`(읽기, `DashboardService`
     경로 전용)로 CQRS 쓰기/읽기 메서드를 한 Interface 안에 함께
     정의한다 — 구현체가 하나(`InMemoryDashboardRepository`)뿐이고
     내부적으로 같은 상태를 갱신·조회하므로 Interface를 둘로
     쪼개는 것은 과설계로 판단했다.
  4. `runtime/dashboard/dashboard_repository.py`의
     `InMemoryDashboardRepository`가 생성자에서 스스로
     `event_bus.subscribe()`한다(`ExecutionDispatcher`는 이 클래스의
     존재를 모름). 통계(`ExecutionStats`/`ReliabilityStats`)는 조회
     시점에 계산하지 않고 매 Event마다 미리 갱신해 둔다("Dashboard는
     통계를 계산하지 않는다", 사용자 설계 원칙) — `_RECENT_EXECUTIONS_KEPT
     = 100`으로 이력을 제한한다.
  5. `runtime/dashboard/dashboard_service.py`의 `DashboardService`는
     `DashboardRepository`를 조합해 조회 요청에 응답하는 순수
     서비스다 — `web/`을 전혀 import하지 않는다(M20-T06에서 `ast`
     기반 의존성 검증으로 증명). `KNOWN_ENGINES` 목록으로 아직 한
     번도 실행되지 않은 Engine도 기본 상태(`READY`)로 표시한다.
  6. `web/`(신규 최상위 패키지, Infrastructure 계층)에
     `DashboardViewModel`(한국어 라벨 DTO,
     `DashboardService`/`domain`은 이 타입을 모름) +
     `DashboardBroadcaster`(WebSocket 연결 관리 + `EventBus` 구독 +
     `asyncio.get_running_loop()`를 연결 시점에 캡처해
     `loop.call_soon_threadsafe()`로 동기 이벤트 콜백에서 비동기
     전송을 예약) + FastAPI `routes.py`(`/api/dashboard`,
     `/api/summary`, `/api/history`, `/api/engines`) + `app.py`
     (`create_app`, `/health`, `/ws/dashboard`, `StaticFiles` 정적
     마운트) + `server.py`(`build_app`/`run_server`) + `static/`
     (`index.html`/`style.css`/`app.js`, 빌드 도구 없는 Vanilla JS)
     를 둔다. 현재 시각·경과 시간(`현재 시각 - started_at`)은
     브라우저가 1초마다 직접 계산한다 — 서버는 Polling하지 않는다.
  7. `pyproject.toml`에 이 프로젝트 최초의 외부 런타임 의존성
     `fastapi>=0.115`/`uvicorn[standard]>=0.30`을 추가한다(기존엔
     `pyyaml`뿐이었다). dev 의존성에 `httpx`(`TestClient`용)를
     추가한다. `domain`/`interfaces`/`engines`/`runtime`(단, `runtime/
     dashboard/`도 포함)은 FastAPI/uvicorn을 import하지 않는다 —
     오직 `web/`만 이 두 패키지를 안다.
  8. `cli/main.py`에 `start` 서브커맨드(`--host`/`--port`)를
     추가하되, `web.server.run_server`를 지연 import한다 — 다른
     기존 CLI 명령은 FastAPI/uvicorn 설치 여부와 무관하게 동작한다.
- 대안:
  - `DashboardRepository`를 쓰기 전용/읽기 전용 두 Interface로 분리
    (엄격한 CQRS) — 기각. 구현체가 하나뿐이고 내부 상태를
    공유하므로 분리는 간접 계층만 늘리고 실질적 이득이 없다(YAGNI).
    필요해지면(예: 쓰기와 읽기가 물리적으로 다른 저장소를 쓰게
    되면) 이 ADR을 갱신해 분리한다.
  - `ExecutionDispatcher`가 `DashboardRepository`를 직접 호출 —
    기각(사용자 확정 조건). Event 기반 간접 결합을 유지해야
    `ExecutionDispatcher`가 Dashboard의 존재 여부와 무관하게 독립적
    으로 테스트·재사용 가능하다.
  - WebSocket 갱신 대신 클라이언트 Polling — 기각(사용자 명시 요구
    "Repository를 Polling하지 않는다"). Event 발생 시점에만 갱신을
    밀어 불필요한 요청을 없앤다.
  - React/Vue 등 빌드 도구 기반 Web UI — 기각(사용자 선택). 이
    프로젝트 규모에서는 정적 HTML/CSS/Vanilla JS로 충분하고, 빌드
    파이프라인을 새로 들이는 비용이 더 크다.
- 이유: CQRS(쓰기는 Event, 읽기는 Service 메서드)로 Dashboard가
  Execution 계층에 어떤 결합도 강제하지 않으면서 실시간성을
  얻는다. `DashboardService`가 `web/`을 모르게 유지하면, 동일한
  Read Model을 향후 다른 Presentation(M23 Mobile 등)이 재사용할 수
  있다. FastAPI/uvicorn을 `web/`에만 가두면 Core 계층의 프레임워크
  독립성(이 프로젝트가 M1부터 지켜온 원칙)이 첫 외부 런타임
  의존성 도입에도 깨지지 않는다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.22.0 신규 §3.18(Real-time
  Dashboard Platform)에 반영, §7 Interfaces 26종으로 갱신
  (`DashboardRepository` 추가), §8 의존성 규칙에 Dashboard Event
  구독 경로 추가, §9 디렉터리 구조에 `runtime/dashboard/`/`web/`
  반영. 실제 `ClaudeCodeEngineAdapter` 실행 결과가 Event → Repository
  → Service → REST API/WebSocket까지 그대로 반영됨을 통합 테스트로
  증명(M20-T06). `DashboardRepository` 쓰기/읽기 분리, 실제
  프로덕션 배포 구성(HTTPS/인증/역방향 프록시), M23 Mobile
  Presentation은 실제 필요성이 생기기 전까지 이월한다.
