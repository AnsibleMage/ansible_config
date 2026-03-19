# Zero-Guess Protocol

## Core Principle

Every line of code must trace to a spec document.
If spec doesn't define it, don't implement it — ask or document the assumption.

## Three Mechanisms

| # | Mechanism | Purpose |
|---|-----------|---------|
| 1 | Implementation Block | PRD defines WHAT not HOW; spec docs contain HOW |
| 2 | Precise Reference | `[[doc]] §section -> what` cross-refs with exact location |
| 3 | Guess Prevention | `[warn] DO NOT ASSUME` markers for ambiguous areas |

## Developer Protocol

1. Read PRD to identify what to build
2. Read ALL cross-references for the feature
3. Check [warn] items to confirm nothing assumed
4. Implement using spec doc code/types/constants
5. Verify against test spec fixtures

## Forbidden Actions

- Inventing constants not in spec
- Defining types inline instead of importing from SSOT
- Computing expected test values instead of using fixtures
- Implementing error behavior not in error rules
- Adding features not in current phase scope

## When Spec Is Insufficient

1. Document the gap explicitly
2. Propose a reasonable default
3. Ask user for confirmation
4. Update spec doc FIRST, then implement

## SSOT Enforcement

| Rule | Description |
|------|-------------|
| Constants | Import from single file, never hardcode |
| Types | Import from types dir, never inline |
| Error behavior | Follow error rules doc, never assume |
| Test expectations | Use fixture values, never calculate |
| Structure | Follow architecture doc, never improvise |
