# RULES — AI Workspace Rules

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.3.0 |
| 작성일 | 2026-07-25 |
| 적용 대상 | 이 저장소에서 작업하는 모든 AI 구현 엔진(Claude Code, Codex, Gemini CLI 등) 및 기여자 |

이 문서는 AI Workspace 프로젝트에서 **반드시 지켜야 하는 개발 규칙**을 정의한다.
아래 규칙은 사용자가 제시한 개발 철학을 프로젝트 내부 규정으로 명문화한 것이며,
모든 Task 수행 시 최우선으로 준수해야 한다.

> **v0.3.0 변경 (DX-01, `.ai/DECISIONS.md` 참고)**: §2.4 Stage Checkpoint를 신규 추가했다 —
> Task 내부 4개 작업 단계(Analysis/Implementation/Validation/Task 완료)
> 경계마다 Smart Model Router를 실행해 Recommendation(model/effort/
> confidence/reason)을 산출하고, 사용자 승인 없이는 Model/Effort를 자동
> 전환하지 않는다. "Stage"라는 이름을 쓴 것은 ADR-0021에서 이미 폐지된
> 프로젝트 관리 계층 "Phase"와의 혼동을 피하기 위함이다. §5.1 언어 규칙을
> 세션 중 사용자에게 보이는 모든 메시지로 확장했다.
>
> **v0.2.1 변경**: Phase 계층 폐지(ADR-0021)에 따라 §1.4 승인 항목의 "Phase
> 완료"를 "Milestone 완료"로, §5.3 커밋 메시지 예시를 `[PhaseN][Pn-x]`에서
> `[Mn][Tn-xx]`로, §7의 Task ID 참조를 갱신했다.
>
> **v0.2.0 변경**: 규칙 체계를 4개 그룹(Project Principles / Development Workflow /
> Context Loading Rules / LLM Coding Rules)으로 재구성하고, `Interface First`,
> `Context Loading Rules`, `LLM Coding Rules`를 추가했다. 기존 언어·코딩·커밋
> 규칙은 §5 공통 규칙으로 보존했다.

---

## 1. Project Principles (프로젝트 원칙)

### 1.1 Documentation First (문서 우선)
- 어떤 기능이든 구현 코드를 작성하기 전에 관련 문서(PRD, ARCHITECTURE 등 해당하는
  문서)를 먼저 작성하거나 갱신한다.
- 문서와 실제 구현이 어긋나는 상태를 방치하지 않는다. 구현이 바뀌면 문서도 같은
  Task 안에서 함께 갱신한다.

### 1.2 Architecture First (아키텍처 우선)
- 새로운 컴포넌트나 모듈을 추가하기 전에 `docs/ARCHITECTURE.md`에 구조와 의존성
  규칙을 먼저 반영한다.
- 기존 아키텍처의 의존성 규칙(ARCHITECTURE.md §7)을 위반하는 구현은 허용하지
  않는다. 위반이 불가피하다면 아키텍처 변경으로 간주하고 승인을 받는다.

### 1.3 Interface First (인터페이스 우선)
- 컴포넌트 간 협력은 구체 구현이 아니라 **인터페이스(추상 계약)**를 통해
  이루어진다 (ADR-0005).
- 구현 전에 인터페이스를 먼저 정의하며, 인터페이스에는 메서드 시그니처뿐 아니라
  **계약(입력 · 출력 · 예외 · 보장 사항)**까지 명시한다.
- Workspace Core를 비롯한 상위 컴포넌트는 구체 클래스를 직접 참조하지 않고
  인터페이스에만 의존한다.

### 1.4 Approval Required (승인 필요 — 아키텍처 변경 등 4가지 행위)
다음 4가지 행위는 **반드시 사용자 승인을 받은 후에만** 진행한다.

1. 아키텍처 변경 (Architecture Change)
2. 새로운 기능 추가 (New Feature)
3. 리팩토링 (Refactoring)
4. Milestone 완료 (Milestone Completion) — 2026-07-24 ADR-0021로 "Phase 완료"에서
   변경됨. Phase 계층이 폐지되면서 승인 지점이 Milestone 단위로 일원화되었다.

승인 요청 시에는 다음을 함께 제시한다.
- 무엇을 변경/추가하려 하는지
- 왜 필요한지 (이유)
- 대안은 무엇이 있었는지, 왜 이 방법을 선택했는지 (장단점 포함)

---

## 2. Development Workflow (개발 워크플로우)

### 2.1 Task Driven Development (Task 단위 개발)
- 모든 작업은 `.ai/TASKS.md`에 정의된 Task 단위로 수행한다.
- Task 없이 임의로 코드를 작성하지 않는다. 새로운 작업이 필요하면 먼저 Task를
  정의한 뒤 진행한다.

### 2.2 One Task At A Time (한 번에 하나)
- 동시에 여러 Task를 병행하지 않는다.
- 하나의 Task를 완료(또는 명시적으로 보류)한 뒤에만 다음 Task로 넘어간다.

### 2.3 Test Before Complete (완료 전 테스트)
- Task를 "완료" 상태로 표시하기 전에 반드시 관련 테스트를 실행하고 통과 결과를
  확인한다.
- 테스트가 없는 영역에 대한 신규 기능은, 해당 Task 범위 안에서 최소한의 테스트를
  함께 작성한다.

### 2.4 Stage Checkpoint (DX-01)
Task는 내부적으로 4개 **Stage** 경계를 가지며, 각 Stage가 끝날 때마다 Smart
Model Router(`.claude/skills/smart-model-router`)를 실행해 다음 작업에 적합한
Model/Effort를 점검한다. **"Stage"는 ADR-0021에서 폐지된 프로젝트 관리 계층
"Phase"(`Milestone → Phase → Task`)와는 다른 개념**이며, 하나의 Task 내부
작업 단계 경계만을 가리킨다.

**Stage 4단계** (`.ai/skills/Task-Planning.md`/`Task-Implementation.md`의
작업 절차와 대응한다)
1. **Analysis 완료** — `Task-Planning.md`의 계획서 작성 완료 직후, 구현 착수 전.
2. **Implementation 완료** — `Task-Implementation.md` §5.1~5.3(테스트 작성/
   구현/범위 관리) 완료 직후, §5.4(검증) 착수 전.
3. **Validation 완료** — `Task-Implementation.md` §5.4(pytest/ruff/mypy)
   통과 직후, §5.5(문서화) 착수 전.
4. **Task 완료** — `Task-Implementation.md` §5.5~5.6(문서화/상태 확정) 및
   커밋 완료 직후, 다음 Task 착수 전 (Documentation과 Report는 하나의
   Checkpoint로 묶는다).

**흐름**
```
Stage Checkpoint
      │
      ▼
Smart Model Router (다음 작업 · 난이도 · 비용 · 토큰 분석)
      │
      ▼
Recommendation (model, effort, confidence, reason)
      │
      ▼
Manual Recommendation Executor (현재)
      │
      ▼
한국어 UI 표시 → 사용자 선택 → (필요 시) `/model` 안내 후 대기
```

**Recommendation**: Smart Model Router는 스스로 실행하지 않고 판단 결과만
아래 구조로 반환한다. 지금 단계에서는 **문서화된 개념적 스키마**이며, 실제
Python 구현(`domain/llm_policy.py` 확장 등)은 Task Driven Development 원칙에
따라 별도 Task 없이 지금 만들지 않는다 — §7 Temporary LLM Policy의 M2 이후
로드맵에서 다룬다.
```
Recommendation(
    model: str,        # 예: "Sonnet"
    effort: str,        # 예: "High"
    confidence: float,  # 0.0~1.0
    reason: str,         # 추천 사유
)
```

**3가지 결과 처리** (Model/Effort는 어떤 경우에도 자동 전환하지 않는다)
- **동일** — 현재 Model/Effort와 추천이 같으면 자동으로 다음 작업을 진행한다.
- **상향 필요** — 추천이 현재보다 높으면 진행을 멈추고 사용자에게 모델 변경
  여부를 질문한다. "예"를 선택하면 `/model`로 전환 후 계속 진행해 달라고
  안내하고 대기한다.
- **하향 가능** — 추천이 현재보다 낮으면 "현재 설정 유지" 또는 "추천
  Model/Effort로 변경" 중 사용자가 선택하게 한다.

**Skip Rule**: 다음 중 하나라도 해당하면 박스 UI 없이 한 줄만 출력하고
자동 진행한다 (불필요한 중단을 막기 위함).
- 직전 Stage의 Recommendation과 동일한 경우
- 현재 Model/Effort가 이미 추천과 일치하는 경우
- 연속된 Stage에서 변경 권고가 없었던 경우

표시 문구 예: "현재 Model/Effort가 다음 작업에도 적합합니다. 계속
진행합니다."

**미래 확장 (Auto Recommendation Executor)**: Milestone 3에서 Engine
Runtime/Engine Adapter가 완성되면 `Manual Recommendation Executor`(사용자
선택 대기)만 `Auto Recommendation Executor`(Engine Runtime을 통한 자동
선택·실행)로 교체한다. Stage Checkpoint, Smart Model Router, Recommendation
구조, 추천 알고리즘, 한국어 UI 정책은 그대로 재사용한다 — §7 Temporary LLM
Policy의 M2(Rule 기반 선택)~M5(Self Optimizer) 로드맵과 연결된다.

---

## 3. Context Loading Rules (컨텍스트 로딩 규칙)

작업에 필요한 최소한의 맥락만 불러온다. 불필요하게 많은 파일을 읽는 것은 오류와
비용을 늘린다.

### 3.1 최소 Context만 로드
- 지금 Task에 직접 필요한 맥락만 로드한다.
- 매 Task마다 우선 참조하는 문서는 `.ai/TASKS.md`(무엇을)와 `.ai/RULES.md`
  (어떻게)이며, `.ai/MEMORY.md`는 필요할 때만 조회한다.

### 3.2 필요한 파일만 읽기
- 관련 없는 파일을 광범위하게 읽지 않는다.
- 수정 대상과 그 직접적인 의존 관계에 있는 파일만 읽는다.

### 3.3 Incremental 변경
- 한 번에 저장소 전체를 바꾸지 않고, 작은 단위로 점진적으로 변경한다.
- 각 변경은 검증 가능한 단위여야 하며, 이전 상태로 되돌리기 쉬워야 한다.

---

## 4. LLM Coding Rules (구현 엔진 코딩 규칙)

모든 구현 엔진(Claude Code, Codex, Gemini CLI 등)은 다음 원칙을 반드시 준수한다.

### 4.1 Think Before Coding
구현 전에 충분히 이해하고 판단한다.
- 요구사항을 추측하지 않는다.
- 가정을 명확하게 설명한다.
- 여러 해석이 가능하면 모두 제시한다.
- 더 단순한 해결 방법이 있다면 먼저 제안한다.
- 요구사항이 불명확하면 구현하지 않고 질문한다.

### 4.2 Simplicity First
가장 단순한 해결책을 선택한다.
- 요청되지 않은 기능은 구현하지 않는다.
- 불필요한 추상화는 만들지 않는다.
- 미래를 위한 확장성은 요구사항이 있을 때만 추가한다.
- 사용되지 않는 설정이나 옵션은 만들지 않는다.
- 불필요한 예외 처리는 작성하지 않는다.

항상 최소한의 코드로 요구사항을 해결한다.

### 4.3 Surgical Changes
필요한 부분만 수정한다.
- 관련 없는 리팩터링을 하지 않는다.
- 관련 없는 코드 개선을 하지 않는다.
- 기존 스타일을 유지한다.
- 자신의 변경으로 인해 발생한 미사용 코드만 정리한다.
- 기존 Dead Code는 삭제하지 않고 보고만 한다.

모든 변경은 사용자의 요청과 직접 연결되어야 한다.

### 4.4 Goal-Driven Execution
구현보다 검증 가능한 목표를 먼저 정의한다. 예를 들어,
- 버그 수정 → 재현 테스트 작성 후 수정
- Validation 추가 → 실패 테스트 작성 후 통과
- 리팩터링 → 변경 전후 테스트 통과 확인

여러 단계 작업은 항상 **1) 작업 → 2) 검증** 형태로 계획을 수립한다.
완료는 반드시 테스트와 검증으로 확인한다.

---

## 5. 공통 규칙 (Common Conventions)

### 5.1 언어 규칙
- 모든 문서, 설명, 작업 계획, 주석, 커밋 메시지는 **한국어**로 작성한다.
- 단, 변수명·함수명·클래스명·파일명은 Python 표준 관례(PEP 8)에 따라 **영어**를
  사용한다.
  - 변수/함수: `snake_case`
  - 클래스: `PascalCase`
  - 상수: `UPPER_SNAKE_CASE`
  - 파일/모듈: `snake_case.py`
- AI 구현 엔진이 세션 중 사용자에게 표시하는 모든 메시지(진행 상황, 질문,
  완료 보고, 추천 결과, 오류 안내, 승인 요청, §2.4 Stage Checkpoint의 Smart
  Model Router 결과 포함)도 **한국어**로 작성한다(DX-01). 단, 기술
  용어(Model, Effort, pytest, ruff, mypy, Commit Message, API 등)와
  클래스명·함수명·파일명은 원문을 유지한다.

### 5.2 Python 코딩 규칙
- PEP 8을 기본 스타일 가이드로 따른다.
- 모든 공개 함수/메서드에는 타입 힌트(type hint)를 사용한다.
- 불필요한 추상화, 과도한 방어적 코드, 발생하지 않는 상황에 대한 예외 처리를
  추가하지 않는다 (YAGNI, §4.2와 일관).
- 주석은 "왜(why)"가 비직관적인 경우에만 작성하고, "무엇(what)"을 설명하는
  주석은 지양한다 (식별자 이름으로 대체한다).

### 5.3 커밋 메시지 규칙
- 커밋 메시지는 한국어로 작성한다.
- 형식 예시: `[M1][T1-14] Project 도메인 모델 정의` (2026-07-24 ADR-0021로 Phase
  계층이 폐지되어 `[PhaseN][Pn-x]` 형식에서 `[Mn][Tn-xx]` 형식으로 변경됨)
- 하나의 커밋은 하나의 Task(또는 Task의 명확한 하위 단위)에 대응한다.

### 5.4 이유 설명 (Explain Reasoning)
- 기술 선택, 설계 결정, 구조 변경에는 항상 선택 이유 · 설계 이유 · 장단점 ·
  검토했던 대안을 함께 설명한다.
- 이유 없는 결정, 근거 없는 코드 변경은 지양한다.

---

## 6. 승인 프로세스와 문서 연동

- 승인이 필요한 4가지 행위(§1.4)가 승인되면, 그 결정과 근거를 `.ai/DECISIONS.md`에
  ADR(Architecture Decision Record) 형식으로 기록한다.
- 승인 결과(승인/반려)와 사유는 `.ai/TASKS.md`의 해당 Task 항목에도 반영한다.

---

## 7. Temporary LLM Policy (임시 LLM 정책)

Agent가 어떤 LLM Provider/Model을 어느 Effort로 사용할지 결정하는 정책은 아직
자동화되어 있지 않다. 2026-07-23 T1-16(당시 ID: P1-4)에서 `LLMProvider`,
`LLMModel`, `LLMEffort` **Domain만** 초안으로 정의했으며, 실제 선택 로직(Policy
Engine, Router 등)은 존재하지 않는다.

### 현재 상태
- 현재는 **문서 기반 정책**만 존재한다 (`docs/llm_policy.example.yaml` 참고).
- 현재는 **사람이 정책을 따른다**. 즉, 어떤 역할에 어떤 Provider/Model/Effort를
  쓸지는 이 문서와 예시 YAML을 참고해 사람이 직접 판단하고 적용한다.
- `domain/llm_policy.py`에는 `LLMProvider`, `LLMModel`, `LLMEffort`와 초기
  모델 목록(`INITIAL_MODELS`)만 존재하며, 이를 소비하는 Policy Engine이나
  Router는 아직 구현되지 않았다.

### 향후 진행 경로 (Milestone별)
- **M2**: Rule 기반 선택을 구현한다 (조건-값 매핑 수준의 단순 규칙).
- **M3**: Agent가 Policy를 참조한다 (Agent 실행 시 정책 문서/규칙을 조회해 사용).
- **M4**: Policy Engine이 자동으로 선택한다 (상황에 따라 Provider/Model/Effort를
  자동 결정).
- **M5**: Self Optimizer가 Policy를 자동으로 최적화한다 (실행 결과 피드백을
  바탕으로 정책 자체를 개선).

### 관련 문서
- Domain 정의: `src/ai_workspace/domain/llm_policy.py`
- 정책 초안(YAML 예시): `docs/llm_policy.example.yaml`

이 섹션은 정책이 실제로 자동화되기 전까지 "임시"임을 나타내며, M2 이후 각
Milestone에서 해당 단계의 구현이 완료되면 이 섹션과 진행 경로를 갱신한다.

**§2.4 Stage Checkpoint와의 관계**: DX-01(§2.4)은 이 로드맵이 자동화되기 전
단계에서, Claude Code 세션 수준에서 Model/Effort를 사람이 점검·선택하도록
돕는 **Manual Recommendation Executor**다. M3에서 Engine Runtime/Engine
Adapter가 완성되면 실행기만 Auto Recommendation Executor로 교체되며,
Recommendation 구조와 추천 알고리즘은 그대로 이어진다.
