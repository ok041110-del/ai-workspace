---
tags: [decision]
---

# Decisions Index

> [[ADR Index]]보다 가벼운 "왜?" 메모 모음. 공식 ADR로 남길 정도는
> 아니지만 반복해서 물어보게 되는 질문들을 정리한다. Status가 "확정"
> 이 아닌 항목은 아직 결론이 나지 않은 질문이다.

## 왜 CQRS인가

- Status: 확정
- 질문: Dashboard/Automation은 왜 Execution 결과를 직접 조회하지
  않고 Event를 거쳐 별도 Read Model에 기록하는가?
- 답: Writer(`ExecutionDispatcher`)가 Reader의 존재를 몰라야 향후
  다른 Presentation(예: M23 Mobile)이 추가돼도 Writer를 건드리지
  않아도 된다. [[Architecture Overview]]의 CQRS 절 참고.

## 왜 EventBus인가

- Status: 확정
- 질문: Dashboard/Automation이 서로를 직접 호출하지 않고 왜
  EventBus를 거치는가?
- 답: Execution 계층(§3.16)이 "누가 구독하는지" 알 필요가 없게 하기
  위해서다. Event Store도 특별한 경로 없이 동일한 방식의 독립
  구독자다(ADR-0018). [[ADR Index]] 참고.

## 왜 Dashboard/Automation/Production을 Core Domain과 분리했는가

- Status: 확정
- 질문: Core Domain(`domain`/`interfaces`/`engines`)이 왜 이 세
  Infrastructure 계층의 존재를 전혀 모르는가?
- 답: Core Domain은 "어떤 Presentation/운영 계층이 붙는지"와 무관하게
  독립적으로 테스트·재사용 가능해야 한다는 원칙(M20 kickoff 때부터
  일관 적용). [[Backend Index]] 참고.

## 왜 Server와 iOS를 분리했는가(또는 분리할지)

- Status: **미정**
- 질문: iOS/Android 앱 코드를 이 저장소(`ok041110-del/ai-workspace`)
  안에 둘지, 별도 저장소로 분리할지?
- 현재 상태: M23 착수 전이라 아직 결정되지 않음. [[iOS Design]]의
  "미결정 사항" 절에 동일 질문 기록. M23 kickoff 시 확정 예정.

## 관련 문서

- [[ADR Index]]
- [[Architecture Overview]]
- [[iOS Design]]

## 원문

- `.ai/DECISIONS.md`(공식 ADR은 여기), 이 문서는 Vault 전용 메모이며
  GitHub 원문이 별도로 없다.
