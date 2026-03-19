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
