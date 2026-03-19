# Error Recovery Playbook

## Gate Failure Scenarios

| Stage | Failure | Diagnosis | Recovery |
|-------|---------|-----------|----------|
| 0 | Project won't start | Missing deps or wrong version | Check doc/03 stack versions, reinstall |
| 1 | Types don't compile | Spec mismatch or syntax error | Compare with doc/04 type definitions |
| 2 | Unit tests fail | Logic bug or wrong fixture | Check doc/04 signatures + doc/06 fixtures |
| 2 | Boundary values fail | Edge case not handled | Review doc/04 error/boundary rules |
| 3 | UI won't render | Component props mismatch | Compare with doc/05 Props interfaces |
| 3 | API returns wrong status | Route handler logic error | Compare with doc/04 function signatures |
| 4 | E2E flow broken | Integration wiring issue | Check state management, middleware order |
| 5 | Integration tests fail | Cross-layer data mismatch | Verify types flow through all layers |
| 6 | Lint errors | Code style violations | Run auto-format, fix remaining manually |
| 6 | Build fails | Import errors or env issues | Check all imports, env config |

## Recovery Protocol

### Step 1: Classify the Error

```
Error detected → Is it in spec? ─── Yes → Implementation bug
                                │         → Fix code per spec
                                │
                                No → Spec gap
                                     → Update spec first
                                     → Then fix code
```

### Step 2: Fix Priority

| Priority | Condition | Action |
|----------|-----------|--------|
| Fix spec first | Spec is ambiguous or missing | Update doc → implement → test |
| Fix code first | Spec is clear, code is wrong | Fix implementation → re-test |
| Fix test first | Fixture has wrong expected value | Verify against spec → update fixture |

### Step 3: Re-verify Gate

After fix:
1. Run the specific failing test(s)
2. Run full gate verification for the stage
3. Confirm no regressions in previous stages
4. Update workplan progress notes

## Common Pitfalls

| Pitfall | Symptom | Prevention |
|---------|---------|------------|
| Hardcoded values | Tests pass but values don't match spec | Import from SSOT constants |
| Inline types | Type mismatch across layers | Import from types directory |
| Calculated test expectations | Tests pass with wrong logic | Use fixture values from doc/06 |
| Business logic in UI | UI breaks when logic changes | Keep logic in core/, import in UI |
| Skipping gate | Later stages fail unexpectedly | Never skip gate verification |

## Rollback Strategy

If a stage is fundamentally broken:

1. **Identify scope**: Which files were changed in this stage?
2. **Check git**: Can you revert to last gate checkpoint?
3. **Re-read spec**: Is the approach correct per doc?
4. **Restart stage**: If approach was wrong, restart from spec reading
5. **Update state**: Save checkpoint after successful recovery

## Escalation

If recovery attempts fail after 3 tries:
1. Document the issue in workplan
2. Present to user with diagnosis
3. Ask: "이 문제를 해결하려면 [spec 변경/접근 방식 변경/외부 도움]이 필요합니다. 어떻게 진행할까요?"
