# Official Antigravity Documentation Analysis

**Date:** 2026-01-24
**Source:** https://antigravity.google/docs/ (Agent Modes, Rules, Skills)

## 1. Directory Structure Standards

The official documentation defines the following standard paths for global processing:

| Feature | Scope | Official Path | Current User Path (Migration Target) |
| :--- | :--- | :--- | :--- |
| **Global Skills** | All Workspaces | `~/.gemini/antigravity/global_skills/` | `~/.gemini/antigravity/skills/` |
| **Workspace Skills** | Project Specific | `<root>/.agent/skills/` | N/A |
| **Global Rules** | All Workspaces | `~/.gemini/GEMINI.md` | `~/.gemini/GEMINI.md` |
| **Workflows** | All/Project | `.agent/workflows/` | `~/.gemini/antigravity/workflows/` (found in audit) |

> **Key Finding:** Your current global skills are in `.../skills/`, but the official standard is `.../global_skills/`.

## 2. Feature Specifications

### 2.1 Agent Skills
**Definition:** Reusable packages extending agent capabilities.
**Structure:**
- Must be a **folder** containing a `SKILL.md` file.
- `SKILL.md` requires YAML frontmatter:
  ```yaml
  ---
  name: skill-name
  description: Clear description for the agent to decide when to use it.
  ---
  ```
- **Discovery:** "Progressive Disclosure" - Agent sees the list, reads `SKILL.md` if relevant. No manual invocation needed.

### 2.2 Rules (Global & Workspace)
**Definition:** Manually defined constraints (Markdown).
**Global Rule:** `~/.gemini/GEMINI.md` acts as the single source of truth for global behavior constraints.
**Activation:**
- Manual (@mention)
- Always On
- Model Decision
- Glob Pattern

### 2.3 Workflows
**Definition:** Repeatable sequences of steps (e.g., `/workflow-name`).
**Format:** Markdown files in `.agent/workflows`.

### 2.4 Agent Modes
- **Planning:** For complex tasks (Research -> Plan -> Execute). Uses Artifacts.
- **Fast:** For simple, quick tasks.

## 3. Analysis of Your Custom "Sub-agents" (Personas)
The official documentation does **not** explicitly define a "Persona" or "Sub-agent" feature with a dedicated directory like `.../personas/`.

**Recommended Migration Strategy:**
To align with official standards, your "Personas" (e.g., `101_system_architect.md`) should likely be converted into:
1.  **Skills:** If they are tools/processes the agent uses (e.g., "System Design Skill").
2.  **Global Rules:** Included in `GEMINI.md` if they are always-on behaviors.
3.  **Workflows:** If they are specific procedures.

Given they are "Roles", converting them to **Skills** (e.g., "Act as System Architect") is often the most flexible pattern, allowing the agent to "activate" that persona when needed.

## 4. Next Steps
Based on this learning, the proposed migration plan would be:
1.  **Move** `~/.gemini/antigravity/skills` -> `~/.gemini/antigravity/global_skills`.
2.  **Refactor** "Personas" into the `global_skills` folder structure (e.g., `global_skills/system-architect/SKILL.md`).
3.  **Verify** `~/.gemini/GEMINI.md` is set up as the Global Rules entry point.
