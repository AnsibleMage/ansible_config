# Phase 2: DEFINE

## Document Hierarchy

```
PRD (What/Where) ──► Work Plan (When/Order/Gate)
       │
       ├── Architecture (structure)
       ├── Implementation Spec (logic)
       ├── UI Spec (interface) [optional]
       ├── Test Spec (verification)
       └── AI Strategy (workflow) [optional]
```

## Generation Order

### Doc 1: PRD (doc/01_PRD.md)

See document-templates.md Section 1 for template.

Rules:
- Define WHAT and WHERE, never HOW
- Every feature links to detail spec via `[[doc]] §section` markers
- Include `[warn] DO NOT ASSUME` for ambiguous areas
- User must approve before generating remaining docs

### Doc 2: Work Plan (doc/02_workplan.md)

See document-templates.md Section 2.

Key sections:
- Stage definitions with entry/exit criteria
- Dependency graph
- Gate verification checklists
- Batch prompt strategy

### Doc 3: Architecture (doc/03_architecture.md)

See document-templates.md Section 3.

Key sections:
- Tech stack with version pinning
- Directory structure (tree format)
- SSOT map (which file is truth for which info)
- Design principles with examples

### Doc 4: Implementation Spec (doc/04_impl_spec.md)

See document-templates.md Section 4. This is the CORE document.

Rules:
- Types must be complete, copy-paste ready code
- Constants must be literal values, never external references
- Every function: input type, output type, error cases
- Edge cases explicitly listed with expected behavior

Security requirements (MANDATORY section in doc/04):
- Input validation rules (injection prevention for user-facing inputs)
- Authentication/authorization requirements (if applicable)
- Sensitive data handling (never hardcode API keys, credentials, secrets)
- Rate limiting / DoS protection (if public-facing)

### Doc 5: UI Spec (doc/05_ui_spec.md) [Skip for non-UI]

Key sections:
- Design system (colors, typography, spacing)
- Component hierarchy with Props interfaces
- Wireframes (ASCII or description)
- Responsive breakpoints + accessibility requirements

### Doc 6: Test Spec (doc/06_test_spec.md)

See document-templates.md Section 5.

Rules:
- Fixtures in target language (importable)
- Expected values pre-calculated, not left to AI
- Each fixture: name, input, expected output

### Doc 7: AI Strategy (doc/07_ai_strategy.md) [Optional]

Chain selection, batch prompts, Teams composition, session plan.

## Cross-Reference Notation

- Reference: `[[doc_name]] §section -> what to extract`
- Warning: `[warn] DO NOT ASSUME: [what] -- see [doc] [section]`
- SSOT: `SSOT for [info]: [doc] [section]`

## User Checkpoint

After PRD: present scope/phases/gates summary, get approval.
On approval: generate remaining docs sequentially.
On revision: update PRD, re-present.
