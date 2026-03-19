# Deletion of Reserved 'nul' File

I have successfully deleted the file named `nul` from your Obsidian Vault.

## Problem
The file name `nul` is a reserved device name in Windows (referring to the null device). Standard file deletion commands like `del nul` or `Remove-Item nul` fail because the operating system interprets `nul` as the device, not a file on the disk.

## Solution
I used the Windows UNC path syntax `\\?\` to bypass the reserved name check and access the file system directly.

### Commands Executed
1. **Verification**: Checked file existence using `dir`.
2. **Deletion**:
   ```cmd
   cmd /c del "\\?\C:\Users\name\Documents\Obsidian Vault\nul"
   ```
   (Note: PowerShell's `Remove-Item` encountered issues even with the prefix, so `cmd.exe` was used for reliable deletion.)
3. **Validation**: Confirmed that the file is no longer present in the directory.

## Result
The `nul` file has been permanently removed.

## Deletion of 'nul' File in Trash

The user requested to delete another `nul` file located in the `.trash` directory.

### Path
`C:\Users\name\Documents\Obsidian Vault\.trash\5200_biokorea_secretariat_web_build\5270_테스트\5271_사용자\nul`

### Process
The same UNC path method was applied:
```cmd
cmd /c del "\\?\C:\Users\name\Documents\Obsidian Vault\.trash\5200_biokorea_secretariat_web_build\5270_테스트\5271_사용자\nul"
```

### Result
The file was successfully deleted.

## Obsidian & Antigravity Physical Integration

To integrate Antigravity's "Brain" (execution logs and artifacts) with Obsidian's "Vault" (knowledge base), I implemented a **Physical Integration** strategy.

### Implemented Solution
I created a Windows **Directory Junction** (Symlink) that maps the global Antigravity brain directory into the Obsidian Vault.

- **Source**: `C:\Users\name\.gemini\antigravity\brain` (Antigravity's storage)
- **Target**: `C:\Users\name\Documents\Obsidian Vault\00_Antigravity_Brain` (Obsidian folder)

### Command Executed
```cmd
mklink /J "C:\Users\name\Documents\Obsidian Vault\00_Antigravity_Brain" "C:\Users\name\.gemini\antigravity\brain"
```

### Benefit
- You can now browse all Antigravity logs, `task.md`, `walkthrough.md`, and other artifacts directly from Obsidian.
- All future conversations and tasks will automatically appear in the `00_Antigravity_Brain` folder.

## Obsidian & Antigravity Contextual Integration

To enable Obsidian to act as the "Command Center" for Antigravity's configuration and project rules, I implemented a **Contextual Integration** strategy.

### 1. Configuration Link (`GEMINI.md`)
I created a **Hardlink** for the global configuration file.
- **System**: `C:\Users\name\.gemini\GEMINI.md` (Original)
- **Obsidian**: `C:\Users\name\Documents\Obsidian Vault\00_Antigravity_Brain\Config\GEMINI.md` (Editable Mirror)
- **Effect**: Updating `GEMINI.md` in Obsidian instantly updates the system configuration.

### 2. Project Rules Link (`Projects` Folder)
I created a **Junction** for project-specific rules.
- **System**: `C:\Users\name\.gemini\antigravity\projects` (Agent's reading path)
- **Obsidian**: `C:\Users\name\Documents\Obsidian Vault\00_Antigravity_Brain\Projects` (User's writing path)

### 3. Protocol Update
I updated `GEMINI.md` with a new protocol:
> "Before starting work, check `antigravity/projects/[ProjectName]/rules.md` for context."

### How to Use
1. **Global Rules**: Edit `00_Antigravity_Brain/Config/GEMINI.md` in Obsidian.
2. **Project Rules**: Create `00_Antigravity_Brain/Projects/[MyProject]/rules.md` in Obsidian. When you ask me to work on `[MyProject]`, I will automatically read that file first.

---

## MacOS Migration & V4.1 Update (2026-01-29)

Migrated the Antigravity system configuration from Windows to macOS environment and updated to V4.1.

### Changes Made
1.  **Documentation Split**:
    - `02_MacOs_Migration_Guide.md`: Updated with strictly macOS-compatible commands (`ln -s`, `/Users/changjaeyou/...`) and confirmed verification steps.
    - `03_Windows_Configuration_Reference.md`: Created to archive the legacy Windows paths (`mklink`, `C:\...`) for reference.
2.  **Configuration Sync**:
    - Updated `GEMINI.md` in the `1007` folder to match the active V4.1 configuration in `.gemini`.
    - Confirmed bidirectional sync between Obsidian and System settings.

### Verification
- Confirmed `02_MacOs_Migration_Guide.md` contains valid zsh commands.
- Confirmed `GEMINI.md` (V4.1) is identical in both `1007` and `.gemini`.
