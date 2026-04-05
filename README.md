# ansible_config

Configuration ontology for Claude Code -- agents, skills, chains, hooks, memory systems, and orchestration patterns evolved across 12 iterative design phases.

## Overview

This repository documents the full evolution of a Claude Code orchestration system, from basic agent definitions to a compound AI system with vector memory, 4-layer prompt analysis, and dynamic chain orchestration. Each top-level directory represents a distinct design phase, preserving the research, decisions, and artifacts that shaped the current system.

The active production configuration lives in `~/.claude/` and is backed up / versioned here for reproducibility and collaboration.

## Key Features

- **28 Specialized Agents** -- cognitive agents (insight, analysis, reframing), role agents (architect, developer, reviewer), evaluation agents (grader, comparator, security-reviewer), and Obsidian utility agents (8)
- **54+ Skills** -- document processing (docx/pdf/pptx/xlsx), design (canvas, themes, brand), web development (frontend, testing, artifacts), Rails 8 vibe-coding, translation, and more
- **10 Dynamic Chain Patterns** (A-J) -- SystemDesignChain, DevChain, ResearchChain, MetaThinkChain, HotfixChain, WebDevChain+, GameDevChain, DocChain+, RailsDevChain, AutomationChain
- **4-Layer Prompt Analyzer** -- Lexical, Syntactic, Discourse, Pragmatic analysis with false-positive prevention and confidence scoring
- **Vector Memory System** -- Qdrant-backed semantic memory with auto-indexing, chunked vectorization, and cosine-similarity recall
- **Hook System** -- UserPromptSubmit auto-analysis + correction detection, PostToolUse formatting + plan review trigger, PreToolUse security checks, Stop debug residue detection, memory auto-indexing
- **Verification Loop** -- `{× MAX 3}` retry with auto-fix on 6 chains, residual reporting on exhaustion
- **Pre-Mortem Gate** -- "If a senior engineer reviewed this plan, what holes would they find?" forced before Gate 2 approval
- **L1/L2 Mistake Cache** -- lessons-learned.md (always loaded, MAX 100) + vector-recalled feedback memory
- **Agent Teams** -- parallel execution with Lead/Teammate architecture, resilience protocol, and hybrid chain integration

## Project Structure

```
ansible_config/
|
|-- 1001_Agent_Systems_Basic/          # Phase 1: Basic agent definitions (35 agents)
|   |-- agents/                        #   System, Dev, Domain, Product agents
|   +-- CLAUDE.md                      #   Meta-agent orchestration guidelines
|
|-- 1002_Agent_Systems_Engine/         # Phase 2: Engine-level agent system
|   |-- agents/                        #   Refined agent definitions
|   +-- CLAUDE.md                      #   Enhanced orchestration rules
|
|-- 1003_Agent_Systems_Thinking/       # Phase 3: Thinking-oriented agents
|   |-- agents/                        #   Cognitive agent focus
|   +-- CLAUDE_THINK.md                #   Thinking process guidelines
|
|-- 1004_Skill_Agent_Systems_*/        # Phase 4: Skill system introduction
|   |-- global_skills/                 #   First skill definitions
|   +-- memory/                        #   Early memory system
|
|-- 1005-1008_Skill_Agent_Systems_*/   # Phases 5-8: Skill iterations
|                                      #   Gemini integration, cross-platform migration
|
|-- 1009_Agent_Systems_Compound/       # Phase 9: Compound AI system (353 files)
|   |-- agents/                        #   24 agents (cognitive + role + management)
|   |-- skills/                        #   17 skill packages
|   |-- commands/                      #   13 slash commands
|   |-- hooks/                         #   Auto-analysis & memory hooks
|   |-- scripts/                       #   prompt_analyzer.py (4-Layer)
|   |-- templates/                     #   Rails 8 templates
|   +-- CLAUDE.md                      #   V3.6 integrated guidelines
|
|-- 1010_Claude_Code_System_Evolution/ # Phase 10: System evolution research
|   +-- 001-009_*.md                   #   Chain upgrades, memory solutions, masterplan
|
|-- 1011_Claude_Code_Team_Composition/ # Phase 11: Agent Teams integration
|   |-- doc/                           #   Team analysis & test reports
|   |-- INSTALL-MAC/                   #   macOS installation configs
|   |-- INSTALL-WIN/                   #   Windows installation configs
|   +-- CLAUDE.md                      #   V4.2.1 with Teams resilience
|
+-- 1012_Claude_Code_Ontology_System_/ # Phase 12: Ontology & modularization (1202 files)
    |-- 101_doc_current_system_analysis/   # Current system analysis
    |-- 102_doc_future_system_research/    # Future system research
    |-- 103_doc_/                          # Improvement planning (C1-C8)
    |-- 104_current_system/                # V4.2.1 system backup
    +-- 105_claude_code_system_package/    # V5.1 production package
        |-- agents/        # 20 agents (14 core + 6 evaluation)
        |-- skills/        # 27 skills (merged commands + skills)
        |-- hooks/         # Production hook scripts
        |-- scripts/       # Prompt analyzer, memory indexer
        |-- rules/         # Modularized rules (orchestration + memory)
        |-- eval/          # Evaluation framework
        +-- workflow/      # research -> plan -> implement templates
|
+-- 1013_Claude_Code_Harness/         # Phase 13: Boris 7 tips & harness research
    |-- 01_*                              # 7 best practices (Boris + hackathon winner)
    |-- 02_*                              # Tip #2+#5 implementation guide
    |-- 03_*                              # Tip #7 hook automation guide
    |-- 04_*                              # Self-evaluation bias analysis (theory + deep)
    |-- 05_*                              # V5.1.0 vs vanilla 5-dimensional analysis
    +-- 06_*                              # Tip #3 plan mode (Pre-Mortem + independent review)
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| AI Platform | Claude Code (Opus model) |
| Vector DB | Qdrant (Docker, localhost:6333) |
| Embedding | `intfloat/multilingual-e5-large` (1024-dim) |
| Runtime | Python 3.11+ (venv) |
| Hooks | Bash + Python (UserPromptSubmit, PostToolUse, PreToolUse) |
| MCP Server | prompt-analyzer (4-Layer analysis) |
| Document Processing | python-docx, reportlab, python-pptx, openpyxl |
| Deployment | Kamal 2 (Rails 8 projects) |
| Version Control | Git + GitHub |

## Installation

This repository is a configuration archive. To deploy the active system:

```bash
# Clone the repository
git clone https://github.com/AnsibleMage/ansible_config.git

# The production-ready package is in:
# 1012_Claude_Code_Ontology_System_/105_claude_code_system_package/

# Copy to ~/.claude/ (the active Claude Code config directory)
cp -r 1012_Claude_Code_Ontology_System_/105_claude_code_system_package/* ~/.claude/

# Install Python dependencies (for prompt analyzer & memory system)
cd ~/.claude && python3 -m venv mcp-env
source mcp-env/bin/activate
pip install qdrant-client sentence-transformers

# Start Qdrant (Docker required)
docker run -d -p 6333:6333 qdrant/qdrant

# Register the MCP prompt analyzer
claude mcp add prompt-analyzer ~/.claude/mcp-env/bin/python3.12 -- ~/.claude/scripts/prompt_analyzer_mcp.py
```

For detailed installation instructions, see:
- `1009_Agent_Systems_Compound/INSTALL_GUIDE.md`
- `1012_Claude_Code_Ontology_System_/105_claude_code_system_package/INSTALL_GUIDE.md`

## Version History

| Version | Phase | Key Changes |
|---------|-------|-------------|
| V1.0 | 1001 | Basic 35-agent system with meta-orchestration |
| V2.0 | 1002-1003 | Engine-level agents, thinking process integration |
| V3.0 | 1004-1008 | Skill system, Gemini integration, cross-platform support |
| V3.6 | 1009 | Compound system -- 24 agents, 17 skills, 11 chains, MCP analyzer |
| V4.2.1 | 1010-1011 | System evolution, Agent Teams with resilience protocol |
| V5.1.0 | 1012 | Ontology system, CLAUDE.md modularization, evaluation framework |
| V5.2.0 | 1013 | Boris 7 tips, Pre-Mortem gate, verification loop, bias countermeasures, Obsidian CLI agents |

## License

[MIT](LICENSE)
