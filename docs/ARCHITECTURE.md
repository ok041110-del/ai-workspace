# ARCHITECTURE — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.1.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft (Phase 0 — 문서화 단계, 코드 미구현) |

이 문서는 `docs/PRD.md`에 정의된 요구사항을 바탕으로 AI Workspace의 구조를 설계한다.
Phase 0 시점에는 애플리케이션 코드가 없으므로, 본 문서는 **구현 이전의 구조적 청사진**이다.
실제 구현이 시작되면 이 문서와 실제 구조가 항상 일치하도록 갱신한다 (Documentation First 원칙).

---

## 1. 아키텍처 원칙

1. **관리자와 구현자의 분리 (Separation of Orchestration and Implementation)**
   AI Workspace(관리자)는 "무엇을, 언제, 누구에게" 시킬지만 결정한다. "어떻게 코드를
   작성하는가"는 전적으로 구현 엔진(Claude Code, Codex, Gemini CLI 등)의 책임이다.

2. **엔진 비종속성 (Engine Agnosticism)**
   Workflow/Task 도메인 로직은 특정 구현 엔진의 API나 CLI 형식을 알지 못한다.
   엔진과의 통신은 반드시 Adapter를 통해서만 이루어진다 (의존성 역전).

3. **승인 지점의 명시적 분리 (Explicit Approval Boundaries)**
   아키텍처 변경, 신규 기능, 리팩토링, Phase 완료는 시스템 내부에서 별도의 상태
   (`승인 대기`)를 가지는 명시적 게이트로 모델링한다. 게이트를 우회하는 경로는
   존재하지 않는다.

4. **기록 우선 (Traceability by Design)**
   Task 상태 변화, 승인/반려, 주요 설계 결정은 사람이 읽을 수 있는 문서
   (`.ai/TASKS.md`, `.ai/DECISIONS.md`, `.ai/MEMORY.md`)와 항상 동기화된다.

5. **단순한 것에서 시작 (Start Simple, Extend Later)**
   Phase 1은 단일 사용자, 로컬 파일 기반 저장을 가정한다. 다중 사용자, 원격 저장,
   동시성 제어 등은 이후 Phase에서 필요할 때 확장한다 (YAGNI).

## 2. 전체 구조 개요

AI Workspace는 4개의 레이어로 구성된다. 의존 방향은 항상 **위(바깥)에서 아래(안쪽)로만**
향한다.

```
┌─────────────────────────────────────────────────────────┐
│  Interface Layer                                         │
│  (CLI / 향후 API·UI) — 사용자와의 접점                     │
├─────────────────────────────────────────────────────────┤
│  Orchestration Layer (핵심 도메인)                         │
│  Project Manager / Task Manager / Workflow Engine /       │
│  Approval Gate / Memory Store / Automation Scheduler       │
├─────────────────────────────────────────────────────────┤
│  Engine Adapter Layer                                     │
│  EngineAdapter 인터페이스 + 엔진별 구현                     │
│  (ClaudeCodeAdapter / CodexAdapter / GeminiCliAdapter)     │
├─────────────────────────────────────────────────────────┤
│  Implementation Engines (외부, AI Workspace 범위 밖)        │
│  Claude Code / Codex / Gemini CLI 등                       │
└─────────────────────────────────────────────────────────┘
```

Persistence(저장)는 별도의 수평 계층으로 두되, Phase 1에서는 파일 기반
(`workspace/` 하위의 프로젝트별 디렉터리 + Markdown/JSON)으로 단순하게 시작한다.

## 3. 핵심 컴포넌트

### 3.1 Project Manager
- 프로젝트 등록/조회/보관을 담당한다.
- 각 프로젝트는 고유 식별자와 메타데이터(이름, 목표, 상태, 우선순위)를 가진다.
- 프로젝트별 문서(PRD, ARCHITECTURE, ROADMAP) 경로를 연결한다.

### 3.2 Task Manager
- Task의 생성, 상태 전이, 완료 조건 검증을 담당한다.
- Task 상태: `TODO → IN_PROGRESS → REVIEW → DONE` (또는 `BLOCKED`, `CANCELLED`)
- 하나의 Task는 하나의 구현 엔진에 위임되거나, 사람이 직접 처리할 수도 있다.

### 3.3 Workflow Engine
- 여러 Task의 실행 순서와 의존관계를 정의하고 조율한다.
- 조건부 분기(예: 테스트 실패 시 재작업 Task 자동 생성)를 지원한다.
- Task Manager와 Approval Gate를 호출하여 실제 진행 여부를 결정한다.

### 3.4 Approval Gate
- 아키텍처 변경 / 신규 기능 / 리팩토링 / Phase 완료 4가지 행위에 대해 승인 요청을
  생성하고, 승인 전까지 다음 단계 진행을 차단한다.
- 승인/반려 이력은 `.ai/DECISIONS.md`와 연동되어 기록된다.

### 3.5 Memory Store
- 프로젝트의 결정 사항, 규칙, 컨텍스트를 세션 간에 유지한다.
- `.ai/MEMORY.md`, `.ai/DECISIONS.md`를 1차 저장소로 사용한다 (Phase 1).
- 향후 검색/요약 기능은 이 컴포넌트 위에 확장한다.

### 3.6 Automation Scheduler
- 정해진 조건이나 일정에 따라 Task/Workflow를 자동으로 트리거한다.
- 자동 실행된 작업도 동일한 Task 이력 체계 안에서 추적된다.

### 3.7 Engine Adapter
- 모든 구현 엔진은 공통 인터페이스(예: `run_task(task) -> EngineResult`)를 구현한다.
- Orchestration Layer는 구체적인 엔진 구현을 알지 못하고, 인터페이스에만 의존한다.
- 신규 엔진 추가 시 Adapter 하나만 새로 작성하면 되도록 설계한다 (Open-Closed Principle).

## 4. 데이터 흐름 (기본 시나리오)

```
사용자 요청
   │
   ▼
Project Manager  ── 프로젝트 확인/등록
   │
   ▼
Task Manager     ── Task 생성 및 상태 관리
   │
   ▼
Workflow Engine  ── Task 순서/의존관계 결정
   │
   ▼
Approval Gate    ── (아키텍처 변경/신규 기능/리팩토링/Phase 완료인 경우) 승인 대기
   │  승인 완료
   ▼
Engine Adapter   ── 구현 엔진 선택 및 호출
   │
   ▼
Implementation Engine (Claude Code 등) ── 실제 코드 작업 수행
   │
   ▼
결과 수집 ──▶ Task 상태 갱신 ──▶ Memory Store 반영 ──▶ 사용자에게 보고
```

## 5. 의존성 규칙 (Dependency Rules)

1. Orchestration Layer는 Engine Adapter의 **인터페이스**에만 의존하고, 특정 엔진
   구현(예: Claude Code CLI 호출 방식)에는 의존하지 않는다.
2. Engine Adapter 구현체는 Orchestration Layer의 도메인 모델(Task, Workflow 등)을
   참조할 수 있지만, 그 반대(도메인 모델이 특정 Adapter를 참조)는 금지한다.
3. Interface Layer(CLI 등)는 Orchestration Layer만 호출하며, Engine Adapter를 직접
   호출하지 않는다.
4. Persistence(파일 저장 구조)는 Orchestration Layer가 정의한 저장 인터페이스를 통해서만
   접근한다. 저장 형식 변경이 도메인 로직에 영향을 주지 않아야 한다.

## 6. 디렉터리 구조와 컴포넌트 매핑

```
ai-workspace/
├── README.md
├── docs/
│   ├── PRD.md              # 요구사항 정의
│   ├── ARCHITECTURE.md     # 본 문서
│   └── ROADMAP.md          # Phase 계획
├── .ai/
│   ├── RULES.md            # AI 개발 규칙
│   ├── TASKS.md            # Task 목록/진행 상태
│   ├── MEMORY.md           # 장기 메모리
│   └── DECISIONS.md        # 설계 결정 기록 (ADR)
├── workspace/               # 프로젝트별 실제 작업 공간 (Phase 1 이후 구체화)
└── tests/                   # 테스트 코드 (Phase 1 이후 구체화)
```

향후 애플리케이션 코드가 도입되면(Phase 1 이후), 아래와 같은 하위 구조를 제안한다
(확정은 아니며, Phase 1 설계 Task에서 승인받아 확정한다).

```
ai-workspace/
└── src/ai_workspace/
    ├── domain/          # Project, Task, Workflow 등 핵심 모델 (엔진 비종속)
    ├── orchestration/   # Task Manager, Workflow Engine, Approval Gate
    ├── memory/          # Memory Store 구현
    ├── automation/      # Automation Scheduler
    ├── engines/         # EngineAdapter 인터페이스 + 엔진별 구현체
    │   ├── base.py
    │   ├── claude_code.py
    │   ├── codex.py
    │   └── gemini_cli.py
    └── cli/             # Interface Layer (CLI 진입점)
```

## 7. 확장성 고려사항

- **신규 엔진 추가**: `EngineAdapter` 인터페이스를 구현하는 새 클래스만 추가하면
  되며, Orchestration Layer 코드 변경은 필요 없어야 한다.
- **신규 승인 대상 추가**: Approval Gate가 다루는 행위 유형은 열거형(enum)으로
  관리하여 확장 시 영향 범위를 최소화한다.
- **저장소 교체**: Phase 1의 파일 기반 저장을 이후 DB 기반으로 교체할 수 있도록,
  저장 접근은 반드시 인터페이스를 통하도록 한다.

## 8. 보안 및 승인 경계

- 구현 엔진 호출은 항상 Task Manager → Workflow Engine → (필요 시) Approval Gate를
  거친 이후에만 이루어진다. Engine Adapter를 우회해서 직접 엔진을 호출하는 경로는
  두지 않는다.
- 승인이 필요한 4가지 행위(아키텍처 변경, 신규 기능, 리팩토링, Phase 완료)는
  Workflow Engine 내부에서 하드코딩된 체크가 아니라, Approval Gate라는 별도
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
| 승인을 별도 Approval Gate 컴포넌트로 분리 | 정책 일관성, 우회 방지, 감사 용이 | 컴포넌트 하나 추가 | **채택** |
| Phase 1부터 DB(SQLite 등) 도입 | 쿼리/동시성 처리 유리 | 초기 복잡도 증가, YAGNI 위반 소지 | 기각 (Phase 1) |
| Phase 1은 파일 기반 저장 | 단순, 사람이 직접 확인 가능, 문서 철학과 부합 | 대규모 데이터/동시성에 취약 | **채택 (Phase 1 한정)** |
