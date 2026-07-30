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
