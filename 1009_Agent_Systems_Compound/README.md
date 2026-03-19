# 🎵 Claude Code Agent Systems Compound

> A comprehensive collection of AI agents, skills, and orchestration systems for Claude Code

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Opus%204.5-blueviolet)](https://claude.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.2-blue)](CLAUDE.md)

## Overview

This repository contains a complete ecosystem for enhancing Claude Code capabilities:

- **24 Specialized Agents** for cognitive tasks, development, and management
- **17 Skills** for document processing, design, testing, and more
- **9 Dynamic Chain Patterns** for complex workflow orchestration
- **MCP Prompt Analyzer** for automatic 4-Layer prompt analysis
- **Integrated Guidelines** (CLAUDE.md) for consistent AI behavior

Built and maintained by **🎵 Ari (AI)** and **🔧 An (Human)**.

## Structure

```
1009_Agent_Systems_Compound/
├── 📋 CLAUDE.md                    # Main guidelines (English)
├── 📋 CLAUDE_KO.md                 # Guidelines (Korean)
├── 📄 001-008_*.md                 # Analysis & configuration docs
├── 📄 Boris-Cherny-Workflow-Guide.md
│
├── 🤖 agents/                      # 24 Agent definitions
│   ├── 101-110_*.md               # Cognitive agents
│   ├── 111-116_*.md               # Role & management agents
│   └── *.md                       # Obsidian-specific agents
│
└── 🛠️ skills/                      # 17 Skill packages
    ├── docx/                      # Word document processing
    ├── pdf/                       # PDF manipulation
    ├── pptx/                      # PowerPoint creation
    ├── xlsx/                      # Excel processing
    ├── frontend-design/           # UI/UX design
    ├── webapp-testing/            # Playwright testing
    ├── canvas-design/             # Visual art creation
    ├── theme-factory/             # Theme generation
    └── ...                        # And more
```

## What's New in V3.2

### MCP Prompt Analyzer

Automatic 4-Layer prompt analysis with the `prompt-analyzer` MCP server:

```bash
# Install
claude mcp add prompt-analyzer ~/.claude/mcp-env/bin/python3.12 -- ~/.claude/scripts/prompt_analyzer_mcp.py

# Verify
claude mcp list
# Output: prompt-analyzer: ✓ Connected
```

**Auto-detection capabilities:**

| Pattern | Detection Example | Auto-Recommendation |
|---------|-------------------|---------------------|
| **Translation** | "~version", "make in Korean" | `/translation-specialist` (HIGH) |
| **Document** | "Word", "pdf", "pptx" | `/docx`, `/pdf`, `/pptx` |
| **Development** | "design", "develop", "TDD" | `system_architect`, `code_developer` |
| **Analysis** | "analyze", "multidimensional" | `multidimensional_analyst` |
| **Design** | "UI", "frontend", "poster" | `/frontend-design`, `/canvas-design` |

### New Slash Commands

| Command | Function |
|---------|----------|
| `/analyze` | 4-Layer prompt analysis |
| `/readme-gen` | Auto-generate README files |

## Key Components

### 🧠 Cognitive Agents (10)

| Agent | Purpose | Model |
|-------|---------|-------|
| Insight Explorer | Pattern recognition, creative connections | sonnet |
| Multidimensional Analyst | Multi-angle analysis (time/space/causal) | **opus** |
| Connection Creator | Concept linking, metaphor construction | sonnet |
| Problem Reframer | Perspective shifts, problem redefinition | **opus** |
| Solution Innovator | Creative solution generation | **opus** |
| Insight Amplifier | 5 Whys, What-If deepening | sonnet |
| Learning Evolver | Knowledge gap analysis, learning strategies | sonnet |
| Complexity Resolver | System decomposition, sequencing | **opus** |
| Balanced Judge | Systematic analysis, pattern-based judgment | **opus** |
| Integrated Sage | Holistic judgment, ethical considerations | **opus** |

### 💼 Role Agents (4)

| Agent | Purpose | Model |
|-------|---------|-------|
| Requirements Analyst | Business requirements, logic mapping | **opus** |
| System Architect | Clean Architecture, SOLID, diagrams | **opus** |
| Code Developer | TDD, DRY, declarative coding | sonnet |
| Quality Reviewer | Test coverage, security, performance | sonnet |

### 🛠️ Skills (17)

| Category | Skills |
|----------|--------|
| **Documents** | `/docx`, `/pdf`, `/pptx`, `/xlsx`, `/doc-coauthoring` |
| **Design** | `/canvas-design`, `/frontend-design`, `/theme-factory`, `/algorithmic-art` |
| **Development** | `/webapp-testing`, `/web-artifacts-builder`, `/mcp-builder` |
| **Utility** | `/translation-specialist`, `/brand-guidelines`, `/slack-gif-creator`, `/skill-creator`, `/internal-comms` |

### 🔗 Chain Patterns (9)

| Chain | Trigger | Pattern |
|-------|---------|---------|
| DevChain | Code development | `analyst → (architect ∥ explore) → developer → reviewer` |
| ThinkChain | Complex analysis | `(explorer ∥ creator) → analyst → sage` |
| FastTrack | Bug fixes | `(resolver ∥ explore) → developer → reviewer` |
| LearnChain | Learning tasks | `evolver → (analyst ∥ explorer) → amplifier` |
| DecisionChain | Decisions | `reframer → (analyst ∥ judge) → sage` |
| DocChain | Documents | `identify → /docx\|pdf\|pptx\|xlsx → reviewer` |
| DesignChain | Visual design | `guidelines → (canvas ∥ theme) → frontend` |
| WebDevChain | Web development | `analyst → architect → frontend → testing → reviewer` |
| CollabChain | Collaborative docs | `/doc-coauthoring → /docx\|pdf\|pptx` |

## Quick Start

### 1. Copy CLAUDE.md to your Claude Code config

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md
```

### 2. Install MCP Prompt Analyzer (optional but recommended)

```bash
# Create Python venv
/opt/homebrew/bin/python3.12 -m venv ~/.claude/mcp-env
~/.claude/mcp-env/bin/pip install mcp

# Register MCP server
claude mcp add prompt-analyzer ~/.claude/mcp-env/bin/python3.12 -- ~/.claude/scripts/prompt_analyzer_mcp.py
```

### 3. Use agents via Task tool

```typescript
Task(
  subagent_type: "system_architect",
  model: "opus",
  prompt: "Design a REST API for user authentication..."
)
```

### 4. Use skills with slash commands

```
/docx Create a project proposal document
/pdf Extract text from uploaded.pdf
/frontend-design Create a dashboard UI
/analyze What agent should I use for this task?
```

## Configuration

See `007_Claude-Code-Settings-Configuration.md` for:
- Pre-allowed permissions (52 commands)
- PostToolUse hooks (auto-formatting)
- Custom slash commands (6 commands)
- Security settings

See `008_MCP-Prompt-Analyzer-Server.md` for:
- MCP server installation
- 4-Layer analysis details
- Keyword mapping database

## Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](CLAUDE.md) | Main integrated guidelines (English) |
| [CLAUDE_KO.md](CLAUDE_KO.md) | Korean version |
| [001_Claude-Code-Available-Tools.md](001_Claude-Code-Available-Tools.md) | Tool inventory |
| [004_Dynamic-Chain-Orchestration-System.md](004_Dynamic-Chain-Orchestration-System.md) | Chain system details |
| [007_Claude-Code-Settings-Configuration.md](007_Claude-Code-Settings-Configuration.md) | Settings guide |
| [008_MCP-Prompt-Analyzer-Server.md](008_MCP-Prompt-Analyzer-Server.md) | MCP analyzer guide |
| [Boris-Cherny-Workflow-Guide.md](Boris-Cherny-Workflow-Guide.md) | Workflow optimization tips |

## Related Projects

- [ansible_config](https://github.com/AnsibleMage/ansible_config) - Parent configuration repository
- [ansible_projects](https://github.com/AnsibleMage/ansible_projects) - Project implementations

## License

MIT License - See individual skill folders for specific licenses.

---

*Built with 🎵 by Ari & An | Claude Code Agent Systems v3.2*
