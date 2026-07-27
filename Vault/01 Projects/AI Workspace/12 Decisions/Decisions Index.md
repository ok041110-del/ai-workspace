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

## 왜 Server와 iOS/Android를 분리했는가

- Status: 확정(2026-07-27, Mobile Experience Start Criteria — 결정 당시 M23, 이후 M23은 "Obsidian Integration & Auto Save"로 재정의됨)
- 질문: iOS/Android 앱 코드를 이 저장소(`ok041110-del/ai-workspace`)
  안에 둘지, 별도 저장소로 분리할지?
- 답: Client 코드는 별도 저장소로 분리한다. 이 저장소
  (`ok041110-del/ai-workspace`)는 Server(API)까지만 담당하고 Mobile
  Client(iOS/Android)는 포함하지 않는다. Push는 이 저장소의 Server가
  생성·관리하되, 실제 전송은 FCM/APNs를 통해 수행한다(별도 Push
  서비스가 아니라 외부 발송 채널만 이용). [[iOS Design]]/
  [[PREPARATION_SUMMARY]]의 "Mobile Experience Start Criteria" 참고.

## 관련 문서

- [[ADR Index]]
- [[Architecture Overview]]
- [[iOS Design]]

## 원문

- `.ai/DECISIONS.md`(공식 ADR은 여기), 이 문서는 Vault 전용 메모이며
  GitHub 원문이 별도로 없다.
