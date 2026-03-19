# Installation Guide
## User Prompt Chain Hook System 설치 가이드

---

## 목차

1. [요구 사항](#1-요구-사항)
2. [자동 설치](#2-자동-설치)
3. [수동 설치](#3-수동-설치)
4. [설정 확인](#4-설정-확인)
5. [문제 해결](#5-문제-해결)
6. [업그레이드](#6-업그레이드)
7. [제거](#7-제거)

---

## 1. 요구 사항

### 필수 소프트웨어

| 소프트웨어 | 최소 버전 | 확인 명령어 |
|-----------|----------|------------|
| macOS | 12.0+ | `sw_vers` |
| Python | 3.8+ | `python3 --version` |
| Claude Code | Latest | `claude --version` |
| jq | 1.6+ | `jq --version` |

### jq 설치 (없는 경우)

```bash
# Homebrew로 설치
brew install jq

# 또는 MacPorts
sudo port install jq
```

### Python 확인

```bash
# Python 3 확인
python3 --version

# 없으면 Homebrew로 설치
brew install python3
```

---

## 2. 자동 설치

### Step 1: 설치 스크립트 실행

```bash
# 패키지 폴더로 이동
cd "/path/to/User Prompt Chain Hook System"

# 실행 권한 부여
chmod +x install.sh

# 설치 실행
./install.sh
```

### Step 2: 설치 확인

```bash
# 파일 확인
ls -la ~/.claude/hooks/
ls -la ~/.claude/scripts/

# 설정 확인
cat ~/.claude/settings.json | jq '.hooks.UserPromptSubmit'
```

### Step 3: Claude Code 재시작

```bash
# 터미널에서 새 세션 시작
claude
```

---

## 3. 수동 설치

### Step 1: 디렉토리 생성

```bash
# Claude 설정 디렉토리 생성
mkdir -p ~/.claude/hooks
mkdir -p ~/.claude/scripts
```

### Step 2: 파일 복사

```bash
# Hook 스크립트 복사
cp hooks/auto-analyze.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/auto-analyze.sh

# 분석기 스크립트 복사
cp scripts/prompt_analyzer.py ~/.claude/scripts/
cp scripts/prompt_analyzer_mcp.py ~/.claude/scripts/
chmod +x ~/.claude/scripts/prompt_analyzer.py
```

### Step 3: settings.json 설정

기존 settings.json이 있는 경우:

```bash
# 백업
cp ~/.claude/settings.json ~/.claude/settings.json.backup

# 편집
code ~/.claude/settings.json  # 또는 vim, nano 등
```

settings.json에 다음 섹션 추가:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/YOUR_USERNAME/.claude/hooks/auto-analyze.sh"
          }
        ]
      }
    ]
  }
}
```

> ⚠️ **중요**: `YOUR_USERNAME`을 실제 사용자명으로 변경하세요.
> 확인: `whoami` 또는 `echo $HOME`

기존 settings.json이 없는 경우:

```bash
# 템플릿 복사
cp templates/settings.json.template ~/.claude/settings.json

# 사용자명 치환
sed -i '' "s/YOUR_USERNAME/$(whoami)/g" ~/.claude/settings.json
```

### Step 4: 경로 수정

auto-analyze.sh 파일 내 경로 수정:

```bash
# 현재 사용자 경로로 수정
sed -i '' "s|/Users/changjaeyou|$HOME|g" ~/.claude/hooks/auto-analyze.sh
```

---

## 4. 설정 확인

### 4.1 Hook 테스트

```bash
# auto-analyze.sh 직접 테스트
echo '{"prompt": "테스트 프롬프트입니다"}' | ~/.claude/hooks/auto-analyze.sh
```

예상 출력:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "============================================================\n🔍 4-LAYER PROMPT ANALYSIS\n..."
  }
}
```

### 4.2 분석기 테스트

```bash
# prompt_analyzer.py 직접 테스트
echo "React로 투두리스트 만들어줘" | python3 ~/.claude/scripts/prompt_analyzer.py
```

### 4.3 settings.json 검증

```bash
# JSON 문법 검증
python3 -m json.tool ~/.claude/settings.json

# 또는 jq로 검증
jq '.' ~/.claude/settings.json
```

### 4.4 Claude Code에서 확인

Claude Code 시작 후 아무 프롬프트나 입력하면:

```
============================================================
🔍 4-LAYER PROMPT ANALYSIS
============================================================
...
```

이 메시지가 컨텍스트로 주입되면 성공입니다.

---

## 5. 문제 해결

### 5.1 Hook이 실행되지 않음

**증상**: 프롬프트 입력 시 분석 결과가 표시되지 않음

**해결 방법**:

1. settings.json 확인:
```bash
cat ~/.claude/settings.json | jq '.hooks.UserPromptSubmit'
```

2. Hook 스크립트 권한 확인:
```bash
ls -la ~/.claude/hooks/auto-analyze.sh
# -rwxr-xr-x 여야 함
chmod +x ~/.claude/hooks/auto-analyze.sh
```

3. jq 설치 확인:
```bash
which jq
# 없으면: brew install jq
```

### 5.2 Python 오류

**증상**: `python3: command not found`

**해결 방법**:

```bash
# Python 설치 확인
which python3

# 없으면 설치
brew install python3

# 또는 경로 지정 (auto-analyze.sh 수정)
# python3 → /usr/local/bin/python3
```

### 5.3 경로 오류

**증상**: `ANALYZER="/Users/changjaeyou/..." not found`

**해결 방법**:

```bash
# auto-analyze.sh 열기
code ~/.claude/hooks/auto-analyze.sh

# 27번 줄 수정
ANALYZER="$HOME/.claude/scripts/prompt_analyzer.py"
```

### 5.4 JSON 파싱 오류

**증상**: `jq: parse error`

**해결 방법**:

```bash
# settings.json 문법 검사
python3 -m json.tool ~/.claude/settings.json

# 오류 발생 시 백업 복원
cp ~/.claude/settings.json.backup ~/.claude/settings.json
```

### 5.5 짧은 프롬프트 생략

**증상**: 10자 미만 프롬프트에서 분석이 안 됨

**설명**: 의도된 동작입니다. 짧은 프롬프트는 분석 효율을 위해 생략됩니다.

수정하려면 auto-analyze.sh 17번 줄:
```bash
if [ ${#PROMPT} -lt 10 ]; then  # 10을 원하는 값으로 변경
```

---

## 6. 업그레이드

### 새 버전으로 업그레이드

```bash
# 1. 기존 파일 백업
cp ~/.claude/hooks/auto-analyze.sh ~/.claude/hooks/auto-analyze.sh.bak
cp ~/.claude/scripts/prompt_analyzer.py ~/.claude/scripts/prompt_analyzer.py.bak

# 2. 새 파일 복사
cp hooks/auto-analyze.sh ~/.claude/hooks/
cp scripts/prompt_analyzer.py ~/.claude/scripts/

# 3. 권한 재설정
chmod +x ~/.claude/hooks/auto-analyze.sh
chmod +x ~/.claude/scripts/prompt_analyzer.py

# 4. 경로 수정 (필요시)
sed -i '' "s|/Users/changjaeyou|$HOME|g" ~/.claude/hooks/auto-analyze.sh
```

---

## 7. 제거

### 완전 제거

```bash
# Hook 제거
rm ~/.claude/hooks/auto-analyze.sh

# 스크립트 제거
rm ~/.claude/scripts/prompt_analyzer.py
rm ~/.claude/scripts/prompt_analyzer_mcp.py

# settings.json에서 Hook 설정 제거
# "UserPromptSubmit" 섹션 삭제
```

### settings.json 수정

```json
{
  "hooks": {
    // "UserPromptSubmit" 섹션 삭제
    "PreToolUse": [...],
    "PostToolUse": [...]
  }
}
```

---

## 추가 설정 (선택)

### MCP 서버로 사용

Hook 대신 MCP 서버로 분석기를 사용할 수도 있습니다:

```bash
# MCP 서버 등록
claude mcp add prompt-analyzer python ~/.claude/scripts/prompt_analyzer_mcp.py
```

### 전체 settings.json 예시

`templates/settings.json.template` 파일을 참조하세요.

---

## 지원

문제가 있으면 GitHub Issues에 등록하거나 직접 문의하세요.

---

*Installation Guide v1.0 - 2026-02-04*
