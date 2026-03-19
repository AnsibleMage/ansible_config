# Claude Code Component Catalog

> Claude Code에서 사용되는 모든 구성 요소를 분류하고 정리한 종합 카탈로그
> 작성일: 2026-02-06 | 기준 버전: Claude Code 1.0.33+

---

## 목차

1. [빌트인 서브에이전트 (Built-in Subagents)](#1-빌트인-서브에이전트)
2. [커스텀 서브에이전트 (Custom Subagents)](#2-커스텀-서브에이전트)
3. [빌트인 스킬 (Built-in Skills)](#3-빌트인-스킬)
4. [커스텀 스킬 (Custom Skills)](#4-커스텀-스킬)
5. [커스텀 슬래시 커맨드 (Custom Slash Commands)](#5-커스텀-슬래시-커맨드)
6. [Hook 시스템 (Hooks)](#6-hook-시스템)
7. [MCP 서버 (MCP Servers)](#7-mcp-서버)
8. [플러그인 - 공식 (Official Plugins)](#8-공식-플러그인)
9. [플러그인 - 외부 연동 (External Plugins)](#9-외부-연동-플러그인)
10. [빌트인 CLI 커맨드 (Built-in Commands)](#10-빌트인-cli-커맨드)
11. [스크립트 (Scripts)](#11-커스텀-스크립트)

---

## 1. 빌트인 서브에이전트

> 공식 Anthropic 제공. Claude Code에 기본 내장.

| # | 서브에이전트 | 기본 모델 | 용도 | 저자 |
|---|------------|----------|------|------|
| 1 | `Explore` | Haiku | 코드베이스 탐색, 파일 검색 (읽기 전용) | Anthropic (공식) |
| 2 | `Plan` | 상속 | Plan 모드에서 코드베이스 리서치 (읽기 전용) | Anthropic (공식) |
| 3 | `general-purpose` | 상속 | 범용 멀티스텝 작업 처리 | Anthropic (공식) |

**특징**:
- 부모 대화의 권한 상속
- 독립된 컨텍스트 윈도우에서 실행
- 도구 접근 제한 가능 (Explore/Plan은 Write/Edit 불가)

---

## 2. 커스텀 서브에이전트

> 앤(An)이 CLAUDE.md에 정의. `~/.claude/agents/` 또는 `.claude/agents/` 위치.

### 2-1. Cognitive Agents (인지 에이전트)

| # | 서브에이전트 | `subagent_type` | 할당 모델 | 용도 | 저자 |
|---|------------|-----------------|----------|------|------|
| 1 | Insight Explorer | `insight_explorer` | sonnet | 패턴 인식, 숨겨진 관계 발견 | 앤 (커스텀) |
| 2 | Multidimensional Analyst | `multidimensional_analyst` | **opus** | 5차원 다면 분석 (시간/공간/추상화/인과/규모) | 앤 (커스텀) |
| 3 | Connection Creator | `connection_creator` | sonnet | 개념 간 창의적 연결, 메타포 구축 | 앤 (커스텀) |
| 4 | Problem Reframer | `problem_reframer` | **opus** | 문제 재정의, 관점 전환 | 앤 (커스텀) |
| 5 | Solution Innovator | `solution_innovator` | **opus** | 혁신적 솔루션 생성, 크로스 도메인 | 앤 (커스텀) |
| 6 | Insight Amplifier | `insight_amplifier` | sonnet | Why/What-If 반복으로 인사이트 심화 | 앤 (커스텀) |
| 7 | Learning Evolver | `learning_evolver` | sonnet | 학습 전략, 지식 격차 식별 | 앤 (커스텀) |
| 8 | Complexity Resolver | `complexity_resolver` | **opus** | 복잡 시스템 분해 (3-7 컴포넌트/레벨) | 앤 (커스텀) |
| 9 | Balanced Judge | `balanced_judge` | **opus** | 의사결정, 체계적 분석 + 패턴 판단 | 앤 (커스텀) |
| 10 | Integrated Sage | `integrated_sage` | **opus** | 종합 지혜, 윤리 고려, 최종 판단 | 앤 (커스텀) |

### 2-2. Role Agents (역할 에이전트)

| # | 서브에이전트 | `subagent_type` | 할당 모델 | 용도 | 저자 |
|---|------------|-----------------|----------|------|------|
| 11 | Requirements Analyst | `requirements_analyst` | **opus** | 요구사항 도출, 비즈니스 로직 매핑 | 앤 (커스텀) |
| 12 | System Architect | `system_architect` | **opus** | Clean Architecture, SOLID, 마이크로서비스 설계 | 앤 (커스텀) |
| 13 | Code Developer | `code_developer` | sonnet | TDD 기반 개발, DRY, 선언형 코딩 | 앤 (커스텀) |
| 14 | Quality Reviewer | `quality_reviewer` | sonnet | 코드 리뷰, 테스트 커버리지, 보안 | 앤 (커스텀) |

### 2-3. Management Agents (관리 에이전트)

| # | 서브에이전트 | `subagent_type` | 할당 모델 | 용도 | 저자 |
|---|------------|-----------------|----------|------|------|
| 15 | Quality Manager | `quality_manager` | sonnet | CLEAR 프레임워크 준수, 단계별 품질 검증 | 앤 (커스텀) |
| 16 | Context Manager | `context_manager` | sonnet | 에이전트 간 정보 흐름, 의존성 관리 | 앤 (커스텀) |

### 2-4. Utility Agents (유틸리티 에이전트)

| # | 서브에이전트 | `subagent_type` | 용도 | 저자 |
|---|------------|-----------------|------|------|
| 17 | Memory Report Generator | `memory-report-generator` | AI 기억 시스템 진화 보고서 생성 | 앤 (커스텀) |
| 18 | Meeting Note Wizard | `meeting-note-wizard` | 구조화된 회의록 자동 생성 | 앤 (커스텀) |
| 19 | Session Memo Writer | `session-memo-writer` | 세션 메모 자동 생성 | 앤 (커스텀) |
| 20 | Project Dashboard | `project-dashboard` | 프로젝트 현황 대시보드 생성 | 앤 (커스텀) |
| 21 | Worklog Analyzer | `worklog-analyzer` | 작업 로그 분석, 패턴 인사이트 | 앤 (커스텀) |
| 22 | Link Doctor | `link-doctor` | Obsidian 양방향 링크 관리 | 앤 (커스텀) |
| 23 | Doc Indexer | `doc-indexer` | 폴더별 인덱스 파일 자동 생성 | 앤 (커스텀) |
| 24 | Knowledge Mapper | `knowledge-mapper` | 문서 간 연결 구조 분석, 지식 맵 | 앤 (커스텀) |

**총 서브에이전트: 27개** (빌트인 3 + 커스텀 24)

---

## 3. 빌트인 스킬

> Anthropic 공식 제공. Claude Code 설치 시 기본 포함.

| # | 스킬 | 호출 | 용도 | 저자 |
|---|------|------|------|------|
| 1 | Document Creation | `/docx` | Word 문서 생성/편집/분석 (tracked changes, comments) | Anthropic (공식) |
| 2 | PDF Toolkit | `/pdf` | PDF 추출, 생성, 병합/분할, 폼 처리 | Anthropic (공식) |
| 3 | Presentation | `/pptx` | PowerPoint 생성/편집/레이아웃 | Anthropic (공식) |
| 4 | Spreadsheet | `/xlsx` | Excel 생성/편집, 수식, 차트 | Anthropic (공식) |
| 5 | Skill Creator | `/skill-creator` | 새로운 스킬 생성 가이드 | Anthropic (공식) |
| 6 | Doc Co-authoring | `/doc-coauthoring` | 구조화된 문서 공동 작성 워크플로우 | Anthropic (공식) |
| 7 | Frontend Design | `/frontend-design` | 프로덕션급 프론트엔드 UI 생성 | Anthropic (공식) |
| 8 | Canvas Design | `/canvas-design` | PNG/PDF 비주얼 아트, 포스터 | Anthropic (공식) |
| 9 | Algorithmic Art | `/algorithmic-art` | p5.js 기반 제너레이티브 아트 | Anthropic (공식) |
| 10 | Web Artifacts Builder | `/web-artifacts-builder` | React + shadcn/ui 멀티컴포넌트 아티팩트 | Anthropic (공식) |
| 11 | Webapp Testing | `/webapp-testing` | Playwright 기반 웹앱 테스트 | Anthropic (공식) |
| 12 | MCP Builder | `/mcp-builder` | MCP 서버 생성 가이드 (Python/Node) | Anthropic (공식) |
| 13 | Theme Factory | `/theme-factory` | 아티팩트 테마 스타일링 (10개 프리셋) | Anthropic (공식) |
| 14 | Brand Guidelines | `/brand-guidelines` | Anthropic 브랜드 색상/타이포그래피 적용 | Anthropic (공식) |
| 15 | Slack GIF Creator | `/slack-gif-creator` | Slack 최적화 애니메이션 GIF 생성 | Anthropic (공식) |
| 16 | Internal Comms | `/internal-comms` | 사내 커뮤니케이션 문서 작성 | Anthropic (공식) |

---

## 4. 커스텀 스킬

> 앤(An)이 직접 생성. `~/.claude/skills/` 위치.

| # | 스킬 | 호출 | 용도 | 저자 |
|---|------|------|------|------|
| 1 | Translation Specialist | `/translation-specialist` | 4-Layer 언어학적 분석 기반 전문 번역 | 앤 (커스텀) |
| 2 | Claude Strategy | `/claude-strategy` | 프로젝트 특성 분석 → Claude Code 사용전략 문서 자동 생성 (체인/에이전트/스킬/Teams/Hook 매핑) | 앤 (커스텀) |
| 3 | Vibe Dev | `/vibe-dev` | 문서 기반 AI 페어 프로그래밍 (4-Phase: 조사→정의→개발→보고, Zero-Guess Protocol, Stage/Gate) | 앤 (커스텀) |

---

## 5. 커스텀 슬래시 커맨드

> 앤(An)이 직접 생성. `~/.claude/commands/` 위치.
> 스킬과 커맨드는 동일하게 `/name`으로 호출됨 (커맨드는 스킬로 통합됨).

### 5-1. 일반 커맨드

| # | 커맨드 | 호출 | 용도 | 저자 |
|---|--------|------|------|------|
| 1 | Commit Push | `/commit-push` | Git 커밋 + 푸시 자동화 | 앤 (커스텀) |
| 2 | PR Review | `/pr-review` | PR diff 변경사항 리뷰 | 앤 (커스텀) |
| 3 | Project Review | `/project-review` | 프로젝트 전체 아키텍처/품질 평가 | 앤 (커스텀) |
| 4 | Memory Save | `/memory-save` | 현재 작업을 메모리 파일로 저장 | 앤 (커스텀) |
| 5 | README Gen | `/readme-gen` | README.md 자동 생성 (영어+한국어) | 앤 (커스텀) |
| 6 | Analyze | `/analyze` | 프롬프트 4-Layer 분석 | 앤 (커스텀) |

### 5-2. Rails 8 바이브코딩 커맨드

| # | 커맨드 | 호출 | 용도 | 저자 |
|---|--------|------|------|------|
| 7 | Rails Init | `/rails-init` | Rails 8 프로젝트 생성 및 초기 설정 | 앤 (커스텀) |
| 8 | Rails PRD | `/rails-prd` | 요구사항 → PRD 문서 자동 생성 | 앤 (커스텀) |
| 9 | Rails Plan | `/rails-plan` | PRD → 작업계획서 + TODO 생성 | 앤 (커스텀) |
| 10 | Rails Dev | `/rails-dev` | TDD 기반 개발 (RED-GREEN-REFACTOR) | 앤 (커스텀) |
| 11 | Rails Test | `/rails-test` | 전체 테스트 + 품질 검증 | 앤 (커스텀) |
| 12 | Rails Deploy | `/rails-deploy` | Kamal 2 프로덕션 배포 | 앤 (커스텀) |
| 13 | Rails Verify | `/rails-verify` | 프로덕션 헬스체크 + 스모크 테스트 | 앤 (커스텀) |

---

## 6. Hook 시스템

> `~/.claude/settings.json`에 정의. 이벤트 기반 자동 실행.

### 6-1. 이벤트 타입

| 이벤트 | 시점 | 설명 | 출처 |
|--------|------|------|------|
| `SessionStart` | 세션 시작 | Claude Code 시작 시 한 번 실행 | Anthropic (공식 기능) |
| `UserPromptSubmit` | 프롬프트 전송 직전 | 사용자 입력 분석/전처리 | Anthropic (공식 기능) |
| `PreToolUse` | 도구 실행 전 | 명령 로깅, 보안 차단 | Anthropic (공식 기능) |
| `PostToolUse` | 도구 실행 후 | 자동 포매팅, 알림 | Anthropic (공식 기능) |
| `Stop` | 응답 완료 후 | 후처리 (제한적) | Anthropic (공식 기능) |
| `SubagentStop` | 서브에이전트 완료 후 | 서브에이전트 결과 후처리 | Anthropic (공식 기능) |

### 6-2. 현재 등록된 Hook 스크립트

| # | Hook | 이벤트 | 파일 | 기능 | 저자 |
|---|------|--------|------|------|------|
| 1 | 세션 시작 알림 | `SessionStart` | inline | `🚀 Claude Code 세션 시작` 표시 | 앤 (커스텀) |
| 2 | 4-Layer 분석 + 이전 저장 | `UserPromptSubmit` | `auto-analyze.sh` | 프롬프트 자동 분석 + 이전 프롬프트 저장 지시 | 앤 (커스텀) |
| 3 | Bash 실행 로깅 | `PreToolUse` (Bash) | inline | `[🔵 실행 예정] Bash 명령: ...` | 앤 (커스텀) |
| 4 | 보안 파일 차단 | `PreToolUse` (Write/Edit) | inline | `.env`, `.secret`, `credentials` 수정 차단 | 앤 (커스텀) |
| 5 | 파일 수정 완료 알림 | `PostToolUse` (Write/Edit) | inline | `[✅ 파일 수정 완료]` | 앤 (커스텀) |
| 6 | 자동 포매팅 | `PostToolUse` (Write/Edit) | inline | Prettier/Black/gofmt/rustfmt 자동 실행 | 앤 (커스텀) |
| 7 | Git 상태 표시 | `PostToolUse` (Write/Edit) | inline | 변경된 파일 5줄 표시 | 앤 (커스텀) |

### 6-3. Hook 관련 스크립트

| # | 파일 | 경로 | 기능 | 저자 |
|---|------|------|------|------|
| 1 | `auto-analyze.sh` | `~/.claude/hooks/` | UserPromptSubmit Hook V2.0 (분석+저장) | 앤 (커스텀) |
| 2 | `auto-memory-save.sh` | `~/.claude/hooks/` | (레거시) Stop Hook 자동 저장 - 현재 미사용 | 앤 (커스텀) |

---

## 7. MCP 서버

> Model Context Protocol 기반 도구 확장

### 7-1. 커스텀 MCP 서버

| # | 서버 | 도구 | 기능 | 저자 |
|---|------|------|------|------|
| 1 | `prompt-analyzer` | `analyze_prompt` | 4-Layer 프롬프트 분석, 스킬/에이전트/체인 추천 | 앤 (커스텀) |
| 2 | `filesystem` | 12개 도구 | 파일 읽기/쓰기/검색/디렉토리 관리 | Anthropic (공식) |
| 3 | `context7` | `resolve-library-id`, `get-library-docs` | 라이브러리 최신 문서 조회 | Upstash (서드파티) |

---

## 8. 공식 플러그인

> Anthropic 공식 마켓플레이스: `anthropics/claude-plugins-official`
> 위치: `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/`

### 8-1. 개발 워크플로우

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 1 | `commit-commands` | Git 커밋/푸시/PR 워크플로우 자동화 | Anthropic (공식) |
| 2 | `code-review` | 멀티 에이전트 PR 코드 리뷰 (신뢰도 스코어링) | Anthropic (공식) |
| 3 | `pr-review-toolkit` | PR 리뷰 전문 에이전트 (주석, 테스트, 에러, 타입, 품질, 단순화) | Anthropic (공식) |
| 4 | `feature-dev` | 코드베이스 탐색/아키텍처/품질 리뷰 포함 피처 개발 | Anthropic (공식) |
| 5 | `code-simplifier` | 코드 단순화, 명확성/일관성 리팩토링 | Anthropic (공식) |
| 6 | `security-guidance` | 보안 경고 Hook (인젝션, XSS, 안전하지 않은 패턴) | Anthropic (공식) |

### 8-2. 프로젝트 설정/관리

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 7 | `claude-code-setup` | 코드베이스 분석 → Hook/스킬/MCP/서브에이전트 자동 추천 | Anthropic (공식) |
| 8 | `claude-md-management` | CLAUDE.md 품질 감사, 세션 학습 캡처, 프로젝트 메모리 유지 | Anthropic (공식) |
| 9 | `hookify` | 대화 패턴 분석 → 자동 Hook 생성 | Anthropic (공식) |
| 10 | `plugin-dev` | 플러그인 개발 도구 | Anthropic (공식) |

### 8-3. SDK/프레임워크

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 11 | `agent-sdk-dev` | Claude Agent SDK 개발 플러그인 | Anthropic (공식) |
| 12 | `frontend-design` | 프론트엔드 UI/UX 디자인 스킬 | Anthropic (공식) |
| 13 | `playground` | 인터랙티브 HTML 플레이그라운드 생성 | Anthropic (공식) |

### 8-4. 출력 스타일

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 14 | `explanatory-output-style` | 구현 선택에 대한 교육적 인사이트 추가 | Anthropic (공식) |
| 15 | `learning-output-style` | 의사결정 포인트에서 사용자 참여 요청 | Anthropic (공식) |

### 8-5. 고급 기법

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 16 | `ralph-loop` | 반복적 자기참조 AI 루프 (Ralph Wiggum Technique) | Anthropic (공식) |
| 17 | `example-plugin` | 모든 확장 옵션을 보여주는 예시 플러그인 | Anthropic (공식) |

### 8-6. LSP (Language Server Protocol) 통합

| # | 플러그인 | 언어 | 저자 |
|---|---------|------|------|
| 18 | `typescript-lsp` | TypeScript | Anthropic (공식) |
| 19 | `pyright-lsp` | Python | Anthropic (공식) |
| 20 | `rust-analyzer-lsp` | Rust | Anthropic (공식) |
| 21 | `gopls-lsp` | Go | Anthropic (공식) |
| 22 | `clangd-lsp` | C/C++ | Anthropic (공식) |
| 23 | `jdtls-lsp` | Java | Anthropic (공식) |
| 24 | `kotlin-lsp` | Kotlin | Anthropic (공식) |
| 25 | `lua-lsp` | Lua | Anthropic (공식) |
| 26 | `php-lsp` | PHP | Anthropic (공식) |
| 27 | `csharp-lsp` | C# | Anthropic (공식) |
| 28 | `swift-lsp` | Swift | Anthropic (공식) |

---

## 9. 외부 연동 플러그인

> 서드파티 서비스 연동. 공식 마켓플레이스에 등록.
> 위치: `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/`

### 9-1. 프로젝트/이슈 관리

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 1 | `asana` | Asana 프로젝트 관리 연동 (태스크, 프로젝트, 진행 추적) | Asana (서드파티) |
| 2 | `linear` | Linear 이슈 트래커 연동 (이슈, 프로젝트, 상태 관리) | Linear (서드파티) |

### 9-2. 코드/DevOps 플랫폼

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 3 | `github` | GitHub MCP 서버 (이슈, PR, 코드 리뷰, API) | GitHub (서드파티) |
| 4 | `gitlab` | GitLab DevOps (레포, MR, CI/CD, 위키) | GitLab (서드파티) |
| 5 | `greptile` | AI 코드 리뷰 에이전트 (GitHub/GitLab PR) | Greptile (서드파티) |
| 6 | `serena` | 시맨틱 코드 분석 (LSP 기반 리팩토링/탐색) | Serena (서드파티) |

### 9-3. 백엔드/인프라

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 7 | `firebase` | Google Firebase (Firestore, Auth, Functions, Hosting) | Google (서드파티) |
| 8 | `supabase` | Supabase (DB, Auth, Storage, 실시간 구독) | Supabase (서드파티) |
| 9 | `stripe` | Stripe 결제 개발 플러그인 | Stripe (서드파티) |

### 9-4. 개발 도구

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 10 | `context7` | Upstash Context7 - 라이브러리 최신 문서 조회 | Upstash (서드파티) |
| 11 | `playwright` | Microsoft Playwright - 브라우저 자동화/E2E 테스트 | Microsoft (서드파티) |
| 12 | `laravel-boost` | Laravel 개발 툴킷 (Artisan, Eloquent, 마이그레이션) | 커뮤니티 (서드파티) |

### 9-5. 커뮤니케이션

| # | 플러그인 | 설명 | 저자 |
|---|---------|------|------|
| 13 | `slack` | Slack 워크스페이스 연동 (메시지 검색, 채널, 스레드) | Slack (서드파티) |

---

## 10. 빌트인 CLI 커맨드

> Claude Code에 내장된 시스템 명령어. 수정 불가.

| # | 커맨드 | 용도 | 저자 |
|---|--------|------|------|
| 1 | `/help` | 도움말 표시 | Anthropic (공식) |
| 2 | `/compact` | 대화 컨텍스트 압축 | Anthropic (공식) |
| 3 | `/clear` | 대화 기록 초기화 | Anthropic (공식) |
| 4 | `/context` | 컨텍스트 사용량 표시 | Anthropic (공식) |
| 5 | `/cost` | 토큰 사용량/비용 표시 | Anthropic (공식) |
| 6 | `/model` | 모델 변경 | Anthropic (공식) |
| 7 | `/permissions` | 권한 설정 | Anthropic (공식) |
| 8 | `/mcp` | MCP 서버 관리 | Anthropic (공식) |
| 9 | `/memory` | 메모리 파일 관리 | Anthropic (공식) |
| 10 | `/agents` | 서브에이전트 목록 | Anthropic (공식) |
| 11 | `/skills` | 스킬 목록 | Anthropic (공식) |
| 12 | `/tasks` | 태스크 목록 | Anthropic (공식) |

---

## 11. 커스텀 스크립트

> `~/.claude/scripts/` 위치. Hook/MCP에서 호출.

| # | 파일 | 용도 | 호출자 | 저자 |
|---|------|------|--------|------|
| 1 | `prompt_analyzer.py` | 4-Layer 프롬프트 분석기 (CLI) | auto-analyze.sh | 앤 (커스텀) |
| 2 | `prompt_analyzer_mcp.py` | 4-Layer 분석기 MCP 서버 버전 | MCP 자동 호출 | 앤 (커스텀) |
| 3 | `chain_report_generator.py` | 일일 체인/에이전트/스킬 사용 리포트 | 수동/cron | 앤 (커스텀) |

---

## 요약 통계

| 카테고리 | 공식 (Anthropic) | 서드파티 | 커스텀 (앤) | 합계 |
|---------|-----------------|---------|------------|------|
| **서브에이전트** | 3 | 0 | 24 | **27** |
| **스킬** | 16 | 0 | 3 | **19** |
| **슬래시 커맨드** | 12 (빌트인) | 0 | 13 | **25** |
| **Hook 스크립트** | 0 (기능만 제공) | 0 | 7 | **7** |
| **MCP 서버** | 1 | 1 | 1 | **3** |
| **공식 플러그인** | 28 | 0 | 0 | **28** |
| **외부 플러그인** | 0 | 13 | 0 | **13** |
| **스크립트** | 0 | 0 | 3 | **3** |
| **합계** | **60** | **14** | **51** | **125** |

---

## 참고 문서

| 문서 | 위치 |
|------|------|
| CLAUDE.md V3.8 | `~/.claude/CLAUDE.md` |
| settings.json | `~/.claude/settings.json` |
| Create custom subagents | 본 폴더 내 |
| Extend Claude with skills | 본 폴더 내 |
| Create plugins | 본 폴더 내 |
| Automate workflows with hooks | 본 폴더 내 |
| Discover and install plugins | 본 폴더 내 |

---

*Generated by Ari & An | 2026-02-06*
