---
tags: [automation]
type: automation
---

# Automation Index

> Automation Engine(Milestone 21, ADR-0033). 사용자의 명시적 요청
> 없이 조건/일정에 따라 Task를 자동 실행한다. Dashboard와 독립적인
> Domain.

> **이름 주의**: M4-T07의 `AutomationEngine`(Interface)과는 다른
> 개념이다 — `AutomationEngine`은 trigger_id↔Workflow 연결 관리만
> 하고, "언제 발동해야 하는가" 판단과 실제 실행은 이번 Milestone이
> 새로 구현한다. 두 개념 모두 그대로 유지된다. ([[ADR Index]]
> ADR-0033)

> **Platform 계층(2026-07-30, 사용자 확정)**: M21(이 Milestone)은
> M36~M38과 함께 **Execution Platform**(실행·상태 전이·스케줄링)에
> 속한다 — M29~M35 **Intelligence Platform**(관찰·분석·추천,
> Read Only)과 책임이 다르다. "Automation Core"라는 이름은 Memory
> Engine/Architecture Guardian/Learning Engine이 갖춰진 뒤로
> 보류됐다. 상세는 `docs/ARCHITECTURE.md` §2.1 참고.

## Rule

`AutomationRule`은 `last_executed_at`/`next_execution_at`을 포함하는
가변 엔티티(`enable()`/`disable()`). `AutomationRepository`(신규
27번째 Interface)에 저장되고, `AutomationService`가 CRUD의 유일한
진입점이다(Action을 직접 실행하지 않음).

## Trigger

`TriggerKind`: TIME/INTERVAL/EVENT/STARTUP. `TriggerEvaluator` 계층이
"지금 발동해야 하는가"만 전담(Scheduler와 책임 분리) —
`TimeTriggerEvaluator`/`IntervalTriggerEvaluator`/
`StartupTriggerEvaluator`/`EventTriggerEvaluator`.

## Scheduler

`AutomationScheduler`(Infrastructure)는 Rule을 별도 보관하지 않고
매 `tick()`/`start()`/Event 수신마다 `AutomationRepository`를 다시
조회한다 — `AutomationService`의 CRUD가 자동 반영됨. Server Runtime이
`automation_tick_seconds`(기본 30초)마다 백그라운드로 `tick()`을
돈다([[Production Index]]).

## Execution Flow

```
AutomationRule → AutomationRepository → AutomationService(CRUD)
  → AutomationScheduler(Trigger 평가) → AutomationActionExecutor
  → ExecutionDispatcher(유일한 실행 진입점) → EventBus → Dashboard
```

`AutomationActionExecutor`는 RUN_TASK를 기존 M17/M18 파이프라인
(`EngineSelectionPolicy.select()` → `ExecutionDispatcher.dispatch()`)
에 그대로 실어 실행한다 — 새 실행 경로를 만들지 않는다. RUN_WORKFLOW는
아직 미지원(`AutomationActionNotSupportedError`).

**RUN_RECOMMENDATION(Milestone 38, ADR-0052)**: `RecommendationExecutionService`
(M36/M37)를 `manual_trigger=True`로 호출해 M35 `source=next_task`
추천을 그대로 실행한다 — `ExecutionGate`는 손대지 않는다(여전히
`source=next_task`만 승인). `web/server.py`의 `build_app()`이
`VaultAdapter`/`AgentAdapter`/Recommendation 파이프라인 전체를
최초로 실배선해, `AutomationScheduler`의 TIME/INTERVAL Trigger로
실제 자동 실행이 가능해졌다.

**Architecture Guardian Gate(Milestone 48, ADR-0065)**:
`RecommendationOrchestrationService`가 `execution_service.execute()`
를 호출하기 직전에(주입된 경우) `ArchitectureGuardianService.
generate()`(M41, Read Only)를 호출한다 — Guardian 위반이 있으면
Recommendation/Adaptation/Explainability는 그대로 생성하되 Execution
만 차단한다(Override 없음). M45 StatusLine에 `AutomationGateStatus`
(PASS/BLOCKED/UNKNOWN)로 최근 1건의 결과가 노출된다.

**Adaptation 규칙 정교화(Milestone 49, ADR-0066)**:
`RecommendationAdjustmentAnalyzer`(M42)의 추천 보류 조건이 "성공
0건 + 실패 1건 이상"에서 "실패율 100% + 표본 3건 이상"으로
정교화됐다 — 표본이 부족한 상태(실패 1~2건)에서 성급하게 보류하지
않도록 최소 표본 조건을 추가했다. Guardian 다건 이력 축적·영속
저장소 도입은 이번 Milestone Scope에서 명시적으로 배제됐다(향후
별도 Milestone 대상).

**Learning Persistence(Milestone 50, ADR-0067)**: `ExecutionMemory
Store`(M39)가 쓰는 `MemoryEngine` 구현체가 `InMemoryMemoryEngine`
에서 `FileMemoryEngine`(신규, `storage/`)으로 교체됐다 —
`<vault_root>/.ai-workspace-data/`에 단일 JSON 파일로 key-value를
영속화해, 서버 재시작 후에도 학습 이력이 유지된다. 새 Interface/
Service 없이 기존 `MemoryEngine` 계약을 구현만 했고, `web/server.py`
Composition Root 1곳만 교체됐다. StatusLine이 이 파일을 읽는
Observability 배선은 이번 Scope 밖(향후 별도 Milestone 대상).

**Learning Evolution(Milestone 51, ADR-0068)**: M49/M50 규칙(실패율
100% + 표본 3건 이상, 전체 이력 기반)에 최근 추세 기반 규칙이
보완으로 추가됐다 — `ExperienceStat.recent_failure_streak`(가장
최근 기록부터 거슬러 올라간 연속 실패 횟수)가 5 이상이면, 전체
이력에 성공이 섞여 있어도 추천을 보류한다(기존 규칙 무변경, OR
병존). 어느 규칙이 발동했는지는 `reason` 텍스트에 "(M49 규칙)"/
"(M51 규칙)"/"(M49+M51 규칙)"로 태깅돼 Explainability(M44)가 그대로
노출한다.

**StatusLine Integration Fix(Milestone 45-1, ADR-0069)**: M45
StatusLine이 실제 Claude Code UI에서 표시되지 않는다는 보고를,
추측 대신 공식 문서(`code.claude.com/docs/en/statusline`) 대조로
조사했다. `.claude/settings.json` 형식과 stdin JSON 필드
(`model.display_name`/`effort.level`/`context_window.*`)는 모두
공식 문서와 일치함을 확인했다. 실제 원인은 `statusline_main.py`의
`ai_workspace.*` import 3개가 `try/except` 바깥에 있어, import
자체가 실패하면 아무 출력 없이 프로세스가 죽는 것이었다 — 공식
Troubleshooting("Status line not appearing")이 말하는 실패 모드와
정확히 일치. import를 `main()` 내부로 옮겨 모든 예외(import 실패
포함)가 항상 한 줄 출력으로 대체되도록 고쳤고, 실패 시에만
`/tmp/statusline.log`를 남기는 디버그 로그를 추가했다(정상 동작
시 로그 없음, `AI_WORKSPACE_STATUSLINE_DEBUG=1`로 실제 payload를
opt-in 캡처 가능). 공식 문서는 Workspace Trust 미승인 시에도
StatusLine이 아예 실행되지 않는다고 별도로 명시하는데, 이는 코드가
아닌 사용자 환경 설정이라 이번 Milestone에서 고칠 수 없어 DoD에
사용자 확인 항목으로 남겼다(`claude --debug` 로그 확인 필요,
헤드리스 원격 세션이라 실제 UI 접근 불가).

**후속 환경 실증(2026-08-01)**: 이 세션 자체가 StatusLine을
지원하는지 직접 조회로 실증했다 — `sys.stdin/stdout.isatty()` 모두
`False`, `CLAUDE_CODE_ENTRYPOINT=remote_mobile`, 실제 `claude`
프로세스가 `--output-format=stream-json --input-format=stream-json`
(비대화형 print 모드)로 구동 중임을 `ps aux`로 확인했다.
`/tmp/statusline.log`가 세션 내내 생성되지 않아 `statusline_main.py`
가 한 번도 호출되지 않았음도 확인했다. **결론(실증)**: 이 세션
타입(Claude Code Remote, 비대화형 stream-json)은 대화형 터미널 UI
자체가 없어 StatusLine을 아키텍처상 지원하지 않는다 — 코드 결함이
아니다. 사용자의 로컬 대화형 터미널 환경에서의 실제 표시 여부는
이 세션이 자체 검증할 수 없어 사용자 확인으로 남는다.

**Learning Weighting(Milestone 52, ADR-0070)**: M49(전체 실패율)/
M51(최근 연속 실패) 두 Rule의 OR 결합을 가중치 점수 결합으로
확장했다. `signal_overall = failure_count/total`(표본 3건 미만이면
0), `signal_recent = min(recent_failure_streak/5, 1.0)`을 각각 0.6
가중치로 합산해 `score >= 0.6`이면 보류한다. 가중치를 신호의 완전
포화값(1.0)과 같은 0.6으로 설정해, 신호 하나가 완전히 1.0이면 그
신호만으로 `score=0.6`이 성립 — 기존 M49/M51 단일 규칙이 정확히
보존됨을 경계값으로 증명했다(회귀 없음). 사용자가 처음 제안한
가중치 0.5/0.5+threshold 0.6 조합이 이 보존 조건을 깨는 실제
회귀임을 수학적으로 지적해 0.6/0.6으로 재확정했다. Explainability는
기존 M49/M51/Both 태깅을 보존하고, 개별 규칙으로는 안 걸리고
가중치 결합으로만 걸린 새 케이스에 "(M52 가중치 결합 규칙)" 태그를
추가했다. 가중치·threshold는 코드에 고정된 상수로 데이터 기반
학습은 하지 않는다(Non-goal 유지).

**Learning Decay(Milestone 53, ADR-0071)**: M52의 `signal_overall`
(단순 평균, 모든 기록을 동등 반영)을 지수 Decay 가중 실패율로
교체했다. `ExperienceStat`에 `decayed_failure_rate: float` 필드를
신설해 `weight(rank) = 0.8**rank`(`rank=0`이 최신 기록)로
`Σ(weight×실패 여부)/Σ(weight)`를 계산한다 — 최근 기록일수록 더
큰 비중을 갖는다. 전체 이력이 100% 실패면 가중치와 무관하게 항상
정확히 1.0이라, M49/M52까지 쌓아온 "신호 1.0 → score=0.6" 회귀
없음 증명 체인이 그대로 보존된다. 구현 중 `ExperienceStat`을 수동
생성하는 기존 테스트 5건이 새 필드 기본값(0.0)으로 M49 트리거가
깨지는 것을 테스트 실행으로 발견해 값 명시 지정으로 수정했다.
Decay 계수(0.8)는 코드에 고정된 상수로 데이터 기반 학습은 하지
않는다(Non-goal 유지).

**Learning Insight(Milestone 54, ADR-0072)**: M49~M53 학습 신호가
Adaptation 내부 판단에만 쓰이고 사람이 볼 수 있는 형태로 노출되지
않았던 것을 StatusLine에 노출했다. 새 `LearningRuntimeAnalyzer`가
`FileMemoryEngine`(M50)+`ExecutionMemoryStore`(M39)+
`ExperienceIntelligenceService`(M40)를 그대로 조합해
`ExperienceReport`를 얻는다(새 Domain/Interface/Service 없음).
`WorkspaceInfo.current_task`가 Phase 1 범위 밖(ADR-0063)이라 "현재
추천 대상"은 여전히 알 수 없어, "추적 중인 전체 task 중 가장
위험한 것"(`decayed_failure_rate` 최댓값, 동점이면 task_id
오름차순 — 새 채점 아니라 표시 로직)으로 범위를 좁혔다. 부수적으로
Pipeline Stage의 Memory 단계가 `NOT_OBSERVABLE`에서
`OBSERVED_DONE`/`OBSERVED_NOT_YET`으로 승격돼, M45/M50에서 두 번
"별도 Milestone 대상"으로 미뤄뒀던 gap도 같은 배선으로 함께
해소했다. 실제 `FileMemoryEngine` 데이터로 end-to-end 수동 검증
완료.

## 관련 GitHub 문서

- `docs/ARCHITECTURE.md` §3.19
- `src/ai_workspace/runtime/automation/`
- `src/ai_workspace/web/automation_routes.py`

## 관련 문서

- [[ADR Index]] — ADR-0033
- [[Dashboard Index]]
- [[API Catalog]]

## 원문

- `docs/ARCHITECTURE.md` §3.19
