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

---

## Milestone 4 — 자동화 및 확장 (Automation & Scale)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 4 Definition of Done" 참고.
> 세부 Task(`T4-01`부터)는 Milestone 3 완료 승인 이후, 착수 시점에 이 문서에
> 추가한다. 예정 작업 영역은 `docs/ROADMAP.md`의 "Milestone 4" 섹션 참고
> (자동화·다중 프로젝트·메모리 고도화).

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
