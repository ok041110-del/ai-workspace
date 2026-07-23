# MEMORY — 프로젝트 장기 메모리

이 문서는 AI Workspace 프로젝트의 **장기 기억 저장소**다. 세션이 종료되어도
유지되어야 할 중요한 컨텍스트, 결정, 용어 정의를 이곳에 누적한다. 새로운 세션을
시작하는 AI 구현 엔진은 작업 전에 이 문서를 먼저 읽어야 한다.

형식: 시간순으로 항목을 추가하며, 기존 항목은 삭제하지 않고 상태가 바뀌면
새 항목을 추가해 이력을 남긴다.

---

## 프로젝트 정체성

- **프로젝트명**: AI Workspace
- **한 줄 정의**: Claude Code, Codex, Gemini CLI 등 AI 구현 엔진을 관리하는
  오케스트레이션 플랫폼.
- **핵심 원칙**: AI Workspace는 코드를 작성하지 않는다. 관리(프로젝트/Task/
  Workflow/메모리/승인/자동화/다중 프로젝트/구현 엔진 관리)만 담당한다.

## 2026-07-23 — Phase 0 시작: 문서화 및 구조 설계

- 사용자가 프로젝트의 개발 철학(문서 우선, 아키텍처 우선, Task 단위 개발, 한 번에
  하나, 완료 전 테스트, 승인 필요, 항상 이유 설명, 한국어 작성 원칙)을 확정했다.
- 이번 작업(Phase 0)에서는 애플리케이션 코드를 작성하지 않고, 문서 구조와 초기
  문서 세트만 작성하기로 합의했다.
- 표준 문서 구조를 확정했다: `README.md`, `docs/{PRD,ARCHITECTURE,ROADMAP}.md`,
  `.ai/{RULES,TASKS,MEMORY,DECISIONS}.md`, `workspace/`, `tests/`.
- 아키텍처 방향으로 "Orchestration Layer / Engine Adapter Layer / Interface
  Layer"의 3단 구조와, Project Manager / Task Manager / Workflow Engine /
  Approval Gate / Memory Store / Automation Scheduler라는 6개 핵심 컴포넌트를
  제안했다 (사용자 승인 대기 — `docs/ARCHITECTURE.md` 참고).
- 승인이 필요한 4가지 행위(아키텍처 변경, 신규 기능, 리팩토링, Phase 완료)를
  `.ai/RULES.md`에 명문화했다.
- Phase 1의 목표를 "핵심 도메인 모델(Project/Task/Workflow) 정의 + 파일 기반
  저장 + 최소 CLI 골격"으로 잠정 설정했다 (`docs/ROADMAP.md` 참고, 승인 대기).

## 유지해야 할 핵심 컨텍스트 (요약)

- 실제 코드 작성 금지 원칙은 **Phase 0(현재 작업)에 한정**된다. Phase 1부터는
  사용자 승인을 받은 뒤 도메인 모델 코드를 작성하기 시작한다.
- 기술 스택(Python, pydantic/dataclasses, 파일 기반 저장, CLI)은 아직 **제안**
  단계이며 확정된 결정이 아니다. Phase 1 착수 시 정식 ADR로 승인받아야 한다.
- 구현 엔진 연동 순서: Claude Code를 최우선으로 지원하고, 이후 Codex, Gemini CLI를
  동일한 Adapter 패턴으로 추가한다.
