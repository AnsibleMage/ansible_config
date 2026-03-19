# 009. UserPromptSubmit Hook Auto-Analysis System

> 프롬프트 입력 시 자동으로 4-Layer 분석을 실행하는 Hook 시스템

---

## 개요

MCP Prompt Analyzer (008번 문서)가 있어도 Claude가 자동으로 호출하지 않는 문제를 해결하기 위해 `UserPromptSubmit` Hook을 구현했습니다.

### 문제 배경

| 문제 | 설명 |
|------|------|
| MCP는 도구일 뿐 | Claude가 필요하다고 판단해야만 호출됨 |
| 자동 실행 불가 | CLAUDE.md의 "반드시 먼저 실행" 지시가 항상 적용되지 않음 |
| 컨텍스트 길이 | 대화가 길어지면 지시사항이 무시될 수 있음 |

### 해결책

`UserPromptSubmit` Hook을 사용하여 **모든 프롬프트 입력 시** 자동으로 분석 실행.

---

## Claude Code Hook 이벤트 (12개)

| 이벤트 | 언제 발동 | 차단 가능 | 설명 |
|--------|---------|---------|------|
| **SessionStart** | 세션 시작/재개 시 | 아니오 | 초기 컨텍스트 로딩, 환경변수 설정 |
| **UserPromptSubmit** | 사용자 프롬프트 제출 시 | **예** | 프롬프트 검증, 컨텍스트 추가, 프롬프트 차단 가능 |
| **PreToolUse** | 도구 실행 전 | **예** | 도구 호출 차단/허용, 입력값 수정 |
| **PermissionRequest** | 권한 요청 대화 시 | **예** | 권한 자동 허용/거부 |
| **PostToolUse** | 도구 성공 후 | 제한적 | 포스트 처리, 검증, Claude에 피드백 |
| **PostToolUseFailure** | 도구 실패 후 | 아니오 | 실패 로깅, Claude에 오류 컨텍스트 |
| **Notification** | 알림 발생 시 | 아니오 | 권한 요청, 유휴 상태 등 감시 |
| **SubagentStart** | 서브에이전트 생성 시 | 아니오 | 서브에이전트에 컨텍스트 주입 |
| **SubagentStop** | 서브에이전트 완료 시 | **예** | 서브에이전트 계속 실행 강제 |
| **Stop** | Claude 응답 완료 시 | **예** | Claude를 계속 실행하도록 강제 |
| **PreCompact** | 컨텍스트 압축 전 | 아니오 | 압축 전 정리 작업 |
| **SessionEnd** | 세션 종료 시 | 아니오 | 정리 작업, 세션 통계 로깅 |

---

## 실행 흐름

### Before (MCP만 있을 때)

```
사용자 프롬프트 입력
        ↓
컨텍스트 로딩 (CLAUDE.md)
        ↓
Claude LLM 처리
        ↓
"analyze_prompt 호출할까 말까?" ← 불확실
        ↓
도구 선택 및 실행
```

### After (UserPromptSubmit Hook 추가)

```
사용자 프롬프트 입력
        ↓
┌───────────────────────────────────────┐
│ UserPromptSubmit Hook (자동 실행)      │
│   ~/.claude/hooks/auto-analyze.sh     │
│   → prompt_analyzer.py 호출           │
│   → 4-Layer 분석 수행                 │
│   → additionalContext로 결과 주입     │
└───────────────────────────────────────┘
        ↓
컨텍스트 로딩 (CLAUDE.md + 분석 결과)
        ↓
Claude LLM 처리 ← 분석 결과를 보고 결정!
        ↓
적절한 스킬/에이전트 선택
```

---

## 파일 구조

```
~/.claude/
├── settings.json                    # UserPromptSubmit 훅 설정
├── hooks/
│   └── auto-analyze.sh             # 자동 분석 훅 스크립트
└── scripts/
    ├── prompt_analyzer.py          # CLI 분석기
    └── prompt_analyzer_mcp.py      # MCP 서버
```

---

## 설치 구성

### 1. 훅 스크립트 생성

**파일**: `~/.claude/hooks/auto-analyze.sh`

```bash
#!/bin/bash
# Claude Code UserPromptSubmit Hook
# 프롬프트를 자동으로 4-Layer 분석하여 컨텍스트로 주입

# stdin에서 JSON 입력 받기
INPUT=$(cat)

# 프롬프트 추출
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')

# 프롬프트가 비어있으면 종료
if [ -z "$PROMPT" ]; then
    exit 0
fi

# 짧은 프롬프트는 분석 생략 (10자 미만)
if [ ${#PROMPT} -lt 10 ]; then
    exit 0
fi

# 단순 명령어 패턴 생략 (/help, /clear 등)
if echo "$PROMPT" | grep -qE '^/[a-z-]+$'; then
    exit 0
fi

# prompt_analyzer.py 실행
ANALYZER="/Users/changjaeyou/.claude/scripts/prompt_analyzer.py"
if [ -f "$ANALYZER" ]; then
    ANALYSIS=$(python3 "$ANALYZER" "$PROMPT" 2>/dev/null)

    if [ -n "$ANALYSIS" ]; then
        # 분석 결과를 additionalContext로 주입
        jq -n \
            --arg ctx "$ANALYSIS" \
            '{
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": $ctx
                }
            }'
        exit 0
    fi
fi

exit 0
```

**실행 권한 부여**:
```bash
chmod +x ~/.claude/hooks/auto-analyze.sh
```

### 2. settings.json 설정

**파일**: `~/.claude/settings.json`

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/changjaeyou/.claude/hooks/auto-analyze.sh"
          }
        ]
      }
    ],
    "PreToolUse": [...],
    "PostToolUse": [...],
    "SessionStart": [...]
  }
}
```

---

## Hook Output 스펙

### 입력 (stdin)

```json
{
  "prompt": "사용자가 입력한 프롬프트"
}
```

### 출력 (stdout)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "분석 결과 문자열"
  }
}
```

### 생략 조건

| 조건 | 이유 |
|------|------|
| 프롬프트 10자 미만 | 분석할 내용 없음 |
| `/command` 형식 | 슬래시 명령어는 분석 불필요 |
| 분석기 파일 없음 | 오류 방지 |

---

## 테스트 결과

### 테스트 명령

```bash
echo '{"prompt": "이 코드를 한국어 버전으로 번역해줘"}' | ~/.claude/hooks/auto-analyze.sh
```

### 테스트 케이스

| 입력 | 분석 결과 |
|------|----------|
| "이 코드를 한국어 버전으로 번역해줘" | `/translation-specialist`, HIGH |
| "Rails 8로 API를 개발해줘" | `code_developer`, MEDIUM |
| "시스템 아키텍처를 설계해줘" | `system_architect`, MEDIUM |
| "/help" | (생략됨) |
| "hi" | (생략됨 - 10자 미만) |

### 실제 출력 예시

```
============================================================
🔍 4-LAYER PROMPT ANALYSIS
============================================================

📝 [1] 어휘적 분석 (Lexical)
   스킬 감지: /translation-specialist
   에이전트 감지: code_developer

📐 [2] 통사적 분석 (Syntactic)
   요청 유형: command

🎯 [3] 화용적 분석 (Pragmatic)
   감지된 의도: translation
   🔴 언어 변환 감지: ? → 한국어

============================================================
💡 RECOMMENDATION
============================================================
   📌 권장 스킬: /translation-specialist
   📌 권장 에이전트: code_developer

   우선순위: HIGH

   근거:
   - 🔴 번역 의도 감지: None → 한국어
   - 키워드 '코드' → code_developer
============================================================
```

---

## Claude Code 확인 방법

세션 시작 시 다음 메시지가 표시되면 정상 작동:

```
<system-reminder>
UserPromptSubmit hook success: Success
</system-reminder>
<system-reminder>
UserPromptSubmit hook additional context: [분석 결과]
</system-reminder>
```

---

## 트러블슈팅

### Hook이 실행되지 않을 때

```bash
# 1. 스크립트 실행 권한 확인
ls -la ~/.claude/hooks/auto-analyze.sh

# 2. jq 설치 확인
which jq

# 3. Python 분석기 확인
python3 ~/.claude/scripts/prompt_analyzer.py "테스트"

# 4. 수동 테스트
echo '{"prompt": "테스트 프롬프트"}' | ~/.claude/hooks/auto-analyze.sh
```

### 분석 결과가 표시되지 않을 때

```bash
# Claude Code 완전 재시작
exit  # 또는 Ctrl+D
claude  # 다시 시작
```

---

## 관련 문서

- [[008_MCP-Prompt-Analyzer-Server]] - MCP 분석기 서버
- [[007_Claude-Code-Settings-Configuration]] - Claude Code 설정
- [[004_Dynamic-Chain-Orchestration-System]] - 동적 체인 오케스트레이션
- [[CLAUDE.md]] - 통합 가이드라인 V3.5

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-02-03 | 1.0 | UserPromptSubmit Hook 구현 및 문서화 |

---

## 첨부 파일

- `hooks/auto-analyze.sh` - 자동 분석 훅 스크립트
