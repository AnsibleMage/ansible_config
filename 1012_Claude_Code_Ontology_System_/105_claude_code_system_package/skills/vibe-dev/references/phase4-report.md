# Phase 4: REPORT

## Step 1: AI Self-Review

Score each document 1-10:

| Document | Criteria |
|----------|----------|
| PRD | Clear scope, cross-refs, Zero-Guess markers |
| Architecture | Complete structure, SSOT map, principles |
| Impl Spec | Types, constants, signatures, error rules present |
| UI Spec | Props, wireframes, design system (if applicable) |
| Test Spec | Structured fixtures, boundaries, scenarios |

## Step 2: Cross-Reference Verification

| Check | Method |
|-------|--------|
| Types match doc/04 | Compare type files with spec |
| Constants match doc/04 | Compare constant files with spec |
| Signatures match doc/04 | Compare implementations with spec |
| Fixtures match doc/06 | Compare test files with spec |
| Structure matches doc/03 | Compare actual tree with spec |

## Step 3: Write doc/08_review.md

```
# Development Review

## 1. Document Quality Scores
| Document | Score | Key Finding |

## 2. Cross-Reference Results
| Check | Status | Details |

## 3. Remaining Guess Items
| Item | Impact | Resolution |

## 4. Improvement Recommendations
### Immediate
### Long-term
```

## Step 4: Write doc/09_final_report.md

```
# Final Report: [Project Name]

## 1. Project Summary
### 1-1. Original Requirements
### 1-2. Delivered Scope
### 1-3. Deviations

## 2. Metrics
| Metric | Value |
| Documents generated | |
| Source files | |
| Test files | |
| Test pass rate | |
| Stages completed | |

## 3. Phase Status
| Phase | Status | Notes |

## 4. Gate Summary
| Stage | Gate | Status |

## 5. Lessons Learned
### What worked
### What to improve

## 6. Next Steps
### Phase 2 features
### Future scope
```

## Step 5: Present Completion

Summarize: scope delivered, metrics, remaining items, next actions.
