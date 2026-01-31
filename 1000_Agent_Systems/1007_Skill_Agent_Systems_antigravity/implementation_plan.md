# Obsidian & Antigravity Context Integration Plan

This plan details the steps to fully integrate Antigravity's configuration and project management with Obsidian, implementing the "Contextual Integration" phase.

## Goal
To enable the user to manage Antigravity's global configuration (`GEMINI.md`) and project-specific rules directly from Obsidian, while maintaining the system's required file structure via Windows Junctions.

## User Review Required
> [!IMPORTANT]
> This operation involves moving the critical `GEMINI.md` file and creating system-level links. While safe, please ensure no other Antigravity processes are running during this update.

## Proposed Changes

### 1. Configuration Migration (`GEMINI.md`)
- **Move**: `C:\Users\name\.gemini\GEMINI.md` -> `C:\Users\name\Documents\Obsidian Vault\00_Antigravity_Brain\Config\GEMINI.md`
- **Link**: Create a Symbolic Link (or Hardlink) at `C:\Users\name\.gemini\GEMINI.md` pointing to the new location in Obsidian.
    - *Note*: `GEMINI.md` is a file, so `mklink` (symbolic link) or `mklink /H` (hardlink) will be used, not `/J` (junction, which is for directories). Hardlink is preferred for single files to avoid some application compatibility issues, but symbolic link is more visible. I will use a **Symbolic Link** for clarity.

### 2. Project Rules Integration (`projects` folder)
- **Create**: `C:\Users\name\.gemini\antigravity\projects` (System side)
- **Create**: `C:\Users\name\Documents\Obsidian Vault\00_Antigravity_Brain\Projects` (User side)
- **Link**: Create a Junction `C:\Users\name\.gemini\antigravity\projects` -> `C:\Users\name\Documents\Obsidian Vault\00_Antigravity_Brain\Projects`.
    - This allows the agent to access `C:\Users\name\.gemini\antigravity\projects\ProjectA\rules.md` which physically resides in Obsidian.

### 3. Configuration Update (`GEMINI.md`)
- **Update**: Modify `GEMINI.md` to include a new rule about checking the `projects` folder for context.
    - Add a section: `## 📂 Project Context Protocol`
    - Instruction: "Before starting work, check if a folder matching the current project name exists in `.../projects/`. If yes, read `rules.md` or `requirements.md` in that folder."

## Verification Plan

### Automated Verification
1. **File Existence**: Verify `GEMINI.md` exists in both new (Obsidian) and old (System, as link) locations.
2. **Link Functionality**: Modify the file in Obsidian and verify the change is reflected in `.gemini`.
3. **Project Context**: Create a dummy project folder and rule file in Obsidian, then have the agent try to read it via the system path.

### Manual Verification
- User opens Obsidian and sees `00_Antigravity_Brain/Config/GEMINI.md`.
- User edits the file and confirms Antigravity accepts the new settings.
