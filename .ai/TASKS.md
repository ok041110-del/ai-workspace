# TASKS — 전체 Task 및 진행 상태

이 문서는 `docs/ROADMAP.md`의 **Milestone → Phase → Task** 계층을 그대로 따른다.
`.ai/RULES.md`에 따라 **한 번에 하나의 Task만** 진행하며, Task를 완료로 표시하기
전 반드시 테스트(해당되는 경우)를 수행한다.

상태 값: `TODO` / `IN_PROGRESS` / `DONE` (필요 시 `BLOCKED` / `CANCELLED` 사용)

각 Task는 다음 정보를 포함한다.

- **목적**: 이 Task가 왜 필요한가
- **작업 내용**: 실제로 수행하는 일
- **완료 조건 (DoD)**: 무엇을 확인해야 완료로 볼 수 있는가
- **상태**: 현재 진행 상태

---

## Milestone 1 — 기반 구축 (Foundation)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 1 Definition of Done" 참고.

### Phase 0 — 문서화 및 구조 설계

#### P0-1: 프로젝트 비전/철학 분석 및 문서 구조 설계
- 목적: 프로젝트 비전과 개발 철학을 바탕으로 어떤 문서를, 어떤 구조로 만들지
  결정한다.
- 작업 내용: 사용자가 제시한 비전/철학을 분석하고 `README/docs/.ai/workspace/tests`
  구조를 설계한다.
- 완료 조건(DoD): 문서 구조가 결정되고 이후 Task(P0-2 이후)의 기준이 된다.
- 상태: DONE

#### P0-2: 디렉터리 구조 생성
- 목적: 설계한 문서 구조를 실제 디렉터리로 반영한다.
- 작업 내용: `docs/`, `.ai/`, `workspace/`, `tests/` 디렉터리를 생성한다.
- 완료 조건(DoD): 4개 디렉터리가 저장소에 존재한다.
- 상태: DONE

#### P0-3: `docs/PRD.md` 작성
- 목적: 프로젝트의 목표와 요구사항을 명확히 정의해 이후 설계의 기준을 세운다.
- 작업 내용: 배경, 목표, 비목표, 핵심 개념, 기능/비기능 요구사항, 성공 기준,
  리스크를 작성한다.
- 완료 조건(DoD): 위 항목이 모두 포함된 PRD가 작성된다.
- 상태: DONE

#### P0-4: `docs/ARCHITECTURE.md` 작성
- 목적: PRD 요구사항을 만족하는 구조를 설계해 구현 전 청사진을 마련한다.
- 작업 내용: 컴포넌트(Workspace Core / Core Engines / Engine Adapter), 데이터
  흐름, 의존성 규칙, 디렉터리 매핑, 대안 비교를 작성한다.
- 완료 조건(DoD): 각 컴포넌트의 책임과 의존 방향이 명시되고, 사용자 피드백
  (v0.2.0)이 반영된다.
- 상태: DONE

#### P0-5: `docs/ROADMAP.md` 작성
- 목적: Milestone/Phase 단위의 장기 계획을 수립한다.
- 작업 내용: Milestone → Phase 계층 구조로 계획을 작성하고 각 Milestone/Phase의
  DoD를 명시한다.
- 완료 조건(DoD): Milestone 1~3, Phase 0~5가 모두 DoD와 함께 정의된다.
- 상태: DONE

#### P0-6: `.ai/RULES.md` 작성
- 목적: 개발 철학을 프로젝트 내부 규정으로 명문화해 모든 작업의 기준으로 삼는다.
- 작업 내용: 언어 규칙, Documentation/Architecture First, Task Driven
  Development, One Task At A Time, Test Before Complete, Approval Required,
  이유 설명 원칙, 코딩/커밋 규칙을 작성한다.
- 완료 조건(DoD): 8개 원칙이 모두 문서화된다.
- 상태: DONE

#### P0-7: `.ai/MEMORY.md` 작성
- 목적: 세션이 끝나도 유지되어야 할 핵심 컨텍스트를 압축된 형태로 보존한다.
- 작업 내용: MEMORY.md의 역할/사용 원칙을 정의하고, 현재 Milestone·프로젝트
  정체성·핵심 아키텍처·설계 원칙·주요 의사결정 요약·다음 작업 컨텍스트를 기록한다.
- 완료 조건(DoD): "필요할 때만 참조하는 압축된 장기 메모리"라는 역할이 문서 내에
  명시되고, 요구된 6개 항목이 모두 포함된다.
- 상태: DONE

#### P0-8: `.ai/DECISIONS.md` 초기 ADR 작성
- 목적: 문서 구조, Adapter 패턴, 승인 체계, 저장 방식에 대한 결정 근거를 남긴다.
- 작업 내용: ADR-0001~0004를 배경/결정/대안/이유/결과 형식으로 작성한다.
- 완료 조건(DoD): 4개 ADR이 모두 "제안" 상태로 작성되고, Phase 완료 승인과 함께
  상태를 갱신할 기준이 마련된다.
- 상태: DONE

#### P0-9: `.ai/TASKS.md` 작성 (본 문서)
- 목적: Milestone/Phase/Task 계층에 따라 실제 작업을 추적할 수 있게 한다.
- 작업 내용: ROADMAP의 Milestone/Phase 구조를 그대로 따르는 Task 목록을 작성한다.
- 완료 조건(DoD): Phase 0의 모든 Task와 Phase 1의 세부 Task가 목적/작업내용/DoD/
  상태 형식으로 작성된다.
- 상태: DONE

#### P0-10: `README.md` 작성
- 목적: 프로젝트를 처음 접하는 사람이 빠르게 개요를 파악할 수 있게 한다.
- 작업 내용: 프로젝트 소개, 시작 방법, 디렉터리 구조, 문서 링크, 개발 철학
  요약을 작성한다.
- 완료 조건(DoD): 위 5개 항목이 모두 포함된다.
- 상태: DONE

#### P0-11: Phase 0 완료 승인 요청
- 목적: Approval Required 원칙에 따라 Phase 0 산출물을 사용자에게 검토받는다.
- 작업 내용: 완성된 문서 세트를 제시하고 승인을 요청한다. 1차 피드백(MEMORY 역할
  명확화, ARCHITECTURE 컴포넌트 보완, ROADMAP Milestone화, TASKS 구조 일치)을
  반영해 재요청한다.
- 완료 조건(DoD): 사용자가 Phase 0 산출물에 대해 명시적으로 승인한다.
- 상태: **DONE (2026-07-23 사용자 승인)**

> Phase 0에서는 애플리케이션 코드를 작성하지 않는다 (사용자 지시 사항).

---

### Phase 1 — 핵심 도메인 모델 & CLI 골격

> 착수 조건: P0-11(Phase 0 완료 승인)이 승인된 이후에만 시작한다. Phase 1
> 자체도 "신규 기능"에 해당하므로 착수 전 승인이 필요하다.
> **2026-07-23 사용자 지시로 Task 순서와 범위를 ADR-0005 기준으로 재구성함**:
> Workspace Core는 순수 오케스트레이터로 한정하고, Workspace Core가 구체
> 구현이 아닌 Interfaces(추상 계약)에만 의존하도록 한다. 최종 순서: 디렉터리
> 구조 → 공통 도메인 모델 → Interfaces 정의(7개) → Workspace Core 골격 →
> ProjectRepository 구현 → CLI → 테스트 환경.

#### P1-0: Phase 1 착수 승인 요청
- 목적: 도메인 모델/CLI 골격 착수 전 범위와 설계 방향을 확인받는다.
- 작업 내용: `docs/ROADMAP.md` Phase 1 목표와 세부 Task 계획을 제시하고 승인을
  요청한다.
- 완료 조건(DoD): 사용자가 Phase 1 착수를 승인한다.
- 상태: **DONE (2026-07-23, Phase 0 승인과 함께 착수 순서 포함하여 승인, 이후
  ADR-0005로 Workspace Core 범위/Interfaces 계층 구조를 재확정)**
- 의존성: P0-11

#### P1-1: `src/ai_workspace/` 디렉터리 구조 생성
- 목적: 이후 모든 코드가 따를 디렉터리 구조를 확정한다.
- 작업 내용: `docs/ARCHITECTURE.md` §6에서 제안한 `domain/ interfaces/ core/
  storage/ engines/ adapters/ cli/` 구조를 실제로 생성한다 (로직 없이 패키지
  골격만).
- 완료 조건(DoD): 생성된 구조가 `docs/ARCHITECTURE.md`와 100% 일치한다.
- 상태: **DONE (2026-07-23)** — 최초 `domain/core/engines/adapters/cli/` 생성 후,
  ADR-0005 반영을 위해 `interfaces/`, `storage/` 패키지를 추가함. 각 패키지에
  빈 `__init__.py` 배치. 로직은 포함하지 않음.
- 의존성: P1-0

#### P1-2: 공통 도메인 모델 정의 (Project, Task, Workflow)
- 목적: Workspace Core와 Interfaces가 공통으로 참조할 핵심 데이터 모델을
  먼저 정의한다.
- 작업 내용:
  - `domain/project.py`: Project 모델(식별자, 이름, 목표, 상태, 우선순위)
  - `domain/task.py`: Task 모델과 `TODO → IN_PROGRESS → REVIEW → DONE
    (/BLOCKED/CANCELLED)` 상태 전이 규칙
  - `domain/workflow.py`: Task 목록과 의존관계를 표현하는 최소 Workflow 모델
    (순환 의존 감지 포함, 실행 로직은 Phase 2에서 다룸)
- 완료 조건(DoD): 세 모델 각각에 대한 단위 테스트(정상 케이스 + 허용되지 않는
  전이/순환 의존 거부)가 통과한다.
- 상태: **DONE (2026-07-23)** — `domain/project.py`(Project, ProjectStatus),
  `domain/task.py`(Task, TaskStatus, 상태 전이 규칙), `domain/workflow.py`
  (Workflow, 순환/미지정 의존 검증) 구현. 테스트 실행을 위해 최소
  `pyproject.toml`(pytest `pythonpath=["src"]`)을 함께 추가하고 `pytest`를
  설치함 (정식 테스트 환경 구성은 P1-7에서 완성).
- 의존성: P1-1

#### P1-3: Interfaces 정의 (7개)
- 목적: Workspace Core와 향후 구체 구현체가 공유할 추상 계약을 확정한다
  (ADR-0002, ADR-0005 반영). Phase 1에서는 계약만 정의하고 구체 구현은 하지
  않는다 (`ProjectRepository`의 구체 구현만 P1-5에서 별도 진행).
- 작업 내용: `interfaces/`에 아래 7개 인터페이스를 정의한다 (`abc.ABC` 또는
  `typing.Protocol` 사용).
  - `project_repository.py` — `ProjectRepository`
  - `workflow_engine.py` — `WorkflowEngine`
  - `task_engine.py` — `TaskEngine`
  - `memory_engine.py` — `MemoryEngine`
  - `approval_engine.py` — `ApprovalEngine`
  - `automation_engine.py` — `AutomationEngine`
  - `engine_adapter.py` — `EngineAdapter` (`run_task(task) -> EngineResult`)
- 완료 조건(DoD): 각 인터페이스에 대해 최소 Mock/Stub 구현체로 계약 준수를
  확인하는 단위 테스트가 통과한다 (실제 로직 없이 계약만 검증).
- 상태: TODO
- 의존성: P1-2

#### P1-4: Workspace Core 기본 골격 구현
- 목적: 순수 오케스트레이터로서 Workspace Core의 최소 형태를 마련한다
  (ADR-0005). Workflow/Task/Memory/Approval/Automation 처리 로직이나 구현
  엔진 호출, 파일 저장 세부 구현은 포함하지 않는다.
- 작업 내용: `core/`에 다음 책임만 구현한다 (모두 §3.2 Interfaces에만 의존).
  1. 설정(Config) 로드
  2. `ProjectRepository` 인터페이스를 통한 프로젝트 로드
  3. 서비스 초기화 (등록된 Interfaces 구현체 연결)
  4. Engine 등록 및 관리 (`WorkflowEngine`, `TaskEngine`, `MemoryEngine`,
     `ApprovalEngine`, `AutomationEngine`, `EngineAdapter` 인터페이스 타입 기준)
  5. Task 실행 요청 (등록된 `TaskEngine`에 위임만 함)
  6. 애플리케이션 종료(Shutdown)
- 완료 조건(DoD): Mock Interfaces 구현체를 주입해 위 6개 책임이 각각 단위
  테스트로 검증된다. Workspace Core 코드에 구체 클래스(FileProjectRepository 등)
  에 대한 직접 참조가 없음을 확인한다 (Interfaces에만 의존).
- 상태: TODO
- 의존성: P1-2, P1-3

#### P1-5: ProjectRepository 파일 기반 구현
- 목적: `ProjectRepository` 인터페이스의 첫 구체 구현체를 마련해 프로젝트
  데이터를 세션 간에 영속화한다 (ADR-0004 반영).
- 작업 내용: `storage/file_project_repository.py`에 `ProjectRepository`를
  구현하는 `FileProjectRepository`를 Markdown/JSON 기반으로 작성한다.
- 완료 조건(DoD): `FileProjectRepository`가 `ProjectRepository` 계약을
  만족함을 테스트로 확인하고, Workspace Core에 주입해도 Workspace Core
  코드 변경이 필요 없음을 확인한다.
- 상태: TODO
- 의존성: P1-2, P1-3

#### P1-6: CLI 진입점 구성
- 목적: 사람이 실제로 Project/Task를 다뤄볼 수 있는 최소 진입점을 제공한다.
- 작업 내용: `cli/`에 Workspace Core(P1-4)와 FileProjectRepository(P1-5)를
  연결해 Project 생성·조회 명령을 구현한다 (Task 관련 명령은 TaskEngine 구체
  구현체가 없는 Phase 1에서는 등록/조회 골격까지만 제공).
- 완료 조건(DoD): CLI로 Project 생성 → 조회가 end-to-end로 동작한다.
- 상태: TODO
- 의존성: P1-4, P1-5

#### P1-7: 기본 테스트 환경 구축 및 테스트 작성
- 목적: Test Before Complete 원칙에 따라 Phase 1 산출물의 정확성을 검증할 수
  있는 환경과 테스트를 마련한다.
- 작업 내용: `pytest` 설정을 구성하고, `tests/domain/`, `tests/interfaces/`,
  `tests/core/`, `tests/storage/`, `tests/cli/`에 각 컴포넌트별 테스트를
  작성한다.
- 완료 조건(DoD): `pytest` 실행 시 전체 테스트가 통과한다.
- 상태: TODO
- 의존성: P1-2 ~ P1-6

#### P1-8: `docs/ARCHITECTURE.md` 갱신
- 목적: 문서와 실제 구현이 항상 일치하도록 유지한다 (Documentation First).
- 작업 내용: 실제로 구현된 구조/세부 사항을 ARCHITECTURE.md에 반영한다
  (이미 v0.3.0으로 선반영된 설계와 최종 구현이 일치하는지 검증 후 필요 시 갱신).
- 완료 조건(DoD): 문서의 디렉터리 구조·컴포넌트 설명이 실제 코드와 일치한다.
- 상태: TODO
- 의존성: P1-1 ~ P1-7

#### P1-9: ADR 상태 갱신 (ADR-0002, ADR-0004)
- 목적: Engine Adapter 인터페이스 설계와 파일 기반 저장 결정을 정식으로
  확정한다.
- 작업 내용: `.ai/DECISIONS.md`의 ADR-0002, ADR-0004 상태를 "제안"에서
  "승인됨"으로 갱신한다.
- 완료 조건(DoD): 두 ADR의 상태가 "승인됨"으로 표시된다.
- 상태: TODO
- 의존성: P1-3(ADR-0002), P1-5(ADR-0004)

#### P1-10: Phase 1 완료 승인 요청
- 목적: Approval Required 원칙에 따라 Phase 1 산출물을 검토받는다.
- 작업 내용: 도메인 모델, Interfaces, Workspace Core, ProjectRepository, CLI,
  테스트 결과를 제시하고 승인을 요청한다.
- 완료 조건(DoD): 위 모든 Task가 DONE이고 테스트가 통과한 상태에서 사용자가
  승인한다.
- 상태: TODO
- 의존성: P1-1 ~ P1-9

---

## Milestone 2 — 오케스트레이션 코어 (Orchestration Core)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 2 Definition of Done" 참고.
> 상세 Task는 Phase 착수 시점에 이 문서에 추가한다 (Task Driven Development).

### Phase 2 — Workflow/Task 실행 관리
- 상세 Task 정의 시점: Phase 1 완료 승인 이후
- Phase 목표/DoD: `docs/ROADMAP.md` "Phase 2" 참고

### Phase 3 — 엔진 어댑터 (Claude Code 우선)
- 상세 Task 정의 시점: Phase 2 완료 승인 이후
- Phase 목표/DoD: `docs/ROADMAP.md` "Phase 3" 참고

---

## Milestone 3 — 자동화 및 확장 (Automation & Scale)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 3 Definition of Done" 참고.
> 상세 Task는 Phase 착수 시점에 이 문서에 추가한다.

### Phase 4 — Automation Engine 도입
- 상세 Task 정의 시점: Phase 3 완료 승인 이후
- Phase 목표/DoD: `docs/ROADMAP.md` "Phase 4" 참고

### Phase 5 — 다중 프로젝트 & Memory Engine 고도화
- 상세 Task 정의 시점: Phase 4 완료 승인 이후
- Phase 목표/DoD: `docs/ROADMAP.md` "Phase 5" 참고

---

## 진행 로그

| 날짜 | 내용 |
|---|---|
| 2026-07-23 | Phase 0 문서 세트(P0-1 ~ P0-10) 작성 완료. P0-11(Phase 0 완료 승인) 1차 요청. |
| 2026-07-23 | 사용자 피드백 반영: MEMORY 역할 명확화, ARCHITECTURE 컴포넌트/의존방향 보완,
ROADMAP·TASKS를 Milestone → Phase → Task 구조로 재구성. P0-11 재요청. |
| 2026-07-23 | 사용자가 Phase 0을 승인(P0-11 DONE)하고 Phase 1 착수 및 권장 순서(디렉터리 →
Workspace Core 골격 → 공통 도메인 모델 → Engine Adapter 인터페이스 → 파일 저장소 →
CLI → 테스트 환경)를 승인(P1-0 DONE). 해당 순서에 맞춰 Phase 1 Task(P1-1~P1-12)를
재구성함. ADR-0001을 "승인됨"으로 갱신. |
| 2026-07-23 | P1-1 완료: `src/ai_workspace/{domain,core,engines,adapters,cli}/` 패키지
골격 생성 (로직 없음). 다음 Task: P1-2 (Workspace Core 기본 골격 구현). |
| 2026-07-23 | 사용자 지시로 Workspace Core 범위(순수 오케스트레이터)와 Interfaces
계층 구조(ProjectRepository/WorkflowEngine/TaskEngine/MemoryEngine/ApprovalEngine/
AutomationEngine/EngineAdapter)를 확정함(ADR-0005). ARCHITECTURE.md v0.3.0으로
갱신하고, Phase 1 Task 순서를 "도메인 모델 → Interfaces 정의 → Workspace Core
골격 → ProjectRepository 구현 → CLI → 테스트"로 재구성(P1-1~P1-10). P1-1에
`interfaces/`, `storage/` 패키지 추가 반영. 다음 Task: P1-2 (공통 도메인 모델 정의). |
| 2026-07-23 | P1-2 완료: Project/Task/Workflow 도메인 모델 구현, `pytest` 10개
테스트 전부 통과. 다음 Task: P1-3 (Interfaces 정의 7개). |
