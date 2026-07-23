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
> Task 순서는 2026-07-23 Phase 0 승인 시 사용자가 제시한 권장 순서(디렉터리 →
> Workspace Core 골격 → 공통 도메인 모델 → Engine Adapter 인터페이스 → 파일
> 저장소 → CLI → 테스트 환경)를 그대로 따른다.

#### P1-0: Phase 1 착수 승인 요청
- 목적: 도메인 모델/CLI 골격 착수 전 범위와 설계 방향을 확인받는다.
- 작업 내용: `docs/ROADMAP.md` Phase 1 목표와 세부 Task 계획을 제시하고 승인을
  요청한다.
- 완료 조건(DoD): 사용자가 Phase 1 착수를 승인한다.
- 상태: **DONE (2026-07-23, Phase 0 승인과 함께 착수 순서 포함하여 승인)**
- 의존성: P0-11

#### P1-1: `src/ai_workspace/` 디렉터리 구조 생성
- 목적: 이후 모든 코드가 따를 디렉터리 구조를 확정한다.
- 작업 내용: `docs/ARCHITECTURE.md` §6에서 제안한 `domain/ core/ engines/
  adapters/ cli/` 구조를 실제로 생성한다 (로직 없이 패키지 골격만).
- 완료 조건(DoD): 생성된 구조가 `docs/ARCHITECTURE.md`와 100% 일치한다.
- 상태: **DONE (2026-07-23)** — `src/ai_workspace/{domain,core,engines,adapters,cli}/`
  생성, 각 패키지에 빈 `__init__.py` 배치. 로직은 포함하지 않음 (다음 Task부터 구현).
- 의존성: P1-0

#### P1-2: Workspace Core 기본 골격 구현
- 목적: 모든 요청의 최상위 진입점이자 프로젝트 등록/다중 프로젝트 관리를
  담당하는 Workspace Core의 최소 형태를 마련한다.
- 작업 내용: `core/`에 프로젝트 등록·조회를 위한 최소 클래스/인터페이스를
  구현한다 (Core Engine 라우팅 로직은 해당 Engine이 존재하는 이후 Phase에서
  확장, Phase 1에서는 프로젝트 등록/조회 경로만 구현).
- 완료 조건(DoD): Workspace Core를 통해 Project를 등록/조회하는 최소 시나리오가
  단위 테스트로 확인된다.
- 상태: TODO
- 의존성: P1-1

#### P1-3: Project 도메인 모델 설계 및 구현
- 목적: 프로젝트라는 핵심 개념을 코드로 표현한다.
- 작업 내용: `domain/project.py`에 Project 모델(식별자, 이름, 목표, 상태,
  우선순위)과 타입 힌트를 구현한다.
- 완료 조건(DoD): Project 모델에 대한 단위 테스트가 통과한다.
- 상태: TODO
- 의존성: P1-1

#### P1-4: Task 도메인 모델 및 상태 전이 규칙 구현
- 목적: Task 단위 작업 관리의 기반을 마련한다.
- 작업 내용: `domain/task.py`에 Task 모델과 `TODO → IN_PROGRESS → REVIEW → DONE
  (/BLOCKED/CANCELLED)` 상태 전이 규칙을 구현한다.
- 완료 조건(DoD): 허용되지 않는 상태 전이가 거부됨을 테스트로 확인한다.
- 상태: TODO
- 의존성: P1-1

#### P1-5: Workflow 도메인 모델 초안 구현
- 목적: Task 간 순서/의존관계를 표현할 최소 모델을 마련한다.
- 작업 내용: `domain/workflow.py`에 Task 목록과 의존관계를 표현하는 최소 모델을
  구현한다 (실행 로직은 Phase 2에서 다룸).
- 완료 조건(DoD): 의존관계가 있는 Task 목록을 표현하고 순환 의존을 감지하는
  테스트가 통과한다.
- 상태: TODO
- 의존성: P1-4

#### P1-6: Engine Adapter 인터페이스 설계
- 목적: 구현 엔진을 비종속적으로 다루기 위한 공통 인터페이스를 확정한다
  (ADR-0002 반영). 특정 엔진(Claude Code 등)의 **구체적인 구현은 Phase 3
  범위**이며, Phase 1에서는 추상 인터페이스만 정의한다.
- 작업 내용: `adapters/base.py`에 `EngineAdapter` 추상 클래스(예:
  `run_task(task) -> EngineResult`)와 `EngineResult` 타입을 정의한다.
- 완료 조건(DoD): 인터페이스를 구현한 최소 Mock/Stub Adapter로 단위 테스트가
  통과한다 (실제 엔진 연동 없이 인터페이스 계약만 검증).
- 상태: TODO
- 의존성: P1-4

#### P1-7: 파일 기반 저장소 구현
- 목적: Project/Task 데이터를 세션 간에 영속화한다.
- 작업 내용: 저장 인터페이스를 정의하고, Markdown/JSON 기반 구현체를 작성한다
  (ADR-0004 반영).
- 완료 조건(DoD): 저장 형식을 변경해도 도메인 모델 테스트가 영향받지 않음을
  확인한다.
- 상태: TODO
- 의존성: P1-3, P1-4

#### P1-8: CLI 진입점 구성
- 목적: 사람이 실제로 Project/Task를 다뤄볼 수 있는 최소 진입점을 제공한다.
- 작업 내용: `cli/`에 Workspace Core를 통해 Project/Task를 생성·조회하는 명령을
  구현한다.
- 완료 조건(DoD): CLI로 Project 생성 → Task 생성 → 조회가 end-to-end로 동작한다.
- 상태: TODO
- 의존성: P1-2, P1-3, P1-4, P1-7

#### P1-9: 기본 테스트 환경 구축 및 테스트 작성
- 목적: Test Before Complete 원칙에 따라 Phase 1 산출물의 정확성을 검증할 수
  있는 환경과 테스트를 마련한다.
- 작업 내용: `pytest` 설정을 구성하고, `tests/core/`, `tests/domain/`,
  `tests/adapters/`, `tests/storage/`, `tests/cli/`에 각 컴포넌트별 테스트를
  작성한다.
- 완료 조건(DoD): `pytest` 실행 시 전체 테스트가 통과한다.
- 상태: TODO
- 의존성: P1-2 ~ P1-8

#### P1-10: `docs/ARCHITECTURE.md` 갱신
- 목적: 문서와 실제 구현이 항상 일치하도록 유지한다 (Documentation First).
- 작업 내용: 실제로 구현된 구조/세부 사항을 ARCHITECTURE.md에 반영한다.
- 완료 조건(DoD): 문서의 디렉터리 구조·컴포넌트 설명이 실제 코드와 일치한다.
- 상태: TODO
- 의존성: P1-1 ~ P1-9

#### P1-11: ADR 상태 갱신 (ADR-0002, ADR-0004)
- 목적: Engine Adapter 인터페이스 설계와 파일 기반 저장 결정을 정식으로
  확정한다.
- 작업 내용: `.ai/DECISIONS.md`의 ADR-0002, ADR-0004 상태를 "제안"에서
  "승인됨"으로 갱신한다.
- 완료 조건(DoD): 두 ADR의 상태가 "승인됨"으로 표시된다.
- 상태: TODO
- 의존성: P1-6, P1-7

#### P1-12: Phase 1 완료 승인 요청
- 목적: Approval Required 원칙에 따라 Phase 1 산출물을 검토받는다.
- 작업 내용: Workspace Core, 도메인 모델, Engine Adapter 인터페이스, 저장소,
  CLI, 테스트 결과를 제시하고 승인을 요청한다.
- 완료 조건(DoD): 위 모든 Task가 DONE이고 테스트가 통과한 상태에서 사용자가
  승인한다.
- 상태: TODO
- 의존성: P1-1 ~ P1-11

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
