# ARCHITECTURE — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.3.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft (Milestone 1 / Phase 1 — 구현 진행 중) |

이 문서는 `docs/PRD.md`에 정의된 요구사항을 바탕으로 AI Workspace의 구조를 설계한다.
실제 구현이 진행됨에 따라 이 문서와 실제 구조가 항상 일치하도록 갱신한다
(Documentation First 원칙).

> **v0.3.0 변경 사항**: Workspace Core의 책임을 순수 오케스트레이션으로 한정하고,
> Workspace Core가 구체 구현이 아닌 **Interfaces(추상 계약)**에만 의존하도록
> 재설계했다. 5개 Core Engine과 Engine Adapter, ProjectRepository는 모두
> "Interfaces(계약) → 구체 구현체(Phase별 구현)"의 2단계로 분리된다.

---

## 1. 아키텍처 원칙

1. **관리자와 구현자의 분리 (Separation of Orchestration and Implementation)**
   AI Workspace(관리자)는 "무엇을, 언제, 누구에게" 시킬지만 결정한다. "어떻게 코드를
   작성하는가"는 전적으로 구현 엔진(Claude Code, Codex, Gemini CLI 등)의 책임이다.

2. **엔진 비종속성 (Engine Agnosticism)**
   Workflow/Task 도메인 로직은 특정 구현 엔진의 API나 CLI 형식을 알지 못한다.
   엔진과의 통신은 반드시 Engine Adapter를 통해서만 이루어진다 (의존성 역전).

3. **인터페이스 우선 설계 (Interface-Driven Design)**
   Workspace Core는 물론, Core Engine과 Engine Adapter가 관여하는 모든 협력은
   구체 클래스가 아니라 **Interfaces(추상 계약)**를 통해 이루어진다. 구체
   구현체는 각 Phase에서 순차적으로 채워지며, 인터페이스만 지켜지면 언제든
   교체·추가할 수 있다.

4. **승인 지점의 명시적 분리 (Explicit Approval Boundaries)**
   아키텍처 변경, 신규 기능, 리팩토링, Phase 완료는 시스템 내부에서 별도의 상태
   (`승인 대기`)를 가지는 명시적 게이트(Approval Engine)로 모델링한다. 게이트를
   우회하는 경로는 존재하지 않는다.

5. **기록 우선 (Traceability by Design)**
   Task 상태 변화, 승인/반려, 주요 설계 결정은 사람이 읽을 수 있는 문서
   (`.ai/TASKS.md`, `.ai/DECISIONS.md`, `.ai/MEMORY.md`)와 항상 동기화된다.

6. **단순한 것에서 시작 (Start Simple, Extend Later)**
   Phase 1은 단일 사용자, 로컬 파일 기반 저장을 가정한다. 다중 사용자, 원격 저장,
   동시성 제어 등은 이후 Phase에서 필요할 때 확장한다 (YAGNI).

## 2. 전체 구조 개요

AI Workspace는 아래와 같은 구조를 가진다. 의존 방향은 항상 **위(사용자와 가까운
쪽)에서 아래(구현 엔진과 가까운 쪽)로만** 향하며, Workspace Core는 오직
**Interfaces(추상 계약)**에만 의존한다.

```
Workspace
   │  (CLI 등 Interface — 사용자와의 접점)
   ▼
Workspace Core
   │  (순수 오케스트레이터: 프로젝트 로드 / 설정 로드 / 서비스 초기화 /
   │   Engine 등록·관리 / Task 실행 요청 / 애플리케이션 종료)
   ▼
Interfaces (추상 계약 — Phase 1에서 정의)
   ├── ProjectRepository
   ├── WorkflowEngine
   ├── TaskEngine
   ├── MemoryEngine
   ├── ApprovalEngine
   ├── AutomationEngine
   └── EngineAdapter
   ▼
구체 구현체 (각 Phase에서 순차적으로 채워짐)
   ├── FileProjectRepository                              (Phase 1)
   ├── Workflow/Task/Memory/Approval/Automation Engine 구현체  (Phase 2)
   └── ClaudeCodeAdapter / CodexAdapter / GeminiCliAdapter     (Phase 3)
   ▼
Implementation Engines (외부, AI Workspace 범위 밖)
   Claude Code / Codex / Gemini CLI 등
```

Workspace Core는 "누가 구체적으로 이 인터페이스를 구현했는가"를 알지 못한다.
초기화 시점에 구체 구현체가 주입(dependency injection)될 뿐이며, 구현체가 아직
없는 인터페이스는 Phase 1에서 등록되지 않은 채로 둘 수 있다 (예: Phase 1 시점의
WorkflowEngine/TaskEngine/MemoryEngine/ApprovalEngine/AutomationEngine 구체
구현체는 아직 존재하지 않는다).

## 3. 핵심 컴포넌트

### 3.1 Workspace Core

Workspace Core는 **오케스트레이션만 수행**하며, 아래 6가지 책임만 가진다.

- **책임 (포함)**
  1. **프로젝트 로드**: `ProjectRepository` 인터페이스를 통해 프로젝트 정보를
     불러온다.
  2. **설정(Config) 로드**: Workspace 실행에 필요한 설정을 읽어온다.
  3. **서비스 초기화**: 등록된 Interfaces의 구체 구현체를 초기화하고 연결한다.
  4. **Engine 등록 및 관리**: `WorkflowEngine`, `TaskEngine`, `MemoryEngine`,
     `ApprovalEngine`, `AutomationEngine`, `EngineAdapter`의 구체 구현체를
     등록하고, 이름/타입으로 조회할 수 있게 관리한다.
  5. **Task 실행 요청**: 등록된 `TaskEngine`에 실행을 위임한다 (Task를 어떻게
     처리할지는 TaskEngine의 책임이며, Workspace Core는 요청만 전달한다).
  6. **애플리케이션 종료(Shutdown)**: 등록된 구성 요소들의 정리(cleanup) 절차를
     호출한다.
- **책임 (제외 — 다른 컴포넌트의 몫)**
  - Workflow 처리 로직 (→ WorkflowEngine)
  - Task 처리 로직 (→ TaskEngine)
  - Memory 처리 로직 (→ MemoryEngine)
  - Approval 처리 로직 (→ ApprovalEngine)
  - Automation 처리 로직 (→ AutomationEngine)
  - Claude Code / Codex / Gemini CLI 등 구현 엔진 직접 호출 (→ EngineAdapter)
  - 파일 저장 세부 구현 (→ ProjectRepository의 구체 구현체, 예: FileProjectRepository)
- **의존 방향**: Workspace(Interface)로부터 호출받음(→ 위) / 오직 §3.2의
  **Interfaces**에만 의존(→ 아래). 어떤 구체 클래스도 직접 알지 못한다.

### 3.2 Interfaces (추상 계약)

Phase 1에서는 아래 7개 인터페이스를 **계약(추상 클래스/Protocol)으로만**
정의한다. 각 인터페이스의 구체 구현체는 표에 명시된 Phase에서 채워진다.

| Interface | 계약 책임 | 구체 구현체 | 구현 시점 |
|---|---|---|---|
| `ProjectRepository` | 프로젝트 데이터의 조회/저장 계약 | `FileProjectRepository` | Phase 1 |
| `WorkflowEngine` | Task 순서/의존관계 조율 계약 | (Phase 2에서 구현) | Phase 2 |
| `TaskEngine` | Task 생성/상태 전이 계약 | (Phase 2에서 구현) | Phase 2 |
| `MemoryEngine` | 장기 메모리 조회/기록 계약 | (Phase 2에서 구현) | Phase 2 |
| `ApprovalEngine` | 승인 대상 행위 판별/차단 계약 | (Phase 2에서 구현) | Phase 2 |
| `AutomationEngine` | 조건/일정 기반 자동 트리거 계약 | (Phase 2에서 구현) | Phase 2 |
| `EngineAdapter` | 구현 엔진 호출 공통 계약 (`run_task`) | `ClaudeCodeAdapter` 등 | Phase 3 |

각 인터페이스가 확정되면, 향후 그 계약을 만족하는 어떤 구체 구현체로도 교체할 수
있다 (Open-Closed Principle). Workspace Core는 이 표의 "구체 구현체"가 무엇인지
알 필요가 없다.

### 3.3 구체 구현체 (Phase별 참고)

아래는 각 인터페이스의 구체 구현체가 최종적으로 수행할 책임을 미리 정의해 둔
것이다. Phase 1에서는 **인터페이스 계약만** 확정하며, 아래 책임은 각 Phase에서
구현될 때 실제로 채워진다.

- **FileProjectRepository** (Phase 1): 파일 기반(Markdown/JSON)으로 Project
  데이터를 읽고 쓴다.
- **WorkflowEngine 구현체** (Phase 2): 여러 Task의 실행 순서와 의존관계를 정의·
  조율하고, 조건부 분기(예: 테스트 실패 시 재작업 Task 생성)를 처리한다.
- **TaskEngine 구현체** (Phase 2): Task의 생성, 상태 전이(`TODO → IN_PROGRESS →
  REVIEW → DONE`/`BLOCKED`/`CANCELLED`), 완료 조건 검증을 수행한다.
- **MemoryEngine 구현체** (Phase 2): 프로젝트의 핵심 컨텍스트를 세션 간에
  압축된 형태로 유지한다 (`.ai/MEMORY.md`, `.ai/DECISIONS.md` 연동).
- **ApprovalEngine 구현체** (Phase 2): 아키텍처 변경/신규 기능/리팩토링/Phase
  완료 4가지 행위에 대한 승인 요청 생성과 차단을 수행한다.
- **AutomationEngine 구현체** (Phase 2): 조건/일정에 따라 Task/Workflow를 자동
  트리거한다.
- **ClaudeCodeAdapter / CodexAdapter / GeminiCliAdapter** (Phase 3): `EngineAdapter`
  계약에 따라 각 구현 엔진을 실제로 호출하고 결과를 공통 형식으로 변환한다.

## 4. 데이터 흐름 (Phase 1 기준 최소 시나리오)

Phase 1 시점에는 WorkflowEngine/TaskEngine 등의 구체 구현체가 아직 없으므로,
아래는 Phase 1에서 **테스트 가능한 최소 흐름**과 Milestone 2 이후 **완성될
흐름**을 함께 보여준다.

```
[Phase 1에서 실제로 동작하는 흐름]
사용자 요청 (CLI)
   │
   ▼
Workspace Core        ── 설정 로드 → ProjectRepository로 프로젝트 로드
   │
   ▼
ProjectRepository (FileProjectRepository)  ── 파일에서 Project 데이터 조회/저장
   │
   ▼
결과를 CLI로 반환

[Milestone 2 이후 완성되는 흐름 — Task 실행 요청]
사용자 요청 (CLI: "Task 실행")
   │
   ▼
Workspace Core        ── 등록된 TaskEngine에 실행 요청 위임
   │
   ▼
TaskEngine 구현체       ── (Phase 2) Task 상태 관리, 필요 시 WorkflowEngine/
   │                      ApprovalEngine과 협력
   ▼
EngineAdapter 구현체     ── (Phase 3) 실제 구현 엔진 호출
   │
   ▼
Implementation Engine (Claude Code 등) ── 실제 코드 작업 수행
   │
   ▼
결과 수집 ──▶ TaskEngine 상태 갱신 ──▶ MemoryEngine 반영 ──▶ 사용자에게 보고
```

## 5. 의존성 규칙 (Dependency Rules)

1. Workspace Core는 §3.2의 **Interfaces에만** 의존한다. 어떤 구체 구현체
   (`FileProjectRepository`, `ClaudeCodeAdapter` 등)도 직접 참조하지 않는다.
2. 구체 구현체는 자신이 구현하는 Interface와 도메인 모델(Project, Task,
   Workflow)을 참조할 수 있지만, Workspace Core나 다른 구체 구현체를 참조하지
   않는다.
3. Interface Layer(CLI 등)는 Workspace Core만 호출하며, Interfaces나 구체
   구현체를 직접 호출하지 않는다.
4. 구체 구현체 간 협력(예: TaskEngine 구현체가 ApprovalEngine 인터페이스를
   호출)은 반드시 **Interface를 통해서만** 이루어진다.
5. Persistence(파일 저장 구조)는 `ProjectRepository` 인터페이스를 통해서만
   접근한다. 저장 형식이 바뀌어도 Workspace Core와 도메인 로직은 영향받지
   않아야 한다.

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
├── src/ai_workspace/        # 애플리케이션 코드 (Phase 1부터)
├── workspace/               # 프로젝트별 실제 작업 공간
└── tests/                   # 테스트 코드
```

`src/ai_workspace/` 하위 구조는 다음과 같다.

```
src/ai_workspace/
├── domain/           # Project, Task, Workflow 등 핵심 모델 (순수 데이터/규칙, 엔진·인터페이스 비종속)
├── interfaces/        # Interfaces — 추상 계약 (Phase 1에서 정의)
│   ├── project_repository.py
│   ├── workflow_engine.py
│   ├── task_engine.py
│   ├── memory_engine.py
│   ├── approval_engine.py
│   ├── automation_engine.py
│   └── engine_adapter.py
├── core/             # Workspace Core — 순수 오케스트레이터 (Interfaces에만 의존)
├── storage/          # ProjectRepository의 구체 구현체 (Phase 1: FileProjectRepository)
├── engines/          # WorkflowEngine/TaskEngine/MemoryEngine/ApprovalEngine/AutomationEngine의 구체 구현체 (Phase 2)
├── adapters/         # EngineAdapter의 구체 구현체 (Phase 3: claude_code.py, codex.py, gemini_cli.py)
└── cli/              # Interface Layer (CLI 진입점, Workspace Core만 호출)
```

## 7. 확장성 고려사항

- **신규 엔진(구현 엔진) 추가**: `EngineAdapter` 인터페이스를 구현하는 새 클래스만
  `adapters/`에 추가하면 되며, Workspace Core나 다른 코드 변경은 필요 없다.
- **신규 승인 대상 추가**: `ApprovalEngine` 구현체가 다루는 행위 유형은
  열거형(enum)으로 관리하여 확장 시 영향 범위를 최소화한다.
- **저장소 교체**: `ProjectRepository` 인터페이스를 만족하는 구현체로 교체하면
  되므로(예: 파일 기반 → DB 기반), Workspace Core는 변경할 필요가 없다.
- **신규 Interface 추가**: 향후 새로운 종류의 Engine이 필요해지면, 인터페이스를
  `interfaces/`에 추가하고 Workspace Core의 "Engine 등록" 목록에 타입만
  추가하면 된다.

## 8. 보안 및 승인 경계

- 구현 엔진 호출은 항상 Workspace Core → `TaskEngine`(Interface) → 구체 구현체
  → (필요 시) `ApprovalEngine`(Interface) → `EngineAdapter`(Interface) → 구체
  구현체 순서로만 이루어진다. Workspace Core나 다른 컴포넌트가 Interface를
  건너뛰고 구체 구현체를 직접 호출하는 경로는 두지 않는다.
- 승인이 필요한 4가지 행위(아키텍처 변경, 신규 기능, 리팩토링, Phase 완료)는
  `TaskEngine`이나 `WorkflowEngine` 내부에 하드코딩된 체크가 아니라,
  `ApprovalEngine`이라는 별도 Interface/구현체로 분리하여 정책 변경 시 한 곳만
  수정하면 되도록 한다.

## 9. 기술 스택 (제안 — Phase 1 설계 Task에서 승인 필요)

| 영역 | 제안 | 이유 |
|---|---|---|
| 언어 | Python 3.11+ | 프로젝트 규칙(PEP 8, type hint)과 AI 생태계 친화성 |
| 데이터 모델 | `dataclasses` 또는 `pydantic` | 명시적 스키마와 검증 용이성 |
| 인터페이스 정의 | `abc.ABC` 또는 `typing.Protocol` | Python 표준 방식으로 계약을 강제/문서화 |
| 저장 (Phase 1) | 파일 기반 (Markdown/JSON) | 별도 인프라 없이 빠르게 시작, 사람이 직접 읽기 용이 |
| 인터페이스(사용자 접점) (Phase 1) | CLI | 가장 단순한 진입점, 이후 API/UI로 확장 가능 |
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
| Workspace Core가 각 Engine의 로직을 직접 포함 | 초기 구현이 단순 | Workspace Core가 비대해지고 책임이 섞임, 테스트 어려움 | 기각 |
| Workspace Core는 Interfaces에만 의존하는 순수 오케스트레이터로 한정 | 책임 분리 명확, 구체 구현 교체/지연이 자유로움, 각 Engine을 독립적으로 테스트 가능 | Interface 계층 설계 비용 발생 | **채택** |
| Phase 1부터 DB(SQLite 등) 도입 | 쿼리/동시성 처리 유리 | 초기 복잡도 증가, YAGNI 위반 소지 | 기각 (Phase 1) |
| Phase 1은 파일 기반 저장 | 단순, 사람이 직접 확인 가능, 문서 철학과 부합 | 대규모 데이터/동시성에 취약 | **채택 (Phase 1 한정)** |
