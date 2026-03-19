#!/bin/bash
# gate2_checker.sh — plan.md approval gate verifier
# Usage: bash gate2_checker.sh <path-to-plan.md>
# Exit 0 = APPROVED (proceed), Exit 1 = BLOCKED (wait for approval)

FILE="$1"
PASS=true
ERRORS=()

# File exists
if [ ! -f "$FILE" ]; then
    echo "FAIL: File not found: $FILE"
    exit 1
fi

# Check Status field
STATUS=$(grep -iE "^\s*>\s*\*\*Status\*\*:" "$FILE" | head -1 | sed 's/.*Status\*\*:\s*//' | tr -d '[:space:]')

case "$STATUS" in
    approved)
        ;;
    draft)
        ERRORS+=("BLOCKED: plan.md Status is 'draft' — awaiting approval")
        PASS=false
        ;;
    rejected)
        ERRORS+=("REJECTED: plan.md Status is 'rejected' — redesign required")
        PASS=false
        ;;
    *)
        ERRORS+=("FAIL: Status field not found or unrecognized value: '$STATUS'")
        PASS=false
        ;;
esac

# Check implementation steps exist (checklist)
STEPS=$(grep -c "\- \[ \]" "$FILE" 2>/dev/null)
STEPS=${STEPS:-0}
COMPLETED=$(grep -c "\- \[x\]" "$FILE" 2>/dev/null)
COMPLETED=${COMPLETED:-0}

if [ "$STEPS" -eq 0 ] && [ "$COMPLETED" -eq 0 ]; then
    ERRORS+=("WARN: No implementation checklist found (Section 3)")
fi

# Check architecture decisions table
if ! grep -qE "\|.*결정.*\|.*선택.*\|" "$FILE" && ! grep -qE "\|.*Decision.*\|.*Choice.*\|" "$FILE"; then
    ERRORS+=("WARN: Architecture decision table not found (Section 2)")
fi

# Output
echo "=== Gate 2: plan.md Approval Check ==="
if [ "$PASS" = true ]; then
    echo "APPROVED: plan.md Status is 'approved' — proceed to implementation"
    TOTAL=$((STEPS + COMPLETED))
    echo "  Checklist: $COMPLETED/$TOTAL steps completed"
    if [ ${#ERRORS[@]} -gt 0 ]; then
        echo "--- Warnings ---"
        for err in "${ERRORS[@]}"; do echo "  $err"; done
    fi
    exit 0
else
    for err in "${ERRORS[@]}"; do echo "  $err"; done
    exit 1
fi
