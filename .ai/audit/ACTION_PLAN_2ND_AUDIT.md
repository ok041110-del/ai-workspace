# AI Workspace — 2차 독립 재감사 실행 계획 (Action Plan)

**기준 문서**: AI Workspace 2차 독립 재감사 보고서(Baseline Audit), `.ai/audit/AWAS.md`
**성격**: 이 문서는 감사가 아니다. 이미 확정된 Finding 6건(P1×3, P2×2, P3×1)을 실행 가능한 개발 작업으로 변환한 것이다. 새 Finding, 새 결론, AWAS 수정은 포함하지 않는다.

---

## 1. Executive Summary

2차 감사가 확정한 Finding 6건 중 3건(P1)은 "즉시 코드를 고치는 작업"이 아니라 **정책/도구를 먼저 세우는 작업**이라는 공통점이 있다 — 리뷰 게이트 부재, EngineRuntime 성장, README 정체는 모두 "규율이 없어서" 생긴 문제이지 "버그가 있어서" 생긴 문제가 아니다. 따라서 이 실행 계획의 핵심 판단은: **코드 리팩터링(Finding 2의 근본 해결)을 먼저 하지 않는다.** 대신 그 성장을 통제할 정책과 게이트(Finding 1, 5)를 먼저 세우고, 정책이 실제로 작동하는 것을 관찰한 뒤 리팩터링 여부를 재판단한다. Finding 3, 6은 30분 내 끝나는 Quick Win이며 선행 조건 없이 지금 바로 처리 가능하다. Finding 4는 배포 시나리오가 확인되지 않은 상태(감사 보고서의 "확인되지 않음")이므로 지금 코드를 고치지 않고 정책 수립 단계로만 남긴다.

---

## 2. Finding 분류

| Finding | 원 Priority | 분류 |
|---|---|---|
| 1. 리뷰 게이트의 실질적 부재 | P1 | 정책 수립 필요 |
| 2. EngineRuntime 성장 궤적 | P1 | 설계 변경 필요 (단, 지금은 관찰) |
| 3. README/ROADMAP 정체 | P1 | 즉시 수정 가능 |
| 4. 웹 API 인증/CORS 부재 | P2 | 정책 수립 필요 |
| 5. CI 자동화 부재 | P2 | 즉시 수정 가능 (설정 작업) |
| 6. ruff 리포지토리 스코프 미설정 | P3 | 즉시 수정 가능 |

---

## 3. Action Item

### AI-01 — README/ROADMAP 최신화 (Finding 3)

- **Action**: `README.md`의 "현재 상태" 절을 Milestone 4/v0.5.0에서 현재 Milestone 번호로 갱신하고, "최신 진행 상황은 `.ai/TASKS.md` 참고" 링크를 추가한다. `pyproject.toml`의 `version`을 최신 상태에 맞게 재검토한다.
- **목적**: 외부 독자(사람/AI)가 README만 보고 프로젝트 성숙도를 심각하게 과소평가하는 것을 방지한다.
- **영향 범위**: `README.md`, `pyproject.toml`(버전 필드만).
- **예상 난이도**: Small
- **예상 위험도**: Low
- **선행 조건**: 없음.
- **완료 조건(DoD)**: README의 "현재 상태" 절이 `.ai/TASKS.md`의 최신 Milestone 번호와 일치하고, `.ai/TASKS.md`로의 링크가 존재한다.

---

### AI-02 — ruff 스코프에서 `.claude/skills` 제외 (Finding 6)

- **Action**: `pyproject.toml`의 `[tool.ruff]`에 `exclude = [".claude"]`(또는 동등한 경로)를 추가한다.
- **목적**: `ruff check .`를 리포 루트에서 실행했을 때 제품 코드와 무관한 도구 스크립트 오류(422건)가 섞여 나오는 것을 방지하고, "ruff clean" 주장의 스코프 혼동을 제거한다.
- **영향 범위**: `pyproject.toml` 1개 파일.
- **예상 난이도**: Small
- **예상 위험도**: Low
- **선행 조건**: 없음.
- **완료 조건(DoD)**: 리포 루트에서 `ruff check .` 실행 시 `.claude/skills/` 관련 오류가 나타나지 않는다. `ruff check src/ai_workspace`는 기존과 동일하게 통과한다(회귀 없음).

---

### AI-03 — CI(GitHub Actions) 도입 (Finding 5)

- **Action**: `.github/workflows/ci.yml` 신설. `pytest`, `ruff check src/ai_workspace`, `mypy src/ai_workspace`를 PR 대상 필수 스텝으로 등록한다.
- **목적**: 현재 전적으로 로컬 실행에 의존하는 품질 검증(pytest/ruff/mypy)을 자동화하고, branch protection의 "필수 상태 검사"가 실제로 걸릴 수 있는 대상을 만든다. (Finding 1 해결의 전제 조건.)
- **영향 범위**: 신규 파일 `.github/workflows/ci.yml` 1개. 기존 소스에는 영향 없음.
- **예상 난이도**: Medium (워크플로 자체는 단순하지만, 현재 로컬 환경과 CI 환경의 의존성 설치 차이를 검증해야 함)
- **예상 위험도**: Low
- **선행 조건**: 없음. (AI-02를 먼저 하면 CI의 ruff 스텝이 처음부터 깨끗하게 통과하므로 순서상 권장되지만 강한 의존은 아님.)
- **완료 조건(DoD)**: 임의의 PR을 열었을 때 GitHub 체크 목록에 pytest/ruff/mypy 3개 상태 검사가 표시되고, 실제로 실행되어 결과가 반영된다.

---

### AI-04 — 리뷰 게이트 정책 수립 및 Branch Protection 강화 (Finding 1)

- **Action**: (a) branch protection 규칙에 "머지 전 필수 상태 검사"로 AI-03의 CI 체크를 등록한다. (b) 1인 개발 체제에서 "제3자 리뷰"가 구조적으로 불가능하다는 감사의 Counter Evidence를 인정하고, 이를 대체할 수 있는 대안(예: 별도 AI 세션의 사전 리뷰를 병합 전 필수 절차로 `.ai/RULES.md`에 명문화)을 정책으로 문서화한다.
- **목적**: `protected: true`이지만 실질적으로 리뷰 게이트가 작동하지 않는 현재 상태(PR #93: 리뷰 0건, 10초 내 자기 병합)를 구조적으로 개선한다. 코드를 고치는 작업이 아니라 정책/설정 작업이다.
- **영향 범위**: GitHub 저장소 설정(branch protection rule), `.ai/RULES.md`(정책 문서).
- **예상 난이도**: Medium
- **예상 위험도**: Medium (지나치게 엄격한 게이트는 1인 개발 속도를 해칠 수 있음 — 감사의 Counter Evidence가 지적한 트레이드오프)
- **선행 조건**: **AI-03 완료 필수** — CI가 없으면 "필수 상태 검사"로 걸 대상이 없다.
- **완료 조건(DoD)**: branch protection 규칙에 필수 상태 검사가 등록되어 있고, `.ai/RULES.md`에 병합 전 리뷰 절차(대안 포함)가 명문화되어 있다.

---

### AI-05 — 웹 API 배포 시나리오 확정 및 인증 정책 수립 (Finding 4)

- **Action**: `runtime/production/` 및 `web/` 하위 API가 로컬 전용인지 외부 노출 대상인지 먼저 확정하고(감사에서 "확인되지 않음"으로 남은 질문), 결과를 `docs/ARCHITECTURE.md`에 명시한다. 외부 노출이 확정될 경우에만 인증 미들웨어 추가를 후속 Action(AI-05b, 미정)으로 분리한다.
- **목적**: 근거 없이 인증 코드를 먼저 작성하지 않는다 — 배포 시나리오가 확인되지 않은 상태에서의 코드 변경은 감사 결과에 없는 가정을 추가하는 것이다.
- **영향 범위**: 문서(`docs/ARCHITECTURE.md`)만. 코드 변경 없음(이번 단계에서는).
- **예상 난이도**: Small (정책 확정 자체는), 후속 구현은 Medium~Large(미확정)
- **예상 위험도**: Low
- **선행 조건**: 없음.
- **완료 조건(DoD)**: `docs/ARCHITECTURE.md`에 배포 대상(로컬 전용/외부 노출)이 명시적으로 기술되어 있다. 외부 노출로 확정될 경우 별도 후속 Action Item이 이 문서에 추가된다.

---

### AI-06 — EngineRuntime 확장 정책 문서화 (Finding 2, 1단계)

- **Action**: Milestone 83/84에서 실제로 관찰된 "옵트인 계층으로 확장" 패턴을 `.ai/RULES.md`에 명문화한다. 예: "EngineRuntime에 메서드를 추가하기 전에, 신규 Domain 값 객체 + 별도 오케스트레이션 클래스로 옵트인 확장이 가능한지 먼저 검토한다."
- **목적**: 감사가 발견한 "최근 2개 Milestone의 방향 전환"이 우연인지 정책인지 불분명하다는 지적을 해소한다 — 우연으로 남겨두지 않고 명문화된 규칙으로 고정한다. 이는 감사 보고서의 최종 권고와 정확히 일치한다.
- **영향 범위**: `.ai/RULES.md` 1개 파일. 코드 변경 없음.
- **예상 난이도**: Small
- **예상 위험도**: Low
- **선행 조건**: 없음.
- **완료 조건(DoD)**: `.ai/RULES.md`에 EngineRuntime 확장 판단 기준이 명문화되어 있고, 이후 Milestone에서 이 기준을 인용해 설계 판단을 내린 사례가 최소 1건 이상 확인된다(관찰 지표, AI-07 참고).

---

### AI-07 — EngineRuntime 리팩터링 여부 재판단 (Finding 2, 2단계 — 지금 착수하지 않음)

- **Action**: AI-06 정책 적용 후 일정 기간(예: 다음 10개 Milestone) `EngineRuntime`/`InMemoryEngineRuntime`의 라인 수·메서드 수 성장을 관찰한다. 정책 적용 후에도 성장이 재개되면 그때 리팩터링(예: 실행 전략별 클래스 분리)을 별도 Milestone으로 계획한다.
- **목적**: 감사 결과(92→1,104줄 단조 증가, 그러나 최근 2개 Milestone은 무변경)가 "확정된 악화 추세"인지 "이미 스스로 개선된 궤적"인지 현재로서는 판단 근거가 부족하다. 근거 없이 큰 리팩터링에 착수하는 것은 Evidence First 원칙(AWAS §2.1)에 위배된다.
- **영향 범위**: (지금은 없음) 착수 시 `interfaces/engine_runtime.py` + 3개 구현체(`engine_runtime.py`, `managed_engine_runtime.py`, `recovering_engine_runtime.py`) + 관련 테스트 전체.
- **예상 난이도**: Large
- **예상 위험도**: High (핵심 실행 경로 전체에 영향)
- **선행 조건**: AI-06 완료 + 관찰 기간 경과 + 관찰 결과 재성장 확인.
- **완료 조건(DoD)**: (지금 단계에서는 "착수하지 않음"이 DoD) 관찰 기간 종료 시점에 성장 여부를 `git show` 실측으로 재확인하고, 재성장이 확인된 경우에만 별도 리팩터링 Milestone을 새로 발행한다.

---

## 4. 우선순위 재정렬 (Execution Order 기준, P0~P3 대신 사용)

| 구분 | Action Item | 이유 |
|---|---|---|
| **Quick Win** | AI-01 (README), AI-02 (ruff exclude) | 선행 조건 없음, 위험도 Low, 30분~1시간 내 완료 |
| **Foundation** | AI-03 (CI 도입), AI-06 (EngineRuntime 정책 문서화), AI-05 (배포 시나리오 확정) | 이후 작업(AI-04, AI-07)의 전제가 되는 도구/정책 기반 |
| **Refactoring** | AI-04 (리뷰 게이트/Branch Protection) | Foundation(AI-03) 위에서만 의미가 있는 구조 변경 |
| **Long-term** | AI-07 (EngineRuntime 리팩터링) | 관찰 데이터가 쌓인 뒤에만 판단 가능, 지금은 대기 |

---

## 5. Milestone Plan

- **Milestone A — 문서/설정 정리 (Quick Win)**: AI-01 + AI-02
- **Milestone B — CI 기반 구축**: AI-03
- **Milestone C — 정책 문서화 (2건 병렬 가능)**: AI-06 + AI-05
- **Milestone D — Review Gate 강화**: AI-04
- **Milestone E — EngineRuntime 관찰 및 재판단 (대기 상태로 시작, 트리거 시 실행)**: AI-07

---

## 6. Dependency Graph

```
AI-01 (README)         ─┐  독립 실행 가능 (Quick Win)
AI-02 (ruff exclude)   ─┘

AI-03 (CI 도입)
   │
   ▼
AI-04 (Review Gate / Branch Protection)

AI-06 (EngineRuntime 정책 문서화)
   │  (정책 적용 후 관찰 기간)
   ▼
AI-07 (EngineRuntime 리팩터링 여부 재판단)

AI-05 (배포 시나리오 확정) ── 독립 실행, 단 결과에 따라
                              후속 AI-05b(인증 구현, 미정)를 새로 발행할 수 있음
```

핵심 의존 관계는 두 갈래뿐이다: **AI-03 → AI-04**(CI 없이는 리뷰 게이트를 걸 대상이 없음), **AI-06 → AI-07**(정책을 먼저 세우지 않고 리팩터링에 착수하면 무엇을 기준으로 "다시 커지지 않게" 만들지가 없음). 나머지 Action Item은 서로 독립적이며 병렬 진행 가능하다.

---

## 7. Quick Wins

- **AI-01** — README/ROADMAP 최신화
- **AI-02** — ruff exclude 설정

두 항목 모두 선행 조건 없음, 위험도 Low, 영향 범위가 파일 1~2개로 한정된다. 지금 바로 착수 가능하다.

---

## 8. Long-term Refactoring

- **AI-07 (EngineRuntime 리팩터링)** — 유일한 Large/High-risk 항목. 감사 결과가 "확정된 악화"가 아니라 "관찰이 더 필요한 추세"였으므로, 정책(AI-06) 적용 후 재관찰 없이 지금 착수하는 것은 근거가 부족한 조기 리팩터링이다. 명시적으로 지금 착수하지 않는다.

---

## 9. Technical Debt Backlog

| Finding | 분류 |
|---|---|
| Finding 2 (EngineRuntime 성장) | **일정 기간 관찰** — AI-06 적용 후 재성장 여부를 관찰하고, 재성장 시 부채를 "지금 해결"로 재분류한다. |
| Finding 1 (리뷰 게이트 부재) | **지금 해결** — AI-03/AI-04로 즉시 착수. |
| Finding 3 (README 정체) | **지금 해결** — AI-01. |
| Finding 4 (웹 API 인증) | **일정 기간 관찰 (배포 시나리오 확정 대기)** — AI-05 결과에 따라 재분류. |
| Finding 5 (CI 부재) | **지금 해결** — AI-03. |
| Finding 6 (ruff 스코프) | **지금 해결** — AI-02. |

---

## 10. Deferred Items (수정하지 않을 항목)

| 항목 | 수정하지 않는 이유 |
|---|---|
| **`EngineAdapter`(8개 메서드, 구현체 3개) 분리** | 감사 보고서에서 "아직 위험 수준은 아니다"로 명시적으로 평가됨(§Interface Health). Finding으로 등록되지 않은 항목을 Action Item으로 만드는 것은 감사 결과를 임의로 확장하는 것이므로 제외한다. |
| **단일 구현체만 있는 인터페이스(WorkflowEngine, DashboardRepository 등)의 통합/축소** | 감사에서 "테스트 목적 In-Memory 구현이 표준 패턴인 이 코드베이스 특성상 자연스러운 결과일 수 있다"고 명시하며 별도 Finding으로 격상하지 않았다. Finding이 아닌 관찰을 Action Item으로 만들지 않는다. |
| **`intelligence/`의 `render_markdown` 반복 패턴 추상화** | 감사에서 "구체적 리팩터링 후보"로 언급됐으나 정식 Finding으로 등록되지 않고 정량 근거(Evidence)도 §12 수준의 제한적 관찰에 그친다. 정식 Finding이 아닌 항목은 이번 실행 계획의 변환 대상이 아니다. |
| **Discussion 운영 여부 조사** | 감사 보고서에서 "확인되지 않음"으로 남은 항목이며, Finding이 아니라 조사 공백이다. Action Item으로 변환할 결론 자체가 없다. |
| **Branch Protection 세부 규칙(필수 리뷰어 수 등) 확인** | 마찬가지로 "확인되지 않음"으로 남은 조사 공백이다. AI-04가 정책을 새로 세우는 방식으로 이 공백을 우회하므로 별도 조사 Action Item을 만들지 않는다. |

---

## 11. 최종 권고

이번 실행 계획에서 가장 중요한 판단은 **"무엇을 하지 않는가"**다. Finding 2(EngineRuntime 성장)를 즉시 리팩터링 과제로 전환하지 않은 것, Finding 4(웹 API 인증)를 확정되지 않은 배포 가정 위에서 코드로 옮기지 않은 것, Deferred Items 5건을 정식 Finding이 아니라는 이유로 Action Item화하지 않은 것 — 이 세 가지 절제가 감사 결과를 과도하게 확대 해석하지 않으면서도 실제로 실행 가능한 계획을 만든다. 권장 착수 순서는 **AI-01/AI-02(Quick Win) → AI-03(CI) → AI-06/AI-05(정책 문서화, 병렬) → AI-04(Review Gate) → AI-07(관찰 후 재판단)**이며, AI-07을 제외한 모든 항목은 위험도 Low~Medium, 난이도 Small~Medium 범위에 있어 별도의 대규모 일정 확보 없이 순차 처리 가능하다.
