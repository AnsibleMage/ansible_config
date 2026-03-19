#!/bin/bash
# gate1_checker.sh — research.md completeness verifier
# Usage: bash gate1_checker.sh <path-to-research.md>
# Exit 0 = PASS, Exit 1 = BLOCKED

FILE="$1"
PASS=true
ERRORS=()

# File exists
if [ ! -f "$FILE" ]; then
    echo "FAIL: File not found: $FILE"
    exit 1
fi

# Required sections check (lenient: multiple keyword variants)
check_section() {
    local label="$1"
    shift
    for keyword in "$@"; do
        if grep -qi "$keyword" "$FILE"; then
            return 0
        fi
    done
    ERRORS+=("FAIL: '$label' section missing")
    PASS=false
    return 1
}

check_section "코드베이스 분석" "코드베이스 분석" "관련 파일" "파일 목록" "기존 코드"
check_section "리스크" "리스크" "제약" "위험" "Risk"
check_section "핵심 발견" "핵심 발견" "발견 요약" "결론" "Finding"

# File table exists (pipe-delimited table with file/role columns)
if ! grep -qE "\|.*파일.*\|.*역할.*\|" "$FILE" && ! grep -qE "\|.*File.*\|.*Role.*\|" "$FILE"; then
    ERRORS+=("WARN: File list table not found (Section 2.1)")
fi

# At least one numbered finding
FINDINGS=$(grep -cE "^[0-9]+\." "$FILE" 2>/dev/null)
FINDINGS=${FINDINGS:-0}
if [ "$FINDINGS" -lt 1 ]; then
    ERRORS+=("FAIL: No numbered findings (Section 5)")
    PASS=false
fi

# Output
echo "=== Gate 1: research.md Completeness Check ==="
if [ "$PASS" = true ]; then
    echo "PASS: Gate 1 verified — research.md is complete"
    if [ ${#ERRORS[@]} -gt 0 ]; then
        echo "--- Warnings ---"
        for err in "${ERRORS[@]}"; do echo "  $err"; done
    fi
    exit 0
else
    echo "BLOCKED: research.md incomplete"
    for err in "${ERRORS[@]}"; do echo "  $err"; done
    exit 1
fi
