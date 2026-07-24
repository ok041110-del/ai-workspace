# PRD (Product Requirements Document) — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.1.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft (Phase 0 — 문서화 단계) |
| 승인 상태 | 승인 대기 |

---

## 1. 개요 (Overview)

AI Workspace는 Claude Code, Codex, Gemini CLI와 같은 **AI 구현 엔진(Implementation Engine)** 을
관리하고 조율하는 **오케스트레이션 플랫폼**이다.

AI Workspace 자체는 코드를 작성하지 않는다. 실제 코드 작성, 파일 수정, 커맨드 실행 등
"구현(Implementation)" 행위는 각 AI 구현 엔진이 수행하며, AI Workspace는 다음을 담당한다.

- 어떤 작업을(Task) 어떤 엔진에게, 어떤 순서로, 어떤 조건에서 맡길 것인가
- 그 결과를 어떻게 검증하고 승인할 것인가
- 여러 프로젝트와 여러 엔진에 걸친 작업을 어떻게 일관되게 추적하고 기억할 것인가

즉, AI Workspace는 **"AI를 위한 프로젝트 매니저 + 오케스트레이터"**이며,
**"또 하나의 코딩 AI"가 아니다.**

> **Multi-Agent First (ADR-0006, 심화·보완: ADR-0010~0019)**: AI Workspace의 모든
> 작업은 능력(Capability: Coordination, Planning, Coding, Review, Documentation,
> Research …)을 가진 **Agent들의 협업**으로 수행된다. 멀티 에이전트는 선택 기능이
> 아니라 시스템의 **기본 구조**다. Workspace Core는 Agent Runtime에 실행을
> 위임하고, Agent는 Engine Runtime을 거쳐 구현 엔진을 사용하며 Event 기반으로
> 협업한다. 구조 세부는 `docs/ARCHITECTURE.md`(v0.6.0)를 참고한다.

## 2. 배경 및 문제 정의 (Background & Problem Statement)

현재 AI 코딩 도구(Claude Code, Codex, Gemini CLI 등)는 각각 독립적으로 동작한다.

이로 인해 다음과 같은 문제가 발생한다.

1. **컨텍스트 단절** — 세션이 끝나면 결정 사항과 맥락이 사라진다. 동일한 설명을
   반복해야 한다.
2. **엔진 종속** — 특정 엔진의 CLI/세션에 작업 이력이 갇혀, 다른 엔진으로 전환하거나
   병행 사용하기 어렵다.
3. **거버넌스 부재** — 어떤 작업이 승인되었는지, 어떤 결정이 왜 내려졌는지 추적할
   공식적인 장치가 없다.
4. **다중 프로젝트 관리의 어려움** — 여러 프로젝트를 동시에 진행할 때 우선순위, 진행
   상태, Task 의존관계를 한눈에 파악하기 어렵다.
5. **일관성 없는 작업 단위** — Task 단위가 아니라 즉흥적인 대화 단위로 작업이 진행되어
   진행 상황을 측정하기 어렵다.

AI Workspace는 이 문제들을 해결하기 위한 **관리 계층(Management Layer)**을 제공한다.

## 3. 목표 (Goals)

AI Workspace는 다음을 달성해야 한다.

1. 여러 프로젝트를 하나의 워크스페이스에서 등록하고 관리할 수 있어야 한다.
2. 프로젝트 내 작업을 Task 단위로 정의, 분해, 추적할 수 있어야 한다.
3. Task 간 의존관계와 실행 순서를 Workflow로 정의하고 조율할 수 있어야 한다.
4. Claude Code, Codex, Gemini CLI 등 서로 다른 구현 엔진을 동일한 인터페이스로
   호출할 수 있어야 한다 (엔진 추가/교체가 용이해야 한다).
5. 프로젝트의 결정 사항, 규칙, 맥락을 장기 메모리로 저장하고 재사용할 수 있어야 한다.
6. 아키텍처 변경, 신규 기능, 리팩토링, Phase 완료와 같은 중요한 지점에서 사용자
   승인을 요구하는 게이트인 Approval Engine을 제공해야 한다.
7. 반복적이고 정형화된 작업(정기 점검, 상태 갱신 등)을 자동화할 수 있어야 한다.
8. 모든 작업 이력과 의사결정 근거를 추적 가능하게(Auditable) 기록해야 한다.

## 4. 비목표 (Non-Goals)

명확히 하기 위해, AI Workspace가 **하지 않는 일**을 정의한다.

- AI Workspace는 자체적으로 코드를 생성하거나 수정하지 않는다. (구현 엔진의 역할)
- AI Workspace는 특정 구현 엔진을 대체하지 않는다. 엔진을 관리하고 연결할 뿐이다.
- AI Workspace는 범용 IDE나 에디터를 목표로 하지 않는다.
- AI Workspace는 1차 버전에서 완전 자율 실행(사용자 개입 없는 완전 자동화)을 목표로
  하지 않는다. 승인 지점은 항상 유지된다.

## 5. 핵심 개념 정의 (Key Concepts / Glossary)

| 용어 | 정의 |
|---|---|
| Project | 사용자가 관리하는 하나의 소프트웨어/작업 단위. |
| Mission | 사용자의 목표를 나타내는 최상위 단위. Workflow로 수행된다 (ADR-0011). |
| Workflow | Mission을 수행하기 위한 협업 흐름(Task 생성 → Agent 할당 → 협업 → 결과 통합). |
| Task | Agent에게 할당되는 작업 단위. |
| Step | Task 내부의 세부 실행 단위 (ADR-0011). |
| WorkspaceSession | Workspace의 현재 실행 상태(현재 프로젝트/Mission/활성 Workflow/활성 Agent/Memory Snapshot/Engine Session) (ADR-0010). |
| Agent | 능력(Capability)을 가지고 작업을 수행하는 실행 주체. Workspace의 핵심 도메인 모델. |
| Agent Capability | Agent의 능력 (Coordination, Planning, Coding, Review, Documentation, Research, Vision, Voice, Git, MCP …). 엔진 종류와 무관하게 Agent 선택 기준이 된다 (ADR-0012, ADR-0019). |
| Coordination Capability | 여러 Agent의 협업을 조정하는 능력. 직접 호출이 아니라 Event 기반으로 흐름을 조정한다 (ADR-0019). |
| Agent Runtime | Agent Registry/Scheduler/Manager/Event Bus로 구성된 Agent 실행 계층 (ADR-0010). |
| Engine Runtime | Agent Runtime과 Engine Adapter 사이에서 엔진 선택/세션 풀/병렬 실행을 관리하는 계층 (ADR-0016). |
| Event Bus | Agent 간 직접 호출 대신 이벤트 발행/구독으로 협업하게 하는 느슨한 결합 인프라 (ADR-0007). |
| Event Store | Event Bus의 **독립 구독자**로서 모든 이벤트를 기록하여 Replay/Audit/복구를 가능하게 한다 (ADR-0014, ADR-0018). |
| Interaction Layer | CLI/Dashboard/Mobile/Voice/REST API/Slack/Discord/Webhook 등 입력 표면을 표준 요청으로 통합하는 계층 (ADR-0013). |
| Implementation Engine | 실제 코드를 작성/실행하는 외부 AI 도구 (Claude Code, Codex, Gemini CLI 등). |
| Engine Adapter | 각 구현 엔진을 동일한 방식으로 호출하기 위한 per-engine 연결 계층. create_session/run/cancel/status/destroy_session/capabilities 등 세션 생명주기 실행 계약을 제공한다 (ADR-0015). |
| Core Engine | 모든 Agent가 사용하는 능력 서비스 (Task/Workflow/Approval/Automation Engine). Memory/Automation은 Agent가 아니라 서비스다 (ADR-0012). |
| Approval Engine | 특정 행위(아키텍처 변경, 신규 기능, 리팩토링, Phase 완료) 전에 사용자 승인을 요구하는 지점(컴포넌트). |
| Context Manager | Agent에게 제공할 Context를 조립하고 Memory Snapshot 생명주기를 관리하는 컴포넌트 (ADR-0017). |
| Memory Engine | Memory 저장/검색을 담당하는 하위 서비스. Context 조립/Snapshot은 Context Manager가 담당한다 (ADR-0017). |
| Automation | 사용자 개입 없이 정해진 조건에 따라 반복 실행되는 작업. |

## 6. 대상 사용자 (Target Users)

- 여러 프로젝트를 동시에 진행하며 AI 구현 엔진을 활용하는 1인 개발자 / 소규모 팀
- 여러 AI 코딩 도구를 병행 사용하며 일관된 프로세스를 원하는 개발자
- 작업 이력과 의사결정 근거를 명확히 남기고 싶은 사용자

## 7. 기능 요구사항 (Functional Requirements)

### 7.1 프로젝트 관리 (Project Management)
- 프로젝트 등록/조회/보관(archive)
- 프로젝트별 메타데이터(목표, 상태, 우선순위) 관리
- 프로젝트별 문서(PRD, ARCHITECTURE, ROADMAP 등) 연결

### 7.2 Task 관리 (Task Management)
- Task 생성, 상태 전이(대기 → 진행 → 완료/보류/취소) 관리
- Task 단위 완료 조건(Definition of Done) 명시
- Task와 Workflow, Task와 구현 엔진 간 매핑

### 7.3 Workflow 관리 (Workflow Orchestration)
- Task 간 순서/의존관계 정의
- 조건부 분기 (예: 테스트 실패 시 재작업 Task 생성)
- Workflow 실행 상태 추적

### 7.4 장기 메모리 (Long-term Memory)
- 프로젝트 단위 결정 사항, 규칙, 컨텍스트 저장
- 세션이 종료되어도 유지되는 저장 구조
- 새 세션/새 엔진 호출 시 관련 메모리를 불러와 컨텍스트로 제공

### 7.5 승인 (Approval)
- 아키텍처 변경, 신규 기능, 리팩토링, Phase 완료 시 승인 요청 생성
- 승인/반려 이력 기록
- 승인 없이는 다음 단계로 진행되지 않는 게이트 로직

### 7.6 자동화 (Automation)
- 정해진 조건/일정에 따른 반복 작업 트리거
- 자동화 작업도 Task/Workflow 체계 내에서 추적 가능해야 함

### 7.7 다중 프로젝트 관리 (Multi-Project Management)
- 여러 프로젝트의 상태를 한 눈에 조회
- 프로젝트 간 우선순위 조정

### 7.8 구현 엔진 관리 (Implementation Engine Management)
- 엔진 등록(Claude Code, Codex, Gemini CLI 등)
- 공통 인터페이스를 통한 엔진 호출 (엔진별 세부 구현은 Adapter가 담당)
- 엔진 실행 결과 수집 및 Task 상태 반영

## 8. 비기능 요구사항 (Non-Functional Requirements)

| 항목 | 요구사항 |
|---|---|
| 확장성 | 신규 구현 엔진을 최소한의 변경으로 추가할 수 있어야 한다 |
| 추적성 (Auditability) | 모든 결정, 승인, Task 상태 변화는 기록되어야 한다 |
| 이식성 | 특정 구현 엔진에 종속되지 않는 구조여야 한다 |
| 안전성 | 승인이 필요한 작업은 승인 없이 실행되지 않아야 한다 |
| 일관성 | 문서(.ai, docs) 구조와 실제 동작이 항상 일치해야 한다 |
| 가독성 | 코드/문서는 한국어 설명 + 영어 식별자 규칙을 일관되게 따라야 한다 |

## 9. 성공 기준 (Success Criteria)

Phase 1 기준으로 다음을 만족하면 성공으로 간주한다.

1. 프로젝트/Task/Workflow의 핵심 도메인 모델이 문서와 구조로 명확히 정의되어 있다.
2. 최소 1개 이상의 구현 엔진(Claude Code)을 위한 Adapter 인터페이스 설계가 완료되어
   있다.
3. 승인이 필요한 4가지 행위(아키텍처 변경/신규 기능/리팩토링/Phase 완료)에 대한
   프로세스가 문서로 정의되어 있다.
4. `.ai/TASKS.md`에 정의된 Phase 1 Task를 하나씩 순서대로 진행할 수 있는 상태이다.

## 10. 제약사항 및 가정 (Constraints & Assumptions)

- 구현 언어는 Python을 기준으로 한다 (변수/함수/클래스/파일명은 영어, PEP 8 준수).
- 모든 문서/설명/주석/커밋 메시지는 한국어로 작성한다.
- 이번 단계(Phase 0)에서는 애플리케이션 코드를 작성하지 않는다.
- 실제 구현 엔진과의 연동 방식(CLI 호출, API, SDK 등)은 Phase 1 이후 상세 설계에서
  확정한다.

## 11. 리스크 (Risks)

| 리스크 | 영향 | 대응 방향 |
|---|---|---|
| 구현 엔진마다 인터페이스/능력이 크게 다름 | Adapter 설계 복잡도 증가 | 공통 최소 인터페이스만 강제하고 엔진별 확장 허용 |
| 승인 절차가 과도해 자동화 이점이 줄어듦 | 생산성 저하 | 승인 대상 행위를 명확히 4가지로 한정 |
| 장기 메모리가 비대해져 컨텍스트 과부하 발생 | 성능/정확도 저하 | 요약/우선순위화 전략을 Phase 2 이후 설계 |
