# ROADMAP — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.3.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft (Multi-Agent First 전환 반영) |

## 계층 구조

AI Workspace의 계획은 다음 4단계 계층으로 관리한다.

```
Roadmap
  └─ Milestone   (프로젝트의 큰 목표)
       └─ Phase   (Milestone을 달성하기 위한 단계)
            └─ Task   (실제 구현 단위)
```

각 **Milestone 완료**와 각 **Phase 완료**는 `.ai/RULES.md`의 Approval Required
원칙에 따라 **사용자 승인**을 받아야 다음 단계로 진행한다.

> **v0.3.0 재구성 (Multi-Agent First)**: ADR-0006~0009 반영. 멀티 에이전트가
> 기본 구조가 되면서 Milestone/Phase를 "멀티 에이전트 코어 → 실행 엔진 연동 →
> 확장" 흐름으로 재편했다. Phase 1은 도메인/인터페이스에 Agent 계열(Agent 도메인,
> AgentManager/AgentRepository/ConversationEngine/EventBus 인터페이스, 확장
> EngineAdapter 계약)을 포함하도록 확장한다.

## Milestone / Phase 개요

| Milestone | 구성 Phase | 핵심 목표 | 상태 |
|---|---|---|---|
| M1. 기반 구축 (Foundation) | Phase 0, Phase 1 | 문서 체계 + 핵심 도메인(Agent 포함) + 전체 Interfaces + Workspace Core 골격 | 진행 중 |
| M2. 멀티 에이전트 코어 (Multi-Agent Core) | Phase 2, Phase 3 | Agent Manager·Agent·Event Bus 구현, Core Engines 구현 | 예정 |
| M3. 실행 엔진 연동 & 대화 계층 (Engine Integration & Conversation) | Phase 4, Phase 5 | Engine Adapter(Claude Code 우선) 구현, Conversation Layer 구현 | 예정 |
| M4. 자동화 및 확장 (Automation & Scale) | Phase 6 | 다중 프로젝트, 장기 메모리 고도화, 자동화 시나리오 | 예정 |

---

## Milestone 1 — 기반 구축 (Foundation)

**목표**: 문서 체계를 완성하고, Multi-Agent First 구조의 토대가 되는 핵심 도메인
(Project/Task/Workflow + Agent/AgentRole/AgentStatus), 전체 Interfaces, 그리고
Agent에 위임하는 Workspace Core 골격과 최소 CLI를 확보한다.

**구성 Phase**: Phase 0, Phase 1

**Milestone Definition of Done**
1. `docs/`, `.ai/` 문서 체계가 작성·승인되었다 (Phase 0).
2. Agent를 포함한 도메인 모델, 전체 Interfaces(11종), 확장 EngineAdapter 계약,
   Agent 위임형 Workspace Core 골격, 파일 저장소, 최소 CLI가 동작하며 테스트를
   통과한다 (Phase 1).
3. Multi-Agent First 관련 아키텍처 결정(ADR-0006~0009)이 문서로 확정되어 있다.

### Phase 0 — 문서화 및 구조 설계 (완료, 승인됨)

- **Phase Definition of Done**: 문서 세트 작성 + 사용자 승인. — **2026-07-23 승인 완료**

### Phase 1 — 핵심 도메인 & 전체 Interfaces & Workspace Core 골격 (진행 중, 재구성됨)

- **목표**: Multi-Agent First 구조의 골격을 만든다. Agent를 핵심 도메인으로
  포함하고, 11개 Interface를 계약으로 정의하며, Workspace Core를 "Task를 직접
  실행하지 않고 Agent에 위임하는" 오케스트레이터 골격으로 구현한다. Agent/Engine/
  Adapter/Event Bus/Conversation의 **구체 구현 로직은 이후 Phase**에서 진행한다.
- **세부 목표** (ADR-0005~0009 반영)
  1. 디렉터리 구조 확장 (`agents/`, `events/`, `conversation/` 추가)
  2. 도메인 모델: Project/Task/Workflow **+ Agent/AgentRole/AgentStatus**,
     Workflow를 협업 흐름 관점으로 재정의
  3. Interfaces 정의: 기존 7종 + **AgentManager, AgentRepository,
     ConversationEngine, EventBus** (계약만), **EngineAdapter 확장 계약**으로 갱신
  4. Workspace Core 골격: Agent 위임 구조(프로젝트/설정 로드, 서비스 초기화,
     Agent 등록/관리, Workflow 시작, Task 분배, Engine 선택/위임, 종료)
  5. 파일 기반 저장소: ProjectRepository(+ AgentRepository) 구현
  6. CLI 진입점 (UI Surface의 하나)
  7. 기본 테스트 환경 구축 및 계약/골격 테스트
- **Phase Definition of Done**: 위 7단계가 구현·테스트 통과하며, ARCHITECTURE.md와
  실제 구조가 일치한다. (Agent/Engine/Adapter/EventBus/Conversation의 실제
  처리 로직은 Phase 1 범위가 아니다 — 계약과 골격까지만.)
- **승인 필요 여부**: 예 — 착수 승인 완료(2026-07-23), Multi-Agent First 재설계
  승인 완료(2026-07-23). 완료 시 별도 Phase 완료 승인 필요.
- **세부 Task**: `.ai/TASKS.md`의 "Milestone 1 > Phase 1" 참고.

---

## Milestone 2 — 멀티 에이전트 코어 (Multi-Agent Core)

**목표**: Agent Manager와 역할별 Agent, Event Bus를 구현하여 실제 멀티 에이전트
협업이 동작하게 하고, Agent가 사용하는 Core Engines를 구현한다.

**구성 Phase**: Phase 2, Phase 3

**Milestone Definition of Done**
1. Agent Manager가 Agent를 생성/선택/생명주기 관리하고, Event Bus로 Agent 간
   협업이 이루어진다 (Phase 2).
2. Core Engines(Task/Workflow/Memory/Approval/Automation)가 구현되고, Workflow가
   협업 흐름(Task 생성→Agent 할당→협업→결과 통합)을 실행한다 (Phase 3).
3. Mock EngineAdapter 위에서 Planner→Coding→Review 협업 시나리오가 통과한다.

### Phase 2 — Agent Manager & Event Bus & 기본 Agent
- **목표**: AgentManager/EventBus 구현, Planner·Coding·Review 등 Agent 골격을
  Event 기반으로 동작시킨다 (실행은 Mock EngineAdapter).
- **Phase DoD**: `TaskCreated`→`ReviewRequested` 등 이벤트 흐름으로 Agent 협업이
  테스트로 검증된다.

### Phase 3 — Core Engines 구현
- **목표**: Task/Workflow/Memory/Approval/Automation Engine 구현. Approval
  Engine으로 승인 대상 4행위 차단(ADR-0003 확정).
- **Phase DoD**: 협업 Workflow가 실제 Engine 위에서 동작하고, 승인 게이트가
  차단 동작함을 테스트로 확인한다.

---

## Milestone 3 — 실행 엔진 연동 & 대화 계층 (Engine Integration & Conversation)

**목표**: 실제 구현 엔진(Claude Code 우선)에 Task를 위임하고, 다양한 표면을
통합하는 Conversation Layer를 구현한다.

**구성 Phase**: Phase 4, Phase 5

**Milestone Definition of Done**
1. `EngineAdapter` 확장 계약을 만족하는 ClaudeCodeAdapter로 Coding Agent가
   실제 Task를 end-to-end 위임·수행·결과 수집한다 (Phase 4).
2. Conversation Layer가 CLI/API 입력을 표준 요청으로 정규화한다 (Phase 5).

### Phase 4 — Engine Adapter 구현 (Claude Code 우선)
- **목표**: 확장 계약(run/cancel/status/capabilities/supports_parallel/
  estimate_cost)을 만족하는 ClaudeCodeAdapter 구현, 이후 Codex/Gemini CLI.
- **Phase DoD**: Coding Agent가 ClaudeCodeAdapter로 최소 1개 Task를 실제로
  수행하고 결과를 통합한다.

### Phase 5 — Conversation Layer 구현
- **목표**: ConversationEngine 구현으로 CLI/API를 통합. Voice 대비 구조 확정
  (Voice 자체 구현은 이후).
- **Phase DoD**: 최소 2개 표면(CLI, API)의 입력이 동일한 표준 요청으로 정규화되어
  Workspace Core에 전달된다.

---

## Milestone 4 — 자동화 및 확장 (Automation & Scale)

**목표**: Automation Agent 고도화, 다중 프로젝트 운용, 장기 메모리 고도화.

**구성 Phase**: Phase 6

### Phase 6 — 자동화 · 다중 프로젝트 · 메모리 고도화
- **목표**: Automation Agent가 조건/일정 기반으로 협업 Workflow를 트리거하고,
  2개 이상 프로젝트를 동시에 운용하며, Memory Agent가 핵심 컨텍스트를 검색/요약한다.
- **Phase DoD**: 자동화 시나리오 1건 이상 동작, 다중 프로젝트 조회, 메모리
  검색이 확인된다. (필요 시 파일→DB 전환은 별도 ADR.)

---

## 우선순위 원칙

1. 기반이 되는 도메인·인터페이스(Milestone 1)를 가장 먼저 확정한다.
2. Multi-Agent First 방향에 따라 Agent 협업 코어(Milestone 2)를 그 다음으로
   우선하고, 실제 엔진 연동과 대화 계층(Milestone 3)을 잇는다.
3. 자동화·다중 프로젝트 고도화(Milestone 4)는 핵심 오케스트레이션이 안정화된
   이후에 진행한다.
