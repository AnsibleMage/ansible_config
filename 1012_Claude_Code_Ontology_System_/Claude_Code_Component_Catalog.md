# Claude Code Component Catalog

> Claude Code에서 사용되는 모든 구성 요소를 분류하고 정리한 종합 카탈로그
> 작성일: 2026-02-06 | **최종 업데이트: 2026-03-17** | 기준 버전: **V5.0.0**

---

## 목차

1. [시스템 개요](#1-시스템-개요)
2. [빌트인 서브에이전트](#2-빌트인-서브에이전트)
3. [커스텀 서브에이전트](#3-커스텀-서브에이전트)
4. [스킬 (Skills)](#4-스킬)
5. [체인 (Chains)](#5-체인)
6. [슬래시 커맨드](#6-슬래시-커맨드)
7. [Hook 시스템](#7-hook-시스템)
8. [스크립트 (Scripts)](#8-스크립트)
9. [MCP 서버](#9-mcp-서버)
10. [워크플로우 & 평가](#10-워크플로우--평가)
11. [플러그인](#11-플러그인)
12. [빌트인 CLI 커맨드](#12-빌트인-cli-커맨드)
13. [인프라 & 디렉토리](#13-인프라--디렉토리)
14. [요약 통계](#14-요약-통계)

---

## 1. 시스템 개요

| 항목 | 값 |
|------|-----|
| CLAUDE.md 버전 | **V5.0.0** (115줄) |
| rules/ | 2파일 (orchestration.md 289줄 + memory-protocol.md 43줄) |
| Hook 활성화 | **8/12** (67%) |
| Phase 진행률 | Phase 0~2 완료, **Phase 3: 5/12** |
| Python | 3.11.12 (venv) |
| Agent Teams | 활성화 (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) |
| Default Model | opus |

---

## 2. 빌트인 서브에이전트

> Anthropic 공식 제공. Claude Code에 기본 내장.

| # | 서브에이전트 | 기본 모델 | 용도 |
|---|------------|----------|------|
| 1 | `Explore` | **Opus** | 코드베이스 탐색, 파일 검색 (읽기 전용) |
| 2 | `Plan` | **Opus** | Plan 모드에서 코드베이스 리서치 (읽기 전용) |
| 3 | `general-purpose` | **Opus** | 범용 멀티스텝 작업 처리 |

---

## 3. 커스텀 서브에이전트

> `~/.claude/agents/` 위치. 총 **20개 활성** + 8개 아카이브.

### 3-1. Primary Agents (101~114) — 14개

| # | 에이전트 | `subagent_type` | 모델 | maxTurns | isolation |
|---|---------|-----------------|------|----------|-----------|
| 101 | Insight Explorer | `insight_explorer` | **opus** | 15 | — |
| 102 | Multidimensional Analyst | `multidimensional_analyst` | **opus** | 20 | — |
| 103 | Connection Creator | `connection_creator` | **opus** | 15 | — |
| 104 | Problem Reframer | `problem_reframer` | **opus** | 15 | — |
| 105 | Solution Innovator | `solution_innovator` | **opus** | 20 | — |
| 106 | Insight Amplifier | `insight_amplifier` | **opus** | 20 | — |
| 107 | Learning Evolver | `learning_evolver` | **opus** | 15 | — |
| 108 | Complexity Resolver | `complexity_resolver` | **opus** | 15 | — |
| 109 | Balanced Judge | `balanced_judge` | **opus** | 15 | — |
| 110 | Integrated Sage | `integrated_sage` | **opus** | 20 | — |
| 111 | Requirements Analyst | `requirements_analyst` | **opus** | 20 | — |
| 112 | System Architect | `system_architect` | **opus** | 25 | worktree |
| 113 | Code Developer | `code_developer` | **opus** | **30** | worktree |
| 114 | Quality Reviewer | `quality_reviewer` | **opus** | 20 | worktree |

### 3-2. Eval/Review Agents — 6개 (Phase 3 신규)

| 에이전트 | 모델 | 용도 | Phase |
|---------|------|------|-------|
| `grader` | **opus** | eval_test.json 기반 채점 | A3 |
| `comparator` | opus | 블라인드 버전 비교 (회귀 감지) | A3 |
| `eval-analyzer` | opus | 실패 근본 원인 분석 + 수정 제안 | A3 |
| `logic-reviewer` | **opus** | 논리적 정합성 전문 리뷰 | B1 |
| `security-reviewer` | **opus** | OWASP Top 10 보안 취약점 리뷰 | B1 |
| `edge-case-reviewer` | **opus** | 엣지케이스/경계값 전문 리뷰 | B1 |

### 3-3. Archived Agents — 8개

> `~/.claude/agents/archive/` — 비활성, 필요 시 복원.

doc-indexer, knowledge-mapper, link-doctor, meeting-note-wizard, memory-report-generator, project-dashboard, session-memo-writer, worklog-analyzer

---

## 4. 스킬 (Skills)

> `~/.claude/skills/` 위치. 총 **27개 디렉토리** (26개 SKILL.md 보유).

### 4-1. 공식 스킬 — 17개 (anthropics/skills)

| # | 스킬 | 호출 | 용도 | 업데이트 |
|---|------|------|------|---------|
| 1 | algorithmic-art | `/algorithmic-art` | p5.js 제너레이티브 아트 | — |
| 2 | brand-guidelines | `/brand-guidelines` | Anthropic 브랜드 스타일 | — |
| 3 | canvas-design | `/canvas-design` | PNG/PDF 비주얼 아트 | — |
| 4 | **claude-api** | `/claude-api` | Claude API/SDK 개발 | **2026-03-17 신규** |
| 5 | doc-coauthoring | `/doc-coauthoring` | 문서 공동 작성 워크플로우 | — |
| 6 | docx | `/docx` | Word 문서 생성/편집 | **2026-03-17 업그레이드** |
| 7 | frontend-design | `/frontend-design` | 프로덕션급 프론트엔드 UI | — |
| 8 | internal-comms | `/internal-comms` | 사내 커뮤니케이션 문서 | — |
| 9 | mcp-builder | `/mcp-builder` | MCP 서버 생성 가이드 | — |
| 10 | pdf | `/pdf` | PDF 추출/생성/병합 | **2026-03-17 업그레이드** |
| 11 | pptx | `/pptx` | PowerPoint 생성/편집 | **2026-03-17 업그레이드** |
| 12 | skill-creator | `/skill-creator` | 스킬 생성/평가/벤치마크 | **2026-03-17 업그레이드** |
| 13 | slack-gif-creator | `/slack-gif-creator` | Slack 최적화 GIF 생성 | — |
| 14 | theme-factory | `/theme-factory` | 아티팩트 테마 스타일링 | — |
| 15 | web-artifacts-builder | `/web-artifacts-builder` | React + shadcn/ui 아티팩트 | — |
| 16 | webapp-testing | `/webapp-testing` | Playwright E2E 테스트 | — |
| 17 | xlsx | `/xlsx` | Excel 생성/편집/수식 | **2026-03-17 업그레이드** |

### 4-2. 커스텀 스킬 — 10개

| # | 스킬 | 호출 | 용도 |
|---|------|------|------|
| 1 | analyze | `/analyze` | 4-Layer 프롬프트 분석 |
| 2 | claude-strategy | `/claude-strategy` | Claude Code 사용전략 문서 생성 |
| 3 | commit-push | `/commit-push` | Git 커밋+푸시 자동화 |
| 4 | memory-save | `/memory-save` | 세션 작업 메모리 저장 |
| 5 | pr-review | `/pr-review` | PR diff 리뷰 |
| 6 | project-review | `/project-review` | 프로젝트 전체 아키텍처 평가 |
| 7 | readme-gen | `/readme-gen` | README.md 자동 생성 (영어+한국어) |
| 8 | translation-specialist | `/translation-specialist` | 4-Layer 언어학적 전문 번역 |
| 9 | vibe-dev | `/vibe-dev` | 문서 기반 AI 페어 프로그래밍 |
| 10 | chains/ | (비호출) | 체인 스킬 파일 디렉토리 |

---

## 5. 체인 (Chains)

> `~/.claude/skills/chains/` 위치. 체인 패턴을 스킬 파일로 정의.
> 전체 10개 체인(A~J)은 `rules/orchestration.md` §2.4에 정의. 스킬 파일은 2개 구현.

| 체인 | 스킬 파일 | Effort | research/plan | 인간 게이트 |
|------|----------|--------|---------------|-----------|
| **A. SystemDesignChain** | `system-design.md` ✅ | HIGH | 필수 | 필수 |
| B. AutomationChain | 미구현 | MEDIUM | — | — |
| C. GameDevChain | 미구현 | MEDIUM | — | — |
| **D. DevChain** | `dev-chain.md` ✅ | MEDIUM | 중규모+ | 조건부/필수 |
| E. ResearchChain | 미구현 | HIGH | 내재적 | — |
| F. DocChain+ | 미구현 | MEDIUM | — | — |
| G. WebDevChain+ | 미구현 | MEDIUM | — | — |
| H. MetaThinkChain | 미구현 | HIGH | — | — |
| I. RailsDevChain | 미구현 | MEDIUM | rails-prd/plan | — |
| J. HotfixChain | 미구현 | LOW | — | — |

---

## 6. 슬래시 커맨드

> `~/.claude/commands/` 위치. 13개 (skills/와 공존 — C-5 규칙).

### 6-1. 일반 커맨드 — 6개

| # | 커맨드 | 용도 | skills/ 대응 |
|---|--------|------|-------------|
| 1 | `/commit-push` | Git 커밋+푸시 | ✅ |
| 2 | `/pr-review` | PR 리뷰 | ✅ |
| 3 | `/project-review` | 프로젝트 평가 | ✅ |
| 4 | `/memory-save` | 메모리 저장 | ✅ |
| 5 | `/readme-gen` | README 생성 | ✅ |
| 6 | `/analyze` | 프롬프트 분석 | ✅ |

### 6-2. Rails 8 커맨드 — 7개

| # | 커맨드 | 용도 |
|---|--------|------|
| 7 | `/rails-init` | Rails 8 프로젝트 초기화 |
| 8 | `/rails-prd` | PRD 자동 생성 |
| 9 | `/rails-plan` | 작업계획서 생성 |
| 10 | `/rails-dev` | TDD 기반 개발 |
| 11 | `/rails-test` | 테스트+품질 검증 |
| 12 | `/rails-deploy` | Kamal 2 배포 |
| 13 | `/rails-verify` | 프로덕션 검증 |

---

## 7. Hook 시스템

> `settings.json`에 등록. **8/12 활성** (67%).

### 7-1. 활성 Hook — 8개

| # | 이벤트 | 스크립트 | 기능 | Phase |
|---|--------|---------|------|-------|
| 1 | UserPromptSubmit | `auto-analyze.sh` | 4-Layer 분석 + 메모리 리콜 + 이전 프롬프트 저장 지시 | 0 |
| 2 | PreToolUse (Write/Edit) | inline | 보안 파일(.env, .secret, credentials) 수정 차단 | 0 |
| 3 | PostToolUse (Write/Edit) | inline | 자동 포매팅(Prettier/Black/gofmt/rustfmt) + Git 상태 | 0 |
| 4 | PostToolUse (*) | `observability-logger.sh` | 모든 도구 호출 1줄 로그 기록 | 0 |
| 5 | SessionStart | `session-start.sh` | 메모리 3개 자동 로드 + 리콜 서버 시작 | 0+2 |
| 6 | Stop | `stop-cleanup.sh` | 체인 미완료 방지(exit 2) + 80%+ 컨텍스트 정리 | 0 |
| 7 | InstructionsLoaded | `instructions-loaded.sh` | 규칙 파일 로딩 감사 로그 | 1 |
| 8 | TeammateIdle | `teammate-idle.sh` | 120s→재활성화, 300s→종료 허용 | 1 |
| 9 | PostCompact | `post-compact-restore.sh` | 컨텍스트 압축 후 핵심 정보 복원 | 2 |

### 7-2. 미활성 Hook — 4개

| 이벤트 | 상태 | 예상 Phase |
|--------|------|-----------|
| PreToolUse (prompt) | ❌ | Phase 4 |
| PostToolUse (agent) | ❌ | Phase 4 |
| Notification | ❌ | 미정 |
| SubagentSpawn | ❌ | 미정 |

---

## 8. 스크립트 (Scripts)

> `~/.claude/scripts/` 위치. 총 **13개** (9 Python + 4 Bash).

### 8-1. Python 스크립트 — 9개

| # | 파일 | 크기 | 용도 | Phase |
|---|------|------|------|-------|
| 1 | `prompt_analyzer.py` | 41KB | 4-Layer 분석기 (CLI, V4.0) | 0 |
| 2 | `prompt_analyzer_mcp.py` | 29KB | 분석기 MCP 서버 버전 | 0 |
| 3 | `memory_embedder.py` | 7KB | 텍스트→1024차원 벡터 (multilingual-e5-large) | 2 |
| 4 | `memory_indexer.py` | 8KB | Qdrant 벡터 인덱싱 파이프라인 | 2 |
| 5 | `memory_mcp.py` | 8KB | Qdrant 벡터 검색 MCP (5개 도구) | 2 |
| 6 | `memory_recall_server.py` | 5KB | 상주 HTTP 리콜 서버 (0.3초 응답) | 2 |
| 7 | `memory_recall.py` | 2KB | Hook용 리콜 클라이언트 (3초 타임아웃) | 2 |
| 8 | `log_analyzer.py` | 18KB | C5 Observability 월간 로그 분석 | 2 |
| 9 | `chain_report_generator.py` | 16KB | 체인/에이전트/스킬 사용 패턴 리포트 | 2 |

### 8-2. Bash 스크립트 — 4개

| # | 파일 | 용도 | Phase |
|---|------|------|-------|
| 1 | `log_rotate.sh` | 로그 로테이션 (90일/180일/무제한) | 2 |
| 2 | `gate1_checker.sh` | research.md 완성도 검증 (Gate 1) | 3-A1 |
| 3 | `gate2_checker.sh` | plan.md 승인 상태 검증 (Gate 2) | 3-A2 |
| 4 | `gate3_checker.sh` | 코드 리뷰 품질 게이트 (Gate 3) | 3-B2 |

---

## 9. MCP 서버

> `settings.json` mcpServers에 등록.

| # | 서버 | 도구 수 | 기능 | 상태 |
|---|------|--------|------|------|
| 1 | `prompt-analyzer` | 1 | analyze_prompt (4-Layer) | ✅ 활성 |
| 2 | `memory-ontology` | 5 | Qdrant 벡터 검색 (memory_mcp.py) | ✅ 활성 |
| 3 | `filesystem` | 12 | 파일 CRUD + 디렉토리 관리 | ✅ 활성 |
| 4 | `context7` | 2 | 라이브러리 최신 문서 조회 (Upstash) | ✅ 활성 |
| 5 | `pencil` | 15+ | .pen 파일 디자인 편집기 | ✅ 활성 |

---

## 10. 워크플로우 & 평가

> Phase 3 A1~A3에서 구축.

### 10-1. 워크플로우 (`~/.claude/workflow/`)

| 디렉토리 | 내용 |
|---------|------|
| `templates/research_template.md` | Research 5섹션 템플릿 |
| `templates/plan_template.md` | Plan 6섹션 템플릿 (Status: draft/approved/rejected) |
| `instances/` | 작업별 인스턴스 저장소 (현재 비어 있음) |

### 10-2. 평가 시스템 (`~/.claude/eval/`)

| 파일 | 내용 |
|------|------|
| `eval_test.json` | 25개 테스트 케이스 (보안 10, 논리 6, 엣지 7, 오탐방지 2) |
| `benchmark.json` | 버전별 통과율 히스토리 (초기 구조) |

### 10-3. 리뷰 규칙 (`~/.claude/REVIEW.md`)

| 심각도 | 동작 |
|--------|------|
| Critical | 병합 차단 (필수 수정) |
| Warning | 경고 (3건+ 시 앤 판단) |
| Info | 참고 (자동 통과) |

---

## 11. 플러그인

> `~/.claude/plugins/marketplaces/claude-plugins-official/`

### 11-1. 공식 플러그인 — 28개

**개발 워크플로우** (6): commit-commands, code-review, pr-review-toolkit, feature-dev, code-simplifier, security-guidance

**프로젝트 관리** (4): claude-code-setup, claude-md-management, hookify, plugin-dev

**SDK/프레임워크** (3): agent-sdk-dev, frontend-design, playground

**출력 스타일** (2): explanatory-output-style, learning-output-style

**고급 기법** (2): ralph-loop, example-plugin

**LSP 통합** (11): typescript, pyright, rust-analyzer, gopls, clangd, jdtls, kotlin, lua, php, csharp, swift

### 11-2. 외부 플러그인 — 13개

**프로젝트 관리** (2): asana, linear
**코드/DevOps** (4): github, gitlab, greptile, serena
**백엔드/인프라** (3): firebase, supabase, stripe
**개발 도구** (3): context7, playwright, laravel-boost
**커뮤니케이션** (1): slack

---

## 12. 빌트인 CLI 커맨드

> Claude Code 내장 시스템 명령어. 수정 불가.

| # | 커맨드 | 용도 |
|---|--------|------|
| 1 | `/help` | 도움말 |
| 2 | `/compact` | 컨텍스트 압축 |
| 3 | `/clear` | 대화 초기화 |
| 4 | `/context` | 컨텍스트 사용량 |
| 5 | `/cost` | 토큰/비용 표시 |
| 6 | `/model` | 모델 변경 |
| 7 | `/permissions` | 권한 설정 |
| 8 | `/mcp` | MCP 서버 관리 |
| 9 | `/memory` | 메모리 관리 |
| 10 | `/agents` | 에이전트 목록 |
| 11 | `/skills` | 스킬 목록 |
| 12 | `/tasks` | 태스크 관리 |

---

## 13. 인프라 & 디렉토리

### 13-1. 핵심 설정 파일

| 파일 | 줄 수 | 용도 |
|------|-------|------|
| `CLAUDE.md` | 115 | 핵심 가이드라인 V5.0.0 |
| `CHANGELOG.md` | 152 | V4.2 이전 변경 이력 |
| `RAILS.md` | 92 | Rails 8 개발 방법론 |
| `REVIEW.md` | 23 | 글로벌 리뷰 규칙 (Critical/Warning/Info) |
| `settings.json` | 185 | Hook/권한/MCP/환경변수 설정 |
| `settings.local.json` | 133 | 로컬 오버라이드 |
| `statusline.sh` | 126 | 셸 상태줄 포매터 |

### 13-2. 데이터 디렉토리

| 디렉토리 | 파일 수 | 용도 |
|---------|--------|------|
| `memory/` | 122 | 세션 메모리 (YYMM_SEQ_keyword.md) |
| `plans/` | 26 | 플랜 모드 문서 |
| `logs/` | 3+1 | 일간 로그 + 월간 리포트 |
| `eval/` | 2 | 평가 테스트 + 벤치마크 |
| `templates/rails8/` | 5 | Rails 8 프로젝트 템플릿 |

### 13-3. 시스템 디렉토리

| 디렉토리 | 용도 |
|---------|------|
| `venv/` | Python 3.11.12 가상환경 |
| `qdrant_data/` | Qdrant 벡터 DB 스토리지 |
| `teams/` | Agent Teams 메타데이터 |
| `plugins/` | 공식/외부 플러그인 |
| `projects/` | 프로젝트별 메타데이터 (12개) |
| `sessions/` | 세션 메타데이터 |

---

## 14. 요약 통계

| 카테고리 | 공식 | 서드파티 | 커스텀 (앤) | 합계 |
|---------|------|---------|------------|------|
| **서브에이전트** | 3 | 0 | 20 (+8 아카이브) | **31** |
| **스킬** | 17 | 0 | 10 | **27** |
| **체인 (스킬파일)** | 0 | 0 | 2 | **2** |
| **슬래시 커맨드** | 12 (빌트인) | 0 | 13 | **25** |
| **Hook (활성)** | 0 (기능만) | 0 | 8 | **8** |
| **스크립트** | 0 | 0 | 13 | **13** |
| **MCP 서버** | 1 | 2 | 2 | **5** |
| **공식 플러그인** | 28 | 0 | 0 | **28** |
| **외부 플러그인** | 0 | 13 | 0 | **13** |
| **합계** | **61** | **15** | **68** | **152** |

### Phase별 구축 이력

| Phase | 기간 | 핵심 산출물 |
|-------|------|-----------|
| **Phase 0** | 2026-03-15 | V5.0.0, rules/ 분리, Hook 5개, Effort Level |
| **Phase 1** | 2026-03-15 | 에이전트 14개 업그레이드, skills/ 6개, Hook 7개, 체인 프로토타입 |
| **Phase 2** | 2026-03-16 | Qdrant 벡터 메모리, MCP 리콜, Observability, Hook 8개 |
| **Phase 3** | 2026-03-17 | 워크플로우 템플릿, 게이트 스크립트 3개, 리뷰어 3종, 평가 에이전트 3종 |

---

## 참고 문서

| 문서 | 위치 |
|------|------|
| CLAUDE.md V5.0.0 | `~/.claude/CLAUDE.md` |
| Orchestration Rules | `~/.claude/rules/orchestration.md` |
| Memory Protocol | `~/.claude/rules/memory-protocol.md` |
| Settings | `~/.claude/settings.json` |
| Phase 3 Implementation | `1012_/103_doc_/04_004_Phase3_Implementation.md` |

---

*Updated by Ari | 2026-03-17 | V5.0.0 기준 전면 업데이트*
