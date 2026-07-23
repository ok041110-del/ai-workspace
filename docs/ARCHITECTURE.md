# ARCHITECTURE — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.2.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft (Phase 0 — 문서화 단계, 코드 미구현) |

이 문서는 `docs/PRD.md`에 정의된 요구사항을 바탕으로 AI Workspace의 구조를 설계한다.
Phase 0 시점에는 애플리케이션 코드가 없으므로, 본 문서는 **구현 이전의 구조적 청사진**이다.
실제 구현이 시작되면 이 문서와 실제 구조가 항상 일치하도록 갱신한다 (Documentation First 원칙).

> v0.2.0 변경 사항: 컴포넌트를 "Workspace Core + Core Engines" 구조로 재정리하고,
> 각 컴포넌트의 이름을 `~Engine` 체계로 통일했다 (Task Manager → Task Engine,
> Memory Store → Memory Engine, Approval Gate → Approval Engine, Automation
> Scheduler → Automation Engine). Project Manager의 역할은 다중 프로젝트 관리
> 책임과 함께 Workspace Core로 통합했다.

---

## 1. 아키텍처 원칙

1. **관리자와 구현자의 분리 (Separation of Orchestration and Implementation)**
   AI Workspace(관리자)는 "무엇을, 언제, 누구에게" 시킬지만 결정한다. "어떻게 코드를
   작성하는가"는 전적으로 구현 엔진(Claude Code, Codex, Gemini CLI 등)의 책임이다.

2. **엔진 비종속성 (Engine Agnosticism)**
   Workflow/Task 도메인 로직은 특정 구현 엔진의 API나 CLI 형식을 알지 못한다.
   엔진과의 통신은 반드시 Engine Adapter를 통해서만 이루어진다 (의존성 역전).

3. **승인 지점의 명시적 분리 (Explicit Approval Boundaries)**
   아키텍처 변경, 신규 기능, 리팩토링, Phase 완료는 시스템 내부에서 별도의 상태
   (`승인 대기`)를 가지는 명시적 게이트(Approval Engine)로 모델링한다. 게이트를
   우회하는 경로는 존재하지 않는다.

4. **기록 우선 (Traceability by Design)**
   Task 상태 변화, 승인/반려, 주요 설계 결정은 사람이 읽을 수 있는 문서
   (`.ai/TASKS.md`, `.ai/DECISIONS.md`, `.ai/MEMORY.md`)와 항상 동기화된다.

5. **단순한 것에서 시작 (Start Simple, Extend Later)**
   Phase 1은 단일 사용자, 로컬 파일 기반 저장을 가정한다. 다중 사용자, 원격 저장,
   동시성 제어 등은 이후 Phase에서 필요할 때 확장한다 (YAGNI).

## 2. 전체 구조 개요

AI Workspace는 컴포넌트 관점에서 아래와 같은 5단 구조를 가진다. 의존 방향은 항상
**위(사용자와 가까운 쪽)에서 아래(구현 엔진과 가까운 쪽)로만** 향한다.

```
Interface
   │  (CLI / 향후 API·UI — 사용자와의 접점)
   ▼
Workspace Core
   │  (프로젝트 등록·다중 프로젝트 관리, 요청의 최상위 진입점 및 조율자)
   ▼
┌───────────────┬───────────────┬───────────────┬─────────────────┬───────────────────┐
│ Workflow Engine│  Task Engine  │ Memory Engine │  Approval Engine │  Automation Engine │
└───────────────┴───────────────┴───────────────┴─────────────────┴───────────────────┘
   │  (Core Engines — Workspace Core가 조율하는 핵심 도메인 로직)
   ▼
Engine Adapter
   │  (EngineAdapter 인터페이스 + 엔진별 구현체)
   ▼
Implementation Engines (외부, AI Workspace 범위 밖)
   Claude Code / Codex / Gemini CLI 등
```

Persistence(저장)는 별도의 수평 계층으로 두되, Phase 1에서는 파일 기반
(`workspace/` 하위의 프로젝트별 디렉터리 + Markdown/JSON)으로 단순하게 시작한다.

## 3. 핵심 컴포넌트

각 컴포넌트마다 **책임**과 **의존 방향**을 함께 명시한다. 의존 방향은 "이 컴포넌트가
누구를 알고 호출하는가"를 뜻하며, 반대 방향의 의존은 금지된다 (§5 참고).

### 3.1 Workspace Core
- **책임**
  - 프로젝트 등록/조회/보관 (구 Project Manager 역할)
  - 다중 프로젝트 관리: 여러 프로젝트의 상태를 파악하고 우선순위를 조정
  - 사용자/Interface Layer로부터 들어오는 모든 요청의 최상위 진입점 역할을 하며,
    요청 종류에 따라 적절한 Core Engine(들)에 위임
- **의존 방향**: Interface로부터 호출받음(→ 위) / Workflow Engine, Task Engine,
  Memory Engine, Approval Engine, Automation Engine을 호출(→ 아래). 특정 구현
  엔진이나 Engine Adapter는 직접 호출하지 않는다.

### 3.2 Workflow Engine
- **책임**
  - 여러 Task의 실행 순서와 의존관계를 정의하고 조율
  - 조건부 분기 처리 (예: 테스트 실패 시 재작업 Task 자동 생성)
  - Task 실행 전, Approval Engine을 통해 승인이 필요한지 확인
- **의존 방향**: Workspace Core로부터 호출받음(→ 위) / Task Engine, Approval
  Engine을 호출(→ 아래, 동일 계층 내 협력). Engine Adapter를 직접 호출하지 않고,
  Task 단위 실행은 Task Engine에 위임한다.

### 3.3 Task Engine
*(구 Task Manager)*
- **책임**
  - Task의 생성, 상태 전이, 완료 조건 검증
  - Task 상태: `TODO → IN_PROGRESS → REVIEW → DONE` (또는 `BLOCKED`, `CANCELLED`)
  - 하나의 Task를 하나의 구현 엔진에 위임하거나, 사람이 직접 처리하도록 표시
- **의존 방향**: Workspace Core, Workflow Engine으로부터 호출받음(→ 위) / 실제
  구현 엔진 호출이 필요할 때 Engine Adapter를 호출(→ 아래).

### 3.4 Memory Engine
*(구 Memory Store)*
- **책임**
  - 프로젝트의 핵심 컨텍스트(결정 사항, 규칙, 현재 Milestone 등)를 세션 간에
    압축된 형태로 유지
  - `.ai/MEMORY.md`, `.ai/DECISIONS.md`를 1차 저장소로 사용 (Phase 1)
  - "필요할 때만 조회"되는 구조를 지향하며, 모든 이력을 무제한 누적하지 않고
    핵심만 유지하도록 관리 (자세한 운영 원칙은 `.ai/MEMORY.md` 참고)
- **의존 방향**: Workspace Core, Task Engine, Approval Engine 등 다른 컴포넌트로
  부터 조회/기록 요청을 받음(→ 위). 다른 컴포넌트를 직접 호출하지 않는
  최하위 협력 컴포넌트다.

### 3.5 Approval Engine
*(구 Approval Gate)*
- **책임**
  - 아키텍처 변경 / 신규 기능 / 리팩토링 / Phase 완료 4가지 행위에 대해 승인
    요청을 생성하고, 승인 전까지 다음 단계 진행을 차단
  - 승인/반려 이력을 `.ai/DECISIONS.md`와 연동하여 기록
- **의존 방향**: Workspace Core, Workflow Engine으로부터 호출받음(→ 위) / 승인
  이력 기록을 위해 Memory Engine을 호출(→ 아래).

### 3.6 Automation Engine
*(구 Automation Scheduler)*
- **책임**
  - 정해진 조건이나 일정에 따라 Task/Workflow를 자동으로 트리거
  - 자동 실행된 작업도 Task Engine을 통해 동일한 이력 체계 안에서 추적되도록 함
- **의존 방향**: 독립적으로 스케줄을 감시하다가 조건 충족 시 Workspace Core(또는
  Workflow Engine)를 호출(→ 아래). 다른 Core Engine으로부터 직접 호출받지 않는다.

### 3.7 Engine Adapter
- **책임**
  - 모든 구현 엔진이 공통으로 구현하는 인터페이스 제공 (예: `run_task(task) ->
    EngineResult`)
  - Task Engine으로부터 받은 Task를 실제 구현 엔진 호출 형식으로 변환하고, 결과를
    다시 공통 형식으로 변환
- **의존 방향**: Task Engine으로부터 호출받음(→ 위) / 실제 구현 엔진(Claude
  Code, Codex, Gemini CLI 등)을 호출(→ 아래). Core Engine의 도메인 모델을 참조할
  수는 있으나, 그 반대는 금지된다 (§5).

## 4. 데이터 흐름 (기본 시나리오)

```
사용자 요청
   │
   ▼
Interface (CLI)
   │
   ▼
Workspace Core        ── 프로젝트 확인/등록, 요청을 적절한 Core Engine으로 전달
   │
   ▼
Workflow Engine        ── Task 순서/의존관계 결정
   │
   ▼
Task Engine            ── Task 생성 및 상태 관리
   │
   ▼
Approval Engine         ── (아키텍처 변경/신규 기능/리팩토링/Phase 완료인 경우) 승인 대기
   │  승인 완료
   ▼
Engine Adapter          ── 구현 엔진 선택 및 호출
   │
   ▼
Implementation Engine (Claude Code 등) ── 실제 코드 작업 수행
   │
   ▼
결과 수집 ──▶ Task Engine 상태 갱신 ──▶ Memory Engine 반영 ──▶ 사용자에게 보고
```

Automation Engine은 위 흐름과 별개로, 조건/일정이 충족되면 스스로 Workspace
Core를 호출하여 동일한 흐름을 트리거한다 (사람의 최초 요청 없이 시작되는 경로).

## 5. 의존성 규칙 (Dependency Rules)

1. Core Engine(Workflow/Task/Memory/Approval/Automation Engine)은 Engine
   Adapter의 **인터페이스**에만 의존하고, 특정 엔진 구현(예: Claude Code CLI
   호출 방식)에는 의존하지 않는다.
2. Engine Adapter 구현체는 도메인 모델(Task, Workflow 등)을 참조할 수 있지만,
   그 반대(도메인 모델이 특정 Adapter를 참조)는 금지한다.
3. Interface Layer(CLI 등)는 Workspace Core만 호출하며, Core Engine이나 Engine
   Adapter를 직접 호출하지 않는다.
4. Workspace Core는 모든 Core Engine을 호출할 수 있지만, Core Engine끼리는
   문서 §3에 명시된 협력 관계(예: Workflow Engine → Task Engine)를 벗어나 서로를
   임의로 호출하지 않는다.
5. Persistence(파일 저장 구조)는 각 컴포넌트가 정의한 저장 인터페이스를 통해서만
   접근한다. 저장 형식 변경이 도메인 로직에 영향을 주지 않아야 한다.

## 6. 디렉터리 구조와 컴포넌트 매핑

```
ai-workspace/
├── README.md
├── docs/
│   ├── PRD.md              # 요구사항 정의
│   ├── ARCHITECTURE.md     # 본 문서
│   └── ROADMAP.md          # Milestone/Phase 계획
├── .ai/
│   ├── RULES.md            # AI 개발 규칙
│   ├── TASKS.md            # Task 목록/진행 상태
│   ├── MEMORY.md           # 장기 메모리 (압축된 핵심 컨텍스트)
│   └── DECISIONS.md        # 설계 결정 기록 (ADR)
├── workspace/               # 프로젝트별 실제 작업 공간 (Phase 1 이후 구체화)
└── tests/                   # 테스트 코드 (Phase 1 이후 구체화)
```

향후 애플리케이션 코드가 도입되면(Phase 1 이후), 아래와 같은 하위 구조를 제안한다
(확정은 아니며, Phase 1 설계 Task에서 승인받아 확정한다).

```
ai-workspace/
└── src/ai_workspace/
    ├── domain/           # Project, Task, Workflow 등 핵심 모델 (엔진 비종속, 순수 데이터/규칙)
    ├── core/             # Workspace Core: 프로젝트 등록, 다중 프로젝트 관리, 진입점 조율
    ├── engines/          # Core Engines
    │   ├── workflow_engine.py
    │   ├── task_engine.py
    │   ├── memory_engine.py
    │   ├── approval_engine.py
    │   └── automation_engine.py
    ├── adapters/         # EngineAdapter 인터페이스 + 엔진별 구현체
    │   ├── base.py
    │   ├── claude_code.py
    │   ├── codex.py
    │   └── gemini_cli.py
    └── cli/              # Interface Layer (CLI 진입점)
```

## 7. 확장성 고려사항

- **신규 엔진 추가**: `EngineAdapter` 인터페이스를 구현하는 새 클래스만 추가하면
  되며, Core Engine 코드 변경은 필요 없어야 한다.
- **신규 승인 대상 추가**: Approval Engine이 다루는 행위 유형은 열거형(enum)으로
  관리하여 확장 시 영향 범위를 최소화한다.
- **저장소 교체**: Phase 1의 파일 기반 저장을 이후 DB 기반으로 교체할 수 있도록,
  저장 접근은 반드시 인터페이스를 통하도록 한다.
- **신규 Core Engine 추가**: Workspace Core가 조율 대상 Engine 목록을 통해
  호출하므로, 신규 Engine 추가 시 Workspace Core의 라우팅 로직만 확장하면 된다.

## 8. 보안 및 승인 경계

- 구현 엔진 호출은 항상 Workspace Core → Workflow Engine → Task Engine →
  (필요 시) Approval Engine을 거친 이후에만 이루어진다. Engine Adapter를
  우회해서 직접 엔진을 호출하는 경로는 두지 않는다.
- 승인이 필요한 4가지 행위(아키텍처 변경, 신규 기능, 리팩토링, Phase 완료)는
  Workflow Engine 내부에서 하드코딩된 체크가 아니라, Approval Engine이라는 별도
  컴포넌트로 분리하여 정책 변경 시 한 곳만 수정하면 되도록 한다.

## 9. 기술 스택 (제안 — Phase 1 설계 Task에서 승인 필요)

| 영역 | 제안 | 이유 |
|---|---|---|
| 언어 | Python 3.11+ | 프로젝트 규칙(PEP 8, type hint)과 AI 생태계 친화성 |
| 데이터 모델 | `dataclasses` 또는 `pydantic` | 명시적 스키마와 검증 용이성 |
| 저장 (Phase 1) | 파일 기반 (Markdown/JSON) | 별도 인프라 없이 빠르게 시작, 사람이 직접 읽기 용이 |
| 인터페이스 (Phase 1) | CLI | 가장 단순한 진입점, 이후 API/UI로 확장 가능 |
| 테스트 | `pytest` | Python 표준 관행 |

이 표는 **제안(proposal)**이며, 최종 채택은 `.ai/DECISIONS.md`에 ADR로 기록하고
사용자 승인을 받은 뒤 확정한다 (Approval Required 원칙).

## 10. 대안 및 트레이드오프

| 대안 | 장점 | 단점 | 채택 여부 |
|---|---|---|---|
| 엔진별로 별도 파이프라인을 구축 | 초기 구현이 빠름 | 엔진 추가마다 전체 로직 중복, 확장성 없음 | 기각 |
| Adapter 패턴으로 엔진 추상화 | 신규 엔진 추가 비용 최소화, 도메인 로직 재사용 | 초기 인터페이스 설계 비용 발생 | **채택** |
| 승인 절차를 워크플로우 로직에 내장 | 구현 단순 | 정책 변경 시 여러 곳 수정 필요, 우회 위험 | 기각 |
| 승인을 별도 Approval Engine 컴포넌트로 분리 | 정책 일관성, 우회 방지, 감사 용이 | 컴포넌트 하나 추가 | **채택** |
| Project 관리와 조율 진입점을 별도 컴포넌트로 분리 | 책임이 잘게 나뉨 | 컴포넌트 수 증가, 소규모 단계에서는 과함 | 기각 |
| Project 관리와 조율 진입점을 Workspace Core로 통합 | 진입점이 단순하고 명확함 | 향후 규모가 커지면 재분리 필요할 수 있음 | **채택 (Phase 1 한정, 필요 시 재검토)** |
| Phase 1부터 DB(SQLite 등) 도입 | 쿼리/동시성 처리 유리 | 초기 복잡도 증가, YAGNI 위반 소지 | 기각 (Phase 1) |
| Phase 1은 파일 기반 저장 | 단순, 사람이 직접 확인 가능, 문서 철학과 부합 | 대규모 데이터/동시성에 취약 | **채택 (Phase 1 한정)** |
