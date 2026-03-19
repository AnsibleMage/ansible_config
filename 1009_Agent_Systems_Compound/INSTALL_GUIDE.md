# Claude Code 이식 가이드

> **용도**: 새 컴퓨터에 Claude Code 설정 이식
> **기준**: V3.4 (2026-02-01)

---

## 1. 이식할 폴더/파일 목록

### 필수 (Core)

| 항목 | 소스 위치 | 대상 위치 | 설명 |
|------|----------|----------|------|
| **CLAUDE.md** | `./CLAUDE.md` | `~/.claude/CLAUDE.md` | 가이드라인 (영어) |
| **settings.json** | `./settings.json` | `~/.claude/settings.json` | 권한, 훅 설정 |
| **commands/** | `./commands/` | `~/.claude/commands/` | 슬래시 커맨드 (6개) |

### 권장 (Recommended)

| 항목 | 소스 위치 | 대상 위치 | 설명 |
|------|----------|----------|------|
| **scripts/** | `./scripts/` | `~/.claude/scripts/` | 프롬프트 분석기 |
| **templates/** | `./templates/` | `~/.claude/templates/` | Rails 8 템플릿 |
| **skills/** | `./skills/` | `~/.claude/skills/` | 커스텀 스킬 |

### 선택 (Optional)

| 항목 | 대상 위치 | 설명 |
|------|----------|------|
| **~/.memory/** | `~/.memory/` | 세션 메모리 (빈 폴더로 시작) |
| **~/.reviews/** | `~/.reviews/` | 프로젝트 리뷰 (빈 폴더로 시작) |

---

## 2. 설치 스크립트

### 자동 설치 (권장)

```bash
# 1. 이 폴더를 새 컴퓨터로 복사 후 해당 폴더에서 실행

# 2. ~/.claude 폴더 생성
mkdir -p ~/.claude

# 3. 필수 파일 복사
cp CLAUDE.md ~/.claude/
cp settings.json ~/.claude/

# 4. 폴더 복사
cp -r commands ~/.claude/
cp -r scripts ~/.claude/
cp -r templates ~/.claude/
cp -r skills ~/.claude/

# 5. 선택 폴더 생성
mkdir -p ~/.memory
mkdir -p ~/.reviews

# 6. 스크립트 실행 권한
chmod +x ~/.claude/scripts/*.py

echo "✅ Claude Code 설정 이식 완료!"
```

### 원라인 설치

```bash
mkdir -p ~/.claude ~/.memory ~/.reviews && cp CLAUDE.md settings.json ~/.claude/ && cp -r commands scripts templates skills ~/.claude/ && chmod +x ~/.claude/scripts/*.py && echo "✅ 완료!"
```

---

## 3. 설치 후 확인

### 3.1 구조 확인

```bash
ls -la ~/.claude/
```

예상 출력:
```
CLAUDE.md
settings.json
commands/
scripts/
templates/
skills/
```

### 3.2 필수 파일 존재 확인

```bash
# CLAUDE.md 버전 확인
head -5 ~/.claude/CLAUDE.md

# settings.json 권한 확인
cat ~/.claude/settings.json | head -10

# commands 폴더 확인
ls ~/.claude/commands/
```

---

## 4. MCP 서버 설정 (선택)

### prompt-analyzer 서버

`~/.claude.json` 또는 프로젝트별 `.claude.json`에 추가:

```json
{
  "mcpServers": {
    "prompt-analyzer": {
      "command": "python3",
      "args": ["~/.claude/scripts/prompt_analyzer_mcp.py"]
    }
  }
}
```

---

## 5. 이식 파일 상세

### commands/ (6개)

| 파일 | 기능 |
|------|------|
| `commit-push.md` | Git 커밋 + 푸시 |
| `pr-review.md` | PR 변경사항 리뷰 |
| `project-review.md` | 프로젝트 전체 평가 |
| `memory-save.md` | 작업 내용 메모리 저장 |
| `readme-gen.md` | README 자동 생성 |
| `analyze.md` | 프롬프트 4-Layer 분석 |

### scripts/ (2개)

| 파일 | 기능 |
|------|------|
| `prompt_analyzer.py` | 프롬프트 분석 라이브러리 |
| `prompt_analyzer_mcp.py` | MCP 서버 버전 |

### templates/rails8/ (5개)

| 파일 | 기능 |
|------|------|
| `PRD_Template.md` | 요구사항 문서 |
| `TaskPlan_Template.md` | 작업계획서 |
| `DeployChecklist_Template.md` | 배포 체크리스트 |
| `Gemfile_Template` | 권장 Gemfile |
| `deploy_yml_Template.yml` | Kamal 설정 |

---

## 6. 트러블슈팅

### 권한 오류

```bash
chmod 644 ~/.claude/settings.json
chmod 644 ~/.claude/CLAUDE.md
chmod -R 755 ~/.claude/commands/
chmod +x ~/.claude/scripts/*.py
```

### MCP 서버 연결 실패

```bash
# Python 경로 확인
which python3

# 스크립트 직접 실행 테스트
python3 ~/.claude/scripts/prompt_analyzer_mcp.py
```

### settings.json 미적용

Claude Code 재시작 필요:
```bash
# 터미널 종료 후 재시작
exit
# 새 터미널에서 Claude Code 실행
```

---

## 7. 참고 문서

| 문서 | 설명 |
|------|------|
| `README.md` | 전체 시스템 개요 |
| `CLAUDE.md` | 가이드라인 (영어) |
| `CLAUDE_KO.md` | 가이드라인 (한국어) |
| `007_Claude-Code-Settings-Configuration.md` | settings.json 상세 |
| `008_MCP-Prompt-Analyzer-Server.md` | MCP 서버 상세 |

---

*Claude Code Migration Guide V3.4*
