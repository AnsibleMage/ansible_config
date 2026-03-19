# Claude Code 사용 가능한 도구 목록

> 마지막 업데이트: 2026-02-01

---

## 🤖 서브에이전트 (Sub-Agents)

Task 도구를 통해 호출 가능한 전문화된 에이전트들입니다.

### 🔍 탐색 및 기본 에이전트

| 에이전트 | subagent_type | 역할 | 사용 시점 |
|---------|---------------|------|----------|
| **Bash** | `Bash` | Git 작업, 명령어 실행, 터미널 작업 | Git 명령, 시스템 명령 실행 |
| **Explore** | `Explore` | 코드베이스 빠른 탐색, 파일/키워드 검색 | 파일 패턴 검색, 코드베이스 이해 |
| **Plan** | `Plan` | 구현 전략 설계, 단계별 계획 수립 | 복잡한 작업의 계획 단계 |
| **General Purpose** | `general-purpose` | 다목적 연구, 코드 검색, 다단계 작업 | 복잡한 검색, 멀티스텝 작업 |

### 🧠 인지 에이전트 (Cognitive Agents)

| 에이전트 | subagent_type | 역할 | 사용 시점 |
|---------|---------------|------|----------|
| **Insight Explorer** | `insight_explorer` | 깊은 관찰, 패턴 인식, 창의적 연결 발견 | 숨겨진 패턴 발견, 창의적 인사이트 필요 시 |
| **Multidimensional Analyst** | `multidimensional_analyst` | 시간/공간/추상화/인과/규모 차원 분석 | 복잡한 시스템의 다각적 분석 |
| **Connection Creator** | `connection_creator` | 개념 간 연결 발견, 메타포 구성 | 서로 다른 개념 연결, 유추적 이해 |
| **Problem Reframer** | `problem_reframer` | 문제 재정의, 관점 전환, 제약 재검토 | 막힌 문제를 새로운 각도로 접근 |
| **Solution Innovator** | `solution_innovator` | 혁신적 솔루션 생성 및 평가 | 창의적 해결책, 새로운 아이디어 |
| **Insight Amplifier** | `insight_amplifier` | 인사이트 심화 (5 Whys, What If) | 초기 인사이트를 깊고 넓게 확장 |
| **Learning Evolver** | `learning_evolver` | 학습 전략, 지식 격차 분석, 메타인지 | 새로운 기술/개념 학습, 연구 |
| **Complexity Resolver** | `complexity_resolver` | 복잡한 시스템 분해, 순서 최적화 | 대규모 시스템 이해 및 분해 |
| **Balanced Judge** | `balanced_judge` | 체계적 분석, 패턴 기반 판단 | 중요한 결정, 여러 옵션 평가 |
| **Integrated Sage** | `integrated_sage` | 종합적 판단, 윤리적 고려, 검증 | 최종 통합 판단, 전체적 관점 |

### 💼 역할 에이전트 (Role Agents)

| 에이전트 | subagent_type | 역할 | 사용 시점 |
|---------|---------------|------|----------|
| **Requirements Analyst** | `requirements_analyst` | 요구사항 분석, 비즈니스 로직, 리스크 평가 | 프로젝트 시작, 요구사항 수집 |
| **System Architect** | `system_architect` | Clean Architecture, SOLID, Mermaid 다이어그램 | 시스템 설계, 아키텍처 문서화 |
| **Code Developer** | `code_developer` | TDD, DRY, 선언적 코딩 스타일 | 실제 코드 구현, 테스트 작성 |
| **Quality Reviewer** | `quality_reviewer` | 테스트 커버리지, 코드 품질, 성능, 보안 | 코드 리뷰, 품질 검증 |

### ⚙️ 관리 에이전트 (Management Agents)

| 에이전트 | subagent_type | 역할 | 사용 시점 |
|---------|---------------|------|----------|
| **Quality Manager** | `quality_manager` | 전역 원칙 준수, 품질 지표, 최종 검토 | 중요 작업 후 품질 검증 |
| **Context Manager** | `context_manager` | 에이전트 간 컨텍스트 관리 및 핸드오프 | 복잡한 멀티 에이전트 워크플로우 |

### 📝 Obsidian 전용 에이전트

| 에이전트 | subagent_type | 역할 | 사용 시점 |
|---------|---------------|------|----------|
| **Link Doctor** | `link-doctor` | 양방향 링크 관리, 누락/깨진 링크 수정 | 링크 일관성 보장 |
| **Doc Indexer** | `doc-indexer` | 폴더별 인덱스 파일 생성/업데이트 | 파일 목록 정리, 구조 시각화 |
| **Knowledge Mapper** | `knowledge-mapper` | 문서 간 연결 분석, 지식 맵 생성 | 고립된 문서 찾기, 관계 분석 |
| **Meeting Note Wizard** | `meeting-note-wizard` | 구조화된 회의록 템플릿 생성 | 회의록 관리 |
| **Worklog Analyzer** | `worklog-analyzer` | 일일 작업 로그 요약, 패턴 분석 | 작업 패턴 인사이트 |
| **Project Dashboard** | `project-dashboard` | 프로젝트 현황 대시보드 생성 | 프로젝트별 통계 확인 |
| **Session Memo Writer** | `session-memo-writer` | 세션 메모 자동 생성 | 세션 간 컨텍스트 연속성 |
| **Memory Report Generator** | `memory-report-generator` | AI 기억 시스템, 진화 과정 문서화 | 시간 캡슐 보고서 생성 |

### 🛠️ 기타 유틸리티 에이전트

| 에이전트 | subagent_type | 역할 | 사용 시점 |
|---------|---------------|------|----------|
| **Claude Code Guide** | `claude-code-guide` | Claude Code CLI 사용법, MCP 서버, API 안내 | Claude Code 기능 질문 |
| **Statusline Setup** | `statusline-setup` | Claude Code 상태 표시줄 설정 | 상태줄 커스터마이징 |

---

## 🎯 스킬 (Skills)

Skill 도구를 통해 호출 가능한 전문화된 기능들입니다. `/스킬명` 형식으로 사용합니다.

### 📄 문서 작업

| 스킬 | 명령어 | 설명 |
|-----|--------|------|
| **PDF** | `/pdf` | PDF 텍스트/테이블 추출, 생성, 병합/분할, 폼 처리 |
| **DOCX** | `/docx` | Word 문서 생성/편집, 변경 추적, 코멘트, 서식 유지 |
| **XLSX** | `/xlsx` | 스프레드시트 생성/편집, 수식, 데이터 분석, 시각화 |
| **PPTX** | `/pptx` | 프레젠테이션 생성/편집, 레이아웃, 스피커 노트 |
| **Doc Coauthoring** | `/doc-coauthoring` | 문서 공동 작성 워크플로우 가이드 |

### 🎨 디자인 및 시각화

| 스킬 | 명령어 | 설명 |
|-----|--------|------|
| **Frontend Design** | `/frontend-design` | 고품질 프론트엔드 인터페이스 생성 |
| **Canvas Design** | `/canvas-design` | PNG/PDF 시각적 아트 및 디자인 생성 |
| **Algorithmic Art** | `/algorithmic-art` | p5.js 기반 생성적 아트 제작 |
| **Theme Factory** | `/theme-factory` | 10가지 프리셋 테마로 아티팩트 스타일링 |
| **Brand Guidelines** | `/brand-guidelines` | Anthropic 브랜드 색상/타이포그래피 적용 |
| **Slack GIF Creator** | `/slack-gif-creator` | Slack 최적화 애니메이션 GIF 생성 |

### 🌐 웹 개발

| 스킬 | 명령어 | 설명 |
|-----|--------|------|
| **Web Artifacts Builder** | `/web-artifacts-builder` | React, Tailwind, shadcn/ui 기반 복잡한 아티팩트 생성 |
| **Webapp Testing** | `/webapp-testing` | Playwright 기반 로컬 웹앱 테스트 |
| **MCP Builder** | `/mcp-builder` | MCP 서버 생성 가이드 (Python FastMCP / Node TypeScript) |

### 📝 커뮤니케이션 및 번역

| 스킬 | 명령어 | 설명 |
|-----|--------|------|
| **Translation Specialist** | `/translation-specialist` | 4-Layer 언어학적 분석 기반 전문 번역 |
| **Internal Comms** | `/internal-comms` | 내부 커뮤니케이션 작성 (상태 보고서, 뉴스레터 등) |

### ⚙️ 설정 및 유틸리티

| 스킬 | 명령어 | 설명 |
|-----|--------|------|
| **Keybindings Help** | `/keybindings-help` | 키보드 단축키 커스터마이징 |
| **Skill Creator** | `/skill-creator` | 새로운 스킬 생성 가이드 |

---

## 📌 사용 예시

### 서브에이전트 호출
```
Task(
  subagent_type: "system_architect",
  description: "시스템 설계",
  prompt: "사용자 인증 시스템 아키텍처를 설계해주세요..."
)
```

### 스킬 호출
```
/pdf           → PDF 작업
/translation-specialist → 번역 작업
/frontend-design → 프론트엔드 디자인
```

### 탐색 에이전트 깊이 설정
- `"quick"`: 기본 검색
- `"medium"`: 중간 수준 탐색
- `"very thorough"`: 포괄적 분석

---

## 🔄 추천 워크플로우

### 새 기능 개발
```
requirements_analyst → system_architect → code_developer → quality_reviewer
```

### 코드베이스 이해
```
Explore → multidimensional_analyst → problem_reframer → solution_innovator
```

### 문서 작업
```
/doc-coauthoring (워크플로우) → /docx 또는 /pdf (출력)
```

---

*이 문서는 Claude Code에서 사용 가능한 도구들을 정리한 참조 문서입니다.*
