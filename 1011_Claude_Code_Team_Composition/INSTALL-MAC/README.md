# Claude Code Orchestration System V4.2.1 — macOS Installation Guide

> **Version**: 4.2.1 | **Platform**: macOS (Apple Silicon / Intel)
> **Features**: 14 Custom Agents, 10 Dynamic Chain Patterns, 4-Layer Prompt Analyzer, Agent Teams

---

## Overview

이 시스템은 Claude Code CLI를 위한 통합 오케스트레이션 프레임워크입니다.

### 주요 기능

| 기능 | 설명 |
|------|------|
| **14 Custom Agents** | 인지(10) + 역할(4) 에이전트, Opus/Sonnet 모델 분배 |
| **10 Dynamic Chains (A~J)** | 작업 유형별 에이전트 파이프라인 자동 구성 |
| **4-Layer Prompt Analysis** | Lexical→Syntactic→Discourse→Pragmatic 자동 분석 |
| **Agent Teams** | 병렬 작업을 위한 팀 기반 협업 시스템 |
| **Memory System** | YYMM_SEQ_keyword.md 형식의 자동 메모리 관리 |
| **Hook Pipeline** | UserPromptSubmit → auto-analyze.sh → prompt_analyzer.py |
| **Auto Formatting** | PostToolUse Hook으로 Prettier/Black/gofmt/rustfmt/StyLua 자동 적용 |
| **Rails 8 Vibe Coding** | 7개 슬래시 커맨드로 Rails 8 풀 사이클 자동화 |

---

## Prerequisites

- **macOS** 12.0+ (Monterey 이상)
- **Node.js** 18+ (`brew install node`)
- **Python 3.10+** (`brew install python@3.12`)
- **jq** (`brew install jq`)
- **bc** (macOS 기본 포함)
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)

### Optional (자동 포매팅용)

```bash
# JavaScript/TypeScript
npm install -g prettier

# Python
pip3 install black

# Go (Homebrew)
brew install go

# Rust
rustup component add rustfmt

# Ruby
gem install rubocop

# Lua/Luau
cargo install stylua
```

---

## Installation

### Step 1: Claude Code 설치

```bash
npm install -g @anthropic-ai/claude-code
```

### Step 2: 기본 디렉토리 확인

```bash
# Claude Code가 자동 생성하는 디렉토리
ls ~/.claude/
# 없으면 claude를 한 번 실행하여 생성
claude --help
```

### Step 3: 시스템 파일 복사

```bash
# 이 저장소를 클론한 위치에서 실행
INSTALL_DIR="$(pwd)/INSTALL-MAC"

# config 파일 복사
cp "$INSTALL_DIR/config/CLAUDE.md" ~/.claude/CLAUDE.md
cp "$INSTALL_DIR/config/settings.json" ~/.claude/settings.json
cp "$INSTALL_DIR/config/CHANGELOG.md" ~/.claude/CHANGELOG.md
cp "$INSTALL_DIR/config/RAILS.md" ~/.claude/RAILS.md

# settings.local.json (선택사항 — MCP 퍼미션)
cp "$INSTALL_DIR/config/settings.local.json" ~/.claude/settings.local.json

# agents 복사
mkdir -p ~/.claude/agents
cp "$INSTALL_DIR/agents/"*.md ~/.claude/agents/

# commands 복사
mkdir -p ~/.claude/commands
cp "$INSTALL_DIR/commands/"*.md ~/.claude/commands/

# hooks 복사
mkdir -p ~/.claude/hooks
cp "$INSTALL_DIR/hooks/auto-analyze.sh" ~/.claude/hooks/
chmod +x ~/.claude/hooks/auto-analyze.sh

# scripts 복사
mkdir -p ~/.claude/scripts
cp "$INSTALL_DIR/scripts/"*.py ~/.claude/scripts/

# statusline 복사
cp "$INSTALL_DIR/statusline.sh" ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh

# templates 복사
mkdir -p ~/.claude/templates/rails8
cp "$INSTALL_DIR/templates/rails8/"* ~/.claude/templates/rails8/

# memory 디렉토리 생성
mkdir -p ~/.claude/memory
```

### Step 4: MCP 서버 설정 (선택사항)

```bash
# Python 가상환경 생성
python3 -m venv ~/.claude/mcp-env
~/.claude/mcp-env/bin/pip install mcp

# MCP 서버 등록
claude mcp add prompt-analyzer python ~/.claude/scripts/prompt_analyzer_mcp.py
```

### Step 5: 개인화

`~/.claude/CLAUDE.md`를 열고 다음 플레이스홀더를 교체하세요:

| 플레이스홀더 | 설명 | 예시 |
|------------|------|------|
| `[YOUR_AI_NICKNAME]` | AI 파트너 닉네임 | 아리, Ari |
| `[YOUR_AI_NAME]` | AI 파트너 이름 | Aria |
| `[YOUR_NICKNAME]` | 사용자 닉네임 | 앤, An |
| `[YOUR_NAME]` | 사용자 이름 | Ansible |
| `[YOUR_REPO_1]` | 리포지토리 이름 | my-project |
| `[YOUR_LOCAL_PATH]` | 로컬 경로 | /Users/me/projects/my-project |
| `[YOUR_REMOTE_URL]` | 원격 URL | github.com/me/my-project |

### Step 6: 첫 실행 테스트

```bash
claude
# 세션 시작 후 테스트:
# "시스템 상태 확인해줘" → SystemDesignChain 활성화 확인
# "간단한 질문이야: 파이썬 버전 알려줘" → Simple Task (체인 생략) 확인
```

---

## File Structure

```
INSTALL-MAC/
├── README.md                          # 이 파일
├── statusline.sh                      # StatusLine 커스텀 표시 (2줄)
├── config/
│   ├── CLAUDE.md                      # 메인 오케스트레이션 가이드라인 (~394행)
│   ├── CHANGELOG.md                   # 버전 이력 (V2.0 ~ V4.2.1)
│   ├── RAILS.md                       # Rails 8 개발 시스템
│   ├── settings.json                  # 메인 설정 (Hook, 퍼미션, Model)
│   └── settings.local.json            # 추가 퍼미션 (MCP 등)
├── hooks/
│   └── auto-analyze.sh                # UserPromptSubmit Hook V3.0
├── scripts/
│   ├── prompt_analyzer.py             # 4-Layer 프롬프트 분석기 V4.0 (999행)
│   ├── prompt_analyzer_mcp.py         # MCP 서버 V4.1 (741행)
│   └── chain_report_generator.py      # 일일 체인 사용 리포트 (477행)
├── agents/                            # 14 Custom Agents
│   ├── 101_Insight_Explorer.md        # [S] 패턴 발견, 관찰
│   ├── 102_Multidimensional_Analyst.md # [O] 다차원 분석
│   ├── 103_Connection_Creator.md      # [O] 연결, 은유
│   ├── 104_Problem_Reframer.md        # [O] 관점 전환
│   ├── 105_Solution_Innovator.md      # [O] 혁신적 솔루션
│   ├── 106_Insight_Amplifier.md       # [O] Why/What-If 심화
│   ├── 107_Learning_Evolver.md        # [O] 학습, 메타인지
│   ├── 108_Complexity_Resolver.md     # [O] 복잡성 분해
│   ├── 109_Balanced_Judge.md          # [O] 의사결정, 판단
│   ├── 110_Integrated_Sage.md         # [O] 통합 지혜
│   ├── 111_Requirements_Analyst.md    # [O] 요구사항 분석
│   ├── 112_System_Architect.md        # [O] 아키텍처 설계
│   ├── 113_Code_Developer.md          # [S] TDD 개발
│   └── 114_Quality_Reviewer.md        # [S] 코드 리뷰
├── commands/                          # 13 Slash Commands
│   ├── analyze.md                     # /analyze — 4-Layer 분석
│   ├── commit-push.md                 # /commit-push — Git 워크플로우
│   ├── memory-save.md                 # /memory-save — 메모리 저장
│   ├── pr-review.md                   # /pr-review — PR 리뷰
│   ├── project-review.md             # /project-review — 프로젝트 리뷰
│   ├── readme-gen.md                  # /readme-gen — README 생성
│   ├── rails-init.md                  # /rails-init — Rails 8 초기화
│   ├── rails-prd.md                   # /rails-prd — PRD 생성
│   ├── rails-plan.md                  # /rails-plan — 작업계획서
│   ├── rails-dev.md                   # /rails-dev — TDD 개발
│   ├── rails-test.md                  # /rails-test — 테스트 실행
│   ├── rails-deploy.md               # /rails-deploy — Kamal 2 배포
│   └── rails-verify.md               # /rails-verify — 프로덕션 검증
└── templates/rails8/                  # Rails 8 템플릿
    ├── PRD_Template.md                # 요구사항 문서 템플릿
    ├── TaskPlan_Template.md           # 작업계획서 템플릿
    ├── Gemfile_Template               # 권장 Gemfile
    ├── deploy_yml_Template.yml        # Kamal 2 설정
    └── DeployChecklist_Template.md    # 배포 체크리스트
```

---

## Dynamic Chain Patterns (A~J)

| Chain | 용도 | 주요 에이전트 |
|-------|------|-------------|
| A. SystemDesignChain | 시스템/아키텍처 설계 | system_architect, solution_innovator, integrated_sage |
| B. AutomationChain | Hook/MCP/스크립트 자동화 | requirements_analyst, code_developer |
| C. GameDevChain | Roblox + Web 게임 개발 | 듀얼 트랙 병렬 |
| D. DevChain | 일반 소프트웨어 개발 | requirements→architect→developer |
| E. ResearchChain | 기술 연구/조사 | multidimensional_analyst, insight_amplifier |
| F. DocChain+ | 문서 생성 (Solo/Collab) | requirements_analyst, quality_reviewer |
| G. WebDevChain+ | 웹 개발 (디자인 통합) | 디자인→프론트→테스트 |
| H. MetaThinkChain | 심층 사고/의사결정 | solution_innovator, insight_amplifier, integrated_sage |
| I. RailsDevChain | Rails 8 풀 사이클 | 7개 슬래시 커맨드 체인 |
| J. HotfixChain | 긴급 버그 수정 | complexity_resolver, code_developer |

---

## Troubleshooting

### Hook이 동작하지 않을 때

```bash
# auto-analyze.sh 실행 권한 확인
chmod +x ~/.claude/hooks/auto-analyze.sh

# jq 설치 확인
which jq || brew install jq

# Python3 확인
python3 --version

# 수동 테스트
echo '{"prompt":"시스템 설계 해줘","sessionId":"test"}' | bash ~/.claude/hooks/auto-analyze.sh
```

### MCP 서버가 인식되지 않을 때

```bash
# MCP 서버 목록 확인
claude mcp list

# 재등록
claude mcp remove prompt-analyzer
claude mcp add prompt-analyzer python ~/.claude/scripts/prompt_analyzer_mcp.py
```

### StatusLine이 표시되지 않을 때

```bash
# 실행 권한 확인
chmod +x ~/.claude/statusline.sh

# 수동 테스트
echo '{"model":{"display_name":"opus"},"cost":{"total_cost_usd":0.5}}' | bash ~/.claude/statusline.sh
```

---

## License

MIT License

---

*Claude Code Orchestration System V4.2.1 — Built with Claude Code*
