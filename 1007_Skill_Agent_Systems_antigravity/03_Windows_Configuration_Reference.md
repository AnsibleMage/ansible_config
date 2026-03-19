# Antigravity Windows Configuration Reference

This document preserves the configuration details for the Windows environment of the Antigravity System. It is intended for reference when migrating to macOS or for maintaining Windows-based backups.

---

## 1. Directory Structure (Windows)

- **Root Config Path**: `C:\Users\%USERNAME%\.gemini`
- **Global Skills Path**: `C:\Users\%USERNAME%\.gemini\antigravity\global_skills`
- **Obsidian Vault**: `D:\Obsidian Vault` (or user defined)

## 2. Command Reference

### Linking Folders (Junction)
On Windows, use `mklink /J` to create directory junctions (symlinks).

```cmd
:: Link .gemini brain to Obsidian
mklink /J "D:\Obsidian Vault\00_Antigravity_Brain" "C:\Users\%USERNAME%\.gemini\antigravity\brain"

:: Link Projects
mklink /J "C:\Users\%USERNAME%\.gemini\antigravity\projects" "D:\Obsidian Vault\00_Antigravity_Brain\Projects"
```

### Linking Files (Hardlink)
On Windows, use `mklink /H` for hard links (or `mklink` for symlinks).

```cmd
:: Link GEMINI.md
mklink /H "C:\Users\%USERNAME%\.gemini\GEMINI.md" "D:\Obsidian Vault\00_Antigravity_Brain\Config\GEMINI.md"
```

## 3. Path Formatting

- **Separator**: Backslash (`\`)
- **Absolute Path Example**: `C:\Users\changjaeyou\.gemini\antigravity\global_skills\multidimensional-analyst\SKILL.md`

## 4. Legacy V4.0 Header
The Windows configuration was based on V4.0.

```markdown
# GEMINI.md - 안티그래비티 (Antigravity) 글로벌 설정 V4.0
...
- **스킬 경로**: `C:\Users\%USERNAME%\.gemini\antigravity\global_skills\`
```
