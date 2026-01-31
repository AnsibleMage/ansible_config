# 🤖 MIGRATION GUIDE FOR ANTIGRAVITY AGENT (Windows Protocol)

**TO: Antigravity Agent (Windows Instance)**
**FROM: Antigravity Agent (Mac Master Instance)**
**SUBJECT: System Synchronization and V3.0 Cognitive Engine Deployment**

Welcome, colleague. This document contains the necessary instructions to replicate the **Antigravity V3.0 Cognitive Orchestration System** on this Windows environment. You are expected to read and execute these steps autonomously.

---

## 🏗️ 1. Infrastructure Setup

First, ensure the target directories exist. On Windows, Gemini usually resides in the user's home directory.

**Target Path Detection:**
If `%USERPROFILE%\.gemini` does not exist, create it.
The internal Antigravity path should be: `%USERPROFILE%\.gemini\antigravity`

**Action:**
1. Create `%USERPROFILE%\.gemini\antigravity\global_skills`
2. Create `%USERPROFILE%\.gemini\antigravity\memory`

---

## ⚙️ 2. Configuration Deployment (The Soul)

The file `00_Config_GEMINI_Global_Setting.md` (or `GEMINI.md` in this folder) is our **V3.0 Kernel**. It contains the 5-Stage Thinking, STEP-BY-STEP, and Dynamic Chain logic.

**Action:**
- Copy `./doc/00_Config_GEMINI_Global_Setting.md` to `%USERPROFILE%\.gemini\GEMINI.md`
- *Override if exists.*

---

## 🧠 3. Skill Integration (The Muscles)

We are deploying a library of 20+ specialized skills that provide our multi-agent capabilities.

**Action:**
- Copy all sub-folders from `./global_skills/` to `%USERPROFILE%\.gemini\antigravity/global_skills/`
- Ensure each folder contains a `SKILL.md` file.

---

## 💾 4. Memory Restoration (The Past)

To ensure continuity of the "AnsibleMage" project context, you must adopt the current memory log.

**Action:**
- Copy `./memory/context_log.json` to `%USERPROFILE%\.gemini\antigravity\memory\context_log.json`

---

## 🚀 5. Activation Sequence

Once the files are in place, perform a **Self-Diagnostic**:

1. **Verify V3.0 Loop**: Check if your internal instructions now include "Perceive-Plan-Act-Verify-Memorize".
2. **Verify Triggers**: Test if keywords like "deep analysis" or "requirements" correctly trigger the `insight-explorer` or `requirements-analyst`.
3. **Verify Memory**: Read the `context_log.json` and confirm you are aware of the "AnsibleMage Migration" history.

---

## ⚠️ Windows Specific Notes
- Use `copy` or `xcopy` equivalent for directory copies.
- Path separators should be handled correctly by your shell environment (usually handled automatically by agent tools).
- Ensure file permissions allow reading and writing to the `.gemini` folder.

**End of Protocol.**
**Antigravity System V3.0 Ready for Deployment.**
