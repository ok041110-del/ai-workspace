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

## ADR-0033: Automation Engine 도입 — `AutomationRepository` Interface, 기존 `AutomationEngine`과의 명시적 분리, Reader→Reader CQRS 확장 (Milestone 21)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: M20으로 완성된 Dashboard는 실행 상태를 "보여주기"만 했다.
  사용자가 "조건/일정에 따라 Task를 자동 실행하는 Automation"을
  `AutomationRule → AutomationRepository → AutomationService →
  AutomationScheduler → ExecutionDispatcher → EventBus → Dashboard`
  흐름으로 요청했다. 설계 검토에서 M4-T07에 이미 `AutomationEngine`
  Interface + `InMemoryAutomationEngine`이 존재함을 발견했다 — 하지만
  그 책임은 "어떤 trigger가 어떤 Workflow와 연결돼 있는가"만 관리하는
  **연결 관리**뿐이고, trigger가 **언제** 발동해야 하는지 판단하는
  조건/일정 평가와 실제 실행은 M4-T07 설계 당시부터 명시적으로
  호출자에게 떠넘겨져 있었다. M21이 요청한 `AutomationRule`(4종
  Trigger+Action)과 `AutomationScheduler`(실제 일정 평가+자동 실행)
  는 바로 그 떠넘겨진 책임을 처음 구현하는 것이라, M16
  `KnowledgeRepository`/M18 `EngineExecutionResult`와 같은 "이름은
  유사하지만 다른 개념" 패턴으로 판단해 새 컴포넌트 세트를 도입하기로
  했다(기존 `AutomationEngine`은 수정 없이 그대로 유지). 사용자는
  최종 승인에서 6개 조건을 확정했다: (1) `AutomationScheduler`와
  Trigger의 책임을 분리한다, (2) Dashboard는 계속 Read Model을
  유지한다, (3) Automation CRUD는 Automation API를 통해서만
  수행한다, (4) Dashboard는 Automation을 직접 제어하지 않는다, (5)
  `ExecutionDispatcher`를 유일한 실행 진입점으로 유지한다, (6)
  `last_executed_at`/`next_execution_at`을 도메인 모델에 포함해 M23
  Mobile Experience와 자연스럽게 연계한다.
- 결정:
  1. `domain/automation.py`에 `TriggerKind`(TIME/INTERVAL/EVENT/
     STARTUP)/`Trigger`/`ActionKind`(RUN_TASK/RUN_WORKFLOW/
     DASHBOARD_REFRESH/NOTIFICATION)/`Action`을 kind로 태그된 Flat
     구조로 정의한다(`ExecutionRecord`(M20)와 동일 스타일 — Trigger/
     Action은 종류별로 필드 모양이 크게 달라 "언제/무엇을" 판단
     로직과 무관하게 순수 데이터로만 존재한다). `AutomationRule`은
     `last_executed_at`/`next_execution_at`을 포함하고(사용자 승인
     조건 6) `enable()`/`disable()`을 갖는 가변 엔티티(`Task`와
     동일 패턴)다.
  2. `interfaces/automation_repository.py`에 `AutomationRepository`
     (신규 27번째 Interface, `get`/`save`/`delete`/`list_rules` —
     `ProjectRepository`와 동일한 upsert 스타일)를 신설한다.
  3. `runtime/automation/`에 `InMemoryAutomationRepository`(저장),
     `AutomationService`(CRUD 유일 진입점, 사용자 승인 조건 3),
     `TriggerEvaluator` 계층(`TimeTriggerEvaluator`/
     `IntervalTriggerEvaluator`/`StartupTriggerEvaluator`/
     `EventTriggerEvaluator` — "언제 발동할지" 판단을 전담),
     `AutomationScheduler`(오케스트레이션만 — Trigger 평가는
     `TriggerEvaluator`에 위임, 사용자 승인 조건 1)를 신설한다.
     `AutomationScheduler`는 Rule을 별도로 등록/보관하지 않고 매
     호출마다 `AutomationRepository`를 다시 조회한다 — `Automation
     Service`가 같은 Repository로 CRUD하면 자동 반영되어 별도 동기화
     계층이 필요 없다.
  4. `AutomationActionExecutor`(신규, `runtime/automation/`)가
     RUN_TASK Action을 M17/M18 파이프라인(`EngineSelectionPolicy.
     select()` → `ExecutionDispatcher.dispatch()`)에 그대로 실어
     실행한다(사용자 승인 조건 5, 새 실행 경로를 만들지 않음).
     `AutomationScheduler`는 이 실행기를 `action_executor:
     Callable[[AutomationRule], None]`로 주입받을 뿐
     `ExecutionDispatcher`를 알지 못한다. RUN_WORKFLOW는 이번
     Milestone이 Task 단위 실행 경로만 다루므로
     `AutomationActionNotSupportedError`로 명시적으로 아직 지원하지
     않는다(향후 Milestone 이월).
  5. Event Trigger는 `AutomationScheduler.bind_event_bus(event_bus)`
     로 `EventBus`를 구독해 처리한다(Automation은 EventBus를 그대로
     재사용한다는 사용자 요구). Rule 실행(`action_executor` 호출)
     실패는 `InMemoryEventBus.publish()`와 동일한 원칙으로
     `try/except Exception: pass`로 삼켜 다른 Rule 평가나 호출자에
     영향을 주지 않는다 — `last_executed_at`은 "실행 시도 시점"만
     기록한다.
  6. Dashboard 연계는 **Reader가 다른 Reader를 참조하는 방식**으로
     확장한다: `DashboardService`가 선택적으로 `automation_service`
     를 주입받아(M15/M16과 동일한 선택적 DI 패턴) 등록/활성 Rule
     수와 마지막/다음 실행 시각을 `AutomationService.list_rules()`
     (읽기 전용)로만 조회해 집계한다(사용자 승인 조건 4 — Dashboard
     는 Automation을 제어하지 않는다). `ExecutionDispatcher`(Writer)
     가 Dashboard를 직접 참조하는 것은 여전히 금지된다 — CQRS
     경계는 "쓰기측이 읽기측을 모른다"는 방향으로만 유지된다.
  7. Automation API(`web/automation_routes.py`) 8종을 신설하고,
     `AutomationScheduler.run_now(rule_id)`(Trigger 조건 무시,
     즉시 발동)를 추가해 `POST /{id}/run`이 위임한다. `web/app.py`
     의 `create_app()`을 `lifespan` Context Manager로 전환해(기존
     `on_event` 대신) 서버 기동 시 `AutomationScheduler.start()`
     (Startup Trigger 1회)를 호출하고, 서버 생존 동안
     `automation_tick_seconds`(기본 30초)마다 `tick()`을 도는
     백그라운드 asyncio Task를 두어 "Scheduler는 Server Runtime과
     함께 실행된다"는 DoD를 충족한다.
- 대안:
  - 기존 `AutomationEngine`을 확장(M19 `RetryPolicy` 패턴처럼) —
    기각. `AutomationEngine`은 "trigger_id↔Workflow 연결 관리"라는
    좁고 다른 책임을 갖고, `bind_workflow`/`fire`의 계약(즉시 반환,
    실행은 호출자 책임)이 M21이 요구하는 "조건 평가+자동 실행"과
    근본적으로 다르다 — 억지로 확장하면 한 Interface가 두 가지
    무관한 책임을 지게 된다(SRP 위반).
  - `AutomationScheduler`가 Rule을 자체 목록으로 등록/관리(사용자
    프롬프트의 "Rule 등록/제거/활성화/비활성화" 문구를 문자 그대로
    별도 API로 구현) — 기각. `AutomationService`(CRUD 유일
    진입점, 조건 3)와 책임이 중복되고 두 컴포넌트의 상태가 어긋날
    위험이 생긴다. 매 호출마다 공유 `AutomationRepository`를
    재조회하면 문구가 요구하는 "효과"(등록/제거/활성화가 Scheduler
    동작에 반영됨)는 동일하게 달성하면서 이중 관리를 없앤다.
  - RUN_WORKFLOW를 `WorkflowRunner`(M12)로 연결 — 기각(이번
    Milestone 범위 밖). `ExecutionDispatcher`를 유일한 실행
    진입점으로 못박은 조건과 정합성을 유지하려면 Workflow 실행
    경로도 이 원칙 안에서 설계해야 하는데, 이번 Milestone에서는
    그 설계까지 확정하지 않았다 — 억지로 연결하면 "유일한 진입점"
    원칙이 두 갈래로 쪼개진다. 명시적 예외로 남겨 후속 Milestone의
    판단 대상으로 이월한다.
- 이유: Trigger 평가를 `TriggerEvaluator`로 분리하면 새 Trigger
  종류(예: Cron 표현식)가 필요해져도 `AutomationScheduler`를 건드리지
  않고 평가기만 추가하면 된다(OCP). `AutomationScheduler`가 Rule
  상태를 자체 보관하지 않고 매번 Repository를 재조회하는 설계는
  "CRUD는 오직 API를 통해서만"이라는 사용자 조건을 코드 구조로
  강제한다 — Scheduler를 우회해 Rule을 바꿀 방법이 없다.
  `last_executed_at`/`next_execution_at`을 도메인에 내장해 두면
  향후 M23 Mobile이 별도 계산 없이 그대로 표시할 수 있다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.23.0 신규 §3.19(Automation
  Engine)에 반영, §7 Interfaces 27종으로 갱신(`AutomationRepository`
  추가), §8 의존성 규칙에 Automation Event 구독 경로 + Dashboard의
  선택적 Automation 조회 추가, §9 디렉터리 구조에 `runtime/
  automation/`/`web/automation_routes.py` 반영. 실제
  `ClaudeCodeEngineAdapter` 조합으로 Event Trigger가 실제 Task
  실행까지 이어짐과, REST API로 만든 Rule이 Dashboard Automation
  현황에 반영됨을 통합 테스트로 증명(M21-T07). `ast` 기반 import
  검사로 Automation Core가 `web/`을 모르고, `ExecutionDispatcher`가
  Automation을 모른다는 단방향 결합도 재확인. RUN_WORKFLOW 실행
  경로, `AutomationRepository`의 파일/DB 구현체, Cron Expression
  기반 Trigger, Distributed/Multi-node Scheduler는 실제 필요성이
  생기기 전까지 이월한다.

## ADR-0034: Production Platform 도입 — `ProductionConfig`/`LifecycleManager`/`HealthMonitor`, Dashboard Reader→Reader 확장, `TYPE_CHECKING` 지연 import로 순환 의존 회피 (Milestone 22)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: M20/M21로 완성된 Dashboard/Automation은 실행 상태는
  보여줬지만 서버 자체의 운영 정보(설정/생명주기/상태/버전)는
  다루지 않았다. 사용자가 "AI Workspace를 실제 운영 가능한
  Production Platform으로 확장한다 — 비즈니스 로직은 추가하지
  않는다"는 목표로 M22를 요청했다. 사용자 최종 승인 조건 5개:
  (1) Configuration은 Infrastructure Layer의 Immutable 설정 객체로
  유지, (2) `LifecycleManager`는 생성이 아닌 생명주기(Startup/
  Shutdown)만 관리, (3) `HealthMonitor`는 조회 전용(Read Model)으로
  유지, (4) Dashboard Health는 기존 `DashboardService`를 확장하여
  구현, (5) `uptime`/`started_at`/`version`/`health_status`를
  표준 상태 정보로 제공해 M23이 재사용할 수 있도록 함. Kickoff
  논의에서 추가로 확정한 사항: Version API는 `pyproject.toml`의
  아키텍처 기준선 버전(ADR-0024)과 다른 별도 상수로 관리, Health
  Monitor의 "Engine" 항목은 `EngineRegistry` Interface를 확장하지
  않고 구조적 연결 여부만 확인, Configuration/Lifecycle/Health는
  `runtime/production/`(FastAPI를 모름)에, 실제 REST 엔드포인트는
  `web/production_routes.py`에 배치, Graceful Shutdown은 별도
  계측 없이 기존 `DashboardService.workspace_status()`(M20이
  이미 Event로 추적)를 폴링해 구현.
- 결정:
  1. `runtime/production/config.py`에 `ProductionConfig`(frozen
     dataclass — `host`/`port`/`log_level`/`dashboard_enabled`/
     `automation_enabled`/`automation_tick_seconds`/
     `engine_settings`, `__post_init__`에서 값 검증)를 신설한다.
     `runtime/production/config_loader.py`의
     `load_production_config(config_path=, env=)`가 기본값→설정
     파일(YAML)→Environment Variable(`AI_WORKSPACE_` 접두사) 순으로
     겹쳐 쓴다 — `storage/llm_policy_loader.py`와 동일하게 "로더만
     PyYAML/`os.environ`을 안다" 원칙을 지킨다.
  2. `runtime/production/logging_setup.py`의 `configure_logging()`
     이 `ProductionConfig.log_level`로 표준 `logging.Logger`
     (`ai_workspace`)를 설정한다(Console 항상 켜짐, `log_file` 선택
     지원). `domain`/`interfaces`/`engines`는 이 모듈을 참조하지
     않는다 — "Logging은 Domain에 침투하지 않는다"(사용자 원칙).
  3. `runtime/production/lifecycle.py`의 `LifecycleManager`
     (STARTUP/RUNNING/SHUTDOWN)는 이미 조립된
     `AutomationScheduler`/`DashboardService`를 선택적으로
     주입받을 뿐 스스로 컴포넌트를 만들지 않는다(사용자 승인 조건
     2). `startup()`이 `started_at`을 기록하고 `AutomationScheduler.
     start()`(Startup Trigger 1회)를 호출한다. `shutdown()`(비동기)
     은 `DashboardService.workspace_status()`를 폴링해 실행 중
     Task가 끝나길 기다리되, `graceful_shutdown_timeout_seconds`를
     넘기면 **강제로 개입하지 않고** 그대로 진행한다(사용자 DoD
     "강제 종료를 수행하지 않는다").
  4. `runtime/production/health.py`의 `HealthMonitor`는 조회
     전용이다(사용자 승인 조건 3) — Server(`LifecycleManager.
     state` 기반)/Dashboard/Automation/EventBus/Engine 5개
     컴포넌트를 각각 "연결돼 있는가"로 판정하고 가장 나쁜 상태로
     전체 `health_status`를 집계한다. Engine 항목은 `EngineRegistry`
     Interface를 확장하지 않고 구조적 연결 여부만 본다(Kickoff
     합의). `ProductionStatus`에 사용자 승인 조건 5의 4개 표준
     필드(`health_status`/`version`/`started_at`/`uptime_seconds`)
     를 담는다.
  5. `runtime/production/version.py`에 `WORKSPACE_VERSION`(제품
     릴리스 버전, `pyproject.toml`의 아키텍처 기준선 버전과 별개)
     과 `get_git_commit_hash()`(실패 시 `None`, git 저장소가 아니어도
     Version API가 항상 동작)를 신설한다.
  6. Dashboard Health는 **기존 `DashboardService`를 확장**해
     구현한다(사용자 승인 조건 4) — 선택적 `health_monitor` DI +
     `production_status()`(M21 `automation_service` DI와 동일한
     Reader→Reader 패턴). `DashboardSnapshot`/`DashboardViewModel`
     에 `production_status` 필드를 추가(기본값 `None`)해 `/api/
     dashboard`·`/api/summary`에 자동 포함시킨다.
  7. **순환 의존 처리**: `HealthMonitor`/`LifecycleManager`가 타입
     힌트로만 `DashboardService`를 참조하도록(`from __future__
     import annotations` + `TYPE_CHECKING` 가드) 바꿔, `dashboard_
     service.py` → `health.py`/`lifecycle.py` → `dashboard_
     service.py`로 되돌아오는 런타임 순환 import를 없앴다. 또한
     `HealthMonitor` 생성에는 이미 만들어진 `DashboardService`가
     필요하지만 `DashboardService`도 `HealthMonitor`를 참조하고
     싶어 하는 조립 순서 문제는 `DashboardService.
     attach_health_monitor(health_monitor)`(생성 후 연결)로
     풀었다 — 실제 순환 의존이 아니라 순수한 조립 순서 문제임을
     이 ADR과 코드 주석에 명시적으로 기록한다.
  8. Production API(`web/production_routes.py`)는 `GET /api/health`
     (컴포넌트별 상세)/`GET /api/config`(`ProductionConfig` 그대로,
     비밀값 없음)/`GET /api/version`/`GET /api/status`(사용자 승인
     조건 5의 4개 표준 필드만 담은 경량 요약 — M23이 그대로 재사용
     하도록 `/api/health`의 상세 `components`와 분리) 4종을
     제공한다. `web/app.py`의 `create_app()`은 `production_config`/
     `lifecycle_manager`/`health_monitor` 3개 모두 주입해야만
     Production 라우터를 등록한다(기존 M20/M21 호출부 무영향).
     `lifecycle_manager`가 주어지면 `lifespan`이 `automation_
     scheduler.start()`를 직접 호출하는 대신 위임하고, 종료 시
     `await lifecycle_manager.shutdown()`(Graceful Shutdown)을
     tick Task 취소보다 먼저 수행한다.
  9. `web/server.py`의 `build_app()`이 `config` 미지정 시
     `load_production_config()`로 채우고 Production 컴포넌트까지
     전부 조립한다. `run_server()`는 CLI `host`/`port`가 주어지면
     Configuration보다 우선(가장 구체적인 값)하고, `configure_
     logging()`을 호출한 뒤 `uvicorn.run()`한다. `cli/main.py`의
     `start` 서브커맨드 `--host`/`--port` 기본값을 하드코딩된
     문자열에서 `None`으로 바꿔 미지정 시 Configuration이 살아
     있게 했다.
- 대안:
  - `LifecycleManager`가 컴포넌트까지 직접 조립 — 기각(사용자 확정
    조건). `web/server.py`의 `build_app()`이 여전히 유일한 조립
    지점으로 남아야 "조립 로직이 여러 곳에 흩어지는" 문제를 막는다.
  - `HealthMonitor`가 `EngineRegistry`에 새 조회 메서드를 추가해
    등록된 Engine 개수/이름까지 점검 — 기각(Kickoff 합의). 아직
    실제 Engine이 등록되지 않는 알려진 한계(M21 Review) 위에 새
    Interface 계약을 얹는 것은 시기상조라고 판단했다 — 실제 Engine
    등록이 이뤄지는 후속 Milestone에서 재검토한다.
  - Version API가 `pyproject.toml`의 `version`을 그대로 재사용 —
    기각. 그 값은 ADR-0024가 관리하는 "아키텍처 기준선 버전"이라
    Milestone이 끝날 때마다 반드시 바뀌는 값이 아니고, 사용자 예시
    (`2.0.0`)가 가리키는 "제품 릴리스 버전"과 의미가 다르다 — 두
    개념을 억지로 합치면 어느 한쪽이 오염된다.
  - `DashboardService`↔`HealthMonitor`의 순환 참조를 완전히 없애기
    위해 Dashboard Health를 별도 독립 컴포넌트로 분리 — 기각(사용자
    확정 조건 4, "기존 DashboardService를 확장"). `TYPE_CHECKING`
    지연 import + `attach_health_monitor()`로 실제 순환 import 없이
    확장 요구를 그대로 만족시킬 수 있어, 사용자 조건을 어기지 않고
    문제를 해결했다.
- 이유: Configuration을 불변으로 유지하면 서버 실행 중 예기치 않게
  설정이 바뀌는 버그 클래스를 원천 차단한다. `LifecycleManager`/
  `HealthMonitor`를 각각 "생명주기만"/"조회만"으로 좁혀 두면 두
  컴포넌트의 책임이 겹치지 않고, 향후 실제 프로덕션 배포 요구
  (Docker/K8s/HTTPS 등, 이번엔 Out of Scope)가 들어와도 이 경계
  안에서 확장할 수 있다. Dashboard Health를 별도 API 대신 기존
  `DashboardService`의 확장으로 구현하면 Web UI/모바일이 한 번의
  `/api/dashboard` 호출로 Workspace/Engine/실행/Automation/
  Production 상태를 전부 받을 수 있어 M23 Mobile Experience의
  API 설계 부담을 줄인다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.24.0 신규 §3.20(Production
  Platform)에 반영. §7 Interfaces는 새 Interface가 없어 27종
  그대로(`ProductionConfig`/`LifecycleManager`/`HealthMonitor`
  전부 구체 클래스/dataclass) — M19에 이어 "새 Interface 없이도
  DoD가 요구해 ADR을 작성"한 두 번째 사례. §8 의존성 규칙에
  Production 관련 경로 추가, §9 디렉터리 구조에 `runtime/
  production/`/`web/production_routes.py` 반영. 실제
  `ClaudeCodeEngineAdapter`+`ExecutionDispatcher`+`uvicorn`
  lifespan 조합으로 서버 기동→Healthy 전이, Graceful Shutdown이
  실행 중 Task를 실제로 기다림, Environment Variable이 실제
  `/api/config`까지 전달됨을 통합 테스트로 증명(M22-T07). `ast`
  기반 import 검사로 `runtime/production/`이 `web/`을 모르고,
  Core Domain(`domain`/`interfaces`/`engines`)이 Production을
  전혀 모르며, `LifecycleManager`가 구체 구현체를 직접 생성하지
  않음을 재확인. Docker/Kubernetes/CI/CD/HTTPS/Reverse Proxy/
  Database/Authentication/Authorization/Multi-node Cluster/
  Mobile 관련 위젯류는 실제 필요성이 생기기 전까지 이월한다.

## ADR-0035: Vault Integration Layer 도입 — `vault/` 신규 패키지(Path Map/Markdown Generator/Vault Writer/Document Router), Core Domain·`web/`과 완전 독립 (Milestone 23, M23-T02)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: M23-Preparation(Obsidian Knowledge Base 구축)으로
  `Vault/`가 만들어진 뒤, 매 Task 완료마다 AI(Claude)가 관련 Vault
  문서 여러 개를 수작업으로 열어 Backlink/Tag/"원문" 섹션 규칙을
  손으로 맞춰 편집해 왔다. 사용자가 Milestone 23을 "Mobile
  Experience"에서 **"Obsidian Integration & Auto Save"**로
  재정의하고(M23-T02~T07 Task List 제시), Retrieval First를
  유지하면서 이 수작업을 표준화된 구조로 대체할 것을 요청했다.
  이번 ADR은 M23-T02(Obsidian Integration Architecture)의 산출물로,
  실제 구현(Markdown 생성/저장 엔진, Auto Save Workflow, Vault
  Synchronization, 자연어 명령 라우팅, 실행 환경 연동)은 M23-T03~
  T07에서 후속 ADR·구현으로 진행한다.
- 결정:
  1. **패키지 위치**: `src/ai_workspace/vault/`를 새 최상위
     패키지로 신설한다 — `storage/`(JSON 기반 도메인 영속성)와
     나란히 존재하되 대상이 다르다(`storage/`는 도메인 객체를
     JSON으로, `vault/`는 Task/ADR/Decision/Design/Implementation/
     API 등 산출물을 Markdown으로). Core Domain(`domain`/
     `interfaces`/`engines`)과 `web/`(FastAPI) 양쪽 모두 이 패키지를
     알지 못한다 — Production Platform(ADR-0034)이 지킨 "Core
     Domain은 자신 위의 계층을 모른다" 원칙을 그대로 적용해,
     `vault/`도 아래 계층(Core Domain)에 의존하지 않고 GitHub
     원문(`.ai/TASKS.md`, `.ai/DECISIONS.md`, `.ai/MEMORY.md`,
     `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`)과 `Vault/` 디렉터리
     양쪽만 다루는 독립 계층으로 둔다. **새 Core Interface를
     추가하지 않는다**(Production Platform과 동일한 판단 — 이
     계층은 비즈니스 로직이 아니라 문서 동기화 도구다).
  2. **Vault Directory Mapping**: 문서 종류(kind) → Vault 디렉터리
     고정 매핑을 코드가 아니라 데이터(모듈 상수 딕셔너리)로
     관리한다 — `AI_RULES`의 Tag Rule 11종과 1:1 대응.
     ```
     "adr"            -> "03 ADR/ADR Index.md"            (append)
     "decision"       -> "12 Decisions/Decisions Index.md" (append)
     "backend"        -> "04 Backend/Backend Index.md"     (append)
     "api"            -> "05 API/API Catalog.md"           (append)
     "dashboard"      -> "06 Dashboard/Dashboard Index.md" (append)
     "automation"     -> "07 Automation/Automation Index.md" (append)
     "production"     -> "08 Production/Production Index.md" (append)
     "ios"            -> "09 iOS/iOS Design.md"            (append)
     "android"        -> "10 Android/Android Placeholder.md" (append)
     "milestone"      -> "11 Milestones/Milestones Index.md" (append)
     "daily"          -> "13 Daily/{{YYYY-MM-DD}}.md"      (create)
     "architecture"   -> "02 Architecture/Architecture Overview.md" (append)
     "system"         -> "00 System/"                      (수동, 자동 대상 아님)
     ```
     `Template - X.md`가 있는 kind(ADR/Decision/Milestone/API/Daily)
     는 append 시 그 Template 형식을 그대로 채운다(Template First).
  3. **Save Flow(4단계 파이프라인)**:
     ```
     구조화 입력(kind, title, summary, related_docs, source_paths)
       → Document Router(kind → 대상 파일 + append/create 결정)
       → Markdown Generator(해당 Template로 렌더링 — frontmatter
         tags/Backlink `[[...]]`/"원문" 섹션 고정 포함)
       → Vault Writer(파일 생성 또는 기존 파일의 대상 절만 교체,
         전체 파일 재작성 금지)
     ```
     구조화 입력은 AI(Claude Code 세션)가 GitHub 원문을 수정한
     직후 Standard Workflow 5단계(Document Update)의 일부로 채운다
     — 자연어 생성이 아니라 이미 결정된 값(제목/요약/관련 문서)을
     고정 스키마에 담아 넘긴다(Minimum Retrieval과 동일하게, Vault
     저장도 "필요한 만큼만" 자동화한다).
  4. **File Strategy**: 신규 문서(Daily 등)는 File Creator로 전체
     파일을 만들고, 기존 Index 문서(ADR Index 등)는 File Updater가
     해당 문서 안의 **대상 섹션만** 문자열 치환하거나 말미에
     추가한다 — 문서 전체를 매번 다시 생성하지 않아 사람이 수동으로
     추가한 절/주석이 보존된다(기존 M23-Preparation 문서들이 전부
     수작업으로 쓰였다는 사실을 존중). 저장 전후로 원본을 비교해
     실제 내용이 바뀔 때만 파일을 쓴다(불필요한 diff 방지).
  5. **Metadata 처리**: frontmatter `tags`는 Tag Rule 11종 중
     kind에 대응하는 값을 자동 채우고, 이미 존재하는 태그는
     보존한다(중복 제거만 수행, 임의 태그 추가/삭제 없음). "원문"
     섹션은 항상 GitHub Link Rule에 따라 경로만 적는다(URL 전체
     금지).
  6. **범위 밖(M23-T02 시점)**: Markdown Generator/Vault
     Writer/Document Router의 실제 코드 구현(M23-T03), Task 완료
     시 자동 트리거(M23-T04), Rename/Delete/Conflict/Version
     정책(M23-T05), 자연어 명령 라우팅(M23-T06), Claude Code/
     Filesystem/MCP 실제 연동 검증(M23-T07)은 이 ADR의 결정
     범위가 아니다 — 각 후속 Task에서 별도로 설계·구현한다.
- 대안:
  - `vault/`를 `storage/` 안에 서브모듈로 두기 — 기각. `storage/`는
    Core Domain 객체(Project/Agent/Event 등)의 JSON 영속성을
    담당하는 계층으로 이미 명확한 책임을 갖고 있어, 성격이 다른
    Markdown/Vault 동기화를 섞으면 "이름은 storage인데 무엇을
    저장하는지 매번 확인해야 하는" 계층이 된다.
  - Obsidian MCP로 직접 실시간 연동(Vault를 라이브로 읽고 쓰기) —
    기각(M23-Prep-T08 Optional의 결정을 그대로 유지). 이 저장소는
    여전히 텍스트 파일 기반 Git 저장소이므로, MCP 없이도 파일
    쓰기 + git 커밋만으로 "자동 저장"의 목표(사람이 수작업으로
    여러 파일을 편집하지 않는 것)를 달성할 수 있다. MCP는 Claude
    Code 도입 시점으로 이월 유지.
  - Vault 문서를 매번 전체 재생성 — 기각. Index 문서는 과거 Task가
    수작업으로 채운 내용을 포함하고 있어, 전체 재생성은 그 내용을
    잃을 위험이 있다(File Strategy 결정 4).
- 이유: Core Domain·`web/` 양쪽으로부터 완전히 독립된 계층으로
  두면 이 기능이 실패하거나 나중에 통째로 교체되어도(예: MCP 기반
  실시간 연동으로 전환) AI Workspace 제품 자체(멀티 에이전트
  오케스트레이션)에는 영향이 없다 — Vault 자동화는 "AI Workspace를
  개발하는 과정을 돕는 도구"이지 AI Workspace가 최종 사용자에게
  제공하는 기능이 아니기 때문이다(`AI_RULES`의 "이 Vault가 아닌 것"
  원칙과 동일한 경계를 코드 계층에도 적용한 것).
- 결과/영향: `docs/ARCHITECTURE.md` v0.25.0 신규 §3.21(Vault
  Integration Layer)에 반영, §9 디렉터리 구조에 `vault/`(설계됨,
  M23-T02, 미구현) 추가. §7 Interfaces는 새 Interface가 없어 27종
  그대로. Vault `02 Architecture/Vault Integration Architecture.md`
  신규(이 ADR의 Vault 반영본), `Architecture Overview`/`Architecture
  Map`/`ADR Index`에 backlink 추가. 실제 구현은 M23-T03(Vault Save
  Engine)부터 시작한다.
- **Verification(2026-07-27, Milestone 23 Verification, 사용자
  요청)**: M23-T03~T07로 이 ADR의 설계가 실제 구현·테스트·실제
  Vault 대상 통합 테스트까지 완료된 뒤, 이 ADR이 정의한 4개 결정
  (Vault Directory Mapping/Save Flow/File Strategy/Metadata 처리)
  이 코드와 일치하는지 검증했다. Mock(`tmp_path`) 38개 + 실제
  `Vault/` 대상 통합 테스트 3개 전부 통과, 실제 Vault는 검증
  과정에서 전혀 수정하지 않음(코드 검토와 Mock만 사용). 검증에서
  ⚠️ 3건(Template 형식 렌더링이 ADR/Decision 2종만 대상 문서 실제
  관행과 검증됨/Auto Save는 AI가 절차를 따라 호출하는 수동 구조/
  `delete_document(force=True)` 이후 Orphan Backlink 미정리)을
  발견했으나, 전부 이 ADR과 M23-T06에서 이미 명시한 의도적 범위
  축소(YAGNI)의 재확인이며 새 결함이 아니라고 최종 확정했다(사용자
  승인, M23-Final) — 이 ADR의 결정을 변경하거나 범위를 확장하지
  않는다. 상세 체크리스트는 `.ai/TASKS.md`의 "Milestone 23
  Verification"/"M23-Final" 절 참고.

## ADR-0036: Real Obsidian Vault Integration — Connection/Filesystem Adapter/Atomic Write 신설, Auto Save Validation을 Incremental로 전환 (Milestone 24)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: M23(ADR-0035)이 만든 `vault/`는 처음부터 실제 `pathlib`
  호출로만 동작했지만(별도 Mock 파일시스템 계층 없음), 호출자가
  항상 `vault_root: Path`를 직접 계산해서 넘겨야 했고(단위 테스트는
  `tmp_path`, M23-T07 통합 테스트는 실제 경로를 수동 계산), 저장
  경로를 못 찾거나 권한이 없을 때의 처리, 쓰기 중단 시 파일이
  반쪽짜리로 남는 문제, Auto Save의 Validation이 매번 Vault
  전체를 다시 스캔해 "이번 저장과 무관한 기존 문제 때문에 저장이
  실패한 것처럼 보이는" 문제가 남아 있었다. 사용자가 "Mock/
  tmp_path가 아니라 실제 Obsidian Vault를 대상으로 동작해야 한다"는
  목표로 M24(T01~T08)를 요청했다.
- 결정:
  1. **`vault/connection.py`(신규)**: `resolve_default_vault_root()`
     가 시작 경로(기본값 `Path.cwd()`)에서 상위로 올라가며
     `Vault/01 Projects/AI Workspace`가 실제로 존재하는 첫 조상
     경로를 찾는다(이 저장소의 루트 위치를 가정하지 않음).
     `connect(root=None)`이 그 경로(또는 명시적으로 넘긴 경로)가
     존재/디렉터리/쓰기 가능한지 검증해 `VaultConnection`을
     돌려주고, 실패하면 `VaultConnectionError`(Permission
     Validation + 존재 여부 확인 + 연결 실패 예외 처리, 사용자
     DoD 요구사항 그대로).
  2. **`vault/filesystem.py`(신규)**: `VaultFileSystem` 클래스가
     Create/Read/Update/Delete/Exists/Rename/Move 7개 연산을
     명시적인 이름으로 노출한다. `writer.py`/`sync.py`의 기존
     동작은 그대로 유지하고(변경 최소화), 이 클래스는 그 연산들의
     경계를 드러내는 얇은 추가 계층이다 — 기존 코드를 이 계층
     위로 재작성하지 않는다.
  3. **`vault/atomic.py`(신규)**: `atomic_write_text()`가 같은
     디렉터리에 임시 파일을 먼저 쓰고 `os.replace()`로 원자적
     교체한다. `VaultWriter.create_file()`/`upsert_section()`
     내부의 `path.write_text()` 호출을 이 함수로 교체했다 — 두
     메서드의 공개 동작(반환값, 언제 파일을 쓰는지)은 전혀 바뀌지
     않았다(기존 테스트 38개 무변경 통과로 확인).
  4. **Auto Save Validation을 Incremental로 전환**:
     `find_broken_backlinks()`에 `only_paths` 파라미터를 추가하고
     (생략 시 기존과 동일하게 Vault 전체 스캔), `run_auto_save()`
     내부 호출을 `find_broken_backlinks(vault_root)`에서
     `find_broken_backlinks(vault_root, only_paths=saved)`로
     바꿨다 — Auto Save는 자신이 그 호출에서 실제로 저장한 파일만
     검증 책임을 진다. Vault 전체 감사(M23-T07 패턴)는 여전히
     `only_paths` 없이 직접 호출하면 된다. 이 변경은 기존 4개
     Auto Save 테스트의 기대 결과를 하나도 바꾸지 않는다(깨진
     링크는 항상 저장한 파일 자체 안에 있었기 때문).
  5. **`run_auto_save_on_default_vault()`(신규,
     `vault/auto_save.py`)**: `vault_root`를 생략하면
     `connection.connect()`로 실제 Vault를 찾아 연결한 뒤
     `run_auto_save()`를 수행한다 — "다음 Task 진행" 같은 명령을
     받은 AI가 매번 실제 경로를 손으로 계산하지 않아도 된다.
  6. **범위를 의도적으로 넓히지 않은 것**: 사용자가 자동 저장
     대상으로 언급한 TASKS/MEMORY/ROADMAP은 GitHub `.ai/`/`docs/`
     원문이며, `vault/`는 ADR-0035부터 "GitHub 원문을 복제하지
     않는다"는 경계를 지켜 왔다 — 이번에도 그 경계를 유지하고
     `vault/`가 GitHub 원문 파일을 직접 쓰도록 확장하지 않았다.
     Design/Implementation/Memory/Roadmap/Task는 실제 Vault(PARA
     구조, M23-Preparation에서 확정)에 대응하는 전용 디렉터리가
     없어 `VaultDocumentKind`에 새 kind를 추가하지 않았다 — 실제로
     존재하지 않는 폴더를 코드가 상상해서 만들지 않는다("실제
     Vault를 기준으로 설계" 원칙).
- 대안:
  - `writer.py`/`sync.py`를 `VaultFileSystem` 위로 전면 재작성 —
    기각. 두 모듈은 이미 실제 파일시스템으로만 동작해 정상 동작하고
    있었고, 재작성은 위험 대비 이득이 없다("변경 최소화" 원칙,
    기존 테스트 유지 요구사항).
  - Auto Save Validation을 계속 Vault 전체 스캔으로 유지 — 기각.
    이번 저장과 무관한 기존 파일의 문제 때문에 매번 저장이 실패한
    것처럼 보이는 것은 "Auto Save가 책임지지 않아도 될 실패"를
    보고하는 것이라 판단했다. 전체 감사가 필요하면 여전히 직접
    호출 가능하므로 기능을 잃지 않는다.
  - Design/Implementation/Memory/Roadmap용 새 Vault 폴더를 즉석에서
    만들기 — 기각. 실제 Vault 구조는 M23-Preparation에서 사용자
    승인으로 확정된 PARA 구조이며, 이번 Task 하나로 임의로 늘리면
    "기존 Architecture 유지" 원칙과 충돌한다.
- 이유: `resolve_default_vault_root()`/`connect()`는 "실제 경로를
  어떻게 찾고 검증하는가"를 한 곳에 모아, 이후 어떤 호출자도
  경로 탐색·권한 검증 로직을 중복 구현하지 않게 한다. Atomic
  Write는 실제 Vault(git으로 추적되는 진짜 파일들)에 쓰는 이상
  중단 시 손상 위험을 없애는 것이 M23 시점보다 훨씬 중요해졌다
  (M23까지는 `tmp_path`라 손상돼도 테스트 재실행이면 그만이었다).
  Incremental Validation은 Auto Save를 "내가 만든 문제만 책임지는"
  좁고 예측 가능한 계약으로 유지한다.
- 결과/영향: `src/ai_workspace/vault/`에 `connection.py`/
  `atomic.py`/`filesystem.py` 3개 파일 신규, `writer.py`/
  `auto_save.py`/`validation.py` 최소 수정(공개 동작 불변).
  새 Interface 없음(27종 그대로) — `vault/`는 ADR-0035부터 Core
  Interface 계약 밖에 있다. `tests/vault/`(Mock/`tmp_path`, 38개)
  는 전부 무변경 통과, `tests/integration/test_m24_real_vault_e2e.py`
  (신규, 5개)가 `tmp_path` 없이 이 저장소의 실제 `Vault/`를 대상으로
  Connect/Create/Update/Rename/Delete/Auto Save 왕복을 검증하고
  테스트 종료 시 스스로 정리해 실제 Vault에는 영구 변경을 남기지
  않는다. `docs/ARCHITECTURE.md` §3.21 갱신, Vault `Vault
  Integration Architecture.md`에 반영.

## ADR-0037: Obsidian Vault Root Refactoring — Vault Root를 저장소 Root로 승격, `Vault/01 Projects/AI Workspace` 계층 제거 (Milestone 26)

- 상태: 승인됨 (2026-07-27, 사용자 승인)
- 날짜: 2026-07-27
- 배경: 사용자가 로컬 Obsidian 앱에서 이 저장소의 Vault를 열려고
  했을 때, Git Vault Sync(iOS)/Obsidian Mobile·macOS가 공통으로
  요구하는 "Vault == Repository Root" 조건을 `Vault/01 Projects/
  AI Workspace/`처럼 저장소 하위에 중첩된 구조가 만족하지 못한다는
  점이 드러났다. 또한 AI Workspace가 "프로젝트 하나 = 저장소 하나
  = Vault 하나" 전략(여러 프로젝트를 하나의 저장소/Vault 아래
  두지 않는 구조)으로 갈 것이 확정되면서, 애초에 여러 프로젝트를
  가정한 PARA 4단 구조(`00 Inbox`/`01 Projects`/`02 Resources`/
  `03 Archives`)도 더 이상 맞지 않게 됐다.
- 결정:
  1. `Vault/01 Projects/AI Workspace/` 아래 15개 디렉터리(`00
     System`~`13 Daily`, `99 Templates`)를 `git mv`로 저장소 root로
     승격한다(파일별 History가 Rename으로 보존됨, Delete+Create
     방식 미사용).
  2. 비어 있던 PARA 뼈대(`Vault/00 Inbox/.gitkeep`, `Vault/02
     Resources/.gitkeep`, `Vault/03 Archives/.gitkeep`)와 이제
     완전히 빈 `Vault/`/`Vault/01 Projects/` 디렉터리는 제거한다
     (다시 필요해지면 그때 새로 만든다 — YAGNI).
  3. `vault/connection.py`의 `resolve_default_vault_root()`가 더
     이상 `Vault/01 Projects/AI Workspace` 하위 경로를 찾지 않고,
     Vault Root에서만 존재하는 표식 파일(`00 System/PROJECT_INDEX.md`)
     이 있는 첫 조상 디렉터리를 찾도록 바꾼다 — Vault Root와 저장소
     root가 이제 같으므로 자연스럽게 일치한다.
  4. `vault/mapping.py`의 `VAULT_DIRECTORY_MAP` 상대 경로(`"03 ADR/
     ADR Index.md"` 등)는 처음부터 `vault_root` 기준 상대 경로였기
     때문에 **변경하지 않는다** — 이 설계(ADR-0035)가 이번 리팩토링을
     사실상 무비용으로 만들었다.
  5. `vault/validation.py`(`_iter_markdown_files`)와 `vault/sync.py`
     (`_iter_vault_markdown_files`, 신규)가 `rglob("*.md")`를
     `vault_root` 전체가 아니라 새로 정의한 `VAULT_DIRECTORY_MAP`
     의 형제 상수 `VAULT_CONTENT_DIRECTORIES`(15종)로 제한하도록
     바꾼다 — `vault_root`가 저장소 root와 같아진 이상, 제한 없는
     `rglob`은 `docs/`/`.claude/`/`.agents/`의 마크다운까지
     Backlink/Tag Validation에 끌어들여 결과를 오염시키기 때문이다.
  6. Backlink는 `[[Wikilink]]`(파일명 기준, 위치 무관) 방식만
     쓰고 있음을 재확인했다 — 이번 이동으로 Wikilink는 전혀 깨지지
     않는다. Vault 안에 마크다운 스타일 상대경로 링크(`[텍스트]
     (경로)`)가 있는지 전수 검색한 결과 0건이라, "Broken Link 0건"
     조건이 애초에 이동 자체로는 위협받지 않았다.
  7. `.obsidian/`은 이번에 만들지 않는다 — 이 세션은 Obsidian 앱을
     실행할 수 없고, Obsidian이 저장소 root를 Vault로 처음 열 때
     자동 생성하는 파일이라 미리 만들 근거가 없다(추측성 설정 파일
     생성 금지).
- 대안:
  - `Vault/` 한 단계만 남기고(`Vault/AI Workspace/` 등) `01
    Projects` 계층만 제거 — 기각. "Vault == Repository Root"
    조건은 중첩 자체를 허용하지 않는다.
  - PARA 4단 구조(`00 Inbox`/`02 Resources`/`03 Archives`)를
    유지 — 기각. AI Workspace가 다중 프로젝트를 한 Vault에 담는
    구조를 포기하기로 한 이상(배경 참고), 그 구조를 위해 만든
    빈 뼈대를 남겨 둘 이유가 없다.
  - `vault/validation.py`/`sync.py`의 스캔 범위를 계속 `vault_root`
    전체로 유지 — 기각. `vault_root`가 저장소 root와 같아진 순간
    이 가정이 깨지므로, 범위를 명시적으로 좁히지 않으면 Validation
    결과가 신뢰할 수 없어진다.
- 이유: `vault/mapping.py`의 상대 경로 설계(ADR-0035)와 `[[Wikilink]]`
  전용 Backlink 관행(AI_RULES) 덕분에, "Vault Root를 옮긴다"는
  근본적인 구조 변경이 실제로는 `connection.py` 1개 파일의 탐색
  로직 교체 + Validation 스캔 범위 제한 정도로 끝났다 — 처음부터
  경로를 하드코딩하지 않고 상대 경로/파일명 기준으로 설계해 둔
  이전 결정들이 이번 리팩토링의 위험을 크게 낮췄다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.32.0 §3.21에 Milestone 26
  구현 상태 반영, Vault `Vault Integration Architecture.md`에도
  동일하게 반영. `vault/connection.py`(교체)/`mapping.py`(상수
  추가, 로직 무변경)/`validation.py`/`sync.py`(스캔 범위 제한) 수정.
  `tests/vault/`(Mock) 46개 중 새 스캔 범위에 맞춰 9개 fixture를
  조정(assertion·검증 대상 함수는 그대로, fixture 파일 위치만
  `00 System/` 하위로 이동), `tests/integration/test_m23_vault_
  environment_integration.py`/`test_m24_real_vault_e2e.py`가
  저장소 root를 직접 Vault Root로 쓰도록 갱신. 새 Interface 없음
  (27종 그대로).

## ADR-0038: Obsidian Workspace Templates 도입 — `VaultDocumentKind.TASK` 신규(개별 Task 문서), Frontmatter/Tag Rule 확장, Project Workspace Template 정의(설계만) (Milestone 27, M25 요청)

- 상태: 승인됨 (2026-07-27, 사용자 요청 "M25 - Obsidian Workspace
  Integration" 반영)
- 날짜: 2026-07-27
- **Milestone 번호 안내**: 사용자 요청 프롬프트는 이 작업을 "M25"로
  지칭했으나, 그 번호는 이미 완료된 Milestone 25(Production Vault
  Activation)가 쓰고 있어 기존 기록을 덮어쓰지 않기 위해
  **Milestone 27**로 새로 번호를 부여했다(ADR-0037이 M24-T01
  충돌에서 Milestone 26을 부여한 것과 동일한 패턴, 투명하게 기록).
  Git 브랜치명/PR 제목 등 외부에 이미 고정된 문자열은 그대로 "M25"
  표기를 유지한다.
- 배경: Obsidian을 단순 문서 저장소가 아니라 "Task 생성 → 문서
  생성 → 진행 관리 → 상태 변경"이 Obsidian 안에서 이루어지는
  Workspace UI로 확장하고 싶다는 요청. Vault Integration Layer
  (ADR-0035)는 이미 12개 kind → Index 파일 append/Daily 파일
  create 매핑을 갖고 있었지만, Task는 전용 kind가 없어 GitHub
  `.ai/TASKS.md` 표 행으로만 존재했고 Obsidian 안에서 상태를 보고
  갱신할 방법이 없었다. Decision/Daily Template도 이번 요청이
  요구하는 필드(Problem/Options/Decision/Reason/Impact,
  진행중/완료 구분)를 전부 갖추고 있지는 않았다.
- 결정:
  1. `vault/models.py`의 `VaultDocumentKind`에 `TASK`를 추가한다.
     `DECISION`처럼 Index에 append하지 않고 `DAILY`처럼 파일 1개를
     통째로 생성한다(create 방식) — 대상 파일은 날짜가 아니라
     `request.fields["task_id"]` 기준.
  2. `vault/mapping.py`에 새 콘텐츠 디렉터리 `14 Tasks`를 추가하고
     `VAULT_DIRECTORY_MAP[TASK]`를 `"14 Tasks/{task_id}.md"`(create)
     로 매핑한다. `VAULT_CONTENT_DIRECTORIES`(기존 15종 → 16종)에도
     포함시켜 `validation.py`/`sync.py`의 Backlink/Tag 스캔 대상이
     되게 한다.
  3. `vault/router.py`가 `DAILY`의 날짜 치환과 같은 방식으로
     `TASK`의 `task_id` 치환을 처리한다 — `fields`에 `task_id`가
     없으면 `MissingVaultFieldError`.
  4. `vault/markdown_generator.py`에 `render_task_file()`을 추가한다
     — frontmatter(`tags: [task]`, `type: task`, `status`,
     `priority`, `milestone`, `owner`, `created`, `updated`) +
     Status/Priority/Milestone/Owner/Created/Updated/Checklist/
     Notes/Related Documents/Decision 섹션(M25 요청 원문 그대로).
     `vault/engine.py`의 `VaultSaveEngine.save()`가 `TASK` create를
     이 함수로 라우팅한다.
  5. `render_daily_file()`을 확장해 "오늘 작업"/"진행중"/"완료"/
     "문제"/"결정사항"/"내일 계획"(M25 요청 Daily Note Template)을
     전부 반영한다 — 기존 "오늘 결정"을 "결정사항"으로 정리하고
     "진행중"/"완료"를 분리했다. `99 Templates/Template - Daily.md`
     도 동일하게 갱신해 코드-문서 1:1 대응(`render_daily_file()`
     docstring이 이미 주장하던 관계)을 유지한다.
  6. `99 Templates/Template - Decision.md`에 M25 요청 Decision
     Template 필드(Problem/Options/Decision/Reason/Impact)를
     반영하고 frontmatter에 `type`/`milestone`/`created`/`updated`
     를 추가한다. 기존 GitHub 원문용 `DECISION_TEMPLATE.md`(가벼운
     판단 기록 절차)는 바꾸지 않는다 — 둘의 역할 분리(ADR-0035
     이전부터 유지된 관행)를 그대로 존중한다.
  7. `AI_RULES`의 Tag Rule에 `#task`/`#meeting`/`#bug`/`#feature`/
     `#research`/`#daily`를 추가하고, 새 **Frontmatter Rule** 절을
     신설해 "상태를 갖는 문서는 `type`/`status`/`priority`/
     `milestone`/`created`/`updated`를 frontmatter에 추가한다"는
     규칙을 명문화한다. Backlink Rule(Wiki Link)은 기존 규칙을
     그대로 재확인(변경 없음, 이미 M25 요청을 만족).
  8. **Workspace Template(다중 Project 폴더 구조)은 설계만 하고
     지금 인스턴스화하지 않는다** — `99 Templates/Template -
     Project Workspace.md`(신규)에 `Projects/<이름>/README.md,
     Tasks/, Notes/, Meetings/, Decisions/, Archive/` 표준 구조와
     이 Vault(단일 Project)의 현재 디렉터리 대응표를 문서화한다.
     이 Vault는 아직 Project 1개(자기 자신)만 다루고
     `ProjectRepository`(`storage/file_project_repository.py`)가
     Vault와 실제로 연결돼 있지 않으므로, 지금 `Projects/` 폴더를
     만드는 것은 추측성 구조 생성이다(YAGNI, `.ai/RULES.md` §4.2).
- 대안:
  - Task도 `DECISION`처럼 `11 Milestones/Milestones Index.md`에
    한 줄만 append — 기각. M25 요청의 핵심("Task 상태를 Obsidian
    안에서 관리")은 Task 1건당 문서가 있어야 Checklist/Status를
    개별적으로 갱신할 수 있다.
  - Workspace Template을 지금 `Projects/AI Workspace/` 폴더로
    실제 이동/생성 — 기각. Milestone 26(ADR-0037)이 정확히 반대
    방향(다중 프로젝트 PARA 구조 제거, Vault == Repository Root)
    으로 리팩토링한 직후이므로, 다시 다중 프로젝트 중첩 구조를
    지금 도입하는 것은 그 결정을 무근거로 되돌리는 것이다.
- 이유: ADR-0035의 kind→매핑 설계(코드가 아니라 데이터)와
  ADR-0037의 `VAULT_CONTENT_DIRECTORIES` 분리 덕분에, `TASK`
  kind 추가가 `DAILY`가 이미 확립한 "create + 동적 파일명" 패턴을
  그대로 재사용하는 것으로 끝났다 — 새 Interface나 새 Save Flow
  단계 없이 기존 4단계(Router→Generator→Writer→Engine)에 값 하나만
  더한 확장.
- 결과/영향: `vault/models.py`/`mapping.py`/`router.py`/
  `markdown_generator.py`/`engine.py` 수정, `14 Tasks/`(신규
  디렉터리 + README.md), `99 Templates/Template - Task.md`/
  `Template - Project Workspace.md`(신규), `Template - Daily.md`/
  `Template - Decision.md`(갱신), `AI_RULES`/`PROJECT_INDEX` 갱신.
  `tests/vault/`(신규 6개 — `render_task_file`/Router TASK 라우팅/
  `VaultSaveEngine` TASK 저장 + Daily 확장 섹션 검증), 기존
  전부 무변경 통과. `docs/ARCHITECTURE.md` §3.21, `docs/ROADMAP.md`,
  `.ai/RULES.md`에 반영. 새 Interface 없음(27종 그대로) —
  `vault/`는 애초에 Interface 계층이 아니라 데이터/함수 계층
  (ADR-0035)이므로 이 확장도 그 성격을 유지한다.

## ADR-0039: Workspace Adapter Layer 도입 — `integration/` 신규 최상위 패키지(Vault/Workflow/Agent Adapter), Core Domain↔vault 직접 의존 금지를 코드로 강제 (Milestone 28-T03)

- 상태: 승인됨 (2026-07-30, 사용자 승인 — "Approve with Architecture
  Direction")
- 날짜: 2026-07-30
- 배경: Milestone 28은 Task Lifecycle(T01)/자동 문서 갱신(T02)까지
  `vault/` 안에서 완결했지만, 이후 Task(T04 Workflow Engine
  Integration, T05 Agent Assignment, T06 Conversation Layer
  Integration)는 전부 Core Domain(`domain`/`interfaces`/`engines`)
  과 `vault/`를 함께 다뤄야 한다. ADR-0035는 "Core Domain은 vault를
  모르고 vault는 Core Domain을 모른다"를 이미 원칙으로 세워뒀으므로,
  이 경계를 지키면서 둘을 연결할 **제3의 계층**이 필요했다. 사용자가
  T03 설계 검토에서 "Vault/Workflow/Agent Adapter 3개로 구현하되,
  이를 단순한 '세 개의 Adapter'가 아니라 향후 Runtime/Service/
  Notification/Sync 등이 추가될 수 있는 **Workspace Adapter Layer**
  의 첫 구성 요소로 문서·아키텍처에 정의할 것"을 조건으로 승인했다.
- 결정:
  1. `src/ai_workspace/integration/`을 신규 최상위 패키지로 만든다
     (`domain`/`interfaces`/`engines`/`vault`/`web` 등과 같은 층위).
     이 패키지가 **Workspace Adapter Layer**의 구현체다 — "Adapter
     3개"가 아니라, 외부 관심사 하나당 Adapter 하나를 추가하는
     확장 가능한 계층으로 공식 정의한다(패키지 docstring에 이
     정의와 향후 확장 후보를 명시).
  2. 초기 구성원은 3개만 만든다: `VaultAdapter`(`vault/`를 아는
     유일한 Integration Layer 구성원), `WorkflowAdapter`
     (`WorkflowEngine`/`TaskEngine` Interface에만 의존),
     `AgentAdapter`(`AgentManager`/`AgentRegistry`/`AgentScheduler`
     Interface에만 의존). 셋은 서로를 참조하지 않는다 — Task↔
     Workflow 연결(T04)/Workflow↔Agent 연결(T05)은 이 Adapter들을
     조합해 쓰는 상위 호출자(Conversation Layer 등)의 책임으로
     미룬다(YAGNI, 지금 만들지 않는다).
  3. **공유 기반 클래스/Protocol을 만들지 않는다.** 세 Adapter의
     메서드 시그니처가 서로 다른 관심사를 다뤄 억지로 공통 인터페이스를
     뽑으면 Speculative Generality(`.ai/RULES.md` §4.2 금지 목록)가
     된다. "Layer"라는 개념은 (a) 패키지 경계(`integration/`),
     (b) `XxxAdapter` 이름 규칙, (c) 이 ADR + `docs/ARCHITECTURE.md`
     문서화로 정의한다 — 실제로 여러 Adapter가 같은 메서드를
     공유해야 하는 필요가 생기면 그때 Interface를 뽑는다(ADR-0029와
     같은 점진적 확장 패턴).
  4. **원칙 — 연결·변환·위임만, 비즈니스 로직 금지**: Adapter는
     자체 알고리즘(계획 수립, 상태 전이 규칙, 자연어 해석 등)을
     갖지 않는다. `WorkflowAdapter.plan()`은 `WorkflowEngine.plan()`
     을 그대로 호출하고, `AgentAdapter.create_agent()`는
     `AgentManager.create()` + `AgentRegistry.register()`를 잇는
     것 이상을 하지 않는다. `VaultAdapter`도 `vault.task_lifecycle`/
     `vault.task_sync`/`vault.engine`을 그대로 호출하며 vault 내부
     타입(`TaskStatus` 등)은 바깥으로 노출하지 않고 문자열로만
     주고받는다 — Core Domain이 vault 타입을 몰라도 되게 하기
     위함이다("Workspace Intelligence"는 여기 두지 않는다 —
     Conversation Layer(T06)나 Core Engine의 몫).
  5. `docs/ARCHITECTURE.md` §8(의존성 규칙)에 새 규칙 18을 추가한다:
     "Core Domain(`domain`/`interfaces`/`engines`)과 `vault/`는
     서로 직접 참조하지 않는다. 이 경계를 넘는 통신은 반드시
     `integration/`의 Adapter를 통해서만 이뤄진다."
  6. 자동 검증을 코드로 만든다 — `tests/integration_layer/
     test_architecture_boundary.py`가 `ast` 모듈로 `src/ai_workspace/`
     전체의 import 문을 파싱해 (a) `domain`/`interfaces`/`engines`
     어떤 파일도 `ai_workspace.vault`를 import하지 않는지, (b)
     `vault/` 어떤 파일도 `ai_workspace.{domain,interfaces,engines}`
     를 import하지 않는지, (c) `integration/` 밖의 어떤 파일도 두
     쪽을 동시에 import하지 않는지 확인한다. 이 규칙은 앞으로도
     리뷰가 아니라 테스트 실패로 강제된다.
  7. 이 계층의 단위 테스트는 `tests/integration/`(기존 Milestone
     End-to-End 테스트 전용, M23~M24부터 써 온 이름)과 겹치지 않게
     `tests/integration_layer/`에 둔다 — 이름 충돌은 우연이며,
     `src/ai_workspace/integration/`을 미러링하는 새 디렉터리임을
     여기 명시적으로 기록한다.
- 대안:
  - Adapter 3개에 공통 `WorkspaceAdapter` Protocol/ABC를 강제 —
    기각(위 결정 3). 지금은 억지 추상화만 될 뿐 실질적 이득이 없다.
  - `vault/`가 직접 `domain.Task`/`WorkflowEngine`을 import하도록
    허용(Integration Layer 생략) — 기각. ADR-0035가 이미 확립한
    "vault는 Core Domain을 모른다" 원칙(GitHub 원문↔Vault 동기화
    도구라는 vault의 정체성)을 무너뜨린다.
  - Core Domain의 `TaskEngine`/`WorkflowEngine`을 vault의
    `VaultDocumentKind.TASK`와 즉시 통합(Task 개념 통일) —
    기각/보류. 두 "Task"(vault의 Markdown 문서, Core Domain의
    `domain.Task`)를 지금 억지로 합치면 그 통합 로직 자체가
    설계 없이 만들어진 비즈니스 로직이 된다 — T04(Workflow Engine
    Integration)에서 명시적으로 설계·승인받고 진행한다.
- 이유: Integration Layer를 "3개의 구체적인 Adapter"가 아니라
  이름 있는 계층으로 정의해 두면, T04(Workflow)/T05(Agent)/T06
  (Conversation)이 이 Adapter들을 조합하는 데서 그치고, 이후
  Milestone(사용자가 언급한 Runtime/Service/Notification/Sync,
  나아가 M40 이후 Core 확장)도 같은 패키지에 새 Adapter만 추가하는
  형태로 자연스럽게 이어진다 — 매번 "이 새 기능은 어느 계층에
  속하는가"를 재설계할 필요가 없다.
- 결과/영향: `src/ai_workspace/integration/`(신규) —
  `__init__.py`(Layer 정의 docstring)/`vault_adapter.py`/
  `workflow_adapter.py`/`agent_adapter.py`. `vault/task_sync.py`의
  `TaskSyncResult`에 `task_id`/`old_status`/`new_status` 필드
  추가(기존 필드는 무변경, `VaultAdapter.transition_task()`가
  실제 이전 상태를 돌려주기 위해 필요했음 — 기존 T02 테스트
  전부 무변경 통과 확인). `tests/integration_layer/`(신규 13개 —
  Adapter별 단위 테스트 + Architecture Boundary 자동 검증 3개).
  `docs/ARCHITECTURE.md` §8 규칙 18, §9 디렉터리 구조,
  `.ai/TASKS.md`에 반영. 새 Core Domain Interface 없음(27종
  그대로) — Integration Layer는 기존 Interface에 의존만 하고
  새 계약을 추가하지 않는다.

## ADR-0040: Integration Layer 내부 분류 — Adapter vs Connector (Milestone 28-T05)

- 상태: 승인됨 (2026-07-30, 사용자 승인 — "Go Ahead" + 방향 지정)
- 날짜: 2026-07-30
- 배경: M28-T04에서 `WorkflowTaskLink`(Vault Task↔Core Domain
  Workflow/Task 연결)를 만들며, `VaultAdapter`/`WorkflowAdapter`
  (외부 시스템 하나만 연결하는 것)와 `WorkflowTaskLink`(둘을
  조합하는 것)가 서로 다른 책임임이 드러났다. M28-T05(Agent
  Assignment)를 시작하며 사용자가 이 구분을 공식화할 것을 조건으로
  승인했다: "`WorkflowTaskLink`에 Agent 책임을 추가하지 않는다,
  `WorkflowAgentLink`를 별도 Connector로 구현한다, Adapter는
  계속 외부 시스템 연결만, Connector는 여러 Adapter를 조합하는
  유스케이스 오케스트레이션만 담당한다." M28 완료 후 예정된
  Architecture Freeze에서 Integration Layer 역할을 명확히 하고,
  M29(Project Intelligence)/M40 이후 Runtime·Service 계층 확장의
  기반이 되게 하려는 목적.
- 결정:
  1. Integration Layer(ADR-0039) 안에서 두 종류의 구성원을
     공식적으로 구분한다.
     - **Adapter**: 외부 시스템 **하나**와의 연결만 담당
       (`VaultAdapter`→`vault/`, `WorkflowAdapter`→`WorkflowEngine`/
       `TaskEngine`, `AgentAdapter`→`AgentManager`/`AgentRegistry`/
       `AgentScheduler`). 다른 Adapter를 참조하지 않는다(ADR-0039
       결정 2 유지).
     - **Connector**: 여러 Adapter를 조합해 유스케이스 하나를
       오케스트레이션한다(`WorkflowTaskLink`—M28-T04, Vault Task로
       Workflow 만들기/상태 반영; `WorkflowAgentLink`—M28-T05, Task에
       Agent 배정/추적). Connector도 자체 비즈니스 로직(상태 전이
       규칙, 선택 알고리즘)은 만들지 않는다 — 항상 Adapter가 감싼
       Core Domain Engine에 위임하고, Connector 자신은 조합·ID
       변환·파생 값 계산만 한다(ADR-0039 원칙 4 그대로 적용).
  2. **Connector는 유스케이스 하나만 책임진다** — Agent 배정
     책임을 이미 있던 `WorkflowTaskLink`에 얹지 않고 별도
     `WorkflowAgentLink`를 새로 만든다. Connector끼리도 서로
     참조하지 않는다(Adapter들이 서로 참조하지 않는 것과 같은
     원칙을 Connector 층위에도 적용).
  3. `WorkflowAgentLink`는 `AgentAdapter`/`WorkflowAdapter`만
     조합한다(Vault는 모른다) — Task 상태를 Vault에 반영하는 것은
     이미 `WorkflowTaskLink`의 책임이라 중복하지 않는다.
  4. Agent 배정 관계(`AgentAssignment`: `WorkflowLink` + `Agent`)와
     Agent별 진행률(`agent_progress()`)은 `domain.Task`/
     `domain.Agent`에 필드를 추가하지 않고 `WorkflowAgentLink`
     내부 상태로만 관리한다(ADR-0039/T04와 동일한 Domain 오염
     금지 원칙 — Agent도 Task와 마찬가지로 순수하게 유지).
- 대안:
  - Agent 배정을 `WorkflowTaskLink`에 메서드로 추가 — 기각(사용자
    명시적 반대). 한 Connector가 두 유스케이스(Task↔Workflow 연결,
    Task↔Agent 배정)를 동시에 책임지면 나중에 Notification/Sync
    등 다른 관심사가 추가될 때 같은 문제가 반복된다.
  - Adapter/Connector 구분을 문서로만 남기고 코드/네이밍에는 반영
    안 함 — 기각. Architecture Freeze에서 "Integration Layer의
    역할이 명확해야 한다"는 목적에 안 맞는다 — 코드 구조(파일명,
    docstring, 패키지 `__init__.py`)에 직접 반영해야 나중에 실수로
    섞이지 않는다.
- 이유: Adapter/Connector를 구분해 두면 M29(Project Intelligence)
  이후 새 유스케이스(예: "Vault Task 변경 → Notification 발송")가
  생겨도 기존 Adapter/Connector를 건드리지 않고 새 Connector 하나만
  추가하면 된다 — Integration Layer가 "무엇이 Adapter이고 무엇이
  Connector인지" 매번 재판단할 필요 없이 일관된 확장 패턴을 갖는다.
- 결과/영향: `integration/workflow_agent_link.py`(신규,
  `WorkflowAgentLink`/`AgentAssignment`), `integration/__init__.py`
  갱신(Adapter/Connector 구분 명시), `integration/
  workflow_task_link.py` docstring에 "Connector" 용어 반영(로직
  무변경). `tests/integration_layer/test_workflow_agent_link.py`
  (신규 6개). `docs/ARCHITECTURE.md`/`.ai/TASKS.md`에 반영. 새 Core
  Domain Interface 없음, `domain.Task`/`domain.Agent` 필드 추가
  없음.

## ADR-0041: Conversation Layer 연동 — Conversation Connector 도입, Orchestrating Connector 개념 추가 (Milestone 28-T06)

- 상태: 승인됨 (2026-07-30, 사용자 승인 — 요구사항/Boundary/금지
  목록을 명시한 상세 지시)
- 날짜: 2026-07-30
- 배경: M28의 마지막 Task. Conversation Layer(자연어로 "로그인
  기능 만들어줘" 같은 요청을 받는 쪽)가 Task/Workflow/Agent를
  다루려면 Integration Layer에 접근해야 하는데, 지금까지의 Peer
  Connector(`WorkflowTaskLink`/`WorkflowAgentLink`, ADR-0040)는
  각자 유스케이스 하나(Task↔Workflow, Task↔Agent)만 책임지고
  서로 참조하지 않는다는 원칙을 갖고 있어, 이 둘을 함께 써야 하는
  "Task 생성→Workflow 생성→Agent 배정→Vault 반영" 같은 상위
  유스케이스를 처리할 자리가 없었다. 사용자가 T06 요청에서
  `integration/conversation_workflow_link.py`의 Conversation
  Connector를 명시적으로 지정하고, "새로운 비즈니스 로직은 절대
  추가하지 않는다"/"Conversation Layer는 Domain·Vault·AgentManager
  를 직접 참조하지 않는다"/"모든 요청은 Integration Layer를 통해
  전달한다"는 조건으로 승인했다.
- 결정:
  1. `integration/conversation_workflow_link.py`(신규)에
     `ConversationConnector`를 만든다. 생성자로 `VaultAdapter`/
     `WorkflowTaskLink`/`WorkflowAgentLink`를 주입받아 조합만
     한다 — 새 상태 전이 규칙, Agent 선택 기준, Task 분해 판단을
     전혀 만들지 않는다. `handle_task_request()`가 "Task 생성→
     Workflow 생성→Agent 배정" 흐름을, `advance_task()`가 상태
     전이+Vault 반영을, `report_status()`가 Task별 상태 조회+
     완료 여부 조합을 각각 기존 Connector 메서드 호출로만
     구현한다.
  2. **ADR-0040 "Connector끼리 서로 참조하지 않는다"에 대한 명시적
     예외를 도입한다**: Connector를 두 하위 개념으로 나눈다.
     - **Peer Connector**(`WorkflowTaskLink`/`WorkflowAgentLink`)
       — 유스케이스 하나만 책임지고 서로 참조하지 않는다(ADR-0040
       원칙 그대로 유지).
     - **Orchestrating Connector**(`ConversationConnector`) — 여러
       Peer Connector/Adapter를 조합해 더 상위 유스케이스(사용자
       요청 전체)를 라우팅·조합하는 것 자체가 존재 이유다. 이
       조합도 비즈니스 로직이 아니라 순서 배열·결과 묶기이므로
       ADR-0039/ADR-0040의 "연결·변환·위임만" 원칙과 충돌하지
       않는다.
  3. **Conversation Layer의 책임을 3가지로 한정한다**(코드가 아니라
     이 Connector의 호출자에게 적용되는 규칙, 사용자 요청 원문):
     사용자 입력 해석, 요청 라우팅, 결과 조합 및 응답 반환.
     Planning/Workflow 생성 규칙/Agent 선택 기준/Task Lifecycle
     전이 규칙 등 모든 비즈니스 로직은 그대로 Core Domain Engine과
     `vault.task_lifecycle`에 남는다 — Milestone 23-T06(Execution
     Engine)에서 이미 확립한 "자연어 해석은 AI 고유 역할이라 결정적
     프로그램 대상이 아니다"라는 전제와 같은 선상이다.
  4. **Conversation Connector 자신도 `vault`/Core Domain Workflow·
     Task Engine/`AgentManager`(및 그 구체 구현)를 직접 import하지
     않는다** — `VaultAdapter`/`WorkflowTaskLink`/`WorkflowAgentLink`
     만 통해서 접근한다. `domain.Task`/`domain.Workflow`/
     `domain.Agent`/`TaskStatus`/`AgentCapability` 같은 순수 값
     타입은 메서드 시그니처에 그대로 쓴다 — `WorkflowAdapter`/
     `AgentAdapter`(T03)가 이미 이 값들을 Integration Layer 밖으로
     노출해 온 전례와 같다(새로운 경계 위반이 아니다).
  5. 이 경계를 `tests/integration_layer/
     test_conversation_connector_boundary.py`(신규)로 `ast` 기반
     자동 검증한다 — `conversation_workflow_link.py`가
     `ai_workspace.vault`/`ai_workspace.interfaces.{workflow_engine,
     task_engine,agent_manager,agent_registry,agent_scheduler}`/
     `ai_workspace.engines.{workflow_engine,task_engine}`/
     `ai_workspace.runtime.agent`를 import하지 않고,
     `ai_workspace.*` import는 전부 `integration.*` 또는
     `domain.*`인지 확인한다.
  6. `domain.Task`/`domain.Workflow`/`domain.Agent`에 새 필드를
     추가하지 않는다(T04/T05와 동일 원칙 — 이번에도 새 요청·응답
     dataclass는 전부 `integration/conversation_workflow_link.py`
     안에서만 정의).
- 대안:
  - `ConversationConnector`를 만들지 않고 Conversation Layer(호출
    자)가 `WorkflowTaskLink`/`WorkflowAgentLink`/`VaultAdapter`를
    각각 직접 호출 — 기각(사용자 명시적 요구사항: "모든 요청은
    Integration Layer를 통해 전달"). 호출자가 세 컴포넌트를 각각
    알아야 하고, 호출 순서(Task→Workflow→Agent) 같은 조합 지식이
    Conversation Layer 쪽에 흩어진다.
  - ADR-0040을 깨지 않기 위해 `WorkflowTaskLink`/`WorkflowAgentLink`
    를 하나로 합쳐 Conversation Connector 역할까지 겸하게 함 —
    기각. 유스케이스 하나(Task↔Workflow, Task↔Agent, 요청 오케스트
    레이션)당 책임 하나 원칙이 오히려 깨진다. 대신 ADR-0040을
    "Peer Connector"로 좁히고 "Orchestrating Connector"라는 이름
    있는 예외를 새로 정의하는 쪽이 더 명확하다(결정 2).
- 이유: Orchestrating Connector를 별도 개념으로 인정하면, M29
  이후 새 상위 유스케이스(예: 여러 Workflow를 묶는 Project 단위
  요청)가 생겨도 Peer Connector 규칙을 깨지 않고 같은 패턴(새
  Orchestrating Connector 하나)으로 확장할 수 있다 — Architecture
  Freeze에서 Integration Layer 역할이 "Adapter/Peer Connector/
  Orchestrating Connector" 3단으로 명확히 정리된다(사용자가 M28
  완료 후 요청한 Freeze 항목과 직접 연결).
- 결과/영향: `integration/conversation_workflow_link.py`(신규,
  `ConversationConnector`/`ConversationTaskRequest`/
  `ConversationTaskResult`/`ConversationStatusReport`),
  `integration/workflow_task_link.py`에 조회 전용 `get_task_status()`
  추가(로직 무변경, `WorkflowAdapter.get_task()` 위임),
  `integration/__init__.py` 갱신(Orchestrating Connector 개념 반영).
  `tests/integration_layer/test_conversation_connector.py`(신규
  3개)/`test_conversation_connector_boundary.py`(신규 2개).
  `docs/ARCHITECTURE.md`/`.ai/TASKS.md`에 반영. 새 Core Domain
  Interface 없음(27종 그대로), Domain 필드 추가 없음. **Milestone
  28(Live Task Management & Integration) 전체 완료** — 다음은
  사용자가 요청한 Architecture Freeze(ADR 전체 재검토/Layer
  의존성 검증/Integration Boundary 검증/Interface 목록 확정/M29
  요구사항 재정의).

## ADR-0042: M28 Architecture Freeze — Baseline 선언

- 상태: 승인됨 (2026-07-30, 사용자 지시 "M28 Architecture Freeze"
  프롬프트로 착수, 검토 결과는 이 ADR + `.ai/TASKS.md`의
  "Milestone 28 — Architecture Freeze" 절에 기록, 최종 승인은
  Freeze Report 제출 후 사용자 확인 대기)
- 날짜: 2026-07-30
- 배경: M28(T01~T06)이 모두 완료되어, ADR-0024(v0.5.0 Baseline
  선언, Milestone 4)와 같은 성격의 검증 절차를 요청받았다 — 새
  기능을 만들지 않고 Layer 구조/Integration Layer/Architecture
  Boundary/Domain/Public Interface/ADR 상호 정합성/확장성을
  전수 검토해 M29(Project Intelligence) 착수 전 기준선으로
  확정한다. 상세 절차와 발견 사항은 Freeze Report(`.ai/TASKS.md`)
  참고, 이 ADR은 그 결과로 내려진 결정만 기록한다.
- 결정:
  1. **Layer 구조를 그대로 기준선으로 확정한다** — Domain(`domain`/
     `interfaces`) → Application(`engines`/`runtime`/`agents`/
     `core`) → Integration(`integration/`) → Vault(`vault/`),
     그리고 Conversation(전용 코드 패키지 없음, `ConversationConnector`
     의 호출자로만 존재 — M23-T06 이후 "자연어 해석은 AI 역할"
     전제 유지). 단방향 의존, 순환 없음을 `git diff main...`
     (M28 브랜치 전체)로 `domain`/`interfaces`/`engines`/`runtime`
     디렉터리가 **한 줄도 바뀌지 않았음**을 근거로 확인했다 —
     Integration Layer가 순수하게 "위에 얹힌" 계층임이 코드
     자체로 증명된다.
  2. **Integration Layer 내부 구조(Adapter/Peer Connector/
     Orchestrating Connector)를 그대로 기준선으로 확정한다.**
     검증 중 실제 위반 1건을 발견해 즉시 수정했다(결정 3).
     `docs/ARCHITECTURE.md` §8에 규칙 19(Adapter/Peer Connector/
     Orchestrating Connector 참조 방향)/20(Conversation Layer
     Boundary)을 명문화해, 지금까지 ADR에만 있던 규칙을 §8 "의존성
     규칙" 표준 목록에도 반영했다(문서 보완, 새 규칙 아님).
  3. **위반 발견 및 수정**: `workflow_agent_link.py`(Peer Connector)
     가 `workflow_task_link.py`(다른 Peer Connector)에서 `WorkflowLink`
     를 import하고 있었다 — ADR-0040 "Peer Connector끼리 서로
     참조하지 않는다" 위반. `tests/integration_layer/
     test_connector_layering.py`(신규, 이번 Freeze에서 작성한 계층
     참조 방향 자동 검증)가 이를 실제로 검출했다. `WorkflowLink`를
     신설한 중립 모듈 `integration/models.py`(로직 없는 값 객체
     전용)로 옮겨 두 Peer Connector 모두 그 모듈만 참조하도록
     고쳤다 — 새 비즈니스 로직·새 Layer·새 Interface가 아니라
     기존 값 객체의 위치 수정이다.
  4. **Core Domain Interface 27종을 Public API로 동결한다** —
     이번 Freeze에서 시그니처 변경 없음, 신규 Interface 없음.
     Integration Layer의 Adapter/Connector 공개 메서드도 함께
     "현재 시점 Public API"로 문서화한다(Freeze Report 5절).
     `_` 접두 함수/상수(`vault/task_sync._upsert_bullet_section()`
     등)는 계속 Internal로 유지한다.
  5. **ADR-0035/0039/0040/0041 사이에 실질적 충돌은 없다**고
     확인한다. 두 곳의 표기 개선이 필요함을 발견했으나 지금
     고치지 않고 개선 후보로만 남긴다(Freeze Report 8절): (a)
     "Vault Integration Layer"(ADR-0035, `vault/`를 가리킴)와
     "Integration Layer"/"Workspace Adapter Layer"(ADR-0039,
     `integration/`을 가리킴)라는 이름이 비슷해 혼동 여지가 있다.
     (b) `docs/ARCHITECTURE.md` §3에서 Workspace Adapter Layer/
     Conversation Layer 절이 §3.21처럼 번호 있는 하위 절
     (`### 3.N`)이 아니라 번호 없는 하위 제목으로 붙어 있어 문서
     구조가 일관되지 않다.
  6. **확장성 확인** — Runtime/Service/Notification/Sync/MCP/
     GitHub Adapter는 전부 "외부 시스템 하나"라는 Adapter 정의를
     만족하므로, 기존 파일을 바꾸지 않고 `integration/`에 새
     `xxx_adapter.py`를 추가하는 것만으로 확장 가능하다고 확인했다.
     단, `test_connector_layering.py`의 분류 집합(`_ADAPTERS`/
     `_PEER_CONNECTORS`/`_ORCHESTRATING_CONNECTORS`)은 새 모듈을
     수동으로 등록해야 검증 대상이 된다는 점을 유지보수 주의사항
     으로 남긴다(자동 판별은 지금 만들지 않는다, YAGNI).
  7. **개선 후보 목록만 작성하고 지금 리팩토링하지 않는다**(사용자
     지시) — 전체 목록은 Freeze Report 8절.
- 대안:
  - 발견된 `WorkflowLink` 위반을 지금 고치지 않고 개선 후보로만
    남긴다 — 기각. "Architecture Boundary 유지"가 이 Freeze의
    완료 조건 중 하나인데, 이미 승인된 규칙(ADR-0040)을 위반하는
    코드를 "기준선"에 포함시키면 Freeze 자체가 거짓 선언이 된다.
    사소하고 기계적인 수정(값 객체 위치 이동)이라 "새 기능 금지"
    원칙과도 충돌하지 않는다고 판단했다.
  - §8에 규칙 19/20을 추가하지 않고 ADR 본문에만 남긴다 — 기각.
    §8은 이 프로젝트의 "의존성 규칙" 표준 목록이라고 이미
    §1.2/여러 ADR이 참조해 왔다 — 실제로 적용 중인 규칙이 그
    목록에 없으면 다음 세션이 §8만 보고 규칙을 놓칠 위험이 있다.
- 이유: Baseline 선언(ADR-0024)과 같은 목적 — 구조적 안정성을
  공식화해 M29 이후 작업이 "기존 구조 위에 조립"을 기본값으로
  삼게 한다. 이번 Freeze는 완전히 새로 설계한 구조가 아니라
  ADR-0039/0040/0041로 이미 점진적으로 승인해 온 구조를
  검증·문서화·(발견된 위반 1건만) 수정한 것이므로, ADR-0024와
  달리 버전 번호 상향은 하지 않는다 — 기능적 완성도가 바뀐 것이
  아니라 이미 존재하던 구조의 정합성을 확인한 것이기 때문이다.
- 결과/영향: `integration/models.py`(신규, `WorkflowLink`),
  `workflow_task_link.py`/`workflow_agent_link.py`/
  `conversation_workflow_link.py`(import 수정, 로직 무변경),
  `tests/integration_layer/test_connector_layering.py`(신규 3개
  — 이번 위반을 검출한 테스트, 이후 회귀 방지),
  `docs/ARCHITECTURE.md` §8 규칙 19/20 추가, `integration/
  __init__.py` 갱신. `.ai/TASKS.md`에 Freeze Report 전문 기록.
  `pytest`/`ruff`/`mypy` 전부 클린 확인(Freeze Report 참고). 새
  Interface 없음(27종 그대로), Domain 필드 추가 없음, `pyproject.toml`
  버전 무변경.

## ADR-0043: Intelligence Layer 도입 — `intelligence/` 신규 최상위 패키지, Vault Task 문서를 Project 단위 조회의 단일 데이터 소스로 채택 (Milestone 29-T01)

- 상태: 승인됨 (2026-07-30, 사용자가 M29 목표/DoD/Task 분해를 직접
  제시하고 승인 — "Query Layer Only/Read Only/Interface 변경
  금지(필요 시 사용자 승인)" 조건 포함)
- 날짜: 2026-07-30
- 배경: M28 Architecture Freeze(ADR-0042)로 27종 Core Domain
  Interface와 Integration Layer(Adapter/Peer Connector/
  Orchestrating Connector) 구조가 기준선으로 확정된 뒤, M29
  (Project Intelligence)는 Project/Workflow/Task/Agent/Event/Vault
  데이터를 종합해 Project Snapshot/Health/Risk/Recommendation을
  만드는 Read Only Query Layer를 요구받았다. 착수 전 데이터 접근
  경로를 조사한 결과 다음 두 가지 구조적 공백을 발견했다.
  1. `TaskEngine`(Core Domain)은 `get_task(task_id)` 단건 조회만
     제공하고 project 단위 전체 목록 조회(`list_tasks`)가 없다.
     `domain.Project`에도 소속 task_id 목록 필드가 없다.
  2. `WorkflowEngine`/`WorkflowTaskLink`/`WorkflowAgentLink`도
     "특정 Link/Agent 하나"에 대한 조회만 제공하고, project 전체의
     Workflow 목록이나 Agent 배정 전체 목록을 얻는 API가 없다.
  즉 Core Domain Interface 27종만으로는 "Project 전체 상태"를 만들
  수 없다 — 새 Interface(`list_tasks()` 등)를 추가하지 않는 한
  Snapshot 자체가 불가능하다. 반면 `vault/`의 `14 Tasks/*.md`
  문서(M27 Task 템플릿, M28 Live Task Management)는 파일 시스템
  열거만으로 project 소속 Task 전체(frontmatter: task_id/status/
  priority/milestone/owner/created/updated)를 이미 얻을 수 있다 —
  M28이 Vault를 "Live" 상태의 실제 운영 소스로 확립해 둔 결과다.
- 결정:
  1. **M29은 신규 Core Domain Interface를 추가하지 않는다.**
     Project 단위 열거가 필요한 Snapshot/Health/Risk/Recommendation은
     **Vault Task 문서(`14 Tasks/*.md`)를 단일 데이터 소스**로
     삼는다. `vault/task_query.py`(신규, Core Domain을 모르는 순수
     읽기 함수 — `vault/task_lifecycle.py`와 같은 성격)가 `14 Tasks/`
     디렉터리를 열거해 frontmatter를 파싱한 `TaskDocument` 목록을
     반환하고, `VaultAdapter.list_tasks()`(신규 메서드, Interface
     아님 — 기존 Adapter 클래스에 메서드 추가)가 이를 Integration
     Layer에 노출한다. `VaultAdapter`는 이미 "vault를 아는 유일한
     Integration 구성원"이라 이 확장은 기존 경계를 그대로 따른다
     (ADR-0039).
  2. **Agent 데이터는 `AgentAdapter.list_active_agents()`(기존
     메서드, M28-T03)를 그대로 재사용한다.** 신규 메서드 없음. 단,
     이 목록은 프로세스 내 `AgentRegistry`의 런타임 등록 상태이므로
     Vault 기반 운영(장기 실행 Agent Runtime 프로세스가 없는 일반
     사용 패턴)에서는 빈 목록일 수 있다는 한계를 그대로 문서화한다
     (해결은 M29 범위 밖).
  3. **Event(EventStore)는 M29 데이터 소스에서 제외한다.**
     `integration/`에 Event Adapter가 아직 없고, Vault frontmatter의
     `updated` 필드만으로 Risk Analyzer가 요구하는 "정체(Stagnant)"
     판단이 충분히 가능하다고 판단했다(YAGNI — 새 Adapter를 M29에서
     만들지 않는다).
  4. **Workflow 단위 집계는 Vault Task의 `milestone` 필드로
     근사한다.** Vault에는 Workflow 전용 문서 종류가 없다(M27
     `VaultDocumentKind`에 WORKFLOW 없음) — Task 그룹핑의 실질적
     상위 단위는 현재 `milestone` 뿐이다. 정확한 `Workflow`
     Interface 기반 집계가 필요해지면 그때 `list_tasks`류 신규
     Interface를 별도 ADR로 재논의한다(지금은 추가하지 않는다).
  5. **"Blocked Task"는 Vault frontmatter에 없는 개념이다** —
     `vault.task_lifecycle.TaskStatus`는 `{todo, in-progress, review,
     done, archived}` 5종뿐이고 `domain.task.TaskStatus`의
     `BLOCKED`/`CANCELLED`에 대응하는 값이 없다(두 enum은 ADR-0035에
     따라 원래 독립적이다). M29은 이 간극을 새 Interface나 새
     frontmatter 필드로 메우지 않고, **"정체(Stagnant) = IN_PROGRESS/
     REVIEW 상태이면서 `updated`가 임계일(기본값, 설정 가능) 이상
     지난 Task"** 규칙으로 "Blocked/장기 미진행"을 하나의 Risk
     신호로 근사한다(M29-T03에서 상세 규칙 정의, Rule 값은 T03
     구현 시 확정).
  6. **새 최상위 패키지 `intelligence/`를 만든다**(`integration/`과
     같은 층위, 그 위에 얹힌 신규 Layer). Analyzer(Snapshot/Health/
     Risk/Recommendation, T02~T04)는 오직 `integration/`의
     `VaultAdapter`/`AgentAdapter`에만 의존하고, `domain`/
     `interfaces`/`engines`/`vault`를 직접 import하지 않는다 —
     §8 규칙 18(Core Domain↔vault 직접 참조 금지)과 같은 성격의
     경계를 `intelligence/`에도 적용한다(§8 신규 규칙 21,
     `tests/intelligence/test_intelligence_layering.py`로 `ast`
     기반 강제 예정, M29-T02에서 작성).
- 대안:
  - `TaskEngine`에 `list_tasks(project_id)`를 추가해 Core Domain을
    단일 진실 공급원으로 삼는다 — 기각(사용자 조건: Interface 변경
    금지, 필요 시 승인). 또한 Vault가 이미 M28부터 "Live" 데이터의
    실질 운영 소스이므로 Core Domain 목록과 Vault 목록이 항상
    동기화된다는 보장이 없어(현재는 `WorkflowTaskLink`가 명시적으로
    연결한 Task만 양쪽에 존재), Core Domain을 소스로 삼으면 Vault에만
    있는 Task를 누락하는 문제가 오히려 생긴다.
  - Vault와 Core Domain 두 소스를 모두 조회해 병합한다 — 기각(YAGNI,
    복잡도 증가). "M29은 추론 엔진을 과도하게 키우지 않는다"는
    사용자 지침과 충돌 — 지금은 단일 소스로 충분히 DoD를 만족한다.
  - `Blocked` 판정을 위해 Vault frontmatter에 `blocked: bool` 필드를
    신규 추가한다 — 기각(지금 범위 밖, 문서 스키마 변경은 별도
    승인 필요). `updated` 기반 정체 규칙만으로 M29 DoD("Blocked Task"
    포함)를 충분히 만족할 수 있다고 판단했다.
- 이유: "Query Layer Only/Read Only/기존 Engine 활용/Core Domain
  수정 금지/Interface 변경 금지"라는 사용자 원칙을 문자 그대로
  지키면서, 실제로 열거 가능한 유일한 데이터 소스(Vault)만으로
  DoD 4가지 산출물(Snapshot/Health/Risk/Recommendation)을 전부
  만들 수 있음을 확인했다 — 새 Interface 없이도 M29 목표를 달성할
  수 있다는 것 자체가 이번 설계 검토의 핵심 결론이다.
- 결과/영향: 코드 변경 없음(설계 Task) — 다음 Task(M29-T02)에서
  `vault/task_query.py`/`VaultAdapter.list_tasks()`/`intelligence/`
  패키지를 실제로 만든다. `docs/ARCHITECTURE.md` §3.22(신규)/§8
  규칙 21(신규) 갱신, `.ai/TASKS.md`에 Milestone 29 절 신규 추가.
  새 Core Domain Interface 없음(27종 그대로), `domain.Project`/
  `domain.Task` 필드 추가 없음, `vault.models.VaultDocumentKind`
  변경 없음.

## ADR-0044: Context Intelligence 설계 — `KnowledgeAdapter` 신규(Integration Layer), Markdown 제목 단위 파싱으로 `ProjectContext` 구성 (Milestone 30-T01)

- 상태: 승인됨 (2026-07-30, 사용자가 M30 목표/DoD/Task 분해를 직접
  제시하고 승인 — "새로운 지식을 생성하지 않는다/LLM 기반 추론을
  하지 않는다/기존 Knowledge Layer Interface만 재사용" 조건 포함)
- 날짜: 2026-07-30
- 배경: M29(Project Intelligence)가 Vault Task 데이터로 "프로젝트
  상태"를 이해하는 기반을 만들었다면, M30(Context Intelligence)은
  "지금 하는 작업(Task/Milestone)과 관련된 맥락"을 모아 정리한다.
  이미 Milestone 16(ADR-0028)이 `KnowledgeRepository`/
  `KnowledgeSearch`/`KnowledgeProvider`(Core Domain Interface 27종
  중 3종)로 `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/RULES.md`
  /`.ai/TASKS.md`/`docs/ROADMAP.md`/`docs/PRD.md` 6개 파일을
  `KnowledgeDocument`로 노출하고 있어, M30의 자연스러운 데이터
  소스다. 다만 `FileKnowledgeRepository`는 파일 하나를 문서 하나로
  통째로 노출한다(M16, YAGNI로 문단 단위 파싱을 하지 않기로 결정)
  — 그래서 "관련 ADR-0043" 같은 세부 항목 단위 참조를 얻으려면,
  이미 반환된 문서 텍스트를 추가로 구조화해야 한다.
- 결정:
  1. **신규 Integration Layer Adapter `KnowledgeAdapter`를 만든다**
     (`integration/knowledge_adapter.py`) — `KnowledgeRepository`/
     `KnowledgeSearch` **Interface**에만 의존한다(Interface First,
     기존 `VaultAdapter`/`WorkflowAdapter`/`AgentAdapter`와 동일한
     설계). 새 Core Domain Interface가 아니다 — 이미 있는 3종
     Interface를 감싸기만 한다. `integration/__init__.py`가 이미
     "Adapter는 향후 Runtime/Service/Notification/Sync 등으로
     확장 가능한 계층"이라고 명시해 둔 대로, 이번 확장은 그 경계
     안에서의 신규 구성원 추가이지 Layer Boundary 변경이 아니다.
  2. **새 지식을 만들지 않는다** — `KnowledgeAdapter`가 반환하는
     6개 문서의 전체 텍스트를, Markdown 제목(`#`/`##`/`###`) 단위로
     쪼개는 것까지만 한다(`intelligence/context.py`,
     `ContextAnalyzer`). 각 (제목, 본문) 구간에 `subject`(예:
     "M30-T03" 또는 "M29")가 부분 문자열로 포함되면 `ContextEntry`
     로 채택한다 — 이 문서들이 실제로 `## ADR-0043: ... (Milestone
     29-T01)`처럼 Milestone/Task 식별자를 제목에 담는 이 저장소의
     실제 작성 관례를 그대로 이용한다. 새 데이터를 생성하거나
     LLM으로 요약하지 않는다(사용자 지시).
  3. **Freshness는 파일 mtime이 아니라 제목에서 추출한 Milestone
     번호 거리로 판단한다**(`intelligence/context_quality.py`).
     이 저장소는 매 세션 fresh clone이라 파일 mtime이 "체크아웃
     시각"만 반영해 실제 최신성과 무관하다 — filesystem stat이나
     git log 조회(별도 외부 시스템 접근)를 새로 추가하는 대신,
     이미 파싱한 Milestone 번호(`현재 Milestone - 언급된 Milestone`)
     로 "오래된 참조"를 근사한다. Adapter가 두 개의 서로 다른 외부
     시스템(Knowledge Interface + git)에 동시에 의존하게 되는 것도
     피한다(ADR-0039 "Adapter는 외부 시스템 하나만" 원칙 유지).
  4. **Gap은 "특정 Knowledge 종류에 subject 언급이 0건"으로
     판정한다** — ADR/TASK/ARCHITECTURE 3종은 Milestone 작업이면
     최소 하나는 있어야 자연스러운 문서라 Gap 판정 대상으로 삼고,
     RULE/PROJECT(ROADMAP/PRD)는 특정 Task마다 언급되지 않는 것이
     정상인 범용 문서라 Gap 판정에서 제외한다.
  5. `ProjectContext`/`ContextEntry`/`ContextQuality`/
     `ContextFreshness`/`ContextGap`을 `intelligence/`의 새 domain
     성격 값 객체로 둔다 — Core Domain `domain/`에는 아무것도
     추가하지 않는다(§8 규칙 21 그대로, `intelligence/`는
     `KnowledgeAdapter`에만 의존).
- 대안:
  - `KnowledgeRepository`/`KnowledgeSearch`에 문단/제목 단위 파싱을
    추가한다(Interface 확장) — 기각(사용자 조건: 기존 Knowledge
    Layer Interface만 재사용). M16이 YAGNI로 이미 보류한 결정을
    M30에서 뒤집을 이유가 없다 — Integration Layer 위에서 파싱해도
    같은 결과를 얻을 수 있다.
  - Freshness를 파일 mtime/git log로 판단한다 — 기각(위 배경 설명,
    mtime은 이 저장소 운영 방식과 안 맞고, git log는 Adapter의
    "외부 시스템 하나" 원칙과 충돌).
  - `intelligence/context.py`가 `KnowledgeRepository`를 직접
    주입받는다(Adapter 생략) — 기각. §8 규칙 21이 이미
    "`intelligence/`는 Integration Layer Adapter에만 의존"이라고
    못박아 뒀고, M29도 예외 없이 이 규칙을 지켰다 — 일관성 유지.
- 이유: 사용자가 요구한 "새 지식 생성 금지/LLM 추론 금지/기존
  Interface만 재사용"을 문자 그대로 지키면서, 이 저장소의 실제
  문서 작성 관례(제목에 ADR/Milestone 번호를 명시하는 습관)만으로
  충분히 유용한 `ProjectContext`(관련 ADR/RULES/Architecture/
  Decision/Task/Roadmap/PRD 연결 + Freshness + Gap)를 만들 수
  있음을 확인했다 — M29-T01이 "새 Interface 없이 가능한가"를
  먼저 검증했던 것과 같은 접근이다.
- 결과/영향: 코드 변경 없음(설계 Task) — 다음 Task(M30-T02)에서
  `integration/knowledge_adapter.py`/`intelligence/context.py`를
  실제로 만든다. `docs/ARCHITECTURE.md` §3.23(신규) 갱신,
  `.ai/TASKS.md`에 Milestone 30 절 신규 추가. 새 Core Domain
  Interface 없음(27종 그대로), `domain/` 필드 추가 없음.

## ADR-0045: Capability Intelligence 설계 — `AgentAdapter` 확장(신규 Adapter 아님), "정의된 Capability 대비 활성 Agent 커버리지"로 Gap 판정 (Milestone 31-T01~T05)

- 상태: 승인됨 (2026-07-30, 사용자가 "M31을 M29/M30과 동일하게
  진행"이라고 지시 — Rule 기반만/LLM 추론 금지/새 Core Domain
  Interface 금지 조건은 M29-T01/M30-T01에서 이미 확립된 원칙을
  그대로 승계)
- 날짜: 2026-07-30
- 배경: M29(Project Intelligence)가 Task 데이터로 "프로젝트 상태",
  M30(Context Intelligence)이 "지금 작업의 맥락"을 정리했다면,
  M31(Capability Intelligence)은 "이 시스템이 실제로 수행할 수
  있는 능력(Capability)"을 정리한다. `domain/agent.py`가 이미
  `AgentCapability` 11종(Coordination/Planning/Coding/Review/
  Documentation/Research/Vision/Voice/Git/MCP/Shell)을 정의하고,
  Milestone 28의 `AgentAdapter`(`AgentManager`/`AgentRegistry`/
  `AgentScheduler` 3종 Interface를 감쌈)가 `list_active_agents()`로
  활성 Agent를 이미 노출하고 있어, M31의 자연스러운 데이터 소스다.
  다만 이 값은 In-Memory Registry 특성상 실제 Agent 프로세스가
  떠 있을 때만 채워진다(M29도 이미 겪은 한계 — 실제 커밋된 Vault
  리포트의 `활성 Agent 수`가 항상 0으로 관찰됨). M31은 이 한계를
  숨기지 않고 그대로 반영한다.
- 결정:
  1. **새 Adapter를 만들지 않는다 — 기존 `AgentAdapter`를
     확장한다**(`integration/agent_adapter.py`). `list_active_agent_
     capabilities() -> list[AgentCapabilityView]`(활성 Agent를
     `domain.agent.Agent`를 노출하지 않는 Adapter 전용 DTO로 변환,
     `VaultAdapter.TaskDocumentView`/`KnowledgeAdapter.
     KnowledgeDocumentView`와 동일한 원칙)와 `known_capabilities()
     -> frozenset[str]`(정의된 `AgentCapability` 전체를 문자열
     카탈로그로 변환, 단순 나열이라 Adapter의 "비즈니스 로직 없음"
     원칙 위반이 아님) 두 메서드만 추가한다 — M30이 `VaultAdapter`
     에 `publish_project_context()`를 추가한 것과 같은 확장
     방식이다. 새 Core Domain Interface가 아니다.
  2. **집계(Snapshot)와 판단(Gap)을 분리한다**(M29/M30과 동일한
     2단 Analyzer 구조). `intelligence/capability.py`의
     `CapabilitySnapshotAnalyzer`는 `AgentAdapter`가 노출한 값만
     읽어 Capability별/Role별 활성 Agent 수를 집계한다(판단 없음).
     `intelligence/capability_gap.py`의 `CapabilityGapAnalyzer`는
     그 Snapshot만 입력으로 받아(Adapter 재호출 없음) "정의된
     Capability 중 활성 Agent가 0명인 것"을 Gap으로 판정한다.
  3. **Coverage 등급은 healthy/warning/critical이 아니라
     none/partial/full을 쓴다.** M29/M30은 "이상 상태를 알리는"
     의미로 healthy/warning/critical을 썼지만, M31에서 활성 Agent
     0명은 시스템 결함이 아니라 이 저장소가 아직 Agent 프로세스를
     상시 구동하지 않는 워크숍 단계라는 사실을 반영할 뿐이다 —
     매번 "Critical"로 표시하면 실제로 없는 문제를 있는 것처럼
     과장하게 된다. 중립적인 이름으로 이 차이를 명시한다.
  4. `AgentCapabilitySnapshot`/`CapabilityGap`/`CapabilityCoverage`/
     `CapabilityGapReport`를 `intelligence/`의 새 domain 성격 값
     객체로 둔다 — Core Domain `domain/`에는 아무것도 추가하지
     않는다(§8 규칙 21 그대로, `intelligence/`는 `AgentAdapter`
     에만 의존).
  5. **결과는 같은 Vault 폴더에 새 파일로 노출한다** —
     `vault/capability_report.py`(M29-T05/M30-T05와 동일 패턴,
     원자적 전체 교체)가 `15 Project Intelligence/Capability
     Intelligence.md`에 쓴다. 새 최상위 Vault 폴더를 만들지 않는다.
- 대안:
  - `AgentRegistry`에 Capability 집계 메서드를 추가한다(Interface
    확장) — 기각. Core Domain Interface는 "생성/등록/조회/선택"
    책임만 가지며, 집계·판단은 Intelligence Layer의 몫이라는 M29/
    M30의 경계를 M31에서 뒤집을 이유가 없다.
  - Vault Task 문서의 `owner` 필드(자유 텍스트, "담당자/담당
    Agent")를 Capability 수요 신호로 매핑한다 — 기각. `owner`는
    고정된 명명 규칙이 없는 자유 텍스트라(사람 이름/역할명 혼용),
    Capability 값으로 안정적으로 매핑할 근거가 없다 — 새 명명
    관례를 이번에 발명하는 것은 "새 지식/판단 기준을 만들지
    않는다"는 M29/M30의 원칙과 충돌한다.
  - Coverage 등급도 M29/M30과 같이 healthy/warning/critical을
    쓴다 — 기각(위 결정 3 이유). 활성 Agent 0명이 상시 "Critical"로
    보고되면 리포트의 신뢰도만 떨어진다.
- 이유: 새 Interface/Adapter 없이 기존 `AgentAdapter`만 확장해
  "정의된 Capability 대비 실제 커버리지"라는, 이 시점에 정직하게
  계산 가능한 값만으로 유용한 리포트를 만들 수 있음을 확인했다 —
  M29-T01/M30-T01이 먼저 검증했던 접근과 동일하다.
- 결과/영향: `integration/agent_adapter.py`(확장)/
  `intelligence/capability.py`(신규)/`intelligence/
  capability_gap.py`(신규)/`intelligence/capability_service.py`
  (신규)/`vault/capability_report.py`(신규)/`integration/
  vault_adapter.py`(`publish_capability_report()` 추가) 구현
  완료(M31-T02~T05, 신규 테스트 18개 포함 pytest 947개, ruff, mypy
  전부 통과). `docs/ARCHITECTURE.md` §3.24(신규) 갱신, `.ai/TASKS.md`
  에 Milestone 31 절 신규 추가. 새 Core Domain Interface 없음
  (27종 그대로), `domain/` 필드 추가 없음.

## ADR-0046: Intelligence Synthesis 도입 — 새 Analyzer/Adapter 없이 M29~M31 Service 3개를 조합해 `IntelligenceOverview` 생성 (Milestone 32-T01~T04)

- 상태: 승인됨 (2026-07-30, 사용자가 "M32는 기능 추가가 아니라
  Intelligence Layer의 통합 계층(Integration at the Intelligence
  Layer)을 완성하는 Milestone"이라고 확정 — Rule 기반만/LLM 추론
  금지/새 Core Domain Interface 금지 조건은 M29-T01/M30-T01/
  M31-T01에서 이미 확립된 원칙을 그대로 승계)
- 날짜: 2026-07-30
- 배경: M29(Project Intelligence)/M30(Context Intelligence)/
  M31(Capability Intelligence)이 각각 독립적으로 계산한 리포트를
  모두 `15 Project Intelligence/` Vault 폴더에 별개 파일(`Project
  Intelligence.md`/`Project Context.md`/`Capability Intelligence.md`)
  로만 노출하고 있어, 세 리포트를 교차로 보려면 파일을 3개 열어야
  했다. M32는 이 셋을 잇는 마지막 조각으로, 새로운 데이터 소스나
  판단 기준을 추가하지 않고 이미 완성된 3개 Service
  (`ProjectIntelligenceService`/`ContextIntelligenceService`/
  `CapabilityIntelligenceService`)의 `generate()` 결과만 조합한다.
- 결정:
  1. **새 Adapter/Interface를 만들지 않는다.** `intelligence/
     synthesis.py`의 `IntelligenceSynthesisAnalyzer`는 이미 생성된
     세 리포트(`ProjectIntelligenceReport`/`ProjectContextReport`/
     `CapabilityIntelligenceReport`)만 입력으로 받는 순수 함수
     계층이다 — Adapter를 전혀 참조하지 않는다.
  2. **§8 규칙 21은 변경 없이 그대로 적용된다.** 지금까지 규칙 21은
     "`intelligence/`의 Analyzer는 `integration/`의 Adapter에만
     의존"이었다. M32는 Adapter가 아니라 **같은 `intelligence/`
     계층의 다른 Service**(`report.py`/`context_service.py`/
     `capability_service.py`)를 조합하므로 애초에 이 규칙이 금지하는
     대상이 아니다 — `tests/intelligence/test_intelligence_layering.py`
     를 그대로 실행해 위반이 없음을 코드로 확인했다(수정 불필요).
     별도 규칙 신설도 하지 않는다.
  3. **집계(Synthesis)와 조합(Service)을 분리한다**(M29/M30/M31과
     동일한 2단 구조). `intelligence/synthesis.py`의
     `IntelligenceSynthesisAnalyzer`는 세 리포트의 등급(Health/
     Freshness/Coverage)과 Risk/Gap을 하나의 `Finding` 목록으로
     모으기만 한다 — 새 우선순위 알고리즘·새 임계값을 만들지 않는다.
     `intelligence/synthesis_service.py`의
     `IntelligenceSynthesisService`가 세 Service를 생성자로 받아
     순서대로 실행한 뒤 Analyzer에 넘기는 조합 책임만 진다(M29-T05
     `report.py`와 동일한 Orchestrating 패턴).
  4. **결과는 같은 Vault 폴더에 새 파일로 노출한다** —
     `vault/intelligence_overview.py`(M29/M30/M31과 동일 패턴, 원자적
     전체 교체)가 `15 Project Intelligence/Intelligence Overview.md`에 쓴다.
     `VaultAdapter`에 `publish_intelligence_overview()` 메서드 1개만
     추가한다(신규 Adapter 아님, M30/M31과 동일한 확장 방식).
- 대안:
  - 세 Service의 Adapter(`VaultAdapter`/`KnowledgeAdapter`/
    `AgentAdapter`)를 Synthesis Service가 직접 다시 주입받아 세
    Analyzer를 처음부터 다시 조립한다 — 기각. 이미 완성된 Service가
    "생성→렌더링→발행"을 캡슐화하고 있는데 이를 우회하면 같은 로직이
    두 곳에 중복된다(DRY 위반, YAGNI).
  - Overview에 세 리포트 각각의 우선순위를 다시 계산하는 새
    가중치/점수 체계를 도입한다 — 기각. 이번 Milestone의 목적은
    "통합"이지 "새 판단 추가"가 아니다 — Finding을 그대로 나열하고
    정렬만 하는 최소 구현으로 충분하다.
  - `15 Project Intelligence/` 대신 새 최상위 Vault 폴더를 만든다 —
    기각. M29~M31이 이미 이 폴더를 "Intelligence 결과 전용"으로
    확립했고, Overview도 같은 성격의 산출물이다.
- 이유: 새 Interface/Adapter/판단 기준 없이 기존 3개 Service만
  조합해도 "프로젝트 상태 + 지금 작업 맥락 + 시스템 능력"을 한 문서로
  볼 수 있음을 확인했다 — M29~M31이 세운 "새 데이터 소스·새 판단
  없이 이미 있는 것만 재사용" 원칙을 통합 계층에도 그대로 적용한
  결과다.
- 결과/영향: `intelligence/synthesis.py`(신규)/`intelligence/
  synthesis_service.py`(신규)/`vault/intelligence_overview.py`
  (신규)/`integration/vault_adapter.py`(`publish_intelligence_
  overview()` 추가) 구현 완료(M32-T02~T04, 신규 테스트 7개 포함
  pytest 954개, ruff, mypy 전부 통과). `docs/ARCHITECTURE.md`
  §3.25(신규) 갱신, `.ai/TASKS.md`에 Milestone 32 절 신규 추가. 새
  Core Domain Interface 없음(27종 그대로), 새 Integration Layer
  Adapter 없음(`VaultAdapter` 확장 1건), `domain/` 필드 추가 없음.

## ADR-0047: Session Resume 도입 — Current Work Selector 1개 + M29~M32 재사용으로 세션 시작 시 자동 복원 문서 생성 (Milestone 33-T01~T04)

- 상태: 승인됨 (2026-07-30, 사용자가 "M33은 새로운 Intelligence를
  계산하지 않는다 — 이미 구축된 Project/Context/Capability
  Intelligence와 Intelligence Overview를 활용해 현재 프로젝트
  상태를 자동으로 복원하는 Read-Only Session Resume를 구현한다"고
  확정)
- 날짜: 2026-07-30
- 배경: M29~M32로 Intelligence Layer 기반이 완성됐지만, 지금까지는
  모두 "리포트를 만들어 Vault에 둔다"까지였다 — 세션을 새로 시작한
  사람(또는 AI)이 "지금 무엇을 하고 있었는가"를 알려면 여전히 3~4개
  파일을 직접 열어야 했다. 기존 세션 연속성 기능(M8,
  `PlanningAgent`의 `memory_snapshot_id` 자동 복원)은 이것과 다른
  계층이다 — M8은 Agent 실행 컨텍스트(LLM에 넘길 요약 텍스트)를
  `ContextManager`/`MemoryEngine`으로 복원하는 내부 메커니즘이고,
  M33은 사람이 읽는 보고서를 Intelligence Layer에서 만드는 Read
  Only Query Layer다 — Interface·Layer가 겹치지 않는다.
- 결정:
  1. **"현재 작업" 판정 규칙 1개만 새로 추가한다.** 새 지표·점수가
     아니라, `VaultAdapter.list_tasks()`(M29부터 존재)가 이미
     노출한 `status`/`updated` 값에서 "활성 상태(in-progress/
     review) Task 중 `updated`가 가장 최근인 1건"을 고르는 순수
     선택 로직이다(`intelligence/session_resume.py`의
     `CurrentWorkSelector`). Health/Risk/Coverage 같은 새 판단
     기준을 만드는 것이 아니라, 이미 계산 가능한 값 중 "지금 보여줄
     것 하나"를 고르는 것뿐이다.
  2. **새 Adapter/Interface를 만들지 않는다.**
     `intelligence/session_resume_service.py`의
     `SessionResumeService`는 `VaultAdapter`(기존, "현재 작업" 조회용)
     + `ProjectIntelligenceService`/`ContextIntelligenceService`/
     `CapabilityIntelligenceService`(M29~M31, 리포트 3종 생성) +
     `IntelligenceSynthesisAnalyzer`(M32, Overview 합성)를 그대로
     조합한다. `IntelligenceSynthesisService`(M32 Service)를 감싸지
     않고 Analyzer 클래스만 재사용하는 이유는 M29
     `ProjectIntelligenceReport.recommendations`("다음 작업")가
     Overview 밖에 있어 직접 필요하기 때문이다 — 어차피 세 리포트를
     손에 쥐고 있어야 하므로, Overview까지 자체적으로 다시 합성하는
     편이 M32 Service를 감싸는 것보다 단순하다(추가 의존성 없음).
  3. **"다음 작업"은 새로 만들지 않고 M29 Recommendation을 그대로
     노출한다.** M29-T04가 이미 "Rule 기반, AI 추론 없음"으로 다음
     행동을 계산해 두었으므로, Session Resume이 이를 다시 계산할
     이유가 없다(DRY) — Recommendation을 그대로 옮겨 담는다.
  4. **결과는 같은 Vault 폴더에 새 파일로 노출한다** —
     `vault/session_resume.py`(M29~M32와 동일 패턴, 원자적 전체
     교체)가 `15 Project Intelligence/Session Resume.md`에 쓴다.
  5. **CLI 노출·자동 트리거는 범위 밖이다.** "문서를 만드는 능력"
     까지가 M33이고, "언제 자동으로 만들지"(세션 시작 Hook/Automation
     Engine 연결)는 M29~M32도 CLI 연동 없이 Vault만 노출한 것과
     같은 이유로 다음 Milestone 대상이다(YAGNI, 현재 CLI는
     Intelligence/Vault를 전혀 모른다).
- 대안:
  - `IntelligenceSynthesisService`(M32)를 그대로 주입받아
    `generate()` 결과(Overview)만 쓰고 "다음 작업"은 Overview의
    Finding으로 대체한다 — 기각. Overview의 Finding은 Risk/Gap만
    담고 있어 M29 Recommendation의 "다음 행동" 의미를 대체하지
    못한다 — 이미 있는 Recommendation을 버리고 Finding으로 재해석
    하면 오히려 "새로운 판단"을 만드는 셈이 된다.
  - "현재 작업" 판정에 Owner 필드나 Priority까지 반영하는 복합
    규칙을 만든다 — 기각. M31이 이미 "Vault Task의 `owner`는 고정
    명명 규칙이 없어 신호로 쓰지 않는다"고 결정했고, Priority까지
    섞으면 "가장 최근 갱신"이라는 단순하고 예측 가능한 규칙이
    깨진다(KISS, YAGNI).
  - Session Resume 전용 CLI 명령을 이번에 함께 추가한다 — 기각.
    CLI(`cli/main.py`)는 현재 `WorkspaceCore`만 조립하고
    Vault/Intelligence를 전혀 참조하지 않는다 — 새 배선이 필요해
    Scope가 커진다. Vault 노출만으로 DoD("Session Resume 생성
    여부")를 충족한다.
- 이유: 새 Interface/Adapter/판단 기준 없이 "현재 작업 선택" 규칙
  하나만 더해도 M29~M32가 이미 계산해 둔 값들로 "지금 무엇을 하고
  있었는가"에 답하는 문서를 만들 수 있음을 확인했다 — Intelligence
  Layer를 처음으로 실제 사용 시나리오(세션 시작)에 연결하는
  Execution 쪽 첫걸음이라는 점에서 M29~M32와 다른 성격이지만, "새로운
  지식을 만들지 않는다"는 원칙은 그대로 유지한다.
- 결과/영향: `intelligence/session_resume.py`(신규)/`intelligence/
  session_resume_service.py`(신규)/`vault/session_resume.py`
  (신규)/`integration/vault_adapter.py`(`publish_session_resume()`
  추가) 구현 완료(M33-T02~T04, 신규 테스트 8개 포함 pytest 962개,
  ruff, mypy 전부 통과). `docs/ARCHITECTURE.md` §3.26(신규) 갱신,
  `.ai/TASKS.md`에 Milestone 33 절 신규 추가. 새 Core Domain
  Interface 없음(27종 그대로), 새 Integration Layer Adapter 없음
  (`VaultAdapter` 확장 1건), `domain/` 필드 추가 없음.

## ADR-0048: Workflow Intelligence 도입 — "Workflow" = Milestone Task 실행 흐름(domain.Workflow 아님), Blocked Rule 1개 + WorkflowFlowAnalyzer 캡슐화 (Milestone 34-T01~T04)

- 상태: 승인됨 (2026-07-30, 사용자가 M34 Milestone 계획(목표/Scope/
  DoD/Task 구성/Architecture 영향/구현 전략)을 승인하며 3가지 수정
  권고 — ① ADR에 Workflow 의미 명시 ② Blocked Rule 기반 정의
  ③ WorkflowFlowAnalyzer로 흐름 분석 캡슐화 — 를 명시적으로 반영할
  것을 조건으로 확정)
- 날짜: 2026-07-30
- 배경: M29~M33으로 Intelligence Layer가 Vault Task 문서를 단일
  데이터 소스로 삼아 Project/Context/Capability/Synthesis/Session
  Resume을 구축했다. `docs/ARCHITECTURE.md` §7과 `.ai/TASKS.md`
  Milestone 32/33 절이 다음 단계로 "Workflow Intelligence"를
  명시했지만, 착수 전 조사 결과 **이 저장소에는 `domain.Workflow`
  인스턴스를 조회할 수 있는 기존 데이터 소스가 없다** —
  `domain/workflow.py`의 `Workflow`는 `workflow_id`/`mission_id`/
  `task_ids`/`dependencies`만 가진 휘발성 in-memory 값 객체로,
  상태·타임스탬프·영속 저장소가 전혀 없고 `WorkflowAdapter`에도
  `list_workflows()` 같은 조회 메서드가 없다. M29 Project
  Intelligence조차 `domain.Workflow`를 전혀 참조하지 않는다(Vault
  Task 문서만 읽음). 반면 이 저장소가 실제로 반복하는 "Workflow"는
  Milestone 안의 Task 실행 순서(`M33-T01`→`T02`→`T03`→`T04`처럼
  매 Task 말미에 "다음 Task"를 명시하는 순차 흐름) 그 자체이며, 이는
  이미 `VaultAdapter.list_tasks()`(M29부터 존재)로 조회 가능하다.
- 결정:
  1. **"Workflow"를 재정의한다 — `domain.Workflow`가 아니라 Milestone
     안의 Task 실행 흐름이다.** `domain/workflow.py`/
     `interfaces/workflow_engine.py`/`runtime/workflow/
     workflow_runner.py`/`integration/workflow_adapter.py`는 이번
     Milestone에서 전혀 사용하지 않는다 — 새 영속 계층을 만들어
     `Workflow` 인스턴스를 저장하기 시작하는 것은 Scope를 크게
     키우는 선택이라 채택하지 않는다(YAGNI). "Workflow Intelligence"
     라는 이름은 유지하되, 대상은 "Vault Task 문서에 이미 기록된
     Milestone·Task 실행 순서"로 한정한다 — 이 재정의를 코드 주석과
     문서에 명시해, 향후 누군가 `domain.Workflow`와 혼동하지 않도록
     한다.
  2. **Blocked를 Rule 기반으로 정의한다.** Task ID(`M{n}-T{nn}`)에서
     추출한 T-번호로 같은 Milestone 내 Task를 정렬했을 때, `status`가
     `todo`이면서 그보다 T-번호가 작은(선행) Task 중 완료 상태
     (`done`/`archived`)가 아닌 것이 하나라도 있으면 **Blocked**다.
     선행 Task가 모두 완료됐는데 아직 `todo`인 Task는 **Next(다음
     실행 가능)**로 구분한다. `in-progress`/`review`는 진행 중,
     `done`/`archived`는 완료로 그대로 노출한다 — 새 상태 분류를
     만들지 않고 기존 `status` 값과 Task ID 순서만으로 판정하는
     순수 Rule이다.
  3. **분석 로직을 `WorkflowFlowAnalyzer`(신규, `intelligence/
     workflow_flow.py`)라는 순수 Analyzer에 전부 캡슐화한다.**
     입력은 `VaultAdapter.list_tasks()`가 반환하는
     `TaskDocumentView` 목록뿐이고, 출력은 Milestone별 정렬된 Task
     흐름 + Blocked/Next 판정이다. `WorkflowIntelligenceService`
     (`intelligence/workflow_service.py`, M34-T03)는 `VaultAdapter`
     호출과 `WorkflowFlowAnalyzer` 실행을 조합·오케스트레이션만
     하고, Blocked/Next 규칙 자체는 갖지 않는다 — M29
     `ProjectSnapshotAnalyzer`/`HealthRiskAnalyzer`와 Service를
     분리해 온 기존 패턴과 동일하며, M35(Recommendation)/M36
     (Automation)이 이 Analyzer를 그대로 재사용할 수 있게 한다.
  4. **새 Adapter/Interface를 만들지 않는다.** `VaultAdapter`에
     `publish_workflow_intelligence()` 메서드 1개만 추가한다
     (M29~M33과 동일 패턴). Core Domain Interface 27종은 그대로다.
  5. **결과는 같은 Vault 폴더에 새 파일로 노출한다** —
     `vault/workflow_intelligence.py`(신규, 원자적 전체 교체)가
     `15 Project Intelligence/Workflow Intelligence.md`에 쓴다.
  6. **CLI 노출·자동 트리거·M35 Recommendation·M36 Automation
     연동은 범위 밖이다.** M29~M33과 동일한 이유(YAGNI, 현재 CLI는
     Intelligence/Vault를 전혀 모른다)로 다음 Milestone 대상이다.
- 대안:
  - `domain.Workflow`/`WorkflowAdapter`를 이번에 확장해 Workflow
    인스턴스를 Vault 또는 별도 저장소에 영속화한 뒤 그것을 분석
    대상으로 삼는다 — 기각. 새 영속 계층 + 새 Adapter 메서드 +
    기존 `WorkflowRunner` 실행 경로와의 동기화까지 필요해 M34
    단독으로 감당하기엔 Scope가 지나치게 커지고, "이미 있는 것을
    재사용"하는 M29~M33의 설계 철학과 어긋난다.
  - Blocked 판정에 `priority`나 `owner`까지 반영하는 복합 규칙을
    만든다 — 기각. M31이 "Vault Task의 `owner`는 고정 명명 규칙이
    없어 신호로 쓰지 않는다"고 이미 결정했고, Priority까지 섞으면
    "선행 Task 완료 여부"라는 단순하고 예측 가능한 규칙이 깨진다
    (KISS, YAGNI).
  - Blocked/Next 판정 로직을 `WorkflowIntelligenceService` 안에 직접
    작성한다(별도 Analyzer 없이) — 기각. 사용자 권고대로 Service에는
    조합·오케스트레이션만 남기고 판정 규칙은 Analyzer에 모아둬야
    M35/M36이 재사용하기 쉽다 — M29의 Analyzer/Service 분리 패턴과도
    일관된다.
- 이유: 새 Interface/Adapter/영속 계층 없이, 이미 Vault에 기록된
  Task ID 순서·상태만으로 "지금 Milestone의 실행 흐름 중 어디가
  막혔고 다음에 무엇을 해야 하는가"에 답할 수 있음을 확인했다 —
  M29~M33이 지켜온 "새로운 지식을 만들지 않는다" 원칙을 그대로
  유지하면서, Workflow라는 이름이 가리키는 대상을 이 저장소의 실제
  데이터 현실에 맞게 재정의한 것이 이번 결정의 핵심이다.
- 결과/영향: `intelligence/workflow_flow.py`(신규)/`intelligence/
  workflow_service.py`(신규)/`vault/workflow_intelligence.py`
  (신규)/`integration/vault_adapter.py`(`publish_workflow_intelligence()`
  추가) 구현 완료(M34-T02~T04, 신규 테스트 14개 포함 pytest 976개,
  ruff, mypy 전부 통과). `docs/ARCHITECTURE.md` §3.27(신규) 갱신,
  `.ai/TASKS.md`에 Milestone 34 절 신규 추가. 새 Core Domain
  Interface 없음(27종 그대로), 새 Integration Layer Adapter 없음
  (`VaultAdapter` 확장 1건), `domain/` 필드 추가 없음,
  `domain.Workflow`/`WorkflowEngine`/`WorkflowAdapter` 무변경
  (사용하지 않음).

## ADR-0049: Recommendation Intelligence 도입 — 5단계 Priority Rule 1개로 M29~M34 Intelligence를 그대로 소비하는 Decision Layer (Milestone 35-T01~T04)

- 상태: 승인됨 (2026-07-30, 사용자가 M35 Milestone 계획(목표/Scope/
  DoD/Architecture/Task 구성 T01~T04/구현 전략/MDD Review)을 승인하며
  "T01부터 T04까지 중간 승인 없이 구현한 뒤 Milestone Review로 최종
  승인을 다시 요청"하는 진행 방식까지 확정)
- 날짜: 2026-07-30
- 배경: M29(Project)/M30(Context)/M31(Capability)/M32(Synthesis)/
  M33(Session Resume)/M34(Workflow)까지 Intelligence Layer는 "지금
  상태가 어떤가"를 관찰·정리하는 계층만 갖췄다. M29 Recommendation
  (`ProjectRecommendationEngine`)이 존재하지만 Project Snapshot/
  Health/Risk만 보고 Session Resume(현재 작업)이나 Workflow
  Intelligence(Blocked/Next)는 전혀 고려하지 않는다 — "그래서 지금
  무엇을 하는 것이 가장 적절한가"에 답하는 단일 창구가 없다.
- 결정:
  1. **새로운 Intelligence를 계산하지 않는다.** M29
     `ProjectIntelligenceService.generate().recommendations`,
     M31 `CapabilityIntelligenceService.generate().gap_report`,
     M33 `session_resume.CurrentWorkSelector`(Analyzer만 재사용,
     M33 Service 전체를 감싸지 않음 — ADR-0047과 같은 이유), M34
     `workflow_flow.WorkflowFlowAnalyzer`(Analyzer만 재사용)를 그대로
     소비한다. 새 지표·점수·Health/Risk 분류를 만들지 않는다.
  2. **5단계 Priority Rule 1개만 추가한다** — 순서대로 첫 번째로
     해당하는 조건에서 멈추고 단일 `NextAction`을 반환한다
     (`intelligence/recommendation_rules.py`의
     `RecommendationRuleAnalyzer`):
     1) Current Work가 있으면 그 Task를 계속 수행하라고 추천
     2) 아니면 Workflow Intelligence의 Next(선행 완료된 `todo`)
        Task가 있으면 그 Task를 시작하라고 추천(Milestone/Task ID
        정렬 순으로 결정적 선택)
     3) 아니면 Workflow Intelligence에 Blocked Task가 있으면 그
        Task의 Block 해소를 추천
     4) 아니면 Capability Gap이 있으면 그 Capability 보완을 추천
     5) 아니면 M29 `ProjectRecommendation` 목록 중 priority
        (high>medium>low, 동률이면 target 사전순)가 가장 높은 것을
        그대로 노출
     다섯 조건이 모두 해당 없으면 `next_action=None`("추천할 다음
     행동 없음")을 반환한다 — Session Resume의 "활성 Task 없음"과
     같은 방어적 처리.
  3. **판정 규칙은 `RecommendationRuleAnalyzer`(순수 함수적
     Analyzer)에 전부 캡슐화하고, `RecommendationIntelligenceService`
     (`intelligence/recommendation_service.py`)는 `VaultAdapter.
     list_tasks()` 1회 조회 + `ProjectIntelligenceService`/
     `CapabilityIntelligenceService`(주입) 실행 + `CurrentWorkSelector`/
     `WorkflowFlowAnalyzer`(같은 tasks 목록 재사용) 실행 + Analyzer
     호출을 조합·오케스트레이션만 한다.** M29
     Analyzer/Service 분리, M34 Analyzer/Service 분리와 동일한
     패턴이며, Automation(M36 이후)이 `RecommendationRuleAnalyzer`를
     그대로 재사용할 수 있게 한다.
  4. **새 Adapter/Interface를 만들지 않는다.** `VaultAdapter`에
     `publish_recommendation_intelligence()` 메서드 1개만 추가한다
     (M29~M34와 동일 패턴).
  5. **결과는 같은 Vault 폴더에 새 파일로 노출한다** —
     `vault/recommendation_intelligence.py`(신규, 원자적 전체 교체)가
     `15 Project Intelligence/Recommendation Intelligence.md`에 쓴다.
  6. **자동 실행하지 않는다.** Recommendation은 추천 문서를 만들
     뿐이며, Task 상태 전이·Workflow 수정·Task 생성을 수행하지
     않는다 — Automation은 M36 이후 범위다. CLI 노출·자동 트리거도
     범위 밖(M29~M34와 동일한 이유, YAGNI).
- 대안:
  - Workflow Intelligence의 "Next Task"를 고를 때 Milestone 우선순위
    (Priority 필드)나 Owner까지 반영하는 복합 규칙을 만든다 — 기각.
    M31/M34가 이미 "owner는 고정 명명 규칙이 없어 신호로 쓰지 않는다"
    /"priority까지 섞으면 예측 가능한 규칙이 깨진다"고 결정했고,
    Milestone/Task ID 정렬만으로 결정적 선택이 이미 가능하다(KISS).
  - `NextAction`을 하나가 아니라 5단계 전부를 항상 리스트로 반환한다
    — 기각. "그래서 지금 무엇을 하는 것이 가장 적절한가"라는 단일
    질문에 답하는 Decision Layer라는 성격에 맞지 않는다(사용자
    Scope: "Next Action을 결정"). 근거가 되는 하위 리포트(Current
    Work/Workflow/Capability Gap/Project Recommendation 전체)는
    Report 안에 그대로 포함해 투명성은 유지한다.
  - `SessionResumeService`(M33) 전체를 주입받아 그 결과만 쓴다 —
    기각. M33은 Context Intelligence(M30)까지 조합하는데, M35는
    Context를 전혀 쓰지 않는 5단계 Rule이라 불필요한 의존성이
    생긴다 — ADR-0047이 M32 Service 대신 Analyzer만 재사용한 것과
    같은 이유로, M33에서도 `CurrentWorkSelector`(Analyzer)만
    가져온다.
- 이유: 새 Interface/Adapter/판단 기준(Health/Risk/Coverage류) 없이,
  이미 계산된 4개 Intelligence 출력을 순서대로 확인하는 Rule 1개만
  더해도 "지금 무엇을 하는 것이 가장 적절한가"에 답할 수 있음을
  확인했다 — M29~M34가 지켜온 "새로운 지식을 만들지 않는다" 원칙을
  그대로 유지하면서, Execution Layer 이전의 마지막 Decision Layer를
  완성한다(Automation은 M36 이후).
- 결과/영향: `intelligence/recommendation_rules.py`(신규)/
  `intelligence/recommendation_service.py`(신규)/`vault/
  recommendation_intelligence.py`(신규)/`integration/vault_adapter.py`
  (`publish_recommendation_intelligence()` 추가) 구현 완료
  (M35-T02~T04, 신규 테스트 12개 포함 pytest 988개, ruff, mypy 전부
  통과). `docs/ARCHITECTURE.md` §3.28(신규) 갱신, `.ai/TASKS.md`에
  Milestone 35 절 신규 추가. 새 Core Domain Interface 없음(27종
  그대로), 새 Integration Layer Adapter 없음(`VaultAdapter` 확장
  1건), `domain/` 필드 추가 없음.

## ADR-0050: Execution 도입 — next_task Recommendation만, 수동 트리거로만, 새 실행 경로 없이 기존 ExecutionDispatcher/EngineRegistry/EngineSelectionPolicy 재사용 (Milestone 36-T01~T04)

- 상태: 승인됨 (2026-07-30, 사용자가 M36 Milestone 계획을 조건부
  승인 — ① DoD의 "거부"를 "지원하지 않음(Not Supported)"으로 표현
  변경 ② `ExecutionGate`(source/manual_trigger/next_task 확인)와
  `ActionBuilder`(NextAction→Action 변환)의 책임을 분리해 설계에
  명시 — 두 가지 수정 권고를 반영하는 조건으로 확정. "Execution은
  이미 존재한다. 우리는 연결만 한다"는 관점을 명시적으로 승인)
- 날짜: 2026-07-30
- 배경: M35 `RecommendationIntelligenceService`는 `NextAction`(추천만,
  실행 없음)을 만든다. 반면 이 저장소의 "실행" 인프라는 이미 완성돼
  있다 — `ExecutionDispatcher`(M18, `runtime/execution/
  execution_dispatcher.py`, 유일한 실행 진입점)와
  `AutomationActionExecutor`(M21,
  `runtime/automation/automation_action_executor.py`)가
  `Action(kind=RUN_TASK, project_id, task_title)` → 새 `Task` 생성 →
  `EngineRegistry.list_candidates()` → `EngineSelectionPolicy.
  select()` → `ExecutionDispatcher.dispatch()`로 실제 AI Engine이
  Task를 수행하는 파이프라인을 이미 갖추고 있다. M36은 M29~M35와
  달리 **Read Only가 아니라 실제 부작용(AI Engine 실행)을 일으키는
  첫 Milestone**이다.
- 결정:
  1. **`NextAction`의 5가지 source 중 `next_task`만 실행 대상으로
     삼는다.** `current_work`(이미 진행 중 — 새로 실행할 것이 없음),
     `blocked_task`/`capability_gap`(사람의 판단이 필요한 문제
     해결형 추천), `project_recommendation`(재할당/우선순위 조정 등
     실행 대상이 모호)은 이번 범위에서 **지원하지 않음(Not
     Supported)**으로 명시적으로 표현한다 — 오류가 아니라 "이번
     Milestone의 Scope 밖"이라는 뜻이다(`AutomationActionExecutor`가
     `RUN_WORKFLOW`를 `AutomationActionNotSupportedError`로 이미
     표현해 온 것과 같은 관례).
  2. **자동/주기적 트리거를 만들지 않는다.** `AutomationScheduler`
     (M21)에 연결하지 않고, 명시적 수동 호출(`manual_trigger=True`를
     호출자가 직접 전달)로만 실행한다 — 사람 개입 없는 완전 자동화는
     다음 Milestone 이후로 미룬다(YAGNI, 위험 최소화).
  3. **책임을 `ExecutionGate`와 `ActionBuilder`로 분리한다**(사용자
     권고): `runtime/execution/recommendation_execution_gate.py`의
     `ExecutionGate.check(next_action, *, manual_trigger)`는 source/
     manual_trigger/next_task 여부만 확인해 `GateDecision(approved,
     reason)`을 반환한다 — 실행 여부 "판정"만 한다. `runtime/
     execution/recommendation_action_builder.py`의
     `ActionBuilder.build(next_action, workflow_report)`는 승인된
     `NextAction`을 `domain.automation.Action(kind=RUN_TASK, ...)`로
     "변환"만 한다. 두 책임을 분리해 두면 다음 Milestone에서
     `blocked_task`용 새 Gate Rule을 추가하기 쉬워진다(사용자 근거
     그대로 채택).
  4. **`AutomationActionExecutor`를 감싸지 않고, 그 내부와 동일한
     3단계(`EngineRegistry.list_candidates()` →
     `EngineSelectionPolicy.select()` → `ExecutionDispatcher.
     dispatch()`)를 `RecommendationExecutionService`
     (`runtime/execution/recommendation_execution_service.py`)가
     직접 재사용한다.** `AutomationActionExecutor.__call__()`은
     `EngineExecutionResult`를 버리는 fire-and-forget 계약
     (`Callable[[AutomationRule], None]`, `AutomationScheduler`가
     의존하는 기존 계약)이라, "실행 결과(성공/실패)를 Vault에
     노출"해야 하는 M36 요구를 만족하지 못한다. 그 계약을 바꾸면
     M21 `AutomationScheduler`와의 기존 계약을 깨뜨리므로 손대지
     않는다 — 새 실행 경로를 만드는 대신, `AutomationActionExecutor`
     가 이미 쓰는 것과 완전히 같은 3개 기존 컴포넌트를 그대로
     재사용해 반환값만 다르게 소비한다(새 Interface/Engine/Dispatcher
     없음).
  5. **Task 상태 자동 전이는 이번 범위에서 하지 않는다.** 실행 성공
     시 Vault Task를 자동으로 `done`으로 전이하는 것은 별도 판단
     기준이 필요해(실패 시 롤백 여부 등) Scope를 키운다 —
     `VaultAdapter.transition_task()`(기존)로 이미 가능한 능력이므로
     필요성이 확인되면 다음 Milestone에서 추가한다. M36은 실행
     결과를 새 Vault 문서(`15 Project Intelligence/Recommendation
     Execution.md`)에 보고만 한다(M29~M35와 같은 "보고서 작성"
     패턴 — 유일한 차이는 보고 전에 실제 실행이 일어난다는 것뿐).
  6. **새 Adapter/Interface를 만들지 않는다.** `VaultAdapter`에
     `publish_recommendation_execution()` 메서드 1개만 추가한다.
- 대안:
  - `AutomationRule`을 즉석에서 만들어 `AutomationActionExecutor`를
    그대로 호출한다 — 기각. `Trigger`가 이 실행 시나리오에 의미가
    없는데도 채워 넣어야 하고, 반환값(`EngineExecutionResult`)을
    버리는 계약이라 실행 결과를 Vault에 남길 수 없다(결정 4 참고).
  - `AutomationScheduler`에 `event_bus` 기반 자동 트리거로 연결한다
    — 기각. 사람 개입 없는 완전 자동화는 이번 Milestone에서 다루기엔
    위험이 크고(어떤 `NextAction`이 실제로 자동 실행돼도 안전한지
    검증되지 않음), 사용자가 명시적으로 "수동 트리거만" 범위로
    승인했다.
  - `NextAction`의 5가지 source 전부를 실행 대상에 포함한다 — 기각.
    `current_work`/`blocked_task`/`capability_gap`/
    `project_recommendation`은 실행 대상(구체적인 "무엇을 실행할
    지")이 불명확하거나 사람의 판단이 전제인 추천이라, 억지로
    실행하려면 각각 새로운 변환 규칙을 만들어야 해 Scope가 크게
    커진다.
  - Task 상태를 실행 성공 시 자동으로 `done` 전이한다 — 기각(결정
    5 참고). 실패 처리 정책(재시도? todo로 유지? 별도 상태?)까지
    함께 설계해야 해 이번 Milestone 범위를 벗어난다.
- 이유: 새 실행 시스템을 만드는 대신 `NextAction → Action →
  dispatch()`라는 얇은 연결부만 추가하고, 실행 가능성이 명확한
  `next_task` 1개 source·수동 트리거 1개 경로로만 좁혀 M36을 "이미
  존재하는 Execution을 연결하는 Milestone"으로 완성했다 — MDD
  원칙(YAGNI/Reuse First)과 첫 side-effecting Milestone이라는 위험
  요인을 함께 반영한 결정이다.
- 결과/영향: `runtime/execution/recommendation_execution_gate.py`
  (신규)/`recommendation_action_builder.py`(신규)/
  `recommendation_execution_service.py`(신규)/`vault/
  recommendation_execution.py`(신규)/`integration/vault_adapter.py`
  (`publish_recommendation_execution()` 추가) 구현 완료
  (M36-T02~T04, 신규 테스트 10개 포함 pytest 998개, ruff, mypy 전부
  통과). `docs/ARCHITECTURE.md` §3.29(신규) 갱신, `.ai/TASKS.md`에
  Milestone 36 절 신규 추가. 새 Core Domain Interface 없음(27종
  그대로), 새 Integration Layer Adapter 없음(`VaultAdapter` 확장
  1건), `AutomationActionExecutor`/`AutomationScheduler`/
  `ExecutionDispatcher` 무변경(그대로 재사용). `tests/
  integration_layer/test_architecture_boundary.py`/`tests/
  intelligence/test_intelligence_layering.py` 회귀 없음(§8 규칙
  18/21 위반 없음을 실제 pytest로 확인).

## ADR-0051: Task Lifecycle 도입 — M36 Execution 결과를 기존 Task 상태 전이 기계(_ALLOWED_TRANSITIONS)에 연결, 새 상태·새 전이 규칙 없음 (Milestone 37-T01~T04)

- 상태: 승인됨 (2026-07-30, 사용자가 M37 Milestone 계획을 조건부
  승인 — ① `TaskLifecycleTransitioner`가 현재 상태를 확인하고 유효한
  전이만 결정할 것 ② Presentation을 "Execution 결과"와 "Task Status
  History"로 역할을 명확히 분리할 것 — 두 가지 수정 권고를 반영하는
  조건으로 확정)
- 날짜: 2026-07-30
- 배경: M36 ADR-0050 결정 5가 "Task 상태 자동 전이는 필요성이
  확인되면 다음 Milestone에서 추가한다"고 명시적으로 미뤘다.
  `vault/task_lifecycle.py`의 `_ALLOWED_TRANSITIONS`(M28)는 이미
  완성된 상태 전이 기계다 — `todo→in-progress`, `in-progress→
  {review, todo}`, `review→done`, `done→archived`만 허용하고,
  `VaultAdapter.transition_task()`가 검증·Daily Note/Milestones
  Index 동기화까지 전부 처리한다. M37은 이 기존 기계에 M36 실행
  결과를 연결하는 얇은 Rule 하나만 추가한다.
- 결정:
  1. **새 상태·새 전이 규칙을 만들지 않는다.** 기존
     `_ALLOWED_TRANSITIONS`의 전이만 사용한다: 실행 시작 시
     `todo→in-progress`, 실행 성공 시 `in-progress→review`(사람
     검토 대기 — `review→done`은 자동화하지 않는다, 이 프로젝트의
     실제 작업 흐름도 항상 사람이 Review를 거쳐 Done을 확정해 왔다),
     실행 실패 시 `in-progress→todo`(되돌려 재시도 가능하게 함).
  2. **`TaskLifecycleTransitioner`(신규,
     `runtime/execution/recommendation_task_lifecycle.py`)는 현재
     상태를 확인하고 유효한 전이만 결정한다**(사용자 권고). 순수
     함수 2개로 나눈다 — `decide_start(current_status)`(현재
     `todo`일 때만 `in-progress` 반환, 아니면 `None`)와
     `decide_completion(current_status, *, success)`(현재
     `in-progress`일 때만 `success` 여부로 `review`/`todo` 반환,
     아니면 `None`). "현재 상태가 예상과 다르면 전이하지 않는다"는
     방어적 규칙이 핵심이다 — 예를 들어 Gate 승인 시점과 실제 전이
     시점 사이에 Task가 이미 다른 상태로 바뀌어 있어도
     `InvalidTaskTransitionError`를 던지는 대신 조용히 건너뛴다.
  3. **`RecommendationExecutionService.execute()`가 두 전이를
     순서대로 호출한다**: Gate 승인 → `decide_start()` → (전이
     발생 시) `VaultAdapter.transition_task()` → `ExecutionDispatcher.
     dispatch()` → `decide_completion()` → (전이 발생 시)
     `VaultAdapter.transition_task()`. 새 상태 조회 경로를 만들지
     않는다 — 현재 상태는 이미 있는 `report.workflow_report`의
     `TaskFlowEntry.status`(M34)를 그대로 읽는다.
  4. **Presentation을 "Execution 결과"와 "Task Status History"로
     분리한다**(사용자 권고). `render_markdown()` 내부를
     `_render_execution_section()`(M36의 Gate/Action/실행 결과)과
     `_render_lifecycle_section()`(신규, 이번 실행에서 발생한 전이
     이력 — old_status/new_status 나열)로 나눠 각 함수가 서로 다른
     책임만 갖게 한다. 같은 Vault 문서(`Recommendation Execution.md`)
     안에 별도 섹션(`## Task Status 이력`)으로 노출한다 — 새 Vault
     파일을 만들지 않는다(YAGNI, 이미 M36이 이 실행 1건을 다루는
     단일 문서를 갖고 있어 분리할 이유가 없다).
  5. **새 Adapter/Interface를 만들지 않는다.** `VaultAdapter.
     transition_task()`(M28, 기존)를 그대로 재사용한다 — 이번
     Milestone에서 Adapter를 확장하지 않는다.
- 대안:
  - `in-progress→review` 대신 `review→done`까지 자동화한다 — 기각.
    `_ALLOWED_TRANSITIONS`상 허용되지만, 이 프로젝트 전체가 항상
    사람이 Review를 거쳐 Done을 확정해 온 실제 작업 흐름과 어긋난다
    (M29~M36 모든 Milestone Review도 사용자 최종 승인을 거쳤다).
  - 실패 시 재시도 횟수 제한이나 별도 실패 상태를 새로 만든다 —
    기각. 재시도 정책은 그 자체로 별도 설계가 필요해 Scope를 키운다
    — 단순히 `todo`로 되돌려 다음 Recommendation 계산에서 자연히
    다시 Next로 잡히게 하는 것으로 충분하다(YAGNI).
  - `TaskLifecycleTransitioner`가 현재 상태를 스스로 다시 조회한다
    (새 Vault 읽기 경로) — 기각. `report.workflow_report`가 이미
    같은 시점에 계산한 상태를 갖고 있어 재조회는 중복이다.
  - Task Status History를 별도 Vault 문서로 분리한다 — 기각.
    사용자 권고의 "역할을 명확히 분리"는 Presentation 책임(렌더링
    함수) 분리를 요구한 것이지 새 파일을 요구한 것이 아니며, 이번
    실행 1건의 결과를 다루는 문서가 이미 있는데 굳이 나눌 이유가
    없다(YAGNI).
- 이유: 새 상태·새 전이 규칙·새 Adapter 없이, 이미 M28부터 존재한
  검증된 상태 전이 기계에 M36 실행 결과를 연결하는 Rule 2개만
  더해도 "실행이 시작·성공·실패했을 때 Task 상태가 어떻게 바뀌어야
  하는가"에 답할 수 있음을 확인했다 — M29~M36이 지켜온 "새로운
  메커니즘을 만들지 않는다" 원칙을 그대로 유지했다.
- 결과/영향: `runtime/execution/recommendation_task_lifecycle.py`
  (신규)/`recommendation_execution_service.py`(확장, 전이 연결 +
  `render_markdown()` 분리) 구현 완료(M37-T02~T04, 신규 테스트 7개
  포함 pytest 1005개, ruff, mypy 전부 통과). `docs/ARCHITECTURE.md`
  §3.30(신규) 갱신, `.ai/TASKS.md`에 Milestone 37 절 신규 추가. 새
  Core Domain Interface/Adapter 없음(27종 그대로, `VaultAdapter`
  확장 없음), `vault/task_lifecycle.py`의 `_ALLOWED_TRANSITIONS`
  무변경.

## ADR-0052: AutomationScheduler 연결 — M21~M37 Composition Root 실배선, 새 정책 없음, source=next_task만 그대로 유지 (Milestone 38)

- 상태: 승인됨 (2026-07-30, 사용자가 "AutomationScheduler 연결"을
  M38 범위로 확정하되 자동 실행 대상은 M36과 동일하게
  `source=next_task`만 유지할 것을 권고 — 반영. 구현 완료 후
  DoD 10개 항목 확인을 거쳐 Milestone 38 완료를 최종 승인)
- 날짜: 2026-07-30
- 배경: M37 완료 시 "다음 Milestone(M38) 이후 논의"로 미룬 6개 항목
  (`done→archived` 자동화/재시도 정책/`review→done` 자동화/
  `AutomationScheduler` 연결/CLI/Hook) 중 `AutomationScheduler`
  연결을 M38 범위로 착수했다. 착수 과정에서 `VaultAdapter`/
  `AgentAdapter`가 `tests/`에서만 생성되고 `web/server.py`의
  `build_app()`(Composition Root)이나 CLI 어디에도 실제로 조립된
  적이 없다는 사실을 발견했다 — M29~M37 전체가 단위 테스트로만
  검증된 "워크숍 단계"였다는 뜻이다. 이 사실을 사용자에게 보고하고,
  "AutomationScheduler 연결"을 실질적으로 완성하려면 이 배선
  자체를 M38 범위에 포함해야 한다는 데 사용자 승인을 받았다.
- 결정:
  1. **새 정책을 만들지 않는다.** `ExecutionGate`(M36, ADR-0050)는
     전혀 손대지 않는다 — 여전히 `source=next_task`만 승인하고
     `current_work`/`blocked_task`/`capability_gap`/
     `project_recommendation`은 계속 Not Supported다. M38은 "기존
     정책을 주기적으로 호출"만 하는 Milestone이다(사용자 권고,
     MDD/YAGNI/Reuse First와 가장 잘 맞음).
  2. **`domain.automation.ActionKind`에 `RUN_RECOMMENDATION`
     1개만 추가**(추가 필드 없음). `AutomationActionExecutor`가
     선택적 `recommendation_execution_service:
     RecommendationExecutionService | None = None` 의존성을 받아,
     발동 시 주입돼 있으면 `RecommendationExecutionService.
     publish(manual_trigger=True)`를 호출하고, 없으면 기존
     `RUN_WORKFLOW`와 동일하게 `AutomationActionNotSupportedError`
     를 던진다.
  3. **`manual_trigger=True`를 고정으로 전달한다.** `ExecutionGate`
     가 `manual_trigger`에 기본값을 두지 않은 이유(ADR-0050)는
     "사람이 개입하지 않은 자동/주기적 트리거가 실수로 승인되는
     것"을 막기 위함이었다. `AutomationRule`은 사용자가
     `AutomationService`(M21 CRUD 진입점)로 명시적으로 만들고
     활성화한 것이므로, Rule 생성/활성화 자체가 이미 사람의 승인
     행위다 — `ExecutionGate` 판정 로직 자체는 바꾸지 않는다.
  4. **`web/server.py`의 `build_app()`에서 Composition Root
     배선을 최초로 완성한다.** `VaultAdapter(Path(config.
     vault_root))` + `AgentAdapter(InMemoryAgentManager(),
     InMemoryAgentRegistry(), InMemoryAgentScheduler())` +
     `RecommendationIntelligenceService` + `RecommendationExecutionService`
     를 `tests/runtime/execution/test_recommendation_execution_service.py`
     와 동일한 생성자 조합으로 조립해 `AutomationActionExecutor`에
     주입한다. `EngineRegistry`/`EngineSelectionPolicy`/
     `ExecutionDispatcher`는 기존 RUN_TASK 배선과 동일 인스턴스를
     공유한다(중복 생성 없음).
  5. **`ProductionConfig.vault_root: str = "."`(신규 필드) +
     `AI_WORKSPACE_VAULT_ROOT` Env Var.** ADR-0037 "Vault ==
     Repository Root"를 그대로 반영한 기본값이다 — 서버가 저장소
     루트에서 기동된다는 기존 전제를 설정값으로 명시했을 뿐, 새로운
     배포 모델을 만들지 않는다.
- 대안:
  - Composition Root 배선 없이 InMemory Fake로 연결 경로만
    증명한다 — 기각. "AutomationScheduler 연결"이라는 목표 자체가
    실제 운영 가능한 상태를 요구하며, Fake로는 M37 완료 노트가
    지적한 "워크숍 단계" 한계를 해소하지 못한다(사용자 최종 결정).
  - `RUN_RECOMMENDATION`이 발동될 때마다 `source=next_task` 외
    나머지 4개도 실행 가능하도록 `ExecutionGate`를 확장한다 —
    기각. 사용자가 명시적으로 "새 정책을 만드는 Milestone이 아니다"
    라고 범위를 좁혔다 — M36 결정을 그대로 유지한다.
  - Rule 생성 시 `manual_trigger` 여부를 판단하는 새 필드를
    `AutomationRule`에 추가한다 — 기각. Rule 자체의 존재/활성화가
    이미 수동 승인을 의미하므로 새 필드 없이 `AutomationActionExecutor`
    가 호출 시점에 고정값을 넘기는 것으로 충분하다(YAGNI).
- 이유: M21(Automation Engine)과 M35~M37(Recommendation→Execution→
  Task Lifecycle)이 각각 독립적으로 완성됐지만 실제로 이어진 적이
  없었다는 배선 공백을 새 정책 없이, 기존 27종 Interface를 그대로
  유지한 채 메운다 — Composition Root 조립만으로 "조건/일정에 따라
  Task를 자동 실행한다"([[Automation Index]]의 M21 목표 정의)는
  약속을 처음으로 next_task 추천까지 완성한다.
- 결과/영향: `domain/automation.py`(확장 1건)/`runtime/automation/
  automation_action_executor.py`(확장 1건)/`runtime/production/
  config.py`·`config_loader.py`(확장 1건)/`web/server.py`
  (Composition Root 배선) 구현 완료, 신규 테스트 5개 포함 pytest
  1010개, ruff, mypy 전부 통과. `docs/ARCHITECTURE.md` §3.31(신규)
  갱신, `.ai/TASKS.md`에 Milestone 38 절 신규 추가. 새 Core Domain
  Interface/Adapter 없음(27종 그대로), `ExecutionGate`/
  `ActionBuilder`/`TaskLifecycleTransitioner` 무변경. `done→archived`
  자동화·재시도 정책·`review→done` 자동화·CLI·Hook은 계속 범위 밖
  (YAGNI, 다음 Milestone 이후 논의).

## ADR-0053: Execution Memory 도입 — Execution 결과를 기존 MemoryEngine에 저장만, 조회 API 제공, Learning 없음 (Milestone 39)

- 상태: 승인됨 (2026-07-30, 사용자가 "M39 Memory Engine 구현 진행"
  요청. 초안 제안서를 검토한 사용자가 조건부 승인 — Scope를
  "저장(store)"과 "조회(query)"로만 한정하고 `RecommendationRuleAnalyzer`
  등 소비 측 반영(Rule 변경)은 M40(Learning Engine)으로 명시적으로
  이관할 것, Memory Record 모델에 embedding/score/vector/confidence를
  절대 포함하지 말 것을 조건으로 제시 — 반영. 구현 완료 후 반영)
- 날짜: 2026-07-30
- 배경: `docs/ARCHITECTURE.md` §2.1(2026-07-30, M38 Review 직후
  재구성)이 "M36~M38(Execution Platform)은 생각하고 실행할 수 있을
  뿐, 아직 스스로 기억하고(Memory Engine) 설계를 감시하고
  (Architecture Guardian) 학습하는(Learning Engine) 단계가 아니다"
  라고 명시하며 M39 이후 이 세 Engine을 각각 별도 제안·승인
  대상으로 남겨뒀다. 이 중 Memory Engine을 M39로 착수한다. 기존
  `MemoryEngine`(M1, `remember`/`recall`/`search`)과 `ContextManager`
  (M1, Snapshot 생명주기)는 이미 존재하지만 어느 것도 M36~M38
  Execution 결과를 자동으로 기록하지 않는다 — Agent가 수동으로
  `remember()`를 호출해야만 채워지고, 그런 호출부 자체가 없다.
- 결정:
  1. **새 Interface를 만들지 않는다.** 기존 `MemoryEngine`
     (`interfaces/memory_engine.py`, M1)을 그대로 재사용한다 —
     `InMemoryContextManager`가 Snapshot을 JSON으로 직렬화해
     `MemoryEngine.remember()`에 저장하는 것과 동일한 패턴이다.
  2. **`ExecutionMemory`(신규, `domain/execution_memory.py`)** —
     `task_id`/`action`/`result`("success"|"failure")/`timestamp`/
     `reason`(선택) 5개 필드만 가진 순수 dataclass. **embedding/
     score/vector/confidence는 의도적으로 포함하지 않는다** — 과거
     기록으로 판단·추천을 바꾸는 것(Learning)은 M40 이후의 책임이다.
  3. **`ExecutionMemoryStore`(신규, `memory/execution_memory_store.py`)**
     — `MemoryEngine` 하나를 감싸는 얇은 서비스. `record()`는
     `ExecutionMemory`를 JSON 직렬화해 `remember(uuid, json)`으로
     저장하고, `query(task_id=None)`는 `search("")`(빈 문자열은
     모든 값의 substring이라는 성질 이용)로 전체 key를 얻은 뒤
     역직렬화해 반환한다 — `MemoryEngine` interface에 새 메서드를
     추가하지 않는다.
  4. **`RecommendationExecutionService`(M36)에 `execution_memory_store:
     ExecutionMemoryStore | None = None` 선택적 의존성을 추가한다**
     (M38의 `recommendation_execution_service` 선택적 주입과 동일한
     패턴). `execute()`가 `ExecutionDispatcher.dispatch()` 결과를
     얻은 직후, 주입돼 있으면 자동으로 `ExecutionMemory`를
     기록한다 — 미주입 시(기본값) 기록을 건너뛰어 M38 이전과 완전히
     동일하게 동작한다. **Agent 수동 `remember()` 호출을 기다리지
     않고 Execution Platform이 스스로 기록한다**는 점이 M1 이후
     처음이다.
  5. **영속화(Vault 파일 등)는 이번 범위에 포함하지 않는다.**
     `web/server.py`의 `build_app()`은 매 프로세스 기동마다 새로
     만들어지는 `InMemoryMemoryEngine()`을 사용한다 — 재시작하면
     기록이 사라진다. `interfaces/memory_engine.py`가 `vault/`나
     `domain/`을 모르는 순수 Core Domain 계약이라, Vault에 영속화
     하려면 `vault/`(Core Domain을 알지 못하는 계층, `docs/
     ARCHITECTURE.md` §7 "vault/는 Core Domain을 알지 못한다")를
     알아야 하는 구현체가 필요한데, 이는 `MemoryEngine`이라는
     Milestone 1부터 있던 기초 Core Engine 계약의 구현체가 M28+에
     생긴 Vault Integration Layer에 의존하게 만드는 방향의
     결합이라 이번 Milestone에서는 시도하지 않는다(YAGNI + 레이어
     결합 최소화). 영속화가 실제로 필요해지면(예: M40 Learning
     Engine이 재시작 후에도 과거 기록을 참고해야 하는 경우) 별도
     제안·승인 대상이다.
  6. **`RecommendationRuleAnalyzer`(M35)는 이번 범위에서 손대지
     않는다.** `ExecutionMemoryStore.query()`를 향후 참고할 수 있는
     기반만 제공할 뿐, 실제로 Rule/추천 판단을 바꾸는 소비 로직은
     M40(Learning Engine, 별도 승인 대상)의 책임이다(사용자 조건).
  7. **`web/app.py`의 `create_app()`에 `execution_memory_store`를
     선택적으로 받아 `app.state.execution_memory_store`로 노출한다.**
     새 REST 엔드포인트는 추가하지 않는다 — "조회 API"는
     `ExecutionMemoryStore.query()` 메서드 자체이며, 이번
     Milestone에서는 HTTP로 노출하지 않는다(YAGNI).
- 대안:
  - **새 `ExecutionHistory` Interface를 신설한다** — 기각. 기존
    `MemoryEngine`(key-value+substring search)으로 표현 가능한
    범위라 27개 Core Domain Interface를 불필요하게 늘린다(MDD
    Interface Review).
  - **`VaultMemoryEngine`을 만들어 Vault 파일에 영속화한다** —
    기각(이번 범위에서는). 최초 제안서에는 포함했으나, 구현 검토
    과정에서 `vault/`를 아는 `MemoryEngine` 구현체가 M1 기초 계약과
    M28+ Vault Layer 사이에 새로운 하향 의존을 만든다는 점을
    발견해 제외했다. 대신 사용자가 조건으로 건 "저장/조회만" 범위와
    맞춰 In-Memory로 좁혔다.
  - **EventBus 구독으로 자동 기록한다**(M20 `InMemoryDashboardRepository`
    패턴 재사용) — 기각. `ENGINE_EXECUTION_COMPLETED` Event
    payload(`runtime/execution/events.py`)에 `task_id`가 없어
    `ExecutionMemory`를 만들 수 없다(payload 필드 추가가 별도로
    필요). `RecommendationExecutionService.execute()` 내부에는 이미
    `target_task_id`/`action`/`result`가 모두 있어 그 자리에서 직접
    기록하는 편이 새 Event 필드 확장 없이 더 최소한의 변경이다.
  - **`RecommendationRuleAnalyzer`가 이번에 바로 Memory를 참고하게
    한다** — 기각(사용자 조건). Memory Engine과 Learning Engine의
    책임을 계층으로 분리하는 것이 장기적 확장성에 더 유리하다는
    사용자 판단(Execution → Memory 저장이 M39, Memory → Learning →
    Recommendation 개선이 M40).
- 이유: M36~M38(Execution Platform)이 실제 부작용을 일으키기
  시작했음에도 그 결과를 아무도 기억하지 않는다는 공백을, 새
  Interface·새 정책 없이 기존 `MemoryEngine` 계약 재사용만으로
  메운다. "저장"과 "활용(Learning)"을 명확히 분리해 M39는 순수하게
  기억하는 역할만 수행하고, 추천/판단을 바꾸는 책임은 M40 이후로
  넘긴다 — Memory Engine → Architecture Guardian → Learning Engine
  순서로 발전하는 전체 흐름(`docs/ARCHITECTURE.md` §2.1)과 일관된다.
- 결과/영향: `domain/execution_memory.py`(신규)/`memory/
  execution_memory_store.py`(신규)/`runtime/execution/
  recommendation_execution_service.py`(확장)/`web/server.py`·
  `web/app.py`(Composition Root 배선) 구현 완료, 신규 테스트 11개
  포함 pytest 1021개, ruff, mypy(194 source files) 전부 통과.
  `docs/ARCHITECTURE.md` §3.8/§8(신규 규칙)/§2.1 갱신,
  `.ai/TASKS.md`에 Milestone 39 절 신규 추가. 새 Core Domain
  Interface/Adapter 없음(27종 그대로). `ExecutionGate`/
  `ActionBuilder`/`TaskLifecycleTransitioner`/`MemoryEngine`
  interface 무변경. 영속화·Learning(Rule 반영)·REST 엔드포인트는
  계속 범위 밖(YAGNI, M40 이후 논의).

## ADR-0054: Domain Vocabulary & Naming Convention 확립 — Milestone 이름은 "{Domain} {Responsibility}", 신규 용어보다 재사용 우선 (Pre-M40)

- 상태: 승인됨 (2026-07-30, 사용자가 M40 착수 전 "프로젝트 전체 명명
  규칙과 Obsidian Graph 규칙을 먼저 확립하라"고 명시적으로 요청.
  문서화 전용 작업으로 범위를 한정(코드/클래스/파일명/기존 Milestone
  이름 변경 없음), 5개 목표(Domain Vocabulary/Milestone Naming
  Convention/Obsidian Graph Convention/Linking Rules/Future Rule)를
  전부 반영해 승인)
- 날짜: 2026-07-30
- 배경: M1~M39를 거치며 Intelligence(M29~M35)/Memory(M1, M39)/Engine
  (M1)/Guardian(§2.1 예약)/Resume(M33)/Lifecycle(M37) 등의 용어가
  각 시점의 필요에 따라 독립적으로 도입되어 어휘가 발산하기
  시작했다. M39 완료 직후 사용자가 "M40(Experience Intelligence)"라는
  새 이름을 제시하면서, 기존에 §2.1이 예고했던 "Learning Engine"과
  이 이름의 관계가 불명확해진 것이 계기가 됐다 — Milestone을
  더 만들기 전에 이름을 짓는 규칙 자체를 먼저 세워야 한다는 판단.
- 결정:
  1. **`docs/ARCHITECTURE.md` 신규 §13(Domain Vocabulary & Naming
     Convention)** — Intelligence/Memory/Execution/Guardian 4개를
     1급 Domain 어휘로 정의(정의/책임/범위/대표 산출물/대표 소비자
     5개 항목씩). Engine/Lifecycle/Resume/Scheduler/Recommendation/
     Automation 6개를 이미 확립된 보조 용어로 별도 표에 정리.
  2. **Milestone Naming Convention**: Milestone 이름은 `{Domain}
     {Responsibility}` 형식을 따른다(`{Domain}`은 §13.2/§13.3의
     기존 어휘). `Knowledge`(이미 M16에 확립)/`Insight`/`Learning`/
     `Analyzer`/`Manager`처럼 기존 어휘와 겹치거나 구현 세부사항에
     불과한 단어는 Milestone/Domain 이름으로 쓰지 않는다.
  3. **신규 용어 도입 절차**: 기존 어휘 중 어느 것도 핵심 책임을
     정확히 표현할 수 없을 때만 새 Domain 용어를 만들며, 이 경우도
     §1.4 Approval Required 대상이다. 승인된 새 용어는 즉시 §13.2에
     추가해 재사용 가능하게 한다.
  4. **`docs/ARCHITECTURE.md` 신규 §14(Obsidian Graph Convention)** —
     Graph Cluster를 폴더가 아니라 §13 Domain 기준으로 정의(🔵
     Intelligence/🟢 Execution/🟡 Memory/🟣 Architecture/🔴 Domain/🟠
     Documentation). 현재 Vault 문서를 Cluster에 매핑한 참고 표와
     Linking Rules(의미 있는 관계만 링크/불필요한 Cross-Cluster 링크
     회피/계층적 링크 우선/완전 연결 그래프 방지)를 포함.
  5. **`.ai/RULES.md` 신규 §1.5(Vocabulary Reuse First)** — 새
     Milestone/Engine/Service/아키텍처 개념 도입 전 §13 어휘 재사용
     여부를 먼저 확인하도록 영구 규칙으로 명문화.
  6. **이번 작업의 범위는 문서화로 한정한다.** 기존 Milestone 이름/
     클래스명/파일명은 변경하지 않는다. Vault 문서에 Domain Cluster
     Tag(예: `#cluster/intelligence`)를 일괄 추가하는 작업과
     `.obsidian/graph.json`의 실제 Group/Color 설정은 별도 후속
     작업으로 남긴다(§14.5) — 수십 개 문서의 Frontmatter를 한 번에
     바꾸는 것은 리팩토링에 해당해 별도 제안·승인이 필요하다.
- 대안:
  - **용어집을 만들지 않고 각 Milestone에서 그때그때 판단한다** —
    기각. M39 이후 "Memory Engine"(M39, 이후 "Execution Memory"로
    개칭)과 "Learning Engine"(§2.1 예약)/"Experience Intelligence"
    (사용자가 M40 착수 시 제시한 이름) 사이의 관계가 이미 한 번
    혼란을 일으켰다 — 사전 정의된 어휘 없이는 이런 혼란이 Milestone
    마다 반복된다.
  - **Obsidian Graph를 폴더 기준으로 유지한다** — 기각(사용자 요청).
    같은 폴더(`15 Project Intelligence/`)에 Intelligence(Read Only)와
    Execution(부작용 발생) 문서가 섞여 있어, 폴더 기준 Graph는
    아키텍처 경계를 시각적으로 드러내지 못한다.
  - **지금 바로 모든 Vault 문서에 Cluster Tag를 추가하고
    `.obsidian/graph.json`을 설정한다** — 기각(이번 범위에서는).
    사용자가 "문서화 전용, 기존 이름/클래스 변경 없음"으로 범위를
    명시했고, 수십 개 문서 Frontmatter 일괄 변경은 별도 승인이
    필요한 작업이라 §14.5에 "적용 계획"으로만 남겼다.
- 이유: Milestone이 거듭될수록 이름이 발산하는 것을 막고, 이름만
  보고도 그 컴포넌트의 아키텍처적 책임(Read Only/저장/실행/감시)을
  알 수 있게 한다 — MDD Review Gate(§2.1.1)가 "코드"에 대해 하는
  Reuse First 검증을 "이름"에도 동일하게 적용한 것이다.
- 결과/영향: `docs/ARCHITECTURE.md` §13(신규)/§14(신규) 추가,
  `.ai/RULES.md` §1.5(신규) 추가(v0.9.0). 코드 변경 없음 — `pytest`/
  `ruff`/`mypy`는 기존 상태(1021 passed) 그대로 유지. 다음
  Milestone(M40)의 이름은 이 규칙에 따라 재검토된다.
- **T01 적용 완료(2026-07-30, `.ai/TASKS.md`의 "Pre-M40 T01" 절
  참고)**: §14.5가 후속 작업으로 미룬 `.obsidian/graph.json` 실제
  설정을 적용했다. 새 Frontmatter Tag를 추가하지 않고 이미 존재하는
  Tag/경로 구조만으로 6개 Cluster를 상호 배타적으로 분류(41개 문서
  전수 시뮬레이션 검증) — MDD 우선순위(①기존 메타데이터 ②기존 Tag
  ③기존 폴더 구조)가 ④(신규 Frontmatter 제안) 없이 전부 해결됨을
  실증했다. Memory Cluster는 아직 매칭 문서가 없다(Execution Memory
  가 Vault에 노출되지 않음, ADR-0053).
- **T01-Fix(2026-07-30, `.ai/TASKS.md`의 "Pre-M40 T01-Fix" 절
  참고)**: 사용자가 실제 Obsidian Graph View에서 모든 노드가 회색
  임을 보고 — T01의 Query가 실제로 적용되지 않았다. 가장 유력한
  원인은 Obsidian이 이미 실행 중인 상태에서 `.obsidian/graph.json`
  을 git으로 외부 수정해 재로딩되지 않은 것(6개 Group이 예외 없이
  전부 실패한 증상이 부분적 문법 오류보다 이쪽에 부합)이며, 2차
  위험 요소로 "여러 부정(-)항 + 괄호 OR 그룹" 조합이 공식 문서
  예시에 없어 파싱 보장이 약했다. Tag 기반 매칭을 전부 폐기하고
  부정·괄호 없는 **`path:"..."` 단순 OR 나열만**으로 전면
  재작성했다 — Vault 44개 `.md` 파일 재검증 결과 43개가 상호
  배타적으로 분류(루트 `README.md` 1개만 미분류, 낮은 우선순위).
  headless 세션이라 실제 Obsidian 화면 확인은 이 세션에서 할 수
  없다는 한계를 명시적으로 기록한다 — 사용자의 실제 앱 확인이
  필요하다.
- **T01-Fix 상태: Pending Verification(2026-07-30, 사용자 확정,
  `.ai/TASKS.md`의 "Pre-M40 T01-Fix 상태" 절 참고)**: 두 차례
  수정(PR #26/#28) 후에도 사용자의 실제 환경(iOS Obsidian Mobile
  뿐, Desktop 접근 없음)에서 결론을 낼 수 없음이 확인돼 검증을
  보류한다. `.obsidian/graph.json`/Schema 비호환, iOS Graph 구현
  자체의 제약, Obsidian Mobile 자체 버그(Forum "Bug graveyard") 세
  가능성 중 무엇이 원인인지 현재 증거로는 구분 불가 — 서로 배타적이
  아니고 겹칠 수도 있다. **`.obsidian/graph.json`은 이번에 전혀
  수정하지 않았다**(PR #28 내용 그대로 유지, 사용자 명시 요청).
  Desktop 접근이 가능해지면 실행할 5단계 검증 체크리스트를
  `.ai/TASKS.md`에 기록했다 — 새 근거 없이는 Graph Query/색상을
  바꾸는 PR을 다시 만들지 않는다.
- **T02~T05 M40 명명 분석 완료(2026-07-30, `.ai/TASKS.md`의
  "Pre-M40 T02~T05" 절 참고)**: M40의 Responsibility를 (a)Read-Only
  Experience Reporting과 (b)Experience-Informed Recommendation 두
  범위로 분석한 결과, 둘 다 부작용이 없어 Domain은 §13.2의
  **Intelligence**로 확정된다(§2.1이 예약했던 "Learning Engine"은
  §13.4가 금지한 동의어 `Learning`과 정확히 겹쳐 사용하지 않는다 —
  새 Domain 0개). Responsibility는 `Recommendation Intelligence`
  (산출물을 이름으로 삼은 선례)와 동일한 패턴으로 사용자 원안
  **`Experience`**를 그대로 유지해, 최종 Milestone 이름을
  **`Experience Intelligence`**로 확정했다. 이 결정은 이름만
  확정하며, 실제 Scope((a)/(b) 선택)/DoD/MDD Review는 M40 착수
  시점에 별도로 진행한다.

## ADR-0055: Experience Intelligence 도입 — Execution Memory를 Read Only로 집계, §8 규칙 21을 Role 기반으로 재정의 (Milestone 40)

- 상태: 승인됨 (2026-07-30, 사용자가 제안서 검토 후 Scope (a)Read-Only
  Experience Reporting으로 조건부 승인. 조건: ①Analyzer는 Deterministic
  ②`ExecutionMemory`는 Immutable Input으로 취급, 절대 수정하지 않음
  ③신규 Interface/Adapter 없음 ④§8 규칙 21에 `ExecutionMemoryStore`
  클래스명을 예외로 나열하지 않음 ⑤대신 Rule을 역할(Role) 중심으로
  재정의해 Service의 오케스트레이션은 허용하고 Analyzer의 순수성은
  계속 강제 — 전부 반영)
- 날짜: 2026-07-30
- 배경: ADR-0053(M39)이 "Learning은 M40 이후"로 미뤘고, ADR-0054의
  T02~T05 분석에서 Domain은 **Intelligence**(기존 어휘 재사용), 이름은
  **`Experience Intelligence`**로 확정됐다. 실제 설계 단계에서
  `ExecutionMemoryStore.query()`가 `domain.execution_memory.
  ExecutionMemory`(domain 타입)를 그대로 반환한다는 사실이 드러났다
  — `intelligence/`는 `domain`을 직접 참조할 수 없다는 §8 규칙 21과
  정면으로 충돌한다(MDD Review 단계에서는 발견하지 못하고 구현
  단계에서 실제로 import를 시도하다 `tests/intelligence/
  test_intelligence_layering.py`가 이를 잡아냈다).
- 결정:
  1. **`ExecutionMemoryStore.query()`의 반환 타입을 domain의
     `ExecutionMemory`에서 `memory/`가 스스로 정의하는
     `ExecutionMemoryEntry`(신규, `memory/execution_memory_store.py`)
     로 변경한다.** `integration/vault_adapter.py`가 `domain.Task`를
     그대로 노출하지 않고 `TaskDocumentView`로 감싸는 것과 동일한
     이유·동일한 패턴이다. `record()`는 여전히 domain의
     `ExecutionMemory`를 받는다 — 쓰기 쪽 호출자(`runtime/execution/`)
     는 domain 참조 제약이 없어 바꿀 이유가 없다.
  2. **`intelligence/experience_rules.py`(신규)의 `ExperienceAnalyzer`
     는 `ExecutionMemoryEntry`조차 직접 받지 않고, `intelligence/`가
     스스로 정의하는 `ExperienceRecord`만 입력으로 받는다.** `memory/`
     를 포함해 이 파일 밖 어떤 패키지도 import하지 않는다 —
     `RecommendationRuleAnalyzer`(M35)가 오직 intelligence/-owned
     dataclass만 받는 것과 동일한 최고 수준의 순수성. Deterministic
     (현재 시각·난수·외부 상태 미참조, 같은 입력에 항상 같은 결과)과
     Immutable Input(입력 `ExperienceRecord`는 frozen, 쓰기 메서드
     호출 없음)을 이 설계로 만족한다(사용자 조건 ①②).
  3. **`intelligence/experience_service.py`(신규)의
     `ExperienceIntelligenceService`가 `ExecutionMemoryStore`를 쥐고
     `ExecutionMemoryEntry`→`ExperienceRecord` 변환 + Analyzer 호출 +
     Vault 노출(`publish()`)까지 담당한다.** `RecommendationIntelligenceService`
     (M35)와 동일한 얇은 조합 계층 뼈대.
  4. **§8 규칙 21을 이름 나열이 아니라 Role 기반으로 재정의한다
     (사용자 조건 ④⑤).** `integration/`의 3개 named Adapter는
     패키지 전체에 계속 허용(기존 관례 무변경). `memory/`는 **`*Service`
     로 끝나는 클래스를 정의하는 모듈에만** 새로 허용 — `tests/
     intelligence/test_intelligence_layering.py`에 `_defines_service_class()`
     기반 검사를 추가해 강제한다. `ExecutionMemoryStore`라는 이름은
     규칙 어디에도 나열하지 않는다 — 앞으로 `memory/`에 무엇이
     추가되든 Service 모듈이면 자동으로 허용된다(장기 확장성, 사용자
     근거).
  5. **`VaultAdapter.publish_experience_intelligence()`(신규 메서드
     1개)** — 기존 `publish_recommendation_intelligence()` 등 8개와
     동일한 시그니처 반복. `vault/experience_intelligence.py`(신규)가
     `15 Project Intelligence/Experience Intelligence.md`에 원자적
     덮어쓰기.
  6. **Composition Root(`web/server.py`) 배선은 이번 범위에 포함하지
     않는다.** M29~M34의 다른 순수 Intelligence Service(Context/
     Session Resume/Workflow/Synthesis)도 `RecommendationIntelligenceService`
     가 필요로 하지 않는 한 `build_app()`에 연결된 적이 없다는 기존
     관례를 그대로 따른다 — `ExperienceIntelligenceService`도
     `RecommendationExecutionService`에 아무것도 제공하지 않으므로
     (Scope (a), Recommendation 미반영) 같은 취급을 받는다.
- 대안:
  - **§8 규칙 21에 `ExecutionMemoryStore`를 이름으로 나열한 예외
    추가** — 기각(사용자 조건 ④). 특정 구현체 이름을 아키텍처
    규칙에 박아 넣으면 `memory/`에 새 컴포넌트가 추가될 때마다 규칙을
    다시 고쳐야 한다 — 유지보수성이 떨어진다.
  - **새 `MemoryAdapter`(Integration Layer) 신설** — 기각(MDD Review
    단계 결론 유지). `ExecutionMemoryStore.query()`를 그대로
    전달만 하는 순수 Passthrough라 레이어 추가 가치가 없다(YAGNI).
  - **`ExecutionMemoryEntry` 없이 `ExecutionMemory`를 그대로
    `intelligence/`에 흘려보낸다** — 기각. §8 규칙 21의 domain 금지
    원칙 자체를 훼손하며, `TaskDocumentView` 선례와도 어긋난다.
  - **Analyzer가 `ExecutionMemoryEntry`를 직접 받는다(Service가
    변환하지 않음)** — 기각. `ExecutionMemoryEntry`가 `memory/`
    소속이라 Analyzer 파일이 `memory/`를 import하게 되고, 새로
    추가한 Role 기반 규칙(Analyzer는 `memory/` import 불가)을
    스스로 어기게 된다.
- 이유: `ExecutionMemoryStore`(M39)가 쌓기만 하던 실행 이력을 처음으로
  "판단 가능한 통찰"로 바꾸면서도, Learning(Rule 반영)은 여전히
  손대지 않아 ADR-0053의 "저장과 활용의 분리" 원칙을 지킨다. 동시에
  §8 규칙 21을 이름 목록에서 역할 정의로 바꿔, Memory Domain(§13.2)이
  이미 "저장/검색만, 판단하지 않음"으로 정의돼 있다는 사실(ADR-0054)
  을 그대로 활용해 향후 `memory/` 확장이 아키텍처 규칙 재작성 없이
  자동으로 흡수되게 한다.
- 결과/영향: `memory/execution_memory_store.py`(확장,
  `ExecutionMemoryEntry` 추가)/`intelligence/experience_rules.py`
  (신규)/`intelligence/experience_service.py`(신규)/`vault/
  experience_intelligence.py`(신규)/`integration/vault_adapter.py`
  (확장 1건)/`tests/intelligence/test_intelligence_layering.py`
  (확장, Role 기반 검사 추가) 구현 완료, 신규 테스트 12개 포함
  pytest 1033개, ruff, mypy(197 source files) 전부 통과. `docs/
  ARCHITECTURE.md` §3.32(신규)/§8 규칙 21(재정의) 갱신, `.ai/TASKS.md`
  에 Milestone 40 절 신규 추가. 새 Core Domain Interface/Adapter
  없음(27종 유지). Composition Root 배선·영속화·Learning(Rule 반영)
  은 계속 범위 밖(YAGNI, M41 이후 논의).

## ADR-0056: Architecture Guardian 도입 — 기존 5곳의 중복 ast 경계 검사를 순수 값 객체 Rule Registry로 통합, Vault 발행이 핵심 Output (Milestone 41)

- 상태: 승인됨 (2026-07-30, 사용자가 제안서 검토 후 3단계에 걸쳐
  조건부 승인. ①제안서: Scope (a)통합+Read Only 리포트만, ②MDD
  Review 1차: 역할 정의("canonical registry and evaluation engine")
  확정 + ArchitectureRule을 확장 가능한 Value Object로/ArchitectureCheckResult
  Domain Model 정의/Checker는 pytest를 모르는 순수 평가기로/Vault
  Report를 핵심 Output으로, ③MDD Review 2차: 역할 정의를
  "Guardian owns the executable representation of architectural
  rules..."로 재확정 + ArchitectureRule ABC 제거(메서드 없는
  immutable Rule 타입 집합으로)/GUARDIAN_RULES를 Final·immutable
  tuple로/Connector 그룹 규칙은 무리하게 일반화하지 말고 제외 —
  전부 반영)
- 날짜: 2026-07-30
- 배경: `docs/ARCHITECTURE.md` §13.2가 Guardian을 1급 Domain
  어휘로 이미 예약해뒀지만 Scope/Output은 "착수 시점에 별도 제안"
  으로 비워둔 상태였다(ADR-0054). Reuse First로 저장소를 확인한
  결과, "아키텍처 규칙 위반 감시"는 이미 `tests/` 5곳(`test_
  architecture_boundary.py`/`test_connector_layering.py`/`test_
  conversation_connector_boundary.py`/`test_intelligence_layering.py`)
  에 개별 구현·중복돼 있었다 — 전부 `ast` 기반, 전부 각자
  `_imported_modules()` 헬퍼를 중복 구현. M41은 새 감시 로직을
  만드는 Milestone이 아니라 이미 존재하는 것을 통합하는 Milestone
  이라는 것이 이번 제안의 핵심 발견이다.
- 결정:
  1. **역할 정의를 `docs/ARCHITECTURE.md` §13.2 Guardian 행에 그대로
     반영한다**: "Guardian owns the executable representation of
     architectural rules. Architecture documentation defines the
     rules; Guardian encodes them, evaluates conformance, and
     publishes architectural health." — Guardian은 규칙을 정의하지
     않는다(§8이 여전히 규칙의 소유자), 평가·공표만 한다.
  2. **`guardian/models.py`** — `ArchitectureViolation`(위반 1건)/
     `ArchitectureCheckResult`(규칙 1개의 평가 결과)/
     `ArchitectureHealthReport`(전체 결과 + `all_passed` 프로퍼티,
     이미 계산된 `passed` 값들의 단순 논리곱이라 새 판정 로직이
     아님).
  3. **`guardian/rules.py`** — `ArchitectureRule`은 ABC가 아니라
     `ForbiddenPackageImportRule`/`AllowedImportPrefixRule`/
     `ServiceRoleGatedImportRule` 3개 `frozen dataclass`의 Union
     이다(메서드 없음, 순수 값 객체, 사용자 조건). 평가 로직은 전부
     `checker.py`가 타입별로 분기해 담당 — Rule을 다형적 객체가
     아니라 데이터로 유지해 새 Rule 종류가 필요할 때 이 Union에
     타입 하나만 추가하면 된다(확장 가능성, 사용자 조건). `GUARDIAN_RULES:
     Final[tuple[ArchitectureRule, ...]]`로 선언해 실행 중 변경
     불가능한 Registry로 고정(사용자 조건).
  4. **`guardian/checker.py`** — `evaluate(rules, src_root) ->
     ArchitectureHealthReport`. `pytest`/`assert`를 전혀 쓰지 않는
     순수 평가기다(사용자 조건) — `pytest` 테스트는 이 함수의 결과를
     받아 자기 스스로 `assert`할 뿐이다.
  5. **`guardian/service.py`의 `ArchitectureGuardianService`** —
     `checker.evaluate()` + Vault 발행을 조합. **`publish()`가 핵심
     진입점**(사용자 조건) — Guardian의 목적("공표한다")은 평가만
     으로 완수되지 않는다는 것을 설계로 명시했다. `VaultAdapter.
     publish_architecture_guardian()`(신규 메서드 1개)이 `15
     Project Intelligence/Architecture Guardian.md`에 원자적으로
     덮어쓴다.
  6. **5곳 중 3개 형태에 자연스럽게 맞는 5개 규칙만 이전한다**:
     `test_architecture_boundary.py`의 2개(Core Domain↔vault 개별
     금지, `ForbiddenPackageImportRule`) + `test_intelligence_
     layering.py`의 3개(금지 패키지/`ForbiddenPackageImportRule`,
     Adapter 화이트리스트/`AllowedImportPrefixRule`, Role 기반
     Memory 접근/`ServiceRoleGatedImportRule`, M40/ADR-0055 패턴
     재사용). 두 파일의 나머지 테스트(`test_architecture_boundary.py`
     의 "Integration Layer만 양쪽을 동시에 참조 가능")는 Guardian
     결과를 `assert`하는 얇은 wrapper로 재작성됐다 — 각 테스트가
     잡아내는 위반 내용은 변경 전과 100% 동일(회귀 없음이 최우선
     검증 대상).
  7. **`test_connector_layering.py`/`test_conversation_connector_
     boundary.py`는 이번 범위에서 제외한다**(사용자 조건 3): 이
     둘은 그룹 기반(Adapter/Peer Connector/Orchestrating Connector)
     또는 단일 파일 기준 규칙이라, 위 3개 Rule 형태로 억지로
     일반화하면 Rule 타입 자체가 특수 사례에 맞춰 뒤틀린다. 두
     파일은 기존 `ast` 검사를 그대로 유지 — Guardian을 거치지
     않는다.
- 대안:
  - **`ArchitectureRule`을 `evaluate()` 메서드를 가진 ABC + 구체
    서브클래스로 설계** — 기각(사용자 조건 1). MDD Review 1차에서
    제안했으나, 2차에서 "메서드 없는 immutable Rule 타입 집합"으로
    재조정 — Rule을 순수 데이터로 유지하면 평가 로직이 `checker.py`
    한 곳에만 있어 감사하기 쉽고, Rule 자체는 어떤 부작용도 가질 수
    없다는 보장이 타입 시스템 수준에서 생긴다.
  - **`GUARDIAN_RULES`를 일반 list로 선언** — 기각(사용자 조건 2).
    list는 실행 중 append/remove가 가능해 "정본 Registry"라는
    Guardian의 정의(규칙을 정의하지 않고 평가만 한다)와 어긋난다 —
    `Final` + `tuple`로 구조적으로 불변임을 보장한다.
  - **모든 5곳(Connector 그룹 규칙 포함)을 억지로 통합** — 기각
    (사용자 조건 3). 그룹 기반 화이트리스트를 표현하려면 기존 3개
    Rule 형태에 없는 새 필드·새 의미론이 필요해 Rule 타입이
    비대해진다 — 억지 일반화보다 정직하게 범위를 좁히는 것을
    택했다.
  - **CI 강제 게이트 신설(Scope (b))** — 기각(제안서 단계 결론
    유지, YAGNI). `pytest` 통과가 이미 §8.6 Merge 조건에 포함돼
    있어 "위반하면 병합이 막힌다"는 새로 만들 게 없다.
- 이유: Guardian이라는 이름이 예약만 되어 있던 §13.2의 빈자리를,
  새 코드를 발명하지 않고 이미 검증된 5곳의 로직을 통합해서
  채운다 — MDD Review Gate의 Reuse First 원칙을 "코드 감시 코드"
  자체에도 그대로 적용한 사례다. Rule을 순수 데이터로, Checker를
  pytest 비의존 순수 함수로 분리해 "규칙을 실행 가능한 명세로
  공식화"하는 것과 "그 명세를 pytest로 강제하는 것"을 완전히
  분리했다 — 후자는 이미 §8.6이 하고 있으므로 새로 만들지 않았다.
- 결과/영향: `guardian/models.py`/`rules.py`/`checker.py`/`service.py`
  (전부 신규)/`vault/architecture_guardian.py`(신규)/`integration/
  vault_adapter.py`(확장 1건)/`tests/integration_layer/test_
  architecture_boundary.py`(확장, 2개 테스트 Guardian 경유)/`tests/
  intelligence/test_intelligence_layering.py`(확장, 3개 테스트
  Guardian 경유) 구현 완료, 신규 테스트 18개 포함 pytest 1051개,
  ruff, mypy(203 source files) 전부 통과. `docs/ARCHITECTURE.md`
  §3.33(신규)/§13.2 Guardian 행(내용 확정) 갱신, `.ai/TASKS.md`에
  Milestone 41 절 신규 추가. 새 Core Domain Interface/Adapter
  없음(27종 유지), 새 Layer 1개(`guardian/`, §13.2가 이미 예약해
  둔 자리). Connector 그룹 규칙 편입·CI 강제 게이트는 범위 밖
  (YAGNI, M42 이후 논의).

## ADR-0057: Repository Naming Standard — 실측 조사로 확인된 클래스/파일/디렉터리 명명 관행을 공식 문서로 승격 (Post-M41, 문서화 전용)

- 상태: 승인됨 (2026-07-30, 사용자가 "Repository Naming Consistency
  Review"를 수행하고 그 결과를 일회성 분석으로 끝내지 않고 ADR로
  공식화할 것을 제안 — 승인. **새 규칙을 만드는 것이 아니라 이번
  분석에서 확인된 규칙을 공식화하는 것**이라는 전제 그대로 반영)
- 날짜: 2026-07-30
- 배경: M39(Execution Memory)~M41(Architecture Guardian) 착수 이후,
  실제 저장소(`src/ai_workspace/` 300개 클래스, 160여 개 모듈,
  `tests/` 18개 디렉터리, Vault 11개 문서)를 전수 조사하는 Domain
  Naming Analysis를 수행했다(코드 변경 없는 분석 전용 리뷰). 결과:
  ADR-0054(§13) 확립 **이후** 착수된 M39~M41은 새 어휘 0개로 기존
  체계를 정확히 재사용했지만, 확립 **이전**(M29~M34) 코드에는 잔재
  (`ProjectRecommendationEngine`의 "Engine" 오용 등)가 남아 있었다.
  이 조사 자체가 재사용 가능한 자산이므로 반복 조사 없이 ADR로
  고정한다.
- 결정:
  1. **`docs/ARCHITECTURE.md` 신규 §13.6(Class/File Naming Standard)**
     — 클래스 접미사 12종(`*Analyzer`/`*Service`/`*Store`/
     `*Repository`/`*Adapter`/`*View`/`*Record`/`*Report`/`*Result`/
     `*Rule`/`*Manager`/`*Engine`)의 역할을 실측 근거와 함께 표로
     고정. `*Engine`은 §3.7(Core Engine)/§3.9(구현 엔진 실행 관리)
     두 의미로만 한정 — 그 밖의 용도로 새로 쓰지 않는다.
  2. **파일명↔클래스명 대응 원칙**: `{name}_service.py`는 반드시
     `{Name}Service` 클래스를 정의해야 하고(M40/M41의 `guardian/`
     Role 기반 `ast` 검사가 이미 이를 실제로 강제하고 있음을 재확인),
     `{name}_rules.py`는 순수 Analyzer/Rule만 담는다.
  3. **디렉터리명↔Domain 대응 원칙**: 새 최상위 디렉터리는 §13.2의
     4개 1급 Domain과 먼저 대응을 확인한다(§1.5 절차를 디렉터리명
     에도 적용). `domain/`(Core Domain Model 패키지, ADR-0001)과
     ADR-0054의 "Domain Vocabulary"가 이름만 같고 다른 개념이라는
     동음이의어 관계를 최초로 명시적으로 기록한다.
  4. **`.ai/RULES.md` 신규 §1.6(Repository Naming Standard, v0.10.0)**
     — 위 내용을 영구 규칙으로 참조.
  5. **개선 여지(이번에 실행하지 않음)**로만 기록: `ProjectRecommendationEngine`
     →`ProjectRecommendationAnalyzer`, `intelligence/recommendation.py`
     →`intelligence/project_recommendation.py`, `tests/integration_layer/`
     명칭 유지 + 주석 추가. 전부 사용자 별도 승인 시에만 실행한다.
- 대안:
  - **이번 리뷰를 문서화하지 않고 지식으로만 남긴다** — 기각(사용자
    요청). 세션이 바뀌면 조사 내용이 사라지고 같은 조사를 반복하게
    된다 — ADR로 고정해야 M42 이후 세션도 재사용할 수 있다.
  - **개선 여지(Rename Candidate)를 이번에 바로 실행한다** — 기각
    (범위 밖). 이번 요청은 "규칙 공식화"이지 "코드 정리"가 아니다
    (사용자가 별도 지시할 때까지 대기).
  - **완전히 새로운 명명 규칙을 발명한다** — 기각. §1.5 Vocabulary
    Reuse First의 정신을 명명 규칙 자체에도 적용 — 이미 있는 관행을
    재사용하지 새로 만들지 않는다.
- 이유: M39~M41이 이미 §13(ADR-0054)을 성실히 지켰다는 사실 자체가
  "명명 규칙이 ADR 수준에서 문서화되면 실제로 지켜진다"는 증거다 —
  이번 실측 조사 결과를 같은 방식으로 승격해 M42 이후에도 반복
  가능한 기준선으로 만든다.
- 결과/영향: `docs/ARCHITECTURE.md` §13.6(신규) 추가, `.ai/RULES.md`
  §1.6(신규, v0.10.0) 추가. 코드 변경 없음 — `pytest`/`ruff`/`mypy`는
  기존 상태(1051 passed) 그대로 유지. 4건의 Rename Candidate는
  실행하지 않고 §13.6에 "개선 여지"로만 기록 — 실행은 별도 승인
  대상.
- **Boy Scout Rule 채택(2026-07-30, 사용자 결정, `.ai/RULES.md`
  §1.6/v0.10.1 참고)**: 4건의 Rename Candidate를 한꺼번에 처리하는
  대규모 Rename PR은 만들지 않기로 했다. 대신 기존 코드는 그 파일을
  기능 개발로 수정할 일이 생길 때 같은 PR 안에서 함께 Rename하고
  (Boy Scout Rule), 신규 코드는 §13.6을 예외 없이 100% 적용한다 —
  이렇게 저장소가 대규모 일괄 작업 없이 점진적으로 표준에
  수렴한다.
- **Naming Technical Debt Ledger 채택(2026-07-30, 사용자 결정,
  `.ai/RULES.md` §1.6/v0.10.2 참고)**: §13.6의 Rename Candidate 표를
  Cleanup Sprint 없이 유지되는 **공식 기술 부채 목록**으로 명문화했다.
  새 위반이 발견되면 표에 행을 추가하고, 항목이 해결되면 행을
  지우지 않고 "현재"/"제안" 칸에 취소선(`~~이전 이름~~`)을 긋고
  "상태" 칸에 해결 일자와 처리한 PR/커밋을 남긴다 — 표 자체가
  변경 이력이 되어 대규모 Rename PR 없이도 저장소가 지속적으로
  표준에 수렴했음을 추적할 수 있다.

## ADR-0058: Recommendation Adaptation — 과거 실행 경험으로 Recommendation을 사후 조정(Milestone 42)

- 상태: 승인됨 (2026-07-31, T02 Domain Analysis → T03 MDD Review →
  T04 Milestone Proposal 순서로 진행, 최종 승인 시 아래 5개 조건을
  반영하는 것을 전제로 승인)
- 날짜: 2026-07-31
- 배경: M35(Recommendation Intelligence)~M41(Architecture Guardian)로
  Intelligence→Execution→Memory→Experience→Guardian까지 "관찰(Observe)"
  축이 완성됐다. ADR-0053(M39)이 "Learning/영속화/Rule 반영은 범위
  밖"이라고 명시적으로 미뤄뒀던 지점 — "과거 실행 결과로 판단 기준
  자체를 조정한다"는 책임을 이번에 처음 다룬다. §13.4가 이미
  `Insight`/`Learning`을 Intelligence와 경계가 흐린 동의어로 배제해둔
  상태였으므로, 새 용어 도입 전 Domain Analysis(T02)를 먼저 수행했다.
- 결정:
  1. **Responsibility는 "생성이 아니라 조정(Adjustment)"** — M35
     `RecommendationRuleAnalyzer`의 5단계 Priority Rule이 이미 고른
     단일 `NextAction`을 그대로 받아, 반복 실패한 대상만 보류하고
     그 밖에는 통과시킨다. 새 Recommendation을 만들지 않는다(사용자
     조건 1).
  2. **`RecommendationAdjustmentAnalyzer`(`intelligence/
     recommendation_adjustment.py`, 신규)의 입력을 Raw `NextAction`
     + `ExperienceReport` 두 값으로 단순화**(사용자 조건 2) — 후보
     목록 재순위화 로직 없음. Deterministic + Immutable Input(M40과
     동일 조건).
  3. **`ExperienceReport` 생성은 M40의 책임(Non-goal)**(사용자 조건
     3) — 이 Milestone은 `ExperienceReport`를 소비만 한다.
  4. **§13.3에 `Adaptation`을 Behavioral Concept로 정의**(사용자 조건
     4) — 5번째 1급 Domain(§13.2) 승격은 보류. Workflow/Agent/
     Capability Adaptation 등으로 개념이 반복 재사용되는 시점에
     별도 ADR로 승격을 재검토한다.
  5. **`experience_report=None`이면 M35와 100% 동일 동작을 DoD로
     명시**(사용자 조건 5) — `RecommendationIntelligenceService.
     generate()/publish()`에 `experience_report: ExperienceReport |
     None = None` 선택적 인자 추가, 미주입 시 기존 동작 완전 보존
     (하위 호환).
- 대안:
  - **`Learning`을 그대로 사용한다** — 기각. §13.4가 이미 Intelligence
    와 구분이 흐리다는 이유로 명시적으로 배제해둔 용어(ADR-0053
    Non-goal 근거).
  - **`Adaptation`을 즉시 5번째 1급 Domain으로 승격한다** — 기각
    (사용자 결정, 보류). 재사용 사례가 이번 1건뿐이라 지금 승격하면
    Domain Vocabulary가 성급하게 확장된다 — §1.5 Vocabulary Reuse
    First의 정신과 어긋난다.
  - **`RecommendationRuleAnalyzer`(M35)를 직접 수정해 Adaptation
    로직을 내장한다** — 기각. M35 Analyzer는 이미 `pytest`로 검증된
    5단계 Priority Rule의 유일한 소유자다 — 새 책임을 감싸는(wrap)
    별도 Analyzer로 분리하는 것이 M39→M40의 "기존 Analyzer 불변,
    새 계층이 감싼다" 선례와 일치하고 회귀 위험도 없다.
  - **`web/server.py`/`RecommendationExecutionService`에 즉시
    배선한다** — 기각(Non-goal). Automation 자동 실행 경로 연결은
    범위를 벗어난다 — Vault 리포트 노출 가능한 능력을 갖추는 것까지가
    이번 Milestone의 범위.
- 이유: M39(Execution Memory)가 명시적으로 미뤄뒀던 "판단 기준 조정"
  책임을 Vocabulary Reuse First 원칙을 지키며(Learning 재사용 대신
  Domain Analysis로 새 용어 검증) 최소 변경으로 구현한다 — 기존
  Analyzer/Report/Service를 그대로 재사용하고 신규 Interface/Adapter
  없이 선택적 인자 1개로 하위 호환을 보존했다.
- 결과/영향: `intelligence/recommendation_adjustment.py`(신규,
  `RecommendationAdjustment`/`RecommendationAdjustmentAnalyzer`),
  `intelligence/recommendation_service.py`(experience_report 선택적
  인자, `adjusted`/`adjustment_reason` 필드 추가, Vault "Adaptation"
  섹션), `docs/ARCHITECTURE.md` §13.3(Adaptation 추가)/§13.4(예시
  행 추가)/§3.34(신규). 새 Core Domain Interface/Adapter 없음(27종
  유지). `pytest` 1060개 통과(9개 신규), `ruff`/`mypy` 통과,
  `guardian.checker.evaluate()` all_passed 유지. `web/server.py`
  배선 없음(Non-goal, 향후 별도 승인 시 진행).

## ADR-0059: Recommendation Orchestration — M35~M42 실행 흐름을 명시적으로 연결(Milestone 43)

- 상태: 승인됨 (2026-07-31, T02 Domain Analysis → T03 MDD Review →
  T04 Milestone Proposal 진행 중 사용자가 결합도 관련 재검토를
  요청 — `RecommendationExecutionService`의 Recommendation 의존성
  제거안으로 T04를 갱신한 뒤 최종 승인)
- 날짜: 2026-07-31
- 배경: M42(Recommendation Adaptation)가 `web/server.py`(Composition
  Root)·`RecommendationExecutionService`(M36)·`AutomationScheduler`
  (M38)에 자동 배선하지 않기로 Non-goal로 명시했었다 — Experience
  기반 Adaptation이 실제 운영 경로(AutomationScheduler → RUN_RECOMMENDATION)
  에서는 여전히 미적용 상태였다. M43은 이 배선을 완성해 M35
  (Recommendation)→M42(Adaptation)→M36(Execution)→M39(Memory)→
  M40(Experience)로 이어지는 하나의 실행 흐름을 명시적으로 연결한다.
- 결정:
  1. **T02 Domain Analysis**: 책임("Recommendation부터 Experience
     까지 하나의 작업 실행 흐름을 제어")이 기존 `Workflow`(M34,
     Read-Only Task 상태 분석)에 포함되지 않음을 확인. `Workflow
     Runtime`/`Workflow Coordination` 등은 이미 다른 의미로 쓰이는
     `Workflow`를 접두어로 재사용해 §13.4가 배제한 `Learning`/
     `Insight`와 같은 유형의 충돌을 일으킨다 — 대신 이 저장소에
     이미 확립된 `Orchestrating Connector`(ADR-0041)/`Orchestrating
     패턴`(M32 Synthesis, M40 Experience)과 정확히 같은 의미임을
     확인하고 `Orchestration`을 재사용한다(§13.3에 구조적 관행으로
     최초 등재, 1급 Domain 승격 아님).
  2. **Milestone 이름은 `Recommendation Orchestration`** — M36/M42
     와 동일한 대상 표현 방식(`{대상} {Domain}`)을 따라 지금 실제로
     다루는 범위(Recommendation→Experience 루프)를 정확히 한정한다.
     원 제안 `Workspace Orchestration`은 범위를 필요 이상으로 넓게
     들리게 해 채택하지 않는다.
  3. **네 가지 책임의 명시적 분리(사용자 결정)**: Composition Root
     (`web/server.py`, 조립) / Analyzer(`RecommendationRuleAnalyzer`/
     `RecommendationAdjustmentAnalyzer`, 판단) / `RecommendationOrchestrationService`
     (신규, 실행 흐름 제어) / `RecommendationExecutionService`(실행).
     이 구조가 유지되면 향후 Automation·Multi-Agent가 동일한
     Orchestration Service를 재사용하는 기반이 된다.
  4. **`RecommendationExecutionService`(M36)의 Recommendation 의존성
     제거**: T04 최초 제안은 `experience_report`를 이 Service에
     선택적으로 threading하는 것이었으나(생성자에 `RecommendationIntelligenceService`
     유지), 사용자가 "Orchestration이 Recommendation 단계를 완결한
     뒤 Execution에는 순수한 실행 대상만 전달하는 방향이 더 낮은
     결합도"라고 재검토를 요청 — 검토 결과 채택. `execute()`/
     `publish()`가 이미 계산된 `RecommendationIntelligenceReport`를
     파라미터로 받고, 생성자에서 `RecommendationIntelligenceService`
     의존성 자체를 제거했다. 실제로는 원안보다 이 Service에 가하는
     변경이 더 작다(파라미터 추가+threading 대신 생성자 의존성
     제거+내부 `generate()` 호출을 파라미터로 교체).
  5. **`RecommendationOrchestrationService`(신규,
     `runtime/execution/recommendation_orchestration_service.py`)**:
     `ExperienceIntelligenceService.generate()`(M40) → `RecommendationIntelligenceService.
     generate(experience_report=...)`(M35/M42) → `RecommendationExecutionService.
     execute()/publish()`를 순서대로 호출만 하는 순수 흐름 제어
     계층. 판단 로직 0줄.
  6. **`AutomationActionExecutor`/`web/server.py` 배선 교체**:
     `AutomationActionExecutor`가 주입받는 의존성을
     `RecommendationExecutionService`에서 `RecommendationOrchestrationService`
     로 교체(파라미터명 `recommendation_orchestration_service`로
     함께 갱신) — `web/server.py`가 `ExperienceIntelligenceService`
     +`RecommendationOrchestrationService`를 조립해 주입한다. M42의
     Non-goal(자동 배선 없음)을 이 Milestone에서 완성한다.
- 대안:
  - **`experience_report`를 `RecommendationExecutionService`에
    선택적으로 threading한다(T04 원안)** — 기각(사용자 재검토
    요청 반영). Execution Service가 여전히 "Recommendation을 어떻게
    얻는지" 알아야 해 결합도가 남는다.
  - **Milestone 이름을 `Workspace Orchestration`(원 제안) 그대로
    확정한다** — 기각. 지금 실제로 다루는 범위(Recommendation→
    Experience 루프)보다 넓게 들려 향후 다른 흐름과 혼동될 위험이
    있다.
  - **`Workflow Runtime`/`Workflow Coordination`을 새로 만든다** —
    기각. `Workflow`가 이미 M34에서 다른 의미(Read-Only Task 상태
    분석)로 확립돼 있어 재사용 시 §13.4가 경계했던 것과 같은 유형의
    혼동을 일으킨다.
  - **`Orchestration`을 즉시 §13.2 1급 Domain으로 승격한다** —
    기각(`Adaptation`과 동일한 논리). 아직 이 저장소 안에서 다루는
    범위가 Recommendation 흐름 하나뿐이며, ADR-0041 Orchestrating
    Connector와의 관계를 §13.3 수준에서 먼저 명확히 하는 것이 더
    안전하다.
- 이유: M42가 명시적으로 남겨둔 Non-goal(자동 배선)을 완성하면서,
  동시에 "Orchestration"이라는 이미 확립된(그러나 §13에는 미등재였던)
  관행을 공식화했다. 사용자의 재검토 요청 덕분에 `RecommendationExecutionService`
  의 결합도를 낮추는 더 나은 설계로 T04를 갱신할 수 있었다 — Execution
  Service가 이제 Recommendation 계산 방식과 완전히 독립적이라 향후
  다른 Recommendation 생성 경로(예: 다른 Analyzer 조합)에도 재사용
  가능하다.
- 결과/영향: `runtime/execution/recommendation_orchestration_service.py`
  (신규), `runtime/execution/recommendation_execution_service.py`
  (Recommendation 의존성 제거, `report` 파라미터 추가),
  `runtime/automation/automation_action_executor.py`(배선 교체),
  `web/server.py`(Composition Root 갱신), `docs/ARCHITECTURE.md`
  §13.3(Orchestration 추가)/§13.4(예시 행 추가)/§3.35(신규). 새 Core
  Domain Interface/Adapter 없음(27종 유지). `pytest` 1063개 통과
  (3개 신규 + 기존 테스트 파라미터 갱신), `ruff`/`mypy` 통과,
  `guardian.checker.evaluate()` all_passed 유지. `build_app()` 실제
  조립 스모크 테스트 통과.

## ADR-0060: Recommendation Vocabulary Decision — Domain Vocabulary 재검토 후 "Recommendation" 유지 확정 (문서화 전용)

- 상태: 승인됨 (2026-07-31, 사용자가 M43 완료 후 "Recommendation"이라는
  용어 자체가 이 책임에 가장 적합한지 재검토를 제안 — T02 Domain
  Vocabulary Analysis로 4개 대안과 비교한 뒤 유지로 결론, 사용자가
  ADR 제목을 "Recommendation Vocabulary Retained"에서
  "Recommendation Vocabulary Decision"으로 일반화할 것과 Context/
  Considered Alternatives/Decision/Consequences 4개 절 구성을
  권고해 반영)
- 날짜: 2026-07-31

### Context

M43(Recommendation Orchestration) 완료 이후 Recommendation의
책임과 경계가 M35~M43 전 구간에서 충분히 명확해졌다 — 이 시점에
"Recommendation"이라는 용어 자체가 이 책임에 가장 적합한지, 아니면
"제안(Suggest)"에 더 가까운 것은 아닌지 재검토할 좋은 시점이라는
사용자 제안에 따라 Domain Vocabulary Migration 절차(단순 Rename이
아니라 T02 분석 → 비교 → ADR 결정 → 결정 시에만 전체 리네이밍)로
다룬다.

### Considered Alternatives

`src/ai_workspace/` 전수 검색으로 각 후보의 기존 충돌 여부를 먼저
확인했다.

| 후보 | 기존 충돌 | 책임과의 적합도 | 판정 |
|---|---|---|---|
| **Recommendation**(현재) | 없음 — M35(2026-07-30) 도입 이후 이 개념 전용으로만 일관되게 쓰임 | "이유(`reason`) 있는 비구속적 조언"이라는 뜻이 `ExecutionGate`(M36)가 별도로 승인해야 실행된다는 구조와 정확히 일치 | 유지 |
| **Suggest/Suggestion** | 코드 내 사용 0건 | Recommendation과 사실상 동의어 — 경계를 더 명확히 하는 지점 없음 | 실질적 이득 없음 |
| **Selection** | `EngineSelectionPolicy`/`EngineSelectionDecision`(M17/18, "후보 Engine 중 하나를 고른다")과 충돌 | "5개 소스 중 하나를 고른다"는 표면적 유사성은 있으나 Engine Selection은 완전히 다른 실행 메커니즘을 가리키는 확립된 용어 | 기존 의미와 충돌 |
| **Decision** | `GateDecision`/`ApprovalDecision`/`EngineSelectionDecision`/`BudgetDecision`/`LLMPolicyDecision`/`RetryDecision` — 이미 6개나 확립된 `*Decision`(정책의 확정적 판정) 접미사 패턴과 충돌 | 의미도 부정확 — Recommendation은 비구속적인데 "Decision"은 확정된 판정을 뜻해, Gate가 담당하는 실제 Decision(`GateDecision`)과의 구분이 흐려짐 | 기존 의미와 충돌 + 의미상 부정확 |
| **Proposal** | 코드에는 없지만 `.ai/TASKS.md`/`.ai/DECISIONS.md`에서 "Milestone Proposal(T04 제안서)"이라는 프로젝트 메타 프로세스 용어로 이미 8회 이상 확립 | 뜻 자체는 나쁘지 않으나 Domain 용어와 프로세스 용어가 같은 단어를 쓰면 향후 문서에서 혼동 위험 | 기존 의미와 충돌(프로세스 어휘) |

### Decision

**"Recommendation"을 AI Workspace의 공식 Domain Vocabulary로
유지한다.** 4개 대안(Suggest/Selection/Decision/Proposal) 모두
기존 의미와 충돌하거나(Selection/Decision/Proposal) 실질적 이득이
없어(Suggest) 채택하지 않는다.

**Recommendation의 정의를 이 ADR로 고정한다**: *The domain concept
responsible for determining the most appropriate Next Action from
the current project state. It represents an actionable
recommendation, not a mandatory decision.* — 이 한 문장이 M35
(Recommendation Intelligence)/M42(Recommendation Adaptation)/M43
(Recommendation Orchestration)를 모두 자연스럽게 설명한다.

### Consequences

- Recommendation은 "사용자에게 제안을 하는 기능"이 아니라, **현재
  프로젝트 상태를 분석해 Next Action을 결정하는 Domain 개념**으로
  정의된다 — 이 정의는 `docs/ARCHITECTURE.md` §13.3에 그대로
  반영되어 새로 합류하는 개발자도 즉시 이 용어의 경계를 이해할 수
  있다.
- 리네이밍을 하지 않으므로 코드 변경은 0건이다 — `pytest`/`ruff`/
  `mypy`/Guardian은 기존 상태 그대로 유지된다.
- 이번에 비교한 4개 대안과 그 기각 사유가 문서로 고정되므로, 향후
  같은 논의("Recommendation이라는 이름이 맞나?")가 재발해도 이
  ADR을 먼저 참고하면 되고 같은 조사를 반복할 필요가 없다.
- 이 ADR은 "리네이밍을 하지 않기로 했다"는 소극적 결론이 아니라,
  Recommendation이 이 프로젝트에서 정확히 무엇을 의미하는지 공식
  정의하고 대안을 검토한 뒤 유지를 결정한 것 — 프로젝트의
  Ubiquitous Language를 확정하는 기준 문서로 남긴다.
- 결과/영향: `docs/ARCHITECTURE.md` §13.3 Recommendation 행에 정의
  문장과 대안 비교 요약 반영. 코드/테스트 변경 없음(문서화 전용).

## ADR-0061: Recommendation Explainability — Recommendation의 근거를 구조적으로 재구성(Milestone 44)

- 상태: 승인됨 (2026-07-31, 사용자가 M43 완료로 Recommendation Flow
  가 완전히 연결된 시점을 근거로 M44 제안서를 직접 작성해 제시 —
  Responsibility/관계 다이어그램/출력 예시/Domain Analysis/구현
  난이도까지 포함된 상세 제안을 검토한 뒤 그대로 진행 승인)
- 날짜: 2026-07-31
- 배경: M43(Recommendation Orchestration)으로 Recommendation(M35)
  →Adaptation(M42)→Orchestration(M43)→Execution(M36)→Memory(M39)
  →Experience(M40)로 이어지는 내부 루프가 완성됐다. 이 시점부터는
  "AI가 올바르게 행동하는 능력"(M29~M43)에서 "AI가 자신의 행동을
  설명할 수 있는 능력"으로 확장하는 것이 자연스럽다는 사용자 판단에
  따라, Recommendation이 왜 선택됐는지("Current Work보다 Capability
  Gap이 왜 선택됐는가", "Experience 때문에 왜 Adjustment가
  발생했는가")를 공식 Domain Concept로 만든다.
- 결정:
  1. **Recommendation과 Explainability는 책임이 다르다(Domain
     Analysis)**: Recommendation은 "무엇을 할 것인가", Explainability
     는 "왜 그렇게 결정했는가" — Explainability는 Recommendation
     자체를 바꾸지 않는다(새 Responsibility, 새 판단 아님).
  2. **`RecommendationExplanationAnalyzer`(신규,
     `intelligence/recommendation_explanation.py`)**: `RecommendationIntelligenceReport`
     (M35, Adaptation 반영 시 M42) + `ExperienceReport`(M40, 선택)를
     입력받아 5단계 Priority Rule 평가 흔적(`PriorityStepTrace`) +
     Experience 성공률 요약 + Adaptation 적용 여부/사유를
     `RecommendationExplanationReport`로 재구성하는 순수 Analyzer.
     새 AI 판단·새 지표 없음 — 이미 계산된 값만 읽는다. Deterministic
     + Immutable Input(M40/M42와 동일 조건).
  3. **`RecommendationExplanationService`(신규,
     `intelligence/recommendation_explanation_service.py`)**: Analyzer
     호출 + Vault 발행만 조합. `VaultAdapter.publish_recommendation_explanation()`
     (신규)이 `15 Project Intelligence/Recommendation Explanation.md`
     에 원자적으로 덮어쓴다.
  4. **`Explainability`는 §13.3 Behavioral Concept로 등재** —
     `Adaptation`(M42)과 동일한 급. 재사용 사례가 이번 1건뿐이라
     1급 Domain(§13.2) 승격은 보류(재사용 사례 축적 시 재검토).
  5. **`RecommendationOrchestrationService`(M43) 연결**:
     `explanation_service`를 선택적으로 주입하면 Recommendation
     계산 직후(Execution 위임 전) Explanation을 Vault에 기록한다 —
     Recommendation→Explainability→Execution 순서(사용자 제안
     다이어그램과 일치). 미주입 시 M43 이전과 100% 동일 동작
     (하위 호환). `web/server.py`가 이 Service를 조립해 실제로
     매 추천 실행마다 근거가 Vault에 기록되도록 배선한다.
- 대안:
  - **Explanation을 Recommendation Report 안에 직접 포함시킨다** —
    기각. Recommendation(M35)/Adaptation(M42)이 이미 안정적으로
    쓰이는 값 객체에 새 필드를 계속 추가하면 책임이 섞인다 —
    별도 Analyzer/Service로 분리해 "무엇을"과 "왜"의 책임을
    명확히 나눈다(Domain Analysis 결론).
  - **`RecommendationExecutionService`(M36)나 `RecommendationOrchestrationService`
    (M43)에 설명 로직을 내장한다** — 기각. 두 Service 모두 이미
    확립된 좁은 책임(실행/흐름 제어)을 갖는다 — Explanation은 별도
    Analyzer로 분리해야 재사용성(Dashboard/API/CLI/Multi-Agent
    Reviewer)이 생긴다.
- 이유: M43로 완성된 Recommendation Flow가 "설명할 대상이 안정된"
  시점을 만들었다 — 이미 계산된 값(Recommendation Report/Experience
  Report/Priority Rule/Adaptation 결과)만 재사용하면 되므로 새로운
  AI 판단이나 새 데이터 접근 경로 없이 구현 난이도가 낮다. Analyzer/
  Service 분리는 ADR-0057 역할 규칙에 그대로 부합한다.
- 결과/영향: `intelligence/recommendation_explanation.py`(신규),
  `intelligence/recommendation_explanation_service.py`(신규),
  `vault/recommendation_explanation.py`(신규), `integration/vault_adapter.py`
  (확장), `runtime/execution/recommendation_orchestration_service.py`
  (`explanation_service` 선택적 인자 추가), `web/server.py`(Composition
  Root 갱신), `docs/ARCHITECTURE.md` §13.3/§13.4/§3.36(신규) 갱신.
  Vault `15 Project Intelligence/Recommendation Explanation.md`
  신규 생성(실제 저장소 상태로 발행). 새 Core Domain Interface/
  Adapter 없음(27종 유지). `pytest` 1073개(9개 신규) 통과, `ruff`/
  `mypy` 통과, `guardian.checker.evaluate()` all_passed 유지,
  `build_app()` 실제 조립 스모크 테스트 통과.

## ADR-0062: Workspace Observability — Claude Runtime + Pipeline 상태를 StatusLine으로 반영(Milestone 45)

- 상태: 승인됨 (2026-07-31, 사용자가 M44까지 완성된 Recommendation
  Flow 위에서 "결과만 보이던 것을 과정도 실시간으로 보이게 한다"는
  목표와 함께 표시 항목·설계 원칙(`WorkspaceRuntimeSnapshot` 읽기
  전용 모델, StatusLine은 표시만)까지 제시하고 T01~T04 프로세스로
  진행을 요청 — 검토 결과에 따라 진행하도록 사전 승인)
- 날짜: 2026-07-31
- 배경: M35~M44로 Recommendation(M35)→Adaptation(M42)→Explainability(M44)
  →Orchestration(M43)→Execution(M36)→Memory(M39)→Experience(M40)
  파이프라인이 완성됐지만, 이 모든 과정은 Vault 문서나 pytest
  로그로만 사후 확인 가능하고 Claude Code 세션 안에서 지금 무엇이
  진행 중인지 실시간으로 볼 방법이 없었다. 새 AI 판단이나 자동화를
  추가하는 것이 아니라, 이미 있는 상태를 사람이 볼 수 있게 만드는
  것이 목적이다.
- 결정:
  1. **Domain Analysis(T01)**: `Observability`는 §13.2 4개 핵심
     Domain 중 어느 것도 아니다 — Intelligence와 같이 Read Only지만
     "지금 상황이 어떤가"를 새로 판단(분석·요약)하지 않고 이미
     계산된 값의 존재 여부만 반영한다는 점에서 다르다. Guardian도
     아니다 — 아키텍처 규칙 준수를 평가하지 않는다. 재사용 사례가
     이번 1건(StatusLine)뿐이므로 `Adaptation`/`Explainability`/
     `Orchestration`과 같은 급의 **Behavioral Concept**로 §13.3에
     등재하고, 1급 Domain(§13.2) 승격은 재사용 사례가 쌓일 때(예:
     Dashboard Observability) 재검토한다.
  2. **Architecture Review(T02)**: 새 Core Domain Interface/Adapter를
     만들지 않는다. `VaultAdapter`에 읽기 전용 메서드
     `report_last_modified()` 1개만 추가(Reuse First — 새 Adapter
     대신 기존 Adapter 확장)해 Vault 산출물의 존재/최신 여부를
     조회한다. `intelligence/`에 얹지 않고 별도 `observability/`
     패키지를 새로 둔다 — Intelligence는 `VaultAdapter`/`AgentAdapter`
     읽기 의존만 허용하는 좁은 계약인데, Observability의 1차
     데이터 소스는 Claude Code StatusLine stdin JSON(Vault/Agent와
     무관한 외부 세션 정보)이라 그 계약에 억지로 끼워 맞추면 의미가
     흐려진다(Guardian이 Read Only이면서도 별도 패키지를 받은
     선례와 동일한 논리).
  3. **Detailed Design(T03) — Phase 1의 정직한 한계**: 7단계 중
     Adaptation/Orchestration은 별도 Vault 산출물이 없다(M42/M43
     Domain Analysis에서 이미 확인된 사실 — 둘 다 다른 산출물에
     구조적으로 포함됨) → `STRUCTURAL_INCLUDED`로 표시. Memory(M39)
     는 `InMemoryMemoryEngine` 기반이라 프로세스 재시작 시 사라지고
     Vault에도 영속화되지 않아, 별도 프로세스로 실행되는 StatusLine
     에서는 조회할 수 없다 → `NOT_OBSERVABLE`로 표시하고 이유를
     명시한다. 실제로 관측 가능한 4단계(Recommendation/Explainability/
     Execution/Experience)만 Vault 문서 존재 여부(`report_last_modified()`)
     로 `OBSERVED_DONE`/`OBSERVED_NOT_YET`을 판정한다 — 값을 지어내지
     않는다는 원칙(사용자 요청 "추정값은 사용하지 않는다")을 그대로
     지킨다. Claude Runtime 정보(Model/Effort/Context 사용량/
     Input·Output Tokens)는 Claude Code StatusLine stdin JSON의
     공식 문서화된 필드(`model.display_name`/`effort.level`/
     `context_window.*`)만 그대로 옮긴다 — 제공되지 않는 필드(예:
     effort를 지원하지 않는 모델)는 `None`으로 남기고 추정하지 않는다.
  4. **Implementation Plan(T04)**: `observability/snapshot.py`
     (`WorkspaceRuntimeSnapshot`/`ClaudeRuntimeInfo`/`WorkspaceInfo`/
     `PipelineStageState`/`PipelineStageStatus`, 메서드 없는 값
     객체만), `observability/claude_runtime_analyzer.py`/
     `pipeline_stage_analyzer.py`/`workspace_info_analyzer.py`(3개
     순수 Analyzer), `observability/runtime_snapshot_service.py`
     (`RuntimeSnapshotService`, 3개 Analyzer 조합만), `observability/
     statusline_renderer.py`(`StatusLineRenderer`, 순수 포맷팅),
     `observability/statusline_main.py`(진입점 — stdin 파싱, 어떤
     예외도 밖으로 내지 않고 항상 한 줄 출력). `.claude/settings.json`
     신규(`statusLine.command`로 배선). `WorkspaceInfo.current_workflow`
     는 §13.2 Workflow와 혼동을 피하기 위해 근거 없이 채우지 않고
     Phase 1은 항상 `None`(사용자가 "선택"으로 표시한 항목, Phase 2
     후보로 명시).
- 대안:
  - **`intelligence/`에 그대로 얹는다** — 기각. Intelligence의
    좁은 의존 계약(§13.2, `VaultAdapter`/`AgentAdapter`만)과
    Observability의 실제 데이터 소스(Claude Code 세션 stdin)가
    맞지 않는다 — 억지로 맞추면 Intelligence의 "판단" 책임과
    Observability의 "이미 있는 것을 보여주기"가 코드에서 구분되지
    않는다.
  - **`runtime/`(기존 Execution/Agent Runtime 패키지)를 재사용한다**
    — 기각. `runtime/`은 이미 Agent Runtime/Engine Runtime/
    Execution/Automation을 가리키는 확립된 이름(§13.6 디렉터리명↔
    Domain 1:1 대응)이라, Claude Code 세션 Runtime이라는 전혀 다른
    의미로 재사용하면 이름만 보고 책임을 유추할 수 없게 된다.
  - **각 단계(Adaptation/Orchestration/Memory)에 새 상태 기록
    (Instrumentation)을 추가해 완전한 실시간 추적을 만든다** —
    기각(Phase 2 후보로만 문서화). 기존 Domain의 책임을 변경/추가
    하는 것이라 이번 Milestone의 목표("새로운 AI 판단이나 자동화를
    구현하는 것이 아니다")와 사용자가 명시한 범위(기존 Domain 책임
    변경 금지)를 벗어난다 — 대신 Phase 1은 관측 가능한 것만
    정직하게 관측한다.
- 이유: M44까지 안정화된 Recommendation 계열 코드/판단 로직을 전혀
  건드리지 않고, 이미 존재하는 Vault 산출물과 Claude Code가 이미
  제공하는 세션 정보만 읽어 실시간 가시성을 얻을 수 있어 구현
  난이도가 낮고 리스크가 없다. Analyzer/Service/Renderer 분리는
  ADR-0057 역할 규칙과 §13.6 명명 규칙에 그대로 부합한다.
- 결과/영향: `observability/`(신규 패키지: `snapshot.py`/
  `claude_runtime_analyzer.py`/`pipeline_stage_analyzer.py`/
  `workspace_info_analyzer.py`/`runtime_snapshot_service.py`/
  `statusline_renderer.py`/`statusline_main.py`), `integration/
  vault_adapter.py`(`report_last_modified()` 1개 메서드 추가),
  `.claude/settings.json`(신규, `statusLine` 배선), `docs/ARCHITECTURE.md`
  §13.3/§13.4/§3.37(신규)/헤더 상태 갱신. Vault 신규 발행 없음(Phase 1은
  StatusLine 전용, Dashboard/Web UI는 범위 밖). 새 Core Domain
  Interface/Adapter 없음(27종 유지). `pytest` 1090개(17개 신규)
  통과, `ruff`/`mypy` 통과, `guardian.checker.evaluate()` all_passed
  유지, `build_app()` 실제 조립 스모크 테스트 통과.

## ADR-0063: Workspace Observability 확장 — Execution Environment(Git/Guardian/Vault/MCP) 관찰(Milestone 45 확장)

- 상태: 승인됨 (2026-07-31, 사용자가 M45(Claude Runtime + Pipeline
  Observability)를 "AI Workspace Runtime"뿐 아니라 "Execution
  Environment"까지 확장하도록 요청 — 관측 가능한 필드를 먼저 조사한
  뒤 추정값 없이 사용 가능한 항목만 구현하도록 명시적으로 조건을
  제시하고 T01~T04 프로세스로 진행 요청)
- 날짜: 2026-07-31
- 배경: ADR-0062(M45)는 Claude Runtime(Model/Effort/Context)과
  Recommendation 파이프라인 7단계만 관찰했다. 실제로 이 파이프라인이
  "어떤 환경에서" 실행되는지(Git 브랜치/Working Tree 상태, Guardian
  아키텍처 준수, Vault 문서 상태, MCP 연결 상태 — 특히 Obsidian MCP)
  는 아직 보이지 않았다. 구현 전에 Claude Code/MCP가 실제로 무엇을
  공식 제공하는지부터 조사(공식 문서 확인)하고, 확인되지 않은 것은
  추정하지 말고 Not Available로 남기는 것을 전제 조건으로 진행했다.
- 결정:
  1. **Domain Analysis(T01)**: 이 확장은 새 Domain도, 새 Behavioral
     Concept도 아니다 — ADR-0062가 이미 §13.3에 등재한 `Observability`
     를 그대로 확장한 것(관찰 대상이 늘었을 뿐 책임의 성격은 동일:
     이미 있는 상태를 읽기만 하고 새 판단을 하지 않음). §13.3에 새
     행을 추가하지 않는다.
  2. **Architecture Review(T02) — 조사 결과(공식 문서 확인)**:
     - StatusLine stdin JSON에는 MCP 관련 필드가 전혀 없음(공식
       문서 확인) — MCP는 별도 경로가 필요.
     - `claude mcp list`(공식 CLI)가 서버별 연결 상태를 사람이 읽는
       텍스트로 출력(`✔`=Connected/`✘`=Failed·Connection error/
       `!`=Needs auth/`⏸`=Pending approval, JSON 옵션 없음, 공식
       문서 확인). `.mcp.json`(프로젝트 범위 설정 파일, 공식 문서화된
       스키마)이 "설정된 서버 목록"을 알려준다.
     - Hook(`PostToolUse`) payload는 `tool_name`이 `mcp__<server>__
       <tool>` 형식으로 MCP 서버/도구를 식별할 수 있지만, 별도 에러
       필드나 "지금 연결 중인 서버" 상태는 제공하지 않음(공식 문서
       확인) — Last MCP Call/Last Error를 안전하게 관측할 공식 경로
       없음.
     - `pytest`/`ruff`/`mypy`/Coverage 전체 재실행은 수 초 이상
       걸려 StatusLine 갱신(세션 이벤트마다)마다 다시 실행하면
       지연·타임아웃 위험이 큼 — `guardian.checker.evaluate()`만
       AST 기반 순수 평가라 저비용으로 재사용 가능, 나머지는 재실행
       금지.
     - 새 Core Domain Interface/Adapter 없음(27종 유지). `observability/`
       패키지(M45)를 그대로 확장 — 새 패키지 분리 불필요.
  3. **Detailed Design(T03) — 관측 가능/불가능 항목 확정**:
     - **관측 가능(구현)**: Git(`current_branch`/`working_tree_dirty`/
       `ahead`/`behind`/`last_commit_summary`, `git` 하위 명령만),
       Guardian(`guardian_all_passed`, 재평가 / `pytest_failed_count`,
       `.pytest_cache/v/cache/lastfailed` 마지막 로컬 실행 결과만),
       Vault(`vault_connected`/`current_milestone`(M45 재사용)/
       `current_adr`/`last_modified_epoch`, `VaultAdapter.
       report_last_modified()`만), MCP(`mcp_enabled`/`configured_servers`,
       `.mcp.json`만 / `connected_servers`, `claude mcp list` 문서화된
       기호만 매칭, 형식 불일치 시 `None`).
     - **관측 불가(Not Available, 이유 명시)**: `ruff_status`/
       `mypy_status`/`coverage_percentage`(재실행 비용), MCP
       `active_server`(정적 조회로 "지금 이 순간" 알 수 없음)/
       `available_tools`(공식 출력에 보장된 형식 없음)/`last_mcp_call`/
       `last_mcp_error`(공식 로그 미문서화, Hook 신규 도입은 별도
       승인 필요), Vault `current_pr`(GitHub API 네트워크+인증
       필요), Workspace `current_task`(상시 실행 프로세스가 아니라
       계측 불가, Domain 책임 변경 금지와 충돌).
     - `ahead`/`behind`는 `git fetch`를 하지 않음(네트워크 호출 없음
       원칙) — 마지막으로 로컬에 캐시된 원격 추적 브랜치 기준.
  4. **Implementation Plan(T04)**: `observability/git_runtime_analyzer.py`/
     `guardian_runtime_analyzer.py`/`vault_runtime_analyzer.py`/
     `mcp_runtime_analyzer.py`(신규 4개 Analyzer) + `snapshot.py`
     확장(`GitRuntimeInfo`/`GuardianRuntimeInfo`/`VaultRuntimeInfo`/
     `McpRuntimeInfo`, `WorkspaceInfo.current_task` 필드 추가) +
     `RuntimeSnapshotService`/`StatusLineRenderer` 확장(4개 Analyzer
     조합 + 4개 줄 렌더링).
- 대안:
  - **MCP 연결 상태를 `~/.cache/claude-cli-nodejs/.../mcp-logs-*`
    같은 비공식 로그 디렉터리에서 읽는다** — 기각. 실제로 관찰되긴
    하지만 공식 문서에 없는 내부 구현 세부사항이라 버전이 바뀌면
    깨질 수 있고, 이번 세션(Claude Code on the web) 환경 한정일
    수 있어 "추정하지 않는다"는 원칙과 맞지 않는다. 문서화된
    `.mcp.json`/`claude mcp list`만 사용한다.
  - **PostToolUse Hook을 새로 추가해 MCP 호출/에러 이력을 로컬
    파일에 기록한다** — 기각(Phase 2 후보로만 문서화). 이미 있는
    상태를 읽는 것이 아니라 새로운 기록 메커니즘을 도입하는
    것이라 "새로운 자동화/계측 추가 없음" 원칙과 이번 승인 범위를
    벗어난다 — 필요하면 별도 제안·승인을 받는다.
  - **`ruff`/`mypy`를 매 StatusLine 갱신마다 실행한다** — 기각.
    수백 밀리초~수 초가 걸려 StatusLine이 매 세션 이벤트마다
    호출된다는 점(공식 문서 확인)과 충돌 — 응답 지연/타임아웃
    위험이 실사용성을 해친다.
  - **Git `ahead`/`behind`를 위해 `git fetch`를 먼저 실행한다** —
    기각. 네트워크 호출이 되어 Observability의 "네트워크 호출
    없음" 원칙(§3.37/ADR-0062)과 충돌하고, StatusLine 응답이
    네트워크 상태에 좌우된다.
- 이유: 확장 대상(Git/Guardian/Vault/MCP) 모두 공식 문서 또는 이미
  존재하는 Vault/Adapter 경로로 안전하게 읽을 수 있는 부분과, 공식
  경로가 없어 정직하게 Not Available로 남겨야 하는 부분을 명확히
  구분했다 — 추정값을 배제하면서도 실제로 유용한 관찰(Git 상태/
  Guardian 준수/Vault 최신성/MCP 설정)을 추가할 수 있다.
- 결과/영향: `observability/`(4개 파일 추가: `git_runtime_analyzer.py`/
  `guardian_runtime_analyzer.py`/`vault_runtime_analyzer.py`/
  `mcp_runtime_analyzer.py`), `observability/snapshot.py`(`GitRuntimeInfo`/
  `GuardianRuntimeInfo`/`VaultRuntimeInfo`/`McpRuntimeInfo` 추가,
  `WorkspaceInfo.current_task` 필드 추가), `observability/
  runtime_snapshot_service.py`/`statusline_renderer.py`(확장),
  `docs/ARCHITECTURE.md` §3.38(신규)/헤더 상태 갱신. 새 Core Domain
  Interface/Adapter 없음(27종 유지, `VaultAdapter`/`guardian.checker`
  기존 계약 재사용만). Vault 신규 발행 없음(StatusLine 전용 유지).
  `pytest` 1108개(18개 신규) 통과, `ruff`/`mypy` 통과,
  `guardian.checker.evaluate()` all_passed 유지, `build_app()` 실제
  조립 스모크 테스트 통과.

## ADR-0064: Vault Information Architecture — Vault를 AI Long-term Memory Layer로 재정의 (Milestone 46, 문서화 전용)

- 상태: 승인됨 (2026-07-31, 사용자가 M39~M45로 기능 아키텍처가
  안정화된 시점에 Vault의 Information Architecture를 재검토하도록
  T01~T04 절차와 "기능 변경 금지"/"Graphify는 참고 모델(그대로
  복사 금지)"/"Long-term Memory First" 3대 원칙을 명시적으로 제시)
- 날짜: 2026-07-31
- 배경: Obsidian Vault는 M23(Obsidian Knowledge Base 구축)부터
  Milestone이 진행될 때마다 점진적으로 자랐다 — 각 Milestone이
  자기 산출물만 추가했을 뿐, Vault 전체를 하나의 Knowledge Graph
  로 보는 상위 설계가 없었다. 실제로 Vault를 전수 분석(T01)한
  결과 이 가설이 데이터로 확인됐다: Frontmatter는 100% 있지만
  `type` 필드는 13/49 문서에만 있고, `ADR Index.md`/`Milestones
  Index.md`가 관련 문서를 `[[WikiLink]]`가 아니라 백틱 텍스트로만
  언급해 Graph View/Backlink 패널에 실제 지식 구조가 드러나지
  않는다.
- 결정:
  1. **T01 Current Vault Analysis(실측)**: 49개 Vault Markdown
     문서를 스크립트로 전수 분석 — Document Type/Tag/Frontmatter/
     Wiki Link/Orphan/Backlink를 정량화했다. 강점(`00 System/
     PROJECT_INDEX.md`가 이미 사실상 MOC로 기능, ADR/Decision
     2단 계층 등)과 한계(백틱 텍스트 참조, 1회성 Tag, `13 Daily`/
     `14 Tasks` 미사용, Concept 문서 부재 등) 모두 추측 없이
     증명했다.
  2. **T02 Domain & Architecture Analysis**: Graphify/Second
     Brain 철학 7개 항목(Knowledge Graph First/MOC/Wiki Link
     First/Metadata First/Project·Label Standard/Concept/Document
     Type Color)마다 채택·수정·기각을 근거와 함께 판단했다 — 예:
     "모든 것을 Node로 만든다"는 원문은 기각(GitHub 원본과 이중
     관리 위험)하고 "GitHub 원문을 대표하는 얇은 Vault Node + Wiki
     Link"로 수정 채택. Dataview는 `.obsidian/community-plugins.json`
     이 빈 배열임을 실측 확인해 기각(Desktop 검증 후 재검토
     조건부).
  3. **T03 MDD Review**: Node Definition(ADR/Milestone/Decision/
     Concept/Project Intelligence는 Node, PR/Runtime은 Node
     아님), Relationship Definition(9종, 별도 Frontmatter 필드
     없이 Wiki Link+문구로만 표현), Folder/Document/Index/Hub/
     Concept/Lesson/Roadmap Role을 정의했다. Long-term Memory
     Strategy로 "Concept 문서가 장기 기억의 뼈대"라는 원칙과 "실제
     데이터 없이 Lesson 구조부터 만들지 않는다"(YAGNI)는 원칙을
     확정했다.
  4. **Document Type Color Strategy는 §14.2를 폐기하지 않고
     확장한다**: 기존 Domain 기반 6-Cluster 색상(Intelligence=
     Blue/Execution=Green/Memory=Yellow/Architecture=Purple/
     Documentation=Orange)을 전부 재사용하고, Document Type이라는
     새 1차 축을 추가한다. `.obsidian/graph.json` 실제 적용은
     **이번에 하지 않는다** — 2026-07-30 사용자 결정으로 동결된
     Pending Verification 상태(Desktop 검증 대기)를 그대로
     유지한다.
  5. **T04 Migration Plan은 삭제 없는 증분 방식**: 기존 문서 삭제
     0건. 이번 PR은 Phase 0(`02 Architecture/`에 IA 문서 5개 신규
     생성 + `PROJECT_INDEX.md`에 진입점 1줄 추가)만 실행한다.
     Recommendation Hub/Concept 문서 8종/기존 문서 `type` 일괄
     추가/Roadmap Hub/Color 실제 적용은 전부 별도 Phase로 제안만
     하고 이번 범위에 포함하지 않는다.
- 대안:
  - **Graphify를 그대로 이식한다**(모든 것을 Node화, 광범위
    Metadata 스키마) — 기각. 이 저장소는 GitHub이 이미 Source of
    Truth이고 Vault는 파생 뷰라는 기존 원칙(§9, ADR-0037)과
    충돌한다.
  - **이번에 `.obsidian/graph.json`을 새 Color 체계로 즉시
    적용한다** — 기각. graph.json은 이미 2026-07-30 Pending
    Verification으로 동결돼 있고(Desktop 검증 없이는 Schema
    비호환/iOS 구현 제약/Mobile 버그를 구분할 수 없음), 이 결정을
    뒤집을 새 증거가 없다.
  - **기존 36개 문서에 `type` Frontmatter를 이번 PR에서 일괄
    추가한다** — 기각. 이번 Milestone 범위(Information Architecture
    설계)를 벗어난 대규모 일괄 편집이며, ADR-0057 Boy Scout Rule과
    동일 정신으로 실제 그 문서를 건드릴 이유가 생겼을 때 점진
    적용한다.
  - **Lesson Node를 이번에 함께 설계·생성한다** — 기각(YAGNI).
    실제 회고 데이터가 없는 상태에서 구조부터 만들면 Graphify가
    경계하는 "구조를 위한 구조"가 된다.
- 이유: 실측(T01) 없이 설계하면 추측에 근거한 재설계가 되어 §9
  "추측하지 않는다" 원칙과 충돌한다. Graphify를 항목별로 채택/
  수정/기각하는 절차를 거쳐야 이 저장소의 기존 원칙(GitHub Source
  of Truth, Vocabulary Reuse First, 최소 Metadata, Boy Scout Rule)
  과 충돌 없이 통합된다. `.obsidian/graph.json` 동결을 유지한 채로
  설계까지만 완료하면, Desktop 검증이 풀리는 즉시 적용 가능한
  상태로 대비할 수 있다.
- 결과/영향: `02 Architecture/Vault Information Architecture.md`
  (신규, 마스터 문서), `Metadata Standard.md`(신규), `Document
  Type Color Strategy.md`(신규), `Map of Content Guide.md`(신규),
  `Vault Migration Plan.md`(신규), `00 System/PROJECT_INDEX.md`
  (Retrieval First 표에 1행 추가), `docs/ARCHITECTURE.md` §14
  (§15로의 연결 문구 추가)/§15(신규)/헤더 상태 갱신. 코드 변경
  없음 — `pytest`/`ruff`/`mypy`/`guardian.checker.evaluate()`
  전부 기존 상태(1108 passed) 그대로 유지. `.obsidian/graph.json`
  무변경(동결 유지). 기존 Vault 문서 삭제 0건, Rename 0건.

### 구현 단계 — Milestone 47(Knowledge Graph Migration, 2026-07-31, 신규 ADR 아님)

**ADR 필요 여부 판단**: 새 ADR을 작성하지 않는다. 이 작업은 새로운
아키텍처 결정이 아니라 ADR-0064가 이미 승인한 Migration Plan
(Phase 1~3)을 실행에 옮긴 것이다 — Domain Vocabulary/Node 정의/
Color 원칙/Backward Compatibility 원칙 중 무엇도 변경하지 않았다.

- **Phase 1 실행**: `15 Project Intelligence/Recommendation Hub.md`
  생성 — Recommendation 파이프라인(M35→M42→M43→M36→M44) 리포트
  3개(outgoing link 0건이었음)를 처음으로 연결.
- **Phase 2 실행(8종 → 7종으로 조정)**: `02 Architecture/Concepts/*.md`
  7개(Recommendation/Execution/Memory/Guardian/Observability/
  Automation/Runtime) + `Concept Index.md` 생성. ADR-0064가 원래
  열거한 8종 중 Adaptation/Orchestration/Explainability는
  Recommendation 파이프라인의 **단계**일 뿐 독립 Domain Vocabulary
  가 아니라고 판단해 별도 Concept 문서를 만들지 않았다(Reuse
  First를 Concept 생성에도 적용, [[Recommendation Hub]]에서 흐름
  으로 대체 표현) — 이 판단 자체가 새 아키텍처 결정이 아니라
  ADR-0064 T02-6("Concept 채택")의 적용 범위를 실측 근거로 좁힌
  것이다.
- **Phase 3 실행(Boy Scout Rule → 전수 백필로 승격)**: ADR-0064는
  원래 점진 적용(Boy Scout Rule)을 제안했으나, 사용자가 Milestone
  47에서 "Metadata Backfill 완료"를 DoD로 명시적으로 요구해 스크립트
  기반 전수 백필로 승격했다 — 기존 36개 문서 전부에 `type`을
  추가해 Vault 54개 문서 100% 커버리지를 달성했다. 매핑은
  [[Metadata Standard]]의 Document Type 표를 그대로 적용(새 Type
  발명 없음).
- **범위 확장 2건(ADR-0064 원안에 없던 것, 이번에 사용자가 명시
  요청)**:
  1. Architecture/Runtime/Decision/Knowledge Hub 4종 신규 — 기존
     Architecture Overview/ADR Index/Decisions Index/Milestones
     Index를 대체하지 않고 그 위에 얇은 진입점만 추가(내용 복제
     없음).
  2. `16 Lessons/Lessons.md` 신규 — ADR-0064 T03이 YAGNI로 명시
     보류했던 Lesson 구조를 이번에 준비만 한다(`13 Daily`/`14
     Tasks`와 동일 패턴 — 구조는 있지만 실제 항목은 없음, 허위
     데이터 생성 금지). `vault/mapping.py`의
     `VAULT_CONTENT_DIRECTORIES`에 17번째 디렉터리로 등록 —
     Recommendation/Execution/Guardian/Automation/Memory/
     Observability/Explainability/Orchestration 8개 보호 기능과
     무관한 Integration Layer 상수 목록 변경이다.
- **Color Migration(Phase 5)은 계속 Pending**: `.obsidian/graph.json`
  은 이번에도 수정하지 않는다 — 2026-07-30 동결 결정 유지. `type`
  필드가 이제 100% 채워져 있어 검증이 풀리는 즉시 적용 가능한
  상태로만 대비했다.
- 결과/영향: `15 Project Intelligence/Recommendation Hub.md`(신규),
  `02 Architecture/Concepts/`(7개 Concept + Concept Index, 신규),
  `02 Architecture/Architecture Hub.md`/`Runtime Hub.md`/`Decision
  Hub.md`/`Knowledge Hub.md`(신규), `16 Lessons/Lessons.md`(신규),
  기존 36개 문서에 `type` Frontmatter 추가, `00 System/
  PROJECT_INDEX.md`(3행 추가), `03 ADR/ADR Index.md`(백틱 참조 3건을
  Wiki Link로 전환), `src/ai_workspace/vault/mapping.py`
  (`VAULT_CONTENT_DIRECTORIES` 17종으로 확장), `docs/ARCHITECTURE.md`
  §15.1(신규)/헤더 상태 갱신. 코드 변경은 위 상수 목록 1건뿐 — 8개
  보호 기능 전부 무변경. `pytest` 1108개(회귀 없음, 신규 테스트
  없음)/`ruff`/`mypy`/`guardian.checker.evaluate()` 전부 기존 상태
  유지. `find_broken_backlinks()`로 신규 문서 전수 검증(줄바꿈 Wiki
  Link 오류 다수 발견·수정). `.obsidian/graph.json` 무변경. 기존
  Vault 문서 삭제 0건, Rename 0건.

## ADR-0065: Automation Foundation — Architecture Guardian을 Recommendation Orchestration의 Execution Gate에 연결 (Milestone 48)

- 상태: 승인됨 (2026-08-01, 사용자가 T01 Domain Analysis 방향에
  동의하고 T02 MDD Review에서 4개 항목 — Guardian 실행 시점/실패
  정책/Observability 연계/Learning과의 경계 — 을 명시적으로 지정,
  T02 MDD Review 결과를 확인 후 T03 구현에 최종 승인. Observability
  연계는 사용자가 "PASS/BLOCKED 상태 필드"를 추가로 요청해 반영)
- 날짜: 2026-08-01
- 배경: M48은 원래 `docs/ARCHITECTURE.md` §2.1이 예약해 둔 "Automation
  Core" 3대 Engine(Memory/Guardian/Learning) 중 마지막 Learning
  Engine 구현으로 시작할 계획이었다. 그러나 M35~M47 구현 완료 후
  사용자 지시로 T01 Domain Analysis를 재수행한 결과(코드 전수
  조사), `RecommendationOrchestrationService`(M43)가 실제로
  Automation Trigger마다 Experience→Recommendation+Adaptation→
  Explainability→Execution→Task Lifecycle→Memory를 자동 실행하고
  있음에도 **Architecture Guardian(M41)은 이 자동 경로 어디에도
  연결돼 있지 않다**(테스트/StatusLine에서만 평가됨)는 것이
  확인됐다. Learning이 관찰할 신호(Guardian 위반 이력)가 애초에
  자동으로 쌓이지 않는 상태에서 Learning Engine을 먼저 설계하는
  것은 DX-02(YAGNI) 위반 소지가 크다고 판단해, M48을 "Automation
  Foundation"(Guardian↔Automation 연결)으로 재정의하고 Learning
  Engine은 M49 이후로 분리했다.
- 결정:
  1. **Guardian 실행 시점 — Pre-Execution(Execution 직전)**:
     Recommendation/Adaptation/Explainability는 Read-Only 분석이라
     Guardian 위반 여부와 무관하게 항상 그대로 계산·발행된다.
     `RecommendationOrchestrationService.execute()/publish()`가
     `execution_service.execute()`를 호출하기 직전에만(주입된 경우)
     `ArchitectureGuardianService.generate()`(M41, Read Only)를
     호출해 `ArchitectureHealthReport`를 얻어 전달한다.
  2. **Guardian 실패 정책 — "Recommendation은 그대로 생성, Execution만
     차단", Override 없음**: `ExecutionGate.check()`에 선택적
     `guardian_report` 파라미터를 추가했다 — 주어지고
     `all_passed`가 `False`이면 `source`/`manual_trigger` 조건보다
     먼저 거부한다(`GUARDIAN_BLOCK_REASON_PREFIX`, `guardian/
     models.py`가 정본 소유). Automation 전체 중단은 채택하지
     않는다(`AutomationScheduler`가 무관한 다른 Rule까지 멈출
     이유가 없다는 기존 설계와 상충). Override는 실제 필요 사례가
     없어 이번에 설계하지 않는다(YAGNI).
  3. **Observability 연계 — `AutomationGateStatus`(PASS/BLOCKED/
     UNKNOWN) 상태 필드 + 이유 문자열**: 사용자가 "PASS/BLOCKED
     상태 하나를 StatusLine에서 한눈에 보여주는 것이 M45와도,
     향후 M49 Learning/M50 이후 정책 Gate 확장과도 자연스럽게
     이어진다"고 최종 의견을 제시해, 이유 문자열
     (`last_automation_gate_reason`) 하나만 노출하려던 MDD Review
     초안에서 `AutomationGateStatus` Enum 필드
     (`last_automation_gate_status`)를 추가로 반영했다. `guardian_
     runtime_analyzer.py`(M45 확장)가 새 Vault 문서나 `VaultAdapter`
     메서드 없이, Vault Root == Repository Root(ADR-0037)를 이용해
     이미 존재하는 `15 Project Intelligence/Recommendation
     Execution.md`(M36)의 "이유" 줄을 직접 읽어 채운다 — 문서가
     없으면(Automation 미실행) `UNKNOWN`으로 정직하게 남긴다(추정
     금지). M45의 `guardian_all_passed`(라이브 재평가, "지금
     소스가 통과하는가")는 그대로 유지 — `last_automation_gate_
     status`는 다른 질문("가장 최근 Automation 실행이 Guardian
     때문에 막혔는가", 이력)에 답한다. "Running" 상태는 만들지
     않는다 — Guardian은 동기 호출이라 그런 중간 상태가 실제로
     존재하지 않는다(허위 표시 금지).
  4. **Learning과의 경계 — M48은 Execution 결과를 학습하지
     않는다**: Guardian 평가 결과는 `ExecutionMemoryStore`(M39)에
     기록되지 않고, `RecommendationAdjustmentAnalyzer`(M42
     Adaptation)의 입력에도 포함되지 않는다. Guardian 위반 이력을
     근거로 향후 추천을 조정하는 로직은 전혀 설계하지 않는다 —
     M49 이후 Learning Engine 제안 시점에 이번에 쌓이는
     `Recommendation Execution.md` 이력을 근거 자료로만 참고한다.
  5. **신규 Interface/Service/Adapter/Layer/File 없음**: MDD
     Review(Reuse First)로 확인된 대로, 기존 6개 파일(`ExecutionGate`/
     `RecommendationExecutionService`/`RecommendationOrchestrationService`/
     `GuardianRuntimeInfo`(`observability/snapshot.py`)/
     `GuardianRuntimeAnalyzer`/`web/server.py`)의 선택적 의존성
     주입(기본값 `None`)만으로 구현했다 — M38/M39/M42/M44와 동일한
     패턴. `GUARDIAN_BLOCK_REASON_PREFIX` 상수는 새 모듈이 아니라
     `guardian/models.py`(기존 파일)에 추가해 Guardian이 정본
     소유자가 되도록 했다.
- 대안:
  - **Guardian을 Recommendation 이전(Pre-flight)에 실행해
    Read-Only 분석 자체를 막는다** — 기각. Recommendation은
    Architecture 위반과 무관하게 유용한 정보이므로 과잉 차단이다.
  - **Guardian 평가를 Execution 이후(Post-flight)에 실행한다** —
    기각. 이미 부작용(Execution)이 발생한 뒤라 "차단"의 의미가
    없고, Post-flight 관측은 이미 M45(`GuardianRuntimeAnalyzer`의
    라이브 재평가)가 제공하고 있어 중복이다.
  - **Warning만 출력하고 Execution은 그대로 진행** — 기각. Guardian이
    "평가·공표"에서 끝나던 M41 이전과 실질적으로 다르지 않아
    연결의 의미가 없다.
  - **Guardian 위반 시 Automation 전체(다른 Rule 포함)를 중단** —
    기각. `AutomationScheduler`의 "한 Rule 실패가 다른 Rule에
    영향 없음" 기존 설계와 상충한다.
  - **Override 플래그를 함께 설계** — 기각(YAGNI). 실제 필요 사례가
    없는 상태에서 "누가/어떤 조건으로"라는 별도 설계 결정을 지금
    내리면 추측성 코드가 된다.
  - **StatusLine에 이유 문자열만 노출하고 상태 필드는 만들지
    않는다**(MDD Review 초안) — 기각(사용자 최종 의견 반영).
    PASS/BLOCKED 상태 필드가 있어야 StatusLine에서 Automation의
    현재 건강 상태를 한눈에 파악할 수 있고, M49/M50 이후 정책
    Gate가 늘어나도 같은 Enum 패턴으로 자연스럽게 확장된다.
- 이유: Automation의 각 단계(Recommendation/Adaptation/Explainability/
  Execution/Task Lifecycle/Memory/Experience)는 이미 자동 연결돼
  있었지만 Guardian만 예외였다 — 이 Gap을 메우는 것이 아직 신호가
  쌓이지 않은 Learning Engine을 새로 설계하는 것보다 우선순위가
  높다는 것이 T01 Domain Analysis의 핵심 발견이었다. Recommendation은
  그대로 생성하고 Execution만 막는 정책은 "관찰은 방해하지 않고
  부작용만 막는다"는 이 프로젝트의 기존 Gate 철학(`ExecutionGate`,
  M36)과 정확히 같은 원칙이다.
- 결과/영향: `guardian/models.py`(`GUARDIAN_BLOCK_REASON_PREFIX`
  상수 추가), `runtime/execution/recommendation_execution_gate.py`
  (`guardian_report` 선택적 파라미터), `runtime/execution/
  recommendation_execution_service.py`(`execute()`/`publish()`에
  `guardian_report` 전달), `runtime/execution/
  recommendation_orchestration_service.py`(`guardian_service` 선택적
  주입), `observability/snapshot.py`(`AutomationGateStatus` Enum
  신규, `GuardianRuntimeInfo`에 필드 2개 추가), `observability/
  guardian_runtime_analyzer.py`(Execution 리포트 직접 읽기),
  `observability/statusline_renderer.py`(Automation Gate 상태
  표시), `web/server.py`(`ArchitectureGuardianService` 조립·주입).
  새 Core Domain Interface/Adapter/Service/Layer/File 없음(27종
  유지, 기존 6개 파일의 선택적 의존성 확장만). `pytest` 1122개
  (14개 신규, 회귀 없음)/`ruff`/`mypy`(220 source files)/
  `guardian.checker.evaluate()` all_passed 전부 통과. `.ai/TASKS.md`
  Milestone 48 절(T01~T03) 신규 추가. Learning Engine은 M49 이후로
  명시적으로 분리.

## ADR-0066: Learning Engine 착수 — RecommendationAdjustmentAnalyzer에 최소 표본 조건 추가 (Milestone 49)

- 상태: 승인됨 (2026-08-01, 사용자가 T01 Domain Analysis에서 학습
  대상을 "Recommendation/Adaptation만"으로, 영속 저장소·Guardian
  다건 이력을 이번 Scope에서 명시적으로 배제하는 데 동의. T02 MDD
  Review에서 실패율 임계값 100%/최소 표본 3회로 최종 승인)
- 날짜: 2026-08-01
- 배경: ADR-0065(M48)가 "Learning Engine은 M49 이후 별도 제안·승인
  대상"으로 명시적으로 분리했다. M49 T01 Domain Analysis(코드 전수
  조사)는 다음을 확인했다: `ExperienceStat`(M40)이 task_id별
  성공/실패 누적 카운트를 이미 제공하고, `RecommendationAdjustment
  Analyzer`(M42)가 "성공 0건 + 실패 1건 이상"이면 추천을 보류하는
  이진 규칙 1개만 갖고 있다는 것 — 즉 실패 1건만으로도 즉시 보류되어
  표본이 부족한 상태에서 성급하게 판단을 바꾸는 한계가 있었다. Guardian
  다건 이력(ADR-0065가 `ExecutionMemoryStore`에 기록하지 않기로 결정한
  부분)과 영속 저장소(`InMemoryMemoryEngine`이 프로세스 재시작 시
  소멸)는 이번에 함께 해결하지 않기로 사용자가 결정했다.
- 결정:
  1. **학습 대상 — Recommendation/Adaptation 규칙 정교화만**: Guardian
     정책·영속화는 다루지 않는다(각각 별도 Milestone 대상으로 배제).
  2. **규칙 — "실패율 100% AND 표본 3건 이상"**: 기존 규칙
     (`success_count == 0 and failure_count > 0`, 즉 표본 1건부터
     보류)을 `success_count == 0 and total >= 3`으로 교체 — 최소
     표본 조건만 1 → 3으로 강화한 상위 집합이라 회귀 없음.
  3. **새 Domain/Service/Interface 없음**: `RecommendationAdjustment
     Analyzer.analyze()` 내부 조건식 1건만 교체, 시그니처·반환 타입
     불변. `§13.4` 금지 어휘(Learning/Insight)를 실제로 쓸 새 1급
     개념은 이번 Scope에 없다 — Milestone 제목은 M48 승인 시 확정된
     "Learning Engine"을 유지하되, 산출물은 기존 Analyzer의 내부
     로직 교체임을 명시한다.
  4. **영속화·Guardian 이력 축적 — 이번엔 하지 않음**: `Execution
     MemoryStore`가 여전히 in-process 저장소이므로, 이번 학습은
     "서버 1회 구동 세션 내"로 자연히 한정된다. 이 한계를 해소하는
     것은 향후 별도 Milestone 대상이다.
- 대안:
  1. 단순 실패율만 사용(최소 표본 조건 없음) — 기각: 실패 1건(실패율
     100%)도 즉시 보류돼 기존 규칙보다 더 공격적으로 동작하는 회귀가
     생긴다.
  2. Guardian 위반 다건 이력을 이번에 함께 쌓기 시작 — 기각: 사용자가
     T01에서 명시적으로 배제(ExecutionMemoryStore 성공/실패만으로
     1차 범위 한정).
  3. 영속 저장소(파일/DB)를 이번에 함께 도입 — 기각: 사용자가 T01에서
     명시적으로 배제(이번엔 in-process 범위로 한정, YAGNI).
  4. 실패율 임계값을 100% 미만(예: 80%)으로 완화 — 기각: 사용자가
     T02에서 100%(기존 조건과 동일한 엄격도) + 표본 3회를 선택.
  5. 가중치·점수화 체계 신규 도입 — 기각: M42 설계 시점부터
     Non-goal로 명시돼 있고, 이번에도 새 데이터 없이 기존
     `ExperienceStat` 필드만으로 해결 가능해 불필요.
- 이유: 프로젝트가 이미 두 번(M40 Experience Intelligence, M42
  Adaptation) "Learning Engine"이라는 무거운 이름을 스스로 피해온
  이력과 일관되게, M49도 실제로 필요한 만큼만 — 기존 이진 규칙의
  한 가지 약점(표본 부족)만 — 최소로 고친다. 새 Domain 개념을
  만들지 않고 기존 파일 하나만 수정하는 것이 Reuse-First/YAGNI에
  가장 부합한다.
- 결과/영향: `intelligence/recommendation_adjustment.py`
  (`_MIN_SAMPLE_SIZE_FOR_WITHHOLD` 상수 추가, 조건식 교체)만 수정.
  새 Core Domain Interface/Adapter/Service/Layer/File 없음(기존 파일
  1개 수정). `tests/intelligence/test_recommendation_adjustment.py`
  (신규 케이스 1건 추가, 기존 케이스 표본 수 조정),
  `tests/intelligence/test_recommendation_service.py`,
  `tests/runtime/execution/test_recommendation_orchestration_service.py`
  (표본 수를 3건으로 조정, 회귀 아님). `pytest` 1123개(신규 1개,
  회귀 없음)/`ruff`/`mypy`(220 source files) 전부 통과. `.ai/
  TASKS.md` Milestone 49 절(T01~T03) 신규 추가. Guardian 다건 이력
  축적·영속 저장소 도입은 향후 별도 Milestone 대상으로 명시적으로
  분리.

## ADR-0067: Learning Persistence — FileMemoryEngine으로 ExecutionMemoryStore 영속화 (Milestone 50)

- 상태: 승인됨 (2026-08-01, 사용자가 T01에서 저장 위치를 "vault_root
  하위 전용 디렉터리"로, T02에서 단일 JSON 파일 설계를 승인)
- 날짜: 2026-08-01
- 배경: ADR-0066(M49)이 "`ExecutionMemoryStore`가 여전히 in-process
  저장소이므로 이번 학습은 서버 1회 구동 세션 내로 한정된다"고 명시,
  해소를 향후 별도 Milestone 대상으로 남겼다. M50 T01 Domain
  Analysis(코드 전수 조사)는 다음을 확인했다: `MemoryEngine`
  Interface(remember/recall/search)는 이미 존재하고 구현체는
  `InMemoryMemoryEngine` 하나뿐이며, 사용처는 `web/server.py`의
  `ExecutionMemoryStore(InMemoryMemoryEngine())` 단 한 곳뿐이다.
  `storage/`에는 이미 `FileAgentRepository`/`FileProjectRepository`/
  `FileKnowledgeRepository`로 확립된 File 기반 영속화 패턴(JSON
  직렬화, `base_dir` 생성자 주입)이 존재한다.
- 결정:
  1. **`FileMemoryEngine` 신설(`storage/file_memory_engine.py`)**:
     기존 `MemoryEngine(ABC)`을 구현. 새 Interface/Service 없음.
  2. **저장 형식 — 단일 JSON 파일**: entry당 파일이 아니라
     `{key: value}` dict 전체를 파일 하나에 담는다 —
     `MemoryEngine.search("")`로 전체 키를 얻는 `ExecutionMemory
     Store`의 현재 사용 패턴에 가장 자연스럽게 맞기 때문.
  3. **저장 위치 — `<vault_root>/.ai-workspace-data/`**:
     `ProductionConfig`에 새 필드를 추가하지 않고 기존 `vault_root`
     만으로 경로를 계산한다. Vault(문서 저장소)와는 분리된 런타임
     상태 디렉터리이며 `.gitignore`에 추가한다.
  4. **적용 범위 — `web/server.py` Composition Root 1곳만**:
     `execution_memory_store = ExecutionMemoryStore(InMemoryMemory
     Engine())`를 `FileMemoryEngine(...)`로 교체. 테스트 픽스처·
     `InMemoryContextManager` 등 다른 `InMemoryMemoryEngine` 사용처는
     그대로 유지(영향 범위 밖).
  5. **Observability 배선은 이번 Scope 밖**: `pipeline_stage_
     analyzer.py`(M45)의 Memory 단계는 여전히 `NOT_OBSERVABLE`로
     남는다 — 이제 영속화는 되지만 StatusLine이 별도 프로세스에서
     이 파일을 읽는 배선이 아직 없기 때문(note 텍스트만 정확하게
     갱신, 로직 변경 없음).
- 대안:
  1. `ProductionConfig`에 `data_dir` 필드 신규 추가 — 기각: 사용자가
     T01에서 "vault_root 하위 전용 디렉터리"를 선택.
  2. `FileAgentRepository`처럼 key당 파일 — 기각: entry 수가 늘어날
     수록 파일 수가 무한정 증가하고 `search("")` 시 디렉터리 전체를
     스캔해야 해 단일 JSON dict보다 복잡도가 높음.
  3. SQLite 등 별도 저장 엔진 도입 — 기각: 현재 규모(단일 프로세스,
     in-process 대체 목적)에 과함(YAGNI).
  4. StatusLine 읽기 배선까지 이번에 함께 구현 — 기각: T02 Scope를
     "영속화"로만 한정, Observability 연동은 별도 판단 필요.
- 이유: `MemoryEngine` Interface와 `storage/`의 File 구현 패턴이
  이미 존재하므로, 새 추상화 없이 기존 계약을 구현하는 Adapter
  하나만 추가하는 것이 Reuse-First/YAGNI에 가장 부합한다. 영향
  범위가 Composition Root 1곳으로 명확히 한정되어 회귀 위험이 낮다.
- 결과/영향: `storage/file_memory_engine.py`(신규),
  `web/server.py`(`InMemoryMemoryEngine()` → `FileMemoryEngine(...)`
  1곳 교체 + docstring 갱신), `observability/pipeline_stage_
  analyzer.py`(note 텍스트만 갱신), `.gitignore`(`.ai-workspace-data/`
  추가). 새 Core Domain Interface/Service 없음.
  `tests/storage/test_file_memory_engine.py`(신규 7건) 추가. `pytest`
  1130개(신규 7개, 회귀 없음)/`ruff`/`mypy`(221 source files) 전부
  통과. `.ai/TASKS.md` Milestone 50 절(T01~T03) 신규 추가.
  StatusLine Observability 배선은 향후 별도 Milestone 대상으로
  명시적으로 분리.

## ADR-0068: Learning Evolution — 최근 연속 실패 추세 규칙을 Adaptation에 보완 추가 (Milestone 51)

- 상태: 승인됨 (2026-08-01, 사용자가 T01에서 "보완(두 규칙 병존)" +
  "최근 N건 슬라이딩 윈도우"를, T02에서 N=5를 선택. T02 승인 시
  `recent_failure_streak` 정의 명문화 및 Explainability 규칙 구분
  기록을 조건으로 추가 요청 — 둘 다 T03에 반영)
- 날짜: 2026-08-01
- 배경: M49/M50(ADR-0066/0067)이 만든 "실패율 100% + 표본 3건 이상"
  규칙은 **전체 이력**만 본다 — task가 과거에 여러 번 성공했더라도
  최근 들어 계속 실패하는 추세 악화를 포착하지 못한다.
  `RecommendationAdjustmentAnalyzer` 독스트링이 이미 "우선순위
  재설계·점수화·가중치 학습은 하지 않는다(Non-goal)"고 명시해 뒀는데,
  이번 Milestone은 이 Non-goal을 최소한으로("추세" 신호 1개) 해제한다.
  T01 조사로 `ExperienceRecord.timestamp`가 이미 정렬 가능한 원재료로
  존재해 새 저장소·새 수집 로직이 불필요함을 확인.
- 결정:
  1. **`ExperienceStat.recent_failure_streak: int` 신규 필드**: 시간순
     정렬된 기록을 가장 최근 것부터 거슬러 올라가며 센 연속 실패
     횟수(성공을 만나면 중단, 최근 기록이 성공이면 0). 특정 윈도우
     크기에 종속되지 않는 범용 신호 — `recent_failure_streak >= N`은
     "최근 N건이 모두 실패"와 동치.
  2. **보류 규칙 — M49/M50과 M51 병존(OR)**: `(success_count == 0 and
     total >= 3) or recent_failure_streak >= 5`. 기존 규칙은 전혀
     수정하지 않는다(대체 아님, 회귀 없음). 윈도우 크기 N=5(사용자
     승인, 오탐 감소를 위해 보수적으로 선택).
  3. **Explainability 규칙 구분 기록(사용자 추가 요청)**: `reason`
     텍스트에 어느 규칙이 발동했는지 "(M49 규칙)"/"(M51 규칙, 과거
     성공 이력 있음)"/"(M49+M51 규칙)"로 명시 태깅. 새 필드나
     `RecommendationAdjustment`/`RecommendationExplanationService`
     시그니처 변경 없이, 기존 prose 기반 reason 채널을 그대로
     재사용해 만족(M44 Explainability 원칙 — "새 판단 없음"과 일관).
  4. **새 Domain/Service/Interface 없음**: `intelligence/
     experience_rules.py`, `intelligence/recommendation_adjustment.py`
     2개 파일만 수정. Analyzer 순수성(외부 상태·시각·난수 미참조)
     유지.
- 대안:
  1. 지수 Decay(exponential weighting) — 기각: 사용자가 슬라이딩
     윈도우를 선택(구현·설명이 더 단순, N=5로 충분히 표현 가능).
  2. 기존 M49/M50 규칙을 가중치 점수로 완전히 대체 — 기각: 사용자가
     "보완(두 규칙 병존)"을 선택해 회귀 위험을 피함.
  3. `recent_results: tuple[str, ...]`(최근 N건 원시 결과를 통째로
     저장) — 기각: `recent_failure_streak: int` 하나로 이번 Rule을
     표현하는 데 충분하고, 원시 리스트를 노출하면 향후 소비처가
     윈도우 크기를 각자 하드코딩할 위험이 있음(YAGNI).
  4. 규칙 구분 기록을 위해 `RecommendationAdjustment`에 새 필드(예:
     `triggered_rule: str`) 추가 — 기각: 기존 prose reason 채널로
     충분히 표현 가능하고, Explainability가 이미 `reason`을 그대로
     노출하는 구조라 새 필드는 불필요한 표면적 확장(YAGNI).
- 이유: `ExperienceRecord.timestamp`라는 이미 존재하는 원재료만으로
  "추세"라는 새로운 신호 축을 최소 형태(정수 1개)로 추가하고, 기존
  규칙을 건드리지 않는 순수 보완이라 회귀 위험이 가장 낮다.
  Reuse-First로 향후 M52(가중치)·M53(Decay) 확장에도 같은 패턴(필드
  추가 + OR 조건 추가)을 그대로 반복할 수 있는 구조를 남긴다.
- 결과/영향: `intelligence/experience_rules.py`(`recent_failure_streak`
  필드 + 헬퍼 함수 추가), `intelligence/recommendation_adjustment.py`
  (`_RECENT_FAILURE_STREAK_THRESHOLD` 상수, OR 조건, reason 태깅
  헬퍼 추가)만 수정. 새 Core Domain Interface/Adapter/Service/Layer/
  File 없음. `tests/intelligence/test_experience_rules.py`(신규 3건),
  `tests/intelligence/test_recommendation_adjustment.py`(신규 4건)
  추가. `pytest` 1137개(신규 7개, 회귀 없음)/`ruff`/`mypy`(221 source
  files) 전부 통과. `.ai/TASKS.md` Milestone 51 절(T01~T03) 신규
  추가.

## ADR-0069: StatusLine Integration Fix — import 순서를 바로잡아 조용한 크래시를 제거 (M45-1)

- 상태: 승인됨 (2026-08-01, 사용자가 "M45 구현은 완료됐지만 Claude
  Code UI에서 StatusLine이 표시되지 않는다"는 문제와 함께 추측 대신
  실제 환경 검증을 전제 조건으로 조사를 요청)
- 날짜: 2026-08-01
- 배경: M45(ADR-0062)로 StatusLine 진입점(`statusline_main.py`)이
  구현되고 `pytest`/`ruff`/`mypy`는 모두 통과했지만, 실제 Claude
  Code UI에서는 한 줄도 표시되지 않는다는 사용자 보고가 있었다.
  구현을 추측으로 고치기 전에 공식 문서(`code.claude.com/docs/en/
  statusline`)를 직접 조회해 StatusLine stdin JSON 스키마와 설정
  형식, 공식 Troubleshooting 절을 확인했다.
- 조사 결과(공식 문서 확인, 이번 세션에서 실행한 검증):
  1. `.claude/settings.json`의 `{"statusLine": {"type": "command",
     "command": "..."}}` 형식은 공식 문서 예시와 동일 — 설정 형식
     자체는 문제 없음.
  2. `ClaudeRuntimeAnalyzer`가 읽는 `model.display_name`/
     `effort.level`/`context_window.*` 필드는 모두 공식 문서에 실제
     문서화된 필드다(추측이 아님) — 공식 Mock Input 예시로 실행해
     정상 동작을 확인했다.
  3. **실제 버그 발견**: `statusline_main.py`의 `ai_workspace.*`
     import 3개가 `try/except` **바깥**(모듈 최상단)에 있었다.
     import 자체가 실패하면(예: `PYTHONPATH` 미설정, 의존성이 없는
     `python3` 사용) 어떤 출력도 없이 프로세스가 죽는다 — 공식
     문서의 "Status line not appearing" Troubleshooting 절이 말하는
     "스크립트가 아무 출력도 내지 않으면 StatusLine이 빈 줄로
     사라진다"는 실패 모드와 정확히 일치한다.
  4. 공식 문서는 그 외에도 **Workspace Trust 미승인**(폴더에 대한
     신뢰 대화상자를 수락하지 않으면 StatusLine이 아예 실행되지
     않고 `claude --debug`가 "Status line command skipped:
     workspace trust not accepted"를 로그로 남김)을 별도
     Troubleshooting 항목으로 명시한다 — 이는 코드가 아니라 사용자
     환경의 설정 상태이므로 이번 Milestone에서 코드로 고칠 수 없고,
     사용자가 직접 `claude --debug`로 확인해야 한다(추측 금지
     원칙에 따라 코드 수정 대상에서 제외).
- 결정:
  1. `ai_workspace.*` import를 `main()` 내부 `try` 블록 안으로
     이동해, import 실패를 포함한 모든 예외가 항상 사람이 읽을 수
     있는 한 줄로 대체된다(공식 문서 권고와 완전히 일치하도록
     수정).
  2. 디버그 로그(`/tmp/statusline.log`)는 실패했을 때만 남긴다
     (정상 동작 시 로그 없음 — 사용자 요청 원칙). 실제 Runtime
     JSON Schema를 검증하고 싶을 때는 `AI_WORKSPACE_STATUSLINE_
     DEBUG=1` 환경 변수로 원본 stdin을 강제로 기록할 수 있게 했다
     (추측 대신 실제 payload로 검증하기 위한 opt-in 수단).
  3. 새 Domain/Interface/Service를 추가하지 않는다 — 기존
     `observability/statusline_main.py` 1개 파일의 제어 흐름만
     수정한다(YAGNI, Reuse-First).
- 대안:
  1. `.claude/settings.json`의 `command`를 `poetry run python -m ...`
     로 바꿔 의존성 환경을 강제 — 기각: 이번 세션에서 실제로
     재현해보니 현재 의존성(`pyyaml`/`fastapi`/`uvicorn`)은
     StatusLine 경로에서 전혀 import되지 않아(순수 stdlib만 사용)
     `python3` 단독 실행이 이미 정상 동작했다 — 근거 없는 변경을
     피했다(추측 금지 원칙).
  2. Workspace Trust 문제를 코드로 우회 — 기각: 공식 문서상 Trust
     승인은 셸 명령을 실행하는 모든 설정(hooks 포함)에 적용되는
     보안 경계이며 코드로 우회할 수 없다. 사용자가 직접 Trust
     대화상자를 수락해야 한다.
- 이유: 코드·테스트 통과만으로는 "빈 줄로 사라짐" 실패 모드를 잡을
  수 없다는 것이 이번 조사의 핵심 확인 사항이다 — import를 try 안
  으로 옮기는 것은 공식 문서가 명시한 실패 모드를 코드 레벨에서
  구조적으로 차단하는 가장 낮은 위험의 수정이다.
- 결과/영향: `observability/statusline_main.py` 수정(import 이동,
  실패 시에만 기록하는 디버그 로그 추가). `tests/observability/
  test_statusline_main.py`(신규 6건: 정상/JSON 파싱 실패/빈 stdin
  각각 크래시 없이 한 줄 출력 보장, 디버그 로그는 실패 시에만 기록,
  `AI_WORKSPACE_STATUSLINE_DEBUG=1`로 강제 기록). `pytest` 1143개
  (신규 6개, 회귀 없음)/`ruff`/`mypy`(221 source files) 전부 통과.
  **DoD 미충족 항목(사용자 확인 필요)**: 이 세션은 헤드리스 원격
  자동화 환경이라 실제 Claude Code 데스크톱/터미널 UI에 접근할 수
  없다 — "UI에서 실제로 표시되는 스크린샷 또는 실행 결과" 검증은
  사용자가 실제 Claude Code 세션에서 `claude --debug`로 직접
  확인해야 완료된다(특히 Workspace Trust 승인 여부).
- 후속(2026-08-01) — 환경 지원 여부 실증: 사용자가 "구현을 바꾸기
  전에 이 실행 환경 자체가 StatusLine을 지원하는지부터 실증하라"고
  재요청해, 이 세션의 실제 프로세스 상태를 직접 조회했다.
  `sys.stdin.isatty()`/`sys.stdout.isatty()` 모두 `False`, `tty`
  명령도 `not a tty`, `CLAUDE_CODE_ENTRYPOINT=remote_mobile`/
  `CLAUDE_CODE_REMOTE=true`, 그리고 `ps aux`로 확인한 실제 `claude`
  프로세스가 `--output-format=stream-json --input-format=stream-json`
  (비대화형 print 모드)로 구동 중임을 확인했다. `/tmp/statusline.log`
  가 세션 내내 한 번도 생성되지 않아(수동 테스트 제외)
  `statusline_main.py`가 이 세션에서 한 번도 호출되지 않았음도
  확인했다. **결론(실증)**: 이 세션(Claude Code Remote —
  `remote_mobile`, 비대화형 stream-json 모드)은 대화형 터미널 UI
  자체가 없어 StatusLine을 아키텍처상 지원하지 않는다 — 코드
  결함이 아니다. 앞서 고친 import 안전성 버그는 사용자의 로컬
  대화형 터미널 사용 환경에는 여전히 유효·필요하지만, 그 환경에서
  실제로 표시되는지는 이 세션이 자체 검증할 수 없어 최종 확인은
  사용자 몫으로 남는다.

## ADR-0070: Learning Weighting — M49/M51 두 신호를 고정 가중치 점수로 결합 (Milestone 52)

- 상태: 승인됨 (2026-08-01, 사용자가 M51 승인 코멘트에서 예고한
  "M52(가중치)" 방향을 확정 요청 — 두 차례 AskUserQuestion으로
  범위(두 신호를 가중치 점수로 결합, 가중치는 고정 상수로 데이터
  학습 아님)와 파라미터(가중치 0.6/0.6, threshold 0.6)를 직접 확정)
- 날짜: 2026-08-01
- 배경: M49(전체 실패율 100%+표본 3건 이상)/M51(최근 연속 실패
  5회 이상) 두 Rule은 지금까지 OR로만 결합돼, 각 Rule의 임계값
  미만이지만 "합쳐 보면 위험한" 조합(예: 실패율 60%+최근 3회 연속
  실패)을 포착하지 못하는 한계가 있었다. `recommendation_
  adjustment.py`의 클래스 docstring에는 M51 시점에 "우선순위
  재설계나 임의의 점수화·가중치 학습은 하지 않는다(Non-goal)"가
  명시돼 있어, 이번 확장은 그 Non-goal을 명시적으로 좁혀야 했다
  (사용자 승인 필요 사항으로 별도 확인).
- 결정:
  1. **Domain Analysis(T01)**: 이 확장도 새 Domain/Behavioral
     Concept가 아니라 기존 `Adaptation`(§13.3)의 연장이다. 새
     Interface/Service 없이 `recommendation_adjustment.py` 1개
     파일만 수정.
  2. **Architecture Review(T02) — 설계**: `ExperienceStat` 필드만
     으로 두 연속값 신호를 계산한다.
     - `signal_overall = failure_count / total`(단, `total <
       _MIN_SAMPLE_SIZE_FOR_WITHHOLD`이면 0 — 기존 최소 표본 조건
       유지)
     - `signal_recent = min(recent_failure_streak /
       _RECENT_FAILURE_STREAK_THRESHOLD, 1.0)`
     - `score = 0.6 * signal_overall + 0.6 * signal_recent`,
       `score >= 0.6`이면 보류
     - 사용자가 처음 제안한 "가중치 0.5/0.5 + threshold 0.6"은
       신호 하나가 완전히 1.0이어도 `score=0.5<0.6`이 되어 기존
       M49/M51 단일 규칙이 더 이상 트리거되지 않는 실제 회귀를
       만든다는 것을 수학적으로 짚어 보고했고, 사용자가 가중치를
       0.6/0.6으로 올려 이 문제를 해결하도록 확정(각 가중치가
       threshold와 같아, 신호 하나가 1.0이면 그 신호만으로 이미
       `score=0.6>=0.6`이 성립 — 기존 두 Rule이 정확히 보존됨을
       경계값으로 증명).
  3. **Detailed Design(T03)**: `_withhold_score()` 헬퍼로 점수를
     계산. Explainability 태깅은 기존 M49/M51 요구(어느 규칙이
     발동했는지 구분)를 그대로 유지하되, 개별 규칙(M49/M51 boolean)
     으로는 안 걸리고 오직 가중치 결합으로만 걸린 새 케이스에
     "(M52 가중치 결합 규칙)" 태그를 추가.
  4. **Implementation**: `recommendation_adjustment.py` 1개 파일만
     수정(상수 3개 추가, `analyze()`를 boolean OR에서 score 비교로
     교체, `_withhold_score()` 신규, `_build_withhold_reason()`에
     M52 분기 추가). 클래스/모듈 docstring의 Non-goal을 "가중치·
     threshold는 고정 상수이며 데이터로부터 학습되지 않는다(온라인
     학습 없음)"로 좁혀 실제로 하는 일과 안 하는 일을 명확히 구분.
- 대안:
  1. 가중치 0.5/0.5 + threshold 0.6 — 기각(회귀 발생, 위 T02 참고).
  2. task_id별 가중치/임계값 차등화 — 기각: 사용자가 "두 신호를
     가중치 점수로 결합"을 선택, task_id별 차등은 범위 밖(향후
     별도 요청 시 검토).
  3. 신호를 boolean 그대로 두고 가중합 — 기각: boolean×가중치는
     결과적으로 기존 OR와 동일해 "가중치"가 무의미해짐 — 신호를
     연속값(실패율/streak 비율)으로 바꿔야 결합이 실질적 의미를
     가짐.
- 이유: 기존 `ExperienceStat` 필드만으로 계산 가능해 새 저장소·
  수집 로직이 필요 없고, 가중치를 개별 신호의 완전 포화값과 같은
  값(0.6)으로 설정해 "기존 규칙 무변경"이라는 M49/M51 계약을 수학적
  경계값 증명으로 지키면서 새 조합 포착 능력만 순수 추가했다.
- 결과/영향: `intelligence/recommendation_adjustment.py` 1개 파일만
  수정. 새 Core Domain Interface/Adapter/Service/Layer/File 없음.
  `tests/intelligence/test_recommendation_adjustment.py`(기존 1건
  수정, 신규 2건 추가 — 조합 트리거, 경계값 회귀 없음 증명).
  `pytest` 1145개(회귀 없음)/`ruff`/`mypy`(221 source files) 전부
  통과. `.ai/TASKS.md` Milestone 52 절(T01~T03) 신규 추가.

## ADR-0071: Learning Decay — signal_overall을 지수 Decay 가중 실패율로 교체 (Milestone 53)

- 상태: 승인됨 (2026-08-01, 사용자가 M51 승인 코멘트에서 예고한
  "M53(Decay)" 착수 요청 — 두 차례 AskUserQuestion으로 적용 대상
  (signal_overall 교체)과 Decay 함수(지수, decay_factor=0.8)를
  직접 확정)
- 날짜: 2026-08-01
- 배경: M52까지 `signal_overall`은 `failure_count / total`(단순
  평균)이었다 — 모든 기록을 동등하게 반영해, "예전엔 실패했지만
  최근엔 성공 중"인 task와 "예전엔 성공했지만 최근 실패가 잦은"
  task를 구분하지 못했다. M51(ADR-0068) 설계 당시 검토했던 지수
  Decay는 그때는 "추천 보류 트리거 자체"에 쓰기엔 슬라이딩 윈도우
  (N=5)보다 복잡하다고 판단해 기각됐지만(대안 1), 이번엔 별도
  Milestone(M53)으로 그 아이디어를 `signal_overall` 계산 방식
  자체에 적용한다 — 트리거 로직(M52의 가중 결합)은 그대로 두고,
  "전체 실패율"이라는 개념 자체를 더 정교하게 만드는 것이라 M51의
  기각 사유와 충돌하지 않는다.
- 결정:
  1. **Domain Analysis(T01)**: 새 Domain/Behavioral Concept 아님 —
     기존 `Adaptation`의 신호 계산 정교화. `ExperienceStat`(M40/M51
     패턴 재사용)에 필드만 추가.
  2. **Architecture Review(T02) — 설계**: `ExperienceStat`에
     `decayed_failure_rate: float` 필드 신설. `experience_rules.py`
     의 `_summarize()`에서 계산(레코드 원본 접근 가능한 유일한
     지점 — `recommendation_adjustment.py`는 집계값만 받으므로 여기
     서만 계산 가능):
     - `weight(rank) = _DECAY_FACTOR ** rank`(`rank=0`이 가장 최근
       기록, `_DECAY_FACTOR = 0.8`)
     - `decayed_failure_rate = Σ(weight × 실패 여부) / Σ(weight)`
     `recommendation_adjustment.py`의 `signal_overall`을
     `stat.decayed_failure_rate`로 교체(단, `total < 3`이면 0 —
     기존 최소 표본 게이트 유지). 전체 이력이 100% 실패면 분자=분모
     라 `decayed_failure_rate`는 가중치와 무관하게 항상 정확히
     1.0 — M49 단일 규칙, M52의 "신호 1.0 → score=0.6" 체인이
     그대로 보존됨(회귀 없음, 수학적으로 보장).
  3. **Detailed Design(T03) — 테스트 인프라 함의 발견**: 구현 중
     `ExperienceStat`을 수동 생성하는 기존 테스트(`test_recommendation_
     adjustment.py`/`test_recommendation_service.py`)가 새 필드의
     기본값(`0.0`)을 그대로 둔 채 "전체 실패" 시나리오를 표현하고
     있었다는 것을 테스트 실행으로 발견 — `decayed_failure_rate`는
     `failure_count`/`total`에서 자동으로 계산되지 않는 독립 필드라,
     수동 생성 시 시나리오에 맞는 값을 직접 지정해야 한다(M51의
     `recent_failure_streak`와 동일한 성격의 함의였지만 이번엔 M49
     단일 규칙의 트리거 여부에 직접 영향을 줘 테스트가 실패로
     드러났다). 영향받은 5개 테스트에 `decayed_failure_rate` 명시
     지정으로 수정.
  4. **Implementation**: `experience_rules.py`(`_DECAY_FACTOR` 상수,
     `_compute_decayed_failure_rate()` 헬퍼, `ExperienceStat.
     decayed_failure_rate` 필드), `recommendation_adjustment.py`
     (`signal_overall` 교체, Non-goal 문구에 Decay 계수도 고정
     상수임을 명시).
- 대안:
  1. Decay를 `recommendation_adjustment.py`에서 raw record로부터
     직접 계산 — 기각: 이 모듈은 `ExperienceStat` 집계값만 받고
     raw record에 접근하지 않는다(Analyzer 계층 분리 유지, Reuse-
     First로 M51과 동일한 계산 위치 패턴 재사용).
  2. Decay를 새 3번째 신호로 추가(기존 두 신호는 그대로 유지) —
     기각: 사용자가 "signal_overall을 교체"를 선택. 신호 개수가
     늘면 가중치 재조정이 필요해 M52의 회귀 없음 증명이 깨질
     위험이 있어, 교체가 더 단순하고 안전.
  3. 선형 Decay — 기각: 사용자가 지수 Decay를 선택.
  4. decay_factor 0.9(완만)/0.7(공격적) — 기각: 사용자가 0.8(중간)
     선택.
- 이유: `signal_overall`이라는 기존 개념의 정의만 정교화하고
  트리거 로직(M52)은 전혀 건드리지 않아 변경 범위가 최소화된다.
  "전체 이력 100% 실패 → 항상 1.0"이라는 불변식이 Decay 가중치
  선택과 무관하게 항상 성립해, M49/M52까지 쌓아온 회귀 없음 증명
  체인이 그대로 이어진다.
- 결과/영향: `intelligence/experience_rules.py`(필드 1개 + 헬퍼
  함수 1개 추가), `intelligence/recommendation_adjustment.py`
  (`signal_overall` 계산식 교체, docstring 갱신) 2개 파일 수정.
  새 Core Domain Interface/Adapter/Service/Layer/File 없음.
  `tests/intelligence/test_experience_rules.py`(신규 4건 — 전체
  실패/전체 성공/최근 실패 가중 우대/입력 순서 무관), 기존 5개
  테스트를 `decayed_failure_rate` 명시 지정으로 수정. `pytest`
  1149개(신규 4개, 회귀 없음)/`ruff`/`mypy`(221 source files) 전부
  통과. `.ai/TASKS.md` Milestone 53 절(T01~T03) 신규 추가.

## ADR-0072: Learning Insight — M39~M53 학습 신호를 StatusLine에 노출 (Milestone 54)

- 상태: 승인됨 (2026-08-01, 사용자가 "M54 Learning Insight" 착수
  요청 — 로드맵에 사전 예고 없던 이름이라 두 차례 AskUserQuestion
  으로 범위(학습 신호를 사람이 볼 수 있게 노출)와 경로(StatusLine에
  줄 추가)를 확정, T02 설계도 별도 승인)
- 날짜: 2026-08-01
- 배경: M49~M53으로 쌓인 학습 신호(`decayed_failure_rate`/
  `recent_failure_streak`/가중치 결합 score)는 지금까지
  `RecommendationAdjustmentAnalyzer`(Adaptation)의 보류 판단에만
  내부적으로 쓰였고, 사람이 직접 조회할 수 있는 형태로는 전혀
  노출되지 않았다. T01 조사 중 `observability/snapshot.py`의
  `WorkspaceInfo.current_task`가 "Phase 1 범위 밖, 항상 `None`"으로
  이미 명시돼 있음을 확인 — StatusLine은 별도 프로세스라 "지금 어떤
  task가 추천 대상인지"는 알 수 없다(ADR-0063에서 이미 확정된 한계,
  이번 Milestone에서도 해소하지 않음). 대신 M50(ADR-0067)이
  `<vault_root>/.ai-workspace-data/`에 영속화해 둔 실행 이력
  전체를 읽어, "현재 추천 대상"이 아니라 "추적 중인 모든 task 중
  가장 위험한 것"을 보여주는 방향으로 범위를 좁혔다 — 이는 M45/M50
  에서 이미 "별도 Milestone 대상"으로 명시적으로 남겨뒀던 Pipeline
  Stage "Memory" 단계의 `NOT_OBSERVABLE` 상태를 해소하는 것과
  동일한 배선이라, 부수적으로 그 gap도 함께 닫힌다.
- 결정:
  1. **Domain Analysis(T01)**: 새 Domain/Behavioral Concept 아님 —
     기존 `Observability`(§13.3, M45)의 확장. `current_task` Phase 1
     한계는 그대로 유지(추정 금지 원칙 — 알 수 없는 것을 알아낸
     척하지 않는다).
  2. **Architecture Review(T02) — 설계**: 새 `LearningRuntimeAnalyzer`
     (observability/)가 `FileMemoryEngine`(M50)+`ExecutionMemoryStore`
     (M39)+`ExperienceIntelligenceService`(M40)를 그대로 조합해
     `ExperienceReport`를 얻는다 — 새 Domain/Interface/Service
     없음, 기존 컴포넌트 재사용만. `LearningRuntimeInfo`(값 객체):
     `tracked_task_count`, `highest_risk_task_id`/
     `decayed_failure_rate`/`recent_failure_streak`(모든 task_id 중
     `decayed_failure_rate` 최댓값, 동점이면 `task_id` 오름차순 —
     새 채점이 아니라 이미 계산된 값 중 최대를 고르는 표시 로직).
     `PipelineStageAnalyzer.analyze()`에 `has_learning_records: bool`
     키워드 인자를 추가해 Memory 단계를 `NOT_OBSERVABLE`에서
     `OBSERVED_DONE`/`OBSERVED_NOT_YET`으로 승격(계산 위치 중복을
     피하려고 `LearningRuntimeAnalyzer`가 이미 낸 결과만 전달받음).
  3. **Detailed Design(T03)**: `RuntimeSnapshotService`에
     `LearningRuntimeAnalyzer` 8번째로 추가, `StatusLineRenderer`에
     "Learning" 줄 렌더링 추가. 실제 `FileMemoryEngine` 데이터로
     end-to-end 수동 실행해 Memory 단계가 실제로 `✓`로 바뀌고
     Learning 줄이 실제 위험 task를 정확히 보여줌을 확인.
- 대안:
  1. "현재 추천 대상"의 학습 신호를 보여주기 — 기각: `current_task`
     Phase 1 한계상 StatusLine이 알 방법이 없음(ADR-0063). 알 수
     없는 것을 추정하지 않는다는 원칙을 지키기 위해 "추적 중인
     전체 중 최고 위험"으로 범위를 좁힘.
  2. Explainability(M44) reason 텍스트를 확장 — 기각: 사용자가
     StatusLine 경로를 선택. 이미 보류된 케이스에만 보이는 기존
     방식과 달리, 보류되지 않은 task도 포함해 상시 노출하는 것이
     "Insight"라는 목표에 더 맞음.
  3. Memory Pipeline Stage 승격을 별도 Milestone으로 미루기 —
     기각: 사용자가 T02에서 포함하기로 승인. 어차피 같은 배선
     (`FileMemoryEngine` 읽기)이라 별도로 미룰 이유가 없음.
- 이유: M39~M53까지 5개 Milestone에 걸쳐 쌓인 학습 인프라를 코드
  변경 없이(순수 조합) 사람이 볼 수 있게 만들면서, 동시에 M45/M50
  에서 두 번이나 "향후 별도 Milestone"으로 명시했던 부채를 정리했다.
- 결과/영향: `observability/snapshot.py`(`LearningRuntimeInfo` 추가,
  `WorkspaceRuntimeSnapshot`에 필드 추가), `observability/
  learning_runtime_analyzer.py`(신규), `observability/
  pipeline_stage_analyzer.py`(`has_learning_records` 파라미터 추가,
  Memory 단계 판정 로직 교체), `observability/runtime_snapshot_
  service.py`(8번째 Analyzer 배선), `observability/statusline_
  renderer.py`(Learning 줄 렌더링 추가) 5개 파일 수정 + 1개 신규.
  새 Core Domain Interface/Adapter/Service/Layer/File 없음(모두
  `observability/` 패키지 내부). `tests/observability/
  test_learning_runtime_analyzer.py`(신규 3건), 기존 `test_
  pipeline_stage_analyzer.py`/`test_statusline_renderer.py`/
  `test_runtime_snapshot_service.py`를 새 필드/파라미터에 맞춰
  수정. `pytest` 1155개(회귀 없음)/`ruff`/`mypy`(222 source files)
  전부 통과. 실제 `FileMemoryEngine` 데이터로 end-to-end 수동 검증
  완료. `.ai/TASKS.md` Milestone 54 절(T01~T03) 신규 추가.

## ADR-0073: Learning Explainability 고도화 — experience_summary에 학습 신호 상시 노출 (Milestone 55)

- 상태: 승인됨 (2026-08-01, 사용자가 "M55 Learning Explainability
  고도화" 착수 요청 — 로드맵에 사전 예고 없던 이름이라 AskUserQuestion
  으로 범위(experience_summary 확장) 확정, T02 설계도 별도 승인)
- 날짜: 2026-08-01
- 배경: M49~M53 학습 신호(`decayed_failure_rate`/`recent_failure_
  streak`/가중치 결합 score)는 M44 Explainability의 `experience_
  summary`에는 전혀 반영되지 않고, Adaptation이 **실제로 보류를
  발동했을 때만**(`adaptation_reason` 프로즈 문자열 안에) 보였다 —
  아직 보류되지 않았지만 값이 임계값에 가까운 "near-miss" 케이스는
  전혀 드러나지 않았다.
- 결정:
  1. **Domain Analysis(T01)**: 새 Domain/Behavioral Concept 아님 —
     기존 `Explainability`(§13.3, M44)의 확장.
  2. **Architecture Review(T02) — 설계**: `recommendation_
     adjustment.py`의 private `_withhold_score()`를 공개 함수
     `compute_learning_score(stat)`로 승격(가중치·threshold 공식을
     두 곳에 중복 구현하지 않기 위함), `WITHHOLD_SCORE_THRESHOLD`
     상수도 공개. `recommendation_explanation.py`의 `_build_
     experience_summary()`가 보류 여부와 무관하게 항상
     `decayed_failure_rate`/`recent_failure_streak`/
     `compute_learning_score()` 결과를 성공률과 함께 노출.
  3. **Implementation(T03)**: `experience_summary` 형식을
     `"성공률 X%(N건 중 M건 성공) · Decay실패율 R · 연속실패 S ·
     학습 Score V/T"`로 확장. Vault 발행(`recommendation_
     explanation_service.py`)은 문자열을 그대로 한 줄에 임베드할
     뿐이라 포맷 가정이 없어 별도 수정 불필요.
- 대안:
  1. `reason` 텍스트 자체를 구조화(새 필드 도입) — 기각: 사용자가
     `experience_summary` 확장을 선택. 기존 `adaptation_reason`
     프로즈 채널은 M49~M52에서 이미 확립된 태깅 방식을 그대로
     유지하고, 새 정보는 항상 채워지는 `experience_summary`에
     추가하는 것이 최소 변경.
  2. `compute_learning_score()`를 `recommendation_explanation.py`
     안에 재구현 — 기각: 가중치·threshold 공식이 두 파일에
     중복되면 향후 M52/M53 파라미터 변경 시 한쪽만 갱신되는 회귀
     위험이 생김. 공개 함수로 승격해 재사용하는 것이 Reuse-First.
- 이유: M52에서 도입한 `compute_learning_score()` 공식을 그대로
  재사용해 새 계산 로직 없이 기존 값만 항상 노출하도록 만들어,
  Explainability의 "새 판단 없음" 원칙(§13.3)을 지키면서 near-miss
  가시성을 확보했다.
- 결과/영향: `intelligence/recommendation_adjustment.py`(`_withhold_
  score`→`compute_learning_score` 공개 승격, `WITHHOLD_SCORE_
  THRESHOLD` 공개), `intelligence/recommendation_explanation.py`
  (`_build_experience_summary()` 확장) 2개 파일만 수정. 새 Core
  Domain Interface/Adapter/Service/Layer/File 없음. `tests/
  intelligence/test_recommendation_explanation.py`(기존 1건 값
  갱신 + 신규 1건 — near-miss 가시성 검증). `pytest` 1156개(신규
  1개, 회귀 없음)/`ruff`/`mypy`(222 source files) 전부 통과.
  `.ai/TASKS.md` Milestone 55 절(T01~T03) 신규 추가.

## ADR-0074: Multi-Agent 자가 확인 가드를 현재 구현된 Agent 전체로 일반화 (Milestone 56)

- 상태: 승인됨 (2026-08-01, 사용자가 "M56 Multi-Agent 진행" 착수
  요청 — 로드맵에 사전 예고 없던 이름이라 AskUserQuestion 2회로
  범위(M13이 CodingAgent에만 적용했던 자가 확인 가드를 다른 Agent로
  확장) + 대상(현재 구현된 모든 Agent, 미래 Agent는 같은 계약을
  따르도록 설계만) 확정)
- 날짜: 2026-08-01
- 배경: M13(Multi-Agent Collaboration)이 `is_agent_selected()` 자가
  확인 가드를 `CodingAgent` 1개에만 적용하고 "Review/Documentation
  등으로 확장은 후속 Milestone"이라고 명시적으로 남겼다(Non-goal).
  T01 조사 중 `PlanningAgent`가 Event를 구독하지 않고
  `plan_mission()`으로 직접 호출되는 진입점이라는 구조적 차이를
  발견 — "여러 인스턴스가 같은 broadcast Event에 반응할 때 자가
  선택"이라는 이 가드의 전제 자체가 성립하지 않는다(호출자가 이미
  어떤 인스턴스를 부를지 결정하므로 선택 모호성이 없음).
- 결정:
  1. **Domain Analysis(T01)**: 새 Domain/Interface 아님 — M13이
     이미 정의한 `is_agent_selected()`(`agents/scheduling.py`)를
     그대로 재사용. 새로운 중앙 디스패처·새 메커니즘 없음.
  2. **PlanningAgent 제외(T01 발견 사항, 사용자 확인)**: Event
     구독 Agent(Coding/Review/Documentation/Shell/Coordinator) 5개
     에만 적용하고, 직접 호출 진입점인 PlanningAgent는 구조적
     이유로 범위에서 제외한다 — 억지로 끼워 맞추지 않는다.
  3. **Architecture Review(T02)**: `CodingAgent`의 정확히 같은
     패턴(선택적 키워드 인자 `agent_registry`/`agent_scheduler`,
     기본값 `None`이면 기존 동작과 100% 동일, 이벤트 핸들러 진입
     시점에 `is_agent_selected()`로 자가 확인)을 `ReviewAgent`/
     `DocumentationAgent`/`ShellAgent`/`CoordinatorAgent` 4개에
     동일하게 적용.
  4. **범위 제한(사용자 확정)**: 현재 구현된 Agent까지만 일반화
     하고, 미래에 추가될 Agent는 이번에 만들지 않는다 — 다만 이
     Milestone으로 "새 Agent는 이 계약(선택적 `agent_registry`/
     `agent_scheduler` 키워드 인자 + `is_agent_selected()` 자가
     확인)을 따른다"는 패턴이 5개 사례로 확립되어, 향후 새 Agent가
     같은 패턴을 그대로 반복하면 된다.
- 대안:
  1. Scheduler 선택 정책 고도화(우선순위/부하 기반) — 기각: 사용자가
     "자가 확인 가드를 다른 Agent로 확장"을 선택. 더 큰 설계 변경.
  2. 병렬 실행 — 기각: 사용자가 선택하지 않음, 동시성 이슈가 많은
     영역이라 별도 Milestone 대상.
  3. PlanningAgent에도 억지로 가드 적용(호출자 정보를 임의로 매핑) —
     기각: 이 가드는 "여러 인스턴스가 같은 Event를 구독"하는 구조를
     전제로 하는데 PlanningAgent는 직접 호출이라 전제 자체가
     성립하지 않는다. 억지로 맞추면 의미 없는 코드만 늘어난다.
  4. 모든 Agent에 새로운 공통 Base Class/Mixin 도입 — 기각: YAGNI —
     5개 사례 모두 각자의 생성자·이벤트 핸들러에 동일한 코드 3~5줄을
     반복하는 것으로 충분하고, 상속 계층을 새로 만들 필요가 없다.
- 이유: M13이 검증한 패턴(결정적 Scheduler 선택 + 자가 확인, 새
  중앙 디스패처 없음)을 그대로 복제해 회귀 위험을 최소화하면서,
  M13이 명시적으로 남긴 기술 부채("Review/Documentation 등으로 확장은
  후속 Milestone")를 해소했다. PlanningAgent를 억지로 포함시키지
  않고 구조적 이유를 문서화한 것은 "추정 금지" 원칙과 일치한다.
- 결과/영향: `agents/review_agent.py`/`agents/documentation_agent.py`/
  `agents/shell_agent.py`/`agents/coordinator_agent.py` 4개 파일
  수정(각각 선택적 `agent_registry`/`agent_scheduler` 키워드 인자 +
  `is_agent_selected()` 자가 확인 추가). 새 Core Domain Interface/
  Adapter/Service/Layer/File 없음(기존 27종 유지). `tests/agents/`
  4개 파일에 각각 M13과 동일한 "선택되지 않은 인스턴스는 아무것도
  하지 않는다" 테스트 신규 추가. `pytest` 1160개(신규 4개, 회귀
  없음)/`ruff`/`mypy`(222 source files) 전부 통과. 프로덕션
  Composition Root(`web/server.py`)에는 M13(CodingAgent)도 아직
  배선되지 않아 이번에도 배선하지 않음(MVP 범위 일관 유지).
  `.ai/TASKS.md` Milestone 56 절(T01~T03) 신규 추가.

## ADR-0075: Scheduler 고도화 — 우선순위·가용성 기반 Agent 선택 (Milestone 57)

- 상태: 승인됨 (2026-08-01, 사용자가 "우선순위·Capability·의존성
  기반 Agent 선택 및 실행 정책 설계"로 M57 착수 요청 — 세 축을
  구체화하는 AskUserQuestion 3회, 구현 중 발견한 두 차례의 실제
  버그를 보고·재설계해 최종 확정)
- 날짜: 2026-08-01
- 배경: M13/M56이 확립한 `InMemoryAgentScheduler.select()`는
  `candidates` 리스트의 첫 매치만 고르는 "첫 매치" 정책이었다(M13
  Non-goal: "Scheduler 선택 정책 고도화... 후속 Milestone"). 사용자가
  우선순위/Capability/의존성 3축을 요청했으나, Capability는 이미
  기존 필터로 충분해 범위 밖(사용자 확인), "의존성"은 Task 도메인에
  선행 Task 개념이 없어 "Agent 가용성"으로 재정의됐다(사용자 확인).
- 결정(설계 확정까지 두 차례 실제 버그 발견·수정):
  1. **Domain Analysis(T01)**: 새 Domain/Interface 아님 — 기존
     `AgentScheduler`/`Agent` 도메인의 확장.
  2. **1차 설계(가용성=IDLE) — 기각(실제 버그 발견)**: `AgentRuntime.
     start_agent()`가 등록 즉시 Agent를 `RUNNING`으로 전이시키고
     어떤 Agent도 이벤트 처리 중 상태를 다시 바꾸지 않는다는 것을
     코드 조사로 발견 — `AgentStatus`는 "지금 바쁜지"가 아니라
     "생명주기(등록됨/중지됨)"를 나타낸다. IDLE만 가용으로 보면
     정상 동작 중인 모든 Agent가 걸러져 Scheduler가 항상 빈
     리스트를 반환하는 회귀가 된다는 것을 보고·확인.
  3. **2차 설계(가용성=RUNNING) — 기각(추가 버그 발견)**: 재정의
     후 전체 `pytest`를 돌려보니 `test_agent_scheduler.py`/
     `test_agent_adapter.py`/`test_workflow_agent_link.py`/
     `test_conversation_connector.py` 9건이 실패 — 이 저장소에
     `AgentRuntime`을 거치지 않고 도메인 기본값(`AgentStatus.IDLE`)
     그대로 `Agent`를 직접 생성하는 별도의 테스트 계열이 이미
     존재함을 발견. RUNNING만 가용으로 보면 이번엔 이 계열이
     걸러진다.
  4. **최종 설계(가용성=STOPPED/ERROR만 제외) — 사용자 확정**: IDLE/
     RUNNING/WAITING/PAUSED 전부 가용으로 취급하고, 명확히 "더 이상
     일할 수 없는" STOPPED/ERROR만 제외 — 두 Agent 생성 경로 모두
     회귀 없이 통과.
  5. **우선순위**: `Agent`에 `priority: int = 0` 필드 신설(낮을수록
     우선). `select()`가 capability+가용성 필터 후 `priority`로
     안정(stable) 정렬 — 동점(기본값 0)이면 `candidates` 원래 순서
     보존, M13/M56의 "첫 매치" 동작과 100% 동일(회귀 없음, 안정
     정렬의 성질로 보장).
- 대안:
  1. Capability 기반 추가 고도화(전문성 우선 등) — 기각: 사용자가
     "지금 그대로 유지" 선택, 기존 필터로 충분.
  2. Task 간 선행/후속 의존성(depends_on) — 기각: 범위가 훨씬 커
     TaskEngine까지 건드려야 하고, 사용자가 Agent 가용성으로 범위를
     좁힘.
  3. AgentStatus에 별도 "busy" 개념 신설 — 기각: 사용자가 기존
     `AgentStatus` 재사용을 선택(새 필드 최소화).
- 이유: 두 차례의 실제 코드 조사(각각 별도 실패)를 통해 "가용성"의
  올바른 정의를 실증적으로 좁혀갔다 — 추측이 아니라 `pytest` 실패
  결과 자체가 근거였다. 우선순위는 안정 정렬 하나로 기존 동작과의
  100% 하위 호환을 수학적으로 보장하면서 새 능력(명시적 우선순위)
  을 추가했다.
- 결과/영향: `domain/agent.py`(`Agent.priority` 필드 추가),
  `runtime/agent/agent_scheduler.py`(`InMemoryAgentScheduler.
  select()`에 가용성 필터 + priority 정렬 추가),
  `interfaces/agent_scheduler.py`(계약 docstring 갱신) 3개 파일
  수정. 새 Core Domain Interface/Adapter/Service/Layer/File 없음
  (기존 27종 유지). `tests/runtime/agent/test_agent_scheduler.py`
  (신규 8건 — priority 우선순위 1건, 안정 정렬 1건, STOPPED/ERROR
  제외 2건(파라미터화), IDLE/RUNNING/WAITING/PAUSED 포함 4건
  (파라미터화)). `pytest` 1168개(신규 8개, 회귀 없음)/`ruff`/
  `mypy`(222 source files) 전부 통과. `.ai/TASKS.md` Milestone 57
  절(T01~T03) 신규 추가.

## ADR-0076: Agent 병렬 실행 — max_parallel로 자가 확인 가드 일반화 (Milestone 58)

- 상태: 승인됨 (2026-08-01)
- 날짜: 2026-08-01
- 배경: M13 Review(T2-08 이후)가 남긴 "M13 범위 밖으로 명시적으로
  제외한 것" 3항목 — 병렬 실행 / Scheduler 선택 정책 고도화(M57이
  해소) / `CodingAgent` 외 다른 Agent로의 확장(M56이 해소) — 중 마지막
  으로 남은 "병렬 실행" 부채를 해소한다. `AgentScheduler.select()`의
  `max_count` 매개변수는 T2-02(Milestone 1)부터 존재했고 ARCHITECTURE.md
  §3.4가 "동시에 활동할 Agent 후보를 최대 max_count개 선택"이라고
  이미 명시했지만, 유일한 호출부인 `agents/scheduling.py`의
  `is_agent_selected()`가 내부적으로 `max_count=1`을 고정 전달해
  실제로는 한 번도 1을 넘겨 쓰인 적이 없었다(코드 조사로 확인, 추측
  아님).
- 결정:
  1. **범위 확정**: 새 스레드/프로세스/비동기 실행 메커니즘은 도입하지
     않는다 — 그 책임은 이미 §3.9 `EngineRuntime.run_parallel()`로
     문서화돼 있고 M58 범위 밖이다. M58은 순수하게 "이미 있는
     `max_count` 축을 실제 협업 흐름에 연결하는 배선(wiring)" 작업으로
     한정한다.
  2. `is_agent_selected()`에 `max_parallel: int = 1` 매개변수를 추가해
     `agent_scheduler.select(candidates, capability, max_parallel)`로
     그대로 전달하고, 판정 로직을 `selected.agent_id == agent_id`(단일
     비교)에서 `any(agent.agent_id == agent_id for agent in selected)`
     (선택된 집합 소속 여부)로 바꾼다. 기본값 1이면 `selected`가 항상
     최대 1개라 M13/M56/M57과 100% 동일한 결론.
  3. `CodingAgent`/`ReviewAgent`/`DocumentationAgent`/`ShellAgent`/
     `CoordinatorAgent` 5개 전부에 M56과 같은 패턴으로 선택적 생성자
     인자 `max_parallel_agents: int = 1`을 추가해 `is_agent_selected()`
     호출부에 전달한다. 새 중앙 디스패처·Base Class는 두지 않는다
     (M56이 확립한 "5개 사례 반복" 패턴 재사용, YAGNI).
- 대안:
  1. `find_agent_by_capability()`(단일 Agent 반환)도 `max_parallel`을
     받도록 확장 — 기각: 파이프라인 구성 시 "이 Capability를 가진
     Agent가 존재하는가"만 확인하는 용도라 다중 반환이 필요 없고,
     시그니처를 유지해 회귀 위험을 없앤다.
  2. Scheduler에 새로운 "병렬 실행 정책" Interface 신설 — 기각:
     `AgentScheduler.select()`가 Milestone 1부터 이미 이 계약을
     담당하고 있어 새 Interface는 YAGNI 위반.
- 이유: ARCHITECTURE.md가 이미 예고해 둔 설계(§3.4 `max_count`
  주석)를 실제로 연결하는 것이므로 새로운 설계 판단이 필요 없었다 —
  M13/M56이 검증한 "여러 인스턴스가 같은 질문에 각자 답한다"는
  자가 확인 패턴을 그대로 재사용하면서 판정 기준만 "선택된 하나"에서
  "선택된 집합"으로 일반화하면 충분했다.
- 결과/영향: `agents/scheduling.py`(`is_agent_selected()`에
  `max_parallel` 매개변수 추가), `agents/coding_agent.py`/
  `review_agent.py`/`documentation_agent.py`/`shell_agent.py`/
  `coordinator_agent.py`(5개 전부에 `max_parallel_agents: int = 1`
  생성자 인자 추가) 6개 파일 수정. 새 Core Domain Interface/Adapter/
  Service/Layer/File 없음(기존 27종 유지, `AgentScheduler.select()`
  계약도 변경 없음). `tests/agents/test_scheduling.py`(신규 3건 —
  기본값 1 하위 호환 1건, max_parallel=2로 상위 2개 모두 선택 1건,
  max_parallel 초과분 제외 1건), `tests/agents/test_coding_agent.py`/
  `test_review_agent.py`/`test_documentation_agent.py`/
  `test_shell_agent.py`/`test_coordinator_agent.py`(각 1건 — 두
  인스턴스에 `max_parallel_agents=2`를 주면 둘 다 같은 Event를
  처리함을 증명) 신규 8건. `pytest` 1176개(신규 8개, 회귀 없음)/
  `ruff`/`mypy`(222 source files) 전부 통과. `.ai/TASKS.md` Milestone 58
  절 신규 추가.

## ADR-0077: Automation — WorkflowRepository 신설로 RUN_WORKFLOW 지원 (Milestone 59)

- 상태: 승인됨 (2026-08-01, AskUserQuestion으로 새 컴포넌트 신설
  필요성을 사전 확인받고 "RUN_WORKFLOW 구현"으로 범위 확정)
- 날짜: 2026-08-01
- 배경: M21(Milestone 21)부터 `AutomationActionExecutor`가
  `ActionKind.RUN_WORKFLOW`에 대해 `AutomationActionNotSupportedError`
  만 던지는 상태가 계속 이월돼 왔고, M48(Automation Foundation)의
  Domain Analysis(T01)에서도 "Gap 3"으로 재확인만 되고 범위 밖으로
  남았다. 사용자가 "M59 Automation 진행"으로 착수를 요청해 코드
  조사(`grep`)로 이 저장소에 `workflow_id`로 실제 `Workflow`를 영속
  조회하는 통로가 전혀 없다는 사실을 확인 — `WorkflowRunner`
  (Milestone 12)는 이미 `Workflow` 인스턴스를 받아 실행하는 조율자로
  존재하지만, Automation Action은 `workflow_id`(문자열)만 갖고 있어
  둘을 이어줄 조회 계층이 없으면 구현이 불가능했다.
- 결정:
  1. **새 Core Domain Interface `WorkflowRepository` 신설**(27종→
     28종, Milestone 2 이후 최초 증가): `AgentRepository`/
     `AutomationRepository`와 동일한 `get`/`save`/`list_workflows`
     스타일, `WorkflowNotFoundError` 포함. `InMemoryWorkflowRepository`
     로 최소 구현(영속화는 향후 `FileWorkflowRepository` 등으로
     확장 가능하도록 Interface만 보고 구현).
  2. `AutomationActionExecutor`에 `workflow_repository`/
     `workflow_runner` 선택적 생성자 인자를 추가(M38 `recommendation_
     orchestration_service`와 동일한 선택적 DI 패턴). 둘 다 주입되면
     `_run_workflow()`가 `workflow_repository.get(action.workflow_id)`
     → `workflow_runner.run(workflow)`로 위임한다. 하나라도 없으면
     기본값 `None`이라 여전히 `AutomationActionNotSupportedError` —
     M21 이후 동작과 100% 동일한 하위 호환.
  3. **프로덕션 배선(`web/server.py`의 `build_app()`)은 하지 않는다**:
     `TaskEngine`/`WorkflowEngine`조차 프로덕션 Composition Root에
     아직 배선돼 있지 않아, 지금 배선하려면 이번 범위를 넘어 그 둘을
     프로덕션에 처음 들이는 훨씬 큰 작업이 된다 — M56/M57/M58이 반복
     확인한 "MVP 범위 유지" 판단을 그대로 적용(YAGNI).
- 대안:
  1. `AutomationActionExecutor`에 `Workflow`를 직접 전달하도록 Action
     자체를 재설계(workflow_id 대신 Workflow 객체 보관) — 기각:
     `AutomationRule`은 직렬화 가능한 Flat 데이터([`domain/
     automation.py`](../src/ai_workspace/domain/automation.py)의
     `Trigger`/`Action` 설계 원칙)여야 하는데 `Workflow` 객체 자체를
     들고 있으면 이 원칙이 깨진다.
  2. `WorkflowRepository` 없이 `WorkflowEngine`만으로 처리 — 기각:
     `WorkflowEngine.plan()`은 이미 만들어진 `Workflow` 인스턴스를
     입력으로만 받을 뿐 `workflow_id`로 조회하는 책임이 없다(계약
     확인, `interfaces/workflow_engine.py`).
  3. RUN_WORKFLOW를 계속 Not Supported로 남기고 다른 Automation Gap을
     다룬다 — 기각: 사용자가 AskUserQuestion에서 "RUN_WORKFLOW 구현"
     을 명시적으로 선택.
- 이유: M21부터 4개 Milestone(M21/M38/M48/M59)에 걸쳐 반복적으로
  재확인만 되고 미뤄져 온 부채였고, 이번에 처음으로 그 이유(조회
  계층 부재)가 코드 조사로 명확해졌다 — 필요한 컴포넌트가 실증적으로
  드러난 뒤에 신설했으므로 추측성 설계가 아니다. 기존 `Agent
  Repository`/`AutomationRepository` 패턴을 그대로 재사용해 새로운
  설계 언어를 만들지 않았다.
- 결과/영향: `interfaces/workflow_repository.py`(신규 Interface),
  `runtime/workflow/workflow_repository.py`(신규
  `InMemoryWorkflowRepository`), `runtime/automation/
  automation_action_executor.py`(선택적 DI 2개 추가 + `_run_workflow()`
  신규), `domain/automation.py`(docstring 갱신) 4개 파일
  추가/수정. **새 Core Domain Interface 1종 추가(27종→28종)** —
  Milestone 2 이후 최초. `tests/interfaces/test_workflow_repository.py`
  (신규 5건), `tests/runtime/automation/test_automation_action_executor.py`
  (미주입 시 하위 호환 1건 이름 갱신 + 신규 1건 — 주입 시 실제
  Workflow 조회→WorkflowRunner 실행까지 end-to-end 증명) 신규 6건.
  `pytest` 1182개(신규 6개, 회귀 없음)/`ruff`/`mypy`(224 source files)
  전부 통과. `.ai/TASKS.md` Milestone 59 절 신규 추가. `docs/
  ARCHITECTURE.md` §7 Interface 표(28종 갱신)/§3.19 Automation 절
  RUN_WORKFLOW 서술 갱신.

## ADR-0078: Autonomous Workspace — AutomationScheduler.tick()의 Trigger 평가 실패 격리 (Milestone 60)

- 상태: 승인됨 (2026-08-01, AskUserQuestion으로 넓은 "장시간 자율
  운영" 주제를 구체적으로 실증된 버그 수정 범위로 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M60 Autonomous Workspace(장시간 자율 운영)"으로
  착수를 요청했으나 이 주제는 세션 영속화/재시도/Health 등 여러
  방향으로 해석될 수 있어, 먼저 코드 경로를 직접 추적해 구체적인
  실제 위험을 찾았다: `web/app.py`의 `_tick_loop()`은
  `automation_scheduler.tick()`을 30초마다 호출하는 `while True`
  백그라운드 asyncio Task인데, `tick()` 내부에서 `TimeTriggerEvaluator`
  /`IntervalTriggerEvaluator`가 `Trigger.time_of_day`/`AutomationRule.
  last_executed_at`을 파싱하다 `ValueError`를 던지면 이를 감싸는
  코드가 `tick()` 어디에도 없어 예외가 `_tick_loop()` 밖으로
  전파된다. asyncio Task가 처리되지 않은 예외로 종료되면 서버
  프로세스는 계속 살아있지만 자동화 전체가 영구히 멈추고, 기존
  `HealthMonitor`(M22)는 `automation_scheduler is not None`만 확인할
  뿐이라 이 상태를 감지하지 못한다 — Rule 하나의 손상된 값만으로
  재현 가능한 실제 공백(추측 아님).
- 결정:
  1. `AutomationScheduler.tick()`의 Rule별 처리(evaluator 생성→
     `should_fire()`→`_fire()`→`compute_next_execution_at()`→
     `save()`) 전체를 `try/except Exception: pass`로 감싼다 — `_fire()`
     가 이미 지키는 "한 Rule의 실패가 다른 Rule에 영향 없음" 원칙
     (Action 실행 단계)을 Trigger 평가 단계까지 그대로 확장한 것뿐,
     새로운 원칙을 만들지 않았다.
  2. **`_on_event()`는 대상에서 제외한다**: `EventTriggerEvaluator.
     should_fire()`는 파싱 없이 항상 `True`만 반환해 현재 코드로는
     실제로 던질 수 없다 — 실증되지 않은 경로에 방어 코드를 추가하지
     않는다(YAGNI, "발생할 수 없는 시나리오에 대한 에러 처리 금지"
     원칙). 이 경로는 이미 `EventBus.publish()`의 구독자 예외 격리
     (T2-02 계약)로 보호되고 있어 중복 보호이기도 하다.
  3. **`run_now()`는 대상에서 제외한다**: REST API `/run`이 직접
     위임하는 1회성 호출이라 `AutomationRuleNotFoundError` 등을
     그대로 전파해 호출자가 즉시 알 수 있는 것이 바람직하다 —
     백그라운드 루프가 아니므로 "루프가 죽는다"는 위험 자체가 없다.
- 대안:
  1. `web/app.py`의 `_tick_loop()` 자체를 감싸는 defense-in-depth
     추가(`while True` 루프 안에서도 예외를 잡아 계속 돎) — 채택하지
     않음(이번 범위에서 보류): 사용자가 승인한 범위가 `Automation
     Scheduler` 수정으로 명확히 좁혀졌고, `tick()` 내부에서 이미
     막으면 이 바깥쪽 방어는 현재로선 실증된 필요가 없다(YAGNI). 향후
     `list_rules()` 자체가 던지는 등 `tick()` 외부 원인이 실제로
     발견되면 별도 검토.
  2. `HealthMonitor`가 "마지막 tick 성공 시각"을 노출하도록 확장 —
     기각(AskUserQuestion에서 사용자가 선택하지 않음): 이번 수정으로
     애초에 tick 루프가 죽지 않으므로 관측보다 예방이 우선이라고
     판단, 필요성이 드러나면 별도 Milestone.
- 이유: 예방(루프가 죽지 않게)이 관측(죽은 걸 감지)보다 근본적이고
  구현 비용도 훨씬 작다 — 새 Interface/컴포넌트 없이 기존 `_fire()`
  가 확립한 예외 격리 원칙을 한 단계 앞(Trigger 평가)으로 옮기기만
  하면 충분했다.
- 결과/영향: `runtime/automation/automation_scheduler.py`
  (`tick()`을 `try/except`로 감쌈, docstring에 근거 기록) 1개 파일
  수정. 새 Core Domain Interface/Adapter/Service 없음(28종 유지).
  `tests/runtime/automation/test_automation_scheduler.py`(신규 2건 —
  손상된 Rule이 있어도 다른 Rule은 정상 발동/손상된 Rule을 만난 뒤에도
  다음 `tick()` 호출이 정상 동작함을 증명). `pytest` 1184개(신규
  2개, 회귀 없음)/`ruff`/`mypy`(224 source files) 전부 통과. `.ai/
  TASKS.md` Milestone 60 절 신규 추가. `docs/ARCHITECTURE.md` §3.19
  Automation 절에 Trigger 평가 실패 격리 서술 추가.

## ADR-0079: Distributed Multi-Agent — Agent.location + RemoteAgentDispatcher 최소 씨앗 (Milestone 61)

- 상태: 승인됨 (2026-08-01, AskUserQuestion으로 "최소 인터페이스
  씨앗" 범위 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M61 Distributed Multi-Agent(원격 Agent)"로 착수를
  요청했다. 조사 결과 이 주제는 M11(scope-out)/M16/M21(scope-out)/
  ADR-0074에서 "Distributed/Multi-node Scheduler"·"Multi-node
  Cluster"로 반복적으로 언급되며 "실제 필요성이 생기기 전까지
  이월한다"고 명시된 Non-goal 영역이었다. `Agent` 도메인에는 host/주소
  개념이 전혀 없고, `AgentRegistry`는 스스로를 "in-memory, 프로세스
  재시작 시 소멸"이라 문서화해 단일 프로세스 전제가 코드에 명시적으로
  박혀 있었다. 유일하게 "원격"을 언급하는 `ExecutionEnvironment`
  (M11, ADR-0025)도 `EngineAdapter` 내부로만 범위를 한정해 Agent
  레벨과는 무관했다.
- 결정:
  1. `Agent`에 `location: str | None = None` 필드를 추가한다.
     기본값 `None`은 "같은 프로세스"를 뜻해 기존 Agent 전부와 100%
     하위 호환이다.
  2. 신규 `RemoteAgentDispatcher` 계약(`interfaces/
     remote_agent_dispatcher.py`)을 도입한다 — `dispatch(agent,
     event)`로 `agent.location`이 가리키는 목적지에 Event를 전달한다.
     `ExecutionEnvironment`가 `EngineAdapter` 내부에서 "어디서 실행할
     지"를 추상화하는 패턴을 Agent Runtime 레벨의 "Event를 어디로
     전달할지"에 그대로 적용한 것이다.
  3. `LoopbackAgentDispatcher`(`runtime/agent/
     remote_agent_dispatcher.py`)를 최소 구현체로 둔다 — 실제
     네트워크/RPC 없이 location마다 독립된 `EventBus`를 연결해 같은
     프로세스 안에서 여러 위치를 흉내낸다. 향후 실제 원격(HTTP 등)
     구현체로 교체해도 이 인터페이스를 쓰는 코드는 변경할 필요가
     없다.
  4. `AgentRuntime`에 `start_agent(..., location=...)`(Agent에 location
     기록)와 `dispatch_event(session_id, event)`(location이 있는
     Agent에만 개입, 없으면 no-op)를 추가한다. `remote_agent_
     dispatcher`는 선택적 생성자 주입(기본값 `None`) — 미주입 시
     `dispatch_event()`는 원격 Agent에 대해 `ValueError`를 던지되,
     location이 없는 로컬 Agent는 계속 100% 기존 동작(EventBus 방송
     + `is_agent_selected()`)과 동일하다.
  5. Production Composition Root(`web/server.py`)에는 연결하지
     않는다 — 실제 소비자(원격에서 실행되는 실제 Agent 프로세스)가
     아직 없으므로 M56~M60과 동일한 YAGNI 판단을 유지한다.
- 대안:
  1. 실동작 HTTP 기반 `RemoteAgentAdapter` 구현(네트워크 계층/인증/
     오류 처리 포함) — 기각(AskUserQuestion에서 사용자가 선택하지
     않음): 지금 실제로 원격에서 실행해야 하는 Agent가 없는데
     네트워크 코드를 작성하는 것은 이 프로젝트가 반복적으로 거부해온
     실증되지 않은 선제 구현이다.
  2. `AgentScheduler.select()`가 location을 선택 기준(예: "가까운
     Agent 우선")으로 반영 — 기각: `select()`는 이미 Capability/
     가용성/우선순위만으로 결정적이며(M57, ADR-0075), location 기반
     정책은 실제 다중 location 배포가 생기기 전까지 근거가 없다.
  3. M61을 진행하지 않고 완전히 대체 주제로 넘어간다 — 기각(사용자가
     "최소 인터페이스 씨앗"을 선택): Non-goal 판단 자체는 유지하되,
     향후 실제 필요가 생겼을 때 `Agent`/`AgentRegistry`/
     `AgentScheduler`를 다시 건드리지 않고 확장할 수 있는 진입점을
     지금 준비해두는 것이 더 낮은 비용이라고 판단.
- 이유: "아직 필요 없다(Non-goal)"는 반복된 판단과 "미래에 필요할 때
  자연스러운 확장점을 남긴다"는 요구를 동시에 만족시키려면, 실제
  네트워크/RPC 코드 없이 도메인 필드 하나 + 인터페이스 하나 +
  In-process 구현체 하나만으로 충분했다 — `ExecutionEnvironment`
  (M11)가 이미 증명한 패턴을 재사용해 새로운 설계 위험을 도입하지
  않았다.
- 결과/영향: `domain/agent.py`(`location` 필드), `interfaces/
  remote_agent_dispatcher.py`(신규, `RemoteAgentDispatcher`),
  `runtime/agent/remote_agent_dispatcher.py`(신규,
  `LoopbackAgentDispatcher`), `runtime/agent/agent_runtime.py`
  (`remote_agent_dispatcher` 선택적 주입, `start_agent(location=...)`,
  `dispatch_event()`) 수정/추가. Core Domain Interface 28→29종
  (`RemoteAgentDispatcher` 추가). `tests/domain/test_agent.py`(2건),
  `tests/runtime/agent/test_remote_agent_dispatcher.py`(신규 5건),
  `tests/runtime/agent/test_agent_runtime.py`(6건) 신규 테스트.
  `pytest` 1197개(신규 13개, 회귀 없음)/`ruff`/`mypy`(226 source
  files) 전부 통과. `.ai/TASKS.md` Milestone 61 절 신규 추가. `docs/
  ARCHITECTURE.md` §3.4에 Distributed Multi-Agent 서술 추가, §7
  Interface 표 갱신.

## ADR-0080: Multi-LLM Orchestrator — EngineRuntime.run_ensemble() (Milestone 62)

- 상태: 승인됨 (2026-08-01, AskUserQuestion으로 "동일 Task를 여러
  Provider에 병렬 실행" 범위 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M62 Multi-LLM Orchestrator(Claude, GPT, Gemini 등
  혼합)"으로 착수를 요청했다. 조사 결과 `LLMProvider` enum(OPENAI/
  ANTHROPIC/GOOGLE/XAI)과 `CLIEngineAdapter`+`CodexProvider`/
  `GeminiCliProvider`로 Provider별 커맨드 조립 코드는 이미 있었지만
  (M6, 단 실제 CLI 바이너리 미검증 — 반복 기록된 기존 부채),
  `EngineRuntime.run()`/`run_parallel()`은 둘 다 "Task 1개당 Adapter
  1개"만 고르는 라우팅이었다. `run_parallel()`조차 여러 **Task**를
  각자 하나의 Adapter로 병렬 실행할 뿐, 하나의 **Task**를 여러
  Provider에 동시에 보내 결과를 비교/합치는 메커니즘은 어디에도
  없었다 — `EngineSelectionPolicy.select()`(M17)도 단일
  `EngineSelectionDecision`만 반환한다. consensus/ensemble/vote
  관련 코드나 문서 언급도 전혀 없었다(추측 아님, 코드 전수 확인).
- 결정:
  1. `EngineRuntime`에 `run_ensemble(task, engine_names, *,
     model=None) -> dict[str, EngineResult]`를 신설한다.
     `required_capabilities` 기반 "첫 매칭" 선택을 쓰지 않고
     `register_engine()`에 쓰인 정확한 이름으로 여러 Adapter를
     지정한다 — 여러 Provider를 의도적으로 섞어 돌리는 것이 목적이라
     capability 매칭 규칙이 맞지 않기 때문이다.
  2. `ManagedEngineRuntime`은 `run_parallel()`과 동일한
     `ThreadPoolExecutor` 메커니즘을 재사용해 실제로 동시에 실행한다
     — 새 동시성 메커니즘을 만들지 않는다.
  3. `run_ensemble()`은 `status(task_id)`(task_id당 상태 1개만
     추적)와 의미가 충돌한다(같은 task_id가 여러 엔진에서 동시에
     도는데 상태 저장소는 1개) — 이 추적에 전혀 관여하지 않고 세션
     생성→실행→정리만 독립 수행한다.
  4. 개별 엔진 실패(미등록 이름 포함)는 `run_parallel()`의
     M10-T01/T02 원칙과 동일하게 그 이름의
     `EngineResult(success=False)`로만 격리하고 다른 결과에 영향을
     주지 않는다.
  5. **결과를 투표/합치는 로직은 추가하지 않는다**(YAGNI) — 호출자가
     반환된 이름별 결과를 직접 비교·선택한다.
  6. `RecoveringEngineRuntime`은 재시도 없이 내부 Runtime에
     위임한다 — 실패한 개별 엔진 결과도 그 자체로 비교에 필요한
     정보이므로 재시도로 덮어쓰면 오히려 왜곡된다.
- 대안:
  1. 결과를 자동으로 합치거나(예: 다수결) "최선" 하나를 골라 반환 —
     기각(AskUserQuestion에서 선택되지 않음, 이번 범위에서 근거
     부족): 무엇을 "최선"으로 볼지(정확도/속도/비용) 정책이 전혀
     정의되지 않은 상태에서 임의로 하나를 고르면 오히려 정보 손실.
     필요성이 증명되면 별도 `OrchestrationPolicy` 검토.
  2. Codex/Gemini CLI를 이 세션에서 실제 바이너리로 검증 — 기각
     (사용자가 다른 선택지 선택): M62의 목적은 "여러 Provider를
     동시에 돌리는 메커니즘 신설"이지 기존 CLI 부채 해소가 아니다.
  3. `EngineSelectionPolicy`에 "여러 후보를 동시에 반환" 옵션 추가 —
     기각: `EngineSelectionPolicy`는 비용 기반 "최선 하나" 결정
     책임(M17, ADR-0029)이 이미 명확히 정의돼 있어, 여러 후보 동시
     반환은 다른 책임(오케스트레이션)이라 별도 메서드로 분리하는
     것이 응집도상 더 낫다.
- 이유: `run_parallel()`이 이미 증명한 "여러 실행을 동시에, 개별
  실패는 격리" 패턴을 "여러 Task"에서 "여러 Provider(같은 Task)"로
  축만 바꿔 재사용하면 충분했다 — 새 동시성 메커니즘이나 Core Domain
  Interface 없이 `EngineRuntime`에 메서드 하나만 추가해 실제
  Multi-LLM 오케스트레이션 능력을 제공한다.
- 결과/영향: `interfaces/engine_runtime.py`(`run_ensemble()` 추상
  메서드), `runtime/engine/engine_runtime.py`
  (`InMemoryEngineRuntime`), `runtime/engine/
  managed_engine_runtime.py`(`ManagedEngineRuntime`, `ThreadPoolExecutor`
  기반 실제 구현), `runtime/engine/recovering_engine_runtime.py`
  (`RecoveringEngineRuntime`, 위임) 수정. `EngineRuntime`의 테스트
  더블 4곳(`tests/interfaces/fakes.py`
  `FakeEngineRuntime`/`tests/agents/test_coding_agent.py`
  `RecordingEngineRuntime`/`tests/core/test_workspace_core.py`
  `SpyEngineRuntime`/`tests/runtime/engine/
  test_recovering_engine_runtime.py` `ScriptedEngineRuntime`)에
  `run_ensemble()` 구현 추가(신규 추상 메서드라 전부 필요). 새 Core
  Domain Interface 없음(29종 유지 — 기존 `EngineRuntime`에 메서드만
  추가). 신규 테스트 10건(`InMemoryEngineRuntime` 3건,
  `ManagedEngineRuntime` 6건, `RecoveringEngineRuntime` 1건). `pytest`
  1207개(신규 10개, 회귀 없음)/`ruff`/`mypy`(226 source files) 전부
  통과. `.ai/TASKS.md` Milestone 62 절 신규 추가. `docs/
  ARCHITECTURE.md` §3.9 Engine Runtime 절에 Multi-LLM Orchestrator
  서술 추가.

## ADR-0081: Result Aggregation / Consensus — ResultAggregator + MajorityVoteAggregator (Milestone 63)

- 상태: 승인됨 (2026-08-01, AskUserQuestion으로 "단순 다수결(exact-match
  voting) 애그리게이터" 범위 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M63 Result Aggregation / Consensus"로 착수를 요청했다.
  ADR-0080(M62)은 `run_ensemble()` 결정 시점에 "결과를 투표/합치는
  로직은 추가하지 않는다(YAGNI) — 호출자가 반환된 이름별 결과를 직접
  비교·선택한다"고 명시적으로 이 기능을 보류해 두었다. M63은 그
  보류를 지금 구현하는 요청이며, `EngineResult.output`이 구조화되지
  않은 문자열이라 정확한 의미(semantic) 비교 자체가 이 프로젝트
  범위를 넘는 별도 과제임을 재확인했다.
- 결정:
  1. 신규 Core Domain Interface `ResultAggregator`를 추가한다 —
     `aggregate(results: dict[str, EngineResult]) -> AggregatedResult`
     하나만 정의한다(29종→30종).
  2. 유일한 구현체 `MajorityVoteAggregator`는 `EngineResult.output`의
     **정확한 문자열 일치**로만 투표한다 — 의미 비교나 LLM judge 기반
     심사, 엔진별 가중치 투표는 범위 밖(YAGNI).
  3. `success=False`인 결과는 투표 대상에서 제외하고
     `failed_engines`로만 별도 보고한다 — `run_parallel()`의
     M10-T01/T02 개별 실패 격리 원칙과 동일 정신을 재사용한다.
  4. 동점 시에는 입력 `results`(=`run_ensemble()`에 넘긴
     `engine_names`) 순회 순서상 그 출력을 가장 먼저 낸 엔진을
     대표로 고른다 — 결정적(deterministic) 규칙.
  5. `EngineRuntime`/`run_ensemble()`은 이 인터페이스를 알지 못한다 —
     자동으로 연결하지 않는다(M61 `RemoteAgentDispatcher`와 동일하게,
     Composition Root 배선은 실제 필요 시나리오가 생길 때 별도
     제안·승인 대상으로 남긴다).
- 대안:
  1. `run_ensemble()`이 직접 `AggregatedResult`를 반환하도록 시그니처
     변경 — 기각: ADR-0080에서 이미 `dict[str, EngineResult]` 계약을
     확정했고, 그 계약을 깨면 M62에서 작성한 모든 구현체·테스트
     더블·테스트가 다시 깨진다. 별도 계약으로 분리하면 호출자가
     원본 결과와 집계 결과 중 필요한 것을 선택할 수 있어 하위 호환도
     100% 유지된다.
  2. LLM judge 기반 의미 비교 채택 — 기각: 사용자가 AskUserQuestion에서
     명시적으로 배제. 별도 API 비용/지연/신뢰성 검증이 필요한 훨씬
     큰 과제이며 이 프로젝트의 최소 복잡도 원칙과 맞지 않는다.
  3. 엔진별 가중치 투표 채택 — 기각: 가중치를 어떻게 산정·저장·조정할지
     자체가 별도 설계가 필요한 신규 메커니즘이라 범위가 커진다 —
     현재 그런 신뢰도 데이터를 추적하는 메커니즘이 전혀 없다.
- 이유: exact-match 다수결은 `run_ensemble()`이 이미 반환하는
  `EngineResult.output`(문자열)만으로 즉시 계산 가능한 가장 단순한
  집계 규칙이다 — 새 상태·새 저장소·새 외부 호출 없이 순수 함수
  하나로 구현되며, `run_parallel()`/`run_ensemble()`이 이미 증명한
  개별 실패 격리 원칙을 그대로 재사용해 일관성을 유지한다.
- 결과/영향: `interfaces/result_aggregator.py`(신규,
  `AggregatedResult`/`ResultAggregator`), `runtime/engine/
  result_aggregator.py`(신규, `MajorityVoteAggregator`) 추가. 새 Core
  Domain Interface 1건 추가(29종→30종). 신규 테스트 6건(다수결 선택,
  동점 타이브레이크, 실패 엔진 격리, 전원 실패, 빈 dict, 만장일치).
  `pytest` 1213개(신규 6개, 회귀 없음)/`ruff`/`mypy`(228 source files)
  전부 통과. `.ai/TASKS.md` Milestone 63 절 신규 추가. `docs/
  ARCHITECTURE.md` §3.9 Engine Runtime 절에 Result Aggregation /
  Consensus 서술 추가, §7 Interface 표에 `ResultAggregator` 행 추가.

## ADR-0082: Cost & Routing Optimization — EngineRuntime 비용 기반 선택 (Milestone 64)

- 상태: 승인됨 (2026-08-01, AskUserQuestion으로 "EngineRuntime에 비용
  기반 선택 도입" 범위 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M64 cost & routing optimization"으로 착수를
  요청했다. 코드 조사 결과 두 갈래 실행 경로가 이미 존재했음을
  확인했다: Automation 파이프라인(`RecommendationExecutionService`)은
  M17부터 이미 비용 기반 `EngineSelectionPolicy`(예산 내 최저 예상
  비용 후보 선택)를 거치지만, Agent가 직접 쓰는
  `EngineRuntime.run()`/`run_parallel()`의 내부 선택 로직(`_select`/
  `_require_adapter`)은 등록 순서상 "능력 만족하는 첫 매칭"만 고르고
  비용을 전혀 보지 않는 완전히 별개의 라우팅 경로였다(추측 아님, 코드
  경로 직접 확인). `Budget`은 Task 단위 개별 확인만 하고 여러 Task에
  걸친 누적 소비 추적은 M15부터 명시적 Non-goal이다.
- 결정:
  1. `InMemoryEngineRuntime`/`ManagedEngineRuntime` 생성자에
     `engine_selection_policy: EngineSelectionPolicy | None = None`,
     `budget_policy_engine: BudgetPolicyEngine | None = None`을
     선택적으로 추가한다.
  2. 주입되면 `_select`/`_require_adapter`가 등록된 Adapter들로
     `EngineCandidate` 목록(M17-T01과 동일 필드)을 만들어
     `EngineSelectionPolicy.select()`에 그대로 위임한다 — 새 선택
     로직을 중복 구현하지 않고 M17이 이미 검증한 로직을 재사용한다
     (DRY). Agent 실행 경로와 Automation 경로가 동일한 비용 기반
     라우팅 규칙을 공유하게 된다.
  3. 생략(기본값 `None`)하면 이전 동작(Milestone 64 이전)과 100%
     동일하다 — 등록 순서상 첫 매칭 규칙 그대로.
  4. `run_parallel()`은 배치 전체에 하나의 Adapter를 고르는 기존
     설계를 유지한다(사전 검사는 `tasks[0]`의 비용 기준). 다만
     `ManagedEngineRuntime.run_parallel()`은 각 Task를 `self.run()`으로
     개별 실행하는 기존 구조이므로 Task별 비용도 자연히 반영된다.
  5. `run_ensemble()`은 호출자가 엔진 이름을 명시적으로 지정하는
     계약(M62)이라 이번 범위에서 변경하지 않는다.
  6. 여러 Task에 걸친 **누적** 예산 소비 추적(M15 Non-goal)은 이번
     범위 밖으로 유지한다(YAGNI) — `BudgetPolicyEngine.check()`는
     여전히 매 호출을 독립적으로 평가하며 상태를 갖지 않는다.
- 대안:
  1. `EngineRuntime`에 새 `CostAwareEngineRuntime` 데코레이터/래퍼
     클래스를 별도로 도입 — 기각: 기존 `EngineRuntime` 구현체를
     감싸는 새 계층을 추가하면 `RecoveringEngineRuntime`과의 합성
     순서, `run_ensemble()`/`status()` 등 나머지 메서드의 위임까지
     전부 다시 설계해야 해서 복잡도가 커진다. 생성자 주입 하나로
     기존 클래스 내부에서 분기하는 편이 훨씬 작다.
  2. 누적 예산(Spend Tracking) 컴포넌트를 함께 도입 — 기각:
     사용자가 AskUserQuestion에서 명시적으로 배제. M15의 명시적
     Non-goal을 뒤집는 훨씬 큰 범위 변경이며 저장소·조회 API를
     새로 설계해야 한다.
  3. `EngineRegistry`를 `EngineRuntime`에 주입해 `list_candidates()`를
     재사용 — 기각: `EngineRuntime`은 이미 자체 `self._engines` dict로
     어댑터를 관리하고 있어, `EngineRegistry`까지 추가로 주입하면 같은
     정보를 두 곳에서 따로 등록·관리해야 하는 이중 관리 문제가
     생긴다. `EngineCandidate` 빌드 로직(약 10줄)만 인라인으로
     재사용하는 편이 더 작은 결합도를 유지한다.
- 이유: `EngineSelectionPolicy`(M17)가 이미 "예산 내 최저 비용" 규칙을
  검증된 형태로 갖고 있었으므로, `EngineRuntime`이 이를 선택적으로
  위임하기만 하면 새 알고리즘 없이 Agent 실행 경로의 비용 인식 공백을
  메울 수 있었다. 선택적 DI로 기존 호출자(주입하지 않는 모든 곳)는
  전혀 영향받지 않는다.
- 결과/영향: `runtime/engine/engine_runtime.py`(`InMemoryEngineRuntime`),
  `runtime/engine/managed_engine_runtime.py`(`ManagedEngineRuntime`)
  수정 — 둘 다 생성자 확장 + `_select`/`_require_adapter` 분기.
  `RecoveringEngineRuntime`은 변경 없음(순수 위임 구조 그대로).
  새 Core Domain Interface 없음(기존 `EngineSelectionPolicy`/
  `BudgetPolicyEngine` 재사용, 30종 유지). 신규 테스트 9건
  (`InMemoryEngineRuntime` 4건, `ManagedEngineRuntime` 5건 — policy
  미주입 시 회귀 없음, 최저 비용 선택, 예산 초과 후보 제외, 예산 내
  후보 없음 시 예외, `run_parallel()` 배치 선택). `pytest` 1222개(신규
  9개, 회귀 없음)/`ruff`/`mypy`(228 source files) 전부 통과. `.ai/
  TASKS.md` Milestone 64 절 신규 추가. `docs/ARCHITECTURE.md` §3.9
  Engine Runtime 절에 Cost & Routing Optimization 서술 추가(기존
  "우선순위 정책 도입하지 않음" 문구 갱신).

## ADR-0083: Engine Learning & Adaptive Routing — 엔진별 신뢰도 추적 (Milestone 65)

- 상태: 승인됨 (2026-08-01, AskUserQuestion으로 "EngineRuntime에
  엔진별 신뢰도 추적 + 실패 엔진 제외" 범위 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M65 engine learning & adaptive routing"으로 착수를
  요청했다. 조사 결과 M49(Learning Engine)는 Recommendation/Adaptation
  파이프라인의 학습만 다뤘고, M64에서 새로 생긴 `EngineRuntime`의 비용
  기반 선택(`EngineSelectionPolicy`)은 순수 정적 비용
  (`estimated_cost_usd`)만 보고 과거 성공/실패 이력을 전혀 반영하지
  않았다 — 계속 실패하는 엔진이라도 비용이 가장 싸면 계속 선택되는
  문제가 실제로 존재했다(추측 아님, 코드 확인). Dashboard의
  `ReliabilityStats`도 워크스페이스 전체 집계일 뿐 엔진별로 분리돼
  있지 않아 재사용할 수 없었다.
- 결정:
  1. `domain/engine_reliability.py`에 `EngineReliabilityStat`(total/
     success_count/failure_count)를 신설한다 — M40 `ExperienceStat`과
     동일한 필드 구성을 의도적으로 재사용하되, `runtime/engine/`이
     `intelligence/`를 참조하면 계층 위반이므로 별도 domain 타입으로
     분리한다.
  2. `is_unreliable()` 판정 규칙은 M49/ADR-0066의 Recommendation
     Adaptation 임계값(`success_count == 0 and total >= 3`)을 그대로
     재사용한다 — 새 규칙을 설계하지 않고 이미 검증된 "표본 부족 시
     성급하게 판단하지 않는다"는 원칙을 그대로 이식한다.
  3. `InMemoryEngineRuntime`/`ManagedEngineRuntime`이 `run()`/
     `run_parallel()`/`run_ensemble()`이 실제로 실행한 엔진의
     성공/실패를 이름별로 in-process 누적한다.
  4. `engine_selection_policy`가 주입된 경로(M64)에서만
     `EngineCandidate` 목록을 만들 때 `is_unreliable()`인 엔진을
     미리 제외한 뒤 비용 기반 선택을 적용한다. `EngineSelectionPolicy`
     인터페이스 자체(`select()` 시그니처)는 변경하지 않는다 — 후보
     필터링은 `EngineRuntime`의 책임으로 남기고, M17의 "Decision
     Only" 계약을 그대로 유지한다.
  5. policy 미주입 시(M64 이전 동작)에는 신뢰도 추적만 계속되고 제외는
     적용되지 않는다 — 100% 하위 호환.
  6. Cancel된 실행(`EngineResult.error == "cancelled"` sentinel)은
     신뢰도에 반영하지 않는다 — 사용자 취소는 엔진 자체의 신뢰성
     문제가 아니다.
  7. 영속 저장소는 M49/M50과 동일하게 이번 범위 밖으로 유지한다(in
     -process 한정, YAGNI).
- 대안:
  1. `EngineSelectionPolicy.select()` 시그니처에 신뢰도 데이터를 정식
     파라미터로 추가 — 기각: 기존 M17 Decision Only 계약을 바꾸는 더
     큰 변경이며, 가중치 산정 방식(비용 vs 신뢰도)까지 새로 설계해야
     한다. 후보 목록에서 미리 걸러내는 편이 더 작은 변경이다.
  2. Guardian 위반 이력처럼 신뢰도 이력도 영속 저장 — 기각: 사용자가
     AskUserQuestion에서 명시적으로 배제. M49/M50이 이미 "in-process
     범위로 한정 → 이후 별도 Milestone에서 영속화"로 단계를 나눈
     전례를 그대로 따른다.
  3. `ExperienceStat`(intelligence 계층)을 직접 재사용 — 기각:
     `runtime/engine/`이 `intelligence/`를 참조하면 §8 의존성 규칙
     위반(Guardian이 이미 검사하는 계층 경계)이다. 같은 필드 구성만
     별도 domain 타입으로 복제하는 편이 계층을 지킨다.
- 이유: M49가 이미 "성공 0건 + 표본 3건 이상"이라는 임계값 규칙을
  검증된 형태로 남겨 두었으므로, 같은 규칙을 엔진 이름 단위로
  재사용하면 새 알고리즘 설계 없이 M64가 남긴 "계속 실패해도 계속
  선택됨" 공백을 메울 수 있었다. `EngineRuntime` 내부 상태만 추가하고
  기존 Interface는 전혀 건드리지 않아 하위 호환이 자동으로 보장된다.
- 결과/영향: `domain/engine_reliability.py`(신규),
  `runtime/engine/engine_runtime.py`(`InMemoryEngineRuntime`),
  `runtime/engine/managed_engine_runtime.py`(`ManagedEngineRuntime`)
  수정 — `_select`/`_require_adapter`가 `(이름, adapter)` 튜플을
  반환하도록 변경, 실행 후 결과를 신뢰도에 기록. 새 Core Domain
  Interface 없음(`EngineReliabilityStat`은 domain 값 객체, 30종
  유지). 신규 테스트 12건(`domain` 6건, `InMemoryEngineRuntime` 3건,
  `ManagedEngineRuntime` 3건). `pytest` 1234개(신규 12개, 회귀 없음)/
  `ruff`/`mypy`(229 source files) 전부 통과. `.ai/TASKS.md` Milestone
  65 절 신규 추가. `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에
  Engine Learning & Adaptive Routing 서술 추가.

## ADR-0084: Self Optimization — 제외 엔진 자동 복구(Probe) 메커니즘 (Milestone 66)

- 상태: 승인됨 (2026-08-01, AskUserQuestion으로 "M65 제외 엔진의 자동
  복구(재시도) 메커니즘"으로 범위 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M66 self optimization"으로 착수를 요청했다. "Self
  Optimization"은 원래 `.ai/RULES.md` §7 로드맵의 M5 "Self Optimizer"
  (실행 결과 피드백으로 Policy 자체를 개선)를 가리켰으나 M6 이후로
  미뤄진 뒤 그 이름으로는 구현된 적이 없었다(`InMemoryLLMPolicyEngine.
  select()`는 여전히 순수 정적 `dict.get()`, 코드 확인). 조사 중 M65
  자체 로직의 실제 공백도 함께 드러났다: `EngineReliabilityStat.
  is_unreliable()`이 한번 참이 되면 `success_count`가 늘어날 방법이
  없어(제외된 엔진은 다시 선택되지 않으므로 `record()` 자체가 호출되지
  않는다) 영구히 후보에서 제외된다 — 근본 원인이 고쳐진 엔진도 재선택될
  길이 없었다(추측 아님, 코드 확인).
- 결정:
  1. AskUserQuestion으로 세 선택지(a. M65 제외 엔진 자동 복구/재시도,
     b. `LLMPolicyEngine` 자체의 Self Optimizer, c. 둘 다)를 제시하고
     사용자가 (a)를 선택 — 원래 M5 개념(b)은 이번 범위에서 명시적으로
     제외한다.
  2. 새 Interface를 추가하지 않고 기존 `EngineReliabilityStat`(M65)만
     확장한다 — `skip_count: int` 필드 + `skip()`(제외될 때마다 호출,
     다른 필드는 유지) + `is_probe_eligible()`(`skip_count >=
     _PROBE_INTERVAL`) 메서드를 추가한다.
  3. `_PROBE_INTERVAL = 5`(모듈 상수) — 제외된 엔진이 5번 연속 후보에서
     빠지면 다음 선택에서 한 번 더 후보로 포함해(probe) 복구 여부를
     재확인한다.
  4. `record()`는 실행 결과(성공/실패)와 무관하게 `skip_count`를 0으로
     되돌린다 — probe가 성공하면 `is_unreliable()`이 거짓이 되어 정상
     복귀하고, 다시 실패하면 다음 probe까지 또 5번의 쿨다운을 거친다.
  5. `InMemoryEngineRuntime._build_candidates()`/
     `ManagedEngineRuntime._require_adapter()`의 제외 조건을
     `is_unreliable()`에서 `is_unreliable() and not is_probe_eligible()`
     로 바꾸고, 제외될 때마다 `self._engine_reliability[name] =
     stat.skip()`으로 갱신한다.
  6. `EngineSelectionPolicy`(M17) Decision-Only 계약은 M64/M65와
     동일하게 무변경 — 필터링은 계속 `EngineRuntime`의 책임으로 둔다.
- 대안:
  1. 시간 기반 쿨다운(예: N초 경과 후 재시도) — 기각: 이 프로젝트는
     `EngineRuntime` 내부에 실시간 시계 의존성을 두지 않는 순수 결정론적
     규칙만 써 왔다(M49/M65와 동일 판단). 선택 시도 횟수 기반 카운터가
     테스트하기도 더 쉽고 이 프로젝트의 기존 패턴과 일관된다.
  2. probe 전용 별도 정책/Interface 신설 — 기각: YAGNI. 기존
     `EngineReliabilityStat` 필드 2개(스킵 카운트, 판정 메서드) 추가로
     충분하며, `EngineSelectionPolicy` 계약을 건드릴 필요가 없다.
  3. `LLMPolicyEngine` Self Optimizer(원래 M5 개념)까지 함께 구현 —
     기각: 사용자가 AskUserQuestion에서 명시적으로 이번 범위에서
     제외하고 M65 공백 해소만 선택했다. 별도 Milestone 후보로 남긴다.
- 이유: M65가 남긴 "한번 제외되면 영구 제외" 공백은 실제로 존재하는
  버그에 가까운 설계 공백이었다 — 일시적 장애로 제외된 엔진이 복구돼도
  다시 쓰일 길이 없었다. 기존 `EngineReliabilityStat`의 필드 구성만
  확장하는 최소 변경으로 이 공백을 메우면서, `EngineSelectionPolicy`/
  `EngineRuntime` 공개 계약과 하위 호환성은 그대로 유지된다.
- 결과/영향: `domain/engine_reliability.py`(`EngineReliabilityStat`에
  `skip_count`/`skip()`/`is_probe_eligible()` 추가, `_PROBE_INTERVAL`
  모듈 상수 신규), `runtime/engine/engine_runtime.py`
  (`InMemoryEngineRuntime._build_candidates()`),
  `runtime/engine/managed_engine_runtime.py`
  (`ManagedEngineRuntime._require_adapter()`) 수정. 새 Core Domain
  Interface 없음(30종 유지). 신규 테스트 8건(`domain` 4건,
  `InMemoryEngineRuntime` 2건, `ManagedEngineRuntime` 2건). `pytest`
  1242개(신규 8개, 회귀 없음)/`ruff`/`mypy`(229 source files) 전부
  통과. `.ai/TASKS.md` Milestone 66 절 신규 추가. `docs/ARCHITECTURE.md`
  §3.9 Engine Runtime 절에 Self Optimization 서술 추가.

## ADR-0085: LLMPolicyEngine Self Optimizer — 실행 결과 기반 정책 자동 대체 (Milestone 67)

- 상태: 승인됨 (2026-08-01, AskUserQuestion 4회로 범위·집계 단위·대체
  소스·피드백 경로를 순차 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M67 self optimization"으로 착수를 요청했다. ADR-0084
  (M66)가 "LLMPolicyEngine Self Optimizer(원래 `.ai/RULES.md` §7 M5
  개념)"를 명시적으로 범위 밖으로 미루고 별도 Milestone 후보로 남겨
  두었던 항목이다. 조사 결과 `InMemoryLLMPolicyEngine.select()`는
  M5-T01 이후 줄곧 순수 정적 `dict.get()`이었고(코드 확인), `AgentSession.
  llm_policy_decision`은 `CodingAgent`/`ReviewAgent`/`DocumentationAgent`
  가 `engine_runtime.run()`에 실제로 전달해 실행 결과(`EngineResult.
  success`)까지 만들어내지만, 그 결과가 정책으로 되먹여지는 경로는
  전혀 없었다(Role+Decision+Outcome이 한 곳에 모이는 지점은 이 3개
  Agent의 `engine_runtime.run()` 직후뿐).
- 결정:
  1. AskUserQuestion으로 범위를 확정: (a) 관측만, (b) 관측 + 자동 대체,
     (c) 관측 + 자동 대체 + Probe 복구까지 한 번에 — 사용자가 (b)를
     선택. M65/M66이 관측→복구를 두 Milestone으로 나눈 전례와 동일하게
     Probe/자동 복구는 이번 범위에서 제외하고 별도 Milestone 후보로
     남긴다.
  2. 집계 단위는 `(AgentRole, LLMModel)` 조합으로 확정 — Role 단독
     집계는 모델 전환 후에도 이전 모델의 실패 이력과 새 모델의 이력이
     뒤섞여 "자동 대체"가 의미를 갖지 못한다.
  3. 대체 소스는 기존 `domain/llm_policy.py`의 `INITIAL_MODELS` 시드
     목록 순서상 다음 모델로 확정 — 새 설정 파일/로더 확장 없이 이미
     있는 데이터를 재사용한다(YAGNI).
  4. 피드백 경로는 `CodingAgent`/`ReviewAgent`/`DocumentationAgent`가
     `engine_runtime.run()` 직후 명시적으로 호출하는 방식으로 확정 —
     `EngineRuntime`이 `LLMPolicyEngine`을 주입받아 자동 기록하는
     대안은 engine 계층이 policy 계층을 알아야 하는 새 계층 의존
     방향이 생겨 기각.
  5. `domain/llm_policy_reliability.py`(신규)에 `LLMPolicyReliabilityStat`
     (total/success_count/failure_count)을 신설한다 — M65
     `EngineReliabilityStat`과 필드 구성·임계값 규칙(`success_count ==
     0 and total >= 3`)을 동일하게 재사용하되, 이번 범위에서 제외한
     `skip_count`/Probe 필드는 가져오지 않는다.
  6. `LLMPolicyEngine` interface에 `record_outcome(role, decision,
     success) -> None` abstract method를 추가한다 — `select()`의
     "side-effect 없음(read-only)" 계약은 그대로 두고, 결과 기록은
     항상 이 별도 메서드를 통해서만 이루어진다(Interface First, 계약
     명시).
  7. `InMemoryLLMPolicyEngine`이 `dict[(AgentRole, LLMModel),
     LLMPolicyReliabilityStat]`과 role별 "현재 활성 Decision" 재정의를
     내부 상태로 갖는다. `select(role)`은 활성 Decision의 `(role,
     model)` 통계가 `is_unreliable()`이면 `INITIAL_MODELS` 순서상 다음
     모델로 전환한 Decision(effort는 원래 값 유지)을 반환하고 그 값을
     활성 Decision으로 저장한다. 이미 목록의 마지막 모델이면 더 이상
     전환하지 않는다(Probe 없이 그대로 유지 — 순환하면 이미 실패한
     모델을 다시 쓰게 될 뿐이다).
  8. `AgentRuntime`에 `record_llm_policy_outcome(session_id, success)`을
     추가한다 — `llm_policy_engine` 미주입이거나 해당 session에 결정된
     policy가 없으면 no-op. 3개 Agent는 `LLMPolicyEngine` interface를
     직접 참조하지 않고 이 메서드 하나만 호출한다(M5-T02가 세운 "Agent는
     LLMPolicyEngine을 모른다" 경계를 그대로 유지, `agent_runtime`을
     생성자에서 저장하는 필드만 3곳에 추가).
  9. 영속 저장소는 M49/M50/M65와 동일하게 이번 범위 밖(in-process
     한정, YAGNI).
- 대안:
  1. `LLMPolicyEngine.select()` 시그니처에 실행 결과를 파라미터로
     추가 — 기각: "규칙 조회는 read-only"라는 M5-T01 계약을 깨고, 모든
     호출부가 매번 직전 결과를 들고 다녀야 해 더 큰 변경이 된다. 별도
     `record_outcome()` 메서드가 훨씬 작은 변경이다.
  2. Role 단독 키로 집계 — 기각: 자동 대체 이후에도 이전/새 모델의
     실패가 뒤섞여 대체가 무의미해진다(위 결정 2 참고).
  3. `docs/llm_policy.example.yaml`/`storage/llm_policy_loader.py`를
     확장해 Role별 명시적 fallback 목록을 설정 가능하게 함 — 기각:
     로더/스키마 변경이 필요해 범위가 커진다. `INITIAL_MODELS` 재사용만
     으로 새 설정 없이 동일한 목표를 달성할 수 있다(YAGNI).
  4. Effort만 단계적으로 낮춤(모델은 유지) — 기각: 사용자가 "다음
     모델로 전환"을 명시적으로 선택. 초기 실패 원인이 Provider 장애 등
     모델 자체 문제인 경우 effort만 낮춰서는 회복되지 않는다.
  5. `EngineRuntime`이 `LLMPolicyEngine`을 주입받아 자동 기록 — 기각:
     `runtime/engine/`이 정책 계층을 알아야 하는 새 의존 방향이
     생긴다(M65/ADR-0083이 `intelligence/` 의존을 피하려고 별도 domain
     타입을 만든 것과 같은 계층 경계 원칙).
  6. M65/M66처럼 Probe 기반 자동 복구까지 이번 범위에 포함 — 기각:
     사용자가 AskUserQuestion에서 "관측 + 자동 대체"만 선택. M65/M66이
     의도적으로 두 Milestone으로 나눈 전례와 일관되게, 복구 메커니즘은
     별도 Milestone 후보로 남긴다.
- 이유: `.ai/RULES.md` §7 M5 로드맵이 원래 의도했던 "실행 결과 피드백
  으로 정책 자체를 개선"을 M65/M66이 엔진 계층에서 이미 검증한 패턴
  (임계값 재사용, 별도 domain 값 객체, 기존 Interface 무변경)을 정책
  계층에 그대로 이식해 구현했다. `select()`의 read-only 계약과
  `LLMPolicyEngine` interface의 최소 확장(메서드 1개 추가)만으로 자동
  대체를 달성해 하위 호환성을 해치지 않는다.
- 결과/영향: `domain/llm_policy_reliability.py`(신규),
  `interfaces/llm_policy_engine.py`(`record_outcome()` abstract method
  추가), `engines/llm_policy_engine.py`(`InMemoryLLMPolicyEngine`에
  통계·활성 Decision 상태 + 자동 대체 로직), `runtime/agent/agent_runtime.py`
  (`record_llm_policy_outcome()` 추가), `agents/coding_agent.py`/
  `review_agent.py`/`documentation_agent.py`(`engine_runtime.run()`
  직후 피드백 호출 + `agent_runtime` 필드 저장) 수정.
  `tests/interfaces/fakes.py`의 `FakeLLMPolicyEngine`에 `record_outcome()`
  구현 추가. 새 Core Domain Interface 없음(기존 `LLMPolicyEngine`
  확장, 30종 유지). 신규 테스트 11건(`domain` 5건, `engines` 대체
  로직 관련 다수 확장, `interfaces` 1건, `AgentRuntime` 3건 — 정확한
  분해는 `.ai/TASKS.md` Milestone 67 참고). `pytest` 1259개(신규 11개,
  회귀 없음)/`ruff`/`mypy`(230 source files) 전부 통과. `.ai/TASKS.md`
  Milestone 67 절 신규 추가. `docs/ARCHITECTURE.md` §3.9에 Self
  Optimization(정책 계층) 서술 추가, §7 Interface 표의 `LLMPolicyEngine`
  행에 M67 확장 반영.

## ADR-0086: Dynamic Ensemble Routing — EngineSelectionPolicy 기반 top-N 자동 선택 (Milestone 68)

- 상태: 승인됨 (2026-08-01)
- 날짜: 2026-08-01
- 배경: 사용자가 "M68 Dynamic Ensemble Routing"으로 명확한 범위를 담아
  착수를 요청했다 — `run_ensemble()`(M62, ADR-0080)은 호출자가
  `engine_names`를 직접 나열해야 하는 계약이라, M64/M65/M66에서
  `run()`/`estimate_cost()` 경로에 이미 구현된 `EngineSelectionPolicy`
  기반 비용·신뢰도 인식 선택을 전혀 활용하지 못했다(코드 확인, 추측
  아님) — 같은 Task를 여러 엔진에 "동적으로" 분산하는 경로가 없었다.
- 결정:
  1. 새 Core Domain Interface를 추가하지 않고 기존 `EngineRuntime`에
     `run_ensemble_auto(task, required_capabilities=frozenset(), *,
     top_n=2, model=None) -> dict[str, EngineResult]` abstract method
     하나만 추가한다.
  2. `InMemoryEngineRuntime`/`ManagedEngineRuntime`은 `run()`/
     `estimate_cost()`가 이미 쓰는 후보 선정 로직(`_build_candidates()`,
     `ManagedEngineRuntime`은 이번에 `_require_adapter()`에서 이 부분을
     별도 메서드로 추출해 재사용)으로 `EngineCandidate` 목록을 만든다 —
     M65/M66의 신뢰도 기반 제외·Probe 규칙이 후보 빌드 단계에서 자동으로
     함께 적용된다.
  3. `engine_selection_policy`가 주입돼 있으면 `EngineSelectionPolicy.
     select()`(M17)를 반복 호출해(매 회 직전 선택 후보를 후보 목록에서
     제거) top_n개를 얻는다 — "예산 내 최저 비용 하나"를 고르는 기존
     규칙을 그대로 반복 적용할 뿐, `EngineSelectionPolicy` 시그니처는
     전혀 바꾸지 않는다(Decision Only 계약 유지).
  4. 정책 미주입 시에는 `run()`의 "등록 순서상 첫 매칭" 원칙을 그대로
     확장해 조건을 만족하는 첫 top_n개를 고른다 — 100% 하위 호환.
  5. 선택된 이름 목록은 새 실행 로직을 만들지 않고 기존 `run_ensemble()`
     (M62의 `ThreadPoolExecutor` 동시 실행 + 개별 엔진 실패 격리)에
     그대로 위임한다(YAGNI).
  6. `required_capabilities`를 만족하며 신뢰도상 제외되지 않는 등록된
     엔진이 하나도 없으면(`top_n >= 1`인 경우) `run()`과 동일하게
     `NoSuitableEngineError`를 전파한다 — 선택 단계 오류와 개별 엔진의
     실행 실패(결과로만 격리)를 구분하는 기존 원칙을 그대로 따른다.
  7. `top_n < 1`이면 후보를 조회하지 않고 빈 dict를 반환한다(`run_ensemble()`
     의 "engine_names가 비어 있으면 빈 dict" 계약과 대칭).
  8. `RecoveringEngineRuntime`은 `run_ensemble()`과 동일한 이유(비교
     대상인 개별 결과를 재시도로 덮어쓰면 안 됨)로 재시도 없이 내부
     Runtime에 그대로 위임한다.
- 대안:
  1. `run_ensemble()` 자체의 시그니처를 `engine_names: list[str] | None`
     으로 바꿔 `None`이면 자동 선택하도록 확장 — 기각: 하나의 메서드가
     "명시적 지정"과 "동적 선택"이라는 서로 다른 계약을 함께 가지면
     반환 dict의 key 집합이 입력과 항상 같다는 기존 `run_ensemble()`의
     계약(§ "언제나 engine_names와 같다")이 깨진다. 별도 메서드가 기존
     계약을 그대로 보존한다.
  2. 새 `EnsembleRoutingPolicy` interface를 별도로 추가 — 기각: 사용자가
     명시적으로 "새 Core Domain Interface는 추가하지 말고" 요청했고,
     top-N 선택은 기존 `EngineSelectionPolicy.select()`를 반복 호출하는
     것만으로 충분해 새 계약을 정당화할 필요성이 없다(YAGNI).
  3. `EngineSelectionPolicy.select()`에 `top_n` 파라미터를 추가해 정책
     구현체가 직접 목록을 반환하도록 확장 — 기각: M17 "Decision Only,
     단일 선택" 계약과 기존 호출부(Automation 파이프라인 등 단일 선택만
     쓰는 곳)에 영향을 준다. `EngineRuntime` 쪽에서 반복 호출하는 편이
     기존 계약을 하나도 건드리지 않는다.
  4. `EngineRegistry`를 통해 후보를 다시 조회 — 기각: ADR-0082(M64)가
     이미 같은 이유로 기각한 대안과 동일 — `EngineRuntime`은 자체
     `self._engines` dict로 이미 관리하므로 이중 관리가 된다.
- 이유: `EngineSelectionPolicy.select()`가 이미 "후보 목록 중 최적 하나"
  를 검증된 형태로 판단하므로, 그 후보 목록에서 직전 선택을 제거하며
  반복 호출하면 새 랭킹 알고리즘 없이 top-N을 얻을 수 있다. `run_ensemble()`
  의 실행/격리 메커니즘도 그대로 재사용해, 이번 Milestone은 순수하게
  "후보를 어떻게 정할지"만 다루는 최소 확장으로 끝난다.
- 결과/영향: `interfaces/engine_runtime.py`(abstract method 추가),
  `runtime/engine/engine_runtime.py`(`InMemoryEngineRuntime`),
  `runtime/engine/managed_engine_runtime.py`(`ManagedEngineRuntime`,
  `_build_candidates()` 추출), `runtime/engine/recovering_engine_runtime.py`
  (`RecoveringEngineRuntime`, 위임) 수정. 새 abstract method 추가로
  기존 `EngineRuntime` 테스트 더블(`tests/interfaces/fakes.py`
  `FakeEngineRuntime`, `tests/runtime/engine/test_recovering_engine_runtime.py`
  `ScriptedEngineRuntime`, `tests/core/test_workspace_core.py`
  `SpyEngineRuntime`, `tests/agents/test_coding_agent.py`
  `RecordingEngineRuntime`)에도 최소 구현을 추가했다(ABC 계약 충족
  목적, 대부분 미사용 경로는 기존 관례대로 `NotImplementedError`/
  `AssertionError`). 새 Core Domain Interface 없음(기존 `EngineRuntime`
  확장, 30종 유지). 신규 테스트 15건(`InMemoryEngineRuntime` 7건,
  `ManagedEngineRuntime` 7건, `RecoveringEngineRuntime` 1건 — 정확한
  분해는 `.ai/TASKS.md` Milestone 68 참고). `pytest` 1274개(신규 15개,
  회귀 없음)/`ruff`/`mypy`(230 source files) 전부 통과. `.ai/TASKS.md`
  Milestone 68 절 신규 추가. `docs/ARCHITECTURE.md` §3.9 Engine Runtime
  절에 Dynamic Ensemble Routing 서술 추가.

## ADR-0087: Execution Memory & Context Routing — 실행 결과 기반 Engine 추천 (Milestone 69)

- 상태: 승인됨 (2026-08-01, AskUserQuestion 4회로 유사도 기준·저장
  위치·반영 방식·지표 범위를 순차 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M69 Execution Memory & Context Routing"으로 착수를
  요청했다 — M68까지 `EngineSelectionPolicy`(M17)/`EngineReliabilityStat`
  (M65)는 "이 엔진이 전반적으로 신뢰할 만한가/저렴한가"만 판단할 뿐,
  "이 종류의 Task에서 어떤 Engine이 더 잘 수행했는가"를 기억해 다음
  실행에 반영하는 경로는 없었다(코드 확인, 추측 아님).
- 결정:
  1. AskUserQuestion으로 유사도 판단 키를 확정: domain.Task에는
     TaskType/난이도 필드가 없고 `EngineRuntime`은 `required_
     capabilities`만 받으므로, Role/TaskType까지 포함하려면 `run()`/
     `run_parallel()`/`run_ensemble_auto()` 전체 시그니처에 새 파라미터가
     필요해 범위가 커진다 — 사용자가 `required_capabilities` 조합만
     사용하는 안(권장)을 선택.
  2. 저장 위치는 새 domain 값 객체 + `EngineRuntime` in-process 상태로
     확정 — 기존 `ExecutionMemoryStore`(M39, `memory/
     execution_memory_store.py`)는 `RecommendationExecutionService`
     (Execution Platform) 전용의 완전히 분리된 경로(ADR-0053,
     ARCHITECTURE.md §8 규칙 14)라, `EngineRuntime`(Agent 경로)에서
     직접 재사용하면 이미 확정된 계층 경계가 깨진다. `EngineReliabilityStat`
     (M65)와 동일한 패턴(도메인 값 객체 + in-process dict)만 재사용한다.
  3. `domain/engine_execution_memory.py`(신규)에
     `EngineExecutionMemoryStat`(total/success_count/failure_count/
     total_latency_seconds)을 신설한다 — `EngineReliabilityStat`과
     필드 구성은 같지만 집계 키가 `(required_capabilities, engine_name)`
     조합이라는 점이 다르다(엔진 이름 단독 키인 M65와 달리 "같은 종류의
     Task에서만" 비교). `success_rate()`는 M49/M65와 동일한 임계값
     (표본 3건 미만이면 `None`)을 재사용한다.
  4. `InMemoryEngineRuntime`/`ManagedEngineRuntime`의 `run()`(Managed는
     Cancel된 경우 제외)/`run_ensemble_auto()`가 실행 결과와 latency를
     `_record_execution_memory()`로 누적한다.
  5. 반영 방식은 "후보 랭킹에 성공률을 반영해 재정렬"로 확정 — 다만
     구현 중 발견한 충돌(아래 참고) 때문에, 문자 그대로 "재정렬"만
     하고 후보를 제외/좁히지는 않는다. `_build_candidates()`가 (기존
     신뢰도 제외 이후) `_reorder_by_execution_memory()`로 후보를 성공률
     내림차순 정렬한다.
  6. latency는 기록만 하고 랭킹 공식에는 반영하지 않는다(사용자 선택,
     새 가중치 공식을 설계하지 않는다, YAGNI).
  7. **설계 충돌과 해결**: 최초 구현("표본 충분 + 최고 성공률 엔진으로
     후보를 좁힘")은 M65 `test_run_with_policy_recovers_after_
     successful_probe`를 깨뜨렸다 — Probe가 성공해 `is_unreliable()`이
     즉시 거짓이 되어도(M66의 "복구 즉시 완전 신뢰" 보장), 과거 실패
     이력이 남아 있는 실행 메모리 성공률이 다른 엔진보다 낮으면 그
     보장이 깨졌다. `EngineSelectionPolicy.select()`가 비용 기준
     `min()`으로 항상 진짜 최저 비용을 고르고, 동률일 때만 순서가
     결과에 영향을 준다는 성질을 이용해, **"후보 제외"가 아니라 "비용
     동률 tie-break로만" 범위를 좁혔다** — 비용이 다른 모든 기존
     M64/M65/M66/M68 테스트는 정렬 순서와 무관하게 그대로 통과한다.
  8. 재정렬 자체도 "표본 부족(미검증)"을 가장 나쁜 값이 아니라
     중립값(`_NEUTRAL_RATE = 0.5`)으로 취급한다 — 그렇지 않으면 아직
     검증되지 않았을 뿐인 엔진이 이미 확인된 저성능(성공률 0.0) 엔진
     보다 부당하게 밀리는 새 버그가 생긴다(구현 중 테스트로 발견해
     즉시 수정).
  9. 신뢰도 제외와 동일하게 `engine_selection_policy` 주입 경로에서만
     적용된다 — 미주입 시(M64 이전 동작) 100% 하위 호환.
  10. `RecoveringEngineRuntime`은 변경 없음(순수 위임 구조 그대로).
  11. 영속 저장소는 M49/M50/M65와 동일하게 이번 범위 밖(in-process
      한정, YAGNI).
- 대안:
  1. 기존 `ExecutionMemoryStore`/`MemoryEngine`(M39) 재사용 — 기각:
     ARCHITECTURE.md §8 규칙 14가 이미 "완전히 별도의 경로"로 분리해
     둔 Agent 경로와 Execution Platform 경로를 다시 합치게 된다.
  2. Role까지 포함한 유사도 키 — 기각: `EngineRuntime`의 `run()`/
     `run_parallel()`/`run_ensemble_auto()` 전체에 새 `role` 파라미터를
     추가해야 해 인터페이스 변경 범위가 M69의 "최소 확장" 취지를
     벗어난다.
  3. 조회 전용 `recommend_engine()` 메서드만 추가하고 실제 선택 로직은
     바꾸지 않음 — 기각: 사용자가 "다음 실행에 반영"을 명시적으로
     요구했고, 단순 조회 API는 그 요구를 충족하지 못한다.
  4. 성공률+평균 latency 가중 합산 랭킹 — 기각: 사용자가 성공/실패만
     반영하는 안을 선택. 가중치 공식(합산 비율)을 새로 설계해야 해
     범위가 커진다.
  5. 표본 충분 시 최고 성공률 엔진으로 후보를 제외/좁힘(최초 구현) —
     기각(구현 중 회귀 발견 후 철회): M65/M66의 "복구 즉시 완전 신뢰"
     보장과 충돌해 기존 통과 테스트가 깨졌다. tie-break 재정렬로
     범위를 좁혀 이 충돌을 해소했다.
- 이유: `EngineReliabilityStat`(M65)이 이미 "표본 부족 시 성급하게
  판단하지 않는다"는 임계값 규칙을 검증된 형태로 갖고 있었으므로, 같은
  패턴을 `(required_capabilities, engine_name)` 키로 재사용하면 새
  알고리즘 없이 "Task 종류별 Engine 성과 기억"이라는 공백을 메울 수
  있었다. `EngineSelectionPolicy`의 비용 `min()`이 동률에서만 순서에
  의존한다는 성질을 활용해 재정렬 범위를 tie-break로 좁힘으로써, 기존
  M64~M68의 모든 확정된 동작(비용 우선, 신뢰도 제외, Probe 복구)을
  전혀 건드리지 않고 새 신호를 안전하게 추가할 수 있었다.
- 결과/영향: `domain/engine_execution_memory.py`(신규),
  `runtime/engine/engine_runtime.py`(`InMemoryEngineRuntime`),
  `runtime/engine/managed_engine_runtime.py`(`ManagedEngineRuntime`)
  수정. `RecoveringEngineRuntime` 무변경. 새 Core Domain Interface 없음
  (기존 `EngineRuntime`의 내부 구현만 확장, 30종 유지). 신규 테스트
  12건(`domain` 7건, `InMemoryEngineRuntime` 2건, `ManagedEngineRuntime`
  2건 — 정확한 분해는 `.ai/TASKS.md` Milestone 69 참고). `pytest` 1286개
  (신규 12개, 회귀 없음)/`ruff`/`mypy`(231 source files) 전부 통과.
  `.ai/TASKS.md` Milestone 69 절 신규 추가. `docs/ARCHITECTURE.md`
  §3.9 Engine Runtime 절에 Execution Memory & Context Routing 서술 추가.

## ADR-0088: Adaptive Consensus — Consensus 합의 이력 기반 가중 투표 (Milestone 70)

- 상태: 승인됨 (2026-08-01, AskUserQuestion 4회로 이력 의미·저장 위치·
  반영 방식·인터페이스 변경 범위를 순차 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M70 Adaptive Consensus"로 착수를 요청했다 — M69까지는
  과거 실행 이력을 바탕으로 Engine/Ensemble 선택 자체는 학습하지만,
  `run_ensemble()`(M62) 결과를 합치는 `ResultAggregator`(M63,
  `MajorityVoteAggregator`)는 `EngineResult.output`의 정확한 문자열
  일치 다수결(표 개수)만 본다 — 어떤 엔진의 표가 과거에 실제 합의와
  자주 일치했는지는 전혀 반영하지 않는다(코드 확인, 추측 아님).
- 결정:
  1. AskUserQuestion으로 "Consensus 성공 이력"의 의미를 확정: M69의
     `EngineExecutionMemoryStat`(태스크 실행 성공/실패)을 그대로
     재사용하는 안과, 엔진의 투표가 최종 합의와 일치했는지를 추적하는
     새 이력을 만드는 안 중 사용자가 후자(권장)를 선택했다 — "실행
     성공"과 "투표가 다수 의견에 속함"은 서로 다른 신호이기 때문이다
     (실행은 성공했지만 소수 의견일 수 있다).
  2. 저장 위치는 M65/M69와 동일한 패턴(`EngineRuntime` in-process
     상태)으로 확정 — 새 `domain/consensus_agreement.py`에
     `ConsensusAgreementStat`(total/agree_count/disagree_count,
     `agreement_rate()`는 M49/M65/M69와 동일한 최소 표본 3건 임계값)을
     신설하고, `InMemoryEngineRuntime`/`ManagedEngineRuntime`에
     `(required_capabilities, engine_name)` 키의 `_consensus_agreement`
     dict로 누적한다.
  3. `EngineRuntime`에 `record_consensus_outcome(required_capabilities,
     agreeing_engines, dissenting_engines)`(기록, side-effect)와
     `consensus_weight(required_capabilities, engine_name)`(조회,
     read-only — 표본 부족/기록 없음이면 중립값 0.5)을 최소 확장한다.
     `EngineRuntime`은 `ResultAggregator`의 존재를 모른 채로 남는다
     (ADR-0080/0081이 이미 명시한 두 계약 간 결합 방지 원칙 유지) — 이
     두 메서드만이 유일한 접점이다.
  4. 반영 방식은 "가중치 합계 비교"로 확정 — 새 `ResultAggregator`
     구현체 `AdaptiveConsensusAggregator`(생성자로 `EngineRuntime`과
     `required_capabilities`를 주입받음)가 `votes`를 표 개수 대신
     `consensus_weight()` 합계로 비교해 승자를 정하고, 동률이면(M63과
     동일하게) 표 개수 → 입력 순서로 2차 tie-break한다. 신뢰도 낮은
     엔진의 표를 아예 제외하는 필터링 방식은 채택하지 않았다 — M69에서
     "제외/필터링" 방식이 M65/M66 회귀를 일으켰던 전례를 반복하지
     않기 위해서다.
  5. 기존 `ResultAggregator` 인터페이스는 무변경으로 확정 — `aggregate()`
     시그니처·반환 타입에 손대지 않고 새 클래스만 추가한다.
     `MajorityVoteAggregator`를 포함한 기존 구현체·호출자는 전혀
     영향받지 않는다(100% 하위 호환).
  6. `AdaptiveConsensusAggregator.aggregate()`는 승자를 정한 직후 자신이
     계산한 `agreeing_engines`/`dissenting_engines`를
     `record_consensus_outcome()`으로 그대로 되돌려준다 — 호출자가
     별도로 기록을 챙기지 않아도 다음 호출부터 자동으로 학습이
     누적된다. `failed_engines`(성공하지 못해 애초에 투표하지 못한
     엔진)는 기록 대상에서 제외한다 — 합의 자체에 참여하지 않았기
     때문이다.
  7. `RecoveringEngineRuntime`은 두 메서드 모두 내부 Runtime에 순수
     위임한다 — 재시도와 무관한 read/write 상태이기 때문이다(M62/M68과
     동일한 근거).
  8. 영속 저장소는 M49/M50/M65/M69와 동일하게 이번 범위 밖(in-process
     한정, YAGNI).
- 대안:
  1. M69 `EngineExecutionMemoryStat`(태스크 실행 성공률)을 그대로 투표
     가중치로 재사용 — 기각: 사용자가 "Consensus 성공 이력을 재사용"을
     명시적으로 요구했고, "실행 성공"과 "투표가 합의와 일치"는 의미가
     다른 신호라 재사용 시 혼란을 야기할 수 있어 별도 값 객체로
     분리하는 안(권장)을 선택했다.
  2. `ResultAggregator` 인스턴스 자체가 상태를 들고 다님(EngineRuntime과
     완전 독립) — 기각: 여러 aggregator 인스턴스 간 이력 공유가 안
     되고, M65/M69가 이미 확립한 "EngineRuntime이 상태를 갖고 조회
     메서드를 노출" 패턴과 어긋난다.
  3. 신뢰도 낮은 엔진 표를 집계에서 아예 제외(필터링) — 기각: M69의
     "narrow candidates" 최초 시도가 M65/M66 회귀를 일으켰던 전례가
     있어, 위험이 검증된 tie-break/가중합 방식(권장안)만 채택했다.
  4. `aggregate()`에 optional `weights` 매개변수 추가 — 기각: 사용자가
     "무변경, 새 클래스만 추가"를 선택했다. 기존 시그니처를 건드리면
     `ResultAggregator`를 구현하는 모든 클래스(현재와 향후)가 새
     매개변수를 알아야 해 계약 변경 범위가 M70의 "최소 확장" 취지를
     벗어난다.
- 이유: `EngineReliabilityStat`(M65)/`EngineExecutionMemoryStat`(M69)이
  이미 검증한 "in-process dict + 최소 표본 임계값 + 중립값 처리" 패턴을
  그대로 재사용하면, `ResultAggregator`/`EngineRuntime` 두 계약의
  시그니처를 전혀 바꾸지 않고도 "과거 합의에 자주 참여한 엔진의 표를
  더 무겁게 반영"이라는 새 요구를 안전하게 추가할 수 있었다. `EngineRuntime`
  이 `ResultAggregator`를 모르는 기존 결합 방지 원칙(ADR-0080/0081)도
  "기록/조회 메서드 2개"로만 접점을 좁혀 그대로 유지했다.
- 결과/영향: `domain/consensus_agreement.py`(신규),
  `interfaces/engine_runtime.py`(`record_consensus_outcome()`/
  `consensus_weight()` abstract method 2개 추가),
  `runtime/engine/engine_runtime.py`(`InMemoryEngineRuntime`),
  `runtime/engine/managed_engine_runtime.py`(`ManagedEngineRuntime`),
  `runtime/engine/recovering_engine_runtime.py`(순수 위임 2개 추가),
  `runtime/engine/result_aggregator.py`(`AdaptiveConsensusAggregator`
  신규 클래스) 수정. 테스트 더블(`tests/interfaces/fakes.py`
  `FakeEngineRuntime`, `tests/core/test_workspace_core.py`
  `SpyEngineRuntime`, `tests/agents/test_coding_agent.py`
  `RecordingEngineRuntime`, `tests/runtime/engine/
  test_recovering_engine_runtime.py` `ScriptedEngineRuntime`) 모두
  새 abstract method 2개에 대한 최소 구현/스텁 추가. 새 Core Domain
  Interface 없음(기존 `EngineRuntime`의 메서드 2개 확장 + 기존
  `ResultAggregator` 계약 재사용, 30종 유지). 신규 테스트 18건(`domain`
  5건, `InMemoryEngineRuntime` 5건, `ManagedEngineRuntime` 3건,
  `ResultAggregator` 4건, `RecoveringEngineRuntime` 1건). `pytest`
  1304개(신규 18개, 회귀 없음)/`ruff`/`mypy`(232 source files) 전부
  통과. `.ai/TASKS.md` Milestone 70 절 신규 추가. `docs/ARCHITECTURE.md`
  §3.9 Engine Runtime 절 및 §7 인터페이스 표(`EngineRuntime`/
  `ResultAggregator`)에 Adaptive Consensus 서술 추가.

## ADR-0089: Workflow Learning — 성공률 높은 실행 순서(Template) 추천 (Milestone 71)

- 상태: 승인됨 (2026-08-01, AskUserQuestion 4회로 유사도 기준·반영
  방식·저장 위치·최소 표본 기준을 순차 확정)
- 날짜: 2026-08-01
- 배경: 사용자가 "M71 Workflow Learning"으로 착수를 요청했다. 최신 main
  기준(`origin/main` = `831ef11`)에서 시작했고 이미 그 커밋을 포함하고
  있어 별도 병합이 필요 없었다. 조사 결과 "Workflow"라는 용어는 이
  코드베이스에 두 갈래로 존재한다 — (a) `domain.Workflow`/`WorkflowEngine`
  /`WorkflowRunner`(Milestone 2/12, task_ids+dependencies 기반 DAG와
  그 위상 정렬·순차 실행), (b) M34(ADR-0048)가 "Workflow"를 `domain.
  Workflow`가 아니라 Milestone Task 실행 흐름으로 재정의한 Intelligence
  경로(`intelligence/workflow_flow.py`, `domain.Workflow`/`WorkflowEngine`
  무변경). 사용자 요청이 "WorkflowEngine"을 명시적으로 지목했으므로
  (a) 경로가 대상임을 확인했다. `WorkflowEngine.plan()`은 의존관계를
  만족하는 위상 정렬만 계산하는 순수 계산이었고, 실행 결과(성공/실패)를
  기억해 다음 계획에 반영하는 경로는 전혀 없었다(코드 확인, 추측 아님).
  "Learning Engine"(M49~M51, ADR-0066/0067/0068)은 `RecommendationAdjustmentAnalyzer`
  /`ExperienceStat` 기반의 완전히 다른 경로(Intelligence/Recommendation)
  라 이번 범위와 무관함을 확인했다.
- 결정:
  1. AskUserQuestion으로 "동일하거나 유사한 Workflow"의 식별 기준을
     확정: `domain.Workflow`에는 이름 있는 템플릿 ID가 없으므로,
     `frozenset(task_ids)` + 의존관계 간선 집합(`frozenset[tuple[str,
     str]]`)을 정확히 일치시키는 키(사용자 선택, 권장안)로 확정했다 —
     M69의 `required_capabilities` 정확 일치 키 패턴을 그대로 재사용해
     새 그래프 유사도 알고리즘을 설계하지 않는다(YAGNI).
  2. 반영 방식은 "성공률 높은 전체 순서를 Template로 저장해 그대로
     추천"으로 확정(사용자 선택, 권장안) — M69/M70의 "tie-break만"
     방식과 달리, 이번에는 서로 충돌하는 기존 보장(M65/M66의 "복구 즉시
     완전 신뢰" 같은)이 없어 더 직접적인 "전체 순서 추천"을 채택해도
     회귀 위험이 없다고 판단했다.
  3. 저장 위치는 "WorkflowEngine in-process 상태 + WorkflowRunner가
     자동 기록"으로 확정(사용자 선택, 권장안) — M65/M69/M70과 동일한
     패턴. `WorkflowEngine`에 `record_run_outcome(workflow, order,
     success)`(기록)/`recommended_order(workflow)`(조회) 두 메서드를
     최소 확장한다. `plan()` 시그니처는 무변경 — 학습 상태는 인스턴스
     내부에서만 조회한다.
  4. 최소 표본 기준은 "기존과 동일하게 3건 이상"으로 확정(사용자 선택,
     권장안) — M49/M65/M69/M70과 동일한 임계값 상수를 그대로 재사용,
     새 임계값을 설계하지 않는다.
  5. `domain/workflow_order_memory.py`(신규)에 `WorkflowOrderStat`
     (total/success_count/failure_count, `success_rate()`는 표본 3건
     미만이면 `None`)을 신설한다 — `EngineReliabilityStat`(M65)/
     `EngineExecutionMemoryStat`(M69)/`ConsensusAgreementStat`(M70)과
     동일한 필드 구성·패턴이지만, 키가 "엔진 이름"이 아니라 "실행
     순서(order tuple) 자체"라는 점이 다르다.
  6. `InMemoryWorkflowEngine.plan()`은 `recommended_order()`가 값을
     반환하면 그 순서를 그대로 반환하고, `None`이면(학습 이력 없음)
     기존 DFS 기반 위상 정렬 그대로 동작한다(100% 하위 호환). 동률이면
     표본 수가 더 많은 순서, 그마저 같으면 먼저 기록된 순서를 반환한다
     (dict 삽입 순서 기반 결정적 tie-break).
  7. `WorkflowRunner.run()`이 완료 직후(성공/실패 모두) 실제로 쓰인
     `order`와 결과를 `record_run_outcome()`으로 자동 기록한다 —
     호출자가 별도로 학습을 챙기지 않아도 다음 `plan()` 호출부터
     반영된다(M70의 `AdaptiveConsensusAggregator` 자동 되먹임과 동일한
     설계).
  8. `WorkflowEngine`의 유일한 다른 구현체인 `FakeWorkflowEngine`
     (`tests/interfaces/fakes.py`)은 두 메서드를 최소 스텁(기록은
     no-op, 조회는 항상 `None`)으로 구현해 기존 테스트 동작을 그대로
     유지한다.
  9. 영속 저장소는 M49/M50/M65/M69/M70과 동일하게 이번 범위 밖
     (in-process 한정, YAGNI).
- 대안:
  1. 구조적 시그니처(task 개수 + 의존관계 그래프 모양, task_id 값 무시)
     — 기각: 그래프 동형(isomorphism) 비교 로직을 새로 설계해야 해
     범위가 M71의 "최소 확장" 취지를 벗어난다.
  2. mission_id 기준 — 기각: Mission이 재실행되는 시나리오에만
     적용되고, 이름은 다르지만 구조가 반복되는 파이프라인 패턴은
     학습되지 않는다.
  3. 위상정렬 동점(tie) 상황에서만 Task별 성공률로 재정렬(M69/M70과
     동일한 tie-break 방식) — 기각(사용자가 더 직접적인 "전체 순서
     추천" 방식을 선택): "실행 순서(Workflow Template)를 추천"이라는
     요구사항을 tie-break보다 더 직접적으로 충족하고, 이번 범위에는
     tie-break로 좁혀야 할 만한 기존 충돌 사례가 없었다.
  4. 새 domain 값 객체를 `MemoryEngine`(M1)에 저장 — 기각:
     `WorkflowEngine`과의 연결고리가 없어 `plan()`이 그 기록을 조회할
     방법이 없다(추천 자체가 동작하지 않는다).
  5. 첫 성공 1건부터 즉시 추천 — 기각(사용자가 기존 임계값 재사용을
     선택): 표본 부족 상태에서 우연한 1회 성공 순서에 과도하게
     의존하는 위험을 M49/M65/M69/M70과 동일하게 피한다.
- 이유: `EngineReliabilityStat`(M65)/`EngineExecutionMemoryStat`(M69)/
  `ConsensusAgreementStat`(M70)이 이미 검증한 "in-process dict + 정확한
  frozenset 키 + 최소 표본 3건" 패턴을 그대로 `WorkflowEngine`에
  옮기면, `plan()`/`WorkflowRunner.run()`의 기존 시그니처를 전혀 바꾸지
  않고도 "성공률 높은 실행 순서를 Template로 기억해 추천"이라는 새
  요구를 안전하게 추가할 수 있었다. `WorkflowEngine`이 `EventBus`를
  몰라야 한다는 §8 계층 규칙, `WorkflowRunner`가 Agent가 아니라는
  ADR-0023의 경계도 전혀 건드리지 않았다.
- 결과/영향: `domain/workflow_order_memory.py`(신규),
  `interfaces/workflow_engine.py`(`record_run_outcome()`/
  `recommended_order()` abstract method 2개 추가),
  `engines/workflow_engine.py`(`InMemoryWorkflowEngine`),
  `runtime/workflow/workflow_runner.py`(`WorkflowRunner.run()`이
  완료 직후 자동 기록) 수정. `tests/interfaces/fakes.py`
  `FakeWorkflowEngine`에 두 메서드 최소 스텁 추가. 새 Core Domain
  Interface 없음(기존 `WorkflowEngine`의 메서드 2개 확장, 30종 유지).
  신규 테스트 12건(`domain` 5건, `InMemoryWorkflowEngine` 6건,
  `WorkflowRunner` 2건 — 정확한 분해는 `.ai/TASKS.md` Milestone 71
  참고). `pytest` 1317개(신규 13개, 회귀 없음)/`ruff`/`mypy`(233 source
  files) 전부 통과. `.ai/TASKS.md` Milestone 71 절 신규 추가.
  `docs/ARCHITECTURE.md` §3.12 Workflow Runner 절 및 §7 인터페이스 표
  (`WorkflowEngine`)에 Workflow Learning 서술 추가.

## ADR-0090: Workflow Adaptive Planning — 학습된 실행 순서를 현재 dependency로 검증 (Milestone 72)

- 배경: M71(ADR-0089)의 `_signature()`는 `task_ids`+`dependencies` 간선까지 정확히 일치해야 추천을 반환했다. 이 상태에서는 추천 순서가 존재하기만 하면 정의상 이미 현재 dependency를 만족하므로, "추천 순서가 유효하지 않으면 fallback"이라는 규칙이 코드에서 발동할 수 없는 죽은 경로였다. 사용자가 "M71의 학습을 실제 계획(plan)에 자동 반영"하는 M72를 요청하며 이 간극을 지적했다.
- 사용자 승인(AskUserQuestion, 1회): `_signature()`를 `task_ids`만으로 완화한다(권장안 채택) — 같은 Task 묶음이면 dependency가 바뀌어도(예: 새 의존관계 추가) 과거 추천을 우선 조회하되, `plan()`이 그 추천을 채택하기 전 현재 dependency를 실제로 만족하는지 검증한다.
- 결정:
  1. `InMemoryWorkflowEngine._signature()`를 `(frozenset(task_ids), edges)`에서 `frozenset(task_ids)`로 축소한다. `WorkflowEngine`(interface) 메서드 시그니처는 무변경 — `plan()`/`record_run_outcome()`/`recommended_order()` 전부 기존 그대로.
  2. `plan()`에 `_is_valid_order(order, workflow)` private 검증을 추가한다: (a) `order`가 `workflow.task_ids`와 정확히 같은 집합(순열)인지, (b) `workflow.dependencies`의 모든 간선(`dependent → {dependencies}`)이 `order` 상에서 dependency가 dependent보다 먼저 오는지. `recommended_order()`가 값을 반환하고 이 검증을 통과할 때만 그 순서를 채택하고, 그렇지 않으면(추천 없음 또는 검증 실패) 기존 DFS 위상 정렬로 완전히 동일하게 fallback한다.
  3. `WorkflowOrderStat`/`recommended_order()` 자체는 M71 그대로 재사용한다 — 새 값 객체, 새 abstract method 없음. "추천은 힌트, 정합성 검증은 plan()의 책임"으로 관심사를 분리했다.
  4. `FakeWorkflowEngine`(`tests/interfaces/fakes.py`)은 `recommended_order()`가 항상 `None`을 반환하는 기존 스텁을 그대로 유지 — 이 검증 경로를 타지 않으므로 수정 불필요.
- 대안:
  1. `_signature()`를 그대로 두고 `plan()`에 검증만 추가 — 기각: 검증이 항상 통과하는 죽은 코드가 되어 "학습을 실제 계획에 반영"한다는 M72 목표(dependency가 바뀌어도 적응)를 달성하지 못한다.
  2. 검증 실패 시 추천에서 dependency를 어긴 부분만 국소 수정(순서 일부만 재배치) — 기각: 어떤 최소 변경이 "올바른" 재배치인지 기준이 불명확해 새 알고리즘을 설계해야 하고, "정합성 위반 시 전량 fallback"이 가장 단순하고 안전하다(YAGNI).
- 이유: `_signature()` 완화는 M71이 이미 구축한 `WorkflowOrderStat`/dict 저장 구조를 전혀 바꾸지 않고 키 하나만 좁히는 최소 변경이다. `plan()`의 검증 로직은 순수 함수(side-effect 없음, `_plan_by_dependency_order()`와 동일한 계층)라 `WorkflowEngine`이 EventBus를 몰라야 한다는 §8 계층 규칙이나 새 Core Domain Interface 없이도 "추천은 힌트일 뿐, 정합성은 항상 보장"이라는 요구를 충족한다.
- 결과/영향: `engines/workflow_engine.py`(`_signature()` 축소, `_is_valid_order()` 신설, `plan()` 검증 로직 추가), `interfaces/workflow_engine.py`(docstring 갱신, 계약 무변경) 수정. 새 파일/Core Domain Interface 없음(기존 `WorkflowEngine`의 메서드 3개 그대로, 30종 유지). `tests/engines/test_workflow_engine.py`에 신규 테스트 2건(추천이 새 dependency를 어기면 fallback, 여전히 유효하면 채택) 추가. `pytest` 1319개(신규 2개, 회귀 없음)/`ruff`/`mypy`(233 source files) 전부 통과. `docs/ARCHITECTURE.md` §3.12 Workflow Runner 절 및 §7 인터페이스 표(`WorkflowEngine`)에 Workflow Adaptive Planning 서술 추가.

## ADR-0091: Workflow Cost Optimization — 동률 학습 순서에 M64 비용 정보로 tie-break (Milestone 73)

- 배경: M72(ADR-0090)의 `recommended_order()`는 성공률이 동률인 복수의 학습된 순서 후보 중 표본 수 → 먼저 기록된 순서로만 tie-break했다. 사용자가 "여러 유효한 실행 순서를 선택할 수 있는 경우, 가장 비용 효율적인 순서를 우선 선택"하는 M73을 요청했다 — M64(ADR-0064) `EngineSelectionPolicy`(예산 내 최저 비용 Engine 선택)를 재사용하되 새 비용 정책은 만들지 않는 제약이었다.
- 사용자 승인(AskUserQuestion, 2회):
  1. 의존성 연결 방식 — **생성자 선택적 주입(권장안 채택)**: `InMemoryWorkflowEngine(*, task_engine=None, engine_registry=None, engine_selection_policy=None)`. 셋 모두 기본값 `None`이면 비용 계산을 시도조차 하지 않고 기존 tie-break로 즉시 fallback. `WorkflowEngine`의 추상 메서드 시그니처(`plan()`/`record_run_outcome()`/`recommended_order()`)는 전혀 바꾸지 않는다 — 기존 호출부(`WorkflowRunner` 등)는 수정 불필요.
  2. 비용 계산 의미 — **합산 방식 그대로 채택(권장안)**: order의 비용 = 그 순서에 속한 모든 task_id에 대해 `EngineRegistry.list_candidates(task)` → `EngineSelectionPolicy.select(task, candidates)`로 고른 Engine의 `estimated_cost_usd`를 합산. `EngineSelectionPolicy.select()`는 순서를 모르는 순수함수이므로, 같은 task_id 집합의 순열(=같은 시그니처 아래 기록된 서로 다른 order)은 비용 합이 항상 동일하다는 점을 사용자에게 명시적으로 확인받았다 — 즉 실제 운영에서는 이 tie-break가 후보를 좁히지 못하고 거의 항상 기존 표본 수 tie-break로 넘어간다. 그럼에도 계약상 올바르고(사용자가 "예, 그대로 구현" 선택), 향후 순서에 민감한 `EngineSelectionPolicy`가 등장하면 그대로 의미 있게 작동하는 정직한 구현을 우선했다.
- 결정:
  1. `InMemoryWorkflowEngine.recommended_order()`를 재구성: 전체 후보 중 최고 성공률(`best_rate`)을 먼저 구하고, 그 값과 동률인 후보 목록(`tied`, 원본 삽입 순서 유지)을 추출한다.
  2. `_break_tie_by_cost(tied)`: `tied`가 1개 이하면 그대로 반환(비용 계산 스킵). 세 협력자(`_task_engine`/`_engine_registry`/`_engine_selection_policy`) 중 하나라도 `None`이면 그대로 반환(비용 정보 없음 → 즉시 fallback). 모두 있으면 각 후보의 비용을 `_order_cost()`로 계산하고, 하나라도 `None`(계산 불가)이면 비용 비교 자체를 포기하고 원래 `tied`를 그대로 반환 — "비용 정보를 계산할 수 없으면 기존 동작으로 즉시 fallback"을 요구사항 그대로 구현. 전부 계산되면 최저 비용과 같은 후보만 남긴다(위에서 설명했듯 실제로는 전부 같은 값이라 좁혀지지 않는 경우가 대부분).
  3. `_order_cost(order)`: order의 각 task_id에 대해 `task_engine.get_task()`(실패 시 `TaskNotFoundError` → `None`) → `engine_registry.list_candidates(task)`(빈 리스트면 `None`) → `engine_selection_policy.select(task, candidates)`(`None`이면 `None`) → 반환된 `engine_name`과 일치하는 후보의 `estimated_cost_usd`를 찾아 누적. 어느 단계든 실패하면 전체 계산을 포기(`None`)한다.
  4. 비용으로 좁힌(혹은 좁히지 못한) 후보 그룹에서 최종 선택은 기존과 동일하게 `max(tied, key=lambda k: orders[k].total)`(표본 수 최다, Python `max()`가 동률 시 첫 항목을 유지하므로 "먼저 기록된 순서" tie-break도 그대로 보존)로 수행한다.
  5. `WorkflowEngine`(interface)은 abstract method 시그니처 무변경 — docstring만 M73 동작을 명시하도록 갱신. 새 Core Domain Interface/새 비용 정책 없음.
- 대안:
  1. `plan()`/`recommended_order()` 시그니처에 선택적 keyword 인자로 비용 협력자를 전달 — 기각(사용자가 생성자 주입을 선택): `WorkflowEngine` 추상 메서드 시그니처가 바뀌어 모든 호출부(`WorkflowRunner` 포함)를 수정해야 하고, "기존 API와 100% 하위 호환" 요구와 어긋난다.
  2. 실제 실행 시 기록된 비용(예상이 아닌 실측)을 `WorkflowOrderStat`에 누적해 tie-break — 기각: "M64 `EngineSelectionPolicy`를 그대로 활용"(예상 비용 기반)이라는 요구사항과 어긋나고, 새 값 객체·기록 경로가 추가로 필요해 YAGNI 위반.
- 이유: 생성자 선택적 주입은 M65/M69/M70/M72가 반복해 온 "구성 시점에만 확장, 계약은 불변" 패턴을 그대로 따른다. 비용 계산이 order-invariant라는 사실을 사용자에게 투명하게 확인받고도 합산 방식을 그대로 채택한 것은, 정직하게 구현한 코드가 "지금은 대부분 무효과"이더라도 계약상 올바르고 미래의 순서-민감 `EngineSelectionPolicy`에 대비하는 편이, 억지로 order-dependent한 비용 모델을 새로 발명하는 것보다 YAGNI에 부합하기 때문이다.
- 결과/영향: `engines/workflow_engine.py`(`__init__`에 3개 선택적 협력자 추가, `recommended_order()` 재구성, `_break_tie_by_cost()`/`_order_cost()` 신설), `interfaces/workflow_engine.py`(docstring 갱신, 계약 무변경) 수정. 새 파일/Core Domain Interface 없음(기존 `WorkflowEngine`의 메서드 3개 시그니처 그대로, 30종 유지). `tests/engines/test_workflow_engine.py`에 신규 테스트 4건(비용 의존성 미주입 시 기존 tie-break 회귀 없음, 비용 계산 경로가 실제로 실행되지만 완전 동률 결과는 불변, Task 조회 실패 시 fallback, 등록된 Engine 없어 후보가 없을 때 fallback) 추가. `pytest` 1323개(신규 4개, 회귀 없음)/`ruff`/`mypy`(233 source files) 전부 통과. `docs/ARCHITECTURE.md` §3.12 Workflow Runner 절 및 §7 인터페이스 표(`WorkflowEngine`)에 Workflow Cost Optimization 서술 추가.
