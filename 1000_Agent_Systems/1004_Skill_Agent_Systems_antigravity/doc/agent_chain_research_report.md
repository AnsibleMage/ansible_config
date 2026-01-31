# Research Report: Agent Chain & Trigger Systems

**Date**: 2026-01-24
**Topic**: enhancing Antigravity's Global Configuration (`GEMINI.md`) via advanced Chain and Trigger systems.
**Sources**: Anthropic (Claude), Google (Gemini), Microsoft (AutoGen), Academic Papers (ReAct, MAS).

---

## 1. Executive Summary
Efficient multi-agent systems rely on two core components: **Triggers** (Intent Detection) and **Chains** (Workflow Orchestration).
Research indicates a shift from simple sequential chains to **Dynamic Semantic Routing** and **Parallel/Hybrid Execution** patterns.
To stand as a "Global Standard" for Antigravity, the configuration must support not just rigid sequences but adaptive workflows that "Perceive, Think, Act, and Verify."

---

## 2. Trigger Systems (The "Brain")

### A. Evolution of Triggers
1.  **Keyword Matching (Generation 1)**: Simple `if "code" in input: call Developer`.
    *   *Limitation*: Fails on nuance (e.g., "Review this logic" might need an Architect, not just a Reviewer).
2.  **Semantic Routing (Generation 2 - Recommended)**:
    *   Uses vector embeddings to map user intent to "Agent Clusters".
    *   *Application*: "Make this faster" → triggers `Performance Optimization Chain` (Developer + Profiler).
3.  **Event-Driven Triggers (Generation 3)**:
    *   System state changes trigger agents (e.g., "Test Failed" event automatically triggers `Debugger Agent`).

### B. Industry Best Practices
*   **Microsoft AutoGen**: Uses a `GroupChatManager` with "Speaker Selection" strategies (Round Robin, Random, or LLM-based) acting as dynamic triggers.
*   **Google Gemini**: Emphasizes `description` fields in agent definitions as the primary API for the semantic router.

### C. Recommendation for Antigravity
Implement a **Dual-Layer Trigger System**:
1.  **Fast Path (Keyword)**: High-confidence, specific commands (e.g., `/architect`).
2.  **Slow Path (Semantic)**: Natural language intent analysis (e.g., "I'm worried about scalability" -> triggers Architect + Complexity Resolver).

---

## 3. Chain Systems (The "Body")

### A. Execution Patterns
| Pattern | Description | Best For |
| :--- | :--- | :--- |
| **Sequential (ReAct)** | `Agent A -> Agent B -> Agent C` | Linear tasks (e.g., Plan -> Code -> Review). |
| **Parallel (Map-Reduce)** | `[Agent A, Agent B, Agent C] -> Aggregator` | Research, Brainstorming (e.g., 3 diverse perspectives). |
| **Hybrid / Nested** | `(A || B) -> C -> Loop(D)` | Complex System Design (e.g., Frontend + Backend Dev -> Integration -> Testing Loop). |
| **Evaluator-Optimizer** | `Generator -> Evaluator -> (Loop if < Score)` | High-quality Code Generation (Claude's preferred pattern). |

### B. The "Universal Agent Loop" (Anthropic)
Effective chains follow a robust internal loop:
1.  **Perceive**: Gather context.
2.  **Think**: Reason about the approach (Chain of Thought).
3.  **Act**: Use tools.
4.  **Verify**: Check results against success criteria. *Critical step often missing in simple chains.*

### C. Recommendation for Antigravity
Define "Standard Chains" in `GEMINI.md` that correspond to these patterns:
*   **DevChain**: `Architect (Plan) -> Developer (Code) -> Reviewer (Verify) -> (Loop if Fail)`
*   **ThinkChain**: `Insight (Explore) -> [Multidim + Connection] (Parallel Analysis) -> Sage (Synthesize)`

---

## 4. Proposed Upgrades to GEMINI.md

Based on this research, the following enhancements are proposed for the Global Configuration:

### 1. Advanced Trigger Definitions
Map triggers not just to single agents, but to **Intent Categories**.
```markdown
| Intent Category | Primary Skill | Support Skills |
| :--- | :--- | :--- |
| **"System is slow"** | `Quality Reviewer` (Perf) | `Complexity Resolver` |
| **"New Feature"** | `Requirements Analyst` | `System Architect` |
```

### 2. Explicit Workflow Definitions
Formalize the "Chain System" section with visualizable paths.
*   **Sequential**: `->`
*   **Parallel**: `||`
*   **Loop**: `(Loop Condition)`

### 3. The "Quality Gate" Rule
Add a global rule that **NO Chain completes without a Verification Step**.
*   *Research*: Systems with a dedicated verifier/evaluator node perform significantly better (Google/Anthropic findings).
*   *Config*: Always end Dev chains with `Quality Reviewer`.

### 4. Semantic Context Sharing
Adopt Google ADK's "State Management" principle:
*   Define a standard `Context Handoff Format` between agents to prevent information loss.
