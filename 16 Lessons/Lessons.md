---
tags: [system]
type: documentation
---

# Lessons 사용법

이 폴더는 회고(Lesson)를 담는다 — 특정 실패나 반복된 실수에서
배운 교훈을 Milestone과 무관하게 남기는 곳이다([[Vault Information Architecture]] T03 Lesson Role).

## 현재 상태(Milestone 47)

**아직 실제 Lesson 항목이 없다.** M46은 실제 회고 데이터 없이 구조
부터 만드는 것을 YAGNI로 판단해 보류했으나, M47에서 구조 자체
(폴더 + 규칙)는 미리 준비해 두기로 결정했다 — `13 Daily`/`14 Tasks`
와 같은 패턴(설계는 있고 실제 항목은 필요할 때 생성).

## Lesson 문서를 언제 만드는가

- Experience Intelligence(M40)가 반복 실패(성공률 낮음)를 보고할
  때, 그 원인 분석을 Lesson으로 남긴다.
- ADR의 "대안" 절에서 기각한 접근이 실제로 문제를 일으켰던 것으로
  드러났을 때.
- 사람이 명시적으로 "이건 교훈으로 남겨야 한다"고 판단할 때.

**자동 생성하지 않는다** — Lesson은 판단이 필요한 회고이므로 항상
사람 또는 AI가 명시적으로 작성한다(Experience Intelligence처럼
자동 집계되는 리포트와 다름).

## Lesson 문서 형식(작성 시 참고)

```markdown
---
tags: [lesson]
type: lesson
project: M{번호}(선택)
---

# {짧은 제목}

## 무슨 일이 있었는가
## 무엇을 배웠는가
## 관련 문서
```

## 관련 문서

- [[Knowledge Hub]]
- [[Vault Information Architecture]]
- [[Experience Intelligence]]
