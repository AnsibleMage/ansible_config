---
name: vibe-dev
description: >
  Document-driven AI pair programming methodology for building any software project from idea to completion.
  Implements Zero-Guess Protocol, SSOT, and Stage/Gate quality system across 4 phases:
  Investigate, Define, Develop, Report.
  Use when: (1) Starting a new project from an idea or requirements ("새 프로젝트", "프로젝트 시작"),
  (2) User says "바이브 개발", "vibe dev", "vibe-dev",
  (3) User wants structured AI-assisted development with full documentation,
  (4) User wants to generate PRD, work plan, or detailed specs,
  (5) User wants Stage/Gate development workflow with quality gates.
  Supports: web apps, CLI tools, APIs, games, mobile apps, scripts, libraries, any software project.
  Trigger: /vibe-dev followed by idea or project description
---

# Vibe Dev - Document-Driven AI Development

4-Phase methodology. All code derives from documents. No guessing.

```
Phase 1: INVESTIGATE (조사) -> Phase 2: DEFINE (정의) -> Phase 3: DEVELOP (개발) -> Phase 4: REPORT (보고)
```

## Entry Point Detection

| User Input | Start Phase |
|------------|-------------|
| Idea only ("~만들고 싶어") | Phase 1 |
| Requirements/specs exist | Phase 2 |
| doc/ folder with specs | Phase 3 |
| Code exists, needs review | Phase 4 |
| "이어서" / "continue" | Resume last |

## Phase 1: INVESTIGATE

See [references/phase1-investigate.md](references/phase1-investigate.md).

1. Ask max 5 clarifying questions (scope, users, constraints, scale, timeline)
2. Domain research via WebSearch (existing solutions, patterns, pitfalls)
3. Technology assessment (stack recommendation with rationale)
4. Write `doc/00_investigation.md`
5. Present summary -> **User approval required**

## Phase 2: DEFINE

See [references/phase2-define.md](references/phase2-define.md) for guide.
See [references/document-templates.md](references/document-templates.md) for templates.

Document generation order:
1. `doc/01_PRD.md` — What + Where + Zero-Guess -> **User approval required**
2. `doc/02_workplan.md` — When + Order + Gate
3. `doc/03_architecture.md` — Tech stack + structure + SSOT map
4. `doc/04_impl_spec.md` — Types, constants, functions, error rules
5. `doc/05_ui_spec.md` — Design system + wireframes + Props (skip if no UI)
6. `doc/06_test_spec.md` — Fixtures, boundary values, scenarios
7. `doc/07_ai_strategy.md` — Chain/batch/Teams strategy (optional)

Zero-Guess Protocol: See [references/zero-guess-protocol.md](references/zero-guess-protocol.md).

## Phase 3: DEVELOP

See [references/phase3-develop.md](references/phase3-develop.md).
Resume protocol: See [references/checkpoint-protocol.md](references/checkpoint-protocol.md).

```
Stage 0: Init (project setup + deps)            -> Gate: runs without errors
Stage 1: Foundation (types + constants + schema) -> Gate: compiles clean
Stage 2: Core Logic (business functions, TDD)    -> Gate: unit tests pass
Stage 3: Interface (UI/API/CLI per spec)         -> Gate: renders/responds
Stage 4: Integration (connect layers)            -> Gate: e2e flow works
Stage 5: Testing (integration + e2e)             -> Gate: all tests pass
Stage 6: Polish (a11y, perf, deploy)             -> Gate: production ready
```

Rules:
- Stage 2 and 3 can run in parallel (Teams) if independent
- Each stage: read spec -> implement per Zero-Guess -> gate verify -> user checkpoint
- Gate failure blocks next stage. Fix first, re-verify.
- Error recovery: See [references/error-recovery.md](references/error-recovery.md).

## Phase 4: REPORT

See [references/phase4-report.md](references/phase4-report.md).

1. AI self-review (score each document 1-10)
2. Cross-reference verification (SSOT consistency)
3. Write `doc/08_review.md` + `doc/09_final_report.md`
4. Present completion summary

## Chain Integration

| Phase | Chain | Key Agents |
|-------|-------|-----------|
| 1 | ResearchChain | multidimensional_analyst, insight_explorer |
| 2 | SystemDesignChain | system_architect, requirements_analyst |
| 3 | DevChain / WebDevChain+ | code_developer, quality_reviewer |
| 4 | MetaThinkChain | balanced_judge, integrated_sage |

## Customization

- `/vibe-dev skip-phase1` — Start from definition
- `/vibe-dev skip-ui` — Skip UI spec (CLI/API/library)
- `/vibe-dev resume` — Resume from last checkpoint
- `/vibe-dev report-only` — Report for existing project

Usage examples: See [references/usage-examples.md](references/usage-examples.md).
