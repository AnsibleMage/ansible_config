# ansible_config

Claude Code 설정 온톨로지 -- 에이전트, 스킬, 체인, 훅, 메모리 시스템, 오케스트레이션 패턴을 12단계 반복 설계 과정에 걸쳐 발전시킨 기록입니다.

## 개요

이 레포지토리는 Claude Code 오케스트레이션 시스템의 전체 진화 과정을 문서화합니다. 기본적인 에이전트 정의에서 시작하여, 벡터 메모리, 4계층 프롬프트 분석, 동적 체인 오케스트레이션을 갖춘 복합 AI 시스템으로 발전했습니다. 각 최상위 디렉토리는 독립된 설계 단계를 나타내며, 현재 시스템을 형성한 리서치, 의사결정, 산출물을 보존합니다.

현재 운영 중인 설정은 `~/.claude/`에 위치하며, 재현성과 협업을 위해 이 레포지토리에 백업/버전 관리됩니다.

## 주요 기능

- **20개 이상의 전문 에이전트** -- 인지 에이전트(인사이트, 분석, 관점 전환), 역할 에이전트(아키텍트, 개발자, 리뷰어), 평가 에이전트(채점, 비교, 보안 리뷰)
- **27개 스킬** -- 문서 처리(docx/pdf/pptx/xlsx), 디자인(캔버스, 테마, 브랜드), 웹 개발(프론트엔드, 테스트, 아티팩트), Rails 8 바이브코딩, 번역 등
- **10개 동적 체인 패턴** (A-J) -- SystemDesignChain, DevChain, ResearchChain, MetaThinkChain, HotfixChain, WebDevChain+, GameDevChain, DocChain+, RailsDevChain, AutomationChain
- **4계층 프롬프트 분석기** -- Lexical, Syntactic, Discourse, Pragmatic 분석 + 오탐 방지 + 신뢰도 점수
- **벡터 메모리 시스템** -- Qdrant 기반 의미적 메모리, 자동 인덱싱, 청크 벡터화, 코사인 유사도 리콜
- **훅 시스템** -- UserPromptSubmit 자동 분석, PostToolUse 포매팅, PreToolUse 보안 검사, 메모리 자동 인덱싱
- **에이전트 팀즈** -- Lead/Teammate 아키텍처 기반 병렬 실행, 복원력 프로토콜, 하이브리드 체인 통합

## 프로젝트 구조

```
ansible_config/
|
|-- 1001_Agent_Systems_Basic/          # 1단계: 기본 에이전트 정의 (35개 에이전트)
|   |-- agents/                        #   시스템, 개발, 도메인, 프로덕트 에이전트
|   +-- CLAUDE.md                      #   메타 에이전트 오케스트레이션 가이드라인
|
|-- 1002_Agent_Systems_Engine/         # 2단계: 엔진 레벨 에이전트 시스템
|   |-- agents/                        #   개선된 에이전트 정의
|   +-- CLAUDE.md                      #   향상된 오케스트레이션 규칙
|
|-- 1003_Agent_Systems_Thinking/       # 3단계: 사고 지향 에이전트
|   |-- agents/                        #   인지 에이전트 중심
|   +-- CLAUDE_THINK.md                #   사고 프로세스 가이드라인
|
|-- 1004_Skill_Agent_Systems_*/        # 4단계: 스킬 시스템 도입
|   |-- global_skills/                 #   최초 스킬 정의
|   +-- memory/                        #   초기 메모리 시스템
|
|-- 1005-1008_Skill_Agent_Systems_*/   # 5-8단계: 스킬 반복 개선
|                                      #   Gemini 통합, 크로스 플랫폼 마이그레이션
|
|-- 1009_Agent_Systems_Compound/       # 9단계: 복합 AI 시스템 (353 파일)
|   |-- agents/                        #   24개 에이전트 (인지 + 역할 + 관리)
|   |-- skills/                        #   17개 스킬 패키지
|   |-- commands/                      #   13개 슬래시 커맨드
|   |-- hooks/                         #   자동 분석 & 메모리 훅
|   |-- scripts/                       #   prompt_analyzer.py (4계층)
|   |-- templates/                     #   Rails 8 템플릿
|   +-- CLAUDE.md                      #   V3.6 통합 가이드라인
|
|-- 1010_Claude_Code_System_Evolution/ # 10단계: 시스템 진화 리서치
|   +-- 001-009_*.md                   #   체인 업그레이드, 메모리 솔루션, 마스터플랜
|
|-- 1011_Claude_Code_Team_Composition/ # 11단계: 에이전트 팀즈 통합
|   |-- doc/                           #   팀 분석 & 테스트 보고서
|   |-- INSTALL-MAC/                   #   macOS 설치 설정
|   |-- INSTALL-WIN/                   #   Windows 설치 설정
|   +-- CLAUDE.md                      #   V4.2.1 팀즈 복원력 포함
|
+-- 1012_Claude_Code_Ontology_System_/ # 12단계: 온톨로지 & 모듈화 (1202 파일)
    |-- 101_doc_current_system_analysis/   # 현재 시스템 분석
    |-- 102_doc_future_system_research/    # 미래 시스템 연구
    |-- 103_doc_/                          # 개선 기획 (C1-C8)
    |-- 104_current_system/                # V4.2.1 시스템 백업
    +-- 105_claude_code_system_package/    # V5.1 프로덕션 패키지
        |-- agents/        # 20개 에이전트 (14 코어 + 6 평가)
        |-- skills/        # 27개 스킬 (커맨드 + 스킬 통합)
        |-- hooks/         # 프로덕션 훅 스크립트
        |-- scripts/       # 프롬프트 분석기, 메모리 인덱서
        |-- rules/         # 모듈화된 규칙 (오케스트레이션 + 메모리)
        |-- eval/          # 평가 프레임워크
        +-- workflow/      # research -> plan -> implement 템플릿
```

## 기술 스택

| 구성요소 | 기술 |
|---------|------|
| AI 플랫폼 | Claude Code (Opus 모델) |
| 벡터 DB | Qdrant (Docker, localhost:6333) |
| 임베딩 모델 | `intfloat/multilingual-e5-large` (1024차원) |
| 런타임 | Python 3.11+ (venv) |
| 훅 시스템 | Bash + Python (UserPromptSubmit, PostToolUse, PreToolUse) |
| MCP 서버 | prompt-analyzer (4계층 분석) |
| 문서 처리 | python-docx, reportlab, python-pptx, openpyxl |
| 배포 | Kamal 2 (Rails 8 프로젝트) |
| 버전 관리 | Git + GitHub |

## 설치 방법

이 레포지토리는 설정 아카이브입니다. 실제 시스템을 배포하려면 다음을 참고하세요:

```bash
# 레포지토리 클론
git clone https://github.com/AnsibleMage/ansible_config.git

# 프로덕션 패키지 위치:
# 1012_Claude_Code_Ontology_System_/105_claude_code_system_package/

# ~/.claude/ (Claude Code 활성 설정 디렉토리)로 복사
cp -r 1012_Claude_Code_Ontology_System_/105_claude_code_system_package/* ~/.claude/

# Python 의존성 설치 (프롬프트 분석기 & 메모리 시스템용)
cd ~/.claude && python3 -m venv mcp-env
source mcp-env/bin/activate
pip install qdrant-client sentence-transformers

# Qdrant 시작 (Docker 필요)
docker run -d -p 6333:6333 qdrant/qdrant

# MCP 프롬프트 분석기 등록
claude mcp add prompt-analyzer ~/.claude/mcp-env/bin/python3.12 -- ~/.claude/scripts/prompt_analyzer_mcp.py
```

상세 설치 가이드:
- `1009_Agent_Systems_Compound/INSTALL_GUIDE.md`
- `1012_Claude_Code_Ontology_System_/105_claude_code_system_package/INSTALL_GUIDE.md`

## 버전 히스토리

| 버전 | 단계 | 주요 변경사항 |
|------|------|-------------|
| V1.0 | 1001 | 기본 35개 에이전트 시스템 + 메타 오케스트레이션 |
| V2.0 | 1002-1003 | 엔진 레벨 에이전트, 사고 프로세스 통합 |
| V3.0 | 1004-1008 | 스킬 시스템, Gemini 통합, 크로스 플랫폼 지원 |
| V3.6 | 1009 | 복합 시스템 -- 24 에이전트, 17 스킬, 11 체인, MCP 분석기 |
| V4.2.1 | 1010-1011 | 시스템 진화, 에이전트 팀즈 + 복원력 프로토콜 |
| V5.1.0 | 1012 | 온톨로지 시스템, CLAUDE.md 모듈화, 평가 프레임워크 |

## 라이선스

[MIT](LICENSE)
