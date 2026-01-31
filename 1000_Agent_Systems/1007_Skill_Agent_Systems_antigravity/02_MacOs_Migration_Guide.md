# Antigravity macOS Migration & Integration Guide (V4.1)

> [!IMPORTANT]
> This guide is specifically for **macOS (Apple Silicon/Intel)** environment. For Windows configuration, please refer to `03_Windows_Configuration_Reference.md`.

## Overview
This document outlines the steps to fully integrate the Antigravity Agent System (V4.1) with Obsidian on macOS. It converts the Windows-based "Junction" architecture into macOS standard "Symbolic Links".

---

## 1. System Requirements & Paths

| Component | Windows Path (Legacy) | **macOS Path (Target)** |
| :--- | :--- | :--- |
| **System Root** | `C:\Users\name\.gemini` | `~/.gemini` (`/Users/changjaeyou/.gemini`) |
| **Obsidian Vault** | `D:\Obsidian Vault` | `~/Documents/Obsidian-Vault` |
| **Link Method** | `mklink /J` | `ln -s` |

---

## 2. Migration Steps (Execute in Terminal)

### Step 1: Initialize Global Directory
Ensure the base Antigravity directory exists.

```zsh
# Create .gemini directory if it doesn't exist
mkdir -p ~/.gemini/antigravity
```

### Step 2: Link System Configuration (GEMINI.md)
Connect the `GEMINI.md` file in Obsidian to the system root. This allow you to edit the agent's brain directly from Obsidian.

```zsh
# Backup existing config if needed
mv ~/.gemini/GEMINI.md ~/.gemini/GEMINI.md.bak 2>/dev/null

# Create Symlink (Target -> Source)
# Note: Adjust the Vault path if yours is different
ln -s "/Users/changjaeyou/Documents/Obsidian-Vault/00_Antigravity_Brain/Config/GEMINI.md" ~/.gemini/GEMINI.md
```

### Step 3: Link "Brain" (Artifacts)
Connect the agent's output directory (`brain`) to Obsidian so artifacts appear in your vault automatically.

```zsh
# Remove existing folder in Obsidian if it's just a folder (WARNING: Check contents first)
# rm -rf "/Users/changjaeyou/Documents/Obsidian-Vault/00_Antigravity_Brain/Brain"

# Link Agent Brain -> Obsidian Folder
ln -s ~/.gemini/antigravity/brain "/Users/changjaeyou/Documents/Obsidian-Vault/00_Antigravity_Brain/Brain"
```

### Step 4: Link "Projects"
Context injection. Allow the agent to see project specific rules defined in Obsidian.

```zsh
# Link Obsidian Projects -> Agent Projects
ln -s "/Users/changjaeyou/Documents/Obsidian-Vault/00_Antigravity_Brain/Projects" ~/.gemini/antigravity/projects
```

---

## 3. Verification

Run the following command to verify the links are established correctly (arrows `->` indicate successful links).

```zsh
ls -l ~/.gemini/GEMINI.md
ls -ld ~/.gemini/antigravity/projects
# Should output: ... -> /Users/changjaeyou/Documents/Obsidian-Vault/...
```

---

## 4. Updates in V4.1 (Mac Optimized)
- **Path Resolution**: All paths in `GEMINI.md` are now absolute macOS paths (`/Users/changjaeyou/...`).
- **Obsidian Deep Integration**: Task boundaries and artifacts now sync bidirectionally.
