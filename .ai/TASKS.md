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
| M17-T02 | `EngineSelectionPolicy` Interface + `InMemoryEngineSelectionPolicy`(Budget 내 최저 비용 우선) | 진행 예정 |
| M17-T03 | End-to-End 통합 테스트(다중 Engine 후보 선택 + 실행과의 비연결 증명) | 진행 예정 |
| M17-T04 | 문서화 + Milestone 17 Review | 진행 예정 |

**진행 상태**: M17-T01 완료. M17-T02 진행 중.

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
