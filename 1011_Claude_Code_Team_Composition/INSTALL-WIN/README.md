# Claude Code PM System - Windows 11 Installation Guide

> Version: 1.0 | Platform: Windows 11 Pro 64bit (AMD)
> Role: SI/SM Project Manager

---

## Overview

macOS 개발자 중심의 Claude Code V4.2.1을 **Windows 11 PM 업무**에 맞게 경량 재구축한 시스템입니다.

| 항목 | Mac/Dev (V4.2.1) | Windows/PM (V1.0) |
|------|------------------|-------------------|
| CLAUDE.md | ~394행 | ~183행 |
| Hook/Script | bash + Python 3개 | **없음** (Zero Dependency) |
| 에이전트 | 14개 | **6개** |
| 체인 | 10개 (A~J) | **5개** (A~E) |
| 스킬 | 18개 | **7개** (기존 활용) |
| 커맨드 | 13개 | **4개** |
| 외부 의존성 | Python, jq, bash | **없음** |

---

## Prerequisites (사전 요구사항)

1. **Node.js** (v18 이상)
   - https://nodejs.org/ 에서 LTS 버전 다운로드
   - 설치 후 확인: `node --version`

2. **npm** (Node.js와 함께 설치됨)
   - 확인: `npm --version`

3. **Git** (선택사항, 버전 관리 시)
   - https://git-scm.com/download/win

---

## Installation (설치)

### Step 1. Claude Code CLI 설치

PowerShell 또는 CMD를 **관리자 권한**으로 실행:

```powershell
npm install -g @anthropic-ai/claude-code
```

설치 확인:

```powershell
claude --version
```

### Step 2. Claude Code 폴더 확인

```powershell
# .claude 폴더 확인 (없으면 생성)
if (!(Test-Path "$env:USERPROFILE\.claude")) { mkdir "$env:USERPROFILE\.claude" }
if (!(Test-Path "$env:USERPROFILE\.claude\agents")) { mkdir "$env:USERPROFILE\.claude\agents" }
if (!(Test-Path "$env:USERPROFILE\.claude\commands")) { mkdir "$env:USERPROFILE\.claude\commands" }
if (!(Test-Path "$env:USERPROFILE\.claude\memory")) { mkdir "$env:USERPROFILE\.claude\memory" }
```

### Step 3. CLAUDE-PM.md 복사

```powershell
copy "INSTALL-WIN\config\CLAUDE-PM.md" "$env:USERPROFILE\.claude\CLAUDE.md"
```

> **중요**: 파일명을 `CLAUDE.md`로 변경하여 복사합니다.

### Step 4. settings.json 복사

```powershell
copy "INSTALL-WIN\config\settings.json" "$env:USERPROFILE\.claude\settings.json"
```

### Step 5. 에이전트 파일 복사

```powershell
copy "INSTALL-WIN\agents\*" "$env:USERPROFILE\.claude\agents\"
```

### Step 6. 커맨드 파일 복사

```powershell
copy "INSTALL-WIN\commands\*" "$env:USERPROFILE\.claude\commands\"
```

### Step 7. 개인정보 설정

`%USERPROFILE%\.claude\CLAUDE.md` 파일을 열어 **Section 6. Project Info**를 수정하세요:

```markdown
| 항목 | 값 |
|------|-----|
| **PM 이름** | (본인 이름) |
| **소속** | (회사/팀명) |
| **주요 프로젝트** | (프로젝트명) |
```

### Step 8. 첫 실행 테스트

```powershell
claude
```

테스트 프롬프트:
- "주간보고서 작성해줘" → DocumentChain 활성화 확인
- "벤더 비교 분석해줘" → AnalysisChain 활성화 확인
- "Q2 WBS 만들어줘" → PlanningChain 활성화 확인

---

## File Structure (파일 구조)

```
INSTALL-WIN/
├── README.md                           # 이 파일 (설치 가이드)
├── config/
│   ├── CLAUDE-PM.md                    # PM용 CLAUDE.md (~183행)
│   └── settings.json                   # PM용 설정 (Hook 없음)
├── agents/                             # PM용 에이전트 6개
│   ├── 201_Requirements_Analyst.md     # 요구사항 분석
│   ├── 202_Multidimensional_Analyst.md # 다차원 분석
│   ├── 203_Balanced_Judge.md           # 의사결정
│   ├── 204_Project_Planner.md          # 프로젝트 계획 (신설)
│   ├── 205_Stakeholder_Communicator.md # 이해관계자 소통 (신설)
│   └── 206_Document_Reviewer.md        # 문서 품질 검토 (변환)
└── commands/                           # PM용 슬래시 커맨드 4개
    ├── memory-save.md                  # 메모리 저장
    ├── project-review.md               # PM 산출물 리뷰
    ├── status-report.md                # 주간/월간 보고서 (신설)
    └── risk-matrix.md                  # 리스크 매트릭스 (신설)
```

---

## Available Chains (체인 안내)

| 체인 | 용도 | 트리거 예시 |
|------|------|-----------|
| **AnalysisChain** | 시장/기술/경쟁사 분석 | "분석해줘", "비교해줘", "조사해줘" |
| **DocumentChain** | 보고서/제안서/문서 생성 | "작성해줘", "만들어줘", "보고서" |
| **PlanningChain** | WBS/일정/리소스 계획 | "계획", "WBS", "간트차트", "로드맵" |
| **DecisionChain** | 벤더 선정/기술 결정 | "선정해줘", "결정", "비교 평가" |
| **CommunicationChain** | 경영진/고객 보고 준비 | "보고 준비", "발표 자료", "커뮤니케이션" |

---

## Available Skills (스킬 안내)

| 스킬 | 용도 |
|------|------|
| `/docx` | Word 문서 생성 |
| `/xlsx` | Excel 스프레드시트 생성 |
| `/pptx` | PowerPoint 프레젠테이션 생성 |
| `/pdf` | PDF 추출/생성 |
| `/doc-coauthoring` | 협업 문서 작성 |
| `/translation-specialist` | 번역 |
| `/internal-comms` | 내부 커뮤니케이션 |

---

## Slash Commands (커맨드 안내)

| 커맨드 | 용도 |
|--------|------|
| `/memory-save` | 현재 작업 내용을 메모리에 저장 |
| `/project-review` | PM 산출물 전체 리뷰 및 등급 평가 |
| `/status-report` | 주간/월간 프로젝트 상태 보고서 생성 |
| `/risk-matrix` | 리스크 매트릭스 생성/업데이트 |

---

## Troubleshooting (문제 해결)

### Claude Code가 설치되지 않는 경우
```powershell
# Node.js 버전 확인 (v18 이상 필요)
node --version

# npm 캐시 정리 후 재설치
npm cache clean --force
npm install -g @anthropic-ai/claude-code
```

### CLAUDE.md가 인식되지 않는 경우
- 파일 경로 확인: `%USERPROFILE%\.claude\CLAUDE.md`
- 파일 인코딩: UTF-8 (BOM 없음) 확인
- 파일명 대소문자: `CLAUDE.md` (대문자)

### 에이전트/커맨드가 인식되지 않는 경우
- 폴더 경로 확인:
  - `%USERPROFILE%\.claude\agents\` (에이전트)
  - `%USERPROFILE%\.claude\commands\` (커맨드)
- Claude Code 재시작: `claude` 종료 후 재실행

---

## Design Decisions (설계 결정)

1. **Hook 완전 제거**: Windows에서 bash/Python 의존성 없이 동작. CLAUDE.md 인라인 패턴 매칭으로 대체.
2. **에이전트 6개**: PM 주간 업무 사이클(분석→계획→실행→보고→결정)에 1:1 매핑.
3. **체인 5개**: "프로세스"가 아닌 "결과물" 기반 설계. PM이 만드는 5가지 산출물 유형에 매핑.
4. **defaultModel: sonnet**: PM은 문서 작업 중심이므로 비용 효율적인 sonnet 기본 사용. 심층 분석 시 에이전트가 opus 자동 사용.

---

*Claude Code PM System V1.0 — Windows 11 SI/SM Project Manager*
