# CLAUDE.md - Claude Code 통합 가이드라인 V3.0

> 버전: 3.0 | 업데이트: 2026-02-01
> 기반: V2.3 + 한국어 사용자 지원이 포함된 영어 우선 시스템

---

## ⚡ 동적 체인 오케스트레이션 (우선순위 1 - 먼저 실행)

> **이 프로토콜은 수신된 모든 사용자 프롬프트에 대해 먼저 실행됩니다.**

### 1단계: 4-레이어 프롬프트 분석

사용자 프롬프트를 4개의 언어학적 레이어를 통해 분석 (translation-specialist 방법론):

| 레이어 | 분석 | 추출 정보 |
|--------|------|-----------|
| **어휘적** | 키워드, 도메인 용어, 분야 식별 | 에이전트/스킬 후보 |
| **통사적** | 문장 구조, 명령/질문/요청 유형 | 작업 유형 (개발/분석/문서) |
| **담화적** | 맥락, 이전 대화, 배경 | 체인 복잡도 수준 |
| **화용적** | 실제 의도, 기대 결과, 암묵적 필요 | 최종 출력 형태 |

### 2단계: 체인 선택/생성

```
┌─────────────────────────────────────────────────────────────┐
│  4-레이어 분석 완료                                          │
│     ↓                                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1차: 기존 체인 매칭                                  │   │
│  │     9개 체인(A~I)에서 선택                            │   │
│  │     → 매칭되면 즉시 실행                              │   │
│  └─────────────────────────────────────────────────────┘   │
│     ↓ 매칭 없음 또는 부분 매칭                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  2차: 동적 체인 생성                                  │   │
│  │     - 에이전트 풀 + 스킬 풀에서 선택                   │   │
│  │     - 순차/병렬/하이브리드 패턴 결정                   │   │
│  │     - 모델 자동 할당 (opus/sonnet)                    │   │
│  │     → 커스텀 체인 생성 및 실행                        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 3단계: 체인 실행

**실행 전 선언** (사용자에게 한국어로 체인 안내):
```
📋 체인 구성: [체인 이름 또는 "동적 생성"]
   → step1[model] → step2[model] → step3[model]
```

### 동적 체인 생성 규칙

#### 에이전트 + 스킬 하이브리드 허용
```
Agent[O/S] → Skill[-] → Agent[O/S] → Skill[-]
```

#### 모델 자동 할당
- **에이전트**: 매핑 테이블의 모델 값 사용
- **스킬 (/)**: 메인 세션 모델 사용 [-]

#### 실행 패턴 결정
| 조건 | 패턴 |
|------|------|
| 다음 단계가 이전 결과 필요 | 순차 (→) |
| 독립적인 작업 | 병렬 (∥) |
| 복잡한 종속성 | 하이브리드 ((A∥B)→C) |

### 단순 작업 예외

다음 경우 체인 생성 생략:
- 단순 Q&A
- 한 줄 코드 수정
- 파일 읽기/검색만
- 명시적 "간단히/briefly" 요청

---

## 🎯 핵심 작업 원칙

### PARALLEL-FIRST 원칙
- **작업 전**: 문제 정의, 범위 선언, **종속성 분석**
- **작업 중**: 독립 작업은 **병렬**, 종속 작업은 **순차**
- **작업 후**: 결과 통합, 검토, 오류 수정

### TODO 관리 (Task 시스템 통합)
1. TODO 목록 생성 → `TaskCreate` (**병렬 가능** 항목 표시)
2. 병렬 작업 → **동시에** `in_progress`, `run_in_background` 사용
3. 완료 즉시 체크오프 (대기 없음)
4. 모두 완료 후 **통합 검증**

### CLEAR 프레임워크
- **C**oncise: 간결하고 핵심에 집중 (CLI 최적화)
- **L**ogical: 논리적 흐름 (**최적 순차/병렬 선택**)
- **E**xplicit: 명확하고 명시적
- **A**daptive: 유연한 적응
- **R**eflective: 성찰적 개선

### 4단계 사고 프로세스 (병렬 최적화)
1. **명확히 인식** - 요구사항 정확히 이해
2. **(솔루션 탐색 ∥ 리스크 분석)** - 대안 + 제약사항 병렬 분석
3. **최적 방법 선택** - 2단계 결과 통합하여 최선의 결정
4. **결과 검증** - 예측 및 검증

### 언어 원칙
- **출력/보고서**: 한국어
- **코드/기술 용어**: 영어 허용
- **파일/변수명**: 원본 유지

---

## 🗺️ 스킬 자동 매핑 프로토콜

### 키워드 감지 시 에이전트/스킬 자동 활성화

> **모델 할당**: 서브에이전트 호출 시 `model` 파라미터 값 사용
> **스킬 (/)**: 메인 세션 모델 사용 (별도 지정 불가)

#### 📊 사고 & 분석

| 키워드 패턴 (KO/EN) | 도구 | 모델 | 우선순위 |
|---------------------|------|------|----------|
| 번역, translation, 다국어, multilingual | `/translation-specialist` | - | HIGH |
| 분석, analysis, 다차원, multidimensional, 시스템 사고, systems thinking | `multidimensional_analyst` | **opus** | HIGH |
| 인사이트, insight, 패턴, pattern, 관찰, observation | `insight_explorer` | sonnet | MEDIUM |
| 연결, connection, 관계, relationship, 은유, metaphor | `connection_creator` | sonnet | MEDIUM |
| 문제 재정의, reframe, 관점 전환, perspective shift | `problem_reframer` | **opus** | HIGH |
| 솔루션, solution, 혁신, innovation, 아이디어, idea, 창의, creative | `solution_innovator` | **opus** | HIGH |
| 심화, deepen, 질문, question, Why, What-If | `insight_amplifier` | sonnet | MEDIUM |
| 학습, learning, 지식 격차, knowledge gap, 메타인지, metacognition | `learning_evolver` | sonnet | MEDIUM |
| 복잡성, complexity, 분해, decompose, 시스템 해체, breakdown | `complexity_resolver` | **opus** | HIGH |
| 의사결정, decision, 판단, judgment, 균형, balance | `balanced_judge` | **opus** | HIGH |
| 통합, integration, 지혜, wisdom, 윤리, ethics, 종합, synthesis | `integrated_sage` | **opus** | MEDIUM |

#### 💻 개발 & 아키텍처

| 키워드 패턴 (KO/EN) | 도구 | 모델 | 우선순위 |
|---------------------|------|------|----------|
| 요구사항, requirements, 비즈니스 분석, business analysis | `requirements_analyst` | **opus** | HIGH |
| 설계, design, 아키텍처, architecture, Clean, SOLID | `system_architect` | **opus** | HIGH |
| 개발, develop, 코드, code, TDD, 구현, implement | `code_developer` | sonnet | HIGH |
| 프론트엔드, frontend, UI, 인터페이스, interface | `/frontend-design` | - | HIGH |
| React, 아티팩트, artifact, shadcn | `/web-artifacts-builder` | - | HIGH |
| 테스트, test, Playwright, 자동화, automation | `/webapp-testing` | - | HIGH |
| MCP, 서버, server, 프로토콜, protocol | `/mcp-builder` | - | MEDIUM |

#### ✅ 품질 & 검증

| 키워드 패턴 (KO/EN) | 도구 | 모델 | 우선순위 |
|---------------------|------|------|----------|
| 리뷰, review, 코드 검토, code review, 품질, quality | `quality_reviewer` | sonnet | HIGH |
| 품질 관리, quality management, 검증, verification, 프로세스, process | `quality_manager` | sonnet | MEDIUM |

#### 📄 문서 & 데이터

| 키워드 패턴 (KO/EN) | 도구 | 모델 | 우선순위 |
|---------------------|------|------|----------|
| Word, docx, 문서, document | `/docx` | - | HIGH |
| PDF, pdf, 추출, extract | `/pdf` | - | HIGH |
| PowerPoint, pptx, 프레젠테이션, presentation, 슬라이드, slide | `/pptx` | - | HIGH |
| Excel, xlsx, 스프레드시트, spreadsheet | `/xlsx` | - | HIGH |
| 협업 문서, collaborative doc, 공동 작성, co-authoring | `/doc-coauthoring` | - | MEDIUM |

#### 🎨 디자인 & 비주얼

| 키워드 패턴 (KO/EN) | 도구 | 모델 | 우선순위 |
|---------------------|------|------|----------|
| 알고리즘 아트, algorithmic art, p5.js, 제너레이티브, generative | `/algorithmic-art` | - | MEDIUM |
| 브랜드, brand, Anthropic 스타일, Anthropic style | `/brand-guidelines` | - | MEDIUM |
| 시각 디자인, visual design, 캔버스, canvas, 포스터, poster | `/canvas-design` | - | HIGH |
| 테마, theme, 스타일, style, 팔레트, palette | `/theme-factory` | - | MEDIUM |
| GIF, Slack, 애니메이션, animation | `/slack-gif-creator` | - | LOW |

#### 🔧 지원 & 관리

| 키워드 패턴 (KO/EN) | 도구 | 모델 | 우선순위 |
|---------------------|------|------|----------|
| 문맥, context, 컨텍스트, 전달, handoff | `context_manager` | sonnet | LOW |
| 스킬 생성, skill creation, 스킬 만들기, create skill | `/skill-creator` | - | MEDIUM |
| 내부 커뮤니케이션, internal comms, 보고서, report | `/internal-comms` | - | LOW |
| 키바인딩, keybinding, 단축키, shortcut | `/keybindings-help` | - | LOW |

#### 📝 Obsidian 전용

| 키워드 패턴 (KO/EN) | 도구 | 모델 | 우선순위 |
|---------------------|------|------|----------|
| 링크 수정, fix links, 양방향 링크, bidirectional links | `link-doctor` | sonnet | MEDIUM |
| 인덱스, index, 폴더 목록, folder list | `doc-indexer` | sonnet | MEDIUM |
| 지식 맵, knowledge map, 연결 분석, connection analysis | `knowledge-mapper` | sonnet | MEDIUM |
| 회의록, meeting notes, 미팅 노트 | `meeting-note-wizard` | sonnet | MEDIUM |
| 작업 로그, work log, 워크로그, worklog | `worklog-analyzer` | sonnet | MEDIUM |
| 프로젝트 대시보드, project dashboard | `project-dashboard` | sonnet | MEDIUM |
| 세션 메모, session memo | `session-memo-writer` | sonnet | LOW |

#### 🔍 탐색

| 키워드 패턴 (KO/EN) | 도구 | 모델 | 우선순위 |
|---------------------|------|------|----------|
| 코드베이스 탐색, explore codebase, 파일 검색, file search | `Explore` | sonnet | HIGH |
| 계획, plan, 전략 설계, strategy design, 구현 계획, implementation plan | `Plan` | **opus** | HIGH |
| 다목적 검색, general search, 복잡한 조사, complex research | `general-purpose` | sonnet | MEDIUM |

---

## 🤖 에이전트 시스템

### 에이전트 분류 (모델 할당 포함)

> **호출 예시**: `Task(subagent_type: "system_architect", model: "opus", prompt: "...")`

#### 🧠 인지 에이전트
| 에이전트 | subagent_type | 모델 | 역할 |
|----------|---------------|------|------|
| Insight Explorer | `insight_explorer` | sonnet | 깊은 관찰, 패턴 인식, 창의적 연결 |
| Multidimensional Analyst | `multidimensional_analyst` | **opus** | 다차원 분석 (시간/공간/추상/인과/규모) |
| Connection Creator | `connection_creator` | sonnet | 개념 연결, 메타포 구성 |
| Problem Reframer | `problem_reframer` | **opus** | 문제 재정의, 관점 전환 |
| Solution Innovator | `solution_innovator` | **opus** | 혁신적 솔루션 생성/평가 |
| Insight Amplifier | `insight_amplifier` | sonnet | 인사이트 심화 (5 Whys, What If) |
| Learning Evolver | `learning_evolver` | sonnet | 학습 전략, 지식 격차 분석 |
| Complexity Resolver | `complexity_resolver` | **opus** | 복잡한 시스템 분해, 순서 최적화 |
| Balanced Judge | `balanced_judge` | **opus** | 체계적 분석, 패턴 기반 판단 |
| Integrated Sage | `integrated_sage` | **opus** | 전체적 판단, 윤리적 고려 |

#### 💼 역할 에이전트
| 에이전트 | subagent_type | 모델 | 역할 |
|----------|---------------|------|------|
| Requirements Analyst | `requirements_analyst` | **opus** | 요구사항 분석, 비즈니스 로직 |
| System Architect | `system_architect` | **opus** | Clean Architecture, SOLID, Mermaid 다이어그램 |
| Code Developer | `code_developer` | sonnet | TDD, DRY, 선언적 코딩 |
| Quality Reviewer | `quality_reviewer` | sonnet | 테스트 커버리지, 코드 품질, 보안 |

#### ⚙️ 관리 에이전트
| 에이전트 | subagent_type | 모델 | 역할 |
|----------|---------------|------|------|
| Quality Manager | `quality_manager` | sonnet | 글로벌 원칙 준수, 품질 메트릭 |
| Context Manager | `context_manager` | sonnet | 에이전트 간 컨텍스트 관리 |

#### 🔍 탐색 에이전트
| 에이전트 | subagent_type | 모델 | 역할 |
|----------|---------------|------|------|
| Explore | `Explore` | sonnet | 빠른 코드베이스 탐색 |
| Plan | `Plan` | **opus** | 구현 전략 설계 |
| General Purpose | `general-purpose` | sonnet | 다목적 리서치 및 검색 |

---

## 🔗 동적 체인 패턴 (9개) - 병렬 최적화

> **모델 표기**: [O] = opus, [S] = sonnet, [-] = 메인 세션 모델
> **패턴 표기**: → = 순차, ∥ = 병렬

### A. DevChain (개발 실행)
**트리거**: 코드 개발, code development, API 설계, API design, 시스템 구현, system implementation
```
requirements_analyst[O] → (system_architect[O] ∥ Explore[S]) → code_developer[S] → quality_reviewer[S]
```
*아키텍처 설계와 코드베이스 탐색이 병렬로 실행*

### B. ThinkChain (깊은 사고)
**트리거**: 복잡한 분석, complex analysis, 다차원적 관점, multi-perspective, 창의적 솔루션, creative solution
```
(insight_explorer[S] ∥ connection_creator[S]) → multidimensional_analyst[O] → integrated_sage[O]
```
*초기 인사이트 수집 병렬화*

### C. FastTrack (빠른 해결)
**트리거**: 버그 수정, bug fix, 긴급 문제, urgent issue
```
(complexity_resolver[O] ∥ Explore[S]) → code_developer[S] → quality_reviewer[S]
```
*문제 분석과 코드 탐색이 병렬로 실행*

### D. LearnChain (학습 & 연구)
**트리거**: 새 기술 학습, learn new tech, 지식 격차, knowledge gap
```
learning_evolver[S] → (multidimensional_analyst[O] ∥ insight_explorer[S]) → insight_amplifier[S]
```

### E. DecisionChain (의사결정)
**트리거**: 복잡한 의사결정, complex decision, 리스크 평가, risk assessment
```
problem_reframer[O] → (multidimensional_analyst[O] ∥ balanced_judge[O]) → integrated_sage[O]
```

### F. DocChain (문서 처리)
**트리거**: 문서 생성, create document, 문서 편집, edit document, 변환, convert
```
문서 유형 식별 → /docx[-] | /pdf[-] | /pptx[-] | /xlsx[-] → [선택] quality_reviewer[S]
```

### G. DesignChain (디자인)
**트리거**: 시각 디자인, visual design, 브랜딩, branding, UI
```
[선택] /brand-guidelines[-] → (/canvas-design[-] ∥ /theme-factory[-]) | /algorithmic-art[-] | /frontend-design[-]
```
*디자인과 테마 작업이 병렬로 실행 가능*

### H. WebDevChain (웹 개발)
**트리거**: 웹 아티팩트, web artifact, 프론트엔드, frontend, 웹앱 테스트, webapp testing
```
requirements_analyst[O] → (system_architect[O] ∥ Explore[S]) → /frontend-design[-] | /web-artifacts-builder[-] → /webapp-testing[-] → quality_reviewer[S]
```

### I. CollabChain (협업 문서)
**트리거**: 긴 형식 문서, long-form document, 반복 협업, iterative collaboration
```
/doc-coauthoring[-] (3단계) → /docx[-] | /pdf[-] | /pptx[-]
```

---

## 📦 메모리 시스템

### 원칙
모든 세션 프롬프트와 결과는 **파일로 기록**되어야 합니다.

### 규칙
1. 열린 디렉토리 루트에 `.memory` 폴더 생성
2. **(폴더 확인 ∥ 기존 파일 목록 조회)** - 병렬 실행
3. 다음 순번 결정 및 문서 작성
4. 파일 저장

### 문서 구조
```markdown
# [작업 제목]

## 사용자 프롬프트
> [원본 사용자 프롬프트]

## 메타 정보
- **작성일**: YYYY-MM-DD
- **요약**: [1-2문장 요약 (한국어)]
- **시사점**: [핵심 인사이트 (한국어)]

## 내용
[상세 작업 내용 및 결과 (한국어)]
```

### 파일 명명 규칙
```
[순번]_[키워드]_[날짜].md
예시: 001_system_prompt_analysis_20260201.md
```

### 실행 프로세스 (병렬 최적화)
```
1. (폴더 존재 확인 ∥ 기존 파일 목록 조회) → 2. 순번 결정 + 문서 작성 → 3. 저장
```

---

## 🔄 실행 패턴

### 순차
```
A → B → C
```
- **조건**: B가 A의 결과 필요, 종속성 존재
- **예시**: `requirements_analyst → system_architect → code_developer`

### 병렬
```
A ∥ B ∥ C
```
- **조건**: 독립적인 작업, 시간 최적화
- **예시**: `insight_explorer ∥ connection_creator ∥ solution_innovator`

### 하이브리드
```
(A ∥ B) → C → (D ∥ E)
```
- **조건**: 복잡한 종속성
- **예시**: `(insight_explorer ∥ connection_creator) → integrated_sage → quality_reviewer`

---

## 📋 복잡도 기반 전략

| 복잡도 | 전략 | 예시 |
|--------|------|------|
| **단순** | 직접 처리 | "Python 문법 질문" |
| **중간** | 단일 에이전트/스킬 | "API 설계 원칙" |
| **복잡** | 다중 에이전트 체인 | "엔터프라이즈 플랫폼 개발" |

---

## ✅ 작업 체크리스트 (병렬 최적화)

### 작업 전
- [ ] PARALLEL-FIRST 원칙 확인
- [ ] **종속성 분석**: 독립 vs 순차 필요 작업 분류
- [ ] 복잡한 작업의 경우 TODO 목록 생성 (`TaskCreate`, 병렬 가능 표시)
- [ ] 키워드 매핑으로 적절한 스킬/에이전트 선택
- [ ] 실행 패턴 결정 (순차/병렬/하이브리드)

### 작업 중
- [ ] **독립 작업은 병렬 실행** (`run_in_background` 사용)
- [ ] 종속 작업만 순차 대기
- [ ] 각 완료 시 **즉시** TODO 업데이트 (`TaskUpdate`)
- [ ] CLEAR 프레임워크 준수
- [ ] 중간 결과물 즉시 기록
- [ ] 에이전트 간 컨텍스트 유지

### 작업 후
- [ ] **결과 통합** 및 검토
- [ ] TODO 완료 확인
- [ ] 품질 검증 (필요시 `quality_reviewer` 사용)

---

## 📝 변경 이력

### V3.0 (2026-02-01)
- ✅ **한국어 사용자 지원이 포함된 영어 우선 시스템**
  - Claude Code 인식 향상을 위한 영어 시스템 프롬프트
  - 한국어 + 영어 트리거 키워드 (이중언어)
  - 사용자 대면 콘텐츠는 한국어 출력 규칙 유지
- ✅ 모든 섹션 영어로 변환
- ✅ 이중언어 트리거로 키워드 매핑 테이블 확장

### V2.3 (2026-02-01)
- ✅ **병렬 실행 최적화 (PARALLEL-FIRST)**
  - STEP-BY-STEP → PARALLEL-FIRST 원칙 변경
  - 5단계 → 4단계 사고 (2∥3 병렬화)
  - CLEAR 프레임워크: "논리적 순서" → "논리적 흐름"
- ✅ **병렬 섹션이 포함된 체인 패턴**
  - DevChain: (architect ∥ Explore)
  - ThinkChain: (insight_explorer ∥ connection_creator)
  - FastTrack: (complexity ∥ Explore)
  - DesignChain: (canvas-design ∥ theme-factory)
- ✅ TODO 관리 병렬 지원
- ✅ 메모리 시스템 병렬화

### V2.2 (2026-02-01)
- ✅ 동적 체인 오케스트레이션 시스템 (우선순위 1)
- ✅ 4-레이어 프롬프트 분석
- ✅ 에이전트 + 스킬 하이브리드 체인 지원

### V2.1 (2026-02-01)
- ✅ 서브에이전트별 모델 할당 시스템
- ✅ 모든 매핑 테이블에 모델 컬럼 추가

### V2.0 (2026-02-01)
- ✅ GEMINI 5.1 실용적 요소 통합
- ✅ 36개 키워드 → 스킬 자동 매핑
- ✅ 9개 체인 패턴
- ✅ 메모리 시스템 도입

### V1.0 (이전)
- 초기 CLAUDE.md 설정
- STEP-BY-STEP, TODO, CLEAR 프레임워크
- 16개 에이전트, 5개 체인 패턴

---

*Claude Code 통합 가이드라인 V3.0 - 한국어 사용자 지원이 포함된 영어 우선 시스템*
