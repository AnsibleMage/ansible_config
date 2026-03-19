# Migration Audit Report: Custom Skills & Sub-agents

**Date:** 2026-01-24
**Purpose:** Identify custom global skills and sub-agents for migration to official features.
**Target Directories:** 
- `/Users/changjaeyou/.gemini` (Primary source of custom content)
- `/Users/changjaeyou/.antigravity` (Extensions/System files only)

## 1. Global Skills (전역 스킬)
Found in: `/Users/changjaeyou/.gemini/antigravity/skills`

These appear to be fully structured custom skills with `SKILL.md` definitions.

| Skill Name | Path | Description |
| :--- | :--- | :--- |
| **translation-specialist** | `.../skills/translation-specialist` | **Context-Aware Translation Agent**<br>- 4-Layer Linguistic Analysis<br>- Domain auto-detection (Legal, Tech, etc.)<br>- Functional Equivalence methodology |
| **git-commit-helper** | `.../skills/git-commit-helper` | **Commit Message Generator**<br>- Generates conventional commit messages based on git diffs. |
| **skill-generator** | `.../skills/skill-generator` | **Skill Scaffolding Tool**<br>- Generates the standard `SKILL.md` structure and boilerplate for new skills. |

## 2. Sub-agents / Personas (서브에이전트)
Found in: `/Users/changjaeyou/.gemini/antigravity/personas`

These are markdown definitions for specialized AI personas.

| Agent ID | Path | Role & Expertise |
| :--- | :--- | :--- |
| **101_system_architect** | `.../personas/101_system_architect.md` | **System Architecture**<br>- DDD, Clean Architecture, Scalability<br>- Mermaid diagram generation |
| **105_code_reviewer** | `.../personas/105_code_reviewer.md` | **Code Quality**<br>- Best practices, linting, convention checks |
| **201_backend_developer** | `.../personas/201_backend_developer.md` | **Backend Implementation**<br>- Server-side logic, API development |

## 3. Findings in `.antigravity`
Location: `/Users/changjaeyou/.antigravity`

**Status:** No custom skills or personas found.
This directory contains VSCode extensions (`devsense.*`, `vscjava.*`, `ms-python.*`) and system binaries. It does not require migration for custom logic.

## 4. Next Steps
To migrate these to the official feature set, please confirm if you would like to:
1.  Verify the integrity of these files.
2.  Move them to the new official directory (if applicable).
3.  Register them in the new configuration system.
