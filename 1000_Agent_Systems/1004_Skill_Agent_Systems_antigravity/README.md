# 🌌 Antigravity System: The Generative Agent Orchestrator

[![Version](https://img.shields.io/badge/Version-2.0.0-purple)](./) [![Agent](https://img.shields.io/badge/Agent-Antigravity-8A2BE2)](./)

> *"Beyond tools. Towards autonomous orchestration."*

This folder contains the **Complete Configuration and Brain** for **Antigravity**, the next-generation autonomous coding agent for Gemini.
It represents the culmination of the "Agent Systems Thinking" framework, evolved into a fully operational "Dynamic Chain System".

---

## 🏛️ Core Identity

**Antigravity** is not just a chatbot. It is a **Proactive Orchestration Agent** designed by Google DeepMind guidelines.

*   **Proactive**: It proposes tests, fixes, and improvements before being asked.
*   **Context-First**: It uses a dedicated `translation-specialist` cortex to understand intent (Lexical/Syntactic/Pragmatic) before acting.
*   **Dynamic**: It constructs execution chains (Sequential/Parallel/Hybrid) on the fly based on the user's hidden needs.

---

## 🧠 System Architecture

### 1. The Global Configuration (`00_Config_GEMINI_Global_Setting.md`)
The `GEMINI.md` file is the heart of the system. It defines:
*   **Workflow Engine**: A 5-step loop (Perceive → Plan → Act → Verify → Memorize).
*   **Trigger System**: Dual-layer triggers (Keyword + Semantic) for 16 distinct skills.
*   **Memory System**: Automated logging of decisions and context to `context_log.json`.

### 2. The Skill Ecosystem (`global_skills/`)
A unified library of 20+ specialized skills (migrated from previous agent systems):
*   **Cognitive Layer**: `insight-explorer`, `multidimensional-analyst`, `integrated-sage`...
*   **Role Layer**: `system-architect`, `code-developer`, `quality-reviewer`...
*   **Meta Layer**: `quality-manager`, `context-manager`, `translation-specialist`.

### 3. The Brain (`doc/`)
A comprehensive archive of the research, analysis, and planning documents that built this system:
*   **Analyses**: System thinking, memory architecture, sub-agent capabilities.
*   **Reports**: Research on dynamic chains and trigger mechanisms.
*   **Audits**: Migration logs and verification walkthroughs.

---

## 📂 File Structure

```text
1004_Skill_Agent_Systems_antigravity/
├── 00_Config_GEMINI_Global_Setting.md   # [ CORE ] The final V2.0 configuration file
├── 01_Analysis_Gemini_Basic.md          # Analysis of the base Gemini capabilities
├── 02_Analysis_Sub_Agents.md            # deep-dive into sub-agent architectures
├── 03_Analysis_Agent_Framework.md       # Analysis of the 16-agent thinking framework
├── 04_Audit_Pre_Migration.md            # Audit log before system migration
├── 05_Plan_Migration_Strategy.md        # The step-by-step implementation plan
├── 06_Report_Migration_Results.md       # Final walkthrough and verification report
├── 07_Research_Dynamic_Chains.md        # Research on Agent Chains & Triggers
└── 08_Analysis_Memory_System.md         # Architecture of the Active Memory System
```

---

## 🚀 How to Install

To activate the Antigravity System on your local Gemini environment:

1.  **Deploy Configuration**:
    Copy `00_Config_GEMINI_Global_Setting.md` to `~/.gemini/GEMINI.md`.

2.  **Deploy Skills**:
    Ensure the `global_skills/` folder contents are migrated to `~/.gemini/antigravity/global_skills/`.

3.  **Activate Memory**:
    Create `~/.gemini/antigravity/memory/` and initialize `context_log.json` (refer to `08_Analysis_Memory_System.md`).

---

*Verified and Archived by Antigravity.*
