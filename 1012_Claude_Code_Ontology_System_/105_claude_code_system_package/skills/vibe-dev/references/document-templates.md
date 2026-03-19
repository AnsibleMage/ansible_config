# Document Templates

## Section 1: PRD Template

```
# [Project Name] — PRD

> Created: [date] | Version: 1.0
> WHAT and WHERE, not HOW.

## Zero-Guess Protocol
> All code must derive from spec documents. No guessing.

## 1. Product Identity
### 1-1. One-Line Definition
### 1-2. Core Values
### 1-3. Target Users

## 2. Document Ecosystem
| # | Document | Role | Key Content |
| 01 | PRD | What/Where | This document |
| 02 | Work Plan | When/Order/Gate | Stage/Gate definitions |
| 03 | Architecture | Structure | Stack, dirs, SSOT |
| 04 | Impl Spec | Logic | Types, constants, functions |
| 05 | UI Spec | Interface | Design, wireframes, Props |
| 06 | Test Spec | Verification | Fixtures, scenarios |

## 3. Feature -> Document Map
### [Feature A]
- MUST-READ: [[doc/04]] §N -> types/constants
- MUST-READ: [[doc/06]] -> test fixtures
- [warn] DO NOT ASSUME: [specific item] -- see [[doc/04]] §M

## 4. Phase Scope
### Phase 1 (MVP)
### Phase 2 (Extension)

## 5. Quality Gates
| Gate | Verification | Criteria |
```

## Section 2: Work Plan Template

```
# [Project Name] — Work Plan

## Stage Definitions
| Stage | Name | Entry | Exit | Est. |
| 0 | Init | PRD approved | Runs | 1 session |
| 1 | Foundation | Stage 0 | Compiles | 1 session |
| 2 | Core Logic | Stage 1 | Tests pass | 2-3 sessions |
| 3 | Interface | Stage 1 | Renders | 2-3 sessions |
| 4 | Integration | 2+3 done | E2E works | 1 session |
| 5 | Testing | Stage 4 | All pass | 1 session |
| 6 | Polish | Stage 5 | Deploy ready | 1 session |

## Progress Tracker
| Stage | Status | Date | Notes |
```

## Section 3: Architecture Template

```
# [Project Name] — Architecture

## 1. Tech Stack
| Layer | Technology | Version | Rationale |

## 2. Project Structure
[directory tree]

## 3. SSOT Map
| Information | Source File | Rule |

## 4. Design Principles
| Principle | Description | Example |
```

## Section 4: Implementation Spec Template

```
# [Project Name] — Implementation Spec

## 1. Type Definitions
[complete code blocks]

## 2. Constants
[complete code blocks with literal values]

## 3. Function Signatures
### [Function A]
- Input: [type]
- Output: [type]
- Errors: [behavior]
- Pseudocode: [if complex]

## 4. Error/Boundary Rules
| Case | Expected Behavior |

## 5. Validation Schema
[complete code]

## 6. Security Requirements
### Input Validation
| Field | Rule | Reject Example |
### Sensitive Data
| Data | Storage | Access |
### Auth (if applicable)
| Endpoint | Auth Required | Role |
```

## Section 5: Test Spec Template

```
# [Project Name] — Test Spec

## 1. Fixtures
[complete importable code]

## 2. Boundary Values
| Function | Input | Expected | Category |

## 3. Integration Scenarios
### Scenario N: [Name]
- Input: [data]
- Expected: [data]
- Validates: [what]

## 4. E2E Scenarios
### Journey N: [Name]
- Steps: [actions]
- Expected: [outcomes]

## 5. Coverage Targets
| Layer | Line Coverage | Branch Coverage |
| Core Logic (lib/) | 90%+ | 80%+ |
| Interface (routes/components) | 70%+ | 60%+ |
| Integration (critical paths) | 100% | - |
| E2E (user journeys) | All primary flows | - |
```
