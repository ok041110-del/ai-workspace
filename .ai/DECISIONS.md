# DECISIONS — Architecture Decision Record (ADR)

이 문서는 AI Workspace 프로젝트의 주요 설계 결정을 기록한다. 각 ADR은 결정
내용뿐 아니라 **배경, 대안, 이유, 결과**를 함께 남겨 이후 재검토가 가능하도록 한다.

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

- 상태: 제안 (Phase 1 착수 시 재확인 및 확정 예정)
- 날짜: 2026-07-23
- 배경: Claude Code, Codex, Gemini CLI는 호출 방식과 능력이 서로 다르다. 이를
  Orchestration Layer가 직접 알게 하면 엔진 추가/교체 시마다 핵심 로직을 수정해야
  한다.
- 결정: 모든 구현 엔진은 공통 `EngineAdapter` 인터페이스(예: `run_task`)를
  구현하고, Orchestration Layer는 이 인터페이스에만 의존한다.
- 대안:
  - 엔진별로 별도 파이프라인을 만드는 방식 — 초기 구현은 빠르지만 엔진이
    늘어날수록 중복과 불일치가 커짐 (기각).
  - 엔진 호출을 설정 파일 기반 스크립트로 느슨하게 연결하는 방식 — 유연하지만
    타입 안전성과 테스트 용이성이 떨어짐 (기각).
- 이유: Open-Closed Principle을 따라, 신규 엔진 추가가 기존 코드 변경 없이
  Adapter 하나를 새로 작성하는 것만으로 가능하도록 하기 위함.
- 결과/영향: Phase 3에서 `EngineAdapter` 인터페이스를 먼저 확정하고, Claude Code
  어댑터를 1차 구현체로 삼는다.

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

- 상태: 제안 (Phase 1 착수 시 재확인 및 확정 예정)
- 날짜: 2026-07-23
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
- 결과/영향: Phase 5에서 다중 프로젝트/장기 메모리 고도화 시 DB 전환 필요성을
  재검토하며, 그 경우 별도 ADR을 작성한다.

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
