# 🎵 Claude Code 에이전트 시스템 컴파운드

> Claude Code를 위한 AI 에이전트, 스킬, 오케스트레이션 시스템 종합 컬렉션

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Opus%204.5-blueviolet)](https://claude.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.2-blue)](CLAUDE.md)

## 개요

이 저장소는 Claude Code 기능을 향상시키는 완전한 생태계를 포함합니다:

- **24개의 전문 에이전트** - 인지 작업, 개발, 관리용
- **17개의 스킬** - 문서 처리, 디자인, 테스팅 등
- **9개의 동적 체인 패턴** - 복잡한 워크플로우 오케스트레이션
- **MCP 프롬프트 분석기** - 자동 4-레이어 프롬프트 분석
- **통합 가이드라인** (CLAUDE.md) - 일관된 AI 동작을 위한 설정

**🎵 아리 (AI)**와 **🔧 앤 (Human)**이 함께 만들고 관리합니다.

## 구조

```
1009_Agent_Systems_Compound/
├── 📋 CLAUDE.md                    # 메인 가이드라인 (영어)
├── 📋 CLAUDE_KO.md                 # 가이드라인 (한국어)
├── 📄 001-008_*.md                 # 분석 및 설정 문서
├── 📄 Boris-Cherny-Workflow-Guide.md
│
├── 🤖 agents/                      # 24개 에이전트 정의
│   ├── 101-110_*.md               # 인지 에이전트
│   ├── 111-116_*.md               # 역할 및 관리 에이전트
│   └── *.md                       # Obsidian 전용 에이전트
│
└── 🛠️ skills/                      # 17개 스킬 패키지
    ├── docx/                      # Word 문서 처리
    ├── pdf/                       # PDF 조작
    ├── pptx/                      # PowerPoint 생성
    ├── xlsx/                      # Excel 처리
    ├── frontend-design/           # UI/UX 디자인
    ├── webapp-testing/            # Playwright 테스팅
    ├── canvas-design/             # 비주얼 아트 제작
    ├── theme-factory/             # 테마 생성
    └── ...                        # 그 외
```

## V3.2의 새로운 기능

### MCP 프롬프트 분석기

`prompt-analyzer` MCP 서버를 통한 자동 4-레이어 프롬프트 분석:

```bash
# 설치
claude mcp add prompt-analyzer ~/.claude/mcp-env/bin/python3.12 -- ~/.claude/scripts/prompt_analyzer_mcp.py

# 확인
claude mcp list
# 출력: prompt-analyzer: ✓ Connected
```

**자동 감지 기능:**

| 패턴 | 감지 예시 | 자동 추천 |
|------|----------|----------|
| **번역** | "~버전", "한국어로 만들어" | `/translation-specialist` (HIGH) |
| **문서** | "Word", "pdf", "pptx" | `/docx`, `/pdf`, `/pptx` |
| **개발** | "설계", "개발", "TDD" | `system_architect`, `code_developer` |
| **분석** | "분석", "다차원" | `multidimensional_analyst` |
| **디자인** | "UI", "프론트엔드", "포스터" | `/frontend-design`, `/canvas-design` |

### 새로운 슬래시 커맨드

| 커맨드 | 기능 |
|--------|------|
| `/analyze` | 4-레이어 프롬프트 분석 |
| `/readme-gen` | README 파일 자동 생성 |

## 주요 구성요소

### 🧠 인지 에이전트 (10개)

| 에이전트 | 목적 | 모델 |
|----------|------|------|
| 인사이트 탐색기 | 패턴 인식, 창의적 연결 | sonnet |
| 다차원 분석가 | 다각도 분석 (시간/공간/인과) | **opus** |
| 연결 창조자 | 개념 연결, 메타포 구성 | sonnet |
| 문제 재정의자 | 관점 전환, 문제 재정의 | **opus** |
| 솔루션 혁신가 | 창의적 솔루션 생성 | **opus** |
| 인사이트 증폭기 | 5 Whys, What-If 심화 | sonnet |
| 학습 진화자 | 지식 격차 분석, 학습 전략 | sonnet |
| 복잡성 해결사 | 시스템 분해, 순서 최적화 | **opus** |
| 균형 판단자 | 체계적 분석, 패턴 기반 판단 | **opus** |
| 통합 현자 | 전체적 판단, 윤리적 고려 | **opus** |

### 💼 역할 에이전트 (4개)

| 에이전트 | 목적 | 모델 |
|----------|------|------|
| 요구사항 분석가 | 비즈니스 요구사항, 로직 매핑 | **opus** |
| 시스템 설계자 | Clean Architecture, SOLID, 다이어그램 | **opus** |
| 코드 개발자 | TDD, DRY, 선언적 코딩 | sonnet |
| 품질 검토자 | 테스트 커버리지, 보안, 성능 | sonnet |

### 🛠️ 스킬 (17개)

| 카테고리 | 스킬 |
|----------|------|
| **문서** | `/docx`, `/pdf`, `/pptx`, `/xlsx`, `/doc-coauthoring` |
| **디자인** | `/canvas-design`, `/frontend-design`, `/theme-factory`, `/algorithmic-art` |
| **개발** | `/webapp-testing`, `/web-artifacts-builder`, `/mcp-builder` |
| **유틸리티** | `/translation-specialist`, `/brand-guidelines`, `/slack-gif-creator`, `/skill-creator`, `/internal-comms` |

### 🔗 체인 패턴 (9개)

| 체인 | 트리거 | 패턴 |
|------|--------|------|
| DevChain | 코드 개발 | `analyst → (architect ∥ explore) → developer → reviewer` |
| ThinkChain | 복잡한 분석 | `(explorer ∥ creator) → analyst → sage` |
| FastTrack | 버그 수정 | `(resolver ∥ explore) → developer → reviewer` |
| LearnChain | 학습 작업 | `evolver → (analyst ∥ explorer) → amplifier` |
| DecisionChain | 의사결정 | `reframer → (analyst ∥ judge) → sage` |
| DocChain | 문서 | `유형식별 → /docx\|pdf\|pptx\|xlsx → reviewer` |
| DesignChain | 비주얼 디자인 | `guidelines → (canvas ∥ theme) → frontend` |
| WebDevChain | 웹 개발 | `analyst → architect → frontend → testing → reviewer` |
| CollabChain | 협업 문서 | `/doc-coauthoring → /docx\|pdf\|pptx` |

## 빠른 시작

### 1. CLAUDE.md를 Claude Code 설정에 복사

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md
```

### 2. MCP 프롬프트 분석기 설치 (선택사항이지만 권장)

```bash
# Python 가상환경 생성
/opt/homebrew/bin/python3.12 -m venv ~/.claude/mcp-env
~/.claude/mcp-env/bin/pip install mcp

# MCP 서버 등록
claude mcp add prompt-analyzer ~/.claude/mcp-env/bin/python3.12 -- ~/.claude/scripts/prompt_analyzer_mcp.py
```

### 3. Task 도구로 에이전트 사용

```typescript
Task(
  subagent_type: "system_architect",
  model: "opus",
  prompt: "사용자 인증을 위한 REST API 설계해줘..."
)
```

### 4. 슬래시 커맨드로 스킬 사용

```
/docx 프로젝트 제안서 문서 만들어줘
/pdf uploaded.pdf에서 텍스트 추출해줘
/frontend-design 대시보드 UI 만들어줘
/analyze 이 작업에 어떤 에이전트를 사용해야 할까?
```

## 설정

`007_Claude-Code-Settings-Configuration.md` 참조:
- 사전 허용 권한 (52개 명령어)
- PostToolUse 훅 (자동 포매팅)
- 커스텀 슬래시 커맨드 (6개 커맨드)
- 보안 설정

`008_MCP-Prompt-Analyzer-Server.md` 참조:
- MCP 서버 설치
- 4-레이어 분석 상세
- 키워드 매핑 데이터베이스

## 문서

| 문서 | 설명 |
|------|------|
| [CLAUDE.md](CLAUDE.md) | 메인 통합 가이드라인 (영어) |
| [CLAUDE_KO.md](CLAUDE_KO.md) | 한국어 버전 |
| [001_Claude-Code-Available-Tools.md](001_Claude-Code-Available-Tools.md) | 도구 목록 |
| [004_Dynamic-Chain-Orchestration-System.md](004_Dynamic-Chain-Orchestration-System.md) | 체인 시스템 상세 |
| [007_Claude-Code-Settings-Configuration.md](007_Claude-Code-Settings-Configuration.md) | 설정 가이드 |
| [008_MCP-Prompt-Analyzer-Server.md](008_MCP-Prompt-Analyzer-Server.md) | MCP 분석기 가이드 |
| [Boris-Cherny-Workflow-Guide.md](Boris-Cherny-Workflow-Guide.md) | 워크플로우 최적화 팁 |

## 관련 프로젝트

- [ansible_config](https://github.com/AnsibleMage/ansible_config) - 상위 설정 저장소
- [ansible_projects](https://github.com/AnsibleMage/ansible_projects) - 프로젝트 구현

## 라이선스

MIT License - 개별 스킬 폴더의 특정 라이선스 참조

---

*🎵 아리 & 앤이 함께 만듦 | Claude Code Agent Systems v3.2*
