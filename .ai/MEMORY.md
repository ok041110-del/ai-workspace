# MEMORY — 프로젝트 장기 메모리

## 0. 이 문서의 역할과 사용 원칙 (중요)

`MEMORY.md`는 단순한 작업 메모가 아니라, AI Workspace 프로젝트의 **장기
메모리(Long-term Memory)**다. 다음 원칙에 따라 관리하고 사용한다.

1. **항상 읽는 문서가 아니다.** 매 Task마다 통째로 읽는 문서는 `.ai/TASKS.md`
   (현재 무엇을 해야 하는가)와 `.ai/RULES.md`(어떻게 해야 하는가)이며,
   `MEMORY.md`는 다음과 같은 **필요한 경우에만** 읽는다.
   - 새 세션(또는 새 AI 구현 엔진 호출)을 시작해 프로젝트 전체 맥락을 빠르게
     파악해야 할 때
   - 오래된 결정의 배경이나 이유가 궁금할 때
   - 프로젝트 규모가 커져 `.ai/TASKS.md`, `.ai/DECISIONS.md`만으로는 전체 그림이
     보이지 않을 때
2. **핵심 컨텍스트를 압축하여 저장한다.** 모든 대화나 변경 이력을 빠짐없이
   기록하는 로그가 아니다. 상세 이력은 `.ai/TASKS.md`의 "진행 로그"와
   `.ai/DECISIONS.md`의 ADR이 담당하고, `MEMORY.md`는 그중 **반드시 기억해야
   하는 결론만** 압축해서 담는다.
3. **프로젝트가 커져도 빠르게 현재 상황을 파악할 수 있도록 유지한다.** 새로운
   내용이 생겼다고 무조건 append하지 않는다. 오래되어 더 이상 유효하지 않은
   내용은 삭제하거나 최신 결론으로 교체한다. 이 문서는 "쌓이는 문서"가 아니라
   "항상 최신 상태의 요약본"이어야 한다.
4. **구현 세부사항이 아니라 사실과 의사결정을 기록한다.** 코드가 어떻게
   짜였는지가 아니라, "무엇이 결정되었는가", "왜 그렇게 결정했는가", "지금
   프로젝트가 어디까지 왔는가"를 기록한다. 구현 세부사항은 코드와
   `docs/ARCHITECTURE.md`가 진실의 원천(source of truth)이다.

이 문서는 아래 6개 섹션을 최소한으로 유지한다: 현재 Milestone, 프로젝트 정체성,
핵심 아키텍처, 반드시 유지해야 하는 설계 원칙, 주요 의사결정 요약, 이후 작업에
필요한 핵심 컨텍스트.

---

## 1. 현재 Milestone

- **현재 위치**: Milestone 1 (기반 구축) / **Phase 1 (핵심 도메인 모델 & CLI
  골격) 진행 중**
- **Phase 0**: 2026-07-23 사용자 승인 완료 (`.ai/TASKS.md` P0-11 DONE).
- **Phase 1 착수**: 2026-07-23 사용자 승인 완료 (P1-0 DONE).
- **완료된 Task**: P1-1(디렉터리), P1-2(Project/Task/Workflow 도메인),
  P1-3(Interfaces 7종), **P1-4(도메인 확장 + LLM Policy 초안)** — 모두 DONE.
  전체 41개 테스트 통과.
- **아키텍처는 v0.6.0으로 확정** (ADR-0006~0019, Multi-Agent First 심화 +
  안정화 보완: Agent Runtime, Engine Runtime, Context Manager, Event Store
  독립 구독자, Coordination Capability 등). 자세한 내용은 §3 참고.
- **P1-4 결과 (2026-07-23)**: `domain/mission.py`, `domain/step.py`,
  `domain/session.py`(WorkspaceSession), `domain/agent.py`(Agent/AgentRole/
  AgentCapability/AgentStatus), `domain/workflow.py`(mission_id 추가)를 구현.
  **사용자 지시로 범위가 확장되어 `domain/llm_policy.py`(LLMProvider/LLMModel/
  LLMEffort — Domain만, Policy Engine·Router 없음)를 추가**하고,
  `.ai/RULES.md`에 "Temporary LLM Policy" 섹션(M2~M5 진행 경로)과
  `docs/llm_policy.example.yaml` 정책 초안을 작성함. `docs/ARCHITECTURE.md`는
  변경하지 않음(사용자 지시).
- **다음 단계**: `.ai/TASKS.md`의 P1-5(신규 Interface 16종 정의 및 EngineAdapter
  세션 계약 확장)부터 진행.

## 2. 프로젝트 정체성

- **프로젝트명**: AI Workspace
- **한 줄 정의**: Claude Code, Codex, Gemini CLI 등 AI 구현 엔진을 **멀티
  에이전트로 오케스트레이션**하는 플랫폼.
- **핵심 원칙**: AI Workspace는 코드를 작성하지 않는다. 실제 코드 작성은 구현
  엔진의 책임이다. AI Workspace는 역할을 가진 Agent들이 협업하여 프로젝트/Task/
  Workflow/메모리/승인/자동화/다중 프로젝트/구현 엔진을 관리하도록 조율한다.
- **Multi-Agent First (ADR-0006)**: 멀티 에이전트는 선택 기능이 아니라 시스템의
  **기본 구조**다.

## 3. 핵심 아키텍처 (요약)

자세한 내용은 `docs/ARCHITECTURE.md` (v0.6.0) 참고. 여기서는 언제든 빠르게
떠올려야 하는 구조만 압축한다.

```
UI(CLI·Dashboard·Mobile·Voice·REST API·Slack·Discord·Webhook)
  → Interaction Layer
  → Workspace Core (최상위 오케스트레이터, WorkspaceSession 관리)
  → Agent Runtime(Registry · Scheduler · Manager · Event Bus)
       └ Event Bus의 독립 구독자: Event Store(기록/Replay/Audit)
  → Agents(Capability 중심: Coordination·Planning·Coding·Review·Documentation·…)  ←(Event Bus)→
  → Agent가 쓰는 3축:
       ① Core Engines(Task·Workflow·Approval·Automation)
       ② Context Manager → Memory Engine(저장/검색)
       ③ Engine Runtime → Engine Adapter → 구현 엔진(Claude Code·Codex·Gemini CLI)
```

- **Workspace Core**: 프로젝트/설정 로드, 서비스 초기화, **WorkspaceSession 관리,
  Agent Runtime·Engine Runtime 초기화, Workflow 시작, 종료**. Task는 Agent
  Runtime에 위임 (ADR-0010).
- **Agent Runtime**: Registry(등록/조회/제거) · Scheduler(Capability 기준 선택/
  병렬/우선순위) · Manager(생성/생명주기/상태) · Event Bus.
- **Event Store**: Event Bus의 **독립 구독자**로 이벤트 기록. 전달 게이팅 없음.
  Replay/Audit/복구 (ADR-0014, ADR-0018).
- **Agents**: **Capability 중심**(엔진 비종속). **Coordination Capability**로
  조정 역할 명시(ADR-0019). Event Bus로만 협업. 실제 일은 Engine Runtime에 위임.
- **Engine Runtime (ADR-0016)**: 엔진 선택/세션 풀/병렬. Agent와 Engine Adapter
  **사이**. Agent는 Engine Adapter를 직접 부르지 않는다.
- **Context Manager (ADR-0017)**: Context 조립 + Memory Snapshot 생명주기. 그 아래
  **Memory Engine은 저장/검색만**. Memory 접근은 Agent→Context Manager→Memory Engine.
- **Core Engines(서비스)**: Task/Workflow/Approval/Automation. Memory/Automation은
  Agent가 아니라 서비스(ADR-0012).
- **Interaction Layer**: UI 표면 입력을 표준 요청으로 정규화(ADR-0013). Voice는
  이 계층에 붙는 표면.
- **Engine Adapter**: per-engine 세션 생명주기 계약 create_session/run/cancel/
  status/destroy_session/capabilities/supports_parallel/estimate_cost (ADR-0015).
- **도메인**: Project · **Mission→Workflow→Task→Step** · **WorkspaceSession** ·
  Agent/AgentRole/AgentCapability(**Coordination 포함**)/AgentStatus.
- **Interfaces (총 16종, Phase 1에서 계약 정의)**: ProjectRepository,
  WorkflowEngine, TaskEngine, MemoryEngine(저장/검색), ApprovalEngine,
  AutomationEngine, EngineAdapter + AgentManager, AgentRepository, AgentRegistry,
  AgentScheduler, InteractionEngine, EventBus, EventStore, **EngineRuntime,
  ContextManager**.
- 의존 방향은 항상 위(UI)에서 아래(구현 엔진)로만 향한다. Agent 협업만 Event
  Bus를 통한 수평 결합이며, Event Store는 Bus의 독립 구독자다.

## 4. 반드시 유지해야 하는 설계 원칙

- 실제 코드 작성 금지 원칙은 **Phase 0(문서화 단계)에 한정**된다. Phase 1부터는
  승인을 받은 뒤 코드를 작성한다.
- **Multi-Agent First**: 모든 작업은 능력 있는 Agent들의 협업으로 수행한다.
  Workspace Core는 Task를 직접 실행하지 않고 **Agent Runtime에 위임**한다(ADR-0010).
- **Workspace Core는 Interfaces에만 의존하는 오케스트레이터다 (ADR-0005 유지).**
  처리 로직, 구현 엔진 직접 호출, 파일 저장 세부 구현을 Core에 넣지 않는다.
  WorkspaceSession 관리와 Agent Runtime 초기화가 Core의 핵심 책임이다.
- **Agent는 Capability 중심으로 선택한다 (ADR-0012).** Memory/Automation은
  Agent가 아니라 Core Engine(서비스)다.
- **Agent 간 직접 호출 금지, Event Bus 우선. 모든 이벤트는 Event Store에 기록**
  (ADR-0007, ADR-0014).
- **Voice 등 UI 표면은 Interaction Layer에 붙인다 (ADR-0013).** Workspace
  Core에 직접 연결하지 않는다.
- 구현 엔진은 반드시 **Engine Adapter(세션 생명주기 계약, ADR-0015)**를 통해서만
  호출한다.
- **Phase 1은 계약과 골격까지만.** Agent Runtime/Engine/Adapter/Event Store/
  Interaction의 실제 처리 로직은 Milestone 2·3에서 구현한다.
- 승인이 필요한 4가지 행위: 아키텍처 변경, 신규 기능, 리팩토링, Phase 완료.
  Approval Engine이 판별·차단한다 (우회 경로 없음).
- 계획은 Milestone → Phase → Task 계층을 따르며, Task는 한 번에 하나씩만
  진행한다.
- 모든 문서/설명/주석/커밋 메시지는 한국어, 코드 식별자는 Python 표준(영어)을
  따른다.

## 5. 주요 의사결정 요약

전체 배경/대안/이유는 `.ai/DECISIONS.md`의 각 ADR 참고. 여기서는 결론만 압축한다.

| ADR | 결론 | 상태 |
|---|---|---|
| ADR-0001 | 문서를 `README` / `docs/`(사람용) / `.ai/`(AI 운영용) 3계층으로 분리 | 승인됨 |
| ADR-0002 | 구현 엔진은 Adapter 패턴으로 추상화 (`EngineAdapter`) | 제안 (P1-5에서 확장 계약 반영 후 승인 예정) |
| ADR-0003 | 승인 절차는 별도 Approval Engine 컴포넌트로 분리 (인라인 금지) | 제안 (Core Engines 구현 Phase에서 확정) |
| ADR-0004 | Phase 1 저장 방식은 파일 기반(Markdown/JSON)으로 시작 | 제안 (P1-7 구현 후 승인 예정) |
| ADR-0005 | Workspace Core는 Interfaces에만 의존하는 오케스트레이터 | 승인됨 (ADR-0010이 책임 재정의) |
| ADR-0006 | Multi-Agent First: Workspace Core=Agent 오케스트레이터, Agent Manager·Agent 도메인 | 승인됨 (ADR-0010~0012가 심화) |
| ADR-0007 | Agent 협업은 Event Bus 기반 느슨한 결합 | 승인됨 |
| ADR-0008 | Conversation Layer 도입 | 승인됨 (**ADR-0013으로 대체 → Interaction Layer**) |
| ADR-0009 | EngineAdapter를 확장 실행 계약으로 확대 | 승인됨 (ADR-0015가 세션 계약으로 확장) |
| ADR-0010 | **Agent Runtime 계층**(Registry/Scheduler/Manager/Event Bus) + Workspace Core 재정의 + WorkspaceSession | 승인됨 |
| ADR-0011 | **Mission→Workflow→Task→Step** 4단 계층 | 승인됨 |
| ADR-0012 | **Capability 중심 Agent**, Memory/Automation은 Engine(서비스) | 승인됨 |
| ADR-0013 | Conversation Layer → **Interaction Layer**(InteractionEngine) | 승인됨 |
| ADR-0014 | **Event Store** 도입(Replay/Audit/복구) | 승인됨 (ADR-0018이 위치 보완) |
| ADR-0015 | EngineAdapter **세션 생명주기 계약**(create/destroy_session 추가) | 승인됨 |
| ADR-0016 | **Engine Runtime** 계층(Agent Runtime↔Engine Adapter 사이): 엔진 선택/세션 풀/병렬 | 승인됨 |
| ADR-0017 | **Context Manager**로 Memory Snapshot 역할 분리(Memory Engine=저장/검색) | 승인됨 |
| ADR-0018 | Event Store를 Event Bus **독립 Subscriber**로 위치 조정 | 승인됨 |
| ADR-0019 | **Coordination Capability** 추가(조정 역할 명시) | 승인됨 |

기술 스택(Python, dataclasses, 파일 기반 저장, CLI, 인메모리 Event Bus+파일
Event Store)은 제안 단계이며 각 구현 Phase에서 확정한다.

## 6. 이후 작업에 필요한 핵심 컨텍스트

- **Phase 1 범위(재구성)**: 도메인(Project/Task **+ Mission/Workflow(재정의)/
  Step + WorkspaceSession + Agent/AgentRole/AgentCapability(Coordination 포함)/
  AgentStatus**) + Interfaces 16종(계약만) + **세션 생명주기 EngineAdapter 계약** +
  Agent Runtime·Engine Runtime 위임형 Workspace Core 골격 + 파일 저장소(Project/
  Agent/EventStore) + 최소 CLI + 테스트. 실제 처리 로직은 Phase 1 범위 밖.
- **Phase별 구체 구현 순서**: Agent Runtime·Event Store·기본 Agent(Phase 2) →
  Core Engines·Context Manager(Phase 3) → Engine Runtime·Engine Adapter(Claude
  Code 우선, Phase 4) → Interaction Layer(Phase 5) → 자동화·다중 프로젝트·메모리
  고도화(Phase 6).
- 구현 엔진 연동 순서: Claude Code 최우선 → Codex → Gemini CLI.
- Voice/Slack 등 표면, Event Store, Interaction은 **구조에는 포함하되 구현은 뒤로**
  미룬다 (인터페이스만 Phase 1에서 정의).
- **미완료 유지 항목**: 이미 구현된 P1-3의 `EngineAdapter`는 `run_task` 기반이므로
  P1-5에서 세션 생명주기 계약(create_session/run/…/destroy_session)으로 교체해야
  한다. `ConversationEngine`은 `InteractionEngine`으로 대체 예정(P1-5).
- **LLM Policy는 "Temporary"다 (P1-4에서 Domain만 추가)**: `domain/llm_policy.py`
  에 `LLMProvider`/`LLMModel`/`LLMEffort`/`INITIAL_MODELS`만 존재하며, 실제 선택
  로직(Policy Engine, Router)은 없다. 사람이 `docs/llm_policy.example.yaml`을
  참고해 수동으로 적용하는 단계다. 진행 경로: M2(Rule 기반 선택) → M3(Agent가
  Policy 참조) → M4(Policy Engine 자동 선택) → M5(Self Optimizer 자동 최적화).
  자세한 내용은 `.ai/RULES.md` §7 "Temporary LLM Policy" 참고.
