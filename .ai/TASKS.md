# TASKS — 전체 Task 및 진행 상태

이 문서는 `docs/ROADMAP.md`의 **Milestone → Task** 계층을 그대로 따른다.
**Phase 계층은 2026-07-24부로 폐지되었다 (ADR-0021, Migration Table은
`docs/ROADMAP.md` 하단 참고).** `.ai/RULES.md`에 따라 **한 번에 하나의 Task만**
진행하며, Task를 완료로 표시하기 전 반드시 테스트(해당되는 경우)를 수행한다.

Task ID 형식: `T{Milestone 번호}-{일련번호}` (예: `T1-01`). 하나의 Task는
**하나의 구현 목표 + 하나의 Commit + 하나의 구현 사이클**이 되도록 설계한다.

상태 값: `TODO` / `IN_PROGRESS` / `DONE` (필요 시 `BLOCKED` / `CANCELLED` 사용)

각 Task는 다음 정보를 포함한다.

- **목적**: 이 Task가 왜 필요한가
- **작업 내용**: 실제로 수행하는 일
- **완료 조건 (DoD)**: 무엇을 확인해야 완료로 볼 수 있는가
- **상태**: 현재 진행 상태

---

## Milestone 1 — 기반 구축 (Foundation)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 1 Definition of Done" 참고.
> T1-01~T1-11은 문서화 작업(구 Phase 0), T1-12~T1-28은 구현 작업(구 Phase 1)에
> 해당한다. 그룹 구분은 참고용 설명일 뿐 별도 승인 단계를 두지 않는다 — Milestone
> 전체에 대한 승인은 T1-28(Milestone 1 Review) 하나로 일원화된다.
> **2026-07-24**: 원래 T1-18~T1-25(8개)였던 구현 Task를 아키텍처 책임 경계에
> 맞춰 T1-18~T1-28(11개)로 재분해함(ADR-0022). 상세 사유는 T1-18 앞의 안내문과
> ADR-0022 참고.

#### T1-01: 프로젝트 비전/철학 분석 및 문서 구조 설계
- 목적: 프로젝트 비전과 개발 철학을 바탕으로 어떤 문서를, 어떤 구조로 만들지
  결정한다.
- 작업 내용: 사용자가 제시한 비전/철학을 분석하고 `README/docs/.ai/workspace/tests`
  구조를 설계한다.
- 완료 조건(DoD): 문서 구조가 결정되고 이후 Task(T1-02 이후)의 기준이 된다.
- 상태: DONE

#### T1-02: 디렉터리 구조 생성
- 목적: 설계한 문서 구조를 실제 디렉터리로 반영한다.
- 작업 내용: `docs/`, `.ai/`, `workspace/`, `tests/` 디렉터리를 생성한다.
- 완료 조건(DoD): 4개 디렉터리가 저장소에 존재한다.
- 상태: DONE

#### T1-03: `docs/PRD.md` 작성
- 목적: 프로젝트의 목표와 요구사항을 명확히 정의해 이후 설계의 기준을 세운다.
- 작업 내용: 배경, 목표, 비목표, 핵심 개념, 기능/비기능 요구사항, 성공 기준,
  리스크를 작성한다.
- 완료 조건(DoD): 위 항목이 모두 포함된 PRD가 작성된다.
- 상태: DONE

#### T1-04: `docs/ARCHITECTURE.md` 작성
- 목적: PRD 요구사항을 만족하는 구조를 설계해 구현 전 청사진을 마련한다.
- 작업 내용: 컴포넌트(Workspace Core / Core Engines / Engine Adapter), 데이터
  흐름, 의존성 규칙, 디렉터리 매핑, 대안 비교를 작성한다.
- 완료 조건(DoD): 각 컴포넌트의 책임과 의존 방향이 명시되고, 사용자 피드백
  (v0.2.0)이 반영된다.
- 상태: DONE

#### T1-05: `docs/ROADMAP.md` 작성
- 목적: Milestone 단위의 장기 계획을 수립한다.
- 작업 내용: (작성 당시에는 Milestone → Phase 계층으로 계획을 작성했으며, 각
  Milestone/Phase의 DoD를 명시함. 이후 T1-?? 시점에 Phase 계층은 폐지됨 —
  Migration Table 참고.)
- 완료 조건(DoD): 당시 기준 Milestone 1~3, Phase 0~5가 모두 DoD와 함께
  정의된다(작성 당시 상태 그대로 보존, 이후 여러 차례 개정을 거쳐 현재 버전에
  이름).
- 상태: DONE

#### T1-06: `.ai/RULES.md` 작성
- 목적: 개발 철학을 프로젝트 내부 규정으로 명문화해 모든 작업의 기준으로 삼는다.
- 작업 내용: 언어 규칙, Documentation/Architecture First, Task Driven
  Development, One Task At A Time, Test Before Complete, Approval Required,
  이유 설명 원칙, 코딩/커밋 규칙을 작성한다.
- 완료 조건(DoD): 8개 원칙이 모두 문서화된다.
- 상태: DONE

#### T1-07: `.ai/MEMORY.md` 작성
- 목적: 세션이 끝나도 유지되어야 할 핵심 컨텍스트를 압축된 형태로 보존한다.
- 작업 내용: MEMORY.md의 역할/사용 원칙을 정의하고, 현재 Milestone·프로젝트
  정체성·핵심 아키텍처·설계 원칙·주요 의사결정 요약·다음 작업 컨텍스트를 기록한다.
- 완료 조건(DoD): "필요할 때만 참조하는 압축된 장기 메모리"라는 역할이 문서 내에
  명시되고, 요구된 6개 항목이 모두 포함된다.
- 상태: DONE

#### T1-08: `.ai/DECISIONS.md` 초기 ADR 작성
- 목적: 문서 구조, Adapter 패턴, 승인 체계, 저장 방식에 대한 결정 근거를 남긴다.
- 작업 내용: ADR-0001~0004를 배경/결정/대안/이유/결과 형식으로 작성한다.
- 완료 조건(DoD): 4개 ADR이 모두 "제안" 상태로 작성되고, 이후 승인과 함께 상태를
  갱신할 기준이 마련된다.
- 상태: DONE

#### T1-09: `.ai/TASKS.md` 작성 (본 문서)
- 목적: Milestone/Task 계층에 따라 실제 작업을 추적할 수 있게 한다.
- 작업 내용: (작성 당시에는 ROADMAP의 Milestone/Phase 구조를 따르는 Task 목록을
  작성함. 이후 Phase 폐지에 따라 본 문서 전체가 Milestone → Task 체계로
  재작성됨 — 2026-07-24, 진행 로그 참고.)
- 완료 조건(DoD): 당시 기준 Phase 0의 모든 Task와 Phase 1의 세부 Task가
  목적/작업내용/DoD/상태 형식으로 작성된다(작성 당시 상태 그대로 보존).
- 상태: DONE

#### T1-10: `README.md` 작성
- 목적: 프로젝트를 처음 접하는 사람이 빠르게 개요를 파악할 수 있게 한다.
- 작업 내용: 프로젝트 소개, 시작 방법, 디렉터리 구조, 문서 링크, 개발 철학
  요약을 작성한다.
- 완료 조건(DoD): 위 5개 항목이 모두 포함된다.
- 상태: DONE

#### T1-11: 문서화 완료 승인 요청 (구 "Phase 0 완료 승인 요청")
- 목적: Approval Required 원칙에 따라 문서화 산출물(T1-01~T1-10)을 사용자에게
  검토받는다.
- 작업 내용: 완성된 문서 세트를 제시하고 승인을 요청한다. 1차 피드백(MEMORY 역할
  명확화, ARCHITECTURE 컴포넌트 보완, ROADMAP Milestone화, TASKS 구조 일치)을
  반영해 재요청한다.
- 완료 조건(DoD): 사용자가 문서화 산출물에 대해 명시적으로 승인한다.
- 상태: **DONE (2026-07-23 사용자 승인)**

> 문서화 작업(T1-01~T1-11)에서는 애플리케이션 코드를 작성하지 않는다 (사용자
> 지시 사항).

---

#### T1-12: 구현 착수 승인 요청 (구 "Phase 1 착수 승인 요청")
- 목적: 도메인 모델/CLI 골격 착수 전 범위와 설계 방향을 확인받는다.
- 작업 내용: `docs/ROADMAP.md`의 구현 목표와 세부 Task 계획을 제시하고 승인을
  요청한다.
- 완료 조건(DoD): 사용자가 구현 착수를 승인한다.
- 상태: **DONE (2026-07-23, 문서화 완료 승인과 함께 착수 순서 포함하여 승인,
  이후 ADR-0005로 Workspace Core 범위/Interfaces 계층 구조를 재확정)**
- 의존성: T1-11

> **2026-07-23 Multi-Agent First 전환(ADR-0006~0009)으로 구현 작업 범위를
> 재구성함.** Agent가 핵심 도메인이 되고, Workspace Core는 Task를 직접 실행하지
> 않고 Agent에 위임하는 오케스트레이터가 된다. 순서: 디렉터리 확장 → 도메인 →
> Interfaces → Agent 도메인 추가 → 신규 Interface/EngineAdapter 확장 →
> Workspace Core 골격(Agent 위임) → 저장소 → CLI → 테스트.
>
> **참고: 이 구현 작업(T1-12~T1-28)은 계약과 골격까지만 만든다.** Agent/Engine/
> Adapter/EventBus/Interaction의 실제 처리 로직은 Milestone 2·3에서 구현한다.

#### T1-13: `src/ai_workspace/` 디렉터리 구조 생성
- 목적: 이후 모든 코드가 따를 디렉터리 구조를 확정한다.
- 작업 내용: `docs/ARCHITECTURE.md` §6에서 제안한 `domain/ interfaces/ core/
  storage/ engines/ adapters/ cli/` 구조를 실제로 생성한다 (로직 없이 패키지
  골격만).
- 완료 조건(DoD): 생성된 구조가 `docs/ARCHITECTURE.md`와 100% 일치한다.
- 상태: **DONE (2026-07-23)** — 최초 `domain/core/engines/adapters/cli/` 생성 후,
  ADR-0005 반영을 위해 `interfaces/`, `storage/` 패키지를 추가함. 각 패키지에
  빈 `__init__.py` 배치. 로직은 포함하지 않음.
- 의존성: T1-12

#### T1-14: 공통 도메인 모델 정의 (Project, Task, Workflow)
- 목적: Workspace Core와 Interfaces가 공통으로 참조할 핵심 데이터 모델을
  먼저 정의한다.
- 작업 내용:
  - `domain/project.py`: Project 모델(식별자, 이름, 목표, 상태, 우선순위)
  - `domain/task.py`: Task 모델과 `TODO → IN_PROGRESS → REVIEW → DONE
    (/BLOCKED/CANCELLED)` 상태 전이 규칙
  - `domain/workflow.py`: Task 목록과 의존관계를 표현하는 최소 Workflow 모델
    (순환 의존 감지 포함, 실행 로직은 Milestone 2에서 다룸)
- 완료 조건(DoD): 세 모델 각각에 대한 단위 테스트(정상 케이스 + 허용되지 않는
  전이/순환 의존 거부)가 통과한다.
- 상태: **DONE (2026-07-23)** — `domain/project.py`(Project, ProjectStatus),
  `domain/task.py`(Task, TaskStatus, 상태 전이 규칙), `domain/workflow.py`
  (Workflow, 순환/미지정 의존 검증) 구현. 테스트 실행을 위해 최소
  `pyproject.toml`(pytest `pythonpath=["src"]`)을 함께 추가하고 `pytest`를
  설치함.
  ※ Multi-Agent First 전환(ADR-0006)으로 Workflow는 "협업 흐름"으로 재정의되며,
    Agent 도메인 추가 및 Workflow 재정의는 후속 Task **T1-16**에서 진행한다.
- 의존성: T1-13

#### T1-15: Interfaces 정의 (7개)
- 목적: Workspace Core와 향후 구체 구현체가 공유할 추상 계약을 확정한다
  (ADR-0002, ADR-0005 반영). 계약만 정의하고 구체 구현은 하지 않는다
  (`ProjectRepository`의 구체 구현만 T1-23에서 별도 진행).
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
- 상태: **DONE (2026-07-23)** — 7개 Interface를 `abc.ABC`로 정의하고 각
  메서드 docstring에 입력/출력/예외/보장사항을 명시함. `tests/interfaces/fakes.py`에
  7개 Fake 구현체(테스트 전용, `src/`에는 포함하지 않음)를 작성하고 22개 계약
  테스트로 검증함.
  ※ Multi-Agent First 심화+안정화 보완(ADR-0010~0019)으로 신규 Interface 9종
    (AgentManager, AgentRepository, AgentRegistry, AgentScheduler,
    InteractionEngine, EventBus, EventStore, EngineRuntime, ContextManager)
    추가, MemoryEngine 계약 축소(Snapshot 이관), EngineAdapter 세션 생명주기
    계약 갱신은 후속 Task **T1-18~T1-21**에서 진행한다(총 16종, ADR-0022로
    책임 경계별 4개 Task로 분해).
- 의존성: T1-14

#### T1-16: 도메인 확장 (Mission/Workflow 재정의/Step, WorkspaceSession, Agent 계열, LLM Policy 초안)
- 목적: Multi-Agent First 심화 구조의 핵심 도메인을 추가·재정의하고, 향후
  Milestone(M2~M4)에서 구현할 LLM 선택 정책의 **Domain만** 미리 정의한다
  (ADR-0010~0012). **2026-07-23 사용자 지시로 LLM Policy Domain 초안이 이
  Task 범위에 추가됨** (Policy Engine/Router 등 실제 동작 로직은 제외).
- 작업 내용:
  - `domain/mission.py`, `domain/step.py`: `Mission`(목표), `Step`(Task 내부
    세부 실행 단위). `domain/workflow.py`는 Mission→Workflow→Task→Step 계층
    안에서 재정의(`mission_id` 추가, 기존 순환 의존 검증 유지).
  - `domain/session.py`: `WorkspaceSession`(현재 프로젝트/Mission/활성 Workflow/
    활성 Agent/Memory Snapshot/Engine Session).
  - `domain/agent.py`: `Agent`, `AgentRole`, `AgentCapability`(**Coordination**/
    Planning/Coding/Review/Documentation/Research/Vision/Voice/Git/MCP …),
    `AgentStatus`(IDLE/RUNNING/WAITING/PAUSED/STOPPED/ERROR 등).
  - `domain/llm_policy.py` (초안, Domain만): `LLMProvider`(OpenAI/Anthropic/
    Google/xAI), `LLMModel`(provider + 확장 가능한 name 문자열, 초기 모델 목록
    데이터 포함), `LLMEffort`(Low/Medium/High). **LLM Policy Engine, LLM Router,
    Provider/Model 선택 로직, Adapter 변경, 실제 LLM 호출 로직은 절대 구현하지
    않는다.**
  - `.ai/RULES.md`에 "Temporary LLM Policy" 섹션 추가(M2~M4 진행 경로 명시) +
    `docs/llm_policy.example.yaml` 정책 초안 작성.
- 완료 조건(DoD): 추가/재정의된 모델에 대한 단위 테스트가 통과한다(기존 도메인
  테스트 회귀 없음). LLM Policy는 Domain 정의와 문서만 존재하고 동작 로직이
  없음을 확인한다.
- 상태: **DONE (2026-07-23)** — `domain/mission.py`(Mission), `domain/step.py`
  (Step), `domain/session.py`(WorkspaceSession), `domain/agent.py`(Agent,
  AgentRole, AgentCapability(Coordination 포함), AgentStatus), `domain/workflow.py`
  에 `mission_id` 추가(기존 순환/미지정 의존 검증 유지), `domain/llm_policy.py`
  (LLMProvider, LLMModel, LLMEffort, INITIAL_MODELS — Domain 데이터만, Policy
  Engine/Router 없음) 구현. `.ai/RULES.md`에 "Temporary LLM Policy" 섹션
  (§7) 추가, `docs/llm_policy.example.yaml` 정책 초안 작성. 신규 테스트 9개
  추가(전체 41개 통과). `docs/ARCHITECTURE.md`는 변경하지 않음(사용자 지시).
- 의존성: T1-14

#### T1-17: Core/Agent/LLM Domain 마무리 및 코드 품질 도구(Ruff/MyPy) 도입
- 목적: T1-16에서 추가한 Domain을 완성도 있게 마무리하고(Task-Workflow 관계
  보완), 이후 모든 Task에서 상시 사용할 코드 품질 도구를 도입한다. **Domain만
  다루며 Policy Engine/Router/Adapter는 구현하지 않는다.**
- 작업 내용:
  - `domain/task.py`에 `workflow_id: str | None = None` 추가 — Task가 어떤
    Workflow에 속하는지 참조할 수 있도록 함(Mission→Workflow→Task→Step 계층의
    부모 참조 체계를 `Workflow.mission_id`, `Step.task_id`와 동일한 패턴으로
    완성). Workflow 배정 전에도 Task가 존재할 수 있어 선택 필드로 둠(필수 필드로
    하면 `TaskEngine.create_task(project_id, title)` 계약을 건드리게 되어
    Interface 변경이 필요해지므로, 이번 Domain 전용 범위에서는 선택 필드가 맞음).
  - Agent Domain 재검토: 특정 LLM Provider/Model에 의존하는 필드가 없는지
    확인 — 기존 구현이 이미 Provider 비의존임을 확인, 코드 변경 없음.
  - LLM Domain 재검토: `LLMModel`이 고정 Enum이 아니라 `provider + name` 조합의
    확장 가능한 구조인지 확인 — 기존 구현이 이미 이 요건을 만족함을 확인, 코드
    변경 없음.
  - `pyproject.toml`에 `[tool.ruff]`, `[tool.mypy]` 설정과 `dev` 선택적
    의존성(pytest/ruff/mypy)을 추가하고, `ruff`/`mypy` 위반을 모두 수정한다.
- 완료 조건(DoD): `ruff check src tests`, `mypy src`, `pytest` 모두 통과한다.
- 상태: **DONE (2026-07-23)** — `domain/task.py`에 `workflow_id` 필드 추가,
  관련 테스트 2개 추가(전체 43개 통과). `ruff`/`mypy` 설정 추가 및 위반 1건
  수정(줄 길이) 후 전부 통과. Agent/LLM Domain은 기존 구현이 요건을 이미
  만족하여 코드 변경 없음.
- 의존성: T1-16

> **2026-07-24 Task 분해 재검토**: T1-18을 "신규 Interface 정의 및 EngineAdapter
> 세션 계약 확장(총 16종)"이라는 단일 Task로 계획했으나, 아키텍처 검토 결과
> 서로 의존하지 않는 4개 하위 계층(Agent Runtime / Engine Runtime / Memory /
> Interaction)을 한 Task에 묶고 있어 "Task = 하나의 구현 목표 + 하나의 Commit"
> 원칙(ADR-0021)에 맞지 않는다고 판단함. 사용자 승인에 따라 T1-18을 4개 Task
> (T1-18~T1-21)로 분리하고, 이후 Task 번호를 T1-22~T1-28로 순연함(ADR-0022).
> **다만 "인터페이스 정의 → 구현 → 테스트"를 한 Task 안에서 끝내는 기존 원칙은
> 유지**하며, 인터페이스 정의 자체만 별도로 잘게 쪼개지 않는다(과도한 세분화
> 방지).

#### T1-18: Agent Runtime Interfaces
- 목적: Agent Runtime 계층(ARCHITECTURE.md §3.4)과 그 이벤트 인프라(§3.5)의
  계약을 확정한다 (ADR-0010, ADR-0018, ADR-0019). 계약만 정의하고 구체 구현은
  이후 Milestone에서 진행한다.
- 작업 내용 (`interfaces/`):
  - `agent_manager.py` — `AgentManager`(생성/생명주기/상태)
  - `agent_registry.py` — `AgentRegistry`(등록/조회/제거 — **런타임 등록부**,
    프로세스 생존 동안만 유지됨을 docstring에 명시하여 `AgentRepository`와 구분)
  - `agent_scheduler.py` — `AgentScheduler`(Capability 기준 선택/병렬/우선순위)
  - `agent_repository.py` — `AgentRepository`(조회/저장 — **영속 저장소**,
    재시작 후에도 유지됨을 docstring에 명시)
  - `event_bus.py` — `EventBus`(publish/subscribe)
  - `event_store.py` — `EventStore`(Bus의 **독립 구독자**, 기록/Replay/Audit;
    지금 구현 안 함, ADR-0018). `EventBus.subscribe()`가 다른 구독자와 동일한
    API로 EventStore를 등록해야 함(버스 내부에 EventStore 전용 특별 경로를
    두지 않음)을 계약에 명시한다.
- 완료 조건(DoD): 6개 인터페이스 각각에 대해 Fake 구현체 + 계약 테스트가
  통과한다 (실제 로직 없이 계약만 검증).
- 상태: **DONE (2026-07-24)** — `interfaces/agent_manager.py`,
  `agent_registry.py`, `agent_scheduler.py`, `agent_repository.py`,
  `event_bus.py`(+`Event` dataclass), `event_store.py` 6개 파일 추가. 각각
  Fake 구현체(`tests/interfaces/fakes.py`)와 계약 테스트
  (`test_agent_manager.py`/`test_agent_registry.py`/`test_agent_scheduler.py`/
  `test_agent_repository.py`/`test_event_bus.py`/`test_event_store.py`)를
  추가했으며, `test_event_bus.py`에 EventStore가 `EventBus.subscribe()`를
  다른 구독자와 동일한 경로로 등록됨(ADR-0018)을 검증하는 테스트를 포함함.
  `AgentRegistry`(런타임 등록부)와 `AgentRepository`(영속 저장소)는 각각
  `AgentNotRegisteredError`/`AgentNotFoundError`로 예외를 구분해 책임을
  명확히 함. `ruff check src tests`, `mypy src`, `pytest`(66개, 기존 43개 +
  신규 23개) 모두 통과.
- 의존성: T1-15, T1-16

#### T1-19: Engine Runtime Interfaces
- 목적: Engine Runtime과 EngineAdapter의 세션 생명주기 계약을 확정한다
  (ADR-0016). EngineRuntime의 엔진 선택 로직이 EngineAdapter의 정확한 메서드
  시그니처(`capabilities`/`estimate_cost`/`supports_parallel`)에 직접 의존하므로
  두 계약을 같은 Task에서 함께 정의한다.
- 작업 내용 (`interfaces/`):
  - `engine_runtime.py` — `EngineRuntime`(엔진 선택/세션 풀 관리/병렬 실행;
    ADR-0016)
  - `engine_adapter.py` 확장 — `create_session`/`run`/`cancel`/`status`/
    `destroy_session`/`capabilities`/`supports_parallel`/`estimate_cost`
    (기존 `run_task` 기반 계약/테스트를 새 계약으로 교체)
- 완료 조건(DoD): `EngineRuntime` Fake + 계약 테스트, 확장된 `EngineAdapter`
  Fake + 계약 테스트가 통과한다 (`run_task` 기반 기존 테스트는 새 계약으로
  교체됨).
- 상태: **DONE (2026-07-24)** — `interfaces/engine_adapter.py`를
  `create_session`/`run`/`cancel`/`status`/`destroy_session`/`capabilities`/
  `supports_parallel`/`estimate_cost` 세션 계약으로 교체(기존 `run_task` 제거,
  `EngineSessionStatus`/`CostEstimate`/`SessionNotFoundError` 추가).
  `interfaces/engine_runtime.py` 신규 추가 — `EngineRuntime`(엔진 선택/
  세션 풀 관리(내부 캡슐화)/병렬 실행 `run_parallel`; `DuplicateEngineError`/
  `NoSuitableEngineError`/`EngineTaskNotFoundError`). `tests/interfaces/
  fakes.py`의 `FakeEngineAdapter`/`FailingFakeEngineAdapter`를 새 계약에 맞게
  재작성하고 `FakeEngineRuntime`을 추가함. `test_engine_adapter.py`를 새
  계약 기준으로 재작성하고 `test_engine_runtime.py`를 신규 추가(총 13개
  테스트). `ruff check src tests`, `mypy src`, `pytest`(79개, 기존 66개 +
  신규 13개) 모두 통과.
- 의존성: T1-15

#### T1-20: Memory Interfaces
- 목적: Context 조립과 Memory 저장/검색의 역할 분리를 계약으로 확정한다
  (ADR-0017). `ContextManager`가 축소된 `MemoryEngine` 계약을 전제로 설계되므로
  같은 Task에서 함께 다룬다.
- 작업 내용 (`interfaces/`):
  - `context_manager.py` — `ContextManager`(Context 조립/Memory Snapshot
    생명주기; ADR-0017)
  - `memory_engine.py` 재확인 — 현재 구현(`remember`/`recall`)을 점검한 결과
    **Snapshot 관련 메서드가 애초에 존재하지 않아 제거할 코드가 없음을 확인**.
    "저장/검색만 담당"이라는 계약이 이미 만족되어 있으므로 **코드 변경 없음**
    (T1-17에서 Agent/LLM Domain을 재검토 후 변경 없음으로 처리한 것과 동일한
    패턴).
- 완료 조건(DoD): `ContextManager` Fake + 계약 테스트가 통과하고, `MemoryEngine`
  기존 계약·테스트에 회귀가 없음을 확인한다.
- 상태: **DONE (2026-07-24)** — `interfaces/context_manager.py` 신규 추가:
  `ContextManager`(`assemble_context`/`create_snapshot`/`restore_snapshot`,
  `SnapshotNotFoundError`). `WorkspaceSession.memory_snapshot_id`가 가리키는
  Snapshot을 Context Manager가 소유·관리하며 `MemoryEngine`은 이를 알지
  못함을 docstring에 명시. `memory_engine.py`는 재검토 결과 계획대로
  **코드 변경 없음**(Snapshot 관련 메서드가 원래 없어 이미 "저장/검색만"
  계약을 만족). `tests/interfaces/fakes.py`에 `FakeContextManager` 추가,
  `test_context_manager.py` 신규 추가(4개 테스트). 기존 `MemoryEngine`
  테스트(`test_memory_engine.py`)는 변경 없이 그대로 통과. `ruff check
  src tests`, `mypy src`, `pytest`(83개, 기존 79개 + 신규 4개) 모두 통과.
- 의존성: T1-15, T1-16

#### T1-21: Interaction Interfaces
- 목적: 입력 표면 정규화 계약을 확정한다 (ADR-0013). Agent Runtime/Engine
  Runtime/Memory 어느 것과도 의존관계가 없는 독립 계층이라 별도 Task로 둔다.
- 작업 내용 (`interfaces/`):
  - `interaction_engine.py` — `InteractionEngine`(입력 정규화; 기존
    `ConversationEngine` 명칭을 대체, 지금 구현 안 함)
- 완료 조건(DoD): `InteractionEngine` Fake + 계약 테스트가 통과한다.
- 상태: **DONE (2026-07-24)** — `interfaces/interaction_engine.py` 신규
  추가: `InteractionEngine`(`normalize`/`format_response`/
  `supported_surfaces`, `NormalizedRequest` dataclass,
  `UnsupportedSurfaceError`). 기존 `ConversationEngine` 명칭을 대체하며,
  Agent Runtime/Engine Runtime/Memory 어느 것에도 의존하지 않고 UI
  Surfaces와 Workspace Core 사이에만 위치함을 docstring에 명시.
  `tests/interfaces/fakes.py`에 `FakeInteractionEngine` 추가,
  `test_interaction_engine.py` 신규 추가(4개 테스트). `ruff check src
  tests`, `mypy src`, `pytest`(87개, 기존 83개 + 신규 4개) 모두 통과.
  (병렬로 진행된 별도 세션에서도 T1-21 구현이 제안되었으나
  `handle_request` 단일 메서드로 정규화와 응답 변환을 합쳐 Workspace
  Core의 책임과 경계가 흐려질 수 있어 채택하지 않고, ARCHITECTURE.md
  §3.2의 "정규화 + 변환" 2단계 책임에 그대로 대응하는 이 설계를 유지함.)
- 의존성: T1-15

#### T1-22: Workspace Core Skeleton
- 목적: 최상위 오케스트레이터로서 Workspace Core의 최소 형태를 마련한다
  (ADR-0005 유지 + ADR-0010 재정의). 실제 처리 로직은 포함하지 않는다.
- 작업 내용: `core/`에 다음 책임만 구현한다 (모두 Interfaces에만 의존).
  1. 프로젝트 로드 (`ProjectRepository`)
  2. 설정(Config) 로드
  3. 서비스 초기화
  4. WorkspaceSession 관리 (생성/갱신/종료)
  5. Agent Runtime · Engine Runtime 초기화 (Registry/Scheduler/Manager/EventBus,
     Engine Runtime 준비)
  6. Workflow 시작 (`WorkflowEngine`)
  7. 종료(Shutdown)
  ※ Task 실행은 Workspace Core가 하지 않고 **Agent Runtime에 위임**한다.
  ※ Registry/Scheduler/Manager/EventBus/EngineRuntime을 조립하는 코드가
    번거로워지면 `AgentRuntime` 파사드 인터페이스 도입을 재검토한다(지금은
    도입하지 않음 — YAGNI).
- 완료 조건(DoD): Mock Interfaces를 주입해 위 책임이 단위 테스트로 검증되고,
  Core 코드에 구체 클래스 직접 참조가 없음을 확인한다. **Task를 직접 실행하지
  않고 Agent Runtime에 위임함**을 테스트로 확인한다.
- 상태: DONE
- 의존성: T1-16, T1-18, T1-19

#### T1-23: Repositories
- 목적: Project/Agent 데이터와 이벤트 로그를 세션 간에 영속화한다 (ADR-0004,
  ADR-0014 반영).
- 작업 내용: `storage/`에 `FileProjectRepository`, `FileAgentRepository`,
  `FileEventStore`(append-only 로그)를 구현한다.
- 완료 조건(DoD): 세 구현체가 각 인터페이스 계약을 만족함을 테스트로 확인하고,
  Workspace Core에 주입해도 Core 코드 변경이 필요 없음을 확인한다.
- 상태: DONE
- 의존성: T1-18

#### T1-24: CLI
- 목적: 사람이 실제로 Project를 다뤄볼 수 있는 최소 진입점을 제공한다 (UI
  Surface의 하나).
- 작업 내용: `cli/`에 Workspace Core와 파일 저장소를 연결해 Project 생성·조회
  명령을 구현한다 (Agent/협업 실행은 구체 구현이 없는 이 시점에는 골격까지만).
- 완료 조건(DoD): CLI로 Project 생성 → 조회가 end-to-end로 동작한다.
- 상태: DONE
- 의존성: T1-22, T1-23

#### T1-25: Tests
- 목적: Test Before Complete 원칙에 따라 Milestone 1 전체 구현 산출물을
  마지막으로 한 번 더 점검한다. (개별 Task(T1-18~T1-24)는 각자 완료 조건에
  자체 테스트를 이미 포함하므로, 이 Task는 신규 테스트를 처음 작성하는 단계가
  아니라 **전체 스위트 통합 점검 및 커버리지 보강**이다.)
- 작업 내용: `pytest` 설정을 정리하고, `tests/{domain,interfaces,core,storage,
  cli}/` 전체를 훑어 누락된 컴포넌트별 테스트를 보강한다. `ruff`/`mypy`도 전체
  기준으로 함께 통과시킨다.
- 완료 조건(DoD): `ruff`, `mypy`, `pytest` 실행 시 전체가 통과한다.
- 상태: DONE
- 의존성: T1-16 ~ T1-24

#### T1-26: Documentation
- 목적: 문서와 실제 구현이 일치하는지 확인한다 (Documentation First).
- 작업 내용: 구현된 구조/디렉터리/컴포넌트를 ARCHITECTURE.md와 대조하고 필요 시
  갱신한다.
- 완료 조건(DoD): 문서와 실제 코드가 일치한다.
- 상태: DONE
- 의존성: T1-16 ~ T1-25

#### T1-27: ADR
- 목적: EngineAdapter(세션 생명주기 계약 포함) 설계와 파일 기반 저장 결정을 정식
  확정한다.
- 작업 내용: `.ai/DECISIONS.md`의 ADR-0002, ADR-0004 상태를 "승인됨"으로 갱신한다
  (ADR-0002는 ADR-0009·ADR-0015의 세션 생명주기 계약을 포함해 재확정).
- 완료 조건(DoD): 두 ADR 상태가 "승인됨"으로 표시된다.
- 상태: DONE
- 의존성: T1-19(ADR-0002), T1-23(ADR-0004)

#### T1-28: Milestone 1 Review
- 목적: Approval Required 원칙에 따라 Milestone 1 산출물을 검토받는다.
- 작업 내용: 도메인(Agent 포함), 전체 Interfaces, Workspace Core 골격, 저장소,
  CLI, 테스트 결과를 제시하고 승인을 요청한다. **T1-29(SOP Skills System)도
  Milestone 1 기간 중 추가된 산출물이므로 함께 검토 대상에 포함한다.**
- 완료 조건(DoD): 위 모든 Task가 DONE이고 테스트가 통과한 상태에서 사용자가
  승인한다.
- 상태: **DONE (2026-07-25 사용자 승인 — Milestone 1 완료)**
- 의존성: T1-01 ~ T1-27

#### T1-29: Standard Operating Procedure (SOP) Skills System
- 목적: LLM/구현 엔진에 독립적인 표준 작업 절차(SOP)를 `.ai/skills/`에
  문서화해, 이후 어떤 구현 엔진이 작업을 이어받아도 동일한 절차를 따르게
  한다.
- 작업 내용: `.ai/skills/`에 7개 SOP 가이드라인 문서를 추가한다
  (`Repository-Analysis.md`, `Architecture-Review.md`, `Task-Planning.md`,
  `Task-Implementation.md`, `Code-Review.md`, `Documentation.md`,
  `Milestone-Review.md`). 공통 8개 섹션 형식과 Repository First/Interface
  First/SOLID/YAGNI 등 이 프로젝트의 핵심 원칙을 반영한다.
- 완료 조건(DoD): 7개 문서가 동일한 형식을 따르고, `pytest`/`ruff`/`mypy`에
  회귀가 없다.
- 상태: **DONE (2026-07-24)** — 별도로 진행된 세션(`google-labs-jules[bot]`,
  PR #1)에서 작업되어 origin 브랜치에 먼저 병합됨. 원래 계획(T1-01~T1-28)에는
  없던 Task로, 병합 시점에 T1-28(Milestone 1 Review) 뒤에 편입함. 코드
  변경 없이 `.ai/skills/` 문서만 추가되어 기존 테스트에 영향 없음.
- 의존성: 없음 (Milestone 1의 다른 구현 Task와 독립적인 문서 작업)

---

## Milestone 2 — 멀티 에이전트 코어 (Multi-Agent Core)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 2 Definition of Done" 참고.
> 2026-07-25 Milestone 1 완료 승인 직후, ADR-0022 원칙(아키텍처 책임 경계로
> 분해, 정의·구현·테스트는 한 Task 안에서 완결)에 따라 T2-01~T2-07(7개)을
> 확정했다. **2026-07-25 T2-01 구현 직후 재분해**: 원래 T2-01은 Registry·
> Scheduler·Manager·EventBus 4종을 한 Task로 묶고 있었으나, 실제 착수 시
> 사용자 지시로 "AgentRuntime 파사드 + AgentSession + Lifecycle(Start/Stop/
> Shutdown)"만 다루고 Scheduler·EventBus는 범위에서 제외하기로 재정의됨
> (T1-22가 보류했던 AgentRuntime 파사드 도입을 재검토하는 결정이기도 함).
> 이에 따라 Scheduler·EventBus를 신규 **T2-02**로 분리하고, 이하 Task를
> T2-03~T2-08(구 T2-02~T2-07)로 순연했다. 총 8개 Task.
>
> T2-01~T2-05는 서로 독립(순서 무관, 병렬 가능 — 단, T2-02는 T2-01이 만든
> `AgentRuntime`에 Scheduler 연동을 붙이므로 사실상 T2-01 이후 진행 권장),
> T2-06은 T2-01~T2-05 전부에 의존, T2-07·T2-08은 순차 진행.
>
> **설계 판단 (T2-05, 구 T2-04)**: `docs/ARCHITECTURE.md` §7 표는
> `EngineRuntime`/`EngineAdapter` 구체 구현을 Milestone 3로 표시하지만,
> Milestone 2 DoD 3번("Mock EngineAdapter 위에서 시나리오 통과")을
> 만족하려면 최소한의 `EngineRuntime` 구현과 `MockEngineAdapter`가 필요해
> 이를 M2로 앞당김. M3에서는 `MockEngineAdapter`만 실제 Claude Code 등
> 어댑터로 교체한다.

#### T2-01: AgentRuntime + AgentSession 구현
- 목적: Agent를 실제로 실행할 수 있는 최소 Runtime 기반을 구축한다
  (T1-22가 보류한 `AgentRuntime` 파사드 도입 재검토).
- 작업 내용: `domain/agent_session.py`에 `AgentSession`(session_id, agent_id
  — 상태는 중복 보관하지 않고 `AgentRegistry`에서 조회)을 정의한다.
  `runtime/agent/agent_runtime.py`에 `AgentRuntime`을 구현한다 —
  `AgentManager`/`AgentRegistry` 두 Interface만 키워드 전용 생성자로 주입,
  `start_agent`/`stop_agent`/`get_session`/`get_agent_state`/`shutdown`
  제공. Scheduler/EventBus/Core Engines/Context Manager/LLM 호출은 범위에서
  제외(각각 T2-02, T2-04, T2-05 이후에서 다룸).
- 완료 조건(DoD): `AgentManager`/`AgentRegistry` 계약을 그대로 사용해
  Lifecycle(시작/중지/종료)과 상태 조회가 단위 테스트로 검증되고, 배제
  범위(Scheduler/EventBus 등)의 어떤 구체 클래스도 import하지 않는다.
- 상태: **DONE (2026-07-25)** — `AgentSession`, `AgentRuntime`,
  `AgentSessionNotFoundError` 구현. `tests/runtime/agent/
  test_agent_runtime.py` 11개 테스트(시작/상태 조회/중지/registry 제거/
  세션 제거/unknown 예외 3종/shutdown 전체 정리/이중 중지 방지). `ruff`/
  `mypy`/`pytest`(150개, 기존 139개 + 신규 11개) 모두 통과.
- 의존성: T1-18

#### T2-02: Agent Scheduler + Event Bus 구현
- 목적: Capability 기준 Agent 선택(Scheduler)과 Agent 간 Event 발행/구독
  (EventBus)을 실제 동작하는 in-memory 구현체로 제공한다.
- 작업 내용: `runtime/agent/`에 `InMemoryAgentScheduler`를 구현한다.
  `events/`에 `InMemoryEventBus`를 구현한다(ARCHITECTURE.md §9 디렉터리
  매핑 기준).
- 완료 조건(DoD): 두 구현체가 각 Interface 계약 테스트를 만족하고,
  Scheduler가 후보 목록에서 Capability를 만족하는 Agent만 선택함을,
  EventBus가 여러 구독자에게 발행 이벤트를 전달함을(구독자 하나가 예외를
  던져도 나머지에는 영향 없음, `EventBus` 계약) 테스트로 확인한다.
- 상태: **DONE (2026-07-25)** — `runtime/agent/agent_scheduler.py`의
  `InMemoryAgentScheduler`, `events/event_bus.py`의 `InMemoryEventBus`
  구현(둘 다 `tests/interfaces/fakes.py`의 대응 Fake 로직을 그대로 승격,
  신규 설계 판단 없음). `tests/runtime/agent/test_agent_scheduler.py`
  3개, `tests/events/test_event_bus.py` 6개 신규 테스트. `AgentRuntime`
  과의 연동은 T2-06 범위. `ruff`/`mypy`/`pytest`(159개, 기존 150개 +
  신규 9개) 모두 통과.
- 의존성: T1-18, T2-01(권장 순서 — 강제 의존은 아님)

#### T2-03: Core Engines 구현
- 목적: Task 생성/전이, Workflow 계획, 승인 게이트, 자동화 트리거를 실제
  동작하는 구현체로 제공한다.
- 작업 내용: `engines/`에 `InMemoryTaskEngine`, `InMemoryWorkflowEngine`,
  `InMemoryApprovalEngine`, `InMemoryAutomationEngine`을 구현한다.
- 완료 조건(DoD): 4개 구현체가 각 Interface 계약을 만족하고, `ApprovalEngine`
  이 승인 대상 4대 행위(아키텍처 변경/신규 기능/리팩토링/Milestone 완료,
  ADR-0003)를 판별·차단함이 테스트로 확인된다.
- 상태: **DONE (2026-07-25)** — `engines/`에 `InMemoryTaskEngine`/
  `WorkflowEngine`/`ApprovalEngine`/`AutomationEngine` 구현(전부
  `tests/interfaces/fakes.py`의 대응 Fake 로직 승격, 신규 설계 없음).
  **부가 수정**: `interfaces/approval_engine.py`의 `ApprovalActionType.
  PHASE_COMPLETION`이 ADR-0021(Phase→Milestone 용어 전환) 이후에도
  갱신되지 않았음을 발견해 `MILESTONE_COMPLETION`으로 정정(사용처 2곳 —
  인터페이스 정의, 기존 테스트 1곳 — 모두 갱신). `task_engine.py`/
  `workflow_engine.py`/`automation_engine.py`의 "Phase 2에서 작성한다"
  docstring도 "Milestone 2(T2-03)에서 작성한다"로 정정(`memory_engine.py`
  는 T2-04 범위라 이번엔 손대지 않음). `tests/engines/`에 17개 신규
  테스트 — `ApprovalActionType` 4개 값 전부를 순회하며 submit→PENDING→
  decide→APPROVED를 검증하는 테스트로 DoD의 "4대 행위 판별·차단"을 직접
  증명. `ruff check src tests`, `mypy src`, `pytest`(176개, 기존 159개 +
  신규 17개) 모두 통과.
- 의존성: T1-15

#### T2-04: Memory 계열 구현
- 목적: Context 조립과 저장/검색 역할 분리(ADR-0017)를 실제 동작하는
  구현체로 제공한다.
- 작업 내용: `memory/`에 `InMemoryMemoryEngine`, `InMemoryContextManager`를
  구현한다. `ContextManager`는 내부적으로 `MemoryEngine`을 사용해 Context를
  조립하고 Snapshot 생명주기를 관리한다.
- 완료 조건(DoD): Snapshot 생성 → 복원 왕복 결과가 원본 Context와 동일함이
  테스트로 확인되고, `MemoryEngine`이 Context Manager를 거치지 않고 직접
  Snapshot을 다루지 않음(ARCHITECTURE.md §8 규칙 7 준수)이 코드로 확인된다.
- 상태: **DONE (2026-07-25)** — `memory/memory_engine.py`의
  `InMemoryMemoryEngine`(Fake 로직 승격, Snapshot 개념을 전혀 모름),
  `memory/context_manager.py`의 `InMemoryContextManager`. T2-02/03과
  달리 **단순 Fake 승격이 아니라 실제 의존 배선을 새로 설계**함 — 기존
  `FakeContextManager`는 자체 dict에 Snapshot을 보관했지만, 이번 구현은
  `MemoryEngine`을 생성자로 주입받아 `remember(snapshot_id,
  json.dumps(context))`/`recall()`+`json.loads()`로 실제 저장·복원함
  (§8 규칙 7 준수를 코드 구조로 강제). `tests/memory/
  test_context_manager.py`에 "MemoryEngine.recall()로 Snapshot이 실제
  저장되었는지" 직접 확인하는 테스트를 포함해 DoD를 코드+테스트 양쪽으로
  증명. `tests/memory/`에 10개 신규 테스트. `ruff check src tests`,
  `mypy src`, `pytest`(186개, 기존 176개 + 신규 10개) 모두 통과.
- 의존성: T1-20

#### T2-05: Engine Runtime 최소 구현 + Mock EngineAdapter
- 목적: Milestone 2 DoD("Mock EngineAdapter 위에서 협업 시나리오 통과")를
  만족하기 위해, 실제 LLM을 호출하지 않는 최소 Engine Runtime과 Mock
  Adapter를 제공한다. Milestone 3에서 실제 Claude Code 등 어댑터로 교체될
  자리표시자다.
- 작업 내용: `runtime/engine/`에 `InMemoryEngineRuntime`(capabilities 기반
  엔진 선택, 순차 실행)을 구현한다. `adapters/`에 `MockEngineAdapter`(세션
  생성/실행/종료 계약은 만족하되 즉시 성공 결과를 반환하고 실제 프로세스는
  호출하지 않음)를 구현한다.
- 완료 조건(DoD): `EngineRuntime.run()`이 `MockEngineAdapter`를 통해 Task를
  "실행"하고 `EngineResult(success=True)`를 반환함이 테스트로 확인된다.
- 상태: **DONE (2026-07-25)** — `runtime/engine/engine_runtime.py`의
  `InMemoryEngineRuntime`, `adapters/mock_engine_adapter.py`의
  `MockEngineAdapter`(둘 다 `tests/interfaces/fakes.py`의
  `FakeEngineRuntime`/`FakeEngineAdapter` 로직 승격, 신규 설계 없음).
  `MockEngineAdapter.estimate_cost()`는 Fake의 임의값(100 토큰/$0.01) 대신
  실제 엔진을 호출하지 않는다는 사실을 정직하게 반영해 0/0.0으로 둠.
  `tests/adapters/test_mock_engine_adapter.py` 5개, `tests/runtime/engine/
  test_engine_runtime.py` 7개(DoD를 직접 명시하는
  `test_run_executes_task_via_mock_adapter_and_returns_success` 포함)
  신규 테스트. `ruff check src tests`, `mypy src`, `pytest`(198개, 기존
  186개 + 신규 12개) 모두 통과.
- 의존성: T1-19

#### T2-06: 능력별 Agent 골격 구현
- 목적: Coordination/Planning/Coding/Review/Documentation Capability를 가진
  Agent가 Event 기반으로 협업하도록 한다.
- 작업 내용: `agents/`에 Capability별 Agent 클래스(최소 Planning/Coding/
  Review/Documentation, 필요 시 Coordination)를 구현한다. 각 Agent는
  `EventBus`를 구독하고 자신의 작업 완료 시 다음 Event를 발행한다. 실행은
  T2-05의 `EngineRuntime`에, Context는 T2-04의 `ContextManager`에, 도메인
  작업은 T2-03의 Core Engines에, Lifecycle은 T2-01의 `AgentRuntime`에,
  선택은 T2-02의 `AgentScheduler`에 위임한다(ARCHITECTURE.md §3.6, §8
  규칙 5).
- 완료 조건(DoD): `MissionPlanned`→`CodeCompleted`→`ReviewCompleted`→
  `DocumentationCompleted` Event 체인이 Agent 간 협업으로 자동 진행됨이
  테스트로 확인된다.
- 상태: **DONE (2026-07-25)** — `agents/`에 `PlanningAgent`(진입점,
  `plan_mission()` 호출로 체인 시작)/`CodingAgent`/`ReviewAgent`/
  `DocumentationAgent` 4종 구현(Coordination은 선형 파이프라인에 불필요해
  배제, YAGNI). 각 Agent는 생성자에서 `AgentRuntime.start_agent()`로
  자신을 시작(T2-01)하고 `EventBus.subscribe()`로 트리거 Event를 구독.
  `CodingAgent`/`ReviewAgent`/`DocumentationAgent`는 `EngineRuntime.run()`
  (T2-05, Mock Adapter)으로 실행을 위임하고 `TaskEngine`(T2-03)으로 상태를
  전이함. `DocumentationAgent`는 완료 시 `ContextManager.create_snapshot()`
  (T2-04)으로 ARCHITECTURE.md §5의 "Context Manager → Memory Engine 갱신"
  마무리 단계를 구현. `agents/scheduling.py`의 `find_agent_by_capability()`
  로 `AgentScheduler`(T2-02) 사용을 이벤트 핸들러 안에 억지로 넣지 않고
  분리해 테스트로 직접 검증. **설계 함정 발견 및 회피**: `InMemoryEventBus`
  는 핸들러 내부에서 재귀적으로 `publish()`가 호출되면(Agent가 이벤트
  처리 중 다음 이벤트를 발행) 동기 재귀 특성상 수신 순서가 뒤집힘(가장
  안쪽에서 발행된 이벤트를 먼저 관측) — 테스트는 순서가 아니라 수신된
  Event 타입의 **집합**과 최종 Task 상태(DONE)로 체인 완주를 검증해 이
  함정을 피함. **남은 공백**: `AgentManager`/`AgentRegistry`의 프로덕션
  구현체(`InMemory*`)가 아직 없어(T2-01에서 의도적으로 보류) 이 둘만
  기존 Fake를 사용하고, 나머지(EventBus/Scheduler/TaskEngine/
  EngineRuntime+MockAdapter/ContextManager)는 T2-02~05에서 만든 실제
  구현체를 사용함. `tests/agents/test_pipeline.py`에 5개 신규 테스트
  (전체 체인 완주, Context Snapshot 생성, Scheduler로 Capability 탐색
  성공/실패, 4개 Agent 모두 서로 다른 Capability로 등록됨). `ruff check
  src tests`, `mypy src`, `pytest`(203개, 기존 198개 + 신규 5개) 모두
  통과.
- 의존성: T2-01, T2-02, T2-03, T2-04, T2-05

#### T2-07: 통합 시나리오 테스트
- 목적: Milestone 2 Definition of Done 3개 항목을 end-to-end로 증명한다.
- 작업 내용: 전체 스위트 통합 점검(T1-25와 동일한 패턴). Event Store
  Replay 검증, 승인 게이트 차단 시나리오 검증을 추가한다.
- 완료 조건(DoD): `ruff`, `mypy`, `pytest` 전체가 통과하고, Milestone 2
  Definition of Done 3개 항목이 각각 명시적 테스트로 매핑된다.
- 상태: **DONE (2026-07-25)** — 사용자가 제시한 설계 철학(Architecture
  First/최소 복잡성/YAGNI/응집도/점진적 확장/기존 코드 존중, 기억에 저장)
  을 적용해 기존 테스트를 먼저 점검한 결과 실제 빈틈 2곳만 남았음을 확인:
  (1) `tests/agents/test_pipeline.py`에
  `test_event_store_records_full_pipeline_event_chain` 추가 —
  `FileEventStore`(T1-23)를 `EventBus.subscribe(event_store.record)`로
  연결해 DoD 1번("Event Bus+Event Store로 협업과 이벤트 기록")을 증명.
  (2) `tests/engines/test_workflow_engine.py`에
  `test_plan_executes_mission_workflow_task_step_hierarchy` 추가 —
  실제 `TaskEngine`으로 생성한 Task를 `Mission`→`Workflow`→`Task`→`Step`
  계층으로 엮어 DoD 2번의 Workflow 실행 부분을 증명. DoD 3번은 T2-06의
  `test_mission_planned_triggers_full_event_chain`으로 이미 검증되어
  있어 재작성하지 않음. 승인 게이트 차단도 T2-03의
  `test_approval_action_type_covers_exactly_four_gated_actions`로 이미
  충분히 검증되어 있어 중복 테스트를 만들지 않음(최소 복잡성/기존 코드
  존중). 새 클래스/파일/추상화 없음 — 기존 두 테스트 파일에 테스트만
  추가. `ruff check src tests`, `mypy src`, `pytest`(205개, 기존 203개 +
  신규 2개) 모두 통과.
- 의존성: T2-01 ~ T2-06

#### T2-08: Milestone 2 Review + Retrospective
- 목적: Approval Required 원칙에 따라 Milestone 2 산출물을 검토받는다.
  사용자 제안으로 단순 산출물 검토를 넘어 **Milestone Retrospective**로
  범위를 확장함 — 목표 달성 여부/설계 원칙 적용 결과/기술 부채/M3 과제/
  아키텍처 변경 필요성/유지하기로 한 설계와 이유를 함께 기록해, M3 착수
  시 "왜 지금 구조가 이렇게 되었는지"를 다시 조사할 필요가 없게 한다.
- 작업 내용: AgentRuntime, Agent Scheduler + Event Bus, Core Engines,
  Memory 계열, Engine Runtime + Mock Adapter, 능력별 Agent, 통합 시나리오
  테스트 결과를 제시하고 승인을 요청한다.
- 완료 조건(DoD): 위 모든 Task가 DONE이고 테스트가 통과한 상태에서 사용자가
  승인한다.
- 상태: **DONE (2026-07-25 사용자 승인 — Milestone 2 완료)**
- 의존성: T2-01 ~ T2-07

**Milestone 2 Retrospective**

**1. 목표 달성 여부** — Goal("Agent Runtime과 Event Store, 능력별 Agent를
구현해 실제 멀티 에이전트 협업이 동작하게 하고, Agent가 사용하는 Core
Engines를 구현한다") 및 DoD 3개 항목 전부 달성함:
1. Agent 등록/선택/스케줄링/생명주기 + Event Bus·Event Store 협업·기록 —
   T2-01(Lifecycle)/T2-02(Scheduler+EventBus)/T2-06(4개 Agent 등록 검증)/
   T2-07(`FileEventStore` Replay 검증)
2. Core Engines(Task/Workflow/Memory/Approval/Automation) + Mission→
   Workflow→Task→Step 실행 — T2-03/T2-04/T2-07
3. Mock EngineAdapter 위 Planner→Coding→Review→Documentation 협업 — T2-05/
   T2-06

`pytest` 205개 통과, `ruff`/`mypy` 클린. 신규 소스 21개 파일, 약 2,093줄.

**Milestone 2는 계획된 범위를 모두 완료하였다. 현재 남아 있는 항목은
Milestone 2의 미완료가 아니라, Milestone 3 이상의 확장 범위 또는
의도적으로 이월한 기술 부채이다.**

**2. 설계 원칙 적용 결과 (DX-02)** — T2-01~06은 철학 공식화 이전 작업이나
사후 확인 결과 이미 원칙을 따르고 있었음(Fake 승격 패턴=점진적 확장,
AgentRuntime 재도입=필요성 확인 후 추상화). T2-07이 첫 공식 적용 사례로,
기존 테스트 점검 후 실제 빈틈 2곳만 채우고 새 파일 0개 생성 — 원칙이
실제로 작업량을 줄인다는 것을 증명함. 가장 뚜렷한 실천은 T2-06에서
`AgentScheduler`를 이벤트 핸들러에 강제로 넣지 않고 별도 헬퍼로 분리한
판단.

**3. 기술 부채 목록** (성격별로 구분)

*Deferred by Design* (의도적으로 뒤로 미룬 설계 — 부채라기보다 계획된
순연):
- #1 `AgentManager`/`AgentRegistry` 프로덕션 구현체(`InMemory*`) 없음
  (T2-01에서 의도적 보류, YAGNI)
- #2 CLI가 `WorkspaceCore`를 완전히 쓰지 못함(T1-24 결정 — 이제 T2-03/04
  구현 완료로 재검토 가능 시점)
- #5 `MockEngineAdapter.supports_parallel()=True`이나 실제 동시성 미검증
  (M3 실제 병렬 어댑터 도입 시 재검증 필요)

*Implementation Observation* (구현 중 발견한 특성/관찰 — 결함은 아니나
기록해 둘 가치가 있음):
- #3 `InMemoryEventBus`가 핸들러 내부 재귀 `publish()` 시 수신 순서를
  뒤집음(문서화 안 됨, 테스트는 이미 회피 설계됨)
- #4 Event ID 생성 방식이 컴포넌트마다 다름(Agent는 `uuid4`, Core/Runtime
  클래스는 로컬 `itertools.count`) — 기능적 문제 없음, 일관성만 부재
- #6 `Step` 도메인이 아직 Workflow 실행에 실질적으로 반영되지 않음(T2-07
  에서 존재만 확인, Task 단위로만 동작)

**4. M3에서 해결할 과제** — ROADMAP.md 기존 M3 범위(Engine Runtime/Adapter
실제 구현, Interaction Layer)는 변경하지 않는다. **M3는 기술 부채 청산이
목표가 아니라 실제 Engine Runtime과 Engine Adapter 구현이 목표다.** 다만
M3 진행 중 자연스럽게 해결 가능한 Deferred by Design 항목(#1 AgentManager/
Registry, #2 CLI 통합, #5 병렬성 검증)은 별도 Task로 포함할 수 있다.
Implementation Observation 항목(#3/#4/#6)은 실사용 중 문제가 생기면 그때
Task화한다.

**5. 아키텍처 변경이 필요한 부분** — 없음. T1-26에서 확인한 ARCHITECTURE.md
와 구현의 일치가 M2 진행 중에도 깨지지 않음 — 기존 설계(§3.4~3.9)가 실제
구현을 정확히 예측했다는 뜻이다. `InMemoryEventBus`의 재귀 발행 순서
특성(#3)은 문서화되지 않은 구현 세부사항이라 M3에서 실사용 패턴이 늘면
재검토 권장(지금 당장 필요하지 않음).

**6. 유지하기로 결정한 설계와 이유**
- AgentRuntime을 별도 파사드로 도입(T2-01) — T1-22의 YAGNI 보류를
  재검토, Lifecycle 관리 반복 필요성 확인 + WorkspaceCore와 동일한 DI
  패턴 유지
- Scheduler/EventBus를 AgentRuntime에서 분리(T2-01→02 재분해) — 응집도
  원칙, AgentRuntime은 순수 Lifecycle만 담당
- ContextManager가 MemoryEngine을 실제로 사용(T2-04) — §8 규칙 7을 코드
  구조로 강제
- MockEngineAdapter를 테스트용 Fake와 별도 유지(T2-05) — M3에서 Mock만
  교체 가능하게 관심사 분리
- AgentScheduler를 이벤트 핸들러 밖 헬퍼로 사용(T2-06) — 강제 사용 대신
  실제 필요한 형태로만, 최소 복잡성 원칙 실천

---

## Milestone 3 — 실행 엔진 연동 & 상호작용 (Engine Integration & Interaction)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 3 Definition of Done" 참고.
> Task 목록은 별도로 준비된 계획을 기준으로 순차 추가한다(사용자 제공).
> **M3 목표는 M2 Retrospective에서 이월된 기술 부채 청산이 아니라 실제
> Engine Runtime/Engine Adapter 구현이다** — Deferred by Design 부채(#1
> AgentManager/Registry, #2 CLI 통합, #5 병렬성 검증)는 자연스럽게 해결
> 가능한 경우에만 개별 Task로 포함한다.

#### M3-T01: Engine Runtime 프로덕션 구현
- 목적: Engine Runtime이 `EngineAdapter`를 이용해 실제 Engine 실행을
  관리할 수 있는 기반을 구축한다. Runtime 자체의 책임만 다루며, 실제
  Claude Code 연동은 이후 Task에서 구현한다.
- 작업 내용: Engine 실행 요청/상태 관리, 실행 생명주기(Start/Running/
  Completed/Failed/Cancelled), 실행 취소(Cancel), Timeout 처리 구조,
  Engine Event 발행, Runtime 테스트.
- 완료 조건(DoD): `MockEngineAdapter`를 통한 실행 가능, 상태 전이 검증,
  Cancel 동작 검증, Timeout 처리 구조 확인, Event 발행 검증, `pytest`/
  `ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-25)** — `runtime/engine/managed_engine_runtime.py`
  에 `ManagedEngineRuntime` 신규 구현. **설계 판단**: T2-05의
  `InMemoryEngineRuntime`(Multi-Engine 등록·Capability 선택 위주의 "최소
  구현")은 "M2에서 완료된 기능은 수정하지 않는다"는 지시에 따라 전혀
  건드리지 않고, 새 파일에 새 클래스로 구현함 — 목적이 근본적으로 다르기
  때문(이번 Task는 Multi Engine·Engine Registry를 명시적으로 제외 범위로
  두고, 대신 단일 Adapter의 생명주기·Timeout·Cancel·Event를 깊게 다룸).
  기존 `EngineRuntime`/`EngineAdapter` 인터페이스(T1-19)는 그대로
  사용하고 새 Interface는 추가하지 않음. 생명주기는 기존
  `EngineSessionStatus`(RUNNING/COMPLETED/FAILED/CANCELLED)를 재사용 —
  "Start"는 별도 상태가 아니라 RUNNING 전이로 해석해 새 Enum을 만들지
  않음. Timeout·Cancel은 `adapter.run()`을 백그라운드 스레드로 실행하고
  `Thread.join(timeout)`으로 감시하는 최소 구조로 구현(기존 동기
  Interface는 변경하지 않음 — Python은 실행 중인 스레드를 강제 종료할 수
  없으므로 "구조"만 제공하고 실제 강제 중단은 하지 않음, 문서화된
  한계). `EventBus`(T2-02)를 주입받아 `engine_task_started`/
  `completed`/`failed`/`timeout`/`cancelled` Event를 발행. `run_parallel`
  은 진짜 병렬 실행 없이 순차적으로 `run()`을 반복 호출(병렬 실행은
  제외 범위). `tests/runtime/engine/test_managed_engine_runtime.py`에
  14개 신규 테스트 — 정상 실행/중복 등록/미등록/Capability 불일치/상태
  전이/`EngineExecutionError` 전파(기존 `FailingFakeEngineAdapter`
  재사용)/Cancel(사후 + 실행 중 동시 호출, 로컬 `SlowEngineAdapter`로
  스레드 경합 재현)/Timeout 구조/Event 발행/`run_parallel` 순서 보존.
  타이밍 기반 테스트는 5회 연속 실행으로 안정성 확인. `ruff check src
  tests`, `mypy src`, `pytest`(219개, 기존 205개 + 신규 14개) 모두 통과.
- 의존성: T1-19, T2-05(설계 참고용, 코드 의존 없음)

#### M3-T02: Claude Code Adapter
- 목적: `EngineAdapter` 계약을 충족하는 실제 Claude Code CLI 어댑터를
  구현한다.
- 작업 내용: `ClaudeCodeEngineAdapter` 구현, `EngineAdapter` 계약 충족,
  Claude Code CLI 실행, stdout/stderr 수집, 실행 결과 반환,
  `EngineExecutionError` 처리.
- 완료 조건(DoD): DoD는 명시적으로 재확인되지 않았으나 `EngineAdapter`
  계약 테스트 전부 통과 + `pytest`/`ruff`/`mypy` 통과로 간주함(M3-T01과
  동일한 기준).
- 상태: **DONE (2026-07-25)** — `adapters/claude_code_engine_adapter.py`
  에 `ClaudeCodeEngineAdapter` 신규 구현. **사전 조사**: 로컬
  `claude --help`로 실제 플래그를 확인(`-p`/`--print`, `--output-format
  json`, `--permission-mode`, `--model`, `--session-id`) — 추측하지 않고
  1차 자료로 확정. `--output-format json`의 실제 필드명은 사용자 승인
  하에 `claude -p "숫자 42라고만 답하세요." --output-format json`을 1회
  실제 호출해 검증함(`is_error`/`result`/`session_id`/`total_cost_usd`
  등 확인, 실제 API 비용 소액 발생). **설계 결정**: `create_session()`은
  `uuid4()`를 생성해 Claude Code의 `--session-id`에 그대로 매핑(우리
  시스템 세션 개념과 CLI 세션 개념을 자연스럽게 일치시킴). `--permission-
  mode`는 헤드리스에서 영원히 대기하는 `manual`을 생성자에서
  `ValueError`로 차단하고 기본값을 `acceptEdits`로 둠. JSON 파싱은
  방어적으로 처리(`is_error`/`result` 없으면 원문 텍스트+종료 코드로
  폴백). `FileNotFoundError`(CLI 미설치)/`subprocess.TimeoutExpired`만
  `EngineExecutionError`로 변환(계약대로 "호출 자체 실패"), 0이 아닌
  종료 코드는 예외가 아니라 `EngineResult(success=False)`로 반환(계약대로
  "Task 처리 자체 실패"). **알려진 한계(M3-T03으로 명시적 이관)**:
  `run()`이 `subprocess.run()`으로 동기 실행되어 `cancel()`이 실제 OS
  프로세스를 종료하지 못함(상태만 CANCELLED로 표시) — 진짜
  `terminate`/`kill`은 `ProcessRunner`(M3-T03) 책임으로 docstring에
  명시. `tests/adapters/test_claude_code_engine_adapter.py`에 16개
  신규 테스트 — **전부 `unittest.mock.patch("subprocess.run", ...)`로
  처리해 실제 프로세스를 호출하지 않음**(비용·속도·비결정성 방지).
  `ruff check src tests`, `mypy src`, `pytest`(235개, 기존 219개 + 신규
  16개) 모두 통과.
- 의존성: M3-T01, T1-19

#### M3-T03: Process Management
- 목적: `ClaudeCodeEngineAdapter`가 실제 OS 프로세스를 안전하게 실행·
  Timeout·Cancel할 수 있는 기반을 제공한다.
- 작업 내용: `ProcessRunner` 구현, subprocess 관리, Timeout 시
  terminate/kill, Cancel 처리, 종료 코드 관리.
- 완료 조건(DoD): 실제(안전한) 프로세스로 정상 실행/Timeout 강제 종료/
  Cancel이 검증되고, `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-25)** — `adapters/process_runner.py`에
  `ProcessRunner`(`subprocess.Popen` 기반), `ProcessResult`,
  `ProcessNotFoundError` 신규 구현. Interface(ABC)는 만들지 않음 —
  상위 계층이 직접 의존하는 대상이 아니라 Adapter 내부 협력자이므로
  Interface First 대상이 아니라고 판단.
  **`ClaudeCodeEngineAdapter` 리팩터링**: `subprocess.run()` 직접 호출
  → `ProcessRunner` 주입(생성자 선택 인자)으로 전환. Timeout은
  `ProcessResult.timed_out`을 확인해 `EngineExecutionError`로 정확히
  전파(계약 그대로). **M3-T02에서 문서화해 둔 한계 해소**: `cancel()`이
  이제 `ProcessRunner.cancel()`을 통해 실제 프로세스를 종료함.
  **발견 및 수정한 버그**: `ClaudeCodeEngineAdapter.cancel()`이
  `interfaces/engine_adapter.py`의 계약("이미 COMPLETED/FAILED로 끝난
  세션은 상태가 유지된다")을 위반해 완료된 세션도 무조건 CANCELLED로
  덮어쓰고 있었음 — 종단 상태 보존 로직 추가로 수정.
  **자체 정정**: 처음에는 `ManagedEngineRuntime.cancel()`(M3-T01)도
  같은 버그로 오판해 수정하려 했으나, `interfaces/engine_runtime.py`의
  `cancel()` 계약을 재확인한 결과 이쪽은 애초에 "완료 상태 유지" 조항이
  없고 무조건 CANCELLED 전이가 맞는 계약임을 확인 — 변경을 되돌리고
  원래 구현이 옳았음을 테스트 주석으로 남김(정직하게 기록). `tests/
  adapters/test_process_runner.py`에 6개 신규 테스트 —
  `sys.executable -c "..."`로 **실제 프로세스**를 띄워 정상 실행/비정상
  종료 코드/Timeout 강제 종료/Cancel/미등록 예외를 검증(타이밍 테스트는
  5회 연속 실행으로 안정성 확인). `tests/adapters/
  test_claude_code_engine_adapter.py`는 `subprocess.run` mock 대신
  주입 가능한 `FakeProcessRunner`로 전면 재작성(테스트 경계 개선) +
  종단 상태 보존 테스트 추가. `ruff check src tests`, `mypy src`,
  `pytest`(244개, 기존 235개 + 신규 9개) 모두 통과.
- 의존성: M3-T02

#### M3-T04: Session & Workspace Integration
- 목적: `WorkspaceCore`가 실제 `ManagedEngineRuntime`과 결합될 수 있음을
  증명하고, Engine 실행 1건을 추적하는 `EngineSession` 생성/종료/이력
  관리를 제공한다.
- 작업 내용: `WorkspaceCore` ↔ `ManagedEngineRuntime` 연결, `EngineSession`
  생성/종료, 실행 기록 관리, EventBus 완전 연동.
- 완료 조건(DoD): `ManagedEngineRuntime`을 실제로 주입해도 Core 코드
  변경이 필요 없음을 테스트로 증명, `EngineSession` 생명주기 검증,
  Core·Runtime이 같은 EventBus를 공유할 때 Event가 실제로 도달함을 검증,
  `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-25)** — 사전 검토: 착수 전 사용자가 "EngineSession을
  새로 만들기 전에 AgentSession/WorkspaceSession과 공통 개념이 있는지
  먼저 검토하라"고 지시함. 세 Session류(AgentSession: session_id+agent_id,
  WorkspaceSession: session_id+7개 필드, 신규 EngineSession:
  session_id+task_id)는 형태만 유사할 뿐 실제로 겹치는 동작이 아직 3곳
  이상에서 드러나지 않아 **`BaseSession` 등 공통 추상화는 만들지 않고
  독립 dataclass로 결정**(점진적 확장 원칙). `domain/engine_session.py`에
  `EngineSession(session_id, task_id)` 신규 추가. **`WorkspaceCore`
  확장**(새 Manager 클래스를 만들지 않고 기존 `WorkspaceSession` 생명주기
  메서드와 동일한 패턴으로 `start_engine_session`/`get_engine_session`/
  `end_engine_session`/`list_engine_session_history` 추가 — 최소
  복잡성/기존 코드 존중). `EngineSession` 관리는 순수 기록용 추적이며
  Engine Runtime을 스스로 호출하지 않음(`SpyEngineRuntime` 테스트가
  검증하는 기존 T1-22 원칙과 동일하게 유지). `WorkspaceSession.
  engine_session_id`(T1-22부터 존재했으나 지금까지 미사용이던 필드)는
  새 필드 추가 없이 기존 `update_session()`과 신규
  `start_engine_session()`의 조합만으로 연결됨을 테스트로 증명.
  `shutdown()`은 활성 `EngineSession`도 함께 정리하되 이력(history)은
  보존. `tests/domain/test_engine_session.py`(1개) +
  `tests/core/test_workspace_core.py`에 11개 신규 테스트 — 생명주기/이력/
  방어적 복사/shutdown 정리 + `ManagedEngineRuntime`+`MockEngineAdapter`+
  `InMemoryEventBus`로 구성한 실제 조립 검증(Core와 Runtime이 같은
  EventBus를 공유할 때 `engine_task_started`/`completed` Event가
  Core.event_bus 구독자에게 도달함을 확인) + `engine_session_id` 연결
  검증. `ruff check src tests`, `mypy src`, `pytest`(256개, 기존 244개 +
  신규 12개) 모두 통과.
- 의존성: T1-22, M3-T01, T2-01

#### M3-T05: Approval Pipeline
- 목적: Engine Task 실행 전 사람 승인을 요구하는 게이트를 제공한다.
- 작업 내용: ApprovalRequest 생성, 사용자 승인 대기, 승인·거부 Event,
  Runtime Resume(승인된 Task만 실제 실행).
- 완료 조건(DoD): 승인 전에는 Task가 실행되지 않음을 검증, 승인/거부 각각
  Event 발행 검증, 승인된 Task만 EngineRuntime으로 실제 실행됨을 검증,
  `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-25)** — 사용자가 설계안 검토 후 2가지 수정을
  요청: (1) `resume()` → `run_approved()`로 이름 변경(승인 전제조건을
  메서드명에 명시), (2) Pipeline 자체의 상태 머신을 만들지 않고 기존
  `ApprovalEngine`(승인 상태)·`EngineRuntime`(실행 상태)의 상태를 그대로
  조합. `runtime/engine/approval_pipeline.py`에 `EngineApprovalPipeline`
  신규 — `EngineRuntime` 인터페이스는 구현하지 않음(사람 승인은 비동기적
  사건이라 `run()` 안에서 동기적으로 기다릴 수 없기 때문에 의도적으로
  분리된 3단계 API: `request_approval`/`decide`/`run_approved`).
  `interfaces/approval_engine.py`의 `ApprovalActionType`에
  `ENGINE_TASK_EXECUTION` 신규 추가(순수 추가, 기존 4개 값 변경 없음) —
  RULES.md §1.4의 AI 세션 거버넌스 승인 4종과는 별개 목적임을 docstring에
  명시. **기존 코드 재사용**: `InMemoryApprovalEngine`(T2-03)은 전혀
  수정하지 않고 그대로 주입받아 사용, EventBus 발행 책임은 Pipeline이
  전담. Pipeline은 `request_id → Task` 매핑만 `run_approved()` 호출에
  필요한 최소 데이터로 보관(상태 머신이 아니라 단순 조회용 데이터).
  `run_approved()`는 미승인/거부/미등록/이미 실행된 request_id 전부를
  단일 예외(`UnapprovedTaskExecutionError`)로 통일 — "지금 실행할 수
  없다"는 같은 의미이므로 별도 예외 타입을 늘리지 않음(최소 복잡성). 기존
  T2-03 테스트 중 `ApprovalActionType`이 정확히 4개임을 단언하던 테스트를
  5개로 갱신(순수 추가이므로 실패가 예상된 결과, 의미도 함께 갱신).
  `tests/runtime/engine/test_approval_pipeline.py`에 11개 신규 테스트 —
  요청 생성/Event 발행/승인·거부 Event/중복 결정 차단/미승인 실행 차단/
  거부 후 실행 차단/미등록 request_id 차단/중복 실행 차단/승인 후 실제
  `EngineRuntime.run()` 호출 검증(`FakeEngineRuntime`+`MockEngineAdapter`
  재사용). `ruff check src tests`, `mypy src`, `pytest`(267개, 기존
  256개 + 신규 11개) 모두 통과.
- 의존성: T2-02, T2-03, M3-T01

#### M3-T06: Runtime Recovery
- 목적: Engine Task 실행 실패를 자동으로 재시도하고, 예외로 인한 비정상
  종료 시에도 Runtime 상태 일관성을 유지한다.
- 작업 내용: 실행 실패 복구, Retry 정책, Runtime 상태 복원, 비정상 종료
  처리.
- 완료 조건(DoD): 실패 후 재시도해 성공하는 경로/재시도 소진 후 실패
  반환 경로/예외 발생 후 재시도 경로/재시도 소진 후 예외 전파 경로 모두
  검증, `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-25)** — 사용자가 설계안 검토 후 1가지 수정을
  요청: 재시도 소진 후 예외는 `EngineResult`로 변환하지 않고 마지막
  예외를 그대로 전파(기존 `EngineRuntime.run()` 계약 "EngineExecutionError
  가 발생하면 그대로 전파한다"를 그대로 지키기 위함 — 사용자가 계약
  위반 가능성을 먼저 짚어냄). `domain/retry_policy.py`에
  `RetryPolicy(max_attempts=3)` 신규(불변 값 객체, `llm_policy.py` 패턴과
  동일, `max_attempts<1`은 `InvalidRetryPolicyError`). `runtime/engine/
  recovering_engine_runtime.py`에 `RecoveringEngineRuntime` 신규 — 다른
  `EngineRuntime`을 감싸는 **데코레이터**로 `EngineRuntime` 인터페이스를
  그대로 구현(Approval Pipeline과 달리 사람 개입이 없어 동기적으로 끝나기
  때문에 인터페이스 구현이 자연스러움). `run()`만 재시도 로직을 갖고,
  `register_engine`/`run_parallel`/`cancel`/`status`는 전부 내부
  Runtime에 위임 — 새 상태 저장소를 두지 않음("Runtime 상태 복원" =
  재시도 중에도 내부 Runtime의 상태만을 유일한 진실로 유지, M3-T05와
  동일한 원칙). `EngineResult(success=False)`(정상 실패)는 재시도 소진 시
  마지막 결과를 그대로 반환, 예외(비정상 종료)는 재시도 소진 시 마지막
  예외를 그대로 재전파. `tests/runtime/engine/
  test_recovering_engine_runtime.py`에 11개 신규 테스트(RetryPolicy
  자체 테스트 2개 포함, 별도 domain 테스트 파일 없이 한 파일에 통합) —
  `ScriptedEngineRuntime`(결과/예외 시퀀스를 순서대로 반환하는 로컬 테스트
  더블)로 첫 성공/실패 후 재시도 성공/재시도 소진 후 실패 반환/예외 후
  재시도 성공/재시도 소진 후 예외 전파 + `FakeEngineRuntime`+
  `MockEngineAdapter`로 4개 위임 메서드 검증 + `RetryPolicy` 기본값/검증
  2개. `ruff check src tests`, `mypy src`, `pytest`(278개, 기존 267개 +
  신규 11개) 모두 통과.
- 의존성: M3-T01

#### M3-T07: End-to-End Integration
- 목적: Milestone 3에서 만든 모든 계층(WorkspaceCore/EngineRuntime 데코레이터
  체인/EngineAdapter/ApprovalPipeline/EventBus)이 실제로 하나의 실행
  흐름으로 연결되는지 검증한다.
- 작업 내용: Workspace→Runtime→Adapter→Claude Code 실제 시나리오, Event
  흐름, Approval 포함 통합 테스트.
- 완료 조건(DoD): 전체 스택을 실제 구현으로 조립한 승인→실행 정상 경로와
  거부→실행 차단 경로 검증, Event 발행 **순서**까지 검증, `pytest`/
  `ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-25)** — 사용자가 설계안 검토 후 2가지를 요청: (1)
  Event 발생 여부뿐 아니라 **순서**까지 검증, (2) EngineSession 생명주기는
  핵심이 아니므로 최소화/부수적으로만 다룰 것. 둘 다 반영함. **"실제
  시나리오"의 해석**: 실제 `claude` CLI를 호출하지 않고(비용·비결정성
  회피, M3-T02 이후 일관된 정책), `ClaudeCodeEngineAdapter` 실제 클래스에
  `FakeProcessRunner`(M3-T02/T03 테스트에서 이미 쓰던 더블, 새로 만들지
  않고 `tests.adapters.test_claude_code_engine_adapter`에서 그대로
  import해 재사용)를 주입 — 명령 조립·JSON 파싱 등 실제 코드 경로는
  그대로 거치되 프로세스만 대체함. **조립 순서**:
  `ClaudeCodeEngineAdapter`(FakeProcessRunner) → `ManagedEngineRuntime`에
  등록 → `RecoveringEngineRuntime`으로 감쌈 → `EngineApprovalPipeline`의
  `engine_runtime`으로 사용, 전부 같은 `InMemoryEventBus` 공유.
  `WorkspaceCore`는 `EngineApprovalPipeline`을 보관할 수 없음(M3-T05에서
  의도적으로 `EngineRuntime` 인터페이스를 구현하지 않았기 때문) — Core는
  `RecoveringEngineRuntime`을 그대로 보관하고, Approval Pipeline은 Core
  밖에서 호출자가 별도로 사용. **Retry(M3-T06) 경로는 재검증하지 않음**
  (이미 단위 테스트로 충분히 검증됨, 중복 방지). 신규
  `tests/integration/` 패키지에 `test_m3_end_to_end.py` 3개 테스트 —
  승인→실행 정상 경로(Event 순서 `approval_requested→approval_granted→
  engine_task_started→engine_task_completed` 정확히 검증, 실제 명령 조립
  결과 확인), 거부→실행 차단 경로(Event 2개까지만 발생하고 프로세스는
  전혀 호출되지 않음을 확인), EngineSession↔WorkspaceSession 연동(부수적
  확인, 최소 범위). `ruff check src tests`, `mypy src`, `pytest`(281개,
  기존 278개 + 신규 3개) 모두 통과.
- 의존성: M3-T01~M3-T06 전체

#### M3-T08: Milestone 3 Review
- 목적: Approval Required 원칙에 따라 Milestone 3 산출물을 검토받는다.
  새 기능 구현 없이 DoD 충족 여부/아키텍처 일치/Interface First 준수/
  테스트 결과/기술 부채를 검토하고 문서를 최종 정리한다.
- 작업 내용: DoD 체크리스트, Architecture Review, Interface First 검토,
  테스트 결과 문서화, Technical Debt 정리, 문서(TASKS/MEMORY/ROADMAP)
  갱신, Milestone 종료 선언.
- 완료 조건(DoD): 위 6개 항목 모두 완료 + 사용자 승인.
- 상태: **DONE (2026-07-25 사용자 승인 — Milestone 3 완료)** — Review에서
  원래 ROADMAP.md DoD 대비 미충족 2개 항목(Interaction Layer, Coding
  Agent 실제 경로 통합)을 발견해 보고했고, 사용자가 8개 Task 체크리스트
  기준 Completed 선언 + 두 항목 Milestone 4 공식 이관을 확정함(상세는
  아래 "Milestone 3 Review" 7절 참고)

---

## Milestone 3 Review

**1. Definition of Done 체크리스트**

*사용자가 제시한 8개 Task 기준 체크리스트*

| 항목 | 상태 | 근거 |
|---|---|---|
| Runtime 구현 완료 | ✅ | M3-T01 `ManagedEngineRuntime`(생명주기/Timeout/Cancel/Event) |
| Claude Adapter 구현 완료 | ✅ | M3-T02 `ClaudeCodeEngineAdapter`(`EngineAdapter` 계약 충족, 실제 CLI 플래그 1차 자료로 확정) |
| Process 실행 가능 | ✅ | M3-T03 `ProcessRunner`(`subprocess.Popen`, 실제 안전한 프로세스로 정상/Timeout/Cancel 검증) |
| Approval Pipeline 동작 | ✅ | M3-T05 `EngineApprovalPipeline`(요청/승인/거부/실행 4개 경로 검증) |
| Retry/Recovery 동작 | ✅ | M3-T06 `RecoveringEngineRuntime`(실패·예외 재시도, 계약 유지 확인) |
| EventBus 연동 | ✅ | M3-T04(Core↔Runtime 공유 검증)/M3-T05/M3-T07(전체 스택 공유 + 순서 검증) |
| End-to-End Integration 완료 | ✅ | M3-T07(실제 구현 조립, 승인→실행/거부→차단 경로) |

7개 항목 전부 충족.

**⚠️ `docs/ROADMAP.md`에 원래 정의되어 있던 Milestone 3 DoD와 대조한 결과,
차이를 발견함** — 위 8개 Task 체크리스트와는 별개로 `docs/ROADMAP.md`
"Milestone Definition of Done"에는 다음 2개 항목이 명시되어 있었다.

1. 세션 생명주기 계약을 만족하는 ClaudeCodeAdapter로 **Coding Agent**가
   실제 Task를 end-to-end(create_session→run→결과 수집→destroy_session)
   수행한다 — **부분 충족**. Adapter의 세션 생명주기 자체는 M3-T02/T03/T07
   에서 실증했지만, M3-T07의 E2E 테스트는 `Task`를
   `EngineApprovalPipeline`/`EngineRuntime`에 직접 넘겼을 뿐, M2에서 만든
   실제 `CodingAgent`(`agents/coding_agent.py`)를 경유하지 않았다. "Agent가
   실제로 이 경로를 쓴다"는 아직 검증되지 않았다.
2. **Interaction Layer가 CLI/API 등 표면 입력을 표준 요청으로
   정규화한다 — 미충족**. `src/ai_workspace/interaction/` 디렉터리 자체가
   아직 존재하지 않는다. 사용자가 제공한 M3-T01~T08 8개 Task 개요에는
   애초에 Interaction Layer 관련 Task가 포함되어 있지 않았다.

이 차이는 지금 이 Review 단계에서 코드로 메우지 않는다(M3-T08 범위 밖 —
"새로운 기능 구현 없음" 원칙 유지). 대신 아래 5절 Technical Debt에
명시적으로 기록하고, Milestone 종료 판단(7절)에서 이 사실을 그대로
보고한다 — 사용자가 원래 DoD 기준으로 M3를 완료로 볼지, 두 항목을 M4로
이월할지 최종 판단해야 한다.

**2. Architecture Review**

실제 구현이 아래 구조와 일치함을 M3-T07 통합 테스트로 확인했다.

```
WorkspaceCore
  └─ engine_runtime: RecoveringEngineRuntime   (직접 호출하지 않음, T1-22 원칙 유지)
       └─ inner: ManagedEngineRuntime
            └─ registered adapter: ClaudeCodeEngineAdapter
                 └─ process_runner: ProcessRunner
```

Approval 경로는 사용자가 제시한 다이어그램처럼 단일 수직 체인이 아니라,
`EngineApprovalPipeline`이 **세 개의 대등한 의존성**(`ApprovalEngine`,
`EngineRuntime`, `EventBus`)을 조합하는 구조임을 확인했다 — `ApprovalEngine`을
거쳐 `EventBus`로 내려가는 체인이 아니라, Pipeline이 세 Interface를 각각
직접 주입받아 조율한다(M3-T05 설계). 다이어그램의 의도(계층 분리)는
일치하지만 정확한 관계는 "체인"이 아니라 "조합"이다.

`EngineApprovalPipeline`은 `WorkspaceCore`가 보관하지 않는다 —
`EngineRuntime` 인터페이스를 구현하지 않기 때문에(사람 승인은 비동기
사건이라 동기 `run()` 계약에 맞지 않음, M3-T05 설계 판단) Core 밖에서
호출자(Agent 역할)가 별도로 사용한다. `WorkspaceCore`는 `RecoveringEngineRuntime`
까지만 보관하며, M3-T07에서 실제로 이 조립이 Core 코드 변경 없이
동작함을 확인했다.

`docs/ARCHITECTURE.md` §3.9(Engine Runtime)·§8 의존성 규칙과 충돌하는
부분 없음.

**3. Interface First 원칙 검토**

| 클래스 | Interface 여부 | 판단 |
|---|---|---|
| `ClaudeCodeEngineAdapter` | 기존 `EngineAdapter`(T1-19) 구현 | 적절 — Mock↔실제 Adapter 교체가 상위 계층 변경 없이 동작함을 M3-T07에서 실증 |
| `RecoveringEngineRuntime` | 기존 `EngineRuntime`(T1-19) 구현 | 적절 — 데코레이터가 어디서든 `EngineRuntime` 자리에 대체 가능해야 함 |
| `ProcessRunner` | 없음 | 적절 — Adapter 내부 협력자일 뿐 상위 계층이 직접 의존하지 않음(M3-T03 판단 유지) |
| `EngineApprovalPipeline` | 없음 | 적절 — 단일 구현체, 비동기 승인이라는 특수 계약이라 `EngineRuntime`과 다형적으로 교체될 이유가 없음(M3-T05 판단 유지) |
| `RetryPolicy` | 없음(값 객체) | 적절 — 동작이 아니라 데이터, Interface 대상 아님 |

**M3 전체에서 새 Interface(ABC)를 하나도 추가하지 않았다** — Milestone 1
(T1-18~21)에서 정의한 `EngineRuntime`/`EngineAdapter` 계약만으로 실제
실행 엔진 전체를 구현할 수 있었다는 뜻이며, Interface First 원칙이 사후에
실증되었다고 판단한다. 불필요한 추상화(예: `EngineSession`/`WorkspaceSession`/
`AgentSession` 공통 Base 클래스, Approval Pipeline·ProcessRunner Interface)를
추가하지 않은 판단들도 이번 Review에서 재확인했다.

**4. 테스트 결과**

- `pytest`: **281개 전부 통과**(M2 완료 시점 205개 → M3에서 76개 신규)
- `ruff check src tests`: 클린
- `mypy src`: 클린(68개 소스 파일)
- 신규 소스 파일 7개(`process_runner.py`, `claude_code_engine_adapter.py`,
  `managed_engine_runtime.py`, `approval_pipeline.py`,
  `recovering_engine_runtime.py`, `engine_session.py`, `retry_policy.py`),
  약 585줄 순증가(M2 완료 커밋 대비)

**5. Technical Debt 정리**

*원래 Milestone 3 DoD 대비 미충족 항목(1절에서 발견, 최우선 이월 후보)*
- **Interaction Layer 미구현** — `docs/ROADMAP.md`의 원래 M3 DoD 2번 항목
  ("CLI/API 등 표면 입력을 표준 요청으로 정규화"). 사용자가 제공한
  M3-T01~T08 개요에 이 Task가 원래 포함되어 있지 않았음 — M4 착수 시
  범위 포함 여부를 다시 논의해야 한다.
- **CodingAgent가 실제 Engine 경로를 쓰는지 미검증** — M3-T07 E2E는
  `Task`를 `EngineApprovalPipeline`에 직접 넘겼고, M2의 `CodingAgent`
  (`agents/coding_agent.py`)를 경유하지 않았다. Agent가 실제로 이
  Engine 스택을 호출하는 통합은 아직 검증되지 않았다.

*M3에서 의도적으로 구현하지 않은 것(M4 이후 과제)*
- Retry Backoff — `RetryPolicy`는 `max_attempts`만 가짐, 지수 백오프 등
  타이밍 정책 없음(M3-T06에서 의도적 최소화)
- Persistent Runtime Recovery — 시스템 전체가 인메모리, 프로세스 재시작 후
  Runtime 상태 복원 없음(M3-T06 Analysis 단계에서 이미 범위 밖으로 명시)
- 실제 Claude CLI 기반 E2E 부재 — M3-T02 1회 검증 이후 전부
  `FakeProcessRunner`/Mock 사용(비용·비결정성 회피가 의도적 트레이드오프)
- Approval 비동기 처리 없음 — `decide()`는 동기 호출, 알림/대기 큐 없음
  (호출자가 나중에 직접 `decide()`를 호출하는 구조로 현재 규모엔 충분)
- Process Timeout 정책 고도화 없음 — `ProcessRunner`는 고정 timeout +
  고정 grace period만 지원, 재시도별 동적 조정 없음

*M2에서 이월된 항목 중 M3에서도 해결되지 않은 것*(M2 Retrospective 참고)
- #1 `AgentManager`/`AgentRegistry` 프로덕션 구현체 여전히 없음(Interface만
  존재) — M3 범위와 자연스럽게 겹치지 않아 이월 지속
- #2 CLI가 `WorkspaceCore`를 여전히 쓰지 않음(`cli/main.py`는
  `FileProjectRepository`만 직접 사용) — 이월 지속
- #5 병렬 실행 실증 여전히 없음 — `ClaudeCodeEngineAdapter.supports_parallel()
  =True`이나 `ManagedEngineRuntime.run_parallel()`은 여전히 순차 실행(M3-T01
  설계 그대로) — 실제 동시성 검증은 M4 이후로 이월
- #3(Event ID 생성 방식 불일치)·#6(`Step` 도메인 미반영)은 이번 Milestone
  범위 밖이라 재검토하지 않음(그대로 이월)

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M3-T01~T08 전체 기록) / `.ai/MEMORY.md`(M1·M2와
동일하게 압축) / `docs/ROADMAP.md`(M3 완료 표시) 갱신 완료. `README.md`의
"현재 상태" 안내가 "Milestone 3 착수" 상태로 멈춰 있어 M3 완료를 반영해
갱신함(M3 결과를 반영할 내용이 있는 경우에 해당).

**7. Milestone 종료 선언**

Architecture Review 완료(2절), Interface First 검토 완료(3절), 테스트
결과 문서화 완료(4절), Technical Debt 정리 완료(5절), 문서 갱신 완료
(6절) — 5개 조건 만족. Review 중 코드 변경이 필요한 치명적 문제(버그·
계약 위반)는 발견되지 않았다(계획대로 코드 변경 없이 종료).

1절에서 발견한 원래 `docs/ROADMAP.md` M3 DoD 2개 항목("Interaction
Layer 정규화", "Coding Agent의 실제 경로 사용")에 대해 **사용자가 선택지
A(8개 Task 체크리스트 기준 Completed 선언 + 두 항목 Milestone 4 공식
이관)를 확정했다.** 두 항목은 M3 미완료가 아니라 **애초에 M3-T01~T08
Task 범위에 포함되지 않았던 것으로 재정의**되어 M4로 재배치된다(M3-T09
추가 없음).

**Definition of Done(실제 Task, 즉 M3-T01~T08 기준) 충족 + Architecture
Review 완료 + Interface First Review 완료 + 테스트 통과 + 문서 최신화
완료 — 6개 조건 모두 만족.**

**Milestone 3 Completed (2026-07-25 사용자 승인).**

**Milestone 4 공식 이관 항목**
1. Interaction Layer 구현(CLI/API 등 표면 입력을 표준 요청으로 정규화)
2. `CodingAgent`(M2)의 실제 Engine 실행 경로 통합 및 End-to-End 검증

---

## Milestone 4 — 자동화 및 확장 (Automation & Scale)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 4 Definition of Done" 참고.
> **M4는 "기반 프레임워크"에서 "사용 가능한 워크스페이스"로 넘어가는
> 전환점**이다(사용자 강조) — Milestone 종료 시 M2·M3처럼 단순 Review에
> 그치지 않고 **v0.5.0 아키텍처 기준선(Baseline)**을 확정해, M5 이후
> 작업이 구조 변경보다 기능 확장에 집중할 수 있게 한다(M4-T09에서 수행).

**Task List**(2026-07-26 확정, 상세 스펙은 각 Task 착수 시점에 이 문서에 추가)

| Task | 내용 | 근거/출처 | 의존성 |
|---|---|---|---|
| M4-T01 | `AgentManager`/`AgentRegistry` 프로덕션 구현 | M2 이월 부채 #1 | 없음 |
| M4-T02 | CLI ↔ WorkspaceCore 완전 연동 | M2 이월 부채 #2 | M4-T01 |
| M4-T03 | Interaction Layer 구현 | M3 Review에서 공식 이관 | 없음 |
| M4-T04 | `CodingAgent` 실제 Engine 통합 + E2E | M3 Review에서 공식 이관 | 없음(M3 스택 완료) |
| M4-T05 | 다중 프로젝트 운용 검증 | M4 목표(ROADMAP DoD) | M4-T02 |
| M4-T06 | `run_parallel` 실제 동시성 검증 | M2 이월 부채 #5 | 없음 |
| M4-T07 | Automation Engine 구현(Analysis 단계에서 Interface 변경 여부 우선 검토) | M4 목표(ROADMAP DoD) | 없음 |
| M4-T08 | Memory Engine 고도화(Analysis 단계에서 Interface 변경 여부 우선 검토) | M4 목표(ROADMAP DoD) | 없음 |
| M4-T09 | Milestone 4 Review + v0.5.0 아키텍처 기준선 확정 | 관례(M2-T08/M3-T08) + 사용자 신규 제안 | M4-T01~T08 |

상태: M4-T01~T09 전체 DONE. Milestone 4 Review는 아래 "Milestone 4
Review" 절 참고.

#### M4-T01: AgentManager/AgentRegistry 프로덕션 구현
- 목적: T1-18에서 계약만 정의된 `AgentManager`/`AgentRegistry`의 실제
  구현체를 제공해 M2 Retrospective의 Deferred by Design 부채 #1을
  해소한다.
- 작업 내용: `InMemoryAgentManager`(Agent 생성/상태 전이), `InMemoryAgentRegistry`
  (런타임 등록/조회/제거) 구현.
- 완료 조건(DoD): 두 Interface의 기존 계약 테스트(`tests/interfaces/
  test_agent_manager.py`/`test_agent_registry.py`)와 동일한 시나리오가
  새 구현체에서도 통과, `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — `tests/interfaces/fakes.py`의
  `FakeAgentManager`/`FakeAgentRegistry`가 이미 완전한 로직(허용 전이
  규칙 `_ALLOWED_AGENT_TRANSITIONS` 포함)을 갖고 있어 T2-02/T2-03과
  동일한 "Fake 승격" 패턴을 그대로 적용함 — 로직 변경 없이 위치만
  `runtime/agent/agent_manager.py`/`agent_registry.py`로 이동. 새
  Interface 없음(T1-18 계약 그대로). CLI/WorkspaceCore 연동은 이번
  Task 범위가 아님(M4-T02에서 수행) — 아직 어디에도 주입되지 않은
  독립 구현체 상태. `tests/runtime/agent/test_agent_manager.py`/
  `test_agent_registry.py`에 기존 계약 테스트와 동일한 10개 테스트
  (T2-02의 `test_agent_scheduler.py` 승격 패턴과 동일). `ruff check src
  tests`, `mypy src`, `pytest`(291개, 기존 281개 + 신규 10개) 모두 통과.
- 의존성: T1-18

#### M4-T02: CLI ↔ WorkspaceCore 완전 연동
- 목적: CLI가 `FileProjectRepository`를 직접 호출하던 것을 없애고
  `WorkspaceCore`를 유일한 진입점으로 쓰도록 바꿔 M2 이월 부채 #2를
  해소한다.
- 작업 내용: `WorkspaceCore.save_project()` 추가, `cli/main.py`가
  `WorkspaceCore`를 조립해 `project create`/`project show`를 Core
  경유로 재구현.
- 완료 조건(DoD): 기존 CLI 동작(입출력/종료 코드)이 그대로 유지된 채
  내부적으로 `WorkspaceCore`만 거치는 것을 테스트로 증명, `pytest`/
  `ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — `WorkspaceCore`에 `save_project(project)`
  추가(기존 `load_project()`와 대칭, `project_repository.save()`에
  위임 — 새 책임 아님). `cli/main.py`에 `_build_workspace_core(data_dir)`
  신규 — `FileProjectRepository`(T1-23)+`InMemoryWorkflowEngine`(T2-03)+
  `InMemoryAgentRegistry`/`InMemoryAgentManager`(M4-T01)+
  `InMemoryAgentScheduler`(T2-02)+`InMemoryEventBus`(T2-02)+
  `ManagedEngineRuntime`(M3-T01)로 실제 `WorkspaceCore`를 조립.
  **사용자 요청 반영**: `ClaudeCodeEngineAdapter`(M3-T02)를 "기본 채택
  Engine"으로 문서화하되, 현재 CLI 명령 중 실제 Engine 실행을 요구하는
  것이 없어 **등록하지 않고 지연 초기화 상태로 남김**(`ManagedEngineRuntime`
  객체 자체는 생성하되 `register_engine()` 호출 없음) — CLI가 `claude`
  실행 파일 설치 여부에 불필요하게 의존하지 않게 함. `_create_project`/
  `_show_project`가 `FileProjectRepository` 대신 `core.save_project()`/
  `core.load_project()`를 사용하도록 변경(기존 `tests/cli/test_main.py`
  5개 테스트는 CLI 입출력만 검증하므로 수정 없이 그대로 통과 — 내부
  구현 변경이 외부 동작에 영향 없음을 증명). `project list` 명령은
  범위에서 제외(M4-T05로 유지). 새 Interface 없음.
  `tests/core/test_workspace_core.py`에 `save_project` 테스트 1개 추가.
  `ruff check src tests`, `mypy src`, `pytest`(292개, 기존 291개 +
  신규 1개) 모두 통과.
- 의존성: M4-T01, T1-22, T1-23, T1-24

#### M4-T03: Interaction Layer 구현
- 목적: T1-21에서 계약만 정의된 `InteractionEngine`의 실제 구현체를
  제공해 M3 Review에서 이관된 항목을 해소한다.
- 작업 내용: `InMemoryInteractionEngine`(정규화/응답 변환/지원 Surface
  조회) 구현.
- 완료 조건(DoD): 기존 `InteractionEngine` 계약 테스트와 동일한 시나리오가
  새 구현체에서도 통과, `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — `tests/interfaces/fakes.py`의
  `FakeInteractionEngine`이 이미 완전한 로직을 갖고 있어 지금까지와
  동일한 "Fake 승격" 패턴 적용. `interaction/interaction_engine.py`
  (신규 `interaction/` 패키지, M3 Review에서 확인했듯 이전까지 존재하지
  않던 디렉터리)에 `InMemoryInteractionEngine` 신규 — `surfaces` 기본값은
  Fake의 `frozenset({"cli"})` 대신 **`frozenset()`으로 변경**(CLI는
  이 계층을 거치지 않는 예외 Surface이므로 기본 지원 목록에 넣지 않음).
  **설계 판단(사용자 확인)**: CLI(`cli/main.py`, M4-T02에서
  `WorkspaceCore`와 완전 연동됨)는 이미 argparse로 구조화된 입력을
  받으므로 이 Interaction Layer를 거치지 않는 예외적인 Surface로
  유지 — 억지로 CLI를 텍스트 재파싱 구조로 바꾸지 않음(최소 복잡성).
  `normalize()`의 반환 타입은 T1-21에서 이미 정의된 `NormalizedRequest`
  dataclass(surface/text/session_id)를 그대로 사용 — 사용자가 제안한
  "모든 Surface가 동일한 DTO를 WorkspaceCore에 전달"하는 목표를 이미
  만족하는 기존 타입이라 새 이름(`InteractionRequest` 등)으로 바꾸지
  않음. **`docs/ARCHITECTURE.md` §3.1/§3.2에 위 예외 관계를 명시적으로
  문서화**(사용자 제안 반영) — CLI는 Interaction Layer를 거치지 않고
  `WorkspaceCore`를 직접 호출하는 예외 Surface임과, Voice/Slack/REST
  같은 자유 텍스트 Surface가 실제로 추가될 때 이 계층을 거친다는 점을
  명시. `tests/interaction/test_interaction_engine.py`(신규 테스트
  디렉터리)에 5개 테스트(voice/slack 등 비-CLI Surface로 검증, CLI가
  예외임을 반영). `ruff check src tests`, `mypy src`, `pytest`(297개,
  기존 292개 + 신규 5개) 모두 통과.
- 의존성: T1-21

#### M4-T04: CodingAgent 실제 Engine 통합 + E2E
- 목적: M3 Review에서 이관된 항목 — M2의 Agent 파이프라인(Coding/Review/
  Documentation)이 `MockEngineAdapter`가 아니라 M3의 실제 Engine 스택
  위에서도 동작함을 증명한다.
- 작업 내용: 실제 Engine 스택(`ClaudeCodeEngineAdapter`+
  `ManagedEngineRuntime`+`RecoveringEngineRuntime`)으로 조립한
  Planning→Coding→Review→Documentation E2E 테스트 추가.
- 완료 조건(DoD): 전체 Event 체인이 실제 Engine 스택 위에서 완주,
  RecoveringEngineRuntime의 재시도가 실제로 한 번 발생·복구되는 시나리오
  검증, Runtime Event와 Agent Event의 연결 순서 검증, `pytest`/`ruff`/
  `mypy` 통과.
- 상태: **DONE (2026-07-26)** — **핵심 발견**: `CodingAgent`(T2-06)는
  이미 `engine_runtime: EngineRuntime`을 Interface로만 주입받아
  `self._engine_runtime.run(task)`를 호출하도록 설계되어 있어(
  `MockEngineAdapter`에 하드코딩되지 않음), **소스 코드 변경 없이 새
  테스트만으로 충분**함을 확인(Interface First가 의도대로 작동한 사례).
  기존 `tests/agents/test_pipeline.py`(T2-06, Mock 기반)는 그대로 유지
  (빠르고 Adapter에 무관한 검증으로 계속 유효) — 신규
  `tests/integration/test_coding_agent_runtime_integration.py`(사용자
  제안대로 Milestone 번호가 아닌 기능 중심 파일명) 추가.
  **사용자가 제안한 3가지 보강 사항 모두 반영**:
  1. `FlakyProcessRunner`(신규 로컬 테스트 더블)로 Coding 단계의 첫 실행만
     실패시켜 `RecoveringEngineRuntime`이 실제로 재시도·복구하는 시나리오
     검증(`test_retry_actually_recovers_a_failed_first_attempt`) — 재시도가
     CodingAgent에게 완전히 투명함(예외가 전파되지 않음)을 확인.
  2. Runtime Event(`engine_task_started`/`completed`/`failed`)와 Agent
     Event(`mission_planned`/`code_completed`/`review_completed`/
     `documentation_completed`)의 연결 순서를 **정확한 전체 순서로 단언**
     (`test_engine_and_agent_events_interleave_in_expected_nested_order`).
     Coding→Review→Documentation이 서로의 이벤트 핸들러 안에서 중첩
     호출되므로, M2 Retrospective Implementation Observation #3
     (`InMemoryEventBus`가 핸들러 내부 재귀 발행 시 가장 안쪽 이벤트를
     먼저 관측)이 정확히 어떤 순서를 만들어내는지 직접 유도해 검증함 —
     `documentation_completed`(가장 안쪽)가 가장 먼저, `mission_planned`
     (가장 바깥쪽 트리거)가 가장 마지막에 관측됨.
  3. 파일명을 `test_m4_...` 대신 기능 중심(`test_coding_agent_runtime_
     integration.py`)으로 명명.
  `ClaudeCodeEngineAdapter`는 `FakeProcessRunner`가 아니라 신규
  `FlakyProcessRunner`(호출 순서대로 결과를 반환하는 더블)를 사용 —
  기존 `FakeProcessRunner`는 고정된 단일 결과만 반환해 이번 시나리오(첫
  실패 후 재시도 성공)에 맞지 않아 새로 작성. `success_result`/
  `error_result` 헬퍼는 `tests.adapters.test_claude_code_engine_adapter`
  에서 그대로 import(M3-T07과 동일한 재사용 원칙). 신규 테스트 3개.
  `ruff check src tests`, `mypy src`, `pytest`(300개, 기존 297개 +
  신규 3개) 모두 통과.
- 의존성: T2-06, M3-T01, M3-T02, M3-T03, M3-T06

#### M4-T05: 다중 프로젝트 운용 검증
- 목적: AI Workspace가 여러 Project를 안전하게 동시에 관리할 수 있음을
  Repository→Core→CLI 전체 경로로 증명한다.
- 작업 내용: `WorkspaceCore.list_projects()` 추가, CLI `project list`
  명령 추가, WorkspaceSession 상태 격리 검증, Project 객체 독립성 검증.
- 완료 조건(DoD): 여러 Project를 CLI로 조회 가능, 서로 다른 Project에
  묶인 WorkspaceSession들의 상태가 서로 간섭하지 않음을 증명, `load()`가
  반환하는 Project 객체가 서로 독립적임을 증명, `pytest`/`ruff`/`mypy`
  통과.
- 상태: **DONE (2026-07-26)** — `WorkspaceCore.list_projects()` 추가
  (`load_project`/`save_project`와 동일 패턴, `project_repository.
  list_projects()`에 위임 — 이미 T1-23에 구현되어 있던 메서드를 그대로
  재사용). `cli/main.py`에 `project list` 서브커맨드 추가(M4-T02에서
  유보했던 항목). **사용자가 요청한 2가지 보강**: (1) Project 객체
  자체의 독립성 검증 — `tests/storage/test_file_project_repository.py`에
  `test_load_returns_independent_project_each_call`/
  `test_list_projects_returns_independent_project_objects` 추가(반환된
  Project를 변경해도 저장소나 재조회 결과에 영향 없음을 증명 —
  `FileProjectRepository.load()`가 매번 JSON에서 새 인스턴스를 생성하는
  기존 구현 덕분에 이미 성립, 회귀 방지용으로 고정). (2) CLI 테스트는
  실제 `FileProjectRepository`를 거치는 통합 경로로 작성 — 기존 CLI
  테스트 전부가 이미 mock 없이 `tmp_path` 기반 실제 파일 저장소를
  사용하는 관례를 그대로 따름(`test_list_shows_multiple_projects_end_to_end`).
  `tests/core/test_workspace_core.py`에 `list_projects` 위임 테스트 +
  `test_multiple_workspace_sessions_for_different_projects_are_isolated`
  (서로 다른 Project에 묶인 2개 WorkspaceSession의 상태 변경이 서로
  영향을 주지 않고, 하나를 종료해도 다른 하나는 그대로 유지됨을 증명)
  추가. 새 Interface·새 클래스 없음. `ruff check src tests`, `mypy src`,
  `pytest`(307개, 기존 300개 + 신규 7개) 모두 통과.
- 의존성: M4-T02, T1-22, T1-23

#### M4-T06: `run_parallel` 실제 동시성 검증
- 목적: M2 이월 부채 #5(`supports_parallel()=True`이나 실제 동시성
  미검증)를 해소하고, `EngineRuntime.run_parallel()`이 실제로 여러
  Task를 동시에 실행함을 증명한다.
- 작업 내용: `AgentScheduler`↔`EngineRuntime` 병렬 책임 경계를 ADR로
  확정, `ManagedEngineRuntime.run_parallel()`을 `ThreadPoolExecutor`
  기반 실제 동시 실행으로 재구현, 통합 테스트 보강(실제 동시 시작/입력
  순서 보장/독립 실패 처리/Retry 상호작용).
- 완료 조건(DoD): 순차 실행이었다면 불가능한 짧은 시간 안에 여러 Task가
  동시에 완료됨을 시간으로 증명, 입력 순서 보장 유지, 한 Task의 실패가
  다른 Task를 막지 않음을 증명, `RecoveringEngineRuntime`과의 상호작용
  확인·기록, `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — **Effort 상향(Medium→High) 사용자 승인**
  (동시성 코드는 일반 구현보다 검토 필요). **ADR-0023 신규**
  (`.ai/DECISIONS.md`) — `AgentScheduler.select()`(동시에 활동할 Agent
  후보를 고르는 "선택" 책임)와 `EngineRuntime.run_parallel()`(여러 Task
  실행을 실제로 동시에 수행하는 "실행" 책임)이 서로 다른 층위임을
  확정. `docs/ARCHITECTURE.md`(v0.8.0) §3.4/§3.9에 이 경계를 명시하는
  문장 추가. **`ManagedEngineRuntime.run_parallel()`을
  `concurrent.futures.ThreadPoolExecutor`로 재구현**(기존 순차 반복
  호출 대체) — `EngineRuntime.run_parallel()` 계약(입력 순서 보장)은
  그대로 유지, 빈 목록은 `ThreadPoolExecutor(max_workers=0)`이 예외를
  던지므로 조기 반환으로 처리. `RecoveringEngineRuntime`은 사용자 지시대로
  **수정하지 않음** — `run_parallel()`이 여전히 `inner.run_parallel()`에
  그대로 위임해 병렬 배치 안의 개별 Task 재시도는 지원하지 않는다는 것을
  테스트로 확인·기록(신규 기술 부채, 필요 시 이후 Task로 이월).
  `tests/runtime/engine/test_managed_engine_runtime.py`에
  `SlowParallelEngineAdapter`(세션 ID가 고유해 동시 호출에 안전 —
  기존 `SlowEngineAdapter`는 세션 ID가 고정이라 동시 호출 시 충돌)/
  `SelectivelyFailingEngineAdapter`(지정된 task_id만 실패) 신규 + 4개
  테스트(실제 동시 실행 시간 증명 — 0.2초 지연 3개 Task가 0.4초 미만에
  완료, 5회 연속 실행으로 안정성 확인/입력 순서 보장/독립 실패 처리 —
  `ThreadPoolExecutor`의 `with` 블록이 예외 전파 전 모든 제출 작업의
  완료를 기다림을 이용/빈 목록 처리). `tests/runtime/engine/
  test_recovering_engine_runtime.py`에 위 미지원 상호작용을 확인하는
  테스트 1개 추가. `ruff check src tests`, `mypy src`, `pytest`(312개,
  기존 307개 + 신규 5개) 모두 통과.
- 의존성: M3-T01, T1-18

#### M4-T07: Automation Engine 구현
- 목적: `AutomationEngine`(T2-03)이 실제로 Workflow를 발동시킬 수 있게
  하여 M4 목표("자동화 시나리오 1건 이상 동작")를 충족한다.
- 작업 내용: Analysis 단계에서 Interface 변경 여부 우선 검토 →
  `AutomationEngine`에 `bind_workflow`/`fire` 추가, `InMemoryAutomationEngine`
  확장.
- 완료 조건(DoD): trigger에 Workflow를 연결하고 발동시켜 실제
  `WorkflowEngine`으로 실행 순서가 나오는 시나리오 1건 이상 검증,
  `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — **Interface 변경 필요 확인**: 기존
  `register_trigger(trigger_id, description)`/`list_triggers()`는 텍스트
  설명만 저장할 뿐 실행 계약이 전혀 없어 확장이 불가피했음. `AutomationEngine`
  에 `bind_workflow(trigger_id, workflow)`/`fire(trigger_id) -> Workflow`
  순수 추가(기존 2개 메서드 변경 없음) + `TriggerNotFoundError`/
  `TriggerNotBoundError` 신규. **사용자가 설계 검토 후 책임 경계를 한 번
  더 좁힐 것을 제안**: 처음 설계안은 `fire()`가 내부적으로
  `WorkflowEngine.plan()`까지 호출해 `InMemoryAutomationEngine`이
  `workflow_engine` 생성자 의존성을 갖는 안이었으나, 사용자 지적에 따라
  `fire()`는 **연결된 Workflow를 반환만** 하고 실제 실행(WorkflowEngine
  호출)은 호출자 책임으로 남기도록 수정 — 결과적으로
  `InMemoryAutomationEngine`은 생성자 변경 없이(기존 `__init__(self)`
  그대로) `WorkflowEngine`에 전혀 의존하지 않게 됨(더 낮은 결합도, M5
  이후 Git/Cron/Webhook/Slack 등 다양한 Trigger 추가 시에도 "연결 관리"
  (AutomationEngine)와 "실행"(WorkflowEngine) 책임이 일관되게 유지됨).
  "조건/일정"의 최소 해석: 언제 발동할지 스스로 판단하는 조건 평가
  엔진은 만들지 않음(YAGNI) — 호출자가 `fire()`를 부르는 시점이 곧
  조건 충족 시점. `docs/ARCHITECTURE.md`(v0.9.0) §3.7에 이 책임 경계
  반영. `FakeAutomationEngine`도 동일하게 확장(다른 계약 테스트가 계속
  통과하도록). `tests/interfaces/test_automation_engine.py`/`tests/
  engines/test_automation_engine.py`에 각각 5개 테스트(미등록 trigger
  연결/발동 오류, 미연결 발동 오류, 발동 시 연결된 Workflow 반환,
  재연결 시 최신 Workflow로 덮어씀) + **자동화 시나리오 E2E 테스트**
  (`test_automation_scenario_fires_and_executes_real_workflow` —
  trigger 등록→Workflow 연결→발동→`InMemoryWorkflowEngine.plan()`으로
  실제 의존관계를 만족하는 실행 순서 산출까지 확인, M4 DoD 충족의
  직접 증거). `ruff check src tests`, `mypy src`, `pytest`(322개, 기존
  312개 + 신규 10개) 모두 통과.
- 의존성: T2-03

#### M4-T08: Memory Engine 고도화
- 목적: `MemoryEngine`(T2-04)이 정확한 key 조회만 지원하던 것을 확장해
  M4 목표("메모리 검색이 확인됨")를 충족한다.
- 작업 내용: Analysis 단계에서 Interface 변경 여부 우선 검토 →
  `MemoryEngine.search()`/`ContextManager.find_snapshots()` 추가.
- 완료 조건(DoD): value에 검색어가 포함된 항목을 key로 찾아내는 검색
  시나리오 검증, `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — **Interface 변경 필요 확인**: 기존
  `remember(key, value)`/`recall(key)`는 정확한 key로만 조회 가능해
  검색 자체가 불가능했음. `MemoryEngine`에 `search(query) -> list[str]`
  (value에 query가 부분 문자열로 포함된 key 목록 반환) 순수 추가.
  `ContextManager`에도 `find_snapshots(query) -> list[str]` 추가 —
  `MemoryEngine.search()`에 그대로 위임(§8 규칙 7, Agent는 ContextManager
  를 통해서만 검색하고 MemoryEngine을 직접 호출하지 않음). **사용자가
  요청한 2가지 반영**: (1) `search()`의 검색 계약(현재는 value의 부분
  문자열 검색, key 자체는 검색 대상 아님)을 Interface docstring에
  명시적으로 기록. (2) 장기적으로 `list[tuple[str, str]]`(key/value
  쌍)로 확장될 가능성을 docstring에 남기되, 지금은 최소 형태(key 목록)
  유지(YAGNI). **"요약"은 이번 범위에서 제외** — ROADMAP의 실제
  검증 가능한 DoD는 "검색"뿐이고, 진짜 요약은 LLM 호출이 필요한데 LLM
  Policy/Router가 아직 Temporary 단계(RULES.md §7)라 지금 만들면 쓸
  백엔드가 없는 껍데기가 됨 — LLM Router 준비 이후 Milestone으로 이관
  (M4-T07의 "조건 평가는 나중" 판단과 동일한 원칙). `FakeMemoryEngine`/
  `FakeContextManager`도 동일하게 확장. `tests/interfaces/`+`tests/
  memory/`의 `test_memory_engine.py`/`test_context_manager.py` 4개
  파일에 총 9개 테스트(검색 성공/실패, key 자체는 검색 안 됨,
  ContextManager가 MemoryEngine.search()에 실제로 위임함을 증명하는
  테스트 포함). `ruff check src tests`, `mypy src`, `pytest`(331개,
  기존 322개 + 신규 9개) 모두 통과.
- 의존성: T2-04

#### M4-T09: Milestone 4 Review + v0.5.0 아키텍처 기준선 확정
- 목적: Approval Required 원칙에 따라 Milestone 4 산출물을 검토받고,
  "기반 프레임워크→사용 가능한 워크스페이스" 전환점으로서 아키텍처
  기준선을 공식 선언한다.
- 작업 내용: DoD 체크리스트, Architecture Review, Interface First 검토,
  테스트 결과 문서화, Technical Debt 정리, v0.5.0 기준선 선언, 문서
  갱신, Milestone 종료 선언.
- 완료 조건(DoD): 위 항목 모두 완료 + 사용자 승인.
- 상태: **DONE (2026-07-26 사용자 승인 — Milestone 4 완료, v0.5.0
  아키텍처 기준선 선언)**

---

## Milestone 4 Review

**1. Definition of Done 체크리스트**

| 항목(ROADMAP 원문 DoD) | 상태 | 근거 |
|---|---|---|
| 자동화 시나리오 1건 이상 동작 | ✅ | M4-T07 `AutomationEngine.bind_workflow/fire` + E2E 테스트(trigger→Workflow→실제 `WorkflowEngine.plan()` 실행) |
| 다중 프로젝트 조회(2개 이상 동시 운용) | ✅ | M4-T05 `WorkspaceCore.list_projects()` + CLI `project list` + WorkspaceSession 격리 검증 |
| 메모리 검색이 확인됨 | ✅(검색만) | M4-T08 `MemoryEngine.search()`/`ContextManager.find_snapshots()` |

**"검색/요약" 중 요약(summarization)은 이번 Milestone에서 구현하지 않았다** —
M3-T08과 달리 이번엔 착수 전 발견한 "놀라운 gap"이 아니라, M4-T08
Analysis 단계에서 **사용자 승인 하에 사전에 합의된 범위 조정**이다: LLM
Policy/Router가 아직 Temporary 단계(RULES.md §7)라 지금 요약을 만들면 실제
호출할 LLM이 없는 껍데기가 되기 때문. LLM Router 준비 이후 Milestone으로
공식 이관한다(6절에서 다시 기록).

M2/M3에서 이월된 부채도 이번 Milestone에서 모두 해소되었다:

| 이월 부채 | 상태 | 근거 |
|---|---|---|
| #1 AgentManager/AgentRegistry 프로덕션 구현 없음 | ✅ 해소 | M4-T01 |
| #2 CLI-WorkspaceCore 미완전 연동 | ✅ 해소 | M4-T02 |
| #5 병렬 실행 실제 미검증 | ✅ 해소 | M4-T06 |
| Interaction Layer 미구현(M3에서 이관) | ✅ 해소 | M4-T03 |
| CodingAgent 실제 Engine 경로 미검증(M3에서 이관) | ✅ 해소 | M4-T04 |

**2. Architecture Review**

M4에서 실제로 바뀐 구조:
- `ManagedEngineRuntime.run_parallel()`이 `ThreadPoolExecutor` 기반 진짜
  동시 실행으로 전환(M4-T06). **ADR-0023**으로 `AgentScheduler`(선택
  책임)와 `EngineRuntime`(실행 책임)의 병렬 경계를 명시적으로 확정 —
  두 컴포넌트의 "병렬" 언급이 겹쳐 보였던 문서상의 모호함을 해소했다.
- `AutomationEngine`/`ContextManager`/`MemoryEngine` Interface가 순수
  추가로 확장됨(`bind_workflow`/`fire`, `find_snapshots`, `search`) —
  기존 메서드는 하나도 변경되지 않았다.
- `WorkspaceCore`가 `save_project`/`list_projects`로 대칭 확장되고(M4-T02/
  T05), CLI가 `WorkspaceCore`를 유일한 진입점으로 쓰게 되어 T1-24부터
  이월되던 "CLI가 Core를 완전히 못 쓴다"는 상태가 마침내 해소됨.
- `interaction/` 패키지가 처음 생겼지만(M4-T03), CLI는 여전히 이 계층을
  거치지 않는 예외 Surface로 남아있다(구조화된 입력이라 정규화가
  불필요, `docs/ARCHITECTURE.md` §3.1에 명시).

`docs/ARCHITECTURE.md` §3.4/§3.9(병렬 경계)/§3.7(Automation Engine
책임)/§3.1~3.2(Interaction Layer 예외)에 위 변경이 모두 문서화되어
있음을 확인했다(각 Task 완료 시점에 즉시 반영해 옴). 구현과 문서 사이의
괴리는 발견되지 않았다.

**3. Interface First 원칙 검토**

M4 전체에서 **새 Interface(ABC) 파일을 하나도 추가하지 않았다** — M1에서
정의한 16종 Interface 중 3종(`AutomationEngine`/`ContextManager`/
`MemoryEngine`)만 메서드를 순수 추가로 확장했고, 나머지는 기존 계약
그대로 재사용했다(`AgentManager`/`AgentRegistry`는 이미 있던 T1-18
계약의 첫 프로덕션 구현체를 얻었을 뿐, 계약 자체는 무변경).
`ManagedEngineRuntime.run_parallel()`은 구현만 바뀌었고 `EngineRuntime`
인터페이스의 시그니처는 그대로다. M3 Review에서 확인한 "M1 Interface
설계가 이후 Milestone 전체를 커버한다"는 결론이 M4에서도 그대로
유지되었다 — 3개 Interface의 추가도 전부 사전에 "Interface 변경 여부
우선 검토"를 거쳐 필요성이 확인된 뒤에만 이뤄졌다(M4-T07/T08).

**4. 테스트 결과**

- `pytest`: **331개 전부 통과**(M3 완료 시점 281개 → M4에서 50개 신규)
- `ruff check src tests`: 클린
- `mypy src`: 클린(72개 소스 파일)
- M3 완료 커밋(`4135559`) 대비 소스 30개 파일 변경(신규 4개:
  `interaction/` 패키지 2개, `runtime/agent/agent_manager.py`/
  `agent_registry.py`), 약 1,102줄 순증가(src+tests 합산)

**5. Technical Debt 정리**

*M4에서 의도적으로 범위를 좁힌 것(다음 Milestone 이후 과제)*
- Memory Engine 요약(summarization) — LLM Router 준비 이후로 이관(1절
  참고)
- Automation Engine의 "조건 평가"(언제 발동할지 판단) — 여전히 호출자
  책임, 실제 Scheduler/Cron 컴포넌트는 아직 없음(M4-T07에서 의도적
  경계로 확정)
- `RecoveringEngineRuntime.run_parallel()`이 병렬 배치 안의 개별 Task
  재시도를 지원하지 않음(M4-T06에서 발견·테스트로 확인, `run()` 단일
  호출과의 차이) — 필요성이 실사용에서 증명되면 재검토
- `MemoryEngine.search()`가 선형 스캔(O(n)) — 현재 인메모리 규모에선
  문제없음, 데이터가 커지면 인덱싱 검토 필요

*M2에서 이월되었으나 M4 범위 밖이라 그대로 유지되는 것*
- #3 Event ID 생성 방식이 컴포넌트마다 다름(기능적 문제 없음)
- #6 `Step` 도메인이 Workflow 실행에 아직 실질 반영되지 않음

*M3에서 이월되었으나 M4 범위 밖이라 그대로 유지되는 것*
- Retry Backoff, Persistent Runtime Recovery, 실제 Claude CLI 기반 E2E,
  Approval 비동기 처리, Process Timeout 정책 고도화 — 전부 M3-T08에서
  기록된 그대로 미해결

**6. v0.5.0 아키텍처 기준선(Baseline) 선언**

사용자 제안대로, M4 종료를 "기반 프레임워크 → 사용 가능한 워크스페이스"
전환점으로 규정한다. 판단 근거:
- Milestone 1~4를 거치며 **16종 Interface + 도메인 모델 + Workspace
  Core + Agent Runtime + Engine Runtime(+3개 데코레이터: Recovering/
  ApprovalPipeline) + Core Engines 4종 + Memory 계열 + Interaction
  Layer + CLI**까지 ARCHITECTURE.md가 그리는 전체 구조가 실제 구현으로
  채워졌다.
- M2/M3/M4 3개 Milestone 내내 **새 최상위 Interface가 추가된 적이
  없다** — M1의 설계가 구조적으로 안정적이라는 뜻이며, 이 안정성이
  "기준선"을 선언할 수 있는 근거다.
- `pyproject.toml`의 `version`을 `0.1.0` → **`0.5.0`**으로 상향해
  이 기준선을 표시한다. `.ai/DECISIONS.md`에 **ADR-0024**로 공식 기록한다
  (아래 결과/영향 참고).
- 기준선 선언의 의미: M5 이후 작업은 **기존 16종 Interface·계층 구조를
  변경하지 않는 것을 기본값**으로 하고, 새 기능은 가능한 한 기존 구조
  위에 조립한다(M2~M4 내내 실증된 패턴). 구조 자체를 바꿔야 하는 경우
  (Interface 추가/계층 변경)는 지금처럼 "Interface 변경 여부 우선
  검토" 절차를 거쳐 명시적 승인을 받는다 — 기준선 선언이 "앞으로 절대
  구조를 안 바꾼다"는 뜻은 아니다.

**7. 문서 정리**

`.ai/TASKS.md`(본 Review) / `.ai/MEMORY.md`(M1~M3와 동일하게 압축) /
`docs/ROADMAP.md`(M4 완료 표시) / `docs/ARCHITECTURE.md`(각 Task 진행 중
이미 갱신됨, 최종 버전 확인) / `pyproject.toml`(버전 0.5.0) /
`.ai/DECISIONS.md`(ADR-0024 신규) / `README.md`(M4 결과 반영) 갱신 완료.

**8. Milestone 종료 선언**

Definition of Done 충족(1절, 요약 제외는 사전 합의된 범위 조정),
Architecture Review 완료(2절), Interface First 검토 완료(3절), 테스트
결과 문서화 완료(4절), Technical Debt 정리 완료(5절), v0.5.0 기준선
선언(6절), 문서 갱신 완료(7절) — 7개 조건 모두 만족. Review 중 코드
변경이 필요한 치명적 문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 4 Completed 및 v0.5.0 아키텍처
기준선을 선언한다.**

---

## Milestone 5 — 실제 개발 수행 (Real Development Execution)

> v0.5.0 아키텍처 기준선(ADR-0024) 이후 첫 Milestone. **핵심 목표는
> "Agent가 실제 개발 작업을 수행하는 단계"** — 구조 변경보다 기능 확장에
> 집중한다(기준선 선언의 취지 그대로).

**사전 조사로 확인한 것**: `.ai/RULES.md` §7(Temporary LLM Policy)이
정의한 로드맵("M2: Rule 기반 선택 → M3: Agent Policy 참조 → M4: Policy
Engine 자동 선택 → M5: Self Optimizer")이 **M2~M4 내내 전혀 진행되지
않았다** — T1-16의 Domain 정의(`LLMProvider`/`LLMModel`/`LLMEffort`)
이후 실제 선택 로직은 한 번도 구현되지 않았음. M5는 "Self Optimizer"로
바로 가지 않고 M2/M3 단계(Rule 기반 선택, Agent Policy 참조)를 M5-T01/
T02로 압축해 소급 구현한다 — Self Optimizer(실행 결과 피드백 기반 정책
자동 최적화)는 M6 이후로 미룬다.

**Task List**(2026-07-26 확정, 상세 스펙은 각 Task 착수 시점에 이 문서에 추가)

| Task | 내용 | 근거/출처 |
|---|---|---|
| M5-T01 | Rule 기반 `LLMPolicyEngine` 구현 | RULES §7 M2 단계 소급 |
| M5-T02 | Agent Runtime/Engine Runtime이 `LLMPolicyEngine`을 통해 Model/Effort·Engine을 선택하도록 연결 | RULES §7 M3 단계 소급 |
| M5-T03 | `DevelopmentContext` 도입 + 기존 Coding/Review Agent 강화(Task 제목만이 아니라 파일 diff·테스트 결과 등 실제 개발 컨텍스트를 주고받도록) | 사용자 지시 — M5 핵심 목표 |
| M5-T04 | `ShellAgent` 신규(실제 쉘 명령 실행 능력을 가진 새 Agent 종류) | 사용자 지시 — M5 핵심 목표 |
| M5-T05 | Codex/Gemini CLI Engine Adapter(가능한 범위) | PRD 7.8 Multi-Engine 지원 |
| M5-T06 | Workflow 조건부 분기(예: 테스트 실패 시 재작업 Task 자동 생성) + 필요한 범위의 `Step` Domain 반영(M2 이월 부채 #6) | PRD 7.3 갭 + M2 이월 부채 #6 |
| M5-T07 | Milestone 5 Review | 관례 |

**M5 착수 전 사전 정리(공식 Task 아님) — 조사 결과 조치 불필요로 종결**:
Event ID 생성 방식 불일치(M2 이월 부채 #4)를 정리하려 `src/ai_workspace/`
전체에서 `Event(...)`를 생성하는 모든 지점(4개 Agent, `ManagedEngineRuntime`,
`EngineApprovalPipeline`)을 조사한 결과, **이미 전부 `str(uuid.uuid4())`로
일관되어 있었다** — M3에서 `ManagedEngineRuntime`/`EngineApprovalPipeline`
이 uuid4 방식으로 구현되며 자연스럽게 해소된 것으로 보인다.
`itertools.count()`는 다른 종류의 ID(session_id/subscription_id/task_id)
에만 쓰이고 Event ID 생성에는 전혀 관여하지 않는다. 코드 변경 없이 이
부채 항목을 해소로 종결한다(아래 5절 각주 참고).

상태: M5-T01~T07 전체 DONE. Milestone 5 Review는 아래 "Milestone 5
Review" 절 참고.

#### M5-T01: Rule 기반 LLMPolicyEngine 구현
- 목적: `.ai/RULES.md` §7이 정의한 LLM Policy 로드맵의 M2 단계(Rule
  기반 선택)를 소급 구현해, T1-16 이후 멈춰 있던 LLM Policy Domain에
  실제 선택 로직을 붙인다.
- 작업 내용: `LLMPolicyEngine` Interface 신규, `InMemoryLLMPolicyEngine`
  구현, `docs/llm_policy.example.yaml` 기반 Rule 로딩, 단위 테스트.
- 완료 조건(DoD): AgentRole별 Provider/Model/Effort를 Rule 기반으로
  조회 가능, `pytest`/`ruff`/`mypy` 통과. Engine 실행이나 실제 Adapter
  선택은 포함하지 않음(M5-T02 범위).
- 상태: **DONE (2026-07-26)** — **M1 이후 첫 신규 최상위 Interface**
  (`LLMPolicyEngine`, 총 17종) — M4 Review에서 확인한 "M2~M4 내내 새
  Interface 미추가" 기록이 M5부터 갱신됨(자연스러운 확장, Interface
  First 위반 아님 — LLM Policy는 RULES §7에서 처음부터 예정된 계약).
  `domain/llm_policy.py`에 `LLMPolicyDecision(model, effort)` frozen
  dataclass 추가. `interfaces/llm_policy_engine.py`에
  `LLMPolicyEngine.select(role: AgentRole) -> LLMPolicyDecision` +
  `PolicyNotFoundError`. `engines/llm_policy_engine.py`에
  `InMemoryLLMPolicyEngine(rules: dict[AgentRole, LLMPolicyDecision])`
  — 규칙을 어디서 읽었는지 전혀 알지 못함(순수 조회만).
  **사용자 요청으로 PolicyLoader 계층 분리**: `storage/
  llm_policy_loader.py`의 `load_llm_policy_rules(path)`가 PyYAML
  파싱을 전담하고 `LLMPolicyEngine`/`InMemoryLLMPolicyEngine`은 YAML을
  전혀 알지 못함 — 저장 형식이 나중에 바뀌어도 Engine은 영향받지 않음.
  **신규 외부 의존성**: 프로젝트 최초로 `pyyaml`을 `pyproject.toml`
  `dependencies`에 추가(순수 stdlib 기조 최초 이탈, 사용자 승인).
  `mypy` strict 통과를 위해 `types-PyYAML`도 `dev` 의존성에 추가.
  `docs/llm_policy.example.yaml`의 최상위 key를 `AgentRole.value`와
  정확히 일치하도록 수정(`planning`→`planner`, `implementation`→
  `coding`, `review`→`reviewer`, 나머지는 이미 일치) — 지금까지는
  "실제로 동작하지 않는 문서 초안"이었으나 이제부터는 실제로 파싱되는
  설정 파일이 됨. `coordinator`는 의도적으로 규칙 없음(`select()` 호출
  시 `PolicyNotFoundError`). 알 수 없는 role/provider/effort 값은
  조용히 넘어가지 않고 `InvalidLLMPolicyRuleError`로 명확히 실패하도록
  구현(오타 방지). `tests/interfaces/`+`tests/engines/`의
  `test_llm_policy_engine.py`(각 2~3개) + `tests/storage/
  test_llm_policy_loader.py`(5개, 저장소의 실제 example YAML 파일을
  직접 로드해 항상 유효한 형식으로 유지되는지 회귀 방지 테스트 포함).
  `ruff check src tests`, `mypy src`, `pytest`(341개, 기존 331개 +
  신규 10개) 모두 통과.
- 의존성: T1-16

#### M5-T02: Agent Runtime이 LLMPolicyEngine을 통해 정책을 조회하도록 연결
- 목적: `.ai/RULES.md` §7 M3 단계(Agent가 Policy 참조)를 소급 구현해,
  Agent 시작 시점에 Role별 LLM 정책이 실제로 조회·기록되게 한다.
- 작업 내용: `AgentRuntime`이 `LLMPolicyEngine`을 선택적으로 주입받아
  `start_agent()` 시점에 정책을 조회해 `AgentSession`에 기록.
- 완료 조건(DoD): Role에 정책이 있으면 실제로 조회·기록됨, 없으면
  `None`으로 정상 처리됨(예외 없음), `pytest`/`ruff`/`mypy` 통과. 실제
  Engine/Adapter 선택 반영은 포함하지 않음(M5-T05 Multi-Engine 이후).
- 상태: **DONE (2026-07-26)** — **M5-T01 인터페이스 자체 정정(자체
  발견 아닌 사용자 제안)**: 착수 전 사용자가 "정책 없음을
  `PolicyNotFoundError` 예외 대신 `None`을 정상 결과로 반환하도록
  설계하라"고 제안 — Policy Engine은 항상 답을 주는 컴포넌트가 되고
  Runtime은 예외 처리 없이 생명주기 관리에만 집중할 수 있다는 이유.
  M5-T01에서 이미 커밋된 `LLMPolicyEngine.select()`/
  `InMemoryLLMPolicyEngine`/`FakeLLMPolicyEngine`을 이번 Task에서
  즉시 수정 — `PolicyNotFoundError` 완전 제거(`select()`가 `LLMPolicyDecision
  | None` 반환), 관련 테스트 전부 "예외 발생" 검증에서 "None 반환" 검증으로
  갱신(같은 Milestone 내 하루 안에 나온 설계 개선이라 별도 마이그레이션
  경로 없이 바로 반영, "M2/M3 완료 기능 수정 금지"는 이 경우에 해당하지
  않음 — M5 자신의 아주 최근 작업에 대한 정상적인 반복 개선).
  **연결 구현**: `AgentSession`(domain)에 `llm_policy_decision:
  LLMPolicyDecision | None = None` 필드 추가 — 상태처럼 변할 수 있는
  값이 아니라 시작 시점에 한 번 결정되는 값이라 `AgentSession`에 직접
  캐싱해도 기존 "status는 중복 보관하지 않는다" 원칙과 충돌하지 않음(새
  `get_policy_decision()` 메서드 불필요, 반환된 `AgentSession`을 그대로
  읽으면 됨). `AgentRuntime.__init__`에 `llm_policy_engine:
  LLMPolicyEngine | None = None`(선택적 — 기존 모든 호출부는 그대로 동작,
  하위 호환) 추가, `start_agent()`가 주어지면 `select(role)`을 호출해
  세션에 기록. **아직 하지 않은 것(범위 밖, M5-T05로 이월)**: 실제
  `ManagedEngineRuntime`/`ClaudeCodeEngineAdapter`의 model이 이 정책을
  따라 바뀌지는 않음 — 현재 Runtime은 Adapter를 하나만 등록할 수 있어
  Role별 실제 모델 전환이 인프라적으로 불가능(여러 Adapter가 실제로
  생기는 M5-T05 이후 의미가 생김). `tests/interfaces/`+`tests/engines/`
  의 `test_llm_policy_engine.py`(예외→None 반환으로 갱신) +
  `tests/runtime/agent/test_agent_runtime.py`에 4개 신규 테스트(정책
  없음/있음/역할 불일치/**실제 `docs/llm_policy.example.yaml`을 로드한
  진짜 `InMemoryLLMPolicyEngine`으로 전체 조립해 검증**하는 통합
  테스트 포함). `ruff check src tests`, `mypy src`, `pytest`(345개,
  기존 341개 + 신규 4개, 기존 테스트 내용 일부 갱신) 모두 통과.
- 의존성: M5-T01

#### M5-T03: DevelopmentContext 도입 + Coding/Review Agent 강화
- 목적: `CodingAgent`/`ReviewAgent`가 `task.title` 문자열 하나만 주고받던
  것을 실제 산출물이 이어지는 구조로 바꿔 "Task 제목만 전달하는 Agent"
  에서 "실제 산출물을 이어받아 협업하는 Agent"로 발전시킨다.
- 작업 내용: `DevelopmentContext` 도메인 객체 신규, `CodingAgent`/
  `ReviewAgent`가 이를 통해 실행 지시를 조립하고 Event payload로 산출물을
  전달하도록 강화.
- 완료 조건(DoD): `ReviewAgent`가 `CodingAgent`의 실제 실행 결과(output)를
  받아 프롬프트에 반영함을 테스트로 증명, 원본 Task는 변경되지 않음,
  `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — **확인한 핵심 문제**: `ReviewAgent`가
  `CodingAgent`의 실행 결과(`EngineResult.output`)를 전혀 모른 채 같은
  `task.title`로 Claude Code를 다시 호출하고 있었음(T2-06부터 있던
  실질적 정보 단절). `domain/development_context.py`에
  `DevelopmentContext(task_id, instructions, prior_output)` +
  `to_prompt()` 신규 — **사용자 지시로 필드 자체를 진실의 원천으로 두고
  `to_prompt()`는 여러 렌더링 방식 중 하나로 위치**시킴(향후 다른 표현이
  필요해져도 dataclass는 그대로 두고 메서드만 추가 가능). `EngineAdapter.
  run(session_id, task)` 계약은 건드리지 않음(보호 자산) — 대신
  `dataclasses.replace(task, title=context.to_prompt())`로 **임시 사본**을
  만들어 Engine 호출에만 쓰고, `TaskEngine`이 추적하는 원본 `task.title`
  은 그대로 보존(테스트로 증명). `CodingAgent`는 `DevelopmentContext
  (instructions=task.title)`(prior_output 없음, 첫 단계라 기존과 동일한
  프롬프트)로 실행하고 결과를 `CODE_COMPLETED` payload에 `output`/
  `success`로 실어 보냄. `ReviewAgent`는 payload의 `output`을
  `prior_output`으로 받아 실제로 무엇을 검토해야 하는지 알고 실행,
  자신도 `output`/`success`를 `REVIEW_COMPLETED` payload에 실음. **사용자
  지시로 `success`도 함께 포함**(M5-T03에서는 쓰지 않지만 M5-T06 Workflow
  조건부 분기가 재사용할 수 있어 Event 형식을 다시 바꿀 필요가 없어짐).
  **범위에서 제외(사용자 확인)**: `DocumentationAgent`는 이번 Task
  이름에 명시되지 않아 그대로 둠(payload에 필드가 늘어도 `task_id`만
  읽어 하위 호환), `EngineResult.success=False`여도 다음 단계로 계속
  진행하는 기존 동작 유지(성공/실패 처리 강화는 범위 밖),
  `ContextManager`/Memory 연동까지는 확장하지 않음. 새 Interface 없음,
  `EngineAdapter`/`EngineRuntime` 계약 무변경. `tests/domain/
  test_development_context.py`(2개) + 신규 `tests/agents/
  test_coding_agent.py`/`test_review_agent.py`(각 3개, `RecordingEngineRuntime`
  테스트 더블로 실제 전달되는 title/payload를 직접 검증 — 기존
  `test_pipeline.py`는 Mock 기반 전체 체인만 검증해 이 정밀도가 없었음)
  신규. 기존 `tests/agents/test_pipeline.py`/`tests/integration/
  test_coding_agent_runtime_integration.py`는 수정 없이 그대로 통과.
  `ruff check src tests`, `mypy src`, `pytest`(353개, 기존 345개 +
  신규 8개) 모두 통과.
- 의존성: T2-06

#### M5-T04: ShellAgent 신규
- 목적: 실제 쉘 명령을 실행할 수 있는 새 Agent 종류를 추가해 "Agent가
  실제 개발 작업을 수행"하는 M5 목표를 확장한다(테스트/린트 실행).
- 작업 내용: `AgentRole.SHELL`/`AgentCapability.SHELL` 신규,
  `ShellAgent` 구현(`ProcessRunner` 재사용, 명령어 삽입 방지 설계).
- 완료 조건(DoD): 고정 화이트리스트 명령만 실행됨(이벤트 payload가 명령
  선택에 전혀 영향 없음을 테스트로 증명), `SHELL_COMPLETED` Event에
  stdout/stderr/exit_code/success 포함, `pytest`/`ruff`/`mypy` 통과.
  Review 이전 조건부 분기 연결은 범위 밖(M5-T06).
- 상태: **DONE (2026-07-26)** — **보안 설계가 핵심**: 명령어를 Task
  제목이나 LLM 출력(`DevelopmentContext`, `EngineResult.output`)에서
  절대 유도하지 않음 — 사용자 지시로 4가지 반영: (1) 고정 명령 +
  화이트리스트 유지(`_WHITELISTED_COMMANDS = {"test": ["pytest"],
  "lint": ["ruff", "check", "."]}`), (2) `ShellAgent` 생성자는 명령
  배열이 아니라 화이트리스트 키(`command_kind: str`, 필수·기본값 없음 —
  암묵적 선택 방지)만 받고 실제 명령 배열은 클래스 내부에만 존재(외부
  비노출), 알 수 없는 키는 `UnknownShellCommandKindError`, (3)
  `SHELL_COMPLETED` payload에 `stdout`/`stderr`/`exit_code`/`success`
  전부 포함(M5-T06 Workflow 조건부 분기가 재사용 가능하도록), (4) Effort는
  Medium 유지(사용자 판단 — 보안 위험이 화이트리스트로 충분히 제한되어
  구현 복잡도 자체는 높지 않음). `ProcessRunner`(M3-T03)를 새 Interface
  없이 concrete class로 그대로 재사용(점진적 확장 — 이번이 딱 2번째
  실제 사용처, 3번째 사례가 나오면 추상화 재검토). `EngineRuntime`/
  `EngineAdapter`는 사용하지 않음(쉘 실행은 LLM 엔진 호출이 아님).
  `CODE_COMPLETED`를 구독해 반응하되, **`ReviewAgent`의 트리거는
  바꾸지 않음**(Shell 결과에 따른 조건부 재작업 연결은 명시적으로
  M5-T06 범위로 남김). `agents/events.py`에 `SHELL_COMPLETED` 신규.
  `tests/agents/test_shell_agent.py`에 7개 테스트 — 미등록 키 거부,
  test/lint 화이트리스트 명령 검증, **이벤트 payload에 악의적 문자열이
  있어도 명령이 절대 바뀌지 않음을 직접 검증**(명령어 삽입 방지
  증명), 성공/실패 payload 필드 검증, 무관한 Event 타입 무시. 기존
  4-Agent 파이프라인 테스트(`test_pipeline.py` 등)는 수정 없이 그대로
  통과(ShellAgent를 파이프라인에 아직 연결하지 않았으므로 영향 없음).
  `ruff check src tests`, `mypy src`, `pytest`(360개, 기존 353개 +
  신규 7개) 모두 통과.
- 의존성: M3-T03, T2-06

#### M5-T05: Codex/Gemini CLI Engine Adapter (가능한 범위)
- 목적: Multi-Engine 지원(PRD 7.8)을 향해 Codex/Gemini CLI를 실제로
  호출할 수 있는 Adapter를 추가한다.
- 작업 내용: `CLIEngineAdapter`+`CLIProvider` 프레임워크 신규(사용자
  제안 — 향후 Qwen CLI/Aider 등 추가 시 Provider 하나만 등록하면 되도록
  확장 가능한 구조), `CodexProvider`/`GeminiCliProvider` 구현.
- 완료 조건(DoD): `EngineAdapter` 계약 충족(Fake 기반 단위 테스트),
  실제 CLI 미설치 상태에서도 안전하게 테스트 가능, `pytest`/`ruff`/
  `mypy` 통과. `ClaudeCodeEngineAdapter` 리팩터링은 범위 밖.
- 상태: **DONE (2026-07-26)** — **범위 확정 경위**: 원래 계획은
  "Codex/Gemini Adapter 각각 구현"이었으나, 사용자가 착수 직전 "CLI
  LLM Adapter Framework(공통) + Provider(개별)" 구조를 제안 — 향후
  Qwen CLI/OpenCode/Aider 등이 추가되어도 Task 없이 Provider 하나만
  등록하면 되는 확장성을 근거로 채택. **`ClaudeCodeEngineAdapter`(M3-T02,
  이미 M3/M4/M5 여러 통합 테스트에서 사용 중)는 사용자 지시로 이번에
  리팩터링하지 않고 그대로 유지** — 2단계 전략으로 확정: 이번 Task는
  Codex/Gemini만 새 프레임워크로 구현하고, Claude Code까지 통합하는
  것은 프레임워크가 충분히 검증된 뒤 M6+로 이월. **CLI 미설치로 인한
  미검증 명시**: 이 환경에 `codex`/`gemini` CLI가 설치되어 있지 않아
  (`command not found` 확인) M3-T02처럼 `--help`나 실제 호출로 검증할
  방법이 없었음 — WebSearch로 공개 문서(OpenAI Developers `codex exec`/
  Non-interactive mode, Gemini CLI Headless Mode/Configuration, 모두
  2026-07 기준)를 조사해 구성했고, 두 Provider의 docstring에 "미검증
  경고"와 근거 문서를 명시해 향후 실제 CLI 확보 시 재확인이 필요함을
  분명히 함. `adapters/cli_provider.py`의 `CLIProvider`(ABC, `adapters/`
  내부 협력자 — `interfaces/`의 보호 자산 목록에는 포함하지 않음,
  Agent/WorkspaceCore는 이를 모르고 `EngineAdapter`만 상대함) +
  `adapters/cli_engine_adapter.py`의 `CLIEngineAdapter`(`EngineAdapter`
  구현체, 세션 생명주기·Timeout·Cancel 로직은 `ClaudeCodeEngineAdapter`
  와 동일하게 검증된 패턴을 그대로 재현 — 두 어댑터 사이 일부 로직
  중복을 의도적으로 감수함, 사용자 승인) 신규. `adapters/
  codex_provider.py`(`codex exec ... --json --full-auto`, NDJSON 마지막
  줄에서 텍스트 필드 추출, 실패 시 원문 폴백)/`adapters/
  gemini_cli_provider.py`(`gemini -p ... --output-format json
  --non-interactive --yolo`, `{"response": ...}` 파싱) 신규. `tests/
  adapters/test_cli_engine_adapter.py`(8개, `FakeCLIProvider`+
  `FakeProcessRunner`로 세션 생명주기·Timeout·Cancel·종단 상태 보존
  전부 재검증) + `test_codex_provider.py`/`test_gemini_cli_provider.py`
  (각 6개, 명령 조립·결과 파싱·폴백 검증) 신규 — 전부 Fake 기반이라
  실제 CLI 없이도 안전하게 통과. `ruff check src tests`, `mypy src`,
  `pytest`(380개, 기존 360개 + 신규 20개) 모두 통과.
- 의존성: M3-T02, M3-T03

#### M5-T06: Workflow 조건부 분기 + Step Domain 반영
- 목적: 테스트 실패 시 자동으로 재작업 Task를 만들어 되돌리는 조건부
  분기를 구현해 M5를 "실제 개발 수행" Milestone으로 완성하고, M2 이월
  부채 #6(Step 도메인 미반영)을 해소한다.
- 작업 내용: `CoordinatorAgent` 신규(ADR-0019 Coordination Capability
  최초 구현), `ReviewAgent` 트리거 재배선(`CODE_COMPLETED`→
  `CODE_VERIFIED`), `TaskEngine`에 Step 실행 이력 추가.
- 완료 조건(DoD): 테스트 통과 시 Review로 진행, 실패 시 재작업 Task로
  되돌아감(무한 루프 방지 포함), Step에 시도 이력이 기록됨,
  `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26, Effort High 승인)** — **핵심 발견**:
  `ReviewAgent`가 여전히 `CODE_COMPLETED`를 직접 구독하고 있어(M5-T04에서
  "조건부 연결은 M5-T06으로 이월"이라 명시한 지점), Shell 테스트 결과와
  무관하게 Review가 이미 실행되고 있었음 — 이번 Task에서 실제로 트리거를
  재배선함. **`AgentRole.COORDINATOR`/`AgentCapability.COORDINATION`은
  ADR-0019(M1)부터 존재했지만 지금까지 어떤 Agent도 쓴 적이 없었음** —
  `CoordinatorAgent`가 최초 구현체. **사용자가 설계 검토 후 2가지 반영**:
  (1) Step의 소유권을 `CoordinatorAgent` 내부 리스트가 아니라 실행
  컨텍스트에 둠 — `TaskEngine`(Task를 실제로 소유하는 컴포넌트)에
  `record_step()`/`get_steps()`를 추가하고 `CoordinatorAgent`는 자체
  상태 없이 이를 호출만 함(Repository/StepEngine은 만들지 않음, YAGNI).
  (2) Effort를 Medium→High로 상향(이벤트 흐름+재시도 로직을 포함하는
  첫 Workflow 오케스트레이션 구현이라 M5에서 가장 복잡한 Task 중 하나).
  **파이프라인 재구성**: `agents/events.py`에 `CODE_VERIFIED`/
  `REWORK_EXHAUSTED` 신규. `CoordinatorAgent`는 `SHELL_COMPLETED`를
  구독 — 성공하면 `CODE_VERIFIED` 발행(ReviewAgent를 깨움), 실패하면
  `TaskEngine.record_step()`으로 시도를 기록하고 `max_rework_attempts`
  (기본 3) 이내면 같은 task_id로 `MISSION_PLANNED`를 재발행(payload에
  `rework_reason`)해 `CodingAgent`로 되돌리며, 초과하면 `REWORK_EXHAUSTED`
  발행 후 중단(무한 루프 방지). `ShellAgent`가 `CODE_COMPLETED`의
  `output`(코드)을 자신의 `SHELL_COMPLETED` payload에 `code_output`으로
  전달하도록 보강(이전엔 유실되고 있었음). `CodingAgent`는 `rework_reason`
  이 있으면 `DevelopmentContext.prior_output`으로 반영해 재작업 시 이전
  실패 내용을 알고 실행. `Task`의 기존 상태 전이 규칙(REVIEW→IN_PROGRESS
  허용)이 이미 재작업 시나리오를 정확히 지원하고 있음을 확인(도메인
  모델 변경 불필요). **기존 테스트 갱신 필요성**: `ReviewAgent`의 트리거
  변경은 실질적 동작 변경이라, T2-06의 `test_pipeline.py`(4-Agent)와
  M4-T04의 `test_coding_agent_runtime_integration.py`가 `ShellAgent`/
  `CoordinatorAgent` 없이는 더 이상 Review까지 도달하지 못하게 됨 — 두
  파일 모두 6-Agent 구성으로 갱신(M4-T04에서 확립한 "정확한 전체 Event
  순서 재유도" 방식 그대로 재검증, 새로 도출한 순서가 실제 실행과 정확히
  일치함을 확인). 신규 `tests/agents/test_coordinator_agent.py`(5개,
  성공/실패/Step 기록/재작업 소진/무관 이벤트 무시) + `tests/interfaces/`
  `tests/engines/`의 `test_task_engine.py`에 Step 테스트 각 6개 +
  `test_coding_agent.py`에 rework_reason 테스트 1개 추가. `ruff check
  src tests`, `mypy src`, `pytest`(398개, 기존 380개 + 신규 18개) 모두
  통과.
- 의존성: M5-T03, M5-T04

#### M5-T07: Milestone 5 Review
- 목적: Approval Required 원칙에 따라 Milestone 5 산출물을 검토받는다.
- 작업 내용: DoD 체크리스트, Architecture Review, Interface First 검토,
  테스트 결과 문서화, Technical Debt 정리, 문서 갱신, Milestone 종료
  선언.
- 완료 조건(DoD): 위 항목 모두 완료 + 사용자 승인.
- 상태: **DONE (2026-07-26 사용자 승인 — Milestone 5 완료)**

---

## Milestone 5 Review

**1. Definition of Done 체크리스트**

M5는 M3/M4와 달리 ROADMAP에 별도 DoD 문구가 없고 Task List(M5-T01~T06)
자체가 DoD다.

| Task | 내용 | 상태 |
|---|---|---|
| M5-T01 | Rule 기반 `LLMPolicyEngine` | ✅ |
| M5-T02 | Agent Runtime이 `LLMPolicyEngine`을 통해 정책 조회·기록 | ✅(실제 Adapter 전환은 아래 5절에서 갭으로 기록) |
| M5-T03 | `DevelopmentContext` + Coding/Review Agent 강화 | ✅ |
| M5-T04 | `ShellAgent` 신규 | ✅ |
| M5-T05 | Codex/Gemini CLI Engine Adapter(가능한 범위) | ✅(실제 CLI 미검증, 아래 명시) |
| M5-T06 | Workflow 조건부 분기 + Step Domain 반영 | ✅ |

6개 Task 전부 완료. PRD 7.8(Multi-Engine)·7.3(Workflow 조건부 분기) 갭도
이번에 해소됨.

**2. Architecture Review**

M5에서 실제로 바뀐 구조:
- **정책 결정 계층 신규**: `LLMPolicyEngine`(M5-T01) → `AgentRuntime`이
  `start_agent()` 시점에 조회해 `AgentSession.llm_policy_decision`에
  기록(M5-T02).
- **Agent 간 정보 전달 구조화**: `DevelopmentContext`(M5-T03)로 Coding→
  Review 사이 실제 산출물이 이어짐. `EngineAdapter.run()` 계약은
  건드리지 않고 `dataclasses.replace()`로 임시 사본만 사용.
- **Agent 파이프라인 확장**: Planning→Coding→**Shell→Coordinator**→
  Review→Documentation(M5-T04/T06) — `ShellAgent`(실제 쉘 실행,
  화이트리스트 기반)와 `CoordinatorAgent`(ADR-0019 Coordination
  Capability 최초 구현, 조건부 분기)가 추가됨. `ReviewAgent`의 트리거가
  `CODE_COMPLETED`→`CODE_VERIFIED`로 재배선되어 테스트를 통과한 코드만
  검토 대상이 됨.
- **Multi-Engine 프레임워크 신규**: `CLIProvider`+`CLIEngineAdapter`
  (M5-T05) — `ClaudeCodeEngineAdapter`(M3-T02)는 의도적으로 별도 유지,
  Codex/Gemini만 이 프레임워크 사용(2단계 전략, M6+에서 통합 검토).
- **Step 실행 이력 반영**: `TaskEngine.record_step()`/`get_steps()`
  (M5-T06) — Step의 소유권은 Agent가 아니라 Task 실행 컨텍스트에
  둠(M2 이월 부채 #6 해소).

`docs/ARCHITECTURE.md`는 각 Task 완료 시점마다 즉시 갱신되어(§3.6
Coordination, §4 Step, §7 Interfaces 표, §3.10~3.11 CLI 계열) 구현과
문서 사이 괴리가 없음을 확인했다.

**3. Interface First 원칙 검토**

**M5는 M2~M4와 달리 새 최상위 Interface를 1개(`LLMPolicyEngine`) 추가했다**
— M1 이후 처음이다. 다만 이 추가는 사전 계획 없이 즉흥적으로 이뤄진 것이
아니라, `.ai/RULES.md` §7이 애초에 "Policy Engine"이라는 이름으로 이
계약의 등장을 예정해 두었던 것이 M5-T01에서 실현된 것이다 — Interface
First 원칙의 "필요성이 실제로 증명된 뒤에 계약을 도입한다"는 정신에
부합한다. `interfaces/task_engine.py`는 기존 계약에 `record_step`/
`get_steps`를 순수 추가(기존 메서드 무변경). `CLIProvider`(M5-T05)는
의도적으로 `interfaces/`에 넣지 않고 `adapters/` 내부 협력자로 유지했다
(Agent/WorkspaceCore가 이를 알 필요가 없어서) — "무엇이든 Interface로
만들지 않는다"는 판단도 함께 실증되었다.

**4. 테스트 결과**

- `pytest`: **398개 전부 통과**(M4 완료 시점 331개 → M5에서 67개 신규)
- `ruff check src tests`: 클린
- `mypy src`: 클린(82개 소스 파일)
- M4 완료 커밋(`7b28391`) 대비 소스 10개 파일 신규, 36개 파일 변경,
  약 1,840줄 순증가(src+tests 합산)
- 프로젝트 최초 외부 런타임 의존성(`pyyaml`) 추가(M5-T01)

**5. Technical Debt 정리**

*M5에서 의도적으로 범위를 좁히거나 이월한 것*
- **정책→실행 연결 미완성**: `LLMPolicyEngine`이 결정을 내려도 실제로
  어떤 Adapter/Model을 쓸지는 아직 자동 전환되지 않는다 —
  `ManagedEngineRuntime`이 Adapter 하나만 등록 가능하고, Agent가
  `LLMPolicyDecision.model.provider`에 따라 `ClaudeCodeEngineAdapter`/
  `CLIEngineAdapter(CodexProvider)`/`CLIEngineAdapter(GeminiCliProvider)`
  중 하나를 실제로 선택하는 라우팅 로직은 아직 없다(M5-T02에서 이미
  예견된 갭).
- **Codex/Gemini CLI 미검증**: 이 환경에 두 CLI가 설치되어 있지 않아
  실제 실행으로 검증하지 못함(M5-T05). 실제 CLI 확보 시 `--help`로
  재확인 필요.
- **`ClaudeCodeEngineAdapter`와 `CLIEngineAdapter` 프레임워크 미통합**:
  두 어댑터 계열 사이 로직 중복을 의도적으로 감수(M6+에서 재검토, 사용자
  2단계 전략).
- **Memory Engine 요약 여전히 미구현**: M4-T08에서 "LLM Router 준비
  이후"로 이관했으나, M5가 만든 건 "정책 결정"(어떤 모델/effort를 쓸지)
  이지 "실제로 LLM을 호출해 텍스트를 처리하는 범용 서비스"가 아니다 —
  전제 조건이 완전히 충족되지 않았음을 재확인.
- **Automation Engine 조건 평가 여전히 호출자 책임**(M4-T07에서 이미
  기록, 이번에도 미해결).
- **`ShellAgent` 화이트리스트가 코드에 고정**: `command_kind`를 CLI나
  설정 파일로 노출하는 기능은 없음(현재는 프로그램적 구성만 가능).

*M2/M3/M4에서 이월된 항목 중 M5 범위 밖이라 여전히 미해결*
- `RecoveringEngineRuntime.run_parallel()`이 병렬 배치 내 개별 Task
  재시도 미지원(M4-T06)
- `MemoryEngine.search()` 선형 스캔(M4-T08)
- Retry Backoff, Persistent Runtime Recovery, Approval 비동기 처리,
  Process Timeout 정책 고도화(M3-T08)
- M2 이월 부채 #4(Event ID 생성 방식 불일치)는 M5 착수 전 사전 정리에서
  조사해 이미 해소로 종결(M5 착수 시점에는 "#3"으로 잘못 표기했으나 이
  Review에서 정정 — 원래 M2 Retrospective 번호는 #3이 EventBus 재귀
  발행 순서, #4가 Event ID 방식임). `Step` 도메인(#6)도 이번에 실질
  반영됨(M5-T06). 결과적으로 M2 이월 부채(#1/#2/#4/#5/#6)는 모두 해소
  또는 종결되었고, **#3(EventBus 재귀 발행 시 수신 순서 뒤집힘)만
  기능적 문제 없음으로 그대로 유지**(M2 Retrospective 당시 판단 그대로).

**6. 문서 정리**

`.ai/TASKS.md`(본 Review) / `.ai/MEMORY.md`(M1~M4와 동일하게 압축) /
`docs/ROADMAP.md`(M5 완료 표시) / `docs/ARCHITECTURE.md`(각 Task 진행
중 이미 갱신됨) 갱신 완료. `pyproject.toml`은 M5-T01에서 이미 의존성을
반영했으므로 버전 추가 상향은 필요 없음(v0.5.0 유지 — 구조적 기준선은
그대로, 이번 Milestone은 그 위에 기능을 얹은 것).

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절), Interface
First 검토 완료(3절, 새 Interface 1개 추가를 투명하게 보고), 테스트 결과
문서화 완료(4절), Technical Debt 정리 완료(5절), 문서 갱신 완료(6절) —
6개 조건 모두 만족. Review 중 코드 변경이 필요한 치명적 문제(버그·계약
위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 5 Completed를 선언한다.**

**Milestone 6 상태**: 아직 목표/DoD/Task List가 전혀 정의되지 않았다.
`.ai/RULES.md` §7 로드맵상 다음 단계는 "Self Optimizer 자동 최적화"이지만,
이는 M5-T01/T02가 이미 대신 처리한 M2/M3 단계 소급 구현 이후의 후속
논의 대상이며 확정된 것은 아니다. Milestone 6는 착수 시점에 이 문서에
목표/DoD/Task List를 새로 정의한다(Task Driven Development 원칙,
M2/M3/M4/M5가 그래왔듯).

---

## Milestone 6 — Policy 기반 실행 라우팅 (Policy-Driven Engine Routing)

**목표**: `.ai/RULES.md` §7(Temporary LLM Policy) 로드맵의 "M4 단계: Policy
Engine이 자동으로 Provider/Model/Effort를 선택한다"를 완성한다. M5-T01/T02가
정책을 "조회·기록"하는 데까지만 연결했던 것을, 이번에는 실제로
`LLMPolicyDecision`에 따라 서로 다른 등록된 `EngineAdapter`
(`ClaudeCodeEngineAdapter`/`CLIEngineAdapter`+`CodexProvider`/
`CLIEngineAdapter`+`GeminiCliProvider`)가 선택되어 실행되도록 만든다 —
정책→실행 연결을 완성하는 것이 M5 Review가 남긴 가장 핵심적인 미해결 갭이다.

> **2026-07-26 사용자 확정**: 핵심 목표를 "Policy→Execution 라우팅 완성"으로
> 좁게 유지한다. Adapter 계열 통합(`ClaudeCodeEngineAdapter`↔
> `CLIEngineAdapter` 흡수), Codex/Gemini CLI 실제 재검증, 소규모 이월
> 부채(`run_parallel` 개별 재시도/`MemoryEngine.search` 성능/`ShellAgent`
> 화이트리스트 외부화 등) 3가지는 사용자가 명시적으로 이번 범위에서
> 제외했다 — 계속 이월.

**Analysis 요약(Repository-Analysis 결과)**:
- `EngineRuntime` 인터페이스(§3.9)는 이미 `register_engine(name, adapter)` +
  `run(task, required_capabilities)` 형태로 **다중 엔진 등록·Capability
  기준 선택을 계약으로 예정**해 두었다(M2/T2-05 `InMemoryEngineRuntime`이
  이미 이렇게 동작). 실제 갭은 인터페이스가 아니라, M3-T01에서 의도적으로
  범위를 좁힌 프로덕션 구현 `ManagedEngineRuntime`에 있다 —
  `register_engine()`이 두 번째 호출부터 무조건 `DuplicateEngineError`를
  던져 **정확히 1개 Adapter만 등록 가능**하다
  (`runtime/engine/managed_engine_runtime.py`).
- `AgentSession.llm_policy_decision`(M5-T02)은 `CodingAgent`/`ReviewAgent`/
  `DocumentationAgent` 3개 Agent가 이미 `self._session`으로 갖고 있지만,
  셋 다 `engine_runtime.run(task)` 호출 시 `required_capabilities`를 전혀
  넘기지 않는다(기본값 `frozenset()`) — 정책이 기록만 되고 실행에는 전혀
  반영되지 않는다.
- `LLMProvider`(도메인, ANTHROPIC/OPENAI/GOOGLE/XAI)와 Adapter의
  `capabilities()` 태그(`ClaudeCodeEngineAdapter`→`"claude_code"`,
  `CLIEngineAdapter`→`CLIProvider.capabilities()`) 사이에는 아직 매핑이 없다.
- `cli/main.py`는 실행이 필요한 명령이 아직 없어 의도적으로 어떤 Adapter도
  등록하지 않는다(지연 초기화) — 이번 Milestone은 CLI 명령 추가를 목표로
  하지 않으므로 이 상태를 그대로 둔다.

**Task List**(2026-07-26 확정, 상세 스펙은 각 Task 착수 시점에 이 문서에 추가)

| Task | 내용 | 근거/출처 |
|---|---|---|
| M6-T01 | `ManagedEngineRuntime` 다중 Adapter 등록 지원(`register_engine`의 "정확히 1개" 제한 해제, name 기준 dict 저장, `required_capabilities` 만족 후보 중 선택) — **완료** | M5 Review 이월 갭 #1 |
| M6-T02 | `LLMProvider` → Engine Capability 태그 매핑 + `CodingAgent`/`ReviewAgent`/`DocumentationAgent`가 `llm_policy_decision`을 `required_capabilities`로 변환해 `engine_runtime.run()`에 전달 — **완료** | RULES §7 M4 단계(자동 선택) |
| M6-T03 | 다중 Adapter 조립 + End-to-End 검증(정책에 따라 실제로 다른 Adapter가 선택·실행됨을 통합 테스트로 증명) — **완료** | Milestone DoD |
| M6-T04 | Milestone 6 Review — **완료** | 관례 |

**Architecture Review(사전 검토, 착수 전)**:
- **컴포넌트 경계**: 이번 변경은 `EngineRuntime`(§3.9)의 **구체 구현체**
  (`ManagedEngineRuntime`)와 `Agent`(§3.6) 계층에 한정된다. `EngineAdapter`
  (§3.10) 계약, `LLMPolicyEngine`(§7 Interfaces) 계약 모두 변경 없음.
- **의존성 방향(DIP)**: Agent는 여전히 구체 Adapter를 모르고 `EngineRuntime`
  인터페이스만 안다 — 역류 없음. `LLMProvider`→Capability 태그 매핑을 3개
  Agent가 각자 중복 구현하면 SRP 위반이므로, 도메인 계층의 작은 순수
  함수 하나로 추출해 공유한다(Agent→domain 방향 유지).
- **Interface First**: `EngineRuntime`/`EngineAdapter` 인터페이스 변경
  **0건** — M2에서 이미 계약해 둔 다중 엔진 선택 기능을 구현체가 이제야
  따라잡는 것뿐이다. 새 Interface 추가 없음(M5가 1개 추가했던 것과 달리
  이번엔 기존 계약으로 충분함을 사전 확인).
- **YAGNI 점검**: `required_capabilities`가 여러 Adapter와 동시에 매칭되는
  상황은 실제로 발생하지 않는다(Provider당 Adapter가 정확히 1개씩만
  등록되므로) — 복수 매칭 시 우선순위 정책(비용 기반 선택 등)은 지금
  필요가 증명되지 않아 설계하지 않는다.
- **리스크**: (1) `CLIProvider`(Codex/Gemini) 구현체의 `capabilities()`가
  실제로 Provider 구분 태그를 포함하는지 M6-T02 착수 시 재확인 필요(포함
  하지 않으면 매핑 태그 추가가 M6-T02 범위에 포함됨). (2) 정책이 없는
  Role은 `required_capabilities=frozenset()`을 유지해 기존 동작과 완전히
  하위 호환. (3) `LLMProvider.XAI`처럼 대응 Adapter가 없는 Provider가
  정책에 등장하면 `NoSuitableEngineError`가 발생하는 것이 의도된
  동작이다(별도 처리 불필요).

**Definition of Done**
1. `LLMPolicyDecision.model.provider`에 따라 `CodingAgent`/`ReviewAgent`/
   `DocumentationAgent`가 실제로 서로 다른 등록된 `EngineAdapter`
   (`ClaudeCodeEngineAdapter`/`CLIEngineAdapter`+`CodexProvider`/
   `CLIEngineAdapter`+`GeminiCliProvider`)를 선택해 실행함이 통합
   테스트로 검증된다.
2. `ManagedEngineRuntime`이 2개 이상의 `EngineAdapter`를 동시에 등록할 수
   있고, `required_capabilities`로 올바른 Adapter를 선택하며, 만족하는
   Adapter가 없으면 `NoSuitableEngineError`를 던진다(계약 테스트로 검증).
3. `EngineRuntime`/`EngineAdapter` 인터페이스 계약이 변경되지 않는다
   (Interface First 재확인).
4. 기존 `pytest` 전체 스위트(M5 종료 시점 398개) + 신규 테스트 모두 통과,
   `ruff`/`mypy` 클린.
5. `docs/ARCHITECTURE.md` §3.9/§3.10에 다중 Adapter 등록·선택 방식이
   반영된다.
6. Adapter 계열 통합, Codex/Gemini CLI 실제 재검증, 소규모 이월 부채는
   이번 Milestone 범위에서 명시적으로 제외되며 계속 이월된다(위 사용자
   확정 참고).

**상태**: M6-T01~T04 전체 DONE. **2026-07-26 사용자 승인으로 Milestone 6
종료.** Review 전문은 아래 "Milestone 6 Review" 절 참고.

#### M6-T01: `ManagedEngineRuntime` 다중 Adapter 등록 지원
- 목적: `EngineRuntime` 인터페이스가 이미 계약해 둔 "다중 엔진 등록·
  Capability 기준 선택"을 프로덕션 구현체 `ManagedEngineRuntime`이
  따라잡게 한다 — M3-T01에서 의도적으로 "Adapter 정확히 1개만 등록
  가능"으로 좁혀 뒀던 것을 M6에서 해제한다.
- 작업 내용: `register_engine()`이 같은 이름을 재등록할 때만
  `DuplicateEngineError`를 던지도록 변경(내부 저장을 `EngineAdapter |
  None` 단일 필드에서 `dict[str, EngineAdapter]`로 교체). `_require_adapter()`
  가 등록된 여러 어댑터 중 `required_capabilities.issubset(capabilities())`
  를 만족하는 첫 어댑터(등록 순서 기준)를 선택하도록 변경. `cancel()`이
  task_id별로 실제 실행에 쓰인 어댑터를 정확히 찾아 취소를 전달하도록
  `_task_adapters: dict[str, EngineAdapter]` 신규 추가(여러 어댑터가
  섞여 있을 때도 잘못된 어댑터에 취소가 전달되지 않도록).
  `tests/interfaces/fakes.py`의 `FakeEngineRuntime`이 이미 이 방식(이름
  기준 dict + 첫 매칭)으로 구현되어 있어 그대로 참고했다.
- 완료 조건(DoD): 서로 다른 이름으로 2개 이상 Adapter 등록 성공, 같은
  이름 재등록은 여전히 `DuplicateEngineError`, `required_capabilities`로
  올바른 Adapter가 선택되어 실행됨(다른 Adapter는 호출되지 않음),
  매칭 실패 시 `NoSuitableEngineError`. `EngineRuntime`/`EngineAdapter`
  인터페이스 변경 없음. `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — `register_engine_twice_raises_duplicate_error`
  테스트를 "같은 이름 재등록 시에만 에러"로 의미를 명확히 갱신
  (`test_register_engine_same_name_twice_raises_duplicate_error`), 신규
  테스트 3개(`test_register_engine_with_different_names_both_succeed`,
  `test_run_selects_matching_adapter_among_multiple_registered` —
  실행 횟수를 기록하는 `RecordingEngineAdapter`로 실제 선택된 어댑터만
  호출됐음을 증명, `test_run_no_matching_adapter_among_multiple_raises_no_suitable_engine`)
  추가. `run_parallel()`의 `supports_parallel()` 필터링 신설은 기존에도
  없던 동작이라 이번 Task 범위에 포함하지 않았다(YAGNI, 범위 이탈
  방지). `docs/ARCHITECTURE.md` §3.9에 다중 Adapter 등록·선택 방식
  반영. `pytest` 401개(M5 종료 시점 398개 + 신규 3개) 전부 통과,
  `ruff check src tests`/`mypy src` 클린. Agent(Coding/Review/
  Documentation)가 실제로 `required_capabilities`를 넘기도록 반영하는
  것은 M6-T02 범위.
- 의존성: 없음(M6 Task List 첫 Task)

#### M6-T02: `LLMProvider` → Engine Capability 매핑 및 Agent 라우팅
- 목적: M6-T01이 만든 다중 Adapter 등록 기반 위에, `LLMPolicyDecision`이
  실제로 어떤 Adapter를 선택할지를 결정하는 신호(`required_capabilities`)
  를 흘려보낸다 — Policy→Execution 라우팅의 실질적인 연결 지점.
- 작업 내용: `domain/llm_policy.py`에 `LLMProvider`→capability 태그
  매핑(`_PROVIDER_ENGINE_CAPABILITY`: ANTHROPIC→`claude_code`, OPENAI→
  `codex`, GOOGLE→`gemini`, XAI→`xai`)과 `required_capabilities(decision:
  LLMPolicyDecision | None) -> frozenset[str]` 순수 함수 추가(정책 없으면
  빈 집합). `CodingAgent`/`ReviewAgent`/`DocumentationAgent` 3곳이
  `self._session.llm_policy_decision`을 이 함수에 넘겨 `engine_runtime.
  run(..., required_capabilities=...)`로 전달하도록 수정.
- 착수 시 확인한 사실: 실제 Adapter의 capability 태그를 재확인한 결과
  `ClaudeCodeEngineAdapter`→`"claude_code"`, `CodexProvider`→`"codex"`,
  `GeminiCliProvider`→`"gemini"`(M6-T01 문서에 "gemini_cli"로 적었던 것은
  오기 — `docs/ARCHITECTURE.md` §3.9에서 바로잡음). `docs/
  llm_policy.example.yaml`의 실제 규칙(`coding→anthropic`, `reviewer→
  openai`, `documentation→google`)이 정확히 이 3개 Agent와 1:1 매칭되어
  설계가 실사용 정책과 들어맞음을 확인했다.
- 완료 조건(DoD): 정책이 없으면 `required_capabilities`가 빈 집합(기존
  동작과 하위 호환), 정책이 있으면 매핑된 태그가 실제로 `engine_runtime.
  run()`에 전달됨을 3개 Agent 각각 단위 테스트로 검증. `EngineRuntime`
  인터페이스·`docs/ARCHITECTURE.md` 컴포넌트 구조 변경 없음(Agent 내부
  로직 변경일 뿐). `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — `tests/domain/test_llm_policy.py`에
  `required_capabilities` 단위 테스트 5개(정책 없음, ANTHROPIC/OPENAI/
  GOOGLE 매핑, 모든 Provider 매핑 존재 확인) 추가. `RecordingEngineRuntime`
  (`tests/agents/test_coding_agent.py`)이 `required_capabilities`도
  기록하도록 확장해 `CodingAgent`/`ReviewAgent`에 각 2개, 신규
  `tests/agents/test_documentation_agent.py`(이전에는 전용 테스트 파일이
  없었음 — `DocumentationAgent` 단위 테스트를 이번에 처음 추가)에 3개
  테스트 추가 — 총 pytest 412개(M6-T01 종료 시점 401개 + 신규 11개) 전부
  통과, `ruff check src tests`/`mypy src` 클린. `docs/ARCHITECTURE.md`
  §3.9에 매핑 규칙과 라우팅 흐름을 반영(인터페이스/컴포넌트 구조는
  무변경이므로 최소 갱신). 실제로 여러 Adapter를 등록해 이 라우팅이
  End-to-End로 동작하는지 증명하는 것은 M6-T03 범위.
- 의존성: M6-T01

#### M6-T03: 다중 Adapter 조립 + End-to-End 검증
- 목적: M6-T01(다중 등록)/M6-T02(Provider→Capability 매핑·Agent 라우팅)이
  실제로 하나의 파이프라인 안에서 맞물려 동작하는지 End-to-End로
  증명한다 — Milestone DoD 1번의 직접적인 검증 대상.
- 작업 내용: `tests/integration/test_m6_policy_routing.py` 신규.
  `ManagedEngineRuntime`에 `ClaudeCodeEngineAdapter`+`CLIEngineAdapter`
  (`CodexProvider`)+`CLIEngineAdapter`(`GeminiCliProvider`) 3개를 각각
  `"claude_code"`/`"codex"`/`"gemini"` 이름으로 동시 등록하고, 저장소의
  실제 `docs/llm_policy.example.yaml`을 로드한 진짜
  `InMemoryLLMPolicyEngine`을 `AgentRuntime`에 주입해 전체 6-Agent
  파이프라인(Planning→Coding→Shell→Coordinator→Review→Documentation)을
  조립했다. 세 Adapter 모두 실제 CLI 프로세스 대신 `SwitchingFakeProcessRunner`
  (신규 테스트 더블)를 공유 주입받는다 — `command[0]`(실행 파일 이름)에
  따라 다른 stdout을 반환해, 여러 어댑터가 하나의 ProcessRunner를
  공유해도 실제로 어느 CLI가 호출됐는지 구분할 수 있게 했다.
- 완료 조건(DoD): 기존 파이프라인(M5-T06 DoD)이 다중 Adapter 등록 상태에서도
  회귀 없이 완주(Task DONE, 6개 Event 타입 전부 발행). `docs/
  llm_policy.example.yaml`의 실제 정책(coding→anthropic, reviewer→
  openai, documentation→google)에 따라 Coding/Review/Documentation이
  각각 claude/codex/gemini CLI 명령을 실제로 조립해 호출했음이
  `command[0]` 기준으로 증명됨. Engine 실행 결과(`output`)가 올바른
  Adapter의 응답으로 Event payload까지 그대로 흘러감. `pytest`/`ruff`/
  `mypy` 통과.
- 상태: **DONE (2026-07-26)** — 테스트 4개 추가:
  `test_full_pipeline_completes_with_multiple_registered_adapters`(회귀
  없음 확인 — `ManagedEngineRuntime`은 `InMemoryEngineRuntime`(T2-05)과
  달리 `engine_task_started`/`engine_task_completed` 자체 Event도
  발행하므로 Event 타입 비교를 정확히 일치가 아니라 부분집합 포함으로
  조정), `test_policy_routes_each_role_to_distinct_registered_engine_adapter`
  (claude/codex/gemini 3개 CLI가 각각 정확히 1번씩 호출됨을 증명),
  `test_coding_agent_result_reflects_claude_code_adapter_output`/
  `test_review_agent_result_reflects_codex_adapter_output`(선택된
  Adapter의 실제 실행 결과가 Event payload까지 정확히 전달됨을 증명).
  `pytest` 416개(M6-T02 종료 시점 412개 + 신규 4개) 전부 통과, `ruff
  check src tests`/`mypy src` 클린. Codex/Gemini CLI 실제 바이너리
  검증, `ClaudeCodeEngineAdapter`/`CLIEngineAdapter` 프레임워크 통합은
  이번 Milestone 범위 밖으로 확정된 대로 손대지 않았다.
- 의존성: M6-T01, M6-T02

#### M6-T04: Milestone 6 Review
- 목적: Approval Required 원칙에 따라 Milestone 6 산출물을 검토받는다.
- 작업 내용: DoD 체크리스트, Architecture Review, Interface First 검토,
  테스트 결과 문서화, Technical Debt 정리, 문서 갱신, Milestone 종료
  선언.
- 완료 조건(DoD): 위 항목 모두 완료 + 사용자 승인.
- 상태: **DONE (2026-07-26 사용자 승인 — Milestone 6 완료)**

---

## Milestone 6 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `LLMPolicyDecision.model.provider`에 따라 3개 Agent가 실제로 서로 다른 등록된 `EngineAdapter`를 선택해 실행함이 통합 테스트로 검증 | ✅ (M6-T03) |
| 2 | `ManagedEngineRuntime`이 2개 이상 `EngineAdapter` 동시 등록·`required_capabilities` 기반 선택·매칭 실패 시 `NoSuitableEngineError` | ✅ (M6-T01) |
| 3 | `EngineRuntime`/`EngineAdapter` 인터페이스 계약 변경 없음 | ✅ (아래 3절) |
| 4 | 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린 | ✅ (아래 4절) |
| 5 | Adapter 계열 통합/Codex·Gemini CLI 실제 재검증/소규모 이월 부채는 범위 제외 유지 | ✅ (아래 5절) |

Task List(M6-T01~T03) 전체 완료. M6-T04(본 Review)로 Milestone을 마감한다.

**2. Architecture Review**

M6에서 실제로 바뀐 구조는 정확히 2곳, 둘 다 M5 Review가 예고했던
"정책→실행 연결" 갭을 메우는 최소 변경이었다:
- **`ManagedEngineRuntime`(M6-T01)**: 내부 저장을 `EngineAdapter | None`
  단일 필드에서 `dict[str, EngineAdapter]`로 교체하고, 어댑터 선택 로직을
  "정확히 1개"에서 "`required_capabilities`를 만족하는 첫 매칭"으로
  바꿨다. `cancel()`이 task별 실제 실행 어댑터를 정확히 추적하도록
  `_task_adapters` 맵을 신규 추가했다. `tests/interfaces/fakes.py`의
  `FakeEngineRuntime`(계약 검증용)이 이미 이 방식으로 구현돼 있어 참고
  구현으로 그대로 따랐다 — 즉 `EngineRuntime` 인터페이스가 애초에
  계약해 둔 것을 프로덕션 구현체가 뒤늦게 따라잡은 것뿐이다.
- **Agent 3종(M6-T02)**: `domain/llm_policy.py`에 `LLMProvider`→
  capability 태그 매핑과 `required_capabilities()` 순수 함수를 추가하고,
  `CodingAgent`/`ReviewAgent`/`DocumentationAgent`가 `AgentSession.
  llm_policy_decision`을 이 함수로 변환해 `engine_runtime.run()`에
  전달하도록 3줄씩만 바꿨다. `PlanningAgent`/`ShellAgent`/
  `CoordinatorAgent`는 애초에 `engine_runtime.run()`을 호출하지 않아
  손대지 않았다.

`git diff --stat`(M5 종료 커밋 `b622e5f` 대비)로 확인한 결과 **소스 파일
5개만 수정**(`llm_policy.py`, `managed_engine_runtime.py`,
`coding_agent.py`/`review_agent.py`/`documentation_agent.py`)되었고
**신규 소스 파일은 0개**다(72줄 순증가, 21줄 삭제) — Milestone 목표가
"정책→실행 연결"이라는 좁은 범위였다는 것과, 그 범위를 지키기 위해
Surgical Changes 원칙을 실제로 지켰다는 것을 정량적으로 뒷받침한다.
`docs/ARCHITECTURE.md` §3.9는 두 Task 완료 시점마다 즉시 갱신되어
구현과 문서 사이 괴리가 없다.

**3. Interface First 원칙 검토**

**M6은 새 최상위 Interface를 0개 추가했다** — M1 이후 유일하게 M5만
1개(`LLMPolicyEngine`)를 추가했었고, M2/M3/M4/M6는 모두 0개다.
`EngineRuntime`/`EngineAdapter`/`LLMPolicyEngine` 계약 중 어느 것도
메서드 시그니처가 바뀌지 않았다 — M6가 실제로 한 일은 "이미 계약된 것을
구현체가 따라잡는 것"(`ManagedEngineRuntime`)과 "이미 존재하는 도메인
값(`AgentSession.llm_policy_decision`)을 이미 존재하는 파라미터
(`required_capabilities`)로 연결하는 것"(Agent 3종)뿐이었다. 이는 M2
시점에 `EngineRuntime`/`EngineAdapter` 인터페이스를 설계할 때 이미
"여러 엔진 등록·Capability 기준 선택"을 내다보고 계약해 둔 결과이며,
v0.5.0 아키텍처 기준선(ADR-0024) 선언 이후 "새 기능은 기존 16(+1)종
Interface 위에 조립한다"는 방침이 M6에서도 그대로 지켜졌음을 보여준다.

**4. 테스트 결과**

- `pytest`: **416개 전부 통과**(M5 완료 시점 398개 → M6에서 18개 신규:
  M6-T01 +3, M6-T02 +11, M6-T03 +4)
- `ruff check src tests`: 클린
- `mypy src`: 클린(82개 소스 파일)
- M5 완료 커밋(`b622e5f`) 대비 소스 5개 파일 수정(신규 소스 파일 0개),
  테스트 9개 파일 수정 + 2개 파일 신규(`test_documentation_agent.py` —
  `DocumentationAgent`의 첫 전용 단위 테스트, `test_m6_policy_routing.py`)
- 신규 외부 런타임 의존성 없음(M5의 `pyyaml` 이후 추가 없음).
  `poetry.lock`을 이번 Milestone에서 처음 커밋했다(이전에는 저장소에
  없었음 — 재현 가능한 의존성 고정을 위한 Maintenance 작업, 코드 변경
  아님).

**5. Technical Debt 정리**

*M6에서 의도적으로 범위를 좁히거나 새로 드러난 것*
- **Model/Effort 수준 라우팅 미완성**: 이번에 완성한 것은 **Provider
  단위** 라우팅(`LLMPolicyDecision.model.provider` → 어느 CLI를 쓸지)
  뿐이다. 같은 Provider 안에서 Model(예: `opus`/`sonnet`/`haiku`)이나
  Effort(low/medium/high)를 실제 Adapter 실행에 반영하는 것은 아직 없다
  — `ClaudeCodeEngineAdapter`/`CodexProvider`/`GeminiCliProvider` 모두
  생성 시점에 `model` 파라미터가 고정되고, `EngineAdapter.run()`은
  Model/Effort를 인자로 받지 않는다. Role별로 서로 다른 Model을 실제로
  쓰려면 Role마다 별도 Adapter 인스턴스를 등록하거나 `EngineAdapter`
  계약 자체를 확장해야 하는데, 이는 Milestone 6가 확정한 범위("Adapter
  선택")를 벗어나는 더 큰 결정이라 **M7+ 논의 대상으로 명시적으로
  이월**한다.
- **복수 매칭 시 우선순위 정책 없음**: `required_capabilities`를 만족하는
  Adapter가 여러 개면 등록 순서상 첫 매칭을 쓴다(실제로는 Provider당
  Adapter가 정확히 1개씩만 등록되므로 지금은 발생하지 않는 상황) — 비용
  기반 선택 등은 필요성이 증명되지 않아 여전히 만들지 않는다(YAGNI,
  M6-T01 Architecture Review에서 이미 확인).
- **`run_parallel()`이 `supports_parallel()`을 필터링하지 않음**: 여러
  Adapter가 등록된 지금, `run_parallel()`이 capability만으로 어댑터를
  고르고 병렬 지원 여부는 확인하지 않는다는 사실이 다중 Adapter 환경에서
  더 뚜렷해졌다(`FakeEngineRuntime`은 `require_parallel` 파라미터로 이미
  이를 거르지만 `ManagedEngineRuntime`은 M3-T01부터 하지 않았다) — M6
  범위(단일 `run()` 경로의 Provider 라우팅)와 무관해 이번에도 손대지
  않았다. 실제로 `run_parallel()`을 정책 라우팅과 함께 쓸 계획이 생기면
  다음에 반드시 확인해야 한다.

*사용자가 명시적으로 이번 범위에서 제외한 것(계속 이월)*
- `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임워크 통합(M5-T05에서
  "M6+에서 재검토"로 예고됐던 것 — 이번에 재검토하지 않기로 확정)
- Codex/Gemini CLI 실제 바이너리 설치 후 재검증(M5-T05 미해결)
- `run_parallel` 개별 Task 재시도 미지원(M4-T06), `MemoryEngine.search()`
  선형 스캔(M4-T08), Retry Backoff/Persistent Runtime Recovery/Approval
  비동기 처리/Process Timeout 정책 고도화(M3-T08), `ShellAgent`
  화이트리스트가 코드에 고정(M5-T04)
- Memory Engine 요약(summarization) 여전히 미구현(M4-T08→M5 Review에서
  재확인 — "정책 결정"과 "실제 LLM 호출 서비스"는 여전히 다른 것이라는
  진단이 M6에서도 변하지 않았다. Model/Effort 라우팅 미완성 항목과
  같은 근본 원인)

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M6-T01~T03 상세 섹션) / `docs/ROADMAP.md`(M6
Task List 완료 표시, Milestone 개요 갱신) / `docs/ARCHITECTURE.md`(§3.9
각 Task 완료 시점마다 이미 갱신됨) 완료. `pyproject.toml` 버전은 v0.5.0
그대로 유지한다(M4-T09에서 선언한 구조적 기준선은 그대로이고, M6은 그
위에 기능을 얹은 것 — M5와 동일한 판단). `.ai/MEMORY.md`는 이 Review
승인 직후 M1~M5와 동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 소스 5개
파일 수정·신규 파일 0개로 Surgical Changes 정량 확인), Interface First
검토 완료(3절, 새 Interface 0개 — M2/M3/M4와 같은 패턴 유지), 테스트
결과 문서화 완료(4절), Technical Debt 정리 완료(5절, Model/Effort 라우팅
미완성을 M7+ 논의 대상으로 투명하게 명시), 문서 갱신 완료(6절) — 6개
조건 모두 만족. Review 중 코드 변경이 필요한 치명적 문제(버그·계약
위반)는 발견되지 않았다.

**2026-07-26 사용자 승인으로 Milestone 6 Completed 확정.**

**Milestone 7 상태**: 아직 목표/DoD/Task List가 전혀 정의되지 않았다.
이번 Review에서 드러난 가장 뚜렷한 후속 논의 대상은 "Model/Effort 수준
라우팅"(Role별로 같은 Provider 안에서도 다른 Model/Effort를 실제로
쓰게 하려면 `EngineAdapter` 계약 확장이 필요한지 검토)이지만, 이는 사전
논의 없이 확정된 것이 아니며 Milestone 7은 착수 시점에 이 문서에
목표/DoD/Task List를 새로 정의한다(Task Driven Development 원칙,
M2~M6가 그래왔듯).

---

## Milestone 7 — Memory 요약 (Memory Summarization)

**목표**: PRD 7.4(장기 메모리)와 M4 DoD가 원래 요구했던 "검색/**요약**" 중
"요약"만 M4-T08에서 "LLM 없이는 구현 불가"로 M5 Router 준비 이후로
이관됐던 항목을 완성한다. M6에서 처음으로 실제 LLM 호출 인프라
(`EngineRuntime`→`EngineAdapter`가 실제 claude/codex/gemini CLI를
호출)가 완성되어, 이 차단 사유가 이제 해소 가능하다.

> **2026-07-26 사용자 확정**: 요약 트리거 시점은 **파이프라인 종료
> 시점**(`DocumentationAgent`)으로 좁힌다. 온디맨드(사용자/CLI 요청)
> 트리거는 이번 범위에서 제외.

**Analysis 요약(Repository-Analysis 결과)**:
- `DocumentationAgent._on_review_completed()`가 이미 `engine_runtime.
  run(task, ...)`을 호출하고 있지만, **반환된 `EngineResult`를 캡처하지
  않고 그대로 버린다** — 이 결과(`output`)를 요약으로 재활용하면 신규
  LLM 호출을 추가하지 않고도(YAGNI) 요약을 만들 수 있다.
- `ContextManager.create_snapshot(session)`은 현재 `assemble_context()`
  결과(project_id/mission_id 등 작은 key-value)만 JSON으로 저장한다.
  요약 문자열을 저장할 필드가 없다.
- `MemoryEngine`(ADR-0017)은 "저장/검색만" 담당하며 Snapshot·요약
  개념을 전혀 모른다 — 이 경계를 지키려면 요약 생성·저장 책임은
  `ContextManager`/`Agent` 층에 있어야 하고, `MemoryEngine`은 손대지
  않아야 한다.
- `MemoryEngine.search()`/`ContextManager.find_snapshots()`(M4-T08)는
  이미 구현되어 있으므로, 요약이 Snapshot JSON에 포함되기만 하면
  **추가 구현 없이 요약 검색이 자동으로 동작**한다.

**Task List**(2026-07-26 확정, 상세 스펙은 각 Task 착수 시점에 이 문서에 추가)

| Task | 내용 | 근거/출처 |
|---|---|---|
| M7-T01 | `ContextManager.create_snapshot()`에 선택적 `summary` 파라미터 추가(인터페이스 확장, 하위 호환) — **완료** | PRD 7.4 갭 |
| M7-T02 | `DocumentationAgent`가 기존에 버려지던 `engine_runtime.run()` 결과를 캡처해 요약으로 전달 — **완료** | PRD 7.4 갭 |
| M7-T03 | End-to-End 검증(파이프라인 실행 후 요약이 저장·검색·복원됨을 통합 테스트로 증명) — **완료** | Milestone DoD |
| M7-T04 | Milestone 7 Review — **완료** | 관례 |

**Architecture Review(사전 검토, 착수 전)**:
- **컴포넌트 경계**: `ContextManager`(§3.8)의 **인터페이스 확장**(신규
  메서드가 아니라 기존 `create_snapshot()`에 선택적 파라미터 추가)과
  `DocumentationAgent`(§3.6) 내부 변경으로 한정된다. `MemoryEngine` 계약은
  변경 없음(ADR-0017의 "저장/검색만" 경계 유지 — 여전히 요약이 뭔지
  모른다).
- **의존성 방향(DIP)**: Agent → Context Manager → Memory Engine 방향
  그대로 유지. 요약은 Agent가 이미 소유한 `EngineResult.output`을
  Context Manager에 "전달"만 할 뿐, Context Manager나 Memory Engine이
  EngineRuntime을 알거나 호출하지 않는다 — 역류 없음.
- **Interface First**: `MemoryEngine` 인터페이스 변경 0건. `ContextManager.
  create_snapshot()`에 `summary: str | None = None`(기본값 있음) 추가는
  기존 호출부(`test_pipeline.py`, `tests/memory/test_context_manager.py`
  등 무인자 호출) 전부 하위 호환. 새 최상위 Interface 추가 없음.
- **YAGNI 점검**: 요약 전용 새 EngineRuntime 호출을 만들지 않는다 —
  `DocumentationAgent`가 이미 하던 호출의 결과를 재활용한다(중복 LLM
  호출 방지). 여러 Snapshot에 걸친 "요약의 요약"(누적 압축)은 필요성이
  증명되지 않아 만들지 않는다 — 매 Snapshot마다 최신 요약 하나만
  저장한다.
- **리스크**: (1) `result.success=False`(요약 생성 실패/에러)여도 그
  출력을 그대로 저장하는 단순한 정책을 쓴다 — 실패 감지·재시도·필터링은
  범위 밖(단순성 우선, 필요성 증명 시 다음 Milestone에서 재검토). (2)
  기존에 버려지던 반환값을 캡처하는 것뿐이라 회귀 위험이 낮다.

**Definition of Done**
1. `DocumentationAgent`가 실제로 `engine_runtime.run()`의 결과(`output`)를
   캡처해 `context_manager.create_snapshot(session, summary=...)`로
   전달한다(기존에는 버려졌음).
2. `ContextManager.create_snapshot()`이 선택적 `summary` 파라미터를 받아
   Snapshot 내용에 포함시키며, 기존 무인자 호출(하위 호환)은 그대로
   동작한다.
3. `restore_snapshot()`/`assemble_context()`로 저장된 요약을 다시 조회할
   수 있고, `find_snapshots(query)`로 요약 내용을 검색할 수 있다(PRD 7.4
   "검색/요약" 완전 충족 — M4-T08이 미룬 항목 해소).
4. `MemoryEngine` 인터페이스는 변경되지 않는다(ADR-0017 경계 유지).
5. 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린.
6. Adapter 계열 통합, Codex/Gemini CLI 실제 재검증, Model/Effort 수준
   라우팅, 그 외 소규모 이월 부채는 이번 Milestone 범위 밖으로 유지된다.

**상태**: 목표/Task List/사전 Architecture Review/DoD 확정(2026-07-26
사용자 확정). M7-T01~T04 전체 DONE. **2026-07-26 사용자 승인으로
Milestone 7 종료.** Review 전문은 아래 "Milestone 7 Review" 절 참고.

#### M7-T01: `ContextManager.create_snapshot()`에 선택적 `summary` 파라미터 추가
- 목적: Memory 요약을 저장할 최소 계약을 마련한다 — `MemoryEngine`은
  손대지 않고(ADR-0017 경계 유지), `ContextManager` 인터페이스만
  하위 호환되게 확장한다.
- 작업 내용: `interfaces/context_manager.py`의 `create_snapshot()`에
  `summary: str | None = None` 파라미터 추가(계약 docstring 갱신).
  `memory/context_manager.py`의 `InMemoryContextManager.create_snapshot()`
  이 summary가 주어지면 `context["summary"] = summary`로 병합 후 기존과
  동일하게 `MemoryEngine.remember()`로 저장. `tests/interfaces/fakes.py`
  의 `FakeContextManager`도 동일하게 갱신(계약 테스트 일관성).
- 완료 조건(DoD): summary 없이 호출하면 기존과 완전히 동일하게 동작(하위
  호환), summary가 있으면 `restore_snapshot()`/`assemble_context()`로
  조회되고 `find_snapshots()`로도 검색됨. `MemoryEngine` 인터페이스
  변경 없음. `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — 계약 테스트(`tests/interfaces/
  test_context_manager.py`) 3개 + 단위 테스트(`tests/memory/
  test_context_manager.py`) 3개 신규(summary 포함/미포함/검색). 기존
  프로덕션 호출부(`DocumentationAgent`)는 아직 무인자로 호출하므로
  회귀 없음(summary 실제 반영은 M7-T02 범위). `docs/ARCHITECTURE.md`
  §3.8에 "Context Manager/Memory Engine 둘 다 요약을 생성하지 않는다"는
  경계를 명시. `pytest` 422개(M7 착수 전 416개 + 신규 6개) 전부 통과,
  `ruff check src tests`/`mypy src` 클린.
- 의존성: 없음(M7 Task List 첫 Task)

#### M7-T02: `DocumentationAgent`가 engine 결과를 요약으로 전달
- 목적: M7-T01이 마련한 `summary` 파라미터에 실제 값을 흘려보낸다 —
  Memory 요약을 "만드는" 지점.
- 작업 내용: `_on_review_completed()`에서 `self._engine_runtime.run(...)`
  의 반환값을 `result` 변수로 캡처(이전에는 버려짐), `self._context_manager
  .create_snapshot(self._workspace_session, summary=result.output)`로
  전달하도록 2줄 변경.
- 완료 조건(DoD): `engine_runtime.run()`의 실제 출력이 그대로
  `create_snapshot()`의 `summary`로 전달됨을 단위 테스트로 증명, 저장된
  요약이 `find_snapshots()`로 검색됨. `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — `tests/agents/test_documentation_agent.py`
  에 실제 `InMemoryContextManager`에 위임하며 `summary` 인자를 기록하는
  `SpyContextManager` 신규 도입(기존 3개 테스트는 반환 튜플에 4번째
  원소가 추가되어 그대로 갱신, 하위 호환 깨짐 아님 — 테스트 헬퍼 시그니처
  변경). 신규 테스트 2개: `test_documentation_agent_passes_engine_result_
  output_as_summary`(engine 결과가 실제로 summary로 전달됨),
  `test_documentation_agent_summary_is_retrievable_via_context_manager`
  (저장된 요약이 `find_snapshots()`로 검색됨 — PRD 7.4 DoD 직접 검증).
  성공/실패 여부와 무관하게 `output`을 그대로 저장하는 단순 정책을
  그대로 구현(사전 Architecture Review에서 이미 승인된 단순화).
  `pytest` 424개(M7-T01 종료 시점 422개 + 신규 2개) 전부 통과, `ruff
  check src tests`/`mypy src` 클린.
- 의존성: M7-T01

#### M7-T03: End-to-End 검증
- 목적: M7-T01(계약 확장)/M7-T02(Agent 반영)가 실제 파이프라인 안에서
  맞물려 동작하는지 증명한다 — Milestone DoD 1·3번의 직접 검증 대상.
- 작업 내용: `tests/agents/test_pipeline.py`에
  `test_pipeline_stores_documentation_summary_searchable_via_memory`
  신규 — 기존 `build_pipeline()`(`InMemoryEngineRuntime`+`MockEngineAdapter`
  +실제 `InMemoryContextManager`/`InMemoryMemoryEngine`, T2-06/M5-T06이
  이미 조립해 둔 헬퍼)을 그대로 재사용해 전체 6-Agent 파이프라인을
  실행한 뒤, `context_manager.find_snapshots(<Documentation 실행
  결과>)`로 요약이 실제로 검색되고 `restore_snapshot()`으로 복원된
  내용에 `summary` 키가 정확히 포함됨을 확인한다. 새 테스트 픽스처를
  만들지 않고 기존 것을 재사용(YAGNI).
- 완료 조건(DoD): 파이프라인 실행 후 요약이 검색 가능(`find_snapshots`),
  복원 가능(`restore_snapshot`)함이 통합 테스트로 증명. 기존 파이프라인
  테스트 전부 회귀 없음. `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — 신규 테스트 1개 추가. `MockEngineAdapter`
  가 `f"{task.task_id} 완료(Mock)"`을 반환하므로 이를 예상 요약값으로
  삼아 검색·복원을 함께 검증. `pytest` 425개(M7-T02 종료 시점 424개 +
  신규 1개) 전부 통과, `ruff check src tests`/`mypy src` 클린. M6의
  다중 Adapter 통합 테스트(`test_m6_policy_routing.py`)는 건드리지
  않았다 — M7 DoD가 요구하는 검증은 기존 파이프라인 헬퍼만으로 충분히
  증명되어 두 Milestone의 테스트 파일 경계를 그대로 유지했다.
- 의존성: M7-T01, M7-T02

#### M7-T04: Milestone 7 Review
- 목적: Approval Required 원칙에 따라 Milestone 7 산출물을 검토받는다.
- 작업 내용: DoD 체크리스트, Architecture Review, Interface First 검토,
  테스트 결과 문서화, Technical Debt 정리, 문서 갱신, Milestone 종료
  선언.
- 완료 조건(DoD): 위 항목 모두 완료 + 사용자 승인.
- 상태: **DONE (2026-07-26 사용자 승인 — Milestone 7 완료)**

---

## Milestone 7 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `DocumentationAgent`가 `engine_runtime.run()` 결과를 캡처해 `create_snapshot(session, summary=...)`로 전달 | ✅ (M7-T02) |
| 2 | `ContextManager.create_snapshot()`이 선택적 `summary` 파라미터를 받고 기존 무인자 호출과 하위 호환 | ✅ (M7-T01) |
| 3 | 저장된 요약을 `restore_snapshot()`/`assemble_context()`로 조회, `find_snapshots(query)`로 검색 가능 | ✅ (M7-T03) |
| 4 | `MemoryEngine` 인터페이스 변경 없음 | ✅ (아래 3절) |
| 5 | 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린 | ✅ (아래 4절) |
| 6 | Adapter 통합/CLI 실제 재검증/Model·Effort 라우팅/소규모 이월 부채는 범위 밖 유지 | ✅ (아래 5절) |

Task List(M7-T01~T03) 전체 완료. M7-T04(본 Review)로 Milestone을 마감한다.

**2. Architecture Review**

M7에서 실제로 바뀐 구조는 정확히 2곳, 둘 다 사전 Architecture Review가
예고한 최소 변경 그대로였다:
- **`ContextManager`(M7-T01)**: `create_snapshot()`에 `summary: str |
  None = None` 파라미터만 추가했다. `MemoryEngine`은 여전히 문자열
  저장/검색만 알 뿐 "요약"이라는 개념 자체를 전혀 모른다(ADR-0017 경계
  그대로) — summary는 `assemble_context()`가 만든 dict에 `"summary"`
  키로 병합된 뒤 기존과 동일한 `MemoryEngine.remember()` 경로로 저장될
  뿐이다.
- **`DocumentationAgent`(M7-T02)**: `engine_runtime.run()`의 반환값을
  `result` 변수로 캡처해(이전에는 완전히 버려짐) `create_snapshot(...,
  summary=result.output)`로 전달하는 2줄 변경. **신규 LLM 호출을 전혀
  추가하지 않았다** — 이미 하던 호출의 결과를 재활용했을 뿐이다.

`git diff --stat`(M6 종료 커밋 `464f0f5` 대비)로 확인한 결과 **소스
파일 3개만 수정**(`interfaces/context_manager.py`,
`memory/context_manager.py`, `agents/documentation_agent.py`), 28줄
순증가/9줄 삭제 — M6(5개 파일, 72줄)보다도 더 작은 변경 폭으로 목표를
달성했다. `docs/ARCHITECTURE.md` §3.8은 두 Task 완료 시점마다 즉시
갱신되어 구현과 문서 사이 괴리가 없다.

**3. Interface First 원칙 검토**

**M7은 새 최상위 Interface를 0개 추가했다**(M2/M3/M4/M6와 동일 패턴,
M5만 예외). `MemoryEngine` 계약은 메서드 하나도 바뀌지 않았다.
`ContextManager.create_snapshot()`은 새 메서드가 아니라 **기존 메서드에
기본값 있는 선택적 파라미터를 추가**한 것으로, 기존 모든 호출부
(`test_pipeline.py` 등 무인자 호출)가 코드 변경 없이 그대로 동작한다.
이는 ADR-0017이 "Context Manager는 Context 조립과 Snapshot 생명주기를,
Memory Engine은 저장/검색만"이라고 그은 경계가 "요약"이라는 새로운
요구사항 앞에서도 흔들리지 않고 정확히 들어맞았음을 보여준다 — 요약을
"만드는" 책임(LLM 호출)은 애초부터 Agent 계층에만 있었고, Context
Manager/Memory Engine은 그 결과를 받아 저장하기만 하면 됐다.

**4. 테스트 결과**

- `pytest`: **425개 전부 통과**(M6 완료 시점 416개 → M7에서 9개 신규:
  M7-T01 +6, M7-T02 +2, M7-T03 +1)
- `ruff check src tests`: 클린
- `mypy src`: 클린(82개 소스 파일)
- M6 완료 커밋(`464f0f5`) 대비 소스 3개 파일 수정(신규 소스 파일 0개),
  테스트 5개 파일 수정(`fakes.py`, `test_context_manager.py`×2,
  `test_documentation_agent.py`, `test_pipeline.py`)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M7에서 의도적으로 범위를 좁힌 것*
- **실패해도 요약을 그대로 저장**: `result.success=False`여도 `output`
  (에러 메시지일 수 있음)을 그대로 summary로 저장한다 — 사전
  Architecture Review에서 이미 승인된 단순화. 실패 시 별도 처리(필터링,
  재시도)는 필요성이 증명되지 않아 만들지 않았다.
- **누적 압축("요약의 요약") 없음**: 매 Snapshot마다 그 시점의 최신
  요약 하나만 저장한다. 여러 Mission에 걸친 히스토리를 압축하는 것은
  YAGNI로 배제.
- **`WorkspaceSession.memory_snapshot_id`가 자동으로 갱신되지 않음**
  (이번에 새로 드러난 사실, M1부터 있었던 기존 상태): `create_snapshot()`
  이 반환하는 `snapshot_id`를 세션에 다시 기록하는 코드가 어디에도
  없다 — `DocumentationAgent`도 이번에 반환값을 요약 용도로만 캡처했을
  뿐, 세션에 되먹임하지는 않는다. 그 결과 PRD 7.4가 요구하는 "검색"은
  `find_snapshots(query)`로 완전히 동작하지만, "새 세션이 이전 세션의
  요약을 **자동으로** 이어받는" 시나리오는 아직 수동(직접 검색 또는
  `memory_snapshot_id`를 명시적으로 지정)으로만 가능하다. Milestone
  DoD는 검색/복원 가능성만 요구했으므로 이번 범위의 미완료는 아니지만,
  **M8+에서 "세션 연속성" 논의 대상으로 투명하게 기록**한다.

*사용자가 명시적으로 이번 범위에서 제외한 것(계속 이월)*
- Model/Effort 수준 라우팅(M6 Review에서 이월, 여전히 미착수)
- Adapter 계열 통합(`ClaudeCodeEngineAdapter`↔`CLIEngineAdapter`),
  Codex/Gemini CLI 실제 바이너리 재검증
- `run_parallel` 개별 Task 재시도 미지원(M4-T06), `MemoryEngine.search()`
  선형 스캔(M4-T08), Retry Backoff/Persistent Runtime Recovery/Approval
  비동기 처리/Process Timeout 정책 고도화(M3-T08), `ShellAgent`
  화이트리스트가 코드에 고정(M5-T04)
- 온디맨드(사용자/CLI 요청) 요약 트리거(이번에 사용자가 명시적으로
  제외, 파이프라인 종료 시점만 구현)

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M7-T01~T03 상세 섹션) / `docs/ROADMAP.md`(M7
Task List 완료 표시) / `docs/ARCHITECTURE.md`(§3.8 각 Task 완료 시점마다
이미 갱신됨) 완료. `pyproject.toml` 버전은 v0.5.0 그대로 유지한다(구조적
기준선은 그대로, M7도 그 위에 기능을 얹은 것). `.ai/MEMORY.md`는 이
Review 승인 직후 M1~M6와 동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 소스 3개
파일 수정·신규 파일 0개로 M6보다도 더 작은 변경 폭 정량 확인), Interface
First 검토 완료(3절, 새 Interface 0개), 테스트 결과 문서화 완료(4절),
Technical Debt 정리 완료(5절, `WorkspaceSession.memory_snapshot_id`
자동 갱신 미비를 M8+ 논의 대상으로 투명하게 명시), 문서 갱신 완료(6절)
— 6개 조건 모두 만족. Review 중 코드 변경이 필요한 치명적 문제(버그·계약
위반)는 발견되지 않았다.

**2026-07-26 사용자 승인으로 Milestone 7 Completed 확정.**

**Milestone 8 상태**: 아직 목표/DoD/Task List가 전혀 정의되지 않았다.
이번 Review에서 드러난 두 후보는 (1) M6 Review가 이월한 "Model/Effort
수준 라우팅", (2) 이번에 드러난 "세션 연속성"(`memory_snapshot_id`
자동 갱신)이지만, 이는 사전 논의 없이 확정된 것이 아니며 Milestone 8은
착수 시점에 이 문서에 목표/DoD/Task List를 새로 정의한다(Task Driven
Development 원칙, M2~M7이 그래왔듯).

---

## Milestone 8 — 세션 연속성 (Session Continuity)

**목표**: M7 Review에서 새로 드러난 갭을 해소한다 — `WorkspaceSession.
memory_snapshot_id`가 자동으로 갱신되지 않아, PRD 7.4("새 세션/새 엔진
호출 시 관련 메모리를 불러와 컨텍스트로 제공")가 요구하는 "자동 이어받기"
가 아직 수동(직접 검색/명시적 지정)으로만 가능하다. M8은 이를 완성한다.

**Analysis 요약(Repository-Analysis 결과)**:
- `WorkspaceCore.update_session()`은 이미 `memory_snapshot_id`를 갱신하는
  파라미터를 갖고 있지만(T1-22부터 존재), 파이프라인의 어떤 Agent도 이를
  호출하지 않는다 — `DocumentationAgent`는 `create_snapshot()`의 반환값
  (snapshot_id)을 여전히 버린다.
- `MemoryEngine.search()`/`ContextManager.find_snapshots()`(M4-T08)는
  "일치하는 모든 snapshot_id"를 반환할 뿐 **정렬 순서를 계약하지 않는다**
  (`interfaces/memory_engine.py` 계약 문서에 명시) — "가장 최근 것"을
  안정적으로 찾으려면 별도의 "project별 최신 snapshot 포인터"가 필요하다.
- **아키텍처 상 중요한 발견**: `docs/ARCHITECTURE.md` §8 규칙 7("Memory
  접근은 Agent → Context Manager → Memory Engine 순서로만")에 따라
  **Workspace Core는 Context Manager에 의존할 수 없다** — `WorkspaceCore.
  start_session()`이 새 세션 생성 시 자동으로 `memory_snapshot_id`를
  채우게 하려면 이 규칙을 어겨야 한다. 대신 **Agent 계층(Rule 5: Agent →
  Context Manager)에서 해결**하면 기존 의존성 규칙을 전혀 건드리지 않고도
  같은 효과를 낼 수 있다 — `PlanningAgent`(파이프라인 진입점)가 Mission
  시작 시 `context_manager`를 통해 최신 snapshot을 복원하면 된다.

**Task List**(2026-07-26 확정, 상세 스펙은 각 Task 착수 시점에 이 문서에 추가)

| Task | 내용 | 근거/출처 |
|---|---|---|
| M8-T01 | `ContextManager`에 `latest_snapshot_id(project_id)` 신규 메서드 추가(계약+구현) — project별 최신 snapshot 포인터 — **완료** | M7 Review 이월 갭 |
| M8-T02 | `DocumentationAgent`가 Mission 종료 시 `workspace_session.memory_snapshot_id`를 새 snapshot_id로 갱신 — **완료** | Milestone DoD |
| M8-T03 | `PlanningAgent`가 Mission 시작 시 `memory_snapshot_id`가 없으면 `latest_snapshot_id(project_id)`로 자동 복원 — **완료** | Milestone DoD |
| M8-T04 | End-to-End 검증(같은 세션 내 연속 Mission + 새 세션에서도 이전 요약을 자동으로 이어받음을 증명) — **완료** | Milestone DoD |
| M8-T05 | Milestone 8 Review | 관례 |

**Architecture Review(사전 검토, 착수 전)**:
- **컴포넌트 경계**: `ContextManager`(§3.8)에 메서드 1개 추가(새 Interface
  아님). `PlanningAgent`/`DocumentationAgent`(§3.6) 내부 변경. `WorkspaceCore`
  (§3.3)·`MemoryEngine` 계약은 변경 없음.
  `PlanningAgent`가 `workspace_session`/`context_manager`를 신규
  생성자 의존성으로 받는다(§8 Rule 5 "Agent는 Context Manager에
  의존"이 이미 허용) — 지금까지 Planning/Coding/Review 3개 Agent는
  Session/ContextManager를 몰랐고 `DocumentationAgent`만 알고 있었는데,
  이번에 `PlanningAgent`도 알게 된다.
- **의존성 방향(DIP)**: `WorkspaceCore`는 여전히 Context Manager를
  전혀 모른다(§8 Rule 3·7 무변경, ADR 추가 불필요) — "세션 연속성"을
  Workspace Core가 아니라 Agent 계층(Rule 5)에서 해결하는 설계 선택이
  핵심이다.
- **SRP 점검**: `PlanningAgent`에 "이어받기" 책임이 추가되는 것이 단일
  책임 원칙에 어긋나는지 검토했다 — Mission을 시작하기 전에 이전
  컨텍스트를 복원하는 것은 "Mission 계획"이라는 책임의 자연스러운
  선행 조건이며, 이를 위해 별도 Agent(예: SessionContinuityAgent)를
  새로 만드는 것은 지금 필요성이 증명되지 않은 과잉 설계(YAGNI 위반)로
  판단해 배제한다.
- **Interface First**: `ContextManager`에 메서드 1개 추가(M4-T08의
  `search`/`find_snapshots` 추가, M5-T06의 `record_step`/`get_steps`
  추가와 같은 패턴 — 필요성이 실제로 증명된 뒤 계약에 추가). `MemoryEngine`
  인터페이스는 기존 `remember`/`recall`만으로 충분해 변경하지 않는다
  (project별 포인터는 `ContextManager`가 내부적으로 `remember(f"...
  {project_id}", snapshot_id)` 패턴으로 구현 — 이미 쓰던 방식 재사용).
- **YAGNI 점검**: 여러 세션이 동시에 같은 project_id로 경쟁하는 상황의
  동시성 안전은 다루지 않는다(현재 시스템에 검증된 동시 다중 세션
  시나리오가 없음, 순차 실행 가정 유지) — 명시적 "세션 리셋" 옵션(항상
  이어받지 않고 사용자가 새로 시작하고 싶은 경우)도 필요성이 증명되지
  않아 만들지 않는다.
- **리스크**: (1) 동시성 경쟁 조건은 명시적으로 범위 밖(위 YAGNI 참고).
  (2) 지금은 Mission이 시작될 때마다 항상 최신 요약을 이어받는데, 이
  동작이 항상 바람직한지(예: 완전히 새로운 작업을 시작하고 싶은 경우)는
  검증되지 않았다 — 다음 Milestone에서 필요성이 드러나면 재검토.

**Definition of Done**
1. `ContextManager.latest_snapshot_id(project_id)`가 그 project_id로
   가장 최근에 생성된 snapshot_id를 반환(없으면 `None`)한다.
2. `DocumentationAgent`가 매 Mission 종료 시 `workspace_session.
   memory_snapshot_id`를 새로 생성된 snapshot_id로 갱신한다.
3. `PlanningAgent`가 `plan_mission()` 호출 시 `workspace_session.
   memory_snapshot_id`가 비어 있으면 `latest_snapshot_id(project_id)`로
   자동 복원한 뒤 Mission을 시작한다.
4. 같은 세션에서 두 번째 Mission을 실행하면 첫 번째 Mission이 만든
   요약이 `assemble_context()`에 자동으로 포함됨이 통합 테스트로
   증명된다. 별도의 새 `WorkspaceSession`(같은 project_id,
   `memory_snapshot_id=None`)으로도 이전 요약을 자동으로 이어받음이
   증명된다("세션 연속성"의 핵심).
5. `WorkspaceCore`/`MemoryEngine` 인터페이스는 변경되지 않는다(§8
   의존성 규칙 3·7 유지, ADR 추가 불필요).
6. 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린.
7. 동시성 경쟁 조건 안전, 명시적 세션 리셋 옵션, Model/Effort 수준
   라우팅, Adapter 계열 통합 등은 이번 Milestone 범위 밖으로 유지된다.

**상태**: 목표/Task List/사전 Architecture Review/DoD 확정(2026-07-26
사용자 확정). M8-T01~T04 완료, 다음 Task는 M8-T05(Milestone Review).

#### M8-T01: `ContextManager.latest_snapshot_id(project_id)` 신규 메서드
- 목적: "project별 최신 snapshot"을 안정적으로 찾을 수 있는 계약을
  마련한다 — `find_snapshots()`는 정렬 순서를 계약하지 않아 "최신"
  판정에 쓸 수 없다.
- 작업 내용: `interfaces/context_manager.py`에 `latest_snapshot_id(project_id:
  str) -> str | None` 추가(계약 docstring). `memory/context_manager.py`의
  `InMemoryContextManager`에 `_latest_snapshot_by_project: dict[str, str]`
  신규 — `create_snapshot()`이 `session.current_project_id`가 있으면
  호출마다 갱신. **이 포인터는 `MemoryEngine`을 거치지 않고 Context
  Manager 내부에서만 관리**(설계 근거: `MemoryEngine.search()`는 값의
  substring 일치라 포인터까지 저장하면 검색 결과 오염 위험). `tests/
  interfaces/fakes.py`의 `FakeContextManager`도 동일하게 갱신.
- 완료 조건(DoD): 같은 project_id로 여러 Snapshot을 만들면 가장 최근
  것만 반환, project_id가 다르면 서로 독립적으로 추적, `current_project_id`
  가 없는 세션은 포인터가 등록되지 않음, 포인터가 `find_snapshots()`
  결과를 오염시키지 않음. `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — 계약 테스트(`tests/interfaces/
  test_context_manager.py`) 4개 + 단위 테스트(`tests/memory/
  test_context_manager.py`) 4개 신규(없음/최신 판정/project별 독립/
  검색 오염 없음 확인). `tests/agents/test_documentation_agent.py`의
  `SpyContextManager`도 위임 메서드 추가(추상 클래스 인스턴스화 유지).
  `docs/ARCHITECTURE.md` §3.8에 반영. `pytest` 433개(M7 종료 시점 425개
  + 신규 8개) 전부 통과, `ruff check src tests`/`mypy src` 클린. Agent가
  실제로 이 메서드를 호출해 세션을 갱신/복원하는 것은 M8-T02/T03 범위.
- 의존성: 없음(M8 Task List 첫 Task)

#### M8-T02: `DocumentationAgent`가 Mission 종료 시 세션에 최신 snapshot_id 기록
- 목적: `create_snapshot()`이 반환하는 snapshot_id를 실제로 세션에
  되먹여 같은 세션 안에서 이어지는 Mission이 자동으로 최신 Snapshot을
  참조하게 한다 — "세션 연속성"의 쓰기 측.
- 작업 내용: `_on_review_completed()`에서 `create_snapshot()`의 반환값을
  `snapshot_id` 변수로 캡처(이전에는 완전히 버려짐), `self._workspace_session
  .memory_snapshot_id = snapshot_id`로 대입하는 2줄 변경.
- 완료 조건(DoD): Mission이 끝나면 `workspace_session.memory_snapshot_id`
  가 새 snapshot_id로 갱신됨, 연속된 두 번째 Mission이 끝나면 최신 것
  하나로 덮어써짐(누적 아님). `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — `tests/agents/test_documentation_agent.py`
  의 `build_documentation_agent()`가 `workspace_session`도 반환하도록
  확장(기존 5개 호출부 갱신). 신규 테스트 2개:
  `test_documentation_agent_writes_new_snapshot_id_back_to_session`
  (세션에 실제로 기록됨 + `restore_snapshot()`으로 그 내용 확인),
  `test_documentation_agent_second_mission_overwrites_session_snapshot_id`
  (두 번째 Mission이 끝나면 다른 snapshot_id로 덮어써짐). `pytest`
  435개(M8-T01 종료 시점 433개 + 신규 2개) 전부 통과, `ruff check src
  tests`/`mypy src` 클린. `PlanningAgent`가 이 값을 실제로 읽어 Mission
  시작 시 복원하는 것은 M8-T03 범위.
- 의존성: M8-T01

#### M8-T03: `PlanningAgent`가 Mission 시작 시 최신 snapshot 자동 복원
- 목적: "세션 연속성"의 읽기 측 — 새 세션(또는 처음부터 세션 중이던
  Mission)이 project의 최신 Memory Snapshot을 실제로 이어받게 한다.
- 작업 내용: `PlanningAgent`에 `context_manager: ContextManager`,
  `workspace_session: WorkspaceSession` 생성자 의존성 신규 추가.
  `plan_mission()` 시작 시 `workspace_session.memory_snapshot_id is None`
  이면 `context_manager.latest_snapshot_id(project_id)`로 채운다(이미
  값이 있으면 건드리지 않음). `PlanningAgent`를 생성하는 3개 호출부
  (`tests/agents/test_pipeline.py`, `tests/integration/
  test_m6_policy_routing.py`, `tests/integration/
  test_coding_agent_runtime_integration.py`) 모두 이미 `context_manager`/
  `workspace_session`을 갖고 있어 전달만 추가.
- 완료 조건(DoD): `memory_snapshot_id`가 비어 있는 세션은 자동 복원됨,
  이미 값이 있으면 덮어쓰지 않음, 대응하는 Snapshot이 없으면 `None`
  그대로 유지됨, 다른 project의 Snapshot을 잘못 이어받지 않음(project별
  독립). `pytest`/`ruff`/`mypy` 통과.
- 상태: **DONE (2026-07-26)** — `tests/agents/test_planning_agent.py`
  신규(`PlanningAgent` 최초 전용 단위 테스트 파일) 5개: 자동 복원됨,
  기존 값 덮어쓰지 않음, 이전 Snapshot 없으면 `None` 유지, 다른
  project는 이어받지 않음, 기존 `MissionPlanned` 발행 동작 회귀 없음.
  `docs/ARCHITECTURE.md` §3.6에 반영. `pytest` 440개(M8-T02 종료 시점
  435개 + 신규 5개) 전부 통과, `ruff check src tests`/`mypy src` 클린.
- 의존성: M8-T01, M8-T02

#### M8-T04: End-to-End 검증
- 목적: M8-T01(포인터)/M8-T02(쓰기)/M8-T03(읽기)가 실제 파이프라인
  안에서 맞물려 동작하는지 증명한다 — Milestone DoD 4번의 직접 검증
  대상.
- 작업 내용: `tests/agents/test_pipeline.py`의 `build_pipeline()`에
  `context_manager`/`session_id` 선택적 파라미터 추가(기존 호출부
  하위 호환) — 같은 `ContextManager`를 공유하는 두 번째 파이프라인/세션을
  조립할 수 있게 함. 신규 테스트 2개:
  `test_second_mission_in_same_session_sees_prior_summary_in_context`
  (같은 세션의 연속 Mission이 이전 요약을 자동으로 이어받음, DoD 4번의
  첫 번째 절), `test_new_session_inherits_previous_session_summary_via_planning_agent`
  (완전히 새로운 `WorkspaceSession`이 실제 `InMemoryContextManager`/
  `InMemoryMemoryEngine`을 통해 이전 세션의 요약을 자동으로 이어받음,
  DoD 4번의 두 번째 절 — "세션 연속성"의 핵심 시나리오). 두 번째
  테스트는 새 세션에 `DocumentationAgent`를 일부러 연결하지 않았다 —
  연결하면 그 세션의 새 Mission이 끝나자마자 자신의 새 요약으로 즉시
  덮어써(M8-T02, "누적이 아니라 최신 하나만 유지") 이어받은 상태를
  관찰할 수 없기 때문이다(그 "덮어쓰기" 자체는 M8-T02의 별도 단위
  테스트가 이미 검증).
- 완료 조건(DoD): 같은 세션의 연속 Mission이 이전 요약을 자동으로
  이어받음, 완전히 새로운 세션도 실제 구현체를 통해 이전 세션의 요약을
  자동으로 이어받음(project별 독립성 유지). `pytest`/`ruff`/`mypy`
  통과.
- 상태: **DONE (2026-07-26)** — 신규 테스트 2개 추가. `pytest` 442개
  (M8-T03 종료 시점 440개 + 신규 2개) 전부 통과, `ruff check src
  tests`/`mypy src` 클린. Fake 기반 단위 테스트(M8-T01~T03)와 달리
  실제 프로덕션 구현체(`InMemoryContextManager`+`InMemoryMemoryEngine`)
  로 교차 세션 시나리오를 검증해 통합 수준의 신뢰도를 더했다.
- 의존성: M8-T01, M8-T02, M8-T03

#### M8-T05: Milestone 8 Review
- 목적: Approval Required 원칙에 따라 Milestone 8 산출물을 검토받는다.
- 작업 내용: DoD 체크리스트, Architecture Review, Interface First 검토,
  테스트 결과 문서화, Technical Debt 정리, 문서 갱신, Milestone 종료
  선언.
- 완료 조건(DoD): 위 항목 모두 완료 + 사용자 승인.
- 상태: 리뷰 작성 완료(2026-07-26) — **사용자 승인 대기**

---

## Milestone 8 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `ContextManager.latest_snapshot_id(project_id)`가 최근 생성된 snapshot_id 반환 | ✅ (M8-T01) |
| 2 | `DocumentationAgent`가 Mission 종료 시 세션에 최신 snapshot_id 기록 | ✅ (M8-T02) |
| 3 | `PlanningAgent`가 Mission 시작 시 비어 있으면 자동 복원 | ✅ (M8-T03) |
| 4 | 같은 세션 연속 Mission + 새 세션 모두 자동 이어받음이 통합 테스트로 증명 | ✅ (M8-T04) |
| 5 | `WorkspaceCore`/`MemoryEngine` 인터페이스 변경 없음 | ✅ (아래 3절) |
| 6 | 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린 | ✅ (아래 4절) |
| 7 | 동시성 경쟁 조건/세션 리셋 옵션/Model·Effort 라우팅/Adapter 통합은 범위 밖 유지 | ✅ (아래 5절) |

Task List(M8-T01~T04) 전체 완료. M8-T05(본 Review)로 Milestone을 마감한다.

**2. Architecture Review**

M8에서 실제로 바뀐 구조는 정확히 3곳:
- **`ContextManager`(M8-T01)**: `latest_snapshot_id(project_id)` 메서드
  1개 추가. 이 "최신" 포인터는 **`MemoryEngine`을 거치지 않고 Context
  Manager 내부에서만** 관리한다 — `MemoryEngine.search()`는 값의
  substring 일치라 포인터까지 저장하면 검색 결과가 오염될 위험이
  있었기 때문이다(`memory/context_manager.py` docstring에 근거 명시).
- **`DocumentationAgent`(M8-T02)**: `create_snapshot()`의 반환값을
  `workspace_session.memory_snapshot_id`에 되먹이는 2줄 변경(세션
  연속성의 쓰기 측).
- **`PlanningAgent`(M8-T03)**: `context_manager`/`workspace_session`을
  신규 생성자 의존성으로 받아, Mission 시작 시 `memory_snapshot_id`가
  비어 있으면 자동 복원(세션 연속성의 읽기 측).

**핵심 설계 결정이 그대로 지켜졌다**: `docs/ARCHITECTURE.md` §8 규칙
7("Memory 접근은 Agent → Context Manager → Memory Engine 순서로만")에
따라 **Workspace Core는 이번에도 전혀 건드리지 않았다** — "세션
연속성"을 Workspace Core가 아니라 Agent 계층(Rule 5)에서 해결한다는
사전 Architecture Review의 결정대로, `WorkspaceCore.start_session()`/
`update_session()`은 손대지 않고 `PlanningAgent`만 확장했다. ADR 추가나
의존성 규칙 변경이 전혀 필요 없었다.

`git diff --stat`(M7 종료 커밋 `aa7f243` 대비)로 확인한 결과 **소스
파일 4개만 수정**(`interfaces/context_manager.py`,
`memory/context_manager.py`, `agents/documentation_agent.py`,
`agents/planning_agent.py`), 69줄 순증가/5줄 삭제 — M6(5개 파일)와
비슷한 폭이며, `PlanningAgent`가 처음으로 `ContextManager`/
`WorkspaceSession`을 알게 된 것을 빼면 대부분 몇 줄짜리 변경이었다.
`docs/ARCHITECTURE.md` §3.6·§3.8은 각 Task 완료 시점마다 즉시 갱신되어
구현과 문서 사이 괴리가 없다.

**3. Interface First 원칙 검토**

**M8은 새 최상위 Interface를 0개 추가했다**(M2/M3/M4/M6/M7과 동일
패턴, M5만 예외). `WorkspaceCore`/`MemoryEngine` 계약은 메서드 하나도
바뀌지 않았다. `ContextManager`에 메서드 1개(`latest_snapshot_id`)가
추가됐지만 이는 M4-T08(`search`/`find_snapshots`)·M5-T06
(`record_step`/`get_steps`)·M7-T01(`create_snapshot`의 `summary`
파라미터)과 같은 패턴 — 필요성이 실제로 증명된 뒤 기존 계약에 추가한
것이다. `PlanningAgent`가 `ContextManager`에 의존하게 된 것은 새
Interface가 아니라 §8 규칙 5("Agent는 Context Manager에 의존")가
이미 허용해 둔 관계를 실제로 쓰기 시작한 것뿐이다.

**4. 테스트 결과**

- `pytest`: **442개 전부 통과**(M7 완료 시점 425개 → M8에서 17개 신규:
  M8-T01 +8, M8-T02 +2, M8-T03 +5, M8-T04 +2)
- `ruff check src tests`: 클린
- `mypy src`: 클린(82개 소스 파일)
- M7 완료 커밋(`aa7f243`) 대비 소스 4개 파일 수정(신규 소스 파일 0개),
  테스트 다수 파일 수정 + `tests/agents/test_planning_agent.py` 신규
  (`PlanningAgent` 최초 전용 단위 테스트 파일)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M8에서 의도적으로 범위를 좁힌 것(사전 Architecture Review에서 이미
확정)*
- **동시성 경쟁 조건 미해결**: 여러 세션이 동시에 같은 project_id로
  Mission을 병행 실행하면 `latest_snapshot_id`/`memory_snapshot_id`
  갱신에 경쟁 조건이 생길 수 있다 — 현재 시스템에 검증된 동시 다중
  세션 시나리오가 없어(순차 실행 가정) 이번 범위에서 다루지 않았다.
- **명시적 "세션 리셋" 옵션 없음**: Mission을 시작할 때마다 항상 최신
  요약을 이어받는다 — 사용자가 의도적으로 완전히 새로 시작하고 싶은
  경우를 구분할 방법이 없다. 필요성이 증명되면 다음에 재검토.
- **`PlanningAgent`의 책임 확장**: "Mission 계획"에 "세션 연속성 복원"
  이 더해졌다 — 사전 Architecture Review에서 별도 Agent 신설은 YAGNI
  위반으로 판단해 배제하고 진입점에 두기로 확정한 그대로다.

*계속 이월되는 기존 항목*
- Model/Effort 수준 라우팅(M6 Review 이월, 여전히 미착수)
- Adapter 계열 통합(`ClaudeCodeEngineAdapter`↔`CLIEngineAdapter`),
  Codex/Gemini CLI 실제 바이너리 재검증
- `run_parallel` 개별 Task 재시도 미지원(M4-T06), `MemoryEngine.search()`
  선형 스캔(M4-T08), Retry Backoff/Persistent Runtime Recovery/Approval
  비동기 처리/Process Timeout 정책 고도화(M3-T08), `ShellAgent`
  화이트리스트가 코드에 고정(M5-T04)

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M8-T01~T04 상세 섹션) / `docs/ROADMAP.md`(M8
Task List 완료 표시) / `docs/ARCHITECTURE.md`(§3.6·§3.8 각 Task 완료
시점마다 이미 갱신됨) 완료. `pyproject.toml` 버전은 v0.5.0 그대로
유지한다(구조적 기준선은 그대로, M8도 그 위에 기능을 얹은 것).
`.ai/MEMORY.md`는 이 Review 승인 직후 M1~M7과 동일한 방식으로 압축
반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 소스 4개
파일 수정·신규 파일 0개, Workspace Core 무변경 원칙 재확인), Interface
First 검토 완료(3절, 새 Interface 0개), 테스트 결과 문서화 완료(4절),
Technical Debt 정리 완료(5절, 동시성/세션 리셋 미해결을 투명하게
명시), 문서 갱신 완료(6절) — 6개 조건 모두 만족. Review 중 코드 변경이
필요한 치명적 문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 8 Completed를 선언한다.**

**Milestone 9 상태**: 아직 목표/DoD/Task List가 전혀 정의되지 않았다.
이번 Review에서 드러난 후보들은 (1) M6 Review가 이월한 "Model/Effort
수준 라우팅", (2) 이번에 드러난 동시성 경쟁 조건/세션 리셋 옵션, (3)
Adapter 계열 통합이지만, 이는 사전 논의 없이 확정된 것이 아니며
Milestone 9는 착수 시점에 이 문서에 목표/DoD/Task List를 새로 정의한다
(Task Driven Development 원칙, M2~M8이 그래왔듯).

---

## Milestone 9 — 세션 견고성 (Session Robustness)

**목표**: M8 Review가 명시적으로 범위 밖에 둔 두 갭 — 세션 리셋 옵션 없음,
동시 Project Session 경쟁 조건 — 을 해소한다. M8 Review가 제시한 3개 후보
(Model/Effort 라우팅, 세션 견고성, Adapter 계열 통합) 중 **세션 견고성**을
선택했다 — Interface 변경이 필요 없어 M9 하나로 완결 가능하고, 외부 CLI
바이너리 의존이 없다(2026-07-26 사용자 확정, 설계 검토 대화 참고).

**Task List**

| Task | 내용 | 근거/출처 |
|---|---|---|
| M9-T01 | 동시 Project Session 시나리오 조사(설계 검토) — **완료, 조치 불필요로 종결** | M8 Review 이월 갭 |
| M9-T02 | (M9-T01 결과에 따라 조건부) 동시성 경쟁 조건 해소 — **스킵(M9-T01에서 불필요 확인)** | M8 Review 이월 갭 |
| M9-T03 | `PlanningAgent` 세션 리셋 옵션(`reset=True`) — **완료** | M8 Review 이월 갭 |
| M9-T04 | End-to-End 검증 — **완료** | Milestone DoD |
| M9-T05 | Milestone 9 Review — 본 절 | 관례 |

**진행 상태**: M9-T01(조사, 불필요로 종결)~M9-T04(검증) 완료. M9-T05(본
Review)로 Milestone을 마감한다.

#### M9-T01: 동시 Project Session 시나리오 조사
- 목적: `InMemoryContextManager._latest_snapshot_by_project`가 락 없는
  plain dict인 것이 실제로 문제가 되는 지원 시나리오가 있는지 확인한다.
  없다면 락을 추가하는 것 자체가 존재하지 않는 문제를 위한 과설계
  (YAGNI 위반)다.
- 작업 내용: `WorkspaceCore`/CLI/Agent 파이프라인 전체에서 같은
  `project_id`로 두 Mission이 실제로 동시 실행될 수 있는 경로가 있는지
  추적.
- 조사 결과(**조치 불필요로 종결**, M2 Event ID 부채 처리와 동일 패턴):
  1. `cli/main.py`에는 Mission을 시작하는 명령이 아예 없다
     (`project create/show/list`뿐) — `PlanningAgent.plan_mission()`은
     현재 테스트 코드에서만 호출된다.
  2. `InMemoryEventBus.publish()`(`events/event_bus.py`)는 완전히
     동기(synchronous)다 — 구독자를 같은 스레드에서 순차 호출한다.
     Planning→Coding→Shell→Coordinator→Review→Documentation 전체
     체인이 한 스레드의 한 호출 스택 안에서 끝난다.
  3. 저장소 전체에서 유일한 스레딩은 `ManagedEngineRuntime`의 per-Task
     timeout 스레드와 `run_parallel()`의 `ThreadPoolExecutor`(M4-T06)뿐이며,
     둘 다 `EngineAdapter`/`Task` 실행 층위에서만 동작하고
     `ContextManager`/`WorkspaceSession`은 전혀 건드리지 않는다.
  4. 따라서 `InMemoryContextManager._latest_snapshot_by_project`에
     두 스레드가 동시에 쓰는 경로가 현재 코드베이스에 **존재하지
     않는다** — "동시 Project Session 경쟁 조건"은 아직 시스템이
     지원하지 않는 시나리오(동시 Mission 실행 자체가 진입점이 없음)에
     대한 이론적 우려였다.
- 결론: 코드 변경 없이 이 갭을 조사 완료로 종결한다. 향후 동시 Mission
  실행 진입점(예: 병렬 CLI 호출, 웹 API)이 실제로 추가되는 시점에
  재검토한다.
- 상태: **DONE (2026-07-26)**

#### M9-T02: 동시성 경쟁 조건 해소
- M9-T01 조사 결과 실제 재현 경로가 없어 **스킵**한다. Technical Debt로
  남기지 않는다 — "문제가 없음"이 조사의 정당한 결론이다.
- 상태: **SKIPPED (M9-T01 결과에 따름)**

#### M9-T03: `PlanningAgent` 세션 리셋 옵션
- 목적: 사용자가 이전 세션 요약을 이어받지 않고 완전히 새로 시작할 수
  있게 한다(M8 Review §5 "명시적 세션 리셋 옵션 없음").
- 작업 내용: `plan_mission()`에 `reset: bool = False` 키워드 전용
  파라미터 추가. `reset=True`면 M8-T03의 자동 복원(`memory_snapshot_id`가
  비어 있을 때 `latest_snapshot_id()`로 채우는 로직)을 건너뛴다. 기본값
  `False`로 기존 M8 동작과 완전히 하위 호환. 같은 세션에 이미 있는
  `memory_snapshot_id`(이어지는 Mission)는 건드리지 않는다 — 이번 갭과
  다른 문제라 범위에 포함하지 않는다(범위를 좁게 유지, YAGNI).
- 완료 조건(DoD): `reset=True` → 새 세션이 이전 프로젝트 요약을 이어받지
  않음, `reset=False`(기본) → 기존 M8 동작 그대로, 기존 + 신규 테스트
  전부 통과.
- 상태: **DONE (2026-07-26)** — `agents/planning_agent.py` 3줄 변경
  (파라미터 추가 + 가드 조건에 `not reset` 추가). 새 Interface/기존
  Interface 변경 없음(`PlanningAgent`는 구체 클래스). CLI에 `--reset`
  플래그로 노출하는 것은 이번 범위에서 제외했다 — 현재 CLI가 Mission
  시작 자체를 노출하지 않아(M4-T02 범위), Agent 계층 기능부터 갖추고
  CLI 노출은 실제 필요성이 확인되면 별도로 다룬다(YAGNI, 사용자 승인).
  `tests/agents/test_planning_agent.py`에 2개 신규 테스트
  (`test_plan_mission_with_reset_skips_snapshot_restoration`,
  `test_plan_mission_reset_does_not_clear_existing_snapshot_id` — 범위
  경계를 명시적으로 검증).

#### M9-T04: End-to-End 검증
- 목적: 리셋 옵션이 전체 파이프라인에서도 올바르게 동작함을 증명한다
  (M6~M8과 동일 패턴).
- 작업 내용: `tests/agents/test_pipeline.py`에
  `test_reset_mission_does_not_inherit_previous_session_summary` 추가 —
  첫 세션이 요약을 만든 뒤, 완전히 새로운 `WorkspaceSession`이
  `reset=True`로 Mission을 시작하면 그 요약을 이어받지 않음을
  `test_new_session_inherits_previous_session_summary_via_planning_agent`
  (reset 없음, 자동 복원됨)와 대비해 검증.
- 완료 조건(DoD): 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린.
- 상태: **DONE (2026-07-26)** — `pytest`: **445개 전부 통과**(M8 완료
  시점 442개 → M9에서 3개 신규: M9-T03 +2, M9-T04 +1). `ruff check src
  tests`: 클린. `mypy src`: 클린(82개 소스 파일, 신규 소스 파일 0개).

---

## Milestone 9 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | 동시 Project Session 시나리오가 실제 재현 가능한지 조사·결론 | ✅ (M9-T01, 조치 불필요로 종결) |
| 2 | `PlanningAgent.plan_mission(reset=True)`가 새 세션의 자동 복원을 건너뜀 | ✅ (M9-T03) |
| 3 | `reset=False`(기본값)는 기존 M8 동작과 완전히 하위 호환 | ✅ (M9-T03) |
| 4 | End-to-End로 리셋 시나리오가 전체 파이프라인에서 검증됨 | ✅ (M9-T04) |
| 5 | `WorkspaceCore`/`ContextManager`/`MemoryEngine` 인터페이스 변경 없음 | ✅ (아래 3절) |
| 6 | 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린 | ✅ (아래 4절) |

Task List(M9-T01·T03·T04) 완료, M9-T02는 M9-T01 조사 결과에 따라
스킵했다. M9-T05(본 Review)로 Milestone을 마감한다.

**2. Architecture Review**

M9에서 실제로 바뀐 구조는 **`PlanningAgent` 1곳뿐**이다 — `plan_mission()`
시그니처에 키워드 전용 `reset: bool = False`를 추가하고 자동 복원 가드에
`not reset` 조건을 더한 것이 전부다(`agents/planning_agent.py`). M8-T03이
확정한 "세션 연속성은 Workspace Core가 아니라 Agent 계층(PlanningAgent)
에서 해결한다"는 결정을 그대로 따랐다 — `WorkspaceCore.start_session()`
은 이번에도 손대지 않았다. `ContextManager`/`MemoryEngine`도 무변경이다.

M9-T01(조사)은 코드 변경이 없는 설계 검토 Task였다 — 조사 결과 "동시
Mission 실행" 자체가 현재 시스템에 진입점이 없는(CLI에 Mission 시작
명령 없음, `InMemoryEventBus.publish()`가 완전 동기) 시나리오임을
확인하고, 존재하지 않는 문제를 위한 락 도입을 하지 않기로 한 것이
M9-T01의 "구현"이다. 이는 §4.2 Simplicity First의 "실제 문제를
해결하는가?" 자문 질문을 그대로 적용한 사례다.

`git diff --stat`(M8 종료 커밋 대비)로 확인한 결과 **소스 파일 1개만
수정**(`agents/planning_agent.py`, 문서 제외), 신규 소스 파일 0개 —
M6(5개)·M8(4개)보다도 좁은 범위였다. `docs/ARCHITECTURE.md` §3.6은
M9-T03 완료 시점에 즉시 갱신되어 구현과 문서 사이 괴리가 없다.

**3. Interface First 원칙 검토**

**M9는 새 최상위 Interface를 0개 추가했다**(M2/M3/M4/M6/M7/M8과 동일
패턴, M5만 예외). `PlanningAgent.plan_mission()`은 Interface 메서드가
아니라 구체 클래스의 공개 메서드이므로, 키워드 전용 파라미터를 기본값과
함께 추가하는 것은 기존 호출자(`plan_mission("p1", "제목")` 형태)를 전혀
깨지 않는다 — 이번 변경은 Interface 계약과 무관하다.

**4. 테스트 결과**

- `pytest`: **445개 전부 통과**(M8 완료 시점 442개 → M9에서 3개 신규)
- `ruff check src tests`: 클린
- `mypy src`: 클린(82개 소스 파일)
- M8 완료 커밋 대비 소스 1개 파일 수정(신규 소스 파일 0개), 테스트
  2개 파일 수정(신규 테스트 파일 0개)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M9에서 조사 후 "조치 불필요"로 종결한 것*
- 동시 Project Session 경쟁 조건 — M9-T01 참고. 향후 동시 Mission 실행
  진입점이 실제로 추가되면 재검토.

*M9에서 의도적으로 범위를 좁힌 것*
- CLI `--reset` 플래그 미노출 — 현재 CLI가 Mission 시작 자체를 노출하지
  않아 Agent 계층 기능만 갖춤(M9-T03 참고). CLI에서 Mission을 시작하는
  기능이 생기는 시점에 함께 재검토.

*계속 이월되는 기존 항목*
- Model/Effort 수준 라우팅(M6 Review 이월, 여전히 미착수)
- Adapter 계열 통합(`ClaudeCodeEngineAdapter`↔`CLIEngineAdapter`),
  Codex/Gemini CLI 실제 바이너리 재검증
- `run_parallel` 개별 Task 재시도 미지원(M4-T06), `MemoryEngine.search()`
  선형 스캔(M4-T08), Retry Backoff/Persistent Runtime Recovery/Approval
  비동기 처리/Process Timeout 정책 고도화(M3-T08), `ShellAgent`
  화이트리스트가 코드에 고정(M5-T04)

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M9-T01~T04 상세 섹션) / `docs/ROADMAP.md`(M9
Task List·Milestone 개요 반영) / `docs/ARCHITECTURE.md`(§3.6 M9-T03
완료 시점에 이미 갱신됨) 완료. `pyproject.toml` 버전은 v0.5.0 그대로
유지한다(구조적 기준선은 그대로, M9도 그 위에 좁은 기능 하나를 얹은
것). `.ai/MEMORY.md`는 이 Review 승인 직후 M1~M8과 동일한 방식으로
압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 소스 1개
파일 수정·신규 파일 0개, Workspace Core/ContextManager 무변경 원칙
재확인), Interface First 검토 완료(3절, 새 Interface 0개), 테스트 결과
문서화 완료(4절), Technical Debt 정리 완료(5절, 동시성 조사 결론을
투명하게 명시), 문서 갱신 완료(6절) — 6개 조건 모두 만족. Review 중
코드 변경이 필요한 치명적 문제(버그·계약 위반)는 발견되지 않았다.

**2026-07-26 사용자 승인으로 Milestone 9 Completed 확정.**

---

## Milestone 10 — 실행 복원력 (Execution Resilience)

**목표**: `run_parallel()`이 개별 Task 예외로 배치 전체 결과를 잃지 않게
하고, 실패한 Task만 재시도되도록 한다. M10 착수 전 사용자가 제시한 5개
Technical Debt 후보(Model/Effort 라우팅, Adapter 계열 통합, Codex/Gemini
CLI 실환경 검증, Memory Summary 최적화, run_parallel 개별 재시도/복원력)
를 PRD·코드와 대조 재분석한 결과: Codex/Gemini 실환경 검증은 이 세션
환경에 CLI 바이너리 자체가 없어 실행 불가, Adapter 통합은 기능 이득
없는 순수 리팩토링, Memory 최적화는 PRD §11이 이미 "필요해지면"으로
유보해 둔 항목 — 이 세 후보를 제외하고 **외부 의존이 없고 확인된 실제
버그가 있는 실행 복원력**을 M10으로 선택했다(2026-07-26 사용자 확정).

코드 조사 결과 `ManagedEngineRuntime.run_parallel()`이
`[future.result() for future in futures]` 리스트 컴프리헨션을 써서, Task
하나가 예외를 던지면 **이미 완료된 다른 Task의 결과까지 전부 유실**되는
버그를 확인했다 — M4 Review가 "개별 재시도 미지원"이라 기록한 것보다
심각한 문제였다. `RecoveringEngineRuntime.run_parallel()`은 내부
Runtime에 그대로 위임해 재시도가 전무했다.

**Milestone Definition of Done**
1. `EngineRuntime.run_parallel()` 계약에 개별 Task 실패 격리를 명시한다
   (반환 길이=입력 길이, 순서 보존, 개별 예외→`EngineResult(success=False)`
   변환, 개별 실패만으로는 `run_parallel()`이 예외를 던지지 않음).
   `NoSuitableEngineError`(Runtime 자체의 치명적 오류)는 이 격리 대상이
   아니라 여전히 즉시 전파된다.
2. `ManagedEngineRuntime.run_parallel()`이 위 계약을 실제로 만족한다
   (확인된 버그 수정).
3. `RecoveringEngineRuntime.run_parallel()`이 첫 병렬 패스 후 실패한
   Task만 기존 `self.run()`의 `RetryPolicy` 루프로 재시도한다.
4. 즉시 성공/일시 실패 후 재시도로 성공/영구 실패가 한 배치에 섞인
   시나리오가 전체 스택(`ManagedEngineRuntime`+`RecoveringEngineRuntime`,
   실제 `ThreadPoolExecutor` 동시 실행 포함)으로 End-to-End 검증된다.
5. `EngineRuntime`/`EngineAdapter` 메서드 시그니처는 변경되지 않는다
   (docstring 보강만).
6. 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린.
7. Model/Effort 라우팅, Adapter 계열 통합, Codex/Gemini 실환경 검증,
   Memory Summary 최적화, Retry Backoff는 범위 밖으로 유지된다.

**Task List**(2026-07-26 확정)

| Task | 내용 | 근거/출처 |
|---|---|---|
| M10-T01 | `EngineRuntime.run_parallel()` 계약 명확화 + `FakeEngineRuntime` 반영 — **완료** | 사용자 지시(4가지 보장 명문화) |
| M10-T02 | `ManagedEngineRuntime.run_parallel()` 개별 예외 캡처(버그 수정) — **완료** | 조사로 확인된 버그 |
| M10-T03 | `RecoveringEngineRuntime.run_parallel()` 실패 Task만 개별 재시도 — **완료** | M4 Review 이월 갭 |
| M10-T04 | End-to-End 검증 — **완료** | Milestone DoD |
| M10-T05 | Milestone 10 Review — 본 절 | 관례 |

**진행 상태**: M10-T01~T04 전체 완료. M10-T05(본 Review)로 Milestone을
마감한다.

#### M10-T01: `EngineRuntime.run_parallel()` 계약 명확화
- 목적/문제: 개별 Task 예외 시 동작이 계약에 정의되어 있지 않아
  구현체마다 다르게 동작할 수 있었다(둘 다 전체 실패).
- 작업 내용: `interfaces/engine_runtime.py`의 `run_parallel()` docstring에
  사용자가 명문화를 요청한 4가지 보장을 추가 — (1) 반환 길이=입력 길이
  (2) 순서 보존 (3) 개별 예외→`EngineResult(success=False)` 변환 (4)
  개별 실패만으로는 예외를 던지지 않음(단, `NoSuitableEngineError`처럼
  Runtime 자체의 치명적 오류는 예외 가능, 기존 예외 조항과 병기).
  `tests/interfaces/fakes.py`의 `FakeEngineRuntime.run_parallel()`을 이
  계약에 맞게 수정(개별 Task를 try/except로 캡처).
- 완료 조건(DoD): 계약 테스트로 "Adapter 하나가 예외를 던져도 나머지
  Task는 정상 결과를 반환하고 길이/순서가 유지됨"이 검증됨.
- 상태: **DONE (2026-07-26)** — `interfaces/engine_runtime.py`(docstring만,
  시그니처 불변), `tests/interfaces/fakes.py`의 `FakeEngineRuntime`,
  `tests/interfaces/test_engine_runtime.py`에 `SelectivelyFailingAdapter`
  +`test_run_parallel_converts_individual_task_exception_to_failed_result`
  신규.

#### M10-T02: `ManagedEngineRuntime.run_parallel()` 개별 예외 캡처
- 목적/문제: 확인된 버그(Task 1개 예외 → 배치 전체 결과 유실) 수정.
- 작업 내용: `run_parallel()`이 `required_capabilities`를 만족하는
  Adapter가 있는지 Task 제출 전에 한 번 미리 확인(`_require_adapter()`,
  `NoSuitableEngineError` fail-fast 유지)한 뒤, 각 `future.result()`를
  개별 try/except로 캐치해 실패한 것만 `EngineResult(success=False)`로
  변환.
- 완료 조건(DoD): 3개 Task 중 1개가 예외를 던져도 나머지 2개는 정상
  결과를 반환함이 단위 테스트로 검증됨.
- 상태: **DONE (2026-07-26)** — `runtime/engine/managed_engine_runtime.py`
  수정(클래스 docstring도 새 격리 보장으로 갱신).
  `tests/runtime/engine/test_managed_engine_runtime.py`의
  `test_run_parallel_independent_failure_does_not_block_others`(구
  버그를 "정상 동작"으로 잘못 문서화하던 테스트)를
  `test_run_parallel_independent_failure_does_not_lose_other_results`로
  재작성 + `test_run_parallel_without_suitable_engine_raises_before_any_
  execution` 신규(구조적 실패는 여전히 즉시 전파됨을 확인).

#### M10-T03: `RecoveringEngineRuntime.run_parallel()` 실패 Task만 재시도
- 목적/문제: M4 Review 이월 부채("개별 재시도 미지원") 해소 — 실제로는
  "재시도 전무"였음을 M10 착수 조사에서 확인.
- 작업 내용: 첫 병렬 패스(`inner.run_parallel()`, M10-T01/T02로 이미
  개별 실패가 격리됨) 후 실패(`success=False`)한 Task만 골라 기존
  `self.run()`의 `RetryPolicy` 루프로 재실행(새 재시도 로직 만들지
  않고 재사용, YAGNI). 재시도도 소진해 `self.run()`이 예외를 던지면
  그 Task만 `EngineResult(success=False)`로 변환 — `run()`은 단일
  Task라 예외를 그대로 전파해도 되지만 `run_parallel()`은 배치 전체를
  보호해야 하므로 의도적으로 다르게 처리(클래스 docstring에 근거 명시).
- 완료 조건(DoD): (a) 일시 실패 후 재시도로 성공 (b) 재시도 소진 시
  그 Task만 실패, 다른 Task는 영향 없음 — 두 시나리오 모두 단위
  테스트로 검증됨.
- 상태: **DONE (2026-07-26)** — `runtime/engine/recovering_engine_runtime.py`
  수정(클래스 docstring 갱신 포함).
  `tests/runtime/engine/test_recovering_engine_runtime.py`의
  `test_run_parallel_does_not_retry_individual_task_failures`(구
  동작을 "알려진 범위"로 문서화하던 테스트)를 제거하고
  `test_run_parallel_retries_individual_task_failure_until_success`+
  `test_run_parallel_exhausts_retries_and_isolates_permanent_failure`
  신규(`EventuallySucceedingEngineAdapter` 테스트 전용 Adapter 추가).

#### M10-T04: End-to-End 검증
- 목적: 즉시 성공/일시 실패 후 회복/영구 실패가 한 배치에 섞여도 전체
  스택(`ManagedEngineRuntime`+`RecoveringEngineRuntime`, 실제
  `ThreadPoolExecutor` 동시 실행)에서 올바르게 수렴함을 증명.
- 작업 내용: `test_run_parallel_end_to_end_mixed_outcomes_across_full_
  stack`(`MixedOutcomeEngineAdapter` 신규) — 4개 Task(즉시 성공/일시
  실패 후 성공/영구 실패/즉시 성공)가 한 배치에서 각각 `True, True,
  False, True`로 올바르게 수렴함을 검증.
- 완료 조건(DoD): 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린.
- 상태: **DONE (2026-07-26)** — `pytest`: **449개 전부 통과**(M9 완료
  시점 445개 → M10에서 4개 신규: M10-T01 +1, M10-T02 +1(순증가, 기존
  1개 재작성), M10-T03 +1(순증가, 기존 1개 제거+2개 신규), M10-T04
  +1). `ruff check src tests`: 클린. `mypy src`: 클린(82개 소스 파일,
  신규 소스 파일 0개).

---

## Milestone 10 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `EngineRuntime.run_parallel()` 계약에 개별 Task 실패 격리 4가지 보장 명시 | ✅ (M10-T01) |
| 2 | `ManagedEngineRuntime.run_parallel()`이 계약을 실제로 만족(버그 수정) | ✅ (M10-T02) |
| 3 | `RecoveringEngineRuntime.run_parallel()`이 실패 Task만 재시도 | ✅ (M10-T03) |
| 4 | 즉시 성공/일시 실패 후 성공/영구 실패 혼합 시나리오가 전체 스택으로 E2E 검증됨 | ✅ (M10-T04) |
| 5 | `EngineRuntime`/`EngineAdapter` 시그니처 변경 없음 | ✅ (아래 3절) |
| 6 | 기존 + 신규 테스트 전부 통과, `ruff`/`mypy` 클린 | ✅ (아래 4절) |
| 7 | Model/Effort 라우팅 등 5개 항목 범위 밖 유지 | ✅ (아래 5절) |

Task List(M10-T01~T04) 전체 완료. M10-T05(본 Review)로 Milestone을
마감한다.

**2. Architecture Review**

M10에서 실제로 바뀐 구조는 `EngineRuntime` 3개 구현체뿐이다 — 새
컴포넌트나 새 계층은 추가되지 않았다.
- **`interfaces/engine_runtime.py`(M10-T01)**: `run_parallel()`
  docstring에 4가지 보장 추가. 시그니처(`def run_parallel(self, tasks,
  required_capabilities=frozenset()) -> list[EngineResult]`)는 전혀
  바뀌지 않았다 — 이전에는 암묵적이던 계약을 명문화한 것뿐이다.
- **`ManagedEngineRuntime`(M10-T02)**: `run_parallel()` 내부에서
  `future.result()` 수집을 개별 try/except로 감쌌다. `_require_adapter()`
  를 Task 제출 전에 한 번 호출해 "Runtime 자체의 치명적 오류(엔진
  없음)"와 "개별 Task 실행 실패"를 구조적으로 분리했다 — 전자는 여전히
  즉시 전파, 후자만 격리한다.
- **`RecoveringEngineRuntime`(M10-T03)**: `run_parallel()`이 더 이상
  `inner`에 단순 위임하지 않고, 첫 병렬 패스 후 실패한 Task만 기존
  `self.run()`(이미 있는 재시도 루프)으로 재실행하는 조합(compose)
  패턴으로 바뀌었다. 새 재시도 상태 저장소나 새 클래스를 만들지 않았다.

**핵심 설계 결정**: 세 구현체 모두 "Runtime 자체의 치명적 오류
(`NoSuitableEngineError`)"와 "개별 Task 실행 실패"를 다르게 취급한다 —
전자는 Task를 하나도 실행하지 못하는 구조적 문제라 즉시 전파해야
사용자가 원인을 바로 알 수 있고, 후자는 배치의 나머지 부분을 계속
쓸모 있게 만들기 위해 격리해야 한다. 이 구분을 `docs/ARCHITECTURE.md`
§3.9와 각 구현체 docstring에 일관되게 반영했다.

`git diff --stat`(M9 종료 커밋 대비)로 확인한 결과 **소스 파일 3개만
수정**(`interfaces/engine_runtime.py`, `managed_engine_runtime.py`,
`recovering_engine_runtime.py`), 신규 소스 파일 0개 — M9(1개)보다는
넓지만 M6(5개)보다는 좁다. `docs/ARCHITECTURE.md` §3.9는 M10 완료
시점에 이미 갱신되어 구현과 문서 사이 괴리가 없다.

**3. Interface First 원칙 검토**

**M10은 새 최상위 Interface를 0개 추가했다**(M2/M3/M4/M6/M7/M8/M9와
동일 패턴, M5만 예외). `EngineRuntime.run_parallel()`의 시그니처는
전혀 바뀌지 않았다 — docstring에 이전부터 암묵적이어야 했던 계약을
명문화했을 뿐이며, 이는 기존 호출자 누구도 깨지 않는다(반환 타입·
개수·순서는 원래도 사실상 이랬어야 하는 것을 이제 문서로 강제한
것). `FakeEngineRuntime`(Fake+계약 테스트) 갱신도 계약 테스트 대상만
바뀌었을 뿐 `EngineRuntime` ABC 자체는 무변경이다.

**4. 테스트 결과**

- `pytest`: **449개 전부 통과**(M9 완료 시점 445개 → M10에서 4개 신규)
- `ruff check src tests`: 클린
- `mypy src`: 클린(82개 소스 파일)
- M9 완료 커밋 대비 소스 3개 파일 수정(신규 소스 파일 0개), 테스트
  3개 파일 수정(신규 테스트 파일 0개, 기존 테스트 2개를 새 계약에
  맞게 재작성)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M10에서 조사 후 확인해 실제로 해소한 것*
- `run_parallel()`이 개별 Task 예외로 배치 전체 결과를 잃는 버그
  (M10 착수 조사에서 새로 확인, M10-T02로 해소)
- `run_parallel` 개별 Task 재시도 미지원(M4-T06 이월, M10-T03으로 해소)

*M10 착수 전 재분석으로 범위에서 명시적으로 제외한 것(계속 이월)*
- Model/Effort 수준 라우팅(M6 Review 최초 이월) — `EngineAdapter.run()`
  Interface 변경 여부부터 설계 검토 필요한 무거운 작업이라 별도
  Milestone 필요
- `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임워크 통합(M5-T05
  최초 이월) — 기능 이득 없는 순수 리팩토링, 실제 유지보수 통증이
  증명되기 전까지 계속 이월 권장
- Codex/Gemini CLI 실제 바이너리 재검증(M5-T05 최초 이월) — **이 세션
  환경에 두 CLI가 설치되어 있지 않아 실행 자체가 불가능**함을 확인
  (`which codex`/`which gemini` 모두 not found). 실제 CLI가 설치된
  환경에서만 착수 가능.
- `MemoryEngine.search()` 선형 스캔(M4-T08 최초 이월) — PRD §11이 이미
  "장기 메모리 비대화 시 요약/우선순위화 전략을 설계"라고 유보해 둔
  항목. 실제 데이터 규모가 문제가 될 증거 없이 지금 최적화하면 YAGNI
  위반 위험 — M9-T01처럼 "조사 우선" 접근이 필요.

*계속 이월되는 기존 항목*
- Retry Backoff/Persistent Runtime Recovery/Approval 비동기 처리/
  Process Timeout 정책 고도화(M3-T08 최초 이월), `ShellAgent`
  화이트리스트가 코드에 고정(M5-T04 최초 이월)

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M10-T01~T04 상세 섹션) / `docs/ROADMAP.md`
(M10 Task List·Milestone 개요 반영) / `docs/ARCHITECTURE.md`(§3.9 M10
완료 시점에 이미 갱신됨) 완료. `pyproject.toml` 버전은 v0.5.0 그대로
유지한다. `.ai/MEMORY.md`는 이 Review 승인 직후 M1~M9와 동일한 방식으로
압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 소스 3개
파일 수정·신규 파일 0개, "Runtime 치명적 오류 vs 개별 Task 실패" 구분
원칙을 세 구현체에 일관 적용), Interface First 검토 완료(3절, 새
Interface 0개·시그니처 무변경), 테스트 결과 문서화 완료(4절), Technical
Debt 정리 완료(5절, 재분석으로 제외한 3개 항목의 이유를 투명하게 명시),
문서 갱신 완료(6절) — 6개 조건 모두 만족. Review 중 코드 변경이 필요한
치명적 문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 10 Completed를 선언한다.**

**Milestone 11 상태**: 착수 확정. 아래 "Milestone 11" 절 참고.

---

## Milestone 11 — Execution Environment

**목표**: `EngineAdapter`가 "무엇을 실행할지(엔진별 명령 조립·결과
파싱)"와 "어디서 실행할지(로컬 프로세스/향후 원격 컨테이너)"를 분리하지
못하고 있다 — `ClaudeCodeEngineAdapter`/`CLIEngineAdapter` 둘 다
`ProcessRunner`(M3-T03, 로컬 프로세스 실행 전용 구체 클래스)를 생성자에서
직접 생성해 사용한다. 이번 Milestone은 `ExecutionEnvironment` 인터페이스를
새로 정의하고, 기존 `ProcessRunner`를 그 인터페이스의 첫 구현체
(`LocalExecutionEnvironment`)로 승격해 두 Adapter가 구체 클래스가 아니라
인터페이스에 의존하도록 전환한다.

> **2026-07-26 설계 검토 결론(사용자 확정)**: `ExecutionEnvironment`를
> Task→Agent→Engine 사이의 새로운 최상위 Layer로 두지 않는다 — Agent나
> Engine Runtime이 "어디서 실행되는지"를 알아야 할 이유가 없고, 이미
> Engine Adapter가 세션 생명주기 계약(ADR-0015)을 갖고 있어 그 내부
> 협력자로 두는 것이 최소 복잡성 원칙에 맞는다. **`ExecutionEnvironment`는
> `EngineAdapter`의 하위(내부) 인터페이스로 유지**하고, Adapter는 이를
> **주입(Dependency Injection)받아** 사용한다(Adapter가 직접
> `LocalExecutionEnvironment()`를 `new`하지 않고, 생성자 매개변수로
> 받는다 — 편의상 기본값은 허용하되 항상 교체 가능해야 함).

**Non-goal(범위 밖, YAGNI)**: `CodespacesExecutionEnvironment`/
`ReplitExecutionEnvironment`/`DockerExecutionEnvironment` 실제 구현,
Claude API 기반 EngineAdapter, Model/Effort 수준 라우팅(M6 Review 최초
이월, 계속 이월).

**Milestone Definition of Done**
1. `ExecutionEnvironment` 인터페이스가 정의되고, Fake 구현체 기반 계약
   테스트가 통과한다.
2. `LocalExecutionEnvironment`가 이 계약을 만족하며, 기존 `ProcessRunner`
   가 제공하던 3가지 동작(정상 실행/Timeout 강제 종료/Cancel)을 회귀
   없이 그대로 제공함이 테스트로 증명된다.
3. `ClaudeCodeEngineAdapter`·`CLIEngineAdapter`가 `ProcessRunner`를 더
   이상 직접 생성하지 않고, 생성자 주입(DI)으로 `ExecutionEnvironment`
   인터페이스에만 의존하도록 바뀌며, 기존 테스트 스위트가 회귀 없이
   통과한다.
4. **새 `ExecutionEnvironment` 구현체(예: 향후 Codespaces)를 추가할 때
   기존 `EngineAdapter` 코드를 수정하지 않고 확장 가능함**이 테스트로
   증명된다(예: `FakeExecutionEnvironment`를 주입해도 Adapter 코드
   변경 없이 정상 동작 — Open-Closed Principle).
5. `docs/ARCHITECTURE.md`(§3.10, §9)가 새 구조를 반영한다.
6. 전체 `pytest`/`ruff`/`mypy`가 통과한다.

**Task List**(2026-07-26 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M11-T01 | `ExecutionEnvironment` Interface 정의 | **완료** |
| M11-T02 | `LocalExecutionEnvironment` 구현 | **완료** |
| M11-T03 | `EngineAdapter`가 `ExecutionEnvironment`를 사용하도록 전환 | **완료** |
| M11-T04 | 문서화 + Milestone 11 Review | **완료** |

**진행 상태**: M11-T01~T04 전체 완료. 아래 "Milestone 11 Review" 참고.

#### M11-T01: `ExecutionEnvironment` Interface 정의
- 목적: EngineAdapter가 실행 환경에 의존할 수 있는 추상 계약을 확정한다
  (Interface First).
- 작업 내용: `interfaces/execution_environment.py`에 정의.
  - `ExecutionResult`(dataclass): `returncode`, `stdout`, `stderr`,
    `timed_out`, `cancelled` — 기존 `ProcessResult`와 동일한 필드.
  - `ExecutionEnvironment`(ABC): `execute(execution_id, command, *,
    cwd=None, timeout=None) -> ExecutionResult`, `cancel(execution_id)
    -> None`. 메서드 docstring에 입력/출력/예외/보장사항 명시.
  - `ExecutionNotFoundError`.
  - 명명: 기존 `ProcessRunner`의 `process_id`를 `execution_id`로
    바꾼다 — "OS 프로세스"를 가정하지 않는 환경 비종속 이름을 계약에
    쓴다.
- 완료 조건(DoD): `tests/interfaces/fakes.py`에 `FakeExecutionEnvironment`
  추가 + 계약 테스트 통과.
- 상태: **DONE (2026-07-26)** — `interfaces/execution_environment.py`에
  `ExecutionEnvironment`(ABC, `execute`/`cancel`), `ExecutionResult`,
  `ExecutionNotFoundError` 정의(기존 `ProcessResult`/`ProcessNotFoundError`
  와 동일한 필드·의미이나 특정 실행 방식을 가정하지 않도록 `execution_id`
  로 명명). `tests/interfaces/fakes.py`에 `FakeExecutionEnvironment` 추가
  (`result`/`exception`으로 결과 구성, `executed_commands`로 호출 검증,
  `cancel()`은 현재 `execute()` 실행 중인 id에만 성공하고 그 외에는
  `ExecutionNotFoundError`). `tests/interfaces/test_execution_environment.py`
  5개 신규 테스트. `ruff check src tests`, `mypy src`, `pytest`(454개,
  기존 449개 + 신규 5개) 모두 통과. 다음 Task: **M11-T02**
  (`LocalExecutionEnvironment` 구현).
- 의존성: 없음.

#### M11-T02: `LocalExecutionEnvironment` 구현
- 목적: 로컬 프로세스를 실행하는 첫 실제 구현체를 제공한다.
- 작업 내용: `adapters/local_execution_environment.py`에
  `LocalExecutionEnvironment` 구현. 새 프로세스 관리 로직을 새로 만들지
  않고, 이미 검증된 `ProcessRunner`(M3-T03)를 내부에서 그대로 사용하는
  얇은 위임 클래스로만 구현한다(Surgical Changes — 기존 코드 존중,
  `ProcessRunner`는 삭제·수정하지 않음).
- 완료 조건(DoD): M11-T01의 계약 테스트 스위트를
  `LocalExecutionEnvironment`에도 재사용해 통과 + 기존
  `test_process_runner.py` 무변경 통과.
- 상태: **DONE (2026-07-26)** — `adapters/local_execution_environment.py`
  에 `LocalExecutionEnvironment` 구현. 새 프로세스 관리 로직 없이
  `ProcessRunner`(M3-T03)에 그대로 위임하고, `ProcessResult`↔
  `ExecutionResult`/`ProcessNotFoundError`↔`ExecutionNotFoundError`만
  변환한다(`ProcessRunner` 자체는 수정하지 않음). `tests/adapters/
  test_local_execution_environment.py`에 `test_process_runner.py`와
  동일한 5개 시나리오(정상 실행/stderr+nonzero/Timeout 강제 종료/
  unknown cancel 예외/실행 중 cancel)를 `ExecutionEnvironment` 계약
  기준으로 재작성. `test_process_runner.py`는 무변경으로 그대로 통과.
  `ruff check src tests`, `mypy src`, `pytest`(459개, 기존 454개 +
  신규 5개) 모두 통과. 다음 Task: **M11-T03**(`EngineAdapter`가
  `ExecutionEnvironment`를 사용하도록 전환).
- 의존성: M11-T01.

#### M11-T03: `EngineAdapter`가 `ExecutionEnvironment`를 사용하도록 전환
- 목적: `ClaudeCodeEngineAdapter`/`CLIEngineAdapter`가 구체 클래스가
  아니라 인터페이스에 의존하게 한다(Interface First를 Engine Adapter
  내부 의존성에도 적용, DI 기본 방향).
- 작업 내용: 두 Adapter의 생성자 매개변수를 `process_runner:
  ProcessRunner | None` → `execution_environment: ExecutionEnvironment
  | None`(기본값 `LocalExecutionEnvironment()`)로 교체하고 내부 호출을
  `execute()`/`cancel()`로 변경한다. 두 클래스는 같은 이유로 항상 함께
  바뀌는 강결합 쌍이라 하나의 Task로 묶는다(ADR-0022 기준).
- 완료 조건(DoD): `test_claude_code_engine_adapter.py`/
  `test_cli_engine_adapter.py`가 (Fake 주입 대상만
  `ExecutionEnvironment` 기준으로 갱신되어) 회귀 없이 통과. 신규
  `FakeExecutionEnvironment` 주입만으로 Adapter 코드 변경 없이 동작함을
  보이는 테스트 포함(Milestone DoD 4번 직접 증명).
- 상태: **DONE (2026-07-26)** — `ClaudeCodeEngineAdapter`/`CLIEngineAdapter`
  생성자 매개변수를 `process_runner: ProcessRunner | None` →
  `execution_environment: ExecutionEnvironment | None`(기본값
  `LocalExecutionEnvironment()`)로 교체, 내부 호출을 `execute()`/
  `cancel()`로 변경(둘 다 DI 기본값만 다르게 감쌈, 로직 변경 없음).
  `CLIProvider.parse_result()`(및 `CodexProvider`/`GeminiCliProvider`
  구현) 시그니처도 `ProcessResult` → `ExecutionResult`로 함께 갱신
  (같은 이유로 항상 함께 바뀌는 강결합이라 이번 Task에 포함).
  `tests/adapters/test_claude_code_engine_adapter.py`/
  `test_cli_engine_adapter.py`의 로컬 `FakeProcessRunner`를
  `tests/interfaces/fakes.py`의 `FakeExecutionEnvironment`로 교체(다른
  Interface들과 동일한 "Fake는 interfaces/fakes.py에 두고 cross-import"
  관례를 따름). `test_cancel_marks_status_cancelled_and_notifies_process_
  runner`는 `ExecutionEnvironment.cancel()`이 미실행 id에 대해
  `ExecutionNotFoundError`를 던지는 새 계약에 맞춰
  `test_cancel_before_execution_marks_status_cancelled`로 재작성(Adapter가
  예외를 삼키고 상태만 전이시킴을 확인하는 것으로 범위를 정정 — 이전
  테스트는 duck-typing Fake가 예외를 던지지 않던 우연한 동작에
  의존했음). `test_cli_engine_adapter.py`에
  `test_new_execution_environment_extends_adapter_without_code_changes`
  신규 추가해 Milestone DoD 4번(OCP)을 직접 증명. `test_m3_end_to_end.py`/
  `test_m6_policy_routing.py`/`test_coding_agent_runtime_integration.py`의
  로컬 duck-typing 더블(`SwitchingFakeProcessRunner`/`FlakyProcessRunner`
  등)도 `ExecutionEnvironment`를 상속하도록 함께 갱신(회귀 없음 확인
  목적). `ShellAgent`가 쓰는 `ProcessRunner`/`FakeProcessRunner`(M5-T04,
  EngineAdapter와 무관한 별도 경로)는 범위 밖으로 전혀 손대지 않음.
  `ruff check src tests`, `mypy src`, `pytest`(460개, 기존 459개 +
  신규 1개) 모두 통과. 다음 Task: **M11-T04**(문서화 + Milestone 11
  Review).
- 의존성: M11-T02.

#### M11-T04: 문서화 + Milestone 11 Review
- 목적: 문서와 구현을 일치시키고 Milestone 종료 승인을 받는다.
- 작업 내용: `docs/ARCHITECTURE.md` §3.10(Engine Adapter 아래
  ExecutionEnvironment 추가)/§9(디렉터리 매핑) 갱신, `.ai/DECISIONS.md`
  에 신규 ADR(ExecutionEnvironment 도입 배경·대안·이유) 기록,
  `docs/ROADMAP.md`/`.ai/MEMORY.md` 갱신, 전체 테스트 결과 정리 및
  제시.
- 완료 조건(DoD): 문서-구현 정합성 확인 + 사용자 승인.
- 상태: **DONE (2026-07-26)** — `docs/ARCHITECTURE.md` v0.13.0 §3.10
  (ExecutionEnvironment 협력자 설명 신규), §7(Interfaces 17종→18종,
  `ExecutionEnvironment` 행 추가), §9(디렉터리 매핑에
  `interfaces/execution_environment.py`/`adapters/
  local_execution_environment.py` 반영), 문서 헤더(버전/상태) 갱신.
  `.ai/DECISIONS.md`에 **ADR-0025**(ExecutionEnvironment를 새 최상위
  Layer 대신 EngineAdapter 하위 인터페이스로 도입 — 배경/결정/대안/
  이유/결과 전문) 신규 작성. `docs/ROADMAP.md` Milestone 11 절 Task
  List 상태 갱신. 아래 "Milestone 11 Review" 절 참고.
- 의존성: M11-T01~T03.

---

## Milestone 11 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `ExecutionEnvironment` 인터페이스 정의 + 계약 테스트 통과 | ✅ (M11-T01) |
| 2 | `LocalExecutionEnvironment`가 `ProcessRunner`와 동일한 3가지 동작을 회귀 없이 제공 | ✅ (M11-T02) |
| 3 | `ClaudeCodeEngineAdapter`/`CLIEngineAdapter`가 DI로 `ExecutionEnvironment`에만 의존 | ✅ (M11-T03) |
| 4 | 새 `ExecutionEnvironment` 구현체 추가 시 기존 `EngineAdapter` 코드 무변경으로 확장 가능(OCP) | ✅ (M11-T03, 전용 테스트로 직접 증명) |
| 5 | `docs/ARCHITECTURE.md`(§3.10, §9)가 새 구조를 반영 | ✅ (M11-T04) |
| 6 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M11-T01~T04) 전체 완료. 사용자 최종 승인 조건 4개
(M11-T01~T04 순서 진행 / 각 Task마다 구현→테스트→문서화 / YAGNI로
`LocalExecutionEnvironment`만 구현 / DI 기본 방향 + OCP DoD 포함)
모두 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `interfaces/execution_environment.py`
  (`ExecutionEnvironment`, `ExecutionResult`, `ExecutionNotFoundError`),
  `adapters/local_execution_environment.py`(`LocalExecutionEnvironment`).
- **변경된 기존 컴포넌트**: `ClaudeCodeEngineAdapter`/`CLIEngineAdapter`
  (생성자 매개변수 교체 + 내부 호출 변경), `CLIProvider`/`CodexProvider`/
  `GeminiCliProvider`(`parse_result()` 시그니처를 `ProcessResult` →
  `ExecutionResult`로, 같은 이유로 함께 변경되는 강결합).
- **손대지 않은 것**: `ProcessRunner`(M3-T03, `LocalExecutionEnvironment`
  가 그대로 감싸기만 함), `ShellAgent`의 `ProcessRunner` 경로(M5-T04,
  `EngineAdapter`와 무관한 완전히 다른 실행 경로), `EngineRuntime`/
  `EngineAdapter`의 기존 세션 생명주기 계약(ADR-0015, 시그니처 무변경 —
  `run()`의 내부 구현만 바뀜).
- **핵심 설계 결정**: `ExecutionEnvironment`를 Task→Agent→Engine
  사이의 새 최상위 Layer로 만들지 않고 `EngineAdapter` 하위(내부)
  인터페이스로 뒀다(ADR-0025). Agent/Engine Runtime은 이 인터페이스의
  존재를 전혀 모른다 — `docs/ARCHITECTURE.md` §2의 최상위 흐름은
  그대로 유지된다.

`git diff --stat`(M11 착수 시점 대비)로 확인한 결과 신규 소스 파일
2개(`execution_environment.py`, `local_execution_environment.py`),
기존 소스 파일 5개 수정(`claude_code_engine_adapter.py`,
`cli_engine_adapter.py`, `cli_provider.py`, `codex_provider.py`,
`gemini_cli_provider.py`) — M5(6개 신규)보다는 좁고 M9(1개)보다는
넓은, 중간 규모의 범위였다.

**3. Interface First 원칙 검토**

**M11은 새 최상위 Interface를 1개 추가했다**(`ExecutionEnvironment`,
17종→18종). M5(`LLMPolicyEngine`) 이후 두 번째 신규 최상위 Interface
추가 사례이며, M2/M3/M4/M6/M7/M8/M9/M10처럼 "기존 계약 위에서만
작업"하지 않은 예외적인 Milestone이다. 다만 이 Interface는 처음부터
"`EngineAdapter` 하위(내부) 협력자"로 설계되어, `EngineAdapter`/
`EngineRuntime` 등 기존 보호 자산(`.ai/RULES.md` §1.2)의 계약은 단
한 글자도 바뀌지 않았다 — `EngineAdapter.run()`의 시그니처, Engine
Runtime이 Adapter를 호출하는 방식 모두 M11 이전과 동일하다.

**4. 테스트 결과**

- `pytest`: **460개 전부 통과**(M10 완료 시점 449개 → M11에서 11개
  신규: M11-T01 +5, M11-T02 +5, M11-T03 +1(순증가 — 기존 테스트
  다수를 `ExecutionEnvironment` 계약 기준으로 재작성했지만 신규
  테스트 파일은 만들지 않음, `test_new_execution_environment_extends_
  adapter_without_code_changes` 1개만 순증가))
- `ruff check src tests`: 클린
- `mypy src`: 클린(84개 소스 파일, 신규 2개)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M11에서 새로 발견해 즉시 해소한 것*
- `test_cancel_marks_status_cancelled_and_notifies_process_runner`가
  로컬 duck-typing `FakeProcessRunner`의 "cancel은 절대 예외를 던지지
  않는다"는 우연한 동작에 암묵적으로 의존하고 있었음(M11-T01에서
  `ExecutionEnvironment.cancel()`이 미실행 id에 대해
  `ExecutionNotFoundError`를 던지는 명시적 계약을 정의하면서 발견).
  `test_cancel_before_execution_marks_status_cancelled`로 재작성해
  "Adapter가 예외를 삼키고 상태만 전이시킨다"는 실제 계약을 정확히
  검증하도록 정정(M11-T03).

*M11 범위 밖으로 명시적으로 제외한 것(YAGNI, 계속 이월)*
- `CodespacesExecutionEnvironment`/`ReplitExecutionEnvironment`/
  `DockerExecutionEnvironment` 등 원격/컨테이너 실행 환경 — 실제
  요구사항이 생기기 전까지 구현하지 않는다.
- `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임워크 통합(M5-T05
  최초 이월, M10 재분석에서 "기능 이득 없는 순수 리팩토링"으로 확인) —
  이번에도 손대지 않음.

*계속 이월되는 기존 항목*
- Model/Effort 수준 라우팅(M6 Review 최초 이월)
- Codex/Gemini CLI 실제 바이너리 미검증(이 세션 환경엔 CLI 없음)
- `MemoryEngine.search()` 선형 스캔(M4-T08 최초 이월)
- Retry Backoff/Persistent Runtime Recovery/Approval 비동기 처리/
  Process Timeout 정책 고도화(M3-T08 최초 이월), `ShellAgent`
  화이트리스트가 코드에 고정(M5-T04 최초 이월)

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M11-T01~T04 상세 섹션) / `docs/ROADMAP.md`
(M11 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.13.0, §3.10/
§7/§9 갱신) / `.ai/DECISIONS.md`(ADR-0025 신규) 완료.
`pyproject.toml` 버전은 v0.5.0 그대로 유지한다(ADR-0024 기준선은
"기존 16→18종 Interface·계층 구조를 기본값으로 유지"를 전제하며,
`ExecutionEnvironment`는 최상위 흐름을 바꾸지 않는 하위 협력자이므로
기준선 재선언이 필요한 변경이 아니다). `.ai/MEMORY.md`는 이 Review
승인 직후 M1~M10과 동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 신규 2/
수정 5 소스 파일, "새 최상위 Layer 대신 EngineAdapter 하위 인터페이스"
설계 결정 명시), Interface First 검토 완료(3절, 새 Interface 1개 추가를
투명하게 보고하되 기존 보호 자산 무변경임을 확인), 테스트 결과 문서화
완료(4절), Technical Debt 정리 완료(5절, 테스트 하나가 우연한 동작에
의존하던 것을 발견·수정한 것 포함), 문서 갱신 완료(6절) — 6개 조건
모두 만족. Review 중 코드 변경이 필요한 치명적 문제(버그·계약 위반)는
발견되지 않았다.

**사용자 승인을 조건으로 Milestone 11 Completed를 선언한다.**

**Milestone 11 종료 — 2026-07-26 사용자 승인.**

**Milestone 12 상태**: 착수 확정. 아래 "Milestone 12" 절 참고.

---

## Milestone 12 — Workflow Automation

**목표**: 여러 Task로 구성된 Workflow가, 사람이 각 Task마다 개별적으로
실행을 트리거하지 않아도 `WorkflowEngine.plan()`이 계산한 의존관계
순서대로 자동으로 순차 실행되게 한다(MVP, 2026-07-26 사용자 확정).

> **설계 검토에서 발견한 사실**: `WorkspaceCore.start_workflow()`가
> 이미 `WorkflowEngine.plan()`을 호출해 순서를 계산하지만, 그 순서를
> 실제로 실행하는 코드는 지금까지 어디에도 없었다. `plan()`은 계약상
> 순수 함수(순서 계산만, side-effect 없음)이고, Task를 실제로 돌리는
> 유일한 경로는 `PlanningAgent.plan_mission()`(Task 1개를 새로 만들며
> 즉시 파이프라인을 시작)뿐이었다. 또한 `InMemoryEventBus.publish()`는
> 완전히 동기(M9-T01 조사에서 확인)라 `MissionPlanned` 발행이 끝나는
> 시점에는 Coding→Shell→Coordinator→Review→Documentation 전체
> 파이프라인이 이미 동기적으로 끝나 있다 — "완료를 기다리는" 별도
> 비동기 로직이 필요 없다.

**설계 방향(사용자 확정)**: `WorkflowEngine`(Core Engine)에 실행 책임을
추가하지 않는다 — Core Engine은 Agent보다 하위 계층이라 EventBus에
의존하면 `docs/ARCHITECTURE.md` §8 의존성 규칙(Agent → Core Engines)이
뒤집힌다. 새 Agent(Capability 포함)로도 만들지 않는다 — Multi-Agent
범위 제외 취지에 맞춰 `AgentRuntime`/`AgentScheduler`를 거치지 않는
순수 조율용 클래스 **`WorkflowRunner`**(신규, `runtime/workflow/
workflow_runner.py`)를 둔다. `WorkflowEngine.plan()` + `EventBus` +
`TaskEngine`만 사용해, `plan()` 순서대로 각 task_id에 `MissionPlanned`
를 발행하고, 발행 직후 `TaskEngine.get_task(task_id).status`가 `DONE`
이 아니면(예: 재작업 소진 `ReworkExhausted`) 그 자리에서 중단한다.
엔진 예외가 그대로 전파되는 경우도 함께 잡아 중단 처리한다.

**Non-goal(범위 밖)**: Multi-Agent 선택/조정 로직 변경(기존 고정
파이프라인 그대로 재사용), Provider/Model Routing, 병렬 실행, Workflow
레벨 Retry, Approval 게이트, Task 간 결과 전달(한 Task의 산출물을 다음
Task 입력으로 넘기는 것).

**Milestone Definition of Done**
1. `WorkflowRunner`가 `Workflow`를 받아 `plan()` 순서대로 각 Task를
   순차 실행한다.
2. 앞 Task가 실패하면(`TaskStatus.DONE`에 도달하지 못하거나 예외 발생)
   이후 Task는 실행되지 않고 즉시 중단된다.
3. Task 2개 이상 + 의존관계가 있는 실제 Workflow가 사람 개입 없이
   완주함이 통합 테스트로 증명된다(성공 케이스 + 중간 실패 시 중단
   케이스 둘 다).
4. 기존 `WorkflowEngine`/`EventBus`/`TaskEngine`/Agent 파이프라인
   계약은 전혀 변경하지 않는다(새 컴포넌트 추가만).
5. 전체 `pytest`/`ruff`/`mypy` 통과.

**Task List**(2026-07-26 확정, 사용자 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M12-T01 | `WorkflowRunner` 구현 | **완료** |
| M12-T02 | End-to-End 검증 | **완료** |
| M12-T03 | 문서화 + Milestone 12 Review | **완료** |

**진행 상태**: M12-T01~T03 전체 완료. 아래 "Milestone 12 Review" 참고.

#### M12-T01: `WorkflowRunner` 구현
- 목적: Workflow의 Task 순차 자동 실행 책임을 가진 컴포넌트를 만든다.
- 작업 내용: `runtime/workflow/workflow_runner.py`에 `WorkflowRunner`
  구현. 생성자로 `workflow_engine: WorkflowEngine`, `event_bus:
  EventBus`, `task_engine: TaskEngine`을 주입받는다(키워드 전용,
  기존 `WorkspaceCore`/`AgentRuntime` 패턴과 동일). `run(workflow:
  Workflow) -> WorkflowRunResult`(가칭) 형태의 단일 공개 메서드 —
  `plan()`으로 순서를 얻고, 각 task_id에 대해 `MissionPlanned` Event를
  발행(`event_id`는 다른 Agent들과 동일하게 `uuid4()`)한 뒤
  `task_engine.get_task(task_id).status`를 확인해 `DONE`이 아니면
  중단하고 어디까지 실행됐는지 반환한다. `AgentRuntime`/
  `AgentScheduler`/`AgentCapability`는 전혀 사용하지 않는다(Agent가
  아님을 코드로도 증명).
- 완료 조건(DoD): 성공적으로 완주하는 경우, 중간에 실패해 중단되는
  경우 각각을 Mock/Fake `WorkflowEngine`/`EventBus`/`TaskEngine`으로
  검증하는 단위 테스트가 통과한다.
- 상태: **DONE (2026-07-26)** — `runtime/workflow/workflow_runner.py`에
  `WorkflowRunner`(`run(workflow) -> WorkflowRunResult`)와
  `WorkflowRunResult`(completed_task_ids/failed_task_id/success)
  구현. `AgentRuntime`/`AgentScheduler`는 전혀 import하지 않음(Agent가
  아님을 코드로 증명). **구현 중 계획을 단순화하는 발견**: `EventBus.
  publish()`는 계약상 "예외: 없음"(구독자 예외는 Bus 내부에서 격리됨,
  `interfaces/event_bus.py`)이므로 애초 계획했던 try/except 기반 실패
  감지는 죽은 코드가 되어 작성하지 않았다 — 실패 감지는 오직
  `TaskEngine.get_task(task_id).status != TaskStatus.DONE` 하나로만
  충분함을 확인(YAGNI, 불필요한 예외 처리 금지 원칙과 일치). `runtime/
  workflow/`, `tests/runtime/workflow/` 신규 패키지.
  `tests/runtime/workflow/test_workflow_runner.py` 3개 신규 테스트
  (전체 완주/두 번째 Task가 DONE에 미도달 시 세 번째 Task 미실행까지
  확인/단일 Task Workflow). `ruff check src tests`, `mypy src`,
  `pytest`(463개, 기존 460개 + 신규 3개) 모두 통과. 다음 Task:
  **M12-T02**(End-to-End 검증).
- 의존성: 없음(기존 Interface만 사용).

#### M12-T02: End-to-End 검증
- 목적: 실제 Agent 파이프라인 위에서 다단계 Workflow가 사람 개입 없이
  완주함을 증명한다.
- 작업 내용: `tests/integration/`에 2~3개 Task + 의존관계가 있는
  실제 `Workflow`를 구성하고, `WorkflowRunner`가 `MockEngineAdapter`(또는
  기존 통합 테스트가 쓰던 패턴)를 통해 각 Task를 실제 6-Agent
  파이프라인(Planning 제외 — Task는 이미 생성돼 있으므로 Coding부터)
  으로 순차 실행함을 검증한다. 성공 시나리오(전체 완주)와 실패
  시나리오(중간 Task 실패 → 이후 Task 미실행) 둘 다 다룬다.
- 완료 조건(DoD): 두 시나리오 모두 통합 테스트로 통과하고, Task 실행
  순서가 `plan()` 결과와 정확히 일치함을 이벤트/상태로 확인한다.
- 상태: **DONE (2026-07-26)** — `tests/integration/
  test_m12_workflow_automation.py` 신규. `build_pipeline()`이
  `PlanningAgent` 없이 Coding/Shell/Coordinator/Review/Documentation
  5-Agent + `MockEngineAdapter` + `WorkflowRunner`를 조립한다(Task는
  `WorkflowRunner`가 `TaskEngine.create_task()`로 만든 것을 그대로
  재사용). `SequencedProcessRunner`(호출 순서별 결과 반환, 마지막
  결과는 이후 호출에 반복)로 `ShellAgent`의 테스트 결과를 제어 —
  Task 2개 성공 시나리오(`test_workflow_with_two_tasks_completes_
  without_human_intervention`)와 두 번째 Task가 재작업 소진
  (`max_rework_attempts=1`)으로 실패해 세 번째 Task가 아예 실행되지
  않음을 증명하는 시나리오(`test_workflow_stops_when_a_task_fails_and_
  later_tasks_never_run`) 2개. 후자에서 `task3.status == TaskStatus.
  TODO`(create_task() 직후 그대로)로 "실행 자체가 안 됨"을 명시적으로
  확인. `ruff check src tests`, `mypy src`, `pytest`(465개, 기존
  463개 + 신규 2개) 모두 통과. 다음 Task: **M12-T03**(문서화 +
  Milestone 12 Review).
- 의존성: M12-T01.

#### M12-T03: 문서화 + Milestone 12 Review
- 목적: 문서와 구현을 일치시키고 Milestone 종료 승인을 받는다.
- 작업 내용: `docs/ARCHITECTURE.md`에 `WorkflowRunner` 반영(어느
  절에 넣을지는 착수 시 재검토 — Core Engines도 Agent도 아닌 새
  종류의 컴포넌트이므로 §3에 소절 신설 여부를 판단), `docs/ROADMAP.md`/
  `.ai/MEMORY.md` 갱신, 전체 테스트 결과 정리 및 제시.
- 완료 조건(DoD): 문서-구현 정합성 확인 + 사용자 승인.
- 상태: **DONE (2026-07-26)** — `docs/ARCHITECTURE.md` v0.14.0 §3.7
  (Workflow Engine 책임을 "계획만"으로 명확화 + §3.12 참조 추가),
  §3.12(신규 소절 — `WorkflowRunner`가 Agent도 Core Engine도 아닌
  이유, 동작, 전제 조건), §9(디렉터리 매핑에 `runtime/workflow/`
  반영), 문서 헤더(버전/상태) 갱신. `docs/ROADMAP.md` Milestone 12
  절 Task List 상태 갱신. 새 최상위 Interface를 추가하지 않아
  (`WorkflowRunner`는 ABC가 아닌 구체 클래스) 신규 ADR은 작성하지
  않음(M6~M10과 동일 패턴 — Task List 승인 시 이미 설계 방향까지
  확정됨). 아래 "Milestone 12 Review" 절 참고.
- 의존성: M12-T01~T02.

---

## Milestone 12 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `WorkflowRunner`가 `plan()` 순서대로 Task를 순차 실행 | ✅ (M12-T01) |
| 2 | 앞 Task 실패 시 이후 Task 미실행·즉시 중단 | ✅ (M12-T01 단위 테스트, M12-T02 E2E) |
| 3 | Task 2개 이상 + 의존관계 Workflow가 사람 개입 없이 완주(성공/중단 두 시나리오) | ✅ (M12-T02) |
| 4 | 기존 `WorkflowEngine`/`EventBus`/`TaskEngine`/Agent 파이프라인 계약 무변경 | ✅ (아래 2절) |
| 5 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M12-T01~T03) 전체 완료. 사용자 승인 조건("M12는 Workflow
Automation, Multi-Agent/Routing/Parallel/Retry/Approval 제외") 그대로
충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `runtime/workflow/workflow_runner.py`
  (`WorkflowRunner`, `WorkflowRunResult`) 하나뿐. `AgentRuntime`/
  `AgentScheduler`/`AgentCapability`를 전혀 import하지 않아 "Agent가
  아님"이 코드로도 증명된다.
- **변경된 기존 컴포넌트**: 소스 코드는 없음 — `docs/ARCHITECTURE.md`
  §3.7의 `WorkflowEngine` 책임 서술("계획/실행"→"계획만")만 실제
  계약(`plan()`이 처음부터 side-effect 없는 순수 함수로 정의돼 있었음,
  M1)과 일치하도록 정정. 계약·시그니처는 M1부터 지금까지 한 번도
  바뀌지 않았다.
- **핵심 설계 결정**: `WorkflowEngine`(Core Engine)이나 신규 Agent가
  아니라, `WorkflowEngine.plan()` + `EventBus` + `TaskEngine` 세
  Interface를 조합하는 독립 조율자로 `WorkflowRunner`를 두었다
  (`EngineApprovalPipeline`, M3-T05와 동일한 패턴 — "새 상태를 최소한만
  갖는 조합형 조율자"). `EventBus.publish()`가 계약상 예외를 던지지
  않는다는 사실(구독자 예외는 Bus 내부에서 격리, M1 계약)을 구현 중
  재확인해, 애초 계획했던 try/except 기반 실패 감지를 걷어내고
  `TaskStatus.DONE` 여부 하나로 단순화했다(M12-T01 "부가 발견").

`git diff --stat`(M11 종료 커밋 대비)로 확인한 결과 신규 소스 파일
1개(`workflow_runner.py`, `__init__.py` 2개는 빈 패키지 마커), 기존
소스 파일 수정 0개 — M9(1개 수정)보다도 좁고, M1 이후 가장 작은 변경
폭 중 하나였다.

**3. Interface First 원칙 검토**

**M12은 새 최상위 Interface를 추가하지 않았다**(M6/M7/M8/M9/M10과
동일 패턴, M5/M11만 예외). `WorkflowRunner`는 기존 3개 Interface
(`WorkflowEngine`/`EventBus`/`TaskEngine`)를 그대로 소비하는 구체
클래스일 뿐이며, 세 Interface의 계약·시그니처는 전혀 바뀌지 않았다.

**4. 테스트 결과**

- `pytest`: **465개 전부 통과**(M11 완료 시점 460개 → M12에서 5개
  신규: M12-T01 +3, M12-T02 +2)
- `ruff check src tests`: 클린
- `mypy src`: 클린(86개 소스 파일, 신규 1개)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M12에서 새로 발견해 즉시 반영한 것*
- (버그 아님, 설계 단순화) `EventBus.publish()`가 예외를 던지지
  않는다는 계약을 재확인해, 계획 단계의 try/except 기반 실패 감지를
  실제 구현에서는 만들지 않음(M12-T01 참고) — 불필요한 코드를 미리
  걷어낸 사례로 기록.

*M12 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- Multi-Agent 선택/조정 로직 변경, Provider/Model Routing, 병렬 실행,
  Workflow 레벨 Retry, Approval 게이트, Task 간 결과 전달.

*계속 이월되는 기존 항목*
- Model/Effort 수준 라우팅(M6 Review 최초 이월)
- `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임워크 미통합
- Codex/Gemini CLI 실제 바이너리 미검증(이 세션 환경엔 CLI 없음)
- `MemoryEngine.search()` 선형 스캔
- Retry Backoff/Persistent Runtime Recovery/Approval 비동기 처리/
  Process Timeout 정책 고도화, `ShellAgent` 화이트리스트가 코드에 고정

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M12-T01~T03 상세 섹션) / `docs/ROADMAP.md`
(M12 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.14.0, §3.7/
§3.12/§9 갱신) 완료. 새 Interface가 없어 `.ai/DECISIONS.md`에 신규
ADR을 추가하지 않았다. `pyproject.toml` 버전은 v0.5.0 그대로 유지
(ADR-0024 기준선 — `WorkflowRunner`는 기존 Interface만 조합하는
구체 클래스라 기준선 재선언 대상이 아님). `.ai/MEMORY.md`는 이 Review
승인 직후 M1~M11과 동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 신규 소스
1개·수정 0개, "Core Engine/Agent가 아닌 독립 조율자" 설계 결정 명시),
Interface First 검토 완료(3절, 새 Interface 0개), 테스트 결과 문서화
완료(4절), Technical Debt 정리 완료(5절), 문서 갱신 완료(6절) — 6개
조건 모두 만족. Review 중 코드 변경이 필요한 치명적 문제(버그·계약
위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 12 Completed를 선언한다.**

**Milestone 12 종료 — 2026-07-26 사용자 승인.**

**Milestone 13 상태**: 착수 확정. 아래 "Milestone 13" 절 참고.

---

## Milestone 13 — Multi-Agent Collaboration

**목표**: 같은 Capability(CODING)를 가진 Agent가 여러 개 등록돼 있을 때,
`AgentScheduler.select()`가 실제로 그중 하나만 고르고 선택되지 않은
Agent는 개입하지 않는다는 것을 실제 동작으로 증명한다(MVP, 2026-07-26
사용자 확정).

> **설계 검토에서 발견한 사실**: `AgentScheduler`(Capability 기준 Agent
> 선택 계약)는 M1부터 정의되어 있었지만, 지금까지 한 번도 실제 협업
> 흐름에서 쓰인 적이 없었다. 현재 파이프라인은 각 Agent가 특정 Event
> 타입을 직접 구독해 무조건 처리하는 고정 배선 구조라, Capability가
> 같은 Agent가 여러 개 있어도 Scheduler가 "이번엔 누가 처리할지"를
> 실제로 고르는 시나리오가 존재한 적이 없었다. `agents/scheduling.py`
> 의 `find_agent_by_capability()`도 테스트에서 "등록 여부 확인" 용도로만
> 쓰였다. `AgentRuntime.start_agent()`가 이미 `AgentRegistry.register()`
> 를 호출하므로, 같은 Capability의 Agent 인스턴스를 여러 개 만들면
> 자동으로 전부 Registry에 등록된다 — 새 Interface 없이 기존 구성요소
> 만으로 이번 MVP를 구현할 수 있다.

**설계 방향(사용자 확정)**: 새로운 중앙 디스패처를 만들지 않는다.
`InMemoryAgentScheduler.select()`가 결정적(candidates 리스트에서 첫
매치)이므로, 모든 후보 Agent가 같은 `candidates`로 같은 질문을 하면
전부 같은 답을 얻는다는 점을 이용한다 — 각 Agent가 처리 직전에
"내가 선택됐나?"를 스스로 확인하고 아니면 조용히 넘어가는 **자가 확인
가드**를 둔다. `agents/scheduling.py`에 `is_agent_selected(agent_registry,
agent_scheduler, capability, agent_id) -> bool` 헬퍼를 추가하고,
`CodingAgent` 생성자에 `agent_registry`/`agent_scheduler`를 **선택적**
(기본값 `None`) 키워드 매개변수로 추가한다 — 주어지지 않으면 기존과
100% 동일하게 동작해 기존 호출부(수십 곳)를 전혀 건드리지 않는다.
MVP는 `CodingAgent` 하나에만 적용한다(Review/Documentation 등으로
확장은 후속 Milestone).

**Non-goal(범위 밖)**: Provider/Model Routing(M6에서 이미 다룸), 병렬
실행, Scheduler 선택 정책 고도화(우선순위/부하 기반 — 기존 "첫 매치"
그대로 사용), `CodingAgent` 외 다른 Agent로의 확장.

**Milestone Definition of Done**
1. `agent_registry`/`agent_scheduler`를 주입하지 않으면 `CodingAgent`는
   기존과 완전히 동일하게 동작한다(회귀 없음).
2. 같은 CODING Capability의 `CodingAgent` 2개가 등록된 상태에서,
   `MissionPlanned` 하나에 대해 Scheduler가 고른 1개만 Task를 처리하고
   나머지는 아무것도 하지 않는다.
3. 위 2번이 실제 `AgentRegistry`/`AgentScheduler` 구현체(Fake 아님)로
   통합 테스트로 증명된다.
4. 기존 `EventBus`/`AgentRegistry`/`AgentScheduler`/`CodingAgent`의
   다른 계약은 변경되지 않는다.
5. 전체 `pytest`/`ruff`/`mypy` 통과.

**Task List**(2026-07-26 확정, 사용자 최종 승인 — 구현/구현/Integration
Test/문서화+Review 4단계 패턴, 이후 Milestone에도 동일 패턴 적용)

| Task | 내용 | 상태 |
|---|---|---|
| M13-T01 | `is_agent_selected()` 헬퍼 정의 | **완료** |
| M13-T02 | `CodingAgent`에 선택적 Scheduler 가드 적용 | **완료** |
| M13-T03 | End-to-End 통합 테스트 | **완료** |
| M13-T04 | 문서화 + Milestone 13 Review | **완료** |

**진행 상태**: M13-T01~T04 전체 완료. 아래 "Milestone 13 Review" 참고.

#### M13-T01: `is_agent_selected()` 헬퍼 정의
- 목적: "이 Agent가 이번에 Scheduler에게 선택됐는가"를 판별하는 순수
  함수를 만든다.
- 작업 내용: `agents/scheduling.py`에 `is_agent_selected(agent_registry:
  AgentRegistry, agent_scheduler: AgentScheduler, capability:
  AgentCapability, agent_id: str) -> bool` 추가 — `agent_registry.
  list_active()`로 후보를 모으고 `agent_scheduler.select(candidates,
  capability, max_count=1)`로 선택된 Agent의 `agent_id`가 인자로 받은
  `agent_id`와 같은지 비교한다. 기존 `find_agent_by_capability()`와
  나란히 두는 순수 함수(side-effect 없음).
- 완료 조건(DoD): 후보가 여러 개일 때 선택된 것만 True, 나머지는
  False임을 확인하는 단위 테스트(Fake `AgentRegistry`/`AgentScheduler`
  사용)가 통과한다.
- 상태: **DONE (2026-07-26)** — `agents/scheduling.py`에
  `is_agent_selected()` 추가. 새 로직을 만들지 않고 기존
  `find_agent_by_capability()`를 그대로 재사용해 "선택된 Agent의
  agent_id와 같은가"만 비교(Surgical Changes). `tests/agents/
  test_scheduling.py` 신규 — 후보 2개 중 선택된 것만 True/나머지
  False, Capability를 만족하는 후보가 아예 없을 때 False, 후보가
  1개뿐일 때 True(항상 선택됨) 4개 테스트. `ruff check src tests`,
  `mypy src`, `pytest`(469개, 기존 465개 + 신규 4개) 모두 통과. 다음
  Task: **M13-T02**(`CodingAgent`에 선택적 Scheduler 가드 적용).
- 의존성: 없음(기존 Interface만 사용).

#### M13-T02: `CodingAgent`에 선택적 Scheduler 가드 적용
- 목적: 여러 `CodingAgent` 인스턴스가 등록돼 있어도 Scheduler가 고른
  것만 실제로 일하게 한다.
- 작업 내용: `CodingAgent.__init__`에 `agent_registry: AgentRegistry |
  None = None`, `agent_scheduler: AgentScheduler | None = None` 추가.
  `_on_mission_planned()` 맨 앞에서 두 인자가 모두 주어졌을 때만
  `is_agent_selected(...)`를 확인하고, False면 Task/Event에 아무 영향
  없이 바로 return한다.
- 완료 조건(DoD): (a) 둘 다 주지 않으면 기존 테스트 전부 회귀 없이
  통과(Milestone DoD 1번), (b) 선택되지 않은 인스턴스는 Task 상태도
  Event도 건드리지 않음을 단위 테스트로 확인.
- 상태: **DONE (2026-07-26)** — `CodingAgent.__init__`에
  `agent_registry: AgentRegistry | None = None`, `agent_scheduler:
  AgentScheduler | None = None` 추가. `_on_mission_planned()` 맨
  앞에서 둘 다 주어졌을 때만 `is_agent_selected(...)`를 확인해 False면
  즉시 return. 기존 6개 테스트(모두 `agent_registry`/`agent_scheduler`
  미지정)가 전혀 손대지 않은 채로 그대로 통과해 회귀 없음을 실증
  (Milestone DoD 1번). `tests/agents/test_coding_agent.py`에
  `test_coding_agent_ignores_mission_planned_when_not_selected_by_
  scheduler` 신규 — 같은 `agent_manager`/`agent_registry`를 공유하는
  `CodingAgent` 2개를 등록하고(agent_id 충돌 방지를 위해
  `FakeAgentManager`도 공유), `MissionPlanned` 발행 후
  `engine_runtime.received_tasks`가 1개뿐임과 Task 상태가 `REVIEW`로
  정확히 한 번만 전이됐음을 확인. `ruff check src tests`, `mypy src`,
  `pytest`(470개, 기존 469개 + 신규 1개) 모두 통과. 다음 Task:
  **M13-T03**(End-to-End 통합 테스트).
- 의존성: M13-T01.

#### M13-T03: End-to-End 통합 테스트
- 목적: 실제 구현체(Fake 아님)로 전체 시나리오를 증명한다.
- 작업 내용: `tests/integration/`에 같은 `AgentRegistry`/
  `AgentScheduler`(`InMemoryAgentRegistry`/`InMemoryAgentScheduler`)를
  공유하는 `CodingAgent` 2개를 등록하고, 하나의 `MissionPlanned`
  Event에 대해 Scheduler가 고른 1개만 `engine_runtime.run()`을
  호출하고 Task를 전이시키며 `CodeCompleted`를 발행함을, 나머지 1개는
  아무 것도 하지 않음을 증명한다.
- 완료 조건(DoD): Milestone DoD 2·3번이 통합 테스트로 직접 증명된다.
- 상태: **DONE (2026-07-26)** — `tests/integration/
  test_m13_multi_agent_collaboration.py` 신규. `InMemoryAgentManager`/
  `InMemoryAgentRegistry`/`InMemoryAgentScheduler`(전부 프로덕션
  구현체, Fake 아님)를 공유하는 `CodingAgent` 2개를 등록하고
  `MissionPlanned` 1회 발행 후 `CodeCompleted`가 정확히 1번만
  발행되고 Task가 `REVIEW`로 전이됨을 확인
  (`test_only_scheduler_selected_coding_agent_processes_mission_
  planned`). 가드가 켜져 있어도 등록된 Agent가 1개뿐이면 항상 자기
  자신이 선택돼 정상 동작함도 함께 확인
  (`test_single_registered_coding_agent_still_works_with_guard_
  enabled`). `ruff check src tests`, `mypy src`, `pytest`(472개,
  기존 470개 + 신규 2개) 모두 통과. 다음 Task: **M13-T04**(문서화 +
  Milestone 13 Review).
- 의존성: M13-T02.

#### M13-T04: 문서화 + Milestone 13 Review
- 목적: 문서와 구현을 일치시키고 Milestone 종료 승인을 받는다.
- 작업 내용: `docs/ARCHITECTURE.md`에 Scheduler 가드 메커니즘 반영
  (§3.4 Agent Scheduler 또는 §3.6 Agents 소절 갱신 — 착수 시 재검토),
  `docs/ROADMAP.md`/`.ai/MEMORY.md` 갱신, 전체 테스트 결과 정리 및
  제시.
- 완료 조건(DoD): 문서-구현 정합성 확인 + 사용자 승인.
- 상태: **DONE (2026-07-26)** — `docs/ARCHITECTURE.md` v0.15.0 §3.4
  (Agent Scheduler 소절에 "선택이 실제로 개입을 가르는 자가 확인
  가드" 서술 추가 — `is_agent_selected()` 메커니즘, `CodingAgent`가
  최초 채택), 문서 헤더(버전/상태) 갱신. §9는 신규 파일/디렉터리가
  없어(기존 `agents/scheduling.py`, `agents/coding_agent.py`만 수정)
  변경하지 않음. `docs/ROADMAP.md` Milestone 13 절 Task List 상태
  갱신. 새 최상위 Interface를 추가하지 않아(`is_agent_selected()`는
  순수 함수, `CodingAgent`는 선택적 매개변수만 추가) 신규 ADR은
  작성하지 않음(M6~M10/M12와 동일 패턴). 아래 "Milestone 13 Review"
  절 참고.
- 의존성: M13-T01~T03.

---

## Milestone 13 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `agent_registry`/`agent_scheduler` 미주입 시 `CodingAgent` 기존과 완전히 동일 | ✅ (M13-T02, 기존 6개 테스트 무변경 통과) |
| 2 | 같은 CODING Capability의 `CodingAgent` 2개 중 Scheduler가 고른 1개만 처리 | ✅ (M13-T02 단위 테스트, M13-T03 E2E) |
| 3 | 실제 `AgentRegistry`/`AgentScheduler` 구현체(Fake 아님)로 통합 테스트 증명 | ✅ (M13-T03) |
| 4 | 기존 `EventBus`/`AgentRegistry`/`AgentScheduler`/`CodingAgent` 다른 계약 무변경 | ✅ (아래 2절) |
| 5 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M13-T01~T04) 전체 완료. 사용자 승인 조건("Scheduler가 실제로
Agent를 고른다", 4단계 Task 패턴) 그대로 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: 없음 — `is_agent_selected()`는 기존
  `agents/scheduling.py`에 함수 하나만 추가됐다.
- **변경된 기존 컴포넌트**: `CodingAgent`(생성자에 `agent_registry`/
  `agent_scheduler` 선택적 매개변수 추가, `_on_mission_planned()`
  맨 앞에 가드 3줄 추가) 하나뿐. `AgentRegistry`/`AgentScheduler`
  계약, `EventBus` 계약, `find_agent_by_capability()` 모두 M1~M12
  그대로 무변경.
- **핵심 설계 결정**: 새로운 중앙 디스패처 없이 "자가 확인 가드"
  패턴을 택했다 — `AgentScheduler.select()`가 결정적이라는 전제 하에,
  같은 후보 목록으로 같은 질문을 하는 모든 Agent 인스턴스가 항상
  같은 결론에 도달한다는 성질을 이용했다. 이 덕분에 Event/payload
  계약을 전혀 바꾸지 않고(예: "선택된 agent_id"를 payload에 싣는
  방식은 채택하지 않음) 기존 Event 기반 협업 구조(§5)를 그대로
  유지하면서 Scheduler 선택을 실제로 의미 있게 만들었다.

`git diff --stat`(M12 종료 커밋 대비)로 확인한 결과 신규 소스 파일
0개, 기존 소스 파일 수정 2개(`agents/scheduling.py`,
`agents/coding_agent.py`) — M12(신규 1개)보다도 좁고, M9(수정 1개)에
버금가는 M1 이후 가장 작은 변경 폭 중 하나였다.

**3. Interface First 원칙 검토**

**M13은 새 최상위 Interface를 추가하지 않았다**(M6/M7/M8/M9/M10/M12와
동일 패턴, M5/M11만 예외). `is_agent_selected()`는 ABC가 아닌 순수
함수이고, `CodingAgent`의 새 매개변수는 둘 다 기본값 `None`이라 기존
호출부(수십 곳) 시그니처 호환성이 100% 유지된다.

**4. 테스트 결과**

- `pytest`: **472개 전부 통과**(M12 완료 시점 465개 → M13에서 7개
  신규: M13-T01 +4, M13-T02 +1, M13-T03 +2)
- `ruff check src tests`: 클린
- `mypy src`: 클린(86개 소스 파일, 신규 소스 파일 0개)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M13 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- Provider/Model Routing(이미 M6에서 다룸, M13과 무관)
- 병렬 실행
- Scheduler 선택 정책 고도화(우선순위/부하 기반 — 기존 "첫 매치" 그대로)
- `CodingAgent` 외 다른 Agent(Review/Documentation 등)로의 확장 —
  이번 MVP가 검증한 패턴은 재사용 가능하지만, 실제 다중 인스턴스
  요구가 생기기 전까지 확장하지 않는다(YAGNI).

*계속 이월되는 기존 항목*
- Model/Effort 수준 라우팅(M6 Review 최초 이월)
- `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임워크 미통합
- Codex/Gemini CLI 실제 바이너리 미검증(이 세션 환경엔 CLI 없음)
- `MemoryEngine.search()` 선형 스캔
- Retry Backoff/Persistent Runtime Recovery/Approval 비동기 처리/
  Process Timeout 정책 고도화, `ShellAgent` 화이트리스트가 코드에 고정

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M13-T01~T04 상세 섹션) / `docs/ROADMAP.md`
(M13 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.15.0, §3.4
갱신) 완료. 새 Interface가 없어 `.ai/DECISIONS.md`에 신규 ADR을
추가하지 않았다. `pyproject.toml` 버전은 v0.5.0 그대로 유지(ADR-0024
기준선 — `CodingAgent`의 선택적 매개변수 추가는 기존 계약을 바꾸지
않아 기준선 재선언 대상이 아님). `.ai/MEMORY.md`는 이 Review 승인
직후 M1~M12와 동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 신규 소스
0개·수정 2개, "자가 확인 가드" 설계 결정 명시), Interface First 검토
완료(3절, 새 Interface 0개·기존 호출부 100% 호환), 테스트 결과 문서화
완료(4절), Technical Debt 정리 완료(5절), 문서 갱신 완료(6절) — 6개
조건 모두 만족. Review 중 코드 변경이 필요한 치명적 문제(버그·계약
위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 13 Completed를 선언한다.**

**Milestone 13 종료 — 2026-07-26 사용자 승인.**

**Milestone 14 상태**: 착수 확정. 아래 "Milestone 14" 절 참고.

---

## Milestone 14 — LLM Routing (Model 수준 라우팅)

**목표**: `AgentSession.llm_policy_decision`의 `model`(예: opus/sonnet/
haiku)이 `ClaudeCodeEngineAdapter`의 실제 `--model` 실행 인자까지
전달되게 한다(MVP, 2026-07-26 사용자 확정).

> **설계 검토에서 발견한 사실**: M6에서 완성한 것은 **Provider 단위**
> 라우팅(Claude Code/Codex/Gemini 중 어떤 CLI를 쓸지)뿐이었다.
> `LLMPolicyDecision`은 `model`(opus/sonnet/haiku 등)과 `effort`(low/
> medium/high)도 담고 있지만, `EngineAdapter.run(session_id, task)`와
> `EngineRuntime.run(task, required_capabilities)` 어디에도 이 값을
> 전달할 자리가 없어 지금까지 한 번도 실제 실행에 반영된 적이 없었다
> (M6 Review 최초 이월, M10에서도 "Interface 변경이 필요한 무거운
> 작업"으로 재확인·재이월).

**범위(사용자 확정)**: **Model만** 다루고 **Effort는 이번 범위에서
뺀다** — `ClaudeCodeEngineAdapter`는 이미 `--model` CLI 플래그와
연결된 `model` 생성자 필드가 있어(M3-T02) 실제로 연결할 지점이
있지만, `effort`는 Claude Code CLI에 대응하는 플래그가 없어 지금
연결하면 검증 불가능한 상태가 된다. **적용 대상은
`ClaudeCodeEngineAdapter`만** — Codex/Gemini(`CLIProvider` 계열)는
이 환경에 CLI가 없어 검증이 불가능해(M5-T05/M10에서 반복 확인) 계약만
만족하도록(받되 무시) 남겨둔다.

**설계 방향**: `EngineAdapter.run()`/`EngineRuntime.run()`(둘 다
인터페이스) 시그니처에 `model: str | None = None`을 선택적으로
추가한다. 기존 호출부는 `model`을 안 주면 100% 그대로 동작한다.
`ClaudeCodeEngineAdapter`는 `run()`에 전달된 `model`을 생성자의 고정
`model`보다 우선 사용한다. `ManagedEngineRuntime`/
`RecoveringEngineRuntime`(둘 다 `EngineRuntime` 구현체)은 이 값을
그대로 다음 계층에 전달만 한다(새 로직 없음). `CodingAgent`/
`ReviewAgent`/`DocumentationAgent` 3개 Agent가
`llm_policy_decision.model.name`을 `engine_runtime.run()`에 함께
전달하도록 연결한다.

**Non-goal(범위 밖)**: Effort 라우팅, Codex/Gemini 실연동, Scheduler
정책 고도화, Provider 단위 라우팅 재작업(M6에서 이미 완료).

**Milestone Definition of Done**
1. `model`을 넘기지 않으면 기존과 완전히 동일하게 동작한다(회귀 없음).
2. `ClaudeCodeEngineAdapter`가 `run()`에 전달된 `model`을 생성자
   기본값보다 우선 사용해 실제 명령에 반영한다.
3. `ManagedEngineRuntime`/`RecoveringEngineRuntime`이 `model`을 그대로
   다음 계층에 전달한다(새 선택 로직 없음).
4. `CodingAgent`/`ReviewAgent`/`DocumentationAgent`가 정책의
   `model.name`을 실제로 `engine_runtime.run()`에 전달함이 통합
   테스트로 증명된다.
5. 전체 `pytest`/`ruff`/`mypy` 통과.

**Task List**(2026-07-26 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M14-T01 | `EngineAdapter`/`EngineRuntime` 계약에 `model` 선택적 파라미터 확장 | **완료** |
| M14-T02 | 구현체 갱신(`ClaudeCodeEngineAdapter` 실제 반영, Runtime들은 전달만) | **완료** |
| M14-T03 | Agent 3종 연결 + End-to-End 통합 테스트 | **완료** |
| M14-T04 | 문서화 + Milestone 14 Review | **완료** |

**진행 상태**: M14-T01~T04 전체 완료. 아래 "Milestone 14 Review" 참고.

#### M14-T01: `EngineAdapter`/`EngineRuntime` 계약에 `model` 선택적 파라미터 확장
- 목적: Model을 실행 계층까지 전달할 수 있는 통로를 계약에 마련한다
  (Interface First).
- 작업 내용: `interfaces/engine_adapter.py`의 `run(self, session_id:
  str, task: Task) -> EngineResult`에 `model: str | None = None` 추가.
  `interfaces/engine_runtime.py`의 `run(self, task, required_
  capabilities=frozenset()) -> EngineResult`와 `run_parallel(...)`에도
  동일하게 `model: str | None = None` 추가(대칭성 유지, 병렬 경로도
  계약상 빠지지 않도록). `tests/interfaces/fakes.py`의
  `FakeEngineAdapter`/`FailingFakeEngineAdapter`/`FakeEngineRuntime`을
  새 시그니처에 맞게 갱신(받되 무시 — 이번 Task는 계약만 확장, 실제
  사용은 M14-T02~T03).
- 완료 조건(DoD): 기존 계약 테스트가 시그니처 갱신 후에도 회귀 없이
  통과한다. `model`을 생략해도 기존과 동일하게 동작함을 계약 테스트로
  확인한다(Milestone DoD 1번 착수).
- 상태: **DONE (2026-07-26)** — `interfaces/engine_adapter.py`의
  `run()`, `interfaces/engine_runtime.py`의 `run()`/`run_parallel()`에
  `model: str | None = None`(키워드 전용) 추가. `EngineAdapter`
  구현체 4종(`MockEngineAdapter`/`ClaudeCodeEngineAdapter`/
  `CLIEngineAdapter`/`FakeEngineAdapter`/`FailingFakeEngineAdapter`)과
  `EngineRuntime` 구현체 3종(`InMemoryEngineRuntime`/
  `ManagedEngineRuntime`/`RecoveringEngineRuntime`/`FakeEngineRuntime`)
  모두 새 시그니처를 받도록 갱신했으나, **이번 Task는 계약 확장까지만**
  — 실제 `model` 사용/전달 로직은 아직 넣지 않았다(`Fake` 계열만 예외
  — 계약 테스트에서 전달 여부를 확인할 수 있도록 `FakeEngineAdapter`가
  `received_models`에 기록하고 `FakeEngineRuntime`이 선택된 Adapter에
  그대로 전달하도록 함). `tests/interfaces/test_engine_adapter.py`/
  `test_engine_runtime.py`에 4개 신규 테스트(model 생략 시 `None`
  기록/명시적 model 기록, Runtime→Adapter 전달 확인) — Milestone DoD
  1번을 Fake 계층에서 먼저 증명. `tests/interfaces/test_engine_runtime.py`
  의 로컬 `SelectivelyFailingAdapter` 테스트 더블도 새 시그니처에 맞춰
  갱신(기존 M10-T01 테스트 회귀 없음 확인). `ruff check src tests`,
  `mypy src`, `pytest`(476개, 기존 472개 + 신규 4개) 모두 통과. 다음
  Task: **M14-T02**(구현체 갱신 — `ClaudeCodeEngineAdapter` 실제 반영,
  프로덕션 Runtime들의 실제 전달 로직).
- 의존성: 없음.

#### M14-T02: 구현체 갱신
- 목적: `ClaudeCodeEngineAdapter`가 `model`을 실제로 반영하고,
  `EngineRuntime` 구현체들은 이를 다음 계층까지 그대로 전달한다.
- 작업 내용: `ClaudeCodeEngineAdapter.run()`이 인자로 받은 `model`이
  있으면 `_build_command()`에서 생성자 `self._model`보다 우선
  사용하도록 변경. `CLIEngineAdapter`/`MockEngineAdapter`는 `model`을
  받되 무시(범위 밖, docstring에 명시). `ManagedEngineRuntime`/
  `RecoveringEngineRuntime`/`InMemoryEngineRuntime`의 `run()`/
  `run_parallel()`이 `model`을 받아 내부 `adapter.run()`/`inner.run()`
  호출에 그대로 전달(새 선택·우선순위 로직 없음).
- 완료 조건(DoD): `ClaudeCodeEngineAdapter`에 대해 `run()`에 전달된
  `model`이 생성자 `model`보다 우선함을 단위 테스트로 확인.
  `ManagedEngineRuntime`/`RecoveringEngineRuntime`이 `model`을
  내부 Adapter 호출까지 정확히 전달함을 단위 테스트로 확인.
- 상태: **DONE (2026-07-26)** — `ClaudeCodeEngineAdapter._build_command()`
  가 `model` 매개변수를 받아 `effective_model = model if model is not
  None else self._model`로 우선순위를 정하도록 변경(`run()`이 이를
  전달). `MockEngineAdapter`/`CLIEngineAdapter`는 `model`을 받되
  사용하지 않음을 docstring에 명시(범위 밖, Codex/Gemini는 이 환경에서
  검증 불가). `InMemoryEngineRuntime`/`ManagedEngineRuntime`(`_execute()`
  내부 `adapter.run()` 호출과 `run_parallel()`의 `executor.submit()`
  둘 다)/`RecoveringEngineRuntime`(`run()`의 재시도 루프와
  `run_parallel()`의 첫 병렬 패스·개별 재시도 둘 다) 전부 `model`을
  새 선택 로직 없이 다음 계층까지 그대로 전달하도록 수정. 로컬
  duck-typing 테스트 더블(`SelectivelyFailingAdapter`,
  `test_managed_engine_runtime.py`/`test_recovering_engine_runtime.py`
  의 4+2개 어댑터, `ScriptedEngineRuntime`)도 새 시그니처에 맞춰
  일괄 갱신(회귀 없음 확인 목적). `tests/adapters/
  test_claude_code_engine_adapter.py`에 2개(run() model이 생성자
  model보다 우선/model 생략 시 생성자 model로 폴백),
  `tests/runtime/engine/test_managed_engine_runtime.py`에
  `RecordingModelEngineAdapter` 신규 테스트 더블 + 2개(run/run_parallel
  전달 확인), `tests/runtime/engine/test_recovering_engine_runtime.py`
  에 2개(위 더블을 cross-file import해 내부 Runtime까지 전달됨을
  실제 `ManagedEngineRuntime` 조합으로 확인) — 총 6개 신규 테스트.
  `ruff check src tests`, `mypy src`, `pytest`(482개, 기존 476개 +
  신규 6개) 모두 통과. 다음 Task: **M14-T03**(Agent 3종 연결 +
  End-to-End 통합 테스트).
- 의존성: M14-T01.

#### M14-T03: Agent 3종 연결 + End-to-End 통합 테스트
- 목적: Policy가 정한 Model이 실제로 Agent 실행 경로를 통해
  Adapter까지 도달함을 증명한다.
- 작업 내용: `domain/llm_policy.py`에 `model_name(decision)` 헬퍼
  추가(기존 `required_capabilities()`와 나란히 두는 순수 함수 — `None`
  이면 `None` 반환). `CodingAgent`/`ReviewAgent`/`DocumentationAgent`
  가 `engine_runtime.run(..., model=model_name(self._session.
  llm_policy_decision))`을 전달하도록 갱신. `tests/integration/`에
  실제 `docs/llm_policy.example.yaml` 기반 정책으로 `CodingAgent`가
  `ClaudeCodeEngineAdapter`에 전달한 `model`이 정책이 지정한 값과
  일치함을 증명하는 통합 테스트를 추가한다(M6-T03/M13-T03과 동일한
  "실제 정책 파일" 검증 방식).
- 완료 조건(DoD): Milestone DoD 4번이 통합 테스트로 직접 증명된다.
- 상태: **DONE (2026-07-26)** — `domain/llm_policy.py`에 `model_name()`
  추가(`required_capabilities()`와 나란히 두는 순수 함수). `CodingAgent`/
  `ReviewAgent`/`DocumentationAgent` 3개 Agent가
  `engine_runtime.run(..., model=model_name(self._session.
  llm_policy_decision))`을 전달하도록 갱신. 세 Agent 테스트가 공유하는
  `tests/agents/test_coding_agent.py`의 `RecordingEngineRuntime`에
  `received_models` 기록 추가(cross-import로 Review/Documentation
  테스트도 함께 갱신됨). 3개 Agent 전부에 대해 "정책 있으면 model
  전달/정책 없으면 None" 단위 테스트 추가(6개). `domain/llm_policy.py`
  의 `model_name()` 자체도 2개 단위 테스트로 검증.
  `tests/integration/test_m14_llm_model_routing.py` 신규 — M6의
  `test_m6_policy_routing.assemble()`(실제 `docs/llm_policy.example.yaml`
  로드, 6-Agent 실제 파이프라인)을 그대로 재사용해, CODING Role 정책
  (anthropic/opus)에 따라 `ClaudeCodeEngineAdapter`가 실제로 조립한
  명령에 `--model opus`가 포함됨을 증명(Milestone DoD 4번 직접 증명).
  `ruff check src tests`, `mypy src`, `pytest`(489개, 기존 482개 +
  신규 7개) 모두 통과. 다음 Task: **M14-T04**(문서화 + Milestone 14
  Review).
- 의존성: M14-T02.

#### M14-T04: 문서화 + Milestone 14 Review
- 목적: 문서와 구현을 일치시키고 Milestone 종료 승인을 받는다.
- 작업 내용: `docs/ARCHITECTURE.md` §3.9(Engine Runtime)/§3.10(Engine
  Adapter)에 `model` 파라미터 반영, `docs/ROADMAP.md`/`.ai/MEMORY.md`
  갱신, 전체 테스트 결과 정리 및 제시.
- 완료 조건(DoD): 문서-구현 정합성 확인 + 사용자 승인.
- 상태: **DONE (2026-07-26)** — `docs/ARCHITECTURE.md` v0.16.0 §3.9
  (Model 라우팅 — Provider 선택과 다른 층위임을 명시), §3.10(`run()`
  메서드 표에 `model` 반영, Model 라우팅 소절 신규 — 적용 대상/제외
  대상/Effort 범위 제외 이유), 문서 헤더(버전/상태) 갱신. `.ai/
  DECISIONS.md`에 **ADR-0026**(EngineAdapter는 RULES §1.2 보호 자산이라
  계약 확장을 ADR-0009/0015와 동일하게 정식 기록 — 배경/결정 6개 항목/
  대안 3개/이유/결과) 신규 작성. `docs/ROADMAP.md` Milestone 14 절
  Task List 상태 갱신. 아래 "Milestone 14 Review" 절 참고.
- 의존성: M14-T01~T03.

---

## Milestone 14 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `model` 미전달 시 기존과 완전히 동일하게 동작(회귀 없음) | ✅ (M14-T01, 기존 테스트 전부 무변경 통과) |
| 2 | `ClaudeCodeEngineAdapter`가 `run()`의 `model`을 생성자 기본값보다 우선 사용 | ✅ (M14-T02) |
| 3 | `ManagedEngineRuntime`/`RecoveringEngineRuntime`이 `model`을 그대로 전달(새 선택 로직 없음) | ✅ (M14-T02) |
| 4 | Agent 3종이 정책의 `model.name`을 실제로 전달함이 통합 테스트로 증명 | ✅ (M14-T03) |
| 5 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M14-T01~T04) 전체 완료. 사용자 승인 조건("Model만, Effort
제외", "ClaudeCodeEngineAdapter만 적용") 그대로 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: 없음.
- **변경된 기존 컴포넌트**: `interfaces/engine_adapter.py`/
  `interfaces/engine_runtime.py`(계약 확장) + `EngineAdapter` 구현체
  4종(`ClaudeCodeEngineAdapter`만 실제 반영, 나머지 3종은 받되 무시) +
  `EngineRuntime` 구현체 3종(전부 전달만) + Agent 3종
  (`CodingAgent`/`ReviewAgent`/`DocumentationAgent`) + `domain/
  llm_policy.py`(`model_name()` 신규 함수 1개).
- **핵심 설계 결정**: `model`을 `run()` 호출 단위로 전달하는 방식을
  택해(`create_session()` 단위 고정 방식은 기각), 세션 생명주기
  계약(ADR-0015)의 의미를 "세션=고정 모델"로 좁히지 않았다. Provider
  선택(M6, 어떤 Adapter를 쓸지)과 Model 지정(M14, 그 Adapter에 어떤
  모델을 쓰라고 할지)이 서로 다른 층위임을 문서로도 명확히 구분했다.

`git diff --stat`(M13 종료 커밋 대비)로 확인한 결과 신규 소스 파일
0개, 기존 소스 파일 수정 11개(Interface 2개, Adapter 4개, Runtime
3개, Agent 3개, domain 1개 — 일부 중복 집계 있음, 실제로는 총 11개
파일) — M11(신규 2/수정 5)보다 넓은, 이번까지 중 두 번째로 넓은 변경
폭이었다(가장 넓은 것은 M5의 6개 신규 파일).

**3. Interface First 원칙 검토**

**M14는 새 최상위 Interface를 추가하지 않았다**(M6/M7/M8/M9/M10/M12/
M13과 동일 패턴, M5/M11만 예외). 다만 **기존 두 Interface
(`EngineAdapter`/`EngineRuntime`)의 계약을 확장**했다는 점에서
M6~M13과는 다르다 — ADR-0009/ADR-0015가 과거 `EngineAdapter` 계약을
확장했던 것과 같은 종류의 결정이라 ADR-0026으로 정식 기록했다
(RULES §1.2가 `EngineAdapter`를 핵심 보호 자산으로 명시하기 때문).
새 매개변수는 전부 기본값이 있는 키워드 전용 인자라 기존 호출부
(수십 곳) 시그니처 호환성은 100% 유지된다.

**4. 테스트 결과**

- `pytest`: **489개 전부 통과**(M13 완료 시점 472개 → M14에서 17개
  신규: M14-T01 +4, M14-T02 +6, M14-T03 +7)
- `ruff check src tests`: 클린
- `mypy src`: 클린(86개 소스 파일, 신규 소스 파일 0개)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M14 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- **Effort 라우팅** — Claude Code CLI에 대응하는 플래그가 없어 검증
  불가능한 상태가 되는 것을 피하기 위해 의도적으로 제외. 실제 대응
  지점이 생기면 재검토.
- **Codex/Gemini 실연동** — 이 세션 환경에 CLI 바이너리가 없어 계속
  이월(M5-T05/M10과 동일 사유).

*계속 이월되는 기존 항목*
- `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임워크 미통합
- `MemoryEngine.search()` 선형 스캔
- Retry Backoff/Persistent Runtime Recovery/Approval 비동기 처리/
  Process Timeout 정책 고도화, `ShellAgent` 화이트리스트가 코드에 고정

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M14-T01~T04 상세 섹션) / `docs/ROADMAP.md`
(M14 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.16.0, §3.9/
§3.10 갱신) / `.ai/DECISIONS.md`(ADR-0026 신규) 완료. `pyproject.toml`
버전은 v0.5.0 그대로 유지(ADR-0024 기준선 — 새 최상위 Interface나
계층 구조 변경이 아니라 기존 두 Interface의 계약 확장이라 기준선
재선언 대상이 아님). `.ai/MEMORY.md`는 이 Review 승인 직후 M1~M13과
동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 신규 0/
수정 11 소스 파일, "run() 호출 단위 model 전달" 설계 결정 명시),
Interface First 검토 완료(3절, 새 Interface는 0개이나 기존 2개 계약
확장을 ADR로 투명하게 기록), 테스트 결과 문서화 완료(4절), Technical
Debt 정리 완료(5절), 문서 갱신 완료(6절) — 6개 조건 모두 만족. Review
중 코드 변경이 필요한 치명적 문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 14 Completed를 선언한다.**

**Milestone 14 종료 — 2026-07-26 사용자 승인.**

**Milestone 15 상태**: 착수 확정. 아래 "Milestone 15" 절 참고.

---

## Milestone 15 — Token & Cost Optimization

**목표**: `EngineAdapter.estimate_cost()`가 실제로 사용되는 Workspace
차원의 Budget(예산) 정책을 도입해, Task를 실행하기 **전에** 예상
비용/토큰을 확인하고 예산을 초과하면 실행을 막는다. Provider(Claude/
GPT/Gemini)에 상관없이 동일하게 동작해야 한다(2026-07-27 사용자 확정).

> **설계 검토에서 발견한 사실**: `EngineAdapter.estimate_cost(task) ->
> CostEstimate`는 M3부터 이미 존재하고 `ClaudeCodeEngineAdapter`/
> `CLIEngineAdapter`/`MockEngineAdapter` 모두 구현하고 있었지만,
> `EngineRuntime`도 어떤 Agent도 이를 호출한 적이 없었다 — M12의
> `WorkflowEngine.plan()`, M13의 `AgentScheduler.select()`와 동일한
> "만들어졌지만 쓰인 적 없는 기능" 패턴. M15는 새 추정 로직을 새로
> 만드는 게 아니라, 이미 있는 `estimate_cost()`를 실제로 활용하는
> Workspace 정책을 얹는 작업이다.

**설계 방향**: Provider와 무관한 순수 domain 객체 `Budget`/
`BudgetDecision`(`domain/budget.py`)을 새로 정의한다. `BudgetPolicyEngine`
Interface(`LLMPolicyEngine`과 동일한 설계 원칙 — 규칙 기반, side-effect
없음, 정책 없으면 허용)를 신설하고 `InMemoryBudgetPolicyEngine`으로
최소 구현한다. `EngineRuntime`에 세션을 만들지 않고 예상 비용을 조회할
수 있는 `estimate_cost(task, required_capabilities) -> CostEstimate`를
추가한다(기존 계약 확장, ADR 필요 여부는 M15-T04에서 판단). `CodingAgent`
가 실행 직전 `estimate_cost()` → `BudgetPolicyEngine.check()`를 거쳐
초과 시 실행하지 않는 경로를 선택적으로(DI 기본값 None) 가진다.

**Non-goal(범위 밖)**: 실제 API 과금 조회/실시간 가격표 연동, Memory
Engine, Knowledge Base, MCP, Approval(예산 초과 시 승인 요청 흐름),
Retry, Dashboard, Provider별 과금 API 연동, 예산 누적 추적(Task 단위
개별 확인만, 여러 Task에 걸친 소비량 합산은 범위 밖).

**Milestone Definition of Done**
1. `Budget`/`BudgetDecision` domain 객체가 어떤 Provider에도 속하지
   않는다(Provider 독립 검증).
2. `BudgetPolicyEngine`이 `LLMPolicyEngine`과 동일하게 side-effect
   없이 동작하고, 정책이 없으면(예산 미설정) 항상 허용한다(하위 호환).
3. `EngineRuntime.estimate_cost()`가 세션을 만들지 않고 `run()`과
   동일한 엔진 선택 로직으로 `CostEstimate`를 반환한다.
4. `CodingAgent`가 예산 초과 시 Approval/Retry 없이 실행을 막음이
   통합 테스트로 증명된다.
5. `estimate_cost()`/Budget을 지정하지 않으면 기존과 완전히 동일하게
   동작한다(회귀 없음).
6. 전체 `pytest`/`ruff`/`mypy` 통과.

**Task List**(2026-07-27 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M15-T01 | `Budget`/`BudgetDecision` domain + `BudgetPolicyEngine` Interface + `InMemoryBudgetPolicyEngine` | **완료** |
| M15-T02 | `EngineRuntime.estimate_cost()` 추가 + `CodingAgent` 연동 | **완료** |
| M15-T03 | End-to-End 통합 테스트 | **완료** |
| M15-T04 | 문서화 + Milestone 15 Review | **완료** |

**진행 상태**: M15-T01~T04 전체 완료. 아래 "Milestone 15 Review" 참고.

#### M15-T01: `Budget`/`BudgetDecision` domain + `BudgetPolicyEngine` Interface + 구현체
- 상태: **DONE (2026-07-27)** — `domain/budget.py`에 `Budget`
  (max_tokens/max_cost_usd, 둘 다 선택적)/`BudgetDecision`(allowed/
  reason) 신규(Provider 독립, 어떤 Provider/Engine 개념도 참조하지
  않음). `interfaces/budget_policy_engine.py`에 `BudgetPolicyEngine`
  Interface 신규(`LLMPolicyEngine`과 동일한 설계 원칙 — side-effect
  없음, `check(estimate) -> BudgetDecision`). `engines/
  budget_policy_engine.py`에 `InMemoryBudgetPolicyEngine` 최소
  구현체(단일 `Budget` 보관, `budget=None`이면 항상 허용). `tests/
  interfaces/fakes.py`에 `FakeBudgetPolicyEngine` 추가. 단위 테스트
  9개(domain 4개, engine 5개) 신규. `pytest`(498개), `ruff`, `mypy`
  통과. 다음 Task: **M15-T02**.
- 의존성: 없음.

#### M15-T02: `EngineRuntime.estimate_cost()` + `CodingAgent` 연동
- 상태: **DONE (2026-07-27)** — `interfaces/engine_runtime.py`에
  `estimate_cost(task, required_capabilities) -> CostEstimate` 추가
  (`run()`과 동일한 엔진 선택 규칙, 세션 미생성). `InMemoryEngineRuntime`/
  `ManagedEngineRuntime`이 각자의 어댑터 선택 로직을 재사용해 구현,
  `RecoveringEngineRuntime`은 `inner.estimate_cost()`에 순수 위임(read-
  only라 재시도 불필요). `FakeEngineRuntime`/`RecordingEngineRuntime`/
  `SpyEngineRuntime`/`ScriptedEngineRuntime` 등 기존 `EngineRuntime`
  테스트 더블 전부 새 추상 메서드에 맞춰 갱신(M14에서 겪은 "ABC
  인스턴스화 실패" 재발 방지). `CodingAgent`에 선택적
  `budget_policy_engine` DI 추가 — `_on_mission_planned()`에서 실행
  직전 `engine_runtime.estimate_cost()` → `BudgetPolicyEngine.check()`
  를 거쳐, 초과 시 `Task`를 `BLOCKED`로 전환하고 `return`(Approval/
  Retry 없음, M13 Scheduler 가드와 동일한 "조용히 멈춤" 패턴).
  미주입 시(기본값 `None`) 이 확인 자체를 건너뛴다. 단위 테스트
  10개 신규(`EngineRuntime` 계약 2개, `ManagedEngineRuntime` 2개,
  `RecoveringEngineRuntime` 1개, `InMemoryEngineRuntime` 2개,
  `CodingAgent` 3개 — 예산 없음/예산 내/예산 초과). `pytest`(508개),
  `ruff`, `mypy` 통과. 다음 Task: **M15-T03**(End-to-End 통합 테스트).
- 의존성: M15-T01.

#### M15-T03: End-to-End 통합 테스트
- 상태: **DONE (2026-07-27)** — `tests/integration/
  test_m15_token_cost_optimization.py` 신규. 실제 `ManagedEngineRuntime`
  + 실제 `ClaudeCodeEngineAdapter`(M15가 새로 만든 로직 없음, M3/M14의
  기존 구현 그대로) + 실제 `CodingAgent`에 `InMemoryBudgetPolicyEngine`
  을 주입해 3가지 시나리오를 검증: (1) 예산 내(`max_tokens=10_000`) —
  `ClaudeCodeEngineAdapter`가 실제로 1회 실행되고 `CodeCompleted`가
  발행되며 Task가 `REVIEW`로 전환됨(Milestone DoD 4번 허용 경로),
  (2) 예산 초과(`max_tokens=1`) — `ClaudeCodeEngineAdapter`가 아예
  호출되지 않고(`executed_commands == []`) Task가 `BLOCKED`로 전환,
  `CodeCompleted`도 발행되지 않음(Milestone DoD 4번 차단 경로, Approval/
  Retry 없이 단순 차단), (3) `budget_policy_engine` 미주입 — M15 이전과
  완전히 동일하게 동작(Milestone DoD 5번). 프로세스 경계만 M11-T03과
  동일하게 `FakeExecutionEnvironment`로 대체하고, 그 외에는 전부 실제
  구현체를 조립했다(M6/M13/M14가 확립한 "진짜 컴포넌트로 조립" 통합
  테스트 방식). `pytest`(511개, 기존 508개 + 신규 3개), `ruff`, `mypy`
  통과. 다음 Task: **M15-T04**(문서화 + Milestone 15 Review).
- 의존성: M15-T02.

#### M15-T04: 문서화 + Milestone 15 Review
- 목적: 문서와 구현을 일치시키고 Milestone 종료 승인을 받는다.
- 작업 내용: `docs/ARCHITECTURE.md` §3.6/§3.9(estimate_cost 반영) +
  신규 §3.13(Budget Policy) + §7(Interfaces 18→19종) 갱신, `.ai/
  DECISIONS.md`에 ADR-0027 신규(`EngineRuntime`은 §1.2 보호 자산이라
  계약 확장을 ADR-0009/0015/0026과 동일하게 기록), `docs/ROADMAP.md`/
  `.ai/MEMORY.md` 갱신, 전체 테스트 결과 정리 및 Review 작성.
- 완료 조건(DoD): 문서-구현 정합성 확인 + 사용자 승인.
- 상태: **DONE (2026-07-27)** — `docs/ARCHITECTURE.md` v0.17.0
  §3.6(Agents, CodingAgent budget_policy_engine 한 줄 요약)/§3.9
  (Engine Runtime, "비용 사전 조회(M15, ADR-0027)" 신규 문단)/신규
  §3.13(Budget Policy — domain 객체/구현체/연동 지점/Provider 독립
  근거)/§7(Interfaces 총 19종, `BudgetPolicyEngine` 행 추가,
  `EngineRuntime` 행에 "비용 사전 조회(M15)" 반영)/§9(interfaces
  디렉터리 주석 19종으로 갱신). `.ai/DECISIONS.md`에 **ADR-0027**
  (배경/결정 6개 항목/대안 4개/이유/결과) 신규 작성. 아래 "Milestone
  15 Review" 절 참고.
- 의존성: M15-T01~T03.

---

## Milestone 15 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `Budget`/`BudgetDecision`이 Provider 독립 | ✅ (M15-T01, 어떤 Provider/Engine 개념도 참조하지 않음) |
| 2 | `BudgetPolicyEngine`이 side-effect 없이 동작, 정책 없으면 항상 허용 | ✅ (M15-T01) |
| 3 | `EngineRuntime.estimate_cost()`가 세션 없이 `CostEstimate` 반환 | ✅ (M15-T02) |
| 4 | `CodingAgent`가 예산 초과 시 실행을 막음이 통합 테스트로 증명 | ✅ (M15-T03) |
| 5 | Budget 미지정 시 기존과 완전히 동일하게 동작(회귀 없음) | ✅ (M15-T02/T03) |
| 6 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M15-T01~T04) 전체 완료. 사용자 승인 조건("실제 API 비용
계산/실시간 과금 조회는 하지 않음", "Memory Engine/Knowledge Base/
MCP/Approval/Retry/Dashboard 범위 밖") 그대로 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `domain/budget.py`(`Budget`/`BudgetDecision`),
  `interfaces/budget_policy_engine.py`(`BudgetPolicyEngine`),
  `engines/budget_policy_engine.py`(`InMemoryBudgetPolicyEngine`).
- **변경된 기존 컴포넌트**: `interfaces/engine_runtime.py`(계약 확장,
  `estimate_cost()` 추가) + `EngineRuntime` 구현체 3종
  (`InMemoryEngineRuntime`/`ManagedEngineRuntime`/
  `RecoveringEngineRuntime`) + `CodingAgent`(선택적
  `budget_policy_engine` DI).
- **핵심 설계 결정**: `estimate_cost()`를 `EngineRuntime` 계약에
  두어 `run()`과 동일한 엔진 선택 규칙을 그대로 재사용하게 했다 —
  Agent가 이미 계산한 `required_capabilities`를 그대로 넘기면 실제로
  선택될 Adapter와 항상 같은 Adapter의 추정치를 얻는다는 보장이
  자연히 성립한다. `BudgetPolicyEngine`을 `LLMPolicyEngine`과 분리된
  별도 Interface로 둔 것은 SRP 때문이다 — 하나는 "어떤 Provider/
  Model을 쓸지" 결정하고, 다른 하나는 "이 비용이 예산 안인지"만
  검사한다. 두 정책을 하나로 합치면 서로 다른 두 질문에 답하는
  결합이 생긴다.

`git diff --stat`(M14 종료 커밋 대비)로 확인한 결과 신규 소스 파일
3개(`domain/budget.py`, `interfaces/budget_policy_engine.py`,
`engines/budget_policy_engine.py`), 기존 소스 파일 수정 5개
(`EngineRuntime` Interface 1개, 구현체 3개, `CodingAgent` 1개) —
M11(신규 2/수정 5)과 비슷한 규모, M14(신규 0/수정 11)보다 신규 파일은
많지만 수정 파일은 적다.

**3. Interface First 원칙 검토**

M15는 **새 최상위 Interface(`BudgetPolicyEngine`)를 추가**했다
(M5/M11과 같은 종류). 동시에 **기존 `EngineRuntime` Interface의
계약도 확장**했다(M14가 `EngineAdapter`/`EngineRuntime`에 `model`을
추가한 것과 같은 종류) — 두 성격이 겹치는 첫 Milestone이다.
`EngineRuntime`은 `.ai/RULES.md` §1.2가 보호하는 핵심 아키텍처
자산이라 ADR-0027로 정식 기록했다(ADR-0009/0015/0026과 동일 계열).
새 매개변수(`required_capabilities`)는 기본값이 있는 선택적 인자라
기존 호출부와 100% 호환된다. `BudgetPolicyEngine`은 신설
Interface이므로 기존 코드에 영향이 없다(주입하지 않으면 기존 동작
그대로).

**4. 테스트 결과**

- `pytest`: **511개 전부 통과**(M14 완료 시점 489개 → M15에서 22개
  신규: M15-T01 +9, M15-T02 +10, M15-T03 +3)
- `ruff check src tests`: 클린
- `mypy src`: 클린(신규 소스 파일 3개 포함, 사전에 존재하던
  `storage/llm_policy_loader.py`의 `types-PyYAML` 미설치 경고 1건은
  M15 변경과 무관 — M15 이전부터 존재)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M15 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- **여러 Task에 걸친 누적 예산 추적** — Task 단위 개별 확인만 구현
  (YAGNI, 실제 필요성 미증명).
- **예산 초과 시 Approval 요청 흐름** — 이번엔 단순 차단(BLOCKED)만.
  실제 승인 워크플로가 필요해지면 재검토.
- **실제 API 과금 조회/Provider별 과금 API 연동** — 사용자 확정 범위
  밖, `EngineAdapter.estimate_cost()`의 기존 naive 추정을 그대로 재사용.
- **Effort 기반 비용 차등** — M14에서 Model만 다루기로 확정한 것과
  같은 이유로 이번에도 범위 밖.

*계속 이월되는 기존 항목*
- Effort 라우팅, `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임
  워크 미통합, Codex/Gemini 실연동 미검증, `MemoryEngine.search()`
  선형 스캔, Retry Backoff/Persistent Runtime Recovery/Approval
  비동기 처리/Process Timeout 정책 고도화, `ShellAgent` 화이트리스트
  코드 고정.

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M15-T01~T04 상세 섹션) / `docs/ROADMAP.md`
(M15 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.17.0, §3.6/
§3.9/신규 §3.13/§7/§9 갱신) / `.ai/DECISIONS.md`(ADR-0027 신규) 완료.
`pyproject.toml` 버전은 v0.5.0 그대로 유지(ADR-0024 기준선 — 새
Interface 1개 추가는 M5/M11과 같은 종류의 확장이라 기준선 재선언
대상이 아님, 상위 계층 구조 변경이 아니다). `.ai/MEMORY.md`는 이
Review 승인 직후 M1~M14와 동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 신규 3/
수정 5 소스 파일, "estimate_cost()를 EngineRuntime에 두고 Budget
검사는 별도 Interface로 분리" 설계 결정 명시), Interface First 검토
완료(3절, 새 Interface 1개 + 기존 1개 계약 확장을 ADR로 투명하게
기록), 테스트 결과 문서화 완료(4절), Technical Debt 정리 완료(5절),
문서 갱신 완료(6절) — 6개 조건 모두 만족. Review 중 코드 변경이
필요한 치명적 문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 15 Completed를 선언한다.**

**Milestone 15 종료 — 2026-07-27 사용자 승인.**

**Milestone 16 상태**: 착수 확정. 아래 "Milestone 16" 절 참고.

---

## Milestone 16 — Project Knowledge System (Memory Engine)

**목표**: 프로젝트의 기존 문서(`docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/
`.ai/RULES.md`/`.ai/TASKS.md`/`docs/ROADMAP.md`/`docs/PRD.md`)를 있는
그대로(재작성 없이) Workspace 전용 Knowledge로 노출하고, Agent가 이를
Keyword 기반으로 검색해 실행 컨텍스트에 참고할 수 있게 한다(2026-07-27
사용자 확정). Provider/Engine/Agent 독립 — Claude/GPT/Gemini 어떤
조합이든 같은 Knowledge를 참조한다. ChatGPT Memory나 Chat History가
아니다.

> **설계 검토에서 발견한 사실**: `interfaces/memory_engine.py`의
> `MemoryEngine`은 M1부터 이미 존재하지만, `ContextManager`가 감싸서
> **Mission 요약/세션 연속성**(M8-T03)에 쓰는 완전히 다른 개념이다.
> 이름을 재사용하면 "세션 기억"과 "프로젝트 지식"이 섞이므로, 이번
> Milestone은 `KnowledgeRepository`/`KnowledgeSearch`/
> `KnowledgeProvider`라는 새 이름의 컴포넌트로 만들고 기존
> `MemoryEngine`은 손대지 않는다(사용자 최종 승인).

**설계 방향**: `domain/knowledge.py`에 `KnowledgeDocument`/
`KnowledgeKind`(ARCHITECTURE/ADR/RULE/TASK/PROJECT 5종 — ADR과
Decision, Workflow와 Task는 대응 파일이 하나뿐이라 통합, YAGNI).
`KnowledgeRepository` Interface + `FileKnowledgeRepository`(파일
하나 = 문서 하나, 문단 단위로 쪼개지 않음). `KnowledgeSearch`
Interface(Keyword 기반, 기존 `MemoryEngine.search()`와 동일한 단순
포함 검색). `KnowledgeProvider` Interface — Agent가 의존하는 유일한
진입점(`ContextManager`가 `MemoryEngine`을 감싸는 것과 동일한 패턴).
`KnowledgeIndexer`는 문서 수가 적어 성능 문제가 없어 이번 범위에서
제외(YAGNI, 사용자 승인). `CodingAgent`에 선택적 `knowledge_provider`
DI를 추가해, `DevelopmentContext`에 검색된 Knowledge를 반영한다.

**Non-goal(범위 밖)**: Chat History 저장, Conversation Memory, User
Profile Memory, Vector Database, Embedding, Semantic Search, RAG,
MCP, 외부 Knowledge 연동, Obsidian API 연동, `KnowledgeIndexer`
(영속 Index 자료구조).

**Milestone Definition of Done**
1. `KnowledgeDocument`/`KnowledgeKind`가 특정 Provider/Engine을 전혀
   참조하지 않는다.
2. `KnowledgeRepository`가 프로젝트 문서 파일을 읽어
   `KnowledgeDocument` 목록으로 노출한다.
3. `KnowledgeSearch`가 Keyword 기반으로 `KnowledgeRepository`의
   문서를 검색한다.
4. `KnowledgeProvider`가 Agent에게 노출되는 유일한 진입점이다 —
   Agent는 `KnowledgeRepository`/`KnowledgeSearch`를 직접 알지
   못한다.
5. `CodingAgent`가 `knowledge_provider` 주입 시 검색된 Knowledge를
   실행 프롬프트에 반영함이 통합 테스트로 증명된다. 미주입 시 기존과
   완전히 동일(하위 호환).
6. LLM 호출 없음 — `KnowledgeSearch`/`KnowledgeProvider`는 side-effect
   없는 순수 조회다.
7. 전체 `pytest`/`ruff`/`mypy` 통과.

**Task List**(2026-07-27 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M16-T01 | `KnowledgeDocument`/`KnowledgeKind` domain + `KnowledgeRepository` Interface + `FileKnowledgeRepository` | **완료** |
| M16-T02 | `KnowledgeSearch`/`KnowledgeProvider` + `CodingAgent` 연동(선택적 DI) | **완료** |
| M16-T03 | End-to-End 통합 테스트(실제 Markdown 문서 검색 + Agent Prompt 반영) | **완료** |
| M16-T04 | 문서화 + Milestone 16 Review | 진행 예정 |

**진행 상태**: M16-T01~T03 완료. M16-T04(문서화 + Review) 진행 중.

#### M16-T01: `KnowledgeDocument`/`KnowledgeKind` domain + `KnowledgeRepository` Interface + 구현체
- 상태: **DONE (2026-07-27)** — `domain/knowledge.py`에
  `KnowledgeKind`(ARCHITECTURE/ADR/RULE/TASK/PROJECT 5종)/
  `KnowledgeDocument`(document_id/kind/title/content/source_path)
  신규(Provider/Engine 독립). `interfaces/knowledge_repository.py`에
  `KnowledgeRepository`(`list_all`/`get`, side-effect 없음,
  `ProjectRepository`와 동일한 설계이나 읽기 전용이라 `save()` 없음)
  신규. `storage/file_knowledge_repository.py`에
  `FileKnowledgeRepository` 신규 — 고정 파일→kind 매핑
  (`DEFAULT_KNOWLEDGE_FILE_MAP`: `docs/ARCHITECTURE.md`→ARCHITECTURE,
  `.ai/DECISIONS.md`→ADR, `.ai/RULES.md`→RULE, `.ai/TASKS.md`→TASK,
  `docs/ROADMAP.md`/`docs/PRD.md`→PROJECT)로 파일 하나를 문서 하나로
  노출, 존재하는 파일만 반환, 제목은 첫 non-empty 줄에서 추출. 단위
  테스트 8개 신규(domain 2개, storage 6개 — 실제 이 저장소의
  `docs/ARCHITECTURE.md` 등을 실제로 읽어 목록에 포함되는지까지
  확인). `pytest`(519개), `ruff`, `mypy` 통과. 다음 Task: **M16-T02**.
- 의존성: 없음.

#### M16-T02: `KnowledgeSearch`/`KnowledgeProvider` + `CodingAgent` 연동
- 상태: **DONE (2026-07-27)** — `interfaces/knowledge_search.py`에
  `KnowledgeSearch`(`search(query) -> list[KnowledgeDocument]`, 생성자로
  주입된 `KnowledgeRepository`만 검색), `interfaces/
  knowledge_provider.py`에 `KnowledgeProvider`(Agent의 유일한 진입점,
  `ContextManager`가 `MemoryEngine`을 감싸는 것과 동일한 패턴) 신규.
  `engines/knowledge_search.py`의 `InMemoryKnowledgeSearch`(title/
  content 포함 검색, 영속 Index 없음, YAGNI)와 `engines/
  knowledge_provider.py`의 `InMemoryKnowledgeProvider`(Search에 위임)
  최소 구현. `domain/development_context.py`에 `related_knowledge:
  list[str] | None = None` 필드 추가, `to_prompt()`가 있으면 "관련
  프로젝트 지식" 섹션을 덧붙인다(기존 `prior_output`과 동일한 선택적
  확장 패턴). `CodingAgent`에 선택적 `knowledge_provider` DI 추가 —
  주입 시 `task.title`로 `provide()`를 호출해 결과를
  `DevelopmentContext.related_knowledge`에 실어 프롬프트에 반영,
  미주입 시(기본값 `None`) 검색 자체를 건너뛰어 기존과 완전히 동일.
  단위 테스트 10개 신규(interfaces engines 5개, development_context
  2개, coding_agent 3개). `pytest`(529개), `ruff`, `mypy` 통과. 다음
  Task: **M16-T03**.
- 의존성: M16-T01.

#### M16-T03: End-to-End 통합 테스트
- 상태: **DONE (2026-07-27)** — `tests/integration/
  test_m16_project_knowledge_system.py` 신규. 실제 프로젝트 문서를
  읽는 `FileKnowledgeRepository`(프로젝트 루트) + 실제
  `InMemoryKnowledgeSearch`/`InMemoryKnowledgeProvider` + 실제
  `CodingAgent`를 조립(Mock인 것은 `MockEngineAdapter` — 실제 LLM/CLI
  프로세스 실행 경계뿐). 3가지 시나리오 검증: (1) 실제
  `docs/ARCHITECTURE.md`에 등장하는 키워드("ExecutionEnvironment")로
  Task를 만들면 파이프라인이 정상 완주(`CodeCompleted.success=True`),
  (2) `MockEngineAdapter`를 상속한 `RecordingAdapter`로 실제 전달된
  Task를 가로채, 검색된 실제 `ARCHITECTURE.md` 문서의 `content`가
  그대로 프롬프트에 포함됐음을 직접 확인(Milestone DoD 5번 증명),
  (3) 매칭되지 않는 검색어("완전히-무관한-검색어-xyz123")를 써도
  파이프라인이 정상 동작(회귀 없음). `pytest`(532개, 기존 529개 +
  신규 3개), `ruff`, `mypy` 통과. 다음 Task: **M16-T04**(문서화 +
  Milestone 16 Review).
- 의존성: M16-T02.

#### M16-T04: 문서화 + Milestone 16 Review
- 목적: 문서와 구현을 일치시키고 Milestone 종료 승인을 받는다.
- 작업 내용: `docs/ARCHITECTURE.md`에 신규 §3.14(Knowledge Layer) +
  §3.6(CodingAgent 한 줄 요약) + §7(Interfaces 19→22종) + §8(의존성
  규칙 11번 신규) + §9 갱신, `.ai/DECISIONS.md`에 ADR-0028 신규(새
  최상위 Interface 3개 추가 + 기존 §8 의존성 규칙 확장), `docs/
  ROADMAP.md`/`.ai/MEMORY.md` 갱신, Review 작성.
- 완료 조건(DoD): 문서-구현 정합성 확인 + 사용자 승인.
- 상태: **DONE (2026-07-27)** — `docs/ARCHITECTURE.md` v0.18.0 신규
  §3.14(Knowledge Layer — 저장/검색/제공 역할 분리, `MemoryEngine`과
  다른 개념임을 명시, `KnowledgeIndexer` 제외 근거)/§3.6(`CodingAgent`
  의 `knowledge_provider` 한 줄 요약)/§7(Interfaces 총 22종,
  `KnowledgeRepository`/`KnowledgeSearch`/`KnowledgeProvider` 3행
  추가)/§8(의존성 규칙 11번 "Agent → Knowledge Provider → Knowledge
  Search → Knowledge Repository" 신규, 규칙 5에도 Knowledge Provider
  추가)/§9(디렉터리 매핑에 `storage/file_knowledge_repository.py`/
  `engines/knowledge_search.py`/`engines/knowledge_provider.py`
  반영). `.ai/DECISIONS.md`에 **ADR-0028**(배경/결정 6개 항목/대안
  4개/이유/결과) 신규 작성. 아래 "Milestone 16 Review" 절 참고.
- 의존성: M16-T01~T03.

---

## Milestone 16 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `KnowledgeDocument`/`KnowledgeKind`가 Provider/Engine 독립 | ✅ (M16-T01) |
| 2 | `KnowledgeRepository`가 프로젝트 문서를 `KnowledgeDocument`로 노출 | ✅ (M16-T01) |
| 3 | `KnowledgeSearch`가 Keyword 기반으로 검색 | ✅ (M16-T02) |
| 4 | `KnowledgeProvider`가 Agent의 유일한 진입점 | ✅ (M16-T02) |
| 5 | `CodingAgent`가 주입 시 Knowledge를 프롬프트에 반영, 미주입 시 하위 호환 | ✅ (M16-T02/T03) |
| 6 | LLM 호출 없음(side-effect 없는 순수 조회) | ✅ (M16-T01/T02, `KnowledgeSearch`/`KnowledgeProvider` 어디도 EngineRuntime을 참조하지 않음) |
| 7 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M16-T01~T04) 전체 완료. 사용자 승인 조건("`KnowledgeIndexer`
제외", "기존 `MemoryEngine`과 이름·역할 분리", "파일 단위 문서화")
그대로 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `domain/knowledge.py`(`KnowledgeDocument`/
  `KnowledgeKind`), `interfaces/knowledge_repository.py`
  (`KnowledgeRepository`), `interfaces/knowledge_search.py`
  (`KnowledgeSearch`), `interfaces/knowledge_provider.py`
  (`KnowledgeProvider`), `storage/file_knowledge_repository.py`
  (`FileKnowledgeRepository`), `engines/knowledge_search.py`
  (`InMemoryKnowledgeSearch`), `engines/knowledge_provider.py`
  (`InMemoryKnowledgeProvider`) — 총 7개 신규 소스 파일.
- **변경된 기존 컴포넌트**: `domain/development_context.py`
  (`related_knowledge` 필드 추가) + `CodingAgent`(선택적
  `knowledge_provider` DI).
- **핵심 설계 결정**: 기존 `MemoryEngine`(세션 연속성)과 이름·역할을
  완전히 분리했다 — `MemoryEngine`을 확장하는 대신 별도 컴포넌트
  계열을 신설해, "세션 기억"과 "프로젝트 지식"이라는 서로 다른
  개념이 하나의 계약 아래 섞이지 않게 했다(SRP). 저장(Repository)/
  검색(Search)/제공(Provider) 3역할 분리는 향후 검색 알고리즘만
  교체(예: Semantic Search)할 수 있는 여지를 남긴다(OCP) —
  `KnowledgeIndexer`는 현재 문서 수(6개 안팎)로는 성능 이점이 없어
  이번 범위에서 뺐다(YAGNI).

`git diff --stat`(M15 종료 커밋 대비)로 확인한 결과 신규 소스 파일
7개, 기존 소스 파일 수정 2개(`development_context.py`,
`coding_agent.py`) — M5(신규 6)보다 넓은, 지금까지 중 가장 넓은
신규 파일 폭이다. Interface 3개가 한 번에 추가된 것도 M1 이후 처음.

**3. Interface First 원칙 검토**

M16은 **새 최상위 Interface 3개(`KnowledgeRepository`/
`KnowledgeSearch`/`KnowledgeProvider`)를 추가**했다 — M5(6개 신규
파일)와 M11(`ExecutionEnvironment`)에 이어 이번까지 중 가장 큰
Interface 확장이다. 기존 `EngineAdapter`/`EngineRuntime`처럼 계약을
"확장"한 것이 아니라 완전히 새로운 계층을 추가한 것이라 ADR-0009/
0015/0026/0027과는 다른 종류의 결정이며, ADR-0017(Context Manager
도입)·ADR-0025(ExecutionEnvironment 도입)과 같은 "신규 계층 도입"
계열로 ADR-0028에 기록했다. `docs/ARCHITECTURE.md` §8 의존성
규칙에도 신규 경로(11번)를 추가해, Agent가 `KnowledgeRepository`/
`KnowledgeSearch`를 직접 호출하지 못하게 하는 경계를 문서로 명시했다.
새 매개변수(`knowledge_provider`)는 기본값이 있는 키워드 전용
인자라 기존 호출부와 100% 호환된다.

**4. 테스트 결과**

- `pytest`: **532개 전부 통과**(M15 완료 시점 511개 → M16에서 21개
  신규: M16-T01 +8, M16-T02 +10, M16-T03 +3)
- `ruff check src tests`: 클린
- `mypy src`: 클린(신규 소스 파일 7개 포함, `storage/
  llm_policy_loader.py`의 `types-PyYAML` 미설치 경고 1건은 M16 이전
  부터 존재하는 무관한 항목)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M16 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- **`KnowledgeIndexer`(영속 Index)** — 문서 수가 적어 성능 문제가
  없어 제외(YAGNI). 문서량이 커지면 재검토.
- **Chat History/Conversation Memory/User Profile Memory** — 사용자
  확정 범위 밖, 기존 `MemoryEngine`의 책임 영역이며 M16과 무관.
- **Vector/Embedding/Semantic Search/RAG/MCP/외부 Knowledge 연동/
  Obsidian API 연동** — 사용자 확정 범위 밖.
- **Review/Documentation Agent로의 `knowledge_provider` 확장** —
  이번엔 `CodingAgent` 하나에만 적용(M12/M13과 동일한 MVP 원칙,
  YAGNI). 실제 필요성이 증명되면 후속 Milestone에서 확장.

*계속 이월되는 기존 항목*
- Effort 라우팅, `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임
  워크 미통합, Codex/Gemini 실연동 미검증, `MemoryEngine.search()`
  선형 스캔, 여러 Task에 걸친 누적 예산 추적, 예산 초과 시 Approval
  흐름, Retry Backoff/Persistent Runtime Recovery/Approval 비동기
  처리/Process Timeout 정책 고도화, `ShellAgent` 화이트리스트 코드
  고정.

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M16-T01~T04 상세 섹션) / `docs/ROADMAP.md`
(M16 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.18.0, 신규
§3.14/§3.6/§7/§8/§9 갱신) / `.ai/DECISIONS.md`(ADR-0028 신규) 완료.
`pyproject.toml` 버전은 v0.5.0 그대로 유지(ADR-0024 기준선 — 새
Interface 3개 추가는 M5/M11/ADR-0017과 같은 종류의 "신규 계층 도입"
이라 기준선 재선언 대상은 아니라고 판단했으나, Interface 수가 크게
늘어난 만큼 다음 기준선 재검토 시점에 M16까지의 누적 변화를 함께
검토할 필요가 있다). `.ai/MEMORY.md`는 이 Review 승인 직후 M1~M15와
동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 신규 7/
수정 2 소스 파일, "MemoryEngine과 이름·역할 분리 + 저장/검색/제공
3역할 분리" 설계 결정 명시), Interface First 검토 완료(3절, 새
Interface 3개를 "신규 계층 도입" 계열 ADR로 투명하게 기록), 테스트
결과 문서화 완료(4절), Technical Debt 정리 완료(5절), 문서 갱신
완료(6절) — 6개 조건 모두 만족. Review 중 코드 변경이 필요한 치명적
문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 16 Completed를 선언한다.**

**Milestone 16 종료 — 2026-07-27 사용자 승인.**

**Milestone 17 상태**: 착수 확정. 아래 "Milestone 17" 절 참고.

---

## Milestone 17 — Intelligent Engine Selection

**목표**: Task + Budget(M15) + Project Knowledge(M16) + 등록된
Engine들의 Capability/비용을 종합해 **최적 Engine 후보를 결정**하는
`EngineSelectionPolicy`를 도입한다. **이 Milestone은 결정만 한다 —
그 결정을 실제 실행에 반영하는 것은 M18(Execution)의 책임**이다
(2026-07-27 사용자 확정, "Decision Only Milestone").

> **설계 검토에서 발견한 사실**: `EngineRuntime`은 `run()`/
> `estimate_cost()` 둘 다 `required_capabilities`를 만족하는 등록된
> Engine 중 **첫 번째 매칭만** 선택한다(`_require_adapter`/`_select`).
> 여러 후보를 나열·비교하는 방법 자체가 없다 — "선택"이라 부를 만한
> 로직이 지금은 존재하지 않는다.

**설계 방향(사용자 승인 조건 반영)**: `EngineRuntime.list_candidates()`
로 계약을 또 확장하는 대신, **`AgentManager`/`AgentRegistry` 분리와
동일한 패턴**으로 신규 `EngineRegistry`(`interfaces/
engine_registry.py`)를 도입한다 — "등록된 Engine이 무엇인지 조회"는
`EngineRegistry`(신규)가, "어떻게 실행하는지"는 기존 `EngineRuntime`
이 그대로 맡는다. **단, 이 저장소에는 `AgentRegistry`에 대응하는
기존 Engine Registry가 없었다**(Engine 등록은 지금까지
`EngineRuntime.register_engine()` 내부 dict가 전부였음) — 그래서
"기존 계층을 활용"이 아니라 **신규 계층을 도입**하는 결정이다. 대신
기존 `EngineRuntime` 3개 구현체(`InMemoryEngineRuntime`/
`ManagedEngineRuntime`/`RecoveringEngineRuntime`)의 내부 구현은 전혀
건드리지 않는다(zero 회귀 위험) — `EngineRegistry`는 실행 경로와는
별도로, 같은 Adapter를 조립 시점에 한 번 더 등록해 후보 조회 전용으로
쓴다(EngineRuntime의 계약 확장 없음). `EngineSelectionPolicy`
(`interfaces/engine_selection_policy.py`)는 `EngineCandidate` 목록과
`BudgetPolicyEngine`(선택, M15 재사용 — 후보별 `CostEstimate`를 만들어
`check()`에 그대로 위임해 예산 비교 로직을 중복 구현하지 않음)/
Knowledge(선택, M16 재사용 — 결정 사유에만 반영, 이번 MVP는 Budget/
비용 기준 판단만)를 받아 순수하게 "판단"만 한다(side-effect 없음).

**Non-goal(범위 밖)**: 실제 실행 연결(M18), Model 수준 결정(계속
M14의 정적 정책이 담당 — 이 Decision은 Engine 선택에만 집중),
`EngineRuntime` 내부 구현 리팩터링, ML/휴리스틱 기반 고급 판단
(규칙 기반 최소 구현만).

**Milestone Definition of Done**
1. `EngineCandidate`/`EngineSelectionDecision`이 특정 Provider를
   전혀 참조하지 않는다.
2. `EngineRegistry`가 `required_capabilities`를 만족하는 등록된 모든
   Engine 후보를 `EngineCandidate`로 나열한다(세션 미생성).
3. `EngineSelectionPolicy`가 Task/Budget/Knowledge/후보 목록을 받아
   결정하는 규칙 기반 계약이다(side-effect 없음, LLM 호출 없음).
   `EngineSelectionDecision`에 선택 이유(`reason`)가 포함된다.
4. 최소 1개 규칙(Budget 내에서 예상 비용이 가장 낮은 후보 선택)이
   실제 여러 Engine이 등록된 상태에서 통합 테스트로 검증된다.
5. `EngineSelectionPolicy`의 결정은 `CodingAgent`의 실제
   `engine_runtime.run()` 호출에 전혀 연결되지 않는다 — 결정 따로,
   실행 따로임을 통합 테스트로 명시적으로 증명한다.
6. 전체 `pytest`/`ruff`/`mypy` 통과.

**Task List**(2026-07-27 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M17-T01 | `EngineCandidate`/`EngineSelectionDecision` domain + `EngineRegistry` Interface + `InMemoryEngineRegistry` | **완료** |
| M17-T02 | `EngineSelectionPolicy` Interface + `InMemoryEngineSelectionPolicy`(Budget 내 최저 비용 우선) | **완료** |
| M17-T03 | End-to-End 통합 테스트(다중 Engine 후보 선택 + 실행과의 비연결 증명) | **완료** |
| M17-T04 | 문서화 + Milestone 17 Review | 진행 예정 |

**진행 상태**: M17-T01~T03 완료. M17-T04(문서화 + Review) 진행 중.

#### M17-T01: `EngineCandidate`/`EngineSelectionDecision` domain + `EngineRegistry` Interface + 구현체
- 상태: **DONE (2026-07-27)** — `domain/engine_selection.py`에
  `EngineCandidate`(engine_name/capabilities/estimated_tokens/
  estimated_cost_usd/supports_parallel)/`EngineSelectionDecision`
  (engine_name/model/reason) 신규(Provider 독립, `CostEstimate`를
  그대로 참조하지 않고 값만 옮겨 담아 domain이 interfaces에 의존하지
  않는 기존 원칙 유지). `interfaces/engine_registry.py`에
  `EngineRegistry`(`register`/`get`/`list_candidates`, `AgentRegistry`
  와 동일한 설계 원칙) 신규 — `EngineRuntime`의 실행 계약(run/
  estimate_cost)은 전혀 확장하지 않음. `runtime/engine/
  engine_registry.py`의 `InMemoryEngineRegistry` 최소 구현체 —
  `list_candidates()`가 각 Adapter의 `estimate_cost(task)`를 호출해
  후보 목록을 조립(세션 미생성). 단위 테스트 8개 신규(domain 2개,
  runtime/engine 6개). `pytest`(540개), `ruff`, `mypy` 통과. 다음
  Task: **M17-T02**.
- 의존성: 없음.

#### M17-T02: `EngineSelectionPolicy` Interface + `InMemoryEngineSelectionPolicy`
- 상태: **DONE (2026-07-27)** — `interfaces/engine_selection_policy.py`
  에 `EngineSelectionPolicy`(`select(task, candidates, *,
  budget_policy_engine=None, knowledge=None) -> EngineSelectionDecision
  | None`, `LLMPolicyEngine`/`BudgetPolicyEngine`과 동일한 설계
  원칙 — 규칙 기반, side-effect 없음) 신규. `engines/
  engine_selection_policy.py`의 `InMemoryEngineSelectionPolicy` —
  `budget_policy_engine`이 주어지면 각 후보의 `estimated_tokens`/
  `estimated_cost_usd`로 `CostEstimate`를 만들어 `BudgetPolicyEngine.
  check()`에 그대로 위임(M15 재사용, 예산 비교 로직 중복 없음),
  예산 내 후보 중 `estimated_cost_usd`(동률이면 `estimated_tokens`)가
  가장 낮은 후보를 선택. `knowledge`는 결정 사유(`reason`)에만 참고로
  반영(후보를 걸러내지 않음, MVP 범위 명시). 후보가 없거나 예산 내
  후보가 하나도 없으면 `None`. 단위 테스트 6개 신규(빈 후보/최저
  비용 선택/예산 초과 제외/전체 초과 시 None/Knowledge 반영/동률
  시 등록 순서 유지). `pytest`(546개), `ruff`, `mypy` 통과. 다음
  Task: **M17-T03**(End-to-End 통합 테스트).
- 의존성: M17-T01.

#### M17-T03: End-to-End 통합 테스트
- 상태: **DONE (2026-07-27)** — `tests/integration/
  test_m17_intelligent_engine_selection.py` 신규, 7개 테스트. 실제
  `InMemoryEngineRegistry`/`InMemoryBudgetPolicyEngine`/
  `InMemoryEngineSelectionPolicy` 조합으로 (1) 여러 Engine이 실제
  등록된 상태에서 Budget 내 최저 비용 후보 선택, (2) 예산 초과 후보
  제외, (3) 전체 후보가 예산을 넘으면 `None`, (4) 실제
  `FileKnowledgeRepository`(프로젝트 루트)로 조회한 실제 Knowledge가
  결정 사유에 반영됨을 검증. **Milestone DoD 5번(가장 중요한 경계)**:
  `EngineSelectionPolicy`가 "cheap"을 추천하더라도, 실제
  `EngineRuntime`에는 "expensive"만 등록해 둔 실제 `CodingAgent`
  파이프라인을 통째로 실행 — Task가 정상적으로 `expensive`로
  실행·완료됨을 확인해(`EngineRuntime.status()`), Selection Decision이
  실행에 전혀 영향을 주지 않음을 직접 증명. 추가로
  `inspect.signature(CodingAgent.__init__)`으로 `CodingAgent`
  생성자가 `engine_selection_policy`/`engine_registry` 파라미터를
  아예 받지 않음을 코드 수준에서 재확인(설계상 약속이 실제로
  지켜지고 있음을 이중으로 증명). `pytest`(553개, 기존 546개 + 신규
  7개), `ruff`, `mypy` 통과. 다음 Task: **M17-T04**(문서화 +
  Milestone 17 Review).
- 의존성: M17-T02.

#### M17-T04: 문서화 + Milestone 17 Review
- 목적: 문서와 구현을 일치시키고 Milestone 종료 승인을 받는다.
- 작업 내용: `docs/ARCHITECTURE.md`에 신규 §3.15(Intelligent Engine
  Selection) + §7(Interfaces 22→24종) + §9 갱신, `.ai/DECISIONS.md`
  에 ADR-0029 신규(새 최상위 Interface 2개 도입, `EngineRuntime`
  계약은 미확장이라는 결정 근거 포함), `docs/ROADMAP.md`/`.ai/
  MEMORY.md` 갱신, Review 작성.
- 완료 조건(DoD): 문서-구현 정합성 확인 + 사용자 승인.
- 상태: **DONE (2026-07-27)** — `docs/ARCHITECTURE.md` v0.19.0 신규
  §3.15(Intelligent Engine Selection — `EngineRegistry`/
  `EngineSelectionPolicy` 역할, `EngineRuntime` 계약 미확장 근거,
  결정과 실행의 분리 경계 명시)/§7(Interfaces 총 24종, `EngineRegistry`
  /`EngineSelectionPolicy` 2행 추가)/§9(디렉터리 매핑에
  `runtime/engine/engine_registry.py`/`engines/
  engine_selection_policy.py` 반영). `.ai/DECISIONS.md`에
  **ADR-0029**(배경/결정 5개 항목/대안 3개/이유/결과) 신규 작성.
  아래 "Milestone 17 Review" 절 참고.
- 의존성: M17-T01~T03.

---

## Milestone 17 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `EngineCandidate`/`EngineSelectionDecision`이 Provider 독립 | ✅ (M17-T01) |
| 2 | `EngineRegistry`가 등록된 모든 후보를 나열(세션 미생성) | ✅ (M17-T01) |
| 3 | `EngineSelectionPolicy`가 규칙 기반·side-effect 없음, `reason` 포함 | ✅ (M17-T02) |
| 4 | Budget 내 최저 비용 우선 규칙이 다중 Engine으로 통합 테스트 검증 | ✅ (M17-T03) |
| 5 | 결정이 `CodingAgent`의 실제 실행에 연결되지 않음을 증명 | ✅ (M17-T03, 파이프라인 실행 + 시그니처 검사 이중 증명) |
| 6 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M17-T01~T04) 전체 완료. 사용자 승인 조건("Decision Only
유지", "`reason` 포함", "가능하면 `EngineRuntime.list_candidates()`
대신 기존/신규 Registry 계층으로 조회·판단 책임 분리") 모두 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `domain/engine_selection.py`(`EngineCandidate`/
  `EngineSelectionDecision`), `interfaces/engine_registry.py`
  (`EngineRegistry`), `interfaces/engine_selection_policy.py`
  (`EngineSelectionPolicy`), `runtime/engine/engine_registry.py`
  (`InMemoryEngineRegistry`), `engines/engine_selection_policy.py`
  (`InMemoryEngineSelectionPolicy`) — 총 5개 신규 소스 파일.
- **변경된 기존 컴포넌트**: 없음. `EngineRuntime`/`CodingAgent`
  어느 쪽도 수정하지 않았다 — M11~M16이 매번 최소 1개 기존
  컴포넌트를 손댔던 것과 달리, M17은 **완전히 새 계층만 추가**하고
  기존 실행 경로는 전혀 건드리지 않았다(Decision Only라는 Milestone
  성격이 코드 구조에도 그대로 반영됨).
- **핵심 설계 결정**: 사용자가 제안한 "`EngineRuntime.list_candidates()`
  대신 기존 Registry/Manager 계층 활용"을 조사한 결과, 대응하는
  기존 계층이 없다는 사실을 확인하고 `AgentManager`/`AgentRegistry`
  분리와 동일한 패턴으로 `EngineRegistry`를 신규 도입했다 — "기존
  활용"이 아니라 "동일 패턴의 신규 계층 도입"이라는 점을 문서에
  정직하게 기록했다. `EngineSelectionPolicy`는 후보가 어디서
  왔는지 알지 못하게 설계해(호출자가 먼저 `list_candidates()`로
  조회한 뒤 넘김) 조회/판단 책임을 코드 구조로도 분리했다.

`git diff --stat`(M16 종료 커밋 대비)로 확인한 결과 신규 소스 파일
5개, 기존 소스 파일 수정 0개 — 지금까지 유일하게 **기존 소스 파일을
전혀 수정하지 않은** Milestone이다(가장 작은 회귀 위험).

**3. Interface First 원칙 검토**

M17은 **새 최상위 Interface 2개(`EngineRegistry`/
`EngineSelectionPolicy`)를 추가**했다 — M16(3개)에 이어 두 Milestone
연속으로 신규 계층을 도입한 것이지만, M17은 기존 Interface(`EngineRuntime`
등)를 단 하나도 확장하지 않았다는 점에서 M14/M15/M16과 다르다.
`EngineRuntime`을 세 번째로 확장하는 대신 완전히 독립된 계층을
분리한 것은 ADR-0017(Context Manager 도입)·ADR-0025
(ExecutionEnvironment 도입)·ADR-0028(Knowledge Layer 도입)과 같은
"신규 계층 도입" 계열이라 ADR-0029로 기록했다. 새 컴포넌트를 호출하는
기존 코드가 없으므로(Decision Only) 하위 호환성 이슈 자체가 발생하지
않는다.

**4. 테스트 결과**

- `pytest`: **553개 전부 통과**(M16 완료 시점 532개 → M17에서 21개
  신규: M17-T01 +8, M17-T02 +6, M17-T03 +7)
- `ruff check src tests`: 클린
- `mypy src`: 클린(신규 소스 파일 5개 포함, `storage/
  llm_policy_loader.py`의 `types-PyYAML` 미설치 경고 1건은 M17
  이전부터 존재하는 무관한 항목)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M17 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- **실행 연결(M18로 예정)** — `EngineSelectionPolicy`의 결정을
  실제 `engine_runtime.run()` 호출에 반영하는 것은 다음 Milestone의
  책임.
- **Model 수준 결정** — 계속 M14의 정적 정책이 담당, 이 Decision은
  Engine 선택에만 집중.
- **ML/휴리스틱 기반 고급 판단** — 규칙 기반 최소 구현(예산 내 최저
  비용)만 제공.
- **`EngineRuntime`↔`EngineRegistry` 중복 등록 제거(통합)** — 같은
  Adapter를 두 곳에 등록하는 약간의 중복이 있으나, `EngineRuntime`
  내부 구현을 리팩터링하는 것은 이번 범위 밖(회귀 위험 최소화 우선).

*계속 이월되는 기존 항목*
- Effort 라우팅, `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임
  워크 미통합, Codex/Gemini 실연동 미검증, `MemoryEngine.search()`
  선형 스캔, 여러 Task에 걸친 누적 예산 추적, 예산 초과 시 Approval
  흐름, `KnowledgeIndexer`, Review/Documentation Agent로의
  `knowledge_provider` 확장, Retry Backoff/Persistent Runtime
  Recovery/Approval 비동기 처리/Process Timeout 정책 고도화,
  `ShellAgent` 화이트리스트 코드 고정.

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M17-T01~T04 상세 섹션) / `docs/ROADMAP.md`
(M17 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.19.0, 신규
§3.15/§7/§9 갱신) / `.ai/DECISIONS.md`(ADR-0029 신규) 완료.
`pyproject.toml` 버전은 v0.5.0 그대로 유지(ADR-0024 기준선 — 새
Interface 2개 추가는 M5/M11/M16과 같은 "신규 계층 도입" 계열이라
기준선 재선언 대상이 아니라고 판단했으나, M16+M17로 Interface가
19→24종까지 늘어난 만큼 다음 기준선 재검토 시점에 누적 변화를 함께
검토할 필요가 있다). `.ai/MEMORY.md`는 이 Review 승인 직후 M1~M16과
동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 신규 5/
수정 0 소스 파일 — 지금까지 유일하게 기존 파일 무수정, "조회
(Registry)/판단(Policy)/실행(Runtime) 책임 분리" 설계 결정 명시),
Interface First 검토 완료(3절, 새 Interface 2개를 "신규 계층 도입"
계열 ADR로 투명하게 기록, 기존 Interface 미확장), 테스트 결과
문서화 완료(4절), Technical Debt 정리 완료(5절), 문서 갱신 완료
(6절) — 6개 조건 모두 만족. Review 중 코드 변경이 필요한 치명적
문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 17 Completed를 선언한다.**

**Milestone 17 종료 — 2026-07-27 사용자 승인.**

**Milestone 18 상태**: 착수 확정. 아래 "Milestone 18" 절 참고.

---

## Milestone 18 — Multi-Engine Execution Integration

**목표**: M17의 `EngineSelectionDecision`을 실제 실행으로 연결하는
`ExecutionDispatcher`를 도입한다. 선택된 Engine을 인증 상태 확인 후
실행하는 것 하나가 이번 Milestone의 목표다(2026-07-27 사용자 확정).

> **설계 검토에서 발견한 사실**: `interfaces/execution_environment.py`
> 의 `ExecutionResult`(returncode/stdout/stderr/timed_out/cancelled,
> M11)와 DoD가 요구하는 새 "success/output/error/engine/
> execution_time" Domain이 이름이 겹친다 — 서로 다른 두 개념이라
> 새 Domain은 **`EngineExecutionResult`**로 명명한다(사용자 승인).

**설계 방향(사용자 최종 승인)**: `ExecutionDispatcher`는 Interface가
아니라 구체 클래스로 구현한다(M12 `WorkflowRunner`와 동일한 패턴) —
`EngineRegistry`/`EngineAdapter`/`AuthenticationManager` Interface만
사용해 OCP를 지킨다. 인증 실패는 `AuthenticationRequiredError`
예외로, `SelectionDecision` 부재는 `EngineExecutionResult(success=
False)`로 구분한다. **이번 Milestone은 `CodingAgent`를 수정하지
않는다** — `ExecutionDispatcher`는 독립적으로 구현·검증한다(Agent
파이프라인 연결은 후속 Milestone).

**Non-goal(범위 밖)**: 실제 로그인/OAuth/API Key 등록/Credential
저장/Token Refresh, Retry/Timeout/Recovery/Approval, Parallel
Execution, Scheduler, Workflow Automation, MCP, Dashboard, Budget/
Knowledge/Selection Policy 개선, Codex/Gemini 실제 구현(Adapter
Stub/Mock으로만 검증), `CodingAgent` 연결.

**Milestone Definition of Done**
1. `ExecutionDispatcher`가 `EngineSelectionDecision`을 받아 선택된
   Engine 하나만 실행한다.
2. `ExecutionDispatcher`는 `AuthenticationManager`를 통해 인증
   상태를 확인한다.
3. 이미 인증되어 있으면 즉시 실행된다.
4. 인증되어 있지 않으면 `AuthenticationRequiredError`를 던진다.
5. Workspace는 실제 로그인을 수행하지 않는다.
6. `AuthenticationManager`는 `is_authenticated()`/
   `authentication_status()`만 제공한다(`login()`/`logout()` 없음).
7. `ExecutionDispatcher`는 `ExecutionEnvironment`를 직접 생성하지
   않는다(DI만 사용, `EngineAdapter` 내부에 이미 DI되어 있음).
8. `ExecutionDispatcher`는 `EngineAdapter` Interface만 사용한다.
9. `EngineExecutionResult` Domain을 추가한다(success/output/error/
   engine/execution_time, Provider 독립).
10. `ClaudeCodeEngineAdapter`와 실제 연결되어 `ExecutionEnvironment`
    를 통해 실행됨을 통합 테스트로 증명한다.
11. `SelectionDecision`이 없는 경우 실행되지 않음을 단위 테스트로
    증명한다.
12. `EngineSelectionPolicy`가 `ExecutionDispatcher`를 참조하지
    않음을 Architecture 의존성 검증으로 증명한다.
13. 전체 `pytest`/`ruff`/`mypy` 통과.

**Task List**(2026-07-27 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M18-T01 | `EngineExecutionResult` domain + `AuthenticationManager` Interface + `InMemoryAuthenticationManager` | **완료** |
| M18-T02 | `ExecutionDispatcher` 핵심 로직(인증 확인/실패/Decision 부재 처리) | **완료** |
| M18-T03 | End-to-End 통합 테스트(실제 `ClaudeCodeEngineAdapter`+`ExecutionEnvironment` 연결 + 의존성 검증) | **완료** |
| M18-T04 | 문서화 + Milestone 18 Review | 진행 예정 |

**진행 상태**: M18-T01~T03 완료. M18-T04(문서화 + Review) 진행 중.

#### M18-T01: `EngineExecutionResult` domain + `AuthenticationManager` Interface + 구현체
- 상태: **DONE (2026-07-27)** — `domain/execution_result.py`에
  `EngineExecutionResult`(success/output/error/engine/execution_time,
  Provider 독립, 기존 `ExecutionResult`(M11, 프로세스 결과)와 이름·
  개념 분리) 신규. `interfaces/authentication_manager.py`에
  `AuthenticationStatus`(AUTHENTICATED/UNAUTHENTICATED)/
  `AuthenticationRequiredError`/`AuthenticationManager`(`is_
  authenticated`/`authentication_status`만 — `login`/`logout` 없음,
  "로그인 수행"이 아니라 "상태 확인"만 담당) 신규. `engines/
  authentication_manager.py`의 `InMemoryAuthenticationManager` —
  생성 시 주어진 인증된 Engine 이름 집합으로만 상태를 판단(실제
  로그인/OAuth/Credential 없음). 단위 테스트 5개 신규(domain 2개,
  engines 3개). `pytest`(558개), `ruff`, `mypy` 통과. 다음 Task:
  **M18-T02**(`ExecutionDispatcher` 핵심 로직).
- 의존성: 없음.

#### M18-T02: `ExecutionDispatcher` 핵심 로직
- 상태: **DONE (2026-07-27)** — `runtime/execution/
  execution_dispatcher.py`에 `ExecutionDispatcher`(구체 클래스, 사용자
  승인) 신규. `dispatch(decision, task) -> EngineExecutionResult`:
  `decision is None`이면 `EngineRegistry`/`AuthenticationManager`를
  전혀 호출하지 않고 즉시 실패 결과 반환(DoD 11). 인증 확인 후
  미인증이면 `AuthenticationRequiredError`를 던진다(DoD 4). 인증됐으면
  `EngineRegistry.get(decision.engine_name)`으로 정확히 하나의
  Adapter만 얻어 `create_session()`→`run(session_id, task,
  model=decision.model)`→`destroy_session()` 순서로 실행하고
  `time.monotonic()`으로 실행 시간을 측정해 `EngineExecutionResult`로
  감싼다(DoD 1/2/3/7/8/9). `EngineSelectionPolicy`는 어디서도
  참조하지 않는다(Decision-Execution 분리, import 자체가 없음).
  단위 테스트 5개 신규(인증됨 실행/미인증 예외/Decision 없음 시
  Registry·Auth 미호출을 Spy로 직접 증명/여러 Engine 중 선택된
  것만 실행/미등록 Engine 예외 전파). `pytest`(563개), `ruff`,
  `mypy` 통과. 다음 Task: **M18-T03**(End-to-End 통합 테스트).
- 의존성: M18-T01.

#### M18-T03: End-to-End 통합 테스트
- 상태: **DONE (2026-07-27)** — `tests/integration/
  test_m18_multi_engine_execution_integration.py` 신규, 4개 테스트.
  (1) 실제 `ClaudeCodeEngineAdapter` + `FakeExecutionEnvironment`를
  `InMemoryEngineRegistry`에 등록하고, `InMemoryEngineSelectionPolicy`
  가 만든 실제 `EngineSelectionDecision`을 `ExecutionDispatcher`에
  전달 — `ExecutionEnvironment.executed_commands`에 실제 `claude`
  명령이 기록됨을 확인해 Milestone DoD 10번을 직접 증명. (2) 미인증
  상태에서는 `AuthenticationRequiredError`가 발생하고
  `ExecutionEnvironment`에는 어떤 명령도 도달하지 않음을 확인(DoD
  4/5번). (3) `EngineRegistry` 조회 → `BudgetPolicyEngine`이 반영된
  `EngineSelectionPolicy.select()` → `ExecutionDispatcher.dispatch()`
  전체 경로를 실제 컴포넌트로 조립해 확인(Task→...→
  `EngineExecutionResult`). (4) **Milestone DoD 12번**:
  `InMemoryEngineSelectionPolicy`/`EngineSelectionPolicy` 소스 코드를
  직접 읽어 `"ExecutionDispatcher"` 문자열이 전혀 없음을 확인 —
  Architecture 의존성을 문서상 약속이 아니라 코드로 직접 검증.
  `pytest`(567개, 기존 563개 + 신규 4개), `ruff`, `mypy` 통과. 다음
  Task: **M18-T04**(문서화 + Milestone 18 Review).
- 의존성: M18-T02.

#### M18-T04: 문서화 + Milestone 18 Review
- 목적: 문서와 구현을 일치시키고 Milestone 종료 승인을 받는다.
- 작업 내용: `docs/ARCHITECTURE.md`에 신규 §3.16(Execution Layer) +
  §7(Interfaces 24→25종) + §9 갱신, `.ai/DECISIONS.md`에 ADR-0030
  신규(새 최상위 Interface 1개 도입, `ExecutionDispatcher`는 구체
  클래스라 ADR 대상 아님을 명시), `docs/ROADMAP.md`/`.ai/MEMORY.md`
  갱신, Review 작성.
- 완료 조건(DoD): 문서-구현 정합성 확인 + 사용자 승인.
- 상태: **DONE (2026-07-27)** — `docs/ARCHITECTURE.md` v0.20.0 신규
  §3.16(Execution Layer — `ExecutionDispatcher`/`AuthenticationManager`
  /`EngineExecutionResult` 역할, Decision-Execution 분리 근거,
  `CodingAgent` 미수정 명시)/§7(Interfaces 총 25종,
  `AuthenticationManager` 행 추가)/§9(디렉터리 매핑에
  `runtime/execution/execution_dispatcher.py`/`engines/
  authentication_manager.py` 반영). `.ai/DECISIONS.md`에
  **ADR-0030**(배경/결정 6개 항목/대안 4개/이유/결과) 신규 작성.
  아래 "Milestone 18 Review" 절 참고.
- 의존성: M18-T01~T03.

---

## Milestone 18 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `ExecutionDispatcher`가 선택된 Engine 하나만 실행 | ✅ (M18-T02/T03) |
| 2~3 | `AuthenticationManager`로 인증 확인, 인증된 경우 즉시 실행 | ✅ (M18-T02/T03) |
| 4 | 미인증 시 `AuthenticationRequiredError` | ✅ (M18-T02/T03) |
| 5 | 실제 로그인 미수행 | ✅ (M18-T01, `login`/`logout` 계약 자체가 없음) |
| 6 | `AuthenticationManager`가 `is_authenticated`/`authentication_status`만 제공 | ✅ (M18-T01) |
| 7~8 | `ExecutionEnvironment` 직접 생성 없음(DI), `EngineAdapter` Interface만 사용 | ✅ (M18-T02) |
| 9 | `EngineExecutionResult` Domain(Provider 독립) | ✅ (M18-T01) |
| 10 | `ClaudeCodeEngineAdapter` 실제 연결 증명 | ✅ (M18-T03) |
| 11 | Decision 없으면 미실행 단위 테스트 증명 | ✅ (M18-T02, Spy로 Registry/Auth 미호출 확인) |
| 12 | `EngineSelectionPolicy`가 `ExecutionDispatcher` 미참조 증명 | ✅ (M18-T03, 소스 코드 직접 검증) |
| 13 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M18-T01~T04) 전체 완료. 사용자 승인 조건(`EngineExecutionResult`
명명, `ExecutionDispatcher` 구체 클래스, 인증 실패=예외/Decision
부재=실패 결과 구분, `CodingAgent` 미수정) 모두 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `domain/execution_result.py`
  (`EngineExecutionResult`), `interfaces/authentication_manager.py`
  (`AuthenticationManager`/`AuthenticationStatus`/
  `AuthenticationRequiredError`), `engines/authentication_manager.py`
  (`InMemoryAuthenticationManager`), `runtime/execution/
  execution_dispatcher.py`(`ExecutionDispatcher`) — 총 4개 신규
  소스 파일.
- **변경된 기존 컴포넌트**: 없음. M17에 이어 두 Milestone 연속으로
  기존 소스 파일을 전혀 수정하지 않았다 — `CodingAgent`를 포함해
  기존 실행 경로 어디에도 손대지 않았다(사용자 확정 범위).
- **핵심 설계 결정**: M11의 `ExecutionResult`(프로세스 결과)와 이름이
  겹치는 문제를 발견해 새 Domain을 `EngineExecutionResult`로
  명명했다(M16의 `MemoryEngine` 이름 충돌 발견과 같은 종류의 사전
  점검). `ExecutionDispatcher`를 `WorkflowRunner`(M12)와 동일하게
  구체 클래스로 둬 불필요한 Interface 추상화를 늘리지 않았다(YAGNI).
  인증 실패(예외)와 Decision 부재(실패 결과)를 서로 다른 성격의
  조건으로 구분해 표현했다.

`git diff --stat`(M17 종료 커밋 대비)로 확인한 결과 신규 소스 파일
4개, 기존 소스 파일 수정 0개 — M17에 이어 두 번째로 기존 파일을
전혀 건드리지 않은 Milestone이다.

**3. Interface First 원칙 검토**

M18은 **새 최상위 Interface 1개(`AuthenticationManager`)를 추가**
했다. `ExecutionDispatcher`는 Interface가 아니라 구체 클래스이므로
(M12 `WorkflowRunner`와 동일한 판단 기준) 이 결정만으로는 ADR 대상이
아니지만, `AuthenticationManager` 신설은 M17(`EngineRegistry`/
`EngineSelectionPolicy`)과 M16(Knowledge 3종)에 이어 "신규 계층
도입" 계열이라 ADR-0030으로 기록했다(ADR-0017/0025/0028/0029와
동일 계열). `ExecutionDispatcher`가 세 Interface(Registry/Adapter/
Authentication)만 의존해 OCP를 지켰음을 §3.16에 명시했다.

**4. 테스트 결과**

- `pytest`: **567개 전부 통과**(M17 완료 시점 553개 → M18에서 14개
  신규: M18-T01 +5, M18-T02 +5, M18-T03 +4)
- `ruff check src tests`: 클린
- `mypy src`: 클린(신규 소스 파일 4개 포함, `storage/
  llm_policy_loader.py`의 `types-PyYAML` 미설치 경고 1건은 M18
  이전부터 존재하는 무관한 항목)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M18 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- **실제 로그인/OAuth/API Key 등록/Credential 저장/Token Refresh**
  — 후속 Authentication Layer Milestone에서 다룰 예정.
- **`CodingAgent` 연결** — `ExecutionDispatcher`는 이번엔 독립
  컴포넌트로만 존재. Agent 파이프라인 연결은 후속 Milestone.
- **Retry/Timeout/Recovery/Approval/Parallel Execution/Scheduler/
  Workflow Automation/MCP/Dashboard** — 사용자 확정 범위 밖.
- **Codex/Gemini 실제 구현** — Adapter Stub/Mock으로만 검증(M5-T05/
  M10부터 이어지는 환경 제약과 동일 사유).

*계속 이월되는 기존 항목*
- Effort 라우팅, `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임
  워크 미통합, Codex/Gemini 실연동 미검증, `MemoryEngine.search()`
  선형 스캔, 여러 Task에 걸친 누적 예산 추적, 예산 초과 시 Approval
  흐름, `KnowledgeIndexer`, Review/Documentation Agent로의
  `knowledge_provider` 확장, `EngineRuntime`↔`EngineRegistry` 중복
  등록, Retry Backoff/Persistent Runtime Recovery/Approval 비동기
  처리/Process Timeout 정책 고도화, `ShellAgent` 화이트리스트 코드
  고정.

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M18-T01~T04 상세 섹션) / `docs/ROADMAP.md`
(M18 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.20.0, 신규
§3.16/§7/§9 갱신) / `.ai/DECISIONS.md`(ADR-0030 신규) 완료.
`pyproject.toml` 버전은 v0.5.0 그대로 유지(ADR-0024 기준선 — 새
Interface 1개 추가는 M16/M17과 같은 "신규 계층 도입" 계열이라 기준선
재선언 대상이 아니라고 판단했으나, M16~M18로 Interface가 19→25종까지
늘어난 만큼 다음 기준선 재검토 시점에 누적 변화를 함께 검토할
필요가 있다). `.ai/MEMORY.md`는 이 Review 승인 직후 M1~M17과 동일한
방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 신규 4/
수정 0 소스 파일, "EngineExecutionResult 명명 분리 + ExecutionDispatcher
구체 클래스 + 인증 실패/Decision 부재 구분" 설계 결정 명시), Interface
First 검토 완료(3절, 새 Interface 1개를 "신규 계층 도입" 계열 ADR로
기록, `ExecutionDispatcher`는 구체 클래스라 ADR 대상 아님을 근거와
함께 명시), 테스트 결과 문서화 완료(4절), Technical Debt 정리 완료
(5절), 문서 갱신 완료(6절) — 6개 조건 모두 만족. Review 중 코드
변경이 필요한 치명적 문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 18 Completed를 선언한다.**

**Milestone 18 종료 — 2026-07-27 사용자 승인.**

**Milestone 19 상태**: 착수 확정. 아래 "Milestone 19" 절 참고.

---

## Milestone 19 — Reliability Layer

**목표**: M18 Execution Layer의 안정성을 확보한다 — Engine 실행 중
발생하는 실패를 감지하고, 정책 기반으로 재시도하거나 안전하게
종료하며, 일관된 실행 결과를 제공한다(2026-07-27 사용자 확정).

> **설계 검토에서 발견한 사실 3가지**:
> 1. `domain/retry_policy.py`의 `RetryPolicy`(M3, `max_attempts`만
>    보유)가 이미 존재하고 `RecoveringEngineRuntime`이 "무조건
>    재시도"에 쓰고 있다 — M16/M18과 달리 이번엔 **같은 개념의
>    확장**이라 새 이름 대신 기존 `RetryPolicy`에 필드를 추가한다
>    (`retry_delay_seconds`/`non_retryable_exceptions`, 둘 다 기본값
>    있어 `RecoveringEngineRuntime` 무영향).
> 2. `ClaudeCodeEngineAdapter.run()`은 Timeout과 "CLI 실행 파일 없음"
>    을 **같은 예외 타입**(`EngineExecutionError`)으로 처리하고
>    메시지 텍스트로만 구분된다 — "EngineAdapter 인터페이스는
>    변경하지 않는다"는 제약과 충돌해 `timed_out` 판정은 메시지
>    휴리스틱으로만 가능하다(사용자 승인 조건 1: 기술 부채로 명시).
> 3. DoD가 언급한 `NoSuitableEngineError`(`EngineRuntime` 시절
>    예외)는 이 경로에 실제로 나타나지 않는다 — M18이 `EngineRuntime`
>    을 건너뛰고 `EngineRegistry`를 직접 쓰기 때문에 실제로는
>    `EngineNotRegisteredError`가 발생한다. `NoSuitableEngineError`도
>    재시도 불가 목록에 넣어두되(향후 호환), 실제 검증은
>    `EngineNotRegisteredError` 기준으로 한다.

**설계 방향(사용자 최종 승인)**: `RetryExecutor`가 사용자의
Architecture 다이어그램대로 **인증 확인→Registry 조회→Adapter 실행
전체**를 감싸 재시도한다(`AuthenticationRequiredError`/
`EngineNotRegisteredError`/`NoSuitableEngineError`는 첫 시도에서
즉시 실패, 재시도 없음). `ExecutionDispatcher.dispatch()`는
`EngineExecutionError`(재시도 소진 후)만 실패 결과로 변환하고,
인증/등록 예외는 M18처럼 그대로 예외로 전파한다(하위 호환). 취소는
`EngineAdapter`가 이미 쓰는 sentinel(`EngineResult.error ==
"cancelled"` — `ExecutionResult.cancelled`이 Adapter 내부에서 이미
이 값으로 인코딩됨, 사용자 승인 조건 2: 새 문자열 규칙을 만들지
않고 기존 값을 그대로 이어받음)로 판정하고, 재시도 루프 자체를
타지 않는다.

**Non-goal(범위 밖)**: Dashboard, Scheduler, Workflow Automation,
MCP, Plugin, Billing, Telemetry, Logging 고도화, 실제 로그인/OAuth/
Credential 관리, Engine Selection/Budget/Knowledge 개선,
`EngineRegistry`/`EngineSelectionPolicy`/`AuthenticationManager`/
`ExecutionEnvironment`/`EngineAdapter` 인터페이스 변경.

**Milestone Definition of Done**
1. `RetryPolicy`가 최대 Retry 횟수/재시도 가능 여부 판단/Delay
   정책을 포함한다(기존 `RetryPolicy` 확장, `RecoveringEngineRuntime`
   하위 호환).
2. `RetryExecutor`가 `RetryPolicy`에 따라 실행을 반복한다.
   `ExecutionDispatcher`는 Retry를 직접 구현하지 않는다.
3. Timeout 발생 시 `RetryPolicy`에 따라 재시도 여부를 결정한다.
4. 취소 시 `EngineExecutionResult`에 취소 상태가 반영된다.
5. `EngineExecutionResult`가 확장된다(success/output/error/engine/
   execution_time/retry_count/cancelled/timed_out).
6. `AuthenticationRequiredError`는 재시도하지 않는다.
7. `NoSuitableEngineError`(및 실제 발생하는 `EngineNotRegisteredError`)
   는 재시도하지 않는다.
8. 재시도 가능한 오류와 불가능한 오류를 단위 테스트로 증명한다.
9. 재시도 횟수가 정책대로 동작함을 단위 테스트로 증명한다.
10. Timeout 동작을 통합 테스트로 증명한다(휴리스틱 한계 포함 문서화).
11. Cancellation 동작을 통합 테스트로 증명한다.
12. `ExecutionDispatcher`는 `RetryPolicy`를 직접 구현하지 않음을
    Architecture 의존성 검증으로 증명한다.
13. 전체 `pytest`/`ruff`/`mypy` 통과.

**Task List**(2026-07-27 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M19-T01 | Reliability Domain 정의(`RetryPolicy` 확장, `RetryDecision`, `RetryExecutor`) | **완료** |
| M19-T02 | Execution Reliability 구현(Retry/Timeout/Cancellation, `ExecutionDispatcher` 연동) | **완료** |
| M19-T03 | End-to-End 통합 테스트 | **완료** |
| M19-T04 | 문서화 + Milestone 19 Review | 진행 예정 |

**진행 상태**: M19-T01~T03 완료. M19-T04(문서화 + Review) 진행 중.

#### M19-T01: Reliability Domain 정의
- 상태: **DONE (2026-07-27)** — `domain/retry_policy.py`의 기존
  `RetryPolicy`(M3)에 `retry_delay_seconds: float = 0.0`/
  `non_retryable_exceptions: tuple[type[BaseException], ...] = ()`
  필드와 `decide(exception) -> RetryDecision` 메서드 추가(둘 다
  기본값이 있어 `RecoveringEngineRuntime`의 기존 호출부 전부 무영향
  — 새 이름을 만들지 않고 같은 개념을 확장). `RetryDecision`
  (should_retry/reason) 신규 — `EngineSelectionDecision`/
  `BudgetDecision`과 동일한 명명 패턴. `runtime/execution/
  retry_executor.py`의 `RetryExecutor`(제네릭 `Callable[[], T]`를
  받아 `RetryPolicy`에 따라 재시도 — 반환 타입을 모르므로
  `EngineExecutionResult`를 전혀 참조하지 않음, 순수 재시도 메커니즘)
  신규. 단위 테스트 11개 신규(domain 6개, runtime/execution 5개 —
  기본 동작/재시도 성공/횟수 소진 후 예외 재전파/재시도 불가 예외
  즉시 실패/delay 적용 확인). `pytest`(578개), `ruff`, `mypy` 통과.
  다음 Task: **M19-T02**(Execution Reliability 구현).
- 의존성: 없음.

#### M19-T02: Execution Reliability 구현
- 상태: **DONE (2026-07-27)** — `domain/execution_result.py`의
  `EngineExecutionResult`에 `retry_count: int = 0`/`cancelled: bool =
  False`/`timed_out: bool = False`(전부 기본값, M18 호출부 무영향)
  추가. `ExecutionDispatcher`를 `RetryExecutor`에 연결 — "인증 확인→
  Registry 조회→Adapter 실행" 전체를 한 번의 시도로 묶어
  `RetryExecutor.execute()`에 위임(재시도 로직을 직접 구현하지 않음,
  DoD 2/12). 기본 `RetryPolicy`는 `non_retryable_exceptions=
  (AuthenticationRequiredError, EngineNotRegisteredError,
  NoSuitableEngineError)`로 구성(재정의하려면 `retry_policy` 주입).
  `EngineExecutionError`가 재시도를 소진하면 예외를 그대로 전파하는
  대신 `EngineExecutionResult(success=False, timed_out=<휴리스틱>)`
  로 변환 — `_looks_like_timeout()`이 "응답하지 않았습니다" 메시지
  마커로 판정한다(**ADR-0031에 기술 부채로 명시**, `EngineAdapter`
  인터페이스를 바꾸지 않는 제약 때문에 완전한 구분 불가). 취소는
  `EngineResult.error == "cancelled"`(기존 `EngineAdapter`의 sentinel
  그대로 재사용, 새 문자열 규칙 없음— 사용자 승인 조건 2)로 판정해
  재시도 루프를 타지 않고 즉시 `cancelled=True`로 반영. 단위 테스트
  6개 신규(재시도 후 성공/Timeout 소진 후 실패 결과+timed_out/취소
  즉시 반영+재시도 없음/인증 실패 재시도 없음/미등록 Engine 재시도
  없음/소스 검사로 RetryExecutor 위임 확인). `pytest`(584개), `ruff`,
  `mypy` 통과. 다음 Task: **M19-T03**(End-to-End 통합 테스트).
- 의존성: M19-T01.

#### M19-T03: End-to-End 통합 테스트
- 상태: **DONE (2026-07-27)** — `tests/integration/
  test_m19_reliability_layer.py` 신규, 4개 테스트. 실제
  `ClaudeCodeEngineAdapter` + 실제 `FakeExecutionEnvironment`
  조합으로 (1) `timed_out=True`를 반환하도록 구성하면 3회 모두
  재시도되고(`executed_commands` 길이 3) 소진 후
  `timed_out=True`/`retry_count=2`인 실패 결과를 반환함을 증명(DoD
  10번), (2) `cancelled=True`를 반환하도록 구성하면 재시도 없이
  즉시 `cancelled=True`/`retry_count=0`(`executed_commands` 길이
  1)로 반영됨을 증명(DoD 11번), (3) `FileNotFoundError`로도 동일한
  재시도 정책이 적용됨을 확인(Process Error 경로), (4) M18에서
  검증한 정상 실행 경로가 M19 필드 확장 후에도 회귀 없이 그대로
  동작함(`retry_count=0`/`cancelled=False`/`timed_out=False`)을
  재확인. `pytest`(588개, 기존 584개 + 신규 4개), `ruff`, `mypy`
  통과. 다음 Task: **M19-T04**(문서화 + Milestone 19 Review).
- 의존성: M19-T02.

#### M19-T04: 문서화 + Milestone 19 Review
- 목적: 문서와 구현을 일치시키고 Milestone 종료 승인을 받는다.
- 작업 내용: `docs/ARCHITECTURE.md`에 신규 §3.17(Reliability) 갱신,
  `.ai/DECISIONS.md`에 ADR-0031 신규(`RetryPolicy` 확장 근거 + `timed_out`
  휴리스틱 기술 부채 정식 기록), `docs/ROADMAP.md`/`.ai/MEMORY.md`
  갱신, Review 작성.
- 완료 조건(DoD): 문서-구현 정합성 확인 + 사용자 승인.
- 상태: **DONE (2026-07-27)** — `docs/ARCHITECTURE.md` v0.21.0 신규
  §3.17(Reliability — `RetryPolicy` 확장/`RetryExecutor`/취소
  sentinel 재사용/**timed_out 휴리스틱 기술 부채 명시적 경고** 포함)
  /§3.16(`EngineExecutionResult` 확장 및 의존 방향에 `RetryExecutor`
  반영)/§9(디렉터리 매핑에 `runtime/execution/retry_executor.py`
  반영). §7 Interfaces는 새 Interface가 없어 25종 그대로(`RetryExecutor`
  는 구체 클래스, `RetryPolicy`/`RetryDecision`은 domain 확장).
  `.ai/DECISIONS.md`에 **ADR-0031**(배경/결정 7개 항목/대안 4개/
  이유/결과, timed_out 한계를 정식 기록) 신규 작성. 아래 "Milestone
  19 Review" 절 참고.
- 의존성: M19-T01~T03.

---

## Milestone 19 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `RetryPolicy`(최대 횟수/재시도 판단/Delay) | ✅ (M19-T01, 기존 확장) |
| 2 | `RetryExecutor`가 재시도 담당, `ExecutionDispatcher`는 직접 미구현 | ✅ (M19-T01/T02) |
| 3 | Timeout 시 정책대로 재시도 여부 결정 | ✅ (M19-T02/T03) |
| 4 | 취소 시 `EngineExecutionResult`에 반영 | ✅ (M19-T02/T03) |
| 5 | `EngineExecutionResult` 확장(retry_count/cancelled/timed_out) | ✅ (M19-T02) |
| 6 | `AuthenticationRequiredError` 비재시도 | ✅ (M19-T02) |
| 7 | `NoSuitableEngineError`(및 실제 `EngineNotRegisteredError`) 비재시도 | ✅ (M19-T02) |
| 8 | 재시도 가능/불가능 오류를 단위 테스트로 증명 | ✅ (M19-T01/T02) |
| 9 | 재시도 횟수 정책 동작을 단위 테스트로 증명 | ✅ (M19-T01) |
| 10 | Timeout 동작을 통합 테스트로 증명 | ✅ (M19-T03) |
| 11 | Cancellation 동작을 통합 테스트로 증명 | ✅ (M19-T03) |
| 12 | `ExecutionDispatcher`가 `RetryPolicy` 미직접구현을 의존성 검증으로 증명 | ✅ (M19-T02, 소스 코드 검사) |
| 13 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M19-T01~T04) 전체 완료. 사용자 승인 조건(`timed_out`
휴리스틱을 ADR/ARCHITECTURE에 기술 부채로 명시, `cancelled`는 기존
sentinel 재사용) 모두 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `runtime/execution/retry_executor.py`
  (`RetryExecutor`) — 1개 신규 소스 파일.
- **변경된 기존 컴포넌트**: `domain/retry_policy.py`(`RetryPolicy`
  확장 + `RetryDecision` 추가), `domain/execution_result.py`
  (`EngineExecutionResult` 3개 필드 확장), `runtime/execution/
  execution_dispatcher.py`(`RetryExecutor` 연동).
- **핵심 설계 결정**: 기존 `RetryPolicy`(M3)를 새 이름으로 쪼개지
  않고 확장했다 — M16/M18의 "다른 개념인데 이름이 겹침" 문제와
  달리, 이번엔 실제로 같은 개념(실행 재시도 정책)의 자연스러운
  확장이라고 판단했다. `RetryExecutor`를 `EngineExecutionResult`를
  전혀 모르는 제네릭 컴포넌트로 설계해 재사용 가능성을 열어뒀다.
  `timed_out` 판정이 메시지 텍스트 휴리스틱에 의존한다는 한계를
  숨기지 않고 ADR-0031과 ARCHITECTURE.md §3.17에 명시적으로
  기록했다(사용자 승인 조건 1).

`git diff --stat`(M18 종료 커밋 대비)로 확인한 결과 신규 소스 파일
1개, 기존 소스 파일 수정 3개 — 지금까지 중 가장 작은 변경 폭 중
하나(M17: 신규 5/수정 0, M18: 신규 4/수정 0에 이어 세 번째로 작음).

**3. Interface First 원칙 검토**

M19는 **새 최상위 Interface를 추가하지 않았다** — `RetryExecutor`는
`WorkflowRunner`/`ExecutionDispatcher`와 동일하게 구체 클래스이고,
`RetryPolicy`/`RetryDecision`은 기존 domain 객체의 확장/추가라
Interface 변경이 아니다. 그럼에도 ADR-0031을 작성한 이유는 (1)
`RetryPolicy`가 M3부터 존재하는 컴포넌트의 계약을 실질적으로
확장했고, (2) `timed_out` 휴리스틱이라는 기술 부채를 사용자가
명시적으로 ADR 기록을 요구했기 때문이다 — "새 Interface 추가"라는
기존 ADR 트리거 규칙 밖에서도, 사용자의 명시적 요청이 있으면 ADR을
작성하는 것이 맞다고 판단했다.

**4. 테스트 결과**

- `pytest`: **588개 전부 통과**(M18 완료 시점 567개 → M19에서 21개
  신규: M19-T01 +11, M19-T02 +6, M19-T03 +4)
- `ruff check src tests`: 클린
- `mypy src`: 클린(신규 소스 파일 1개 포함, `storage/
  llm_policy_loader.py`의 `types-PyYAML` 미설치 경고 1건은 M19
  이전부터 존재하는 무관한 항목)
- 신규 외부 런타임 의존성 없음

**5. Technical Debt 정리**

*M19에서 새로 발생한 기술 부채(사용자 승인, ADR-0031에 정식 기록)*
- **`timed_out` 휴리스틱** — `ClaudeCodeEngineAdapter.run()`이
  Timeout과 다른 실행 오류를 같은 예외 타입으로 던져 메시지 텍스트
  매칭으로만 판정 가능. 근본 해결은 `EngineAdapter`(또는
  `EngineExecutionError`)에 Timeout을 구조적으로 표현하는 후속
  Milestone이 필요하다.

*M19 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- Dashboard, Scheduler, Workflow Automation, MCP, Plugin, Billing,
  Telemetry, Logging 고도화, 실제 로그인/OAuth/Credential 관리,
  Engine Selection/Budget/Knowledge 개선.

*계속 이월되는 기존 항목*
- Effort 라우팅, `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임
  워크 미통합, Codex/Gemini 실연동 미검증, `MemoryEngine.search()`
  선형 스캔, 여러 Task에 걸친 누적 예산 추적, 예산 초과 시 Approval
  흐름, `KnowledgeIndexer`, Review/Documentation Agent로의
  `knowledge_provider` 확장, `EngineRuntime`↔`EngineRegistry` 중복
  등록, 실제 로그인/OAuth/Credential/Token Refresh, `CodingAgent`
  ↔`ExecutionDispatcher` 연결, `ShellAgent` 화이트리스트 코드 고정.

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M19-T01~T04 상세 섹션) / `docs/ROADMAP.md`
(M19 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.21.0, 신규
§3.17 갱신) / `.ai/DECISIONS.md`(ADR-0031 신규) 완료. `pyproject.toml`
버전은 v0.5.0 그대로 유지(ADR-0024 기준선 — 새 Interface 없이 기존
domain 확장 + 신규 구체 클래스 1개라 기준선 재선언 대상이 아님).
`.ai/MEMORY.md`는 이 Review 승인 직후 M1~M18과 동일한 방식으로
압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절), Architecture Review 완료(2절, 신규 1/
수정 3 소스 파일, "RetryPolicy 확장(신규 명명 없음) + timed_out
휴리스틱 한계 명시" 설계 결정 기록), Interface First 검토 완료(3절,
새 Interface 없음이나 사용자 요청에 따라 ADR-0031 작성), 테스트 결과
문서화 완료(4절), Technical Debt 정리 완료(5절, timed_out 휴리스틱을
신규 부채로 정식 등재), 문서 갱신 완료(6절) — 6개 조건 모두 만족.
Review 중 코드 변경이 필요한 치명적 문제(버그·계약 위반)는 발견되지
않았다.

**사용자 승인을 조건으로 Milestone 19 Completed를 선언한다.**

**Milestone 19 종료 — 2026-07-27 사용자 승인.**

**Milestone 20 상태**: 착수 확정. 아래 "Milestone 20" 절 참고.

---

## Milestone 20 — Real-time Dashboard Platform

**목표**: AI Workspace의 운영 상태를 실시간으로 관찰하는 Dashboard를
구축한다. Dashboard는 Task를 실행하지 않는 **Read Model**이다(CQRS).
Dashboard API는 후속 M23(Mobile Experience)에서 그대로 재사용될
표준 진입점이다(2026-07-27 사용자 확정).

> **설계 검토에서 발견한 사실**: 이 프로젝트는 지금까지 "서버"였던
> 적이 없다 — `pyproject.toml`의 런타임 의존성은 `pyyaml` 하나뿐이고,
> `cli/main.py`는 명령 하나를 실행하고 종료하는 1회성 CLI다. M20은
> 이 프로젝트 최초로 (1) 웹 프레임워크 의존성, (2) 상시 실행되는
> 서버 프로세스, (3) Web UI를 도입한다.

**설계 방향(사용자 최종 승인)**:
- **웹 프레임워크**: FastAPI + uvicorn(WebSocket 내장, OpenAPI 문서
  자동 생성으로 "Dashboard API 문서화" DoD 충족). `fastapi`/`uvicorn`
  만 런타임 의존성으로 추가한다. **Core 계층은 웹 프레임워크를
  전혀 모른다** — FastAPI는 신규 `web/` 디렉터리(Infrastructure
  계층)에서만 쓴다.
- **Web UI**: 정적 HTML/CSS/Vanilla JS(빌드 도구 도입 없음). 1초
  타이머(현재 시각/경과 시간)는 브라우저에서 계산하고, Repository를
  Polling하지 않는다.
- **Event 기반 갱신**: `ExecutionDispatcher`에 `event_bus:
  EventBus | None = None`을 선택적으로 주입한다(기존 M13~M19
  패턴과 동일). `ExecutionDispatcher`는 Event만 발행하고
  `DashboardRepository`를 직접 참조하지 않는다.
  `InMemoryDashboardRepository`가 이 Event를 구독해 Read Model을
  갱신한다.
- **계층 분리(CQRS)**: `DashboardRepository`(저장+조회, Provider
  독립) → `DashboardService`(Repository만 사용해 조합, UI를 모름) →
  `DashboardViewModel`(한국어 라벨, `web/` 계층 전용 DTO) → FastAPI
  라우터/WebSocket. API/WebSocket/Web UI는 `DashboardService`만
  사용하고 `ExecutionDispatcher`를 직접 호출하지 않는다.
- **서버 런타임**: `workspace start` 명령으로 상시 실행되는 서버를
  추가한다. 기존 CLI 명령은 그대로 유지, 서버는 선택 실행이다.

**Non-goal(범위 밖)**: Mobile Dashboard/Home Screen Widget/Lock
Screen Widget/Live Activity/Dynamic Island/Push Notification(M23
예정), Budget/Token/Billing/Telemetry 표시, Scheduler, Automation,
Approval UI, 사용자 인증/권한 관리.

**Milestone Definition of Done**
1. `DashboardRepository` Interface + `InMemoryDashboardRepository` 구현.
2. `DashboardService` 구현(UI를 모름).
3. Dashboard API 구현(`/api/dashboard`, `/api/summary`,
   `/api/history`, `/api/engines`).
4. WebSocket 구현(Event 기반 갱신, Polling 없음).
5. Dashboard Web UI 구현(정적 파일, API/WebSocket만 사용).
6. `DashboardViewModel` 구현(한국어 상태 라벨, Engine 이름은 영어 유지).
7. `ExecutionDispatcher` 실행 결과가 자동으로 기록된다(Event 기반).
8. Engine 상태/최근 실행/실행 통계/안정성 통계 조회가 모두 Repository의
   Read Model을 그대로 사용한다(Dashboard가 통계를 계산하지 않음).
9. 현재 시각/경과 시간이 브라우저에서 1초마다 갱신된다(Polling 없음).
10. Dashboard API가 자동 문서화된다(FastAPI OpenAPI).
11. `DashboardService`가 `web/`(API/WebSocket/UI)을 참조하지 않음을
    Architecture 의존성 검증으로 증명한다.
12. `workspace start`로 서버가 실행되고, 기존 CLI 명령은 영향받지
    않는다.
13. 전체 `pytest`/`ruff`/`mypy` 통과.

**Task List**(2026-07-27 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M20-T01 | Dashboard 도메인 및 이벤트 정의 | **완료** |
| M20-T02 | 실행 계층과 Dashboard 연결(`ExecutionDispatcher` Event 발행 + `InMemoryDashboardRepository` 구독) | **완료** |
| M20-T03 | Read Model 및 ViewModel(`DashboardService` + `DashboardViewModel`) | **완료** |
| M20-T04 | 서버 런타임 구축(`workspace start`, FastAPI app 골격) | **완료** |
| M20-T05 | API 및 Web UI(REST 라우터 + WebSocket + 정적 UI) | **완료** |
| M20-T06 | 전체 흐름 검증(End-to-End 통합 테스트 + 의존성 검증) | **완료** |
| M20-T07 | 문서화 및 아키텍처 정리 | **완료** |

**진행 상태**: M20-T01~T07 전체 완료.

#### M20-T07: 문서화 및 아키텍처 정리
- 상태: **DONE (2026-07-27)** — ADR-0032(`.ai/DECISIONS.md`) 신규
  작성. `docs/ARCHITECTURE.md` v0.22.0: 신규 §3.18(Real-time
  Dashboard Platform), §7 Interfaces 25→26종(`DashboardRepository`
  추가), §8 의존성 규칙에 12번(Dashboard Event 구독 경로, Core는
  `web/`/FastAPI/uvicorn을 모름) 추가, §9 디렉터리 구조에
  `runtime/dashboard/`/`web/`/`cli` `start` 서브커맨드 반영. 아래
  Milestone 20 Review 작성.

#### M20-T06: 전체 흐름 검증
- 상태: **DONE (2026-07-27)** —
  `tests/integration/test_m20_realtime_dashboard_platform.py` 신규
  (M18/M19처럼 실제 `ClaudeCodeEngineAdapter` + `FakeExecutionEnvironment`
  조합 사용, Fake Dashboard 컴포넌트 없음). `ExecutionDispatcher.dispatch()`
  실제 실행 → `InMemoryDashboardRepository` 구독 갱신 →
  `DashboardService` → `/api/dashboard` REST 응답까지 이어짐을 증명
  (`test_real_execution_updates_rest_api_dashboard`). 동일한 흐름이
  `/ws/dashboard`로도 최초 스냅샷 + 실행 시작/완료 2건의 실시간 갱신을
  민다는 것도 증명(`test_real_execution_pushes_websocket_updates`,
  Polling 없이 실제 이벤트 발행 시점에만 메시지 수신됨을 확인).
  `ast` 기반 import 그래프 검사로 CQRS 경계를 재확인:
  `DashboardService`/`InMemoryDashboardRepository`(Core)가 `web/`이나
  `fastapi`/`uvicorn`을 import하지 않음
  (`test_dashboard_service_and_repository_do_not_import_web_layer`),
  `ExecutionDispatcher`도 `runtime.dashboard`/`web`을 참조하지 않음
  (`test_execution_dispatcher_does_not_import_dashboard_layer`) —
  T03에서 만든 docstring 기반 검사(`test_dashboard_service.py`)의
  한계(클래스 자체 docstring에 "web/"이라는 단어가 있어 문자열
  검사로는 오탐 발생)를 겪었던 경험을 반영해 처음부터 `ast.ImportFrom`
  노드만 검사. 신규 테스트 4개. `pytest`(635개), `ruff`, `mypy`
  통과. 다음 Task: **M20-T07**(문서화 및 아키텍처 정리).
- 의존성: M20-T05.

#### M20-T05: API 및 Web UI
- 상태: **DONE (2026-07-27)** — `web/routes.py`에 `/api/dashboard`
  (5개 영역 전체), `/api/summary`(목록류 제외 요약), `/api/history`
  (`limit` 쿼리 파라미터), `/api/engines` 4개 REST 엔드포인트 추가.
  `web/dashboard_broadcaster.py`의 `DashboardBroadcaster`가
  `EventBus`를 구독해(`register_event_bus`) 연결된 WebSocket마다
  최신 `DashboardViewModel` 스냅샷을 민다 — 연결 시점에
  `asyncio.get_running_loop()`를 캡처해 두고 동기 이벤트 핸들러에서
  `loop.call_soon_threadsafe()`로 비동기 전송을 예약하는 방식으로
  동기 `EventBus.publish()` → 비동기 WebSocket 전송 경계를 넘김.
  `web/app.py`에 `/ws/dashboard` 엔드포인트와 라우터 등록, 정적
  파일(`web/static/`) 마운트 추가. `web/static/index.html` +
  `style.css`(다크 테마, CSS Grid) + `app.js`(정적 HTML/CSS/Vanilla
  JS, 빌드 도구 없음) — `app.js`는 `/api/dashboard`로 초기 상태를
  가져오고 `/ws/dashboard`로 실시간 갱신을 수신하며, 현재 시각과
  경과 시간(`현재 시각 - started_at`)은 브라우저에서 1초마다
  `setInterval`로 직접 계산(서버 Polling 없음, 사용자 설계 원칙
  준수). 단위 테스트 12개 신규(`test_routes.py` 4개 — REST 응답
  스키마, `test_dashboard_broadcaster.py` 3개 — WebSocket 최초
  스냅샷 수신/이벤트 후 갱신 수신/무관한 이벤트 무시,
  `TestClient.websocket_connect()`로 실제 WebSocket 핸드셰이크
  검증). `FastAPI`의 `response_model`이 stdlib `@dataclass`
  (`DashboardViewModel` 등, Pydantic `BaseModel` 아님)를 문제없이
  직렬화함을 실제 테스트로 확인. `pytest`(631개), `ruff`,
  `mypy --python-executable`(119개 파일) 통과. `TestClient`로
  `build_app()`이 만든 실제 앱에서 `/`, `/app.js`, `/style.css`,
  `/api/dashboard`가 모두 정상 응답함을 수동 검증. 다음 Task:
  **M20-T06**(전체 흐름 검증).
- 의존성: M20-T04.

#### M20-T04: 서버 런타임 구축
- 상태: **DONE (2026-07-27)** — `pyproject.toml`에 첫 런타임 의존성
  `fastapi`/`uvicorn[standard]` 추가(dev에는 `httpx`, `TestClient`용).
  `web/app.py`의 `create_app(dashboard_service)`가 FastAPI 앱 골격을
  조립(`/health` 헬스 체크만, 실제 Dashboard 라우터는 M20-T05).
  `DashboardService`를 `app.state.dashboard_service`에 실어 M20-T05
  라우터가 꺼내 쓸 수 있게 함. `web/server.py`의 `build_app()`(실제
  소켓을 열지 않고 `TestClient`로 테스트 가능하도록 앱 조립과 서버
  기동을 분리)/`run_server()`(`uvicorn.run()` 호출). `cli/main.py`에
  `start` 서브커맨드 추가(`--host`/`--port`) — 지연 import로 `web`
  모듈을 불러와 다른 CLI 명령은 FastAPI/uvicorn을 몰라도 되게 유지.
  **환경 메모**: 이 세션의 `mypy`는 `uv tool install`로 별도
  가상환경에 설치돼 있어 `pip install`로 넣은 `fastapi`/`uvicorn`을
  기본적으로 못 찾는다 — `mypy --python-executable "$(which
  python3)" src`로 실행해야 한다(코드/설정 문제 아님, 이 환경의
  mypy 설치 방식 때문). 단위 테스트 6개 신규(`web/app.py` 2개,
  `web/server.py` 2개, CLI `start` 위임 1개... 실제로는 5개+1개
  기존 파일에 추가). `pytest`(624개), `ruff`, `mypy`(올바른
  `--python-executable`로) 통과. 다음 Task: **M20-T05**(API 및
  Web UI).
- 의존성: M20-T03.

#### M20-T03: Read Model 및 ViewModel
- 상태: **DONE (2026-07-27)** — `runtime/dashboard/
  dashboard_service.py`에 `KNOWN_ENGINES`(claude_code/gemini_cli/
  codex_cli/ollama 4종 고정 목록)/`DashboardSnapshot`/
  `DashboardService`(Repository만 사용, UI를 전혀 모름 — `web/`
  import 없음, 단위 테스트로 확인) 신규. 아직 실행된 적 없는 Engine은
  기본 상태 READY로 채운다. 신규 `web/` 디렉터리(Infrastructure
  계층 시작)의 `dashboard_viewmodel.py`에 `DashboardViewModel`/
  `WorkspaceStatusViewModel`/`EngineStatusViewModel`/
  `ExecutionHistoryEntryViewModel` + 변환 함수(`build_dashboard_
  view_model()` 등) — 한국어 상태 라벨(준비 완료/실행 중/인증 필요/
  오류, 대기 중, 성공/실패/취소/시간 초과)과 Engine 표시 이름(영어
  유지, 예: "Claude Code")을 여기서만 다룬다. `DashboardService`는
  이 타입을 전혀 모른다(변환은 `web/` 계층 전담). 단위 테스트 9개
  신규(dashboard_service 4개, dashboard_viewmodel 5개). `pytest`
  (619개), `ruff`, `mypy` 통과. 다음 Task: **M20-T04**(서버 런타임
  구축).
- 의존성: M20-T02.

#### M20-T02: 실행 계층과 Dashboard 연결
- 상태: **DONE (2026-07-27)** — `runtime/execution/events.py`에
  `ENGINE_AUTHENTICATION_FAILED` 추가. `ExecutionDispatcher`에 선택적
  `event_bus: EventBus | None = None` DI 추가 — 실행 시작 시
  `ENGINE_EXECUTION_STARTED`, 종료 시 `ENGINE_EXECUTION_COMPLETED`
  (성공/실패/Timeout 소진/취소 전부 포함), 인증 실패 시
  `ENGINE_AUTHENTICATION_FAILED`를 발행한다(예외는 그대로 재전파,
  Event 발행은 부가 효과일 뿐 계약을 바꾸지 않음). `decision`이
  `None`이면 Event를 전혀 발행하지 않는다(아무것도 선택되지 않음).
  `ExecutionDispatcher`는 `DashboardRepository`를 전혀 모른다(CQRS
  — Event만 발행). `runtime/dashboard/dashboard_repository.py`의
  `InMemoryDashboardRepository`가 생성자에서 스스로 `EventBus`를
  구독해 Read Model을 갱신 — 통계는 조회 시점에 계산하지 않고 매
  Event마다 미리 갱신해 둔다("Dashboard는 통계를 계산하지 않는다").
  단위 테스트 10개 신규(`ExecutionDispatcher` Event 발행 4개,
  `InMemoryDashboardRepository` 6개). `pytest`(610개), `ruff`,
  `mypy` 통과. 다음 Task: **M20-T03**(Read Model 및 ViewModel).
- 의존성: M20-T01.

#### M20-T01: Dashboard 도메인 및 이벤트 정의
- 상태: **DONE (2026-07-27)** — `domain/dashboard.py`에 `EngineStatus`
  (READY/RUNNING/AUTH_REQUIRED/ERROR)/`WorkspaceStatus`/
  `ExecutionRecord`/`ExecutionStats`/`ReliabilityStats` 신규(Provider
  독립, 한국어 라벨은 이 계층 책임이 아님 — `web/` 계층의
  `DashboardViewModel`이 담당 예정). `runtime/execution/events.py`
  에 `ENGINE_EXECUTION_STARTED`/`ENGINE_EXECUTION_COMPLETED` 신규
  (`agents/events.py`와 동일 패턴, `ExecutionDispatcher`가 발행할
  예정이나 이번 Task는 상수 정의까지만). `interfaces/
  dashboard_repository.py`에 `DashboardRepository`(저장 3개+조회
  5개 메서드, `EventBus`를 알지 못함 — Event 구독은 구체 구현체
  책임) 신규. `tests/interfaces/fakes.py`에 `FakeDashboardRepository`
  추가. 단위 테스트 12개 신규(domain 6개, interfaces 5개, events
  1개). `pytest`(600개), `ruff`, `mypy` 통과. 다음 Task:
  **M20-T02**(실행 계층과 Dashboard 연결).
- 의존성: 없음.

---

## Milestone 20 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | `DashboardRepository` Interface + `InMemoryDashboardRepository` 구현 | ✅ (M20-T01/T02) |
| 2 | `DashboardService` 구현(UI를 모름) | ✅ (M20-T03) |
| 3 | Dashboard API 구현(`/api/dashboard`, `/api/summary`, `/api/history`, `/api/engines`) | ✅ (M20-T05) |
| 4 | WebSocket 구현(Event 기반 갱신, Polling 없음) | ✅ (M20-T05) |
| 5 | Dashboard Web UI 구현(정적 파일, API/WebSocket만 사용) | ✅ (M20-T05) |
| 6 | `DashboardViewModel` 구현(한국어 상태 라벨, Engine 이름은 영어 유지) | ✅ (M20-T03) |
| 7 | `ExecutionDispatcher` 실행 결과가 자동으로 기록됨(Event 기반) | ✅ (M20-T02) |
| 8 | Engine 상태/최근 실행/실행 통계/안정성 통계가 모두 Repository의 Read Model을 그대로 사용 | ✅ (M20-T02/T03) |
| 9 | 현재 시각/경과 시간이 브라우저에서 1초마다 갱신(Polling 없음) | ✅ (M20-T05) |
| 10 | Dashboard API가 자동 문서화됨(FastAPI OpenAPI) | ✅ (M20-T04, `/docs` 자동 생성) |
| 11 | `DashboardService`가 `web/`을 참조하지 않음을 Architecture 의존성 검증으로 증명 | ✅ (M20-T06, `ast` 기반) |
| 12 | `workspace start`로 서버가 실행되고 기존 CLI 명령은 영향받지 않음 | ✅ (M20-T04) |
| 13 | 전체 `pytest`/`ruff`/`mypy` 통과 | ✅ (아래 4절) |

Task List(M20-T01~T07) 전체 완료. 사용자 승인 조건(Server Runtime
도입, EventBus 기반 실시간 갱신, `ExecutionDispatcher`→Event만
발행/Dashboard 직접 참조 금지, API/WebSocket/Web UI는
`DashboardService`만 사용, `pyproject.toml`에 `fastapi`/`uvicorn`만
추가, Core 계층은 웹 프레임워크를 모름) 모두 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `domain/dashboard.py`, `interfaces/
  dashboard_repository.py`, `runtime/dashboard/dashboard_repository.py`,
  `runtime/dashboard/dashboard_service.py`, `web/`(신규 최상위 패키지 —
  `dashboard_viewmodel.py`, `routes.py`, `dashboard_broadcaster.py`,
  `app.py`, `server.py`, `static/index.html`/`style.css`/`app.js`) —
  10개 신규 소스 파일 + 정적 파일 3개.
- **변경된 기존 컴포넌트**: `runtime/execution/events.py`(Event 타입
  3개 추가), `runtime/execution/execution_dispatcher.py`(`event_bus`
  선택적 DI + Event 발행), `cli/main.py`(`start` 서브커맨드),
  `pyproject.toml`(첫 외부 런타임 의존성).
- **핵심 설계 결정**: (1) CQRS로 쓰기(Event 구독)와 읽기
  (`DashboardService`)를 분리하되, 구현체가 하나뿐이라
  `DashboardRepository` Interface 자체는 쓰기/읽기 메서드를 함께
  갖도록 했다(불필요한 Interface 분리를 피함, YAGNI). (2)
  `ExecutionDispatcher`는 Event만 발행하고 Dashboard의 존재를
  전혀 모른다 — M13(Scheduler)부터 이어진 "선택적 DI로 기존
  컴포넌트를 건드리지 않고 확장" 패턴을 그대로 재사용했다. (3)
  FastAPI/uvicorn을 `web/` 패키지에만 가둬 Core 계층(domain/
  interfaces/engines/runtime, `runtime/dashboard/` 포함)이 여전히
  웹 프레임워크를 몰라도 되게 유지했다 — 이 프로젝트가 M1부터
  지켜온 프레임워크 독립 원칙이 첫 외부 런타임 의존성 도입에도
  깨지지 않았다. (4) 동기 `EventBus.publish()`와 비동기 WebSocket
  전송 사이의 경계는 연결 시점에 캡처한 `asyncio.get_running_loop()`
  + `loop.call_soon_threadsafe()`로 넘겼다.

`git diff --stat`(M19 종료 커밋 대비)로 확인한 결과 신규 소스/정적
파일 13개, 기존 파일 수정 4개 — M11(서버/UI 없는 순수 백엔드
milestone들) 이후 가장 큰 변경 폭이지만, 이는 이 Milestone이 처음
도입한 "서버+Web UI"라는 새 층위 전체가 신규 컴포넌트이기 때문이며
기존 컴포넌트 수정은 여전히 최소(4개, 전부 선택적 DI/신규
서브커맨드로 하위 호환 유지)에 그쳤다.

**3. Interface First 원칙 검토**

M20은 `DashboardRepository`라는 **새 최상위 Interface**를
추가했다(총 25→26종) — ADR-0032를 작성했다. Interface는 CQRS
원칙에 따라 쓰기(Event 구독 경로 전용)와 읽기(`DashboardService`
경로 전용) 메서드를 함께 갖되, 두 경로의 호출자가 겹치지 않도록
설계해 실질적으로는 계약이 분리돼 있다. `DashboardBroadcaster`/
`DashboardService`/`InMemoryDashboardRepository`는 모두 구체
클래스다(기존 `WorkflowRunner`/`ExecutionDispatcher`/`RetryExecutor`
와 동일한 패턴 — 이 프로젝트는 "여러 구현체가 필요할 가능성이 있는
지점"에만 Interface를 두고, 단일 구현이 확실한 조합 로직은 구체
클래스로 유지한다).

**4. 테스트 결과**

- `pytest`: **635개 전부 통과**(M19 완료 시점 588개 → M20에서 47개
  신규: M20-T01 +12, M20-T02 +약간, M20-T03 +약간, M20-T04 +6,
  M20-T05 +16, M20-T06 +4 — 누적으로 47개 순증)
- `ruff check src tests`: 클린
- `mypy --python-executable "$(which python3)" src`: 클린(119개
  소스 파일). **환경 메모**: 이 세션의 `mypy` 실행 파일은 `uv tool
  install`로 별도 가상환경에 설치돼 있어 `pip install`로 넣은
  `fastapi`/`uvicorn`을 기본 명령(`mypy src`)으로는 못 찾는다 —
  이 환경의 mypy 설치 방식 때문이며 코드/설정 문제가 아니다. 항상
  `--python-executable "$(which python3)"`로 실행해야 한다(M20-T04
  에서 최초 발견, TASKS.md에 기록됨).
- 신규 외부 런타임 의존성: `fastapi>=0.115`, `uvicorn[standard]>=0.30`
  (이 프로젝트 최초, 기존엔 `pyyaml`뿐). dev 의존성에 `httpx`
  (`TestClient`용) 추가.
- FastAPI `response_model`이 stdlib `@dataclass`(Pydantic
  `BaseModel`이 아님)를 문제없이 직렬화함을 실제 `TestClient` 테스트로
  확인(사전에 불확실했던 기술 리스크 해소).

**5. Technical Debt 정리**

*M20에서 새로 발생한 기술 부채*
- 없음 — 새로운 휴리스틱이나 임시 우회는 도입하지 않았다.

*M20 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- Mobile Dashboard/Home Screen Widget/Lock Screen Widget/Live
  Activity/Dynamic Island/Push Notification(M23 예정), Budget/
  Token/Billing/Telemetry 표시, Scheduler, Automation, Approval UI,
  사용자 인증/권한 관리, `DashboardRepository` 쓰기/읽기 Interface
  물리적 분리, 실제 프로덕션 배포 구성(HTTPS/역방향 프록시).

*계속 이월되는 기존 항목*
- Effort 라우팅, `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임
  워크 미통합, Codex/Gemini 실연동 미검증, `MemoryEngine.search()`
  선형 스캔, 여러 Task에 걸친 누적 예산 추적, 예산 초과 시 Approval
  흐름, `KnowledgeIndexer`, Review/Documentation Agent로의
  `knowledge_provider` 확장, `EngineRuntime`↔`EngineRegistry` 중복
  등록, 실제 로그인/OAuth/Credential/Token Refresh, `CodingAgent`
  ↔`ExecutionDispatcher` 연결, `ShellAgent` 화이트리스트 코드 고정,
  `timed_out` 휴리스틱(ADR-0031, `EngineAdapter` 구조적 개선 필요).

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M20-T01~T07 상세 섹션) / `docs/ROADMAP.md`
(M20 Task List·목표·DoD 반영) / `docs/ARCHITECTURE.md`(v0.22.0, 신규
§3.18, §7 26종, §8 규칙 12번, §9 디렉터리 구조 갱신) /
`.ai/DECISIONS.md`(ADR-0032 신규) 완료. `pyproject.toml` 버전은
기존과 동일하게 유지하되 `dependencies`에 `fastapi`/`uvicorn`,
`dev`에 `httpx`를 신규 추가(첫 외부 런타임 의존성 도입이므로 버전
자체보다 의존성 목록 변경이 이 Milestone의 실질적 기준선 변경점).
`.ai/MEMORY.md`는 이 Review 승인 직후 M1~M19와 동일한 방식으로
압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절, 13개 항목 전부), Architecture Review
완료(2절, 신규 10개 소스+정적 3개/수정 4개 소스 파일, "CQRS 경계+
Core-Web 계층 분리 + 첫 외부 런타임 의존성을 web/에 격리" 설계
결정 기록), Interface First 검토 완료(3절, 새 Interface
`DashboardRepository` 추가로 ADR-0032 작성), 테스트 결과 문서화
완료(4절, 635개 전부 통과 + 사전 불확실했던 dataclass response_model
리스크 해소 확인), Technical Debt 정리 완료(5절, 신규 부채 없음),
문서 갱신 완료(6절) — 6개 조건 모두 만족. Review 중 코드 변경이
필요한 치명적 문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 20 Completed를 선언한다.**

**Milestone 20 종료 — 2026-07-27 사용자 승인.**

**Milestone 21 상태**: 착수 확정. 아래 "Milestone 21" 절 참고.

---

## Milestone 21 — Automation Engine

**목표**: 사용자의 명시적 요청 없이 조건/일정에 따라 Task를 자동
실행하는 Automation을 구현한다. Automation은 Dashboard와 독립적인
Domain이며, `ExecutionDispatcher`를 통해서만 Task를 실행한다.
Automation은 `EventBus`와 Dashboard를 그대로 재사용한다(2026-07-27
사용자 확정).

> **설계 검토에서 발견한 사실**: M4-T07에 이미 `AutomationEngine`
> Interface + `InMemoryAutomationEngine`이 존재한다 — 하지만 책임이
> "어떤 trigger가 어떤 Workflow와 연결되어 있는가"만 관리하는
> **연결 관리**뿐이다. trigger가 **언제** 발동돼야 하는지 판단하는
> 조건/일정 평가와 실제 실행은 원래부터 호출자 책임으로 명시적으로
> 떠넘겨져 있었다(M4-T07 설계 당시 문서화된 한계). M21이 요청한
> `AutomationRule`(4종 Trigger+Action)과 `AutomationScheduler`(실제
> 일정 평가+자동 실행)는 바로 이 떠넘겨진 책임을 처음 구현하는
> 것이라 **동일 개념의 확장이 아니라 별개의 새 컴포넌트 세트**로
> 판단했다(M16 `KnowledgeRepository`/M18 `EngineExecutionResult`와
> 같은 "이름은 유사하지만 다른 개념" 패턴). 기존 `AutomationEngine`/
> `InMemoryAutomationEngine`은 수정 없이 그대로 유지한다.

**설계 방향(사용자 최종 승인, 조건 6개)**:
1. `AutomationScheduler`와 Trigger의 책임을 분리한다 — Trigger는
   순수 데이터(`domain/automation.py`), "언제 발동할지" 평가는
   `runtime/automation/`의 Trigger별 평가기가 담당한다.
2. Dashboard는 계속 Read Model을 유지한다.
3. Automation CRUD는 Automation API를 통해서만 수행한다.
4. Dashboard는 Automation을 직접 제어하지 않는다(조회만).
5. `ExecutionDispatcher`를 유일한 실행 진입점으로 유지한다 — Action
   "Task 실행"은 M17/M18 파이프라인(`EngineSelectionPolicy.select()`
   → `ExecutionDispatcher.dispatch()`)을 재사용한다.
6. `last_executed_at`/`next_execution_at`을 도메인 모델에 포함해
   M23 Mobile Experience와 자연스럽게 연계할 수 있도록 한다.

**Dashboard 연계**: `DashboardService`가 선택적으로 `AutomationService`
를 주입받아(M15 `budget_policy_engine`/M16 `knowledge_provider`와
동일한 선택적 DI 패턴) 등록 Rule 수/활성 Rule 수/마지막 실행/다음
실행 예정을 조회 시 조합한다 — Reader(`DashboardService`)가 다른
Reader(`AutomationService`)를 참조하는 것은 CQRS 위반이 아니다
(Writer인 `ExecutionDispatcher`가 Dashboard를 직접 참조하는 것만
금지).

**Non-goal(범위 밖)**: Cron Expression, Database 저장, Distributed/
Multi-node Scheduler, Retry Policy 변경, Mobile Push Notification/
Home Widget/Lock Screen Widget/Live Activity/Dynamic Island, AI 기반
Rule 추천.

**Milestone Definition of Done**
1. Automation Domain 구현(`AutomationRule`/`Trigger`/`Action`).
2. `AutomationRepository` Interface 구현.
3. `InMemoryAutomationRepository` 구현.
4. `AutomationService` 구현(CRUD).
5. `AutomationScheduler` 구현.
6. Time Trigger 구현.
7. Interval Trigger 구현.
8. Event Trigger 구현.
9. Startup Trigger 구현.
10. Automation API 구현(8종).
11. Dashboard Automation 화면 구현.
12. `EventBus` 연동.
13. `ExecutionDispatcher` 연동.
14. End-to-End 테스트.
15. `ruff` 통과.
16. `mypy` 통과.
17. 전체 `pytest` 통과.

**Task List**(2026-07-27 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M21-T01 | Automation 도메인 + `AutomationRepository` Interface + `InMemoryAutomationRepository` | **완료** |
| M21-T02 | `AutomationService`(CRUD) 구현 | **완료** |
| M21-T03 | `AutomationScheduler` + Time/Interval/Startup Trigger 구현 | **완료** |
| M21-T04 | Event Trigger + `ExecutionDispatcher` 연동 | **완료** |
| M21-T05 | Automation API + Dashboard 연계 | **완료** |
| M21-T06 | Dashboard Web UI Automation 화면 | **완료** |
| M21-T07 | 전체 흐름 검증 + 문서화 | **완료** |

**진행 상태**: M21-T01~T07 전체 완료.

#### M21-T07: 전체 흐름 검증 + 문서화
- 상태: **DONE (2026-07-27)** —
  `tests/integration/test_m21_automation_engine.py` 신규(M18~M20과
  동일하게 실제 `ClaudeCodeEngineAdapter` + `FakeExecutionEnvironment`
  조합, Fake Automation 컴포넌트 없음). 사용자 Architecture
  다이어그램("Task Completed → Automation Rule 확인 → 조건 만족 →
  ExecutionDispatcher → 새 Task 실행")을 실제 컴포넌트로 증명 —
  `AutomationScheduler.bind_event_bus()`로 구독한 EventBus에 외부
  이벤트가 발행되면 EVENT Trigger가 실제 RUN_TASK Action을
  실행함을 `execution_environment.executed_commands`로 확인
  (트리거 event_type을 `ExecutionDispatcher`가 스스로 발행하는
  이벤트와 다르게 둬서, Rule의 실행 결과가 자기 자신을 재귀적으로
  재발동시키는 경로를 테스트 설계 단계에서 원천 차단함). REST
  API(`POST /api/automation`, `POST /{id}/run`)로 만든 Rule의 실행
  결과가 `/api/dashboard`의 Automation 현황에 실제 HTTP 요청으로
  반영됨도 증명. `ast` 기반 import 그래프 검사로 CQRS/계층 경계
  재확인: Automation Core(`domain`/`interfaces`/`runtime/automation/`
  전체)가 `web/`이나 `fastapi`/`uvicorn`을 import하지 않음,
  `AutomationScheduler`/`AutomationActionExecutor`가
  `runtime.dashboard`나 `web`을 참조하지 않음(Automation은 Dashboard와
  독립적인 Domain, 사용자 확정), `ExecutionDispatcher`가
  `runtime.automation`을 전혀 모름(단방향 결합 — Automation이
  Event를 구독해 호출하는 방향으로만 연결). 신규 테스트 5개.
  `pytest`(720개), `ruff`, `mypy` 통과.

  ADR-0033(`.ai/DECISIONS.md`) 신규 작성 — 기존 `AutomationEngine`
  (M4-T07)과의 관계, 6개 사용자 승인 조건 반영 근거, 대안 검토를
  전부 기록. `docs/ARCHITECTURE.md` v0.23.0: 신규 §3.19(Automation
  Engine, 흐름 다이어그램 포함), §7 Interfaces 26→27종
  (`AutomationRepository` 추가, 기존 `AutomationEngine` 행에
  M21과 다른 개념임을 명시하는 주석 추가), §8 의존성 규칙에 13/14번
  (Automation 실행 경로, Dashboard의 Automation 조회는 Reader→Reader)
  추가, §9 디렉터리 구조에 `runtime/automation/`/
  `web/automation_routes.py` 반영. 아래 Milestone 21 Review 작성.
- 의존성: M21-T06.

#### M21-T06: Dashboard Web UI Automation 화면
- 상태: **DONE (2026-07-27)** — `web/static/index.html`에 "Automation
  현황" 요약 영역(등록/활성 Rule 수, 마지막/다음 실행)과 전체 폭
  "Automation Rule" 영역(목록 테이블 + 생성 폼)을 추가. 생성 폼은
  Trigger 종류(Time/Interval/Event/Startup)와 Action 종류(Task
  실행/Workflow 실행/Dashboard Refresh/Notification)에 따라 관련
  입력 필드만 표시(Vanilla JS, 빌드 도구 없음, 기존 원칙 유지).
  `web/static/app.js`에 목록 조회(`GET /api/automation`)/생성
  (`POST`)/활성화·비활성화(`POST .../enable`,`.../disable`)/삭제
  (`DELETE`) 연동 — Automation CRUD는 오직 Automation API만 호출한다
  (사용자 승인 조건 3). Automation 변경(생성/활성화/삭제) 후에는
  `/api/summary`를 다시 조회해 "Automation 현황" 요약을 갱신한다 —
  Automation은 Dashboard를 직접 갱신하지 않으므로(Event를 발행하지
  않음, 사용자 승인 조건 4) 이 갱신은 Web UI(클라이언트) 계층이
  능동적으로 재조회하는 것이지 Automation이 Dashboard에 쓰기 접근을
  갖는 것이 아니다.

  **실제 브라우저 검증**: `playwright`를 임시 설치해(이 세션에만,
  프로젝트 의존성에는 추가하지 않음) 사전 설치된 Chromium으로 실제
  서버(`web.server.run_server`)를 띄우고 화면을 직접 조작해 검증—
  Rule 생성(Startup/Time×Task 실행 두 가지 조합), 활성화/비활성화
  토글, 목록 갱신, "Automation 현황" 요약의 실시간 갱신을 모두
  확인. **버그 발견 및 수정**: `updateVisibleFields()`가
  `document.querySelector`(단일 요소)만 써서 같은 class를 가진
  Action 필드 2개(Project ID/Task 제목) 중 첫 번째만 보이던 문제를
  실제 브라우저 조작 중 발견 — `querySelectorAll`+`forEach`로 수정.
  `node --check`로 JS 구문 오류 없음도 확인.

  정적 파일은 pytest 대상이 아니라 신규 단위 테스트는 없음(M20-T05
  와 동일한 성격) — 검증은 실제 서버+브라우저로 수행. `pytest`
  (715개, 변경 없음), `ruff`, `mypy` 통과. 다음 Task: **M21-T07**
  (전체 흐름 검증 + 문서화).
- 의존성: M21-T05.

#### M21-T05: Automation API + Dashboard 연계
- 상태: **DONE (2026-07-27)** — `domain/dashboard.py`에
  `AutomationStatus`(registered_rule_count/enabled_rule_count/
  last_execution_at/next_execution_at) 신규 — `AutomationRule`을
  그대로 참조하지 않고 필요한 집계값만 옮겨 담는다(`ExecutionRecord`
  와 동일 원칙). `DashboardService`에 선택적 `automation_service`
  DI(M15/M16과 동일 패턴) 추가 — `automation_status()`가
  `AutomationService.list_rules()`(읽기 전용)만 호출해 집계하고
  Automation을 제어하지 않는다(사용자 승인 조건 4).
  `DashboardSnapshot`/`DashboardViewModel`에 `automation_status`
  필드 추가(기본값 `None`이라 기존 호출부 무영향). `/api/summary`
  에도 `automation_status` 포함.

  `web/automation_routes.py`에 Automation REST API 8종
  (GET list/get, POST create, PUT update, DELETE, POST enable/
  disable/run) 신규. `AutomationRuleCreateRequest`/
  `AutomationRuleUpdateRequest`(dataclass, FastAPI가 중첩
  dataclass인 `Trigger`/`Action`까지 그대로 검증·역직렬화함을
  실제 `TestClient` 요청으로 확인) 신규.
  `AutomationScheduler.run_now(rule_id)` 추가 — Trigger 조건과
  무관하게 즉시 발동(`POST /{id}/run`이 위임, `_fire()`를 그대로
  재사용해 `ExecutionDispatcher` 유일 진입점 원칙 유지).

  `web/app.py`의 `create_app()`에 `automation_service`/
  `automation_scheduler`를 선택적으로 받아 둘 다 있을 때만
  Automation 라우터를 등록(기존 M20 호출부 무영향). `lifespan`
  Context Manager로 전환(기존 `on_event` 대신) — 서버 기동 시
  `AutomationScheduler.start()`(Startup Trigger 1회 평가) +
  `automation_tick_seconds`(기본 30초)마다 `tick()`을 도는 백그라운드
  asyncio Task를 띄우고, 종료 시 Task를 취소해 정리한다("Scheduler는
  Server Runtime과 함께 실행된다", DoD). `web/server.py`의
  `build_app()`이 `InMemoryEngineRegistry`/`InMemoryAuthenticationManager`
  /`ExecutionDispatcher`/`AutomationActionExecutor`까지 전부
  조립해 Automation의 RUN_TASK가 실제로 동작 가능한 상태로
  구성한다 — 다만 이 시점엔 등록된 `EngineAdapter`가 없어(실제
  Engine 등록은 Workspace Core/CLI 경로 책임, Out of Scope) RUN_TASK
  발동 시 `EngineNotRegisteredError`가 나지만 `AutomationScheduler`
  가 삼켜 다른 Rule에 영향이 없다(TASKS.md에 명시적으로 기록해 둔
  현재 범위의 한계).

  단위/통합 테스트 19개 신규(domain 1, dashboard_service 2,
  dashboard_viewmodel 2, automation_routes 11, server lifespan 3).
  `pytest`(715개), `ruff`, `mypy` 통과. 다음 Task: **M21-T06**
  (Dashboard Web UI Automation 화면).
- 의존성: M21-T02, M21-T04.

#### M21-T04: Event Trigger + ExecutionDispatcher 연동
- 상태: **DONE (2026-07-27)** — `trigger_evaluator.py`에
  `EventTriggerEvaluator` 신규(사전 필터링은 `AutomationScheduler`
  책임이라 `should_fire`는 항상 True — event가 이미 일치를 확인한
  뒤에만 호출됨). `AutomationScheduler`에 `bind_event_bus(event_bus)`
  추가 — `EventBus`를 구독해 `event_type`이 일치하는 활성 EVENT
  Rule만 발동시킨다. `_fire()`가 `action_executor` 호출을
  `try/except Exception: pass`로 감싸도록 변경(`InMemoryEventBus.
  publish()`와 동일한 "구독자 예외가 다른 구독자에 영향을 주지
  않는다" 원칙 적용) — `last_executed_at`은 "실행 시도 시점"만
  기록하고 성공을 보장하지 않는다.

  `runtime/automation/automation_action_executor.py`의
  `AutomationActionExecutor`(사용자 승인 조건 5 — `ExecutionDispatcher`
  가 유일한 실행 진입점) 신규: RUN_TASK는 새 `Task` 생성 →
  `EngineRegistry.list_candidates()` → `EngineSelectionPolicy.select()`
  → `ExecutionDispatcher.dispatch()`로 M17/M18 파이프라인을 그대로
  재사용(새 실행 경로를 만들지 않음). DASHBOARD_REFRESH/NOTIFICATION
  은 실행할 Task가 없어 아무것도 하지 않음(Dashboard는 이미
  `ExecutionDispatcher`가 발행하는 Event로 갱신되고, 실제 알림
  발송은 Out of Scope). **범위 결정**: RUN_WORKFLOW는 이번
  Milestone이 Task 단위 실행 경로만 다루므로
  `AutomationActionNotSupportedError`를 던지며 아직 지원하지
  않는다(향후 Milestone에서 Workflow 실행 경로가 별도로 필요).

  실제 `ClaudeCodeEngineAdapter`+`FakeExecutionEnvironment`로 RUN_TASK
  가 진짜 실행됨을 통합 테스트로 증명. 단위/통합 테스트 8개 신규
  (executor 4개, scheduler event/예외격리 4개). `pytest`(696개),
  `ruff`, `mypy` 통과. 다음 Task: **M21-T05**(Automation API +
  Dashboard 연계).
- 의존성: M21-T03.

#### M21-T03: AutomationScheduler + Time/Interval/Startup Trigger
- 상태: **DONE (2026-07-27)** — `runtime/automation/trigger_evaluator.py`
  에 `TriggerEvaluator` ABC(`should_fire`/`compute_next_execution_at`)
  + `TimeTriggerEvaluator`(요일/일자 제약 지원, 같은 날 중복 발동
  방지는 `last_executed_at`의 날짜 비교로 판정 — tick 주기가 정확한
  분과 맞지 않아도 놓치지 않음)/`IntervalTriggerEvaluator`
  (`last_executed_at`, 없으면 `created_at` 기준 경과 시간 계산)/
  `StartupTriggerEvaluator`(`last_executed_at is None`으로 최초
  1회만 발동 판정) 신규 — 사용자 승인 조건 1(Scheduler·Trigger
  책임 분리)에 따라 "언제 발동할지" 판단을 전담. `runtime/
  automation/automation_scheduler.py`의 `AutomationScheduler`
  (`start()`는 Startup Trigger 1회 평가, `tick(now=...)`은 Time/
  Interval Trigger를 평가) 신규 — Rule을 별도로 등록/보관하지
  않고 매 호출마다 `AutomationRepository.list_rules()`를 다시
  조회한다(`AutomationService`가 같은 Repository로 CRUD하면 자동
  반영, 사용자 승인 조건 3). Action 실행은 생성자로 주입된
  `action_executor: Callable[[AutomationRule], None]`에 위임 —
  이 클래스는 `ExecutionDispatcher`를 전혀 모른다(실제 연동은
  M21-T04, 사용자 승인 조건 5). `tick()`은 고정된 `now`를 받아
  결정적으로 테스트 가능(실제 주기적 백그라운드 루프 연결은
  M21-T05, Server Runtime 기동 시). Event Trigger는 `tick()`이
  다루지 않는다(주기 평가 대상이 아니라 `EventBus` 구독 필요,
  M21-T04). 단위 테스트 26개 신규(trigger_evaluator 20개,
  scheduler 10개 — 일부 중복 제외 실제 26개). `pytest`(688개),
  `ruff`, `mypy` 통과. 다음 Task: **M21-T04**(Event Trigger +
  `ExecutionDispatcher` 연동).
- 의존성: M21-T01, M21-T02.

#### M21-T02: AutomationService(CRUD)
- 상태: **DONE (2026-07-27)** — `runtime/automation/automation_service.py`
  의 `AutomationService(automation_repository)`가 `create_rule`/
  `get_rule`/`list_rules`/`update_rule`(부분 갱신 — 넘긴 필드만
  변경)/`delete_rule`/`enable_rule`/`disable_rule`을 제공한다.
  `create_rule`이 `rule_id`(uuid4)와 `created_at`/`updated_at`
  (ISO 8601, `ExecutionDispatcher`의 `_now_iso()`와 동일한 패턴)을
  채운다. `update_rule`/`enable_rule`/`disable_rule` 모두
  `updated_at`을 갱신한다. **Action 실제 실행은 이 Task 범위 밖**
  (`AutomationScheduler`/`ExecutionDispatcher` 연동은 M21-T03/T04)
  — API의 `POST /{id}/run`은 그 두 Task가 끝난 뒤 M21-T05에서
  연결한다. `web/`이나 `Dashboard`를 전혀 참조하지 않음(`DashboardService`
  와 동일한 순수 서비스 패턴). 단위 테스트 10개 신규. `pytest`
  (662개), `ruff`, `mypy` 통과. 다음 Task: **M21-T03**
  (`AutomationScheduler` + Time/Interval/Startup Trigger).
- 의존성: M21-T01.

#### M21-T01: Automation 도메인 + Repository
- 상태: **DONE (2026-07-27)** — `domain/automation.py`에 `TriggerKind`
  (TIME/INTERVAL/EVENT/STARTUP)/`Trigger`(kind로 태그된 Flat 구조,
  `ExecutionRecord`(M20)와 동일한 스타일 — kind별로 실제 쓰이는
  필드만 채움)/`ActionKind`(RUN_TASK/RUN_WORKFLOW/DASHBOARD_REFRESH/
  NOTIFICATION)/`Action`(동일 스타일)/`AutomationRule`(rule_id/name/
  description/trigger/action/created_at/updated_at/enabled=True/
  `last_executed_at`/`next_execution_at`, 사용자 승인 조건 6 반영,
  `enable()`/`disable()` 메서드로 Task처럼 가변 엔티티) 신규.
  `interfaces/automation_repository.py`에 `AutomationRepository`
  (`get`/`save`/`delete`/`list_rules`, `ProjectRepository`와 동일한
  upsert 스타일)+`AutomationRuleNotFoundError` 신규. `runtime/
  automation/automation_repository.py`의 `InMemoryAutomationRepository`
  구현(방어적 복사 포함). 단위 테스트 17개 신규(domain 10개,
  interfaces 7개). `pytest`(652개), `ruff`, `mypy` 통과. 다음 Task:
  **M21-T02**(`AutomationService` CRUD).
- 의존성: 없음.

---

## Milestone 21 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | Automation Domain 구현 | ✅ (M21-T01) |
| 2 | `AutomationRepository` Interface 구현 | ✅ (M21-T01) |
| 3 | `InMemoryAutomationRepository` 구현 | ✅ (M21-T01) |
| 4 | `AutomationService` 구현 | ✅ (M21-T02) |
| 5 | `AutomationScheduler` 구현 | ✅ (M21-T03) |
| 6 | Time Trigger 구현 | ✅ (M21-T03) |
| 7 | Interval Trigger 구현 | ✅ (M21-T03) |
| 8 | Event Trigger 구현 | ✅ (M21-T04) |
| 9 | Startup Trigger 구현 | ✅ (M21-T03) |
| 10 | Automation API 구현 | ✅ (M21-T05, 8종) |
| 11 | Dashboard Automation 화면 구현 | ✅ (M21-T06) |
| 12 | `EventBus` 연동 | ✅ (M21-T04, `bind_event_bus`) |
| 13 | `ExecutionDispatcher` 연동 | ✅ (M21-T04, `AutomationActionExecutor`) |
| 14 | End-to-End 테스트 | ✅ (M21-T07) |
| 15 | `ruff` 통과 | ✅ (아래 4절) |
| 16 | `mypy` 통과 | ✅ (아래 4절) |
| 17 | 전체 `pytest` 통과 | ✅ (아래 4절) |

Task List(M21-T01~T07) 전체 완료. 사용자 승인 조건 6개(Scheduler·
Trigger 책임 분리/Dashboard Read Model 유지/Automation CRUD는 API
전용/Dashboard는 Automation 미제어/ExecutionDispatcher 유일 진입점/
`last_executed_at`·`next_execution_at` 도메인 내장) 모두 충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `domain/automation.py`, `interfaces/
  automation_repository.py`, `runtime/automation/`(전체 신규
  패키지 — `automation_repository.py`/`automation_service.py`/
  `trigger_evaluator.py`/`automation_scheduler.py`/
  `automation_action_executor.py`), `web/automation_routes.py`,
  `web/static/` Automation 화면 추가분 — 8개 신규 소스 파일 +
  정적 파일 갱신 3개.
- **변경된 기존 컴포넌트**: `domain/dashboard.py`(`AutomationStatus`
  추가), `runtime/dashboard/dashboard_service.py`(선택적
  `automation_service` DI), `web/app.py`(선택적 Automation 라우터
  등록 + `lifespan` 전환), `web/server.py`(Automation 실행
  파이프라인까지 전부 조립), `web/routes.py`(`/api/summary`에
  `automation_status` 추가) — 5개 소스 파일 수정, 전부 선택적
  DI/기본값으로 기존 호출부 무영향.
- **핵심 설계 결정**: (1) M4-T07 `AutomationEngine`(trigger_id↔
  Workflow 연결 관리)과 M21 Automation Engine(조건 평가+자동 실행)
  을 이름만 유사한 별개 컴포넌트로 명확히 분리했다 — 기존
  Interface는 손대지 않았다. (2) `AutomationScheduler`(오케스트
  레이션)와 `TriggerEvaluator`(평가 로직)의 책임을 물리적으로
  분리해(사용자 승인 조건 1) 새 Trigger 종류 추가가 Scheduler
  수정 없이 가능하도록 했다. (3) `AutomationScheduler`가 Rule을
  자체 보관하지 않고 매 호출마다 `AutomationRepository`를
  재조회하는 설계로 "CRUD는 API를 통해서만"이라는 조건을 코드
  구조로 강제했다(우회 경로 자체가 존재하지 않음). (4) Dashboard
  연계를 "Reader가 다른 Reader를 참조"하는 방향으로 확장해, 기존
  CQRS 원칙("쓰기측이 읽기측을 모른다")을 깨지 않으면서 새로운
  조회 요구를 수용했다.

`git diff --stat`(M20 종료 커밋 대비)로 확인한 결과 신규 소스/정적
파일 11개, 기존 파일 수정 5개 — M20과 유사한 규모(새 층위 전체가
신규이면서 기존 컴포넌트 변경은 최소).

**3. Interface First 원칙 검토**

M21은 `AutomationRepository`라는 **새 최상위 Interface**를
추가했다(총 26→27종) — ADR-0033을 작성했다.
`AutomationService`/`AutomationScheduler`/`TriggerEvaluator`
계열/`AutomationActionExecutor`는 모두 구체 클래스다(기존
`WorkflowRunner`/`ExecutionDispatcher`/`RetryExecutor`/
`DashboardService`와 동일한 패턴 — 단일 구현이 확실한 조합 로직은
구체 클래스로 유지). 기존 `AutomationEngine` Interface는 계약을
전혀 확장하지 않았다(완전히 별개 컴포넌트이므로) — ADR-0033은
"새 Interface 추가"에 더해 "이름이 유사한 기존 컴포넌트와의 관계를
명시적으로 정리"하는 근거로도 작성됐다(M16 ADR-0028/M18 ADR-0030과
동일한 사전 점검 전통).

**4. 테스트 결과**

- `pytest`: **720개 전부 통과**(M20 완료 시점 635개 → M21에서 85개
  신규: M21-T01 +17, M21-T02 +10, M21-T03 +26, M21-T04 +8,
  M21-T05 +19, M21-T06 +0(정적 파일, 실제 브라우저로 검증),
  M21-T07 +5)
- `ruff check src tests`: 클린
- `mypy --python-executable "$(which python3)" src`: 클린(128개
  소스 파일)
- 신규 외부 런타임 의존성 없음(M20에서 도입한 FastAPI/uvicorn을
  그대로 사용)
- **실제 브라우저 검증**(M21-T06): 이 세션에 한해 `playwright`를
  임시 설치해(프로젝트 의존성에는 추가하지 않음) 사전 설치된
  Chromium으로 실제 서버를 띄우고 Rule 생성/토글/목록 갱신/요약
  갱신을 직접 조작해 확인 — 그 과정에서 `updateVisibleFields()`의
  `querySelector`(단일 요소) 버그를 실제 조작 중 발견해 즉시
  `querySelectorAll`로 수정함(정적 JS라 pytest로는 잡히지 않는
  종류의 결함).

**5. Technical Debt 정리**

*M21에서 새로 발생한 기술 부채*
- **RUN_WORKFLOW 미지원**: `AutomationActionExecutor`가 RUN_TASK만
  실제로 실행하고 RUN_WORKFLOW는 `AutomationActionNotSupportedError`
  를 던진다 — `ExecutionDispatcher`를 유일한 실행 진입점으로
  못박은 조건과 정합성을 유지하려면 Workflow 실행 경로도 그 원칙
  안에서 별도로 설계해야 하는데, 이번 Milestone은 그 설계까지
  확정하지 않았다(ADR-0033에 대안 검토로 기록). 후속 Milestone에서
  `WorkflowRunner`(M12) 연동 여부를 판단해야 한다.
- **Dashboard 서버의 실제 Engine 미등록**: `web/server.py`가
  조립하는 `InMemoryEngineRegistry`에는 시작 시점에 등록된
  `EngineAdapter`가 없다 — 실제 Engine 등록/인증은 Workspace
  Core(CLI 경로)의 책임이라 Out of Scope로 뒀다. 현재는 RUN_TASK가
  발동해도 `EngineNotRegisteredError`가 나고 `AutomationScheduler`
  가 삼킬 뿐이다. Dashboard/Automation 서버와 Workspace Core를
  실제로 통합하는 것은 이후 Milestone 과제다.

*M21 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- Cron Expression, Database 저장(`AutomationRepository`의 File/DB
  구현체), Distributed/Multi-node Scheduler, Retry Policy 변경,
  Mobile Push Notification/Home Widget/Lock Screen Widget/Live
  Activity/Dynamic Island, AI 기반 Rule 추천.

*계속 이월되는 기존 항목*
- Effort 라우팅, `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임
  워크 미통합, Codex/Gemini 실연동 미검증, `MemoryEngine.search()`
  선형 스캔, 여러 Task에 걸친 누적 예산 추적, 예산 초과 시 Approval
  흐름, `KnowledgeIndexer`, Review/Documentation Agent로의
  `knowledge_provider` 확장, `EngineRuntime`↔`EngineRegistry` 중복
  등록, 실제 로그인/OAuth/Credential/Token Refresh, `CodingAgent`
  ↔`ExecutionDispatcher` 연결, `ShellAgent` 화이트리스트 코드 고정,
  `timed_out` 휴리스틱(ADR-0031), `DashboardRepository` 쓰기/읽기
  Interface 물리적 분리, 실제 프로덕션 배포 구성.

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M21-T01~T07 상세 섹션) / `docs/ROADMAP.md`
(M21 Task List·진행 상태 반영) / `docs/ARCHITECTURE.md`(v0.23.0, 신규
§3.19, §7 27종, §8 규칙 13/14번, §9 디렉터리 구조 갱신) /
`.ai/DECISIONS.md`(ADR-0033 신규) 완료. `pyproject.toml` 변경 없음
(신규 외부 의존성 없음). `.ai/MEMORY.md`는 이 Review 승인 직후
M1~M20과 동일한 방식으로 압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절, 17개 항목 전부), Architecture Review
완료(2절, 신규 8개 소스+정적 3개/수정 5개 소스 파일, "기존
AutomationEngine과 명시적 분리 + Scheduler/Trigger 책임 분리 +
Reader→Reader CQRS 확장" 설계 결정 기록), Interface First 검토
완료(3절, 새 Interface `AutomationRepository` 추가로 ADR-0033
작성), 테스트 결과 문서화 완료(4절, 720개 전부 통과 + 실제
브라우저 검증에서 발견한 버그를 즉시 수정한 이력 포함), Technical
Debt 정리 완료(5절, RUN_WORKFLOW 미지원과 Dashboard 서버의 실제
Engine 미등록을 신규 부채로 정식 등재), 문서 갱신 완료(6절) — 6개
조건 모두 만족. Review 중 코드 변경이 필요한 치명적 문제(버그·계약
위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 21 Completed를 선언한다.**

**Milestone 21 종료 — 2026-07-27 사용자 승인.**

**Milestone 22 상태**: 착수 확정. 아래 "Milestone 22" 절 참고.

---

## Milestone 22 — Production Platform

**목표**: AI Workspace를 실제 운영 가능한 Production Platform으로
확장한다. Server Runtime의 생명주기(Lifecycle)/설정(Configuration)/
상태(Health)/Logging을 담당한다. 비즈니스 로직을 추가하지 않는다 —
Execution/Dashboard/Automation은 그대로 유지한다(2026-07-27 사용자
확정).

**설계 방향(사용자 최종 승인, 조건 5개)**:
1. Configuration은 Infrastructure Layer의 Immutable 설정 객체로
   유지한다 — `domain/`이 아니라 `runtime/production/`에 둔다.
2. `LifecycleManager`는 생성이 아닌 생명주기(Startup/Shutdown)만
   관리한다 — 컴포넌트 조립은 여전히 `web/server.py`의 책임이다.
3. `HealthMonitor`는 조회 전용(Read Model)으로 유지한다.
4. Dashboard Health는 기존 `DashboardService`를 확장하여
   구현한다(M21의 `automation_service` 선택적 DI와 동일한 Reader→
   Reader 패턴).
5. `uptime`/`started_at`/`version`/`health_status`를 표준 상태
   정보로 제공해 M23(Mobile Experience)에서 재사용할 수 있도록
   한다.

**설계 검토에서 확정한 세부 사항**(사용자 승인, 이견 없어 그대로
진행):
- **Version API 값**: `pyproject.toml`의 `version`(ADR-0024가
  관리하는 아키텍처 기준선 버전)과 별개로, 제품 릴리스 버전을
  담는 별도 상수(`runtime/production/version.py`의
  `WORKSPACE_VERSION`)를 신설한다 — 두 버전 개념이 다른 것을
  추적하기 때문이다.
- **Health Monitor의 "Engine" 항목**: 이 서버는 아직 실제
  `EngineAdapter`를 등록하지 않는다(M21 Review에 기록된 기존
  한계) — 이번 Milestone은 `EngineRegistry` Interface를 확장하지
  않고, "구조적으로 조립돼 있는가"만 조회 전용으로 확인한다.
- **컴포넌트 배치**: Configuration/Lifecycle Manager/Health
  Monitor 등 FastAPI를 모르는 코드는 `runtime/production/`
  (`runtime/dashboard/`/`runtime/automation/`과 동일한 패턴)에,
  실제 REST 엔드포인트는 `web/production_routes.py`에 둔다.
- **Graceful Shutdown**: 별도 계측 없이 기존 `DashboardService.
  workspace_status()`(M20)가 이미 추적하는 실행 중 여부(`status
  == "running"`)를 폴링(타임아웃 포함)해 "실행 중인 Task 완료
  대기"를 구현한다 — `ExecutionDispatcher`를 직접 건드리지 않아
  "Core Domain은 Production을 모른다" 원칙을 지킨다.

**Non-goal(범위 밖)**: Docker, Kubernetes, CI/CD, HTTPS, Reverse
Proxy, Database, Authentication, Authorization, Multi-node
Cluster, Mobile App, Home Widget, Lock Screen Widget, Live
Activity, Push Notification.

**Milestone Definition of Done**
1. Configuration 구현(불변).
2. Configuration Loader 구현(Env Var + 설정 파일).
3. Lifecycle Manager 구현.
4. Health Monitor 구현.
5. Production Logging 구현(표준 `logging`, Console+File).
6. Production API 구현.
7. Dashboard Health 화면 구현.
8. Graceful Shutdown 구현.
9. Version API 구현.
10. Environment Variable 지원.
11. 설정 파일 지원.
12. End-to-End 테스트.
13. Architecture Test.
14. ADR 작성.
15. ARCHITECTURE.md 갱신.
16. TASKS.md Review.
17. `ruff`/`mypy`/전체 `pytest` 통과.

**Task List**(2026-07-27 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M22-T01 | Production Configuration + Loader(Env Var+설정 파일, 불변) | **완료** |
| M22-T02 | Production Logging(표준 `logging`, Console+File) | **완료** |
| M22-T03 | Lifecycle Manager(Startup/Running/Shutdown, Graceful Shutdown) | **완료** |
| M22-T04 | Health Monitor + Version 조회 | **완료** |
| M22-T05 | Production API(4종) + Server Runtime 연동 | **완료** |
| M22-T06 | Dashboard Health 화면 | **완료** |
| M22-T07 | 전체 흐름 검증 + 문서화 | **완료** |

**진행 상태**: M22-T01~T07 전체 완료.

#### M22-T07: 전체 흐름 검증 + 문서화
- 상태: **DONE (2026-07-27)** —
  `tests/integration/test_m22_production_platform.py` 신규(7개
  테스트). 실제 FastAPI `lifespan`으로 서버 기동 시 Lifecycle이
  `running`/`healthy`로 전이함을 증명. 실제 `ClaudeCodeEngineAdapter`
  +`ExecutionDispatcher` 조합으로 Graceful Shutdown이 실행 중인
  Task(Dashboard가 Event로 추적)를 감지해 완료까지 기다린 뒤에야
  종료함을 비동기 테스트로 증명(강제 종료 없음). Production API가
  실제 Dashboard/Automation 연결 상태를 반영함을 REST 호출로
  증명. `AI_WORKSPACE_LOG_LEVEL`/`AI_WORKSPACE_AUTOMATION_TICK_SECONDS`
  Environment Variable이 `load_production_config()`→`build_app()`
  →`/api/config`까지 실제로 이어짐을 증명. `ast` 기반 Architecture
  Test 4종: `runtime/production/` 전체가 `web/`/FastAPI/uvicorn을
  import하지 않음, `domain`/`interfaces`/`engines` 전체가
  `runtime.production`을 import하지 않음("Core Domain은 Production
  을 모른다"), `LifecycleManager`가 `InMemory*` 구체 구현체를 전혀
  import하지 않음(사용자 승인 조건 2 재확인). `pytest`(771개),
  `ruff`, `mypy` 통과.

  ADR-0034(`.ai/DECISIONS.md`) 신규 작성 — 사용자 승인 조건 5개
  반영 근거, Version API 분리 이유, `DashboardService`↔
  `HealthMonitor` 순환 참조를 `TYPE_CHECKING`+`attach_health_monitor()`
  로 해결한 경위, 대안 검토를 전부 기록. `docs/ARCHITECTURE.md`
  v0.24.0: 신규 §3.20(Production Platform, 사용자 Architecture
  다이어그램 포함), §7은 새 Interface 없어 27종 그대로 유지(주석만
  갱신), §8 의존성 규칙에 15/16/17번(Core는 Production을 모름,
  Dashboard Health Reader→Reader, LifecycleManager는 비생성) 추가,
  §9 디렉터리 구조에 `runtime/production/`/
  `web/production_routes.py`/CLI 옵션 변경 반영. 아래 Milestone 22
  Review 작성.
- 의존성: M22-T06.

#### M22-T06: Dashboard Health 화면
- 상태: **DONE (2026-07-27)** — `DashboardService`를 확장(사용자
  승인 조건 4)해 선택적 `health_monitor: HealthMonitor | None = None`
  DI + `production_status()`(미주입 시 `None`) 추가 — M21의
  `automation_service` 선택적 DI와 동일한 Reader→Reader 패턴.
  `DashboardSnapshot`/`DashboardViewModel`에 `production_status`
  필드 추가(기본값 `None`, 기존 호출부 무영향), `/api/dashboard`와
  `/api/summary`에 자동 포함.

  **순환 import 회피**: `HealthMonitor`(M22-T04)가 타입 힌트로만
  `DashboardService`를 참조하고(`_dashboard_health()`는 주입 여부만
  확인, 메서드 호출 없음), `LifecycleManager`도 동일하게
  `DashboardService`를 타입 힌트로만 쓰므로(`workspace_status()`
  호출은 하지만 그 시점엔 이미 인스턴스가 존재) 두 모듈 모두
  `TYPE_CHECKING` 가드로 지연 import 처리해 `dashboard_service.py`
  → `health.py`/`lifecycle.py` → `dashboard_service.py`로 되돌아오는
  런타임 순환 import를 없앴다. **조립 순서 문제**: `HealthMonitor`
  가 생성되려면 이미 만들어진 `DashboardService`가 필요하지만,
  `DashboardService`도 `HealthMonitor`를 참조하고 싶어 해 생성자
  주입만으로는 순서를 맞출 수 없다 — `DashboardService.
  attach_health_monitor(health_monitor)`(생성 후 연결) 메서드를
  추가해 `web/server.py`의 `build_app()`이 `dashboard_service`→
  `lifecycle_manager`→`health_monitor`를 만든 뒤 마지막에
  `attach_health_monitor()`로 연결하도록 했다(실제 순환 의존이
  아니라 순수한 조립 순서 문제임을 문서화).

  `web/static/index.html`에 "Production 현황" 영역(최상단) 추가,
  `web/static/app.js`에 Health 상태 한국어 라벨(정상/저하/비정상)/
  Uptime 포맷터/컴포넌트별 상태 목록/Configuration 요약(최초
  로드 시 `/api/config` 1회 조회) 렌더링 로직 추가.

  **실제 브라우저 검증**(Playwright, 이전 T06과 동일하게 세션
  한정): 실제 `run_server()`로 띄운 서버에서 "Production 현황"
  섹션이 Server 상태/Version/시작 시각/Uptime/컴포넌트별 상태/
  Configuration 요약을 전부 정확히 렌더링함을 확인.

  단위 테스트 3개 신규(`production_status` 미주입 시 `None`/
  `attach_health_monitor` 연결 후 반영/ViewModel 변환). `pytest`
  (764개), `ruff`, `mypy` 통과. 다음 Task: **M22-T07**(전체 흐름
  검증 + 문서화).
- 의존성: M22-T04, M20-T03(`DashboardService`).

#### M22-T05: Production API + Server Runtime 연동
- 상태: **DONE (2026-07-27)** — `web/production_routes.py`에
  `GET /api/health`(`HealthMonitor.status()` 상세, `components`
  배열 포함)/`GET /api/config`(`ProductionConfig` 그대로 노출,
  비밀값 없음)/`GET /api/version`(`VersionInfo`)/`GET /api/status`
  (사용자 승인 조건 5의 4개 표준 필드만 담은 경량 요약 — M23이
  이 최소 형태를 그대로 재사용할 수 있도록 `/api/health`의 상세
  `components`와 분리) 신규.

  `web/app.py`의 `create_app()`에 `production_config`/
  `lifecycle_manager`/`health_monitor` 3개 모두 주입해야만
  Production 라우터가 등록되도록 확장(기존 M20/M21 호출부는
  무영향, 새 파라미터 전부 기본값 `None`). `lifecycle_manager`가
  주어지면 `lifespan`이 `automation_scheduler.start()`를 직접
  호출하는 대신 `lifecycle_manager.startup()`에 위임하고, 종료 시
  `await lifecycle_manager.shutdown()`(Graceful Shutdown — 실행 중
  Task 완료 대기)을 tick Task 취소보다 먼저 수행한다(사용자 DoD
  순서: 실행 중 Task 완료 대기 → Scheduler 종료). 미주입 시(기존
  M20/M21 호출부) 이전과 동일하게 즉시 시작·즉시 종료한다.

  `web/server.py`의 `build_app(*, project_name=, config=)`가
  `config` 미지정 시 `load_production_config()`로 채우고,
  `LifecycleManager`/`HealthMonitor`까지 전부 조립해
  `create_app()`에 넘긴다. `run_server(*, host=None, port=None,
  config_path=None, log_file=None)`은 Configuration을 로드한 뒤
  CLI `host`/`port`가 주어지면(가장 구체적인 값) 그것으로
  덮어쓰고, `configure_logging()`(M22-T02)까지 호출한 다음
  `uvicorn.run()`한다. `cli/main.py`의 `start` 서브커맨드
  `--host`/`--port` 기본값을 하드코딩된 문자열에서 `None`으로
  바꿔 미지정 시 Configuration 값이 살아있도록 했다(명시하면 여전히
  CLI가 최우선).

  실제 `uvicorn.run()`으로 띄운 서버에 `curl`로 `/api/status`/
  `/api/config`를 직접 호출해 `host`/`port` 오버라이드와 Lifecycle
  상태 전이(`running`/`healthy`)가 실제로 동작함을 확인. 단위/통합
  테스트 12개 신규(production_routes 5개, server 3개, 기존 CLI
  테스트 무영향 확인). `pytest`(761개), `ruff`, `mypy` 통과. 다음
  Task: **M22-T06**(Dashboard Health 화면).
- 의존성: M22-T01, M22-T02, M22-T04.

#### M22-T04: Health Monitor + Version 조회
- 상태: **DONE (2026-07-27)** — `runtime/production/version.py`에
  `WORKSPACE_VERSION`(제품 릴리스 버전, `pyproject.toml`의 아키텍처
  기준선 버전과 별개 — M22 kickoff 승인 사항) + `get_git_commit_hash()`
  (`git rev-parse HEAD`, 실패 시 `None` — git 저장소가 아니어도
  Version API가 항상 동작) + `get_version_info()` 신규.
  `runtime/production/health.py`에 `HealthStatus`(HEALTHY/DEGRADED/
  UNHEALTHY)/`ComponentHealth`/`ProductionStatus`(사용자 승인
  조건 5의 `uptime_seconds`/`started_at`/`version`/`health_status`
  표준 필드 포함) + `HealthMonitor`(사용자 승인 조건 3 — 조회
  전용, 상태를 바꾸지 않음) 신규. Server/Dashboard/Automation/
  EventBus/Engine 5개 컴포넌트를 각각 점검해 가장 나쁜 상태로
  전체 `health_status`를 집계한다(`server`는 `LifecycleManager.state`
  로 판정 — RUNNING=Healthy/STARTUP=Degraded/SHUTDOWN=Unhealthy,
  나머지 4개는 주입 여부로 판정). **Engine 항목 범위**: M22 kickoff
  합의대로 `EngineRegistry` Interface를 확장하지 않고 "연결돼
  있는가"만 확인한다(개별 Engine 상태는 범위 밖, `detail`에 명시).
  `uptime_seconds`는 `LifecycleManager.started_at`과 현재 시각의
  차이로 계산(시작 전이면 `None`). 단위 테스트 14개 신규(health
  8개, version 3개, 추가 aggregate/shutdown 케이스 3개). `pytest`
  (753개), `ruff`, `mypy` 통과. 다음 Task: **M22-T05**(Production
  API + Server Runtime 연동).
- 의존성: M22-T03.

#### M22-T03: Lifecycle Manager
- 상태: **DONE (2026-07-27)** — `runtime/production/lifecycle.py`의
  `LifecycleState`(STARTUP/RUNNING/SHUTDOWN) + `LifecycleManager`
  신규(사용자 승인 조건 2 — **생성이 아닌 생명주기만** 관리, 이미
  조립된 `AutomationScheduler`/`DashboardService`를 선택적으로
  주입받을 뿐 컴포넌트를 스스로 만들지 않음). `startup(now=)`이
  `started_at`(ISO 8601)을 기록하고 `AutomationScheduler.start()`
  (Startup Trigger 1회 평가)를 호출한 뒤 RUNNING으로 전이한다.
  `shutdown()`(비동기)은 SHUTDOWN으로 즉시 전이한 뒤
  `DashboardService.workspace_status()`(M20이 이미 추적하는 실행 중
  여부)를 `graceful_shutdown_poll_interval_seconds`마다 폴링해
  "idle"이 될 때까지 기다린다 — `graceful_shutdown_timeout_seconds`
  (기본 30초)를 넘기면 **강제로 개입하지 않고** 그대로 진행한다
  (사용자 DoD "강제 종료를 수행하지 않는다"). `ExecutionDispatcher`
  를 직접 참조하지 않아 Core Domain은 이 클래스를 전혀 모른다.
  단위 테스트 7개 신규(Startup 전이/Startup Trigger 연동/Dashboard
  미주입 시 즉시 반환/실행 중 Task 완료 대기 후 정상 종료/타임아웃
  후 강제 없이 진행). `pytest`(745개), `ruff`, `mypy` 통과. 다음
  Task: **M22-T04**(Health Monitor + Version 조회).
- 의존성: M21-T03(`AutomationScheduler`), M20-T03(`DashboardService`).

#### M22-T02: Production Logging
- 상태: **DONE (2026-07-27)** — `runtime/production/logging_setup.py`
  의 `configure_logging(config, *, log_file=None)`이
  `ProductionConfig.log_level`을 기준으로 `ai_workspace` 이름의
  표준 `logging.Logger`를 설정한다. Console 출력(`StreamHandler`)은
  항상 켜지고, `log_file`을 주면 `FileHandler`도 함께 추가된다(둘 다
  지원, 사용자 DoD). 매 호출마다 기존 핸들러를 비워 idempotent하게
  재설정한다(중복 로그 방지). `get_logger(name=None)`은
  `ai_workspace`(또는 `ai_workspace.<name>`) 로거를 반환 — 설정
  이전에도 표준 `logging` 기본 동작으로 안전하게 쓸 수 있다.
  "Logging은 Domain에 침투하지 않는다"는 원칙대로 이 모듈은
  `runtime/production/`에만 있고 `domain`/`interfaces`/`engines`는
  참조하지 않는다. 단위 테스트 6개 신규. `pytest`(738개), `ruff`,
  `mypy` 통과. 다음 Task: **M22-T03**(Lifecycle Manager).
- 의존성: M22-T01.

#### M22-T01: Production Configuration + Loader
- 상태: **DONE (2026-07-27)** — `runtime/production/config.py`의
  `ProductionConfig`(frozen dataclass, 사용자 승인 조건 1 —
  Infrastructure Layer의 Immutable 설정 객체)에 `host`/`port`/
  `log_level`/`dashboard_enabled`/`automation_enabled`/
  `automation_tick_seconds`(M20 `web/app.py`의
  `DEFAULT_AUTOMATION_TICK_SECONDS`를 여기로 이관 예정, T05에서
  실제 연결)/`engine_settings`(실제 Engine 미등록 상태를 반영한
  최소 자리표시자) 신규. `__post_init__`에서 `log_level` 허용값/
  `port` 양수/`automation_tick_seconds` 양수를 검증
  (`InvalidConfigurationError`). `runtime/production/
  config_loader.py`의 `load_production_config(config_path=,
  env=)`가 기본값→설정 파일(YAML, `storage/llm_policy_loader.py`
  와 동일한 "로더가 PyYAML을 알고 데이터 타입은 모른다" 분리
  패턴)→Environment Variable(`AI_WORKSPACE_` 접두사) 순으로
  겹쳐 써 `ProductionConfig`를 만든다 — Env Var가 가장 구체적인
  값으로 최종 우선한다. 단위 테스트 12개 신규(config 6개, loader
  6개). `pytest`(732개), `ruff`, `mypy` 통과. 다음 Task:
  **M22-T02**(Production Logging).
- 의존성: 없음.

---

## Milestone 22 Review

**1. Definition of Done 체크리스트**

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | Configuration 구현 | ✅ (M22-T01) |
| 2 | Configuration Loader 구현 | ✅ (M22-T01) |
| 3 | Lifecycle Manager 구현 | ✅ (M22-T03) |
| 4 | Health Monitor 구현 | ✅ (M22-T04) |
| 5 | Production Logging 구현 | ✅ (M22-T02) |
| 6 | Production API 구현 | ✅ (M22-T05, 4종) |
| 7 | Dashboard Health 화면 구현 | ✅ (M22-T06) |
| 8 | Graceful Shutdown 구현 | ✅ (M22-T03, 실제 검증 M22-T07) |
| 9 | Version API 구현 | ✅ (M22-T04/T05) |
| 10 | Environment Variable 지원 | ✅ (M22-T01, 실제 검증 M22-T07) |
| 11 | 설정 파일 지원 | ✅ (M22-T01) |
| 12 | End-to-End 테스트 | ✅ (M22-T07) |
| 13 | Architecture Test | ✅ (M22-T07, `ast` 기반 4종) |
| 14 | ADR 작성 | ✅ (ADR-0034) |
| 15 | ARCHITECTURE.md 갱신 | ✅ (v0.24.0) |
| 16 | TASKS.md Review | ✅ (본 절) |
| 17 | `ruff`/`mypy`/전체 `pytest` 통과 | ✅ (아래 4절) |

Task List(M22-T01~T07) 전체 완료. 사용자 승인 조건 5개(Configuration
Immutable/Infrastructure Layer, LifecycleManager는 생명주기만,
HealthMonitor는 조회 전용, Dashboard Health는 기존 DashboardService
확장, uptime/started_at/version/health_status 표준 필드) 모두
충족됨.

**2. Architecture Review**

- **신규 컴포넌트**: `runtime/production/`(신규 패키지 전체 —
  `config.py`/`config_loader.py`/`logging_setup.py`/`lifecycle.py`/
  `health.py`/`version.py`), `web/production_routes.py` — 7개
  신규 소스 파일.
- **변경된 기존 컴포넌트**: `runtime/dashboard/dashboard_service.py`
  (선택적 `health_monitor` DI + `production_status()`+
  `attach_health_monitor()`), `web/app.py`(Production 라우터 조건부
  등록 + `lifecycle_manager` 기반 Startup/Graceful Shutdown),
  `web/server.py`(Configuration 로드 + Production 컴포넌트 전부
  조립), `web/routes.py`(`/api/summary`에 `production_status`
  추가), `web/dashboard_viewmodel.py`(`production_status` 필드),
  `cli/main.py`(`--host`/`--port` 기본값 `None`), `web/static/`
  (Production 현황 화면) — 6개 소스 파일 수정, 전부 선택적 DI/
  기본값으로 기존 호출부 무영향.
- **핵심 설계 결정**: (1) `ProductionConfig`를 frozen dataclass로
  두고 `runtime/production/`(Infrastructure Layer)에만 배치해
  Core Domain이 이 개념을 전혀 모르게 했다. (2) `LifecycleManager`
  /`HealthMonitor`의 책임을 "생명주기만"/"조회만"으로 엄격히
  좁혀 서로 겹치지 않게 했다 — 컴포넌트 조립은 여전히
  `web/server.py`가 전담한다. (3) Dashboard Health를 별도 API가
  아니라 **기존 `DashboardService`의 확장**으로 구현하면서 발생한
  `DashboardService`↔`HealthMonitor` 순환 참조를, `TYPE_CHECKING`
  지연 import(런타임 순환 없음) + `attach_health_monitor()`(생성
  후 연결, 조립 순서 문제 해결)로 실제 코드 순환 없이 풀었다 — 이
  프로젝트에서 처음 등장한 "두 컴포넌트가 서로를 참조하고 싶어
  하는" 설계 상황을 사용자 조건을 어기지 않고 해결한 사례.

`git diff --stat`(M21 종료 커밋 대비)로 확인한 결과 신규 소스 파일
7개, 기존 파일 수정 6개 — M20/M21과 비슷한 규모(신규 층위 전체가
새 컴포넌트, 기존 컴포넌트 변경은 선택적 DI로 최소화).

**3. Interface First 원칙 검토**

M22는 **새 최상위 Interface를 추가하지 않았다** — `ProductionConfig`
/`LifecycleManager`/`HealthMonitor`/`VersionInfo` 전부 구체
클래스이거나 dataclass다(총 27종 그대로). 그럼에도 ADR-0034를
작성한 이유는 사용자 DoD가 "ADR 작성"을 명시적으로 요구했고, (1)
`AutomationEngine`(M4-T07)/`AutomationRepository`(M21)에 이어
"기존 개념과의 관계"를 정리할 필요는 없었지만 순환 참조 처리
방식(`TYPE_CHECKING` + `attach_*`)이라는 새로운 패턴을 도입했으며,
(2) Version API의 값이 `pyproject.toml`의 버전과 다른 개념임을
명확히 기록해야 했기 때문이다 — M19(ADR-0031)에 이어 "새 Interface
없이도 사용자 요청/설계 결정 기록 필요성으로 ADR을 작성"한 두 번째
사례.

**4. 테스트 결과**

- `pytest`: **771개 전부 통과**(M21 완료 시점 720개 → M22에서
  51개 신규: M22-T01 +12, M22-T02 +6, M22-T03 +7, M22-T04 +14,
  M22-T05 +8, M22-T06 +3, M22-T07 +7 — 일부 중복 조정 포함 실제
  51개 순증)
- `ruff check src tests`: 클린
- `mypy --python-executable "$(which python3)" src`: 클린(136개
  소스 파일)
- 신규 외부 런타임 의존성 없음(M20의 FastAPI/uvicorn 그대로 사용)
- **실제 서버 검증**: `uvicorn.run()`으로 실제 소켓을 열어
  `curl`로 `/api/status`/`/api/config`를 호출해 CLI `--host`/
  `--port` 오버라이드와 Lifecycle 상태 전이(`running`/`healthy`)
  가 실제로 동작함을 확인.
- **실제 브라우저 검증**(M22-T06, Playwright 세션 한정 설치):
  Chromium으로 "Production 현황" 화면이 Server 상태/Version/시작
  시각/Uptime/컴포넌트별 상태/Configuration 요약을 정확히
  렌더링함을 확인.

**5. Technical Debt 정리**

*M22에서 새로 발생한 기술 부채*
- 없음 — 새로운 휴리스틱이나 임시 우회는 도입하지 않았다(순환
  참조는 `TYPE_CHECKING` 지연 import로 근본 해결, 우회가 아님).

*M22 범위 밖으로 명시적으로 제외한 것(사용자 확정, 계속 이월)*
- Docker, Kubernetes, CI/CD, HTTPS, Reverse Proxy, Database,
  Authentication, Authorization, Multi-node Cluster, Mobile App,
  Home Widget, Lock Screen Widget, Live Activity, Push
  Notification. `EngineRegistry`의 실제 Engine 등록 개수 점검
  (Health Monitor의 Engine 항목 심화)도 이번엔 다루지 않음.

*계속 이월되는 기존 항목*
- Effort 라우팅, `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임
  워크 미통합, Codex/Gemini 실연동 미검증, `MemoryEngine.search()`
  선형 스캔, 여러 Task에 걸친 누적 예산 추적, 예산 초과 시 Approval
  흐름, `KnowledgeIndexer`, Review/Documentation Agent로의
  `knowledge_provider` 확장, `EngineRuntime`↔`EngineRegistry` 중복
  등록, 실제 로그인/OAuth/Credential/Token Refresh, `CodingAgent`
  ↔`ExecutionDispatcher` 연결, `ShellAgent` 화이트리스트 코드 고정,
  `timed_out` 휴리스틱(ADR-0031), `DashboardRepository` 쓰기/읽기
  Interface 물리적 분리, RUN_WORKFLOW 미지원(ADR-0033), Dashboard
  서버의 실제 Engine 미등록(ADR-0033), 실제 프로덕션 배포 구성.

**6. 문서 정리**

`.ai/TASKS.md`(본 Review, M22-T01~T07 상세 섹션) / `docs/ROADMAP.md`
(M22 Task List·진행 상태 반영) / `docs/ARCHITECTURE.md`(v0.24.0,
신규 §3.20, §8 규칙 15/16/17번, §9 디렉터리 구조 갱신) /
`.ai/DECISIONS.md`(ADR-0034 신규) 완료. `pyproject.toml` 변경 없음
(신규 외부 의존성 없음, `WORKSPACE_VERSION`은 별도 상수로 관리).
`.ai/MEMORY.md`는 이 Review 승인 직후 M1~M21과 동일한 방식으로
압축 반영한다.

**7. Milestone 종료 선언**

Definition of Done 충족(1절, 17개 항목 전부), Architecture Review
완료(2절, 신규 7개/수정 6개 소스 파일, "Configuration Immutable +
Lifecycle/Health 책임 분리 + Dashboard Reader→Reader 확장의 순환
참조를 TYPE_CHECKING+attach_*로 해결" 설계 결정 기록), Interface
First 검토 완료(3절, 새 Interface 없음이나 사용자 DoD 요구에 따라
ADR-0034 작성), 테스트 결과 문서화 완료(4절, 771개 전부 통과 +
실제 서버·브라우저 이중 검증), Technical Debt 정리 완료(5절, 신규
부채 없음), 문서 갱신 완료(6절) — 6개 조건 모두 만족. Review 중
코드 변경이 필요한 치명적 문제(버그·계약 위반)는 발견되지 않았다.

**사용자 승인을 조건으로 Milestone 22 Completed를 선언한다.**

**Milestone 22 종료 — 2026-07-27 사용자 승인.**

**Milestone 23 상태**: 착수 전 — M23-Preparation(Obsidian Knowledge
Base 구축)을 먼저 진행한다. 아래 "M23-Preparation" 절 참고.

---

## M23-Preparation — Obsidian Knowledge Base 구축

**목표**: Mobile Experience(M23) 착수 전 AI Workspace의 장기
Knowledge Base를 구축한다. GitHub는 Source of Truth를 유지하고,
Obsidian Vault는 GitHub 문서를 빠르게 탐색하기 위한 지식
Index(요약+링크, 원문 비복제)를 제공한다(2026-07-27 사용자 확정).
PARA 구조(`00 Inbox`/`01 Projects`/`02 Resources`/`03 Archives`)를
따르며, 저장소 루트의 `Vault/`에 체크인해 GitHub와 함께 버전
관리한다. MCP 연동(Obsidian을 AI가 직접 읽고 쓰게 하는 것)은 이번
범위가 아니다 — Claude Code 도입 시점의 별도 Task(M23-Prep-T08,
Optional)로 이월한다.

**Task List**(2026-07-27 확정, 사용자 최종 승인)

| Task | 내용 | 상태 |
|---|---|---|
| M23-Prep-T01 | Vault 초기 구성 및 시스템 문서 작성 | **완료** |
| M23-Prep-T02 | 프로젝트 개요 및 아키텍처 작성 | **완료** |
| M23-Prep-T03 | ADR 정리 | **완료** |
| M23-Prep-T04 | Backend/API 문서화 | **완료** |
| M23-Prep-T05 | 서버 구성 문서화 | **완료** |
| M23-Prep-T06 | Client 및 프로젝트 이력 정리 | **완료** |
| M23-Prep-T07 | 운영 문서 및 검증 | **완료** |
| M23-Prep-T01A | Vault Retrieval/Prompt 효율화(Router+Template) | **완료** |
| M23-Prep-T01B | 산출물별 작성 Template 5종 + Template Mapping | **완료** |
| M23-Prep-T01C | EXECUTION_PROFILE(Standard Workflow) 도입 | **완료** |
| M23-Prep-T01D | PREPARATION_SUMMARY + M23 Start Criteria + 완료 반영 | **완료** |
| M23-Prep-T08 (Optional) | Obsidian MCP 연동 — Claude Code 도입 시점으로 이월 | 보류 |

**진행 상태**: **M23-Preparation 전체 완료(T01~T07 + T01A~T01D,
2026-07-27).** T08(Optional)만 Claude Code 도입 시점으로 이월
보류. 다음은 Milestone 23(Mobile Experience) 목표 검토 —
[[PREPARATION_SUMMARY]](Vault)의 M23 Start Criteria 참고.

#### M23-Prep-T01D: PREPARATION_SUMMARY + M23 Start Criteria + 완료 반영

**목표**: M23-Preparation(T01~T07 + T01A~T01C) 전체를 마무리
짓는다. 결과를 한 문서로 종합하고, 프로젝트 기준선(Baseline)을
확정하며, M23(Mobile Experience) 착수 전 반드시 확인해야 할
조건(Start Criteria)을 명시한다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `PREPARATION_SUMMARY.md` 신규(구현 완료 항목/신규 시스템 구성요소/템플릿 목록/Workflow 요약/Baseline/Start Criteria/Deferred Items 7절 포함) | ✅ |
| 2 | `PROJECT_INDEX.md`에 Preparation Status 절 추가 | ✅ |
| 3 | `AI_CONTEXT.md`의 "현재 상태" 절을 M23 기준으로 갱신 | ✅ |
| 4 | `.ai/TASKS.md`를 M23-Preparation 전체 완료 상태로 반영 | ✅ |
| 5 | `docs/ROADMAP.md` 갱신 | ✅ |
| 6 | `.ai/MEMORY.md` 갱신 | ✅ |
| 7 | M23 Start Criteria 정의(미해결 항목 정직하게 기록) | ✅ |
| 8 | 기존 구조·Backlink·Tag·원문 규칙 유지(검증 완료, 미해결 링크 0건) | ✅ |
| 9 | 변경된 파일만 수정 | ✅ |

**구현 내용**

- `00 System/PREPARATION_SUMMARY.md`(신규): T01~T07/T01A~T01C
  10개 Task를 표로 종합, `00 System/`의 6개 구성요소(PROJECT_INDEX/
  AI_CONTEXT/AI_RULES/PROMPT_PROFILE/EXECUTION_PROFILE/이 문서)와
  `99 Templates/`의 13개 템플릿(설계·실행용 6종 + Vault 등록용
  6종 + Architecture 1종)을 목록화. Baseline은 코드/아키텍처(v0.5.0
  기준선, Interface 27종)와 지식 관리(Vault 30개 문서, 4개 운영
  원칙) 두 층위로 구분해 기록. M23 Start Criteria 5개 중 3개(Client
  저장소 위치/서버 지원 범위/Push 발송 주체)를 "미정"으로 정직하게
  남기고, 나머지 2개(Production API 표준 필드/Vault 컨텍스트
  충족)는 "충족"으로 확인.
- `00 System/PROJECT_INDEX.md`(수정): "Preparation Status" 절
  추가 — M23-Preparation 완료 선언 + [[PREPARATION_SUMMARY]]로
  안내, 새 세션이 이 Vault를 쓰기 전 Start Criteria부터 확인하도록
  유도.
- `00 System/AI_CONTEXT.md`(수정): "현재 상태" 절을 M23-Preparation
  완료/M23 착수 대기 기준으로 갱신. T01A만 언급하던 "최근 변경"을
  "완료"/"다음"/"Baseline" 3항목으로 재구성하고 [[PREPARATION_SUMMARY]]
  로 위임.
- Vault 전체 재검증: 미해결 Backlink 0건(기존과 동일한 3건의
  텍스트 설명 오탐 외 신규 문제 없음).

**의존성**: M23-Prep-T01~T07 + T01A~T01C(전부 완료돼야 종합 가능).

---

**목표**: T01A(무엇을 읽을지)/T01B(무엇으로 만들지)에 이어, "요청을
받은 뒤 AI가 실제로 어떻게 처리하는가"의 표준 절차를 명문화한다.
Task Start부터 Completion Report까지 매 Task마다 반복해 온 절차
(이번 T01A/T01B 작업 자체가 실제 예시)를 문서화해 다음 세션도
동일한 순서를 따르게 한다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `EXECUTION_PROFILE.md` 신규 | ✅ |
| 2 | Standard Workflow 7단계(Task Start/Context Retrieval/Template Selection/Task Execution/Document Update/Validation/Completion Report) 정의 | ✅ |
| 3 | `PROMPT_PROFILE.md`에 Execution Profile 연계 절 추가 | ✅ |
| 4 | `PROJECT_INDEX.md`에 Execution Flow 절 추가 | ✅ |
| 5 | 기존 구조·Backlink·Tag·원문 규칙 유지(검증 완료, 미해결 링크 0건) | ✅ |
| 6 | 변경된 파일만 수정 | ✅ |
| 7 | `.ai/TASKS.md`/`docs/ROADMAP.md`/`.ai/MEMORY.md` 반영 | ✅ |

**구현 내용**

- `00 System/EXECUTION_PROFILE.md`(신규): Standard Workflow 7단계.
  Task Start(승인된 DoD 확인, 없으면 먼저 승인받음 — GitHub `.ai/
  RULES.md`의 승인 필요 원칙 참고)/Context Retrieval([[PROJECT_INDEX]]
  라우팅 표 사용)/Template Selection(Template Index/Mapping에서
  선택)/Task Execution(DoD 범위만, 변경된 파일만 수정)/Document
  Update(GitHub 원문 + Vault Index 동시 갱신)/Validation(Vault는
  Backlink·Tag·원문 섹션, GitHub는 테스트/`ruff`/`mypy`)/Completion
  Report(요청자 지정 형식 우선). 각 단계가 기존 원칙(GitHub Link
  Rule/Backlink Rule/Tag Rule/AI Reading Rule)을 대체하지 않고
  참조하도록 작성.
- `00 System/PROMPT_PROFILE.md`(수정): "Execution Profile 연계"
  절 추가 — 프롬프트 예시 표는 7단계 중 1단계(Task Start)의
  입력일 뿐임을 명시해 두 문서의 역할 경계를 분명히 함.
- `00 System/PROJECT_INDEX.md`(수정): "Execution Flow — 요청부터
  완료까지" 절 추가 — Retrieval First/Template Index/
  EXECUTION_PROFILE 3개 절을 하나의 흐름도로 연결.
- Vault 전체 재검증: 미해결 Backlink 0건(기존과 동일한 3건의
  텍스트 설명 오탐 외 신규 문제 없음).

**의존성**: M23-Prep-T01A/T01B(Retrieval First 라우팅 표와
Template Index/Mapping이 먼저 존재해야 Execution Flow가 그것들을
참조할 수 있음).

---

#### M23-Prep-T01B: 산출물별 작성 Template 5종 + Template Mapping

**목표**: T01A가 도입한 Template First 원칙을, Milestone/기능 설계
(DESIGN_TEMPLATE)뿐 아니라 개발 과정에서 반복 생성되는 산출물
(Task 기록/구현 보고/ADR/API 설계/가벼운 판단 기록)까지 확장한다.
"GitHub 원문 작성용 템플릿"과 "Vault Index 등록용 템플릿"(T01의
`Template - X.md` 6종)을 명확히 구분해 혼동을 없앤다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `IMPLEMENTATION_TEMPLATE.md` 신규 | ✅ |
| 2 | `ADR_TEMPLATE.md` 신규 | ✅ |
| 3 | `API_TEMPLATE.md` 신규 | ✅ |
| 4 | `DECISION_TEMPLATE.md` 신규 | ✅ |
| 5 | `TASK_TEMPLATE.md` 신규 | ✅ |
| 6 | `PROMPT_PROFILE.md`에 Template Mapping 절 추가 | ✅ |
| 7 | `PROJECT_INDEX.md`에 Template Index 절 추가 | ✅ |
| 8 | 기존 구조·Backlink·Tag·원문 규칙 유지(검증 완료, 미해결 링크 0건) | ✅ |
| 9 | 변경된 파일만 수정 | ✅ |
| 10 | `.ai/TASKS.md`/`docs/ROADMAP.md`/`.ai/MEMORY.md` 반영 | ✅ |

**구현 내용**

- `99 Templates/TASK_TEMPLATE.md`(신규): Task List 행/DoD 표/완료
  write-up 3단 구조 — TASKS.md의 실제 작성 패턴을 그대로 템플릿화.
- `99 Templates/IMPLEMENTATION_TEMPLATE.md`(신규): 변경 파일/핵심
  변경/설계 결정/테스트·검증/문서 갱신 5절 — 커밋 전 정리
  체크리스트, [[TASK_TEMPLATE]] 완료 write-up으로 압축해 들어감.
- `99 Templates/ADR_TEMPLATE.md`(신규): `.ai/DECISIONS.md`의 실제
  ADR 형식(상태/날짜/배경/결정/대안/이유/결과·영향) — 기존
  [[Template - ADR Summary]](Vault 3줄 요약 등록용)와 역할을
  명확히 구분.
- `99 Templates/API_TEMPLATE.md`(신규): 구현 전 계약 설계용
  (Request/Response/에러 처리/CQRS 분류/테스트 계획) — 기존
  [[Template - API]](완료된 엔드포인트의 회고적 카탈로그 등록용)와
  구분.
- `99 Templates/DECISION_TEMPLATE.md`(신규): ADR보다 가벼운 판단
  기록(Status/질문/답/근거) — 기존 [[Template - Decision]](Vault
  등록용)과 구분, "미정" 상태를 정직하게 남기는 것을 허용.
- `00 System/PROMPT_PROFILE.md`(수정): "Template Mapping" 절 추가
  — 산출물 종류(11행) → 템플릿 매핑 표 + "`_TEMPLATE.md`는 원문
  작성 전 계약 정리용, `Template - X.md`는 Vault 등록용"이라는
  구분 원칙 명문화.
- `00 System/PROJECT_INDEX.md`(수정): "Template Index" 절 추가 —
  Retrieval First 라우팅 표(작업 종류 기준)와 별개로, 산출물 종류
  기준의 템플릿 선택표를 보완.
- Vault 전체 재검증: 미해결 Backlink 0건(기존과 동일한 3건의
  텍스트 설명 오탐 외 신규 문제 없음).

**의존성**: M23-Prep-T01A(Template First 원칙과 DESIGN_TEMPLATE이
먼저 존재해야 함).

---

#### M23-Prep-T01A: Vault Retrieval/Prompt 효율화(Router+Template)

**목표**: M23-Preparation 완료 후 실사용 과정에서, 매 세션이 Vault
전체 구조를 다시 파악하거나 프롬프트에 문서 내용을 다시 붙여넣는
비효율을 줄인다. Retrieval First(문서를 다시 읽지 말고 라우팅부터)/
Short Prompt Workflow(문서 링크만 참조)/Template First(자유 서술
대신 표준 템플릿)를 Vault 운영 원칙에 추가한다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `PROJECT_INDEX.md` 신규 — 작업 종류→문서 라우팅 표 | ✅ |
| 2 | `AI_CONTEXT.md`를 "현재 상태" 섹션이 최상단에 오도록 개편 | ✅ |
| 3 | `AI_RULES.md`에 Context Retrieval Rule/Prompt Rules 추가 | ✅ |
| 4 | `PROMPT_PROFILE.md` 신규 — 짧은 프롬프트 패턴 예시 | ✅ |
| 5 | `DESIGN_TEMPLATE.md` 신규(`99 Templates/`) — 표준 설계 템플릿 | ✅ |
| 6 | 기존 구조·Backlink·Tag·원문 규칙 유지(검증 완료, 미해결 링크 0건) | ✅ |
| 7 | 변경된 파일만 수정(불필요한 리팩터 없음) | ✅ |
| 8 | `.ai/TASKS.md`/`docs/ROADMAP.md`/`.ai/MEMORY.md` 반영 | ✅ |

**구현 내용**

- `00 System/PROJECT_INDEX.md`(신규): "작업 종류 → 읽을 문서" 표
  13행, Short Prompt Workflow/Template First 절 포함. Vault 진입
  순서에서 `AI_CONTEXT`보다 앞선 최초 진입점으로 위치시킴.
- `00 System/AI_CONTEXT.md`(수정): "현재 상태(가장 먼저 확인)" 절을
  최상단으로 이동(완료/진행 중/최근 변경 3줄 요약), "이 Vault를
  읽는 순서" 절은 전체 흐름을 다시 설명하지 않고 [[PROJECT_INDEX]]
  로 위임하도록 축약. 기존 "Source of Truth는 GitHub다" 절과
  원문/관련 문서 링크는 그대로 유지.
- `00 System/AI_RULES.md`(수정): "Context Retrieval Rule(Retrieval
  First)"/"Prompt Rules(Short Prompt Workflow)" 2개 절을 "관련
  문서" 절 앞에 추가. 기존 6개 절(이 Vault가 아닌 것/하는 것/
  Backlink/Tag/GitHub Link/AI Reading Rule)은 변경 없음.
- `00 System/PROMPT_PROFILE.md`(신규): 반복 작업 유형 7종의 짧은
  프롬프트 예시 표 + 안티패턴 3종.
- `99 Templates/DESIGN_TEMPLATE.md`(신규): 지금까지 모든 Milestone
  Kickoff가 실제로 써온 구조(목표/배경/설계 원칙/범위/Out of Scope/
  DoD)를 `{{placeholder}}` 템플릿으로 정식화.
- Vault 전체 재검증: 미해결 Backlink 0건(순수 텍스트 설명 중
  "링크"/"문서 제목"/"이중 대괄호" 3건은 오탐 — 실제 `[[]]` 링크가
  아니라 문법을 설명하는 프롬프트/규칙 텍스트).

**의존성**: M23-Prep-T01~T07(모든 Index 문서가 이미 존재해야
PROJECT_INDEX 라우팅 표가 유효함).

---

#### M23-Prep-T07: 운영 문서 및 검증
- 상태: **DONE (2026-07-27)** — `12 Decisions/Decisions Index.md`
  신규(ADR보다 가벼운 "왜?" 메모, Status 필드 포함 — CQRS/EventBus/
  Core Domain 분리는 "확정", Server-iOS 저장소 분리 여부는 "미정"으로
  정직하게 기록). `13 Daily/README.md` 신규(Daily Note 사용법,
  [[Template - Daily]] 안내 — Daily Note는 Index 문서가 아니므로
  "원문" 섹션을 강제하지 않음을 명시). Vault 전체 검증: (1) 전체
  `[[Backlink]]` 스캔 결과 미해결 링크 0건(순수 텍스트 설명 중
  "이중 대괄호" 표현 1건은 오탐, 실제 깨진 링크 아님). (2) Tag Rule
  — 21개 문서 전부 frontmatter `tags:`가 `AI_RULES.md`에 정의된
  11종 중 하나를 사용함을 확인. (3) GitHub Link Rule — Index류
  문서(19개) 전부 "## 원문" 섹션 보유 확인, Daily Note류(Template/
  README)는 설계상 예외로 확인. 다음 단계: M23-Preparation 전체
  완료 승인 요청(아래 Review).
- 의존성: M23-Prep-T06.

#### M23-Prep-T06: Client 및 프로젝트 이력 정리
- 상태: **DONE (2026-07-27)** — `09 iOS/iOS Design.md` 신규(범위
  계획 — Home/Lock Screen Widget/Live Activity/Push, 사용할 서버
  API 목록, 미결정 사항 명시, "아직 구현하지 않는다" 원칙 준수).
  `10 Android/Android Placeholder.md` 신규(미착수 상태 기록).
  `11 Milestones/Milestones Index.md` 신규(M1~M22 전체를 이름/핵심
  결과/관련 ADR 표로 정리 + M23-Preparation 안내). 다음 Task:
  **M23-Prep-T07**(운영 문서 및 검증).
- 의존성: M23-Prep-T05.

#### M23-Prep-T05: 서버 구성 문서화
- 상태: **DONE (2026-07-27)** — `06 Dashboard/Dashboard Index.md`
  (Health/Automation Reader→Reader/Execution/ViewModel),
  `07 Automation/Automation Index.md`(Rule/Trigger/Scheduler/
  Execution Flow, M4-T07 AutomationEngine과의 이름 구분 경고 포함),
  `08 Production/Production Index.md`(Configuration/Lifecycle/
  Logging/Health/Version/배포 계획) 3종 신규. 각각 관련 ADR·
  Architecture·API Catalog로 상호 링크. 다음 Task: **M23-Prep-T06**
  (Client 및 프로젝트 이력 정리).
- 의존성: M23-Prep-T04.

#### M23-Prep-T04: Backend/API 문서화
- 상태: **DONE (2026-07-27)** — `04 Backend/Backend Index.md`
  신규(디렉터리별 역할 표, Interface 27종 중 최근 3개 Milestone
  요약, Core Engines vs Runtime 구분 설명). `05 API/API Catalog.md`
  신규(Dashboard/Automation/Production REST API 전체 + `/ws/
  dashboard` WebSocket 표, `/api/health`와 `/api/status`를 의도적으로
  분리한 설계 원칙 기록). 다음 Task: **M23-Prep-T05**(서버 구성
  문서화).
- 의존성: M23-Prep-T03.

#### M23-Prep-T03: ADR 정리
- 상태: **DONE (2026-07-27)** — `03 ADR/ADR Index.md` 신규. `.ai/
  DECISIONS.md`의 ADR-0001~ADR-0034(34개, 템플릿 자리표시자
  `ADR-000X` 제외) 전체를 전문 복사 없이 목적/결정/영향 3줄
  요약으로 압축해 하나의 Index 문서에 담았다(개별 ADR 파일 34개로
  쪼개지 않음 — 목표 검토 때 합의한 방식). 문서 끝에 `.ai/
  DECISIONS.md` 전체를 가리키는 "원문" 섹션 추가. `.gitkeep` 제거.
  다음 Task: **M23-Prep-T04**(Backend/API 문서화).
- 의존성: M23-Prep-T02.

#### M23-Prep-T02: 프로젝트 개요 및 아키텍처
- 상태: **DONE (2026-07-27)** — `01 Overview/Overview.md`(프로젝트
  소개, 저장소 목록, 현재 진행률, Backend 상태, Mobile 계획, 현재
  Milestone). `02 Architecture/Architecture Overview.md`(Layer
  구조, 핵심 컴포넌트 표, CQRS/EventBus/Repository 패턴 요약,
  Interface 27종). `02 Architecture/Architecture Map.md`(영역별
  진입점 지도 — 아직 만들어지지 않은 T04~T07 산출물도 미리
  `[[]]` 링크로 걸어둠, Obsidian에서 "unresolved link"로 보이다가
  이후 Task가 채우면 자동 연결됨). 다음 Task: **M23-Prep-T03**
  (ADR 정리).
- 의존성: M23-Prep-T01.

#### M23-Prep-T01: Vault 초기 구성 및 시스템 문서
- 상태: **DONE (2026-07-27)** — 저장소 루트에 `Vault/`(PARA 구조)
  생성: `00 Inbox`/`01 Projects/AI Workspace/`(00 System~99
  Templates 16개 하위 폴더)/`02 Resources`/`03 Archives`. `00
  System/AI_CONTEXT.md`(AI가 Vault를 열었을 때 가장 먼저 읽는
  문서 — 프로젝트 정의, Source of Truth는 GitHub임을 명시, 읽기
  순서 안내)와 `AI_RULES.md`(Vault가 코드 저장소가 아니고 GitHub를
  대체/수정/복제하지 않는다는 원칙, Backlink Rule/Tag Rule
  (`#backend #ios #android #dashboard #automation #production
  #architecture #decision #api #milestone #system`)/GitHub Link
  Rule(Index 문서 마지막에 "원문" 섹션)/AI Reading Rule(작업별
  최소 문서만 읽고 필요 시 GitHub 원문 확인)) 신규. `99 Templates/`
  에 6종 Template(Architecture/ADR Summary/API/Decision/Milestone/
  Daily) 신규 — 전부 frontmatter 태그 + Backlink + "원문" 섹션
  틀을 포함해 이후 Task가 이 틀을 그대로 채우도록 함. 아직 내용이
  없는 폴더에는 `.gitkeep`을 둬 폴더 구조 자체가 Git에 반영되게
  했다. 다음 Task: **M23-Prep-T02**(프로젝트 개요 및 아키텍처).
- 의존성: 없음.

---

## M23-Preparation Review

**1. Definition of Done 체크리스트**(사용자 원본 스펙 기준 요약)

| # | DoD 항목 | 상태 |
|---|---|---|
| 1 | GitHub가 Source of Truth로 유지되고 Vault는 이를 복제하지 않음 | ✅ (`AI_RULES.md`, 모든 Index의 "원문" 섹션) |
| 2 | Vault가 저장소 루트 `Vault/`에 체크인되어 GitHub와 함께 버전 관리 | ✅ (T01) |
| 3 | PARA 구조(00 Inbox/01 Projects/02 Resources/03 Archives) | ✅ (T01) |
| 4 | `00 System/AI_CONTEXT.md`, `AI_RULES.md` | ✅ (T01) |
| 5 | Backlink Rule(`[[Wikilink]]`) 적용 | ✅ (T02~T07, 미해결 링크 0건) |
| 6 | Tag Rule(11종 태그) 적용 | ✅ (T01 정의, T07 검증) |
| 7 | GitHub Link Rule("원문" 섹션) | ✅ (T01 Template, T07 검증) |
| 8 | AI Reading Rule 문서화 | ✅ (T01 `AI_RULES.md`) |
| 9 | Overview/Architecture Overview/Architecture Map | ✅ (T02) |
| 10 | ADR Index(전문 비복제, 목적/결정/영향 요약) | ✅ (T03, 34개) |
| 11 | Backend Index/API Catalog | ✅ (T04) |
| 12 | Dashboard/Automation/Production Index | ✅ (T05) |
| 13 | iOS Design(설계만)/Android Placeholder | ✅ (T06) |
| 14 | Milestones Index(M1~M22) | ✅ (T06) |
| 15 | Decisions Index | ✅ (T07) |
| 16 | Daily Notes Template/사용법 | ✅ (T01 Template, T07 README) |
| 17 | Template 6종 | ✅ (T01) |
| 18 | Vault 전체 링크/태그/원문 섹션 검증 | ✅ (T07) |

**2. 산출물 요약**

- 신규 문서 19개(Index/Design류) + Template 6개 + System 문서 2개
  + Daily README 1개 = 총 28개 Markdown 파일.
- Obsidian MCP 연동(T08, Optional)은 사용자 지시대로 보류 —
  Claude Code 도입 시점에 별도 Task로 이월.

**3. 원칙 준수 확인**

- GitHub 원문을 복사한 곳 없음 — 모든 Index가 요약 + 링크로만
  구성됨(특히 ADR Index가 34개 ADR을 각 3줄로 압축).
- Core Domain은 Dashboard/Automation/Production을 모른다는 원칙과
  동일하게, Vault도 GitHub 문서 구조를 그대로 반영하되 원문을
  소유하지 않음.
- M23(Mobile Experience) 착수 전 필요한 배경지식(Backend 구조,
  API 목록, Production 표준 필드, 기존 Milestone 이력)이 한 곳에
  정리되어 다음 세션이 GitHub 전체를 다시 훑지 않고도 M23을 시작할
  수 있는 상태.

**4. Out of Scope 확인**

- MCP 연동(T08) — 이번 범위 아님, 보류.
- Vault 내용에 대한 자동 동기화/알림 — 이번 범위 아님.

Task List(M23-Prep-T01~T07) 전체 완료. 이후 T01A(Retrieval/Prompt
효율화)~T01D(PREPARATION_SUMMARY+Start Criteria)가 추가되어
**M23-Preparation 전체 완료**(2026-07-27, T01D를 통한 사용자
지시로 최종 반영 — 상세 Baseline/Start Criteria는 Vault
`PREPARATION_SUMMARY.md` 참고).

---

## M23-T01 — Reading Profiles

**목표**: M23-Prep-T01A~T01D에서 도입한 Retrieval First/Minimum
Retrieval/Short Prompt Workflow/Template First/Standard Execution
Workflow 원칙을 작업 유형별로 세분화한 **표준 Reading Profile**을
정의한다. AI가 매 작업마다 무엇을 읽을지 새로 판단하지 않고, 15개
작업 유형(Architecture Design/Feature Design/API Design/Backend·
Frontend·Mobile Implementation/Dashboard·Automation Development/
ADR·Decision 작성/Bug Fix/Refactoring/Documentation/Milestone
Planning/Daily 기록) 각각에 대해 필수/선택/제외 문서, 쓸 Template,
예상 Retrieval 순서, 예상 출력 문서를 고정된 형식으로 미리
정해두어 최소 문서 Retrieval 기준을 제공한다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `READING_PROFILES.md` 신규(15개 Profile, 항목별 목적/필수/선택/제외 문서/Template/Retrieval 순서/예상 출력 7항목 고정) | ✅ |
| 2 | `PROJECT_INDEX.md`에 Reading Profiles Index 절 추가 | ✅ |
| 3 | `EXECUTION_PROFILE.md`의 Context Retrieval/Template Selection 단계에 Reading Profile 적용 절차 추가 | ✅ |
| 4 | `PROMPT_PROFILE.md`에 Reading Profile 연계 절 추가 | ✅ |
| 5 | 기존 구조·Backlink·Tag·원문 규칙 유지, 변경된 파일만 수정 | ✅ |
| 6 | `.ai/TASKS.md`/`docs/ROADMAP.md`/`.ai/MEMORY.md` 반영 | ✅ |

**구현 내용**

- `Vault/.../00 System/READING_PROFILES.md`(신규): 사용 원칙
  (Retrieval First/Minimum Retrieval/Short Prompt Workflow/
  Template First/Standard Execution Workflow) + Profile Index
  표 + 15개 Profile 절. 각 Profile은 목적/필수 문서/선택 문서/
  읽지 않는 문서/쓸 Template/예상 Retrieval 순서/예상 출력 문서
  7항목을 동일한 형식으로 고정. Backend Implementation은
  [[Backend Index]]를 필수로, iOS Design/Android Placeholder를
  제외 문서로 두는 식으로 작업 간 경계를 명시해 불필요한 교차
  Retrieval을 방지.
- `00 System/PROJECT_INDEX.md`(수정): "Reading Profiles Index"
  절 추가 — 기존 Retrieval First 표(작업→문서 1줄 라우팅)와
  [[READING_PROFILES]](작업 유형별 세부 Retrieval 절차)의 역할
  경계를 명시.
- `00 System/EXECUTION_PROFILE.md`(수정): 2단계 Context Retrieval에
  Reading Profile이 정의된 작업 유형이면 그 Profile의 필수 문서만
  읽도록 절차 추가, 3단계 Template Selection에 Reading Profile의
  "쓸 Template"도 동일한 Template Index/Mapping과 일치함을 명시.
- `00 System/PROMPT_PROFILE.md`(수정): "Reading Profile 연계" 절
  추가 — 프롬프트에 "[[READING_PROFILES]]의 <Profile 이름> 기준으로"
  를 덧붙이는 패턴 예시 추가.
- Vault 전체 재검증: 신규 문서의 Backlink/Tag/원문 섹션 확인,
  기존 문서 대비 신규 미해결 Backlink 없음.

**의존성**: M23-Prep-T01A(Retrieval First 라우팅 표)~T01D
(Standard Execution Workflow 정착) 전부 완료돼야 세분화할 기반이
존재함.

---

## Milestone 23 — Obsidian Integration & Auto Save

**목표**(2026-07-27 사용자 재정의 — 기존 "Mobile Experience"에서
전환): AI Workspace(GitHub)와 Obsidian Vault를 통합한다. Retrieval
First Workflow를 유지하면서 Markdown 문서를 자동 생성·저장·갱신
하는 구조를 구현해, 사용자가 짧은 명령만 입력해도 AI가 Retrieval
→ 작업 → Vault 저장까지 수행할 수 있는 기반을 마련한다.

**기본 원칙**: Retrieval First / Minimum Retrieval / Template
First / Short Prompt Workflow / Standard Execution Workflow /
기존 Architecture 및 문서 구조 유지 / 변경된 파일만 수정 / 모든
설계는 Obsidian Vault를 기준으로 한다.

**Mobile Experience는 이 Milestone에서 분리되어 이월됨**: M23이
"Obsidian Integration & Auto Save"로 재정의됨에 따라, 이전 M23
kickoff에서 다룬 Mobile Experience(Push Notification 아키텍처
설계 등, 구 M23-T02~T05 제안)는 별도 Milestone(번호 미정, kickoff
시점에 확정)으로 이월한다. **M23 Start Criteria로 확정했던 3개
결정(Client 별도 저장소/Server API 전용 범위/Push는 Server 생성+
FCM·APNs 전송)은 그대로 유효**하며, 해당 Milestone 착수 시 다시
불러와 그대로 적용한다([[PREPARATION_SUMMARY]], [[Decisions Index]]
"왜 Server와 iOS/Android를 분리했는가" 참고).

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M23-T01 | Reading Profiles — 작업 유형별 Retrieval Profile 정의 | **완료** |
| M23-T02 | Obsidian Integration Architecture — Vault 연동 구조/저장 전략/Auto Save Architecture 설계, ADR 작성 | **완료** |
| M23-T03 | Vault Save Engine — Markdown 생성/저장 엔진 구현 | **완료** |
| M23-T04 | Auto Save Workflow — Task 완료 후 자동 Vault 갱신 | **완료** |
| M23-T05 | Vault Synchronization — Create/Update/Rename/Delete/Conflict/Version/Link·Backlink 검증 정책 | **완료** |
| M23-T06 | Execution Engine — 자연어 명령 → Retrieval → Template → 작업 → Vault 저장 → Validation → 완료 보고 라우팅 | **완료** |
| M23-T07 | Execution Environment Integration — Claude Code/Filesystem/MCP/GitHub 실제 연동 검증 | **완료** |

#### M23-T02: Obsidian Integration Architecture

**목표**: AI Workspace(GitHub) ↔ Obsidian Vault 연동 구조를
설계한다. Vault Directory Mapping/Document Routing/Save Flow/File
Strategy를 정의하고 ADR로 결정을 기록한다. 실제 구현(Markdown
생성기/Writer 코드)은 이 Task 범위가 아니다(M23-T03).

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `.ai/DECISIONS.md`에 ADR-0035(Vault Integration Layer) 신규 | ✅ |
| 2 | `docs/ARCHITECTURE.md`에 §3.21(Vault Integration Layer) + §9 디렉터리 구조에 `vault/` 반영 | ✅ |
| 3 | Vault Directory Mapping(kind → Vault 파일, Tag Rule 11종과 1:1) 정의 | ✅ |
| 4 | Save Flow(구조화 입력 → Document Router → Markdown Generator → Vault Writer) 정의 | ✅ |
| 5 | File Strategy(신규 생성 vs 기존 섹션 치환, 변경 시에만 저장) 정의 | ✅ |
| 6 | Vault `Vault Integration Architecture.md` 신규(설계를 Vault 기준으로 반영) | ✅ |
| 7 | `ADR Index`/`Architecture Overview`/`Architecture Map`에 backlink 추가 | ✅ |
| 8 | 새 Core Interface 미추가 확인(Production Platform과 동일 판단) | ✅ |
| 9 | 기존 구조·Backlink·Tag·원문 규칙 유지, 변경된 파일만 수정 | ✅ |

**구현 내용**

- `.ai/DECISIONS.md`(수정): ADR-0035 신규. `vault/`를 `storage/`와
  나란한 새 최상위 패키지로 결정하되 Core Domain·`web/` 양쪽 모두
  이를 모르는 완전 독립 계층으로 설계(제품 기능이 아니라 개발
  도구). Vault Directory Mapping 13종(kind→대상 파일), 4단계 Save
  Flow, File Strategy(섹션만 치환·변경 시에만 저장), Metadata
  처리 원칙을 결정. M23-T03~T07은 이 ADR의 결정 범위 밖으로 명시.
- `docs/ARCHITECTURE.md`(수정, v0.25.0): 신규 §3.21 Vault
  Integration Layer — Execution Flow 다이어그램 + 컴포넌트 요약.
  §9에 `vault/`(설계됨, 미구현) 추가. 상단 상태 표기를 M23 재정의
  기준으로 갱신.
- `Vault/.../02 Architecture/Vault Integration Architecture.md`
  (신규): [[Template - Architecture]] 구조로 ADR-0035를 Vault
  기준으로 반영 — 핵심 컴포넌트/Execution Flow/Vault Directory
  Mapping 표/File Strategy/범위 밖 목록.
- `ADR Index`/`Architecture Overview`/`Architecture Map`(수정):
  ADR-0035 3줄 요약 추가, [[Vault Integration Architecture]]
  backlink 추가.
- Vault 전체 재검증: 신규 문서 Backlink/Tag/"원문" 섹션 확인.

**의존성**: M23-T01(Reading Profiles) 완료.

---

#### M23-T03: Vault Save Engine

**목표**: M23-T02(ADR-0035)에서 결정한 Vault Directory Mapping/
Save Flow/File Strategy를 실제 코드로 구현한다. Markdown 생성 및
저장 엔진(Markdown Generator/Vault Writer/File Creator/File
Updater/Metadata 처리/Template 적용)을 신규 `vault/` 패키지로
만든다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `vault/models.py` — `VaultDocumentKind`(12종)/`VaultDocumentRequest` 구조화 입력 | ✅ |
| 2 | `vault/mapping.py` — ADR-0035의 Vault Directory Mapping을 그대로 데이터로 구현 | ✅ |
| 3 | `vault/router.py` — `DocumentRouter`(kind→대상 파일+append/create 결정, Daily는 날짜 치환) | ✅ |
| 4 | `vault/markdown_generator.py` — ADR/Decision은 실제 Vault 관행(목적/결정/영향, Status/질문/답)에 맞춘 전용 렌더링, 나머지 kind는 공통 Summary 형식(Template 적용) | ✅ |
| 5 | `vault/writer.py` — `VaultWriter`(File Creator: 신규 생성, 기존 파일 덮어쓰지 않음 / File Updater: 대상 섹션만 upsert, 내용 불변 시 파일 미변경) | ✅ |
| 6 | `vault/engine.py` — `VaultSaveEngine`(Router→Generator→Writer Save Flow 전체를 잇는 진입점) | ✅ |
| 7 | `tests/vault/` 신규 18개(Router/Generator/Writer/Engine) — 신규 삽입/기존 섹션 교체/무변경 시 no-op/"관련 문서" 절 없을 때 fallback 케이스 포함 | ✅ |
| 8 | `ruff check src/ai_workspace/vault tests/vault`, `mypy src/ai_workspace/vault` 클린 | ✅ |
| 9 | `docs/ARCHITECTURE.md`(§3.21 구현 상태 반영, §9 `vault/` 완료 표시) 갱신 | ✅ |
| 10 | Vault `Vault Integration Architecture.md`/`Backend Index`에 구현 상태 반영 | ✅ |
| 11 | Core Domain·`web/`이 `vault/`를 참조하지 않음(반대 방향 의존도 없음) 확인 | ✅ |
| 12 | 변경된 파일만 수정, 새 Core Interface 미추가 | ✅ |

**구현 내용**

- `src/ai_workspace/vault/models.py`(신규): `VaultDocumentKind`
  Enum(Tag Rule 11종 중 자동 저장 대상 12종 — `system`은 수동 문서라
  제외), `VaultDocumentRequest`(frozen dataclass — kind/title/
  summary/related_docs/source_paths/fields/date). Core Domain
  타입을 전혀 import하지 않음(ADR-0035가 요구한 완전 독립).
- `src/ai_workspace/vault/mapping.py`(신규): `VAULT_DIRECTORY_MAP`
  — kind→(상대 경로, append/create) 딕셔너리. ADR-0035의 매핑표를
  코드가 아니라 데이터로 그대로 옮김.
- `src/ai_workspace/vault/router.py`(신규): `DocumentRouter.
  resolve()`가 매핑을 조회해 `VaultTarget(path, mode)`을 만든다.
  Daily는 `request.date`(없으면 오늘 날짜)로 `{date}.md` 파일명을
  채운다. 매핑에 없는 kind는 `UnroutableVaultKindError`.
- `src/ai_workspace/vault/markdown_generator.py`(신규):
  `render_section()`이 (heading, body) 튜플을 만든다. ADR/Decision
  kind는 실제 `ADR Index`/`Decisions Index`에서 관찰되는 형식
  (목적/결정/영향, Status/질문/답)을 그대로 따르고, 나머지 kind는
  제목+요약+관련 문서 링크로 구성된 공통 Summary 형식을 쓴다(kind별
  전용 형식은 실제로 필요해질 때 추가 — YAGNI). `render_daily_file()`
  은 [[Template - Daily]] 구조를 그대로 생성한다. 필수 `fields`가
  빠지면 `MissingVaultFieldError`.
- `src/ai_workspace/vault/writer.py`(신규): `VaultWriter.
  create_file()`은 파일이 이미 있으면 덮어쓰지 않고 `False`를
  반환(Conflict 정책은 M23-T05로 이월). `upsert_section()`은 같은
  "## {heading}" 섹션이 있으면 그 섹션만 교체하고, 없으면 "## 관련
  문서" 절 바로 앞에 삽입하며, "관련 문서" 절 자체가 없는 파일은
  말미에 추가한다. 렌더링 결과가 원본과 같으면 파일을 쓰지 않고
  `False`를 반환(File Strategy의 "실제 변경 시에만 저장" 그대로
  구현).
- `src/ai_workspace/vault/engine.py`(신규): `VaultSaveEngine.save()`
  가 Router→Generator→Writer 전체 Save Flow를 하나의 호출로
  묶는다. M23-T04(Auto Save Workflow)가 이 클래스 하나만 호출하면
  되도록 설계.
- `tests/vault/`(신규, 18개): `test_router.py`(kind→경로 매핑,
  Daily 날짜 치환, 알 수 없는 kind 예외), `test_markdown_generator.py`
  (ADR/Decision 전용 필드 렌더링과 필수 필드 누락 예외, 공통 Summary
  형식, Daily 템플릿 구조), `test_writer.py`(신규 삽입/기존 섹션
  교체/무변경 시 no-op/"관련 문서" 없을 때 fallback/기존 파일
  덮어쓰지 않음), `test_engine.py`(ADR 저장→ADR Index 반영, Daily
  파일 생성, 반복 저장 시 두 번째 호출은 `False`).
- `docs/ARCHITECTURE.md`(v0.26.0): §3.21에 구현 상태 절 추가, §9
  `vault/` 항목을 "설계됨" → "구현됨"으로 갱신.
- Vault `Vault Integration Architecture.md`(수정): "범위 밖" 절을
  "구현 상태" 절로 교체. `Backend Index`(수정): `vault/` 행 추가.
- 검증: `poetry run ruff check src/ai_workspace/vault tests/vault`
  / `poetry run mypy src/ai_workspace/vault` / `poetry run pytest
  tests/vault` 전부 통과(18개). 전체 `pytest`/`mypy src`는 이 세션
  환경에 `pyyaml`/`fastapi`/`uvicorn`이 설치돼 있지 않아 기존
  Milestone 코드 쪽에서도 동일하게 실패함을 확인(내가 만든 `vault/`
  와 무관한 사전 존재 환경 제약 — `pyproject.toml`은 건드리지
  않음).

**의존성**: M23-T02(Obsidian Integration Architecture, ADR-0035)
완료.

---

#### M23-T04: Auto Save Workflow

**목표**: Task 완료 후 여러 `VaultDocumentRequest`를 한 번에
저장하고, Vault 전체를 Validation한 뒤, 완료 보고 문구까지 만드는
Workflow를 구현한다. EXECUTION_PROFILE Standard Workflow의 4단계
(Task Execution 종료)~7단계(Completion Report) 사이에서 "자동 저장
→ Validation → 완료 보고" 흐름을 코드 한 번의 호출로 수행한다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `vault/validation.py` — `find_broken_backlinks`(Vault 전체 Backlink Rule 검증) | ✅ |
| 2 | `vault/validation.py` — `find_missing_tags`(신규 생성 파일의 Tag Rule 검증) | ✅ |
| 3 | `vault/auto_save.py` — `run_auto_save()`가 여러 요청을 `VaultSaveEngine`으로 저장 | ✅ |
| 4 | `run_auto_save()`가 저장 후 Backlink/Tag Validation을 자동 수행 | ✅ |
| 5 | `AutoSaveReport`(저장/미변경/Validation 실패 목록 + `ok`/`summary()`)로 완료 보고 문구 생성 | ✅ |
| 6 | `tests/vault/test_validation.py`/`test_auto_save.py` 신규 9개(깨진 Backlink 탐지, Tag 누락 탐지, 저장 성공/중복 저장 시 unchanged, 신규 파일 생성 케이스 포함) | ✅ |
| 7 | `ruff check src/ai_workspace/vault tests/vault`, `mypy src/ai_workspace/vault` 클린 | ✅ |
| 8 | `docs/ARCHITECTURE.md`/Vault `Vault Integration Architecture.md`/`Backend Index`에 구현 상태 반영 | ✅ |
| 9 | 변경된 파일만 수정, 새 Core Interface 미추가 | ✅ |

**구현 내용**

- `src/ai_workspace/vault/validation.py`(신규): `find_broken_
  backlinks()`가 Vault 전체 `.md` 파일에서 `[[제목]]` 패턴을 찾아
  파일명(확장자 제외) 집합과 대조한다 — 존재하지 않는 문서를
  가리키면 `VaultValidationIssue`. `find_missing_tags()`는 주어진
  경로들의 frontmatter에 `tags: [...]` 줄이 있는지 확인한다 —
  append 모드는 기존 파일의 frontmatter를 건드리지 않으므로
  `run_auto_save()`는 이 함수를 **새로 만든 파일(create 모드)에만**
  적용한다.
- `src/ai_workspace/vault/auto_save.py`(신규): `run_auto_save
  (vault_root, requests)`가 각 요청을 `DocumentRouter.resolve()`로
  대상 경로를 먼저 알아낸 뒤 `VaultSaveEngine.save()`로 저장하고,
  변경 여부에 따라 저장됨/미변경 목록에 나눠 담는다. 저장이 끝나면
  Vault 전체 Backlink 검증 + 새로 생성된 파일의 Tag 검증을 실행해
  `AutoSaveReport`(저장/미변경 경로, Validation 이슈 목록)를
  만든다. `AutoSaveReport.summary()`가 "저장됨 N개/변경 없음 N개/
  Validation 통과(또는 실패 목록)" 형태의 완료 보고 문구를 만들어,
  Standard Workflow 7단계(Completion Report)에 바로 붙여 쓸 수
  있게 한다.
- `tests/vault/test_validation.py`(신규, 5개): 깨진 Backlink 탐지/
  전부 정상일 때 빈 목록/frontmatter 없는 파일 탐지/tags 있는
  파일 통과/존재하지 않는 경로는 건너뜀.
- `tests/vault/test_auto_save.py`(신규, 4개): 저장 성공 시 report
  구성 확인, 동일 요청 재호출 시 `unchanged_paths`로 분류, 관련
  문서에 존재하지 않는 문서를 링크하면 `ok=False`로 잡힘, Daily
  파일 생성 후 Tag Validation 통과.
- `docs/ARCHITECTURE.md`(v0.27.0)/Vault `Vault Integration
  Architecture.md`/`Backend Index`(수정): 구현 상태 절 추가.
- 검증: `poetry run ruff check src/ai_workspace/vault tests/vault`
  / `poetry run mypy src/ai_workspace/vault` / `poetry run pytest
  tests/vault` 전부 통과(27개, T03 18 + T04 9). 전체 `pytest`/
  `mypy src`는 M23-T03과 동일한 사전 존재 환경 제약(이 세션에
  `pyyaml`/`fastapi`/`uvicorn` 미설치)으로 여전히 실패 — `vault/`
  와 무관.

**의존성**: M23-T03(Vault Save Engine) 완료.

---

#### M23-T05: Vault Synchronization

**목표**: Create/Update 외 나머지 Vault 파일 관리 정책(Rename/
Delete/Conflict Handling/Version Strategy/Link·Backlink 검증)을
구현한다. Create/Update는 M23-T03의 `VaultWriter`가 이미 담당하고,
Link/Backlink 검증은 M23-T04의 `find_broken_backlinks()`가 이미
담당하므로 이 Task는 그 위에 Rename/Delete/Conflict Handling을
추가하고 Version Strategy를 결정하는 데 집중한다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `vault/sync.py` — `rename_document()`(파일명 변경 + Vault 전체 Backlink 일괄 갱신) | ✅ |
| 2 | `vault/sync.py` — `delete_document()`(참조 중이면 기본 거부, `force=True`로 강제 삭제 가능) | ✅ |
| 3 | `vault/sync.py` — `find_references()`(Delete 전 참조 확인에 재사용) | ✅ |
| 4 | `vault/sync.py` — `content_hash()` + `VaultWriter.upsert_section(expected_hash=...)`(Conflict Handling) | ✅ |
| 5 | Version Strategy 결정(별도 버전 시스템 신설 없이 git 기반 유지) 및 문서화 | ✅ |
| 6 | Link/Backlink Validation은 M23-T04 `find_broken_backlinks()` 재사용 확인(중복 구현 없음) | ✅ |
| 7 | `tests/vault/test_sync.py` 신규 9개 + `test_writer.py` Conflict 케이스 2개 | ✅ |
| 8 | `ruff check src/ai_workspace/vault tests/vault`, `mypy src/ai_workspace/vault` 클린 | ✅ |
| 9 | `docs/ARCHITECTURE.md`/Vault `Vault Integration Architecture.md`/`Backend Index`에 구현 상태 반영 | ✅ |
| 10 | 변경된 파일만 수정, 새 Core Interface 미추가 | ✅ |

**구현 내용**

- `src/ai_workspace/vault/sync.py`(신규): `rename_document(vault_
  root, old_title, new_title)`이 `{old_title}.md`를 찾아 이름을
  바꾸고, Vault 전체 `.md` 파일에서 `[[old_title]]`/
  `[[old_title|별칭]]`/`[[old_title#절]]`을 정규식으로 찾아
  `new_title` 기준으로 갱신한다(Backlink Rule 유지). 대상 이름이
  이미 존재하면 `VaultConflictError`, 원본이 없으면
  `VaultDocumentNotFoundError`. `delete_document(vault_root, title,
  force=False)`는 `find_references()`로 아직 참조 중인 문서가
  있으면 삭제하지 않고 `DeleteResult(deleted=False, referencing_
  paths=...)`를 돌려준다(Orphan Backlink 방지) — `force=True`일
  때만 참조가 남아 있어도 삭제한다. `content_hash()`(sha256)는
  `vault/writer.py`의 `VaultWriter.upsert_section()`에 새 키워드
  인자 `expected_hash`로 연결돼, 저장 직전에 실제 파일 해시가
  다르면(그 사이 다른 경로로 파일이 바뀜) 조용히 덮어쓰는 대신
  `VaultConflictError`를 낸다.
- **Version Strategy 결정**: 별도 버전 관리 시스템(파일별 리비전
  번호, 스냅샷 등)을 새로 만들지 않는다 — `Vault/`는 이미 GitHub
  저장소와 함께 git으로 버전 관리되므로 파일 단위 변경 이력은
  git이 그대로 담당한다(ADR-0035와 동일한 최소 복잡성 원칙 적용,
  새 ADR 불필요 — 기존 결정의 연장).
- `tests/vault/test_sync.py`(신규, 9개): 해시 변화 감지, 참조
  문서 탐색, Rename 후 파일 이동 + 별칭/절 포함 Backlink 갱신
  확인, 원본 없음/대상 이름 충돌 예외, 참조 중인 문서 삭제 거부/
  `force=True` 강제 삭제/참조 없는 문서 정상 삭제/원본 없음 예외.
- `tests/vault/test_writer.py`(수정, 2개 추가): `expected_hash`가
  다르면 `VaultConflictError`, 일치하면 정상 저장.
- `docs/ARCHITECTURE.md`(v0.28.0)/Vault `Vault Integration
  Architecture.md`/`Backend Index`(수정): 구현 상태 반영.
- 검증: `poetry run ruff check src/ai_workspace/vault tests/vault`
  / `poetry run mypy src/ai_workspace/vault` / `poetry run pytest
  tests/vault` 전부 통과(38개, T03 18 + T04 9 + T05 11). 전체
  `pytest`/`mypy src`는 M23-T03/T04와 동일한 사전 존재 환경 제약
  (`pyyaml`/`fastapi`/`uvicorn` 미설치)으로 여전히 실패 — `vault/`
  와 무관.

**의존성**: M23-T03(Vault Save Engine)/M23-T04(Auto Save Workflow)
완료.

---

#### M23-T06: Execution Engine

**목표**: 자연어 명령("다음 Task 진행", "M23-T05 진행", "ADR 작성"
등)이 실제 작업으로 이어지는 전체 경로(PROJECT_INDEX → AI_CONTEXT
→ TASKS → READING_PROFILES → Retrieval → Template 선택 → 작업
수행 → Vault 저장 → Validation → 완료 보고)를 명문화한다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 명령 라우팅을 새 결정적 프로그램이 아니라 절차 문서로 구현하기로 판단하고 근거 기록(자연어 해석은 AI 역할) | ✅ |
| 2 | Vault `EXECUTION_PROFILE`에 "Execution Engine" 절 추가 — 흐름도(사용자 명령→...→완료 보고) | ✅ |
| 3 | "지원 명령 예시" 표(다음 Task 진행/M23-T05 진행/ADR 작성/Bug Fix/Feature Design/API 설계 → 적용 Reading Profile) | ✅ |
| 4 | 5단계(Document Update)가 `vault.auto_save.run_auto_save()`를 구체적으로 가리키도록 갱신 | ✅ |
| 5 | 6단계(Validation)가 `AutoSaveReport`를 구체적으로 가리키도록 갱신 | ✅ |
| 6 | Vault `Vault Integration Architecture.md`/`docs/ARCHITECTURE.md`에 구현 상태(절차 문서) 반영 | ✅ |
| 7 | 변경된 파일만 수정, 새 Core Interface/새 코드 미추가(의도적) | ✅ |

**구현 내용**

- **판단**: 자연어 명령("다음 Task 진행" 등)을 해석해 어떤
  Task/Reading Profile을 적용할지 정하는 것은 AI(이 세션) 자체의
  역할이다 — 정규식/키워드 매칭으로 흉내 낸 "명령 파서"를 만들면
  실제로 아무도 호출하지 않는 죽은 코드가 된다(이 세션의 판단은
  Python 함수 호출이 아니라 매 턴의 추론이다). 그래서 T06은
  Retrieval/Template/저장/검증처럼 **이미 코드로 뒷받침되는
  부분**([[READING_PROFILES]], `vault/`)과, **AI가 그때그때
  해석하는 부분**(자연어 이해)의 경계를 명확히 하고, 전자를 후자가
  일관되게 거치도록 절차로 고정하는 데 집중했다.
- Vault `00 System/EXECUTION_PROFILE.md`(수정): "Execution Engine
  — 자연어 명령 라우팅" 절 신규. 사용자가 제시한 흐름(PROJECT_INDEX
  → AI_CONTEXT → TASKS → READING_PROFILES → Retrieval → Template
  선택 → 작업 수행 → Vault 저장 → Validation → 완료 보고)을 그대로
  다이어그램으로 옮기고, "지원 명령 예시" 표(다음 Task 진행/다음
  작업 진행/M23-T05 진행/ADR 작성/Bug Fix/Feature Design/API 설계
  → 적용 Reading Profile)를 추가했다. 5단계(Document Update)에
  "GitHub 원문 갱신 내용을 `VaultDocumentRequest`로 정리할 수
  있으면 `vault.auto_save.run_auto_save()`를 호출" 문구를 추가하고,
  6단계(Validation)를 `AutoSaveReport.ok`/`summary()` 기준으로
  구체화했다.
- Vault `Vault Integration Architecture.md`/`docs/ARCHITECTURE.md`
  (v0.29.0, §3.21)(수정): "구현 상태(M23-T06)" 절 추가 — 새 코드가
  아니라 절차 문서임을 명시.
- 코드 변경 없음(의도적) — `tests/vault/`는 38개 그대로.

**의존성**: M23-T04(Auto Save Workflow)/M23-T05(Vault
Synchronization) 완료(Execution Engine이 가리키는 `run_auto_save()`
/`AutoSaveReport`가 실제로 존재해야 함).

---

#### M23-T07: Execution Environment Integration

**목표**: `vault/`(M23-T03~T06)가 이 세션의 실제 실행 환경(Claude
Code CLI, Filesystem, MCP, GitHub Repository)에서 실제로 동작하는지
검증한다. `tests/vault/`는 전부 `tmp_path` 최소 fixture만 다뤘으므로,
실제 `Vault/` 디렉터리를 대상으로 한 통합 테스트로 마무리한다.
Milestone 23의 마지막 Task.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Filesystem 접근 검증 — 실제 `Vault/` 디렉터리와 `PROJECT_INDEX.md` 존재 확인 | ✅ |
| 2 | Retrieval/Validation 검증 — 실제 Vault 전체에서 `find_broken_backlinks()`가 알려진 프롬프트 예시 텍스트 외 새 문제가 없는지 확인 | ✅ |
| 3 | Auto Save 검증 — 실제 Vault 트리 복사본 위에서 `run_auto_save()` 저장→검증 왕복 성공 확인, 실제 Vault는 건드리지 않음을 함께 확인 | ✅ |
| 4 | 검증 과정에서 발견한 실제 문제가 있으면 수정 | ✅ (아래 참고) |
| 5 | MCP 연동 범위 확인 — M23-Prep-T08 Optional 이월 결정 유지, 이번 범위 아님을 명시 | ✅ |
| 6 | GitHub Repository 연동 확인 — M23-T01~T07 매 Task 커밋·푸시 성공 이력으로 확인 | ✅ |
| 7 | `tests/integration/test_m23_vault_environment_integration.py` 신규 3개 | ✅ |
| 8 | `ruff`/`mypy`/`pytest tests/vault tests/integration/test_m23_vault_environment_integration.py` 클린 | ✅ |
| 9 | `docs/ARCHITECTURE.md`/Vault `Vault Integration Architecture.md`에 Milestone 23 전체 완료 반영 | ✅ |
| 10 | 변경된 파일만 수정 | ✅ |

**구현 내용**

- `tests/integration/test_m23_vault_environment_integration.py`
  (신규, 3개): `test_vault_root_exists_and_is_readable`(Filesystem
  접근), `test_real_vault_has_no_unexpected_broken_backlinks`(실제
  Vault 전체 Backlink 검증, `AI_RULES`/`PROMPT_PROFILE`/
  `READING_PROFILES`/`Vault Integration Architecture`가 문법
  설명용으로 쓰는 `[[이중 대괄호]]`/`[[링크]]`/`[[문서 제목]]`/
  `[[..]]`만 알려진 오탐으로 허용), `test_auto_save_round_trip_
  against_copy_of_real_vault`(실제 `Vault/`를 `tmp_path`로 복사한
  뒤 `run_auto_save()`로 ADR 항목을 저장해 실제 `ADR Index.md`
  구조 위에서 왕복이 되는지 확인, 원본 Vault는 변경되지 않음을
  검증).
- **실제 버그 발견 및 수정**: 검증 테스트를 작성하며 `find_broken_
  backlinks()`를 실제 Vault에 처음 돌려본 결과, `[[Vault Integration
  Architecture]]`(M23-T06에서 이번 세션이 직접 도입, `EXECUTION_
  PROFILE.md`)와 `[[Architecture Overview]]`(`Backend Index.md`,
  M23-Preparation 시점부터 있던 훨씬 이전 문제)가 줄바꿈 때문에
  `[[Vault Integration\nArchitecture]]`/`[[Architecture\n
  Overview]]`로 깨져 있던 것을 발견해 둘 다 링크가 줄 안에서
  끊기지 않도록 고쳤다. Validation 계층이 실제로 문제를 잡아낸
  첫 사례.
- MCP: Obsidian MCP를 통한 실시간 Vault 연동은 M23-Prep-T08
  (Optional)에서 이미 "Claude Code 도입 시점으로 이월"로 결정됐고,
  이번 Task 범위에서 다시 검토하지 않는다(재확인만).
- `docs/ARCHITECTURE.md`(v0.30.0)/Vault `Vault Integration
  Architecture.md`(수정): "Milestone 23(Obsidian Integration &
  Auto Save) 전체 완료(T01~T07)" 선언.
- 검증: `poetry run ruff check tests/integration/test_m23_vault_
  environment_integration.py` / `poetry run mypy src/ai_workspace/
  vault` / `poetry run pytest tests/vault tests/integration/
  test_m23_vault_environment_integration.py` 전부 통과(41개, 기존
  38 + 신규 3). 전체 `pytest`는 여전히 M23-T03부터 기록해 온
  사전 존재 환경 제약(`pyyaml`/`fastapi`/`uvicorn` 미설치)으로
  다른 모듈에서 실패 — `vault/`와 무관.

**의존성**: M23-T03~T06 전부 완료.

---

## Milestone 23 Verification — Obsidian Integration & Auto Save Validation

**목적**: M23(T01~T07)가 실제로 목표(Obsidian Integration & Auto
Save 기반 완성)를 달성했는지 구현 코드/테스트/문서를 기준으로
검증한다(사용자 요청, 2026-07-27). 실제 Vault에 쓰기는 하지 않고
Mock(`tmp_path`)과 기존 코드 검토로만 확인했다. 새 기능은
구현하지 않고 설계 대비 누락만 확인한다.

### 1. Architecture Validation

| 항목 | 결과 | 근거 |
|---|---|---|
| Obsidian Integration Architecture 존재 | ✅ | `Vault/.../02 Architecture/Vault Integration Architecture.md`(M23-T02) |
| Vault 구조 정의 완료 | ✅ | ADR-0035 결정 2(Vault Directory Mapping) + `vault/mapping.py`의 `VAULT_DIRECTORY_MAP`(12종) |
| Save Workflow 정의 완료 | ✅ | ADR-0035 결정 3(4단계 Save Flow) + `vault/engine.py`의 `VaultSaveEngine.save()` |
| Document Routing 정의 완료 | ✅ | `vault/router.py`의 `DocumentRouter.resolve()` |
| Retrieval Workflow와 충돌 없음 | ✅ | `EXECUTION_PROFILE` 2단계(Context Retrieval)는 [[READING_PROFILES]]만 참조하고, Vault 저장은 5~6단계(Document Update/Validation)에서만 개입 — 단계가 겹치지 않음 |
| Architecture 문서 최신화 | ✅ | `docs/ARCHITECTURE.md` v0.30.0 §3.21, 헤더 상태 줄이 M23-T01~T07 전체 완료를 반영 |

### 2. Save Engine Validation

| 항목 | 결과 | 근거 |
|---|---|---|
| Markdown Generator 구현 | ✅ | `vault/markdown_generator.py`(`render_section`/`render_daily_file`) |
| Vault Save Engine 구현 | ✅ | `vault/engine.py`(`VaultSaveEngine`) |
| Document Router 구현 | ✅ | `vault/router.py`(`DocumentRouter`) |
| Template 적용 구조 구현 | ⚠️ 부분 | ADR/Decision 2종은 실제 Vault 관행(목적/결정/영향, Status/질문/답)에 맞춰 전용 렌더링을 구현했지만, 나머지 10종(backend/api/dashboard/automation/production/ios/android/milestone/architecture)은 "제목+요약" 공통 Summary 형식 하나로 처리한다(`markdown_generator.py` 주석의 명시적 YAGNI 판단). 아래 "발견된 누락 사항" 참고 |
| Metadata 처리 구현 | ✅ | `vault/validation.py`의 `find_missing_tags()` — append 모드는 기존 frontmatter를 건드리지 않고, create 모드(Daily)만 `tags: [daily]`를 직접 채워 넣는다(코드로 확인) |
| 파일 생성 로직 존재 | ✅ | `vault/writer.py`의 `VaultWriter.create_file()` |
| 파일 수정 로직 존재 | ✅ | `vault/writer.py`의 `VaultWriter.upsert_section()` |

### 3. Auto Save Workflow Validation

```
Task 완료 → 자동 저장 요청 → 대상 문서 결정 → Markdown 생성 → Save Engine 호출 → 저장 결과 반환
```

| 단계 | 대응 코드 | 결과 |
|---|---|---|
| 자동 저장 요청 | `vault/auto_save.py`의 `run_auto_save(vault_root, requests)` | ✅ |
| 대상 문서 결정 | 내부에서 `DocumentRouter.resolve()` 호출 | ✅ |
| Markdown 생성 | 내부에서 `VaultSaveEngine.save()` → `render_section()`/`render_daily_file()` | ✅ |
| Save Engine 호출 | `VaultSaveEngine.save()` → `VaultWriter` | ✅ |
| 저장 결과 반환 | `AutoSaveReport`(saved/unchanged/validation_issues + `ok`/`summary()`) | ✅ |

전체 파이프라인 자체는 구현·테스트(`tests/vault/test_auto_save.py`
4개)로 확인됨. **다만 "Task 완료 시"라는 트리거는 시스템이 자동
으로 호출하는 것이 아니라, AI가 `EXECUTION_PROFILE` 5단계를 따라
그때그때 수동으로 `run_auto_save()`를 호출하는 구조다** — `src/
ai_workspace/` 전체에서 `run_auto_save`/`VaultSaveEngine`을
호출하는 곳이 `vault/` 패키지 자신 외에는 없음을 확인했다
(`grep -rn "run_auto_save\|VaultSaveEngine" src/ai_workspace/`
결과 `vault/` 외 0건). M23-T06 write-up에서 이미 "자연어 해석은
AI 역할이라 결정적 트리거를 코드로 만들지 않았다"고 명시했던
설계 그대로이며, 새로운 문제는 아니지만 "완전 자동"으로 오해하지
않도록 이 검증에서 다시 명확히 기록한다.

### 4. Execution Engine Validation

`EXECUTION_PROFILE`의 "지원 명령 예시" 표에 요청된 7개 명령이
전부 등재돼 있다.

| 명령 | 표에 존재 | PROJECT_INDEX→READING_PROFILES→Retrieval→Template→Execution 연결 |
|---|---|---|
| 다음 Task 진행 | ✅ | ✅ (해당 Task 내용에 따라 Reading Profile 결정 → 그 Profile의 Retrieval/Template 순서를 그대로 따름) |
| 다음 작업 진행 | ✅ (동일 행) | ✅ |
| M23-T03 진행 | ✅ ("M23-T05 진행" 예시로 일반화된 패턴) | ✅ |
| ADR 작성 | ✅ | ✅ (READING_PROFILES "ADR 작성" → ADR_TEMPLATE) |
| Feature Design | ✅ | ✅ (READING_PROFILES "Feature Design" → DESIGN_TEMPLATE) |
| API 설계 | ✅ ("API 설계" 행) | ✅ (READING_PROFILES "API Design" → API_TEMPLATE) |
| Bug Fix | ✅ | ✅ (READING_PROFILES "Bug Fix" → TASK_TEMPLATE 경량 DoD) |

연결은 표 하나로 명시적으로 그려져 있지 않고, "지원 명령 예시"
표(명령→Reading Profile)와 [[READING_PROFILES]] 각 Profile의
"쓸 Template"이 서로 연결되는 방식(간접 참조)이다 — 동작은
가능하지만 명령별로 Template까지 한 표에 나열되어 있지는 않다.

### 5. Routing Validation

Reading Profile → Template → 저장 대상 3단 연결을 kind별로
대조했다.

| kind | Reading Profile "쓸 Template" | `vault/mapping.py` 저장 대상 | 일치 여부 |
|---|---|---|---|
| ADR | ADR_TEMPLATE(원문) / Template - ADR Summary(Vault) | `03 ADR/ADR Index.md` | ✅ (단, 실제 렌더링은 Template - ADR Summary의 원문 구조(H2 하위 절)가 아니라 ADR Index의 실제 관행(불릿 3줄)을 따름 — 의도된 선택, 아래 참고) |
| Decision | DECISION_TEMPLATE / Template - Decision | `12 Decisions/Decisions Index.md` | ✅ (동일한 "실제 관행 우선" 선택) |
| Daily | Template - Daily | `13 Daily/{date}.md` | ✅ (구조 그대로 일치) |
| Milestone | Template - Milestone | `11 Milestones/Milestones Index.md` | ⚠️ Milestones Index는 표(Milestone별 1행) 구조인데 generic 렌더러는 "## 제목" 절을 추가한다 — 파일 자체 규칙과 형식이 어긋남 |
| Backend/API/Dashboard/Automation/Production/iOS/Android/Architecture | 각 Profile의 Template | 각 Index/Design 문서 | ⚠️ 동일 사유 — 대상 문서 8종 전부 "주제별 절"(iOS Design/Automation Index 등) 또는 "표"(Backend Index) 구조인데, generic 렌더러는 "## 제목 + 요약" 절을 그 앞에 끼워 넣는다. 저장 **위치**(파일)는 항상 맞지만, 저장 **형식**이 그 문서의 기존 관행과 다를 수 있다 |

**결론**: 저장 대상(파일) 라우팅은 12종 전부 설계대로 정확하다.
저장 **내용 형식**은 ADR/Decision/Daily 3종만 대상 문서의 실제
관행과 검증됐고, 나머지 9종은 기계적으로는 동작하지만(파일이
깨지지는 않음) 대상 문서의 기존 구조(표/주제별 절)와 다른
형식으로 삽입된다 — Template 적용 구조의 "부분 구현"과 같은
근본 원인.

### 6. Mock Save Validation

실제 Vault가 아니라 `tmp_path`(pytest fixture, Fake Filesystem)에서
전부 확인했다 — 실제 Vault는 이번 검증에서 전혀 수정하지 않았다
(`git status` 결과 이 절 작성 전까지 변경 없음).

| 동작 | 결과 | 테스트 |
|---|---|---|
| Create | ✅ | `test_writer.py::test_create_file_writes_new_file`, `test_create_file_does_not_overwrite_existing` |
| Update | ✅ | `test_writer.py::test_upsert_section_*`(삽입/교체/no-op/fallback 4종) |
| Rename | ✅ | `test_sync.py::test_rename_document_renames_file_and_updates_backlinks` 등 4종 |
| Delete | ✅ | `test_sync.py::test_delete_document_*` 4종(참조 중 거부/강제 삭제/무참조 삭제/원본 없음) |

4개 동작 모두 Mock 환경에서 정상 수행 확인(`pytest tests/vault`
38개 전부 통과).

### 7. Synchronization Validation

| 항목 | 결과 | 근거 |
|---|---|---|
| 중복 저장 방지 | ✅ | `upsert_section()`이 같은 heading이면 교체(중복 절 생성 없음), 내용 동일 시 파일 미기록(`test_upsert_section_is_noop_when_content_unchanged`) |
| 문서 경로 유지 | ✅ | append/create 어느 쪽도 대상 외 문서의 경로를 바꾸지 않음(코드상 단일 `path` 인자만 다룸) |
| Metadata 유지 | ✅ | append 모드는 frontmatter를 전혀 읽지도 쓰지도 않음(코드 확인 — `upsert_section`은 본문 라인만 다룸) |
| 링크 구조 유지 | ✅ | 대상 섹션 경계 밖 텍스트는 그대로 보존(`test_upsert_section_inserts_before_related_docs_heading`이 기존 절 보존을 함께 검증) |
| Backlink 영향 없음 | ⚠️ 부분 | Create/Update/일반 Delete는 다른 문서의 Backlink를 건드리지 않음(설계대로). 단, `delete_document(force=True)`로 참조 중인 문서를 강제 삭제하면 다른 문서에 남은 `[[제목]]` Backlink는 자동으로 정리되지 않는다(다음 `find_broken_backlinks()` 실행에서만 뒤늦게 발견됨) — Rename은 반대로 의도적으로 Backlink를 갱신한다(설계대로, 영향 있음이 정상) |
| 이름 변경 정책 정상 | ✅ | 별칭(`\|`)/절(`#`) 포함 링크까지 갱신 확인(`test_rename_document_renames_file_and_updates_backlinks`), 대상 이름 충돌/원본 없음 예외 처리 확인 |

### 8. Documentation Validation

| 항목 | 결과 | 근거 |
|---|---|---|
| ADR-0035가 `.ai/DECISIONS.md`에 기록됨 | ✅ | ADR-0035(M23-T02) |
| `docs/ARCHITECTURE.md` §3.21이 T01~T07 전체를 반영 | ✅ | v0.30.0 |
| `docs/ROADMAP.md`가 Milestone 23 완료를 반영 | ✅ | v0.31.0 |
| `.ai/TASKS.md`에 T01~T07 write-up 전부 존재 | ✅ | 이 절 바로 위 |
| `.ai/MEMORY.md`에 M23 전체 요약 존재 | ✅ | M23-T01~T07 항목 |
| Vault `PROJECT_INDEX`/`EXECUTION_PROFILE`/`READING_PROFILES`가 서로 backlink로 연결 | ✅ | 상호 "관련 문서" 절에 반영됨 |
| Vault 전체 Backlink 무결성 | ⚠️ 참고 | `tests/integration/test_m23_vault_environment_integration.py`가 실제 Vault를 대상으로 상시 검증 중(알려진 프롬프트 예시 텍스트 8건 제외 신규 문제 0건) |

### 발견된 누락 사항(Gaps) — 요약

1. **Template 적용이 12종 중 2종(ADR/Decision)만 대상 문서의 실제
   관행과 검증됨**. 나머지 10종은 "제목+요약" 공통 형식이라
   Milestones Index/Backend Index(표 구조), Dashboard/Automation/
   Production Index/iOS Design(주제별 절 구조)에 저장하면 기존
   문서 관행과 형식이 어긋난다. `markdown_generator.py`에 이미
   YAGNI로 문서화된 의도적 범위 축소이지만, "Template 적용 구조
   완성"이라고 부르기엔 이르다.
2. **Auto Save는 "자동 트리거"가 아니라 "AI가 수동으로 호출하는
   함수"** 다. `src/ai_workspace/` 어디에도 Task 완료를 감지해
   `run_auto_save()`를 자동 호출하는 코드가 없다(M23-T06에서
   의도적으로 코드화하지 않기로 한 결정과 일치하지만, "Auto Save
   Workflow"라는 이름과 실제 자동화 수준 사이에 기대치 차이가
   있을 수 있어 명시적으로 기록).
3. **`delete_document(force=True)` 이후 Backlink 정리 없음** —
   강제 삭제로 생긴 Orphan Backlink는 다음 Validation 실행 전까지
   감지되지 않는다.

이 세 가지는 모두 설계 문서/코드 주석에 이미 명시된 의도적 범위
제한(YAGNI)이거나 M23-T06에서 이미 인지된 사항이며, 이번 검증은
그 사실을 실제 코드/테스트 기준으로 재확인하고 한 곳에 모아
기록한 것이다. **새 코드는 작성하지 않았다**(사용자 지시).

### 종합 결론

Milestone 23이 목표한 "Obsidian Integration & Auto Save 기반"은
**핵심 파이프라인(Routing/Save/Validation/Sync/Conflict Handling)
기준으로 완성**됐고 Mock 환경에서 38개 + 실제 Vault 대상 통합
테스트 3개 전부 통과한다. 다만 (1) Template 형식 적용은 ADR/
Decision 2종만 실전 검증됐고 나머지는 아직 범용 형식이라는 점,
(2) "자동" 저장은 실제로는 AI가 절차를 따라 호출하는 수동 트리거
라는 점은 M23을 "완전 자동화"로 오해하지 않기 위해 명확히 남겨
둔다. 코드 변경/실제 Vault 변경 없음.

---

## M23-Final — Verification 결과 반영 및 Milestone 23 Completed 선언

**사용자 결정(2026-07-27)**: Verification에서 표시된 ⚠️ 3건
(Template 형식 적용 범위/Auto Save 수동 호출 구조/강제 삭제 후
Orphan Backlink 미정리)은 전부 기존 설계(YAGNI)에 따른 의도된
동작이며 새 결함이 아니다 — **M23의 범위를 확장하지 않는다.**
이 절은 그 결정에 따라 문서만 최종 정리한다. 구현/리팩터링 없음.

### M23 DoD 최종 확인

Milestone 23 kickoff 시점의 목표·원칙(위 "목표"/"기본 원칙" 절)을
기준으로 최종 확인한다.

| # | DoD 항목(Milestone 23 목표) | 상태 |
|---|---|---|
| 1 | AI Workspace(GitHub)와 Obsidian Vault를 통합한다 | ✅ `vault/`(M23-T03~T05) + Vault Integration Architecture(M23-T02) |
| 2 | Retrieval First Workflow를 유지하면서 Markdown 문서를 자동 생성·저장·갱신하는 구조를 구현한다 | ✅ Markdown Generator/Vault Writer/Auto Save Workflow(M23-T03~T04), 단 "자동"은 AI가 절차를 따라 호출하는 구조(Verification 기록, 의도된 동작) |
| 3 | 사용자가 짧은 명령만 입력해도 AI가 Retrieval → 작업 → Vault 저장까지 수행할 수 있는 기반을 마련한다 | ✅ Execution Engine 절(M23-T06) + READING_PROFILES + `run_auto_save()` |
| 4 | 기본 원칙 8개(Retrieval First/Minimum Retrieval/Template First/Short Prompt Workflow/Standard Execution Workflow/기존 구조 유지/변경된 파일만 수정/Obsidian Vault 기준 설계) 준수 | ✅ 전 Task write-up과 Verification에서 확인, 위반 없음 |
| 5 | Task List(T01~T07) 전부 완료 | ✅ 위 Task List 표 |
| 6 | Verification으로 설계 대비 누락 확인 | ✅ Milestone 23 Verification 절(⚠️ 3건, 전부 의도된 동작으로 확정) |

**M23 DoD 전 항목 충족. 신규 결함 없음(사용자 확정).**

### Milestone 23 상태

**Milestone 23(Obsidian Integration & Auto Save) — Completed.**
(2026-07-27, 사용자 승인) 다음 Milestone은 미정 — 원 M23이 다루던
Mobile Experience 이월분([[Decisions Index]]/[[PREPARATION_SUMMARY]]
의 Start Criteria 3개 결정 보존) 또는 사용자가 지정하는 새 작업
중 착수 시점에 결정한다.

---

## Milestone 24 — Real Obsidian Vault Integration

**목표**(2026-07-27 사용자 요청): M23이 구축한 Obsidian Integration
Foundation을 기반으로, Mock/`tmp_path`가 아닌 **실제 Obsidian
Vault**(`Vault/01 Projects/AI Workspace`)를 대상으로 Markdown 문서를
생성·수정·삭제할 수 있도록 구현한다. "다음 Task 진행" 같은 짧은
명령이 PROJECT_INDEX → READING_PROFILES → Retrieval → Task 수행 →
Markdown 생성 → 실제 Vault 저장 → Validation → 완료 보고까지 하나의
Workflow로 동작하는 것이 최종 목표.

**기본 원칙**: Retrieval First / Minimum Retrieval / Template
First / Short Prompt Workflow / Standard Execution Workflow /
기존 Architecture 유지 / Mock 구현 제거 금지 / Mock와 실제 구현
분리 / 변경 최소화 / 기존 테스트 유지 / 실제 Vault를 기준으로
설계.

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M24-T01 | Real Vault Connection — Vault Root 설정/Configuration/Path Resolver/Permission Validation/존재 확인/연결 실패 예외 처리 | **완료** |
| M24-T02 | Filesystem Adapter — 실제 Vault Create/Read/Update/Delete/Exists/Rename/Move | **완료** |
| M24-T03 | Real Markdown Writer — UTF-8/Frontmatter 유지/Directory 자동 생성/파일명 충돌 처리/Metadata 유지/Atomic Write | **완료** |
| M24-T04 | Template Integration — Template 기반 Markdown을 실제 Vault 문서로 생성 | **완료(범위 축소, 아래 참고)** |
| M24-T05 | Real Auto Save — Task 완료 시 실제 Vault 자동 저장 | **완료** |
| M24-T06 | Execution Integration — 짧은 명령을 실제 실행으로 연결 | **완료** |
| M24-T07 | Real Vault Synchronization — Create/Update/Rename/Delete/Link·Backlink Validation/Conflict Detection/Incremental Sync | **완료** |
| M24-T08 | End-to-End Integration Test — 실제 Obsidian Vault 대상 통합 테스트 | **완료** |

### M24-T01~T03: Real Vault Connection / Filesystem Adapter / Real Markdown Writer

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `vault/connection.py` — `resolve_default_vault_root()`(상위 경로 탐색), `connect()`(존재/디렉터리/쓰기 권한 검증) | ✅ |
| 2 | 연결 실패 시 `VaultConnectionError`(경로 없음/디렉터리 아님/쓰기 권한 없음 3종 메시지) | ✅ |
| 3 | `vault/filesystem.py` — `VaultFileSystem`(Create/Read/Update/Delete/Exists/Rename/Move 7종) | ✅ |
| 4 | 기존 Mock(`tmp_path`) 기반 `tests/vault/` 제거하지 않고 그대로 유지 | ✅ |
| 5 | `vault/atomic.py` — `atomic_write_text()`(임시 파일 + `os.replace()`) | ✅ |
| 6 | `VaultWriter.create_file()`/`upsert_section()`이 내부적으로 Atomic Write 사용, 공개 동작(반환값) 불변 | ✅ |
| 7 | UTF-8/Frontmatter 유지/Directory 자동 생성/파일명 충돌 처리(기존 파일 미덮어씀)/Metadata 유지 — 전부 M23에서 이미 구현된 것을 재확인 | ✅ |
| 8 | `ruff`/`mypy`/`pytest tests/vault`(38개, 무변경) 통과 | ✅ |

**구현 내용**: `src/ai_workspace/vault/connection.py`(신규),
`filesystem.py`(신규), `atomic.py`(신규) — 상세 설계 근거는 ADR-0036
참고. `writer.py`는 `path.write_text()` 2곳을 `atomic_write_text()`
로 교체한 것 외에는 변경 없음(공개 API·반환값 동일, 기존 테스트
전부 무변경 통과로 확인).

### M24-T04: Template Integration(범위 축소)

**목표**: 모든 산출물 종류를 실제 Vault 문서로 생성 가능하게 한다.

**실제 결정**: 사용자가 예시로 든 kind 목록(ADR/API/Decision/
Design/Documentation/Feature/Implementation/Memory/Roadmap/Task)
중 **ADR/API/Decision은 이미 M23의 `VaultDocumentKind`에 존재**
한다. 나머지(Design/Documentation/Feature/Implementation/Memory/
Roadmap/Task)는 실제 Vault(PARA 구조, M23-Preparation에서 확정)에
대응하는 전용 디렉터리가 없다 — Roadmap은 개념적으로 [[Milestones
Index]](kind=milestone)로 이미 대응되고, Memory/Task는 GitHub
`.ai/MEMORY.md`/`.ai/TASKS.md` 원문이라 ADR-0035부터 지켜 온
"GitHub 원문을 `vault/`가 대신 쓰지 않는다"는 경계 밖이다. 새
Vault 폴더를 이번 Task 하나로 임의로 만들면 "기존 Architecture
유지"/"실제 Vault를 기준으로 설계" 원칙과 충돌한다고 판단해
**kind를 추가하지 않았다**(ADR-0036에 대안으로 기각 사유 기록).
대신 기존 12종 kind가 실제 Vault 위에서 정말 동작하는지를
M24-T08에서 실제로 검증했다(ADR/Daily 2종을 실제 파일로 왕복).

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 기존 12종 kind와 실제 Vault 대응 여부 재확인 | ✅ |
| 2 | 범위를 넓히지 않기로 한 결정과 근거를 ADR-0036에 기록 | ✅ |
| 3 | 실제 Vault 대상 왕복 테스트(M24-T08)로 최소 2종(ADR/Daily) 실증 | ✅ |

### M24-T05: Real Auto Save

**목표**: Task 완료 시 실제 Vault에 자동 저장되는 Workflow를
완성한다(Task 완료 → Markdown 생성 → Validation → Vault 저장 →
결과 보고).

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `run_auto_save()`가 실제 Vault 경로에 대해서도 그대로 동작 확인 | ✅ (M24-T08 실측) |
| 2 | `run_auto_save_on_default_vault()`(신규) — `vault_root` 생략 시 `connection.connect()`로 실제 Vault 자동 연결 | ✅ |
| 3 | Validation을 Incremental로 전환(저장한 파일만 검사) — 이번 저장과 무관한 기존 문제로 실패하지 않음 | ✅ |
| 4 | `find_broken_backlinks()`에 `only_paths` 추가, 생략 시 기존과 동일한 전체 스캔(하위 호환) | ✅ |
| 5 | 자동 저장 대상: ADR/Decision/Backend/API/Dashboard/Automation/Production/iOS/Android/Milestone/Daily/Architecture(Vault 12종). TASKS/MEMORY/ROADMAP(GitHub 원문)은 범위 밖(ADR-0035/0036 경계 유지) | ✅ |
| 6 | 기존 Auto Save 테스트(`tests/vault/test_auto_save.py` 4개) 무변경 통과 | ✅ |

### M24-T06: Execution Integration

**목표**: "다음 Task 진행"/"M24-Txx 진행"/"ADR 작성"/"API 설계"/
"Feature Design"/"Bug Fix" 같은 짧은 명령이 PROJECT_INDEX →
READING_PROFILES → Retrieval → Task → Markdown 생성 → **실제 Vault
저장** → Validation → 완료 보고로 이어지도록 연결한다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | M23-T06에서 정의한 Execution Engine 절차([[EXECUTION_PROFILE]])가 M24 이후에도 그대로 유효한지 확인 | ✅ |
| 2 | 5단계(Document Update)가 가리키는 `run_auto_save()`를 실제 Vault에도 호출 가능하게(`run_auto_save_on_default_vault()`) 갱신 | ✅ |
| 3 | 지원 명령 표에 "M24-Txx 진행" 패턴이 기존 "M23-T05 진행" 예시로 이미 일반화돼 있음을 재확인(신규 항목 추가 불필요) | ✅ |

**구현 내용**: `EXECUTION_PROFILE.md`는 M23-T06에서 이미 kind에
무관한 절차로 작성돼 있어 구조 변경이 필요하지 않았다. 5단계
설명에 `run_auto_save_on_default_vault()`가 실제 Vault로 자동
연결됨을 반영(아래 Vault 문서 갱신 참고).

### M24-T07: Real Vault Synchronization

**목표**: Create/Update/Rename/Delete/Link·Backlink Validation/
Conflict Detection/Incremental Sync가 실제 Vault 위에서 전부
동작하는지 확인한다.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Create/Update/Delete가 실제 Vault에서 동작(M24-T08 실측) | ✅ |
| 2 | Rename이 실제 Vault에서 파일명 변경 + Backlink(별칭/절 포함) 일괄 갱신(M24-T08 실측) | ✅ |
| 3 | Link/Backlink Validation — `find_broken_backlinks()` 재사용 | ✅ |
| 4 | Conflict Detection — `content_hash()`+`expected_hash`(M23-T05) 유지, 신규 변경 없음 | ✅ |
| 5 | Incremental Sync — `only_paths`로 검사 범위를 좁히는 기능 신규 구현(M24-T05와 공유) | ✅ |

### M24-T08: End-to-End Integration Test

**목표**: Mock가 아닌 실제 Obsidian Vault를 대상으로 문서 생성/
수정/삭제/Rename/Link 유지/Backlink 유지/Template 적용/Auto
Save/Retrieval 결과 저장/Validation을 통합 테스트로 검증한다.
`tmp_path`만 쓰는 테스트는 이 Task의 완료 기준으로 인정하지
않는다(사용자 명시).

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `tests/integration/test_m24_real_vault_e2e.py` 신규 — `tmp_path` 미사용 | ✅ |
| 2 | 실제 Vault 연결(`connect`) + 미존재 경로 예외 처리 테스트 | ✅ |
| 3 | 실제 Vault 위에서 Create→Update→Rename→Delete 왕복(Backlink 별칭/절 포함 갱신 확인) | ✅ |
| 4 | 실제 `ADR Index.md`(기존 문서)에 `run_auto_save()`로 저장 후 `finally`로 원본 완전 복원 | ✅ |
| 5 | 테스트가 만든 파일은 전부 스스로 정리(존재할 수 없는 미래 날짜 제목 사용) | ✅ |
| 6 | 테스트 종료 후 `git status`/`git diff`로 실제 Vault 무변경 확인 | ✅ |
| 7 | 기존 문서에 대한 삭제/Rename은 수행하지 않음(사용자 명시 제약 준수 — 전부 테스트가 스스로 만든 문서만 대상) | ✅ |
| 8 | `ruff`/`mypy`/`pytest`(5개) 통과 | ✅ |

**구현 내용**: 위 "변경된 파일" 참고. `test_connect_to_real_vault`/
`test_resolve_default_vault_root_finds_real_vault`/
`test_connect_rejects_nonexistent_path`(연결)·
`test_real_vault_create_update_rename_delete_round_trip`(CRUD+Rename
+Backlink)·`test_run_auto_save_writes_to_real_adr_index_and_restores_it`
(Auto Save, 임시 반영 후 원상복구) 5개.

### 검증 요약(M24 전체)

- `poetry run ruff check src/ai_workspace/vault tests/vault
  tests/integration/test_m23_vault_environment_integration.py
  tests/integration/test_m24_real_vault_e2e.py` — 통과.
- `poetry run mypy src/ai_workspace/vault` — 통과.
- `poetry run pytest tests/vault tests/integration/
  test_m23_vault_environment_integration.py tests/integration/
  test_m24_real_vault_e2e.py` — **46개 전부 통과**(Mock/`tmp_path`
  38개 + M23-T07 실제 Vault 3개 + M24-T08 실제 Vault 5개).
- 실제 Vault(`Vault/`) 대상 테스트 실행 전후 `git status`/`git diff`
  로 무변경 확인(테스트가 만든 파일은 자체 정리, 기존 `ADR
  Index.md`는 `finally`로 원본 그대로 복원).
- 전체 `pytest`/`mypy src`는 M23부터 기록해 온 사전 존재 환경
  제약(`pyyaml`/`fastapi`/`uvicorn` 미설치)으로 다른 모듈에서 여전히
  실패 — `vault/`와 무관.

**의존성**: Milestone 23(Obsidian Integration & Auto Save) 전체
완료.

**Milestone 24(Real Obsidian Vault Integration) — Completed.**
(2026-07-27, 사용자 승인)

---

## Milestone 25 — Production Vault Activation

**목표**(2026-07-27 사용자 요청): M24에서 구현한 Real Obsidian
Vault Integration을 실제 운영 환경(Production Vault)에서
활성화한다. 구현 자체는 변경하지 않고 (1) 권한 확인 → (2) 안전성
검증 → (3) 실제 Vault 동기화 순으로 진행한다.

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M25-T01 | Vault Permission Verification — Root/Read/Write/Create/Update/Delete/Rename 권한 + Configuration 확인 | **완료** |
| M25-T02 | Production Safety Test — TEST_DOCUMENT.md 생성→수정→저장 확인→삭제, Vault 원상복구 | **완료** |
| M25-T03 | Production Vault Synchronization — 실제 프로젝트 문서와 Vault 동기화 상태 확인·보정 | **완료** |
| M25-T04 | Production Verification — 실제 Vault 반영 결과(링크/Backlink/Frontmatter/Template/중복/누락) 검증 | **완료** |
| M25-T05 | Production Completion — 결과 요약, 운영 준비 여부 확정 | **완료** |

### M25-T01: Vault Permission Verification

**목표**: 실제 Obsidian Vault 접근 가능 여부를 문서 생성 없이
확인한다. 실패 시 원인만 보고하고 아무것도 만들지 않는다.

**검증 방법**: `vault.connection.resolve_default_vault_root()`/
`connect()`(존재/디렉터리/쓰기 권한)를 실제로 호출하고, 나머지
권한(Read/Create/Update/Delete/Rename)은 `os.access()`로 순수
읽기 전용 확인만 수행(파일을 만들지 않음).

**결과**

| # | 항목 | 결과 |
|---|---|---|
| 1 | Vault Root 확인(`resolve_default_vault_root`) | ✅ `Vault/01 Projects/AI Workspace` |
| 2 | `connect()` — 존재/디렉터리/쓰기 권한 | ✅ |
| 3 | Read 권한(R_OK, root) | ✅ |
| 4 | Write 권한(W_OK, root) | ✅ |
| 5 | Create/Delete/Rename 권한(디렉터리 W_OK+X_OK, `03 ADR/` 표본) | ✅ |
| 6 | Update 권한(기존 파일 `PROJECT_INDEX.md`의 W_OK) | ✅ |
| 7 | Configuration 확인(PARA 구조 15개 디렉터리 전부 존재) | ✅ |

**모든 권한 확인 통과 — 문서는 생성하지 않음(순수 읽기 전용
검증).**

### M25-T02: Production Safety Test

**목표**: 실제 Vault에서 Create/Update/Delete가 안전하게 동작하는지
실제로 확인하고, 종료 후 Vault를 원래 상태로 되돌린다.

**절차 및 결과**: `VaultFileSystem`/`VaultWriter`로 실제 Vault
루트에 `TEST_DOCUMENT.md`를 생성 → 섹션 추가로 수정 → 저장 내용
읽어 확인 → 삭제까지 전부 실제로 수행했다.

| # | 항목 | 결과 |
|---|---|---|
| 1 | 생성(`VaultFileSystem.create`) | ✅ |
| 2 | 수정(`VaultWriter.upsert_section`) | ✅ |
| 3 | 저장 확인(다시 읽어 내용 대조) | ✅ |
| 4 | Frontmatter(`tags: [system]`) 유지 | ✅ |
| 5 | UTF-8(한글 "가나다라" 보존) | ✅ |
| 6 | Link(`[[Overview]]`) | ✅ (대상 문서 실제 존재) |
| 7 | Backlink Validation(`find_broken_backlinks`) | ✅ 이슈 0건 |
| 8 | Tag Validation(`find_missing_tags`) | ✅ 이슈 0건 |
| 9 | 삭제(`VaultFileSystem.delete`) | ✅ |
| 10 | "Obsidian에서 정상 표시 확인" | ⚠️ 대리 검증 — 이 세션에 Obsidian 앱이 없어 직접 열어 확인할 수 없다. Frontmatter 파싱 가능 여부/Backlink·Tag Validation 통과로 대신 확인했다(정직하게 기록) |
| 11 | 테스트 후 Vault 원상복구 | ✅ `git status`/`git diff -- Vault/` 확인 결과 무변경 |

**Production Safety Test 통과.**

### M25-T03: Production Vault Synchronization

**목표**: 실제 프로젝트 문서(TASKS/MEMORY/ROADMAP/ADR/API/DESIGN/
IMPLEMENTATION/DECISION/DOCUMENTATION)를 실제 Vault와 동기화한다.
M25-T02가 성공했으므로 진행(사용자 제약 조건 충족).

**실제 동기화 범위 확인**: `vault/`는 ADR-0035/0036부터 "GitHub
원문(TASKS/MEMORY/ROADMAP)을 대신 쓰지 않는다"는 경계를 지켜 왔다
— 이번에도 그 경계를 유지했다(범위를 넓히지 않음, M24-T04와 동일
판단). DESIGN/IMPLEMENTATION/DOCUMENTATION은 실제 Vault(PARA
구조)에 대응하는 전용 디렉터리가 없어 동기화 대상에서 제외(동일
판단 근거). 실제로 동기화 가능한 대상(ADR/API/DECISION, 그리고
표 구조 문서인 Backend Index)을 실제 Vault와 대조한 결과:

| 대상 | 상태 |
|---|---|
| ADR Index | ✅ ADR-0035/0036 모두 이미 등록됨(직전 Task에서 반영) |
| API Catalog | ✅ M23~M25에서 신규 REST 엔드포인트 없음 — 동기화 필요 없음 |
| Decisions Index | ✅ 관련 결정("왜 Server와 iOS/Android를 분리했는가") 이미 최신 |
| Backend Index | ⚠️→✅ `vault/` 행이 M23(ADR-0035)까지만 언급하고 M24/ADR-0036 (connection/filesystem/atomic)을 빠뜨리고 있어 **실제로 갱신함**(이번 Task에서 발견·수정한 유일한 실제 Gap) |

**의도적으로 하지 않은 것**: `run_auto_save()`(kind=ADR)로 ADR
Index의 기존 ADR-0035/0036 섹션을 다시 렌더링해 덮어쓰는 것 —
기각. 이미 수작업으로 정확히 작성된 요약을 자동 생성기의 범용
포맷으로 교체하면 내용 품질이 떨어질 위험이 있고, "구현 자체를
변경하는 것이 아니라"는 이번 Milestone의 원칙과도 맞지 않는다
(대상 섹션이 이미 최신이므로 다시 쓸 이유가 없다).

### M25-T04: Production Verification

**목표**: 실제 Vault 반영 결과(문서 위치/링크/Backlink/Frontmatter/
Template/중복/누락)를 확인한다.

**실제 Vault 전체(34개 파일) 대상 검증 결과**

| # | 항목 | 결과 |
|---|---|---|
| 1 | 문서 위치(Vault Directory Mapping과 실제 파일 경로 일치) | ✅ |
| 2 | 링크/Backlink(`find_broken_backlinks(root)` 전체 스캔) | ⚠️ 9건 — 전부 `AI_RULES`/`PREPARATION_SUMMARY`/`PROMPT_PROFILE`/`READING_PROFILES`/`Vault Integration Architecture`가 `[[...]]` 문법을 설명하려고 쓰는 예시 텍스트(기존에 이미 알려진 오탐, 신규 문제 아님) |
| 3 | Frontmatter(전체 34개 파일 `tags` 존재 여부) | ✅ 누락 0건 |
| 4 | Template 일관성(ADR/Decision/Daily는 실제 관행과 일치, 나머지 kind는 M23 Verification에서 이미 기록한 "범용 형식" 한계 유지 — 이번에 새로 악화되지 않음) | ✅ (기존 상태 유지 확인) |
| 5 | 중복 여부(파일 내 `## ` heading 중복 스캔) | ⚠️ `AI_RULES.md`에서 "## 원문"이 2번 발견되나, 하나는 GitHub Link Rule을 설명하는 **코드 펜스(```markdown) 안의 예시**이고 실제 중복 섹션이 아님(수동 확인). `AI_RULES`는 kind=`system`으로 애초에 자동 저장 대상이 아니므로 운영상 영향 없음 — 다만 Vault Writer의 줄 기반 섹션 매칭이 코드 펜스를 인식하지 못한다는 점은 향후 참고용으로 기록 |
| 6 | 누락 여부(15개 PARA 디렉터리 + `PROJECT_INDEX.md` 등 핵심 문서 존재) | ✅ |

**신규 결함 없음 — 전부 이미 알려졌거나(M23 Verification) 운영에
영향이 없는 항목임을 재확인.**

### M25-T05: Production Completion

**목표**: Production 환경 활성화를 완료 선언한다.

**DoD 최종 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Vault 권한 확인 완료 | ✅ |
| 2 | 테스트 문서 생성 성공 | ✅ |
| 3 | 테스트 문서 수정 성공 | ✅ |
| 4 | 테스트 문서 삭제 성공 | ✅ |
| 5 | 테스트 후 Vault 원상복구 | ✅ |
| 6 | 실제 프로젝트 문서 동기화 완료 | ✅ (범위: ADR/API/Decision/Backend Index — TASKS/MEMORY/ROADMAP은 의도적 범위 밖, 위 M25-T03 참고) |
| 7 | 링크 및 Backlink 정상 | ✅ (알려진 예시 텍스트 오탐만 존재, 신규 문제 없음) |
| 8 | Validation 통과 | ✅ |
| 9 | 운영 환경 활성화 완료 | ✅ |

**Task List(M25-T01~T05) 전부 완료. 실제 Obsidian Vault가 M24
구현으로 안전하게 운영 가능한 상태임을 확인했다 — Milestone
25(Production Vault Activation) 자체의 "Completed" 선언은 M23/
M24와 동일하게 사용자의 최종 확인을 거친다.**

**의존성**: Milestone 24(Real Obsidian Vault Integration) 완료.

---

## Merge — Milestone 23~25가 feature branch에만 존재하던 문제 해결

**배경**: 사용자가 로컬 Obsidian 앱에서 Vault가 "1개 파일, 0개
폴더"로 보인다고 보고(2026-07-27). 확인 결과, M23-Preparation
이후의 모든 작업(M23~M25, `.ai/TASKS.md`/`.ai/MEMORY.md`/`docs/
ARCHITECTURE.md`/`docs/ROADMAP.md`/Vault 문서/`src/ai_workspace/
vault/` 전체)이 이 세션의 작업 브랜치 `claude/m23-t01-reading-
profiles-pmnpue`에만 존재했고, **한 번도 PR로 병합된 적이
없었다**(브랜치 자체는 `origin`에 push돼 있었지만 base 브랜치와
분리된 상태). 저장소에 `main`은 없고, 과거 병합된 PR 2건 모두
`claude/ai-workspace-docs-setup-aj3jvo`를 base로 사용해 이 브랜치가
실질적 default임을 확인했다.

**진행**:
1. **비교**: base(`claude/ai-workspace-docs-setup-aj3jvo`)는 이
   브랜치가 갈라진 뒤 커밋이 0개(behind 0) — 43개 파일, +3671/-70줄,
   12커밋의 순수 선형 연장선임을 확인.
2. **충돌 분석**: `git merge-base --is-ancestor`로 fast-forward
   가능 확인, 로컬 dry-run 병합(`git merge --no-commit --no-ff`,
   push 없음)으로 **충돌 0건** 확인.
3. **PR 생성**: [#3](https://github.com/ok041110-del/ai-workspace/pull/3)
   (`claude/m23-t01-reading-profiles-pmnpue` → `claude/ai-workspace-
   docs-setup-aj3jvo`), Merge 안전성 검토와 Test plan을 PR 본문에
   기록.
4. **사용자 승인 후 Merge**: 2026-07-27, `merge` 방식으로 병합
   (커밋 `4882fc4`).
5. **Merge 후 검증**: 병합된 base 브랜치를 다시 checkout해
   `pytest tests/vault tests/integration/test_m23_vault_
   environment_integration.py tests/integration/
   test_m24_real_vault_e2e.py`(46개) 재실행 통과, 실제 Vault
   34개 파일·Backlink(9건, 전부 기존에 알려진 예시 텍스트)·
   Frontmatter(누락 0건) 재확인 — merge 전후 상태 완전히 동일함을
   확인.

**Milestone 23(Obsidian Integration & Auto Save) — Completed.**
**Milestone 24(Real Obsidian Vault Integration) — Completed.**
**Milestone 25(Production Vault Activation) — Completed.**
(2026-07-27, 사용자 승인 + PR #3 Merge 완료로 세 Milestone 모두
최종 확정)

**사용자 조치 필요**: 로컬 Obsidian 앱이 여는 Vault 폴더가 이
저장소의 `claude/ai-workspace-docs-setup-aj3jvo` 브랜치(또는 그
브랜치를 반영하는 로컬 clone)를 가리키고 있는지 확인 필요 — 이
세션은 로컬 파일시스템에 접근할 수 없어 그 경로 자체는 확인할
수 없다.

---

## Milestone 26 — Obsidian Vault Root Refactoring

**목표**(2026-07-27 사용자 요청): Obsidian Vault == Git Repository
Root 구조를 확립해 Git Vault Sync(iOS)/Obsidian Mobile·macOS가
동일한 Vault를 쓸 수 있게 한다. 구현 자체(코드/문서 내용)는 바꾸지
않고 위치만 옮긴다는 최소 변경 원칙을 따른다.

**Task ID 안내**: 사용자가 이 작업을 "M24-T01"로 지칭했으나, 그
ID는 이미 완료된 Milestone 24의 "Real Vault Connection" Task가
쓰고 있어 기존 기록을 덮어쓰지 않기 위해 **Milestone 26,
M26-T01**로 번호를 새로 부여했다(투명하게 기록).

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M26-T01 | Vault Root Refactoring — `Vault/01 Projects/AI Workspace/`를 저장소 root로 승격, 참조 수정, Validation | **완료** |

### M26-T01: Obsidian Vault Root Refactoring

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `Vault/01 Projects/AI Workspace/`의 15개 디렉터리를 `git mv`로 저장소 root에 이동, History 보존(Delete+Create 아님) | ✅ |
| 2 | 비어 있던 `Vault/00 Inbox`/`02 Resources`/`03 Archives`(.gitkeep만) 및 이제 빈 `Vault/`/`Vault/01 Projects/` 제거 | ✅ |
| 3 | `vault/connection.py`를 Vault Root == 저장소 root 기준(표식 파일 탐색)으로 재작성 | ✅ |
| 4 | `vault/mapping.py` 상대 경로는 처음부터 `vault_root` 기준이라 무변경 확인 | ✅ |
| 5 | `vault/validation.py`/`vault/sync.py`의 문서 스캔 범위를 Vault 콘텐츠 15개 디렉터리로 제한(신규 `VAULT_CONTENT_DIRECTORIES`) — `docs/`/`.claude/`/`.agents/` 오염 방지 | ✅ |
| 6 | Wikilink(`[[...]]`)는 파일명 기준이라 이동으로 깨지지 않음을 확인, 마크다운 상대경로 링크 0건 확인 | ✅ |
| 7 | Broken Markdown Link = 0(알려진 프롬프트 예시 텍스트 9건 제외) | ✅ |
| 8 | `tests/vault/`(Mock) fixture를 새 스캔 범위에 맞춰 조정, 전부 통과 | ✅ |
| 9 | `tests/integration/test_m23_vault_environment_integration.py`/`test_m24_real_vault_e2e.py`가 저장소 root를 직접 Vault Root로 사용하도록 갱신 | ✅ |
| 10 | Python Import 오류 없음(사전 존재하는 `pyyaml` 미설치 제약 제외) | ✅ |
| 11 | ADR-0037 작성, `docs/ARCHITECTURE.md`/Vault `Vault Integration Architecture.md`/`ADR Index` 반영 | ✅ |
| 12 | `.obsidian/` 직접 생성하지 않음(Obsidian이 처음 열 때 자동 생성 — 추측성 설정 파일 생성 금지) | ✅ |
| 13 | 변경된 파일만 수정(최소 변경 원칙), 기존 기능 회귀 없음 | ✅ |

**구현 내용**

- **T01-1 Vault Root 승격**: `git mv "Vault/01 Projects/AI
  Workspace/<X>" "<X>"` 15회(00 System~13 Daily, 99 Templates),
  전부 git이 Rename(R)으로 인식(History 보존). `git rm`으로
  `.gitkeep` 3개 제거 후 빈 디렉터리 자동 정리.
- **T01-2 Git History 유지**: `git mv` 전용 — Delete+Create 미사용.
  `git status`가 전 파일을 `R`(Rename)로 표시함으로 확인.
- **T01-3 Repository 참조 수정**: 코드(`src/ai_workspace/vault/
  connection.py` 전면 재작성 — Vault Root 표식 파일(`00 System/
  PROJECT_INDEX.md`) 기준 탐색으로 전환), 테스트(`tests/
  integration/test_m23_vault_environment_integration.py`/
  `test_m24_real_vault_e2e.py`의 `_VAULT_ROOT` 계산과 스캔 방식
  갱신), Vault 문서(`01 Overview/Overview.md`, `00 System/
  PREPARATION_SUMMARY.md`, `02 Architecture/Vault Integration
  Architecture.md`에 M26 구현 상태 절 추가) 갱신. `.ai/TASKS.md`/
  `.ai/DECISIONS.md`/`.ai/MEMORY.md`의 **기존(역사적) 기록은
  그대로 둔다** — 그 시점에는 실제로 `Vault/01 Projects/AI
  Workspace` 경로가 맞았으므로, 소급 수정하면 오히려 진행 로그의
  정확성이 깨진다(대신 이 Task에서 새 기록을 추가해 전환 시점을
  명시). README/`docs/PRD.md`는 Vault 경로를 언급하지 않아 수정
  대상이 아님을 확인.
- **핵심 발견(설계가 이미 준비돼 있었음)**: `vault/mapping.py`의
  대상 경로가 ADR-0035부터 이미 `vault_root` 기준 **상대 경로**
  (`"03 ADR/ADR Index.md"` 등, `"Vault/01 Projects/AI Workspace/..."`
  같은 절대/중첩 경로가 아님)로 설계돼 있어 **한 줄도 바꿀 필요가
  없었다**. Backlink도 전부 Wikilink(파일명 기준)라 위치 이동에
  영향받지 않는다 — 이 두 가지 기존 설계 덕분에 "Vault Root를
  옮긴다"는 근본적인 변경이 실제로는 `connection.py` 1개 파일
  교체로 끝났다.
- **부수적으로 발견해 고친 위험**: `vault_root`가 저장소 root와
  같아지면서, 제한 없는 `rglob("*.md")`가 `docs/`/`.claude/`/
  `.agents/`의 마크다운(특히 `.claude/skills/`/`.agents/skills/`
  아래 서드파티 Skill 문서 수백 개)까지 Backlink/Tag Validation에
  끌어들이는 잠재적 버그를 미리 발견해 `VAULT_CONTENT_DIRECTORIES`
  (신규, `mapping.py`)로 스캔 범위를 명시적으로 제한했다(`validation.
  py`/`sync.py` 수정). 이 문제는 사용자가 요청한 범위 밖이지만
  고치지 않으면 T01-7 Validation 자체가 거짓 결과를 낼 수 있어
  포함했다.
- **T01-4 Obsidian 설정 검증**: `.obsidian/`은 이 세션에 존재하지
  않았고(이동 전에도 없었음) 새로 만들지 않았다 — Obsidian이 저장소
  root를 Vault로 처음 열 때 자동 생성하는 파일이라 미리 만들
  근거가 없다. "Workspace 정상 로드"/"Internal Link 정상"은 실제
  Obsidian 앱을 이 세션에서 실행할 수 없어 직접 확인이 불가능하다
  (정직하게 기록) — 대신 Wikilink Backlink 무결성(코드 기반
  `find_broken_backlinks`)과 폴더 인식 가능 여부(디렉터리 존재
  확인)로 대리 검증했다.
- **T01-5 Git Vault Sync 호환성**: 최종 구조가 저장소 root == Vault
  Root 조건을 만족함을 `vault.connection.connect()`(표식 파일
  기준 탐색)로 실제 재확인.
- **T01-6 Claude Code 영향 분석**: 이 세션(Claude Code) 자체의
  작업 root는 원래도 저장소 root였으므로 영향 없음 — 오히려 Vault
  경로와 처음으로 일치하게 됐다. Workflow(`EXECUTION_PROFILE`)는
  Vault 문서 상대 경로를 참조하지 않고 wikilink/제목 기준이라
  무변경. Automation(`vault/auto_save.py`)은 `run_auto_save_on_
  default_vault()`가 `connection.connect()`를 그대로 재사용해
  무변경. Prompt(`READING_PROFILES`/`PROMPT_PROFILE`)는 문서
  제목만 참조해 무변경. README는 애초에 Vault 경로를 언급하지
  않아 무변경.
- **T01-7 Validation**: 아래 "검증 결과" 참고.

**검증 결과**

- Directory 구조: `00 System`~`13 Daily`, `99 Templates` 15개가
  저장소 root에 존재, `Vault/`는 완전히 사라짐(확인 완료).
- Git Status: 이동된 파일 전부 `R`(Rename)로 표시, 신규 추적
  파일 없음(내용까지 바뀐 파일은 `RM`).
- Git History 유지: `git mv` 전용 사용, `git log --follow`로
  이동 전 이력 접근 가능.
- Broken Markdown Link: 실제 Vault 전체(34개 파일) 스캔 결과 9건
  — 전부 `AI_RULES`/`PREPARATION_SUMMARY`/`PROMPT_PROFILE`/
  `READING_PROFILES`/`Vault Integration Architecture`가 Wikilink
  문법을 설명하는 프롬프트 예시 텍스트(M23 Verification부터
  누적 추적돼 온 알려진 오탐), **신규 broken link 0건**.
  Broken Relative Path: Vault 안 마크다운 스타일 상대경로 링크
  0건(전수 검색 확인) — 애초에 해당 없음.
- Python Import: `pkgutil.walk_packages`로 `ai_workspace` 전체
  모듈을 import해 확인, 실패 1건(`storage.llm_policy_loader`,
  `pyyaml` 미설치)은 M23-T03부터 문서화해 온 사전 존재 환경
  제약이며 이번 변경과 무관.
- Tests: `poetry run ruff check src/ai_workspace/vault tests/vault
  tests/integration/test_m23_vault_environment_integration.py
  tests/integration/test_m24_real_vault_e2e.py` 클린,
  `poetry run mypy src/ai_workspace/vault` 클린, `poetry run pytest`
  (같은 대상) **46개 전부 통과**.

**의존성**: Milestone 25(Production Vault Activation) 완료.

**병합**: PR #4(`claude/m23-t01-reading-profiles-pmnpue` →
`claude/ai-workspace-docs-setup-aj3jvo`)로 2026-07-27 병합 완료
(커밋 `e6648ed`, 사용자 승인). 병합된 base 브랜치로 로컬 checkout을
재설정해 `pytest`(46개) 재검증, merge 전후 완전히 동일함을 확인.

**Milestone 26(Obsidian Vault Root Refactoring) — Completed.**
(2026-07-27, 사용자 승인)

---

## Milestone 27 — Obsidian Workspace Templates

**목표**(2026-07-27 사용자 요청, 원문 제목 "M25 - Obsidian Workspace
Integration"): Obsidian을 단순 Markdown 저장소가 아니라 "Task 생성
→ 문서 생성 → 진행 관리 → 상태 변경"이 Obsidian 안에서 이루어지는
AI Workspace의 실제 작업 인터페이스로 확장한다.

**Milestone 번호 안내**: 사용자 요청은 이 작업을 "M25"로 지칭했으나,
그 번호는 이미 완료된 Milestone 25(Production Vault Activation)가
쓰고 있어 기존 기록을 덮어쓰지 않기 위해 **Milestone 27, M27-T01**
로 번호를 새로 부여했다(ADR-0037이 M24-T01 충돌 때 Milestone 26으로
부여한 것과 동일한 패턴). Git 브랜치명(`claude/m25-obsidian-workspace-
c6hudf`)과 PR 제목은 사용자 요청 원문 그대로 "M25" 표기를 유지한다.

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M27-T01 | Task/Daily/Decision/Project Workspace Template 정의 + Frontmatter/Tag/Wiki Link 규칙 확장 + Task Vault 저장 자동화(`VaultDocumentKind.TASK`) | **완료** |

### M27-T01: Obsidian Workspace Templates

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Workspace(Project) Template 정의(README/Tasks/Notes/Meetings/Decisions/Archive) | ✅ (`Template - Project Workspace.md` 신규, 설계만 — 이 Vault가 단일 Project라 인스턴스화하지 않음, YAGNI) |
| 2 | Task Template 정의(Status/Priority/Milestone/Owner/Created/Updated/Checklist/Notes/Related Documents/Decision) | ✅ (`Template - Task.md` 신규 + `vault/markdown_generator.py`의 `render_task_file()`로 코드 생성 자동화) |
| 3 | Daily Note Template 정의(오늘 작업/진행중/완료/문제/결정사항/내일 계획) | ✅ (`Template - Daily.md` + `render_daily_file()` 확장) |
| 4 | Decision Template 정의(Problem/Options/Decision/Reason/Impact), ADR과 별도 유지 | ✅ (`Template - Decision.md` 갱신, `DECISION_TEMPLATE.md`(GitHub 원문용)는 무변경) |
| 5 | Wiki Link 규칙 정의 | ✅ (`AI_RULES`의 기존 Backlink Rule 재확인, 신규 문서에도 그대로 적용 — 변경 없음) |
| 6 | Tag 규칙 정의 | ✅ (`AI_RULES` Tag Rule에 `#task`/`#meeting`/`#bug`/`#feature`/`#research`/`#daily` 추가) |
| 7 | Frontmatter 규칙 정의 | ✅ (`AI_RULES`에 신규 Frontmatter Rule 절 — 상태를 갖는 문서는 `type`/`status`/`priority`/`milestone`/`created`/`updated`) |
| 8 | README/RULES/ARCHITECTURE/ROADMAP 갱신, 필요 시 ADR 작성 | ✅ (ADR-0038, `docs/ARCHITECTURE.md` §3.21 갱신, `docs/ROADMAP.md`/`.ai/RULES.md`(§9)/README.md 반영) |
| 9 | Template 생성이 정상 동작하는지 테스트 | ✅ (`tests/vault/` 신규 6개: `render_task_file` 정상/필드 누락 에러, Router TASK 라우팅/`task_id` 누락 에러, `VaultSaveEngine` TASK 저장, Daily 확장 섹션 검증) |
| 10 | 기존 Architecture 변경 없이 Workspace 확장 수준 유지 | ✅ (새 Interface 없음, 기존 4단계 Save Flow(Router→Generator→Writer→Engine) 그대로, `DAILY`가 이미 확립한 create 패턴 재사용) |

**구현 내용**

- `vault/models.py`: `VaultDocumentKind.TASK` 신규(create 방식,
  `DECISION`과 달리 Index에 append하지 않음).
- `vault/mapping.py`: `14 Tasks` 디렉터리 신설(`VAULT_CONTENT_
  DIRECTORIES` 15종→16종) + `VAULT_DIRECTORY_MAP[TASK]` = `"14
  Tasks/{task_id}.md"`(create).
- `vault/router.py`: `TASK`의 `task_id` 치환 처리(`DAILY`의 날짜
  치환과 동일한 패턴), 누락 시 `MissingVaultFieldError`.
- `vault/markdown_generator.py`: `render_task_file()` 신규(M25
  요청 Task Template 필드 전부 반영), `render_daily_file()`에
  진행중/완료/결정사항 섹션 추가(기존 "오늘 결정" 정리).
- `vault/engine.py`: `VaultSaveEngine.save()`가 `TASK` create를
  `render_task_file()`로 라우팅.
- `14 Tasks/README.md`(신규), `99 Templates/Template - Task.md`
  (신규), `99 Templates/Template - Project Workspace.md`(신규,
  설계만), `99 Templates/Template - Daily.md`/`Template -
  Decision.md`(갱신), `00 System/AI_RULES.md`(Tag Rule 확장 +
  Frontmatter Rule 신설), `00 System/PROJECT_INDEX.md`(Template
  Index/Retrieval 표에 Task/Project Workspace 행 추가).
- Vault `03 ADR/ADR Index.md`/`11 Milestones/Milestones Index.md`/
  `02 Architecture/Architecture Overview.md`에 ADR-0038/Milestone
  27 요약 반영.

**검증**

- `poetry run ruff check src tests` 클린, `poetry run mypy src`
  클린(기존에 존재하던 `types-PyYAML` 미설치 경고 2건 제외, 이번
  변경과 무관).
- `poetry run pytest`: `tests/vault/` 신규 6개 포함 전부 통과,
  `tests/integration/test_m23_vault_environment_integration.py`
  (Broken Backlink 0건 신규 유지, `14 Tasks/README.md`의
  `[[Template - Task]]` 링크 포함)/`test_m24_real_vault_e2e.py`
  전부 통과. 전체 스위트(웹 계층의 `httpx`/`starlette` 환경 의존성
  이슈 제외, 이번 변경과 무관) 806개 통과.

**Milestone 27(Obsidian Workspace Templates) — Completed.**
(2026-07-27, ADR-0038)

---

## Milestone 28 — Live Task Management & Integration

**목표**(2026-07-27 사용자 요청): Milestone 27이 만든 정적인
Markdown Workspace를 실제로 동작하는 AI Workspace로 확장한다 —
Task Lifecycle, 자동 문서 갱신, Vault↔Core Domain Integration
Layer, Workflow Engine 연동, Agent Assignment, Conversation Layer
연동. **Architecture Rule**(사용자 요청 원문): ADR-0035를 반드시
유지한다 — Core Domain은 vault를 알지 못하고, vault는 Core Domain을
알지 못한다. 경계를 넘는 통신은 반드시 Integration Layer(Vault
Adapter/Workflow Adapter/Agent Adapter)를 통해서만 이뤄진다.

**진행 방식**: `.ai/RULES.md` §2.2(One Task At A Time)에 따라
T01부터 순서대로 완료하고 각 Task마다 테스트/문서화를 마친 뒤 다음
Task로 진행한다.

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M28-T01 | Task Lifecycle(Status Transition, `updated` 자동 갱신, Archive 처리) | **완료** |
| M28-T02 | Automatic Document Synchronization(Task 변경 → Daily/Decision/Roadmap/Milestone 갱신) | **완료** |
| M28-T03 | Integration Layer(Vault Adapter/Workflow Adapter/Agent Adapter) | **완료** |
| M28-T04 | Workflow Engine Integration | **완료** |
| M28-T05 | Agent Assignment | **완료** |
| M28-T06 | Conversation Layer Integration | **완료** |

### M28-T01: Task Lifecycle

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Status Transition(Todo→In Progress→Review→Done→Archived) | ✅ |
| 2 | `updated` 자동 갱신 | ✅ |
| 3 | Archive 처리 | ✅ |
| 4 | Frontmatter 동기화 | ✅ |
| 5 | Task 상태 변경 API | ✅ |
| 6 | 테스트 통과 | ✅ |

**구현 내용**

- `vault/task_lifecycle.py`(신규): `TaskStatus` Enum(5개 상태),
  `_ALLOWED_TRANSITIONS`(Todo→In Progress→Review→Done→Archived,
  In Progress↔Todo/Review 되돌아가기 허용, Done은 Archived로만,
  Archived는 종단 상태), `transition_task_status(vault_root,
  task_id, new_status, *, today=None)` — Task 상태 변경 API.
  `sync.py`(Rename/Delete)와 같은 성격의 "문서 생성 이후 관리"
  계층으로 배치해 기존 Router→Generator→Writer→Engine Save Flow는
  건드리지 않았다(Task 생성은 여전히 Milestone 27의
  `VaultSaveEngine`/`render_task_file()` 몫).
- Frontmatter 동기화는 파일 전체를 재작성하지 않고 `status`/
  `updated` 두 줄만 정규식으로 치환한다(`writer.upsert_section()`이
  Index 문서의 섹션만 치환하는 것과 같은 최소 변경 원칙).
- Archive 처리: `ARCHIVED`로 전이하면 `14 Tasks/Archive/{task_id}.md`
  로 파일을 옮긴다. 파일명(`task_id`)은 그대로이므로 그 문서를
  가리키는 `[[task_id]]` Wikilink는 깨지지 않는다(`validation.py`/
  `sync.py`가 이미 `14 Tasks/`를 `rglob("*.md")`로 재귀 스캔하므로
  `mapping.py`/`VAULT_CONTENT_DIRECTORIES` 변경 불필요).
- `99 Templates/Template - Task.md`의 Status 절을 5개 상태 +
  Transition 다이어그램으로 갱신(기존 `blocked`는 M25 요청 5개
  상태에 없어 제거).
- 새 Interface 없음, Core Domain 참조 없음(ADR-0035 유지, vault
  패키지 내부 확장).

**검증**: `tests/vault/test_task_lifecycle.py`(신규 6개 — 정상
전이/허용되지 않은 전이/Archive 이동/Archived 종단 상태/Task
없음/frontmatter 없음), `ruff check src tests` 클린, `mypy
src/ai_workspace/vault` 클린, `pytest`(812개, 기존 806개 + 신규 6개)
전부 통과.

### M28-T02: Automatic Document Synchronization

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Task 변경 시 Daily Note 갱신 | ✅ |
| 2 | Task 변경 시 Decision 갱신 | ✅ |
| 3 | Task 변경 시 Roadmap 갱신 | ✅ (Vault 쪽 대응 문서로 구현, 아래 참고) |
| 4 | Task 변경 시 Milestone 갱신 | ✅ |
| 5 | Wiki Link 유지 | ✅ |
| 6 | Backlink 손실 없음 | ✅ |
| 7 | 테스트 통과 | ✅ |

**구현 내용**

- `vault/task_sync.py`(신규): `sync_task_change(vault_root,
  task_id, old_status, new_status, *, date=None)`가 Task 상태
  변경 하나를 관련 문서 3곳에 반영한다.
  1. **Daily Note**: 오늘(또는 지정한 날짜) Daily Note가 없으면
     `render_daily_file()`로 만들고, 새 상태에 대응하는 섹션
     (`TODO`→"오늘 작업", `IN_PROGRESS`/`REVIEW`→"진행중",
     `DONE`→"완료")에 `- [[task_id]] {이전} → {새} 상태` 줄을
     추가한다. `ARCHIVED`는 `DONE` 시점에 이미 "완료"에 기록됐으므로
     Daily Note를 다시 건드리지 않는다.
  2. **Milestone/Roadmap**: `docs/ROADMAP.md`는 GitHub 원문이라
     Vault가 직접 쓸 수 없다(`AI_RULES` "GitHub 문서를 수정하지
     않는다"). 그 대신 **Vault 쪽 대응 문서**인 `11 Milestones/
     Milestones Index.md`에 "## Task 변경 로그" 절을 만들고(없으면
     새로 생성) 같은 방식으로 로그 줄을 추가한다 — 이 매핑을 문서
     상단 안내문으로 명시했다.
  3. **Decision**: Task 문서의 `## Decision` 절에 실제 Wikilink가
     있을 때만(빈 `-` placeholder는 무시) `12 Decisions/Decisions
     Index.md`에 "## Task 연결" 절로 `[[task_id]] → [[결정 제목]]`
     을 기록한다 — 모든 Task가 아니라 실제로 판단이 내려진 Task만
     대상이 되게 해 과도한 자동화(YAGNI)를 피했다.
  - 공통 저장 전략 `_upsert_bullet_section()`: 섹션이 없으면
    "## 관련 문서" 앞에 새로 만들고(`writer.py`의 관련 문서 삽입
    규칙과 동일), 있으면 중복 없이 줄만 추가하며, 빈 `-`
    placeholder만 있으면 그 자리를 대체한다. `writer.upsert_section()`
    (섹션 전체 치환)과 달리 **누적 로그**에 맞게 새로 작성했다 —
    기존 함수를 억지로 재사용하지 않고 그 옆에 필요한 만큼만
    추가했다(Cohesion 원칙, 서로 다른 책임을 억지로 합치지 않음).
  - `transition_and_sync(vault_root, task_id, new_status, *,
    today=None)`: `transition_task_status()` + `sync_task_change()`
    를 이어 붙인 편의 함수 — "Task 변경 시 자동 문서 갱신"의 단일
    진입점. 둘을 분리해 둔 `task_lifecycle.py`/`task_sync.py`는
    각각 독립적으로도 쓸 수 있다(테스트에서 실제로 두 경로 모두
    검증).
  - Wiki Link/Backlink 유지: 새로 만드는 모든 링크는 파일명
    (`task_id`) 또는 이미 존재하는 문서 제목만 가리키므로 끊어질
    수 없다. 실제 Vault 대상 `find_broken_backlinks()` 통합 테스트
    (신규 broken link 0건 유지)로 확인했다.
  - `11 Milestones/Milestones Index.md`/`12 Decisions/Decisions
    Index.md` 상단에 이 자동 생성 절을 설명하는 안내문 추가(사람이
    나중에 "## Task 변경 로그"/"## Task 연결" 절을 보고 당황하지
    않도록).

**검증**: `tests/vault/test_task_sync.py`(신규 6개 — Daily 생성+
추가/멱등성/Milestone 로그/Decision 있음/Decision 없음/
`transition_and_sync` 통합), `ruff check src tests` 클린, `mypy
src/ai_workspace/vault` 클린, `tests/integration/
test_m23_vault_environment_integration.py`(Broken Backlink 0건
유지) 포함 `pytest`(818개, 기존 812개 + 신규 6개) 전부 통과.

### M28-T03: Integration Layer(Workspace Adapter Layer)

**설계 승인**(2026-07-30, 사용자): "Approve with Architecture
Direction" — 구현은 Vault/Workflow/Agent Adapter 3개로 진행하되,
문서·아키텍처에서는 이를 향후 Runtime/Service/Notification/Sync
Adapter가 추가될 수 있는 **Workspace Adapter Layer**의 첫 구성
요소로 정의할 것을 조건으로 승인. 상세는 ADR-0039.

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Core Domain → vault 의존성 없음 | ✅ |
| 2 | vault → Core Domain 의존성 없음 | ✅ |
| 3 | Integration Layer만 양쪽을 사용 | ✅ |
| 4 | Vault Adapter/Workflow Adapter/Agent Adapter 구현 | ✅ |
| 5 | ADR 작성(Workspace Adapter Layer 개념 명시) | ✅ (ADR-0039) |
| 6 | 테스트 통과 | ✅ |

**구현 내용**

- `src/ai_workspace/integration/`(신규 최상위 패키지):
  - `__init__.py` — Workspace Adapter Layer 정의(패키지 docstring):
    "Adapter 3개"가 아니라 확장 가능한 계층으로 명시, 현재 구성원과
    향후 확장 후보(Runtime/Service/Notification/Sync) 나열.
  - `vault_adapter.py`의 `VaultAdapter` — `vault/`를 아는 유일한
    구성원. `create_task()`는 `vault.engine.VaultSaveEngine`을,
    `transition_task()`는 `vault.task_lifecycle.
    transition_task_status()`/`vault.task_sync.transition_and_sync()`
    를 그대로 호출한다(`sync_related_documents` 플래그로 선택).
    `vault.task_lifecycle.TaskStatus`는 이 파일 밖으로 노출하지
    않고 문자열로만 주고받는다 — 반환값도 이 파일 안에서 정의한
    `TaskTransitionOutcome`(문자열/`bool`만) 하나로 통일했다.
  - `workflow_adapter.py`의 `WorkflowAdapter` — `WorkflowEngine`/
    `TaskEngine` **Interface**에만 생성자 의존(Interface First),
    `plan()`/`create_task()`/`transition_task()`가 각각 그대로
    위임한다. 자체 계획 수립 로직 없음.
  - `agent_adapter.py`의 `AgentAdapter` — `AgentManager`/
    `AgentRegistry`/`AgentScheduler` Interface에만 의존.
    `create_agent()`가 `AgentManager.create()` + `AgentRegistry.
    register()`를 잇는 것 — 두 Interface를 조합하는 것 자체가
    이 Adapter의 유일한 역할이다.
  - 세 Adapter는 서로를 참조하지 않는다(의도적) — Task↔Workflow
    (M28-T04)/Workflow↔Agent(M28-T05) 연결은 다음 Task에서 이
    Adapter들을 조합하는 상위 계층으로 만든다.
  - **공유 기반 클래스 없음**: 서로 다른 관심사에 억지로 공통
    Interface를 뽑는 대신, 패키지 경계 + 이름 규칙(`XxxAdapter`)
    + ADR-0039/`docs/ARCHITECTURE.md`로 "Layer" 개념을 정의했다
    (Speculative Generality 회피, `.ai/RULES.md` §4.2).
- **부수 변경**: `vault/task_sync.py`의 `TaskSyncResult`에
  `task_id`/`old_status`/`new_status` 필드 추가(기존 필드 무변경)
  — `VaultAdapter.transition_task()`가 실제 이전 상태를 돌려주려면
  필요했다. 기존 M28-T02 테스트 6개 전부 무변경 통과 확인.
- **경계 강제(자동화)**: `tests/integration_layer/
  test_architecture_boundary.py`(신규 3개) — `ast` 모듈로
  `src/ai_workspace/` 전체 import 문을 파싱해 Core Domain↔vault
  직접 의존 0건, `integration/` 밖에서 양쪽 동시 import 0건을
  코드로 강제한다. 앞으로 이 규칙을 어기면 리뷰가 아니라 테스트
  실패로 드러난다.
- `docs/ARCHITECTURE.md` §8에 의존성 규칙 18(Core Domain↔vault
  직접 참조 금지) 추가, §9 디렉터리 구조에 `integration/` 반영,
  §3에 "Workspace Adapter Layer(Milestone 28-T03, ADR-0039)" 절
  신설.
- 단위 테스트 디렉터리 이름 안내: 기존 `tests/integration/`은
  Milestone 23부터 써 온 "End-to-End 통합 테스트" 전용 이름이라,
  `src/ai_workspace/integration/`을 미러링하는 단위 테스트는 이름
  충돌을 피해 `tests/integration_layer/`에 뒀다(ADR-0039에 이유
  기록).

**검증**: `tests/integration_layer/`(신규 13개 — Vault/Workflow/
Agent Adapter 단위 테스트 10개 + Architecture Boundary 자동 검증
3개), `ruff check src tests` 클린, `mypy src/ai_workspace/integration
src/ai_workspace/vault` 클린, `pytest`(831개, 기존 818개 + 신규
13개) 전부 통과.

**Milestone 28-T03(Workspace Adapter Layer) 완료.** 다음 Task:
**M28-T04**(Workflow Engine Integration — `WorkflowAdapter`를 써서
Vault Task와 Core Domain Workflow를 실제로 연결).

### M28-T04: Workflow Engine Integration

**설계 승인**(2026-07-30, 사용자): "Go Ahead" — 단, 4개 원칙을
아키텍처 규칙으로 유지할 것을 조건으로 승인: (1) Workflow↔Vault
직접 의존 금지, (2) 모든 연결은 Integration Layer를 통해서만,
(3) Domain 객체는 Markdown/Vault 표현으로 오염되지 않음, (4)
Adapter는 연결·변환·위임만(비즈니스 로직 금지). 4개 전부 아래
구현에 그대로 반영했다(상세는 `docs/ARCHITECTURE.md`의 "구현
상태(Milestone 28-T04)" 절 참고).

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Workflow 생성(Task → Workflow) | ✅ |
| 2 | Workflow 종료 | ✅ |
| 3 | 상태 동기화(Workflow 상태 변경 → Task 상태 반영) | ✅ |
| 4 | 테스트 통과 | ✅ |

**구현 내용**

- `integration/workflow_task_link.py`(신규)의 `WorkflowTaskLink` —
  `VaultAdapter`(T03)와 `WorkflowAdapter`(T03)를 조합하는 4번째
  Integration Layer 구성 요소. 세 Adapter(Vault/Workflow/Agent)는
  여전히 서로를 참조하지 않는다는 ADR-0039 원칙은 유지하되,
  "연결" 자체가 목적인 T04는 두 Adapter를 함께 쓰는 별도 구성
  요소로 명시적으로 분리했다(Adapter 자체에 서로 참조를 넣지
  않음).
- `WorkflowLink`(값 객체) — Vault task_id(사람이 붙인 ID, 예
  `T28-04a`)와 Core Domain `Task`(⁠`TaskEngine`이 발급하는
  `task-N`)를 1:1로 묶는다. `domain.Task`/`domain.Workflow`에는
  필드를 추가하지 않았다 — 대신 기존에 있던 `Task.workflow_id`
  필드를 채워 재사용했다(Domain 오염 금지 원칙).
- `create_workflow_from_vault_tasks()` — `(vault_task_id, title)`
  목록을 받아 Core Domain `Task`를 각각 만들고(`WorkflowAdapter.
  create_task()`), Vault task_id 기준으로 받은 `dependencies`를
  Core Domain task_id로 변환해 `Workflow`를 만든다(`WorkflowAdapter.
  create_workflow()`) — "Task → Workflow 생성".
- `transition_and_reflect()` — Core Domain `Task`를 전이
  (`WorkflowAdapter.transition_task()`)한 뒤, Vault Task Lifecycle
  (Milestone 28-T01)에 대응하는 상태(TODO/IN_PROGRESS/REVIEW/DONE)
  면 `VaultAdapter.transition_task()`로 Vault 문서에도 반영한다 —
  "Workflow 상태 변경 → Task 상태 반영". `BLOCKED`/`CANCELLED`는
  Vault Task Lifecycle에 대응 상태가 없어 의도적으로 Vault를
  건드리지 않는다(억지로 끼워 맞추지 않음).
- `is_workflow_complete()` — Workflow 자체는 상태 필드가 없으므로
  ("종료"는 파생 값), 소속 Task 전체가 Core Domain 기준 `DONE`인지
  로 계산한다 — "Workflow 종료".
- `plan()`은 그대로 `WorkflowAdapter.plan()`(→`WorkflowEngine.
  plan()`)에 위임 — 새 계획 수립 알고리즘 없음.

**검증**: `tests/integration_layer/test_workflow_task_link.py`
(신규 6개 — Workflow 생성+의존관계 변환/`plan()` 순서/상태 동기화/
매핑 불가 상태는 Vault 미반영/Domain Lifecycle 위반 시 예외/
Workflow 종료 판정), `tests/integration_layer/
test_architecture_boundary.py`(기존 3개, 무변경 통과 — 새 파일도
`integration/` 안이라 경계 위반 없음), `ruff check src tests`
클린, `mypy src/ai_workspace/integration src/ai_workspace/vault
src/ai_workspace/engines src/ai_workspace/domain` 클린,
`pytest`(837개, 기존 831개 + 신규 6개) 전부 통과.

**Milestone 28-T04(Workflow Engine Integration) 완료.** 다음 Task:
**M28-T05**(Agent Assignment).

### M28-T05: Agent Assignment

**설계 승인**(2026-07-30, 사용자): "Go Ahead" — 단, `WorkflowTaskLink`
에 Agent 책임을 추가하지 말고 `WorkflowAgentLink`를 별도 Connector로
구현할 것, Adapter는 외부 시스템 연결만·Connector는 여러 Adapter를
조합하는 유스케이스 오케스트레이션만 담당하는 구분을 지킬 것을
조건으로 승인. 이 구분을 ADR-0040으로 공식화했다 — M28 완료 후
Architecture Freeze에서 Integration Layer 역할을 명확히 하려는
목적(사용자 코멘트).

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Agent 지정 가능(Agent Assignment) | ✅ |
| 2 | Agent 상태 추적(Agent Status) | ✅ |
| 3 | Workflow와 연결 | ✅ |
| 4 | Agent Registry 연동 | ✅ (AgentAdapter 재사용으로 충족) |
| 5 | Agent Manager 연동 | ✅ (AgentAdapter 재사용으로 충족) |
| 6 | 진행률 기록(Agent Progress) | ✅ |
| 7 | 테스트 통과 | ✅ |

**구현 내용**

- `integration/workflow_agent_link.py`(신규)의 `WorkflowAgentLink`
  — `WorkflowTaskLink`(T04)와 별도인 새 Connector. `AgentAdapter`/
  `WorkflowAdapter`만 조합한다(Vault는 모른다 — Task 상태의 Vault
  반영은 이미 `WorkflowTaskLink` 책임이라 중복하지 않음).
- `AgentAssignment`(값 객체) — `WorkflowLink` + `Agent`.
  `domain.Task`/`domain.Agent` 어느 쪽에도 필드를 추가하지
  않는다(Domain 오염 금지, T04와 동일 원칙) — 배정 관계는
  `WorkflowAgentLink`가 내부 `dict`로만 관리.
- `assign_agent()` — `AgentAdapter.select_agent()`(→
  `AgentScheduler.select()`)가 고른 Agent를 배정. 후보 없으면
  `NoAvailableAgentError`.
- `transition_agent_status()` — `AgentAdapter.transition_agent()`
  (→ `AgentManager.transition()`)에 위임해 배정된 Agent 상태를
  전이. 배정 전이면 `AgentNotAssignedError`.
- `agent_progress()` — 해당 Agent에게 배정된 Task 중 Core Domain
  기준 `DONE` 비율을 매번 파생 계산(캐시된 필드 없음).
- **ADR-0040(Adapter vs Connector 공식화)**: `integration/
  __init__.py`를 갱신해 두 종류 구성원(외부 시스템 1개만 연결하는
  Adapter / 여러 Adapter를 조합하는 Connector)을 명시하고, Connector
  는 서로도 참조하지 않는다는 원칙을 문서화. `workflow_task_link.py`
  docstring에도 "Connector" 용어 반영(로직 무변경).

**검증**: `tests/integration_layer/test_workflow_agent_link.py`
(신규 6개 — 배정/후보 없음/미배정 상태 전이 거부/상태 전이 반영/
진행률 계산/미배정 Agent 진행률 0), `tests/integration_layer/
test_architecture_boundary.py`(기존 3개, 무변경 통과), `ruff check
src tests` 클린, `mypy src/ai_workspace/integration
src/ai_workspace/vault src/ai_workspace/engines src/ai_workspace/domain
src/ai_workspace/runtime/agent` 클린, `pytest`(843개, 기존 837개 +
신규 6개) 전부 통과.

**Milestone 28-T05(Agent Assignment) 완료.** 다음 Task:
**M28-T06**(Conversation Layer Integration) — M28의 마지막 Task이며,
완료 후 사용자가 요청한 Architecture Freeze(ADR 전체 재검토/Layer
의존성 검증/Integration Boundary 검증/Interface 목록 확정/M29
요구사항 재정의)를 진행한다.

### M28-T06: Conversation Layer Integration

**설계 승인**(2026-07-30, 사용자): 요구사항/Boundary/금지 목록을
상세히 명시한 지시로 승인. 핵심 조건: (1) 새 비즈니스 로직 절대
추가 금지, (2) `integration/conversation_workflow_link.py`(또는
적절한 이름)의 Conversation Connector로 기존 Adapter/Connector를
조합, (3) Conversation Layer는 Domain/Vault/AgentManager를 직접
참조하지 않고 모든 요청은 Integration Layer를 통해 전달, (4)
Conversation Layer 책임은 사용자 입력 해석/요청 라우팅/결과 조합
및 응답 반환으로 한정(Planning/Workflow 생성/Agent 선택/Task
Lifecycle 등은 그대로 Core에 남김), (5) T06 완료 후 M29 시작하지
않고 종료(Architecture Freeze 대기).

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Conversation Connector 구현(`integration/conversation_workflow_link.py`) | ✅ |
| 2 | 기존 Adapter/Connector 조합으로 요청 처리, 새 비즈니스 로직 없음 | ✅ |
| 3 | Conversation Layer가 Domain/Vault/AgentManager 직접 참조 금지 | ✅ |
| 4 | ADR-0041 작성(역할/Boundary/책임/Integration Layer와의 관계) | ✅ |
| 5 | `docs/ARCHITECTURE.md` 갱신 | ✅ |
| 6 | 단위 테스트 추가 + 기존 Architecture Boundary 테스트 통과 | ✅ |
| 7 | 전체 테스트/ruff/mypy 통과 | ✅ |

**구현 내용**

- `integration/conversation_workflow_link.py`(신규)의
  `ConversationConnector` — 생성자로 `VaultAdapter`/
  `WorkflowTaskLink`/`WorkflowAgentLink`를 주입받아 조합만 한다.
  - `handle_task_request()` — "Task 생성→Workflow 생성→Agent
    Assignment→Vault 업데이트"(M25 요청 예시 흐름)를 세 컴포넌트
    호출 순서 배열만으로 구현.
  - `advance_task()` — `WorkflowTaskLink.transition_and_reflect()`
    그대로 위임.
  - `report_status()` — `WorkflowTaskLink.get_task_status()`(신규
    조회 전용 메서드, `WorkflowAdapter.get_task()` 위임)/
    `is_workflow_complete()` 결과를 dataclass로 묶기만("결과
    조합").
  - 요청/결과는 이 파일 안에서만 정의한 dataclass
    (`ConversationTaskRequest`/`ConversationTaskResult`/
    `ConversationStatusReport`)로 주고받는다 — `domain.Task`/
    `domain.Agent`에 필드를 추가하지 않는다.
- **ADR-0041(Orchestrating Connector 도입)**: ADR-0040("Connector
  끼리 서로 참조하지 않는다")을 Peer Connector(`WorkflowTaskLink`/
  `WorkflowAgentLink`, 유스케이스 하나만 책임)로 좁히고,
  `ConversationConnector`를 그 원칙의 명시적 예외인
  **Orchestrating Connector**(여러 Peer Connector/Adapter를
  조합해 상위 유스케이스를 라우팅·조합)로 정의. `integration/
  __init__.py` 갱신.
- **Boundary 강제**: `tests/integration_layer/
  test_conversation_connector_boundary.py`(신규)가 `ast`로
  `conversation_workflow_link.py`가 `ai_workspace.vault`/
  `ai_workspace.interfaces.{workflow_engine,task_engine,
  agent_manager,agent_registry,agent_scheduler}`/`ai_workspace.
  engines.{workflow_engine,task_engine}`/`ai_workspace.runtime.agent`
  를 import하지 않고, `ai_workspace.*` import가 전부
  `integration.*`/`domain.*`인지 확인한다.

**검증**: `tests/integration_layer/test_conversation_connector.py`
(신규 3개 — Task 요청 처리/상태 전이+Vault 반영/상태 조회 조합),
`test_conversation_connector_boundary.py`(신규 2개),
`test_architecture_boundary.py`(기존 3개, 무변경 통과), `ruff check
src tests` 클린, `mypy src/ai_workspace/integration
src/ai_workspace/vault src/ai_workspace/engines src/ai_workspace/domain
src/ai_workspace/runtime/agent` 클린, `pytest`(848개, 기존 843개 +
신규 5개) 전부 통과.

**Milestone 28-T06(Conversation Layer Integration) 완료.**

**Milestone 28(Live Task Management & Integration) 전체 완료
(T01~T06).** `.ai/RULES.md` §2.2(One Task At A Time)에 따라 M29는
시작하지 않는다 — 사용자가 요청한 Architecture Freeze(ADR 전체
재검토/Layer 의존성 검증/Integration Boundary 검증/Interface 목록
확정/M29 요구사항 재정의)의 승인을 기다린다.

---

## Milestone 28 — Architecture Freeze

**목표**(2026-07-30 사용자 요청): M28(T01~T06)이 만든 아키텍처를
새 기능 구현 없이 검증·정리·기준선(Baseline)으로 확정한다. 결과는
ADR-0042(결정 요약)와 이 절(Freeze Report 전문)에 나눠 기록한다.

### 1. Architecture Review Report

#### 1.1 Layer 검토

| Layer | 대응 디렉터리 | 책임 |
|---|---|---|
| Domain | `domain/`, `interfaces/` | 순수 값 객체 + 추상 계약. 외부 시스템 의존 0건 |
| Application | `engines/`, `runtime/`, `agents/`, `core/` | Domain 위에서 실제 오케스트레이션(Task/Workflow 생성·전이, Agent 생명주기) |
| Integration | `integration/` | Domain(Application 포함)과 Vault를 잇는 유일한 경계층 |
| Vault | `vault/` | Obsidian Markdown 저장/동기화, Core Domain을 모름 |
| Conversation | (전용 코드 패키지 없음) | `ConversationConnector`의 호출자로만 존재 — 자연어 해석은 코드가 아니라 AI 역할(M23-T06 전제 유지) |

**단방향성/순환 없음 검증**: `git diff main...feature/m28-live-task-management --stat -- src/ai_workspace/domain src/ai_workspace/interfaces src/ai_workspace/engines src/ai_workspace/runtime`
결과 **0 파일 변경** — M28 전체(6개 Task)가 Domain/Application에
단 한 줄도 손대지 않고 그 위에 `integration/`만 추가했다는 뜻이다.
`grep -rn "ai_workspace.integration" src/ai_workspace/{domain,interfaces,engines,vault,runtime,core,agents,web,adapters,storage}`
결과도 0건 — 아래 계층이 위 계층(`integration/`)을 참조하는 사례가
전혀 없다. 이 두 확인만으로 "Layer 간 의존성이 단방향"이라는 조건과
"순환 의존 없음"이 코드 사실로 증명된다(리뷰가 아니라 grep 결과).

#### 1.2 Integration Layer 검토

구성: Adapter(`VaultAdapter`/`WorkflowAdapter`/`AgentAdapter`) →
Peer Connector(`WorkflowTaskLink`/`WorkflowAgentLink`) →
Orchestrating Connector(`ConversationConnector`).

5개 원칙 확인:

| 원칙 | 확인 방법 | 결과 |
|---|---|---|
| Adapter는 외부 시스템 하나만 | `test_connector_layering.py::test_adapters_do_not_reference_other_integration_modules` | ✅ |
| Connector는 여러 Adapter를 조합 | 코드 리뷰(`WorkflowTaskLink.__init__`이 Vault+Workflow Adapter 2개, `WorkflowAgentLink.__init__`이 Agent+Workflow Adapter 2개를 주입받음) | ✅ |
| Peer Connector끼리 직접 참조 금지 | `test_connector_layering.py::test_peer_connectors_only_reference_adapters` | ⚠️→✅ (아래 위반 발견/수정 참고) |
| Orchestrating Connector만 여러 Connector 조합 | `test_connector_layering.py::test_nothing_references_orchestrating_connectors`(반대 방향 금지 확인) + 코드 리뷰(`ConversationConnector.__init__`이 Peer Connector 2개 + Adapter 1개 주입) | ✅ |
| Connector는 비즈니스 로직 없음 | 코드 리뷰 — 모든 Connector 메서드가 Adapter 호출 또는 dict/list 조합·파생 계산(사칙연산·비교 수준)만 수행, 새 상태 전이 규칙·선택 알고리즘 없음 | ✅ |

**발견한 위반 1건(즉시 수정)**: `workflow_agent_link.py`(Peer
Connector)가 `workflow_task_link.py`(다른 Peer Connector)에서
`WorkflowLink`를 import하고 있었다 — "Peer Connector끼리 직접
참조 금지" 위반. `test_connector_layering.py`(이번 Freeze에서
신규 작성)가 이를 실제로 잡아냈다. 수정: `WorkflowLink`를 로직 없는
값 객체 전용 신규 모듈 `integration/models.py`로 옮기고, 두 Peer
Connector가 그 모듈만 참조하도록 고쳤다. 새 비즈니스 로직·새
Layer·새 Interface가 아니라 기존 값 객체의 위치만 옮긴 것이다
(ADR-0042 결정 3).

문서 보완: `docs/ARCHITECTURE.md` §8에 규칙 19(Adapter/Peer
Connector/Orchestrating Connector 참조 방향)/20(Conversation
Layer가 Vault/Core Domain Engine을 직접 참조 금지)을 추가해,
지금까지 ADR에만 있던 규칙을 프로젝트 표준 "의존성 규칙" 목록에도
반영했다.

#### 1.3 Architecture Boundary 검토

확인한 규칙과 근거:

- **Conversation → Integration → Core**: `ConversationConnector`
  생성자가 `VaultAdapter`/`WorkflowTaskLink`/`WorkflowAgentLink`만
  받는다(코드 리뷰) — Conversation Layer가 그 아래 어떤 것도 직접
  구성하지 않는다.
- **Core는 Vault를 모른다 / Domain은 Vault를 모른다**:
  `test_architecture_boundary.py::test_core_domain_does_not_import_vault`
  (통과).
- **Conversation은 Vault를 직접 접근하지 않는다 / WorkflowEngine·
  TaskEngine·AgentManager를 직접 호출하지 않는다**:
  `test_conversation_connector_boundary.py`(2개, 통과) — `ast`로
  `conversation_workflow_link.py`의 import가 `ai_workspace.vault`/
  `ai_workspace.interfaces.{workflow_engine,task_engine,
  agent_manager,agent_registry,agent_scheduler}`/`ai_workspace.
  engines.{workflow_engine,task_engine}`/`ai_workspace.runtime.agent`
  중 어느 것도 포함하지 않음을 확인.
- **모든 연결은 Integration Layer를 통해 이뤄진다**:
  `test_architecture_boundary.py::test_only_integration_layer_imports_both_sides`
  (통과) + `test_connector_layering.py`(3개, 통과, 위 1.2 참고).

**AST 기반 Architecture Test 전체 목록**(모두 통과, `pytest`
결과는 2절 참고):

| 테스트 파일 | 검증 대상 |
|---|---|
| `test_architecture_boundary.py`(3개) | Core Domain↔vault 직접 의존 0건, `integration/` 밖에서 양쪽 동시 import 0건 |
| `test_conversation_connector_boundary.py`(2개) | Conversation Connector가 vault/Core Domain Engine을 직접 import하지 않음 |
| `test_connector_layering.py`(3개, 이번 Freeze 신규) | Adapter/Peer Connector/Orchestrating Connector 참조 방향 |

#### 1.4 Domain 검토

`git diff main...feature/m28-live-task-management -- src/ai_workspace/domain`
결과 **0줄 변경** — M28 전체에서 Domain은 전혀 건드리지 않았다.

- **불필요한 필드 없음**: `Task`(task_id/project_id/title/status/
  workflow_id), `Workflow`(workflow_id/mission_id/task_ids/
  dependencies), `Agent`(agent_id/role/capabilities/status) —
  M28이 필요로 한 "Vault task_id 매핑"/"Agent 배정 관계"는 전부
  Integration Layer 쪽 값 객체(`WorkflowLink`/`AgentAssignment`)
  로 옮겨졌고 Domain에는 하나도 추가되지 않았다.
- **외부 시스템 의존 없음**: `domain/{task,workflow,agent}.py`는
  `dataclasses`/`enum`(표준 라이브러리)만 import한다(grep 확인).
- **Value Object 사용 적절**: `TaskStatus`/`AgentRole`/
  `AgentCapability`/`AgentStatus`는 모두 Enum. `Task`/`Workflow`/
  `Agent`는 mutable dataclass(M28 이전부터의 기존 설계, 이번에
  바꾸지 않음) — Integration Layer가 `domain_task.workflow_id = …`
  처럼 공개 필드를 직접 대입하는 지점이 있는데, 이는 캡슐화를
  깨는 것이 아니라 원래 공개 필드였던 것을 그대로 쓰는 것이다.
  `TaskEngine.create_task()`가 `workflow_id`를 생성 시점 인자로
  받지 않는 것은 기존 설계 공백으로, 8절 개선 후보에 남긴다.
- **M29 기준선으로 사용 가능**: 평가 — **가능**. Domain은 M28 내내
  완전히 안정적이었고(무변경), Integration Layer가 이미 그 위에서
  Task/Workflow/Agent 세 도메인 객체를 실제로 조합해 왔으므로
  M29(Project Intelligence)가 추가할 "지능형 판단"도 Domain을
  더 건드리지 않고 Integration Layer 상위(또는 새 Orchestrating
  Connector)에서 조립될 가능성이 높다.

#### 1.5 Public Interface Freeze

**Core Domain — 27종 Interface(무변경, `docs/ARCHITECTURE.md` §7)**:
이번 Freeze에서 시그니처 변경 없음, 신규 Interface 없음. 특히
M28이 직접 감싼 5종: `WorkflowEngine.plan()`, `TaskEngine.
{create_task,transition,get_task,record_step,get_steps}()`,
`AgentManager.{create,transition}()`, `AgentRegistry.
{register,get,list_active,remove}()`, `AgentScheduler.select()`.

**Integration Layer — Public API(신규, Milestone 28)**:

| 구성원 | 공개 메서드 |
|---|---|
| `VaultAdapter` | `create_task()`, `transition_task()` |
| `WorkflowAdapter` | `create_workflow()`, `plan()`, `create_task()`, `transition_task()`, `get_task()` |
| `AgentAdapter` | `create_agent()`, `list_active_agents()`, `select_agent()`, `transition_agent()` |
| `WorkflowTaskLink` | `create_workflow_from_vault_tasks()`, `plan()`, `transition_and_reflect()`, `is_workflow_complete()`, `get_task_status()` |
| `WorkflowAgentLink` | `assign_agent()`, `get_assignment()`, `transition_agent_status()`, `agent_progress()`, `list_assignments()` |
| `ConversationConnector` | `handle_task_request()`, `advance_task()`, `report_status()` |
| 값 객체(Public) | `models.WorkflowLink`, `workflow_agent_link.AgentAssignment`, `vault_adapter.TaskTransitionOutcome`, `conversation_workflow_link.{ConversationTaskRequest,ConversationTaskResult,ConversationStatusReport}` |

**Internal API(Public 아님, 사전 공지 없이 바뀔 수 있음)**: `_`
접두 함수/상수 전부 — 예: `vault/task_sync._upsert_bullet_section()`/
`_section_body()`, `vault/task_lifecycle._replace_frontmatter_field()`/
`_read_frontmatter()`, `workflow_task_link._DOMAIN_TO_VAULT_STATUS`.
클래스 메서드 중 `_`로 시작하는 것은 없음(코드 리뷰로 확인) —
모든 클래스의 공개 표면이 위 표와 정확히 일치한다.

#### 1.6 ADR 검토

ADR-0035/0039/0040/0041 사이 **실질적 충돌 없음**을 확인했다.
관계: ADR-0035(vault↔Core Domain 독립 원칙 최초 선언) →
ADR-0039(그 경계를 넘는 유일한 통로로 Integration Layer 신설) →
ADR-0040(Integration Layer 내부를 Adapter/Peer Connector로 세분화)
→ ADR-0041(Peer Connector만으로 부족한 상위 유스케이스를 위해
Orchestrating Connector라는 명시적 예외 추가) — 각 ADR이 이전
ADR을 명시적으로 좁히거나 확장할 뿐, 서로 모순되는 지점은 없다.

발견한 표기 개선 후보(지금 고치지 않음, 8절 참고): "Vault
Integration Layer"(ADR-0035)와 "Integration Layer"/"Workspace
Adapter Layer"(ADR-0039) 이름이 비슷해 혼동 여지가 있다.

중복 내용: 없음 — 각 ADR이 서로 다른 결정을 기록하고 있어 정리가
필요한 중복은 발견되지 않았다.

보완: ADR-0042(이 Freeze 자체)를 신규 작성해 검증 결과와 위반
수정 1건을 공식 기록했다.

#### 1.7 확장성 검토

예상 구성요소(Runtime/Service/Notification/Sync/MCP/GitHub
Adapter) 전부 "외부 시스템 하나"라는 Adapter 정의를 만족한다 —
기존 파일을 하나도 바꾸지 않고 `integration/`에 새 `xxx_adapter.py`
를 추가하는 것만으로 확장 가능하다고 확인했다. 필요하면 그 위에
새 Peer Connector(예: "Sync Adapter + Vault Adapter를 조합하는
SyncTaskLink") 또는 `ConversationConnector`가 그 Peer Connector를
추가로 조합하는 형태로 자연스럽게 이어진다 — 현재 구조 변경 없이
가능하다.

**유지보수 주의사항 1건**: `test_connector_layering.py`의 분류
집합(`_ADAPTERS`/`_PEER_CONNECTORS`/`_ORCHESTRATING_CONNECTORS`)
은 새 모듈을 만들 때 수동으로 등록해야 검증 대상이 된다 — 자동
판별(예: docstring 마커 파싱)은 지금 만들지 않는다(YAGNI). 8절
개선 후보에 남긴다.

#### 1.8 Architecture 개선사항(목록만, 리팩토링하지 않음)

| # | 항목 | 내용 |
|---|---|---|
| 1 | 네이밍 | "Vault Integration Layer"(ADR-0035, `vault/`)와 "Integration Layer"/"Workspace Adapter Layer"(ADR-0039, `integration/`)가 이름이 비슷해 혼동 여지. 문서에서 명확히 구분할 이름 재검토 후보 |
| 2 | 문서 구조 | `docs/ARCHITECTURE.md` §3의 Workspace Adapter Layer/Conversation Layer 절이 `### 3.N` 번호 하위 절 형식을 따르지 않고 번호 없는 제목으로 붙어 있음 — 다음 문서 정리 때 `### 3.22`/`### 3.23`으로 정식 번호 부여 후보 |
| 3 | 문서 정확도 | §7 Interface 표에서 `WorkflowEngine`/`TaskEngine`/`AgentManager`/`AgentRegistry`/`AgentScheduler`가 "완료(계약)"로만 표시돼 있으나, 실제로는 Milestone 2(T2-01~T2-06)부터 `InMemory*` 구체 구현체가 존재하고 M28 Integration Layer가 실사용 중 — 표 상태를 "완료(계약+구현)"로 갱신할 문서 정확도 개선 후보(M28 이전부터 있던 문서 부채, M28이 만든 것은 아님) |
| 4 | API 확장 여지 | `ConversationConnector.handle_task_request()`는 Task 1개짜리 Workflow만 다룬다 — 여러 Task/의존관계가 있는 Workflow는 `WorkflowTaskLink.create_workflow_from_vault_tasks()`가 이미 지원하지만 Conversation Connector에는 아직 노출되지 않음. 실제 Conversation Layer 요구사항이 나오면(M29 이후) 자연스러운 확장 지점 |
| 5 | API 형태 | `VaultAdapter.transition_task(..., sync_related_documents: bool = True)`의 boolean 플래그가 두 가지 동작을 분기 — 필요해지면 메서드 2개로 분리하는 게 더 명확할 수 있음(현재는 낮은 우선순위) |
| 6 | 테스트 디렉터리 네이밍 | `tests/integration/`(Milestone 23부터의 E2E 테스트 전용)과 `tests/integration_layer/`(M28, `src/ai_workspace/integration/` 미러) 이름이 비슷해 혼동 여지 — ADR-0039에 의도적 선택으로 기록은 해 뒀으나, 다음 테스트 스위트 정리 때 재검토 후보 |
| 7 | 계층 등록 자동화 | `test_connector_layering.py`의 Adapter/Peer/Orchestrating 분류가 수동 등록 방식 — 새 Adapter/Connector를 깜빡 등록하지 않으면 그 모듈의 "밖으로 나가는" 참조는 검증되지 않음(들어오는 참조는 `test_nothing_references_orchestrating_connectors`가 계속 잡아냄). 자동 판별 도입은 지금은 YAGNI |

### 2. Freeze 결과(완료 조건 확인)

| 조건 | 결과 |
|---|---|
| Architecture Boundary 유지 | ✅ (위반 1건 발견 즉시 수정, 이후 재검증 통과) |
| Layer 구조 검증 완료 | ✅ (1.1절) |
| Integration Layer 검증 완료 | ✅ (1.2절) |
| Public Interface 확정 | ✅ (1.5절) |
| ADR 검토 완료 | ✅ (1.6절, ADR-0042 신규) |
| 전체 테스트 통과 | ✅ `pytest`(웹 계층 `httpx`/`starlette` 환경 이슈 3개 제외, 무관) **851개 전부 통과**(기존 848개 + Freeze 신규 3개 `test_connector_layering.py`) |
| ruff clean | ✅ `ruff check src tests` |
| mypy clean | ✅ `mypy src/ai_workspace/integration src/ai_workspace/vault src/ai_workspace/engines src/ai_workspace/domain src/ai_workspace/runtime/agent`(기존 `types-PyYAML` 미설치 경고 2건은 M28 이전부터 존재, 무관) |

### 3. 수정된 문서

`.ai/DECISIONS.md`(ADR-0042 신규), `docs/ARCHITECTURE.md`(§8 규칙
19/20 추가), `integration/__init__.py`(models.py/계층 참조 규칙
반영), `integration/workflow_task_link.py`/`workflow_agent_link.py`/
`conversation_workflow_link.py`(WorkflowLink import 경로만 수정,
로직 무변경), `integration/models.py`(신규), `tests/integration_layer/
test_connector_layering.py`(신규).

### 4. 개선 권장사항

1.8절 표 7건 — 전부 "목록만", 이번 Freeze에서 리팩토링하지 않음.
우선순위를 매긴다면 #3(문서 정확도)이 가장 저비용·저위험이라
다음 문서 정리 Task에서 바로 처리 가능하고, #1/#2/#6(네이밍/문서
구조)은 문서 전용 변경이라 역시 낮은 리스크, #4/#5/#7은 M29 이후
실제 요구사항이 생겼을 때 판단하는 것이 적절하다.

### 5. M29 진행 가능 여부

**가능** — Layer 구조/Integration Boundary/Public Interface/ADR
정합성 전부 검증 완료, 발견된 유일한 위반은 이 Freeze 안에서
수정 및 회귀 테스트 추가까지 마쳤다. 단, 이 보고서는 승인 대기
상태이며, `.ai/RULES.md` §2.2(One Task At A Time)에 따라 사용자
승인 전에는 M29(Project Intelligence)를 시작하지 않는다.

**Milestone 28 Architecture Freeze 완료 — 사용자 승인 완료
(2026-07-30).**

---

## Milestone 29 — Project Intelligence

**목표**(2026-07-30 사용자 확정, ChatGPT와 사전 합의한 M29~M40
로드맵 기준): Project/Workflow/Task/Agent/Event/Vault 데이터를
종합하여 프로젝트의 현재 상태를 분석하고, **Project Snapshot/
Health/Risk/Recommendation**을 생성하는 **Project Intelligence
Foundation**을 구축한다. Project Intelligence는 **Read Only(Query
Layer)**로 동작하며 기존 Core Domain 비즈니스 로직을 변경하지
않는다. 모든 데이터 접근은 기존 Engine/Adapter/Connector를 통해
수행하며 Architecture Freeze(M28, ADR-0042)의 Layer Boundary를
유지한다. 이후 M30(Context Intelligence)~M33(Planning Intelligence)
로드맵이 활용할 기반까지만 담당하고, 추론 엔진을 과도하게 키우지
않는다 — Rule 기반만 구현하고 AI 추론/LLM 호출은 M33 이후로 미룬다.

**Definition of Done**

| # | 항목 |
|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 |
| 2 | Domain/Interfaces/Engine의 책임 변경 없음 |
| 3 | Project Snapshot 생성 가능 |
| 4 | Project Health 계산 가능 |
| 5 | Project Risk 분석 가능 |
| 6 | Project Recommendation 생성 가능 |
| 7 | Dashboard 또는 Vault를 통해 실제 결과 노출 |
| 8 | Integration Layer를 통한 접근만 허용(§8 규칙 21 신설) |
| 9 | Layer Boundary 테스트 통과 |
| 10 | `pytest`/`ruff`/`mypy` 모두 통과 |
| 11 | Architecture 및 ADR 문서 최신화 |

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M29-T01 | Project Intelligence Architecture 설계 | **완료** |
| M29-T02 | Project Snapshot Analyzer | **완료** |
| M29-T03 | Project Health & Risk Analyzer | **완료** |
| M29-T04 | Project Recommendation | **완료** |
| M29-T05 | Integration & Presentation | **완료** |

### M29-T01: Project Intelligence Architecture

**목표**: Project Intelligence의 역할/책임을 정의하고, 데이터
소스·Output·신규 Interface 필요 여부를 결정한다.

**조사 결과(구조적 공백 2건 발견)**

1. `TaskEngine`은 `get_task(task_id)` 단건 조회만 제공 —
   project 단위 전체 목록 조회가 없다. `domain.Project`에도
   소속 task_id 목록 필드가 없다.
2. `WorkflowEngine`/`WorkflowTaskLink`/`WorkflowAgentLink`도
   "Link/Agent 하나" 단위 조회만 제공 — project 전체 Workflow
   목록/Agent 배정 전체 목록을 얻는 API가 없다.

Core Domain 27종 Interface만으로는 Snapshot 자체가 불가능하다는
뜻이다. 반면 `vault/`의 `14 Tasks/*.md` 문서(M27/M28)는 파일
열거만으로 project 소속 Task 전체(frontmatter: task_id/status/
priority/milestone/owner/created/updated)를 이미 제공한다 — M28이
Vault를 "Live" 상태의 실제 운영 소스로 확립해 둔 결과다.

**결정(ADR-0043, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- 신규 Core Domain Interface를 추가하지 않는다(27종 유지). Project
  단위 열거가 필요한 데이터는 **Vault Task 문서를 단일 데이터
  소스**로 삼는다.
- 데이터 접근 경로: `vault/task_query.py`(신규, Core Domain을
  모르는 순수 읽기 함수) → `VaultAdapter.list_tasks()`(신규 메서드,
  기존 Adapter 클래스 확장 — Interface 아님) → `intelligence/`
  Analyzer. Agent 데이터는 `AgentAdapter.list_active_agents()`
  (기존, M28-T03)를 그대로 재사용, 신규 메서드 없음.
- Event(EventStore)는 M29 데이터 소스에서 제외(Adapter 미존재,
  YAGNI — Vault `updated` 필드로 정체 판단 충분). Workflow 단위
  집계는 Vault Task의 `milestone` 필드로 근사(Vault에 Workflow
  전용 문서 종류 없음).
- "Blocked Task"는 Vault `TaskStatus`(todo/in-progress/review/
  done/archived)에 대응 값이 없음(Core Domain `TaskStatus.BLOCKED`
  와 별개 enum, ADR-0035) — "정체(Stagnant) = IN_PROGRESS/REVIEW
  상태이면서 `updated`가 임계일 이상 지난 Task" 규칙으로 근사한다
  (임계값은 M29-T03에서 확정).
- 새 최상위 패키지 `intelligence/`를 만든다(`integration/`과 같은
  층위, 그 위에 얹힘). Analyzer는 오직 `integration/`의
  `VaultAdapter`/`AgentAdapter`에만 의존하고 `domain`/`interfaces`/
  `engines`/`vault`를 직접 import하지 않는다(§8 규칙 21 신설,
  `tests/intelligence/test_intelligence_layering.py`로 M29-T02에서
  `ast` 기반 강제 예정).

**Intelligence Output 정의(설계, 구현은 T02~T04)**

| Output | 핵심 필드(초안) |
|---|---|
| `ProjectSnapshot` | project_id, total/done/in_progress/review/todo/archived 개수, milestone별/owner별 집계, progress_ratio, active_agent_count |
| `ProjectHealth` | level(Healthy/Warning/Critical), reasons |
| `ProjectRisk` | kind(Stagnant Task/Agent 과부하/Workflow 정체/의존성 위험), 대상 id, severity |
| `ProjectRecommendation` | action, target, reason, priority(Rule 기반, LLM 호출 없음) |

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| 설계 문서 완료 | ✅ (`docs/ARCHITECTURE.md` §3.22, `.ai/DECISIONS.md` ADR-0043) |
| Architecture 검토 완료 | ✅ (Core Domain Interface 조회 공백 2건 확인, 대안 3건 검토·기각 근거 ADR-0043) |
| 신규 Interface 필요 여부 결정 | ✅ (불필요 — Vault 단일 소스로 DoD 4대 산출물 모두 달성 가능) |

코드 변경 없음(설계 Task). 다음 Task: **M29-T02**(Project Snapshot
Analyzer — `vault/task_query.py`/`VaultAdapter.list_tasks()`/
`intelligence/` 패키지 실제 구현).

### M29-T02: Project Snapshot Analyzer

**목표**: T01 설계대로 Vault Task 문서를 읽어 진행률/상태별·
Milestone별·Owner별 집계와 활성 Agent 수를 계산하는 Snapshot
Analyzer를 구현한다.

**구현 내용**

- `vault/task_query.py`(신규) — `list_task_documents(vault_root,
  include_archived=True)`가 `14 Tasks/*.md`(+ `Archive/`)를 열거해
  frontmatter를 파싱한 `TaskDocument` 목록을 반환한다. Core Domain을
  모른다(ADR-0035와 동일 원칙). frontmatter에 `status`가 없는 문서
  (`14 Tasks/README.md`)는 자연스럽게 제외된다.
- `integration/vault_adapter.py`에 `VaultAdapter.list_tasks()`(신규
  메서드, Interface 아님) 추가 — `TaskDocumentView`(값 객체, 다른
  공개 메서드와 동일하게 `vault` 내부 타입을 노출하지 않음)로
  변환해 반환한다.
- 신규 최상위 패키지 `intelligence/`(ADR-0043 §3.22) —
  `intelligence/snapshot.py`의 `ProjectSnapshotAnalyzer`가
  `VaultAdapter`(필수)/`AgentAdapter`(선택)만 생성자로 주입받아
  `ProjectSnapshot`(총 개수/상태별·Milestone별·Owner별 집계/
  progress_ratio/active_agent_count)과 집계에 쓰인 Task 목록을
  함께 반환한다. `domain`/`interfaces`/`engines`/`vault`를 직접
  import하지 않는다.
- `tests/intelligence/test_intelligence_layering.py`(신규, `ast`
  기반) — `intelligence/`가 금지된 패키지를 직접 import하지 않고
  `integration/`의 `VaultAdapter`/`AgentAdapter`에만 의존함을
  강제한다(§8 규칙 21 회귀 방지).

**테스트**: `tests/vault/test_task_query.py`(5개), `tests/
integration_layer/test_vault_adapter.py`에 `list_tasks()` 테스트
3개 추가, `tests/intelligence/test_snapshot_analyzer.py`(5개),
`tests/intelligence/test_intelligence_layering.py`(2개) — 신규
14개. `pytest`(881개, 기존 867개 + 신규 14개), `ruff check src
tests`, `mypy src` 전부 클린.

**완료 조건 확인**: Snapshot 생성 테스트 통과(빈 Vault/상태별
집계/Milestone·Owner 집계/Agent 미주입 시 0/Archive 포함·제외 모두
검증). 새 Core Domain Interface 없음(27종 그대로), `domain.Project`/
`domain.Task` 필드 추가 없음, Core Domain(`domain`/`interfaces`/
`engines`) 코드 무변경.

코드 변경: `src/ai_workspace/vault/task_query.py`(신규),
`src/ai_workspace/integration/vault_adapter.py`(메서드 추가),
`src/ai_workspace/intelligence/__init__.py`/`snapshot.py`(신규).
다음 Task: **M29-T03**(Project Health & Risk Analyzer).

### M29-T03: Project Health & Risk Analyzer

**목표**: T02의 `ProjectSnapshotWithTasks`를 입력으로 Health
(Healthy/Warning/Critical)와 Risk를 Rule 기반으로 판단한다.

**구현 내용**

- `intelligence/health_risk.py`(신규)의 `ProjectHealthRiskAnalyzer`
  — Adapter를 직접 호출하지 않고 Snapshot 산출물(`ProjectSnapshotWithTasks`)
  만 입력으로 받는다(새로운 데이터 접근 경로 없음, T02가 이미 읽은
  값을 재사용). 세 가지 Risk를 계산한다.
  1. `stagnant_task` — IN_PROGRESS/REVIEW 상태이면서 `updated`가
     임계일(기본 7일, 생성자 파라미터로 조정 가능) 이상 지난 Task.
     ADR-0043에서 결정한 "Blocked/장기 미진행" 근사 규칙을 그대로
     구현했다. 임계일의 2배 이상 지나면 `critical`, 아니면 `warning`.
  2. `owner_overload` — 진행 중(in-progress/review) Task가 같은
     `owner`에게 임계 건수(기본 3건) 이상 배정된 경우. Core Domain
     `AgentRegistry`에는 Agent별 배정 목록 조회가 없어(T01에서
     확인한 공백), Vault Task의 `owner` 필드를 Agent/담당자 부하의
     근사치로 썼다.
  3. `milestone_stall` — 어떤 Milestone에 done/archived Task가
     하나도 없고, 그 Milestone 소속 Task 중 가장 최근 `updated`도
     임계일 이상 지난 경우(Workflow 정체 근사, ADR-0043 결정 4 —
     Vault에 Workflow 전용 문서가 없어 milestone으로 근사).
  - **"의존성 위험"은 이번 Task에서 구현하지 않았다** — Vault Task
    문서에 의존관계 필드가 없고, Core Domain `WorkflowEngine`의
    실제 의존관계는 project 전체 열거 Interface가 없어(T01에서
    이미 확인한 공백) 접근할 수 없다. 새 Interface 추가 없이는
    풀 수 없는 범위라 ADR-0043에서 예견한 대로 M29 범위 밖으로
    남긴다(필요해지면 별도 승인 대상 — Interface 변경에 해당하므로
    사용자 지시에 따라 이번엔 만들지 않는다).
  - Health 판정: Risk 중 `critical` severity가 하나라도 있으면
    `critical`, Risk가 있지만 전부 `warning`이면 `warning`, Risk가
    없으면 `healthy`(단순 Rule, 사용자 지시대로 LLM 호출 없음).

**테스트**: `tests/intelligence/test_health_risk_analyzer.py`(신규
8개 — 빈 Snapshot/정체 감지·미감지/완료 Task 제외/critical 승격/
Owner 과부하/Milestone 정체 감지·미감지). `pytest`(889개, 기존
881개 + 신규 8개), `ruff check src tests`, `mypy src` 전부 클린.

**완료 조건 확인**: Health/Risk 테스트 통과. 새 Core Domain
Interface 없음(27종 그대로), Core Domain(`domain`/`interfaces`/
`engines`) 코드 무변경, `intelligence/`는 여전히 `integration/`의
Adapter 또는 자기 자신의 다른 모듈(`snapshot`)에만 의존(§8 규칙
21 유지, `test_intelligence_layering.py` 회귀 없음 확인).

다음 Task: **M29-T04**(Project Recommendation).

### M29-T04: Project Recommendation

**목표**: T02/T03 산출물(Snapshot/Health/Risk)을 입력으로 다음
행동을 Rule 기반으로 추천한다. AI 추론/LLM 호출 없음.

**구현 내용**

- `intelligence/recommendation.py`(신규)의
  `ProjectRecommendationEngine.recommend(snapshot_result,
  health_report)` — Adapter를 직접 호출하지 않고 T02/T03 산출물만
  입력으로 받는다(새로운 데이터 접근 경로 없음). Risk 하나당
  추천 하나를 1:1로 매핑한다(새 판단 기준을 추가하지 않음).
  - `stagnant_task`(critical) → `unblock_task`("Blocked 해소
    필요", priority=high)
  - `stagnant_task`(warning) → `prioritize_task`("우선 처리해야
    할 Task", priority=medium)
  - `owner_overload` → `reassign_owner`("Agent/담당자 재배정
    추천", severity에 따라 priority high/medium)
  - `milestone_stall` → `advance_milestone`("Workflow 진행
    추천", priority=medium)
  - 전체 진행률이 임계값(기본 30%) 미만이고 Task가 1건 이상이면
    `improve_progress`("진행률 개선 제안", target="project")를
    별도로 추가한다.

**테스트**: `tests/intelligence/test_recommendation.py`(신규 8개
— Risk 없음/critical·warning stagnant/owner overload/milestone
stall/낮은 진행률 추가·Task 0건일 때 생략/Risk와 진행률 추천
동시 발생). `pytest`(897개, 기존 889개 + 신규 8개), `ruff check
src tests`, `mypy src` 전부 클린.

**완료 조건 확인**: Recommendation 테스트 통과. Rule 기반만
구현했고 AI 추론/LLM 호출 없음. 새 Core Domain Interface
없음(27종 그대로), Core Domain 코드 무변경, `intelligence/`는
여전히 자기 자신의 다른 모듈에만 의존(§8 규칙 21 유지 —
`recommendation.py`는 Adapter조차 직접 참조하지 않음).

다음 Task: **M29-T05**(Integration & Presentation).

### M29-T05: Integration & Presentation

**목표**: T02~T04(Snapshot/Health·Risk/Recommendation)를 하나로
묶어 실제로 노출한다.

**구현 내용**

- `intelligence/report.py`(신규)의 `ProjectIntelligenceService` —
  세 Analyzer를 Snapshot→Health/Risk→Recommendation 순서로 실행해
  `ProjectIntelligenceReport`를 만든다(`generate()`). 새 판단 기준을
  만들지 않고 이미 만든 Analyzer를 순서대로 배열·결과를 묶기만
  한다는 점에서 ADR-0041 Orchestrating Connector와 같은 성격의
  조합 책임이다 — 다만 `integration/` 패키지 자체에 넣지 않고
  Intelligence Layer 안에 둔다(ADR-0043이 이미 `intelligence/`를
  `integration/`과 별개 층위로 정의했으므로, Integration Layer의
  Adapter/Connector 분류 체계를 그대로 확장하지 않는다 — 대신 §8
  규칙 21의 "Adapter에만 의존" 제약을 그대로 지킨다. 이는 Layer
  Boundary 변경이 아니라 이미 승인된 경계 안에서의 조합이다).
  `render_markdown()`(순수 함수)이 리포트를 Markdown으로 렌더링하고,
  `publish()`가 `VaultAdapter.publish_intelligence_report()`를
  통해 실제로 Vault에 쓴다.
- `vault/intelligence_report.py`(신규) —
  `write_project_intelligence_report()`가 `15 Project Intelligence/
  Project Intelligence.md`에 원자적으로 전체 교체(overwrite)한다.
  기존 `VaultDocumentKind` 체계(Index append/Backlink 검증)를 쓰지
  않는다 — 이 문서는 매번 다시 계산해 덮어쓰는 **생성된 리포트**라
  다른 kind의 관례가 맞지 않는다(YAGNI로 판단, 새 `VaultDocumentKind`
  를 추가하지 않았다).
- `VaultAdapter.publish_intelligence_report()`(신규 메서드) — 위
  writer를 Integration Layer에 노출.
- **Dashboard 대신 Vault를 선택했다**(DoD는 "Dashboard 또는
  Vault" 중 하나). FastAPI Dashboard(`web/`/`runtime/dashboard/`)
  연동은 서버 기동·라우트·ViewModel까지 손대야 하는 별도 범위라,
  "M29은 추론 엔진을 과도하게 키우지 않는다"는 지시에 맞춰 이미
  이 프로젝트의 실제 운영 방식(M28 Live Task Management)과 같은
  Vault 노출을 택했다. `06 Dashboard/Dashboard Index.md`에
  [[Project Intelligence]]로의 연결 절을 추가해 Dashboard 문서
  체계와도 연결해 두었다. 향후 실제 Dashboard 연동이 필요해지면
  `ProjectIntelligenceService.generate()`(순수 조회)를 그대로
  재사용할 수 있다.
- Vault 문서: `15 Project Intelligence/README.md`(신규, 사용법),
  `15 Project Intelligence/Project Intelligence.md`(신규, 실제
  생성된 리포트 — 현재 Vault에 Task가 없어 Healthy/Risk 없음 상태로
  커밋됨), `06 Dashboard/Dashboard Index.md` 절 추가, [[Milestones
  Index]] M29 행 갱신.
- **회귀 발견 및 수정**: `vault/mapping.py`의
  `VAULT_CONTENT_DIRECTORIES`(Backlink Validation이 스캔하는 16개
  Vault 디렉터리 목록)에 `15 Project Intelligence`가 빠져 있어
  `06 Dashboard/Dashboard Index.md`의 `[[Project Intelligence]]`가
  "존재하지 않는 문서"로 오탐되는 것을 `tests/integration/
  test_m23_vault_environment_integration.py::
  test_real_vault_has_no_unexpected_broken_backlinks`(M23-Final
  회귀 방지 테스트)가 실제로 잡아냈다. `VAULT_CONTENT_DIRECTORIES`
  에 `15 Project Intelligence`를 추가해 해결(M27이 `14 Tasks`를
  추가했을 때와 같은 패턴).

**실제 결과 확인**: 임시 Vault 사본에 정체 Task 1건을 만들어
`publish()`를 실행 — Snapshot(전체 1/진행률 0%)·Health
(Critical)·Risk(`stagnant_task`+`milestone_stall`)·Recommendation
(`unblock_task`+`advance_milestone`+`improve_progress`)이 기대대로
Markdown에 렌더링됨을 확인했다. 이후 이 저장소의 실제 `vault_root`
(현재 `14 Tasks/`에 실 Task 문서 없음)에도 `publish()`를 실행해
`15 Project Intelligence/Project Intelligence.md`를 실제로
커밋했다(Healthy/Risk 없음 — 실제 현재 상태를 정직하게 반영).

**테스트**: `tests/vault/test_intelligence_report.py`(신규 2개),
`tests/integration_layer/test_vault_adapter.py`에
`publish_intelligence_report()` 테스트 1개 추가, `tests/
intelligence/test_report.py`(신규 4개). `pytest`(904개, 기존
897개 + 신규 7개), `ruff check src tests`, `mypy src` 전부 클린.

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| 실제 Dashboard 또는 Vault에서 결과 확인 | ✅ (Vault, `15 Project Intelligence/Project Intelligence.md`) |
| Architecture 문서 최신화 | ✅ (`docs/ARCHITECTURE.md` §3.22 갱신) |
| Review 완료 | Milestone Review는 M29 전체 완료 후 별도 요청 예정(사용자 지시) |

새 Core Domain Interface 없음(27종 그대로), Layer Boundary
변경 없음(§8 규칙 21 그대로, `test_intelligence_layering.py` 회귀
없음), Core Domain 코드 무변경.

**Milestone 29(Project Intelligence) T01~T05 전체 완료.** Milestone
Review는 사용자 요청에 따라 별도로 진행한다.

### Milestone 29 Review 및 완료 승인(2026-07-30)

**Review 결과 요약**(전문은 세션 기록 참고, 핵심만 기록):

| 항목 | 결과 |
|---|---|
| DoD 검증 | 11개 중 10개 완전 충족, "의존성 위험" 1건은 구조적 불가 확인 후 Deferred by Design |
| Architecture Review | `intelligence/`를 `integration/` 위 신규 Layer로 확정(ADR-0043), 데이터 소스 선택 근거가 ADR에 명시 |
| Layer Boundary Review | `test_intelligence_layering.py` 신규 + 기존 경계 테스트 회귀 없음. `vault/mapping.py` 회귀 1건 발견 즉시 수정(`15 Project Intelligence` 누락) |
| Interface Review | Core Domain 27종 무변경. Integration Layer 공개 API 확장 2건(`VaultAdapter.list_tasks()`/`publish_intelligence_report()`, Interface 아님) |
| ADR Review | ADR-0043 1건만 신규(T02~T05는 순수 구현이라 추가 ADR 없음), 기존 ADR과 충돌 없음 |
| pytest/ruff/mypy | 904 passed, ruff clean, mypy clean(166 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/Dashboard Index/`15 Project Intelligence/`) 전부 갱신 확인 |

**사용자 승인(2026-07-30)**: 아래를 명시적으로 승인함.

- M28 이후 Core Domain(27개 Interface 포함) 무변경
- Intelligence Layer를 별도 계층으로 추가해 Layer Boundary 유지
- Snapshot/Health/Risk/Recommendation을 Rule 기반으로 구현(AI 추론/LLM 호출 없음)
- Integration Layer를 통해서만 접근하도록 구성
- Architecture/ADR/문서와 테스트가 함께 갱신됨
- "의존성 위험" 미구현을 **Deferred by Design**으로 승인(Architecture Freeze를 깨거나 Interface를 추가할 필요 없음)
- 리팩터링 제안(문자열 상수/임계값/Risk 상세 링크)은 개선 아이디어로만 유지, 이번 Milestone에서 반영하지 않음 — 실제 요구사항 발생 시 별도 Milestone/ADR에서 검토

**Milestone 29(Project Intelligence) 공식 완료(Approved).** 다음은
Milestone 30(Context Intelligence) — 세부 Task는 착수 시점에 별도
제안·승인 후 정의한다.

**향후 개발 프로세스(2026-07-30 사용자 확정)**: Task 단위 중간
리뷰는 원칙적으로 생략하고, Milestone 구현 완료 후 한 번의
Milestone Review를 수행한다. 단, Core Domain 변경/Interface
추가·변경/Layer Boundary 변경/Public API 변경/ADR 수정이 필요한
경우에만 구현을 중단하고 중간 승인을 요청한다(M29부터 적용, 계속
유지).

---

## Milestone 30 — Context Intelligence

**목표**(2026-07-30 사용자 확정): 프로젝트의 현재 작업(Task/
Milestone)에 필요한 맥락(Context)을 기존 Knowledge Layer(M16)와
Intelligence Layer(M29) 정보를 기반으로 수집·정리하는 Read Only
Context Intelligence를 구현한다. **새로운 지식을 생성하지 않는다.
LLM 기반 추론도 하지 않는다** — 기존 데이터를 수집·분석·정리하는
Rule 기반 계층으로 유지한다.

**Definition of Done**

| # | 항목 |
|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 |
| 2 | 기존 Knowledge Layer Interface(`KnowledgeRepository`/`KnowledgeSearch`/`KnowledgeProvider`)만 재사용 |
| 3 | Task 또는 Milestone 기준 `ProjectContext` 생성 가능 |
| 4 | 관련 ADR/RULES/Architecture/Decision/Task/Roadmap/PRD를 연결 가능 |
| 5 | Context Freshness를 Rule 기반으로 판단 가능 |
| 6 | Context Gap(필요 문서 없음, 연결 누락 등) 탐지 가능 |
| 7 | Vault를 통해 결과 확인 가능 |
| 8 | Integration Layer를 통해서만 접근 가능 |
| 9 | Layer Boundary 테스트 통과 |
| 10 | `pytest`/`ruff`/`mypy` 통과 |
| 11 | Architecture/ADR/문서 최신화 |

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M30-T01 | Context Intelligence Architecture 설계 | **완료** |
| M30-T02 | Context Analyzer | **완료** |
| M30-T03 | Freshness & Gap Analyzer | **완료** |
| M30-T04 | Integration | **완료** |
| M30-T05 | Presentation | **완료** |

### M30-T01: Context Intelligence Architecture

**목표**: Context Intelligence의 데이터 소스, `ProjectContext` 모델,
신규 Adapter 필요 여부를 결정한다.

**결정(ADR-0044, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- 신규 Integration Layer Adapter `KnowledgeAdapter`를 추가한다 —
  기존 `KnowledgeRepository`/`KnowledgeSearch` Interface만 감싼다
  (새 Core Domain Interface 아님, 기존 Adapter 3종과 동일한 패턴).
- `FileKnowledgeRepository`는 파일 하나를 문서 하나로 통째로
  노출한다(M16 결정 그대로 유지, Interface 변경 없음). M30은 이미
  반환된 문서 텍스트를 Markdown 제목(`#`/`##`/`###`) 단위로 쪼개
  `subject`(Task/Milestone 식별자)가 언급된 항목만 추리는 방식으로
  세부 참조(예: "ADR-0043")를 얻는다 — 이 저장소가 실제로 제목에
  Milestone/Task 번호를 담는 관례를 그대로 활용, 새 지식을 만들지
  않는다.
- Freshness는 파일 mtime/git log 대신, 제목에서 추출한 Milestone
  번호와 현재 Milestone 번호의 거리로 판단한다(fresh clone 환경이라
  mtime이 무의미하고, git log는 Adapter가 "외부 시스템 하나만"
  다뤄야 한다는 ADR-0039 원칙과 충돌).
- Gap은 ADR/TASK/ARCHITECTURE 3종 Knowledge에서 subject 언급이
  0건일 때만 판정한다(RULE/PROJECT는 특정 Task마다 언급되는 것이
  자연스럽지 않은 범용 문서라 제외).
- `ProjectContext`/`ContextEntry`/`ContextQuality`/
  `ContextFreshness`/`ContextGap`은 `intelligence/`의 값 객체로
  두고 `domain/`에는 아무것도 추가하지 않는다.

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| 데이터 소스 정의 | ✅ (Knowledge Layer 6개 문서, ADR-0044) |
| Context 모델 정의 | ✅ (`ProjectContext`/`ContextEntry`/`ContextQuality` 등) |
| Adapter 필요 여부 판단 | ✅ (`KnowledgeAdapter` 신규, 기존 Interface만 감쌈) |
| ADR 작성 | ✅ (ADR-0044) |

코드 변경 없음(설계 Task). 다음 Task: **M30-T02**(Context Analyzer).

### M30-T02: Context Analyzer

**목표**: T01 설계대로 `KnowledgeAdapter`를 만들고, Knowledge 문서를
Markdown 제목 단위로 쪼개 subject가 언급된 항목을 `ProjectContext`
로 모으는 `ContextAnalyzer`를 구현한다.

**구현 내용**

- `integration/knowledge_adapter.py`(신규) — `KnowledgeAdapter`가
  `KnowledgeRepository`(필수)/`KnowledgeSearch`(선택)만 생성자로
  주입받아 `KnowledgeDocumentView`로 변환해 노출한다. Knowledge
  조회/검색 로직은 새로 만들지 않고 전부 위임한다. `integration/
  __init__.py`/`tests/integration_layer/test_connector_layering.py`
  의 `_ADAPTERS`에 등록(§8 규칙 19 대상에 신규 Adapter 편입).
- `intelligence/context.py`(신규) — `ContextAnalyzer.analyze(subject)`
  가 `KnowledgeAdapter.list_all()`이 반환한 문서를 Markdown 제목
  (`#`/`##`/`###`) 단위로 평면 분할한 뒤, subject가 언급된 (제목,
  본문) 구간만 `ContextEntry`로 채택해 `ProjectContext`를 만든다.
  **실제 구현 중 발견한 표기 불일치**: 이 저장소는 Task 문서
  제목엔 "M29-T01:", ADR 제목엔 "(Milestone 29-T01)"처럼 같은
  식별자를 문서 종류마다 다르게 표기한다 — `subject`가 "M30-T01"
  하나만 들어와도 두 표기를 모두 만들어 대조하는
  `_subject_variants()`를 추가해 실제로 놓치지 않도록 했다(설계
  단계에서 예상 못 한 디테일, 표준 Interface나 데이터 변경 없이
  Analyzer 내부 Rule로 흡수).
  `_split_sections()`는 평면 분할이라 상위 제목(`## Milestone 30`)
  본문에 하위 제목(`### M30-T01`) 텍스트가 섞이지 않는다는 한계를
  docstring에 명시했다 — 실질적으로는 하위 제목 자체가 별도 항목
  으로 매칭되어 누락은 없다.
  `intelligence/`는 여전히 `integration/`의 Adapter에만 의존한다
  (§8 규칙 21 유지, `test_intelligence_layering.py`의
  `allowed_prefixes`에 `knowledge_adapter` 추가).

**테스트**: `tests/integration_layer/test_knowledge_adapter.py`(신규
3개), `tests/intelligence/test_context_analyzer.py`(신규 5개).
`pytest`(912개, 기존 904개 + 신규 8개), `ruff check src tests`,
`mypy src` 전부 클린.

**완료 조건 확인**: 데이터 소스 정의대로 `KnowledgeAdapter` 동작
확인, `ProjectContext` 생성 테스트 통과(언급된 항목 채택/무관 항목
제외/Milestone 추출/언급 없을 때 빈 결과/`by_kind()` 필터). 새 Core
Domain Interface 없음(27종 그대로), Core Domain 코드 무변경.

다음 Task: **M30-T03**(Freshness & Gap Analyzer).

### M30-T03: Freshness & Gap Analyzer

**목표**: T02의 `ProjectContext`를 입력으로 Freshness(Healthy/
Warning)와 Gap(필요 문서 없음)을 Rule 기반으로 판단한다.

**구현 내용**

- `intelligence/context_quality.py`(신규)의
  `ContextFreshnessGapAnalyzer` — Adapter를 새로 호출하지 않고
  `ProjectContext`만 입력으로 받는다(새로운 데이터 접근 경로 없음,
  T03 health_risk.py와 동일한 설계 원칙).
  - **Gap**: ADR/TASK/ARCHITECTURE 3종 중 subject 언급이 0건인
    kind마다 `ContextGap` 1건. RULE/PROJECT는 범용 문서라 Gap
    판정에서 제외(ADR-0044 결정 그대로).
  - **Freshness**: `current_milestone`(선택 인자)이 주어지면, 매칭된
    항목의 Milestone 번호와의 거리가 임계값(기본 3) 초과일 때
    Warning. `current_milestone`을 생략하면 항상 Healthy(비교
    기준이 없으므로 판단하지 않음, 억지 판정 금지).
  - **score**: Gap 개수 기반 기본 점수(0.0~1.0)에서 Freshness가
    Warning이면 0.2 감점한다 — 새 판단 기준을 늘리지 않고 이미
    계산한 Gap/Freshness만 조합.

**테스트**: `tests/intelligence/test_context_quality.py`(신규 7개
— 전체 Gap/Gap 없음/rule·project 제외 확인/current_milestone 없을
때 Healthy/먼 Milestone Warning/가까운 Milestone Healthy/score
감점). `pytest`(919개, 기존 912개 + 신규 7개), `ruff check src
tests`, `mypy src` 전부 클린.

**완료 조건 확인**: Health/Gap 테스트 통과. 새 Core Domain
Interface 없음(27종 그대로), Core Domain 코드 무변경,
`intelligence/`는 여전히 자기 자신의 다른 모듈에만 의존(§8 규칙
21 유지 — `context_quality.py`는 Adapter조차 직접 참조하지 않음).

다음 Task: **M30-T04**(Integration).

### M30-T04: Integration

**목표**: `KnowledgeAdapter`(T02)/`ContextAnalyzer`(T02)/
`ContextFreshnessGapAnalyzer`(T03)를 하나의 진입점으로 조립한다.

**구현 내용**

- `intelligence/context_service.py`(신규)의
  `ContextIntelligenceService` — `KnowledgeAdapter`만 생성자로
  주입받아 `generate(subject, current_milestone=None)`이
  Context→Freshness/Gap 순서로 두 Analyzer를 실행해
  `ProjectContextReport`(Context+Quality)를 만든다. 새 판단 기준을
  만들지 않고 이미 만든 두 Analyzer를 조합만 한다(M29 `report.py`
  의 조합 방식과 동일).

**테스트**: `tests/intelligence/test_context_service.py`(신규 3개
— Context/Quality 결합 확인, subject 미언급 시 Gap 3종 전부, 인접
Milestone Healthy). `pytest`(922개, 기존 919개 + 신규 3개), `ruff
check src tests`, `mypy src` 전부 클린.

**완료 조건 확인**: `KnowledgeAdapter` 연결 확인, Service 구성
테스트 통과. 새 Core Domain Interface 없음(27종 그대로), Core
Domain 코드 무변경, §8 규칙 21 유지.

다음 Task: **M30-T05**(Presentation).

### M30-T05: Presentation

**목표**: T04의 `ContextIntelligenceService`를 실제로 Vault에
노출한다.

**구현 내용**

- `intelligence/context_service.py`(T04에서 확장) — `render_markdown()`
  (순수 함수)이 `ProjectContextReport`를 Markdown으로 렌더링하고,
  `publish()`가 `VaultAdapter.publish_project_context()`(신규
  메서드)를 통해 실제로 Vault에 쓴다. `vault_adapter`를 주입하지
  않고 `publish()`를 호출하면 `ValueError`.
- `vault/context_report.py`(신규) — `write_project_context_report()`
  가 `15 Project Intelligence/Project Context.md`에 원자적으로
  전체 교체(overwrite)한다(`vault/intelligence_report.py`, M29-T05
  와 동일한 패턴, 같은 폴더를 재사용해 새 최상위 폴더를 만들지
  않았다).
- `VaultAdapter.publish_project_context()`(신규 메서드) — 위 writer
  를 Integration Layer에 노출.
- **Dashboard 대신 Vault를 선택**(M29-T05와 동일한 이유 — DoD는
  "Vault를 통해 결과 확인"만 요구, FastAPI 연동은 범위 확장이라
  보류). `06 Dashboard/Dashboard Index.md`에 [[Project Context]]
  연결 절을 추가했다.
- Vault 문서: `15 Project Intelligence/README.md`(두 리포트 설명
  으로 갱신), `15 Project Intelligence/Project Context.md`(신규,
  실제 생성된 리포트), `06 Dashboard/Dashboard Index.md`,
  [[Milestones Index]] M30 행 갱신.

**실제 결과 확인 및 버그 발견·수정**: 이 저장소의 실제 vault_root에
`ContextIntelligenceService.publish("M30-T05", current_milestone=30)`
를 실행해 검증하던 중, `docs/ARCHITECTURE.md` 최상단 `# ARCHITECTURE
— AI Workspace` 절처럼 본문 한 줄에 여러 Milestone 이력이 나열된
경우 Freshness가 실제로는 최근(M30)인데도 본문 "첫 Milestone 언급"
(예: "Milestone 1~22")을 잘못 골라 Warning으로 오판하는 버그를
발견했다. `intelligence/context.py`의 Milestone 추출을 "본문 전체
첫 언급"에서 "subject 언급 위치와 텍스트 거리가 가장 가까운 언급"
으로 고쳐 해결(`_extract_milestone_near_subject()`,
`_all_milestone_matches()` 신규) — 회귀 방지 테스트
(`test_analyze_ignores_unrelated_milestone_mentions_before_subject`)
를 추가했다. 수정 후 실제 리포트가 Freshness Healthy로 정정됨을
확인하고 Vault에 커밋했다.

**테스트**: `tests/vault/test_context_report.py`(신규 2개), `tests/
integration_layer/test_vault_adapter.py`에 `publish_project_context()`
테스트 1개 추가, `tests/intelligence/test_context_service.py`에
`render_markdown()`/`publish()` 테스트 3개 추가, `tests/intelligence/
test_context_analyzer.py`에 Milestone 오판 회귀 방지 테스트 1개
추가. `pytest`(929개, 기존 922개 + 신규 7개), `ruff check src
tests`, `mypy src` 전부 클린.

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| Vault를 통해 결과 확인 가능 | ✅ (`15 Project Intelligence/Project Context.md`) |
| Architecture 문서 최신화 | ✅ (`docs/ARCHITECTURE.md` §3.23 갱신) |
| Review 완료 | Milestone Review는 M30 전체 완료 후 별도 요청 예정(M29와 동일한 프로세스) |

새 Core Domain Interface 없음(27종 그대로), Layer Boundary 변경
없음(§8 규칙 21 그대로), Core Domain 코드 무변경.

**Milestone 30(Context Intelligence) T01~T05 전체 완료.** Milestone
Review는 사용자 요청에 따라 별도로 진행한다.

### Milestone 30 Review

**Review 결과 요약**

| 항목 | 결과 |
|---|---|
| DoD 검증 | 11개 항목 전부 충족 |
| Architecture Review | `intelligence/context*.py`를 M29 Intelligence Layer와 같은 계층에 추가(ADR-0044), Knowledge Layer(M16) 재사용 근거가 ADR에 명시 |
| Layer Boundary Review | `test_intelligence_layering.py`(allowed_prefixes에 `knowledge_adapter` 추가) + `test_connector_layering.py`(`_ADAPTERS`에 `knowledge_adapter` 추가) 모두 회귀 없음 |
| Interface Review | Core Domain 27종 무변경(`git diff --stat origin/main...` 확인). Integration Layer 신규 Adapter 1건(`KnowledgeAdapter`, 기존 `KnowledgeRepository`/`KnowledgeSearch`만 감쌈, Interface 아님), `VaultAdapter` 확장 1건(`publish_project_context()`) |
| ADR Review | ADR-0044 1건만 신규(T02~T05는 순수 구현), 기존 ADR과 충돌 없음 |
| pytest/ruff/mypy | 929 passed, ruff clean, mypy clean(171 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/Dashboard Index/`15 Project Intelligence/`) 전부 갱신 확인 |

**실제 발견·수정한 버그**: T05 실제 검증 중, `docs/ARCHITECTURE.md`
최상단 절처럼 본문 한 줄에 여러 Milestone 이력이 나열되면 Freshness
가 "본문 첫 Milestone 언급"을 잘못 골라 최신 항목도 Warning으로
오판하는 문제를 발견 — "subject와 텍스트 거리가 가장 가까운 언급"
으로 추출 방식을 고치고 회귀 방지 테스트를 추가했다(상세는 위
M30-T05 항목).

**개선 여지(참고용, 이번에 처리하지 않음)**: (1) Milestone 추출이
정규식 기반 근사라 특이한 표기(예: "M30~32")는 놓칠 수 있다. (2)
`_split_sections()`가 평면 분할이라 계층적 문맥(상위 절 전체가
관련된 경우)을 놓칠 수 있다 — 지금은 하위 제목이 대신 매칭돼
실질적 누락은 적다. (3) Context Quality Score 산식(Gap 개수 +
Freshness 감점)은 단순 근사이며 가중치 근거가 없다. 전부 실제
요구사항이 생기면 별도 Milestone/ADR에서 재검토한다.

**사용자 승인(2026-07-30)**: Scope 준수/Architecture 유지/Interface
유지/Rule 기반 구현/Documentation 완료/Test 통과를 모두 만족함을
확인해 **Milestone 30(Context Intelligence) 공식 완료(Approved)**.
"M28(Live Task Management & Integration)→M29(Project Intelligence)
→M30(Context Intelligence)"로 이어지며, AI Workspace가 단순 작업
관리 도구를 넘어 프로젝트 상태를 이해하고 현재 작업에 필요한 맥락
까지 제공하는 기반 계층을 갖췄다는 점에서 프로젝트 차원의 의미가
있음을 사용자가 확인함 — 이후 Session Resume/AI Agent 협업/장기
메모리 활용 등 상위 기능의 토대가 된다.

**다음은 Milestone 31(Capability Intelligence)** — 세부 Task는
착수 시점에 별도 제안·승인 후 정의한다.

---

## Milestone 31 — Capability Intelligence

**목표**(2026-07-30 사용자 확정 — "M31을 M29/M30과 동일하게 진행"):
이 시스템이 정의한 `AgentCapability`(11종) 대비, 실제로 활성 Agent가
커버하는 Capability가 무엇인지 정리하는 Read Only Capability
Intelligence를 구현한다. M29/M30과 동일한 조건 — **새로운 지식을
생성하지 않는다. LLM 기반 추론도 하지 않는다** — 기존 데이터를
수집·분석·정리하는 Rule 기반 계층으로 유지한다.

**Definition of Done**

| # | 항목 |
|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 |
| 2 | 기존 Agent Layer Interface(`AgentManager`/`AgentRegistry`/`AgentScheduler`)만 재사용 |
| 3 | 활성 Agent를 Capability/Role별로 집계 가능 |
| 4 | 정의된 Capability 대비 커버리지(Coverage)를 Rule 기반으로 판단 가능 |
| 5 | Capability Gap(활성 Agent가 0명인 Capability) 탐지 가능 |
| 6 | Vault를 통해 결과 확인 가능 |
| 7 | Integration Layer를 통해서만 접근 가능 |
| 8 | Layer Boundary 테스트 통과 |
| 9 | `pytest`/`ruff`/`mypy` 통과 |
| 10 | Architecture/ADR/문서 최신화 |

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M31-T01 | Capability Intelligence Architecture 설계 | **완료** |
| M31-T02 | Capability Snapshot Analyzer | **완료** |
| M31-T03 | Coverage & Gap Analyzer | **완료** |
| M31-T04 | Integration | **완료** |
| M31-T05 | Presentation | **완료** |

### M31-T01: Capability Intelligence Architecture

**목표**: Capability Intelligence의 데이터 소스, 모델, 신규
Adapter/Interface 필요 여부를 결정한다.

**결정(ADR-0045, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- 새 Adapter를 만들지 않는다 — 기존 `AgentAdapter`(M28,
  `AgentManager`/`AgentRegistry`/`AgentScheduler` 3종 Interface를
  이미 감쌈)를 확장한다. `list_active_agent_capabilities()`(활성
  Agent를 Adapter 전용 DTO `AgentCapabilityView`로 열거)와
  `known_capabilities()`(정의된 `AgentCapability` 11종을 문자열
  카탈로그로 노출) 두 메서드만 추가한다(M30이 `VaultAdapter`에
  `publish_project_context()`를 추가한 것과 같은 확장 방식).
- 집계(Snapshot)와 판단(Gap)을 분리한다(M29/M30과 동일한 2단
  Analyzer 구조) — Snapshot Analyzer는 Adapter 값만 읽어 집계,
  Gap Analyzer는 Snapshot만 입력으로 받아 판단한다.
- Coverage 등급은 healthy/warning/critical이 아니라
  none/partial/full을 쓴다 — 활성 Agent 0명은 이 저장소가 아직
  Agent 프로세스를 상시 구동하지 않는 워크숍 단계의 자연스러운
  상태이지 시스템 이상이 아니기 때문이다(M29 `active_agent_count`
  도 항상 0으로 관찰됨, 매번 "Critical"로 표시하면 리포트 신뢰도만
  떨어진다).
- Vault Task 문서의 `owner` 필드(자유 텍스트)는 Capability 수요
  신호로 쓰지 않는다 — 고정된 명명 규칙이 없어 안정적으로 매핑할
  근거가 없고, 새 명명 관례를 이번에 발명하는 것은 "새 지식/판단
  기준을 만들지 않는다"는 원칙과 충돌한다.
- `AgentCapabilitySnapshot`/`CapabilityGap`/`CapabilityCoverage`/
  `CapabilityGapReport`는 `intelligence/`의 값 객체로 두고
  `domain/`에는 아무것도 추가하지 않는다.

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| 데이터 소스 정의 | ✅ (기존 `AgentAdapter`, ADR-0045) |
| Capability 모델 정의 | ✅ (`AgentCapabilitySnapshot`/`CapabilityGap`/`CapabilityCoverage` 등) |
| Adapter 필요 여부 판단 | ✅ (신규 Adapter 없음, 기존 `AgentAdapter` 확장만) |
| ADR 작성 | ✅ (ADR-0045) |

코드 변경 없음(설계 결론만 확정). 다음 Task: **M31-T02**(Capability
Snapshot Analyzer).

### M31-T02: Capability Snapshot Analyzer

**목표**: T01 설계대로 `AgentAdapter`를 확장하고, 활성 Agent를
Capability/Role별로 집계하는 `CapabilitySnapshotAnalyzer`를
구현한다.

**구현 내용**

- `integration/agent_adapter.py`(확장) — `AgentCapabilityView`
  (신규 dataclass, `agent_id`/`role`/`capabilities`/`status`를
  모두 문자열/frozenset[str]로만 노출, `domain.agent.Agent`를
  직접 반환하지 않음)와 `list_active_agent_capabilities()`/
  `known_capabilities()` 두 메서드를 추가했다. `known_capabilities()`
  는 `AgentCapability` enum 값을 문자열로 나열만 할 뿐 집계·판단은
  하지 않는다(Adapter는 비즈니스 로직을 갖지 않는다, ADR-0039
  원칙 유지).
- `intelligence/capability.py`(신규) — `CapabilitySnapshotAnalyzer.
  analyze()`가 `AgentAdapter.list_active_agent_capabilities()`/
  `known_capabilities()`만 읽어 `AgentCapabilitySnapshot`(활성
  Agent 수 + Capability별/Role별 집계 + 정의된 Capability 카탈로그)
  을 만든다. `intelligence/`는 여전히 `integration/`의 Adapter에만
  의존한다(§8 규칙 21 유지 — `agent_adapter`는 이미
  `test_intelligence_layering.py`의 `allowed_prefixes`에 M29부터
  등록돼 있어 추가 변경 불필요).

**테스트**: `tests/integration_layer/test_agent_adapter.py`에 신규
메서드 테스트 3개 추가, `tests/intelligence/test_capability_analyzer.py`
(신규 3개). `pytest`(935개, 기존 929개 + 신규 6개), `ruff check src
tests`, `mypy src` 전부 클린.

**완료 조건 확인**: 데이터 소스 정의대로 `AgentAdapter` 확장 동작
확인, `AgentCapabilitySnapshot` 생성 테스트 통과(Capability/Role
집계/카탈로그 전체 포함/활성 Agent 없을 때 전부 0). 새 Core Domain
Interface 없음(27종 그대로), Core Domain 코드 무변경.

다음 Task: **M31-T03**(Coverage & Gap Analyzer).

### M31-T03: Coverage & Gap Analyzer

**목표**: T02의 `AgentCapabilitySnapshot`을 입력으로 Coverage
(none/partial/full)와 Gap(활성 Agent가 0명인 Capability)을 Rule
기반으로 판단한다.

**구현 내용**

- `intelligence/capability_gap.py`(신규)의 `CapabilityGapAnalyzer`
  — Adapter를 새로 호출하지 않고 `AgentCapabilitySnapshot`만
  입력으로 받는다(새로운 데이터 접근 경로 없음, `health_risk.py`/
  `context_quality.py`와 동일한 설계 원칙).
  - **Gap**: `by_capability`에서 집계 0인 Capability마다
    `CapabilityGap` 1건(Capability 이름 오름차순 정렬).
  - **Coverage**: `(정의된 Capability 수 − Gap 수) / 정의된
    Capability 수`를 비율로 계산해 0이면 none, 1이면 full, 그
    사이면 partial.

**테스트**: `tests/intelligence/test_capability_gap.py`(신규 4개
— 전체 Coverage/부분 Coverage+Gap 목록/활성 Agent 0명일 때 전부
Gap/Gap 정렬 확인). `pytest`(939개, 기존 935개 + 신규 4개), `ruff
check src tests`, `mypy src` 전부 클린.

**완료 조건 확인**: Coverage/Gap 테스트 통과. 새 Core Domain
Interface 없음(27종 그대로), Core Domain 코드 무변경,
`intelligence/`는 여전히 자기 자신의 다른 모듈에만 의존(§8 규칙
21 유지 — `capability_gap.py`는 Adapter조차 직접 참조하지 않음).

다음 Task: **M31-T04**(Integration).

### M31-T04: Integration

**목표**: `AgentAdapter`(T02)/`CapabilitySnapshotAnalyzer`(T02)/
`CapabilityGapAnalyzer`(T03)를 하나의 진입점으로 조립한다.

**구현 내용**

- `intelligence/capability_service.py`(신규)의
  `CapabilityIntelligenceService` — `AgentAdapter`만 생성자로
  주입받아 `generate()`가 Snapshot→Coverage/Gap 순서로 두 Analyzer
  를 실행해 `CapabilityIntelligenceReport`(Snapshot+GapReport)를
  만든다. 새 판단 기준을 만들지 않고 이미 만든 두 Analyzer를
  조합만 한다(M29 `report.py`/M30 `context_service.py`의 조합
  방식과 동일).

**테스트**: `tests/intelligence/test_capability_service.py`에
`generate()` 조합 테스트 2개 추가. `pytest`(941개, 기존 939개 +
신규 2개), `ruff check src tests`, `mypy src` 전부 클린.

**완료 조건 확인**: `AgentAdapter` 연결 확인, Service 구성 테스트
통과. 새 Core Domain Interface 없음(27종 그대로), Core Domain 코드
무변경, §8 규칙 21 유지.

다음 Task: **M31-T05**(Presentation).

### M31-T05: Presentation

**목표**: T04의 `CapabilityIntelligenceService`를 실제로 Vault에
노출한다.

**구현 내용**

- `intelligence/capability_service.py`(T04에서 확장) —
  `render_markdown()`(순수 함수)이 `CapabilityIntelligenceReport`
  를 Markdown으로 렌더링하고, `publish()`가 `VaultAdapter.
  publish_capability_report()`(신규 메서드)를 통해 실제로 Vault에
  쓴다. `vault_adapter`를 주입하지 않고 `publish()`를 호출하면
  `ValueError`(M29-T05/M30-T05와 동일한 계약).
- `vault/capability_report.py`(신규) — `write_capability_report()`
  가 `15 Project Intelligence/Capability Intelligence.md`에
  원자적으로 전체 교체(overwrite)한다(`vault/context_report.py`,
  M30-T05와 동일한 패턴, 같은 폴더를 재사용해 새 최상위 폴더를
  만들지 않았다).
- `VaultAdapter.publish_capability_report()`(신규 메서드) — 위
  writer를 Integration Layer에 노출.

**테스트**: `tests/vault/test_capability_report.py`(신규 2개),
`tests/integration_layer/test_vault_adapter.py`에
`publish_capability_report()` 테스트 1개 추가, `tests/intelligence/
test_capability_service.py`에 `publish()`/`render_markdown()` 테스트
3개 추가. `pytest`(947개, 기존 941개 + 신규 6개), `ruff check src
tests`, `mypy src` 전부 클린.

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| Vault를 통해 결과 확인 가능 | ✅ (`15 Project Intelligence/Capability Intelligence.md`) |
| Architecture 문서 최신화 | ✅ (`docs/ARCHITECTURE.md` §3.24 신규) |
| Review 완료 | Milestone Review는 M31 전체 완료 후 별도 요청 예정(M29/M30과 동일한 프로세스) |

새 Core Domain Interface 없음(27종 그대로), Layer Boundary 변경
없음(§8 규칙 21 그대로), Core Domain 코드 무변경.

**Milestone 31(Capability Intelligence) T01~T05 전체 완료.**
Milestone Review는 사용자 요청에 따라 별도로 진행한다.

### Milestone 31 Review

**Review 결과 요약**

| 항목 | 결과 |
|---|---|
| DoD 검증 | 10개 항목 전부 충족 |
| Architecture Review | `intelligence/capability*.py`를 M29/M30 Intelligence Layer와 같은 계층에 추가(ADR-0045), Agent Layer(M28) 재사용 근거가 ADR에 명시 |
| Layer Boundary Review | `test_intelligence_layering.py`(신규 파일이 `agent_adapter`만 참조, M29부터 이미 허용됨 — 변경 불필요) 회귀 없음 |
| Interface Review | Core Domain 27종 무변경. Integration Layer 신규 Adapter 없음, `AgentAdapter` 확장 1건(`list_active_agent_capabilities()`/`known_capabilities()`), `VaultAdapter` 확장 1건(`publish_capability_report()`) |
| ADR Review | ADR-0045 1건만 신규, 기존 ADR과 충돌 없음 |
| pytest/ruff/mypy | 947 passed, ruff clean, mypy clean(175 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/Dashboard Index/`15 Project Intelligence/`) 전부 갱신 확인 |

**개선 여지(참고용, 이번에 처리하지 않음)**: (1) `AgentRegistry`가
In-Memory 전용이라 실제 Agent 프로세스가 떠 있지 않으면
`활성 Agent 수`가 항상 0으로 관찰된다(M29 `active_agent_count`와
동일한 이미 알려진 한계) — Coverage가 항상 none으로 보고될 수
있다는 뜻이며, 실제 Agent 상시 구동 체계가 생기면 재검토 대상이다.
(2) Vault Task `owner` 필드를 Capability 수요 신호로 쓰지 않기로
했으므로, "필요한데 없는 Capability"(수요 대비 공급 Gap)가 아니라
"정의됐는데 활성 Agent가 없는 Capability"(공급 자체의 Gap)만
판정한다 — 수요 신호가 필요해지면 별도 ADR 대상이다.

**사용자 승인(2026-07-30)**: Scope 준수/Architecture 유지/Interface
유지/Rule 기반 구현/Documentation 완료/Test 통과를 모두 만족함을
확인해 **Milestone 31(Capability Intelligence) 공식 완료(Approved)**.
"M29(Project Intelligence)→M30(Context Intelligence)→M31(Capability
Intelligence)"로 이어지며, AI Workspace가 프로젝트 상태/현재 작업
맥락에 이어 "이 시스템이 실제로 수행할 수 있는 능력"까지 이해하는
기반 계층을 갖췄다는 점에서 프로젝트 차원의 의미가 있음을 사용자가
확인함.

## Milestone 32 — Intelligence Synthesis

**목표**(2026-07-30 사용자 확정 — "M32는 기능 추가보다는 Intelligence
Layer의 통합 계층(Integration at the Intelligence Layer)을 완성하는
Milestone"): M29(Project Intelligence)/M30(Context Intelligence)/
M31(Capability Intelligence)이 각각 독립적으로 계산한 리포트를
새로운 데이터 소스나 판단 기준 없이 하나의 `IntelligenceOverview`로
합성한다. M29~M31과 동일한 조건 — **새로운 지식을 생성하지 않는다.
LLM 기반 추론도 하지 않는다** — 이미 완성된 세 Service를 조합하는
Rule 기반 계층으로 유지한다.

**Definition of Done**

| # | 항목 |
|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 |
| 2 | 새 Interface 0개 |
| 3 | 새 Integration Layer Adapter 0개(`VaultAdapter` 메서드 1개만 확장) |
| 4 | `intelligence/synthesis*.py`는 오직 `intelligence/report.py`/`context_service.py`/`capability_service.py`(기존 3개 Service)에만 의존 |
| 5 | Rule 기반(집계·정렬만)으로 동작, LLM 호출 없음 |
| 6 | `15 Project Intelligence/Intelligence Overview.md`에 세 리포트의 등급 + 통합 Finding 목록 노출 |
| 7 | 기존 M29/M30/M31 pytest 회귀 없음 + 신규 테스트 통과 |
| 8 | `pytest`/`ruff`/`mypy` 통과 |
| 9 | Architecture/ADR/문서 최신화 |

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M32-T01 | Intelligence Synthesis 설계 | **완료** |
| M32-T02 | Synthesis Analyzer | **완료** |
| M32-T03 | Integration + Presentation | **완료** |
| M32-T04 | End-to-End 검증 + 문서화 + Milestone Review | **완료** |

### M32-T01: Intelligence Synthesis 설계

**목표**: Synthesis의 입력·출력 계약과 §8 규칙 21과의 관계를
결정한다.

**결정(ADR-0046, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- 새 Adapter/Interface를 만들지 않는다 — `intelligence/synthesis.py`
  의 `IntelligenceSynthesisAnalyzer`는 이미 생성된 세 리포트
  (`ProjectIntelligenceReport`/`ProjectContextReport`/
  `CapabilityIntelligenceReport`)만 입력으로 받는 순수 함수다.
- §8 규칙 21("`intelligence/`의 Analyzer는 `integration/`의
  Adapter에만 의존")은 변경 없이 그대로 적용된다 — Synthesis는
  Adapter가 아니라 같은 `intelligence/` 계층의 다른 Service를
  조합하므로 애초에 이 규칙의 금지 대상이 아니다.
  `tests/intelligence/test_intelligence_layering.py`를 코드 변경
  없이 그대로 실행해 위반이 없음을 확인했다(사전 조사 결과).
- 집계(Synthesis Analyzer)와 조합(Synthesis Service)을 분리한다
  (M29/M30/M31과 동일한 2단 구조).
- 결과는 같은 Vault 폴더에 새 파일(`Overview.md`)로 노출한다 — 새
  최상위 Vault 폴더를 만들지 않는다.

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| 입력/출력 계약 정의 | ✅ (세 리포트 → `IntelligenceOverview`) |
| §8 규칙 21 위반 여부 확인 | ✅ (위반 없음, 규칙 변경 불필요) |
| ADR 작성 | ✅ (ADR-0046) |

코드 변경 없음(설계 결론만 확정). 다음 Task: **M32-T02**(Synthesis
Analyzer).

### M32-T02: Synthesis Analyzer

**목표**: T01 설계대로 세 리포트를 조합해 `IntelligenceOverview`를
만드는 `IntelligenceSynthesisAnalyzer`를 구현한다.

**구현 내용**

- `intelligence/synthesis.py`(신규) — `SynthesizedFinding`/
  `IntelligenceOverview`(신규 값 객체)와 `IntelligenceSynthesisAnalyzer.
  analyze()`가 `ProjectIntelligenceReport.health_report.risks`/
  `ProjectContextReport.quality.gaps`/
  `CapabilityIntelligenceReport.gap_report.gaps`를 하나의
  `SynthesizedFinding` 목록으로 옮겨 담고(target 기준 정렬), 세
  리포트의 등급(Health/Freshness/Coverage)을 그대로 노출한다. 새
  우선순위 알고리즘·새 임계값을 만들지 않는다.

**테스트**: `tests/intelligence/test_synthesis.py`(신규 3개 — 세
리포트 등급 조합/Finding 병합/Critical 등급 반영). `pytest`(957개,
기존 954개 + 신규 3개), `ruff check src tests`, `mypy` 전부 클린.

**완료 조건 확인**: `IntelligenceOverview` 생성 테스트 통과. 새 Core
Domain Interface 없음(27종 그대로), Core Domain 코드 무변경,
`intelligence/`는 여전히 자기 자신의 다른 모듈에만 의존(§8 규칙 21
그대로 — `synthesis.py`는 Adapter조차 직접 참조하지 않는다).

다음 Task: **M32-T03**(Integration + Presentation).

### M32-T03: Integration + Presentation

**목표**: `ProjectIntelligenceService`/`ContextIntelligenceService`/
`CapabilityIntelligenceService`(T02가 아니라 M29/M30/M31의 기존
Service)와 `IntelligenceSynthesisAnalyzer`(T02)를 하나의 진입점으로
조립하고, 실제로 Vault에 노출한다.

**구현 내용**

- `intelligence/synthesis_service.py`(신규)의
  `IntelligenceSynthesisService` — 세 Service를 생성자로 주입받아
  `generate()`가 순서대로(Project→Context→Capability) 실행한 뒤
  `IntelligenceSynthesisAnalyzer.analyze()`에 넘긴다. `render_markdown()`
  (순수 함수)/`publish()`가 `VaultAdapter.
  publish_intelligence_overview()`(신규 메서드)를 통해 실제로
  Vault에 쓴다. `vault_adapter`를 주입하지 않고 `publish()`를
  호출하면 `ValueError`(M29-T05/M30-T05/M31-T05와 동일한 계약).
- `vault/intelligence_overview.py`(신규) —
  `write_intelligence_overview_report()`가 `15 Project
  Intelligence/Overview.md`에 원자적으로 전체 교체(overwrite)한다
  (`vault/capability_report.py`, M31-T05와 동일한 패턴).
- `VaultAdapter.publish_intelligence_overview()`(신규 메서드) — 위
  writer를 Integration Layer에 노출.

**테스트**: `tests/intelligence/test_synthesis_service.py`(신규 5개
— 세 Service 조합/`publish()` 예외/Vault 기록/Markdown 섹션 확인).
`pytest`(954개 → 이 Task까지 신규 7개 누적 포함), `ruff check src
tests`, `mypy` 전부 클린.

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| Vault를 통해 결과 확인 가능 | ✅ (`15 Project Intelligence/Intelligence Overview.md`) |
| Architecture 문서 최신화 | ✅ (`docs/ARCHITECTURE.md` §3.25 신규) |
| Review 완료 | Milestone Review는 M32-T04에서 진행 |

새 Core Domain Interface 없음(27종 그대로), 새 Integration Layer
Adapter 없음(`VaultAdapter` 확장 1건), Layer Boundary 변경 없음(§8
규칙 21 그대로), Core Domain 코드 무변경.

다음 Task: **M32-T04**(End-to-End 검증 + 문서화 + Milestone
Review).

### M32-T04: End-to-End 검증 + 문서화 + Milestone Review

**목표**: 전체 스택(세 Service→Synthesis→Vault) 통합 검증과 문서
갱신을 마무리하고 Milestone Review를 작성한다.

**구현 내용**

- 실제 저장소 Vault(`15 Project Intelligence/`)를 대상으로
  `IntelligenceSynthesisService.publish()`를 실행해
  `Overview.md`가 실제로 생성됨을 확인(Project Health: Healthy,
  Context Freshness/Capability Coverage 등급과 통합 Finding 목록
  포함).
- `docs/ARCHITECTURE.md` §3.25(신규)/상단 상태 갱신, `.ai/
  DECISIONS.md`(ADR-0046 신규), `.ai/TASKS.md`(본 절), Vault(ADR
  Index/Milestones Index) 갱신.

**테스트**: 전체 `pytest`/`ruff`/`mypy` 재실행으로 회귀 없음 확인.

**완료 조건 확인**: DoD 9개 항목 전부 충족.

**Milestone 32(Intelligence Synthesis) T01~T04 전체 완료.**

### Milestone 32 Review

**Review 결과 요약**

| 항목 | 결과 |
|---|---|
| DoD 검증 | 9개 항목 전부 충족 |
| Architecture Review | `intelligence/synthesis*.py`를 M29/M30/M31 Intelligence Layer와 같은 계층에 추가(ADR-0046), M29~M31 Service 3개를 조합하는 근거가 ADR에 명시 |
| Layer Boundary Review | `test_intelligence_layering.py`를 코드 변경 없이 그대로 실행해 §8 규칙 21 위반 없음을 확인(신규 Adapter 참조 자체가 없음) |
| Interface Review | Core Domain 27종 무변경. Integration Layer 신규 Adapter 없음, `VaultAdapter` 확장 1건(`publish_intelligence_overview()`) |
| ADR Review | ADR-0046 1건만 신규, 기존 ADR과 충돌 없음(§8 규칙 21 변경 없음을 ADR 안에서도 명시) |
| pytest/ruff/mypy | 954 passed, ruff clean, mypy clean(178 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/`15 Project Intelligence/Intelligence Overview.md`) 전부 갱신 확인 |

**개선 여지(참고용, 이번에 처리하지 않음)**: M29(`active_agent_count`)/
M31(Coverage)이 이미 겪은 "활성 Agent 0명" 한계가 Overview에도 그대로
드러난다(Capability Finding이 항상 채워짐) — 실제 Agent 상시 구동
체계가 생기면 Overview도 함께 재검토 대상이다. Synthesis는 이 한계를
새로 만들지 않고 그대로 승계했을 뿐이다.

**사용자 승인(2026-07-30)**: Scope 준수/Architecture 유지/Interface
유지/Layer Boundary 유지/Rule 기반 구현/Documentation 완료/Test
완료를 모두 만족함을 확인해 **Milestone 32(Intelligence Synthesis)
공식 완료(Approved)**. "M29(Project Intelligence)→M30(Context
Intelligence)→M31(Capability Intelligence)→M32(Intelligence
Synthesis)"로 이어지며, 각 Milestone이 독립적인 책임을 가지면서도
M32를 통해 하나의 일관된 Intelligence Layer로 통합되었다는 점에서
프로젝트 차원의 의미가 있음을 사용자가 확인함. `15 Project
Intelligence/Intelligence Overview.md`가 공식 결과로 확정된다.

**다음 단계(사용자 코멘트)**: 이 시점부터는 Intelligence Layer를
"구축"하는 단계보다, 이를 활용하는 상위 기능(Session Resume/
Workflow Intelligence/Agent Orchestration/Automation 등)으로
확장하는 것이 자연스러운 다음 단계다 — Milestone 33 세부 Task는
착수 시점에 별도 제안·승인 후 정의한다.

---

## Milestone 33 — Session Resume

**목표**(2026-07-30 사용자 확정 — "M33은 새로운 Intelligence를
계산하지 않는다"): 새 세션이 시작될 때 "지금 무엇을 하고 있었는가"를
자동 복원하는 Read Only Session Resume를 구현한다. M29(Project)/
M30(Context)/M31(Capability) Intelligence와 M32(Intelligence
Overview)를 그대로 활용하고, "현재 작업" 판정 규칙 1개만 새로
더한다. **새로운 판단·새로운 Intelligence·LLM 추론을 하지 않는다.**

**Definition of Done**

| # | 항목 |
|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 |
| 2 | 새 Interface 0개 |
| 3 | 새 Integration Layer Adapter 0개(`VaultAdapter` 메서드 1개만 확장) |
| 4 | `intelligence/session_resume*.py`는 `VaultAdapter`(기존)와 `intelligence/`의 기존 Service/Analyzer(M29~M32)에만 의존 |
| 5 | "현재 작업" 판정은 이미 있는 `status`/`updated` 값을 읽는 Rule 1개뿐 — 새 지표·점수 없음 |
| 6 | `15 Project Intelligence/Session Resume.md`에 현재 Milestone/Task, Project 상태, 관련 Context, Capability 상태, 다음 작업 노출 |
| 7 | 활성 Task가 없을 때도 예외 없이 정상 표시 |
| 8 | 기존 M29~M32 pytest 회귀 없음 + 신규 테스트 통과 |
| 9 | `pytest`/`ruff`/`mypy` 통과 |
| 10 | Architecture/ADR/문서 최신화 |

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M33-T01 | Session Resume 설계 | **완료** |
| M33-T02 | Current Work Selector | **완료** |
| M33-T03 | Session Resume Service(Integration) | **완료** |
| M33-T04 | Presentation + E2E 검증 + 문서화 + Milestone Review | **완료** |

### M33-T01: Session Resume 설계

**목표**: 데이터 소스, "현재 작업" 판정 Rule, §8 규칙 21과의 관계를
결정한다.

**결정(ADR-0047, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- 새 Adapter/Interface를 만들지 않는다 — "현재 작업" 판정은
  `VaultAdapter.list_tasks()`(M29부터 존재)가 이미 노출한 값에서
  고르는 순수 선택 로직이다.
- M8 세션 연속성(Agent 실행 컨텍스트 복원)과는 Interface·Layer가
  겹치지 않는 별개 기능이다 — M33은 사람이 읽는 보고서를
  Intelligence Layer에서 만든다.
- `SessionResumeService`는 `VaultAdapter` + M29~M31 Service 3개 +
  M32 `IntelligenceSynthesisAnalyzer`(Service가 아니라 Analyzer만
  재사용)를 조합한다 — M29 `ProjectIntelligenceReport.
  recommendations`가 Overview 밖에 있어 직접 필요하기 때문이다.
- "다음 작업"은 M29 Recommendation을 그대로 노출한다(새 추천 로직
  없음).
- CLI 노출·자동 트리거는 범위 밖(M29~M32와 동일하게 Vault 노출까지).

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| 데이터 소스 정의 | ✅ (기존 `VaultAdapter`/M29~M32 Service, ADR-0047) |
| "현재 작업" 판정 Rule 정의 | ✅ (활성 상태 + 최신 updated) |
| Adapter 필요 여부 판단 | ✅ (신규 Adapter 없음) |
| ADR 작성 | ✅ (ADR-0047) |

코드 변경 없음(설계 결론만 확정). 다음 Task: **M33-T02**(Current
Work Selector).

### M33-T02: Current Work Selector

**목표**: T01 설계대로 Vault Task 목록에서 "현재 작업" 1건(또는
없음)을 고르는 `CurrentWorkSelector`를 구현한다.

**구현 내용**

- `intelligence/session_resume.py`(신규) — `CurrentWork`(값 객체)와
  `CurrentWorkSelector.select(tasks)`가 활성 상태(in-progress/
  review)이면서 archived가 아닌 Task 중 `updated`가 가장 최근인
  1건을 고른다(동률이면 `task_id`가 더 큰 쪽, 활성 Task 없으면
  `None`). `VaultAdapter.list_tasks()`가 반환하는 `TaskDocumentView`
  만 입력으로 받는다 — 새로운 데이터 접근 경로 없음.

**테스트**: `tests/intelligence/test_session_resume.py`(신규 4개 —
활성 Task 없음/최신 갱신 선택/동률 처리/archived 제외).
`pytest`(958개, 기존 954개 + 신규 4개), `ruff check src tests`,
`mypy` 전부 클린.

**완료 조건 확인**: `CurrentWorkSelector` 테스트 통과. 새 Core
Domain Interface 없음(27종 그대로), Core Domain 코드 무변경.

다음 Task: **M33-T03**(Session Resume Service).

### M33-T03: Session Resume Service (Integration)

**목표**: `CurrentWorkSelector`(T02) + M29~M31 Service 3개 + M32
`IntelligenceSynthesisAnalyzer`를 조합해 `SessionResumeReport`를
만든다.

**구현 내용**

- `intelligence/session_resume_service.py`(신규)의
  `SessionResumeService.generate()` — `VaultAdapter.list_tasks()`로
  Current Work 판정 → subject/milestone 결정(Task 없으면 subject
  ""·milestone `None`) → `ProjectIntelligenceService`/
  `ContextIntelligenceService`/`CapabilityIntelligenceService`
  실행 → `IntelligenceSynthesisAnalyzer.analyze()`로 Overview
  합성. `SessionResumeReport`(current_work + 세 리포트 + overview)
  로 반환.

**테스트**: `tests/intelligence/test_session_resume_service.py`
(신규 4개 — 활성 Task 없을 때/현재 작업+Context 매칭/publish 검증/
Markdown 섹션 확인). `pytest`(962개, 기존 958개 + 신규 4개), `ruff
check src tests`, `mypy` 전부 클린.

**완료 조건 확인**: 세 Service + Analyzer 연결 확인, Report 구성
테스트 통과. 새 Core Domain Interface 없음(27종 그대로), Core
Domain 코드 무변경, §8 규칙 21 유지.

다음 Task: **M33-T04**(Presentation + E2E 검증 + 문서화 + Milestone
Review).

### M33-T04: Presentation + E2E 검증 + 문서화 + Milestone Review

**목표**: `SessionResumeService`를 실제로 Vault에 노출하고, 전체
스택 검증과 문서 갱신을 마무리한다.

**구현 내용**

- `intelligence/session_resume_service.py`(T03에서 확장) —
  `render_markdown()`(순수 함수)이 `SessionResumeReport`를
  Markdown으로 렌더링하고, `publish()`가 `VaultAdapter.
  publish_session_resume()`(신규 메서드)를 통해 실제로 Vault에
  쓴다.
- `vault/session_resume.py`(신규) — `write_session_resume_report()`
  가 `15 Project Intelligence/Session Resume.md`에 원자적으로 전체
  교체(overwrite)한다(M29~M32와 동일 패턴).
- `VaultAdapter.publish_session_resume()`(신규 메서드) — 위 writer를
  Integration Layer에 노출.
- 실제 저장소 Vault를 대상으로 `publish()`를 실행해 `Session
  Resume.md`가 생성됨을 확인(활성 Task 0건 → "현재 진행 중인 Task
  없음"으로 정상 표시).
- **실제 검증 중 발견해 수정한 버그**: 활성 Task가 없을 때 빈
  subject(`""`)를 `ContextAnalyzer.analyze()`에 그대로 넘기면 —
  이 메서드가 "빈 subject 아니어야 함"을 명시적 전제조건으로 문서화
  하고 있었음에도 — 모든 Knowledge 문서의 모든 제목이 매칭돼 버려
  Session Resume이 관련 없는 항목 수백 줄로 오염되는 결함을
  실제 Vault(대용량 `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`
  포함)로 검증하다 발견했다. 현재 작업이 없으면 Context Intelligence
  호출 자체를 건너뛰고 "해당 없음"을 직접 반환하도록
  `SessionResumeService.generate()`를 수정하고, 회귀 테스트를
  추가했다(`test_session_resume_service.py`).
- `docs/ARCHITECTURE.md` §3.26(신규)/상단 상태 갱신, `.ai/
  DECISIONS.md`(ADR-0047 신규), `.ai/TASKS.md`(본 절), Vault(ADR
  Index/Milestones Index) 갱신.

**테스트**: 전체 `pytest`/`ruff`/`mypy` 재실행으로 회귀 없음 확인.

**완료 조건 확인**: DoD 10개 항목 전부 충족.

**Milestone 33(Session Resume) T01~T04 전체 완료.**

### Milestone 33 Review

**Review 결과 요약**

| 항목 | 결과 |
|---|---|
| DoD 검증 | 10개 항목 전부 충족 |
| Architecture Review | `intelligence/session_resume*.py`를 M29~M32 Intelligence Layer와 같은 계층에 추가(ADR-0047), M29~M32 재사용 근거가 ADR에 명시, M8 세션 연속성과의 구분을 §3.26에 명문화 |
| Layer Boundary Review | `test_intelligence_layering.py`를 코드 변경 없이 그대로 실행해 §8 규칙 21 위반 없음을 확인(`VaultAdapter`는 M29부터 이미 허용된 Adapter) |
| Interface Review | Core Domain 27종 무변경. Integration Layer 신규 Adapter 없음, `VaultAdapter` 확장 1건(`publish_session_resume()`) |
| ADR Review | ADR-0047 1건만 신규, 기존 ADR과 충돌 없음(M8과의 경계를 ADR 안에서도 명시) |
| pytest/ruff/mypy | 962 passed, ruff clean, mypy clean(181 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/`15 Project Intelligence/README.md`+`Session Resume.md`) 전부 갱신 확인 |

**개선 여지(참고용, 이번에 처리하지 않음)**: (1) 이 저장소는 아직
`14 Tasks/*.md`에 실시간 Task 문서를 쓰지 않아(GitHub `.ai/TASKS.md`
가 원문) 실제 Session Resume의 "현재 작업"이 항상 `None`으로
관찰된다 — M29 `active_agent_count`/M31 Coverage와 같은 성격의
"워크숍 단계" 한계이며, Vault Task 문서를 실시간으로 쓰는 워크플로가
생기면 그때부터 실제로 채워진다. (2) CLI 노출·자동 트리거(세션
시작 Hook)는 명시적으로 범위 밖으로 남겨 M34 이후 논의 대상이다.

**사용자 승인(2026-07-30)**: DoD 10개 항목/Architecture/MDD/Layer/
Interface/Adapter/ADR/Tests/Documentation Review를 모두 확인해
**Milestone 33(Session Resume) 공식 완료(Approved)**. "M29(Project
Intelligence)→M30(Context Intelligence)→M31(Capability
Intelligence)→M32(Intelligence Synthesis)→M33(Session Resume)"로
이어지며, Intelligence Layer가 처음으로 실제 사용 시나리오(세션
시작)에 연결됐다. `15 Project Intelligence/Session Resume.md`가
공식 결과로 확정된다.

**다음은 Milestone 34** — 세부 Task는 착수 시점에 별도 제안·승인
후 정의한다.

---

## Milestone 34 — Workflow Intelligence

**목표**(2026-07-30 사용자 확정 — Milestone 계획을 3가지 수정 권고
반영 조건으로 승인): Vault Task 문서의 Milestone별 Task 실행 흐름을
분석하는 Read Only Workflow Intelligence를 구현한다. "Workflow"는
`domain.Workflow`(휘발성 in-memory DAG, 영속 저장소 없음)가 아니라
**Milestone 안의 Task 실행 순서**를 가리킨다(ADR-0048). 새로운 데이터
소스·새 Core Domain Interface·`domain.Workflow` 영속화 없음.

**Definition of Done**

| # | 항목 |
|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 |
| 2 | 새 Interface 0개 |
| 3 | 새 Integration Layer Adapter 0개(`VaultAdapter` 메서드 1개만 확장 — `publish_workflow_intelligence()`) |
| 4 | `intelligence/workflow_flow.py`/`workflow_service.py`는 `VaultAdapter.list_tasks()`(기존)에만 의존, `domain.Workflow`/`WorkflowEngine`/`WorkflowAdapter`는 사용하지 않음 |
| 5 | Blocked/Next 판정은 Task ID 순서 + 기존 `status` 값만 읽는 Rule 기반(`WorkflowFlowAnalyzer`) — 새 지표·LLM 추론 없음 |
| 6 | `15 Project Intelligence/Workflow Intelligence.md`에 Milestone별 Task 흐름(완료/진행 중/Blocked/Next) 노출 |
| 7 | 진행 중 Milestone(미완료 Task가 있는 Milestone)이 없을 때도 예외 없이 정상 표시 |
| 8 | 기존 M29~M33 pytest 회귀 없음 + 신규 테스트 통과 |
| 9 | `pytest`/`ruff`/`mypy` 통과 |
| 10 | Architecture/ADR(ADR-0048)/문서 최신화 |

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M34-T01 | Workflow Intelligence 설계 | **완료** |
| M34-T02 | Workflow Flow Analyzer | **완료** |
| M34-T03 | Workflow Intelligence Service(Integration) | **완료** |
| M34-T04 | Presentation + E2E 검증 + 문서화 + Milestone Review | **완료** |

### M34-T01: Workflow Intelligence 설계

**목표**: "Workflow"의 의미, Blocked/Next 판정 Rule, Analyzer/Service
책임 분리를 확정한다.

**결정(ADR-0048, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- "Workflow"는 `domain.Workflow`가 아니라 Milestone 안의 Task 실행
  순서다 — `domain.Workflow`/`WorkflowEngine`/`WorkflowAdapter`는
  이번 Milestone에서 전혀 사용하지 않는다(영속 데이터 소스가 없어
  YAGNI상 새 영속 계층을 만들지 않기로 결정).
- Blocked = Task ID(`M{n}-T{nn}`)의 T-번호로 같은 Milestone 내
  Task를 정렬했을 때, `status`가 `todo`이면서 선행 Task 중
  완료(`done`/`archived`)가 아닌 것이 하나라도 있는 경우. 선행이
  전부 완료된 `todo` Task는 Next.
- Blocked/Next 판정 로직은 `WorkflowFlowAnalyzer`
  (`intelligence/workflow_flow.py`, 신규)에 전부 캡슐화하고,
  `WorkflowIntelligenceService`(`intelligence/workflow_service.py`,
  M34-T03)는 `VaultAdapter` 조회 + Analyzer 실행 조합만 담당한다 —
  M29 Analyzer/Service 분리 패턴과 동일, M35/M36 재사용을 위함.
- 새 Adapter/Interface를 만들지 않는다 — `VaultAdapter`에
  `publish_workflow_intelligence()` 메서드 1개만 추가(M34-T04).

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| "Workflow" 정의 확정 | ✅ (Milestone Task 실행 흐름, ADR-0048) |
| Blocked Rule 정의 | ✅ (선행 Task 미완료 시 Blocked) |
| Analyzer/Service 책임 분리 결정 | ✅ (`WorkflowFlowAnalyzer` ↔ `WorkflowIntelligenceService`) |
| ADR 작성 | ✅ (ADR-0048) |

코드 변경 없음(설계 결론만 확정). 다음 Task: **M34-T02**(Workflow
Flow Analyzer).

### M34-T02: Workflow Flow Analyzer

**목표**: T01 설계대로 Vault Task 목록에서 Milestone별 Task 실행
흐름(완료/진행 중/Blocked/Next)을 계산하는 `WorkflowFlowAnalyzer`를
구현한다.

**구현 내용**

- `intelligence/workflow_flow.py`(신규) — `TaskFlowEntry`/
  `MilestoneFlow`/`WorkflowFlowReport`(값 객체)와
  `WorkflowFlowAnalyzer.analyze(tasks)`가 Task ID(`M{n}-T{nn}`)의
  T-번호로 같은 Milestone 내 Task를 정렬한 뒤, `status`가
  `done`/`archived`면 완료, `in-progress`/`review`면 진행 중,
  `todo`이면서 선행 Task 중 미완료가 있으면 Blocked, 선행이 모두
  완료된 `todo`면 Next로 판정한다. 미완료 Task가 없는(이미 끝난)
  Milestone은 결과에서 제외하고, archived Task는 흐름 계산에서
  제외한다. `VaultAdapter.list_tasks()`가 반환하는 `TaskDocumentView`
  만 입력으로 받는다 — 새로운 데이터 접근 경로 없음.

**테스트**: `tests/intelligence/test_workflow_flow.py`(신규 8개 —
빈 목록/완료된 Milestone 제외/Next·Blocked 판정/선행 미완료 시 전체
Blocked 전파/T-번호 순 정렬/archived 제외/완료율 계산/Milestone별
독립 그룹핑). `pytest`(970개, 기존 962개 + 신규 8개), `ruff check
src tests`, `mypy` 전부 클린.

**완료 조건 확인**: `WorkflowFlowAnalyzer` 테스트 통과. 새 Core
Domain Interface 없음(27종 그대로), Core Domain 코드 무변경.

다음 Task: **M34-T03**(Workflow Intelligence Service).

### M34-T03: Workflow Intelligence Service (Integration)

**목표**: `VaultAdapter.list_tasks()` 조회와 `WorkflowFlowAnalyzer`
(T02) 실행을 조합하는 `WorkflowIntelligenceService`를 구현한다.

**구현 내용**

- `intelligence/workflow_service.py`(신규)의
  `WorkflowIntelligenceService.generate()` — `VaultAdapter.
  list_tasks()`로 Task 전체를 조회한 뒤 `WorkflowFlowAnalyzer.
  analyze()`에 그대로 위임해 `WorkflowFlowReport`를 반환한다.
  Blocked/Next 판정 규칙 자체는 갖지 않는다(조합·오케스트레이션만,
  ADR-0048 결정 3).

**테스트**: `tests/intelligence/test_workflow_service.py`(신규 3개
— Task 없을 때 빈 결과/실제 Vault Task 생성 후 흐름 반영/완전히
끝난 Milestone 제외). `pytest`(973개, 기존 970개 + 신규 3개), `ruff
check src tests`, `mypy` 전부 클린.

**완료 조건 확인**: `WorkflowIntelligenceService` ↔
`WorkflowFlowAnalyzer` 연결 확인, Report 구성 테스트 통과. 새 Core
Domain Interface 없음(27종 그대로), Core Domain 코드 무변경, §8
규칙 21 유지.

다음 Task: **M34-T04**(Presentation + E2E 검증 + 문서화 + Milestone
Review).

### M34-T04: Presentation + E2E 검증 + 문서화 + Milestone Review

**목표**: `WorkflowIntelligenceService`를 실제로 Vault에 노출하고,
전체 스택 검증과 문서 갱신을 마무리한다.

**구현 내용**

- `intelligence/workflow_service.py`(T03에서 확장) —
  `render_markdown()`(순수 함수)이 `WorkflowFlowReport`를 Milestone별
  진행률/Blocked 수/Next Task/Task별 상태 표로 Markdown 렌더링하고,
  `publish()`가 `VaultAdapter.publish_workflow_intelligence()`(신규
  메서드)를 통해 실제로 Vault에 쓴다.
- `vault/workflow_intelligence.py`(신규) —
  `write_workflow_intelligence_report()`가 `15 Project Intelligence/
  Workflow Intelligence.md`에 원자적으로 전체 교체(overwrite)한다
  (M29~M33과 동일 패턴).
- `VaultAdapter.publish_workflow_intelligence()`(신규 메서드) — 위
  writer를 Integration Layer에 노출.
- 실제 저장소 Vault를 대상으로 `publish()`를 실행해 `Workflow
  Intelligence.md`가 생성됨을 확인(이 저장소는 아직 `14 Tasks/*.md`
  에 실시간 Task 문서를 쓰지 않아 — M29~M33 Review에서 이미 기록된
  "워크숍 단계" 한계와 동일한 이유로 — 진행 중 Milestone 0건으로
  "현재 진행 중인 Milestone 없음"이 정상 표시됨을 확인).
- `docs/ARCHITECTURE.md` §3.27(신규)/상단 상태 갱신, `.ai/
  DECISIONS.md`(ADR-0048 신규), `.ai/TASKS.md`(본 절), Vault(ADR
  Index/Milestones Index/`15 Project Intelligence/README.md`) 갱신.

**테스트**: 전체 `pytest`/`ruff`/`mypy` 재실행으로 회귀 없음 확인
(976개 전부 통과, 기존 973개 + 신규 3개 — `render_markdown` 빈
상태/Task 흐름 표시, `publish` 파일 생성 검증).

**완료 조건 확인**: DoD 10개 항목 전부 충족.

**Milestone 34(Workflow Intelligence) T01~T04 전체 완료.**

### Milestone 34 Review

**Review 결과 요약**

| 항목 | 결과 |
|---|---|
| DoD 검증 | 10개 항목 전부 충족 |
| Architecture Review | `intelligence/workflow_flow.py`/`workflow_service.py`를 M29~M33 Intelligence Layer와 같은 계층에 추가(ADR-0048), "Workflow" 재정의(`domain.Workflow`와 무관)를 §3.27과 ADR에 명시, Blocked/Next Rule과 Analyzer/Service 책임 분리(사용자 3가지 권고)를 코드·문서 양쪽에 반영 |
| Layer Boundary Review | `test_intelligence_layering.py`를 코드 변경 없이 그대로 실행해 §8 규칙 21 위반 없음을 확인(`VaultAdapter`는 M29부터 이미 허용된 Adapter) |
| Interface Review | Core Domain 27종 무변경. Integration Layer 신규 Adapter 없음, `VaultAdapter` 확장 1건(`publish_workflow_intelligence()`). `domain.Workflow`/`WorkflowEngine`/`WorkflowAdapter` 무변경(사용하지 않음) |
| ADR Review | ADR-0048 1건만 신규, 기존 ADR과 충돌 없음(§4 `domain.Workflow`와의 경계를 ADR 안에서도 명시) |
| pytest/ruff/mypy | 976 passed(기존 962 + 신규 14), ruff clean, mypy clean(184 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/`15 Project Intelligence/README.md`+`Workflow Intelligence.md`) 전부 갱신 확인 |

**개선 여지(참고용, 이번에 처리하지 않음)**: (1) M29~M33과 동일한
"워크숍 단계" 한계로, 이 저장소가 아직 `14 Tasks/*.md`에 실시간
Task 문서를 쓰지 않아 실제 Vault에서의 Workflow Intelligence는
항상 "진행 중인 Milestone 없음"으로 관찰된다 — Vault Task 문서를
실시간으로 쓰는 워크플로가 생기면 그때부터 실제로 채워진다. (2)
CLI 노출·자동 트리거·M35(Recommendation)/M36(Automation) 연동은
명시적으로 범위 밖으로 남겨 다음 Milestone 이후 논의 대상이다.

**사용자 승인(2026-07-30)**: DoD 10개 항목/Architecture/MDD/Layer/
Interface/Adapter/ADR/Tests/Documentation Review를 모두 확인해
**Milestone 34(Workflow Intelligence) 공식 완료(Approved)**.
"M29(Project Intelligence)→M30(Context Intelligence)→M31(Capability
Intelligence)→M32(Intelligence Synthesis)→M33(Session Resume)→
M34(Workflow Intelligence)"로 이어지며, "Workflow"를
`domain.Workflow`가 아니라 Milestone Task 실행 흐름으로 재정의하고
Blocked/Next Rule 1개 + `WorkflowFlowAnalyzer` 캡슐화로 M29~M33
설계 철학을 그대로 유지했다. `15 Project Intelligence/Workflow
Intelligence.md`가 공식 결과로 확정된다.

**다음은 Milestone 35** — 세부 Task는 착수 시점에 별도 제안·승인
후 정의한다.

---

## Milestone 35 — Recommendation Intelligence

**목표**(2026-07-30 사용자 확정 — Milestone 계획(목표/Scope/DoD/
Architecture/Task 구성/구현 전략/MDD Review)을 승인하며 "T01~T04
중간 승인 없이 구현 후 Milestone Review로 최종 승인" 진행 방식까지
확정): M29(Project)/M31(Capability)/M33(Session Resume)/M34
(Workflow) Intelligence를 그대로 조합해 "지금 무엇을 하는 것이
가장 적절한가"를 결정하는 Read Only Recommendation Intelligence를
구현한다(ADR-0049). Execution Layer 이전의 마지막 Decision Layer —
자동 실행하지 않고 추천만 제공한다(Automation은 M36 이후).

**Definition of Done**

| # | 항목 |
|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 |
| 2 | 새 Interface 0개 |
| 3 | 새 Integration Layer Adapter 0개(`VaultAdapter` 메서드 1개만 확장 — `publish_recommendation_intelligence()`) |
| 4 | `intelligence/recommendation_rules.py`/`recommendation_service.py`는 기존 Intelligence(M29/M31/M33/M34)만 사용 |
| 5 | 새 점수·LLM·추론 없음, Recommendation은 Rule 기반(`RecommendationRuleAnalyzer`)으로만 결정 |
| 6 | `15 Project Intelligence/Recommendation Intelligence.md` 생성 |
| 7 | 5단계 Priority 모두 해당 없을 때도 예외 없이 정상 표시("추천할 다음 행동 없음") |
| 8 | 기존 M29~M34 pytest 회귀 없음 + 신규 테스트 통과 |
| 9 | `pytest`/`ruff`/`mypy` 통과 |
| 10 | Architecture/ADR-0049/TASKS 최신화 |

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M35-T01 | Recommendation Rule 설계 | **완료** |
| M35-T02 | RecommendationRuleAnalyzer | **완료** |
| M35-T03 | Recommendation Intelligence Service(Integration) | **완료** |
| M35-T04 | Presentation + E2E 검증 + 문서화 + Milestone Review | **완료** |

### M35-T01: Recommendation Rule 설계

**목표**: 5단계 Priority Rule, Analyzer/Service 책임 분리를 확정한다.

**MDD Review 요약**(전체 서술은 세션 대화 기록 참고, 결론만 기록)

- **Scope(YAGNI)**: Task 우선순위 재계산/AI 추론/점수 계산/Workflow
  수정/Task 생성/Automation/CLI/Hook은 전부 제외(사용자 Scope 그대로
  채택).
- **Reuse**: `intelligence/recommendation.py`의 `ProjectRecommendation`
  /`ProjectRecommendationEngine`(M29), `intelligence/capability_gap.py`
  의 `CapabilityGapReport`(M31), `intelligence/session_resume.py`의
  `CurrentWorkSelector`(M33), `intelligence/workflow_flow.py`의
  `WorkflowFlowAnalyzer`(M34) — 4개 기존 Analyzer/Engine 산출물을
  그대로 입력으로 소비한다. 새로운 Vault 조회 경로 없음(`VaultAdapter.
  list_tasks()` 기존 메서드만 재사용).
- **Interface/Service/Adapter**: 새 Interface 불필요(순수 함수적
  Analyzer로 충분). 새 Service는 조합 전용
  `RecommendationIntelligenceService` 1개만 필요(기존 4개 Service를
  감싸는 게 아니라 필요한 Analyzer/Service만 선택적으로 조합 —
  M33이 M32 Service 대신 Analyzer만 재사용한 것과 같은 이유로, M35도
  `SessionResumeService`(Context까지 포함) 대신 `CurrentWorkSelector`
  만 가져온다). 새 Adapter 불필요, `VaultAdapter` 확장 1건만.
- **Layer**: 기존 Intelligence Layer 안에서 해결, 새 Layer/Engine/
  Manager/Factory/Registry 불필요.
- **File Review**: `recommendation_rules.py`(Rule, 신규 — 기존
  `recommendation.py`는 M29 Project 전용이라 재사용 불가, 대상이
  다름), `recommendation_service.py`(조합, 신규 — 기존 Service 중
  이 4가지 조합을 담당하는 것이 없음), `vault/
  recommendation_intelligence.py`(Writer, 신규 — 기존 Writer는
  각자 다른 파일에 씀).

**결정(ADR-0049, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- 5단계 Priority: ① Current Work 계속 수행 ② Workflow Next Task
  시작 ③ Workflow Blocked 해소 ④ Capability Gap 보완 ⑤ M29
  Project Recommendation(priority 최고) 그대로 노출. 모두 해당 없으면
  `next_action=None`.
- 판정 로직은 `RecommendationRuleAnalyzer`
  (`intelligence/recommendation_rules.py`, 신규)에 전부 캡슐화하고,
  `RecommendationIntelligenceService`(`intelligence/
  recommendation_service.py`, M35-T03)는 `VaultAdapter.list_tasks()`
  1회 조회 + 기존 Service/Analyzer 4개 실행 + Analyzer 호출 조합만
  담당한다.
- 새 Adapter/Interface를 만들지 않는다 — `VaultAdapter`에
  `publish_recommendation_intelligence()` 메서드 1개만 추가(M35-T04).

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| 5단계 Priority Rule 정의 | ✅ (ADR-0049) |
| Analyzer/Service 책임 분리 결정 | ✅ (`RecommendationRuleAnalyzer` ↔ `RecommendationIntelligenceService`) |
| MDD Review 수행 | ✅ (Scope/Reuse/Interface/Service/Adapter/Layer/File 전 항목 검토) |
| ADR 작성 | ✅ (ADR-0049) |

코드 변경 없음(설계 결론만 확정). 다음 Task: **M35-T02**
(RecommendationRuleAnalyzer).

### M35-T02: RecommendationRuleAnalyzer

**목표**: T01 설계대로 Current Work/Workflow Next/Workflow Blocked/
Capability Gap/Project Recommendation을 순서대로 확인해 단일
`NextAction`을 고르는 `RecommendationRuleAnalyzer`를 구현한다.

**구현 내용**

- `intelligence/recommendation_rules.py`(신규) — `NextAction`(값
  객체)과 `RecommendationRuleAnalyzer.analyze()`가 M33 `CurrentWork`
  /M34 `WorkflowFlowReport`/M31 `CapabilityGapReport`/M29
  `ProjectRecommendation` 목록만 입력으로 받아 5단계 Priority를
  순서대로 확인한다. Workflow Next/Blocked Task는 Milestone 정렬
  순 → Task ID(T-번호) 정렬 순으로 첫 번째 항목을 결정적으로 고르고,
  Priority 5(Project Recommendation)는 priority(high>medium>low,
  동률이면 target 사전순)로 가장 높은 것을 고른다. 다섯 조건 모두
  해당 없으면 `None`.

**테스트**: `tests/intelligence/test_recommendation_rules.py`(신규
7개 — Priority 1이 나머지를 모두 이기는지/Priority 2~4 각각 단독
발생/Priority 5의 priority 정렬 및 동률 처리/모두 해당 없을 때
`None`). `pytest`(983개, 기존 976개 + 신규 7개), `ruff check src
tests`, `mypy` 전부 클린.

**완료 조건 확인**: `RecommendationRuleAnalyzer` 테스트 통과. 새
Core Domain Interface 없음(27종 그대로), Core Domain 코드 무변경.

다음 Task: **M35-T03**(Recommendation Intelligence Service).

### M35-T03: Recommendation Intelligence Service (Integration)

**목표**: `VaultAdapter.list_tasks()` 1회 조회 + 기존 Service/
Analyzer 4개 실행 + `RecommendationRuleAnalyzer`(T02) 호출을
조합하는 `RecommendationIntelligenceService`를 구현한다.

**구현 내용**

- `intelligence/recommendation_service.py`(신규)의
  `RecommendationIntelligenceService.generate()` — `VaultAdapter.
  list_tasks()`로 Task 전체를 한 번만 조회한 뒤, `CurrentWorkSelector`
  (M33)/`WorkflowFlowAnalyzer`(M34)에 같은 목록을 재사용해 전달하고,
  `ProjectIntelligenceService`/`CapabilityIntelligenceService`(M29/
  M31, 주입)를 각각 실행한 뒤 `RecommendationRuleAnalyzer`에 네
  결과를 넘겨 `RecommendationIntelligenceReport`(단일 `next_action`
  + 근거가 된 하위 리포트 전체)를 만든다. `SessionResumeService`
  (M33) 전체가 아니라 `CurrentWorkSelector` Analyzer만 가져온다 —
  M35는 Context Intelligence를 쓰지 않기 때문이다(ADR-0049).

**테스트**: `tests/intelligence/test_recommendation_service.py`
(신규 3개 — 아무 Task도 없을 때 Priority 4(Capability Gap)로
귀결되는 이 저장소의 워크숍 단계 현실 확인/Current Work 존재 시
Priority 1/Next Task 존재 시 Priority 2). `pytest`(986개, 기존
983개 + 신규 3개), `ruff check src tests`, `mypy` 전부 클린.

**완료 조건 확인**: `RecommendationIntelligenceService` ↔
`RecommendationRuleAnalyzer` 연결 확인, Report 구성 테스트 통과.
새 Core Domain Interface 없음(27종 그대로), Core Domain 코드
무변경, §8 규칙 21 유지.

다음 Task: **M35-T04**(Presentation + E2E 검증 + 문서화 + Milestone
Review).

### M35-T04: Presentation + E2E 검증 + 문서화 + Milestone Review

**목표**: `RecommendationIntelligenceService`를 실제로 Vault에
노출하고, 전체 스택 검증과 문서 갱신을 마무리한다.

**구현 내용**

- `intelligence/recommendation_service.py`(T03에서 확장) —
  `render_markdown()`(순수 함수)이 `RecommendationIntelligenceReport`
  를 다음 행동 + 근거(현재 작업/Workflow/Capability/Project
  Recommendation) 섹션으로 Markdown 렌더링하고, `publish()`가
  `VaultAdapter.publish_recommendation_intelligence()`(신규 메서드)
  를 통해 실제로 Vault에 쓴다.
- `vault/recommendation_intelligence.py`(신규) —
  `write_recommendation_intelligence_report()`가 `15 Project
  Intelligence/Recommendation Intelligence.md`에 원자적으로 전체
  교체(overwrite)한다(M29~M34와 동일 패턴).
- `VaultAdapter.publish_recommendation_intelligence()`(신규 메서드)
  — 위 writer를 Integration Layer에 노출.
- 실제 저장소 Vault를 대상으로 `publish()`를 실행해 `Recommendation
  Intelligence.md`가 생성됨을 확인 — 활성 Agent 0명인 이 저장소의
  워크숍 단계 현실상 Priority 1~3(Current Work/Next/Blocked Task)이
  모두 해당 없어 Priority 4(Capability Gap, `coding` 보완)로
  귀결됨을 실제 데이터로 확인했다(DoD 7의 "5단계 모두 해당 없을 때"
  케이스는 `test_recommendation_rules.py`의 단위 테스트로 별도
  검증).
- `docs/ARCHITECTURE.md` §3.28(신규)/상단 상태 갱신, `.ai/
  DECISIONS.md`(ADR-0049 신규), `.ai/TASKS.md`(본 절), Vault(ADR
  Index/Milestones Index/`15 Project Intelligence/README.md`) 갱신.

**테스트**: 전체 `pytest`/`ruff`/`mypy` 재실행으로 회귀 없음 확인
(988개 전부 통과, 기존 986개 + 신규 2개 — `render_markdown` 다음
행동/근거 표시, `publish` 파일 생성 검증).

**완료 조건 확인**: DoD 10개 항목 전부 충족.

**Milestone 35(Recommendation Intelligence) T01~T04 전체 완료.**

### Milestone 35 Review

**Review 결과 요약**

| 항목 | 결과 |
|---|---|
| DoD 검증 | 10개 항목 전부 충족 |
| Architecture Review | `intelligence/recommendation_rules.py`/`recommendation_service.py`를 M29~M34 Intelligence Layer와 같은 계층에 추가(ADR-0049), "새 Intelligence를 계산하지 않는다"는 원칙과 5단계 Priority Rule을 §3.28과 ADR에 명시, Execution Layer 이전 마지막 Decision Layer로서 자동 실행하지 않음을 코드·문서 양쪽에 반영 |
| Layer Boundary Review | `test_intelligence_layering.py`를 코드 변경 없이 그대로 실행해 §8 규칙 21 위반 없음을 확인(`VaultAdapter`는 M29부터 이미 허용된 Adapter) |
| Interface Review | Core Domain 27종 무변경. Integration Layer 신규 Adapter 없음, `VaultAdapter` 확장 1건(`publish_recommendation_intelligence()`) |
| ADR Review | ADR-0049 1건만 신규, 기존 ADR과 충돌 없음(M33 `SessionResumeService` 대신 `CurrentWorkSelector`만 재사용한 이유를 ADR 안에서도 명시) |
| pytest/ruff/mypy | 988 passed(기존 976 + 신규 12), ruff clean, mypy clean(187 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/`15 Project Intelligence/README.md`+`Recommendation Intelligence.md`) 전부 갱신 확인 |

**개선 여지(참고용, 이번에 처리하지 않음)**: (1) 이 저장소는 아직
`14 Tasks/*.md`에 실시간 Task 문서를 쓰지 않아(M29~M34와 동일한
"워크숍 단계" 한계) Current Work/Workflow Next/Blocked Task가 항상
`None`으로 관찰되고, 활성 Agent도 0명이라 Capability Gap이 항상
존재해 Recommendation은 실제 Vault에서 거의 항상 Priority 4로
귀결된다 — Vault Task 문서를 실시간으로 쓰고 Agent가 상시 구동되는
워크플로가 생기면 그때부터 Priority 1~3/5도 실제로 관찰된다. (2)
Task 우선순위 재계산·AI 추론·Automation·CLI·Hook은 명시적으로 범위
밖으로 남겨 다음 Milestone(M36) 이후 논의 대상이다.

**사용자 승인(2026-07-30)**: DoD 10개 항목/Architecture/MDD/Layer/
Interface/Adapter/ADR/Tests/Documentation Review를 모두 확인해
**Milestone 35(Recommendation Intelligence) 공식 완료(Approved)**.
"M29(Project Intelligence)→M30(Context Intelligence)→M31(Capability
Intelligence)→M32(Intelligence Synthesis)→M33(Session Resume)→
M34(Workflow Intelligence)→M35(Recommendation Intelligence)"로
이어지며, 5단계 Priority Rule 1개로 새로운 Intelligence 계산 없이
Execution Layer 이전의 마지막 Decision Layer를 완성했다. `15
Project Intelligence/Recommendation Intelligence.md`가 공식 결과로
확정된다.

**다음은 Milestone 36** — 세부 Task는 착수 시점에 별도 제안·승인
후 정의한다.

---

## Milestone 36 — Execution

**목표**(2026-07-30 사용자 확정 — Milestone 계획을 2가지 수정 권고
반영 조건으로 승인): M35 `NextAction` 중 `next_task`(Workflow의
다음 실행 가능 Task) 추천만, 수동 트리거로만, 이미 존재하는
`ExecutionDispatcher`(M18)/`EngineRegistry`/`EngineSelectionPolicy`
파이프라인에 연결해 실제로 실행하고 결과를 Vault에 보고한다
(ADR-0050). M29~M35와 달리 **Read Only가 아니라 실제 부작용(AI
Engine 실행)을 일으키는 첫 Milestone**이며, 그만큼 범위를 최소로
좁힌다 — 새 실행 경로·자동/주기적 트리거·Task 상태 자동 전이는
전부 범위 밖이다.

**Definition of Done**

| # | 항목 |
|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 |
| 2 | 새 실행 경로 0개 — `ExecutionDispatcher`/`EngineRegistry`/`EngineSelectionPolicy`(M17/M18) 그대로 재사용 |
| 3 | 새 Adapter 0개(`VaultAdapter` 메서드 1개만 확장 — `publish_recommendation_execution()`) |
| 4 | `source=next_task` 외 4개 NextAction은 실행하지 않고 "지원하지 않음(Not Supported)"으로 명시적으로 표현 |
| 5 | 자동/주기적 트리거 없음 — `manual_trigger=True`를 호출자가 명시해야만 실행(`ExecutionGate`) |
| 6 | `ExecutionGate`(판정)와 `ActionBuilder`(변환) 책임 분리 |
| 7 | 실행 결과(성공/실패) `15 Project Intelligence/Recommendation Execution.md`에 노출, Task 상태 자동 전이는 하지 않음 |
| 8 | 기존 M29~M35 pytest 회귀 없음 + 신규 테스트 통과 |
| 9 | `pytest`/`ruff`/`mypy` 통과 |
| 10 | Architecture/ADR-0050/TASKS 최신화 |

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M36-T01 | Execution 설계 | **완료** |
| M36-T02 | ExecutionGate + ActionBuilder | **완료** |
| M36-T03 | Recommendation Execution Service(Integration) | **완료** |
| M36-T04 | Presentation + E2E 검증 + 문서화 + Milestone Review | **완료** |

### M36-T01: Execution 설계

**목표**: 실행 대상 범위(source), Gate/Builder 책임 분리,
`AutomationActionExecutor` 재사용 여부를 확정한다.

**MDD Review 요약**(전체 서술은 세션 대화 기록 참고, 결론만 기록)

- **Scope(YAGNI)**: `current_work`/`blocked_task`/`capability_gap`/
  `project_recommendation`의 실행, `AutomationScheduler` 자동 트리거
  연결, Task 상태 자동 전이, CLI/Hook 노출은 전부 범위 밖.
- **Reuse**: `runtime/execution/execution_dispatcher.py`의
  `ExecutionDispatcher`(M18, 유일한 실행 진입점),
  `interfaces/engine_registry.py`의 `EngineRegistry`(M17),
  `interfaces/engine_selection_policy.py`의
  `EngineSelectionPolicy`(M17) — `AutomationActionExecutor`(M21)가
  이미 조합해 온 것과 동일한 3개 컴포넌트를 그대로 재사용한다. 새
  실행 경로를 만들지 않는다.
- **Interface/Service/Adapter**: 새 Interface 불필요. 새 Service는
  조합 전용 `RecommendationExecutionService` 1개만 필요
  (`AutomationActionExecutor`를 감싸지 않고 그 내부와 같은 3단계를
  직접 재사용 — `__call__()`이 `EngineExecutionResult`를 버리는
  기존 계약이라 실행 결과를 Vault에 남길 수 없기 때문, ADR-0050
  결정 4). 새 Adapter 불필요, `VaultAdapter` 확장 1건만.
- **Layer**: 첫 side-effecting Milestone이므로 `intelligence/`(Read
  Only, §8 규칙 21)에 두지 않고 `runtime/execution/`(기존 Layer,
  `execution_dispatcher.py`/`retry_executor.py`와 같은 디렉터리)에
  신규 파일만 추가한다 — 새 top-level 패키지·새 Layer 없음.
- **File Review**: `recommendation_execution_gate.py`(판정, 신규 —
  기존 Gate 없음), `recommendation_action_builder.py`(변환, 신규 —
  기존 Builder 없음), `recommendation_execution_service.py`(조합,
  신규), `vault/recommendation_execution.py`(Writer, 신규 — 기존
  Writer는 각자 다른 파일에 씀).

**결정(ADR-0050, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- `NextAction`의 `source=next_task`만 실행 대상. 나머지 4개는
  "지원하지 않음(Not Supported)"으로 명시(오류가 아니라 Scope
  밖이라는 뜻 — `AutomationActionNotSupportedError`의 기존 관례와
  동일한 정신).
- 자동/주기적 트리거를 만들지 않는다 — `manual_trigger=True`를
  호출자가 직접 전달해야만 `ExecutionGate`가 승인한다.
- `ExecutionGate.check(next_action, *, manual_trigger)`(판정만,
  `GateDecision(approved, reason)` 반환)와
  `ActionBuilder.build(next_action, workflow_report)`(변환만,
  `Action(kind=RUN_TASK, ...)` 반환)로 책임을 분리한다 — 다음
  Milestone에서 `blocked_task`용 새 Gate Rule 추가가 쉬워진다.
- `AutomationActionExecutor`를 감싸지 않고,
  `EngineRegistry.list_candidates()` → `EngineSelectionPolicy.
  select()` → `ExecutionDispatcher.dispatch()` 3단계를
  `RecommendationExecutionService`가 직접 재사용해
  `EngineExecutionResult`(성공/실패)를 그대로 받는다.
- Task 상태 자동 전이는 하지 않는다 — 실행 결과를 새 Vault 문서에
  보고만 한다.

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| 실행 대상 범위(source) 확정 | ✅ (`next_task`만, ADR-0050) |
| Gate/Builder 책임 분리 결정 | ✅ (`ExecutionGate` ↔ `ActionBuilder`) |
| `AutomationActionExecutor` 재사용 여부 확정 | ✅ (감싸지 않고 3단계 직접 재사용) |
| MDD Review 수행 | ✅ (Scope/Reuse/Interface/Service/Adapter/Layer/File 전 항목 검토) |
| ADR 작성 | ✅ (ADR-0050) |

코드 변경 없음(설계 결론만 확정). 다음 Task: **M36-T02**
(ExecutionGate + ActionBuilder).

### M36-T02: ExecutionGate + ActionBuilder

**목표**: T01 설계대로 실행 승인 판정(`ExecutionGate`)과
`NextAction → Action` 변환(`ActionBuilder`)을 각각 순수 함수로
구현한다.

**구현 내용**

- `runtime/execution/recommendation_execution_gate.py`(신규) —
  `GateDecision`(값 객체)과 `ExecutionGate.check(next_action, *,
  manual_trigger)`가 manual_trigger/next_action 존재 여부/
  source=next_task 여부를 순서대로 확인해 승인·거부(+사유)를
  반환한다. source가 next_task가 아니면 "지원하지 않음(Not
  Supported): source={source}"로 명시한다.
- `runtime/execution/recommendation_action_builder.py`(신규) —
  `NextTaskNotFoundError`(예외)와 `ActionBuilder.build(next_action,
  workflow_report)`가 `WorkflowFlowReport`에서 `next_action.target`
  과 같은 `task_id`를 찾아 `Action(kind=RUN_TASK,
  project_id=milestone, task_title=title)`로 변환한다. Milestone
  문자열을 `project_id`로 그대로 재사용한다(새 필드 없음).

**테스트**: `tests/runtime/execution/test_recommendation_execution_gate.py`
(신규 4개)/`test_recommendation_action_builder.py`(신규 2개) —
manual_trigger 거부/next_action 없음/source 불일치 시 Not
Supported/승인/변환 성공/target 없을 때 예외. `pytest`(994개, 기존
988개 + 신규 6개), `ruff check src tests`, `mypy` 전부 클린.

**완료 조건 확인**: `ExecutionGate`/`ActionBuilder` 테스트 통과. 새
Core Domain Interface 없음(27종 그대로), Core Domain 코드 무변경
(`domain.automation.Action`은 M21에서 이미 존재하는 값 객체를 그대로
사용).

다음 Task: **M36-T03**(Recommendation Execution Service).

### M36-T03: Recommendation Execution Service (Integration)

**목표**: M35 `NextAction` 계산 → `ExecutionGate` 판정 → (승인 시)
`ActionBuilder` 변환 → `ExecutionDispatcher` 실행을 조합하는
`RecommendationExecutionService`를 구현한다.

**구현 내용**

- `runtime/execution/recommendation_execution_service.py`(신규)의
  `RecommendationExecutionService.execute(*, manual_trigger)` —
  `RecommendationIntelligenceService.generate()`(M35, 주입)로
  `NextAction`을 계산 → `ExecutionGate.check()` 판정 → 승인된
  경우에만 `ActionBuilder.build()` → 새 `Task` 생성 →
  `EngineRegistry.list_candidates()` → `EngineSelectionPolicy.
  select()` → `ExecutionDispatcher.dispatch()`(M17/M18, 그대로
  재사용)를 실행해 `RecommendationExecutionOutcome`(Gate 판정 +
  Action + `EngineExecutionResult`)을 반환한다.
  `AutomationActionExecutor`를 감싸지 않고 그 내부와 동일한 3단계를
  직접 재사용한 이유는 T01 결정(반환값을 버리지 않기 위함) 그대로다.

**테스트**: `tests/runtime/execution/test_recommendation_execution_service.py`
(신규 2개 — manual_trigger=False일 때 실행 자체를 시도하지 않음/
next_task 존재 시 실제 `ExecutionDispatcher` 파이프라인으로 실행되어
`FakeExecutionEnvironment`에 명령이 기록됨,
`AutomationActionExecutor` 테스트와 동일한 Fake 구성 재사용).
`pytest`(996개, 기존 994개 + 신규 2개), `ruff check src tests`,
`mypy` 전부 클린.

**완료 조건 확인**: `RecommendationExecutionService` ↔
`ExecutionGate`/`ActionBuilder`/`ExecutionDispatcher` 연결 확인. 새
Core Domain Interface 없음(27종 그대로), Core Domain 코드 무변경,
`tests/integration_layer/test_architecture_boundary.py`/`tests/
intelligence/test_intelligence_layering.py` 회귀 없음(§8 규칙
18/21 위반 없음).

다음 Task: **M36-T04**(Presentation + E2E 검증 + 문서화 + Milestone
Review).

### M36-T04: Presentation + E2E 검증 + 문서화 + Milestone Review

**목표**: `RecommendationExecutionService`를 실제로 Vault에 노출하고,
전체 스택 검증과 문서 갱신을 마무리한다.

**구현 내용**

- `recommendation_execution_service.py`(T03에서 확장) —
  `render_markdown()`(순수 함수)이 `RecommendationExecutionOutcome`
  을 Gate 판정/실행된 Action/실행 결과(성공 여부·Engine·소요
  시간·오류) 섹션으로 Markdown 렌더링하고, `publish()`가
  `VaultAdapter.publish_recommendation_execution()`(신규 메서드)를
  통해 실제로 Vault에 쓴다.
- `vault/recommendation_execution.py`(신규) —
  `write_recommendation_execution_report()`가 `15 Project
  Intelligence/Recommendation Execution.md`에 원자적으로 전체
  교체(overwrite)한다(M29~M35와 동일 패턴).
- `VaultAdapter.publish_recommendation_execution()`(신규 메서드) —
  위 writer를 Integration Layer에 노출.
- 실제 저장소 Vault를 대상으로 `publish(manual_trigger=True)`를
  실행해 `Recommendation Execution.md`가 생성됨을 확인 — 활성 Agent
  0명·등록된 Engine 없음인 이 저장소의 워크숍 단계 현실상 실제
  Recommendation이 여전히 Priority 4(Capability Gap)로 귀결돼 Gate가
  "지원하지 않음(Not Supported): source=capability_gap"으로 정상
  거부함을 확인했다(실제 AI Engine 실행은 트리거되지 않음 — 승인
  경로는 `FakeExecutionEnvironment`를 쓰는 단위 테스트로 이미 안전하게
  검증됨).
- `docs/ARCHITECTURE.md` §3.29(신규)/상단 상태 갱신, `.ai/
  DECISIONS.md`(ADR-0050 신규), `.ai/TASKS.md`(본 절), Vault(ADR
  Index/Milestones Index/`15 Project Intelligence/README.md`) 갱신.

**테스트**: 전체 `pytest`/`ruff`/`mypy` 재실행으로 회귀 없음 확인
(998개 전부 통과, 기존 996개 + 신규 2개 — `render_markdown` 거부/
승인 표시, `publish` 파일 생성 검증).

**완료 조건 확인**: DoD 10개 항목 전부 충족.

**Milestone 36(Execution) T01~T04 전체 완료.**

### Milestone 36 Review

**Review 결과 요약**

| 항목 | 결과 |
|---|---|
| DoD 검증 | 10개 항목 전부 충족 |
| Architecture Review | `runtime/execution/recommendation_execution_gate.py`/`recommendation_action_builder.py`/`recommendation_execution_service.py`를 `runtime/execution/`(기존 Layer)에 추가(ADR-0050), M29~M35와 달리 실제 부작용을 일으키는 첫 Milestone임을 §3.29와 ADR에 명시, `AutomationActionExecutor`/`AutomationScheduler`/`ExecutionDispatcher`를 감싸지 않고 재사용한 이유를 코드·문서 양쪽에 반영 |
| Layer Boundary Review | `test_architecture_boundary.py`(§8 규칙 18)/`test_intelligence_layering.py`(§8 규칙 21)를 코드 변경 없이 그대로 실행해 위반 없음을 확인 — `RecommendationExecutionService`는 `ai_workspace.vault`를 직접 import하지 않고 `VaultAdapter`(허용된 통로)만 사용 |
| Interface Review | Core Domain 27종 무변경. Integration Layer 신규 Adapter 없음, `VaultAdapter` 확장 1건(`publish_recommendation_execution()`). `AutomationActionExecutor`/`AutomationScheduler`/`ExecutionDispatcher`/`EngineRegistry`/`EngineSelectionPolicy` 무변경(그대로 재사용) |
| ADR Review | ADR-0050 1건만 신규, 기존 ADR과 충돌 없음(M21 ADR과의 "감싸지 않는 이유"를 ADR 안에서도 명시) |
| pytest/ruff/mypy | 998 passed(기존 988 + 신규 10), ruff clean, mypy clean(191 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/`15 Project Intelligence/README.md`+`Recommendation Execution.md`) 전부 갱신 확인 |

**개선 여지(참고용, 이번에 처리하지 않음)**: (1) 이 저장소는 아직
운영 Engine을 등록하지 않아(실제 Vault E2E에서는 빈
`EngineRegistry` 사용) `next_task`가 승인되는 실제 실행 경로는
단위 테스트(`FakeExecutionEnvironment`)로만 검증됐다 — 실제 Claude
Code 등 Engine을 상시 등록하는 운영 배선이 생기면 그때부터 실제
승인·실행이 관찰된다(M29~M36 공통의 "워크숍 단계" 한계). (2)
`current_work`/`blocked_task`/`capability_gap`/`project_recommendation`
실행, `AutomationScheduler` 자동 트리거 연결, Task 상태 자동
전이는 명시적으로 범위 밖으로 남겨 다음 Milestone(M37) 이후 논의
대상이다.

**사용자 승인(2026-07-30)**: DoD 10개 항목/Architecture/MDD/Layer/
Interface/Adapter/ADR/Tests/Documentation Review를 모두 확인해
**Milestone 36(Execution) 공식 완료(Approved)**. "M29(Project
Intelligence)→M30(Context Intelligence)→M31(Capability
Intelligence)→M32(Intelligence Synthesis)→M33(Session Resume)→
M34(Workflow Intelligence)→M35(Recommendation Intelligence)→
M36(Execution)"으로 이어지며, next_task 1개 source·수동 트리거
1개 경로로만 좁혀 M29~M35의 Read Only Intelligence를 실제 실행으로
처음 연결했다. `15 Project Intelligence/Recommendation
Execution.md`가 공식 결과로 확정된다.

**다음은 Milestone 37** — 세부 Task는 착수 시점에 별도 제안·승인
후 정의한다.

---

## Milestone 37 — Task Lifecycle

**목표**(2026-07-30 사용자 확정 — Milestone 계획을 2가지 수정 권고
반영 조건으로 승인): M36 Execution 결과(Gate 승인/실행 성공·실패)를
이미 존재하는 Task 상태 전이 기계(`vault/task_lifecycle.py`의
`_ALLOWED_TRANSITIONS`, M28)에 연결한다(ADR-0051). 새 상태·새 전이
규칙·새 Adapter 없이, 실행 시작 시 `todo→in-progress`, 성공 시
`in-progress→review`, 실패 시 `in-progress→todo`만 자동화한다.
`review→done`은 자동화하지 않는다(사람 검토 유지).

**Definition of Done**

| # | 항목 |
|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 |
| 2 | 새 Interface/Adapter 0개(`VaultAdapter.transition_task()` 그대로 재사용, 확장 없음) |
| 3 | 새 상태·새 전이 규칙 0개(`_ALLOWED_TRANSITIONS` 무변경) |
| 4 | `review→done`은 자동화하지 않음(사람 검토 유지) |
| 5 | `TaskLifecycleTransitioner`는 현재 상태를 확인하고 유효한 전이만 결정(예상과 다른 상태면 조용히 건너뜀) |
| 6 | 실행 실패 시 `todo`로 되돌아가 재시도 가능 |
| 7 | Presentation을 "Execution 결과"와 "Task Status 이력"으로 렌더링 함수 분리 |
| 8 | 기존 M29~M36 pytest 회귀 없음 + 신규 테스트 통과 |
| 9 | `pytest`/`ruff`/`mypy` 통과 |
| 10 | Architecture/ADR-0051/TASKS 최신화 |

**Task List**

| Task | 내용 | 상태 |
|---|---|---|
| M37-T01 | Task Lifecycle 설계 | **완료** |
| M37-T02 | TaskLifecycleTransitioner | **완료** |
| M37-T03 | RecommendationExecutionService 통합 | **완료** |
| M37-T04 | Presentation 분리 + E2E 검증 + 문서화 + Milestone Review | **완료** |

### M37-T01: Task Lifecycle 설계

**목표**: 전이 규칙, `TaskLifecycleTransitioner` 방어 로직,
Presentation 분리 방식을 확정한다.

**MDD Review 요약**(전체 서술은 세션 대화 기록 참고, 결론만 기록)

- **Scope(YAGNI)**: `done→archived` 자동화, 재시도 정책, `review→
  done` 자동화, `AutomationScheduler` 연결, CLI/Hook은 전부 범위
  밖.
- **Reuse**: `vault/task_lifecycle.py`의 `_ALLOWED_TRANSITIONS`(M28,
  이미 검증된 상태 전이 기계), `VaultAdapter.transition_task()`
  (M28, 전이+Daily Note/Milestones Index 동기화까지 이미 처리),
  `report.workflow_report`의 `TaskFlowEntry.status`(M34, 현재 상태
  재조회 없이 재사용) — 새 상태 조회 경로·새 전이 규칙을 만들지
  않는다.
- **Interface/Service/Adapter**: 새 Interface 불필요. 새 Adapter
  불필요(`VaultAdapter` 확장 없음, M35/M36과 달리 이번엔 메서드
  추가도 없음 — `transition_task()`가 이미 있음). 새 Service는
  기존 `RecommendationExecutionService`(M36) 확장만으로 충분.
- **Layer**: `runtime/execution/`(기존 Layer, M36 파일들과 같은
  디렉터리)에 신규 파일 1개만 추가한다 — 새 Layer 없음.
- **File Review**: `recommendation_task_lifecycle.py`(순수 Rule,
  신규 — 기존 파일 중 "현재 상태 확인 후 전이 결정" 책임을 가진
  것이 없음).

**결정(ADR-0051, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- `TaskLifecycleTransitioner.decide_start(current_status)`(현재
  `todo`일 때만 `in-progress` 반환)와 `decide_completion
  (current_status, *, success)`(현재 `in-progress`일 때만 성공
  여부로 `review`/`todo` 반환) — 둘 다 현재 상태를 먼저 확인하고
  예상과 다르면 `None`(전이하지 않음)을 반환한다.
- `RecommendationExecutionService.execute()`가 Gate 승인 →
  `decide_start()` → (전이 시) `VaultAdapter.transition_task()` →
  `ExecutionDispatcher.dispatch()` → `decide_completion()` → (전이
  시) `VaultAdapter.transition_task()` 순서로 호출한다.
- Presentation은 `_render_execution_section()`(M36의 Gate/Action/
  실행 결과)과 `_render_lifecycle_section()`(신규, 전이 이력)으로
  분리하고, 같은 Vault 문서(`Recommendation Execution.md`) 안에
  별도 섹션(`## Task Status 이력`)으로 노출한다 — 새 Vault 파일
  없음.

**완료 조건 확인**

| 항목 | 결과 |
|---|---|
| 전이 규칙 확정 | ✅ (시작/성공/실패 3가지, `_ALLOWED_TRANSITIONS` 그대로) |
| Transitioner 방어 로직 결정 | ✅ (현재 상태 확인 후 유효한 전이만) |
| Presentation 분리 방식 결정 | ✅ (렌더링 함수 분리, 같은 문서 안 별도 섹션) |
| MDD Review 수행 | ✅ (Scope/Reuse/Interface/Service/Adapter/Layer/File 전 항목 검토) |
| ADR 작성 | ✅ (ADR-0051) |

코드 변경 없음(설계 결론만 확정). 다음 Task: **M37-T02**
(TaskLifecycleTransitioner).

### M37-T02: TaskLifecycleTransitioner

**목표**: T01 설계대로 현재 상태를 확인하고 유효한 전이만 결정하는
`TaskLifecycleTransitioner`를 구현한다.

**구현 내용**

- `runtime/execution/recommendation_task_lifecycle.py`(신규) —
  `TaskLifecycleTransitioner.decide_start(current_status)`(현재
  `todo`일 때만 `"in-progress"` 반환, 아니면 `None`)와
  `decide_completion(current_status, *, success)`(현재
  `in-progress`일 때만 성공 여부로 `"review"`/`"todo"` 반환, 아니면
  `None`). `vault.task_lifecycle.TaskStatus`를 직접 import하지
  않고 문자열 status 값만 주고받는다(§8 규칙 18/19 경계를 넘지
  않기 위함).

**테스트**: `tests/runtime/execution/test_recommendation_task_lifecycle.py`
(신규 5개 — start: todo일 때/아닐 때, completion: 성공·실패 시
in-progress일 때/아닐 때). `pytest`(1003개, 기존 998개 + 신규 5개),
`ruff check src tests`, `mypy` 전부 클린.

**완료 조건 확인**: `TaskLifecycleTransitioner` 테스트 통과. 새
Core Domain Interface 없음(27종 그대로), Core Domain 코드 무변경,
`_ALLOWED_TRANSITIONS` 무변경.

다음 Task: **M37-T03**(RecommendationExecutionService 통합).

### M37-T03: RecommendationExecutionService 통합

**목표**: `RecommendationExecutionService.execute()`에 시작/완료
전이를 연결하고, `RecommendationExecutionOutcome`에
`lifecycle_transitions` 필드를 추가한다.

**구현 내용**

- `runtime/execution/recommendation_action_builder.py`(확장) —
  `ActionBuilder.find_entry()`(신규 공개 메서드)가 `next_action.
  target`과 같은 `task_id`를 가진 Milestone 이름 + `TaskFlowEntry`
  를 반환한다(`build()`도 내부적으로 재사용) — M37이 현재 status를
  새로 조회하지 않고 재사용하기 위함.
- `runtime/execution/recommendation_execution_service.py`(확장) —
  `execute()`가 `ActionBuilder.find_entry()`로 현재 status 확인 →
  `TaskLifecycleTransitioner.decide_start()` → (전이 시)
  `VaultAdapter.transition_task()` → `ExecutionDispatcher.
  dispatch()` → `decide_completion()` → (전이 시) `VaultAdapter.
  transition_task()` 순서로 호출해 `RecommendationExecutionOutcome.
  lifecycle_transitions`(신규 필드, `list[TaskTransitionOutcome]`)
  에 발생한 전이를 담는다. Gate가 승인하지 않으면 빈 목록.

**테스트**: `tests/runtime/execution/test_recommendation_execution_service.py`
(신규 1개 — 실행 실패 시 `todo`로 되돌아감, 기존 성공 케이스
테스트에 전이 이력/최종 Vault Task 상태 검증 추가). `pytest`
(1004개, 기존 1003개 + 신규 1개), `ruff check src tests`, `mypy`
전부 클린.

**완료 조건 확인**: `RecommendationExecutionService` ↔
`TaskLifecycleTransitioner` 연결 확인, 성공/실패 각각 실제 Vault
Task 상태 변경 검증. 새 Core Domain Interface 없음(27종 그대로),
Core Domain 코드 무변경.

다음 Task: **M37-T04**(Presentation 분리 + E2E 검증 + 문서화 +
Milestone Review).

### M37-T04: Presentation 분리 + E2E 검증 + 문서화 + Milestone Review

**목표**: "Execution 결과"와 "Task Status 이력"을 렌더링 함수로
분리하고, 전체 스택 검증과 문서 갱신을 마무리한다.

**구현 내용**

- `recommendation_execution_service.py`(확장) — `render_markdown()`
  을 `_render_execution_section()`(Gate/Action/실행 결과, M36
  그대로)과 `_render_lifecycle_section()`(신규, 발생한 전이 이력을
  `task_id: old_status → new_status` 형태로 나열)으로 분리하고
  둘을 조합만 한다. `VaultAdapter` 확장 없음(M35/M36과 달리 새
  메서드 추가도 없음 — `transition_task()`가 이미 있었음).
- 실제 저장소 Vault를 대상으로 `publish(manual_trigger=True)`를
  실행해 "Task Status 이력" 섹션이 정상 표시됨을 확인 — 이 저장소
  현실상 Gate가 거부(Not Supported)해 "발생한 전이 없음"으로
  정상 표시됨(실제 Vault Task는 건드리지 않음). 성공/실패 각각의
  전이는 단위 테스트(`FakeExecutionEnvironment`)로 실제 Vault Task
  문서 상태 변경까지 검증됨.
- `docs/ARCHITECTURE.md` §3.30(신규)/상단 상태 갱신, `.ai/
  DECISIONS.md`(ADR-0051 신규), `.ai/TASKS.md`(본 절), Vault(ADR
  Index/Milestones Index/`15 Project Intelligence/README.md`) 갱신.

**테스트**: 전체 `pytest`/`ruff`/`mypy` 재실행으로 회귀 없음 확인
(1005개 전부 통과, 기존 1004개 + 신규 1개 — `render_markdown`이
Task Status 이력을 표시).

**완료 조건 확인**: DoD 10개 항목 전부 충족.

**Milestone 37(Task Lifecycle) T01~T04 전체 완료.**

### Milestone 37 Review

**Review 결과 요약**

| 항목 | 결과 |
|---|---|
| DoD 검증 | 10개 항목 전부 충족 |
| Architecture Review | `runtime/execution/recommendation_task_lifecycle.py`를 `runtime/execution/`(M36과 같은 디렉터리)에 추가(ADR-0051), 새 상태·새 전이 규칙 없이 기존 `_ALLOWED_TRANSITIONS`만 재사용함을 §3.30과 ADR에 명시, `review→done`을 자동화하지 않는 이유를 코드·문서 양쪽에 반영 |
| Layer Boundary Review | `test_architecture_boundary.py`(§8 규칙 18)/`test_intelligence_layering.py`(§8 규칙 21)를 코드 변경 없이 그대로 실행해 위반 없음을 확인 — `TaskLifecycleTransitioner`는 `vault.task_lifecycle.TaskStatus`를 직접 import하지 않고 문자열 status만 사용 |
| Interface Review | Core Domain 27종 무변경. Integration Layer 신규 Adapter 없음, `VaultAdapter` 확장도 없음(M35/M36과 달리 기존 `transition_task()` 그대로 재사용). `_ALLOWED_TRANSITIONS` 무변경 |
| ADR Review | ADR-0051 1건만 신규, 기존 ADR과 충돌 없음(M36 ADR-0050 결정 5에서 미룬 항목을 이어받는 관계를 ADR 안에서도 명시) |
| pytest/ruff/mypy | 1005 passed(기존 998 + 신규 7), ruff clean, mypy clean(192 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/`15 Project Intelligence/README.md`+`Recommendation Execution.md`) 전부 갱신 확인 |

**개선 여지(참고용, 이번에 처리하지 않음)**: (1) M29~M36과 동일한
"워크숍 단계" 한계로, 실제 Vault에서는 아직 등록된 Engine이 없어
전이가 발생하는 실제 경로는 단위 테스트로만 검증됐다. (2)
`done→archived` 자동화·재시도 정책·`review→done` 자동화·
`AutomationScheduler` 연결·CLI·Hook은 명시적으로 범위 밖으로 남겨
다음 Milestone(M38) 이후 논의 대상이다.

**사용자 승인(2026-07-30)**: DoD 10개 항목/Architecture/MDD/Layer/
Interface/Adapter/ADR/Tests/Documentation Review를 모두 확인해
**Milestone 37(Task Lifecycle) 공식 완료(Approved)**. "M29(Project
Intelligence)→M30(Context Intelligence)→M31(Capability
Intelligence)→M32(Intelligence Synthesis)→M33(Session Resume)→
M34(Workflow Intelligence)→M35(Recommendation Intelligence)→
M36(Execution)→M37(Task Lifecycle)"로 이어지며, 새 상태·새 전이
규칙 없이 M28부터 존재한 검증된 상태 전이 기계에 M36 실행 결과를
연결했다. `15 Project Intelligence/Recommendation Execution.md`의
"Task Status 이력" 섹션이 공식 결과로 확정된다.

**다음은 Milestone 38** — 세부 Task는 착수 시점에 별도 제안·승인
후 정의한다.

---

## Milestone 38 — AutomationScheduler 연결

**목표**(2026-07-30 사용자 확정): M37이 "M38 이후"로 미룬 6개 항목
(`done→archived` 자동화/재시도 정책/`review→done` 자동화/
`AutomationScheduler` 연결/CLI/Hook) 중 `AutomationScheduler` 연결만
범위로 확정한다(ADR-0052). **새 기능 Milestone이 아니라 M21~M37이
만든 컴포넌트를 Composition Root(`web/server.py`의 `build_app()`)에서
실제로 조립하는 배선 Milestone**이다 — 사용자 권고에 따라 자동 실행
대상은 M36과 동일하게 `source=next_task`만 유지하고 나머지 4개
source(`current_work`/`blocked_task`/`capability_gap`/
`project_recommendation`)는 계속 Not Supported로 남긴다.

**MDD Review 요약**

- **Scope(YAGNI)**: `ExecutionGate` 판정 로직 변경 없음(여전히
  `source=next_task`만 승인). `done→archived`/재시도 정책/
  `review→done` 자동화/CLI/Hook은 계속 범위 밖.
- **발견(범위 확정에 영향)**: `VaultAdapter`/`AgentAdapter`가
  `tests/`에서만 생성되고 `web/server.py`(`build_app()`)나 CLI
  어디에도 실제로 조립된 적이 없었다 — M29~M37 전체가 단위 테스트로만
  검증된 "워크숍 단계"였다는 뜻. "AutomationScheduler 연결"을
  완성하려면 이 배선 자체가 필요하다는 사실을 사용자에게 보고하고
  범위에 포함하기로 확정(사용자 승인).
- **Reuse**: `RecommendationExecutionService`/
  `RecommendationIntelligenceService`/`ProjectIntelligenceService`/
  `CapabilityIntelligenceService`/`VaultAdapter`/`AgentAdapter`(전부
  M29~M37 기존 클래스) 그대로 재사용 — 생성자 조합은
  `tests/runtime/execution/test_recommendation_execution_service.py`
  와 동일한 패턴.
- **Interface/Service/Adapter**: 새 Interface/Adapter 0개(27종 유지).
  `domain.automation.ActionKind`에 `RUN_RECOMMENDATION` 1개만 추가
  (추가 필드 없음) — Trigger→Action 매핑 표현을 위한 최소 확장.
- **Layer**: 새 Layer 없음. `AutomationActionExecutor`(기존 파일)에
  선택적 의존성 1개 추가, `ProductionConfig`(기존 파일)에
  `vault_root` 필드 1개 추가, `build_app()`(기존 함수)에 조립 코드
  추가.

**결정(ADR-0052, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- `AutomationActionExecutor.__init__()`에 `recommendation_execution_service:
  RecommendationExecutionService | None = None` 추가. `RUN_RECOMMENDATION`
  발동 시 주입돼 있으면 `publish(manual_trigger=True)` 호출, 아니면
  `RUN_WORKFLOW`와 동일하게 `AutomationActionNotSupportedError`.
- `manual_trigger=True`를 고정 전달하는 이유: `ExecutionGate`가
  막으려는 것은 "사람이 개입하지 않은 자동/주기적 트리거의 실수
  승인"인데, `AutomationRule`은 사용자가 `AutomationService`(M21
  CRUD 진입점)로 명시적으로 만들고 활성화한 것이므로 이미 사람의
  승인을 거친 상태다. `ExecutionGate` 내부 판정 로직 자체는 전혀
  바꾸지 않는다.
- `ProductionConfig.vault_root: str = "."`(신규, ADR-0037 "Vault ==
  Repository Root"를 그대로 반영) + `AI_WORKSPACE_VAULT_ROOT` Env
  Var. `build_app()`이 `VaultAdapter(Path(config.vault_root))`로
  바인딩한다.

**구현 내용**

- `domain/automation.py`(확장) — `ActionKind.RUN_RECOMMENDATION`
  추가, `Action` docstring 갱신.
- `runtime/automation/automation_action_executor.py`(확장) —
  `recommendation_execution_service` 선택적 의존성 + `_run_recommendation()`.
- `runtime/production/config.py`/`config_loader.py`(확장) —
  `vault_root` 필드 + `AI_WORKSPACE_VAULT_ROOT` Env Var.
- `web/server.py`(Composition Root 배선) — `VaultAdapter`/
  `AgentAdapter`(`InMemoryAgentManager`/`InMemoryAgentRegistry`/
  `InMemoryAgentScheduler`)/`RecommendationIntelligenceService`/
  `RecommendationExecutionService`를 최초로 조립해
  `AutomationActionExecutor`에 주입. `EngineSelectionPolicy` 인스턴스는
  기존 RUN_TASK 배선과 공유(중복 생성 없음).

**테스트**: `tests/domain/test_automation.py`(`ActionKind` 카탈로그
갱신), `tests/runtime/automation/test_automation_action_executor.py`
(신규 2개 — 의존성 미주입 시 Not Supported, 주입 시 Vault에
`Recommendation Execution.md` 작성 확인), `tests/runtime/production/
test_config.py`/`test_config_loader.py`(신규 각 1개 —
`vault_root` 기본값/Env Var), `tests/web/test_server.py`(신규 1개
— `build_app()`이 조립한 `AutomationScheduler.run_now()`로
`RUN_RECOMMENDATION` Rule을 실제로 실행해 Vault 파일이 쓰여짐을
검증, `tmp_path`를 `vault_root`로 써서 실제 저장소 Vault는 건드리지
않음). `pytest` 1010개(기존 1005개 + 신규 5개) 전부 통과,
`ruff check src tests` clean, `mypy`(192 source files) clean.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음 | ✅ |
| 2 | 새 Interface/Adapter 0개(생성자 조합만 재사용) | ✅ |
| 3 | `ExecutionGate` 판정 로직 무변경(`source=next_task`만 승인 유지) | ✅ |
| 4 | `RUN_RECOMMENDATION` 미주입 시 기존 `RUN_WORKFLOW`와 동일하게 Not Supported | ✅ |
| 5 | `AutomationScheduler`/`ExecutionDispatcher`/`ActionBuilder`/`TaskLifecycleTransitioner` 무변경 | ✅ |
| 6 | `build_app()`에서 `VaultAdapter`/`AgentAdapter`/Recommendation 파이프라인 최초 실배선 | ✅ |
| 7 | 실제 저장소 Vault를 건드리지 않는 테스트 설계(`tmp_path` 사용) | ✅ |
| 8 | 기존 M21~M37 pytest 회귀 없음 + 신규 테스트 통과 | ✅ |
| 9 | `pytest`/`ruff`/`mypy` 통과 | ✅ |
| 10 | Architecture/ADR-0052/TASKS 최신화 | ✅ |

**개선 여지(참고용, 이번에 처리하지 않음)**: `done→archived` 자동화·
재시도 정책·`review→done` 자동화·CLI·Hook은 여전히 범위 밖으로
남아 다음 Milestone 이후 논의 대상이다. 실제 운영 환경에서
`AutomationScheduler.tick()`이 주기적으로 `RUN_RECOMMENDATION`을
발동시키려면 사용자가 `AutomationRule`을 직접 등록해야 한다(자동
생성되는 기본 Rule 없음 — 이번 범위에 포함되지 않음, YAGNI).

**Milestone 38(AutomationScheduler 연결) T01(설계+MDD Review+구현)
전체 완료.**

### Milestone 38 Review

**Review 결과 요약**

| 항목 | 결과 |
|---|---|
| DoD 검증 | 10개 항목 전부 충족 |
| Architecture Review | `web/server.py`의 `build_app()`(Composition Root)에 `VaultAdapter`/`AgentAdapter`/`RecommendationIntelligenceService`/`RecommendationExecutionService`를 최초 실배선함을 §3.31과 ADR-0052에 명시. `ExecutionGate`는 손대지 않아 `source=next_task`만 승인하는 M36 결정을 그대로 유지함을 문서에 반영 |
| MDD Review | Scope(YAGNI: `ExecutionGate` 정책 무변경)/Reuse(기존 5개 클래스 생성자 조합만 재사용)/Interface(`ActionKind` 1개 추가 외 신규 0개)/Service(`RecommendationExecutionService` 그대로)/Adapter(신규 0개)/Layer(신규 Layer 없음) 전 항목 검토 결과가 ADR-0052/TASKS 양쪽에 기록됨 |
| Layer Boundary Review | 코드 변경 없이 기존 경계 테스트를 그대로 실행해 위반 없음 확인 — `AutomationActionExecutor`는 여전히 Infrastructure Layer에서만 `RecommendationExecutionService`를 참조(Core Domain 무참조) |
| Interface Review | Core Domain 27종 무변경. `ExecutionGate`/`ActionBuilder`/`TaskLifecycleTransitioner` 무변경. `ActionKind.RUN_RECOMMENDATION` 1개만 신규(추가 필드 없음) |
| ADR Review | ADR-0052 1건만 신규, 기존 ADR(특히 ADR-0050의 `manual_trigger` 안전장치)과 충돌 없음 — Rule 생성/활성화 자체를 수동 승인으로 해석한 근거를 ADR 안에 명시 |
| pytest/ruff/mypy | 1010 passed(기존 1005 + 신규 5), ruff clean, mypy clean(192 source files) |
| 문서 최신화 | `docs/ARCHITECTURE.md`/`.ai/DECISIONS.md`/`.ai/TASKS.md`/Vault(ADR Index/Milestones Index/Automation Index/`15 Project Intelligence/README.md`) 전부 갱신 확인 |

**개선 여지(참고용, 이번에 처리하지 않음)**: `done→archived` 자동화·
재시도 정책·`review→done` 자동화·CLI·Hook은 명시적으로 범위 밖으로
남겨 다음 Milestone(M39) 이후 논의 대상이다. 실제 운영 환경에서
`AutomationScheduler.tick()`이 주기적으로 `RUN_RECOMMENDATION`을
발동시키려면 사용자가 `AutomationRule`을 직접 등록해야 한다(자동
생성되는 기본 Rule 없음, YAGNI).

**사용자 승인(2026-07-30)**: DoD 10개 항목/Architecture/MDD/Layer/
Interface/ADR/Tests/Documentation Review를 모두 확인해 **Milestone
38(AutomationScheduler 연결) 공식 완료(Approved)**. "M29(Project
Intelligence)→…→M37(Task Lifecycle)→M38(AutomationScheduler 연결)"
로 이어지며, M21 Automation Engine과 M29~M37 Intelligence→
Execution→Task Lifecycle 파이프라인이 처음으로 실제 서버
Composition Root에서 연결돼 **Intelligence → Execution → Automation
기본 폐쇄 루프**가 완성됐다. 새 정책 없이(`ExecutionGate`
무변경) 기존 27개 Core Domain Interface를 그대로 유지했다.

**문서 재구성 — Intelligence Platform / Execution Platform 계층
정의(2026-07-30 사용자 확정)**: 처음 제안됐던 "Intelligence
Core(M29~M34) / Automation Core v1.0(M35~M38)" 구분을 사용자가
재검토해 **Intelligence Platform(M29~M35, 관찰·분석·추천)**과
**Execution Platform(M36~M38, 실행·상태 전이·스케줄링)**으로
다시 정의했다 — M35(Recommendation Intelligence)는 아직 추천만
하고 실행하지 않아(Read Only) Intelligence 쪽 책임에 더 가깝고,
M36부터 실제 부작용(AI Engine 실행, Task 상태 변경)이 시작된다는
근거다. **새 컴포넌트/코드 변경 없는 순수 문서 재구성**이라 별도
ADR을 만들지 않는다(`docs/ARCHITECTURE.md` §2.1 신설/재정의).

**"Automation Core" 명명 보류(사용자 판단)**: M36~M38(Execution
Platform)은 "생각하고 실행"할 수 있을 뿐, 아직 스스로 기억하고
(Memory Engine) 설계를 감시하고(Architecture Guardian) 학습하는
(Learning Engine) 단계가 아니다. 이 세 Engine이 실제로 설계·구현·
승인된 뒤에야(M39 이후, 각각 별도 제안·승인 대상) 그 시점까지의
전체를 묶어 "Automation Core"로 명명하는 것이 더 일관된다는 것이
사용자 의견이다 — 지금은 이름을 붙이지 않는다. 이 세 Engine의
구체 설계·구현은 이번 결정에 포함되지 않는다(각각 별도 §1.4
Approval Required 대상).

**다음은 Milestone 39** — 세부 Task는 착수 시점에 별도 제안·승인
후 정의한다.

---

## Milestone 39 — Execution Memory

**목표**(2026-07-30 사용자 확정): M38 Review가 M39 이후로 미룬 세
Engine(Memory Engine/Architecture Guardian/Learning Engine) 중
Memory Engine을 착수한다(ADR-0053). **Execution 결과를 Memory에
축적한다**만 M39 범위다 — 기존 `MemoryEngine`(M1)을 재사용해
"저장"과 "조회 API"만 제공하고, 과거 기록으로 추천/판단을 바꾸는
"Learning"은 명시적으로 M40 이후로 이관한다(사용자 조건부 승인 2건
반영: ① `RecommendationRuleAnalyzer` 반영은 M40으로, ②
`ExecutionMemory`에 embedding/score/vector/confidence 금지).

**MDD Review 요약**

- **Scope(YAGNI)**: Vector/Embedding/Scoring/Rule 변경/Recommendation
  개선 전부 범위 밖(사용자 명시 제외 목록). Vault 영속화도 범위
  밖으로 확정(아래 "발견" 참고) — 프로세스 생존 기간 동안만
  유지되는 In-Memory 저장.
- **발견(범위 확정에 영향)**: 최초 제안서는 "Vault 파일에 영속화"를
  포함했으나, 설계 검토 중 `interfaces/memory_engine.py`(M1 기초
  Core Domain 계약)의 구현체가 `vault/`(Core Domain을 모르는 계층,
  M28+)를 알아야 하는 하향 결합이 생긴다는 사실을 발견해 제외했다
  (ADR-0053 대안 문단 참고). 영속화가 실제로 필요해지면 별도
  제안·승인 대상이다.
- **Reuse**: `MemoryEngine`(M1, remember/recall/search 그대로),
  `InMemoryContextManager`의 "JSON 직렬화해 remember()에 저장"
  패턴(M1) 그대로 재사용. `RecommendationExecutionService`(M36)의
  선택적 의존성 주입 패턴(M38의
  `recommendation_execution_service: ... | None = None`과 동일)도
  그대로 재사용.
- **Interface/Service/Adapter**: 새 Interface 0개(27종 유지,
  `MemoryEngine` interface 무변경). 새 Service 1개
  (`ExecutionMemoryStore`, `MemoryEngine`을 감싸는 얇은 계층 —
  `ContextManager`와 병렬 관계, Snapshot이 아니라 Execution 이력을
  다룸). 새 Adapter 0개.
- **Layer**: 새 Layer 없음. `RecommendationExecutionService`(기존
  파일)에 선택적 의존성 1개 추가, `web/server.py`/`web/app.py`
  (기존 파일)에 조립 코드 추가.

**결정(ADR-0053, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- `domain/execution_memory.py`(신규) — `ExecutionMemory` frozen
  dataclass: `task_id`/`action`/`result`("success"|"failure")/
  `timestamp`/`reason`(선택) 5개 필드만.
- `memory/execution_memory_store.py`(신규) — `ExecutionMemoryStore`:
  `record()`는 JSON 직렬화해 `MemoryEngine.remember(uuid, json)`,
  `query(task_id=None)`는 `search("")`(빈 문자열은 모든 값의
  substring)로 전체 key를 얻어 역직렬화 후 timestamp 오름차순 반환.
- `runtime/execution/recommendation_execution_service.py`(확장) —
  `execution_memory_store: ExecutionMemoryStore | None = None` 선택적
  의존성. `execute()`가 `ExecutionDispatcher.dispatch()` 직후 주입돼
  있으면 자동 기록, 미주입 시 M38 이전과 동일.
- `web/server.py`(Composition Root 배선) — `InMemoryMemoryEngine()`
  + `ExecutionMemoryStore`를 조립해 `RecommendationExecutionService`
  에 주입.
- `web/app.py`(확장) — `execution_memory_store`를 선택적으로 받아
  `app.state.execution_memory_store`로 노출(새 REST 엔드포인트
  없음, YAGNI).

**구현 내용**: 위 결정 그대로 5개 파일(신규 2 + 확장 3).

**테스트**: `tests/domain/test_execution_memory.py`(신규 2),
`tests/memory/test_execution_memory_store.py`(신규 6 — record/query
왕복, 정렬, task_id 필터, 빈 조회, 실패 사유 보존, 공유
`MemoryEngine`에서 무관한 key 무시), `tests/runtime/execution/
test_recommendation_execution_service.py`(신규 2 — 주입 시 자동
기록/미주입 시 회귀 없음), `tests/web/test_server.py`(신규 1 —
`build_app()` Composition Root 배선 확인). `pytest` 1021개(기존
1010개 + 신규 11개) 전부 통과, `ruff check src tests` clean,
`mypy`(194 source files) clean.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 기존 27개 Core Domain Interface 변경 없음(`MemoryEngine` 무변경) | ✅ |
| 2 | 새 Interface/Adapter 0개(`ExecutionMemoryStore` 1개는 Service) | ✅ |
| 3 | Execution 결과가 Agent 수동 호출 없이 Memory에 자동 기록됨 | ✅ |
| 4 | `ExecutionMemoryStore.query()`로 저장된 기록을 조회할 수 있음 | ✅ |
| 5 | `ExecutionMemory`에 embedding/score/vector/confidence 없음 | ✅ |
| 6 | `RecommendationRuleAnalyzer`/추천 판단 로직 무변경(Learning 없음) | ✅ |
| 7 | `execution_memory_store` 미주입 시 M38 이전과 완전히 동일하게 동작 | ✅ |
| 8 | 기존 M21~M38 pytest 회귀 없음 + 신규 테스트 통과 | ✅ |
| 9 | `pytest`/`ruff`/`mypy` 통과 | ✅ |
| 10 | Architecture/ADR-0053/TASKS 최신화 | ✅ |

**개선 여지(참고용, 이번에 처리하지 않음)**: 영속화(Vault 파일 등,
프로세스 재시작 시 소실)·Learning(Rule/추천 반영)·REST 조회
엔드포인트는 범위 밖으로 남아 M40(Learning Engine) 이후 논의
대상이다.

**Milestone 39(Execution Memory) T01(ADR-0053 초안 검토·조건부 승인
반영)~T04(구현+통합+테스트+문서화) 전체 완료.**

**사용자 승인(2026-07-30)**: DoD 10개 항목/MDD Review/ADR-0053/
Tests/Documentation을 확인해 **Milestone 39(Execution Memory) 공식
완료(Approved)**. "M29(Project Intelligence)→…→M38(AutomationScheduler
연결)→M39(Execution Memory)"으로 이어지며, Execution Platform이
처음으로 자신의 실행 결과를 스스로 기억하기 시작했다 — 저장과
조회만 제공하고 학습(추천/판단 변경)은 하지 않는다는 계층 분리를
명확히 지켰다.

**다음은 Milestone 40** — 세부 Task는 착수 시점에 별도 제안·승인
후 정의한다.

---

## Pre-M40: Domain Vocabulary & Naming Convention

**목표**(2026-07-30 사용자 요청): M40 착수 전 프로젝트 전체 명명
규칙과 Obsidian Graph 규칙을 먼저 확립한다(ADR-0054). M39 완료 직후
사용자가 "M40 Experience Intelligence"라는 새 이름을 제시하면서, M38
Review가 예고했던 "Learning Engine"과의 관계가 불명확해진 것이
계기다 — Milestone을 더 만들기 전에 이름을 짓는 규칙 자체를
세운다. **문서화 전용 작업**(사용자 명시) — 코드/클래스명/파일명,
기존 Milestone 이름은 변경하지 않는다.

**반영 내용**

1. `docs/ARCHITECTURE.md` 신규 §13(Domain Vocabulary & Naming
   Convention) — Intelligence/Memory/Execution/Guardian을 1급 Domain
   어휘로 정의(정의/책임/범위/대표 산출물/대표 소비자). Engine/
   Lifecycle/Resume/Scheduler/Recommendation/Automation을 이미
   확립된 보조 용어로 정리. Milestone 이름은 `{Domain}
   {Responsibility}` 형식(예: Project Intelligence, Execution
   Memory)만 쓰고, `Knowledge`/`Insight`/`Learning`/`Analyzer`/
   `Manager` 같은 동의어 신설을 금지.
2. `docs/ARCHITECTURE.md` 신규 §14(Obsidian Graph Convention) —
   Graph Cluster를 폴더가 아니라 §13 Domain 기준(🔵Intelligence/🟢
   Execution/🟡Memory/🟣Architecture/🔴Domain/🟠Documentation)으로
   재정의. 현재 Vault 문서 → Cluster 매핑 참고표, Linking Rules
   (의미 있는 관계만 링크/Cross-Cluster 링크 최소화/계층적 링크
   우선/완전 연결 그래프 방지) 포함.
3. `.ai/RULES.md` 신규 §1.5(Vocabulary Reuse First, v0.9.0) — 새
   Milestone/Engine/Service/아키텍처 개념 도입 전 §13 어휘 재사용
   여부를 먼저 확인하는 영구 규칙.

**적용 계획(후속 작업으로 이관)**: Vault 문서에 Domain Cluster
Tag(예: `#cluster/intelligence`)를 일괄 추가하는 작업과
`.obsidian/graph.json`의 실제 Group/Color 설정은 이번 범위에
포함하지 않는다 — 수십 개 문서 Frontmatter 일괄 변경은 리팩토링에
해당해 별도 제안·승인이 필요하다(§14.5).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Domain Vocabulary 4개 용어(Intelligence/Memory/Execution/Guardian) 정의 | ✅ |
| 2 | 보조 용어 6개(Engine/Lifecycle/Resume/Scheduler/Recommendation/Automation) 정리 | ✅ |
| 3 | Milestone Naming Convention("{Domain} {Responsibility}") 명문화 | ✅ |
| 4 | 신규 용어 도입 절차(기존 어휘 우선 확인) 명문화 | ✅ |
| 5 | Obsidian Graph Cluster를 Domain 기준으로 재정의 | ✅ |
| 6 | Linking Rules 4개 항목 명문화 | ✅ |
| 7 | `.ai/RULES.md` §1.5 신규 추가 | ✅ |
| 8 | 코드/클래스명/파일명/기존 Milestone 이름 무변경 | ✅ |
| 9 | `pytest`/`ruff`/`mypy` 기존 상태(1021 passed) 유지 확인 | ✅ |
| 10 | ADR-0054/TASKS/Vault(ADR Index/Milestones Index) 최신화 | ✅ |

**사용자 승인(2026-07-30)**: 위 10개 항목을 확인해 **Pre-M40 Domain
Vocabulary & Naming Convention 공식 완료(Approved)**. M40의 실제
이름은 이 규칙("Experience Intelligence"가 §13.2/§13.3 어휘로
표현 가능한지, 또는 새 Domain 용어가 필요한지)에 따라 착수 시점에
다시 확정한다.

### T01: Obsidian Graph Convention 실제 적용 (2026-07-30)

**목표**(사용자 요청): §14.5가 후속 작업으로 미룬 "`.obsidian/
graph.json`의 실제 Group/Color 설정"을 적용한다. MDD 원칙에 따라
새 Frontmatter Tag를 일괄 추가하지 않고, **이미 존재하는 Tag/
경로(Path) 구조만으로** 6개 Cluster를 분류한다(우선순위: ①기존
메타데이터 ②기존 Tag ③기존 폴더 구조 ④필요시 최소 Frontmatter
제안 — 이번 작업은 ①~③만으로 전부 해결돼 ④는 불필요했다).

**구현**: `.obsidian/graph.json`(신규) — `colorGroups` 6개, 각각
`{Domain}` 소비 Query + 고유 색상.

| Cluster | 색상 | Query 근거 |
|---|---|---|
| 🟠 Documentation | `#FB8C00` | `path:"99 Templates"`/`"01 Overview"`/`"00 System"`/`"13 Daily"` + `tag:#system`/`#ios`/`#android` + `file:"README"` |
| 🔴 Domain | `#E53935` | `tag:#task`(Documentation 경로 제외) |
| 🟣 Architecture | `#8E44AD` | `tag:#architecture`/`#decision`/`#milestone`/`#backend`/`#api`/`#production`(Documentation 경로 제외) |
| 🟡 Memory | `#FDD835` | `tag:#memory` — 현재 일치 문서 없음(M39 Execution Memory가 Vault에 아직 노출되지 않음, ADR-0053 결정) |
| 🟢 Execution | `#43A047` | `tag:#recommendation-execution`/`#automation`/`#dashboard`(Documentation 경로 제외) |
| 🔵 Intelligence | `#4A90D9` | `tag:#project-intelligence`/`#project-context`/`#capability-intelligence`/`#workflow-intelligence`/`#recommendation-intelligence`/`#intelligence-overview`/`#session-resume`(Documentation 경로 제외) |

`99 Templates/`/`01 Overview/`/`00 System/`/`13 Daily/`를 다른 5개
Query에서 명시적으로 제외한 이유: 이 4개 경로 안의 문서는 개별 Tag가
무엇이든(예: `Template - Milestone.md`가 `tag:#milestone`) §14.3
매핑표상 항상 Documentation Cluster에 속해야 하기 때문이다 — Tag만
보면 다른 Cluster와 겹치는 41개 문서 전수를 시뮬레이션 검증해 이
설계로 전부 상호 배타적임(각 문서가 정확히 1개 Cluster에만 속함)을
확인했다.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `.obsidian/graph.json` 생성(기존 설정 없었음 — 새 파일) | ✅ |
| 2 | 6개 Graph Group 생성, 각각 고유 색상 지정 | ✅ |
| 3 | 기존 Tag/경로만으로 문서 분류(새 Frontmatter 추가 없음) | ✅ |
| 4 | 현재 Vault 41개 문서 전수 시뮬레이션 — 상호 배타적 분류 확인 | ✅ |
| 5 | Milestone 이름/ADR/코드/클래스명/파일명/폴더 구조 무변경 | ✅ |

**개선 여지(참고용)**: 🟡 Memory Cluster는 현재 매칭 문서가 없다 —
Execution Memory(M39)를 Vault에 노출하기로 결정하면(현재는
ADR-0053에 따라 영속화하지 않음) 그 문서에 `tags: [memory]`를
붙이는 것만으로 자동 편입된다. Obsidian은 그래프 물리(중심/반발력)
를 Cluster별로 따로 지정하는 기능이 없어 "Architecture가 중심이
된다"는 목표는 설정이 아니라 §14.4 Linking Rules(Index 문서가 가장
많이 링크됨)의 결과로 자연히 달성되도록 남겨둔다.

#### T01-Fix: Graph Group이 실제 Obsidian에서 적용되지 않는 문제 수정 (2026-07-30)

**증상**(사용자 보고): T01에서 만든 `.obsidian/graph.json`을 Python
시뮬레이션으로는 검증했지만, 실제 Obsidian Graph View를 열면 모든
노드가 기본 회색으로 남아 Color Group이 전혀 적용되지 않았다.

**Root Cause 분석**

1. **가장 유력한 원인 — 설정 재로딩 문제**: Obsidian은 `.obsidian/
   graph.json`을 Vault 로딩 시점에 메모리로 읽어들이고, 그 이후에는
   앱을 통해서만(설정 UI 변경 또는 종료 시 flush) 파일에 다시
   쓴다. Obsidian이 이미 실행 중인 상태에서 git이 파일을 외부에서
   직접 덮어쓰면, 실행 중인 Obsidian은 그 변경을 감지하지 못하고
   기존 메모리 상태(Color Group 없음)를 계속 쓰다가, 이후 아무
   설정이나 변경되는 순간 그 "빈 상태"를 다시 파일에 덮어써 우리가
   git으로 반영한 내용을 지울 수도 있다. **6개 Group이 하나도 남김
   없이 전부 회색이라는 증상은 "쿼리 일부가 잘못됨"보다 "파일이
   아예 다시 로딩되지 않음"에 훨씬 더 부합한다** — 쿼리 문법
   오류라면 보통 일부 Group만 실패하고 나머지는 성공하는 부분적
   실패가 나타나기 때문이다.
   → **조치**: 병합 후 Obsidian을 완전히 종료했다가 다시 열거나
   (또는 Vault를 다시 불러오거나) Graph View를 새로 열어야 한다.
2. **쿼리 문법 위험 요소(2차 원인 가능성)**: 기존 쿼리는 `-path:"A"
   -path:"B" -path:"C" -path:"D" (tag:#x OR tag:#y OR ...)`처럼
   **여러 개의 부정(-) 항과 괄호로 묶인 OR 그룹을 한 줄에 혼합**
   했다. Obsidian 공식 문서가 명시적으로 예시로 드는 조합(`tag:#a
   OR tag:#b`, `-tag:#a`, `(tag:#a OR tag:#b) path:"x"`)과 달리, "4개
   부정항 + 괄호 OR 그룹"처럼 복잡하게 중첩된 조합은 공식 예시에
   없어 실제 파서가 의도대로 파싱한다는 보장이 약하다.
   → **조치**: 부정(`-`)과 괄호를 모두 제거하고, **경로(`path:`)
   문자열의 단순 OR 나열만** 쓰도록 전면 재작성했다(아래 참고).
3. **Tag 매칭 의존성 제거**: 기존 쿼리는 YAML Frontmatter
   `tags: [architecture]` 같은 리스트가 Obsidian 내부에서 `#architecture`
   태그로 정확히 색인되는지에 의존했다. 이 자체는 표준 동작이지만,
   경로 기반 매칭보다 검증 표면이 하나 더 있다 — 새 쿼리는 태그에
   전혀 의존하지 않고 폴더/파일 경로만 사용해 검증 표면을
   최소화했다.

**수정된 쿼리**(전부 `path:"..."` 단순 OR 나열, 부정·괄호·태그 없음)

| Cluster | 새 Query |
|---|---|
| 🟠 Documentation | `path:"99 Templates" OR path:"01 Overview" OR path:"00 System" OR path:"13 Daily" OR path:"09 iOS" OR path:"10 Android" OR path:"15 Project Intelligence/README"` |
| 🔴 Domain | `path:"14 Tasks"` |
| 🟣 Architecture | `path:"02 Architecture" OR path:"03 ADR" OR path:"11 Milestones" OR path:"12 Decisions" OR path:"04 Backend" OR path:"05 API" OR path:"08 Production"` |
| 🟡 Memory | `path:"Execution Memory"`(현재 매칭 문서 없음, 의도된 상태) |
| 🟢 Execution | `path:"Recommendation Execution.md" OR path:"07 Automation" OR path:"06 Dashboard"` |
| 🔵 Intelligence | `path:"Project Intelligence.md" OR path:"Project Context.md" OR path:"Capability Intelligence.md" OR path:"Workflow Intelligence.md" OR path:"Recommendation Intelligence.md" OR path:"Intelligence Overview.md" OR path:"Session Resume.md"` |

**검증(Python 시뮬레이션, `path:` substring 매칭 재현)**: 실제 Vault
44개 `.md` 파일 전수 재검증 — 43개가 정확히 1개 Cluster에만
매칭(상호 배타), 루트 `README.md` 1개만 어느 Query와도 겹치지 않는
substring이라 미분류(회색)로 남는다(낮은 우선순위 — 필요하면 별도
Query로 추가 가능, 이번 수정 범위 밖).

**중요한 한계(정직하게 기록)**: 이 세션은 GUI/Obsidian이 설치되지
않은 headless 컨테이너다 — 실제 Obsidian 앱을 실행해 화면으로
색상을 확인하는 것은 이 세션에서 불가능하다. 위 검증은 (1)JSON
유효성 (2)공식 문서에 명시된 단순 연산자(`path:`, `OR`)만 사용
(3)Python으로 재현한 매칭 로직 3가지로 최대한 뒷받침했지만, **최종
확인은 사용자가 실제 Obsidian에서 Graph View를 열어(완전 재시작
후) 직접 봐야 한다** — 이는 대체할 수 없는 검증 단계다.

**Regression 확인**: `docs/ARCHITECTURE.md`/`.ai/TASKS.md`의 Milestone
서술/ADR 본문/코드/클래스명/파일명은 변경하지 않았다 —
`.obsidian/graph.json` 1개 파일만 수정했다. `pytest`/`ruff`/`mypy`는
애초에 이 변경과 무관(Python 코드 없음).

#### T01-Fix 상태: Pending Verification (2026-07-30, 사용자 확정)

**상태: 검증 보류(Pending Verification)** — 두 차례 수정(PR #26, #28)
후에도 실제 환경에서 Graph Group이 적용되는지 이 환경에서는 결론을
낼 수 없다는 것이 확인됐다. 사용자 요청에 따라 **더 이상 `.obsidian/
graph.json`을 수정하지 않는다** — 이 절은 코드/설정 변경이 아니라
검증 상태를 기록하는 것만이 목적이다.

**환경 제약(기록)**

1. 사용자가 실제로 테스트 중인 환경은 **iOS(Obsidian Mobile)뿐**이다
   — Desktop Obsidian 접근이 없다.
2. 이 세션(Claude Code 실행 환경)은 GUI가 없는 headless 컨테이너로,
   Desktop이든 Mobile이든 실제 Obsidian 앱을 실행해 화면을 확인할
   방법이 이 세션에는 전혀 없다.
3. 따라서 **Desktop 환경에서의 검증은 현재 이용 불가능**하다 — Query
   문법이 Desktop에서는 정상 동작하는지조차 이 시점에는 알 수 없다.

**Root Cause를 확정할 수 없는 이유**: 다음 세 가지 가능성 중 무엇이
실제 원인인지 현재 증거로는 구분할 수 없다.

| 가능성 | 설명 | 구분 불가능한 이유 |
|---|---|---|
| (a) `graph.json`/Schema 비호환 | Query 문법 또는 파일 구조가 사용자의 Obsidian 버전과 맞지 않음 | Desktop에서 동일 파일을 열어봐야 확인 가능한데 Desktop 접근이 없음 |
| (b) iOS Graph 구현 자체의 제약 | Obsidian Mobile(iOS)의 Graph View가 Desktop과 다른 렌더링/설정 로딩 경로를 쓸 가능성 | iOS와 Desktop 양쪽에서 같은 파일로 비교 테스트를 해야 구분 가능한데 Desktop이 없음 |
| (c) Obsidian Mobile 버그 | 이전 라운드에서 조사한 "Graph 설정은 Hot-Reload 대상이 아니다"/"기기 간 동기화 후 미반영" 등 Obsidian 자체의 알려진 이슈(Forum "Bug graveyard")가 iOS에서 더 심할 가능성 | Obsidian 개발팀만 확인 가능한 내부 동작이라 외부에서 확정 불가 |

이 셋은 **서로 배타적이지 않고 원인이 여러 개 겹쳐 있을 수도 있다**
— 지금 시점에 하나로 좁히는 것은 증거 부족 상태에서의 추측이라
시도하지 않는다.

**Desktop 접근이 가능해지면 실행할 검증 체크리스트**

- [ ] 1. 동일 Vault를 Desktop Obsidian에서 열고, git `main`의 최신
      `.obsidian/graph.json`(PR #28 버전)을 그대로 사용한다.
- [ ] 2. Desktop에서 완전히 새로 앱을 시작(cold start, 재시작이
      아니라 완전 종료 후 최초 기동)한 상태에서 Settings → Graph →
      Groups를 열어 6개 Group이 목록에 보이는지 확인한다.
      - 보인다 → 파일은 정상적으로 파싱된다는 뜻(원인 (a) 기각).
        다음 단계로.
      - 안 보인다 → 원인 (a)(Schema 비호환) 가능성이 높아진다 —
        Command Palette → "Reload app without saving"을 실행한 뒤
        다시 확인한다(그래도 안 보이면 Schema 문제로 사실상 확정).
- [ ] 3. Groups가 보인다면 Graph View를 열어 실제로 노드에 색이
      입혀지는지 확인한다.
      - 색이 보인다 → Desktop은 정상 동작 — 원인은 iOS 쪽((b) 또는
        (c))으로 좁혀진다.
      - 색이 안 보인다 → Query 자체의 매칭 문제(문서 실제 경로가
        Query와 다른지 재확인) — `docs/ARCHITECTURE.md` §14.3 매핑표와
        실제 Vault 문서 경로를 다시 대조한다.
- [ ] 4. Desktop에서 정상 동작이 확인되면, 같은 Vault를 iOS
      Obsidian에서 열어(동기화 반영 후) 같은 절차(Groups 목록 확인 →
      Graph View 색상 확인)를 반복해 iOS에서만 실패하는지 교차
      검증한다.
- [ ] 5. 위 4단계 결과를 조합해 원인을 (a)/(b)/(c) 중 하나 또는
      조합으로 확정하고, 이 절의 "상태"를 Pending Verification에서
      확정된 결론으로 갱신한다 — 그 결론에 따라서만 `.obsidian/
      graph.json`을 다시 수정한다(근거 없는 재수정 금지, 사용자
      명시적 요청).

**이번 기록의 범위**: 이 절은 검증 상태 기록만 수행한다 —
`.obsidian/graph.json`은 이번에 전혀 수정하지 않았다(PR #28의 내용
그대로 유지). 새 근거 없이는 Graph Query/색상을 바꾸는 PR을 다시
만들지 않는다(사용자 명시).

### T02: M40 Responsibility Analysis (2026-07-30)

**목표**: M40이 실제로 무엇을 하는 Milestone인지 정의한다. ADR-0053
(M39)이 "Learning(Rule 반영)은 M40 이후로 명시적으로 이관"이라고
남긴 대목과, 사용자가 제시한 이름 "Experience Intelligence"를
근거로 두 가지 Responsibility 범위를 검토했다.

- **(a) Read-Only Experience Reporting** — `ExecutionMemoryStore`
  (M39)가 쌓은 기록을 집계해 "이 Task/Action의 성공률·최근 실패
  이력" 같은 요약을 만들어 Vault에 노출한다. `RecommendationRuleAnalyzer`
  (M35)의 판정 로직에는 관여하지 않는다.
- **(b) Experience-Informed Recommendation** — (a)와 동일한 집계에
  더해, 그 결과를 `RecommendationRuleAnalyzer`의 Priority Rule에
  새 입력으로 연결해 "최근 자주 실패한 Task는 우선순위를 낮춘다"
  같은 판단에 반영한다.

**핵심 발견**: (a)와 (b) 둘 다 **부작용이 없다** — Task를 실행하거나
상태를 바꾸지 않는다. (b)가 `RecommendationRuleAnalyzer`의 계산에
관여하더라도, `Recommendation` 자체가 이미 Intelligence Domain
소속(§13.3 "Recommendation은 Intelligence가 계산한 단일 결정")이므로
(b) 역시 Read Only Intelligence 판단 로직의 확장일 뿐, Execution으로
분류되지 않는다. 즉 (a)/(b) 선택은 **Domain을 바꾸지 않는다** — 둘
다 Intelligence다. 정확히 어느 범위로 착수할지는 이 분석의 대상이
아니라 실제 M40 착수 시점의 별도 Scope 제안·MDD Review(§2.1.1)
대상이다.

### T03: Existing Vocabulary Mapping (2026-07-30)

§13.2(1급 Domain)/§13.3(보조 용어) 전체와 T02의 두 범위를 대조했다.

| 어휘 | 정의 | M40과의 부합 여부 |
|---|---|---|
| **Intelligence** | Read Only로 데이터를 분석·요약·판단 | **부합** — (a)/(b) 모두 읽기만 하고 판단만 한다 |
| **Memory** | 저장/검색만, 판단하지 않음 | 불일치 — M40은 판단(집계·분석)이 핵심이라 저장만 하는 Memory로 표현 불가. 원재료(`ExecutionMemory`, M39)는 이미 Memory Domain이 담당 중 |
| **Execution** | 실제 부작용을 일으킴 | 불일치 — M40은 Task를 실행하거나 상태를 바꾸지 않는다 |
| **Guardian** | 아키텍처 규칙 위반 감시(미구현) | 무관 — 전혀 다른 개념 |
| Recommendation(보조) | Intelligence가 계산한 단일 결정 | T02(b)에서만 부분적으로 관련 — 그래도 Domain은 Intelligence로 귀속 |

**결론**: 4개 Domain 중 정확히 **Intelligence**만 M40의 핵심 책임을
정확히 표현한다.

### T04: New Domain Necessity Evaluation (2026-07-30)

§13.4 "새 용어 도입이 허용되는 경우"(기존 어휘 중 어느 것도 핵심
책임을 정확히 표현할 수 없을 때만) 기준으로 판단한다.

- T03에서 **Intelligence**가 M40의 핵심 책임(Read Only 판단)을
  정확히 표현함을 확인했다 — "기존 어휘로 표현 불가능"이라는 새
  Domain 도입 조건을 만족하지 않는다.
- 따라서 **새 Domain 어휘를 만들지 않는다.** §2.1이 예약해 둔
  "Learning Engine"이라는 이름도 사용하지 않는다 — Learning이라는
  별도 Domain을 만들 필요 없이 기존 Intelligence Domain의 확장으로
  충분하다(§13.4가 명시적으로 금지한 동의어 목록의 `Learning`과
  정확히 일치하는 사례).
- **결정**: M40의 Domain은 **Intelligence**(기존 어휘 재사용, 신규
  용어 0개)로 확정한다.

### T05: Final Milestone Naming (2026-07-30)

**형식**: §13.4 Milestone Naming Convention에 따라 `{Responsibility}
{Domain}` 형태(기존 예시 전부가 이 어순 — `Project Intelligence`/
`Workflow Intelligence`/`Recommendation Execution`/`Execution
Memory` 참고)로 짓는다. Domain은 T04에서 확정한 **Intelligence**.

**Responsibility 후보 비교**

| 후보 | 근거 | 평가 |
|---|---|---|
| `Memory` | M40이 분석하는 원재료(M39 `ExecutionMemory`)를 직접 가리킴 | 짧고 정확하지만, M1의 범용 MemoryEngine(Session/Mission Summary)까지 포함하는 것으로 오해될 위험 |
| `Execution Memory` | M39와 완전히 동일한 이름을 그대로 사용 | 가장 정확하지만 3단어(`Execution Memory Intelligence`)로, 기존 명명 관행(전부 2단어)과 어긋남 |
| **`Experience`**(사용자 제안) | M40이 **만들어내는 산출물**(누적된 실행 이력을 판단 가능한 통찰로 바꾼 것)을 가리킴 | `Recommendation Intelligence`(산출물 `Recommendation`을 Responsibility로 삼은 선례)와 동일한 패턴. 2단어 관행과도 일치 |

**결정**: **`Experience Intelligence`**(사용자 원안)를 그대로
확정한다. `Recommendation Intelligence`가 원재료가 아니라
산출물(`Recommendation`)을 Responsibility로 삼은 선례와 동일한
패턴이며, T04에서 확정한 Domain(`Intelligence`)과 결합하면
`{Responsibility} {Domain}` 형식·2단어 관행·§1.5 Vocabulary Reuse
First(신규 Domain 어휘 0개) 전부를 만족한다.

**참고**: 이 결정은 **이름만** 확정한다. 실제 Milestone 40의
Scope/DoD/MDD Review는 T02가 남겨둔 (a)/(b) 범위 선택을 포함해
착수 시점에 별도로 제안·승인받는다(§1.4 Approval Required, §2.1.1
MDD Review Gate) — 이 분석은 그 절차를 대체하지 않는다.

---

## Milestone 40 — Experience Intelligence

**목표**(2026-07-30 사용자 승인, ADR-0055): Pre-M40 T02~T05가 확정한
이름 그대로 착수. `ExecutionMemoryStore`(M39)에 쌓인 실행 기록을
task_id별 성공/실패 집계로 바꾸는 Read Only Intelligence 계층 —
Scope는 **(a) Read-Only Experience Reporting만**(Recommendation
판정 로직 미반영, Learning 없음). 사용자가 최종 승인 시 추가한 DoD
2건: ①Analyzer는 Deterministic ②`ExecutionMemory`는 Immutable
Input으로 취급, 절대 수정하지 않음.

**MDD Review 요약**(제안서 단계, 착수 전 승인)

- **Scope(YAGNI)**: (a)만 — (b)Experience-Informed Recommendation은
  판단 기준 자체를 바꾸는 더 큰 결정이라 범위 밖. 영속화·embedding/
  score도 범위 밖(ADR-0053 원칙 유지).
- **Reuse**: `ExecutionMemoryStore.query()`(M39), `RecommendationRuleAnalyzer`
  (M35, "순수 Analyzer" 패턴), `RecommendationIntelligenceService`
  (M35, "얇은 조합 Service" 패턴), `VaultAdapter`의 8개 `publish_*`
  메서드와 동일한 시그니처 패턴 재사용.
- **Interface/Service/Adapter**: 새 Interface 0개. 새 Service 1개
  (`ExperienceIntelligenceService`). 새 Adapter 0개 — MDD Review
  단계에서 "새 `MemoryAdapter` 신설"을 검토했으나 순수 Passthrough라
  YAGNI로 기각.
- **Layer**: 새 Layer 없음. **다만 §8 규칙 21(Intelligence Layer
  의존 규칙)의 재정의가 필요하다는 것을 MDD Review에서 발견** —
  `ExecutionMemoryStore`는 `integration/`이 아니라 `memory/`에 있어
  기존 "VaultAdapter/AgentAdapter에만 의존" 규칙과 충돌. 사용자가
  최종 승인 시 "특정 클래스명을 규칙에 나열하지 말고 Role(Service
  오케스트레이션 허용/Analyzer 순수성 강제) 기준으로 재정의하라"고
  조건을 제시해 반영(아래 결정 참고).

**구현 중 추가로 발견한 것(제안서에 없었던 내용)**

- `ExecutionMemoryStore.query()`가 domain의 `ExecutionMemory`를 그대로
  반환한다는 사실이 실제 import 시도 단계에서 드러났다 — `intelligence/`
  는 `domain`을 직접 참조할 수 없다는 §8 규칙 21(무변경 부분)과 정면
  충돌. `tests/intelligence/test_intelligence_layering.py`가 이를
  실제로 잡아냈다(MDD Review 단계에서는 발견하지 못함, M38의 "실제
  구현 중 배선 공백 발견" 사례와 같은 성격).
- 해결: `ExecutionMemoryStore.query()`의 반환 타입을 `ExecutionMemoryEntry`
  (신규, `memory/`가 스스로 정의하는 View 타입)로 바꿨다 —
  `integration/vault_adapter.py`의 `TaskDocumentView`가 `domain.Task`
  를 감싸는 것과 동일한 이유·패턴. Analyzer(`experience_rules.py`)는
  이 `ExecutionMemoryEntry`조차 직접 받지 않고, `intelligence/`가
  스스로 정의하는 `ExperienceRecord`만 받는다(Analyzer는 `memory/`도
  import하지 않음 — Role 기반 규칙의 "Analyzer 순수성 강제"를 가장
  엄격하게 만족).

**결정(ADR-0055, 상세 근거는 `.ai/DECISIONS.md` 참고)**

- `memory/execution_memory_store.py`(확장) — `ExecutionMemoryEntry`
  신규, `query()` 반환 타입 변경. `record()`는 domain의
  `ExecutionMemory`를 그대로 받음(무변경).
- `intelligence/experience_rules.py`(신규) — `ExperienceRecord`/
  `ExperienceStat`/`ExperienceReport`/`ExperienceAnalyzer`. 외부
  패키지 import 0개(완전 순수).
- `intelligence/experience_service.py`(신규) — `ExperienceIntelligenceService`
  (`ExecutionMemoryEntry`→`ExperienceRecord` 변환 + Analyzer 호출 +
  `publish()`) + `render_markdown()`.
- `vault/experience_intelligence.py`(신규) — `15 Project Intelligence/
  Experience Intelligence.md` 원자적 덮어쓰기.
- `integration/vault_adapter.py`(확장) — `publish_experience_intelligence()`
  메서드 1개.
- `tests/intelligence/test_intelligence_layering.py`(확장) — `memory/`
  를 import하는 모듈은 반드시 `*Service` 클래스를 정의해야 한다는
  검사 추가(Role 기반, 클래스 이름 나열 없음).
- `docs/ARCHITECTURE.md` §8 규칙 21을 Role 기반으로 재정의, §3.32
  (신규) 추가.
- **Composition Root(`web/server.py`) 배선은 하지 않는다** — M29~M34의
  다른 순수 Intelligence Service와 동일하게, `RecommendationIntelligenceService`
  가 필요로 하지 않는 한 `build_app()`에 연결되지 않는다는 기존
  관례를 그대로 따른다.

**테스트**: `tests/memory/test_execution_memory_store.py`(수정,
`ExecutionMemoryEntry` 반영), `tests/intelligence/test_experience_rules.py`
(신규 7개 — 빈 입력/집계/최신 결과 판정/정렬/Deterministic/입력
불변), `tests/intelligence/test_experience_service.py`(신규 4개 —
빈 리포트/집계/Vault 발행/빈 Markdown), `tests/integration_layer/
test_vault_adapter.py`(신규 1개 — `publish_experience_intelligence`),
`tests/intelligence/test_intelligence_layering.py`(신규 1개 — Role
기반 `memory/` 접근 검사). `pytest` 1033개(기존 1021개 + 신규 12개)
전부 통과, `ruff check src tests` clean, `mypy`(197 source files)
clean.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Scope (a)Read-Only Experience Reporting만 — Recommendation 미반영 | ✅ |
| 2 | `ExperienceAnalyzer`가 Deterministic(같은 입력 → 같은 결과, 시각/난수 미참조) | ✅ |
| 3 | `ExecutionMemory`/`ExperienceRecord`를 Immutable Input으로 취급(frozen, 쓰기 메서드 미호출) | ✅ |
| 4 | 새 Core Domain Interface/Adapter 0개(27종 유지) | ✅ |
| 5 | §8 규칙 21에 `ExecutionMemoryStore` 클래스명 예외 미나열 — Role 기반 재정의로 대체 | ✅ |
| 6 | `RecommendationRuleAnalyzer`/`ExecutionGate`/`ActionBuilder` 등 기존 판단·실행 로직 무변경 | ✅ |
| 7 | 데이터 없을 때 안전하게 "기록 없음" 표시(예외 없음) | ✅ |
| 8 | 기존 pytest 전량 회귀 없음 + 신규 테스트 통과 | ✅ |
| 9 | `pytest`/`ruff`/`mypy` 통과 | ✅ |
| 10 | `docs/ARCHITECTURE.md`/ADR-0055/`.ai/TASKS.md`/Vault 최신화 | ✅ |

**개선 여지(참고용, 이번에 처리하지 않음)**: 영속화(Vault 파일 등,
ADR-0053 유지)·Learning((b) Experience-Informed Recommendation)·
Composition Root 배선·REST 조회 엔드포인트는 범위 밖으로 남아
M41 이후 논의 대상이다.

**Milestone 40(Experience Intelligence) 전체 완료.**

**사용자 승인(2026-07-30)**: 제안서(Scope (a) 확정) → MDD Review
(§8 규칙 21 Role 기반 재정의 조건부 승인) → 구현 완료까지 확인해
**Milestone 40(Experience Intelligence) 공식 완료(Approved)**.
"M29(Project Intelligence)→…→M39(Execution Memory)→M40(Experience
Intelligence)"로 이어지며, Execution Platform이 스스로 기록한
Memory(M39)를 처음으로 판단 가능한 통찰로 바꿨다 — Learning(판단
기준 자체를 바꾸는 것)은 여전히 하지 않아 "저장(M39)과 활용(M40 Read
Only 요약)"의 분리를 지켰다.

**다음은 Milestone 41** — 세부 Task는 착수 시점에 별도 제안·승인
후 정의한다.

---

## Milestone 41 — Architecture Guardian

**목표**(2026-07-30 사용자 승인, ADR-0056): `docs/ARCHITECTURE.md`
§13.2가 예약해 둔 Guardian Domain의 내용을 채운다. 역할 정의: "Guardian
owns the executable representation of architectural rules. Architecture
documentation defines the rules; Guardian encodes them, evaluates
conformance, and publishes architectural health." Scope는 (a)기존
`tests/` 5곳에 흩어진 `ast` 경계 검사 통합 + Vault Read Only 리포트만
— CI 강제 게이트(b)는 이미 §8.6 Merge 조건이 하고 있어 범위 밖.

**MDD Review 요약(제안서 → 2차에 걸친 조건부 승인)**

- **Scope(YAGNI)**: 새 위반 탐지 로직 0개 — 기존 5곳의 규칙만 옮긴다.
  CI 강제 게이트 신설 없음(이미 `pytest` 통과가 §8.6 Merge 조건).
- **Reuse(핵심 발견)**: "아키텍처 규칙 위반 감시"는 이미 `test_
  architecture_boundary.py`/`test_connector_layering.py`/`test_
  conversation_connector_boundary.py`/`test_intelligence_layering.py`
  4개 파일(5개 이상의 개별 테스트)에 중복 구현돼 있었다 — 전부
  `ast` 기반, 전부 각자 `_imported_modules()` 재구현. M41은 새로
  만드는 Milestone이 아니라 통합하는 Milestone.
- **Interface/Service/Adapter**: 새 Core Domain Interface 0개.
  `ArchitectureGuardianService` 1개 신규(Vault 발행이 핵심 진입점,
  사용자 조건). 새 Adapter 0개 — `VaultAdapter`에 `publish_
  architecture_guardian()` 1개만 추가.
- **Layer**: 새 Layer 1개(`guardian/`) — §13.2가 Guardian을 Intelligence
  와 별개 Domain으로 이미 예약해 둔 자리를 채우는 것이라 새 Layer
  도입 자체는 이미 승인된 결정.

**결정(ADR-0056, 상세 근거는 `.ai/DECISIONS.md` 참고, 2차례 조건부
승인 전부 반영)**

- `guardian/models.py`(신규) — `ArchitectureViolation`/
  `ArchitectureCheckResult`/`ArchitectureHealthReport`(`all_passed`
  프로퍼티, 새 판정 로직 아님).
- `guardian/rules.py`(신규) — `ArchitectureRule`은 ABC가 아니라
  `ForbiddenPackageImportRule`/`AllowedImportPrefixRule`/
  `ServiceRoleGatedImportRule` 3개 메서드 없는 `frozen dataclass`의
  Union(사용자 조건: ABC 제거). `GUARDIAN_RULES: Final[tuple[...]]`
  로 실행 중 불변 Registry 고정(사용자 조건).
- `guardian/checker.py`(신규) — `evaluate(rules, src_root)`. `pytest`/
  `assert` 없는 순수 평가기(사용자 조건).
- `guardian/service.py`(신규) — `ArchitectureGuardianService`.
  `publish()`가 핵심 진입점(사용자 조건) — `VaultAdapter.publish_
  architecture_guardian()`(신규 메서드 1개)로 위임.
- `vault/architecture_guardian.py`(신규) — `15 Project Intelligence/
  Architecture Guardian.md` 원자적 덮어쓰기.
- **이전한 5개 규칙**(기존 5곳 중 3개 Rule 형태에 자연스럽게 맞는
  것만): `test_architecture_boundary.py`의 2개(Core Domain↔vault
  개별 금지) + `test_intelligence_layering.py`의 3개(금지 패키지/
  Adapter 화이트리스트/Role 기반 Memory 접근, M40/ADR-0055 재사용).
  두 파일은 이 규칙들에 한해 Guardian 결과를 `assert`하는 얇은
  wrapper로 재작성 — 잡아내는 위반 내용은 100% 동일(회귀 없음).
- **의도적으로 제외한 것(사용자 조건)**: `test_connector_layering.py`
  (Adapter/Peer Connector/Orchestrating Connector 그룹 화이트리스트)
  와 `test_conversation_connector_boundary.py`(단일 파일 기준
  규칙)는 3개 Rule 형태로 자연스럽게 표현되지 않아 억지로
  일반화하지 않고 제외 — 두 파일은 기존 `ast` 검사 그대로 유지.
  `test_architecture_boundary.py`의 "Integration Layer만 양쪽을
  동시에 참조 가능" 검사도 같은 이유로 미이전.

**테스트**: `tests/guardian/test_models.py`(신규 3개)/`test_rules.py`
(신규 3개 — 불변 tuple/이름 중복 없음/frozen)/`test_checker.py`
(신규 7개 — 3개 Rule 타입별 통과/위반 케이스 + 순서 보존)/
`test_service.py`(신규 3개 — 실제 소스 트리 평가/Vault 발행/Markdown
렌더링), `tests/integration_layer/test_vault_adapter.py`(신규 1개),
`tests/integration_layer/test_architecture_boundary.py`(기존 2개
테스트가 Guardian 경유하도록 수정, 1개는 그대로), `tests/intelligence/
test_intelligence_layering.py`(기존 3개 테스트가 Guardian 경유하도록
수정 + 신규 1개 — Registry 누락 방지 안전장치). `pytest` 1051개
(기존 1033개 + 신규 18개) 전부 통과, `ruff check src tests` clean,
`mypy`(203 source files) clean.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Scope (a)통합+Vault Read Only 리포트만 — CI 게이트 신설 없음 | ✅ |
| 2 | `ArchitectureRule`이 메서드 없는 immutable 값 객체(ABC 아님) | ✅ |
| 3 | `GUARDIAN_RULES`가 `Final`+`tuple`(실행 중 변경 불가) | ✅ |
| 4 | `guardian/checker.py`가 `pytest`/`assert`를 전혀 참조하지 않음 | ✅ |
| 5 | `ArchitectureGuardianService.publish()`가 핵심 진입점(부가 기능 아님) | ✅ |
| 6 | Connector 그룹 규칙 2개는 억지로 일반화하지 않고 범위 제외 | ✅ |
| 7 | 이전된 5개 규칙이 기존과 100% 동일한 위반을 잡아냄(회귀 없음) | ✅ |
| 8 | 새 Core Domain Interface/Adapter 0개(27종 유지) | ✅ |
| 9 | 기존 pytest 전량 회귀 없음 + 신규 테스트, `ruff`/`mypy` 통과 | ✅ |
| 10 | `docs/ARCHITECTURE.md`(§3.33/§13.2)/ADR-0056/`.ai/TASKS.md`/Vault 최신화 | ✅ |

**개선 여지(참고용, 이번에 처리하지 않음)**: Connector 그룹 규칙
(`test_connector_layering.py`/`test_conversation_connector_boundary.py`)
의 Guardian 편입은 그룹 기반 Rule 형태가 필요해지는 시점에 별도
논의. CI 강제 게이트, Composition Root 배선도 범위 밖으로 남아
M42 이후 논의 대상이다.

**Milestone 41(Architecture Guardian) 전체 완료.**

**사용자 승인(2026-07-30)**: 제안서 → MDD Review 2차(역할 정의 재확정
+ ArchitectureRule ABC 제거/Final tuple/Connector 규칙 제외) →
구현 완료까지 확인해 **Milestone 41(Architecture Guardian) 공식
완료(Approved)**. "M29(Project Intelligence)→…→M40(Experience
Intelligence)→M41(Architecture Guardian)"로 이어지며, §13.2가
예약해 둔 세 번째 Domain(Guardian)이 처음으로 실제 코드를 갖췄다
— Learning Engine만 남아 "Automation Core" 명명 논의가 계속된다.

**다음은 Milestone 42** — 세부 Task는 착수 시점에 별도 제안·승인
후 정의한다.

---

## Post-M41: Repository Naming Standard

**목표**(2026-07-30 사용자 요청, ADR-0057): M39~M41 실제 코드를
전수 조사하는 "Repository Naming Consistency Review"(분석 전용,
코드 변경 없음)를 수행한 뒤, 그 결과를 일회성으로 끝내지 않고 ADR로
공식화한다. **새 규칙을 만드는 것이 아니라 이미 지켜지던 관행을
문서화**하는 것이 목적 — Milestone 번호가 아닌 Pre-M40/M23-Preparation
과 같은 준비/정리 단계.

**리뷰 결과 요약**: `src/ai_workspace/` 300개 클래스·160여 개 모듈을
전수 조사한 결과, ADR-0054(§13) 확립 **이후** 착수된 M39~M41은 새
어휘 0개로 기존 체계를 정확히 재사용했다(Architecture Alignment
Score: 양호). 확립 **이전**(M29~M34) 코드에만 잔재(`ProjectRecommendationEngine`
의 "Engine" 오용 등 4건)가 남아 있었다 — 규칙 자체는 지금 시점부터
잘 지켜지고 있고, 남은 건 과거 정리뿐이라는 결론.

**반영 내용**

1. `docs/ARCHITECTURE.md` 신규 §13.6(Class/File Naming Standard) —
   클래스 접미사 12종(`*Analyzer`/`*Service`/`*Store`/`*Repository`/
   `*Adapter`/`*View`/`*Record`/`*Report`/`*Result`/`*Rule`/
   `*Manager`/`*Engine`)의 역할을 실측 근거와 함께 표로 고정.
   `*Engine`은 Core Engine(§3.7)/구현 엔진 실행 관리(§3.9) 두 의미로만
   한정. 파일명↔클래스명 대응(`{name}_service.py`는 반드시
   `{Name}Service` 정의), 디렉터리명↔Domain 대응 원칙 명문화.
   `domain/` 패키지와 ADR-0054 "Domain Vocabulary"가 동음이의어임을
   최초로 명시적으로 기록.
2. `.ai/RULES.md` 신규 §1.6(Repository Naming Standard, v0.10.0) —
   위 내용을 영구 규칙으로 참조.

**개선 여지(이번에 실행하지 않음, Rename Candidate로만 기록)**:
`ProjectRecommendationEngine`→`ProjectRecommendationAnalyzer`,
`intelligence/recommendation.py`→`intelligence/project_recommendation.py`,
`tests/integration_layer/` 명칭 유지 + `docs/ARCHITECTURE.md` §9에
주석 추가, `docs/ARCHITECTURE.md` §13.3에 "Store vs Repository"
구분 명문화(문서만, 코드 변경 없음). 전부 사용자 별도 승인 시에만
실행한다.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 클래스 접미사 12종 역할을 실측 근거와 함께 §13.6에 고정 | ✅ |
| 2 | 파일명↔클래스명/디렉터리명↔Domain 대응 원칙 명문화 | ✅ |
| 3 | `domain/` 패키지 vs ADR-0054 "Domain Vocabulary" 동음이의어 기록 | ✅ |
| 4 | `.ai/RULES.md` §1.6 신규 추가 | ✅ |
| 5 | 코드/클래스명/파일명 무변경(분석 전용) | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 기존 상태(1051 passed) 유지 확인 | ✅ |
| 7 | ADR-0057/TASKS/Vault(ADR Index) 최신화 | ✅ |

**사용자 승인(2026-07-30)**: 위 7개 항목을 확인해 **Post-M41
Repository Naming Standard 공식 완료(Approved)**. 발견된 4건의
Rename Candidate는 실행하지 않고 §13.6에 개선 여지로만 남긴다 —
실행은 별도 요청·승인 시점에 진행한다.

**후속 결정 — Boy Scout Rule 채택(2026-07-30)**: 4건의 Rename
Candidate를 처리하는 별도 대규모 Rename PR은 만들지 않는다. 대신
①기존 코드는 해당 파일을 기능 개발로 수정할 일이 생길 때 같은 PR
안에서 함께 Rename하고, ②신규 코드는 §13.6을 예외 없이 100%
적용한다. `.ai/RULES.md` §1.6(v0.10.1)에 영구 반영.

**후속 결정 — Naming Technical Debt Ledger 채택(2026-07-30)**: §13.6의
Rename Candidate 표를 Cleanup Sprint 없이 유지되는 공식 기술 부채
목록으로 명문화한다. 새 위반이 발견되면 표에 행을 추가하고, 항목이
해결되면 행을 지우지 않고 "현재"/"제안" 칸에 취소선(`~~이전 이름~~`)을
긋고 "상태" 칸에 해결 일자와 처리한 PR/커밋을 남긴다 — 표 자체가
변경 이력이 된다. `.ai/RULES.md` §1.6(v0.10.2)에 영구 반영.

---

## Milestone 42 — Recommendation Adaptation

**목표**(2026-07-31 사용자 요청, ADR-0058): M35(Recommendation
Intelligence)의 `NextAction`을 M40(Experience Intelligence)의
`ExperienceReport`로 사후 조정(Adjustment)한다 — ADR-0053(M39)이
"Learning/영속화/Rule 반영은 범위 밖"으로 명시적으로 미뤄뒀던 지점을
처음 다루는 Milestone.

**T02 — Domain Analysis(완료, 사용자 승인)**: Responsibility("과거
실행 결과로 판단 기준을 조정")를 §13.2/§13.3 기존 어휘로 표현
불가능함을 확인(§13.4가 이미 Learning/Insight를 배제해둔 상태).
`Adaptation` 용어 채택(Optimization/Evolution/Refinement 대비 책임을
가장 정확히 표현). Milestone 명명 `Recommendation Adaptation`
(`{Domain} {Responsibility}`).

**T03 — MDD Review(완료, 사용자 승인)**: 신규 Interface/Adapter 없음,
`ExperienceReport`/`NextAction` 그대로 재사용, `intelligence/` 안에
1개 파일(`recommendation_adjustment.py`)로 구현 가능함을 확인. §8/
ADR-0054/ADR-0057 위반 없음.

**T04 — Milestone Proposal(조건부 승인 → 최종 승인, 2026-07-31)**:
아래 5개 조건을 반영하는 것을 전제로 승인됨.

1. Recommendation 생성이 아니라 Adjustment임을 명확히 할 것
2. 입력을 Raw `NextAction` + `ExperienceReport` 중심으로 단순화할 것
3. `ExperienceReport` 생성은 M40 책임임을 Non-goal에 명시할 것
4. §13.3에서 `Adaptation`을 Behavioral Concept로 정의할 것(1급 Domain
   승격 보류)
5. `experience_report=None`일 때 M35와 100% 동일 동작을 DoD에
   명시할 것

**T05 — Implementation(완료)**:
- `intelligence/recommendation_adjustment.py`(신규) —
  `RecommendationAdjustment`/`RecommendationAdjustmentAnalyzer`.
  대상의 과거 실행이 전부 실패(성공 0건)일 때만 추천 보류, 그 밖의
  모든 경우 통과. Deterministic + Immutable Input.
- `intelligence/recommendation_service.py` — `generate()`/`publish()`
  에 `experience_report` 선택적 인자 추가, `RecommendationIntelligenceReport`
  에 `adjusted`/`adjustment_reason` 필드(기본값 `False`/`None`) 추가,
  Vault 문서에 "Adaptation(Milestone 42)" 섹션 추가.
- `docs/ARCHITECTURE.md` §13.3(Adaptation 추가)/§13.4(예시 행 추가)/
  §3.34(신규 서브섹션)/헤더 상태 갱신.
- 테스트 9건 신규(`test_recommendation_adjustment.py` 6건 +
  `test_recommendation_service.py` 3건) — 전체 `pytest` 1060개 통과,
  `ruff`/`mypy` 통과, `guardian.checker.evaluate()` all_passed 유지.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Recommendation 생성이 아닌 Adjustment로 책임 한정 | ✅ |
| 2 | 입력을 Raw `NextAction` + `ExperienceReport`로 단순화 | ✅ |
| 3 | `ExperienceReport` 생성이 M40 책임임을 Non-goal에 명시 | ✅ |
| 4 | `Adaptation`을 §13.3 Behavioral Concept로 정의(1급 Domain 승격 보류) | ✅ |
| 5 | `experience_report=None`일 때 M35와 100% 동일 동작 DoD 충족 | ✅ |
| 6 | 신규 Core Domain Interface/Adapter 0개(27종 유지) | ✅ |
| 7 | `pytest`/`ruff`/`mypy`/Guardian 통과, 회귀 없음 | ✅ |
| 8 | `web/server.py`/`RecommendationExecutionService` 자동 배선 없음(Non-goal) | ✅ |

**사용자 승인(2026-07-31)**: 위 5개 조건 반영을 확인해 **Milestone 42
Recommendation Adaptation 공식 완료(Approved)**.

---

## Milestone 43 — Recommendation Orchestration

**목표**(2026-07-31 사용자 요청, ADR-0059): M42가 Non-goal로 남겨둔
`web/server.py` 자동 배선을 완성한다 — M35(Recommendation)→M42
(Adaptation)→M36(Execution)→M39(Memory)→M40(Experience)로 이어지는
하나의 실행 흐름을 명시적으로 연결한다.

**T02 — Domain Analysis(완료, 사용자 승인)**: 책임("Recommendation
부터 Experience까지 하나의 작업 실행 흐름을 제어")이 기존
`Workflow`(M34, Read-Only Task 상태 분석)에 포함되지 않음을 확인.
`Workflow Runtime`/`Workflow Coordination`은 §13.4가 배제한
`Learning`/`Insight`와 같은 유형의 충돌(이미 다른 의미인 `Workflow`
재사용)을 일으켜 기각. 이 저장소에 이미 확립된 `Orchestrating
Connector`(ADR-0041)/`Orchestrating 패턴`(M32, M40)과 정확히 같은
의미임을 확인하고 `Orchestration`을 재사용(§13.3 구조적 관행으로
최초 등재, 1급 Domain 승격 아님). Milestone 이름은 실제 다루는
범위를 정확히 한정하기 위해 `Recommendation Orchestration`으로
확정(원 제안 `Workspace Orchestration`은 범위가 넓게 들려 기각).

**T03 — MDD Review(완료, 사용자 재검토 요청 반영)**: 신규 Interface/
Adapter 없음, `intelligence_/`가 아니라 `runtime/execution/`(Execution
Domain)에 위치해야 §8 규칙 21 위반 없음을 확인. T04 검토 과정에서
사용자가 "Orchestration이 Recommendation 단계를 완결한 뒤 Execution
에는 순수한 실행 대상만 전달하는 방향이 더 낮은 결합도"라는 재검토를
요청 — 검토 결과 채택하여 `RecommendationExecutionService`(M36)의
`RecommendationIntelligenceService` 의존성 자체를 제거하기로 설계
변경.

**T04 — Milestone Proposal(최종 승인, 2026-07-31)**: 아래 네 가지
책임 분리를 반영해 승인됨.

1. Composition Root(`web/server.py`) — 조립
2. Analyzer(`RecommendationRuleAnalyzer`/`RecommendationAdjustmentAnalyzer`) — 판단
3. `RecommendationOrchestrationService`(신규) — 실행 흐름 제어
4. `RecommendationExecutionService` — 실행(Recommendation 의존성 제거)

**T05 — Implementation(완료)**:
- `runtime/execution/recommendation_orchestration_service.py`(신규)
  — `RecommendationOrchestrationService`: Experience 조회 →
  Recommendation 계산(Adaptation 포함) → Execution 위임을 순서대로
  호출만 함. 판단 로직 0줄.
- `runtime/execution/recommendation_execution_service.py` —
  `RecommendationIntelligenceService` 생성자 의존성 제거,
  `execute()`/`publish()`가 `RecommendationIntelligenceReport`를
  파라미터로 받도록 변경.
- `runtime/automation/automation_action_executor.py` — 주입 의존성을
  `RecommendationExecutionService`에서 `RecommendationOrchestrationService`
  로 교체(파라미터명도 갱신).
- `web/server.py`(Composition Root) — `ExperienceIntelligenceService`
  +`RecommendationOrchestrationService`를 조립해 `AutomationActionExecutor`
  에 주입. `build_app()` 실제 조립 스모크 테스트 통과.
- `docs/ARCHITECTURE.md` §13.3(Orchestration 추가)/§13.4(예시 행
  추가)/§3.35(신규)/헤더 상태 갱신.
- 테스트: 신규 `test_recommendation_orchestration_service.py`(3건),
  `test_recommendation_execution_service.py`/`test_automation_action_executor.py`
  기존 호출부를 `report` 파라미터 방식으로 갱신. 전체 `pytest` 1063개
  통과, `ruff`/`mypy` 통과, `guardian.checker.evaluate()` all_passed
  유지.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 책임이 기존 Workflow에 포함되지 않음을 Domain Analysis로 확인 | ✅ |
| 2 | `Orchestration`을 §13.3 구조적 관행으로 정의(1급 Domain 승격 아님) | ✅ |
| 3 | Milestone 이름을 `Recommendation Orchestration`으로 범위 한정 | ✅ |
| 4 | 네 가지 책임(조립/판단/흐름 제어/실행) 명시적 분리 | ✅ |
| 5 | `RecommendationExecutionService`의 Recommendation 의존성 제거(결합도 개선) | ✅ |
| 6 | `web/server.py` 자동 배선 완성(M42 Non-goal 해소) | ✅ |
| 7 | 신규 Core Domain Interface/Adapter 0개(27종 유지) | ✅ |
| 8 | `pytest`/`ruff`/`mypy`/Guardian 통과, `build_app()` 스모크 테스트 통과 | ✅ |

**사용자 승인(2026-07-31)**: 위 8개 항목을 확인해 **Milestone 43
Recommendation Orchestration 공식 완료(Approved)**.

---

## Post-M43: Recommendation Vocabulary Review

**목표**(2026-07-31 사용자 요청, ADR-0060): M43 완료로 Recommendation의
책임과 경계가 M35~M43 전 구간에서 충분히 명확해진 시점에, "Recommendation"
이라는 용어 자체가 이 책임에 가장 적합한지 Domain Vocabulary
Migration 절차(단순 Rename 아님)로 재검토한다.

**T02 — Domain Vocabulary Analysis(완료, 사용자 승인)**: `src/ai_workspace/`
전수 검색으로 4개 대안의 기존 충돌 여부 확인 — `Suggest`(충돌 없으나
실질적 이득 없음), `Selection`(`EngineSelectionPolicy`/
`EngineSelectionDecision`, M17/18과 충돌), `Decision`(`GateDecision`/
`ApprovalDecision`/`EngineSelectionDecision`/`BudgetDecision`/
`LLMPolicyDecision`/`RetryDecision` 6개 기존 `*Decision` 패턴과 충돌 +
비구속성을 반영하지 못해 의미도 부정확), `Proposal`("Milestone
Proposal" 프로세스 용어와 충돌).

**결정(ADR-0060)**: `Recommendation`을 공식 Domain Vocabulary로
유지. 정의를 한 문장으로 고정 — *"The domain concept responsible
for determining the most appropriate Next Action from the current
project state. It represents an actionable recommendation, not a
mandatory decision."* `docs/ARCHITECTURE.md` §13.3 Recommendation
행에 반영.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 4개 대안(Suggest/Selection/Decision/Proposal)과 객관적 비교 | ✅ |
| 2 | ADR-0060 작성(Context/Considered Alternatives/Decision/Consequences) | ✅ |
| 3 | Recommendation 정의를 한 문장으로 고정, §13.3 반영 | ✅ |
| 4 | 리네이밍 없음(유지 결정이므로 코드 변경 0건) | ✅ |

**사용자 승인(2026-07-31)**: 위 4개 항목을 확인해 **Post-M43
Recommendation Vocabulary Review 공식 완료(Approved)** — Recommendation
유지 확정.

---

## Milestone 44 — Recommendation Explainability

**목표**(2026-07-31 사용자 제안, ADR-0061): M43로 Recommendation(M35)
→Adaptation(M42)→Orchestration(M43)→Execution(M36)→Memory(M39)→
Experience(M40) 내부 루프가 완성된 시점에, Recommendation이 "무엇을
할 것인가"뿐 아니라 "왜 그렇게 결정했는가"를 공식 Domain Concept로
만든다. 사용자가 Responsibility/관계 다이어그램/출력 예시/Domain
Analysis/구현 난이도까지 포함한 상세 제안서를 직접 작성해 제시,
그대로 진행 승인.

**Domain Analysis(사용자 제시, 검토 완료)**: Recommendation과
Explainability는 책임이 다르다 — Recommendation은 "무엇을", Explainability
는 "왜"를 답한다. Explainability는 Recommendation 자체를 바꾸지
않는 별도 Responsibility.

**T05 — Implementation(완료)**:
- `intelligence/recommendation_explanation.py`(신규) —
  `RecommendationExplanationAnalyzer`: `RecommendationIntelligenceReport`
  (M35/M42) + `ExperienceReport`(M40, 선택)를 읽어 5단계 Priority
  Rule 평가 흔적(`PriorityStepTrace`) + Experience 성공률 요약 +
  Adaptation 적용 여부/사유를 재구성. 새 AI 판단·새 지표 없음,
  Deterministic + Immutable Input.
- `intelligence/recommendation_explanation_service.py`(신규) —
  `RecommendationExplanationService`: Analyzer 호출 + Vault 발행만
  조합. `VaultAdapter.publish_recommendation_explanation()`(신규)이
  `15 Project Intelligence/Recommendation Explanation.md`에 발행.
- `Explainability`는 §13.3 Behavioral Concept로 등재(`Adaptation`과
  동일 급, 1급 Domain 승격 보류).
- `runtime/execution/recommendation_orchestration_service.py`
  (M43) — `explanation_service` 선택적 인자 추가. Recommendation
  계산 직후(Execution 위임 전) Explanation을 Vault에 기록 —
  Recommendation→Explainability→Execution 순서. 미주입 시 M43
  이전과 100% 동일 동작.
- `web/server.py`(Composition Root) — `RecommendationExplanationService`
  조립해 `RecommendationOrchestrationService`에 주입.
- `docs/ARCHITECTURE.md` §13.3(Explainability 추가)/§13.4(예시 행
  추가)/§3.36(신규)/헤더 상태 갱신.
- 테스트: `test_recommendation_explanation.py`(5건),
  `test_recommendation_explanation_service.py`(3건),
  `test_recommendation_orchestration_service.py`에 explanation_service
  배선 테스트 2건 추가. 전체 `pytest` 1073개 통과, `ruff`/`mypy`
  통과, `guardian.checker.evaluate()` all_passed 유지, `build_app()`
  스모크 테스트 통과. Vault `Recommendation Explanation.md` 실제
  저장소 상태로 신규 발행.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Recommendation과 Explainability의 책임 차이를 Domain Analysis로 확인 | ✅ |
| 2 | Recommendation 자체를 바꾸지 않음(새 AI 판단 없음) | ✅ |
| 3 | `Explainability`를 §13.3 Behavioral Concept로 등재(1급 Domain 승격 보류) | ✅ |
| 4 | `RecommendationOrchestrationService`에 선택적 주입, 미주입 시 M43과 100% 동일 동작 | ✅ |
| 5 | 신규 Core Domain Interface/Adapter 0개(27종 유지) | ✅ |
| 6 | `pytest`/`ruff`/`mypy`/Guardian 통과, `build_app()` 스모크 테스트 통과 | ✅ |
| 7 | Vault `Recommendation Explanation.md` 실제 발행 확인 | ✅ |

**사용자 승인(2026-07-31)**: 위 7개 항목을 확인해 **Milestone 44
Recommendation Explainability 공식 완료(Approved)**.

---

## Milestone 45 — Workspace Observability

**목표**(2026-07-31 사용자 요청, ADR-0062): M44까지 완성된
Recommendation(M35)→Adaptation(M42)→Explainability(M44)→
Orchestration(M43)→Execution(M36)→Memory(M39)→Experience(M40)
파이프라인은 사후(Vault 문서/pytest 로그)로만 확인 가능했다. 새
AI 판단이나 자동화를 만드는 것이 아니라, Claude Code 세션 안에서
이 파이프라인이 지금 어떤 상태인지 + Claude Code 자체 Runtime
(Model/Effort/Context 사용량)을 **StatusLine으로 실시간 반영**하는
Observability를 Phase 1(Claude Code 내부 표시만, Dashboard/Web UI/
Automation 제외)로 구축한다. 사용자가 표시 항목·설계 원칙
(`WorkspaceRuntimeSnapshot` 읽기 전용 모델, StatusLine은 표시만
담당)까지 제시하고 T01(Domain Analysis)~T04(Implementation Plan)
프로세스로 진행을 요청.

**T01 — Domain Analysis(완료)**: `Observability`는 §13.2 4개 핵심
Domain(Intelligence/Memory/Execution/Guardian) 중 어느 것도 정확히
들어맞지 않는다 — Intelligence와 같이 Read Only지만 "지금 상황이
어떤가"를 새로 판단(분석·요약)하지 않고 이미 계산된 값의 존재
여부만 반영한다는 점이 다르다. 재사용 사례가 이번 1건(StatusLine)
뿐이므로 `Adaptation`/`Explainability`/`Orchestration`과 같은 급의
**Behavioral Concept**로 §13.3에 신규 등재(1급 Domain 승격 보류).

**T02 — Architecture Review(완료)**: 새 Core Domain Interface/Adapter
0개(27종 유지). `VaultAdapter`에 읽기 전용 메서드
`report_last_modified()` 1개만 추가(Reuse First — 새 Adapter 대신
기존 Adapter 확장). `intelligence/`에 얹지 않고 별도 `observability/`
패키지로 분리 — Intelligence의 좁은 의존 계약(`VaultAdapter`/
`AgentAdapter`만)과 Observability의 실제 데이터 소스(Claude Code
StatusLine stdin, Vault/Agent와 무관)가 맞지 않기 때문(Guardian이
Read Only이면서도 별도 패키지를 받은 선례와 동일 논리). `runtime/`
재사용은 기각 — 이미 Agent/Engine/Execution/Automation Runtime을
가리키는 확립된 이름이라 전혀 다른 의미로 재사용하면 이름만으로
책임을 유추할 수 없게 된다.

**T03 — Detailed Design(완료, Phase 1의 정직한 한계 포함)**: 7단계
중 Adaptation/Orchestration은 별도 Vault 산출물이 없음(M42/M43에서
이미 확인된 사실, 다른 산출물에 구조적으로 포함) → `STRUCTURAL_INCLUDED`.
Memory(M39)는 `InMemoryMemoryEngine` 기반이라 프로세스 재시작 시
사라지고 영속화되지 않아 별도 프로세스인 StatusLine에서 조회 불가
→ `NOT_OBSERVABLE`(이유 명시). 실제로 관측 가능한 4단계
(Recommendation/Explainability/Execution/Experience)만 Vault 문서
존재 여부로 `OBSERVED_DONE`/`OBSERVED_NOT_YET` 판정 — 값을 지어내지
않는다(사용자 요청 "추정값 사용 금지"를 그대로 지킴). Claude Runtime
정보는 StatusLine stdin JSON의 공식 문서화된 필드(`model.display_name`/
`effort.level`/`context_window.*`)만 옮기고, 제공되지 않는 필드는
`None`으로 남긴다. `WorkspaceInfo.current_workflow`는 §13.2 Workflow
와 혼동을 피하기 위해 Phase 1은 항상 `None`(사용자가 "선택"으로
표시한 항목, Phase 2 후보).

**T04 — Implementation Plan + 구현(완료)**:
- `observability/snapshot.py`(신규) — `WorkspaceRuntimeSnapshot`/
  `ClaudeRuntimeInfo`/`WorkspaceInfo`/`PipelineStageState`/
  `PipelineStageStatus`: 메서드 없는 `frozen dataclass`/`Enum`만
  (`guardian/rules.py` `*Rule`과 동일 원칙).
- `observability/claude_runtime_analyzer.py`(신규) —
  `ClaudeRuntimeAnalyzer`: StatusLine stdin JSON을 그대로 옮기는
  순수 Analyzer.
- `observability/pipeline_stage_analyzer.py`(신규) —
  `PipelineStageAnalyzer`: `VaultAdapter.report_last_modified()`로
  7단계 상태를 재구성하는 순수 Analyzer.
- `observability/workspace_info_analyzer.py`(신규) —
  `WorkspaceInfoAnalyzer`: `pyproject.toml`/`Milestones Index.md`만
  읽는 순수 Analyzer.
- `observability/runtime_snapshot_service.py`(신규) —
  `RuntimeSnapshotService`: 3개 Analyzer 호출만 조합.
- `observability/statusline_renderer.py`(신규) —
  `StatusLineRenderer`: `WorkspaceRuntimeSnapshot` → StatusLine
  평문 문자열 변환만 하는 순수 함수형 Renderer.
- `observability/statusline_main.py`(신규) — 진입점. stdin 파싱
  실패/예외 발생 시에도 항상 한 줄을 출력(StatusLine이 빈 줄로
  사라지지 않도록).
- `integration/vault_adapter.py`(확장) — `report_last_modified()`
  1개 메서드 추가.
- `.claude/settings.json`(신규) — `statusLine.command`로
  `observability/statusline_main.py` 배선(`PYTHONPATH=src python3 -m
  ai_workspace.observability.statusline_main`).
- `docs/ARCHITECTURE.md` §13.3(Observability 추가)/§13.4(예시 행
  추가)/§3.37(신규)/헤더 상태 갱신.
- 테스트: `tests/observability/`(신규, 5개 파일 17건) +
  `tests/integration_layer/test_vault_adapter.py`에
  `report_last_modified()` 테스트 2건 추가. 전체 `pytest` 1090개
  (17개 신규) 통과, `ruff`/`mypy` 통과, `guardian.checker.evaluate()`
  all_passed 유지, `build_app()` 실제 조립 스모크 테스트 통과.
  `statusline_main.py`를 실제 stdin JSON으로 수동 실행해 실제
  저장소 상태(M44/Recommendation Intelligence.md 등)를 정확히
  반영하는 것을 확인.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Observability가 §13.2 4개 핵심 Domain 중 무엇에도 해당하지 않음을 Domain Analysis로 확인 | ✅ |
| 2 | `Observability`를 §13.3 Behavioral Concept로 등재(1급 Domain 승격 보류) | ✅ |
| 3 | 새 Core Domain Interface/Adapter 0개(27종 유지, `VaultAdapter` 확장 1건만) | ✅ |
| 4 | 기존 Domain(Recommendation/Adaptation/Explainability/Orchestration/Execution/Memory/Experience) 판단 로직 무변경 | ✅ |
| 5 | 관측 불가능한 부분(Adaptation/Orchestration/Memory)을 값 지어내지 않고 정직하게 표시 | ✅ |
| 6 | Claude Runtime 정보가 StatusLine 공식 문서 필드만 사용(추정값 없음) | ✅ |
| 7 | Dashboard/Web UI/Automation/Telemetry 범위 밖 유지(Phase 1 = Claude Code 내부 표시만) | ✅ |
| 8 | `pytest`/`ruff`/`mypy`/Guardian 통과, `build_app()` 스모크 테스트 통과 | ✅ |
| 9 | `.claude/settings.json` StatusLine 실배선 + 실제 stdin 입력으로 수동 검증 | ✅ |

**사용자 승인(2026-07-31)**: 위 9개 항목을 확인해 **Milestone 45
Workspace Observability(Phase 1) 공식 완료(Approved)**.

### Milestone 45 확장 — Execution Environment Observability

**목표**(2026-07-31 사용자 요청, ADR-0063): M45(Claude Runtime +
Pipeline Observability)를 "AI Workspace Runtime"뿐 아니라 "Execution
Environment"(Git/Guardian/Vault/MCP, 특히 Obsidian MCP)까지
관찰하도록 확장. 구현 전에 Claude Code/MCP에서 실제로 관측 가능한
필드를 공식 문서로 먼저 조사하고, 추정값 없이 사용 가능한 항목만
구현하며 관측 불가 항목은 이유와 함께 Not Available로 처리하도록
사용자가 조건을 명시.

**T01 — Domain Analysis(완료)**: 새 Domain도 새 Behavioral Concept도
아니다 — ADR-0062가 §13.3에 이미 등재한 `Observability`를 그대로
확장(관찰 대상만 늘어남, 책임의 성격 동일: 이미 있는 상태를 읽기만
함). §13.3에 새 행을 추가하지 않는다.

**T02 — Architecture Review(완료, 공식 문서 조사 결과)**: StatusLine
stdin JSON에는 MCP 필드가 전혀 없음(공식 문서 확인). `claude mcp
list`(공식 CLI)가 서버별 연결 상태를 문서화된 기호(`✔`/`✘`/`!`/`⏸`)
로 출력(JSON 옵션 없음), `.mcp.json`(공식 문서화된 스키마)이 설정된
서버 목록을 알려줌. Hook payload는 `tool_name`(`mcp__<server>__
<tool>`)만 MCP 식별에 쓸 수 있고 별도 에러/연결 상태 필드는 없음.
`pytest`/`ruff`/`mypy`/Coverage 전체 재실행은 StatusLine 갱신마다
하기엔 너무 느림 — `guardian.checker.evaluate()`만 AST 기반 저비용
평가라 재사용 가능. `observability/` 패키지(M45)를 그대로 확장,
새 패키지 분리 불필요.

**T03 — Detailed Design(완료, 관측 가능/불가능 확정)**: 관측 가능 —
Git(`current_branch`/`working_tree_dirty`/`ahead`/`behind`/
`last_commit_summary`, `git` 하위 명령만, `fetch` 없음), Guardian
(`guardian_all_passed` 재평가, `pytest_failed_count`는 `.pytest_cache`
마지막 로컬 결과만), Vault(`vault_connected`/`current_milestone`(M45
재사용)/`current_adr`/`last_modified_epoch`, `VaultAdapter.
report_last_modified()`만), MCP(`mcp_enabled`/`configured_servers`
는 `.mcp.json`만, `connected_servers`는 `claude mcp list` 문서화된
기호만 매칭). 관측 불가(Not Available) — `ruff_status`/`mypy_status`/
`coverage_percentage`(재실행 비용), MCP `active_server`/
`available_tools`/`last_mcp_call`/`last_mcp_error`(공식 경로 없음,
Hook 신규 도입은 별도 승인 필요), Vault `current_pr`(GitHub API
네트워크+인증 필요), Workspace `current_task`(계측 불가).

**T04 — Implementation Plan + 구현(완료)**:
- `observability/git_runtime_analyzer.py`(신규) — `GitRuntimeAnalyzer`:
  `git` 하위 명령만 읽기 전용 호출, 1.5초 타임아웃.
- `observability/guardian_runtime_analyzer.py`(신규) —
  `GuardianRuntimeAnalyzer`: `guardian.checker.evaluate()` 재사용 +
  `.pytest_cache/v/cache/lastfailed` 읽기.
- `observability/vault_runtime_analyzer.py`(신규) —
  `VaultRuntimeAnalyzer`: `VaultAdapter.report_last_modified()` +
  `WorkspaceInfoAnalyzer` 재사용.
- `observability/mcp_runtime_analyzer.py`(신규) — `McpRuntimeAnalyzer`:
  `.mcp.json` 읽기 + `claude mcp list` 2초 타임아웃 파싱(문서화된
  기호만 매칭).
- `observability/snapshot.py`(확장) — `GitRuntimeInfo`/
  `GuardianRuntimeInfo`/`VaultRuntimeInfo`/`McpRuntimeInfo` 추가,
  `WorkspaceInfo.current_task` 필드 추가(항상 `None`).
- `observability/runtime_snapshot_service.py`/`statusline_renderer.py`
  (확장) — 4개 Analyzer 조합 + StatusLine에 Git/Guardian/Vault/MCP
  줄 추가 렌더링.
- `docs/ARCHITECTURE.md` §3.38(신규)/헤더 상태 갱신.
- 테스트: `tests/observability/`에 4개 파일(18건) 추가. 전체 `pytest`
  1108개(18개 신규) 통과, `ruff`/`mypy` 통과, `guardian.checker.
  evaluate()` all_passed 유지, `build_app()` 스모크 테스트 통과.
  `statusline_main.py` 실제 stdin JSON으로 수동 실행해 Git/Guardian/
  Vault/MCP 줄이 실제 저장소 상태(현재 브랜치, dirty 여부, Guardian
  OK, 최신 Milestone/ADR, MCP 미설정 등)를 정확히 반영하는 것을 확인.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 이번 확장이 새 Domain/새 Behavioral Concept가 아니라 기존 Observability 확장임을 Domain Analysis로 확인 | ✅ |
| 2 | Claude Code/MCP 공식 문서로 관측 가능 여부를 먼저 조사(추측 금지) | ✅ |
| 3 | 관측 불가 항목(ruff/mypy/Coverage/MCP 상세/Current PR/Current Task)을 이유와 함께 Not Available로 표시 | ✅ |
| 4 | 새 Core Domain Interface/Adapter 0개(27종 유지) | ✅ |
| 5 | `ruff`/`mypy`/Coverage 실시간 재실행 없음(StatusLine 지연 방지) | ✅ |
| 6 | `git fetch`/GitHub API 등 네트워크 호출 없음(로컬 캐시 기준만 사용) | ✅ |
| 7 | MCP 관측은 `.mcp.json`/`claude mcp list`(공식 경로)만 사용, 새 Hook 도입 없음 | ✅ |
| 8 | `pytest`/`ruff`/`mypy`/Guardian 통과, `build_app()` 스모크 테스트 통과 | ✅ |
| 9 | `statusline_main.py` 실제 stdin 입력으로 Git/Guardian/Vault/MCP 줄 수동 검증 | ✅ |

**사용자 승인(2026-07-31)**: 위 9개 항목을 확인해 **Milestone 45
확장(Execution Environment Observability) 공식 완료(Approved)**.

---

## Milestone 45-1 — StatusLine Integration Fix (ADR-0069, 완료)

**배경**: M45 구현·테스트는 모두 통과했지만, 사용자가 실제 Claude
Code UI에서 StatusLine이 표시되지 않는다고 보고. 추측 대신 공식
문서(`code.claude.com/docs/en/statusline`) 확인과 실제 실행 검증을
전제 조건으로 조사를 요청.

**조사(공식 문서 확인)**:
- `.claude/settings.json`의 `statusLine.type`/`command` 형식은
  공식 문서와 일치 — 문제 없음.
- `ClaudeRuntimeAnalyzer`가 쓰는 `model.display_name`/`effort.level`/
  `context_window.*`는 모두 공식 문서화된 필드(추측 아님) — 공식
  Mock Input으로 실행해 정상 동작 확인.
- **실제 버그**: `statusline_main.py`의 `ai_workspace.*` import 3개가
  `try/except` 바깥에 있어, import 실패 시 아무 출력 없이 프로세스가
  죽는다 — 공식 문서 Troubleshooting("Status line not appearing")이
  명시하는 실패 모드와 정확히 일치.
- 공식 문서는 별도로 **Workspace Trust 미승인** 시에도 StatusLine이
  아예 실행되지 않는다고 명시(`claude --debug`로 확인 가능) — 이는
  사용자 환경 설정이라 코드로 고칠 수 없음, DoD에 사용자 확인 항목으로
  남김.

**구현**: `observability/statusline_main.py` — import를 `main()`
내부 `try` 블록으로 이동(모든 예외를 항상 한 줄 출력으로 대체).
실패 시에만 `/tmp/statusline.log`에 디버그 기록(정상 동작 시 로그
없음), `AI_WORKSPACE_STATUSLINE_DEBUG=1`로 실제 payload를 opt-in
캡처 가능. 새 Domain/Interface/Service 없음.

**테스트**: `tests/observability/test_statusline_main.py`(신규
6건) — 정상/JSON 파싱 실패/빈 stdin 모두 크래시 없이 한 줄 출력,
디버그 로그는 실패 시에만 기록, 환경 변수로 강제 기록 확인. 전체
`pytest` 1143개(신규 6개, 회귀 없음)/`ruff`/`mypy`(221 source files)
통과. 공식 문서의 Mock Input 예시로 수동 실행해 `model.display_name`/
`effort.level`/`context_window.used_percentage` 정상 반영 확인.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 실제 Runtime JSON Schema를 추측 없이 공식 문서로 확인 | ✅ |
| 2 | `.claude/settings.json` 형식을 공식 문서와 대조 검증 | ✅ |
| 3 | 프로젝트 `.claude/settings.json` 로드 여부 확인(로컬 오버라이드 없음 확인) | ✅ |
| 4 | 실패 시에만 디버그 로그를 남기고 정상 동작 시 로그 없음 | ✅ |
| 5 | 기존 Observability 구조만 재사용, 새 Domain/Interface/Service 없음 | ✅ |
| 6 | 실제 Claude Code UI에서 표시되는 스크린샷/실행 결과 검증 | ⚠️ 사용자 확인 필요 |

**DoD 미충족 항목**: 이 세션은 헤드리스 원격 자동화 환경이라 실제
Claude Code 데스크톱/터미널 UI에 접근할 수 없다. 코드 레벨에서
확인 가능한 모든 것(공식 문서 대조, 실제 payload 스키마, 크래시
안전성, 설정 파일 형식)은 검증했지만, 사용자가 실제 세션에서
`claude --debug`로 최종 확인해야 완료된다 — 특히 Workspace Trust
승인 여부(`Status line command skipped: workspace trust not
accepted` 로그 유무).

### 후속 조사(2026-08-01) — "이 세션 자체가 StatusLine을 지원하는가" 실증 확인

사용자가 "구현을 바꾸기 전에 현재 실행 환경이 실제로 StatusLine을
지원하는지부터 실증하라"고 재요청. 추측 없이 이 세션의 실제
프로세스 상태를 직접 조회해 확인:

- `python3 -c "import sys; print(sys.stdout.isatty(), sys.stdin.isatty())"`
  → 둘 다 `False`. `tty` 명령도 `not a tty`를 반환 — 이 세션은
  터미널에 연결되어 있지 않다.
- 환경 변수 `CLAUDE_CODE_ENTRYPOINT=remote_mobile`,
  `CLAUDE_CODE_REMOTE=true`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=
  cloud_default` — 이 세션이 원격/모바일 진입점에서 시작된 세션임을
  실행 환경 자체가 명시.
- `ps aux`로 이 세션을 구동하는 실제 `claude` 프로세스의 커맨드라인을
  확인한 결과 `--output-format=stream-json --input-format=stream-json
  --debug-to-stderr`로 실행 중 — `claude --help`가 명시하는 기본
  동작("starts an interactive session by default, use -p/--print for
  non-interactive output")과 대조하면, 이 세션은 **비대화형
  (non-interactive, print/stream-json) 모드**로 구동되고 있다.
  StatusLine은 공식 문서상 대화형 터미널 UI 하단 바 기능이며, 이
  모드에는 그 UI 렌더링 루프 자체가 존재하지 않는다.
- `/tmp/statusline.log`가 세션 전체에서 한 번도 생성되지 않음(수동
  테스트로 만든 것 외에는 부재) — `statusline_main.py`가 이 세션
  안에서 단 한 번도 호출된 적이 없다는 증거. "설정 미적용"도 "버전
  차이"도 아니라, 이 세션 타입 자체가 StatusLine 파이프라인을 아예
  트리거하지 않는다(호출 시도조차 없음, 조용한 실패조차 아님).

**결론(실증, 추측 아님)**: 현재 이 세션(Claude Code Remote —
`remote_mobile` 진입점, `--input-format=stream-json
--output-format=stream-json` 비대화형 모드)에서는 StatusLine이
아키텍처상 지원되지 않는다 — 코드 결함이 아니라 이 실행 모드에
대화형 터미널 UI 자체가 없기 때문이다. M45-1에서 수정한 import
안전성 버그는 사용자가 로컬 대화형 터미널에서 `claude`를 실행하는
환경에는 여전히 유효하고 필요하지만, 그 환경에서 실제로 표시되는지는
이 세션이 자체 검증할 수 없다 — 사용자가 로컬 대화형 터미널에서
직접 확인해야 한다(§ DoD 항목 6, Workspace Trust 승인 포함).

---

## Milestone 46 — Vault Information Architecture

**목표**(2026-07-31 사용자 요청, ADR-0064): M39~M45로 기능 아키텍처
(Recommendation/Execution/Memory/Experience/Guardian/Observability/
Explainability/Orchestration)가 안정화된 시점에, Obsidian Vault를
"문서 저장소"가 아니라 "AI Workspace의 Long-term Memory Layer"로
재정의한다. **기능 변경 금지**(위 8개 기능 전부 무변경), Graphify는
참고 모델이되 항목마다 채택/수정/기각 근거 제시, Long-term Memory
First 관점으로 판단 — 3대 원칙을 사용자가 명시.

**T01 — Current Vault Analysis(완료)**: Vault 49개 Markdown 문서를
스크립트로 전수 분석(추측 없음). Frontmatter 100% 커버리지지만
`type` 필드 13/49만 존재, Tag 대부분 1회성(재사용 0회), `15
Project Intelligence/`의 AI 생성 리포트 6개는 outgoing link 0개,
`ADR Index.md`/`Milestones Index.md`가 관련 문서를 `[[WikiLink]]`
가 아닌 백틱 텍스트로만 언급(핵심 발견). 강점(`PROJECT_INDEX.md`가
이미 사실상 MOC, ADR/Decision 2단 계층)과 한계(`13 Daily`/`14
Tasks` 미사용, Concept 문서 부재, `04 Backend`~`10 Android` 정체)
모두 증명.

**T02 — Domain & Architecture Analysis(완료)**: Graphify/Second
Brain 7개 항목(Knowledge Graph First/MOC/Wiki Link First/Metadata
First/Project·Label Standard/Concept/Document Type Color)마다
채택·수정·기각 판단. Dataview는 `.obsidian/community-plugins.json`
이 빈 배열임을 실측 확인해 기각. Document Type Color는 §14.2
(ADR-0054) Domain Cluster를 폐기하지 않고 확장.

**T03 — MDD Review(완료)**: Node Definition(ADR/Milestone/
Decision/Concept/Project Intelligence는 Node, PR/Runtime은 Node
아님), Relationship 9종(별도 Frontmatter 필드 없이 Wiki Link+문구),
Folder/Document/Index/Hub/Concept/Lesson/Roadmap Role, Long-term
Memory Strategy(Concept가 장기 기억의 뼈대, Lesson은 YAGNI로 보류)
확정.

**T04 — Implementation Proposal(완료)**: Migration Plan은 삭제
없는 증분 방식 — Phase 0(이번 PR, IA 문서 5개 신규 생성 +
`PROJECT_INDEX.md` 진입점 1줄)만 즉시 실행. Recommendation Hub/
Concept 문서 8종/기존 문서 `type` 일괄 추가/Roadmap Hub/Color 실제
적용은 Phase 1~5로 제안만(별도 승인 또는 Boy Scout Rule 트리거
대기). `.obsidian/graph.json` 실제 수정은 Desktop 검증 대기로
계속 보류(2026-07-30 동결 유지).

**ADR 검토**: 이번 변경은 Architecture 변경(코드 아님)이지만 향후
Vault 문서 생성이 따라야 할 구속력 있는 표준(Node/Relationship
모델, Metadata Standard, Document Type Color)을 정의하므로 ADR이
필요하다고 판단 — ADR-0054(Domain Vocabulary)/ADR-0057(Naming
Standard) 선례와 동일한 성격. **ADR-0064 작성**.

**산출물**: `02 Architecture/Vault Information Architecture.md`
(마스터), `Metadata Standard.md`, `Document Type Color Strategy.md`,
`Map of Content Guide.md`, `Vault Migration Plan.md`(전부 신규).
`00 System/PROJECT_INDEX.md` Retrieval First 표에 1행 추가(기존
구조 무변경). `docs/ARCHITECTURE.md` §14(연결 문구)/§15(신규)/헤더
상태 갱신.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 기능 변경 없음(8개 기존 기능 전부 무변경) | ✅ |
| 2 | Guardian 통과 | ✅ |
| 3 | 기존 테스트 전부 통과 | ✅ |
| 4 | 기존 Link 최대 유지(삭제 0건, Rename 0건) | ✅ |
| 5 | Metadata 표준 정의 | ✅ |
| 6 | Color Strategy 정의(적용은 Desktop 검증 대기) | ✅ |
| 7 | MOC 구조 정의 | ✅ |
| 8 | Knowledge Graph 설계 완료(Node/Relationship Definition) | ✅ |
| 9 | Long-term Memory Layer 설계 완료 | ✅ |
| 10 | Migration Plan 완료(Phase 0~5) | ✅ |
| 11 | ADR-0064 작성 | ✅ |

**사용자 승인(2026-07-31)**: 위 11개 항목을 확인해 **Milestone 46
Vault Information Architecture 공식 완료(Approved)**.

---

## Milestone 47 — Knowledge Graph Migration

**목표**(2026-07-31 사용자 요청, ADR-0064 구현 단계): M46이 Phase 0
까지만 실행하고 Deferred로 남긴 Metadata Backfill/Wiki Link
Migration/Concept Notes/Hub/Graph Color Migration을 실제 Vault
전체에 적용한다. 새 기능 구현이 아니라 M46 설계의 실행이며, 기능
변경 금지(Recommendation/Execution/Guardian/Automation/Memory/
Observability/Explainability/Orchestration 8개 전부 무변경).

**T01 — Migration Analysis(완료)**: Vault 54개 문서(M46 이후 +5)를
재실측. Metadata(`type`) 13/49 → 부분 완료, Wiki Link(백틱 텍스트
위주) → 미구현, Concept(0개) → 미구현, Hub(비공식 4개만 존재) →
부분 완료, Color(경로 기준 그대로) → 미구현, Lessons(구조 없음) →
미구현으로 분류.

**T02 — Domain Analysis(완료)**: M46 VIA 기준으로 재평가 — Metadata
Coverage 27%, Wiki Link Coverage 낮음(핵심 Index 2곳이 백틱 텍스트
위주), Concept Coverage 0%, Hub Coverage 이름 없는 4개만 존재,
Color Coverage 0%(§14.2 그대로).

**T03 — MDD Review(완료)**: Metadata는 전수 백필로 결정(Boy Scout
Rule 대신 승격, 사용자 DoD 요구 반영). Wiki Link는 ADR Index/
Milestones Index의 실제 Vault 문서 파일명 참조만 전환(코드 경로
백틱은 유지 — Broken/Circular Link 없음을 `find_broken_backlinks()`
로 검증). Concept은 8종 중 5종만 신규 생성(Adaptation/Orchestration/
Explainability는 Recommendation Hub 흐름으로 대체). Hub는 5개
(Recommendation/Architecture/Runtime/Knowledge/Decision) 신규
생성, 기존 Index 대체 안 함. Color는 Desktop 검증 대기 Pending
유지 결정.

**T04 — Implementation(완료)**:
1. Metadata Backfill — 기존 36개 문서에 `type` 추가(54/54 100%).
2. Wiki Link Migration — `ADR Index.md` 백틱 참조 3건을 `[[WikiLink]]`
   로 전환(`Recommendation Explanation`/`Architecture Guardian`),
   `Milestones Index.md` 1건 전환.
3. Concept Notes — `02 Architecture/Concepts/` 7개 + Concept Index.
4. Hub(MOC) — `Recommendation Hub`(`15 Project Intelligence/`),
   `Architecture Hub`/`Runtime Hub`/`Decision Hub`/`Knowledge Hub`
   (`02 Architecture/`).
5. Lessons — `16 Lessons/Lessons.md` 신규(실제 항목은 아직 없음,
   허위 데이터 생성 금지). `vault/mapping.py`
   `VAULT_CONTENT_DIRECTORIES` 17종으로 확장.
6. Graph Color — `.obsidian/graph.json` 실제 적용은 이번에도 하지
   않음(Desktop 검증 대기, 2026-07-30 동결 유지) — DoD의 "Pending
   유지" 조건 그대로 적용.

**ADR 검토**: 새 ADR 작성하지 않음 — ADR-0064의 구현 단계임을
`.ai/DECISIONS.md`에 근거와 함께 명시(ADR-0064 항목 하단 addendum).

**Migration 검증**: `type` 커버리지 13/49(27%)→54/54(100%), Orphan
문서 4→3, Recommendation 파이프라인 리포트 inbound 링크 0건→1~4건씩,
Hub 4(비공식)→9(4 재확인+5 신규), `find_broken_backlinks()` 신규
문서 전수 통과.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 기능 변경 없음(8개 기존 기능 전부 무변경) | ✅ |
| 2 | Guardian 통과 | ✅ |
| 3 | 기존 테스트 전부 통과(1108개, 회귀 없음) | ✅ |
| 4 | Metadata Backfill 완료(54/54, 100%) | ✅ |
| 5 | Wiki Link Migration 완료(ADR/Milestone Index 핵심 참조 전환) | ✅ |
| 6 | Hub(MOC) 구축(5개 신규) | ✅ |
| 7 | Concept Note 구축(7개 + Index) | ✅ |
| 8 | Lessons 구조 구축(`16 Lessons/`, 실제 데이터 없음) | ✅ |
| 9 | Graph Color Migration — Desktop 검증 필요해 Pending 유지 | ✅ |
| 10 | Graph View가 실제 Knowledge Graph를 반영함을 검증(구조적 지표로) | ✅ |

**사용자 승인(2026-07-31)**: 위 10개 항목을 확인해 **Milestone 47
Knowledge Graph Migration 공식 완료(Approved)**.

---

## Milestone 48 — Automation Foundation (완료)

**목표**(2026-08-01 사용자 요청, 재정의): `docs/ARCHITECTURE.md`
§2.1은 원래 "Automation Core" 명명을 Memory Engine(M39)/Architecture
Guardian(M41)/Learning Engine 3대 Engine 완성 이후로 미뤄뒀고, 그
연장선에서 M48을 "Learning Engine 구현"으로 시작할 계획이었다.
그러나 M35~M47 구현 완료 후 사용자가 이 계획을 재검토하도록
지시함 — Recommendation/Execution/Memory/Experience/Guardian/
Observability/Explainability/Orchestration/Knowledge Layer가 모두
갖춰지며 "Automation" 범위가 초기 설계보다 넓어졌으므로, Learning
Engine을 그대로 진행하지 말고 **현재 Runtime Pipeline이 실제로
어디까지 자동 연결돼 있는지 T01 Domain Analysis를 다시 수행**하고,
Learning Engine을 M48에 포함할지 M49 이후로 분리할지를 그 결과로
판단하라는 지시(기존 §2.1 설계보다 현재 구현 상태 우선).

**T01 — Domain Analysis(완료, 코드 전수 조사 기반)**

*조사 방법*: 추측 없이 `web/server.py`(`build_app()`, 203줄
전체)/`runtime/automation/`(Scheduler·ActionExecutor·Service)/
`recommendation_orchestration_service.py`/`guardian/`/
`observability/`/`web/automation_routes.py`를 직접 읽고, `.ai/
TASKS.md` M45~M47 Deferred/Non-goal 목록을 재확인.

*실제 자동 연결 상태(Automated Path, `AutomationScheduler` 기준)*:
- `TriggerKind`(TIME/INTERVAL/EVENT/STARTUP) → `ActionKind.
  RUN_RECOMMENDATION` → `RecommendationOrchestrationService.publish()`
  → `ExperienceIntelligenceService.generate()`(M40) →
  `RecommendationIntelligenceService.generate()`(M35 + M42 Adaptation
  내장) → (선택) `RecommendationExplanationService.publish()`(M44) →
  `RecommendationExecutionService.execute()/.publish()`(M36, 내부에서
  M37 Task Lifecycle 전이 + M39 Execution Memory 저장까지 수행) 순서로
  실제로 매 Trigger마다 실행된다. `web/automation_routes.py`
  `POST /{rule_id}/run`으로 수동 발동도 동일 경로.
- **Gap 1 — Architecture Guardian(M41) 미연결**: `guardian/checker.py`/
  `service.py`는 `observability/guardian_runtime_analyzer.py`(StatusLine
  표시용 재평가)와 `tests/`에서만 호출된다. `runtime/automation/`
  어디에도 import되지 않아 **Guardian 평가가 Automation Trigger로 자동
  발동되는 경로가 전혀 없다** — 사람이 StatusLine을 보거나 `pytest`를
  돌릴 때만 결과를 확인할 수 있다.
- **Gap 2 — Workspace Observability(M45/M45 확장) 완전 분리**:
  `.claude/settings.json`의 `statusLine.command` Hook으로만 실행되는
  세션 전용 기능이며, M45 DoD가 "Dashboard/Web UI/Automation/Telemetry
  범위 밖"을 명시적으로 선언했다(TASKS.md M45 절). `build_app()`/
  `AutomationScheduler`/REST API 어디에도 연결돼 있지 않다 — 이는
  M45가 의도적으로 그렇게 설계한 것이라 "미완성 Gap"이 아니라
  "확정된 설계 경계"로 재확인됨.
- **Gap 3 — `RUN_WORKFLOW` 미지원**: `AutomationActionExecutor`가
  `AutomationActionNotSupportedError`를 던지는 상태 그대로(M21 이후
  변경 없음).
- **관찰(Gap 아님, 참고용)**: `AutomationScheduler._fire()`가 Action
  실행 중 예외를 전부 삼켜(`try/except: pass`) `RUN_RECOMMENDATION`
  실패가 조용히 무시된다 — 이번 Domain Analysis 범위에서는 사실만
  기록하고 판단은 T02(MDD Review)로 이관.

*Learning Engine 재평가*: M42 `RecommendationAdjustmentAnalyzer`
이외에 규칙/추천을 실제로 "학습"(가중치 갱신, 이력 기반 재조정,
영속화)하는 컴포넌트는 전혀 없다. M40(Experience Intelligence)는
설계 단계에서부터 "Learning"이라는 이름 자체를 의도적으로 피해왔고
(TASKS.md M40 T04: "Learning(Rule 반영)은 M40 이후로 이관"), M41
완료 후에도 "Learning Engine만 남아 'Automation Core' 명명 논의가
계속된다"고 반복적으로 미뤄져 왔다(ARCHITECTURE.md §2.1). M42는
그 자리를 채우지 않고 "Adaptation"이라는 §13.3 **Behavioral
Concept**(1급 Domain 아님, 재사용 1건뿐이라 승격 보류)로만
축소해서 다뤘다 — 즉 이 프로젝트는 이미 두 번(M40, M42) "Learning
Engine"이라는 무거운 이름을 스스로 거부한 이력이 있다.

**T01 결론(Gap 종합, 판단은 T02 MDD Review로 이관)**: Learning이
학습할 대상(Guardian 위반 이력, Execution 성공/실패 추세)이 아직
자동으로 쌓이는 경로 자체가 없다(Gap 1) — Guardian이 Automation에
연결되지 않은 상태에서 "학습 Engine"을 새로 설계하면 관찰할 신호가
없는 상태에서 설계하는 것이 되어 DX-02(YAGNI/최소 복잡성) 위반
소지가 크다. 따라서 M48은 §2.1 원안("Learning Engine 구현")을
그대로 따르지 않고, **Gap 1(Guardian↔Automation 연결)을 우선
메우는 "Automation Foundation"으로 재정의하는 것이 현재 구현
상태와 더 일치**한다고 잠정 판단한다. Learning Engine은 Gap 1이
해소된 뒤 실제로 쌓이는 신호를 근거로 M49 이후 별도 제안·승인
대상으로 분리하는 안을 다음 단계(T02 MDD Review)에 상정한다.

**사용자 승인(2026-08-01)**: T01 방향("Automation Foundation" +
Learning Engine M49 이후 분리)에 동의하고, T02(MDD Review)에서
반드시 다루라며 4개 항목(Guardian 실행 시점/실패 정책/Observability
연계/Learning과의 경계)을 명시적으로 지정.

### T02 — MDD Review(완료)

#### Scope Review
- Scope: T01 Gap 1(Architecture Guardian↔Automation 미연결)만
  다룬다. Gap 2(Observability 자동화 미연결)는 M45가 이미 "Dashboard/
  Web UI/Automation 범위 밖"을 명시적으로 확정한 설계 경계이므로
  **이번에도 재확인만 하고 변경하지 않는다**(YAGNI — 사용자가 별도로
  Observability 자동화를 요청한 적 없음). Gap 3(`RUN_WORKFLOW` 미지원)
  /Scheduler 예외 흡수 관찰은 Guardian 연결과 무관한 별개 이슈라 이번
  Scope에서 제외(YAGNI, 필요성이 드러나면 별도 Milestone).
- YAGNI 검토: Guardian↔Automation 연결은 T01에서 실측으로 확인된
  실제 공백이며(추측 아님), Learning Engine이 관찰할 신호(위반 이력)
  가 자동으로 쌓이려면 반드시 필요한 선행 조건이다 — "미래를 위한
  코드"가 아니라 이미 완성된 Guardian(M41)을 실제로 쓰는 것.

#### Reuse Review
재사용 가능한 구성요소:
- `ArchitectureGuardianService`(M41, `guardian/service.py`) —
  `generate()`(Read-Only 평가) + `publish()`(Vault
  `Architecture Guardian.md` 발행) 이미 완비. 신규 평가 로직 불필요.
- `ExecutionGate`(M36, `recommendation_execution_gate.py`) —
  이미 `GateDecision(approved, reason)`으로 "승인/거부 + 이유"
  판정 계약을 갖고 있다. Guardian 위반도 "실행을 승인하지 않는 이유"
  중 하나로 자연스럽게 표현 가능.
- `GateDecision.reason` → `RecommendationExecutionService`의 Vault
  Execution 리포트 렌더링(`recommendation_execution_service.py:188`,
  `f"- 이유: {outcome.gate_decision.reason}"`)이 이미 이유 문자열을
  그대로 노출한다 — Guardian Skip Reason을 위한 새 렌더링 불필요.
- `GuardianRuntimeAnalyzer`(M45 확장, `observability/
  guardian_runtime_analyzer.py`) — 이미 Guardian을 매 StatusLine
  갱신마다 라이브 재평가해 `guardian_all_passed`를 보여주고 있다.
- `VaultAdapter.report_last_modified()`(M45, `PipelineStageAnalyzer`
  가 이미 쓰는 패턴) — "Architecture Guardian.md가 언제 마지막으로
  갱신됐는가"를 새 Adapter 메서드 없이 그대로 재사용 가능.

재사용 전략: 새 평가 로직·새 렌더링·새 Adapter 메서드 없이, 기존
4개 컴포넌트(Guardian Service/Execution Gate/Execution Report
렌더링/Guardian Runtime Analyzer)를 배선만 새로 연결한다.

#### Interface Review
- 신규 Interface 불필요. `ExecutionGate.check()`의 시그니처에
  선택적 파라미터 1개(`guardian_report: ArchitectureHealthReport
  | None = None`, 기본값 `None`이면 M43 이전과 100% 동일 동작)만
  추가 — 새 Interface 계약이 아니라 기존 메서드 확장.

#### Service Review
**1) Guardian 실행 시점 — Pre-Execution(Execution 직전)으로 결정**:
Recommendation(M35)/Adaptation(M42)/Explainability(M44)는 전부
Read-Only 분석이라 Guardian과 무관하게 항상 그대로 생성·발행돼야
한다(Recommendation 자체가 "지금 무엇을 하면 좋을지"에 대한 정보이므로
Architecture 위반과 무관하게 유용하다). 따라서:
  - Recommendation 이전(Pre-flight) — 기각: Read-Only 분석까지
    막을 이유가 없다(과잉 차단, YAGNI 위반).
  - **Execution 이전(Pre-flight for Execution) — 채택**: `Recomm
    endationOrchestrationService.execute()/publish()`가
    `execution_service.execute()`를 호출하기 직전, `guardian_
    service`가 주입돼 있으면 `generate()`(Read-Only, Vault
    미기록)를 호출해 `ArchitectureHealthReport`를 얻고
    `RecommendationExecutionService.execute()`에 전달한다. 이 값이
    최종적으로 `ExecutionGate.check()`의 새 파라미터로 흘러간다.
  - Execution 이후(Post-flight) — 기각: 이미 실행(부작용)이
    발생한 뒤라 "차단"의 의미가 없다. Post-flight 관측은 이미
    M45(`GuardianRuntimeAnalyzer`)가 StatusLine에서 라이브
    재평가로 제공하고 있어 중복.

**2) Guardian 실패 정책 — "Recommendation은 생성하지만 Execution
차단"으로 결정, Override 없음**:
  - Warning만 출력 — 기각: 경고만으로는 Guardian이 "평가·공표"에서
    끝나던 M41 이전과 실질적으로 다르지 않다(연결의 의미가 없음).
  - **Recommendation은 생성하지만 Execution 차단 — 채택**:
    `ExecutionGate.check()`에 `guardian_report`가 주어지고
    `guardian_report.all_passed is False`이면 `GateDecision(
    approved=False, reason=f"Architecture Guardian 위반으로 실행
    차단: {violation 요약}")`을 반환한다. Recommendation/Adaptation/
    Explainability는 이미 Guardian 평가 이전에 계산이 끝나 있으므로
    영향받지 않는다(Orchestration 호출 순서상 자연히 보장됨).
  - Automation 전체 중단 — 기각: `AutomationScheduler`가 다른
    무관한 Rule(`RUN_TASK` 등)까지 멈출 이유가 없다. 기존
    `_fire()`의 "한 Rule 실패가 다른 Rule에 영향 없음" 설계와도
    상충.
  - Override 허용 — **M48에서는 허용하지 않는다**(YAGNI). 아직
    Override가 실제로 필요했던 사례가 없고, Override 정책(누가/
    어떤 조건으로) 자체가 별도 설계 결정이 필요한 사안이라 지금
    설계하면 추측성 코드가 된다. 필요성이 실제로 드러나면 별도
    제안·승인 대상.

**3) Observability 연계 — StatusLine에 "마지막 Automation Guardian
Gate" 1개 필드만 최소 추가, 실시간 재평가는 M45 그대로 유지**:
  M45의 `guardian_all_passed`(라이브 재평가)와 이번에 필요한 정보
  ("Automation이 마지막으로 Execution을 막았는가")는 서로 다른
  정보다 — 전자는 "지금 소스가 통과하는가", 후자는 "가장 최근
  Automation 실행이 Guardian 때문에 막혔는가"(이력). 신규 Vault
  문서/Adapter 없이, 이미 Execution Gate 결과가 기록되는
  `15 Project Intelligence/Recommendation Execution.md`(M36, 위
  Reuse Review의 `GateDecision.reason` 렌더링)를 `GuardianRuntime
  Analyzer`가 `VaultAdapter.report_last_modified()`로 함께 읽어
  `GuardianRuntimeInfo`에 필드 1개(`last_automation_gate_reason:
  str | None`, 최근 Execution 리포트에서 "Architecture Guardian
  위반으로 실행 차단"으로 시작하는 이유 문자열이 있으면 그대로,
  없으면 `None`)만 추가한다. Guardian Running 상태는 별도 표시
  불필요(Guardian 평가는 동기 호출이라 "Running" 중간 상태가
  존재하지 않음 — 실제로 없는 상태를 표시하면 §16 Lessons처럼
  허위 데이터가 된다). Skip Reason은 위 필드가 이유 문자열을 그대로
  전달하므로 별도 Enum 불필요.

**4) Learning과의 경계 — M48은 Execution 결과를 절대 학습하지
않는다(사용자 지정, 명문화)**:
  - Guardian 평가 결과(`ArchitectureHealthReport`)는 `Execution
    Memory`(M39, `ExecutionMemoryStore`)에 기록하지 않는다 — M39는
    Task 실행 결과만 다루는 계약이고, Guardian 위반 이력을 저장하는
    것은 "학습을 위한 데이터 축적"에 해당해 Scope 밖.
  - `RecommendationAdjustmentAnalyzer`(M42 Adaptation)는 Guardian
    결과를 입력으로 받지 않는다 — 여전히 `ExperienceReport`
    (성공/실패 이력)만 본다. Guardian 위반 때문에 Gate가 거부해도
    이는 `ExecutionGate`의 판정이지 Adaptation의 판정이 아니다.
  - Guardian 위반 이력을 근거로 향후 추천을 조정하는 로직(예:
    "이 파일은 자주 위반되니 추천에서 제외") 일체는 M48 범위가
    아니며, M49 이후 Learning Engine 제안 시점에 실제로 쌓인
    `Recommendation Execution.md` 이력(위 3번 필드)을 근거 자료로만
    참고한다 — 지금 그 소비 로직을 설계하지 않는다.

#### Adapter Review
- 신규 Adapter 불필요. `VaultAdapter`도 확장하지 않는다 — Guardian
  Vault 발행은 M41의 `publish_architecture_guardian()`을 그대로
  쓰고, Execution 리포트 발행도 M36의 기존 메서드를 그대로 쓴다
  (내용에 Guardian 이유 문자열이 자연히 포함될 뿐, 메서드 시그니처
  변경 없음).

#### Layer Review
- 새 Layer 없음. `guardian/`(M41)과 `runtime/execution/`(M36/M43)
  사이에 새 의존 방향 1개만 추가된다 — `RecommendationOrchestration
  Service`(execution 담당)가 `ArchitectureGuardianService`를 선택적
  으로 호출(생성자 주입, 기본값 `None`)하는 것으로 Architecture 변경
  없이 흡수 가능. `docs/ARCHITECTURE.md` §2.1 다이어그램/텍스트에
  "Guardian이 Automation Execution Gate에 연결됨" 1문장만 추가
  (레이어 재배치 아님).

#### File Review
| 파일 | 기존 수정 가능 | 신규 필요 | 이유 |
|------|---------------|----------|------|
| `runtime/execution/recommendation_execution_gate.py` | ✅ 수정 | — | `check()`에 선택적 `guardian_report` 파라미터 1개 추가 |
| `runtime/execution/recommendation_execution_service.py` | ✅ 수정 | — | `execute()`/`publish()`가 Guardian 평가 결과를 받아 Gate에 전달 |
| `runtime/execution/recommendation_orchestration_service.py` | ✅ 수정 | — | 선택적 `guardian_service` 주입 + Execution 직전 `generate()` 호출 1줄 |
| `observability/guardian_runtime_analyzer.py` | ✅ 수정 | — | `GuardianRuntimeInfo`에 필드 1개 추가, Execution 리포트 mtime/내용 재사용 |
| `observability/snapshot.py` | ✅ 수정 | — | `GuardianRuntimeInfo`에 `last_automation_gate_reason: str \| None` 필드 추가 |
| `web/server.py` | ✅ 수정 | — | `build_app()`에서 `ArchitectureGuardianService`를 생성해
`RecommendationOrchestrationService`에 주입(Composition Root 배선) |
| (신규 파일) | — | 없음 | 위 6개 기존 파일 확장만으로 충분 |

#### Minimal Implementation Plan
신규 파일 0개, 신규 클래스 0개. 변경만:
1. `ExecutionGate.check(next_action, *, manual_trigger, guardian_report=None)`
   — `guardian_report is not None and not guardian_report.all_passed`
   이면 최우선으로 거부(다른 판정보다 먼저 확인 — Guardian 위반은
   `source`/`manual_trigger` 조건과 독립적으로 항상 차단).
2. `RecommendationExecutionService.execute()/publish()`에
   `guardian_report: ArchitectureHealthReport | None = None` 파라미터
   추가, `ExecutionGate.check()`로 그대로 전달.
3. `RecommendationOrchestrationService.__init__`에
   `guardian_service: ArchitectureGuardianService | None = None`
   추가, `execute()/publish()`에서 Execution 위임 직전
   `guardian_report = self._guardian_service.generate() if
   self._guardian_service else None`.
4. `GuardianRuntimeInfo`에 필드 1개 추가, `GuardianRuntimeAnalyzer`
   가 `VaultAdapter.report_last_modified()`+기존 리포트 텍스트에서
   최근 Guardian 차단 이유만 읽어 채움(신규 파싱은 "Architecture
   Guardian 위반으로 실행 차단"로 시작하는 줄 유무만 확인하는 최소
   로직).
5. `web/server.py`에 `ArchitectureGuardianService` 인스턴스 1개
   생성 후 `RecommendationOrchestrationService` 생성자에 주입.

미주입/미제공 시(기존 테스트, 기존 배선 순서) 전부 M43 이전과
100% 동일 동작 — 기존 15개 Milestone이 반복해 온 "선택적 의존성
주입, 기본값 None" 패턴(M38/M39/M42/M44와 동일) 그대로 재사용.

### 최종 결정
✅ **기존 구조 확장**(새 Interface/Service/Adapter/Layer/File 없음
— `ExecutionGate`/`RecommendationExecutionService`/`Recommendation
OrchestrationService`/`GuardianRuntimeInfo`/`GuardianRuntimeAnalyzer`
/`web/server.py` 6개 기존 파일의 최소 확장만).

**사용자 승인(2026-08-01)**: T02 MDD Review 방향에 최종 동의하며,
Observability 필드를 이유 문자열 1개에서 "PASS/BLOCKED 상태 필드 +
이유 문자열"로 확장하도록 지정(M45 StatusLine에서 Automation 건강
상태를 한눈에 보여주고, M49 Learning/M50 이후 정책 Gate 확장에도
자연스럽게 이어지는 것이 이유). T03 구현 착수 승인.

### T03 — 구현(완료)

MDD Review 계획대로 신규 파일 없이 기존 6개 파일만 확장했다(+
사용자 요청으로 `AutomationGateStatus` Enum 1개 추가):

1. **`guardian/models.py`** — `GUARDIAN_BLOCK_REASON_PREFIX`(Final
   str) 상수 추가. Guardian이 이 문자열의 정본 소유자가 되어
   `ExecutionGate`(Execution 차단 판정)와 `GuardianRuntimeAnalyzer`
   (StatusLine 판독)가 같은 상수를 재사용한다(문자열 중복 정의
   없음).
2. **`runtime/execution/recommendation_execution_gate.py`** —
   `ExecutionGate.check()`에 `guardian_report: ArchitectureHealthReport
   | None = None` 파라미터 추가. 위반 시(`all_passed=False`)
   `source`/`manual_trigger` 조건보다 먼저 거부 — Guardian 위반은
   무조건 최우선으로 차단된다.
3. **`runtime/execution/recommendation_execution_service.py`** —
   `execute()`/`publish()`에 같은 이름의 선택적 파라미터를 추가해
   Gate로 그대로 전달.
4. **`runtime/execution/recommendation_orchestration_service.py`** —
   `guardian_service: ArchitectureGuardianService | None = None`
   생성자 인자 추가. Recommendation/Adaptation/Explainability 계산이
   모두 끝난 뒤(Execution 위임 직전) 주입돼 있으면 `generate()`
   (Read Only, Vault 미기록)를 호출해 Execution Service에 전달한다.
5. **`observability/snapshot.py`** — `AutomationGateStatus`
   Enum(`PASS`/`BLOCKED`/`UNKNOWN`, 사용자 요청으로 MDD Review
   초안에서 확장) 신규. `GuardianRuntimeInfo`에
   `last_automation_gate_status`(기본값 `UNKNOWN`)/
   `last_automation_gate_reason`(기본값 `None`) 필드 추가 — 기존
   호출부는 전부 기본값으로 100% 동일 동작.
6. **`observability/guardian_runtime_analyzer.py`** — 새 Vault
   문서·`VaultAdapter` 메서드 없이, Vault Root == Repository Root
   (ADR-0037)를 이용해 `15 Project Intelligence/Recommendation
   Execution.md`를 `.pytest_cache` 캐시 파일과 같은 방식으로 직접
   읽어 "이유" 줄을 파싱한다. 문서가 없으면(Automation 미실행)
   `UNKNOWN`/`None`으로 정직하게 남긴다(추정 금지). `GUARDIAN_
   BLOCK_REASON_PREFIX`로 시작하면 `BLOCKED`, 아니면(문서는
   있지만 Guardian 사유가 아님) `PASS`로 판정한다.
7. **`observability/statusline_renderer.py`** — Guardian 줄에
   `Automation Gate {PASS|BLOCKED|N/A}` 항목 추가(이유 문자열 자체는
   한 줄 StatusLine에 넣기엔 길어 상태만 표시 — 이유는
   `GuardianRuntimeInfo.last_automation_gate_reason` 필드로 이미
   노출돼 있어 향후 Dashboard 등 다른 Renderer가 재사용 가능).
8. **`web/server.py`** — `ArchitectureGuardianService(vault_adapter,
   Path(config.vault_root) / "src" / "ai_workspace")`를 조립해
   `RecommendationOrchestrationService`에 주입 — Guardian이 처음으로
   자동 실행 경로에 실배선됐다(ADR-0065).

**검증**: `pytest` 1122개(기존 1108개 + 신규 14개, 회귀 없음),
`ruff check src tests`, `mypy src`(220 source files) 전부 통과.
`guardian.checker.evaluate()` 저장소 자체 `all_passed=True` 유지
(새 코드도 5개 규칙 전부 통과). 신규 테스트는 (a) `ExecutionGate`
단위 테스트 3개(Guardian 통과/위반/위반이 manual_trigger보다
우선), (b) `RecommendationExecutionService` 단위 테스트 1개
(Guardian 위반 시 실제 Task가 `todo`에 머무름 확인), (c)
`RecommendationOrchestrationService` 통합 테스트 4개(Guardian
미주입 시 M43과 동일 동작, Guardian 통과 시 실행, Guardian 위반 시
Execution만 차단, Execution 리포트에 위반 이유 기록), (d)
`GuardianRuntimeAnalyzer` 단위 테스트 3개(문서 없음→UNKNOWN, 위반
이유 있음→BLOCKED, 없음→PASS), (e) `StatusLineRenderer` 렌더링
테스트 2개(BLOCKED/PASS 표시), (f) `build_app()` End-to-End
스모크 테스트 1개(실제 위반 파일을 배치하고 `RUN_RECOMMENDATION`
자동 발동 → Execution 리포트에 차단 이유 기록 + `ExecutionMemory`
에 미기록 확인).

**ADR 검토**: 새 ADR 필요 — Execution Gate 정책(Guardian이 무조건
최우선 차단)과 Observability 계약(`AutomationGateStatus`)을 새로
정의하므로 ADR-0056/ADR-0050과 동일한 성격. **ADR-0065 작성**.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Guardian 실행 시점 결정(Pre-Execution) | ✅ |
| 2 | Guardian 실패 정책 결정(Execution만 차단, Override 없음) | ✅ |
| 3 | Observability 연계(PASS/BLOCKED/UNKNOWN 상태 필드 + 이유) | ✅ |
| 4 | Learning과 완전 분리(Execution 결과 학습 없음, M49 이후로 이관) | ✅ |
| 5 | 신규 Interface/Service/Adapter/Layer/File 없음(MDD Review 계획대로) | ✅ |
| 6 | 기존 테스트 전체 통과(회귀 없음) | ✅ |
| 7 | 신규 테스트로 Guardian↔Automation 연결 End-to-End 증명 | ✅ |
| 8 | `ruff`/`mypy`/Guardian 자체 검사 통과 | ✅ |
| 9 | ADR-0065 작성 | ✅ |

**사용자 승인(2026-08-01)**: 위 9개 항목을 확인해 **Milestone 48
Automation Foundation 공식 완료(Approved)**. Learning Engine은
M49 이후 별도 제안·승인 대상으로 확정 분리.

---

## Milestone 49 — Learning Engine (완료)

**완료 처리(2026-08-01)**: PR #43 병합(`b3fdc0d`), Vault/ADR Index 갱신
누락분 PR #44로 보완(`cfea316`). 사용자 승인 완료 — Milestone 49 공식
종료.

**목표**: ADR-0065(M48)가 명시적으로 분리해 둔 "Learning Engine"을
착수한다. ADR-0065 결정 4는 "M49 이후 Learning Engine 제안 시점에
이번에 쌓이는 Recommendation Execution.md 이력을 근거 자료로만
참고한다"고 명시했으므로, T01은 추측이 아니라 **현재 코드에 실제로
존재하는 신호·데이터를 전수 조사**하는 것에서 시작한다.

### T01 — Domain Analysis(진행 중, 코드 전수 조사 기반)

*조사 방법*: `memory/execution_memory_store.py`,
`domain/execution_memory.py`, `intelligence/experience_service.py`,
`intelligence/experience_rules.py`,
`intelligence/recommendation_service.py`,
`intelligence/recommendation_adjustment.py`,
`runtime/execution/recommendation_orchestration_service.py`,
`observability/guardian_runtime_analyzer.py`,
`observability/snapshot.py`를 직접 읽고, `.ai/DECISIONS.md` ADR-0065·
`.ai/TASKS.md` M35~M48(특히 M40, M42, M48 T01) 내 "Learning"/"학습"
전수 검색으로 과거 판단 이력을 재확인.

*이미 존재하는 신호(재사용 대상)*:
- **`ExecutionMemoryStore.query()`**(M39,
  `memory/execution_memory_store.py`) — `task_id/action/result/
  timestamp/reason` 원시 기록을 시각순 정렬로 제공. 집계 기능 없음
  (`ADR-0053`: "저장만, 학습 없음"). 다만 저장소 자체가
  `InMemoryMemoryEngine`(순수 in-process dict, M1)이라 **프로세스
  재시작 시 소멸** — 영속화 안 됨(M45 ADR-0062에서 `NOT_OBSERVABLE`로
  이미 확인됨).
- **`ExperienceIntelligenceService`/`ExperienceAnalyzer`**(M40,
  `intelligence/experience_rules.py`) — task_id별
  `total/success_count/failure_count/last_result/last_timestamp`를
  이미 집계한다. Trend/시간창(windowing)/가중치는 전혀 없음(순수
  누적 카운트). M49가 재사용할 1차 입력 후보 — `ExecutionMemory
  Store`를 직접 재집계하면 이 컴포넌트와 중복.
- **`RecommendationAdjustmentAnalyzer`**(M42, "Adaptation") — 유일한
  기존 "학습형" 로직: `success_count == 0 and failure_count > 0`이면
  추천을 보류하는 이진 규칙 1개뿐. 가중치·점수화는 Non-goal로 명시
  (`recommendation_adjustment.py` 독스트링).
- **`RecommendationIntelligenceService.generate(experience_report=
  None)`**(M35/M40/M42) — 이미 `experience_report`를 선택적 파라미터로
  받아 `RecommendationAdjustmentAnalyzer`에 전달하는 배선이 존재.
  M38/M39/M42/M44/M48이 반복해 온 "선택적 의존성 주입, 기본값
  `None`, 미주입 시 기존 동작과 100% 동일" 관용구가 이 지점에도 이미
  적용돼 있음 — 향후 Learning 신호를 꽂을 자리로 가장 유력한 기존
  Seam.
- **`AutomationGateStatus`(PASS/BLOCKED/UNKNOWN)**(M48,
  `observability/snapshot.py`) — `Recommendation Execution.md`를 매
  실행마다 통째로 덮어써서 얻는 **가장 최근 1건**의 Guardian Gate
  결과만 노출. 다건 이력이 전혀 아님.

*Gap(누락 확인, 추측 아님)*:
- **Gap A — Guardian 위반 다건 이력 없음**: ADR-0065 결정 4가 명시한
  대로 Guardian 평가 결과는 `ExecutionMemoryStore`에 전혀 기록되지
  않는다. `Recommendation Execution.md`도 매번 덮어써지므로, 시간에
  따른 Guardian PASS/BLOCKED 추이를 재구성할 방법이 코드 어디에도
  없다.
- **Gap B — 시간창/추세 계산 없음**: `ExperienceStat`은 전체 누적
  카운트만 제공하고 "최근 N회", "개선/악화 추세" 개념이 전혀 없다.
- **Gap C — 영속 저장소 없음**: `ExecutionMemoryStore`의 백엔드가
  in-process dict뿐이라, 프로세스 재시작(예: 서버 재기동)마다 모든
  실행 이력이 소멸한다. 시간 경과에 따른 "학습"을 하려면 최소한 이
  데이터가 재시작 후에도 남아야 하는지가 먼저 결정돼야 한다.
- **Gap D — 가중치/점수화 매커니즘 부재**: Recommendation 경로
  어디에도 숫자 점수·가중치·파라미터 저장소가 없다. M42의 이진 규칙이
  유일한 전례.

*"Learning" 명명에 대한 프로젝트 자체 이력*: 이 프로젝트는 이미 두 번
(M40, M42) "Learning Engine"이라는 이름을 의도적으로 피하고 각각
"Experience Intelligence"(집계만)와 "Adaptation"(이진 규칙 1개, §13.3
Behavioral Concept로 축소)으로 범위를 좁혀 왔다. `§13.4` 금지 어휘
목록에 `Learning`/`Insight`가 이미 예약돼 있다(진짜 Learning Engine
전용). M49는 그 예약을 실제로 쓰는 첫 Milestone이 된다.

**T01 잠정 결론(사용자 확인 필요)**: 현재 코드에는 "Learning"이 학습할
1차 재료(`ExperienceStat` 누적 카운트, 최근 1건짜리 Guardian Gate
상태)는 있지만, (1) Guardian 위반의 다건 이력, (2) 시간창/추세 계산,
(3) 영속 저장소, (4) 가중치 반영 메커니즘은 전부 없다(Gap A~D). 따라서
M49 Scope는 이 네 가지 중 실제로 필요한 것만 최소로 채우는 방향이어야
하며, MDD Review(T02)에서 사용자가 다음을 결정해야 한다:
1. M49이 실제로 "학습"해서 바꿀 대상은 무엇인가 — Recommendation
   순위/Adaptation 규칙만인지, Guardian 정책까지 포함하는지(M48이
   "Guardian 판단 자체는 M49~M50 이후 정책 Gate 확장 대상"이라고 여지를
   남겨둔 것과 연결).
2. Gap C(영속 저장소 부재)를 M49에서 함께 해결할지, 아니면 in-process
   상태로도 "학습"이 의미 있는 범위(예: 서버 1회 구동 세션 내에서만
   추세 반영)로 M49를 좁힐지.
3. Gap A(Guardian 다건 이력)를 M49에서 새로 쌓기 시작할지, 아니면
   ExecutionMemoryStore의 성공/실패 이력만으로 1차 범위를 한정할지.

**사용자 승인(2026-08-01)**: T01 세 가지 질문에 대해 모두 최소 범위로
결정.
1. 학습 대상 = **Recommendation/Adaptation만**(M42
   `RecommendationAdjustmentAnalyzer`의 이진 규칙을 정교화하는 데만
   집중, Guardian 정책은 건드리지 않음).
2. 영속 저장소(Gap C) = **이번엔 in-process 범위로 한정**(서버 1회
   구동 세션 내 학습만, 영속화는 별도 Milestone).
3. Guardian 다건 이력(Gap A) = **이번엔 쌓지 않음**,
   `ExecutionMemoryStore`의 성공/실패 이력만으로 1차 범위 한정.

즉 M49 Scope = `ExperienceStat`(누적 성공/실패 카운트, 이미 존재)를
근거로 `RecommendationAdjustmentAnalyzer`의 판단을 이진 규칙보다
정교하게(예: 추세/임계값) 조정하는 것으로 확정. Gap A/C는 M49에서
다루지 않고 향후 별도 Milestone 대상으로 명시적으로 배제.

### T02 — MDD Review

#### Scope Review
- Scope: T01에서 사용자가 확정한 대로 `RecommendationAdjustmentAnalyzer`
  (M42)의 단일 이진 규칙(`success_count == 0 and failure_count > 0`이면
  보류)을 `ExperienceStat`(이미 존재하는 필드: `total/success_count/
  failure_count`)만 근거로 조금 더 정교화하는 것으로 한정한다. Guardian
  이력 축적(Gap A)·영속 저장소(Gap C)·새 점수화 체계는 Scope 밖(사용자가
  T01에서 명시적으로 배제).
- YAGNI 검토: 현재 규칙은 "성공 0건 + 실패 1건 이상"일 때만 보류한다 —
  즉 성공 1건 + 실패 20건이어도 보류되지 않는다. 이는 실측으로 확인된
  실제 한계(추측 아님)이며, `ExperienceStat`이 이미 갖고 있는
  `failure_count`/`total`만으로 바로 개선 가능하다 — 새 데이터 수집
  없이 기존 필드의 활용도만 높이는 것이므로 YAGNI 위반이 아니다.

#### Reuse Review
재사용 가능한 구성요소:
- `ExperienceStat`(M40, `experience_rules.py`) — `total/success_count/
  failure_count` 필드가 이미 존재. 새 필드·새 집계 로직 불필요.
- `RecommendationAdjustmentAnalyzer`(M42, `recommendation_adjustment.py`)
  — `analyze()` 시그니처·`RecommendationAdjustment` 반환 타입 그대로
  유지 가능. 내부 판정 조건 하나만 교체.
- `RecommendationIntelligenceService.generate(experience_report=None)`
  (M35/M40/M42) — 이미 뚫려 있는 배선. 변경 불필요.

재사용 전략: **새 파일·새 클래스·새 Interface를 전혀 만들지 않는다.**
`RecommendationAdjustmentAnalyzer.analyze()` 내부의 단일 조건식만
"성공 0건"에서 "실패율이 임계값을 넘고 표본이 충분함"으로 교체한다.

**Naming 재확인(사용자 T01 결정 반영)**: 이 프로젝트는 이미 M40/M42에서
"Learning Engine"이라는 이름을 의도적으로 피해 왔고, T01에서 사용자가
Scope를 "기존 Adaptation 규칙의 정교화"로 좁혔다 — 즉 이번 변경은 새
Domain 개념이나 새 Service를 만드는 것이 아니라 **기존
`RecommendationAdjustmentAnalyzer` 내부 로직 1건 교체**에 그친다. 따라서
`§13.4` 금지 어휘(Learning/Insight)를 실제로 쓸 만한 새 1급 개념이 이번
Milestone에는 생기지 않는다 — Milestone 제목은 "Learning Engine"으로
유지하되(사용자가 이미 M48 승인 시 이 이름으로 확정), 실제 산출물은 새
"Engine" 클래스가 아니라 기존 Analyzer의 규칙 정교화임을 명확히 기록한다.

#### Interface Review
- 신규 Interface 불필요. `RecommendationAdjustment`/`analyze()` 시그니처
  변경 없음(순수 내부 로직 교체).

#### Service Review
**규칙 정교화 — "실패율 임계값 + 최소 표본" 방식으로 결정**:
- 기각 1 — 단순 실패율(`failure_count / total > threshold`)만 사용:
  표본이 1건(실패 1건, 실패율 100%)이어도 보류돼 버려 기존 "성공 0건"
  규칙보다 더 공격적으로 보류하는 회귀가 생긴다(성공 0건 + 실패 1건은
  기존 규칙도 이미 보류 대상이라 문제 없지만, 최소 표본 없이 임계값만
  쓰면 "성공 0건" 조건이 사실상 무의미해진다).
- **채택 — 실패율(`failure_count / total >= 임계값`) AND 최소 표본
  수(`total >= 최소 표본`) 둘 다 만족할 때만 보류**: 기존 규칙("성공
  0건 + 실패 1건 이상")을 포함하는 상위 집합으로 확장 가능(임계값=1.0,
  최소 표본=1로 두면 기존 규칙과 100% 동일 — 회귀 없음을 보장하는
  근거). 표본이 적을 때(예: 실패 1건뿐) 성급하게 보류하지 않도록
  최소 표본 조건을 추가하는 것이 실제 "학습"에 해당하는 정교화 지점.
- **사용자 승인(2026-08-01)**: 실패율 임계값 = **100%**(`success_count
  == 0`, 기존 조건 그대로 유지), 최소 표본 수 = **3**(`total >= 3`,
  신규 추가). 즉 새 규칙 = `success_count == 0 and total >= 3`. 기존
  규칙(`success_count == 0 and failure_count > 0`, 즉 `total >= 1`)
  대비 최소 표본 조건만 1 → 3으로 강화 — 실패 1~2건만으로 성급하게
  보류하지 않고, 3건 이상 실패가 쌓였을 때만 보류하도록 정교화한다.

#### Adapter Review
- 신규 Adapter 불필요. Vault 발행 경로(`Recommendation Execution.md`,
  `RecommendationExecutionService`)는 변경 없음 — `reason` 문자열
  내용만 달라질 수 있음(기존 렌더링 그대로 재사용).

#### Layer Review
- 신규 Layer 불필요. `intelligence/` 내부 기존 Analyzer 파일 하나만
  수정.

#### File Review
- 새 파일 없음. `src/ai_workspace/intelligence/recommendation_adjustment.py`
  기존 파일만 수정. 테스트도 기존
  `tests/intelligence/test_recommendation_adjustment.py`에 케이스
  추가(신규 테스트 파일 불필요).

### T03 — Implementation(완료)

- `intelligence/recommendation_adjustment.py`: `_MIN_SAMPLE_SIZE_
  FOR_WITHHOLD: Final[int] = 3` 상수 추가, `analyze()`의 보류 조건을
  `success_count == 0 and failure_count > 0`에서 `success_count == 0
  and total >= _MIN_SAMPLE_SIZE_FOR_WITHHOLD`로 교체. 모듈/클래스
  독스트링에 ADR-0066 근거 반영.
- `tests/intelligence/test_recommendation_adjustment.py`: 기존
  "전량 실패 시 보류" 테스트를 표본 3건으로 조정, "표본 부족(실패
  2건)이면 보류하지 않는다" 신규 테스트 1건 추가.
- `tests/intelligence/test_recommendation_service.py`,
  `tests/runtime/execution/test_recommendation_orchestration_service.py`:
  기존 "전량 실패 시 보류" 테스트가 표본 1건을 쓰고 있어 새 규칙
  아래에서는 더 이상 보류되지 않으므로, 표본 3건(실패 3건)으로 조정
  (회귀 아님 — 새 규칙의 의도된 동작).
- `.ai/DECISIONS.md`: ADR-0066 신규 작성.

**완료 체크리스트**:

| # | 항목 | 결과 |
|---|------|------|
| 1 | 새 Domain/Service/Interface/Adapter/Layer/File 없음(기존 파일 1개만 수정) | ✅ |
| 2 | 기존 규칙(표본 1건부터 보류)의 상위 집합 — 회귀 없음 근거 명시 | ✅ |
| 3 | 표본 부족(실패 1~2건) 시 보류하지 않음을 신규 테스트로 증명 | ✅ |
| 4 | 기존 테스트 전체 통과(의도된 동작 변화만 반영, 그 외 회귀 없음) | ✅ |
| 5 | `ruff`/`mypy`(220 source files) 통과 | ✅ |
| 6 | ADR-0066 작성 | ✅ |
| 7 | Guardian 다건 이력·영속 저장소는 이번 Scope에서 명시적으로 배제 | ✅ |

`pytest` 1123개(신규 1개, 회귀 없음) 전부 통과.

**사용자 승인(2026-08-01)**: 위 7개 항목 확인 완료 — Milestone 49
Learning Engine 공식 완료 승인됨.

---

## Milestone 50 — Learning Persistence (완료)

**목표**: M49가 "in-process 범위로 한정"했던 `ExecutionMemoryStore`의
학습 데이터를 파일로 영속화해 서버 재시작 후에도 학습 이력이 유지되게
한다. 사용자가 M50 로드맵에서 명시한 범위: "in-process Learning을
영속 저장 / 재시작 후에도 학습 유지".

### T01 — Domain Analysis(완료)

*조사 방법*: `interfaces/memory_engine.py`,
`memory/memory_engine.py`, `memory/execution_memory_store.py`,
`web/server.py`(Composition Root), `storage/` 하위 기존 File 구현체
전수 조사.

*발견*:
1. `MemoryEngine` Interface(remember/recall/search)는 이미 존재 —
   새 Interface 불필요.
2. 구현체는 `InMemoryMemoryEngine` 하나뿐이며, 사용처는
   `web/server.py:125`(`ExecutionMemoryStore(InMemoryMemoryEngine())`)
   단 한 곳뿐 — 영향 범위가 명확히 한정됨.
3. `storage/`에 이미 확립된 File 기반 영속화 패턴 존재
   (`FileAgentRepository`/`FileProjectRepository`/
   `FileKnowledgeRepository`) — JSON 직렬화, `base_dir` 주입.
4. 이 갭은 ADR-0053("영속화는 이번 Milestone 범위 밖 — YAGNI")과
   `observability/pipeline_stage_analyzer.py`(M45)의
   `Memory: NOT_OBSERVABLE` 상태로 이미 문서화되어 있던 알려진 한계.

*결론*: 새 Domain/Interface/Service 없이, 기존 `MemoryEngine`을
구현하는 `FileMemoryEngine`(`storage/` 하위) 하나만 추가하고
`web/server.py`의 `InMemoryMemoryEngine()`을 교체 — Reuse-First 조건
충족.

**사용자 승인(2026-08-01)**: 영속 파일 위치를 "vault_root 하위 전용
디렉터리"로 확정(`ProductionConfig`에 새 필드를 추가하지 않고 기존
`vault_root`만으로 경로 계산).

### T02 — MDD Review(완료)

- **Scope**: `ExecutionMemoryStore`가 쓰는 `MemoryEngine` 구현체
  하나만 교체. `ExecutionMemoryStore`/`MemoryEngine` Interface 자체는
  무변경.
- **Reuse**: `MemoryEngine` Interface, `storage/` 디렉터리의 File 구현
  패턴(JSON 직렬화 + `base_dir` 생성자 주입)을 그대로 재사용. 새
  포맷/새 계약을 만들지 않는다.
- **Interface**: 신규 Interface 없음 — `FileMemoryEngine`은 기존
  `MemoryEngine(ABC)`을 구현만 한다.
- **Service**: 신규 Service 없음.
- **Adapter**: `storage/file_memory_engine.py`에 `FileMemoryEngine`
  신설. 저장 형식은 `FileAgentRepository`(entry당 파일)가 아니라
  key-value 전체를 담는 **단일 JSON 파일**(`{key: value}` dict) —
  `MemoryEngine.search("")`가 전체 키를 얻는 데 쓰이는 현재
  `ExecutionMemoryStore` 사용 패턴과 가장 자연스럽게 맞는 표현이라
  entry-per-file보다 적합하다고 판단(YAGNI, 불필요한 파일 수 증가
  방지).
- **Layer**: `storage/`는 이미 Infrastructure Layer로 확립된 위치 —
  새 Layer/디렉터리 불필요.
- **File**: `web/server.py` Composition Root에서
  `InMemoryMemoryEngine()` → `FileMemoryEngine(<vault_root>/
  .ai-workspace-data)`로 1줄 교체.

*기각한 대안*:
1. `ProductionConfig`에 `data_dir` 필드 신규 추가 — 사용자가
   "vault_root 하위 전용 디렉터리"를 선택해 불필요.
2. `FileAgentRepository`처럼 key당 파일 — entry 수가 늘어날수록 파일
   수가 무한정 증가하고, `search("")` 시 전체 디렉터리를 스캔해야
   해 단일 JSON dict보다 복잡도가 높음.
3. SQLite 등 별도 저장 엔진 도입 — 현재 규모(단일 프로세스,
   in-process 대체 목적)에 과함(YAGNI).

**사용자 승인(2026-08-01)**: 위 T02 설계로 T03 구현 진행 승인됨.

### T03 — Implementation(완료)

*수정 파일*:
- `src/ai_workspace/storage/file_memory_engine.py`(신규) —
  `FileMemoryEngine(MemoryEngine)`, 단일 JSON 파일 key-value 영속화.
- `src/ai_workspace/web/server.py` — `execution_memory_store` 조립
  부분의 `InMemoryMemoryEngine()`을 `FileMemoryEngine(<vault_root>/
  .ai-workspace-data)`로 교체, docstring 갱신.
- `src/ai_workspace/observability/pipeline_stage_analyzer.py` —
  Memory 단계 `NOT_OBSERVABLE` note 텍스트를 "영속화는 됐지만 읽기
  배선이 없다"로 정확하게 갱신(로직/상태값 변경 없음).
- `.gitignore` — `.ai-workspace-data/` 추가(런타임 상태, 커밋 대상
  아님).
- `tests/storage/test_file_memory_engine.py`(신규 7건).
- `.ai/DECISIONS.md`(ADR-0067), `docs/ARCHITECTURE.md`(§2.1).

| # | 완료 조건 | 상태 |
|---|---|---|
| 1 | 새 Domain/Service/Interface 없이 기존 `MemoryEngine` 구현만 추가 | ✅ |
| 2 | 저장 위치 `<vault_root>/.ai-workspace-data/`(사용자 승인) | ✅ |
| 3 | 단일 JSON 파일 key-value 형식(사용자 승인) | ✅ |
| 4 | `web/server.py` Composition Root 1곳만 교체, 다른 사용처 무변경 | ✅ |
| 5 | 재시작 후에도 학습 이력 유지(영속성 회귀 테스트로 검증) | ✅ |
| 6 | Observability 배선은 Scope 밖으로 명시적 분리 | ✅ |
| 7 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1130개(신규 7개, 회귀 없음)/`ruff`/`mypy`(221 source files)
전부 통과.

**사용자 승인(2026-08-01)**: 위 7개 항목 확인 완료 — Milestone 50
Learning Persistence 공식 완료 승인됨. PR #45(코드) 병합(`d721857`),
PR #46(Vault Index 보완) 병합(`8333888`), `main` 반영 확인.

---

## Milestone 51 — Learning Evolution (완료)

**목표**: M49/M50이 만든 "실패율 100% + 표본 3건 이상" 단일 규칙을
추세(trend)/가중치/Decay 기반으로 확장해 Recommendation 품질을
높인다. `RecommendationAdjustmentAnalyzer` 독스트링에 명시된 Non-goal
("우선순위 재설계·점수화·가중치 학습은 하지 않는다")을 이번
Milestone에서 부분적으로 해제한다.

### T01 — Domain Analysis(완료)

*조사 방법*: `intelligence/experience_rules.py`,
`intelligence/recommendation_adjustment.py`,
`intelligence/experience_service.py`,
`intelligence/recommendation_explanation.py` 전수 조사.

*발견*:
1. `RecommendationAdjustmentAnalyzer` 독스트링에 이미 "우선순위
   재설계·점수화·가중치 학습은 하지 않는다(Non-goal)"이라고 명시
   — 이번 Milestone이 이 Non-goal을 Adaptation 범위 안에서 해제.
2. `ExperienceRecord`(M40)는 이미 개별 실행 기록마다 `timestamp`를
   가지며 `ExperienceAnalyzer._summarize()`가 `sorted(entries,
   key=timestamp)`로 시간순 정렬까지 이미 수행 — 추세 계산에 필요한
   원재료는 이미 존재, 새 저장소·새 필드 수집 불필요.
3. `ExperienceAnalyzer._summarize()`는 현재 단순 집계(성공/실패
   카운트 + 최근 1건)만 하고 있어, 추세 신호를 추가하려면 이 지점을
   확장하는 것이 자연스러운 재사용 지점.
4. `ExperienceStat`은 `experience_rules.py` 한 곳에서만 생성되고,
   소비처는 `experience_service.py`(Markdown 렌더링),
   `recommendation_explanation.py`(성공률 텍스트),
   `recommendation_adjustment.py`(보류 판정) 3곳뿐 — 필드 추가의
   영향 범위가 명확히 한정됨.

**사용자 승인(2026-08-01)**:
- 기존 M49/M50 규칙과의 관계: **보완**(두 규칙 병존 — 기존 규칙 삭제
  없음, 회귀 없음).
- 추세 계산 방식: **최근 N건 슬라이딩 윈도우**(exponential decay
  대신 — 구현·검증이 단순함).
- 윈도우 크기: **N=5**(더 보수적, 오탐 감소).

### T02 — MDD Review(완료)

- **Scope**: `ExperienceStat`에 필드 1개 추가 + `RecommendationAdjustmentAnalyzer`
  에 조건 1개 추가(OR 병존). 기존 필드/기존 규칙은 무변경.
- **Reuse**: `ExperienceRecord.timestamp` 기반 정렬(이미 `_summarize()`
  가 수행)을 그대로 재사용. 새 Domain/Service/Interface 없음.
- **Interface**: 신규 Interface 없음.
- **Service**: 신규 Service 없음. `ExperienceIntelligenceService`/
  `RecommendationAdjustmentAnalyzer` 시그니처 불변.
- **Adapter**: 신규 Adapter 없음.
- **Layer**: `intelligence/`(Analyzer 순수성 유지) 내부에서만 변경 —
  Layer 이동 없음.
- **File**: `intelligence/experience_rules.py`(`ExperienceStat`에
  `recent_failure_streak: int` 필드 추가, `_summarize()`에서 계산),
  `intelligence/recommendation_adjustment.py`(`_RECENT_FAILURE_
  STREAK_THRESHOLD: Final[int] = 5` 상수 추가, 기존 조건에 OR로
  새 조건 추가).

*설계 상세*:
- `recent_failure_streak`: 시간순 정렬된 기록의 **끝에서부터** 연속
  실패 개수(가장 최근 기록이 성공이면 0). 특정 윈도우 크기에
  종속되지 않는 범용 "연속 실패 추세" 신호로 설계 — `stat.
  recent_failure_streak >= 5`는 정확히 "최근 5건이 모두 실패"와
  동치(총 기록이 5건 미만이면 자연히 5 미만이 되어 조건 불충족).
- 보류 조건(최종): `(success_count == 0 and total >= 3) or
  recent_failure_streak >= 5` — 첫 항은 M49/M50 규칙 그대로, 둘째
  항이 M51 신규. 전체 이력에 성공이 섞여 있어도 최근 추세가
  나빠지면 보류하는 케이스를 새로 포착한다(기존 규칙은 포착 못 함).
- `reason` 텍스트를 트리거된 조건에 따라 분기(기존 규칙 텍스트 유지,
  신규 규칙은 별도 텍스트로 "최근 N회 연속 실패" 명시) — Explainability
  (M44)가 그대로 소비 가능.

*기각한 대안*:
1. 지수 Decay(exponential weighting) — 기각: 사용자가 슬라이딩
   윈도우를 선택(구현·설명이 더 단순).
2. 기존 규칙을 가중치 점수로 완전히 대체 — 기각: 사용자가 "보완(두
   규칙 병존)"을 선택, 회귀 위험 회피.
3. `recent_results: tuple[str, ...]`(최근 N건 결과 자체를 저장) —
   기각: `recent_failure_streak: int` 하나로 이번 Rule을 표현하는 데
   충분하고, 원시 리스트를 노출하면 향후 다른 소비처가 윈도우 크기를
   하드코딩하게 만들 위험이 있음(YAGNI).

**사용자 승인(2026-08-01)**: 위 T02 설계로 T03 구현 진행 승인됨. 단,
구현 전 아래 2가지를 문서/코드에 명시하도록 사용자가 추가 요청:
1. `recent_failure_streak`의 정확한 정의(가장 최근 기록부터 거슬러
   올라가며 연속 실패를 센다) 명문화.
2. Explainability에서 어느 규칙(M49/M51/Both)이 보류를 발생시켰는지
   구분해 기록.

### T03 — Implementation(완료)

*수정 파일*:
- `src/ai_workspace/intelligence/experience_rules.py` —
  `ExperienceStat`에 `recent_failure_streak: int = 0` 필드 추가(정확한
  정의를 클래스 docstring에 명문화), `_count_recent_failure_streak()`
  헬퍼로 `_summarize()`에서 계산.
- `src/ai_workspace/intelligence/recommendation_adjustment.py` —
  `_RECENT_FAILURE_STREAK_THRESHOLD: Final[int] = 5` 추가, `analyze()`
  가 M49/M51 두 조건을 모두 평가해 OR로 판정. `_build_withhold_reason()`
  헬퍼가 어느 규칙이 발동했는지에 따라 reason 텍스트에 "(M49 규칙)"/
  "(M51 규칙, 과거 성공 이력 있음)"/"(M49+M51 규칙)"을 명시적으로
  태깅 — Explainability(M44)가 그대로 소비하는 기존 prose 채널을
  재사용해 사용자가 요청한 "규칙 구분 기록"을 만족(새 필드/시그니처
  변경 없음).
- `tests/intelligence/test_experience_rules.py`(신규 3건 —
  `recent_failure_streak` 계산 검증).
- `tests/intelligence/test_recommendation_adjustment.py`(신규 4건 —
  M51 단독 발동/미달/M49+M51 동시 발동/M49 단독 발동 시 reason 태그
  분기 검증).
- `.ai/DECISIONS.md`(ADR-0068), `docs/ARCHITECTURE.md`(§2.1).

| # | 완료 조건 | 상태 |
|---|---|---|
| 1 | 새 Domain/Service/Interface 없이 기존 파일 2개만 수정 | ✅ |
| 2 | M49/M50 규칙 무변경(보완, 대체 아님) — 기존 테스트 전부 통과 | ✅ |
| 3 | 추세 계산 = 최근 N건 슬라이딩 윈도우(N=5, 사용자 승인) | ✅ |
| 4 | `recent_failure_streak` 정의 명문화(사용자 추가 요청) | ✅ |
| 5 | Explainability reason에 M49/M51/Both 구분 태깅(사용자 추가 요청) | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1137개(신규 7개, 회귀 없음)/`ruff`/`mypy`(221 source files)
전부 통과.

**사용자 승인(2026-08-01)**: 위 6개 항목 확인 완료 — Milestone 51
Learning Evolution 공식 완료 승인됨. PR #47(코드) 병합(`384214c`),
PR #48(Vault Index 반영) 병합(`1db0b7a`), `main` 반영 확인.

---

## Milestone 52 — Learning Weighting (완료)

**배경**: M51 승인 코멘트에서 사용자가 예고한 "이후 M52(가중치),
M53(Decay)로도 확장하기 쉬운 구조" 중 M52를 착수. 착수 전 사용자가
"Multi-Agent Foundation"으로 잘못 요약된 이전 세션 요약 오류를
스스로 발견해 정정하고, M52는 실제로 "가중치" 확장임을 재확인.

**T01 Domain Analysis(사용자 확인)**: 두 신호(M49 전체 실패율, M51
최근 연속 실패)를 가중치 점수로 결합하는 확장으로 확정 — 가중치는
데이터로부터 학습되는 것이 아니라 코드에 고정된 상수(사실상
"학습" 아님, Deterministic 유지). 새 Domain/Behavioral Concept
아님, 기존 `Adaptation`(§13.3)의 연장.

**T02 MDD Review(사용자 승인, 2단계)**:
1. 최초 설계안(신호 2개를 0.5/0.5로 가중, threshold 0.5, 기존 규칙
   회귀 없음을 수학적으로 보장)을 제시 — 사용자가 "가중치는
   0.5/0.5 유지, threshold는 0.6으로" 요청.
2. 이 조합이 기존 M49/M51 **단일** 규칙(신호 하나가 완전히 1.0)의
   트리거를 깨는 실제 회귀(`score=0.5<0.6`)를 만든다는 것을 수학적
   경계값 계산으로 지적·보고 — 사용자가 "가중치를 0.6/0.6으로
   올려 threshold=0.6 유지"로 재확정(신호 하나가 1.0이면 그 신호만
   으로 `score=0.6>=0.6`이 성립해 기존 두 Rule이 정확히 보존됨).

**T03 구현**:
- `src/ai_workspace/intelligence/recommendation_adjustment.py` —
  `_OVERALL_FAILURE_WEIGHT`/`_RECENT_STREAK_WEIGHT`/
  `_WITHHOLD_SCORE_THRESHOLD`(모두 `Final[float] = 0.6`) 추가.
  `_withhold_score()` 신규 헬퍼(`signal_overall = failure_count /
  total`(단, `total < 3`이면 0)와 `signal_recent = min
  (recent_failure_streak / 5, 1.0)`를 각각 0.6 가중치로 합산).
  `analyze()`를 boolean OR 판정에서 `score >=
  _WITHHOLD_SCORE_THRESHOLD` 판정으로 교체. `_build_withhold_reason()`
  에 개별 규칙(M49/M51 boolean)으로는 안 걸리고 가중치 결합으로만
  걸린 새 케이스를 위한 "(M52 가중치 결합 규칙)" 분기 추가 — 기존
  M49/M51/M49+M51 태깅은 그대로 유지(사용자 M51 승인 시 요구사항
  보존). 클래스/모듈 docstring의 Non-goal을 "가중치·threshold는
  고정 상수이며 데이터로부터 학습되지 않는다"로 좁힘.
- `tests/intelligence/test_recommendation_adjustment.py` —
  기존 `test_analyze_passes_through_when_recent_failure_streak_
  below_threshold`가 새 가중치 결합 로직 하에서는 실제로 트리거되는
  케이스였음을 발견해 값 조정(총 8건/실패 1건/연속 1회로 진짜
  낮은 결합 점수를 테스트하도록 수정) 후 이름도 `..._combined_
  score_below_threshold`로 변경. 신규 2건 추가: 개별 규칙은 둘 다
  미달이지만 결합 점수는 threshold 이상인 케이스(M52 태그 검증),
  신호 하나가 완전히 1.0이고 다른 신호가 0이어도 여전히 보류되는
  경계값(회귀 없음 증명).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 새 Domain/Service/Interface 없이 기존 파일 1개만 수정 | ✅ |
| 2 | M49/M51 단일 규칙 무변경(회귀 없음) — 경계값 테스트로 증명 | ✅ |
| 3 | 가중치는 고정 상수, 데이터 기반 학습 아님(사용자 확인) | ✅ |
| 4 | 가중치/threshold 값 사용자 직접 확정(0.6/0.6, 회귀 이슈 보고 후 재확정) | ✅ |
| 5 | Explainability에 M52 전용 태그 추가, 기존 M49/M51/Both 태깅 보존 | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음(값 조정 1건 제외) | ✅ |

`pytest` 1145개(신규 2개, 수정 1개, 회귀 없음)/`ruff`/`mypy`(221
source files) 전부 통과. ADR-0070.

**사용자 승인(2026-08-01)**: 위 6개 항목을 확인해 **Milestone 52
Learning Weighting 공식 완료(Approved)**. PR #53(코드) 병합
(`4af8498`), PR #54(Vault Index 반영) 병합(`e9895e9`), `main` 반영
확인.

---

## Milestone 53 — Learning Decay (완료)

**배경**: M51 승인 코멘트에서 사용자가 예고한 "M52(가중치), M53
(Decay)" 중 마지막 M53 착수.

**T01 Domain Analysis(사용자 확인)**: M52의 `signal_overall`
(`failure_count/total`, 모든 기록을 동등 반영)을 지수 Decay 가중
실패율로 교체하는 확장으로 확정 — 새 Domain/Behavioral Concept
아님, 기존 `Adaptation`의 신호 계산 정교화.

**T02 MDD Review(사용자 승인)**: `ExperienceStat`에
`decayed_failure_rate: float` 필드 신설(M51 `recent_failure_streak`
패턴 재사용), `experience_rules.py`에서 계산(`weight(rank) =
decay_factor**rank`, `rank=0`이 최신). Decay 함수는 지수(사용자
선택), `decay_factor=0.8`(사용자 선택 — 10번째 이전 기록도
0.8^9≈0.13 가중치로 약간 반영되는 중간 강도). `recommendation_
adjustment.py`의 `signal_overall`을 이 필드로 교체(M52의 가중치
0.6/0.6·threshold 0.6은 그대로 유지). 전체 이력 100% 실패 시
`decayed_failure_rate`가 가중치와 무관하게 항상 정확히 1.0임을
근거로 M49 단일 규칙 보존을 재확인.

**T03 구현**:
- `src/ai_workspace/intelligence/experience_rules.py` —
  `_DECAY_FACTOR: Final[float] = 0.8` 추가, `_compute_decayed_
  failure_rate()` 헬퍼 신규, `ExperienceStat.decayed_failure_rate`
  필드 추가.
- `src/ai_workspace/intelligence/recommendation_adjustment.py` —
  `_withhold_score()`의 `signal_overall`을 `stat.failure_count /
  stat.total`에서 `stat.decayed_failure_rate`로 교체. `reason`
  텍스트에 `(Decay 반영 {rate:.2f})` 추가로 투명성 확보. Non-goal
  문구에 Decay 계수도 고정 상수임을 명시.
- **구현 중 발견한 테스트 인프라 함의**: `ExperienceStat`을 수동
  생성하는 기존 테스트 5건이 새 필드 기본값(`0.0`)을 그대로 둔 채
  "전체 실패" 시나리오를 표현하고 있어, M49 트리거가 깨지는 것을
  테스트 실행으로 발견 — 각 테스트에 `decayed_failure_rate` 명시
  지정으로 수정(`test_recommendation_adjustment.py` 4건,
  `test_recommendation_service.py` 1건).
- `tests/intelligence/test_experience_rules.py`(신규 4건 — 전체
  실패 시 정확히 1.0, 전체 성공 시 0.0, 최근 실패가 오래된 실패보다
  더 높게 반영됨(수치 검증 포함), 입력 순서 무관).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 새 Domain/Service/Interface 없이 기존 파일 2개만 수정 | ✅ |
| 2 | M49 단일 규칙 무변경(전체 실패 시 decayed_failure_rate=1.0 보장) | ✅ |
| 3 | Decay 계수는 고정 상수, 데이터 기반 학습 아님(사용자 확인) | ✅ |
| 4 | Decay 함수/계수 값 사용자 직접 확정(지수, 0.8) | ✅ |
| 5 | 최근 기록이 오래된 기록보다 더 큰 비중을 갖는 것을 수치로 검증 | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음(값 명시 5건 제외) | ✅ |

`pytest` 1149개(신규 4개, 회귀 없음)/`ruff`/`mypy`(221 source files)
전부 통과. ADR-0071.

**사용자 승인(2026-08-01)**: 위 6개 항목을 확인해 **Milestone 53
Learning Decay 공식 완료(Approved)**. PR #56(코드) 병합(`c4c37bd`),
PR #57(Vault Index 반영) 병합(`7639b14`), `main` 반영 확인.

---

## Milestone 54 — Learning Insight (완료)

**배경**: 로드맵에 사전 예고 없던 이름이라 착수 전 범위부터 확인.

**T01 Domain Analysis(사용자 확인)**: M49~M53 학습 신호를 사람이
볼 수 있게 노출하는 확장으로 확정(새 Domain/Behavioral Concept
아님, 기존 `Observability`의 확장). 조사 중 `WorkspaceInfo.
current_task`가 이미 "Phase 1 범위 밖, 항상 `None`"으로 명시돼
있음을 재확인 — StatusLine은 별도 프로세스라 "지금 어떤 task가
추천 대상인지"는 알 수 없다(ADR-0063 기존 한계, 이번에도 해소하지
않음). "현재 추천 대상"이 아니라 "추적 중인 모든 task 중 가장
위험한 것"으로 범위를 좁힘.

**T02 MDD Review(사용자 승인)**: 새 `LearningRuntimeAnalyzer`가
`FileMemoryEngine`(M50)+`ExecutionMemoryStore`(M39)+
`ExperienceIntelligenceService`(M40)를 그대로 조합(새 Domain/
Interface/Service 없음). `LearningRuntimeInfo`: `tracked_task_count`,
`highest_risk_*`(decayed_failure_rate 최댓값, 동점이면 task_id
오름차순 — 새 채점 아니라 표시 로직). Pipeline Stage의 Memory
단계를 `NOT_OBSERVABLE`에서 `OBSERVED_DONE`/`OBSERVED_NOT_YET`으로
승격하는 것도 T02에서 함께 승인(M45/M50에서 두 번 미뤄뒀던 gap).

**T03 구현**:
- `src/ai_workspace/observability/snapshot.py` — `LearningRuntimeInfo`
  값 객체 추가, `WorkspaceRuntimeSnapshot`에 필드 추가.
- `src/ai_workspace/observability/learning_runtime_analyzer.py`
  (신규) — `LearningRuntimeAnalyzer.analyze(project_root)`.
- `src/ai_workspace/observability/pipeline_stage_analyzer.py` —
  `analyze()`에 `has_learning_records: bool` 키워드 인자 추가,
  Memory 단계 판정을 `_memory_stage()` 헬퍼로 교체.
- `src/ai_workspace/observability/runtime_snapshot_service.py` —
  8번째 Analyzer로 배선.
- `src/ai_workspace/observability/statusline_renderer.py` —
  "Learning" 줄 렌더링 추가.
- `tests/observability/test_learning_runtime_analyzer.py`(신규
  3건 — 기록 없음/실제 FileMemoryEngine 데이터 반영/동점 시
  task_id 오름차순). 기존 `test_pipeline_stage_analyzer.py`(Memory
  판정 테스트 2건으로 분리)/`test_statusline_renderer.py`/
  `test_runtime_snapshot_service.py`를 새 필드/파라미터에 맞춰 수정.
- 실제 `FileMemoryEngine` 데이터로 end-to-end 수동 실행 — Memory
  단계가 `?`에서 `✓`로 바뀌고 Learning 줄이 실제 위험 task를
  정확히 보여줌을 확인.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 새 Domain/Service/Interface 없이 기존 컴포넌트만 조합 | ✅ |
| 2 | `current_task` Phase 1 한계 유지(추정 금지 원칙) | ✅ |
| 3 | Memory Pipeline Stage NOT_OBSERVABLE → OBSERVED_DONE/NOT_YET 승격 | ✅ |
| 4 | 실제 FileMemoryEngine 데이터로 end-to-end 수동 검증 | ✅ |
| 5 | 새 채점 로직 없이 기존 값(decayed_failure_rate) 표시만 | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1155개(신규 3개, 회귀 없음)/`ruff`/`mypy`(222 source files)
전부 통과. ADR-0072.

**사용자 승인(2026-08-01)**: 위 6개 항목을 확인해 **Milestone 54
Learning Insight 공식 완료(Approved)**. PR #59(코드) 병합
(`f4315b0`), PR #60(Vault Index 반영) 병합(`12c4e1a`), `main` 반영
확인.

---

## Milestone 55 — Learning Explainability 고도화 (완료)

**배경**: 로드맵에 사전 예고 없던 이름이라 착수 전 범위부터 확인.

**T01 Domain Analysis(사용자 확인)**: `experience_summary`를 학습
신호 전체로 확장하는 것으로 확정(새 Domain/Behavioral Concept
아님, 기존 `Explainability`의 확장). M49~M53 학습 신호가 Adaptation
이 실제로 보류를 발동했을 때만 보이고, 아직 보류되지 않은 near-miss
케이스는 전혀 드러나지 않는 한계를 확인.

**T02 MDD Review(사용자 승인)**: `recommendation_adjustment.py`의
private `_withhold_score()`를 공개 함수 `compute_learning_score
(stat)`로 승격(`WITHHOLD_SCORE_THRESHOLD` 상수도 공개) — 가중치·
threshold 공식을 두 곳에 중복 구현하지 않기 위함. `_build_
experience_summary()`가 보류 여부와 무관하게 항상
`decayed_failure_rate`/`recent_failure_streak`/학습 Score를 성공률과
함께 노출.

**T03 구현**:
- `src/ai_workspace/intelligence/recommendation_adjustment.py` —
  `_withhold_score()` → `compute_learning_score()` 공개 승격,
  `WITHHOLD_SCORE_THRESHOLD` 공개.
- `src/ai_workspace/intelligence/recommendation_explanation.py` —
  `_build_experience_summary()`를 `"성공률 X%(N건 중 M건 성공) ·
  Decay실패율 R · 연속실패 S · 학습 Score V/T"` 형식으로 확장.
  `compute_learning_score()` 재사용.
- Vault 발행(`recommendation_explanation_service.py`)은 문자열을
  그대로 한 줄에 임베드할 뿐이라 별도 수정 불필요(포맷 가정 없음,
  확인만 함).
- `tests/intelligence/test_recommendation_explanation.py` — 기존
  1건을 새 형식 값으로 갱신, 신규 1건 추가(near-miss 가시성 —
  `adaptation_applied=False`인 상태에서도 학습 Score가 노출되는지
  검증).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 새 Domain/Service/Interface 없이 기존 파일 2개만 수정 | ✅ |
| 2 | 새 계산 로직 없이 기존 값(compute_learning_score) 재사용만 | ✅ |
| 3 | 보류 여부와 무관하게 학습 신호 상시 노출(near-miss 가시성) | ✅ |
| 4 | 가중치·threshold 공식 중복 없음(공개 함수 재사용으로 확인) | ✅ |
| 5 | Vault 발행 포맷에 영향 없음(문자열 임베드 방식 확인) | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음(값 갱신 1건 제외) | ✅ |

`pytest` 1156개(신규 1개, 회귀 없음)/`ruff`/`mypy`(222 source files)
전부 통과. ADR-0073.

**사용자 승인(2026-08-01)**: 위 6개 항목을 확인해 **Milestone 55
Learning Explainability 고도화 공식 완료(Approved)**. PR #62(코드)
병합(`e32e2e0`), PR #63(Vault Index 반영) 병합(`7980d4c`), `main`
반영 확인.

---

## Milestone 56 — Multi-Agent 자가 확인 가드 일반화 (완료)

**배경**: 로드맵에 사전 예고 없던 이름이라 착수 전 범위부터 확인.
"Multi-Agent"는 이 프로젝트에서 반복적으로 Non-goal로 미뤄온 넓은
영역이라, M13이 남긴 구체적 후속 과제(병렬 실행/Scheduler 정책
고도화/다른 Agent로 확장) 중 무엇을 다룰지부터 확정.

**T01 Domain Analysis(사용자 확인)**: M13의 자가 확인 가드
(`is_agent_selected()`)를 `CodingAgent` 외 다른 Agent로 확장하는
것으로 확정. 조사 중 `PlanningAgent`가 Event를 구독하지 않고
`plan_mission()`으로 직접 호출되는 진입점이라, "여러 인스턴스가
같은 broadcast Event에 반응할 때 자가 선택"이라는 이 가드의 전제가
성립하지 않음을 발견 — 사용자가 PlanningAgent 제외(구조적 이유
문서화)를 확정.

**T02 MDD Review(사용자 승인)**: `CodingAgent`의 정확히 같은 패턴
(선택적 키워드 인자 `agent_registry`/`agent_scheduler`, 기본값
`None`이면 기존 동작과 100% 동일)을 `ReviewAgent`/
`DocumentationAgent`/`ShellAgent`/`CoordinatorAgent` 4개에 적용.
사용자가 "현재 구현된 모든 Agent까지 일반화, 미래 Agent는 동일
계약을 따르도록 설계"로 범위를 확정 — 새 Base Class/Mixin 없이
5개 사례 모두 같은 패턴을 반복하는 것으로 충분(YAGNI).

**T03 구현**:
- `src/ai_workspace/agents/review_agent.py`/`documentation_agent.py`/
  `shell_agent.py`/`coordinator_agent.py` — 각각 선택적
  `agent_registry: AgentRegistry | None = None`/`agent_scheduler:
  AgentScheduler | None = None` 키워드 인자 추가, 이벤트 핸들러
  진입 시점에 `is_agent_selected()`로 자가 확인(둘 다 주어졌을
  때만 확인, 기본값이면 건너뜀).
- `tests/agents/test_review_agent.py`/`test_documentation_agent.py`/
  `test_shell_agent.py`/`test_coordinator_agent.py` — 각각 M13과
  동일한 "선택되지 않은 인스턴스는 아무것도 하지 않는다" 테스트
  신규 추가.
- 확인: `web/server.py`(프로덕션 Composition Root)에는 M13
  (CodingAgent)도 아직 배선되지 않음 — 이번에도 배선하지 않아
  MVP 범위 일관성 유지(`grep`으로 5개 Agent 모두 `src/` 프로덕션
  코드에서 생성되지 않고 테스트에서만 생성됨을 확인).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 새 Domain/Interface 없이 M13의 기존 `is_agent_selected()` 재사용 | ✅ |
| 2 | 4개 Agent 모두 미주입 시(기본값) 기존 동작과 100% 동일(회귀 없음) | ✅ |
| 3 | PlanningAgent는 구조적 이유로 제외, 문서화 | ✅ |
| 4 | 새 중앙 디스패처/새 Base Class 없음(YAGNI) | ✅ |
| 5 | 각 Agent에 M13과 동일한 "미선택 인스턴스는 무동작" 테스트 | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1160개(신규 4개, 회귀 없음)/`ruff`/`mypy`(222 source files)
전부 통과. ADR-0074.

**사용자 승인(2026-08-01)**: 위 6개 항목을 확인해 **Milestone 56
Multi-Agent 자가 확인 가드 일반화 공식 완료(Approved)**. PR #65
(코드) 병합(`3c8637b`), PR #66(Vault Index 반영) 병합(`ebd4d34`),
`main` 반영 확인.

---

## Milestone 57 — Scheduler 고도화 (완료)

**배경**: 사용자가 "우선순위·Capability·의존성 기반 Agent 선택 및
실행 정책 설계"로 명시적 범위를 제시하며 착수 요청.

**T01 Domain Analysis(사용자 확인, 3회)**: Capability 축은 기존
필터로 충분해 범위 밖 확정. "의존성"은 Task 도메인에 선행 Task
개념이 없어 "Agent 가용성"으로 재정의. 우선순위는 Agent에 명시적
`priority` 필드 신설로 확정.

**T02 MDD Review — 두 차례 실제 버그 발견·재설계(사용자 확인)**:
1. 1차 설계(가용성=IDLE)를 승인받았으나, 구현 전 코드 조사로
   `AgentRuntime.start_agent()`가 등록 즉시 Agent를 RUNNING으로
   전이시키고 이벤트 처리 중 상태를 바꾸지 않는다는 것을 발견 —
   IDLE만 가용으로 보면 모든 정상 Agent가 걸러지는 회귀가 됨을
   보고, 사용자가 "RUNNING을 가용으로" 재확정.
2. RUNNING 기준으로 구현 후 전체 `pytest` 실행 결과 9건 실패 —
   `AgentRuntime`을 거치지 않고 도메인 기본값(IDLE)으로 `Agent`를
   직접 생성하는 별도 테스트 계열이 이미 존재함을 발견. 사용자가
   "STOPPED/ERROR만 제외(나머지 다 가용)"로 최종 재확정 — 두 Agent
   생성 경로 모두 회귀 없이 통과.

**T03 구현**:
- `src/ai_workspace/domain/agent.py` — `Agent.priority: int = 0`
  필드 추가(낮을수록 우선).
- `src/ai_workspace/runtime/agent/agent_scheduler.py` —
  `InMemoryAgentScheduler.select()`에 가용성 필터(STOPPED/ERROR만
  제외) + `priority` 안정 정렬 추가.
- `src/ai_workspace/interfaces/agent_scheduler.py` — 계약 docstring
  을 새 가용성·우선순위 규칙으로 갱신.
- `tests/runtime/agent/test_agent_scheduler.py` — 신규 8건(priority
  우선순위, 안정 정렬로 동점 시 원래 순서 보존, STOPPED/ERROR 제외
  2건 파라미터화, IDLE/RUNNING/WAITING/PAUSED 포함 4건 파라미터화).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 새 Domain/Interface 없이 기존 `AgentScheduler`/`Agent` 확장 | ✅ |
| 2 | Capability 축은 범위 밖(기존 필터 유지, 사용자 확인) | ✅ |
| 3 | 가용성 정의를 실제 코드 조사로 두 차례 검증·재확정(추측 없음) | ✅ |
| 4 | priority 안정 정렬로 M13/M56 "첫 매치" 동작 100% 보존(회귀 없음) | ✅ |
| 5 | 두 Agent 생성 경로(IDLE 기본값/RUNNING 실행) 모두 회귀 없음 | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과 | ✅ |

`pytest` 1168개(신규 8개, 회귀 없음)/`ruff`/`mypy`(222 source files)
전부 통과. ADR-0075.

**사용자 승인(2026-08-01)**: 위 6개 항목을 확인해 **Milestone 57
Scheduler 고도화 공식 완료(Approved)**. PR #68(코드) 병합
(`8e79c12`), PR #69(Vault Index 반영) 병합(`fc8c7e3`), `main` 반영
확인.

---

## Milestone 58 — Agent 병렬 실행 (완료)

**배경**: M13 Review(T2-08 이후)가 "M13 범위 밖으로 명시적으로 제외한
것" 3항목으로 남긴 병렬 실행 / Scheduler 정책 고도화(M57 해소) /
다른 Agent로의 확장(M56 해소) 중 마지막으로 남은 항목. 사용자가
"이어서 구현"으로 착수 요청.

**T01 Domain Analysis(코드 조사로 확정)**: `AgentScheduler.select()`
의 `max_count`는 T2-02(Milestone 1)부터 존재했고 ARCHITECTURE.md
§3.4가 "동시에 활동할 Agent 후보를 최대 max_count개 선택"이라고 이미
문서화해 뒀지만, 유일한 호출부인 `agents/scheduling.py`의
`is_agent_selected()`가 내부적으로 `max_count=1`을 고정 전달해 실제
협업 흐름에서 한 번도 1을 넘겨 쓰인 적이 없음을 `grep`으로 확인.
새 스레드/프로세스 실행 메커니즘(§3.9 `EngineRuntime.run_parallel()`
책임)은 범위 밖으로 확정 — M58은 순수하게 이미 있는 `max_count` 축을
실제로 연결하는 배선 작업으로 한정.

**T02 설계**: `is_agent_selected()`에 `max_parallel: int = 1` 매개변수
추가 → `agent_scheduler.select(candidates, capability, max_parallel)`
로 전달, 판정을 `selected.agent_id == agent_id`(단일 비교)에서
`any(agent.agent_id == agent_id for agent in selected)`(집합 소속
여부)로 일반화. 기본값 1이면 M13/M56/M57과 100% 동일. 5개 Agent
(`CodingAgent`/`ReviewAgent`/`DocumentationAgent`/`ShellAgent`/
`CoordinatorAgent`) 전부에 M56과 동일한 반복 패턴으로 선택적 생성자
인자 `max_parallel_agents: int = 1` 추가(새 중앙 디스패처·Base Class
없음, YAGNI).

**T03 구현**:
- `src/ai_workspace/agents/scheduling.py` — `is_agent_selected()`에
  `max_parallel` 매개변수 추가, 판정 로직을 집합 소속 여부로 일반화.
- `src/ai_workspace/agents/coding_agent.py`/`review_agent.py`/
  `documentation_agent.py`/`shell_agent.py`/`coordinator_agent.py` —
  각각 `max_parallel_agents: int = 1` 생성자 인자 추가, `is_agent_
  selected()` 호출부에 전달.
- `tests/agents/test_scheduling.py` — 신규 3건(기본값 1 하위 호환,
  max_parallel=2로 상위 2개 모두 선택, 초과분 제외).
- `tests/agents/test_coding_agent.py`/`test_review_agent.py`/
  `test_documentation_agent.py`/`test_shell_agent.py`/
  `test_coordinator_agent.py` — 각 1건(두 인스턴스에 `max_parallel_
  agents=2`를 주면 같은 Event를 병렬로 처리함을 증명).
- `docs/ARCHITECTURE.md` §2(변경 이력)/§3.4(Agent Scheduler 절)
  갱신.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 새 Domain/Interface 없이 기존 `AgentScheduler`/`is_agent_selected()` 확장 | ✅ |
| 2 | 실제 스레드/프로세스 병렬성은 범위 밖(`run_parallel()`과 명확히 구분) | ✅ |
| 3 | `max_parallel_agents` 미지정 시(기본값 1) 5개 Agent 전부 기존 동작과 100% 동일 | ✅ |
| 4 | 2 이상 지정 시 우선순위 상위 N개 인스턴스가 실제로 같은 Event를 처리함을 테스트로 증명 | ✅ |
| 5 | 새 중앙 디스패처/Base Class 없음(M56 패턴 재사용, YAGNI) | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1176개(신규 8개, 회귀 없음)/`ruff`/`mypy`(222 source files)
전부 통과. ADR-0076.

---

## Milestone 59 — Automation: RUN_WORKFLOW 지원 (완료)

**배경**: 사용자가 "M59 Automation 진행"으로 착수 요청. 코드 조사 결과
M48(Automation Foundation)이 남긴 유일한 미해결 Gap은 "RUN_WORKFLOW
미지원"(M21부터 계속 이월 — `AutomationActionExecutor`가 `Action
Kind.RUN_WORKFLOW`에 대해 `AutomationActionNotSupportedError`만
던지는 상태). 이를 실제로 구현하려면 이 저장소에 아직 없던 새
컴포넌트(`workflow_id`로 `Workflow`를 조회할 Repository)가 필요함을
사용자에게 확인(AskUserQuestion)받고 "RUN_WORKFLOW 구현"으로 범위
확정.

**T01 Domain Analysis**: `WorkflowRunner`(Milestone 12)가 이미
`Workflow` 인스턴스를 받아 `WorkflowEngine.plan()` 순서대로 Task를
순차 실행하는 조율자로 존재하지만, `workflow_id`만 갖고 실제
`Workflow`를 영속 조회하는 통로가 이 저장소 어디에도 없음을
`grep`으로 확인(추측 아님). `AgentRepository`/`AutomationRepository`
와 동일한 `get`/`save`/`list_*` 스타일로 새 Core Domain Interface
`WorkflowRepository`를 신설하는 것이 최소 범위로 확정(사용자 승인).

**T02 설계**: `AutomationActionExecutor`에 `workflow_repository`/
`workflow_runner` 선택적 생성자 인자를 추가(M38 `recommendation_
orchestration_service`와 동일한 패턴). 둘 다 주입되면 `RUN_WORKFLOW`
Action에서 `workflow_repository.get(action.workflow_id)`로 실제
Workflow를 조회해 `workflow_runner.run(workflow)`에 위임한다. 둘 중
하나라도 없으면(기본값 `None`) 여전히
`AutomationActionNotSupportedError`로 M21 이후 동작과 100% 동일.
프로덕션 Composition Root(`web/server.py`의 `build_app()`)에는
`TaskEngine`/`WorkflowEngine`조차 아직 배선돼 있지 않아, 이번에도
배선하지 않음(M56/M57/M58과 동일한 "MVP 범위 유지" 판단 — 배선하려면
`TaskEngine`을 프로덕션에 처음 들이는 훨씬 큰 범위가 되어 YAGNI
위반).

**T03 구현**:
- `src/ai_workspace/interfaces/workflow_repository.py` — 신규
  `WorkflowRepository` Interface(`get`/`save`/`list_workflows`),
  `WorkflowNotFoundError`.
- `src/ai_workspace/runtime/workflow/workflow_repository.py` — 신규
  `InMemoryWorkflowRepository`(`InMemoryAutomationRepository`와
  동일한 최소 구현 패턴).
- `src/ai_workspace/runtime/automation/automation_action_executor.py`
  — `workflow_repository`/`workflow_runner` 선택적 생성자 인자 추가,
  `_run_workflow()` 신규 메서드로 RUN_WORKFLOW 실제 실행.
- `src/ai_workspace/domain/automation.py` — `Action.workflow_id`
  docstring을 "Not Supported"에서 실제 동작 설명으로 갱신.
- `tests/interfaces/test_workflow_repository.py` — 신규 5건(save→get,
  upsert, 미존재 예외, list, 방어적 복사).
- `tests/runtime/automation/test_automation_action_executor.py` —
  미주입 시 하위 호환 테스트(이름 갱신) + 신규 1건(주입 시
  `WorkflowRunner`로 실제 실행되어 Task가 DONE까지 전이됨을 증명).
- `docs/ARCHITECTURE.md` §7 Interface 표에 `WorkflowRepository` 추가
  (27종→28종), §3.19 Automation 절 RUN_WORKFLOW 서술 갱신.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `WorkflowRepository` 신설 필요성을 사용자에게 사전 확인(추측 설계 아님) | ✅ |
| 2 | `AgentRepository`/`AutomationRepository`와 동일한 스타일로 일관성 유지 | ✅ |
| 3 | `workflow_repository`/`workflow_runner` 미주입 시 기존 동작과 100% 동일 | ✅ |
| 4 | 주입 시 실제 Workflow 조회→WorkflowRunner 실행까지 테스트로 증명 | ✅ |
| 5 | 프로덕션 배선은 YAGNI로 범위 제외(M56~M58 선례와 일관) | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1182개(신규 6개, 회귀 없음)/`ruff`/`mypy`(224 source files)
전부 통과. ADR-0077.

---

## Milestone 60 — Autonomous Workspace: Tick 루프 내구성 (완료)

**배경**: 사용자가 "M60 Autonomous Workspace(장시간 자율 운영)"으로
착수 요청. "장시간 자율 운영"이라는 주제가 넓어(세션 영속화/재시도/
Health 등 여러 해석 가능) 코드 조사로 구체적인 실제 버그를 먼저
발견해 AskUserQuestion으로 범위를 확정.

**T01 Domain Analysis**: `web/app.py`의 `_tick_loop()`이
`automation_scheduler.tick()`을 `automation_tick_seconds`(기본
30초)마다 호출하는 `while True` 백그라운드 asyncio Task임을 확인.
`AutomationScheduler.tick()` 내부에서 `TimeTriggerEvaluator`/
`IntervalTriggerEvaluator`가 `_parse_time_of_day()`/`_parse_iso()`로
`Trigger.time_of_day`/`AutomationRule.last_executed_at`을 파싱하는데,
값이 손상돼 있으면 `ValueError`를 던지고 이를 감싸는 코드가
`tick()` 어디에도 없어 예외가 그대로 `_tick_loop()` 밖으로 전파됨을
확인 — asyncio Task가 처리되지 않은 예외로 조용히 종료되면 **서버
프로세스는 계속 살아있지만 자동화 전체가 영구히 멈추고, 기존
`HealthMonitor`(M22)도 `automation_scheduler is not None`만 확인할
뿐 tick 루프가 실제로 도는지는 확인하지 않아 이 상태를 감지하지
못함**을 확인(추측 아님, 코드 경로 직접 추적). Rule 하나의 손상된
`time_of_day`/`last_executed_at`만으로 재현 가능.

**사용자 승인(AskUserQuestion)**: "Tick 루프 내구성 수정"으로 범위
확정(HealthMonitor 연동 확장이나 다른 자율 운영 이슈 조사는 범위
밖).

**T02 설계**: `_fire()`가 이미 지키는 "한 Rule의 실패가 다른 Rule에
영향 없음" 원칙(Action 실행 단계)을 Trigger 평가 단계까지 확장한다.
`tick()`의 Rule별 처리(evaluator 생성→`should_fire()`→`_fire()`→
`compute_next_execution_at()`→`save()`) 전체를 `try/except`로 감싸
한 Rule의 평가 실패가 나머지 Rule 평가나 `tick()` 자체를 죽이지
못하게 한다. **`_on_event()`는 대상에서 제외**(YAGNI) — `Event
TriggerEvaluator.should_fire()`는 파싱 없이 항상 `True`만 반환해
실제로 던질 수 없고(실증 불가능한 방어 코드는 추가하지 않음), 이미
`EventBus.publish()`의 구독자 예외 격리(T2-02, `interfaces/
event_bus.py` 계약)가 이 경로를 보호하고 있어 중복 보호가 된다.
`run_now()`도 대상 밖 — REST API의 `/run`이 직접 위임하는 1회성
호출이라 `AutomationRuleNotFoundError` 등을 그대로 전파해 호출자가
즉시 알 수 있는 것이 오히려 바람직하다(백그라운드 루프가 아님).

**T03 구현**:
- `src/ai_workspace/runtime/automation/automation_scheduler.py` —
  `tick()`의 Rule별 처리를 `try/except Exception: pass`로 감쌈(기존
  `_fire()`의 swallow 원칙과 동일 패턴), docstring에 근거 기록.
- `tests/runtime/automation/test_automation_scheduler.py` — 신규
  2건(손상된 Rule이 있어도 다른 Rule은 정상 발동/손상된 Rule을 만난
  뒤에도 다음 `tick()` 호출이 정상 동작함을 증명).
- `docs/ARCHITECTURE.md` §3.19(Automation 절)에 Trigger 평가 실패
  격리 서술 추가.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 실제 코드 경로 추적으로 버그를 실증(추측 아님) | ✅ |
| 2 | 넓은 "자율 운영" 주제를 사용자 확인으로 좁은 범위로 확정 | ✅ |
| 3 | 손상된 Rule 1개가 있어도 나머지 Rule 평가는 계속됨을 테스트로 증명 | ✅ |
| 4 | 손상된 Rule을 만난 뒤에도 Scheduler가 다음 tick에서 계속 동작함을 증명 | ✅ |
| 5 | 실증 불가능한 경로(`_on_event()`)에는 방어 코드 추가하지 않음(YAGNI) | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1184개(신규 2개, 회귀 없음)/`ruff`/`mypy`(224 source files)
전부 통과. ADR-0078.

---

## Milestone 61 — Distributed Multi-Agent: 최소 인터페이스 씨앗 (완료)

**배경**: 사용자가 "M61 Distributed Multi-Agent(원격 Agent)"로 착수
요청. 조사 결과 이 주제는 M11(§scope-out)/M16/M21(scope-out)/ADR-0074
에서 **반복적으로 Non-goal로 이월**되어온 영역임을 확인 — "Distributed/
Multi-node Scheduler"·"Multi-node Cluster"는 "실제 필요성이 생기기
전까지 이월한다"고 명시되어 있었다. `Agent` 도메인
(`agent_id/role/capabilities/status/priority`)에는 host/주소 개념이
전혀 없고, `AgentRegistry`는 스스로 "in-memory, 프로세스 재시작 시
소멸"이라 문서화하고 있어 단일 프로세스 전제가 코드 자체에 명시적임을
확인. 유일하게 "원격"을 언급하는 `ExecutionEnvironment`(M11,
ADR-0025)도 `EngineAdapter` 내부로만 범위를 한정해 Agent 레벨과는
무관함을 확인.

**사용자 승인(AskUserQuestion)**: "최소 인터페이스 씨앗" 범위로 확정
(선택지: 최소 인터페이스 씨앗 / 실동작 HTTP 기반 구현 / 다른 주제로
대체). 반복된 Non-goal 판단은 유지하되, 실제 네트워크/RPC 코드는 작성
하지 않고 향후 확장을 위한 최소 진입점만 추가한다.

**T02 설계**: `ExecutionEnvironment`(M11)가 `EngineAdapter` 내부에서
"명령을 어디서 실행할지"를 추상화하는 패턴을, Agent Runtime 레벨의
"Event를 어느 위치의 Agent에게 전달할지"에 그대로 적용한다.
- `Agent.location: str | None = None`(신규 필드) — 기본값 `None`은
  "같은 프로세스"(기존 동작과 100% 동일), 값이 있으면 원격이라고
  선언하는 불투명한 식별자.
- 신규 `RemoteAgentDispatcher` 계약(`interfaces/
  remote_agent_dispatcher.py`) — `dispatch(agent, event)`로 location이
  가리키는 목적지에 Event를 전달. location이 없는(로컬) Agent는 이
  계약과 무관 — 여전히 기존 `EventBus.publish()` 방송 + `is_agent_
  selected()`(M13) 경로로 처리.
- `LoopbackAgentDispatcher`(`runtime/agent/remote_agent_dispatcher.py`)
  — 실제 네트워크 없이 location별 `EventBus`를 연결해 여러 위치를
  같은 프로세스 안에서 흉내내는 최소 구현체(향후 HTTP 등 실제 구현체로
  교체해도 인터페이스 소비자는 변경 불필요).
- `AgentRuntime`: `start_agent(..., location=...)`로 Agent에 location
  기록, `dispatch_event(session_id, event)`로 원격 Agent에만 개입(로컬
  Agent는 no-op — 100% 하위 호환). `remote_agent_dispatcher`는 선택적
  생성자 주입(기본값 `None`).
- Production Composition Root(`web/server.py`)에는 연결하지 않음
  (M56~M60과 동일한 YAGNI 판단 — 실제 소비자가 생기기 전까지 인터페이스
  +구현체만 준비).

**T03 구현**:
- `src/ai_workspace/domain/agent.py` — `Agent.location` 필드 추가.
- `src/ai_workspace/interfaces/remote_agent_dispatcher.py`(신규) —
  `RemoteAgentDispatcher` ABC, `AgentUnreachableError`.
- `src/ai_workspace/runtime/agent/remote_agent_dispatcher.py`(신규) —
  `LoopbackAgentDispatcher`.
- `src/ai_workspace/runtime/agent/agent_runtime.py` — `remote_agent_
  dispatcher` 생성자 주입(선택적), `start_agent(location=...)`,
  `dispatch_event()` 신규 메서드.
- `tests/domain/test_agent.py` — location 기본값/설정 테스트 2건.
- `tests/runtime/agent/test_remote_agent_dispatcher.py`(신규) —
  `LoopbackAgentDispatcher` 5건.
- `tests/runtime/agent/test_agent_runtime.py` — location/dispatch_event
  관련 6건.
- `docs/ARCHITECTURE.md` §3.4에 Distributed Multi-Agent 서술 추가, §7
  Interface 표에 `RemoteAgentDispatcher` 추가(28→29종).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 반복된 Non-goal 이력을 코드/문서 근거로 확인(추측 아님) | ✅ |
| 2 | 넓은 "원격 Agent" 주제를 사용자 확인으로 좁은 범위로 확정 | ✅ |
| 3 | 실제 네트워크/RPC 코드 없이 최소 진입점(도메인 필드+인터페이스+ InMemory 구현)만 추가 | ✅ |
| 4 | `location`이 없는 기존 Agent는 100% 기존 동작과 동일(회귀 없음) | ✅ |
| 5 | Production Composition Root에 연결하지 않음(YAGNI, M56~M60과 동일 판단) | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1197개(신규 13개, 회귀 없음)/`ruff`/`mypy`(226 source files)
전부 통과. ADR-0079.

---

## Milestone 62 — Multi-LLM Orchestrator: run_ensemble() (완료)

**배경**: 사용자가 "M62 Multi-LLM Orchestrator(Claude, GPT, Gemini 등
혼합)"으로 착수 요청. 조사 결과 `LLMProvider` enum은 이미 OPENAI/
ANTHROPIC/GOOGLE/XAI 4종을 모델링하고 있고, `CLIEngineAdapter` +
`CodexProvider`/`GeminiCliProvider`로 Provider별 커맨드 조립 코드까지
존재했다(단, 이 세션 환경엔 실제 CLI 바이너리가 없어 검증 불가 —
`.ai/TASKS.md` M6 절 등에 반복 기록됨). 그러나 "Engine 선택"은
`EngineRuntime.run()`/`run_parallel()` 둘 다 "Task 1개당 Adapter
1개"만 고르는 라우팅이었다 — `run_parallel()`조차 여러 Task를 각자
하나의 Adapter로 돌릴 뿐, **하나의 Task를 여러 Provider에 동시에
보내 결과를 비교/합치는 메커니즘은 어디에도 없었다**(추측 아님, 코드
경로 직접 확인).

**사용자 승인(AskUserQuestion)**: "동일 Task를 여러 Provider에 병렬
실행"으로 범위 확정(Codex/Gemini CLI 실제 검증이나 다른 주제는 범위
밖).

**T02 설계**: `EngineRuntime`에 `run_ensemble(task, engine_names, *,
model=None) -> dict[str, EngineResult]`를 신설한다. `run()`처럼
`required_capabilities` 기반 "첫 매칭" 선택을 쓰지 않고
`register_engine()`에 쓰인 정확한 이름으로 여러 Adapter를 지정한다 —
여러 Provider를 의도적으로 섞어 돌리는 것이 목적이므로 capability
매칭 규칙은 맞지 않는다. `ManagedEngineRuntime`은 `run_parallel()`과
동일한 `ThreadPoolExecutor` 메커니즘을 재사용해 실제로 동시에
실행한다. `status(task_id)`(task_id당 상태 1개)와는 의미가 충돌해
(같은 task_id가 여러 엔진에서 동시에 도는데 상태 저장소는 1개뿐)
`run_ensemble()`은 이 추적에 관여하지 않는다 — 세션 생성→실행→정리만
독립 수행. 개별 엔진 실패(미등록 이름 포함)는 `run_parallel()`의
M10-T01/T02 원칙과 동일하게 그 이름의 `EngineResult(success=False)`로
격리한다. 결과 투표/합치기 로직은 추가하지 않는다(YAGNI) — 호출자가
비교한다. `RecoveringEngineRuntime`은 재시도 없이 내부 Runtime에
위임(실패한 개별 결과도 비교 대상이라 재시도로 덮으면 왜곡).

**T03 구현**:
- `src/ai_workspace/interfaces/engine_runtime.py` — `run_ensemble()`
  추상 메서드 추가.
- `src/ai_workspace/runtime/engine/engine_runtime.py`
  (`InMemoryEngineRuntime`) — 순차 구현.
- `src/ai_workspace/runtime/engine/managed_engine_runtime.py`
  (`ManagedEngineRuntime`) — `ThreadPoolExecutor` 기반 실제 병렬 구현.
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py`
  (`RecoveringEngineRuntime`) — 재시도 없이 내부 Runtime에 위임.
- `EngineRuntime`의 모든 테스트 더블(`tests/interfaces/fakes.py`
  `FakeEngineRuntime`, `tests/agents/test_coding_agent.py`
  `RecordingEngineRuntime`, `tests/core/test_workspace_core.py`
  `SpyEngineRuntime`, `tests/runtime/engine/
  test_recovering_engine_runtime.py` `ScriptedEngineRuntime`)에
  `run_ensemble()` 추가(신규 추상 메서드이므로 전부 구현 필요).
- 신규 테스트 10건: `InMemoryEngineRuntime` 3건, `ManagedEngineRuntime`
  6건(동시 실행 증명·개별 실패 격리·미등록 이름·빈 목록·`status()`
  비관여), `RecoveringEngineRuntime` 위임 1건.
- `docs/ARCHITECTURE.md` §3.9에 Multi-LLM Orchestrator 서술 추가(새
  Core Domain Interface 없음 — `EngineRuntime`에 메서드만 추가, 29종
  유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | "Task 1개-Adapter 1개" 라우팅과 "같은 Task-여러 Provider" 오케스트레이션의 실제 공백을 코드 경로로 확인 | ✅ |
| 2 | 넓은 "Multi-LLM Orchestrator" 주제를 사용자 확인으로 좁은 범위로 확정 | ✅ |
| 3 | `run_ensemble()`이 실제로 동시 실행됨을 시간 측정으로 증명 | ✅ |
| 4 | 개별 엔진 실패(미등록 이름 포함)가 다른 결과에 영향 없음을 증명 | ✅ |
| 5 | 투표/합치기 로직 등 실증되지 않은 확장은 추가하지 않음(YAGNI) | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1207개(신규 10개, 회귀 없음)/`ruff`/`mypy`(226 source files)
전부 통과. ADR-0080.

---

## Milestone 63 — Result Aggregation / Consensus: ResultAggregator (완료)

**배경**: 사용자가 "M63 Result Aggregation / Consensus"로 착수 요청.
ADR-0080(M62)이 "결과를 투표/합치는 로직은 추가하지 않는다(YAGNI) —
호출자가 반환된 이름별 결과를 직접 비교·선택한다"고 명시적으로
보류해 둔 부분을 지금 구현하는 요청이다.

**사용자 승인(AskUserQuestion)**: "단순 다수결(exact-match voting)
애그리게이터"로 범위 확정 — `EngineResult.output`의 정확한 문자열
일치만 비교하고, 의미(semantic) 비교나 LLM judge 기반 심사, 엔진별
가중치 투표는 범위 밖(`EngineResult.output`이 구조화되지 않은
문자열이라 정확한 의미 비교 자체가 별도 과제이고, 가중치 산정·조정
메커니즘도 아직 없음).

**설계**: 신규 Core Domain Interface `ResultAggregator`를 추가한다 —
`aggregate(results: dict[str, EngineResult]) -> AggregatedResult`
하나만 정의. `EngineRuntime`/`run_ensemble()`은 이 인터페이스의 존재를
알지 못한다 — `run_ensemble()`에 자동 연결하지 않고 호출자가 두 단계를
직접 이어 쓴다(M61 `RemoteAgentDispatcher`와 동일하게, 아직 실제 필요
시나리오가 없는 Composition Root 배선은 하지 않는다). 실패한
(`success=False`) 결과는 투표 대상에서 제외하고 `failed_engines`로만
별도 보고한다 — `run_parallel()`의 M10-T01/T02 개별 실패 격리 원칙과
동일 정신. 동점 시에는 `results` 순회 순서(=`run_ensemble()`에 넘긴
`engine_names` 순서)상 그 출력을 가장 먼저 낸 엔진을 대표로 고른다.

**구현**:
- `src/ai_workspace/interfaces/result_aggregator.py`(신규) —
  `AggregatedResult`(output, success, agreeing_engines,
  dissenting_engines, failed_engines, agreement_ratio) +
  `ResultAggregator(ABC)`.
- `src/ai_workspace/runtime/engine/result_aggregator.py`(신규) —
  `MajorityVoteAggregator`: 성공한 결과만 모아 `output` 문자열이 같은
  것끼리 투표수를 세고 최다 득표 출력을 대표로 선택.
- `tests/runtime/engine/test_result_aggregator.py`(신규) — 6건: 다수결
  선택, 동점 시 입력 순서 우선, 실패 엔진 격리, 전원 실패, 빈 dict,
  만장일치(`agreement_ratio == 1.0`).
- `docs/ARCHITECTURE.md` §3.9에 Result Aggregation / Consensus 서술
  추가, §7 Interface 표에 `ResultAggregator` 행 추가(29종→30종).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | ADR-0080이 명시적으로 보류했던 투표/합치기 공백을 이번 범위로 확인 | ✅ |
| 2 | 넓은 "Result Aggregation / Consensus" 주제를 사용자 확인으로 exact-match 다수결로 좁힘(semantic/LLM judge/가중치는 범위 밖) | ✅ |
| 3 | 개별 엔진 실패가 투표에 영향 없이 격리됨을 테스트로 증명 | ✅ |
| 4 | 동점 상황의 결정적(deterministic) 타이브레이크 규칙을 테스트로 증명 | ✅ |
| 5 | `run_ensemble()`/`EngineRuntime`에 자동 배선하지 않음(YAGNI, Composition Root 무변경) | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1213개(신규 6개, 회귀 없음)/`ruff`/`mypy`(228 source files)
전부 통과. ADR-0081.

---

## Milestone 64 — Cost & Routing Optimization: EngineRuntime 비용 기반 선택 (완료)

**배경**: 사용자가 "M64 cost & routing optimization"으로 착수 요청.
코드 조사 결과 두 갈래 실행 경로가 이미 존재했다: (1) Automation
파이프라인(`RecommendationExecutionService`)은 M17부터 이미 비용 기반
`EngineSelectionPolicy`(예산 내 최저 예상 비용 후보 선택)를 거치지만,
(2) Agent가 직접 쓰는 `EngineRuntime.run()`/`run_parallel()`/
`run_ensemble()`은 등록 순서상 "능력 만족하는 첫 엔진"만 고르고 비용을
전혀 보지 않는 완전히 별개의 라우팅 경로였다(`_select`/
`_require_adapter`, 추측 아님·코드 전수 확인). 또한 `Budget`은 Task
단위 개별 확인만 하고 여러 Task에 걸친 누적 소비 추적은 M15부터
명시적 Non-goal이다.

**사용자 승인(AskUserQuestion)**: "EngineRuntime에 비용 기반 선택
도입"으로 범위 확정 — 누적 예산(Spend Tracking) 추적은 M15 Non-goal을
그대로 유지하고 범위 밖으로 둔다.

**설계**: `InMemoryEngineRuntime`/`ManagedEngineRuntime` 생성자에
`engine_selection_policy: EngineSelectionPolicy | None = None`,
`budget_policy_engine: BudgetPolicyEngine | None = None`을 선택적으로
추가한다. 주입되면 `_select`/`_require_adapter`가 등록된 Adapter들로
`EngineCandidate` 목록(M17-T01과 동일 필드)을 만들어
`EngineSelectionPolicy.select()`에 그대로 위임한다 — 새 선택 로직을
중복 구현하지 않고 M17 로직을 재사용한다(DRY). 생략(기본값 `None`)하면
이전 동작(Milestone 64 이전)과 100% 동일하다. `run_parallel()`은 배치
전체에 하나의 Adapter를 고르는 기존 설계를 유지하되(사전 검사는
`tasks[0]`의 비용 기준), `ManagedEngineRuntime.run_parallel()`은 각
Task를 `self.run()`으로 개별 실행하므로 Task별 비용도 자연히 반영된다.
`run_ensemble()`은 호출자가 이름을 명시적으로 지정하므로 이번 범위에서
변경하지 않는다. `RecoveringEngineRuntime`은 내부 Runtime에 순수
위임하므로 변경 없음(생성자 주입도 내부 Runtime 쪽에서 이미 처리됨).

**구현**:
- `src/ai_workspace/runtime/engine/engine_runtime.py`
  (`InMemoryEngineRuntime`) — 생성자에 선택적 `engine_selection_policy`/
  `budget_policy_engine` 추가. `_select()`가 policy 유무에 따라 분기(기존
  첫 매칭 vs `EngineCandidate` 빌드 + `select()` 위임). `run_parallel()`에
  빈 tasks 가드 추가(`_select()`가 이제 `task`를 필요로 하므로
  `tasks[0]`을 사용 — 이전에는 필요하지 않았다).
- `src/ai_workspace/runtime/engine/managed_engine_runtime.py`
  (`ManagedEngineRuntime`) — 동일한 생성자 확장, `_require_adapter()`가
  같은 방식으로 분기.
- `tests/runtime/engine/test_engine_runtime.py` — `CostedEngineAdapter`
  (고정 비용 반환 + `run_count` 기록) 신규, 테스트 4건: policy 미주입 시
  기존 동작 유지(회귀), policy 주입 시 최저 비용 선택, budget과 함께
  주입 시 예산 초과 후보 제외, 예산 내 후보가 없으면
  `NoSuitableEngineError`.
- `tests/runtime/engine/test_managed_engine_runtime.py` — 동일한
  `CostedEngineAdapter` + 테스트 5건(위 4건 + `run_parallel()`이 배치
  전체에 비용 기반 선택을 적용하는지 확인).
- `docs/ARCHITECTURE.md` §3.9에 Cost & Routing Optimization 서술 추가
  (기존 "복수 매칭 시 우선순위 정책은 도입하지 않는다" 문구를 M64로
  갱신). 새 Core Domain Interface 없음(기존 `EngineSelectionPolicy`/
  `BudgetPolicyEngine` 재사용, 30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Agent 직접 실행 경로(`EngineRuntime`)가 비용을 전혀 보지 않는 별도 라우팅이었음을 코드로 확인 | ✅ |
| 2 | 넓은 "Cost & Routing Optimization" 주제를 사용자 확인으로 "EngineRuntime 비용 기반 선택"으로 좁힘(누적 예산 추적은 범위 밖) | ✅ |
| 3 | 기존 M17 `EngineSelectionPolicy`/`BudgetPolicyEngine` 로직을 재사용(중복 구현 없음, DRY) | ✅ |
| 4 | policy 미주입 시 이전 동작과 100% 동일함을 테스트로 증명(회귀 없음) | ✅ |
| 5 | policy 주입 시 최저 비용 선택 + 예산 초과 후보 제외를 테스트로 증명 | ✅ |
| 6 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1222개(신규 9개, 회귀 없음)/`ruff`/`mypy`(228 source files)
전부 통과. ADR-0082.

---

## Milestone 65 — Engine Learning & Adaptive Routing: 엔진별 신뢰도 추적 (완료)

**배경**: 사용자가 "M65 engine learning & adaptive routing"으로 착수
요청. 조사 결과 M49(Learning Engine)는 Recommendation/Adaptation
파이프라인의 학습만 다뤘고, M64에서 새로 생긴 `EngineRuntime`의 비용
기반 선택(`EngineSelectionPolicy`)은 순수 정적 비용만 보고 과거
성공/실패 이력을 전혀 반영하지 않았다 — 계속 실패하는 엔진이라도
비용이 가장 싸면 계속 선택된다(추측 아님, 코드 확인). Dashboard의
`ReliabilityStats`도 워크스페이스 전체 집계일 뿐 엔진별로 분리돼 있지
않아 재사용할 수 없었다.

**사용자 승인(AskUserQuestion)**: "EngineRuntime에 엔진별 신뢰도 추적 +
실패 엔진 제외"로 범위 확정 — `EngineSelectionPolicy.select()` 시그니처
확장(성공률 정식 점수화)이나 영속 저장소를 포함한 전체 파이프라인은
범위 밖으로 명시적으로 제외.

**설계**: `domain/engine_reliability.py`(신규)에 `EngineReliabilityStat`
(total/success_count/failure_count, M40 `ExperienceStat`과 동일한 필드
구성을 계층만 바꿔 재사용 — `runtime/engine/`이 `intelligence/`에
의존하면 계층 위반이라 별도 타입으로 둠) + `is_unreliable()`(M49/
ADR-0066과 완전히 동일한 임계값 규칙 `success_count == 0 and total >=
3`을 그대로 재사용, 새 규칙 설계 없음). `InMemoryEngineRuntime`/
`ManagedEngineRuntime`이 `run()`/`run_parallel()`/`run_ensemble()`이
실제로 실행한 엔진의 성공/실패를 이름별로 in-process 누적한다.
`engine_selection_policy`가 주입된 경로(M64)에서만
`EngineCandidate` 목록을 만들 때 `is_unreliable()`인 엔진을 미리
제외한 뒤 비용 기반 선택을 적용한다 — `EngineSelectionPolicy`
인터페이스 자체는 변경하지 않는다(Decision Only 계약 유지, 후보
필터링은 `EngineRuntime`의 책임으로 둠). policy 미주입 시(M64 이전
동작)에는 신뢰도 추적만 계속되고 제외는 적용되지 않아 100% 하위
호환이다. Cancel된 실행은 신뢰도에 반영하지 않는다(`EngineResult.error
== "cancelled"` sentinel로 판별). 영속 저장소는 M49/M50과 동일하게
이번 범위 밖(in-process 한정, YAGNI).

**구현**:
- `src/ai_workspace/domain/engine_reliability.py`(신규) —
  `EngineReliabilityStat`(frozen dataclass) + `record()`/
  `is_unreliable()`.
- `src/ai_workspace/runtime/engine/engine_runtime.py`
  (`InMemoryEngineRuntime`) — `_select()`가 이제 `(이름, adapter)`
  튜플을 반환. `run()`/`run_parallel()`/`run_ensemble()`이 실행 후
  `_record_engine_outcome()`으로 결과를 누적. `_build_candidates()`가
  `is_unreliable()`인 엔진을 후보에서 제외.
- `src/ai_workspace/runtime/engine/managed_engine_runtime.py`
  (`ManagedEngineRuntime`) — `_require_adapter()`가 동일하게
  `(이름, adapter)` 튜플 반환 + 신뢰도 필터링. `run()`은 Cancel되지
  않은 완료/실패/타임아웃만 신뢰도에 반영. `_run_named()`(`run_ensemble()`
  내부)도 결과를 누적.
- `tests/domain/test_engine_reliability.py`(신규) — `EngineReliabilityStat`
  단위 테스트 6건(성공/실패 기록, 표본 부족 시 미제외, 표본 충분 +
  전량 실패 시 제외, 성공 1건 이상이면 미제외).
- `tests/runtime/engine/test_engine_runtime.py`,
  `tests/runtime/engine/test_managed_engine_runtime.py` — 각각 3건:
  반복 실패 후 제외, 표본 부족 시 미제외, policy 미주입 시 제외
  미적용(회귀 없음).
- `docs/ARCHITECTURE.md` §3.9에 Engine Learning & Adaptive Routing
  서술 추가. 새 Core Domain Interface 없음(`EngineReliabilityStat`은
  Interface가 아닌 domain 값 객체, 30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | M64 비용 기반 선택이 과거 성공/실패를 전혀 반영하지 않음을 코드로 확인 | ✅ |
| 2 | 넓은 "Engine Learning & Adaptive Routing" 주제를 사용자 확인으로 "신뢰도 추적 + 실패 엔진 제외"로 좁힘 | ✅ |
| 3 | M49/ADR-0066 임계값 규칙을 그대로 재사용(새 규칙 설계 없음) | ✅ |
| 4 | 반복 실패 엔진이 후보에서 제외됨을 테스트로 증명 | ✅ |
| 5 | 표본 부족(실패 1~2건) 시 성급하게 제외하지 않음을 테스트로 증명 | ✅ |
| 6 | policy 미주입 시 이전 동작과 100% 동일함을 테스트로 증명(회귀 없음) | ✅ |
| 7 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1234개(신규 12개, 회귀 없음)/`ruff`/`mypy`(229 source files)
전부 통과. ADR-0083.

---

## Milestone 66 — Self Optimization: 제외 엔진 자동 복구(Probe) 메커니즘 (완료)

**배경**: 사용자가 "M66 self optimization"으로 착수 요청. "Self
Optimization"은 원래 `.ai/RULES.md` §7 로드맵의 M5 "Self Optimizer"(실행
결과 피드백으로 Policy 자체를 개선)를 가리켰으나(M6 이후로 미루고 그
이름으로는 구현된 적 없음, `InMemoryLLMPolicyEngine.select()`는 여전히
순수 정적 `dict.get()`), 조사 중 M65 자체 로직의 실제 공백도 함께
확인됐다: `EngineReliabilityStat.is_unreliable()`이 한번 참이 되면
`success_count`가 늘어날 방법이 없어(제외된 엔진은 `record()`가 호출되지
않음) 영구히 후보에서 빠진다 — 근본 원인이 고쳐진 엔진도 재선택될 길이
없다(추측 아님, 코드 확인).

**사용자 승인(AskUserQuestion)**: 세 선택지(a. M65 제외 엔진 자동
복구/재시도, b. `LLMPolicyEngine` 자체의 Self Optimizer, c. 둘 다) 중
**"M65 제외 엔진의 자동 복구(재시도) 메커니즘"**(a, 권장)으로 확정 —
`LLMPolicyEngine` Self Optimizer(원래 M5 개념)는 이번 범위 밖으로 명시적
제외.

**설계**: 새 Interface 없이 기존 `EngineReliabilityStat`(M65)만 확장한다.
`skip_count: int` 필드 + `skip()`(제외될 때마다 호출, 다른 필드는
유지하고 `skip_count`만 +1) + `is_probe_eligible()`(`skip_count >=
_PROBE_INTERVAL`(5)) 추가. `record()`는 실제 실행 결과와 무관하게
`skip_count`를 0으로 되돌린다(다음 탐색까지 다시 카운트). `_build_
candidates()`(`InMemoryEngineRuntime`)/`_require_adapter()`
(`ManagedEngineRuntime`)의 제외 조건을 `is_unreliable()`에서
`is_unreliable() and not is_probe_eligible()`로 변경 — 조건을 만족하지
못하면(아직 probe 자격 없음) `skip()`으로 카운트만 하고 여전히 후보에서
제외, `_PROBE_INTERVAL`번 연속 제외됐으면 후보에 다시 포함해(probe) 한
번 더 기회를 준다. probe 실행이 성공하면 `is_unreliable()`이 거짓이 되어
정상 복귀하고, 다시 실패하면 `skip_count`가 0부터 다시 쌓여 다음 probe
까지 또 5번의 쿨다운을 거친다. `EngineSelectionPolicy`(M17) Decision-Only
계약은 M64/M65와 동일하게 무변경 — 필터링은 계속 `EngineRuntime`의
책임으로 둔다.

**구현**:
- `src/ai_workspace/domain/engine_reliability.py` — `EngineReliabilityStat`에
  `skip_count` 필드 + `skip()`/`is_probe_eligible()` 메서드 추가,
  `record()`가 `skip_count`를 0으로 리셋. `_PROBE_INTERVAL: Final[int] = 5`
  모듈 상수 신규.
- `src/ai_workspace/runtime/engine/engine_runtime.py`
  (`InMemoryEngineRuntime`) — `_build_candidates()`의 제외 조건에
  `is_probe_eligible()` 반영, 제외 시 `self._engine_reliability[name] =
  stat.skip()`으로 갱신.
- `src/ai_workspace/runtime/engine/managed_engine_runtime.py`
  (`ManagedEngineRuntime`) — `_require_adapter()`에 동일 로직 적용.
- `tests/domain/test_engine_reliability.py` — `skip()`/`is_probe_eligible()`
  단위 테스트 4건(임계값 미달/도달, skip이 신뢰도 카운트에 영향 없음,
  `record()`가 `skip_count` 리셋).
- `tests/runtime/engine/test_engine_runtime.py`,
  `tests/runtime/engine/test_managed_engine_runtime.py` — 각각 2건: 제외된
  엔진이 `_PROBE_INTERVAL`번 연속 건너뛴 뒤 다시 후보로 포함됨을 증명,
  probe 실행이 성공하면 정상 복귀해 계속 선택됨을 증명.
- `docs/ARCHITECTURE.md` §3.9에 "Self Optimization — 제외 엔진 자동
  복구(Milestone 66, ADR-0084)" 서술 추가. 새 Core Domain Interface 없음
  (30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | M65 `is_unreliable()`이 영구 제외임을 코드로 확인(성공 기록 경로 부재) | ✅ |
| 2 | 넓은 "Self Optimization" 주제를 사용자 확인으로 "M65 제외 엔진 자동 복구"로 좁힘 | ✅ |
| 3 | 새 Interface 없이 기존 `EngineReliabilityStat`만 확장(YAGNI) | ✅ |
| 4 | 제외 상태에서는 선택되지 않음을 테스트로 증명 | ✅ |
| 5 | `_PROBE_INTERVAL`번 경과 후 다시 후보로 포함됨을 테스트로 증명 | ✅ |
| 6 | probe 성공 시 정상 복귀함을 테스트로 증명 | ✅ |
| 7 | policy 미주입 경로는 M64/M65와 동일하게 영향 없음(회귀 없음) | ✅ |
| 8 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1242개(신규 8개, 회귀 없음)/`ruff`/`mypy`(229 source files)
전부 통과. ADR-0084.

---

## Milestone 67 — LLMPolicyEngine Self Optimizer: 실행 결과 기반 정책 자동 대체 (완료)

**배경**: 사용자가 "M67 self optimization"으로 착수 요청. ADR-0084(M66)가
"`LLMPolicyEngine` Self Optimizer(원래 `.ai/RULES.md` §7 M5 개념)"를
명시적으로 범위 밖으로 미루고 별도 Milestone 후보로 남겨 두었던 항목이다.
조사 결과 `InMemoryLLMPolicyEngine.select()`는 M5-T01 이후 줄곧 순수 정적
`dict.get()`이었고(코드 확인), `AgentSession.llm_policy_decision`은
`CodingAgent`/`ReviewAgent`/`DocumentationAgent`가 `engine_runtime.run()`에
실제로 전달해 실행 결과(`EngineResult.success`)까지 만들어내지만, 그 결과가
정책으로 되먹여지는 경로는 전혀 없었다.

**사용자 승인(AskUserQuestion, 4회)**:
1. 범위 — (a) 관측만/(b) 관측+자동 대체/(c) 관측+자동 대체+Probe 복구 중
   **(b, 권장)**으로 확정. M65/M66이 관측→복구를 두 Milestone으로 나눈
   전례와 동일하게 Probe/자동 복구는 범위 밖.
2. 집계 단위 — **`(AgentRole, LLMModel)` 조합(권장)**으로 확정.
3. 대체 소스 — **기존 `INITIAL_MODELS` 목록에서 다음 모델(권장)**로 확정.
4. 피드백 경로 — **`CodingAgent` 등 호출부가 명시적으로 기록(권장)**으로
   확정 — `EngineRuntime`이 `LLMPolicyEngine`을 자동 주입받는 대안은
   engine 계층이 policy 계층을 아는 새 의존 방향이 생겨 기각.

최종 구체 설계(신설 타입/메서드 시그니처/전환 규칙)도 별도 AskUserQuestion
으로 확인 후 구현 착수.

**설계**: `domain/llm_policy_reliability.py`(신규)에
`LLMPolicyReliabilityStat`(total/success_count/failure_count, M65
`EngineReliabilityStat`과 동일한 필드 구성·임계값 규칙 `success_count == 0
and total >= 3`을 재사용하되 `skip_count`/Probe는 가져오지 않음). `LLMPolicyEngine`
interface에 `record_outcome(role, decision, success) -> None` abstract method를
추가한다 — `select()`의 read-only 계약은 그대로 유지하고 결과 기록은 이
메서드로만 이루어진다. `InMemoryLLMPolicyEngine`이 `dict[(AgentRole,
LLMModel), LLMPolicyReliabilityStat]`과 role별 활성 Decision 재정의를
내부 상태로 갖는다 — `select(role)`은 활성 Decision의 `(role, model)`
통계가 `is_unreliable()`이면 `INITIAL_MODELS` 순서상 다음 모델로 전환한
Decision(effort는 원래 값 유지)을 반환한다. 이미 마지막 모델이면 더 이상
전환하지 않는다. `AgentRuntime.record_llm_policy_outcome(session_id,
success)`가 `llm_policy_engine`/session의 policy decision 유무를 확인해
`LLMPolicyEngine.record_outcome()`으로 위임한다(둘 중 하나라도 없으면
no-op) — Agent는 `LLMPolicyEngine` interface를 직접 알지 못하고
`AgentRuntime` 한 곳만 거친다.

**구현**:
- `src/ai_workspace/domain/llm_policy_reliability.py`(신규) —
  `LLMPolicyReliabilityStat`(frozen dataclass) + `record()`/`is_unreliable()`.
- `src/ai_workspace/interfaces/llm_policy_engine.py` — `record_outcome()`
  abstract method 추가(계약 docstring 포함).
- `src/ai_workspace/engines/llm_policy_engine.py`
  (`InMemoryLLMPolicyEngine`) — 통계 dict + 활성 Decision dict 추가,
  `select()`가 신뢰 불가 시 `INITIAL_MODELS` 다음 모델로 자동 전환,
  `record_outcome()` 구현, `_next_model()` 헬퍼.
- `src/ai_workspace/runtime/agent/agent_runtime.py` —
  `record_llm_policy_outcome(session_id, success)` 추가.
- `src/ai_workspace/agents/coding_agent.py`,
  `review_agent.py`, `documentation_agent.py` — `agent_runtime` 필드
  저장 + `engine_runtime.run()` 직후 `record_llm_policy_outcome()` 호출.
- `tests/interfaces/fakes.py` — `FakeLLMPolicyEngine`에 `record_outcome()`
  구현 + `recorded_outcomes` 기록 리스트 추가.
- `tests/domain/test_llm_policy_reliability.py`(신규) — 5건(성공/실패
  기록, 표본 부족 시 미판정, 표본 충분+전량 실패 시 판정, 성공 1건
  이상이면 미판정).
- `tests/engines/test_llm_policy_engine.py` — 7건 추가(기록만으로는
  선택 불변, 신뢰 불가 시 다음 모델로 대체, 표본 부족/성공 1건 이상 시
  미대체, 연속 대체로 여러 단계 전환, 마지막 모델에서 정지, 다른 Role은
  영향받지 않음).
- `tests/interfaces/test_llm_policy_engine.py` — `record_outcome()` 계약
  테스트 1건.
- `tests/runtime/agent/test_agent_runtime.py` — `record_llm_policy_outcome()`
  테스트 3건(정상 위임, engine 미주입 시 no-op, decision 없을 시 no-op).
- `docs/ARCHITECTURE.md` §3.9에 Self Optimization(정책 계층, M67) 서술
  추가, §7 Interface 표의 `LLMPolicyEngine` 행 갱신. 새 Core Domain
  Interface 없음(기존 `LLMPolicyEngine` 확장, 30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `InMemoryLLMPolicyEngine.select()`가 여전히 순수 정적 `dict.get()`임을 코드로 확인 | ✅ |
| 2 | 넓은 "Self Optimization" 주제를 AskUserQuestion 4회로 "관측 + 자동 대체" + 구체 설계까지 좁힘 | ✅ |
| 3 | M65/ADR-0083 임계값 규칙을 그대로 재사용(새 규칙 설계 없음) | ✅ |
| 4 | 반복 실패한 (Role, Model)이 `INITIAL_MODELS` 다음 모델로 자동 대체됨을 테스트로 증명 | ✅ |
| 5 | 표본 부족/성공 1건 이상이면 대체하지 않음을 테스트로 증명 | ✅ |
| 6 | 마지막 모델에서는 더 이상 대체하지 않음을 테스트로 증명 | ✅ |
| 7 | 한 Role의 대체가 다른 Role에 영향을 주지 않음을 테스트로 증명 | ✅ |
| 8 | `record_outcome()`을 호출하지 않으면 기존 동작과 100% 동일함을 테스트로 증명(회귀 없음) | ✅ |
| 9 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1259개(신규 11개, 회귀 없음)/`ruff`/`mypy`(230 source files)
전부 통과. ADR-0085.

---

## Milestone 68 — Dynamic Ensemble Routing: EngineSelectionPolicy 기반 top-N 자동 선택 (완료)

**배경**: 사용자가 "M68 Dynamic Ensemble Routing"으로 착수 요청. `run_ensemble()`
(M62)은 `engine_names`를 호출자가 직접 나열해야 했고, M64/M65/M66에서
`run()`/`estimate_cost()` 경로에 이미 구현된 `EngineSelectionPolicy` 기반
비용·신뢰도 인식 선택(`engine_selection_policy` 주입 시 `_select`/
`_require_adapter`가 수행)을 전혀 활용하지 못했다 — 같은 Task를 여러
엔진에 "동적으로" 분산하려면 호출자가 후보 목록을 미리 알아야 했다
(코드 확인, 추측 아님).

**설계**: 새 Core Domain Interface를 추가하지 않고 기존 `EngineRuntime`에
`run_ensemble_auto(task, required_capabilities=frozenset(), *, top_n=2,
model=None) -> dict[str, EngineResult]` abstract method 하나만 추가한다.
내부적으로 `run()`/`estimate_cost()`가 쓰는 후보 선정 로직
(`InMemoryEngineRuntime._build_candidates()`, `ManagedEngineRuntime`은
`_require_adapter()`에서 동일 로직을 `_build_candidates()`로 추출해 재사용)
을 그대로 활용해 `EngineCandidate` 목록을 만들고, `engine_selection_policy`가
주입돼 있으면 `EngineSelectionPolicy.select()`를 반복 호출한다(매 회마다
직전에 선택된 후보를 제거하고 재호출) — "가장 낮은 비용"을 고르는 M17
규칙을 그대로 반복 적용해 top-N을 얻는다(`EngineSelectionPolicy.select()`
시그니처는 무변경, Decision Only 계약 유지). M65/M66의 신뢰도 기반
제외·Probe 규칙도 후보 빌드 단계에서 자동으로 함께 적용된다. 정책 미주입
시에는 `run()`의 "등록 순서상 첫 매칭" 원칙을 그대로 확장해 "첫 top_n개"를
고른다(100% 하위 호환). 선택된 이름 목록은 기존 `run_ensemble()`에 그대로
위임한다 — 동시 실행/개별 엔진 실패 격리 메커니즘(M62, `ThreadPoolExecutor`)
을 재사용하고 새로 만들지 않는다(YAGNI).

**구현**:
- `src/ai_workspace/interfaces/engine_runtime.py` — `run_ensemble_auto()`
  abstract method 추가(계약 docstring 포함).
- `src/ai_workspace/runtime/engine/engine_runtime.py`
  (`InMemoryEngineRuntime`) — `run_ensemble_auto()` + `_select_top_n()` 추가,
  기존 `run_ensemble()`에 위임.
- `src/ai_workspace/runtime/engine/managed_engine_runtime.py`
  (`ManagedEngineRuntime`) — `_require_adapter()`의 후보 빌드 로직을
  `_build_candidates()`로 추출(재사용), `run_ensemble_auto()` +
  `_select_top_n()` 추가.
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py`
  (`RecoveringEngineRuntime`) — `run_ensemble()`과 동일한 이유로 재시도
  없이 내부 Runtime에 그대로 위임.
- `tests/interfaces/fakes.py`(`FakeEngineRuntime`),
  `tests/runtime/engine/test_recovering_engine_runtime.py`
  (`ScriptedEngineRuntime`), `tests/core/test_workspace_core.py`
  (`SpyEngineRuntime`), `tests/agents/test_coding_agent.py`
  (`RecordingEngineRuntime`) — 새 abstract method 구현 추가(ABC 계약
  충족, 대부분 미사용 경로는 `NotImplementedError`/`AssertionError`로
  기존 테스트 더블 관례 유지).
- `tests/runtime/engine/test_engine_runtime.py`,
  `tests/runtime/engine/test_managed_engine_runtime.py` — 각 7건 추가
  (정책 미주입 시 첫 top_n개, 정책 주입 시 최저 비용 top_n개, capability
  필터링, 후보 부족 시 있는 만큼만 반환, 후보 없음 시
  `NoSuitableEngineError`, `top_n < 1`이면 빈 dict, 신뢰도 기반 제외
  규칙이 그대로 적용됨).
- `tests/runtime/engine/test_recovering_engine_runtime.py` — 위임 확인
  테스트 1건 추가.
- `docs/ARCHITECTURE.md` §3.9에 Dynamic Ensemble Routing(M68) 서술 추가.
  새 Core Domain Interface 없음(기존 `EngineRuntime` 확장, 30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | `run_ensemble()`이 호출자가 엔진 이름을 직접 나열해야 하는 계약임을 코드로 확인 | ✅ |
| 2 | 새 Core Domain Interface 없이 기존 `EngineRuntime`만 확장(`run_ensemble_auto()` 1개 메서드) | ✅ |
| 3 | `EngineSelectionPolicy`(M17) 재사용 — 시그니처 무변경, 새 알고리즘 없음 | ✅ |
| 4 | top-N 동적 선택이 비용 기준으로 동작함을 테스트로 증명 | ✅ |
| 5 | required_capabilities로 후보가 필터링됨을 테스트로 증명 | ✅ |
| 6 | M65/M66 신뢰도 기반 제외 규칙이 그대로 적용됨을 테스트로 증명 | ✅ |
| 7 | M62의 `run_ensemble()`(병렬 실행 + 개별 실패 격리)을 그대로 재사용(중복 구현 없음) | ✅ |
| 8 | 정책 미주입 시 등록 순서상 첫 top_n개를 고르는 기존 원칙과 일치(회귀 없음) | ✅ |
| 9 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1274개(신규 15개, 회귀 없음)/`ruff`/`mypy`(230 source files)
전부 통과. ADR-0086.

---

## Milestone 69 — Execution Memory & Context Routing: 실행 결과 기반 Engine 추천 (완료)

**배경**: 사용자가 "M69 Execution Memory & Context Routing"으로 명확한
범위를 담아 착수를 요청했다 — M68까지는 Engine 선택이 (비용/신뢰도로)
학습은 하지만, Task의 종류별로 "어떤 Engine 조합이 더 좋았는지"를
기억해 다음 실행에 반영하는 메커니즘은 없었다.

**사용자 승인(AskUserQuestion, 4회)**:
1. 유사도 기준 — domain.Task에 TaskType/난이도 필드가 없어 **required_
   capabilities 조합만 사용(권장)**으로 확정. Role까지 포함하려면
   `EngineRuntime` 전체 시그니처에 새 파라미터가 필요해 범위가 커진다.
2. 저장 위치 — **새 domain 값 객체 + EngineRuntime in-process 상태
   (권장)**로 확정. 기존 `ExecutionMemoryStore`(M39)는 Agent 실행 경로와
   완전히 분리된 별도 통로(ADR-0053, §8 규칙 14)라 재사용 시 계층 경계가
   깨진다.
3. 반영 방식 — **후보 랭킹에 성공률을 반영해 재정렬(권장)**으로 확정.
4. 지표 범위 — **성공/실패만 랭킹에 반영, latency는 기록만(권장)**으로
   확정.

**설계상 발견한 충돌과 해결**: 최초 구현("표본 충분 + 최고 성공률
엔진으로 후보를 좁힘")은 M65 `test_run_with_policy_recovers_after_
successful_probe` 테스트를 깨뜨렸다 — Probe가 성공해 `is_unreliable()`
이 즉시 거짓이 되어도(M66의 "복구 즉시 완전 신뢰"), 과거 실패 이력이
여전히 남아 있는 실행 메모리 성공률이 다른 엔진보다 낮으면 후보에서
계속 밀려나 M65/M66이 이미 보장한 동작이 깨졌다. 이를 해결하기 위해
"후보 제외/좁히기"가 아니라 **비용이 동률(tie)인 후보끼리만 성공률로
재정렬**하는 방식으로 범위를 좁혔다 — `EngineSelectionPolicy`의 `min()`
은 비용이 다르면 항상 진짜 최저 비용을 그대로 고르므로, 비용이 다른
기존 모든 M64/M65/M66/M68 테스트는 전혀 영향받지 않는다. 또한 재정렬
자체도 "표본 부족(미검증)"을 가장 나쁜 값이 아니라 중립값(0.5)으로
취급한다 — 그렇지 않으면 아직 검증되지 않았을 뿐인 엔진이 이미 확인된
저성능 엔진보다 부당하게 밀리는 새 버그가 생긴다.

**구현**:
- `src/ai_workspace/domain/engine_execution_memory.py`(신규) —
  `EngineExecutionMemoryStat`(total/success_count/failure_count/
  total_latency_seconds, M65 `EngineReliabilityStat`과 필드 구성은
  같지만 집계 키가 `(required_capabilities, engine_name)` 조합이라는
  점이 다르다). `success_rate()`는 표본 3건 미만이면 `None`(M49/M65와
  동일한 임계값), `average_latency_seconds()`는 기록만 하고 랭킹에는
  반영하지 않는다.
- `src/ai_workspace/runtime/engine/engine_runtime.py`
  (`InMemoryEngineRuntime`), `src/ai_workspace/runtime/engine/
  managed_engine_runtime.py`(`ManagedEngineRuntime`) — `run()`(Managed는
  Cancel 제외)/`run_ensemble_auto()`가 실행 결과+latency를
  `_record_execution_memory()`로 누적. `_build_candidates()`가 (기존
  신뢰도 제외 이후) `_reorder_by_execution_memory()`로 후보를 성공률
  내림차순 재정렬(표본 부족/미검증 엔진은 중립값 0.5) — `engine_
  selection_policy` 주입 경로에서만 적용, 비용이 다른 경우 결과에
  영향 없음(100% 하위 호환).
- `RecoveringEngineRuntime`은 변경 없음(순수 위임 구조 그대로, `run()`/
  `run_ensemble_auto()`를 그대로 내부 Runtime에 위임).
- `tests/domain/test_engine_execution_memory.py`(신규) — 7건(성공/실패
  기록+latency, 표본 부족 시 `None`, 표본 충분 시 성공률 계산, latency
  평균 계산).
- `tests/runtime/engine/test_engine_runtime.py`,
  `tests/runtime/engine/test_managed_engine_runtime.py` — 각 2건 추가
  (비용 동률에서 검증된 성공 이력이 미검증 엔진보다 우선, 반대로
  검증된 "전량 실패" 이력은 미검증 엔진보다 밀림).
- `docs/ARCHITECTURE.md` §3.9에 Execution Memory & Context Routing(M69)
  서술 추가. 새 Core Domain Interface 없음(기존 `EngineRuntime`의 내부
  구현만 확장, 30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | M68까지 Task 종류별 Engine 추천 메커니즘이 없었음을 코드로 확인 | ✅ |
| 2 | 넓은 "Execution Memory & Context Routing" 주제를 AskUserQuestion 4회로 구체 설계까지 좁힘 | ✅ |
| 3 | 기존 Learning/Memory 구조(M65 `EngineReliabilityStat` 패턴) 재사용, 새 Core Domain Interface 없음 | ✅ |
| 4 | 유사한 Task(같은 required_capabilities)에서 성공률이 높은 엔진이 우선 추천됨을 테스트로 증명 | ✅ |
| 5 | M65/M66의 신뢰도 제외·Probe 복구 회귀 테스트가 전부 그대로 통과(설계 충돌 해결 확인) | ✅ |
| 6 | 비용이 다른 경우 기존 M64 cost 규칙이 100% 그대로 유지됨(회귀 없음) | ✅ |
| 7 | latency는 기록만 하고 랭킹에 반영하지 않음을 코드/테스트로 확인 | ✅ |
| 8 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1286개(신규 12개, 회귀 없음)/`ruff`/`mypy`(231 source files)
전부 통과. ADR-0087.

---

## Milestone 70 — Adaptive Consensus: Consensus 합의 이력 기반 가중 투표 (완료)

**배경**: 사용자가 "M70 Adaptive Consensus"로 명확한 범위를 담아 착수를
요청했다 — M69까지는 과거 실행 이력을 바탕으로 Engine/Ensemble 선택
자체는 학습하지만, `run_ensemble()`(M62) 결과를 합치는
`ResultAggregator`(M63, `MajorityVoteAggregator`)는 정확한 문자열 일치
다수결(표 개수)에만 머물러 있었다 — 어떤 엔진의 표가 과거에 실제
합의와 자주 일치했는지는 전혀 반영하지 않았다.

**사용자 승인(AskUserQuestion, 4회)**:
1. 이력 정의 — M69 `EngineExecutionMemoryStat`(실행 성공률) 재사용 안과
   새 Consensus 전용 이력(투표가 합의와 일치했는지) 안 중 **새
   Consensus 합의 이력(권장)**으로 확정. "실행 성공"과 "투표가 다수
   의견에 속함"은 서로 다른 신호이기 때문이다.
2. 저장 위치 — **EngineRuntime in-process 상태(권장)**로 확정.
   M65/M69와 동일한 패턴을 재사용한다.
3. 반영 방식 — **가중치 합계 비교(권장)**로 확정. 신뢰도 낮은 엔진의
   표를 아예 제외하는 필터링 방식은 M69에서 겪은 회귀 전례 때문에
   기각했다.
4. 인터페이스 변경 범위 — **무변경, 새 클래스만 추가(권장)**로 확정.
   `ResultAggregator.aggregate()` 시그니처는 그대로 두고 새
   `AdaptiveConsensusAggregator` 클래스만 추가한다.

**구현**:
- `src/ai_workspace/domain/consensus_agreement.py`(신규) —
  `ConsensusAgreementStat`(total/agree_count/disagree_count).
  `agreement_rate()`는 표본 3건 미만이면 `None`(M49/M65/M69와 동일한
  임계값). M69의 `EngineExecutionMemoryStat`과 필드 구성은 비슷하지만
  "실행 성공/실패"가 아니라 "투표가 합의와 일치했는지"를 추적하는
  별개 신호라 별도 값 객체로 분리했다.
- `src/ai_workspace/interfaces/engine_runtime.py` — `EngineRuntime`에
  `record_consensus_outcome(required_capabilities, agreeing_engines,
  dissenting_engines)`(기록)/`consensus_weight(required_capabilities,
  engine_name)`(조회, 표본 부족 시 중립값 0.5) 두 abstract method를
  최소 확장. `EngineRuntime`은 `ResultAggregator`를 전혀 알지 못하며
  (ADR-0080/0081의 결합 방지 원칙 유지) 이 두 메서드로만 연결된다.
- `src/ai_workspace/runtime/engine/engine_runtime.py`
  (`InMemoryEngineRuntime`), `src/ai_workspace/runtime/engine/
  managed_engine_runtime.py`(`ManagedEngineRuntime`) — 위 두 메서드
  구현, `(required_capabilities, engine_name)` 키의 `_consensus_agreement`
  dict로 누적.
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py` — 두
  메서드 모두 내부 Runtime에 순수 위임(재시도와 무관한 상태).
- `src/ai_workspace/runtime/engine/result_aggregator.py` —
  `AdaptiveConsensusAggregator`(신규, `ResultAggregator` 구현체) 추가.
  생성자로 `EngineRuntime`과 `required_capabilities`를 주입받아,
  `consensus_weight()` 가중치 합계로 승자를 정하고(동률이면 표
  개수 → 입력 순서로 2차 tie-break), 집계 직후 자신이 계산한
  `agreeing_engines`/`dissenting_engines`를 `record_consensus_outcome()`
  으로 되돌려준다. `aggregate()`의 기존 계약(시그니처·반환 타입·빈
  입력/전원 실패 처리)은 전혀 바꾸지 않아 `MajorityVoteAggregator`는
  영향받지 않는다(100% 하위 호환).
- 테스트 더블(`tests/interfaces/fakes.py` `FakeEngineRuntime`,
  `tests/core/test_workspace_core.py` `SpyEngineRuntime`,
  `tests/agents/test_coding_agent.py` `RecordingEngineRuntime`,
  `tests/runtime/engine/test_recovering_engine_runtime.py`
  `ScriptedEngineRuntime`) 모두 새 abstract method 2개에 대한 최소
  구현/스텁 추가.
- `tests/domain/test_consensus_agreement.py`(신규) — 5건(합의/불합치
  기록, 표본 부족 시 `None`, 표본 충분 시 비율 계산).
- `tests/runtime/engine/test_engine_runtime.py`,
  `tests/runtime/engine/test_managed_engine_runtime.py` — 각각
  `consensus_weight()`/`record_consensus_outcome()` 기본값·표본
  임계값·capability별 분리·엔진별 독립 기록을 검증하는 테스트 추가.
- `tests/runtime/engine/test_result_aggregator.py` — 4건 추가(이력
  없을 때 순수 다수결과 동일, 표는 적어도 과거 합의 일치율이 높은
  엔진이 표가 많은 소수 의견 그룹을 이기는 핵심 시나리오, 집계 후
  이력이 자동 기록됨, 전원 실패 시 이력 기록 없음).
- `tests/runtime/engine/test_recovering_engine_runtime.py` — 1건 추가
  (두 메서드 모두 내부 Runtime에 위임됨을 확인).
- `docs/ARCHITECTURE.md` §3.9에 Adaptive Consensus(M70) 서술 추가,
  §7 인터페이스 표 `EngineRuntime`/`ResultAggregator` 행 갱신. 새 Core
  Domain Interface 없음(기존 `EngineRuntime`의 메서드 2개 확장 + 기존
  `ResultAggregator` 계약 재사용, 30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | M69까지 Consensus 결과 자체가 단순 다수결에 머물렀음을 코드로 확인 | ✅ |
| 2 | 넓은 "Adaptive Consensus" 주제를 AskUserQuestion 4회로 구체 설계까지 좁힘 | ✅ |
| 3 | 기존 Learning/Memory/EngineSelection 구조(M65/M69 패턴) 재사용, 새 Core Domain Interface 없음 | ✅ |
| 4 | 기존 Majority Voting(`MajorityVoteAggregator`)과 100% 하위 호환(계약 무변경, 회귀 없음) | ✅ |
| 5 | 표는 적어도 과거 합의 일치율이 높은 엔진의 표가 표는 많지만 이력이 나쁜 그룹을 이김을 테스트로 증명 | ✅ |
| 6 | 이력이 없을 때(중립값) 순수 다수결과 동일하게 동작함을 테스트로 확인 | ✅ |
| 7 | `EngineRuntime`이 `ResultAggregator`를 모르는 기존 결합 방지 원칙 유지(기록/조회 메서드 2개로만 연결) | ✅ |
| 8 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1304개(신규 18개, 회귀 없음)/`ruff`/`mypy`(232 source files)
전부 통과. ADR-0088.

---

## Milestone 71 — Workflow Learning: 성공률 높은 실행 순서(Template) 추천 (완료)

**배경**: 사용자가 "M71 Workflow Learning"으로 명확한 범위를 담아
착수를 요청했다 — 최신 main(`831ef11`)은 이미 작업 브랜치에 포함돼
있어 별도 병합이 필요 없었다. 조사 결과 "Workflow"는 두 갈래로 존재함을
확인했다: (a) `domain.Workflow`/`WorkflowEngine`/`WorkflowRunner`
(Milestone 2/12, task_ids+dependencies 기반 DAG 위상 정렬·순차 실행),
(b) M34(ADR-0048)가 재정의한 Intelligence 경로(Milestone Task 실행
흐름, `domain.Workflow` 무변경). 사용자가 "WorkflowEngine"을 명시했으므로
(a)가 대상이다. `WorkflowEngine.plan()`은 의존관계만 만족하면 되는 순수
계산이었고, 실행 결과를 기억해 다음 계획에 반영하는 경로는 없었다.
"Learning Engine"(M49~M51)은 Recommendation 경로의 완전히 다른
기능이라 이번 범위와 무관함을 확인했다.

**사용자 승인(AskUserQuestion, 4회)**:
1. 유사도 기준 — domain.Workflow에는 템플릿 ID가 없어 **task_ids+
   dependencies 정확히 일치(권장)**로 확정. M69의 `required_capabilities`
   정확 일치 키 패턴을 그대로 재사용한다.
2. 반영 방식 — **성공률 높은 전체 순서를 Template로 저장해 그대로
   추천(권장)**으로 확정. M69/M70의 tie-break 방식과 달리, 충돌하는
   기존 보장이 없어 더 직접적인 전체 순서 추천을 채택했다.
3. 저장/기록 위치 — **WorkflowEngine in-process 상태 + WorkflowRunner가
   자동 기록(권장)**으로 확정. M65/M69/M70과 동일한 패턴.
4. 최소 표본 기준 — **기존과 동일하게 3건 이상(권장)**으로 확정.

**구현**:
- `src/ai_workspace/domain/workflow_order_memory.py`(신규) —
  `WorkflowOrderStat`(total/success_count/failure_count). `success_rate()`
  는 표본 3건 미만이면 `None`(M49/M65/M69/M70과 동일한 임계값). 키가
  "엔진 이름"이 아니라 "실행 순서(order tuple) 자체"라는 점이 M65/M69/
  M70의 값 객체와 다르다.
- `src/ai_workspace/interfaces/workflow_engine.py` — `WorkflowEngine`에
  `record_run_outcome(workflow, order, success)`(기록)/
  `recommended_order(workflow)`(조회, 표본 부족/이력 없음 시 `None`)
  두 abstract method를 최소 확장. `plan()` 시그니처는 무변경.
- `src/ai_workspace/engines/workflow_engine.py`(`InMemoryWorkflowEngine`)
  — `_signature(workflow)`로 `frozenset(task_ids)` + 의존관계 간선
  집합을 키로 `_order_stats` dict에 누적. `plan()`은 `recommended_order()`
  가 값을 반환하면 그대로 쓰고, 없으면(이력 없음) 기존 DFS 기반 위상
  정렬 그대로 동작(100% 하위 호환). 동률이면 표본 수 → 먼저 기록된
  순서 순으로 결정적 tie-break.
- `src/ai_workspace/runtime/workflow/workflow_runner.py`(`WorkflowRunner`)
  — `run()`이 완료 직후(성공/실패 모두) 실제로 쓰인 `order`와 결과를
  `record_run_outcome()`으로 자동 기록. 호출자가 별도로 챙기지 않아도
  다음 `plan()` 호출부터 반영된다.
- `tests/interfaces/fakes.py`(`FakeWorkflowEngine`) — 두 메서드를 최소
  스텁(기록은 no-op, 조회는 항상 `None`)으로 구현해 기존 테스트 동작
  유지.
- `tests/domain/test_workflow_order_memory.py`(신규) — 5건(성공/실패
  기록, 표본 부족 시 `None`, 표본 충분 시 성공률 계산).
- `tests/engines/test_workflow_engine.py` — 6건 추가(이력 없을 때
  `None`, 표본 부족 시 `None`, 성공률 높은 순서 추천, `plan()`이 학습된
  순서를 그대로 반환, 이력 없으면 기존 위상정렬과 동일, task_ids/
  dependencies가 다르면 학습이 섞이지 않음).
- `tests/runtime/workflow/test_workflow_runner.py` — 2건 추가(`run()`
  이 자동으로 이력을 기록함, `WorkflowEngine`이 추천한 순서를
  `WorkflowRunner`가 그대로 따름).
- `docs/ARCHITECTURE.md` §3.12 Workflow Runner 절에 Workflow
  Learning(M71) 서술 추가, §7 인터페이스 표 `WorkflowEngine` 행 갱신.
  새 Core Domain Interface 없음(기존 `WorkflowEngine`의 메서드 2개
  확장, 30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작(이미 포함돼 있음을 `git merge-base`로 확인) | ✅ |
| 2 | 기존 ADR/TASKS/ROADMAP과 실제 코드를 조사해 "Workflow"의 두 갈래(도메인 DAG vs Intelligence 재정의)를 구분하고 대상 확정 | ✅ |
| 3 | 넓은 "Workflow Learning" 주제를 AskUserQuestion 4회로 구체 설계까지 좁힘 | ✅ |
| 4 | 기존 WorkflowEngine/Learning/Memory 구조(M65/M69/M70 패턴) 재사용, 새 Core Domain Interface 없음 | ✅ |
| 5 | 동일/유사 Workflow 재실행 시 성공률 높은 순서가 추천됨을 테스트로 증명 | ✅ |
| 6 | 학습 이력이 없으면 기존 `plan()`과 100% 동일하게 동작함을 테스트로 확인(회귀 없음) | ✅ |
| 7 | 영속화 없음(in-process 한정)을 코드로 확인 | ✅ |
| 8 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1317개(신규 13개, 회귀 없음)/`ruff`/`mypy`(233 source files)
전부 통과. ADR-0089.

---

## Milestone 72 — Workflow Adaptive Planning: 학습된 순서를 실제 계획에 안전하게 반영 (완료)

**배경**: 사용자가 "M71의 Workflow Learning을 실제 Workflow 계획(plan)에
자동 반영"하는 M72 착수를 요청했다. 코드를 조사한 결과 `InMemoryWorkflowEngine.
plan()`은 M71에서 이미 `recommended_order()`를 먼저 조회하고 없으면 기존
DFS 위상 정렬로 fallback하는 구조였다. 다만 M71의 `_signature()`는
`task_ids`+`dependencies` 간선까지 정확히 일치해야 추천을 반환했기 때문에,
"추천 순서가 현재 dependency를 만족하지 않으면 fallback"이라는 M72 요구
사항이 코드에서 발동할 수 없는 죽은 경로였다(추천이 존재하면 정의상 이미
현재 dependency와 일치).

**사용자 승인(AskUserQuestion, 1회)**: `_signature()`를 `task_ids`만으로
완화(권장안 채택) — 같은 Task 묶음이면 dependency가 바뀌어도(예: 새
의존관계 추가) 과거 추천을 우선 조회하되, `plan()`이 채택 전 현재
dependency를 실제로 만족하는지 검증하도록 확정했다.

**구현**:
- `src/ai_workspace/engines/workflow_engine.py`(`InMemoryWorkflowEngine`)
  — `_signature()`를 `(frozenset(task_ids), edges)`에서
  `frozenset(task_ids)`로 축소. `plan()`에 `_is_valid_order(order,
  workflow)` 검증(순열 일치 + 모든 dependency가 대상보다 앞섬)을 추가해,
  `recommended_order()`가 값을 반환하고 이 검증을 통과할 때만 채택하고,
  아니면(추천 없음 또는 dependency 위반) 기존 DFS 위상 정렬로 완전히
  동일하게 fallback.
- `src/ai_workspace/interfaces/workflow_engine.py` — `plan()`/
  `record_run_outcome()`/`recommended_order()` 시그니처는 무변경, docstring만
  갱신(추천은 "힌트"이고 dependency 정합성 검증은 `plan()`의 책임임을
  명시).
- `tests/engines/test_workflow_engine.py` — 2건 추가(추천 순서가 새
  dependency를 어기면 fallback, 여전히 dependency를 만족하면 그대로
  채택).
- `docs/ARCHITECTURE.md` §3.12 Workflow Runner 절에 Workflow Adaptive
  Planning(M72) 서술 추가, §7 인터페이스 표 `WorkflowEngine` 행 갱신.
  새 Core Domain Interface 없음(기존 `WorkflowEngine`의 메서드 3개 그대로,
  30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 기존 WorkflowEngine/WorkflowRunner 구조 재사용, 새 컴포넌트 없음 | ✅ |
| 2 | M71의 `WorkflowOrderStat`/`recommended_order()` 그대로 활용(수정 없음) | ✅ |
| 3 | `plan()`이 학습된 추천 순서를 먼저 조회하고 유효하면 사용 | ✅ |
| 4 | 추천 순서가 현재 dependency를 만족하지 않거나 없으면 기존 DFS 위상 정렬로 완전히 동일하게 fallback을 테스트로 증명 | ✅ |
| 5 | 추천은 "최적화 힌트"일 뿐 Workflow 정합성을 깨뜨리지 않음(dependency 위반 시 항상 fallback) | ✅ |
| 6 | 새 Core Domain Interface 없음(`WorkflowEngine` 계약 메서드 시그니처 무변경) | ✅ |
| 7 | 기존 API와 100% 하위 호환(학습 이력 없으면 M71 이전과 동일 동작) | ✅ |
| 8 | 넓은 "Workflow Adaptive Planning" 주제를 AskUserQuestion으로 구체 설계까지 좁힘 | ✅ |
| 9 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1319개(신규 2개, 회귀 없음)/`ruff`/`mypy`(233 source files)
전부 통과. ADR-0090.

---

## Milestone 73 — Workflow Cost Optimization: 동률 학습 순서를 M64 비용 정보로 tie-break (완료)

**배경**: 사용자가 "M72의 Adaptive Planning이 여러 유효한 실행 순서를
선택할 수 있는 경우, 가장 비용 효율적인 순서를 우선 선택"하는 M73을
요청했다. M72의 `recommended_order()`는 성공률이 동률인 복수 학습 순서를
표본 수 → 먼저 기록된 순서로만 tie-break했고, 비용은 전혀 고려하지
않았다. M64(ADR-0064) `EngineSelectionPolicy`(예산 내 최저 비용 Engine
선택)를 그대로 재사용하되 새 비용 정책은 만들지 않는 제약이었다.

**사용자 승인(AskUserQuestion, 2회)**:
1. 의존성 연결 방식 — **생성자 선택적 주입(권장안 채택)**:
   `InMemoryWorkflowEngine(*, task_engine=None, engine_registry=None,
   engine_selection_policy=None)`. `WorkflowEngine` 추상 메서드 시그니처는
   무변경, 기존 호출부 수정 불필요.
2. 비용 계산 의미 — **합산 방식 그대로 채택(권장안)**: order의 비용 =
   모든 task_id의 선택된 Engine `estimated_cost_usd` 합. `EngineSelectionPolicy.
   select()`가 순서를 모르는 순수함수라 같은 task_id 집합의 순열은 비용
   합이 항상 동일함(=실제로는 tie-break가 후보를 거의 좁히지 못함)을
   사용자에게 명시적으로 확인받고도, 계약상 올바르고 향후 순서-민감
   `EngineSelectionPolicy`에도 대비되는 정직한 구현을 그대로 채택했다.

**구현**:
- `src/ai_workspace/engines/workflow_engine.py`(`InMemoryWorkflowEngine`)
  — `__init__`에 `task_engine`/`engine_registry`/`engine_selection_policy`
  선택적 협력자 3개 추가(기본값 `None`). `recommended_order()`를
  재구성해 최고 성공률 동률 후보(`tied`)를 먼저 추출하고,
  `_break_tie_by_cost()`(세 협력자 모두 있고 비용 계산이 전부 성공할
  때만 최저 비용 후보로 좁힘, 하나라도 실패하면 즉시 원래 `tied` 그대로
  반환)를 거쳐, 최종적으로 기존과 동일한 `max(..., key=total)`(표본 수 →
  먼저 기록된 순서)로 선택한다. `_order_cost()`가 `TaskEngine.get_task()`
  → `EngineRegistry.list_candidates()` → `EngineSelectionPolicy.select()`
  체인으로 order 전체 비용을 합산한다.
- `src/ai_workspace/interfaces/workflow_engine.py` — 추상 메서드
  시그니처는 무변경, docstring만 M73 동작 명시.
- `tests/engines/test_workflow_engine.py` — 4건 추가(비용 의존성 미주입
  시 기존 tie-break 회귀 없음, 비용 계산 경로가 실제로 실행되지만 완전
  동률 결과는 불변, Task 조회 실패 시 fallback, 등록된 Engine 없어 후보가
  없을 때 fallback).
- `docs/ARCHITECTURE.md` §3.12 Workflow Runner 절에 Workflow Cost
  Optimization(M73) 서술 추가, §7 인터페이스 표 `WorkflowEngine` 행 갱신.
  새 Core Domain Interface 없음(기존 `WorkflowEngine`의 메서드 3개
  시그니처 그대로, 30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 기존 WorkflowEngine/WorkflowRunner/M71~M72 구현 재사용, 새 컴포넌트 없음 | ✅ |
| 2 | M64 `EngineSelectionPolicy`를 그대로 활용, 새 비용 정책 없음 | ✅ |
| 3 | 여러 실행 후보가 가능할 때 예상 비용이 낮은 순서를 우선 추천하는 로직 구현 | ✅ |
| 4 | 학습된 추천 순서가 있으면 그것을 우선 사용, 동일 성공률 후보가 여럿일 때만 비용을 tie-break로 사용 | ✅ |
| 5 | 비용 정보를 계산할 수 없으면(의존성 미주입/Task 조회 실패/후보 없음) 기존 동작으로 즉시 fallback을 테스트로 증명 | ✅ |
| 6 | 새 Core Domain Interface 없음(`WorkflowEngine` 계약 메서드 시그니처 무변경) | ✅ |
| 7 | 기존 API와 100% 하위 호환(비용 의존성 미주입 시 M72 이전과 동일 동작) | ✅ |
| 8 | 넓은 "Workflow Cost Optimization" 주제를 AskUserQuestion 2회로 구체 설계까지 좁힘 | ✅ |
| 9 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1323개(신규 4개, 회귀 없음)/`ruff`/`mypy`(233 source files)
전부 통과. ADR-0091.

---

## Milestone 74 — Provider Concurrency Management: 엔진별 동시 실행 상한 (완료)

**배경**: 사용자가 "여러 Agent가 동시에 동일 Provider(Claude/Codex/Gemini
등)를 선택할 때 Provider의 동시 실행 한계를 안전하게 관리"하는 M74를
요청했다. M64~M70이 쌓아온 선택 로직(비용/신뢰도/실행 이력/합의)은
"어떤 엔진이 더 나은가"만 판단했고, "그 엔진이 지금 몇 개나 동시에
실행 중인가"는 전혀 보지 않았음을 코드로 확인했다.

**사용자 승인(AskUserQuestion, 2회)**:
1. 적용 범위 — **`InMemoryEngineRuntime`과 `ManagedEngineRuntime` 둘 다
   구현(권장안 채택)**: M65~M70이 두 구현체를 항상 함께 확장해온 기존
   패턴과 일치.
2. 설정 API — **`register_engine()`에 선택적 keyword 추가(권장안
   채택)**: `register_engine(name, adapter, *, max_concurrency:
   int | None = None)`. M14의 `run()` `model` 파라미터 확장과 동일한
   패턴, 기존 호출부 수정 불필요.

**구현**:
- `src/ai_workspace/interfaces/engine_runtime.py` — `register_engine()`
  시그니처에 `max_concurrency` 선택적 keyword 추가, docstring 갱신(그
  외 계약 무변경).
- `src/ai_workspace/runtime/engine/engine_runtime.py`(`InMemoryEngineRuntime`)
  /`src/ai_workspace/runtime/engine/managed_engine_runtime.py`
  (`ManagedEngineRuntime`) — `_max_concurrency`/`_in_flight`(`threading.
  Lock` 보호) 신설. `_has_capacity()` 필터를 `_select()`/`_build_
  candidates()`(`_require_adapter()`)의 신뢰도 필터와 같은 자리에 추가해
  한도 도달 엔진을 후보에서 제외(capacity 있으면 기존과 동일 선택,
  없으면 자동 fallback, 전부 busy면 기존 `NoSuitableEngineError`).
  `_try_acquire()`/`_release()`(원자적 증감) + `_select_and_acquire()`/
  `_require_adapter_and_acquire()`(필터-스냅샷과 실제 획득 사이 경쟁
  처리, 획득 실패 시 제외하고 재선택)로 `run()`/`run_parallel()`을
  감싼다(`finally`로 정상/실패/예외/타임아웃 모든 경로에서 해제 보장).
  `run_ensemble()`/`run_ensemble_auto()`(M62/M68)는 여러 Provider를
  의도적으로 동시에 비교하는 기능이라 범위에서 제외(YAGNI).
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py` —
  `register_engine()`이 `max_concurrency`를 내부 Runtime에 위임하도록
  시그니처 갱신.
- `tests/interfaces/fakes.py`(`FakeEngineRuntime`) — `register_engine()`
  시그니처만 새 keyword를 수용하도록 갱신(로직은 그대로, YAGNI).
- `tests/runtime/engine/test_engine_runtime.py` — 재진입(reentrant)
  Adapter 기법(스레드 없이 결정적으로 "이미 사용 중" 상태 재현)으로
  신규 테스트 6건(capacity 있으면 기존과 동일 선택, capacity 도달 시
  자동 fallback, 전부 busy면 기존 예외, 해제 후 재사용 가능, 비용 기반
  선택 경로에서도 필터 적용).
- `tests/runtime/engine/test_managed_engine_runtime.py` — `ThreadPoolExecutor`
  기반 실제 동시성 신규 테스트 3건(fallback, 여유 있을 때 회귀 없음,
  전부 busy 시 개별 Task 실패 격리 — M10-T01/T02 원칙 재확인), 5회
  연속 실행으로 타이밍 안정성 확인.
- `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에 Provider Concurrency
  Management(M74) 서술 추가, §7 인터페이스 표 `EngineRuntime` 행 갱신.
  새 Core Domain Interface 없음(기존 `EngineRuntime`의 메서드 시그니처
  1개만 확장, 30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 기존 EngineRuntime/EngineRegistry/EngineSelectionPolicy 구조 재사용, 새 컴포넌트 없음 | ✅ |
| 2 | Provider별 max_concurrency를 선택적으로 지원 | ✅ |
| 3 | Provider가 여유(capacity)가 있으면 기존과 동일하게 선택함을 테스트로 증명 | ✅ |
| 4 | Provider가 capacity에 도달하면 다른 후보 Engine으로 자동 fallback함을 테스트로 증명(InMemory 재진입 테스트 + Managed 실제 스레드 테스트) | ✅ |
| 5 | 모든 Provider가 busy이면 기존 예외 처리 정책(NoSuitableEngineError)을 그대로 따름을 테스트로 증명 | ✅ |
| 6 | 동시 실행 카운트는 EngineRuntime 내부 in-process 상태로만 관리(영속화 없음) | ✅ |
| 7 | 새 Core Domain Interface 없음(EngineRuntime 계약은 register_engine() 선택적 확장 1개뿐) | ✅ |
| 8 | 기존 API와 100% 하위 호환(max_concurrency 미지정 시 M74 이전과 동일 동작) | ✅ |
| 9 | 넓은 "Provider Concurrency Management" 주제를 AskUserQuestion 2회로 구체 설계까지 좁힘 | ✅ |
| 10 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1331개(신규 8개, 회귀 없음)/`ruff`/`mypy`(233 source files)
전부 통과. ADR-0092.

---

## Milestone 75 — Diversity Routing: 동률 후보의 Provider 분산 tie-break (완료)

**배경**: 사용자가 "여러 Agent가 병렬 실행될 때 동일 Provider/Model에
불필요하게 집중되지 않도록 다양성을 고려한 Engine 선택을 지원"하는
M75를 요청했다. 최신 main(M74/ADR-0092까지 반영, PR #83 병합 확인) 기준
으로 시작해 조사한 결과, M64~M74가 쌓아온 선택 로직은 전부 "어떤
엔진이 더 나은가"/"지금 쓸 수 있는가"만 판단했고, 비용·성공률이 완전히
동률인 후보 여럿이 등록 순서상 첫 번째로만 계속 몰리는 문제(M74의
capacity 여유를 낭비)가 코드로 확인됐다.

**사용자 승인(AskUserQuestion, 2회)**:
1. 다양성 신호 — **M74 `_in_flight`(현재 동시 실행 중인 세션 수) 재사용
   (권장안 채택)**: 새 카운터 없이 "지금 가장 한가한 Provider"를 그대로
   활용, 요구사항의 "기존 구조 재사용"/"상태는 in-process로만 관리"에
   정확히 부합.
2. 범위(Provider vs Model) — **Provider(engine_name) 수준만(권장안
   채택)**: `EngineCandidate`에 `model` 필드가 없고 M14(ADR-0026)가
   이미 "Model은 엔진 선택에 관여하지 않는다"고 확정해둔 경계를 다시
   열지 않는다.

**구현**:
- `src/ai_workspace/runtime/engine/engine_runtime.py`(`InMemoryEngineRuntime`)
  /`src/ai_workspace/runtime/engine/managed_engine_runtime.py`
  (`ManagedEngineRuntime`) — `_reorder_by_diversity(candidates)` 신설
  (`_in_flight` 오름차순 안정 정렬). `_build_candidates()`에서 M74
  capacity 필터링 이후, `_reorder_by_execution_memory()`(M69) 적용
  **직전**에 배치해 정렬 안정성만으로 "비용·성공률 완전 동률일 때만
  개입"을 보장(새 조건문 없음). `engine_selection_policy` 미주입 경로/
  `run_ensemble()`/`run_ensemble_auto()`는 M74와 동일한 이유로 범위 밖
  (YAGNI).
- `EngineRuntime`(interface) 계약은 전혀 무변경 — 새 메서드/파라미터
  없음, private 메서드 추가와 `_build_candidates()` 내부 배선 한 줄뿐.
- `tests/runtime/engine/test_engine_runtime.py` — 실제 스레드
  (`threading.Thread`) 기반 신규 테스트 4건(완전 동률 시 한가한
  Provider 우선, 비용 우선순위 불변, 실행 이력 성공률 우선순위 불변,
  정책 미주입 시 회귀 없음).
- `tests/runtime/engine/test_managed_engine_runtime.py` — `ThreadPoolExecutor`
  기반 실제 병렬 신규 테스트 2건(동률 시 분산, 비용 우선순위 불변),
  5회 연속 실행으로 타이밍 안정성 확인.
- `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에 Diversity Routing
  (M75) 서술 추가, §7 인터페이스 표 `EngineRuntime` 행 갱신. 새 Core
  Domain Interface 없음(기존 `EngineRuntime` 계약 완전 무변경, 30종
  유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작, 기존 ADR/TASKS/ROADMAP·구현 상태를 먼저 조사 | ✅ |
| 2 | 기존 EngineSelectionPolicy/EngineRuntime/Provider Capacity(M74) 구조 재사용, 새 컴포넌트 없음 | ✅ |
| 3 | M74 capacity 검사 이후에만 Diversity Routing 적용 | ✅ |
| 4 | 동일 성능(비용·신뢰도) 후보가 여러 개일 때만 다양성을 tie-break로 사용함을 테스트로 증명 | ✅ |
| 5 | 비용·신뢰도 우선순위를 절대 변경하지 않음을 테스트로 증명(정렬 안정성으로 구조적 보장) | ✅ |
| 6 | Diversity가 기존 선택 결과를 강제로 바꾸지 않는 "선택적 최적화"임을 확인(완전 동률에서만 개입) | ✅ |
| 7 | 새 Core Domain Interface 없음(EngineRuntime 계약 완전 무변경) | ✅ |
| 8 | 기존 API와 100% 하위 호환(engine_selection_policy 미주입 시 M75 이전과 동일 동작) | ✅ |
| 9 | 상태는 EngineRuntime 내부 in-process로만 관리(M74 `_in_flight` 재사용, 영속화 없음) | ✅ |
| 10 | 넓은 "Diversity Routing" 주제를 AskUserQuestion 2회로 구체 설계까지 좁힘 | ✅ |
| 11 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1337개(신규 6개, 회귀 없음)/`ruff`/`mypy`(233 source files)
전부 통과. ADR-0093.

---

## Milestone 76 — Adaptive Load Balancing: 상대 부하율 기반 tie-break 개선 (완료)

**배경**: 사용자가 "M74(Provider Concurrency)와 M75(Diversity Routing)를
기반으로 현재 Provider의 실시간 부하를 고려하여 Engine을 자동 분산
선택"하는 M76을 요청했다. 최신 main(M75/ADR-0093까지 반영) 기준으로
시작해 조사한 결과, M75가 이미 "비용·신뢰도·capacity 동률일 때 M74
`_in_flight`가 가장 적은 Provider를 tie-break로 선택"하는 로직을
구현·병합해 M76 요구사항과 거의 동일했다. 다만 M75는 raw `_in_flight`
**개수**만 비교해, Provider마다 `max_concurrency` 한도가 다르면 실제
여유를 거꾸로 판단하는 문제가 있었다.

**사용자 승인(AskUserQuestion, 2회)**:
1. M76 차별점 — **상대 부하율(`in_flight/max_concurrency`)로 개선
   (권장안 채택)**: raw 개수 대신 비율로 계산해 Provider마다 한도가
   다를 때 실제 여유를 정확히 반영.
2. 무제한 엔진 처리 — **부하율 0으로 간주(권장안 채택)**: 실제 동시
   실행 상한이 없어 병목 위험이 없다는 사실을 그대로 반영.
3. (구현 중 회귀 발견 후 재질의) 무제한 엔진끼리 부하율이 항상 0.0으로
   동률이 되어 M75의 "무제한 엔진 간 분산" 동작이 사라지는 문제 —
   **부하율이 동률이면 raw `_in_flight`로 2차 tie-break(권장안 채택)**.

**구현**:
- `src/ai_workspace/runtime/engine/engine_runtime.py`(`InMemoryEngineRuntime`)
  /`src/ai_workspace/runtime/engine/managed_engine_runtime.py`
  (`ManagedEngineRuntime`) — `_load_ratio(name)`(= `_in_flight /
  max_concurrency`, 무제한이면 0.0) 및 `_load_rank(candidate)`(=
  `(load_ratio, in_flight)` 튜플, read-only) 신설. `_reorder_by_
  diversity()`의 정렬 키를 raw `_in_flight` 개수에서 `_load_rank()`로
  교체 — 호출 위치(M74 capacity 필터링 이후, `_reorder_by_execution_
  memory()` 이전)·정렬 안정성·tie-break 전용 범위는 M75와 완전히 동일.
- `EngineRuntime`(interface) 계약은 전혀 무변경 — 새 메서드/파라미터
  없음, private 메서드 추가와 정렬 키 교체뿐.
- `tests/runtime/engine/test_engine_runtime.py`/`tests/runtime/engine/
  test_managed_engine_runtime.py` — 서로 다른 `max_concurrency`를 가진
  두 엔진에 서로 다른 개수의 동시 실행을 재현해 상대 부하율이 raw
  in-flight 개수보다 우선함을 증명하는 신규 테스트 각 1건, M75의
  기존 6개 다양성 테스트가 회귀 없이 통과함을 확인, 5회 연속 실행으로
  타이밍 안정성 확인.
- `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에 Adaptive Load
  Balancing(M76) 서술 추가, §7 인터페이스 표 `EngineRuntime` 행 갱신.
  새 Core Domain Interface 없음(기존 `EngineRuntime` 계약 완전 무변경,
  30종 유지).

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작, 기존 ADR/TASKS/ROADMAP·구현 상태를 먼저 조사 | ✅ |
| 2 | 기존 EngineRuntime/EngineSelectionPolicy/Provider Concurrency(M74)/Diversity Routing(M75) 구조 재사용, 새 컴포넌트 없음 | ✅ |
| 3 | Provider별 active execution 수(M74 `_in_flight`)로 현재 부하를 계산 | ✅ |
| 4 | 비용·신뢰도·Capacity가 동일한 후보일 때만 가장 부하가 낮은 Provider를 우선 선택함을 테스트로 증명 | ✅ |
| 5 | 부하는 tie-break 용도로만 사용, 기존 비용·신뢰도 정책 불변임을 테스트로 증명(정렬 안정성으로 구조적 보장) | ✅ |
| 6 | 상태는 EngineRuntime 내부 in-process로만 관리(M74 상태 재사용, 영속화 없음) | ✅ |
| 7 | 새로운 Core Domain Interface 없음(EngineRuntime 계약 완전 무변경) | ✅ |
| 8 | 기존 API와 100% 하위 호환(engine_selection_policy 미주입 시 이전과 동일 동작) | ✅ |
| 9 | 넓은 "Adaptive Load Balancing" 주제를 AskUserQuestion 2회(+구현 중 회귀 발견에 따른 재질의 1회)로 구체 설계까지 좁힘 | ✅ |
| 10 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트(M75 포함) 회귀 없음 | ✅ |

`pytest` 1339개(신규 2개, 회귀 없음)/`ruff`/`mypy`(233 source files)
전부 통과. ADR-0094.

---

## Milestone 77 — Engine Benchmark & Capability Profiling: Provider별 성능 프로파일 조회 (완료)

**배경**: 사용자가 "M65~M76에서 축적된 실행 결과를 바탕으로 Provider/Model별
객관적인 성능 프로파일을 생성하여 이후 Routing의 근거 데이터로 활용"하는
M77을 요청했다. 최신 main(M76/ADR-0094까지 반영) 기준으로 조사한 결과,
M65(`EngineReliabilityStat`)/M69(`EngineExecutionMemoryStat`)가 이미
필요한 원시 데이터를 in-process로 누적하고 있었지만, 이를 하나의
"Benchmark Profile"로 합쳐 조회하는 public API는 없었다.

**사용자 승인(AskUserQuestion, 2회)**:
1. Model 차원 — **Provider(engine_name) 수준만(권장안 채택)**: 어떤
   기존 통계도 model을 키로 쓰지 않고, M14(ADR-0026)/M75가 이미 같은
   이유로 Provider 수준으로 범위를 좁힌 선례를 그대로 따른다.
2. Latency 집계 범위 — **Execution Count/Success/Failure는
   `EngineReliabilityStat`(모든 실행 경로), Latency는
   `EngineExecutionMemoryStat` 집계(기록된 경로만, 표본 부족 시 None)
   (권장안 채택)**: `run_parallel()`/`run_ensemble()`은 latency를
   기록하지 않는다는 점을 코드로 확인 후 결정.

**구현**:
- `src/ai_workspace/domain/engine_benchmark.py` — `EngineBenchmarkProfile`
  (frozen dataclass) 신설. `execution_count`/`success_count`/
  `failure_count`(M65), `latency_sample_count`/`total_latency_seconds`
  (M69, `engine_name`으로 필터링해 합산)를 보관하고 `success_rate()`/
  `failure_rate()`/`average_latency_seconds()`를 계산(표본 0이면 `None`).
- `src/ai_workspace/interfaces/engine_runtime.py` — `benchmark_profile
  (engine_name)` 추상 메서드 신설(M70 `consensus_weight()`와 동일한
  방식의 계약 확장, 새 Core Domain Interface 아님). 미기록이어도 예외
  없이 0 카운트 프로필 반환.
- `src/ai_workspace/runtime/engine/engine_runtime.py`/
  `managed_engine_runtime.py` — `_engine_reliability`/`_execution_memory`
  를 새 상태 없이 읽기 전용으로 조합해 구현. Routing 로직(`_select()`/
  `_build_candidates()`/`_reorder_by_diversity()`/`_reorder_by_execution_
  memory()`)은 전혀 수정하지 않음.
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py` — 내부
  Runtime에 위임.
- 테스트 대역 4곳(`tests/interfaces/fakes.py` `FakeEngineRuntime`,
  `tests/agents/test_coding_agent.py` `RecordingEngineRuntime`,
  `tests/core/test_workspace_core.py` `SpyEngineRuntime`,
  `tests/runtime/engine/test_recovering_engine_runtime.py`
  `ScriptedEngineRuntime`)에 계약 준수 최소 구현 추가.
- `tests/domain/test_engine_benchmark.py`(도메인 단위 테스트 4건),
  `tests/runtime/engine/test_engine_runtime.py`(신규 4건: 미기록 시
  빈 프로필/reliability+execution memory 집계/여러 capability 조합
  합산/Routing 결과 불변 증명), `tests/runtime/engine/
  test_managed_engine_runtime.py`(신규 2건: latency 기록 경로와
  미기록 경로가 섞였을 때 count와 latency 표본 수가 다름을 증명/
  미실행 엔진 빈 프로필) 추가.
- `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에 Engine Benchmark &
  Capability Profiling(M77) 서술 추가, §7 인터페이스 표 `EngineRuntime`
  행 갱신.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작, 기존 ADR/TASKS/ROADMAP·구현 상태를 먼저 조사 | ✅ |
| 2 | 기존 EngineRuntime/EngineSelectionPolicy/Learning/Statistics(M65/M69) 구조 재사용 | ✅ |
| 3 | Provider별 Success Rate/Failure Rate/Average Latency/Execution Count를 하나의 Benchmark Profile로 관리 | ✅ |
| 4 | Routing 로직 무변경, Benchmark 정보만 생성·조회 가능함을 테스트로 증명 | ✅ |
| 5 | M65~M76 기록 데이터 재사용, 새로운 측정 시스템 없음(새 record 지점 추가 없음) | ✅ |
| 6 | 새로운 Core Domain Interface 없음(EngineRuntime 계약 확장만, M70과 동일 방식) | ✅ |
| 7 | 상태는 EngineRuntime 내부 in-process로만 관리, 영속화 없음 | ✅ |
| 8 | 기존 API와 100% 하위 호환(YAGNI) | ✅ |
| 9 | 넓은 "Engine Benchmark & Capability Profiling" 주제를 AskUserQuestion 2회로 구체 설계까지 좁힘 | ✅ |
| 10 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1349개(신규 10개, 회귀 없음)/`ruff`/`mypy`(234 source files)
전부 통과. ADR-0095.

---

## Milestone 78 — Adaptive Engine Benchmark Routing: Benchmark Profile을 Routing tie-break에 반영 (완료)

**배경**: 사용자가 "M77에서 생성한 Provider/Model Benchmark Profile을
실제 Engine 선택(Routing)에 안전하게 반영"하는 M78을 요청했다. 최신
main(M77/ADR-0095까지 반영) 기준으로 조사한 결과, M77 `benchmark_profile()`
은 순수 조회 전용이라 Routing 파이프라인 어디에도 반영되지 않고 있었다.
M69 `_reorder_by_execution_memory()`가 이미 같은 목적(성공률 기반
tie-break)의 더 좁은 범위 신호를 최우선으로 쓰고 있었다.

**사용자 승인(AskUserQuestion, 3회)**:
1. 파이프라인 내 위치 — **`_reorder_by_execution_memory()`와
   `_reorder_by_diversity()` 사이(권장안 채택)**: M69의 정밀한 신호가
   최우선을 유지하고, M78 Benchmark(Provider 전체 누적)는 M69가 표본
   부족이거나 동률일 때만 개입, M75/76 부하보다는 우선한다.
2. 지표 결합 방식 — **성공률 우선, 레이턴시로 2차 tie-break(권장안
   채택)**: `failure_rate()`는 `success_rate()`의 보완값이라 별도 사용
   안 함. 정렬 키는 `(-success_rate, average_latency_seconds)`.
3. 표본 부족 기준 — **`execution_count < 3`이면 중립값 처리(권장안
   채택)**: M69/M65가 이미 쓰는 "표본 3건 미만 판정 보류" 규칙을 그대로
   재사용(새 임계치 발명 안 함). 성공률은 `_NEUTRAL_RATE`(0.5), 레이턴시는
   `math.inf`로 대체해 기존 순서(diversity 결과)를 그대로 보존한다.

**구현**:
- `src/ai_workspace/runtime/engine/engine_runtime.py`/
  `managed_engine_runtime.py` — `_MIN_BENCHMARK_SAMPLES = 3` 상수,
  `_benchmark_rank(candidate) -> tuple[float, float]`(M77
  `benchmark_profile()`을 읽어 `(-success_rate, average_latency_seconds)`
  키 생성, 표본 부족 시 `(-_NEUTRAL_RATE, math.inf)`), `_reorder_by_
  benchmark(candidates)` 신설.
- `_build_candidates()`에서 `_reorder_by_diversity()` 다음·`_reorder_by_
  execution_memory()` 이전에 `_reorder_by_benchmark()`를 삽입 — 안정
  정렬 특성상 최종 우선순위는 cost > execution_memory(M69) >
  benchmark(M78) > diversity(M75/76)가 되며, 기존 우선순위는 전혀
  바뀌지 않는다.
- `EngineRuntime`(interface)·`benchmark_profile()` 계약은 무변경 — 두
  구현체의 내부 private 메서드만 추가.
- `tests/runtime/engine/test_engine_runtime.py`(신규 4건: Benchmark가
  execution_memory 동률 시 성공률 높은 엔진 우선/execution_memory
  우선순위를 절대 뒤집지 않음/표본 부족 시 diversity로 fallback/정책
  미주입 시 미관여), `tests/runtime/engine/test_managed_engine_runtime.py`
  (동일 시나리오 3건 + 테스트 전용 `FailableCostedSlowEngineAdapter`
  추가) 추가.
- `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에 Adaptive Engine
  Benchmark Routing(M78) 서술 추가, §7 인터페이스 표 `EngineRuntime`
  행 갱신.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작, 기존 ADR/TASKS/ROADMAP·구현 상태를 먼저 조사 | ✅ |
| 2 | 기존 EngineSelectionPolicy/EngineRuntime/Benchmark Profile(M77) 구조 재사용 | ✅ |
| 3 | Benchmark의 Success Rate/Failure Rate/Average Latency로 후보 재정렬 | ✅ |
| 4 | 비용 1순위, Benchmark는 동일 비용 후보에 대한 tie-break로만 사용(execution_memory보다 낮은 우선순위) | ✅ |
| 5 | 표본 3건 미만/데이터 없으면 즉시 기존 Routing으로 fallback(중립값 처리) | ✅ |
| 6 | 새로운 Core Domain Interface 없음(EngineRuntime 계약 무변경, 내부 private 메서드만 추가) | ✅ |
| 7 | 상태는 EngineRuntime 내부 in-process로만 관리, 영속화 없음(M77 상태 재사용, 새 상태 없음) | ✅ |
| 8 | 기존 API와 100% 하위 호환(YAGNI) | ✅ |
| 9 | 파이프라인 위치·지표 결합 방식·표본 부족 기준을 AskUserQuestion 3회로 확정 | ✅ |
| 10 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1356개(신규 7개, 회귀 없음)/`ruff`/`mypy`(234 source files)
전부 통과. ADR-0096.

---

## Milestone 79 — Adaptive Engine Recommendation: 실행 없는 Engine 추천 API (완료)

**배경**: 사용자가 "M65~M78에서 축적된 Learning, Benchmark, Routing
정보를 종합하여 현재 Task에 가장 적합한 Provider/Model(또는 Ensemble)을
추천하는 Recommendation Layer"를 요청했다(M79). 최신 main(M78/ADR-0096
까지 반영) 기준으로 조사한 결과, `_build_candidates()`/
`EngineSelectionPolicy.select()`가 이미 "Task에 가장 적합한 Provider"
판단에 필요한 신호(M64 비용/M65 신뢰도/M69 실행 메모리/M77 Benchmark/
M78 tie-break)를 전부 갖추고 있었지만, 실행(`run()`)하지 않고 그
판단만 조회하는 API가 없었다.

**사용자 승인(AskUserQuestion, 3회)**:
1. 추가 위치 — **`EngineRuntime`에 `recommend_engine()` 신규 public
   메서드(권장안 채택)**: M70/M77과 동일한 방식으로 기존 계약을
   확장한다.
2. "Workflow Learning" 근거 범위 — **EngineRuntime이 이미 추적 중인
   M69 실행 메모리(성공률)를 "학습된 근거"로 그대로 재사용(권장안
   채택)**: M71 `WorkflowEngine.recommended_order()`는 Task 순서
   학습이지 Engine 선택과 무관한 별개 계약이고, M70/ADR-0088의 결합
   금지 원칙을 재확인해 `WorkflowEngine`을 직접 참조하지 않는다.
3. 추천 결과 구조 — **단일 `engine_name` + 근거 dict(`evidence`) +
   신뢰도 플래그(`confident`), `top_n`으로 여러 개 조회(권장안
   채택)**.

**구현**:
- `src/ai_workspace/domain/engine_recommendation.py`(신규) —
  `EngineRecommendation`(frozen dataclass: `engine_name`/`reason`/
  `evidence: dict[str, float | None]`/`confident: bool`).
- `src/ai_workspace/interfaces/engine_runtime.py` — `recommend_engine
  (task, required_capabilities=frozenset(), *, top_n=1) -> list[
  EngineRecommendation]` 추상 메서드 신설(M70/M77과 동일한 방식의 계약
  확장, 새 Core Domain Interface 아님). 후보가 없으면 예외 없이 빈
  목록 반환(`run()`과 달리 `NoSuitableEngineError` 없음).
- `src/ai_workspace/runtime/engine/engine_runtime.py`/
  `managed_engine_runtime.py` — `_build_recommendation()`/
  `recommend_engine()` 구현. `_build_candidates()`/`EngineSelectionPolicy.
  select()`를 `estimate_cost()`와 동일한 read-only 경로로 반복 호출해
  (`_select_top_n()`과 같은 패턴) `run()`을 호출하지 않고 추천만
  만든다. 근거는 M65(`reliability_success_rate`)/M69(`execution_memory_
  success_rate`/`latency_seconds`, 이번 capability 조합 전용)/M77
  (`benchmark_success_rate`/`benchmark_average_latency_seconds`)을 조합.
  둘 다 표본 부족(3건 미만)이면 `confident=False`. 정책 미주입 시(첫
  매칭 경로) `run()`이 고를 엔진과 같은 엔진을 `confident=False`로 반환.
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py` — 내부
  Runtime에 위임.
- 테스트 대역 4곳(`tests/interfaces/fakes.py` `FakeEngineRuntime`,
  `tests/agents/test_coding_agent.py` `RecordingEngineRuntime`,
  `tests/core/test_workspace_core.py` `SpyEngineRuntime`,
  `tests/runtime/engine/test_recovering_engine_runtime.py`
  `ScriptedEngineRuntime`)에 계약 준수 최소 구현 추가.
- `tests/runtime/engine/test_engine_runtime.py`(신규 5건: 표본 충분 시
  confident=True+run() 결과와 동일 엔진/표본 부족 시 confident=False/
  top_n 비용순 정렬/top_n<1 시 빈 목록/정책 미주입 시 첫 매칭과 동일
  엔진+confident=False), `tests/runtime/engine/
  test_managed_engine_runtime.py`(동일 시나리오 3건) 추가.
- `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에 Adaptive Engine
  Recommendation(M79) 서술 추가, §7 인터페이스 표 `EngineRuntime`
  행 갱신.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작, 기존 ADR/TASKS/ROADMAP·구현 상태를 먼저 조사 | ✅ |
| 2 | 기존 EngineSelectionPolicy/EngineRuntime/Benchmark Profile(M77)/Adaptive Benchmark Routing(M78)/Learning 구조 재사용 | ✅ |
| 3 | Recommendation은 실행을 강제하지 않고 추천만 제공(run() 미호출) | ✅ |
| 4 | 추천 근거로 Cost/Reliability/Latency/Benchmark/Workflow Learning(M69 재해석)을 함께 사용 | ✅ |
| 5 | Recommendation 없음/근거 부족 시 기존 Routing 결과를 그대로 사용(confident=False로 명시, run()과 동일 엔진 반환) | ✅ |
| 6 | 새로운 Core Domain Interface 없음(EngineRuntime 계약 확장만, M70/M77과 동일 방식) | ✅ |
| 7 | 상태는 EngineRuntime 내부 in-process로만 관리, 영속화 없음(M65/M69/M77 상태 재사용, 새 상태 없음) | ✅ |
| 8 | 기존 API와 100% 하위 호환(YAGNI) | ✅ |
| 9 | 추가 위치·Learning 신호 범위·추천 결과 구조를 AskUserQuestion 3회로 확정 | ✅ |
| 10 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1364개(신규 8개, 회귀 없음)/`ruff`/`mypy`(235 source files)
전부 통과. ADR-0097.

---

## Milestone 80 — Autonomous Decision Engine: 추천을 최종 실행 결정으로 통합 (완료)

**배경**: 사용자가 "M65~M79에서 구현된 Learning, Benchmark, Workflow
Learning, Routing, Recommendation을 하나의 의사결정 계층으로 통합하여
실행 직전 최적의 Provider/Model을 자동 결정하는 Autonomous Decision
Engine"을 요청했다(M80). 최신 main(M79/ADR-0097까지 반영) 기준으로
조사한 결과, M79 `recommend_engine()`이 이미 모든 신호를 통합한 "1순위
후보"를 계산하고 있었지만 이를 "결정"으로 표현하는 API가 없었다.

**사용자 승인(AskUserQuestion, 3회)**:
1. 추가 위치/반환 타입 — **`EngineRuntime.decide_engine()` + 기존
   `EngineSelectionDecision`(M17) 재사용(권장안 채택)**: 새 domain
   타입을 만들지 않는다.
2. 실행 경로 결합 — **기존 `_select()` 무수정, `decide_engine()`은
   `recommend_engine()`을 재사용하는 병렬 조회 API(권장안 채택)**:
   `decide_engine()`의 engine_name은 `recommend_engine()`의 1순위(동일
   파이프라인 결과)를 그대로 쓰므로 `run()`이 실제로 고를 엔진과
   수학적으로 항상 같다.
3. Ensemble 범위 — **단일 결정만(top_n 미지원)(권장안 채택)**: Ensemble
   조합 결정은 `run_ensemble_auto()`(M68)가 이미 담당한다.

**구현**:
- `src/ai_workspace/interfaces/engine_runtime.py` — `decide_engine
  (task, required_capabilities=frozenset()) -> EngineSelectionDecision`
  추상 메서드 신설(M70/M77/M78/M79와 동일한 방식의 계약 확장, 새 domain
  타입 없음).
- `src/ai_workspace/runtime/engine/engine_runtime.py`/
  `managed_engine_runtime.py` — `recommend_engine()`(M79)의 1순위를
  `EngineSelectionDecision`에 그대로 담아 반환. 추천이 없으면 `_select()`/
  `_require_adapter()`를 그대로 호출해 `run()`과 동일한
  `NoSuitableEngineError`를 낸다.
- **부수 버그 수정**: `recommend_engine()`(M79)의 `engine_selection_
  policy` 미주입 경로가 `_has_capacity()`(M74)를 확인하지 않아 `_select()`
  와 다른(capacity가 꽉 찬) 엔진을 추천할 수 있던 불일치를 발견, 필터를
  추가해 바로잡았다 — `decide_engine()`의 "항상 run()과 같은 엔진" 보장에
  필요.
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py` — 내부
  Runtime에 위임.
- 테스트 대역 4곳에 계약 준수 최소 구현 추가.
- `tests/runtime/engine/test_engine_runtime.py`(신규 6건: capacity
  버그 수정 검증/정책 주입 시 run()과 동일 엔진/confident별 reason/
  정책 미주입 시 fallback/후보 없을 때 예외), `tests/runtime/engine/
  test_managed_engine_runtime.py`(동일 시나리오 5건) 추가.
- `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에 Autonomous Decision
  Engine(M80) 서술 추가, §7 인터페이스 표 `EngineRuntime` 행 갱신.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작, 기존 ADR/TASKS/ROADMAP·구현 상태를 먼저 조사 | ✅ |
| 2 | 기존 EngineSelectionPolicy/EngineRuntime/Recommendation(M79)/Benchmark(M77)/Workflow Learning/Adaptive Routing 재사용 | ✅ |
| 3 | AutonomousDecisionEngine은 Recommendation 결과를 종합하는 오케스트레이션 계층으로만 동작(새 실행 경로 없음) | ✅ |
| 4 | 새 알고리즘 없이 기존 Cost/Reliability/Benchmark/Workflow Learning/Diversity/Load Balancing 결과를 순차 통합(recommend_engine() 1순위 재사용) | ✅ |
| 5 | Recommendation 없음/근거 부족 시 기존 EngineSelectionPolicy로 즉시 fallback(예외 정책까지 일치) | ✅ |
| 6 | 새로운 Core Domain Interface 없음(EngineRuntime 계약 확장만, 새 domain 타입 없음) | ✅ |
| 7 | 상태는 EngineRuntime 내부 in-process로만 관리, 영속화 없음(M65/M69/M77/M79 상태 재사용) | ✅ |
| 8 | 기존 API와 100% 하위 호환(YAGNI) | ✅ |
| 9 | 추가 위치·실행 경로 결합 방식·Ensemble 범위를 AskUserQuestion 3회로 확정 | ✅ |
| 10 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1373개(신규 9개, 회귀 없음)/`ruff`/`mypy`(235 source files)
전부 통과. ADR-0098.

---

## Milestone 81 — Workspace Reflection & Continuous Improvement: Decision을 사후 평가하는 Reflection 계층 (완료)

**배경**: 사용자가 "M80 Autonomous Decision Engine이 내린 실행 결과를
사후 평가(Reflection)하여 다음 실행에서 더 나은 의사결정을 할 수 있도록
Continuous Improvement 계층을 추가"하는 M81을 요청했다. 최신 main(M80/
ADR-0098까지 반영) 기준으로 조사한 결과, `_build_recommendation()`(M79)이
실행 *전* 근거(evidence)를 계산하는 로직은 있었지만, `run()` 실행이 끝난
뒤 그 근거가 실제 결과와 얼마나 맞았는지 비교·기록하는 계층은 없었다.

**사용자 승인(AskUserQuestion, 4회)**:
1. 적용 범위 — **`run()`만(권장안 채택)**: M80 `decide_engine()`이
   "단일 결정만" 범위로 한정한 것과 동일. `run_parallel()`/
   `run_ensemble()`/`run_ensemble_auto()`는 범위 밖(YAGNI).
2. "예상"의 정의 — **evidence 전체 스냅샷(권장안 채택)**:
   `_build_recommendation()`/`recommend_engine()`(M79)의 evidence dict
   구조를 그대로 재사용해, 실행 직전(이번 실행 자체가 통계에 반영되기
   전) 스냅샷한다.
3. 보관 정책 — **엔진별 최근 20개만(권장안 채택)**: 영속화 없음, 엔진별
   `deque(maxlen=20)`로 무제한 메모리 증가를 방지한다.
4. 참고 정보 반영 방식 — **`reason` 텍스트에 문구 추가(권장안 채택)**:
   `evidence`/`confident`/순위(Routing 결과)는 전혀 바뀌지 않는다.

**구현**:
- `src/ai_workspace/domain/reflection.py` 신설 — `ReflectionReport`
  (frozen dataclass: `engine_name`/`expected_evidence`/`expected_
  confident`/`expected_success_rate`/`expected_latency_seconds`/
  `actual_success`/`actual_latency_seconds`/`expectation_matched`/
  `latency_gap_seconds`).
- `src/ai_workspace/interfaces/engine_runtime.py` — `reflection_reports
  (engine_name: str | None = None) -> list[ReflectionReport]` 추상
  메서드 신설(M70/M77/M79/M80과 동일한 방식의 계약 확장).
- `src/ai_workspace/runtime/engine/engine_runtime.py`/
  `managed_engine_runtime.py` — `_build_recommendation()`의 evidence
  계산을 `_evidence_snapshot()`(신규 private 헬퍼)로 공유·재사용.
  `run()`이 엔진을 선택·실행하기 직전 이 스냅샷을 캡처해, 실행 후
  `_record_reflection()`이 실제 결과와 비교해 `ReflectionReport`를
  엔진별 `deque(maxlen=20)`에 추가. `_build_recommendation()`의
  `reason`에 `_reflection_note()`(최근 불일치 횟수 참고 문구)를 덧붙임
  — `evidence`/`confident`/순위는 무변경.
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py` — 내부
  Runtime에 위임.
- 테스트 대역 4곳에 계약 준수 최소 구현 추가.
- `tests/runtime/engine/test_engine_runtime.py`(신규 6건), `tests/
  runtime/engine/test_managed_engine_runtime.py`(동일 시나리오 5건)
  추가.
- `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에 Workspace Reflection
  & Continuous Improvement(M81) 서술 추가, §7 인터페이스 표
  `EngineRuntime` 행 갱신.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작, 기존 ADR/TASKS/ROADMAP·구현 상태를 먼저 조사 | ✅ |
| 2 | 기존 AutonomousDecisionEngine(M80)/Recommendation/Workflow Learning/Benchmark/Learning 구조 최대 재사용 | ✅ |
| 3 | 실행 종료 후 Decision → Outcome을 비교해 ReflectionReport 생성 | ✅ |
| 4 | Reflection은 "예상과 실제의 차이"만 기록하며 즉시 Routing 정책을 변경하지 않음 | ✅ |
| 5 | Reflection 결과는 다음 Recommendation/Learning에서 참고 정보로만 활용(reason 문구, evidence/confident/순위 무변경) | ✅ |
| 6 | 새로운 Core Domain Interface 없음(EngineRuntime 계약 확장만) | ✅ |
| 7 | 상태는 EngineRuntime 내부 in-process로만 관리, 영속화 제외(엔진별 최근 20건 ring buffer) | ✅ |
| 8 | 기존 API와 100% 하위 호환(YAGNI) | ✅ |
| 9 | 적용 범위·예상 정의·보관 정책·참고 정보 반영 방식을 AskUserQuestion 4회로 확정 | ✅ |
| 10 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1384개(신규 11개, 회귀 없음)/`ruff`/`mypy`(236 source files)
전부 통과. ADR-0099.

---

## Milestone 82 — Goal-Aware Decision Policy: Cost/Quality/Latency 우선순위를 조정하는 Policy 계층 (완료)

**배경**: 사용자가 "M80 Autonomous Decision Engine이 모든 Task를 동일한
기준으로 처리하지 않고, 사용자가 지정한 목표(Goal)에 따라 의사결정
우선순위를 동적으로 변경"하는 M82를 요청했다. 최신 main(M81/ADR-0099까지
반영) 기준으로 조사한 결과, `decide_engine()`(M80)은 항상 `recommend_
engine()`(M79)의 1순위를 채택하고 `recommend_engine()`은 항상
`EngineSelectionPolicy.select()`(비용 최소 고정)의 결과만 반환해, Task/
호출자가 "품질 우선"·"latency 우선" 같은 의도를 표현할 방법이 없었다.

**사용자 승인(AskUserQuestion, 4회)**:
1. Goal 노출 위치 — **`recommend_engine()`/`decide_engine()`에만 선택적
   `goal` 키워드 파라미터(권장안 채택)**: `run()`/`_select()`는 전혀
   건드리지 않는다(100% 하위 호환). 이 결정으로 M80의 "decide_engine()은
   항상 run()과 같은 엔진" 보장은 `goal=BALANCED`(기본값)일 때만
   유효해진다.
2. Goal별 순위 결정 방식 — **우선순위 튜플 정렬(권장안 채택)**:
   `(1차키, 2차키, 3차키, engine_name)` tie-break 튜플. `COST_OPTIMIZED
   =(cost,-quality,latency,name)` / `QUALITY_OPTIMIZED=(-quality,cost,
   latency,name)` / `LATENCY_OPTIMIZED=(latency,cost,-quality,name)` /
   `BALANCED`=기존 `EngineSelectionPolicy.select()` 그대로.
3. Budget 필터링 — **기존과 동일하게 적용(권장안 채택)**: Goal 기반
   재정렬 전에 `budget_policy_engine.check()`로 예산 초과 후보를 먼저
   제외한다.
4. `decide_engine()`의 "run()과 항상 같은 엔진" 보장 범위 —
   **`BALANCED`일 때만 보장(권장안 채택)**: 다른 goal이면 `reason`에
   "run()과 다른 엔진일 수 있음"을 명시한다.

**구현**:
- `src/ai_workspace/domain/decision_goal.py` 신설 — `DecisionGoal`
  (Enum: `COST_OPTIMIZED`/`QUALITY_OPTIMIZED`/`LATENCY_OPTIMIZED`/
  `BALANCED`).
- `src/ai_workspace/interfaces/engine_runtime.py` — `recommend_engine()`/
  `decide_engine()`에 `goal: DecisionGoal = DecisionGoal.BALANCED` 추가
  (M70/M77/M79/M80/M81과 동일한 방식의 계약 확장).
- `src/ai_workspace/runtime/engine/engine_runtime.py`/
  `managed_engine_runtime.py` — `goal=BALANCED`(기본값)면 기존 코드
  경로를 그대로 실행(신규 분기 완전 우회). 다른 goal이면(`engine_
  selection_policy` 주입 시에만) `_build_candidates()`가 만든 후보에
  Budget 필터링 적용 후 `_goal_rank_key()`(신규)로 재정렬. `_evidence_
  snapshot()`(M79/M81) 재사용. `_representative_success_rate()`/
  `_representative_latency_seconds()`를 모듈 함수로 신설해 M81
  `_record_reflection()`의 인라인 계산을 대체(리팩터링)하고 M82가 공유.
  `decide_engine()`은 `goal != BALANCED`면 `reason`에 "run()과 다른
  엔진일 수 있음" 문구 추가.
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py` — 내부
  Runtime에 위임 확장.
- 테스트 대역 4곳에 `goal` 파라미터 추가(동작 무변경).
- `tests/runtime/engine/test_engine_runtime.py`(신규 9건), `tests/
  runtime/engine/test_managed_engine_runtime.py`(동일 시나리오 7건)
  추가.
- `docs/ARCHITECTURE.md` §3.9 Engine Runtime 절에 Goal-Aware Decision
  Policy(M82) 서술 추가, §7 인터페이스 표 `EngineRuntime` 행 갱신.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작, 기존 ADR/TASKS/ROADMAP·구현 상태를 먼저 조사 | ✅ |
| 2 | 기존 AutonomousDecisionEngine/EngineSelectionPolicy/Recommendation/Benchmark/Workflow Learning 최대 재사용 | ✅ |
| 3 | Goal은 새 알고리즘이 아니라 기존 요소(Cost/Reliability/Latency/Benchmark/Diversity/Workflow Learning)의 우선순위를 조정하는 Policy로만 구현 | ✅ |
| 4 | 최소 Goal Profile 4종(Cost/Quality/Latency Optimized, Balanced 기본값) | ✅ |
| 5 | Goal 미지정 시 기존 동작(Balanced)과 100% 동일 | ✅ |
| 6 | 기존 Routing/Recommendation 알고리즘 무변경, Policy Layer만 추가 | ✅ |
| 7 | 새로운 Core Domain Interface 없음(EngineRuntime 계약 확장 + Enum만) | ✅ |
| 8 | 상태는 EngineRuntime 내부 in-process로만 관리, 영속화 제외 | ✅ |
| 9 | 기존 API와 100% 하위 호환(YAGNI) | ✅ |
| 10 | Goal 노출 위치·순위 결정 방식·Budget 필터링·decide_engine 보장 범위를 AskUserQuestion 4회로 확정 | ✅ |
| 11 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1400개(신규 16개, 회귀 없음)/`ruff`/`mypy`(237 source files)
전부 통과. ADR-0100.

---

## Milestone 83 — Persistent Learning Memory: 학습 상태를 단일 JSON 파일로 영속화 (완료)

**배경**: 사용자가 "M65~M82에서 학습한 Engine Reliability, Benchmark,
Workflow Learning, Reflection, Recommendation 데이터를 세션 종료 후에도
유지"하는 M83을 요청했다. 최신 main(M82/ADR-0100까지 반영) 기준으로
조사한 결과, 관련 학습 데이터는 모두 in-process dict/deque로만 존재해
프로세스 종료(CLI는 매 명령마다 새 프로세스) 시 사라졌다. Benchmark/
Recommendation은 그 자체가 저장 대상이 아니라 4가지 원시 데이터(M65/
M69/M70/M81)를 조합한 파생값임을 확인했다.

**사용자 승인(AskUserQuestion, 4회)**:
1. 연결 지점 — **`WorkspaceCore.__init__`/`shutdown()`(권장안 채택)**:
   `shutdown()`이 이미 "종료" 의미를 갖고 있고, 생성자가 `engine_runtime`/
   `workflow_engine`을 이미 주입받는다.
2. API 표면 — **기존 `EngineRuntime`/`WorkflowEngine` 추상 인터페이스
   확장(권장안 채택)**: M70~M82와 동일한 계약 확장 방식.
3. 파일 구성 — **단일 JSON 파일로 통합(권장안 채택)**: `<data_dir 상위>/
   .ai-workspace-data/learning_state.json`.
4. 실패 처리 — **조용히 무시하고 in-process 기본값으로 fallback
   (권장안 채택)**: 새 로깅/예외 인프라 추가하지 않음(YAGNI).

**구현**:
- `src/ai_workspace/interfaces/engine_runtime.py`/`workflow_engine.py` —
  `export_learning_state() -> dict[str, Any]`/`import_learning_state
  (state) -> None` 추상 메서드 신설.
- `src/ai_workspace/runtime/engine/engine_runtime.py`/
  `managed_engine_runtime.py` — M65/M69/M70/M81 4가지 값 객체를 JSON
  직렬화 가능한 dict로 인코딩/디코딩. `(required_capabilities,
  engine_name)` 튜플 키는 레코드 리스트로 표현. `import_learning_state()`
  는 기존 상태를 대체(병합 아님).
- `src/ai_workspace/engines/workflow_engine.py` — `_order_stats`(이중
  중첩 키 dict)를 평평한 레코드 리스트로 표현.
- `src/ai_workspace/storage/file_learning_state_store.py` 신설 —
  `FileLearningStateStore`(새 Core Domain Interface 아님, 순수 I/O
  헬퍼). `FileMemoryEngine`(M50)과 동일한 패턴. 모든 I/O·파싱 예외를
  조용히 무시.
- `src/ai_workspace/core/workspace_core.py` — `restore_learning_state`/
  `persist_learning_state`(둘 다 `Callable[[], None] | None = None`)
  추가. `WorkspaceCore`는 §8 규칙 3("Interfaces에만 의존")에 따라 구체
  저장소를 몰라야 하므로 콜백으로만 연결(클로저는 Composition Root가
  구성).
- `src/ai_workspace/cli/main.py` — `_build_workspace_core()`가 저장소를
  조립하고 콜백을 연결, `main()`이 `finally`에서 `core.shutdown()` 호출.
- `src/ai_workspace/runtime/engine/recovering_engine_runtime.py` — 위임
  추가.
- 테스트 대역 5곳에 최소 구현 추가.
- `tests/runtime/engine/test_engine_runtime.py`(신규 4건), `tests/
  runtime/engine/test_managed_engine_runtime.py`(신규 3건), `tests/
  runtime/engine/test_recovering_engine_runtime.py`(신규 1건), `tests/
  engines/test_workflow_engine.py`(신규 3건), `tests/storage/
  test_file_learning_state_store.py`(신규 5건), `tests/core/
  test_workspace_core.py`(신규 3건), `tests/cli/test_main.py`(신규 2건)
  추가.
- `docs/ARCHITECTURE.md` §3.3 Workspace Core·§3.9 Engine Runtime 절 및
  §7 인터페이스 표(`EngineRuntime`/`WorkflowEngine`)에 Persistent
  Learning Memory(M83) 서술 추가.

**완료 조건 확인**

| # | 항목 | 상태 |
|---|---|---|
| 1 | 최신 main 기준에서 시작, 기존 ADR/TASKS/ROADMAP·구현 상태를 먼저 조사 | ✅ |
| 2 | 기존 Learning/EngineRuntime/WorkflowEngine/Reflection 구조 최대 재사용 | ✅ |
| 3 | in-process 상태를 Workspace 종료 시 저장, 시작 시 자동 복원 | ✅ |
| 4 | 저장 대상은 기존 학습 데이터로 제한, 새 Learning 데이터 없음 | ✅ |
| 5 | 저장 실패 시 기존 in-process 동작으로 즉시 fallback | ✅ |
| 6 | 저장 형식이 기존 Workspace 저장 방식(FileMemoryEngine)과 일관 | ✅ |
| 7 | 새로운 Core Domain Interface 없음(기존 인터페이스 확장 + 순수 I/O 헬퍼) | ✅ |
| 8 | 기존 API와 100% 하위 호환(YAGNI, 콜백 기본값 None) | ✅ |
| 9 | 연결 지점·API 표면·파일 구성·실패 처리를 AskUserQuestion 4회로 확정 | ✅ |
| 10 | `pytest`/`ruff`/`mypy` 전부 통과, 기존 테스트 회귀 없음 | ✅ |

`pytest` 1421개(신규 21개, 회귀 없음)/`ruff`/`mypy`(238 source files)
전부 통과. ADR-0101.

---

## GitHub Flow Migration

**목표**(2026-07-27 사용자 요청, 3단계): `claude/ai-workspace-docs-setup-aj3jvo`
가 우연히 Default Branch로 고정돼 있던 문제를 바로잡아, `main` 단일
상시 브랜치 + Pull Request 기반 **GitHub Flow**를 이 저장소의 공식
브랜치 전략으로 확립한다.

**진행 경과**

| 단계 | 내용 | 상태 |
|---|---|---|
| Phase 1 | `claude/m23-t01-reading-profiles-pmnpue` → `claude/ai-workspace-docs-setup-aj3jvo` → `main` 순차 Fast-forward 병합(충돌 0건, `pytest` 46개 통과) | **완료** |
| (사용자 직접 조치) | GitHub Default Branch를 `main`으로 변경, 이전 Default였던 `claude/ai-workspace-docs-setup-aj3jvo` 포함 사용하지 않는 브랜치 전부 삭제(`claude/ai-workspace-m11-execution-yrw0bx`/`claude/milestone-6-planning-lzc855`/`sop-skills-implementation-...`/`claude/m23-t01-reading-profiles-pmnpue`) | **완료** |
| Phase 3(M24-T04) | Git Vault Sync 검증 + 문서/규칙 업데이트 + GitHub Flow Baseline 확정 평가 | **완료(아래 참고)** |

### M24-T04: GitHub Flow Migration (Phase 3)

**DoD**

| # | 항목 | 상태 |
|---|---|---|
| 1 | Git Vault Sync 검증(Repository/Branch/Push/Pull/설정 이상 여부) | ✅ |
| 2 | README/`.ai/RULES.md`/`docs/ROADMAP.md`/`docs/ARCHITECTURE.md`/CONTRIBUTING.md 검토, Git Flow·`develop`·`claude/*` 언급 제거 | ✅ (제거할 내용 없음 확인) |
| 3 | Claude Code가 따를 GitHub Flow 규칙을 `.ai/RULES.md`에 명문화 | ✅ |
| 4 | GitHub Flow 운영 검증(브랜치 전략/PR 흐름/Merge 정책/Branch Protection/GitHub 설정/프로젝트 구조/Claude Code 작업 방식) | ✅ |
| 5 | GitHub Flow Baseline 확정 여부 평가 | ✅ |
| 6 | 신규 기능/리팩터링/테스트 코드 수정/CI 구축/Git Vault Sync 설정 변경/테스트용 브랜치·PR 생성 금지 준수 | ✅ |

**구현 내용**

- **T04-1 Git Vault Sync 검증**: `git remote show origin`으로
  `HEAD branch: main` 확인, GitHub API(`search_repositories`)로
  `default_branch: "main"`/`private: false`/`permissions.push:
  true`/`admin: true` 확인. `git fetch origin main`(Pull)과 이전
  Task들의 실제 push 이력(Pull/Push 정상)으로 재확인. **Git Vault
  Sync 자체에서(즉 이 세션이) 확인할 수 없는 항목**: 실제 iOS
  Git Vault Sync 앱이 이 저장소를 열어 정상 동작하는지는 이 세션이
  모바일 앱을 실행할 수 없어 직접 검증 불가 — 서버 측(GitHub
  저장소/브랜치) 조건은 전부 충족을 확인했다는 선에서 보고한다.
- **T04-2 프로젝트 문서 정리**: `README.md`/`.ai/RULES.md`/`docs/
  ROADMAP.md`/`docs/ARCHITECTURE.md` 전수 검색 결과 Git Flow/
  `develop` 브랜치/`claude/*` 브랜치 전략을 설명하는 내용이
  **어디에도 없었다**(제거 대상 0건 — 이전에는 브랜치 전략 자체가
  문서화된 적이 없었다). `CONTRIBUTING.md`는 이 저장소에 존재하지
  않아 해당 없음.
- **T04-3 Claude Code 규칙 업데이트**: `.ai/RULES.md`에 신규
  **§8 Git Branch Strategy(GitHub Flow)** 추가(v0.4.0 → v0.5.0) —
  Default Branch=`main`, 모든 작업 브랜치는 `main`에서 생성, 허용
  접두사(`feature/*`/`fix/*`/`docs/*`/`refactor/*`/`chore/*`),
  금지 브랜치(`claude/*`/`develop`/`release/*`/`hotfix/*`), PR
  기반 Merge, Merge 후 작업 브랜치 삭제, AI 세션에 대한 구속력
  명시. `README.md` "개발 철학" 목록에 9번 항목으로 GitHub Flow
  요약과 `.ai/RULES.md` §8 링크 추가(최소 변경).
- **핵심 발견(자기 적용 사례)**: 방금 작성한 §8 규칙에 따르면
  이 세션이 계속 써 온 `claude/*` 브랜치명 자체가 금지 대상이다
  — 그래서 이 문서 변경분부터 새 규칙을 즉시 자기 적용해
  `docs/github-flow-migration-phase3`(신규, `main`에서 분기)
  브랜치에서 작업하고 PR로 병합을 요청한다(아래 참고). 이 세션의
  기존 지정 브랜치(`claude/m23-t01-reading-profiles-pmnpue`)는
  사용자가 이미 삭제해 원격에 존재하지 않음을 확인했다.

**T04-4 GitHub Flow 운영 검증**

| 항목 | 결과 |
|---|---|
| 브랜치 전략 | ✅ `main` 단일 상시 브랜치만 원격에 존재(`git ls-remote --heads origin` 확인), §8 규칙 문서화 완료 |
| Pull Request 흐름 | ✅ PR #1~#4 전부 정상적으로 생성·병합된 이력 확인(Merge 방식: `merge`) |
| Merge 정책 | ⚠️ **미확정** — 지금까지는 PR마다 `merge`(병합 커밋) 방식을 수동으로 선택했다. Squash/Merge/Rebase 중 어느 것을 표준으로 할지 저장소 설정(Settings → General → Pull Requests)에 명시적으로 고정돼 있지 않다 — **개선 제안**: Squash and merge를 기본/유일 옵션으로 강제하면 `main` 커밋 이력이 Task 단위로 깔끔하게 유지된다(§5.3 "하나의 커밋은 하나의 Task"와도 일치) |
| Branch Protection | ⚠️ **이 세션에서 직접 확인 불가** — 설정 조회 API를 노출하는 도구가 없어, 사용자가 "이미 완료"라고 알려주신 것을 그대로 신뢰하는 것 외에 검증 방법이 없다. **권장**: GitHub 웹 UI(Settings → Branches → main)에서 "Require pull request before merging"/"Require status checks"/"Do not allow force pushes"가 실제로 켜져 있는지 직접 한 번 더 확인 |
| GitHub 설정 | ✅ `default_branch: main`, 저장소 정상(archived/disabled 아님), 관리 권한 보유 확인 |
| 프로젝트 구조 | ✅ Milestone 26(Vault Root Refactoring)으로 Vault 콘텐츠가 저장소 root에 있고, GitHub Flow(브랜치 전략)와는 독립적인 관심사라 충돌 없음 |
| Claude Code 작업 방식 | ⚠️ **이번 Task로 규칙은 갖췄지만 강제 메커니즘은 없음** — `.ai/RULES.md` §8은 "따라야 하는 문서"일 뿐, 이 세션(또는 향후 세션)이 실수로 다시 `claude/*` 브랜치를 만드는 것을 코드/설정 차원에서 막지는 못한다. **개선 제안**: Branch Protection의 브랜치 이름 패턴 제한(GitHub Rulesets)으로 `claude/*`/`develop`/`release/*`/`hotfix/*` 생성 자체를 서버 단에서 차단하면 완전히 강제할 수 있다(이번 Task 범위 밖 — GitHub 설정 변경 금지 조항에 해당해 수행하지 않음, 다음 Task로 제안) |

**T04-5 GitHub Flow Baseline 평가**: 아래 "Baseline 평가" 참고.

**의존성**: GitHub Flow Migration Phase 1(브랜치 Fast-forward 병합) +
사용자의 Default Branch 변경/브랜치 정리 완료.

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
| 2026-07-23 | P1-3 완료: 사용자 지시(계약 명시, Fake+계약 테스트 수준 검증)에 따라
ProjectRepository/WorkflowEngine/TaskEngine/MemoryEngine/ApprovalEngine/
AutomationEngine/EngineAdapter 7개 Interface를 계약(입력/출력/예외/보장사항 docstring
포함)으로 정의. Fake 구현체 + 계약 테스트 22개 작성, 전체(도메인 포함) 32개 테스트
통과. 다음 Task: P1-4 (Workspace Core 기본 골격 구현). |
| 2026-07-23 | **Multi-Agent First 전환**: 사용자 지시로 프로젝트 방향을 상시 멀티
에이전트 Workspace로 변경. 구현을 중단하고 아키텍처를 먼저 수정함. ADR-0006(Workspace
Core를 Agent 오케스트레이터로 재정의 + Agent Manager + Agent 도메인), ADR-0007(Event
Bus), ADR-0008(Conversation Layer), ADR-0009(EngineAdapter 확장 계약) 추가.
ARCHITECTURE.md v0.4.0, ROADMAP v0.3.0(M1~M4/Phase 0~6) 갱신. Phase 1을 P1-1~P1-12로
재구성(Agent 도메인 P1-4, 신규 Interface/EngineAdapter 확장 P1-5, Agent 위임형
Workspace Core P1-6 등). 기존 P1-1~P1-3 산출물은 유지. 구현 재개 대기. |
| 2026-07-23 | 사용자 지시로 `.ai/RULES.md`를 v0.2.0으로 재구성. 4개 그룹(Project
Principles / Development Workflow / Context Loading Rules / LLM Coding Rules)으로
정리하고 Interface First, Context Loading Rules, LLM Coding Rules(Think Before
Coding / Simplicity First / Surgical Changes / Goal-Driven Execution)를 추가함.
기존 언어·코딩·커밋 규칙은 공통 규칙으로 보존. |
| 2026-07-23 | **Multi-Agent First 심화**: 사용자 지시로 아키텍처를 재차 수정(문서만).
Agent Runtime 계층(Registry/Scheduler/Manager/Event Bus) 도입 + Workspace Core
책임 축소 + WorkspaceSession(ADR-0010), Mission→Workflow→Task→Step 계층(ADR-0011),
Capability 중심 Agent·Memory는 Engine(ADR-0012), Interaction Layer(ADR-0013),
Event Store(ADR-0014), EngineAdapter 세션 생명주기 계약(ADR-0015) 추가.
ARCHITECTURE.md v0.5.0, ROADMAP v0.4.0 갱신. Phase 1 P1-4~P1-7을 도메인 확장
(Mission/Step/WorkspaceSession/AgentCapability)·신규 Interface 7종·Agent Runtime
위임형 Workspace Core·EventStore 저장소로 갱신. 구현 재개 대기. |
| 2026-07-23 | **안정화 보완(P1-4 승인 조건)**: 사용자 권고 4건 반영(문서만).
Engine Runtime 계층 추가(Agent Runtime↔Engine Adapter 사이, ADR-0016), Context
Manager로 Memory Snapshot 역할 분리(ADR-0017), Event Store를 Event Bus 독립
Subscriber로 위치 조정(ADR-0018), Coordination Capability 추가(ADR-0019).
ARCHITECTURE.md v0.6.0, ROADMAP v0.5.0 갱신. Interfaces 14→16종(+EngineRuntime,
+ContextManager), MemoryEngine 계약 축소. Phase 1 P1-4~P1-6 반영. 구현 재개 대기. |
| 2026-07-23 | **P1-4 완료**: 사용자 지시로 범위를 확장해 Mission/Step/
WorkspaceSession/Agent 계열 도메인과 함께 **LLM Policy Domain 초안**(LLMProvider/
LLMModel/LLMEffort, Policy Engine·Router 제외)을 구현. `.ai/RULES.md`에
"Temporary LLM Policy" 섹션 추가, `docs/llm_policy.example.yaml` 작성. 신규
테스트 9개, 전체 41개 통과. `docs/ARCHITECTURE.md`는 변경하지 않음. 다음 Task:
P1-5 (신규 Interface 16종 정의 및 EngineAdapter 세션 계약 확장). |
| 2026-07-23 | **P1-5 완료**: 사용자 지시로 P1-5 범위를 "Core/Agent/LLM Domain
마무리 + 코드 품질 도구 도입"으로 재정의(기존 P1-5 "Interfaces 정의"는 P1-6으로
번호 이동, 이하 P1-6~P1-12를 P1-7~P1-13으로 순연). `domain/task.py`에
`workflow_id` 필드 추가(Task-Workflow 관계 보완). Agent/LLM Domain은 기존 구현이
요건(Provider 비의존, 확장 가능한 LLMModel 구조)을 이미 만족하여 코드 변경 없음.
`pyproject.toml`에 ruff/mypy 설정 추가, 위반 1건 수정 후 `ruff`/`mypy`/`pytest`
전부 통과(43개 테스트). `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`,
`.ai/DECISIONS.md`(ADR-0020) 갱신. 다음 Task: P1-6 (신규 Interface 16종 정의 및
EngineAdapter 세션 계약 확장). |
| 2026-07-24 | **Migration: Phase → Task 체계 전환 (ADR-0021)**. 사용자 지시로
프로젝트 관리 체계를 `Milestone → Phase → Task` 4단 계층에서 `Milestone → Task`
2단 계층으로 전환. 기능 구현/리팩터링/API 변경/기존 코드 변경은 전혀 하지 않음
(순수 문서 마이그레이션). 기존 Phase 0(P0-1~P0-11) + Phase 1(P1-0~P1-13) 총 25개
Task를 Milestone 1 소속 `T1-01`~`T1-25`로 그대로 재번호(내용·상태·이력 보존,
Migration Table은 `docs/ROADMAP.md` 하단 참고). Milestone 2~4는 아직 세부 Task가
없으므로 Phase 단위로 서술되어 있던 목표를 "예정 작업 영역"으로 재서술하고, 착수
시점에 `T2-01`/`T3-01`/`T4-01`부터 정의하기로 함. `docs/ROADMAP.md`,
`docs/ARCHITECTURE.md`, `.ai/DECISIONS.md`(ADR-0021), 본 문서, `.ai/MEMORY.md`,
`.ai/RULES.md`, `README.md`를 함께 갱신함. 다음 Task: **T1-18** (신규 Interface
16종 정의 및 EngineAdapter 세션 계약 확장 — 기존 계획상 "P1-6"과 동일한 작업). |
| 2026-07-24 | **T1-18 설계 검토 및 재분해 (ADR-0022)**. 사용자 요청으로 T1-18(신규
Interface 16종 정의 및 EngineAdapter 세션 계약 확장)의 설계를 검토함. Interface
계약 내용 자체는 대부분 유지(ADR-0010~0019에서 이미 충분히 근거가 검토된 결정)로
판정했으나, 서로 의존하지 않는 4개 아키텍처 하위 계층(Agent Runtime/Engine
Runtime/Memory/Interaction)을 하나의 Task로 묶은 것은 "Task = 하나의 구현
목표 + 하나의 커밋"(ADR-0021) 원칙에 어긋난다고 판단해 분리를 제안함. 사용자가
분리 방향을 승인하고 구체적인 분해 구조(T1-18~T1-28, 11개 Task)를 지시함. 이에
따라 기존 T1-18~T1-25(8개)를 T1-18~T1-28(11개)로 재구성: T1-18(Agent Runtime
Interfaces) / T1-19(Engine Runtime Interfaces) / T1-20(Memory Interfaces) /
T1-21(Interaction Interfaces) / T1-22(Workspace Core Skeleton, 구 T1-19) /
T1-23(Repositories, 구 T1-20) / T1-24(CLI, 구 T1-21) / T1-25(Tests, 구 T1-22) /
T1-26(Documentation, 구 T1-23) / T1-27(ADR, 구 T1-24) / T1-28(Milestone 1
Review, 구 T1-25). "인터페이스 정의 → 구현 → 테스트를 한 Task 안에서 완료"하는
기존 원칙은 유지하고, 구현/테스트를 별도 Task로 추가 분리하지는 않음. 부가 발견:
`memory_engine.py`는 이미 저장/검색만 담당하는 계약이라 T1-20에서 실질적인 코드
변경이 없음(No-Op). `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `.ai/DECISIONS.md`
(ADR-0022), `.ai/MEMORY.md`, `README.md`를 함께 갱신함. 다음 Task: **T1-18**
(Agent Runtime Interfaces). |
| 2026-07-24 | **T1-18 완료: Agent Runtime Interfaces**. 사용자 지시로 Agent
Runtime 계층(ARCHITECTURE.md §3.4)과 이벤트 인프라(§3.5)의 계약 6종을 정의함
(구현은 포함하지 않음). `interfaces/agent_manager.py`(`AgentManager`,
`InvalidAgentTransitionError`), `agent_registry.py`(`AgentRegistry`, 런타임
등록부 — `AgentNotRegisteredError`/`DuplicateAgentRegistrationError`),
`agent_scheduler.py`(`AgentScheduler`, Capability 기준 선택),
`agent_repository.py`(`AgentRepository`, 영속 저장소 —
`AgentNotFoundError`), `event_bus.py`(`EventBus`, `Event` dataclass,
`SubscriptionNotFoundError`), `event_store.py`(`EventStore`, `EventBus`의
독립 구독자, ADR-0018)를 추가함. `AgentRegistry`와 `AgentRepository`는 예외
이름을 다르게 하고 docstring에 런타임/영속 범위를 명시해 책임을 구분함.
`tests/interfaces/fakes.py`에 6개 Fake 구현체를 추가하고, 각 인터페이스별
계약 테스트 파일(`test_agent_manager.py` 등 6개, 총 23개 테스트)을 작성함 —
`test_event_bus.py`에는 `EventStore`가 `EventBus.subscribe()`를 다른 구독자와
동일한 경로로 등록됨을 검증하는 테스트를 포함함. `ruff check src tests`,
`mypy src`, `pytest`(66개, 전부 통과) 모두 통과함. 다음 Task: **T1-19**
(Engine Runtime Interfaces, 동일한 패턴). |
| 2026-07-24 | **T1-19 완료: Engine Runtime Interfaces**. Engine Runtime과
EngineAdapter의 세션 생명주기 계약을 확정함(ADR-0016). `interfaces/
engine_adapter.py`를 기존 `run_task` 단일 메서드 계약에서 세션 기반 계약
(`create_session`/`run`/`cancel`/`status`/`destroy_session`/`capabilities`/
`supports_parallel`/`estimate_cost`)으로 교체하고 `EngineSessionStatus`,
`CostEstimate`, `SessionNotFoundError`를 추가함. `interfaces/
engine_runtime.py`를 신규 추가해 `EngineRuntime`(엔진 선택, 세션 풀 관리는
구현체 내부로 캡슐화, `run_parallel`을 통한 병렬 실행)을 정의함 —
`DuplicateEngineError`/`NoSuitableEngineError`/`EngineTaskNotFoundError`.
Agent가 EngineAdapter를 직접 호출하지 않고 EngineRuntime을 거치는 의존
방향(ARCHITECTURE.md §8 규칙 6)을 계약에 명시함. `tests/interfaces/
fakes.py`의 `FakeEngineAdapter`/`FailingFakeEngineAdapter`를 새 계약으로
재작성하고 `FakeEngineRuntime`을 추가함. `test_engine_adapter.py`를 새
계약 기준으로 재작성(기존 `run_task` 기반 테스트 대체)하고
`test_engine_runtime.py`를 신규 추가함. `docs/ARCHITECTURE.md` §7
Interface 표를 갱신함. `ruff check src tests`, `mypy src`, `pytest`(79개,
기존 66개 + 신규 13개) 모두 통과. 다음 Task: **T1-20** (Memory Interfaces,
동일한 패턴). |
| 2026-07-24 | **T1-20 완료: Memory Interfaces**. Context 조립과 Memory
저장/검색의 역할 분리를 계약으로 확정함(ADR-0017). `interfaces/
context_manager.py`를 신규 추가해 `ContextManager`(`assemble_context`/
`create_snapshot`/`restore_snapshot`, `SnapshotNotFoundError`)를 정의함 —
`WorkspaceSession.memory_snapshot_id`가 가리키는 Snapshot을 Context
Manager가 소유·관리하고 `MemoryEngine`은 이를 알지 못함을 docstring에
명시함. `memory_engine.py`는 재검토 결과 Snapshot 관련 메서드가 애초에
없어 "저장/검색만" 계약을 이미 만족하고 있음을 확인, **코드 변경 없음**
(T1-17에서 Agent/LLM Domain을 재검토 후 변경 없음으로 처리한 것과 동일한
패턴). `tests/interfaces/fakes.py`에 `FakeContextManager`를 추가하고
`test_context_manager.py`를 신규 추가함(4개 테스트). 기존 `MemoryEngine`
계약·테스트는 변경 없이 그대로 통과해 회귀가 없음을 확인함.
`docs/ARCHITECTURE.md` §7 Interface 표를 갱신함. `ruff check src tests`,
`mypy src`, `pytest`(83개, 기존 79개 + 신규 4개) 모두 통과. 다음 Task:
**T1-21** (Interaction Interfaces, 동일한 패턴). |
| 2026-07-24 | **T1-21 완료: Interaction Interfaces**. 입력 표면 정규화
계약을 확정함(ADR-0013). `interfaces/interaction_engine.py`를 신규
추가해 `InteractionEngine`(`normalize`/`format_response`/
`supported_surfaces`, `NormalizedRequest`, `UnsupportedSurfaceError`)을
정의함 — 기존 `ConversationEngine` 명칭을 대체하고, Agent Runtime/Engine
Runtime/Memory 어느 것에도 의존하지 않고 UI Surfaces와 Workspace Core
사이에만 위치하는 독립 계층임을 docstring에 명시함.
`tests/interfaces/fakes.py`에 `FakeInteractionEngine`을 추가하고
`test_interaction_engine.py`를 신규 추가함(4개 테스트).
`docs/ARCHITECTURE.md` §7 Interface 표를 갱신함. `ruff check src tests`,
`mypy src`, `pytest`(87개, 기존 83개 + 신규 4개) 모두 통과. 이로써
T1-18~T1-21(Agent Runtime/Engine Runtime/Memory/Interaction Interfaces)
그룹이 모두 완료됨. **병합 메모**: 별도로 진행된 다른 세션에서도 같은
T1-21에 대해 `InteractionRequest`/`InteractionResponse`/
`InteractionError`/`InvalidRequestError` + `handle_request` 단일 메서드
설계를 독립적으로 구현해 origin 브랜치에 먼저 병합되어 있었음(PR #1).
두 설계가 병합 시점에 충돌하여 검토한 결과, `handle_request` 설계는
정규화와 Workspace Core의 응답 처리를 한 메서드로 묶어 Interaction
Layer와 Workspace Core의 책임 경계(ARCHITECTURE.md §3.2, §8 규칙 1~2)가
흐려질 수 있다고 판단해 채택하지 않고, 위 `normalize`/`format_response`
설계를 최종안으로 유지함. 다음 Task: **T1-22** (Workspace Core Skeleton). |
| 2026-07-24 | **병합: origin 브랜치의 병렬 작업 반영 (PR #1)**. `git push` 시
origin에 이미 다른 세션에서 병합한 커밋이 있어 `git merge`로 충돌을
해결함. T1-21 InteractionEngine은 위 병합 메모대로 이 세션의 설계
(`normalize`/`format_response`/`supported_surfaces`)를 유지함. 원래
계획에 없던 **T1-29(SOP Skills System)**: `.ai/skills/`에 7개 SOP
가이드라인 문서를 추가하는 순수 문서 작업으로, 코드/아키텍처와 충돌이
없어 그대로 수용하고 `.ai/TASKS.md`에 정식 Task로 편입함(T1-28 뒤,
Milestone 1 Review 검토 대상에 포함). `ruff check src tests`, `mypy src`,
`pytest`(87개, T1-21 관련 회귀 없음) 모두 통과 확인 후 병합 커밋 진행. |
| 2026-07-25 | **T1-22 완료: Workspace Core Skeleton**. `core/workspace_core.py`에
`WorkspaceCore`를 신규 구현함(ADR-0005, ADR-0010). 생성자에서
`ProjectRepository`/`WorkflowEngine`/`AgentRegistry`/`AgentScheduler`/
`AgentManager`/`EventBus`/`EngineRuntime` 7개 Interface와 `config:
dict[str, str]`를 키워드 전용으로 주입받아 보관한다 — Registry/Scheduler/
Manager/EventBus를 하나의 `AgentRuntime` 파사드로 묶지 않고 개별 필드로
유지함(T1-22 명세의 YAGNI 지시 그대로 따름). `load_project`(→
`ProjectRepository.load` 위임), `config` 프로퍼티(방어적 복사),
`start_session`/`get_session`/`update_session`/`end_session`(WorkspaceSession은
어떤 Interface로도 영속화 대상이 아니므로 Core 내부 in-memory 레지스트리로
관리, 신규 예외 `WorkspaceSessionNotFoundError`), `agent_registry`/
`agent_scheduler`/`agent_manager`/`event_bus`/`engine_runtime` 읽기 전용
프로퍼티(Milestone 2 구현체가 사용할 수 있도록 노출만 함), `start_workflow`
(→ `WorkflowEngine.plan` 위임), `shutdown`(모든 Session 정리)을 구현함.
**Task 직접 실행 금지 증명**: `run_task`/`execute_task` 같은 메서드를
아예 두지 않았고, 테스트에서 `run()`/`run_parallel()` 등 모든 메서드가
호출되면 `AssertionError`를 던지는 `SpyEngineRuntime`을 주입한 뒤 Core의
모든 공개 메서드를 호출해도 예외가 발생하지 않음을 확인해 Core가 Engine
Runtime을 스스로 호출하지 않음을 테스트로 증명함(`tests/core/
test_workspace_core.py`, 13개 테스트). `docs/ARCHITECTURE.md` §3.3·§9는
이미 이 설계와 일치해 변경하지 않음. `ruff check src tests`, `mypy src`,
`pytest`(100개, 기존 87개 + 신규 13개) 모두 통과. 다음 Task: **T1-23**
(Repositories: FileProjectRepository/FileAgentRepository/FileEventStore). |
| 2026-07-25 | **DX-01 완료: Stage Checkpoint + Smart Model Router 통합**
(`.ai/DECISIONS.md`의 `DX-01` 항목 참고 — 시스템 아키텍처 결정이 아니라 AI
세션 운영 절차 변경이라 ADR 번호를 소비하지 않고, Milestone 1의 T1-XX Task도
아니라 별도 Task ID 없이 진행 로그로만 기록함). `.ai/RULES.md`에 §2.4 Stage
Checkpoint를 신규 추가: Task 내부 4개 작업 단계 경계(Analysis/
Implementation/Validation/Task 완료 — `Task-Planning.md`/
`Task-Implementation.md` §5.1~5.6 절차 경계에 대응)마다 Smart Model
Router(`.claude/skills/smart-model-router`)를 실행해 Recommendation
(model/effort/confidence/reason)을 산출하고, Manual Recommendation
Executor(사용자 선택 + 한국어 UI + `/model` 안내 후 대기)로 소비함. "Phase"
대신 **"Stage"**를 공식 명칭으로 채택함(ADR-0021에서 이미 폐지된 프로젝트
관리 계층 "Phase"와의 혼동 방지). 동일/상향/하향 어떤 경우도 Model/Effort를
자동 전환하지 않으며, 불필요한 UI 노출을 막는 Skip Rule을 정의함. §5.1
언어 규칙을 세션 중 사용자에게 보이는 모든 메시지(진행 상황/질문/완료
보고/추천 결과/오류 안내/승인 요청)로 확장하고, 기술 용어(Model/Effort/
pytest/ruff/mypy/Commit Message/클래스·함수·파일명/API)는 원문 유지로
명시함. `Recommendation`의 실제 Python 구현은 Task Driven Development
원칙에 따라 지금 하지 않고 §7 로드맵(M2 이후)으로 미룸 — 지금은 §2.4 안의
개념적 스키마로만 정의함. `Task-Planning.md`(1곳), `Task-Implementation.md`
(3곳: §5.3→5.4, §5.4→5.5, §5.6 뒤)에 Stage Checkpoint 상호 참조를 추가함.
`README.md`/`docs/ARCHITECTURE.md`는 변경하지 않음(시스템 아키텍처가 아님).
적용 대상 소스 코드 없음(문서 전용 변경). |
| 2026-07-25 | **T1-23 완료: Repositories**(§2.4 Stage Checkpoint 적용,
Sonnet/Medium). `storage/`에 `FileProjectRepository`/`FileAgentRepository`
(엔티티당 JSON 파일 1개)/`FileEventStore`(단일 append-only JSON Lines
로그)를 구현함. Enum/frozenset은 JSON 직렬화가 안 되어 각 구현체 내부에서
`.value`↔생성자로 변환하고 도메인 모델(`Project`/`Agent`/`Event`)은 건드리지
않음. `tests/storage/`에 21개 신규 테스트 추가 — CRUD, Interface 계약
예외(`ProjectNotFoundError`/`AgentNotFoundError`), `replay(since_event_id)`
순서·필터링, 그리고 파일 기반의 핵심 차별점인 "새 인스턴스로 재오픈해도
데이터 유지"를 검증함. DoD의 "Workspace Core 주입 시 Core 코드 변경
불필요"는 `FileProjectRepository`를 `WorkspaceCore`에 직접 주입하는 테스트로
증명함(`AgentRepository`/`EventStore`는 T1-22 설계상 Workspace Core
생성자의 직접 의존 대상이 아니므로 해당 없음 — Agent Runtime/Event Bus
독립 구독자가 Milestone 2에서 사용할 대상). `ruff check src tests`,
`mypy src`, `pytest`(121개, 기존 100개 + 신규 21개) 모두 통과. 다음 Task:
**T1-24** (CLI).

**DX-01 첫 실사용 회고**: §2.4의 4개 Stage Checkpoint 중 실제로 Smart Model
Router가 재판단을 수행한 것은 Task 착수 전 1회뿐이었다. Implementation→
Validation, Validation→문서화 경계에서는 §2.4가 최소 요구하는 Skip Rule
한 줄 출력조차 하지 않고 통과함 — 규칙 자체의 결함이 아니라 실행 누락으로
판단됨(규칙은 정확히 쓰여 있음). Skip Rule 경로는 이번에 한 번도 실행되지
않아 검증되지 못함. 표시된 한국어 UI(박스 2회)는 승인된 템플릿과 일관됨.
TASKS.md 편집 중 `old_string` 오지정으로 텍스트를 잘못 덮어썼다가 즉시
되돌린 실수가 1건 있었음(Effort 인과관계는 불명확하나 참고 신호로 기록).
T1-24부터는 나머지 경계에서도 실제로 멈춰 재판단하기로 함. |
| 2026-07-25 | **T1-24 완료: CLI**(§2.4 Stage Checkpoint 4개 경계 모두 실제
발동 — 4회 전부 "동일" 판정으로 Sonnet/Medium 유지, 한 줄 Skip Rule 출력 확인).
`cli/main.py`에 argparse 기반 CLI 진입점 구현: `project create <id> <name>
<goal> [--priority N]` / `project show <id>`, `--data-dir`(기본값
`workspace/projects`). **설계 판단**: 명세는 "Workspace Core와 파일 저장소를
연결"이라 되어 있으나, `WorkspaceCore` 생성자는 `ProjectRepository` 외
6개 Interface(`WorkflowEngine`/`AgentRegistry`/`AgentScheduler`/
`AgentManager`/`EventBus`/`EngineRuntime`)를 필수로 요구하고 이들은 아직
구체 구현이 없음(Milestone 2+ 예정) — 지금 이를 위한 임시 더미 구현체를
만드는 것은 범위 밖의 선점 구현(YAGNI 위반)이라 판단해, CLI는
`FileProjectRepository`를 직접 사용함. DoD("생성→조회 e2e 동작")는 이것만
으로 충분히 만족됨. `WorkspaceCore` 완전 연동은 Agent/Engine Runtime
구체 구현이 준비되는 Milestone 이후로 미룸. `tests/cli/test_main.py`에
5개 신규 테스트(e2e, priority 반영/기본값, 존재하지 않는 Project 조회 시
오류(exit code 1 + stderr), 프로세스 재시작 후 영속성). `ruff check src
tests`, `mypy src`, `pytest`(126개, 기존 121개 + 신규 5개) 모두 통과.
다음 Task: **T1-25** (Tests: 전체 스위트 통합 점검 및 커버리지 보강). |
| 2026-07-25 | **T1-25 완료: Tests**(§2.4 Stage Checkpoint 4개 경계 모두
발동, 전부 "동일" 판정으로 Sonnet/Medium 유지). `pytest` 설정(`pythonpath`/
`testpaths`)은 점검 결과 이미 최소·정확해 변경 없음. `tests/interfaces/`
(708줄, 16개 Interface)는 T1-15~T1-21에서 이미 계약 테스트로 탄탄하게
작성되어 있음을 확인(가장 짧은 2개 파일을 직접 재확인) — 보강 대상에서
제외. 실제 갭 3곳을 보강함: (1) `tests/core/test_workspace_core.py` —
T1-22 리뷰에서 지적된 5개 경계 조건(`update_session`의 `active_workflow_id`/
`active_agent_ids`(방어적 복사 포함)/`memory_snapshot_id`/
`engine_session_id`, `config` 기본값 `{}`, `start_session` 기본
`project_id=None`, 존재하지 않는 session에 대한 `update_session` 예외) 6개
테스트 추가. (2) `tests/domain/test_task.py` — `TaskStatus`의 두 종단
상태(`DONE`/`CANCELLED`)가 전이 불가임을 검증하는 테스트, `BLOCKED` 순환
경로(`IN_PROGRESS`→`BLOCKED`→`IN_PROGRESS`), `REVIEW`→`IN_PROGRESS`(반려),
`TODO`→`CANCELLED` 5개 테스트 추가. (3) `tests/domain/test_workflow.py` —
3노드 간접 순환(직접·자기 순환 외의 경로) 1개 테스트 추가. 프로덕션 코드는
전혀 변경하지 않음(테스트 전용 Task). `ruff check src tests`, `mypy src`,
`pytest`(139개, 기존 126개 + 신규 13개) 모두 통과. 다음 Task: **T1-26**
(Documentation: `docs/ARCHITECTURE.md` 최종 정합성 확인). |
| 2026-07-25 | **T1-26 완료: Documentation**(§2.4 Stage Checkpoint 4개 경계
모두 발동. Analysis 단계에서 Sonnet/Medium→**Sonnet/Low**로 하향 — 순수
대조/표기 수정이라 Effort를 낮춰도 충분하다고 판단, 이후 3개 경계 모두
Low 유지로 "동일" 판정). `docs/ARCHITECTURE.md`를 v0.6.3→v0.7.0으로 갱신,
실제 구현과 대조해 불일치 3곳만 수정(신규 아키텍처 결정 없음): (1) 문서
헤더 상태를 "T1-17까지 완료"에서 "T1-25까지 완료"로 갱신. (2) §7 Interface
표에서 `ProjectRepository`/`AgentRepository`/`EventStore`가 T1-23에서
각각 `FileProjectRepository`/`FileAgentRepository`/`FileEventStore`로
실제 구현되었음을 반영(상태를 "완료(계약)"→"완료(계약+구현)"으로 세분화하고,
나머지 계약 전용 Interface는 "완료(계약)"으로 명확화, 범례 추가). (3) §9
디렉터리 구조에서 이미 구현된 `core/`(T1-22)/`storage/`(T1-23)/`cli/`
(T1-24)에 완료 표시를 추가해 Milestone 2/3 이후로 표시된 미구현
디렉터리와 구분되게 함. §3.3 Workspace Core 책임 서술, §2 다이어그램, §8
의존성 규칙, §11 기술 스택은 대조 결과 이미 실제 구현과 일치해 변경하지
않음(§11 저장 방식 "Markdown/JSON"은 ADR-0004가 아직 "제안" 상태라 JSON
으로 단정하지 않고 그대로 둠 — 확정은 T1-27 소관). 소스 코드는 전혀
변경하지 않음. `ruff check src tests`, `mypy src`, `pytest`(139개, 회귀
없음) 모두 통과. 다음 Task: **T1-27** (ADR: ADR-0002, ADR-0004 상태를
"승인됨"으로 갱신). |
| 2026-07-25 | **T1-27 완료: ADR**(§2.4 Stage Checkpoint 4개 경계 모두
발동, 전부 "동일" 판정으로 Sonnet/Low 유지). `.ai/DECISIONS.md`의
ADR-0002/ADR-0004를 "제안"에서 "승인됨"으로 확정. ADR-0002는 ADR-0009가
예고한 대로 "결정" 항목을 옛 `run_task()` 단일 메서드 예시에서 T1-19에서
실제 확정된 최종 계약(`create_session`/`run`/`cancel`/`status`/
`destroy_session`/`capabilities`/`supports_parallel`/`estimate_cost`)으로
갱신함. ADR-0004는 "결정" 원문(과거 결정 텍스트)은 그대로 두고 "결과/영향"에
T1-23에서 실제로는 **JSON만** 채택되었다는 사실(Markdown 미사용, 이유:
Enum/frozenset 등 구조화된 값을 다루기에 JSON이 더 적합)을 추가함. 소스
코드는 전혀 변경하지 않음. `ruff check src tests`, `mypy src`,
`pytest`(139개, 회귀 없음) 모두 통과. 다음 Task: **T1-28** (Milestone 1
Review — 최종 승인 요청). |
| 2026-07-25 | **T1-28 완료 & Milestone 1 종료: 사용자 승인**. 도메인
(Project/Mission/Workflow/Task/Step/WorkspaceSession/Agent 계열, LLM
Policy 초안), Interfaces 16종(`ProjectRepository`/`AgentRepository`/
`EventStore` 3종은 계약+구현 완료, 나머지 13종은 계약만 완료 — Milestone
2·3에서 구현 예정), Workspace Core 골격(T1-22), 파일 기반 저장소 3종
(T1-23), CLI 진입점(T1-24), 테스트 스위트(139개 통과, T1-25에서 커버리지
보강), 문서 정합성(T1-26), ADR 확정(T1-27), SOP Skills System(T1-29)을
종합 제시했고 사용자가 Milestone 1 완료를 승인함. 미결 항목(Interfaces
13종 구체 구현, `AgentRuntime` 파사드 도입 여부, CLI-WorkspaceCore 완전
연동)은 결함이 아니라 Milestone 2·3으로 계획대로 이월됨. DX-01(Stage
Checkpoint)도 Milestone 1 기간 중 도입되어 "동일"·"하향"·"상향" 3가지
판정 경로가 모두 실사용 검증됨. **Milestone 1(기반 구축) 종료.** 사용자
권고에 따라 다음은 Milestone 2 목표/DoD 확정 후 `T2-01`부터 착수 예정
(아직 세부 Task 미정의 — Task Driven Development 원칙상 착수 시점에
정의). |
| 2026-07-25 | **Milestone 2 계획 확정**(세션 종료 전 사용자 요청 —
"Milestone 2는 처음부터 범위와 완료 기준이 명확한 상태에서 시작"). Goal과
Milestone DoD(3개 항목)는 기존 `docs/ROADMAP.md` 서술을 그대로 유지하고,
ADR-0022 원칙(아키텍처 책임 경계로 분해)에 따라 `T2-01`~`T2-07`(7개) 확정.
T2-01(Agent Runtime: Registry/Scheduler/Manager/EventBus), T2-02(Core
Engines: Task/Workflow/Approval/Automation Engine), T2-03(Memory 계열:
MemoryEngine+ContextManager)은 서로 독립이라 순서 무관. **설계 판단**:
`docs/ARCHITECTURE.md` §7 표는 EngineRuntime/EngineAdapter 구체 구현을
Milestone 3로 표시하지만, Milestone 2 DoD 3번("Mock EngineAdapter 위에서
협업 시나리오 통과")을 만족하려면 최소 구현이 필요해 T2-04(`InMemoryEngineRuntime`
+ `MockEngineAdapter`)로 앞당김 — M3에서는 Mock만 실제 어댑터로 교체.
T2-05(능력별 Agent 골격)는 T2-01~T2-04 전부에 의존(ARCHITECTURE.md §8
규칙 5). T2-06(통합 시나리오 테스트)·T2-07(Milestone 2 Review)은 순차
진행. `docs/ROADMAP.md`(v0.7.0, Milestone 2 절을 표 형식으로 재작성)와
본 문서(Milestone 2 섹션에 T2-01~T2-07 상세 추가)에 반영함. 코드는 전혀
작성하지 않음(계획 전용). 다음 세션은 **T2-01**부터 바로 구현 착수 가능. |
| 2026-07-25 | **T2-01 완료: AgentRuntime + AgentSession**(§2.4 Stage
Checkpoint 4개 경계 모두 발동, Analysis에서 Sonnet/Low→**Sonnet/Medium**
상향 — 신규 파사드+도메인 모델 설계라 단순 CRUD보다 복잡도가 높다고 판단,
이후 3개 경계는 "동일" 유지). 사용자 지시로 T2-01 범위가 계획 문서보다
좁아짐: `AgentRuntime`은 `AgentManager`+`AgentRegistry` 두 Interface만
사용하고 Scheduler/EventBus/Core Engines/Context Manager/LLM 호출/
Multi-Agent 협업/Planner·Worker·Validator Agent/Workflow 실행을 명시적으로
배제함(T1-22가 보류했던 `AgentRuntime` 파사드 도입을 지금 재검토하는
결정). `domain/agent_session.py`에 `AgentSession`(session_id, agent_id —
status는 중복 보관하지 않고 매번 `AgentRegistry.get(agent_id).status`로
조회, 단일 진실 원천 유지) 신규 정의. `runtime/agent/agent_runtime.py`에
`AgentRuntime`(`start_agent`/`stop_agent`/`get_session`/`get_agent_state`/
`shutdown`, 신규 예외 `AgentSessionNotFoundError`) 구현 — WorkspaceCore와
동일한 키워드 전용 DI 패턴. 새 Interface는 추가하지 않음(AgentRuntime도
WorkspaceCore처럼 ABC 없는 구체 클래스). `tests/runtime/agent/
test_agent_runtime.py` 11개 신규 테스트(기존 `FakeAgentManager`/
`FakeAgentRegistry` 재사용, 신규 Fake 불필요). `ruff check src tests`,
`mypy src`, `pytest`(150개, 기존 139개 + 신규 11개) 모두 통과. **범위
축소에 따라 Milestone 2 Task 목록을 T2-01~T2-07(7개)에서 T2-01~T2-08
(8개)로 재분해**: Scheduler+EventBus를 신규 T2-02로 분리하고 이하 Task를
T2-03~T2-08로 순연(상세 사유는 Milestone 2 섹션 상단 안내문 참고). 다음
Task: **T2-02** (Agent Scheduler + Event Bus 구현). |
| 2026-07-25 | **T2-02 완료: Agent Scheduler + Event Bus**(§2.4 Stage
Checkpoint 4개 경계 모두 발동, Analysis에서 Sonnet/Medium→**Sonnet/Low**
하향 — 이미 검증된 Fake 로직을 그대로 승격하는 기계적 작업이라 판단,
이후 3개 경계는 "동일" 유지). `runtime/agent/agent_scheduler.py`에
`InMemoryAgentScheduler`, 신규 `events/` 패키지의 `event_bus.py`에
`InMemoryEventBus` 구현 — 둘 다 `tests/interfaces/fakes.py`의
`FakeAgentScheduler`/`FakeEventBus`와 로직이 동일해 새로운 설계 판단이
없었음(T1-23의 File 저장소 구현 때와 같은 "Fake 승격" 패턴).
`AgentRuntime`과의 실제 연동(Scheduler로 후보 선택, EventBus로 Agent 간
통신)은 의도적으로 하지 않음 — T2-06(능력별 Agent 골격) 범위.
`tests/runtime/agent/test_agent_scheduler.py` 3개(Capability 매칭/
max_count/미매칭 시 빈 리스트), `tests/events/test_event_bus.py` 6개
(단일·다중 구독 전달, 구독자 예외 격리, 구독 해제, 존재하지 않는 구독
해제 예외, 구독 전 발행분 소급 전달 안 됨) 신규 테스트. `ruff check src
tests`, `mypy src`, `pytest`(159개, 기존 150개 + 신규 9개) 모두 통과.
다음 Task: **T2-03** (Core Engines 구현). |
| 2026-07-25 | **T2-03 완료: Core Engines**(§2.4 Stage Checkpoint 4개
경계 모두 발동, 전부 "동일" 판정으로 Sonnet/Low 유지). `engines/`에
`InMemoryTaskEngine`/`InMemoryWorkflowEngine`/`InMemoryApprovalEngine`/
`InMemoryAutomationEngine` 구현(전부 기존 Fake 로직 승격). **부가 발견 및
수정**: `ApprovalActionType.PHASE_COMPLETION`이 ADR-0021 이후 갱신되지
않고 남아있던 것을 발견해 `MILESTONE_COMPLETION`으로 정정(인터페이스
정의 + 기존 테스트 1곳). `task_engine.py`/`workflow_engine.py`/
`automation_engine.py`의 "Phase 2에서 작성한다" docstring도 함께 정정.
`tests/engines/`에 17개 신규 테스트 — `ApprovalActionType` 4개 값 전부에
대해 submit→PENDING→decide→APPROVED를 검증하는 테스트로 DoD("4대 행위
판별·차단")를 직접 증명. `ruff check src tests`, `mypy src`,
`pytest`(176개, 기존 159개 + 신규 17개) 모두 통과. 다음 Task: **T2-04**
(Memory 계열 구현). |
| 2026-07-25 | **T2-04 완료: Memory 계열**(§2.4 Stage Checkpoint 4개
경계 모두 발동. Analysis에서 Sonnet/Low→**Sonnet/Medium** 상향 — T2-02/03
과 달리 ContextManager↔MemoryEngine 실제 의존 배선이 필요한 설계 작업
이라 판단, 이후 3개 경계는 "동일" 유지). `memory/memory_engine.py`의
`InMemoryMemoryEngine`은 Fake 로직 그대로 승격. `memory/
context_manager.py`의 `InMemoryContextManager`는 기존 `FakeContextManager`
(자체 dict에 Snapshot 보관)와 다르게 설계 — `MemoryEngine`을 생성자로
주입받아 `remember(snapshot_id, json.dumps(context))`/`recall()`+
`json.loads()`로 Snapshot을 실제 저장·복원해 ARCHITECTURE.md §8 규칙 7
("Memory 접근은 Agent → Context Manager → Memory Engine 순서로만")을
코드 구조로 강제함. `tests/memory/test_context_manager.py`에
`MemoryEngine.recall()`로 Snapshot이 실제 저장되었는지 직접 확인하는
테스트를 포함해 DoD를 코드+테스트 양쪽으로 증명. `tests/memory/`에 10개
신규 테스트(Context 조립 2, 왕복 일치, MemoryEngine 경유 저장 증명,
unknown 예외, 방어적 복사, Snapshot 복원이 assemble_context에 반영됨).
`ruff check src tests`, `mypy src`, `pytest`(186개, 기존 176개 + 신규
10개) 모두 통과. 다음 Task: **T2-05** (Engine Runtime 최소 구현 + Mock
EngineAdapter). |
| 2026-07-25 | **T2-05 완료: Engine Runtime + Mock EngineAdapter**(§2.4
Stage Checkpoint 4개 경계 모두 발동. Analysis에서 Sonnet/Medium→
**Sonnet/Low** 하향 — 기존 `FakeEngineRuntime`/`FakeEngineAdapter` 로직
승격 위주라 판단, 이후 3개 경계는 "동일" 유지). `runtime/engine/
engine_runtime.py`의 `InMemoryEngineRuntime`, `adapters/
mock_engine_adapter.py`의 `MockEngineAdapter` 구현 — 둘 다 기존 Fake
로직 그대로 승격. 한 가지 의도적 차이: `MockEngineAdapter.
estimate_cost()`는 Fake의 임의 테스트값(100 토큰/$0.01) 대신 실제 엔진을
호출하지 않는다는 사실을 정직하게 반영해 0/0.0을 반환하도록 함.
`tests/adapters/test_mock_engine_adapter.py` 5개, `tests/runtime/engine/
test_engine_runtime.py` 7개(DoD "Mock EngineAdapter로 Task 실행 →
success=True"를 직접 명시하는 테스트 포함) 신규 테스트. `ruff check src
tests`, `mypy src`, `pytest`(198개, 기존 186개 + 신규 12개) 모두 통과.
다음 Task: **T2-06** (능력별 Agent 골격 구현 — T2-01~T2-05 전부에 의존,
지금까지 만든 5개 컴포넌트를 실제로 엮는 첫 Task). |
| 2026-07-25 | **T2-06 완료: 능력별 Agent 골격**(§2.4 Stage Checkpoint
4개 경계 모두 발동. Analysis에서 Sonnet/Low→**Sonnet/High** 상향 — 5개
컴포넌트를 처음 실제로 엮는 Milestone 2 핵심 통합 작업이라 판단, 이후
3개 경계는 "동일" 유지). 상세 내용은 위 T2-06 항목의 "상태" 필드 참고.
요약: `PlanningAgent`/`CodingAgent`/`ReviewAgent`/`DocumentationAgent`
4종을 Event 기반으로 연결해 DoD의 4단계 Event 체인을 구현·검증함.
`InMemoryEventBus`의 재귀 publish 순서 뒤집힘 함정을 설계 단계에서
발견해 집합 기반 검증으로 회피(순서 기반 assertion이었다면 실패했을
것). `AgentManager`/`AgentRegistry` 프로덕션 구현체 공백을 문서화(향후
Task 후보). `pytest`(203개, 기존 198개 + 신규 5개), `ruff`, `mypy` 모두
통과. 다음 Task: **T2-07** (통합 시나리오 테스트 — Milestone 2 DoD 3개
항목을 end-to-end로 최종 증명). |
| 2026-07-25 | **설계 철학 확립**: 사용자가 Architecture First/최소
복잡성/YAGNI/응집도 우선/점진적 확장/기존 코드 존중 6원칙을 앞으로의
모든 작업 기본 원칙으로 제시함(기억 시스템에 저장). **T2-07 완료: 통합
시나리오 테스트**(§2.4 Stage Checkpoint 4개 경계 모두 발동. Analysis에서
Sonnet/High→**Sonnet/Medium** 하향 — 새 컴포넌트를 만들기보다 이미 만든
것들을 검증·연결하는 작업이라 판단). 새 설계 철학을 적용해 기존 테스트를
먼저 점검한 뒤 실제 빈틈 2곳만 채움(상세는 위 T2-07 항목 참고). 새 파일/
클래스 없음. `pytest`(205개, 기존 203개 + 신규 2개), `ruff`, `mypy` 모두
통과. 다음 Task: **T2-08** (Milestone 2 Review — 최종 승인 요청). |
| 2026-07-25 | **설계 철학을 `.ai/RULES.md` 영구 규칙으로 승격(DX-02)**.
T2-07에서 처음 제시됐던 설계 철학(Architecture First 강화/최소 복잡성/
YAGNI/점진적 확장/응집도/기존 코드 존중)을 일회성 제안이 아니라 프로젝트
공식 규칙으로 통합함. 새 섹션을 만들지 않고 기존 구조에 병합(v0.3.0→
v0.4.0): §1.2 Architecture First에 핵심 아키텍처 자산 보호 목록
(`EngineAdapter`/`AgentRegistry`/`WorkflowEngine`/`ProjectRepository`/
Workspace Core/Agent Runtime)과 "아키텍처 vs 단순함 충돌 시 아키텍처
우선" 규칙 추가. §4.2 Simplicity First에 최소 복잡성·점진적 확장·자문
질문 6개·금지 사항 목록 통합(YAGNI는 기존 내용과 중복이 커 별도 절 없이
소제목으로만 재확인). §4.3 Surgical Changes에 "기존 코드 존중" 추가.
신규 **§4.5 Cohesion**(응집도 우선, 기존 규칙에 없던 내용). §4 도입부에
4.1~4.5를 잇는 구현 순서 추가. `.ai/DECISIONS.md`에 `DX-02`로 기록(ADR
번호는 소비하지 않음, DX-01과 동일한 정책). 코드 변경 없음, 회귀 없음
확인(205개 테스트 통과). |
| 2026-07-25 | **T2-08 완료 & Milestone 2 종료: 사용자 승인**. 단순 산출물
검토가 아니라 **Milestone Retrospective**로 확장해 진행(사용자 제안).
목표/DoD 3개 항목 전부 달성 확인(상세는 위 T2-08 항목의 Retrospective
참고). "Milestone 2는 계획된 범위를 모두 완료했으며, 남은 항목은 M2
미완료가 아니라 M3 이상 확장 범위 또는 의도적 이월 부채"임을 명시적으로
선언(사용자 요청). 기술 부채를 **Deferred by Design**(#1 AgentManager/
Registry, #2 CLI 통합, #5 병렬성 검증)과 **Implementation Observation**
(#3 EventBus 발행 순서, #4 Event ID 생성 방식 불일치, #6 Step 미세분화
실행)로 성격 구분(사용자 제안). 아키텍처 변경 불필요 확인(T1-26 이후
ARCHITECTURE.md와 구현 일치 유지). 유지하기로 한 설계 5건과 이유 기록.
`docs/ROADMAP.md` Milestone 3 절에 "M3는 부채 청산이 아니라 Engine
Runtime/Adapter 구현이 목표이되, #1/#2/#5는 자연스럽게 포함 가능"이라는
문구 반영(사용자 제안). **Milestone 2(멀티 에이전트 코어) 종료.** 다음은
Milestone 3(실행 엔진 연동 & 상호작용) 착수 — 세부 Task는 착수 시점에
`T3-01`부터 정의. |
| 2026-07-25 | **M3-T01 완료: Engine Runtime 프로덕션 구현**(§2.4 Stage
Checkpoint 4개 경계 모두 발동. Analysis에서 Sonnet/Medium→**Sonnet/High**
상향 — 스레드 기반 Timeout/Cancel이라는 새 메커니즘 도입이라 판단, 이후
3개 경계는 "동일" 유지). `ManagedEngineRuntime`을 새 파일로 구현하고
T2-05의 `InMemoryEngineRuntime`은 전혀 수정하지 않음(상세 설계 근거는
위 M3-T01 항목 참고). DX-02 설계 철학 적용: 새 Interface 미생성(기존
`EngineRuntime`/`EngineAdapter`/`EventBus` 재사용), 새 Enum 미생성(기존
`EngineSessionStatus` 재사용), Multi Engine·병렬 실행 등 제외 범위는
정말로 구현하지 않고 TODO로도 남기지 않음(다음 Task 범위이므로). `ruff
check src tests`, `mypy src`, `pytest`(219개, 기존 205개 + 신규 14개)
모두 통과, 타이밍 테스트 5회 연속 안정성 확인. 다음 Task: **M3-T02**
(실제 Claude Code Adapter 연동 — 별도 준비된 계획 참고). |
| 2026-07-25 | **사용자가 M3-T01~T08 전체 개요 제공**("Engine Adapter &
Execution", ChatGPT 작성). `docs/ROADMAP.md`의 Milestone 3 절에 8개
Task 개요 반영. **M3-T02 완료: Claude Code Adapter**(§2.4 Stage
Checkpoint 4개 경계 모두 발동, 전부 Sonnet/High "동일" — M3-T01과 동일한
복잡도의 새 통합이라 판단). 로컬 `claude --help`로 실제 플래그를
확인하고, 사용자 승인 하에 `claude -p ... --output-format json`을 1회
실제 호출해 JSON 스키마를 검증함(추측 없이 1차 자료 확보). 상세 설계
근거는 위 M3-T02 항목 참고. `ClaudeCodeEngineAdapter`를 새 파일로 구현.
테스트 16개는 전부 `subprocess.run`을 mock 처리해 실제 프로세스 호출
없음. `ruff check src tests`, `mypy src`, `pytest`(235개, 기존 219개 +
신규 16개) 모두 통과. 다음 Task: **M3-T03**(Process Management —
`ProcessRunner`, Timeout 시 terminate/kill, Cancel, 종료 코드 관리). |
| 2026-07-25 | **M3-T03 완료: Process Management**(§2.4 Stage Checkpoint
4개 경계 모두 발동, 전부 Sonnet/High "동일"). `adapters/process_runner.py`
에 `ProcessRunner` 신규 구현, `ClaudeCodeEngineAdapter`를 이를 사용하도록
리팩터링(M3-T02에서 문서화해 둔 "cancel()이 실제 프로세스를 못 죽이는
한계" 해소). **버그 발견 및 수정**: `ClaudeCodeEngineAdapter.cancel()`이
`EngineAdapter` 계약("완료된 세션 상태 유지")을 위반하고 있었음을
발견해 수정. **자체 정정**: `ManagedEngineRuntime.cancel()`(M3-T01)도
같은 문제로 오판해 고치려 했으나, `EngineRuntime.cancel()` 계약은
애초에 "완료 상태 유지" 조항이 없어 원래 구현이 맞았음을 재확인하고
변경을 되돌림 — 두 인터페이스의 계약이 서로 다르다는 점을 놓칠 뻔한
사례로 정직하게 기록. `tests/adapters/test_process_runner.py`는
`sys.executable -c "..."`로 **실제(안전한) 프로세스**를 띄워 검증(정상
실행/Timeout 강제 종료/Cancel), `test_claude_code_engine_adapter.py`는
`subprocess.run` mock 대신 주입식 `FakeProcessRunner`로 전면 재작성.
`ruff check src tests`, `mypy src`, `pytest`(244개, 기존 235개 + 신규
9개) 모두 통과, 타이밍 테스트 5회 연속 안정성 확인. 다음 Task:
**M3-T04**(Session & Workspace Integration — WorkspaceCore↔
ManagedEngineRuntime 연결, EngineSession 생명주기, 실행 기록, EventBus
완전 연동). |
