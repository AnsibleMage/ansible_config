# Gemini Evolution v2.0: Global Skills Architecture

**Version:** 2.0
**Date:** 2026-01-24
**Author:** Antigravity (Gemini)

## 1. Introduction

Gemini Evolution v2.0 marks a significant architectural shift from the "Sub-agent" pattern (v1.0) to a **Unified Global Skills Architecture**. 

In v1.0, we distinguished between "Sub-agents" (identity/persona) and "Skills" (tools). In v2.0, we recognize that **Skills are a superset of Sub-agents**. A well-structured Skill can contain not only tools (scripts) but also the persona (identity) and rules required to execute complex tasks.

## 2. Core Concept: Skill as a Superset

The traditional Sub-agent definition was limited to a single Markdown file defining a persona. The "Skill" definition in Antigravity is a directory structure that can contain:
1.  **Identity** (in `SKILL.md`): Who the agent becomes.
2.  **Rules** (in `SKILL.md`): How the agent behaves.
3.  **Tools** (in `scripts/`): Executable code (Python/Shell) to perform deterministic actions.
4.  **Resources** (in `resources/`): Templates and data files.

Therefore, we do not need a separate `personas/` directory. All capabilities are unified under `global_skills/`.

## 3. Directory Structure

The new standard location for all global capabilities is:

```
~/.gemini/antigravity/global_skills/
├── backend-developer/     # [Transformed Sub-agent]
│   └── SKILL.md
├── code-reviewer/         # [Transformed Sub-agent]
│   └── SKILL.md
├── git-commit-helper/     # [Original Skill]
│   └── SKILL.md
├── skill-generator/       # [Original Skill]
│   └── SKILL.md
├── system-architect/      # [Transformed Sub-agent]
│   └── SKILL.md
└── translation-specialist/ # [Original Skill]
    ├── SKILL.md
    └── examples.md
```

## 4. Migration Strategy (v1.0 -> v2.0)

To upgrade from v1.0 to v2.0:

1.  **Consolidate**: Move all separate tool skills to `global_skills/`.
2.  **Transform**: Convert "Persona" markdown files (`*.md`) into Skill folders.
    *   Create a folder matching the agent's role (e.g., `system-architect`).
    *   Create `SKILL.md` inside.
    *   Migrate the "Role", "Expertise", and "Rules" sections from the Persona file into `SKILL.md`.
    *   Add a standard YAML frontmatter.

## 5. Usage

The Antigravity system automatically indexes these skills.
- **Implicit Invocation**: The agent naturally selects the best skill for the task.
- **Explicit Invocation**: You can mention the skill name (e.g., "Use **code-reviewer**") to force a specific persona/strategy.

---
**Status:** Implemented & Verified
**Next Steps:** Continue expanding the library of Global Skills.
