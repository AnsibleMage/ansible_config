#!/bin/bash
# gate3_checker.sh — code review quality gate verifier
# Usage: bash gate3_checker.sh <path-to-review-report.md>
# Exit 0 = PASS (merge allowed), Exit 1 = BLOCKED (fix required)
#
# Decision matrix:
#   Critical 1+ → BLOCKED (fix required)
#   Warning 3+  → WARNING (proceed with caution, 앤 판단)
#   Info only   → PASS (auto-approve)
#
# Expected report format: ### C-N (Critical), ### W-N (Warning), ### I-N (Info)

FILE="$1"

# File exists
if [ ! -f "$FILE" ]; then
    echo "FAIL: Review report not found: $FILE"
    exit 1
fi

# Count individual issues by section header pattern
# Critical: ### C-1, ### C-2, etc.
CRITICAL=$(grep -cE "^### C-[0-9]" "$FILE" 2>/dev/null)
CRITICAL=${CRITICAL:-0}

# Warning: ### W-1, ### W-2, etc.
WARNING=$(grep -cE "^### W-[0-9]" "$FILE" 2>/dev/null)
WARNING=${WARNING:-0}

# Info: ### I-1, ### I-2, etc.
INFO=$(grep -cE "^### I-[0-9]" "$FILE" 2>/dev/null)
INFO=${INFO:-0}

# Output
echo "=== Gate 3: Code Review Quality Check ==="
echo "  Critical: $CRITICAL"
echo "  Warning:  $WARNING"
echo "  Info:     $INFO"

if [ "$CRITICAL" -gt 0 ]; then
    echo "BLOCKED: $CRITICAL Critical issue(s) found — fix required before merge"
    exit 1
elif [ "$WARNING" -ge 3 ]; then
    echo "WARNING: $WARNING Warning(s) found — proceed with caution (앤 판단 필요)"
    exit 0
else
    echo "PASS: Quality gate cleared — merge allowed"
    exit 0
fi
