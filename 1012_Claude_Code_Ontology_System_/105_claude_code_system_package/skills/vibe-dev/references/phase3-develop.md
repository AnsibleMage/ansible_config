# Phase 3: DEVELOP

## Stage/Gate System

```
Stage 0 → Gate → Stage 1 → Gate → Stage 2 ──┐
                                              Gate
Stage 6 ← Gate ← Stage 5 ← Gate ← Stage 4 ← Stage 3
```

## Stage Details

### Stage 0: Init
- Create project with framework CLI
- Install deps per doc/03
- Create directory structure per doc/03
- Configure lint, format, git
- **Gate**: project runs without errors, structure matches doc/03

### Stage 1: Foundation
- Types from doc/04
- Constants from doc/04
- Validation schemas from doc/04
- Test fixtures from doc/06
- **Gate**: all types compile, constants match doc/04, SSOT files created

### Stage 2: Core Logic
- Business functions per doc/04 signatures (TDD)
- Group related functions (3-5 per batch)
- Each batch: implement + test in same prompt
- **Gate**: all unit tests pass, boundary values pass, no hardcoded values

### Stage 3: Interface

Adapt per project type:

| Type | Stage 0 (Init) | Stage 3 (Interface) | Stage 6 (Polish) |
|------|----------------|---------------------|-------------------|
| Web App | Framework CLI (Next.js, Vite...) | UI components per doc/05 | a11y audit + deploy |
| API Server | Express/Fastify/Hono setup | Route handlers + middleware | Swagger + deploy |
| CLI Tool | Package init + bin setup | Command handlers + arg parsing | man page + npm publish |
| Library | Package init + exports | Public API surface per doc/04 | Docs + npm/pypi publish |
| Game | Engine setup (Roblox/Phaser) | Game loop + UI per doc/05 | Performance + build |
| Mobile | React Native / Flutter init | Screens + navigation | Store submission prep |

Default interface tasks:
- Web: UI components per doc/05
- API: route handlers per doc/04
- CLI: command handlers per doc/04
- Library: public API per doc/04
- **Gate**: all interfaces per spec, no business logic in interface layer

### Stage 4: Integration
- Connect core logic to interface
- State management / middleware
- Wire up validation
- **Gate**: end-to-end flow works for primary use case

### Stage 5: Testing
- Integration tests from doc/06 scenarios
- E2E tests (if applicable)
- Cross-reference all expectations with doc/06
- **Gate**: all tests pass, no hardcoded expected values

### Stage 6: Polish
- Performance optimization
- Accessibility audit (if UI)
- README generation
- Deploy configuration
- **Gate**: lint passes, no TODOs, deploy ready

## Batch Strategy

```
Stage 1: All types + constants + schema in 1 batch
Stage 2: 3-5 related functions per batch
Stage 3: Shared components first, then feature groups
Stage 4: Single integration batch
Stage 5: Unit/integration batch, then E2E batch
```

## Teams Parallelism

Stage 2 + 3 can run in parallel if:
- Logic layer has no UI dependencies
- Interface has no logic dependencies
- Separate file directories (no shared writes)

Configuration:
- Teammate A (logic-dev): Stage 2 in lib/ or core/
- Teammate B (ui-dev): Stage 3 in components/ or routes/
- Lead: Stage 1 (before), Stage 4 (after both complete)

## User Checkpoints

After each stage gate:
1. What was completed (file list + test results)
2. Gate checklist status
3. Deviations from spec (if any)
4. "Stage N 완료. 다음으로 진행할까요?"

## Hotfix Protocol

Bug found during development:
1. Check which spec doc should cover it
2. Spec gap → update doc first, then fix code
3. Implementation error → fix code, verify against doc
4. Document fix in workplan progress
