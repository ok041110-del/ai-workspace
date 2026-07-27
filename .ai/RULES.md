# RULES — AI Workspace Rules

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.6.0 |
| 작성일 | 2026-07-27 |
| 적용 대상 | 이 저장소에서 작업하는 모든 AI 구현 엔진(Claude Code, Codex, Gemini CLI 등) 및 기여자 |

이 문서는 AI Workspace 프로젝트에서 **반드시 지켜야 하는 개발 규칙**을 정의한다.
아래 규칙은 사용자가 제시한 개발 철학을 프로젝트 내부 규정으로 명문화한 것이며,
모든 Task 수행 시 최우선으로 준수해야 한다.

> **v0.6.0 변경 (Branch Deletion 표준화, M24-T05)**: 신규 §8.5 Branch
> Deletion 추가. PR 병합 후 작업 브랜치 삭제는 GitHub의 "Automatically
> delete head branches" 기능에 위임하는 것을 표준으로 삼는다.
> `git push origin --delete`/`git branch -d`/`-D` 등 브랜치 삭제 명령을
> Claude Code Workflow에 포함하지 않는다 — 이 환경의 git 프록시에서
> `git push --delete`가 구조적으로 `403 Forbidden`을 반환해 신뢰할 수
> 없기도 하고, 2026-07-27 PR #6 실증 테스트로 GitHub 자동 삭제가 정상
> 동작함을 확인했기 때문이다. 자동 삭제가 동작하지 않는 경우에도 GitHub
> Actions 등 별도 자동화는 기본적으로 도입하지 않는다.
>
> **v0.5.0 변경 (GitHub Flow Migration, M24-T04)**: 신규 §8 Git Branch
> Strategy(GitHub Flow) 추가. 이 저장소는 2026-07-27부로 `main` 단일
> 상시 브랜치 + 짧은 수명 작업 브랜치(`feature/*`/`fix/*`/`docs/*`/
> `refactor/*`/`chore/*`) + Pull Request 기반 GitHub Flow를 공식
> 브랜치 전략으로 채택한다. 이전 세션들이 써 온 `claude/*` 브랜치명
> 패턴은 더 이상 쓰지 않는다 — Default Branch가 세션이 생성한 임시
> 브랜치명으로 고정되는 문제(Git Vault Sync 등 표준 Git 클라이언트와의
> 호환성 저해)가 실제로 발생해 바로잡았다(상세 경위는 `.ai/TASKS.md`의
> "GitHub Flow Migration" 절 참고).
>
> **v0.4.0 변경 (설계 철학 공식 채택, DX-02)**: Milestone 2 T2-07 진행 중
> 사용자가 제시한 설계 철학(Architecture First 강화·최소 복잡성·YAGNI·
> 점진적 확장·응집도·기존 코드 존중)을 프로젝트 영구 규칙으로 승격했다.
> 새 섹션을 만들지 않고 기존 규칙에 통합했다 — §1.2 Architecture First에
> 핵심 아키텍처 자산 보호와 "아키텍처 vs 단순함" 우선순위, §4.2 Simplicity
> First에 최소 복잡성·점진적 확장·자문 질문 체크리스트·금지 사항, §4.3
> Surgical Changes에 기존 코드 존중, 신규 §4.5 Cohesion에 응집도 원칙을
> 추가했다. YAGNI는 기존 §4.2 내용과 대부분 중복되어 별도 절 없이 §4.2
> 안에서 명시적으로 재확인만 했다. 상세 근거는 `.ai/DECISIONS.md`의
> `DX-02` 항목 참고.
>
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
- **핵심 아키텍처 자산은 단순화를 이유로 제거·우회하지 않는다.** `EngineAdapter`,
  `AgentRegistry`, `WorkflowEngine`, `ProjectRepository`, Workspace Core,
  Agent Runtime 등 `docs/ARCHITECTURE.md` §3에 정의된 컴포넌트·계층 경계는
  프로젝트의 설계 자산이다. **아키텍처와 단순함이 충돌하면 항상 아키텍처를
  우선한다** — "더 단순해 보인다"는 이유만으로 이런 경계를 지우거나 우회하지
  않는다(§4.2 Simplicity First와의 우선순위 관계).
- AI Workspace는 **프레임워크 프로젝트**다. 단순함(§4.2)은 아키텍처를 대체하는
  것이 아니라, 아키텍처를 더 명확하고 유지보수하기 쉽게 만드는 방향으로만
  작동해야 한다.

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
아래 4.1~4.5는 서로 독립된 규칙이 아니라 하나의 구현 순서로 이어진다.

**구현 순서**: 1) 기존 구현 검토(4.3) → 2) 가장 단순한 해결책 탐색(4.2) →
3) 아키텍처 준수 여부 확인(§1.2) → 4) 필요한 최소한만 구현(4.5) → 5) 검증
및 리팩터링(4.4, §2.3 Test Before Complete).

### 4.1 Think Before Coding
구현 전에 충분히 이해하고 판단한다.
- 요구사항을 추측하지 않는다.
- 가정을 명확하게 설명한다.
- 여러 해석이 가능하면 모두 제시한다.
- 더 단순한 해결 방법이 있다면 먼저 제안한다.
- 요구사항이 불명확하면 구현하지 않고 질문한다.

### 4.2 Simplicity First (최소 복잡성 · YAGNI · 점진적 확장)
같은 결과를 만들 수 있다면 항상 더 단순한 구현을 선택한다. 단, §1.2
Architecture First가 우선한다 — 단순함이 기존 아키텍처 경계와 충돌하면
아키텍처를 따른다.

**최소 복잡성**: 새로운 Class/Interface/Manager/Factory/Builder/Service/
Strategy/Helper/Utility를 만들기 전에 반드시 기존 구조로 해결 가능한지
먼저 검토한다(§4.3 기존 코드 존중과 연결). 새 파일 하나도 유지보수
비용이라는 점을 항상 고려한다.

**YAGNI**: 미래를 위한 기능은 구현하지 않는다. "나중에 필요할 수도 있다"는
이유만으로 구현하지 않는다. 현재 Task의 요구사항만 만족한다.
- 요청되지 않은 기능은 구현하지 않는다.
- 불필요한 추상화는 만들지 않는다.
- 미래를 위한 확장성은 요구사항이 있을 때만 추가한다.
- 사용되지 않는 설정이나 옵션은 만들지 않는다.
- 불필요한 예외 처리는 작성하지 않는다.

**점진적 확장**: 패턴이 명확해질 때까지 중복을 허용한다. 너무 이른
추상화(Early Abstraction)를 피한다 — 추상화는 실제 필요성이 여러 차례
확인된 이후에만 수행한다.

**새 컴포넌트를 만들기 전 자문 질문** (모두에 합리적인 이유가 있을 때만
새 구조를 추가한다):
- 기존 코드만 수정해서 해결 가능한가?
- 이 추상화가 지금 정말 필요한가?
- 실제 문제를 해결하는가?
- 유지보수 비용보다 얻는 이점이 큰가?
- 현재 Task의 범위를 벗어나지 않는가?
- 프로젝트 아키텍처(§1.2)와 일치하는가?

**금지 사항**: 미래를 위한 코드 작성 / 사용되지 않는 추상화 생성 /
불필요한 인터페이스 추가 / 과도한 디자인 패턴 적용 / 파일 수 증가를 위한
분리 / 하나의 Task에 여러 책임 추가(§4.5) / 프로젝트 아키텍처를 우회하는
구현(§1.2).

항상 최소한의 코드로 요구사항을 해결한다. 좋은 코드는 많은 코드가 아니라
**필요한 코드만 존재하는 코드**다.

### 4.3 Surgical Changes (기존 코드 존중)
필요한 부분만 수정한다. **새 코드를 작성하기 전에 항상 기존 구현을 먼저
검토한다** — 가능하면 기존 클래스 확장, 기존 함수 수정, 기존 구조 활용을
신규 작성보다 우선한다(§4.2 최소 복잡성과 직결).
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

### 4.5 Cohesion (응집도 우선)
하나의 컴포넌트는 하나의 책임만 가진다. 하나의 Task도 하나의 책임만
수행한다(§2.1 Task Driven Development, ADR-0022 "한 Task = 하나의
아키텍처 책임 경계"와 동일한 원칙을 코드 단위로 적용한 것).
- 필요하지 않은 기능은 현재 Task에 포함하지 않는다.
- 컴포넌트 하나가 여러 책임을 갖게 되면(예: 저장과 조회 로직이 승인 판단
  로직과 섞임) 책임 경계를 따라 분리를 검토한다 — 단, 분리 자체가 §4.2의
  "새 컴포넌트를 만들기 전 자문 질문"을 통과해야 한다.

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

---

## 8. Git Branch Strategy — GitHub Flow (M24-T04, 2026-07-27)

이 저장소는 **GitHub Flow**를 공식 브랜치 전략으로 따른다. `main` 하나만
상시 존재하는 안정 브랜치이며, 모든 작업은 짧은 수명의 작업 브랜치에서
진행한 뒤 Pull Request로 `main`에 합류한다.

### 8.1 Default Branch
- `main`이 이 저장소의 유일한 Default/상시 브랜치다.
- `main`은 항상 배포 가능한(정상 테스트를 통과하는) 상태를 유지한다.

### 8.2 작업 브랜치 생성 규칙
- 모든 작업 브랜치는 **항상 `main`에서** 새로 만든다(다른 작업 브랜치에서
  분기하지 않는다).
- 허용되는 브랜치 접두사(prefix):
  - `feature/*` — 새 기능
  - `fix/*` — 버그 수정
  - `docs/*` — 문서만 변경
  - `refactor/*` — 동작 변경 없는 리팩터링
  - `chore/*` — 빌드/설정/의존성 등 그 외 유지보수
- 금지되는 브랜치명:
  - `claude/*` — AI 세션이 자동 생성하는 임시 브랜치명 패턴. 과거 이
    패턴이 실수로 Default Branch 자리를 차지해 Git Vault Sync 등
    표준 Git 클라이언트와 호환성 문제를 일으킨 적이 있어(2026-07-27
    확인) 금지한다.
  - `develop` — Git Flow의 상시 통합 브랜치 개념. 이 저장소는 GitHub
    Flow(단일 `main`)를 쓰므로 존재해서는 안 된다.
  - `release/*`, `hotfix/*` — Git Flow 전용 브랜치 유형. 이 저장소의
    배포 모델에는 해당 개념이 없다.

### 8.3 Pull Request 및 Merge
- 작업 브랜치의 변경은 Pull Request를 통해서만 `main`에 반영한다.
- Merge 전 관련 테스트(`pytest`)와 `ruff`/`mypy`를 통과해야 한다(§2.3
  Test Before Complete).
- **Merge가 끝난 작업 브랜치는 삭제한다** — `main`에 이미 반영된 브랜치를
  계속 남겨 두지 않는다. 삭제 방식은 §8.5를 따른다.

### 8.4 AI 구현 엔진(Claude Code 등)에 대한 구속력
- 이 저장소에서 작업하는 모든 AI 세션은 새 작업을 시작할 때 `claude/*`
  형식의 브랜치를 만들지 않는다 — §8.2의 허용 접두사 중 작업 성격에
  맞는 것을 사용한다(예: 새 기능이면 `feature/*`, 문서 정리면 `docs/*`).
- 세션 환경이 기본적으로 `claude/*` 브랜치명을 자동 생성해 준다면, 그
  이름을 그대로 쓰지 않고 §8.2 접두사로 즉시 rename하거나 새 브랜치를
  만들어 전환한다.
- PR 없이 `main`에 직접 push하지 않는다(단, Fast-forward만으로 이력이
  정확히 일치함을 사전에 확인한 관리 작업은 예외로 다룰 수 있다 — 이
  경우에도 충돌 검증·테스트·보고 절차는 동일하게 따른다).

### 8.5 Branch Deletion (M24-T05, 2026-07-27)
- PR 병합 후 작업 브랜치 삭제는 **GitHub의 "Automatically delete head
  branches" 기능에 위임한다** — 이것이 표준이다(2026-07-27 PR #6으로
  실제 Squash Merge 후 자동 삭제가 동작함을 실증 확인).
- Claude Code(및 다른 AI 구현 엔진)는 `git push origin --delete`,
  `git branch -d`, `git branch -D` 등 브랜치 삭제 명령을 Workflow에
  포함하지 않는다. 이 환경의 git 프록시에서 `git push --delete`가
  구조적으로 `403 Forbidden`을 반환해 신뢰할 수 없기 때문이기도 하다.
- 자동 삭제가 동작하지 않는 경우(예: 과거 PR에서 실제로 미동작이
  관찰된 사례가 있었다) 원인을 조사하되, GitHub 네이티브 설정을
  우선 사용하는 방향을 유지한다. GitHub Actions 등 별도의 삭제
  자동화는 기본적으로 도입하지 않는다 — 브랜치 하나를 지우기 위해
  CI/CD를 신설하는 것은 과한 대응이다.
- 자동 삭제로 정리되지 않은 브랜치가 남아 있다면 삭제 여부와 방법을
  사용자에게 확인한 뒤 진행한다(GitHub 웹 UI 수동 삭제 등).

## 9. Obsidian Workspace Templates (Milestone 27, ADR-0038, 2026-07-27)

Obsidian Vault(이 저장소 root, `docs/ARCHITECTURE.md` §3.21)에
저장하는 모든 문서가 따르는 Template/Frontmatter/Tag/Wiki Link
규칙의 전체 원문은 Vault의 `00 System/AI_RULES.md`(Tag Rule/
Frontmatter Rule/Backlink Rule)와 `99 Templates/`에 있다 — 이
저장소 문서(RULES.md 등)는 그 규칙을 복사하지 않고 요약만 남긴다
(Vault → GitHub 반대 방향으로도 원문을 복제하지 않는 원칙,
`AI_RULES`의 "이 Vault가 아닌 것" 참고).

- **Task Template**: `14 Tasks/{task_id}.md` 1개 문서 = Task
  1건. Status/Priority/Milestone/Owner/Created/Updated/Checklist/
  Notes/Related Documents/Decision 섹션 + frontmatter(`tags:
  [task]`, `type: task`, `status`, `priority`, `milestone`,
  `owner`, `created`, `updated`). GitHub `.ai/TASKS.md`(이 문서의
  Task List/DoD/완료 write-up)를 대체하지 않는다 — 원문은 여전히
  `.ai/TASKS.md`, Vault 쪽은 실시간 상태 보기/갱신용.
- **Daily Note Template**: `13 Daily/{date}.md`. 오늘 작업/
  진행중/완료/문제/결정사항/내일 계획.
- **Decision Template**: `99 Templates/Template - Decision.md`.
  Problem/Options/Decision/Reason/Impact + frontmatter(`type:
  decision`, `status`, `milestone`, `created`, `updated`). ADR로
  승격되기 전 가벼운 판단 기록용, ADR과 별도(`.ai/DECISIONS.md`).
- **Workspace(Project) Template**: `99 Templates/Template -
  Project Workspace.md`에 `Projects/<이름>/README.md, Tasks/,
  Notes/, Meetings/, Decisions/, Archive/` 표준 구조를 정의하되,
  이 Vault가 아직 단일 Project(자기 자신)만 다루므로 지금
  인스턴스화하지 않는다(YAGNI, 두 번째 Project가 생길 때 적용).
- **Tag Rule 확장**: `#task`/`#meeting`/`#bug`/`#feature`/
  `#research`/`#daily`.
- **Frontmatter Rule**: 상태를 갖는 문서(Task/Decision)는
  `type`/`status`/`priority`/`milestone`/`created`/`updated`를
  frontmatter에 둔다. 상태 개념이 없는 문서(Daily 등)는 `tags`만
  으로 충분하다.
