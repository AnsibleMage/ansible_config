# Phase 1: INVESTIGATE

## Step 1: Clarifying Questions

Ask maximum 5 questions. Infer when possible.

| Category | Example |
|----------|---------|
| Scope | "핵심 기능 3가지는?" |
| Users | "주요 사용자와 해결할 문제는?" |
| Constraints | "기술 제약이나 선호 스택은?" |
| Scale | "예상 사용자/데이터 규모는?" |
| Timeline | "MVP 완성 목표 시기는?" |

If user says "알아서 해줘", make reasonable assumptions and document them.

## Step 2: Domain Research

WebSearch for:
1. Existing similar products (2-3 examples, strengths/weaknesses)
2. Common implementation patterns
3. Known pitfalls and edge cases
4. Relevant APIs or libraries

## Step 3: Technology Assessment

| Factor | Consideration |
|--------|--------------|
| Project type | Web/CLI/API/Game/Mobile |
| Performance | Real-time, batch, offline |
| Deploy target | Cloud, edge, desktop |
| User preferences | Stated constraints |

## Step 4: Write doc/00_investigation.md

Template:

# Investigation Report: [Project Name]

## 1. Problem Definition
### 1-1. One-Line Summary
### 1-2. Target Users
### 1-3. Core Value Proposition

## 2. Existing Solutions Analysis
### 2-1. [Solution A] — Strengths / Weaknesses
### 2-2. [Solution B] — Strengths / Weaknesses
### 2-3. Differentiation Strategy

## 3. Technical Landscape
### 3-1. Recommended Stack (with rationale)
### 3-2. Key Libraries / APIs
### 3-3. Known Risks and Mitigations

## 4. Scope Recommendation
### 4-1. MVP (Phase 1)
### 4-2. Extension (Phase 2+)
### 4-3. Out of Scope

## 5. Assumptions (if any inferred)

## Step 5: Present and Await Approval

Ask: "조사 결과를 확인해주세요. Phase 2(정의)로 진행할까요?"
