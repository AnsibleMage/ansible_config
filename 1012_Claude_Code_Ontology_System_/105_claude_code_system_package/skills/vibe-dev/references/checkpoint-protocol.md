# Checkpoint & Resume Protocol

## Checkpoint State

After each stage gate or phase transition, save state to `doc/.vibe-dev-state.md`:

```markdown
# Vibe Dev State

## Current Position
- Phase: [1-4]
- Stage: [0-6] (Phase 3 only)
- Last Completed: [description]
- Next Action: [description]

## Documents Generated
| # | Document | Status |
| 00 | investigation | ✅/❌/⏳ |
| 01 | PRD | ✅/❌/⏳ |
| 02 | workplan | ✅/❌/⏳ |
| 03 | architecture | ✅/❌/⏳ |
| 04 | impl_spec | ✅/❌/⏳ |
| 05 | ui_spec | ✅/❌/⏳ |
| 06 | test_spec | ✅/❌/⏳ |
| 07 | ai_strategy | ✅/❌/⏳ |
| 08 | review | ✅/❌/⏳ |
| 09 | final_report | ✅/❌/⏳ |

## Gate History
| Stage | Gate | Status | Date |
```

## Resume Logic

When `/vibe-dev resume` is invoked:

1. Check for `doc/.vibe-dev-state.md`
2. If found: read current position, present to user
3. If not found, scan `doc/` folder to infer state:
   - Only `doc/00_investigation.md` exists → Resume at Phase 2
   - `doc/01_PRD.md` through `doc/06_test_spec.md` exist → Resume at Phase 3
   - Source code + tests exist → Detect last completed stage via gate checks
   - All code + tests pass → Resume at Phase 4
4. Present: "[Phase/Stage] 완료 확인. 다음 단계로 진행할까요?"
5. On approval, continue from detected position

## State Update Triggers

| Event | Action |
|-------|--------|
| Phase 1 complete (investigation approved) | Save: phase=1, next=Phase 2 |
| PRD approved | Save: phase=2, doc 01 done |
| All Phase 2 docs generated | Save: phase=2, next=Phase 3 |
| Stage N gate passed | Save: phase=3, stage=N, next=Stage N+1 |
| All Stage 6 gates passed | Save: phase=3, next=Phase 4 |
| Final report written | Save: phase=4, status=complete |

## Fallback (No State File, No doc/ Folder)

Treat as new project → Start Phase 1.
