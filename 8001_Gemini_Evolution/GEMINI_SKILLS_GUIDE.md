# Gemini Antigravity 스킬(Skills) 시스템 구현 가이드

이 문서는 Claude Code의 [Agent Skills](https://code.claude.com/docs/ko/skills) 개념을 분석하고, 이를 Gemini Antigravity 환경에 맞게 이식하는 방법을 설명합니다.

## 1. 스킬(Skills)의 개념

**Skills**는 에이전트가 특정 작업을 수행하기 위해 필요한 **"지식(Instructions) + 도구(Scripts) + 예제(Examples)"**의 묶음입니다.
서브에이전트(Sub-agent)가 "전문가 페르소나"라면, 스킬은 그 전문가가 사용하는 "장비와 매뉴얼"입니다.

### Claude Code vs Gemini Antigravity

| 구분 | Claude Code | Gemini Antigravity (제안) |
| :--- | :--- | :--- |
| **정의** | `SKILL.md` (YAML frontmatter + Markdown) | `~/.gemini/antigravity/skills/<name>/SKILL.md` |
| **구성** | 매뉴얼, 스크립트(`scripts/`), 템플릿 | 매뉴얼, 실행 스크립트(`scripts/`), 참조 문서 |
| **제한** | `allowed-tools`로 도구 제한 가능 | 프롬프트 지시를 통해 도구 사용 범위 제한 |
| **사용** | 자연어 호출 시 자동/수동 로드 | 워크플로우를 통해 로드하거나, 작업 시작 시 참조 |

---

## 2. 디렉토리 구조 (Directory Structure)

프로젝트별 로컬 폴더 대신 **전역 설정 폴더**(`~/.gemini/antigravity/skills/`)를 사용하여 관리합니다.

```text
~/.gemini/antigravity/
├── personas/           # (이미 구현됨) 에이전트 페르소나
├── workflows/          # (이미 구현됨) 워크플로우
└── skills/             # [NEW] 스킬 디렉토리
    ├── git-commit/     # 스킬 1: Git 커밋 도우미
    │   └── SKILL.md
    ├── pdf-processing/ # 스킬 2: PDF 처리 (복합 스킬)
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   └── extract_text.py
    │   └── templates/
    └── ...
```

---

## 3. SKILL.md 표준 포맷

Claude Code의 포맷을 그대로 차용하되, Antigravity가 이해하기 쉽도록 섹션을 구성합니다.

```markdown
---
name: [스킬 이름, 예: git-commit-helper]
description: [언제 이 스킬을 사용해야 하는지 설명]
tools: [필요한 도구 목록, 예: run_command, git]
---

# [스킬 이름]

## Instructions (지침)
이 스킬을 사용할 때 따라야 할 단계별 지침입니다.
1. ...
2. ...

## Scripts (스크립트)
이 스킬에서 사용할 수 있는 유틸리티 스크립트입니다.
- `python ~/.gemini/antigravity/skills/<name>/scripts/helper.py`: [용도 설명]

## Examples (예제)
사용 예시:
> User: "..."
> Agent: "..."
```

---

## 4. 구현 예시 (Examples)

### 예시 1: Git Commit Helper (단일 파일)
**경로**: `~/.gemini/antigravity/skills/git-commit/SKILL.md`

```markdown
---
name: git-commit-helper
description: Git 변경사항을 분석하여 Conventional Commits 규격에 맞는 메시지를 작성하고 커밋합니다.
---

# Git Commit Helper

## Instructions
1. `git diff --staged` 명령어로 변경사항을 확인합니다.
2. 변경사항이 없다면 사용자에게 파일을 stage 하라고 안내합니다.
3. 변경 내용을 요약하여 Conventional Commits (`feat:`, `fix:`, `docs:` 등) 형식의 메시지를 제안합니다.
4. 사용자가 동의하면 `git commit -m "..."`을 실행합니다.

## Rules
- 메시지는 영어 또는 한글(사용자 선호에 따름)로 작성합니다.
- 본문은 72자를 넘지 않도록 줄바꿈합니다.
```

### 예시 2: Data Analysis (스크립트 포함)
**경로**: `~/.gemini/antigravity/skills/data-analysis/SKILL.md`

```markdown
---
name: data-analysis
description: CSV/Excel 데이터를 분석하고 시각화합니다.
---

# Data Analysis Skill

## Instructions
1. `scripts/analyze.py`를 사용하여 데이터 요약 통계를 산출합니다.
2. 주요 컬럼의 분포를 확인합니다.

## Scripts
- `~/.gemini/antigravity/skills/data-analysis/scripts/analyze.py [file_path]`: pandas를 사용해 데이터를 분석하고 요약본을 출력합니다.
```

---

## 5. 활성화 방법 (Activation)

스킬을 사용하는 방법은 **"명시적 로드"** 워크플로우를 사용하는 것입니다.

**워크플로우**: `~/.gemini/antigravity/workflows/use_skill.md` (신규 생성 필요)
1. 사용자가 스킬 이름을 입력 (예: `/use_skill git-commit`).
2. 에이전트가 `~/.gemini/antigravity/skills/git-commit/SKILL.md`를 읽음.
3. 해당 지침을 숙지하고 작업 수행.

## 6. 다음 단계 제안

1. `.agent/skills` 디렉토리 생성
2. `.agent/workflows/use_skill.md` 워크플로우 생성
3. 시범 스킬 구현: `git-commit-helper` (바로 쓸 수 있어 유용함)

이 가이드를 바탕으로 **스킬 시스템 구조**를 잡고, 첫 번째 스킬로 **Git Commit Helper**를 만들어볼까요?
