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
  P1-3(Interfaces 7종) — 모두 DONE. 전체 32개 테스트 통과.
- **⚠ Multi-Agent First 전환 (2026-07-23, ADR-0006~0009)**: 프로젝트 방향이
  "상시 멀티 에이전트 Workspace"로 변경됨. 구현을 중단하고 아키텍처를 먼저
  수정함(문서만). Phase 1이 P1-1~P1-12로 재구성됨. 기존 P1-1~P1-3 산출물은
  유지하되, Agent 도메인(P1-4)·신규 Interface 및 EngineAdapter 확장(P1-5)·
  Agent 위임형 Workspace Core(P1-6) 등 후속 Task가 추가됨.
- **다음 단계**: 문서 검토·승인 후 구현 재개. `.ai/TASKS.md`의 P1-4(Agent
  도메인 추가 및 Workflow 재정의)부터 진행.

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

자세한 내용은 `docs/ARCHITECTURE.md` (v0.4.0) 참고. 여기서는 언제든 빠르게
떠올려야 하는 구조만 압축한다.

```
UI(CLI·Dashboard·Mobile·Voice·API)
  → Conversation Layer
  → Workspace Core (Agent 오케스트레이터)
  → Agent Manager
  → Agents(Planner·Coding·Review·Research·Memory·Automation)   ←(Event Bus)→
  → [Core Engines 서비스]  /  Engine Adapter
  → 구현 엔진(Claude Code·Codex·Gemini CLI)
```

- **Workspace Core**: Agent 최상위 오케스트레이터. 프로젝트/설정 로드, 서비스
  초기화, **Agent 등록/관리, Workflow 시작, Task 분배, Engine 선택/위임**, 종료.
  Task를 직접 실행하지 않고 **Agent에 위임**한다. 오직 Interfaces에만 의존한다
  (ADR-0005 유지 + ADR-0006 재정의).
- **Agent Manager**: Agent 생성/생명주기/선택/협업/상태 관리.
- **Agents**: 역할별 실행 주체. **Event Bus**로 느슨하게 협업(직접 호출 금지,
  ADR-0007). 실제 일은 Engine Adapter를 통해 구현 엔진에 위임.
- **Core Engines**: Task/Workflow/Memory/Approval/Automation — Agent와 Core가
  쓰는 능력 서비스(Agent 자체가 아님).
- **Conversation Layer**: 모든 UI 표면 입력을 표준 요청으로 정규화(ADR-0008).
  Voice는 이 계층에 붙는 UI.
- **Engine Adapter**: 확장 실행 계약 run/cancel/status/capabilities/
  supports_parallel/estimate_cost (ADR-0009). 구체 구현은 Phase 4.
- **Interfaces (총 11종, Phase 1에서 계약 정의)**: ProjectRepository,
  WorkflowEngine, TaskEngine, MemoryEngine, ApprovalEngine, AutomationEngine,
  EngineAdapter + AgentManager, AgentRepository, ConversationEngine, EventBus.
- 의존 방향은 항상 위(UI)에서 아래(구현 엔진)로만 향한다. Agent 협업만 Event
  Bus를 통한 수평 결합이다.

## 4. 반드시 유지해야 하는 설계 원칙

- 실제 코드 작성 금지 원칙은 **Phase 0(문서화 단계)에 한정**된다. Phase 1부터는
  승인을 받은 뒤 코드를 작성한다.
- **Multi-Agent First (ADR-0006)**: 모든 작업은 역할 있는 Agent들의 협업으로
  수행한다. Workspace Core는 Task를 직접 실행하지 않고 Agent에 위임한다.
- **Workspace Core는 Interfaces에만 의존하는 오케스트레이터다 (ADR-0005 유지).**
  처리 로직, 구현 엔진 직접 호출, 파일 저장 세부 구현을 Core에 넣지 않는다.
- **Agent 간 직접 호출 금지, Event Bus 우선 (ADR-0007).**
- **Voice 등 UI 표면은 Conversation Layer에 붙인다 (ADR-0008).** Workspace
  Core에 직접 연결하지 않는다.
- 구현 엔진은 반드시 **Engine Adapter(확장 계약, ADR-0009)**를 통해서만 호출한다.
- **Phase 1은 계약과 골격까지만.** Agent/Engine/Adapter/EventBus/Conversation의
  실제 처리 로직은 Milestone 2·3에서 구현한다.
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
| ADR-0005 | Workspace Core는 Interfaces에만 의존하는 오케스트레이터 | 승인됨 (ADR-0006이 책임을 Agent 위임으로 재정의) |
| ADR-0006 | **Multi-Agent First**: Workspace Core=Agent 오케스트레이터, Agent Manager·Agent 도메인 추가, Workflow=협업 흐름 | 승인됨 |
| ADR-0007 | Agent 협업은 Event Bus 기반 느슨한 결합 | 승인됨 |
| ADR-0008 | Conversation Layer 도입(입력 표면 통합, Voice 대비) | 승인됨 |
| ADR-0009 | EngineAdapter를 확장 실행 계약으로 확대 | 승인됨 |

기술 스택(Python, dataclasses, 파일 기반 저장, CLI, 인메모리 Event Bus)은
제안 단계이며 각 구현 Phase에서 확정한다.

## 6. 이후 작업에 필요한 핵심 컨텍스트

- **Phase 1 범위(재구성)**: 도메인(Project/Task/Workflow **+ Agent/AgentRole/
  AgentStatus**) + Interfaces 11종(계약만) + **확장 EngineAdapter 계약** +
  Agent 위임형 Workspace Core 골격 + 파일 저장소(Project/Agent) + 최소 CLI +
  테스트. 실제 처리 로직은 Phase 1 범위 밖.
- **Phase별 구체 구현 순서**: Agent Manager·Agent·Event Bus(Phase 2) → Core
  Engines(Phase 3) → Engine Adapter(Claude Code 우선, Phase 4) → Conversation
  Layer(Phase 5) → 자동화·다중 프로젝트·메모리 고도화(Phase 6).
- 구현 엔진 연동 순서: Claude Code 최우선 → Codex → Gemini CLI.
- Voice/Event Bus/Conversation은 **구조에는 포함하되 구현은 뒤로** 미룬다
  (인터페이스만 Phase 1에서 정의).
- 이미 구현된 P1-3의 `EngineAdapter`는 `run_task` 기반이므로, P1-5에서
  확장 계약(run/cancel/status/…)으로 갱신해야 한다 (미완료 항목, 잊지 말 것).
