# Smart Model Router — 사용 예시 모음

`SKILL.md`의 §A/§B 규칙을 적용한 결과 예시다. 전체 `## Task Analysis`
형식이 아니라 핵심 결론만 압축한 표로 정리했다(토큰 최소화 원칙).
새로운 사례를 판단할 때 가장 비슷한 행을 찾아 대조하는 용도로 쓴다.

| # | 작업 설명 | Task Type | Scope | Recommended Model | Recommended Effort | 핵심 이유 |
|---|---|---|---|---|---|---|
| 1 | README에 설치 방법 섹션 추가 | Documentation | 파일 | Haiku | Minimal | 정형적 문서 추가, 추론 불필요 |
| 2 | 함수에 docstring/주석 작성 | Documentation | 함수 | Haiku | Minimal | 설명 작성만, 로직 변경 없음 |
| 3 | ruff가 지적한 line-length 위반 수정 | Formatting | 파일 | Haiku | Low | 기계적 포맷 수정 |
| 4 | 특정 함수가 정의된 파일 찾기 | Research | - | Haiku | Minimal | 단순 검색 |
| 5 | pytest 실행 후 실패 목록만 보고 | Testing | - | Haiku | Minimal | 실행+결과 요약, 판단 없음 |
| 6 | 기존 테스트에 케이스 1개 추가(해피 패스) | Testing | 파일 | Haiku | Low | 기존 패턴 그대로 복제 |
| 7 | ADR 문서 오탈자·띄어쓰기 정리 | Documentation | 파일 | Haiku | Minimal | 내용 변경 없는 교정 |
| 8 | 특정 라이브러리 API 시그니처 확인 | Research | - | Haiku | Low | 단순 조회성 리서치 |
| 9 | TODO 주석 목록 정리 | Documentation | 여러 파일 | Haiku | Minimal | 정리 작업, 판단 최소 |
| 10 | 이 클래스가 하는 일을 설명해 달라는 요청 | Review | 클래스 | Haiku | Low | 기존 코드 설명, 변경 없음 |
| 11 | 단일 함수의 버그 수정 | Debugging | 함수 | Sonnet | Medium | 원인 파악에 일반 추론 필요 |
| 12 | 신규 CLI 서브커맨드 1개 추가 | Implementation | 파일 | Sonnet | Medium | 표준적인 신규 기능 구현 |
| 13 | 새 Interface의 Fake 구현체 + 계약 테스트 작성 | Testing | 파일 | Sonnet | Medium | 기존 패턴을 따르는 구현+테스트 |
| 14 | Workspace Core 골격에 세션 관리 로직 구현 | Implementation | 파일 | Sonnet | Medium | 기존 Interface를 소비하는 구현 |
| 15 | PR 하나에 대한 코드 리뷰 | Review | 여러 파일 | Sonnet | Medium | 표준 코드 리뷰, 구조 변경 없음 |
| 16 | 긴 함수를 여러 함수로 분리(리팩터링) | Refactoring | 함수 | Sonnet | Medium | 동작 보존 리팩터링 |
| 17 | 여러 파일에 걸친 회귀 버그 원인 추적·수정 | Debugging | 여러 파일 | Sonnet | High | 원인이 여러 파일에 걸쳐 있어 깊은 추적 필요 |
| 18 | 특정 모듈의 핫패스 성능 최적화 | Refactoring | 모듈 | Sonnet | High | 트레이드오프 분석 필요하나 모듈 경계는 유지 |
| 19 | 여러 파일에 테스트 커버리지 보강 | Testing | 여러 파일 | Sonnet | Medium | 반복적이나 규모가 있는 표준 작업 |
| 20 | 기존 설계 결정이 여전히 유효한지 재검토(변경 없음 결론 포함) | Review | 프로젝트 전체 | Sonnet | High | 폭넓게 훑어봐야 하나 새 설계 결정은 아님 |
| 21 | 여러 모듈에 걸친 대규모 리팩터링(구조는 유지, 코드만 정리) | Refactoring | 여러 모듈 | Sonnet | High | 범위는 크지만 경계·책임 변경은 없음 |
| 22 | Milestone 다음 단계 세부 Task 목록 초안 작성 | Planning | 프로젝트 전체 | Sonnet | Medium | 기존 원칙(ADR-0022 등)을 적용하는 정형적 계획 |
| 23 | 여러 Provider의 LLM 비교 조사 정리 | Research | - | Sonnet | Medium | 종합·비교 판단이 들어가는 리서치 |
| 24 | Agent Runtime ↔ Engine Runtime 의존 방향 재설계 + ADR 작성 | Architecture | 여러 모듈 | Opus | Maximum | 컴포넌트 책임 경계 변경 + ADR 수준 결정 |
| 25 | 여러 Interface의 계약을 동시에 재설계 | Architecture | 여러 모듈 | Opus | Maximum | 여러 컴포넌트의 계약 자체를 바꿈 |
| 26 | 프로젝트 디렉터리/패키지 구조 전면 개편 | Architecture | 프로젝트 전체 | Opus | Maximum | 프로젝트 전체 구조 변경 |
| 27 | 신규 스케줄링 알고리즘 설계(다중 제약 최적화) | Implementation | 모듈 | Opus | High | 복잡한 알고리즘 설계, 다단계 추론 필요 |
| 28 | Milestone→Task 거버넌스 체계 자체를 다시 바꾸는 결정 | Planning | 프로젝트 전체 | Opus | Maximum | 프로젝트 운영 방향을 바꾸는 ADR 수준 결정 |

## 표를 읽는 법

- **Model이 같아도 Effort가 다른 사례**를 비교해보면(#11 vs #17, #12 vs #21)
  "모델을 올리기 전에 Effort를 올릴 수 있는지 먼저 검토한다"(SKILL.md
  A-2 원칙 4)가 실제로 어떻게 적용되는지 알 수 있다 — Scope가 커져도
  모듈 경계가 그대로면 Model은 Sonnet에 머무르고 Effort만 오른다.
- **#20, #24를 비교**하면 "프로젝트 전체를 훑어보는 작업"이라고 해서
  자동으로 Opus가 되는 것이 아님을 알 수 있다. #20은 범위는 넓지만 결론이
  "기존 결정 유지"인 검토이고, #24는 실제로 설계를 바꾸고 ADR을 쓰는
  작업이라 Opus 조건(§B-1)을 충족한다.
