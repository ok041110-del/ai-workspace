# Skill: MDD Review (Minimal Design Decision Review)

## 1. 목적
이 Skill의 목적은 Milestone 구현에 착수하기 전, "어떻게 구현할 것인가"가 아니라
**"새로운 코드가 정말 필요한가"**를 검증하는 것입니다. 새로운 코드보다 기존
Architecture(Domain Model/Interface/Service/Adapter)를 최대한 활용하는 것을
우선하여, Milestone이 거듭될수록 코드와 아키텍처가 불필요하게 증가하는 것을
억제합니다.

## 2. 사용 시점
- Milestone 계획(범위·DoD)이 사용자 승인을 받은 직후, Task Planning(T01~T0n
  개별 Task 계획 수립) 착수 전
- 새 Interface/Service/Adapter/Layer 도입이 논의될 때
- "새 파일을 만들어야 하나?"라는 의문이 드는 모든 시점

**흐름**
```
Milestone 계획 승인
      │
      ▼
MDD Review (필수 게이트)
      │
      ▼
사용자 승인
      │
      ▼
T01 ~ T0n 구현 (Task Planning → Task Implementation)
      │
      ▼
Milestone Review
      │
      ▼
PR → Merge
```

## 3. 입력
- **대상 Milestone 범위·DoD**: `docs/ROADMAP.md`, `.ai/TASKS.md`
- **기존 구조 전수 검색 대상**: Domain Model, Value Object, Service, Analyzer,
  Adapter, Repository, Utility, Markdown Renderer, Vault Writer, Report
  Model, Test Helper (`src/` 전체)
- **아키텍처 제약**: `docs/ARCHITECTURE.md`
- **적용 규정**: `.ai/RULES.md` §1.2 Architecture First, §4.2 Simplicity
  First(YAGNI)

## 4. 원칙 — 항상 아래 순서를 따른다
1. 정말 필요한 기능인가? (YAGNI)
2. 이미 프로젝트에 같은 기능이 있는가? (Reuse First)
3. 기존 Interface로 해결 가능한가? (Interface First)
4. 기존 Service를 확장할 수 있는가? (Service Reuse)
5. 기존 Adapter를 확장할 수 있는가? (Adapter Reuse)
6. 새로운 Layer(Engine/Manager/Factory/Registry/Strategy)가 정말 필요한가?
7. 그때만(6단계까지 모두 막힌 경우에만) 최소 코드를 작성한다.

## 5. 작업 절차

### 5.1 Scope Review
- Scope에 포함되는가?
- DoD를 만족하기 위해 반드시 필요한가?
- 미래를 위한 코드(YAGNI 위반)는 아닌가?
- Scope 밖 기능은 구현하지 않는다.

### 5.2 Reuse Review
- 프로젝트 전체(Domain Model/Value Object/Service/Analyzer/Adapter/
  Repository/Utility/Markdown Renderer/Vault Writer/Report Model/Test
  Helper)를 우선 검색한다.
- 이미 존재하는 기능으로 해결 가능하면 새로운 코드를 작성하지 않는다.
- 반드시 "무엇을 재사용하는가"를 명시한다.

### 5.3 Interface Review
- 새 Interface가 정말 필요한가? 가능하면 기존 Interface 사용/확장으로
  해결한다.
- 새 Interface는 기존 Interface로 해결할 수 없는 경우에만 허용한다.

### 5.4 Service Review
- 새 Service를 만들기 전에 기존 Service를 조합하거나 메서드 추가만으로
  해결 가능한지 검토한다.
- 반드시 기존 Service 재사용 가능성을 먼저 설명한다.

### 5.5 Adapter Review
- 새 Adapter를 만들기 전에 기존 Adapter 확장(`publish_xxx()` 메서드 추가 등)
  으로 해결 가능한지 검토한다.
- 새 Adapter는 기존 Adapter로 해결할 수 없는 경우에만 허용한다.

### 5.6 Layer Review
- 새로운 Layer/Engine/Manager/Factory/Registry/Strategy 추가가 정말
  필요한가? 기존 Layer 안에서 해결 가능한지 먼저 검토한다.
- Architecture 변경은 최후의 선택이다(§1.2 Architecture First와 동일한
  Approval Required 대상).

### 5.7 File Review
- 새 파일이 필요한 경우, 각 파일마다 왜 새 파일이 필요한지 설명한다.
- 검토 대상: 기존 파일 확장 가능 여부, 기존 클래스 확장 가능 여부, 기존
  Renderer 재사용 가능 여부, 기존 Writer 재사용 가능 여부.
- 새 파일은 기존 파일 수정으로 해결할 수 없을 때만 허용한다.

### 5.8 Minimal Implementation
- 위 모든 검토를 통과한 경우에만 새 코드를 작성한다.
- 새 코드 역시 최소 클래스·최소 함수·최소 파일·최소 변경·최소 의존성
  원칙을 따른다.

## 6. 출력 형식

```
## MDD Review

### Scope Review
- Scope 적합 여부
- YAGNI 검토 결과

### Reuse Review
재사용 가능한 구성요소
- ...
재사용 전략
- ...

### Interface Review
- 기존 Interface 활용 여부
- 신규 Interface 필요 여부

### Service Review
- 기존 Service 활용 방법
- 신규 Service 필요 여부

### Adapter Review
- 기존 Adapter 활용 방법
- 신규 Adapter 필요 여부

### Layer Review
- Layer 영향
- Architecture 변경 여부

### File Review
| 파일 | 기존 수정 가능 | 신규 필요 | 이유 |
|------|---------------|----------|------|

### Minimal Implementation Plan
새로 추가되는 파일/클래스/함수/메서드 목록과, 각각 "왜 기존 코드로 해결할
수 없는가"를 설명한다.
```

### 최종 결정
다음 중 하나를 선택하고 근거를 설명한다.
- ✅ 기존 구조 확장
- ✅ 최소 코드 추가

## 7. 수행 원칙
- **Approval Required**: MDD Review는 Milestone 계획 승인과 Task 구현 착수
  사이의 필수 게이트다. 사용자 승인 없이 Review를 건너뛰고 구현에 들어가지
  않는다(`.ai/RULES.md` §1.4).
- **Repository First**: 재사용 가능성 판단은 실제 저장소 검색(Grep/코드 읽기)
  결과에 근거하며, 추측으로 "없을 것"이라 단정하지 않는다.
- **최종 목표**: 코드를 많이 작성하는 것이 아니라, 기존 Architecture를 최대한
  활용하여 가장 작은 변경으로 요구사항을 만족하는 것이다.
- MDD Review가 끝난 후에만 구현을 시작한다. 구현 중에도 더 단순한 방법이
  발견되면 기존 설계를 수정하고 불필요한 코드를 제거한다.

## 8. 금지 사항
- **재사용 검토 생략 금지**: 기존 Domain Model/Interface/Service/Adapter
  검색 없이 곧바로 새 코드 작성을 제안하지 않는다.
- **Scope 확장 금지**: Milestone DoD에 없는 기능을 "미래 대비"라는 이유로
  함께 구현하지 않는다(YAGNI).
- **승인 생략 금지**: Interface/Service/Adapter/Layer 신설이 필요하다고
  판단되어도, 사용자 승인 없이 바로 구현에 들어가지 않는다.
