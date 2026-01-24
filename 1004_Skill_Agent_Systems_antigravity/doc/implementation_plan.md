# Implementation Plan: Agent Systems Thinking Migration

**Goal:** Migrate the 16 agents from the 'Agent Systems Thinking' framework (`1003_Agent_Systems_Thinking`) into the `global_skills` architecture. This will create a comprehensive ecosystem of cognitive and role-based skills.

## User Review Required
> [!IMPORTANT]
> This operation will create 16 new/updated folders in `~/.gemini/antigravity/global_skills`.
> Existing skills `system-architect` and `code-reviewer` will be updated with richer content.

## Proposed Changes

### 1. Cognitive Agents (New Skills)
Create new skill folders and `SKILL.md` for agents 01-10:
- `global_skills/insight-explorer/`
- `global_skills/multidimensional-analyst/`
- `global_skills/connection-creator/`
- `global_skills/problem-reframer/`
- `global_skills/solution-innovator/`
- `global_skills/insight-amplifier/`
- `global_skills/learning-evolver/`
- `global_skills/complexity-resolver/`
- `global_skills/balanced-judge/`
- `global_skills/integrated-sage/`

### 2. Role Agents (Update/New Skills)
- `global_skills/requirements-analyst/` (New)
- `global_skills/system-architect/` (Update: overwrite with `112_System_Architect.md`)
- `global_skills/code-developer/` (New: distinct from `backend-developer`)
- `global_skills/quality-reviewer/` (New/Update: will replace or coexist with `code-reviewer`? Plan is to create new `quality-reviewer` skill based on `114`.)

### 3. Meta Agents (New Skills)
- `global_skills/quality-manager/`
- `global_skills/context-manager/`

## Verification Plan
1.  Run `ls -R ~/.gemini/antigravity/global_skills` to verify 16+ folders (total ~20 skills).
2.  Check `SKILL.md` in `system-architect` to confirm it reflects the new 'Agent 112' content.

