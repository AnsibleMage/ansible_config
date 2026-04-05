---
title: "Tip #7 훅 자동화 — 구현 가이드"
version: "1.0.0"
created: "2026-04-05"
updated: "2026-04-05"
tags: [claude-code, hook, prettier, black, debug-residue, boris-tip7]
status: completed
type: design
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: Mac에서 Boris Tip #7 구현 완료 → Windows 재현 가이드 작성

### 다음 작업 (TODO)
- [ ] Windows 회사컴에서 이 가이드를 따라 동일하게 적용
- [ ] rubocop 설치 (Rails 환경 구성 후)
- [ ] 적용 후 디버그 잔재 검출 테스트

### 작업 조언
> [!tip] 다음 Claude Code에게
> - Boris Tip #7의 3종 Hook을 적용한 가이드 문서
> - PreToolUse는 deny 목록으로 이미 충분 → 추가 작업 없음
> - PostToolUse는 포매터 설치만 필요 (코드는 이미 존재)
> - Stop 잔재 검출만 신규 스크립트 생성

---

# Tip #7 훅 자동화 — 구현 가이드

## 개요

Boris의 3종 Hook을 앤의 V5.1.0 시스템에 적용한 내역. 기존 시스템과의 충돌 분석 후, 최소 변경으로 구현.

| Boris Hook | 구현 방식 | 작업량 |
|-----------|----------|--------|
| PreToolUse 위험 차단 | **이미 충분** (deny 목록 17개) | 없음 |
| PostToolUse 자동 포맷 | **포매터 설치** (prettier, black) | 설치만 |
| Stop 디버그 잔재 검출 | **신규 스크립트** + settings.json | 소규모 |

---

## Part A: PostToolUse — 포매터 설치

### 설치 명령

```bash
npm install -g prettier          # JS/TS/CSS/HTML
pip3 install black               # Python
```

> rubocop(Ruby)은 시스템 Ruby 2.6 권한 문제로 보류. Rails 환경(rbenv/asdf) 구성 후 설치.

### 검증

```bash
prettier --version   # → 3.8.1
black --version      # → 25.11.0
```

### 작동 원리

기존 PostToolUse Hook 코드(`settings.json`)가 `command -v prettier`로 자동 감지. 설치만 하면 Write/Edit 시 자동 포매팅 활성화.

---

## Part B: Stop — 디버그 잔재 검출

### B-1. 스크립트 생성

파일: `~/.claude/hooks/debug-residue-check.sh`

```bash
#!/bin/bash
# debug-residue-check.sh — Stop Hook: 디버그 잔재 검출
# Boris Tip #7: "실수를 시스템으로 원천 차단"
# V1.0 (2026-04-05)

INPUT=$(cat)

# Teammate 스킵
if [ "$CLAUDE_CODE_AGENT_TEAM_ROLE" = "teammate" ]; then
    exit 0
fi

# git이 없거나 git 저장소가 아니면 스킵
if ! command -v git &> /dev/null || [ ! -d .git ]; then
    exit 0
fi

# 변경된 파일 목록 수집 (unstaged + staged)
CHANGED_FILES=$(git diff --name-only 2>/dev/null)
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null)
ALL_FILES=$(echo -e "${CHANGED_FILES}\n${STAGED_FILES}" | sort -u | grep -v '^$')

if [ -z "$ALL_FILES" ]; then
    exit 0
fi

# 디버그 잔재 패턴 검색
RESIDUES=""
while IFS= read -r file; do
    [ -f "$file" ] || continue

    # 바이너리/설정 파일 제외
    case "$file" in
        *.md|*.json|*.yml|*.yaml|*.toml|*.lock|*.log) continue ;;
    esac

    MATCHES=$(grep -nE \
        'console\.log\(|debugger;|binding\.pry|byebug|require.*pry|puts.*debug|print\(.*debug|# ?TODO:? ?remove|# ?FIXME|# ?XXX' \
        "$file" 2>/dev/null)

    if [ -n "$MATCHES" ]; then
        MATCHES_SHORT=$(echo "$MATCHES" | head -5)
        COUNT=$(echo "$MATCHES" | wc -l | tr -d ' ')
        RESIDUES="${RESIDUES}
📄 ${file} (${COUNT}건):
${MATCHES_SHORT}"
        if [ "$COUNT" -gt 5 ]; then
            RESIDUES="${RESIDUES}
  ... +$((COUNT - 5))건 더"
        fi
        RESIDUES="${RESIDUES}
"
    fi
done <<< "$ALL_FILES"

# 결과 출력
if [ -n "$RESIDUES" ]; then
    WARNING_MSG="
⚠️ [디버그 잔재 검출] 커밋 전 확인 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${RESIDUES}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> 위 항목들이 의도적인지 확인하세요.
"
    jq -n --arg ctx "$WARNING_MSG" '{
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": $ctx
        }
    }'
fi

exit 0
```

### B-2. 실행 권한 설정

```bash
chmod +x ~/.claude/hooks/debug-residue-check.sh
```

### B-3. settings.json 수정

`Stop` 배열에 새 그룹 추가 (기존 stop-cleanup.sh 아래):

```json
"Stop": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "/Users/changjaeyou/.claude/hooks/stop-cleanup.sh"
      }
    ]
  },
  {
    "hooks": [
      {
        "type": "command",
        "command": "/Users/changjaeyou/.claude/hooks/debug-residue-check.sh"
      }
    ]
  }
]
```

> Windows에서는 경로를 `%USERPROFILE%\.claude\hooks\debug-residue-check.sh`로 변경

---

## Part C: 추가 — 교정 감지 Hook (L1 기록 강제)

이 세션에서 발견된 문제: 앤이 교정해도 L1 실수 기록이 자동으로 안 됨.

`auto-analyze.sh`에 교정 키워드 감지 블록 추가 완료:

```bash
# auto-analyze.sh 내부 (4-Layer 분석 직전에 삽입)
if echo "$PROMPT" | grep -qE '아니|그거 말고|다시|실수|잘못|안 돼|하지 마|틀렸|고쳐|수정해|왜 이렇게|이상해|아닌데|그게 아니라|다르게|제대로'; then
    CORRECTION_INSTRUCTION="⚠️ [L1 기록 의무] 앤의 교정/거부 감지됨 → L1+L2 기록 먼저!"
fi
```

---

## 실행 순서 요약 (Windows에서)

```
[Step 1] prettier 설치: npm install -g prettier
[Step 2] black 설치: pip install black
[Step 3] debug-residue-check.sh 생성 + chmod +x
[Step 4] settings.json Stop 배열에 새 그룹 추가
[Step 5] auto-analyze.sh에 교정 감지 블록 추가 (Part C)
[Step 6] 검증 (prettier --version, black --version, 스크립트 문법, JSON 유효성)
```

---

## 관련 문서

### 직접 참조 (Direct Links)
- `1013_Claude_Code_Harness/01_claude_code_7_best_practices.md` — 원본 7가지 팁
- `1013_Claude_Code_Harness/02_tip2_tip5_implementation_guide.md` — Tip #2+#5 가이드
- `~/.claude/hooks/debug-residue-check.sh` — Stop 잔재 검출 스크립트
- `~/.claude/hooks/auto-analyze.sh` — 교정 감지 추가된 분석 Hook
- `~/.claude/settings.json` — Hook 설정

### 역참조 (Backlinks)
- (없음)

### 관련 주제 (Topic Links)
- `~/.claude/rules/lessons-learned.md` — L1 실수 캐시 (이 세션에서 2건 기록)

---

## Release Notes

### v1.0.0 (2026-04-05)
- 초기 작성: Boris Tip #7 훅 자동화 3종 구현 + 교정 감지 Hook 추가
> **프롬프트:** "7번 훅 자동화를 진행해야하는데... 계획모드로 전체 계획하고 진행해줘. 완료 후 검증해줘"
