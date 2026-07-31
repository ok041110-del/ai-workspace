---
tags: [architecture]
type: architecture
---

# Vault Information Architecture

> Milestone 46(Vault Information Architecture)의 핵심 산출물. Vault를
> "문서 저장소"가 아니라 **AI Workspace의 Long-term Memory Layer**로
> 재정의한다(ADR-0064). 기능 변경은 없다 — 대상은 Information
> Architecture(폴더/문서/Metadata/Link/Graph)뿐이다.

## 관련 문서

- [[Metadata Standard]]
- [[Document Type Color Strategy]]
- [[Map of Content Guide]]
- [[Vault Migration Plan]]
- [[Architecture Overview]]

---

## T01 — Current Vault Analysis(실측)

이 절의 모든 수치는 2026-07-31 시점 실제 Vault(`00 System`~`99
Templates`, 49개 Markdown 문서)를 스크립트로 분석한 결과다 —
추측하지 않는다.

### 1.1 Folder 구조

| Folder | 문서 수 | 실질 역할 |
|---|---|---|
| `00 System` | 7 | AI Operating Manual(PROJECT_INDEX→AI_CONTEXT→READING_PROFILES→PROMPT_PROFILE→EXECUTION_PROFILE 순서로 서로 [[WikiLink]]) |
| `01 Overview` | 1 | 프로젝트 소개 |
| `02 Architecture` | 3(+이번에 5개 추가) | Architecture Map/Overview/Vault Integration Architecture |
| `03 ADR` | 1(ADR Index, 397줄, ADR 63건 수록) | 모든 ADR을 단일 파일에 순차 append |
| `04 Backend`/`05 API`/`06 Dashboard`/`07 Automation`/`08 Production`/`09 iOS`/`10 Android` | 각 1 | 각각 "{Name} Index/Catalog/Design/Placeholder" 1개뿐 — M23~M24 Vault 최초 구축 시 만들어진 골격, 이후 내용이 거의 자라지 않음 |
| `11 Milestones` | 1(Milestones Index, 102줄, Milestone 43건 행) | ADR Index와 동일 패턴(단일 파일 append) |
| `12 Decisions` | 1(Decisions Index) | ADR보다 가벼운 "왜?" 메모 — ADR과 의도적으로 분리된 별도 계층(중복 아님) |
| `13 Daily` | 1(README만) | 설계는 있으나 실제 Daily Note가 하나도 생성된 적 없음 |
| `14 Tasks` | 1(README만) | 설계는 있으나 실제 Task 문서(`{task_id}.md`)가 하나도 생성된 적 없음 — Task 상태는 전부 `.ai/TASKS.md`에만 존재 |
| `15 Project Intelligence` | 12(README + 11개 생성 리포트) | M29~M44가 매번 덮어쓰는 AI 생성 리포트 전용 |
| `99 Templates` | 14 | Task/ADR/Daily/API/Design/Decision/Milestone 등 템플릿 |

### 1.2 Document/Metadata/Frontmatter

- **Frontmatter 커버리지**: Vault 49개 문서 **전부** Frontmatter 보유(`--- tags: [...] ---`) — 이 부분은 이미 강점.
- **`type` 필드**: 49개 중 **13개만** `type`을 가짐(M29~M44 Project Intelligence 리포트 9개 + Decision 1 + Task 템플릿 1 + 기타). 나머지 36개(ADR Index/Milestones Index/Architecture 문서/System 문서 등 "핵심" 문서 다수 포함)는 `type` 없음 — Document Type을 Frontmatter로 질의(Dataview 등)할 수 없다.
- **`tags` 필드**: 존재하지만 사실상 **1회성 라벨**로 쓰인다 — `architecture-guardian`/`capability-intelligence`/`experience-intelligence` 등 M29~M44 리포트 태그는 전부 그 문서 하나에서만 등장(재사용 0회). 진짜 반복 태그는 `system`(17회)/`architecture`(5회)/`decision`(4회)/`milestone`(3회)뿐 — **분류 체계가 아니라 폴더명의 변주**에 가깝다.

### 1.3 Wiki Link / Graph 구조

- **완전 고립 문서(outgoing link 0개, 6개)**: `Architecture Guardian.md`/`Experience Intelligence.md`/`Recommendation Execution.md`/`Recommendation Explanation.md`/`Recommendation Intelligence.md`/`Workflow Intelligence.md` — 전부 `15 Project Intelligence/`의 AI 생성 리포트. 다른 문서를 전혀 링크하지 않는다.
- **Orphan 문서(backlink 0개, 4개)**: `13 Daily/README.md`, `14 Tasks/README.md`, `15 Project Intelligence/README.md`, `15 Project Intelligence/Recommendation Explanation.md`.
- **결정적 발견 — "가짜 링크" 문제**: `ADR Index.md`/`Milestones Index.md`는 각 ADR/Milestone 항목에서 관련 파일·클래스를 백틱(`` `Recommendation Explanation.md` ``)으로만 표기하고 **`[[WikiLink]]`를 쓰지 않는다**. 그 결과 ADR/Milestone 본문이 어떤 Vault 문서를 실제로 참조하는지 Graph View와 Backlink 패널에 전혀 나타나지 않는다 — 프로즈(설명)는 풍부하지만 그래프는 텅 비어 있다. 이것이 이번 Milestone이 존재하는 핵심 이유다.
- **PR 참조**: `PR #28`처럼 GitHub PR 번호가 ADR 본문에 텍스트로만 등장 — 별도 PR 노드나 링크 규칙이 없다.
- **집중 허브(backlink 상위)**: `Architecture Overview.md`(62), `PROJECT_INDEX.md`(45), `ADR Index.md`(36), `API Catalog.md`(35) — 이 4개가 사실상 이미 MOC(Map of Content) 역할을 하고 있으나 "MOC"로 명명·설계되지는 않았다.

### 1.4 Graph View 설정(`.obsidian/graph.json`)

현재 6개 `colorGroups`는 전부 **폴더 경로 또는 파일명 문자열 매칭**(`path:"02 Architecture" OR path:"03 ADR" OR ...`)이다 — Document Type이나 Domain Concept가 아니라 "어디 저장돼 있는가"만 색으로 표현한다. `docs/ARCHITECTURE.md` §14(ADR-0054)가 이미 Domain 기반 6-Cluster 체계를 정의해뒀지만(§14.5) "실제 graph.json 반영은 별도 후속 작업"으로 명시적으로 미뤄져 있었다 — 이번이 그 후속이다.

**중요한 제약(변경 없음)**: `.obsidian/graph.json`은 2026-07-30 사용자 결정으로 **Pending Verification 상태로 동결**돼 있다(iOS Obsidian Mobile 환경에서 Desktop 검증 없이는 Schema 비호환/iOS 구현 제약/Mobile 버그 중 원인을 구분할 수 없음). 이번 Milestone도 **`.obsidian/graph.json`을 직접 수정하지 않는다** — Color Strategy는 설계·문서화만 하고, 실제 적용은 Desktop 검증 이후로 미룬다([[Document Type Color Strategy]] 참고).

### 1.5 현재 구조의 장점(증명됨)

1. **Frontmatter 100% 커버리지** — 모든 Vault 문서가 최소한의 구조를 갖춤.
2. **`00 System`이 이미 실질적 MOC** — PROJECT_INDEX를 진입점으로 서로 [[WikiLink]]로 강하게 연결된 "AI 작업 매뉴얼" 역할을 함(재사용 가능한 성공 패턴).
3. **ADR/Decision 2단 계층** — 공식 ADR(무거움)과 비공식 Decision(가벼움)을 의도적으로 분리 — 확장 가능한 설계.
4. **자동 생성 리포트(`15 Project Intelligence/`)의 규율** — "직접 편집 금지, 매번 재계산해 덮어씀"이라는 원칙이 README에 명시돼 있고 실제로 지켜짐.

### 1.6 현재 구조의 한계(증명됨)

1. **ADR/Milestones Index가 단일 파일 무한 append 구조** — 397줄/63건, 102줄/43건. Node 단위 분리 없이 계속 자라기만 해 10년 뒤에는 수천 줄이 된다.
2. **Wiki Link가 아니라 백틱 텍스트로 참조** — Graph/Backlink가 실제 지식 구조를 반영하지 못함(§1.3).
3. **Document Type이 질의 가능한 Metadata가 아님** — 36/49 문서에 `type` 없음, Dataview 등으로 "모든 ADR 목록", "모든 Concept 목록"을 자동 조회할 수 없음.
4. **Tag가 분류 체계로 기능하지 않음** — 대부분 1회성.
5. **설계됐지만 비어 있는 폴더 2개** — `13 Daily`/`14 Tasks`(README만 있고 실제 문서 없음).
6. **범용 템플릿 폴더 다수가 사실상 정체** — `04 Backend`~`10 Android`는 M23~M24 이후 내용이 거의 자라지 않은 1-문서 폴더.
7. **Evergreen Concept 문서 부재** — Recommendation/Guardian/Observability 등 §13 Domain 어휘를 설명하는 "개념 자체"의 독립 문서가 없다 — 전부 `docs/ARCHITECTURE.md`(GitHub 원문)에만 있고 Vault에는 요약조차 없음.
8. **PR/커밋이 Vault에 구조적으로 존재하지 않음** — 텍스트 언급뿐, Node/Link 없음(§1.3).

---

## T02 — Domain & Architecture Analysis

Graphify/Obsidian Best Practice/Second Brain/Knowledge Graph 관점에서
7개 항목을 각각 **채택/수정/기각**으로 판단한다. Graphify 철학을
그대로 복사하지 않는다.

### 1. Knowledge Graph First — **채택(수정)**

Graphify의 "모든 정보를 Node+Edge로 표현한다"는 원칙은 채택한다.
다만 원문 그대로는 아니다 — **이 저장소는 GitHub(`*.ai/DECISIONS.md`
등)가 이미 Source of Truth이고 Vault는 그 파생 뷰**라는 기존 원칙
(§9, ADR-0037)을 깨지 않는다. 따라서 "모든 것을 Node로 만든다"가
아니라 **"GitHub 원문을 대표하는 얇은 Vault Node를 만들고, Node
사이를 Wiki Link로 연결한다"**로 수정 채택한다. Node 자체가 정보의
원본이 되는 순수 Graphify 방식은 기각한다 — 이중 관리(Vault ↔
GitHub) 비용이 이 저장소 규모에서 이득보다 크다.

### 2. Map of Content(MOC) — **채택**

이미 `00 System/PROJECT_INDEX.md`가 사실상 MOC로 기능하고 있음을
T01에서 확인했다 — 이 패턴을 공식화하고 확장한다. 제안하는 Hub:

- **Roadmap Hub**(`docs/ROADMAP.md`를 가리키는 Vault Node) — 전체
  로드맵 진입점
- **Architecture Hub**(`Architecture Overview.md`, 이미 backlink 1위
  — 그대로 승격) — Domain/§8/§13/§14 규칙의 진입점
- **Recommendation Hub**(신규) — M35/M42/M43/M44가 만드는 4개
  리포트(`Recommendation Intelligence/Adaptation은 별도 산출물
  없음/Orchestration은 별도 산출물 없음/Explanation`)를 한 곳에서
  묶어 보여줌 — 현재 이 4개가 서로 링크되지 않는 문제(§1.3)를
  직접 해결
- **ADR Hub**(`ADR Index.md`, 이미 backlink 3위 — 역할 재확인만)
- **Milestone Hub**(`Milestones Index.md` — 역할 재확인만)

자세한 설계는 [[Map of Content Guide]] 참고.

### 3. Wiki Link First — **채택**

T01이 실측한 "백틱 텍스트 참조" 문제(§1.3)를 Wiki Link로 전환하는
것을 원칙으로 채택한다. 다만 **§14.4 Linking Rules(ADR-0054, 이미
존재)의 "완전 연결 그래프 금지" 원칙을 그대로 유지**한다 — 모든
언급을 링크로 바꾸지 않는다. 기준: ① Index→개별 문서(계층적 링크,
필수), ② 실제 소비 관계가 있는 문서 간 직접 링크(예:
Recommendation Intelligence → Recommendation Execution), ③ 그 외
(코드 파일 경로, PR 번호, 클래스명)는 백틱 텍스트로 남긴다 — 코드
심볼까지 Vault Node로 만드는 것은 Graphify 원문에 있지만 **기각**
한다(Vault Node 폭발, GitHub가 이미 원본).

### 4. Metadata First — **채택(최소 원칙 유지)**

Frontmatter 표준을 정의하되(→ [[Metadata Standard]]), "과도한
Metadata를 추가하지 않는다"는 사용자 원칙을 그대로 따른다.
Graphify가 제안하는 광범위한 Metadata 스키마(status/priority/
owner/reviewed 등 10+ 필드)는 **기각**한다 — 이 Vault는 이미
GitHub(`.ai/TASKS.md`)에 Status/Priority가 있어 중복이다. 채택하는
필드는 `type`/`tags`/`project`(선택)/`related`(선택) 4개뿐.

### 5. Project / Label Standard — **수정 채택**

Graphify의 Project/Label 개념을 그대로 쓰지 않는다 — 이 저장소는
이미 `Milestone`(§13.4 명명 규칙)이라는 강한 상위 단위가 있으므로,
Graphify의 "Project"는 **Milestone과 동일시**한다(새 개념 추가
아님). "Label"은 §13.2/13.3의 **Domain Vocabulary**(Intelligence/
Memory/Execution/Guardian/Adaptation/Orchestration/Explainability/
Observability)를 그대로 재사용한다(신규 발명 금지, §1.5 Vocabulary
Reuse First와 동일 원칙). Tag는 이 둘(Milestone/Domain)의 파생값만
허용 — 임의 자유 Tag는 기각(T01에서 확인한 "1회성 Tag" 문제 재발
방지).

### 6. Concept(Evergreen Note) — **채택**

Milestone과 무관하게 유지되는 Concept 문서를 신규 도입한다. §13.2/
13.3에 이미 정의된 8개 어휘(Intelligence/Memory/Execution/Guardian/
Adaptation/Orchestration/Explainability/Observability)를 각각 1개
Concept 문서로 만든다. **내용을 새로 쓰지 않는다** — `docs/
ARCHITECTURE.md` §13의 정의를 그대로 요약 인용하고 GitHub 원문을
가리킨다(원본 중복 금지, §2). Concept 문서는 Milestone 번호가 없고
절대 archive되지 않는다 — Graphify의 "Evergreen Note는 특정 시점에
묶이지 않는다" 원칙을 정확히 이 저장소의 Domain Vocabulary에
적용한 것.

### 7. Document Type Color Strategy — **채택(§14 확장)**

폴더 기준이 아니라 Document Type 기준으로 Color Palette를 재설계
한다. §14.2(ADR-0054)의 Domain Cluster 6종은 **폐기하지 않고
재사용**한다 — Document Type을 더 세분화된 축으로 추가해 §14를
확장한다(중복 발명 금지). 상세 팔레트와 선택 이유는 [[Document Type Color Strategy]]
참고. **`.obsidian/graph.json` 실제 적용은
Desktop 검증 이후로 계속 보류**한다(T01.4의 동결 결정 유지) —
이번 산출물은 색상 체계의 **설계**까지이지 **적용**이 아니다.

---

## T03 — MDD Review

### Node Definition

AI Workspace에서 Knowledge Node는 "GitHub 원문 또는 AI 생성 결과를
대표하는, Wiki Link로 연결 가능한 Vault 문서 1개"로 정의한다.

| Node 종류 | 정의 | 원본(Source of Truth) | Vault 표현 |
|---|---|---|---|
| **ADR** | 아키텍처 결정 1건 | `.ai/DECISIONS.md`의 `## ADR-NNNN` | `ADR Index.md`의 `## ADR-NNNN` 절(현재 유지 — 개별 파일 분리는 [[Vault Migration Plan]] Phase 2 후보) |
| **Milestone** | Milestone 1건 | `.ai/TASKS.md`의 `## Milestone N` | `Milestones Index.md`의 표 행 |
| **PR** | GitHub PR 1건 | GitHub | **Node 아님** — ADR/Milestone 본문에 `PR #NN` 텍스트로만 인라인 표기(T02-3 판단: 코드/트랜잭션성 메타데이터는 Node화하지 않음) |
| **Decision**(비공식) | ADR보다 가벼운 "왜?" 메모 | `Decisions Index.md` 자체가 원본 | `Decisions Index.md`의 절 |
| **Lesson** | 회고/교훈 | 현재 Vault에 없음(T01 확인) | 아직 미도입 — Future Usage([[Vault Information Architecture#Long-term Memory Strategy]]) 참고, 이번에 강제로 만들지 않는다(YAGNI) |
| **Architecture(문서)** | §1~§14 구조 설명 | `docs/ARCHITECTURE.md` | `02 Architecture/*.md` |
| **Concept**(Evergreen) | §13 Domain 어휘 1개 | `docs/ARCHITECTURE.md` §13 | 신규 `02 Architecture/Concepts/*.md`(T02-6) |
| **Project Intelligence(리포트)** | AI 생성 관찰 결과 | 없음(매번 재계산) | `15 Project Intelligence/*.md`(변경 없음) |
| **Runtime(Observability)** | StatusLine 상태 | 없음(휘발성) | **Node 아님** — 영속 문서가 아니라 실시간 표시(§3.37/3.38)이므로 Vault Node 대상에서 제외 |

### Relationship Definition

| 관계 | 의미 | 예시 |
|---|---|---|
| `implements` | 코드가 ADR/Concept를 구현 | (코드는 Node가 아니므로 텍스트로만 표기, 링크 아님) |
| `documents` | 문서가 다른 대상을 설명 | Concept → Architecture Overview |
| `belongs_to` | 하위가 상위에 속함 | ADR → Milestone |
| `generated_by` | AI 생성 리포트의 출처 | Recommendation Intelligence.md → (Service, 텍스트) |
| `explains` | Explanation류 문서가 다른 Node의 근거를 설명 | Recommendation Explanation → Recommendation Intelligence |
| `references` | 느슨한 참조 | Milestone → 관련 ADR |
| `related_to` | 대칭적 연관 | Concept ↔ Concept |
| `decides` | ADR이 Decision을 공식화 | ADR-0054 → "왜 Vocabulary Reuse인가"(Decision) |
| `supersedes` | 새 결정이 이전 결정을 대체 | (현재 사례 없음, 정의만 해 둠) |

모든 관계는 **Wiki Link + 관계를 명시하는 짧은 문구**로 표현한다 —
Dataview/Graphify처럼 별도 관계 타입 Frontmatter 필드는 도입하지
않는다(T03 Dataview Review 참고, 최소 Metadata 원칙 유지).

### Information Architecture — Role 정의

| Role | 정의 | 예시 |
|---|---|---|
| **Folder Role** | Node 종류별 저장 위치(분류 축 아님) | `03 ADR/` = ADR 저장 위치 |
| **Document Role** | 개별 Node | `ADR-0064` 절 |
| **Index Role** | 같은 종류 Node를 시간순으로 모음 | `ADR Index.md` |
| **Hub Role** | 여러 종류 Node를 주제로 묶음(MOC) | Recommendation Hub |
| **Concept Role** | Milestone 무관 Evergreen 정의 | `Concepts/Recommendation.md` |
| **Lesson Role** | 회고(미도입, Future Usage) | — |
| **Roadmap Role** | 시간 축 전체 조망 | `docs/ROADMAP.md`를 가리키는 Vault Node |

### Metadata Standard

→ [[Metadata Standard]] 별도 문서로 분리(참조가 잦아 독립 문서화).

### Graph Strategy

- Graph View는 **Cluster(Domain, §14, 기존 유지) + Document Type
  Color(T02-7, 신규)** 2개 축을 동시에 쓰지 않는다 — 동시 적용 시
  색이 서로 충돌한다. **Document Type Color를 1차 축으로 채택**
  하고, §14 Domain Cluster는 "같은 Document Type 안에서 Domain으로
  더 나누고 싶을 때"의 참고 자료로 격하한다(Deprecation 아님,
  우선순위 조정).
- 탐색 전략: PROJECT_INDEX(진입) → Hub(주제별) → Index(종류별) →
  개별 Node. Graph View는 "탐색 도구"이지 "1차 진입점"이 아니다
  (사람은 여전히 PROJECT_INDEX부터 시작 — §13.4 Retrieval First
  원칙 유지).

### Long-term Memory Strategy

Vault를 AI Memory Layer로 쓰는 기준:

1. **원본(GitHub)과 파생(Vault)을 혼동하지 않는다** — Vault Node는
   항상 원본을 가리키는 "요약+링크"이지 원본의 대체물이 아니다
   (§9 원칙 재확인, 변경 없음).
2. **Concept 문서가 장기 기억의 뼈대다** — Milestone은 오고 가지만
   Domain Vocabulary(Concept)는 남는다. 새 세션(AI든 사람이든)이
   Concept 문서 8개만 읽으면 프로젝트의 핵심 어휘를 전부 복원할 수
   있어야 한다.
3. **Lesson은 지금 강제로 만들지 않는다** — 실제 회고 데이터가
   없는데 빈 구조부터 만들면 Graphify가 경계하는 "구조를 위한
   구조"가 된다. 실제 Automation/Learning이 회고를 생성하기
   시작하면(Future Usage) 그때 Lesson Node를 도입한다.

### Dataview Review

**도입하지 않는다(기각)**. 근거:

- 이 저장소는 iOS Obsidian Mobile 환경이 확인된 유일한 실사용
  환경이다(§1.4, graph.json Pending Verification 배경과 동일) —
  Dataview는 Community Plugin이며 현재 `.obsidian/community-
  plugins.json`이 빈 배열(`[]`)로 **아무 플러그인도 설치돼 있지
  않음**을 실측 확인했다. 새 Plugin 설치는 이번 Milestone의 "기능
  변경 금지" 원칙 밖의 결정이며, Desktop 검증이 막혀 있는 지금
  Mobile에서 Plugin이 정상 동작하는지조차 검증할 수 없다.
- Dataview의 실제 필요(예: "모든 ADR 목록을 자동 조회")는 이미
  `ADR Index.md` 자체가 그 역할을 하고 있어 시급하지 않다.
- **재검토 조건**: Desktop 검증이 풀리고, `type`/`tags` Metadata
  표준(T02-4)이 실제로 안착해 질의할 가치가 있는 데이터가 쌓이면
  그때 별도 제안으로 재검토한다.

---

## T04 — Implementation Proposal

→ [[Vault Migration Plan]]에 Phase별 상세 계획, [[Document Type Color Strategy]]
에 Color Migration 상세.

### Future Usage(이번에 구현하지 않음)

| 소비자 | 향후 활용 방식 |
|---|---|
| **Automation** | Concept 문서의 `type: concept` Frontmatter를 조건으로 삼아, 특정 Domain 관련 Milestone이 끝날 때마다 해당 Concept 문서에 "최근 관련 ADR" 절을 자동 갱신하는 Action을 구상할 수 있다(현재는 수동) |
| **Learning**(M42 Adaptation의 장기 확장) | Lesson Node가 도입되면 Experience Intelligence(M40)의 실패 패턴을 Lesson으로 자동 요약해 Concept에 연결하는 것이 자연스러운 다음 단계 |
| **Dashboard** | Hub 문서(Recommendation Hub 등)를 Dashboard의 "관련 문서" 패널이 그대로 재사용 가능 |
| **Agent(Multi-Agent)** | Concept 문서가 "이 프로젝트에서 X란 무엇인가"의 표준 답변이 되어, Reviewer Agent가 새 코드를 Concept 정의와 대조하는 데 쓸 수 있다 |
| **StatusLine(M45)** | `VaultRuntimeAnalyzer`가 이미 `current_adr`/`current_milestone`을 읽는다 — Hub 구조가 자리잡으면 "현재 어느 Hub 아래에서 작업 중인가"까지 확장 가능(Non-goal, 별도 승인 필요) |
| **MCP(Obsidian MCP)** | Node/Relationship 모델이 명확해지면 MCP를 통한 구조화된 질의("Recommendation Domain의 모든 ADR")가 실제로 의미 있는 답을 준다 — 현재는 백틱 텍스트라 불가능 |

---

## DoD 충족 여부

| 항목 | 상태 |
|---|---|
| 기능 변경 없음 | ✅(`src/` 변경 없음, 이 Milestone은 문서만 생성) |
| Guardian 통과 | ✅(코드 변경 없어 `guardian.checker.evaluate()` 결과 불변) |
| 기존 테스트 전부 통과 | ✅(코드 변경 없음) |
| 기존 Link 최대 유지 | ✅([[Vault Migration Plan]]이 삭제 없는 증분 마이그레이션만 제안) |
| Metadata 표준 정의 | ✅([[Metadata Standard]]) |
| Color Strategy 정의 | ✅([[Document Type Color Strategy]], 적용은 Desktop 검증 대기) |
| MOC 구조 정의 | ✅([[Map of Content Guide]]) |
| Knowledge Graph 설계 완료 | ✅(본 문서 Node/Relationship Definition) |
| Long-term Memory Layer 설계 완료 | ✅(본 문서 Long-term Memory Strategy) |
| Migration Plan 완료 | ✅([[Vault Migration Plan]]) |
