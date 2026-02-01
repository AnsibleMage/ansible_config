# CLAUDE.md - Claude Code Integrated Guidelines V3.0

> Version: 3.0 | Updated: 2026-02-01
> Based on: V2.3 + English-first system with Korean user support

---

## ⚡ Dynamic Chain Orchestration (PRIORITY 1 - Execute First)

> **This protocol executes first for every user prompt received.**

### Step 1: 4-Layer Prompt Analysis

Analyze user prompts through 4 linguistic layers (translation-specialist method):

| Layer | Analysis | Extracted Info |
|-------|----------|----------------|
| **Lexical** | Keywords, domain terms, field identification | Agent/skill candidates |
| **Syntactic** | Sentence structure, command/question/request type | Task type (dev/analysis/doc) |
| **Discourse** | Context, previous conversation, background | Chain complexity level |
| **Pragmatic** | Actual intent, expected result, implicit needs | Final output form |

### Step 2: Chain Selection/Generation

```
┌─────────────────────────────────────────────────────────────┐
│  4-Layer Analysis Complete                                  │
│     ↓                                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Primary: Match Existing Chain                       │   │
│  │     Select from 9 chains (A~I)                       │   │
│  │     → Execute immediately if matched                 │   │
│  └─────────────────────────────────────────────────────┘   │
│     ↓ No match or partial match                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Secondary: Dynamic Chain Generation                 │   │
│  │     - Select from agent pool + skill pool            │   │
│  │     - Determine sequential/parallel/hybrid pattern   │   │
│  │     - Auto-assign model (opus/sonnet)                │   │
│  │     → Generate and execute custom chain              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Chain Execution

**Pre-execution Declaration** (Announce chain to user in Korean):
```
📋 체인 구성: [Chain name or "동적 생성"]
   → step1[model] → step2[model] → step3[model]
```

### Dynamic Chain Generation Rules

#### Agent + Skill Hybrid Allowed
```
Agent[O/S] → Skill[-] → Agent[O/S] → Skill[-]
```

#### Auto Model Assignment
- **Agents**: Use model value from mapping table
- **Skills (/)**: Use main session model [-]

#### Execution Pattern Decision
| Condition | Pattern |
|-----------|---------|
| Next step needs previous result | Sequential (→) |
| Independent tasks | Parallel (∥) |
| Complex dependencies | Hybrid ((A∥B)→C) |

### Simple Task Exception

Skip chain generation for:
- Simple Q&A
- One-line code fix
- File read/search only
- Explicit "간단히/briefly" request

---

## 🎯 Core Working Principles

### PARALLEL-FIRST Principle
- **Before Work**: Define problem, declare scope, **analyze dependencies**
- **During Work**: **Parallel** for independent, **sequential** for dependent tasks
- **After Work**: Integrate results, review, fix errors

### TODO Management (Task System Integration)
1. Create TODO list → `TaskCreate` (mark **parallel-ready** items)
2. Parallel tasks → **simultaneous** `in_progress`, use `run_in_background`
3. Check off **immediately** upon completion (no waiting)
4. **Integrated verification** after all complete

### CLEAR Framework
- **C**oncise: Brief and focused (CLI optimized)
- **L**ogical: Logical flow (**optimal sequential/parallel selection**)
- **E**xplicit: Clear and explicit
- **A**daptive: Flexible adaptation
- **R**eflective: Reflective improvement

### 4-Stage Thinking Process (Parallel Optimized)
1. **Recognize clearly** - Understand requirements accurately
2. **(Explore solutions ∥ Analyze risks)** - Parallel alternatives + constraints
3. **Select optimal method** - Integrate step 2 results for best decision
4. **Verify results** - Predict and validate

### Language Principles
- **Output/Reports**: Korean (한국어)
- **Code/Technical terms**: English acceptable
- **File/Variable names**: Keep original

---

## 🗺️ Skill Auto-Mapping Protocol

### Auto-activate agents/skills when keywords detected

> **Model Assignment**: Use `model` parameter value for subagent calls
> **Skills (/)**: Use main session model (cannot specify separately)

#### 📊 Thinking & Analysis

| Keyword Pattern (KO/EN) | Tool | Model | Priority |
|-------------------------|------|-------|----------|
| 번역, translation, 다국어, multilingual | `/translation-specialist` | - | HIGH |
| 분석, analysis, 다차원, multidimensional, 시스템 사고, systems thinking | `multidimensional_analyst` | **opus** | HIGH |
| 인사이트, insight, 패턴, pattern, 관찰, observation | `insight_explorer` | sonnet | MEDIUM |
| 연결, connection, 관계, relationship, 은유, metaphor | `connection_creator` | sonnet | MEDIUM |
| 문제 재정의, reframe, 관점 전환, perspective shift | `problem_reframer` | **opus** | HIGH |
| 솔루션, solution, 혁신, innovation, 아이디어, idea, 창의, creative | `solution_innovator` | **opus** | HIGH |
| 심화, deepen, 질문, question, Why, What-If | `insight_amplifier` | sonnet | MEDIUM |
| 학습, learning, 지식 격차, knowledge gap, 메타인지, metacognition | `learning_evolver` | sonnet | MEDIUM |
| 복잡성, complexity, 분해, decompose, 시스템 해체, breakdown | `complexity_resolver` | **opus** | HIGH |
| 의사결정, decision, 판단, judgment, 균형, balance | `balanced_judge` | **opus** | HIGH |
| 통합, integration, 지혜, wisdom, 윤리, ethics, 종합, synthesis | `integrated_sage` | **opus** | MEDIUM |

#### 💻 Development & Architecture

| Keyword Pattern (KO/EN) | Tool | Model | Priority |
|-------------------------|------|-------|----------|
| 요구사항, requirements, 비즈니스 분석, business analysis | `requirements_analyst` | **opus** | HIGH |
| 설계, design, 아키텍처, architecture, Clean, SOLID | `system_architect` | **opus** | HIGH |
| 개발, develop, 코드, code, TDD, 구현, implement | `code_developer` | sonnet | HIGH |
| 프론트엔드, frontend, UI, 인터페이스, interface | `/frontend-design` | - | HIGH |
| React, 아티팩트, artifact, shadcn | `/web-artifacts-builder` | - | HIGH |
| 테스트, test, Playwright, 자동화, automation | `/webapp-testing` | - | HIGH |
| MCP, 서버, server, 프로토콜, protocol | `/mcp-builder` | - | MEDIUM |

#### ✅ Quality & Verification

| Keyword Pattern (KO/EN) | Tool | Model | Priority |
|-------------------------|------|-------|----------|
| 리뷰, review, 코드 검토, code review, 품질, quality | `quality_reviewer` | sonnet | HIGH |
| 품질 관리, quality management, 검증, verification, 프로세스, process | `quality_manager` | sonnet | MEDIUM |

#### 📄 Document & Data

| Keyword Pattern (KO/EN) | Tool | Model | Priority |
|-------------------------|------|-------|----------|
| Word, docx, 문서, document | `/docx` | - | HIGH |
| PDF, pdf, 추출, extract | `/pdf` | - | HIGH |
| PowerPoint, pptx, 프레젠테이션, presentation, 슬라이드, slide | `/pptx` | - | HIGH |
| Excel, xlsx, 스프레드시트, spreadsheet | `/xlsx` | - | HIGH |
| 협업 문서, collaborative doc, 공동 작성, co-authoring | `/doc-coauthoring` | - | MEDIUM |

#### 🎨 Design & Visual

| Keyword Pattern (KO/EN) | Tool | Model | Priority |
|-------------------------|------|-------|----------|
| 알고리즘 아트, algorithmic art, p5.js, 제너레이티브, generative | `/algorithmic-art` | - | MEDIUM |
| 브랜드, brand, Anthropic 스타일, Anthropic style | `/brand-guidelines` | - | MEDIUM |
| 시각 디자인, visual design, 캔버스, canvas, 포스터, poster | `/canvas-design` | - | HIGH |
| 테마, theme, 스타일, style, 팔레트, palette | `/theme-factory` | - | MEDIUM |
| GIF, Slack, 애니메이션, animation | `/slack-gif-creator` | - | LOW |

#### 🔧 Support & Management

| Keyword Pattern (KO/EN) | Tool | Model | Priority |
|-------------------------|------|-------|----------|
| 문맥, context, 컨텍스트, 전달, handoff | `context_manager` | sonnet | LOW |
| 스킬 생성, skill creation, 스킬 만들기, create skill | `/skill-creator` | - | MEDIUM |
| 내부 커뮤니케이션, internal comms, 보고서, report | `/internal-comms` | - | LOW |
| 키바인딩, keybinding, 단축키, shortcut | `/keybindings-help` | - | LOW |

#### 📝 Obsidian Specific

| Keyword Pattern (KO/EN) | Tool | Model | Priority |
|-------------------------|------|-------|----------|
| 링크 수정, fix links, 양방향 링크, bidirectional links | `link-doctor` | sonnet | MEDIUM |
| 인덱스, index, 폴더 목록, folder list | `doc-indexer` | sonnet | MEDIUM |
| 지식 맵, knowledge map, 연결 분석, connection analysis | `knowledge-mapper` | sonnet | MEDIUM |
| 회의록, meeting notes, 미팅 노트 | `meeting-note-wizard` | sonnet | MEDIUM |
| 작업 로그, work log, 워크로그, worklog | `worklog-analyzer` | sonnet | MEDIUM |
| 프로젝트 대시보드, project dashboard | `project-dashboard` | sonnet | MEDIUM |
| 세션 메모, session memo | `session-memo-writer` | sonnet | LOW |

#### 🔍 Exploration

| Keyword Pattern (KO/EN) | Tool | Model | Priority |
|-------------------------|------|-------|----------|
| 코드베이스 탐색, explore codebase, 파일 검색, file search | `Explore` | sonnet | HIGH |
| 계획, plan, 전략 설계, strategy design, 구현 계획, implementation plan | `Plan` | **opus** | HIGH |
| 다목적 검색, general search, 복잡한 조사, complex research | `general-purpose` | sonnet | MEDIUM |

---

## 🤖 Agent System

### Agent Classification (with Model Assignment)

> **Call Example**: `Task(subagent_type: "system_architect", model: "opus", prompt: "...")`

#### 🧠 Cognitive Agents
| Agent | subagent_type | Model | Role |
|-------|---------------|-------|------|
| Insight Explorer | `insight_explorer` | sonnet | Deep observation, pattern recognition, creative connections |
| Multidimensional Analyst | `multidimensional_analyst` | **opus** | Multi-dimensional analysis (time/space/abstract/causal/scale) |
| Connection Creator | `connection_creator` | sonnet | Connect concepts, construct metaphors |
| Problem Reframer | `problem_reframer` | **opus** | Redefine problems, shift perspectives |
| Solution Innovator | `solution_innovator` | **opus** | Generate/evaluate innovative solutions |
| Insight Amplifier | `insight_amplifier` | sonnet | Deepen insights (5 Whys, What If) |
| Learning Evolver | `learning_evolver` | sonnet | Learning strategy, knowledge gap analysis |
| Complexity Resolver | `complexity_resolver` | **opus** | Decompose complex systems, optimize sequence |
| Balanced Judge | `balanced_judge` | **opus** | Systematic analysis, pattern-based judgment |
| Integrated Sage | `integrated_sage` | **opus** | Holistic judgment, ethical considerations |

#### 💼 Role Agents
| Agent | subagent_type | Model | Role |
|-------|---------------|-------|------|
| Requirements Analyst | `requirements_analyst` | **opus** | Requirements analysis, business logic |
| System Architect | `system_architect` | **opus** | Clean Architecture, SOLID, Mermaid diagrams |
| Code Developer | `code_developer` | sonnet | TDD, DRY, declarative coding |
| Quality Reviewer | `quality_reviewer` | sonnet | Test coverage, code quality, security |

#### ⚙️ Management Agents
| Agent | subagent_type | Model | Role |
|-------|---------------|-------|------|
| Quality Manager | `quality_manager` | sonnet | Global principle compliance, quality metrics |
| Context Manager | `context_manager` | sonnet | Context management between agents |

#### 🔍 Exploration Agents
| Agent | subagent_type | Model | Role |
|-------|---------------|-------|------|
| Explore | `Explore` | sonnet | Fast codebase exploration |
| Plan | `Plan` | **opus** | Implementation strategy design |
| General Purpose | `general-purpose` | sonnet | Multi-purpose research and search |

---

## 🔗 Dynamic Chain Patterns (9) - Parallel Optimized

> **Model Notation**: [O] = opus, [S] = sonnet, [-] = main session model
> **Pattern Notation**: → = sequential, ∥ = parallel

### A. DevChain (Development Execution)
**Trigger**: 코드 개발, code development, API 설계, API design, 시스템 구현, system implementation
```
requirements_analyst[O] → (system_architect[O] ∥ Explore[S]) → code_developer[S] → quality_reviewer[S]
```
*Architecture design and codebase exploration run in parallel*

### B. ThinkChain (Deep Thinking)
**Trigger**: 복잡한 분석, complex analysis, 다차원적 관점, multi-perspective, 창의적 솔루션, creative solution
```
(insight_explorer[S] ∥ connection_creator[S]) → multidimensional_analyst[O] → integrated_sage[O]
```
*Initial insight collection parallelized*

### C. FastTrack (Rapid Resolution)
**Trigger**: 버그 수정, bug fix, 긴급 문제, urgent issue
```
(complexity_resolver[O] ∥ Explore[S]) → code_developer[S] → quality_reviewer[S]
```
*Problem analysis and code exploration run in parallel*

### D. LearnChain (Learning & Research)
**Trigger**: 새 기술 학습, learn new tech, 지식 격차, knowledge gap
```
learning_evolver[S] → (multidimensional_analyst[O] ∥ insight_explorer[S]) → insight_amplifier[S]
```

### E. DecisionChain (Decision Making)
**Trigger**: 복잡한 의사결정, complex decision, 리스크 평가, risk assessment
```
problem_reframer[O] → (multidimensional_analyst[O] ∥ balanced_judge[O]) → integrated_sage[O]
```

### F. DocChain (Document Processing)
**Trigger**: 문서 생성, create document, 문서 편집, edit document, 변환, convert
```
Identify document type → /docx[-] | /pdf[-] | /pptx[-] | /xlsx[-] → [optional] quality_reviewer[S]
```

### G. DesignChain (Design)
**Trigger**: 시각 디자인, visual design, 브랜딩, branding, UI
```
[optional] /brand-guidelines[-] → (/canvas-design[-] ∥ /theme-factory[-]) | /algorithmic-art[-] | /frontend-design[-]
```
*Design and theme work can run in parallel*

### H. WebDevChain (Web Development)
**Trigger**: 웹 아티팩트, web artifact, 프론트엔드, frontend, 웹앱 테스트, webapp testing
```
requirements_analyst[O] → (system_architect[O] ∥ Explore[S]) → /frontend-design[-] | /web-artifacts-builder[-] → /webapp-testing[-] → quality_reviewer[S]
```

### I. CollabChain (Collaborative Document)
**Trigger**: 긴 형식 문서, long-form document, 반복 협업, iterative collaboration
```
/doc-coauthoring[-] (3 stages) → /docx[-] | /pdf[-] | /pptx[-]
```

---

## 📦 Memory System

### Principle
All session prompts and results must be **recorded as files**.

### Rules
1. Create `.memory` folder at the root of the open directory
2. **(Check folder ∥ List existing files)** - parallel execution
3. Determine next sequence number and write document
4. Save file

### Document Structure
```markdown
# [Task Title]

## 사용자 프롬프트
> [Original user prompt]

## 메타 정보
- **작성일**: YYYY-MM-DD
- **요약**: [1-2 sentence summary in Korean]
- **시사점**: [Key insights in Korean]

## 내용
[Detailed work content and results in Korean]
```

### File Naming Convention
```
[sequence]_[keyword]_[date].md
Example: 001_system_prompt_analysis_20260201.md
```

### Execution Process (Parallel Optimized)
```
1. (Check folder exists ∥ Query existing file list) → 2. Determine sequence + Write document → 3. Save
```

---

## 🔄 Execution Patterns

### Sequential
```
A → B → C
```
- **Condition**: B needs A's result, dependency exists
- **Example**: `requirements_analyst → system_architect → code_developer`

### Parallel
```
A ∥ B ∥ C
```
- **Condition**: Independent tasks, time optimization
- **Example**: `insight_explorer ∥ connection_creator ∥ solution_innovator`

### Hybrid
```
(A ∥ B) → C → (D ∥ E)
```
- **Condition**: Complex dependencies
- **Example**: `(insight_explorer ∥ connection_creator) → integrated_sage → quality_reviewer`

---

## 📋 Complexity-Based Strategy

| Complexity | Strategy | Example |
|------------|----------|---------|
| **Simple** | Direct handling | "Python syntax question" |
| **Medium** | Single agent/skill | "API design principles" |
| **Complex** | Multi-agent chain | "Enterprise platform development" |

---

## ✅ Work Checklist (Parallel Optimized)

### Before Work
- [ ] Confirm PARALLEL-FIRST principle
- [ ] **Dependency analysis**: Classify independent vs sequential-required tasks
- [ ] Create TODO list for complex tasks (`TaskCreate`, mark parallel-ready)
- [ ] Select appropriate skills/agents via keyword mapping
- [ ] Decide execution pattern (sequential/parallel/hybrid)

### During Work
- [ ] **Execute independent tasks in parallel** (use `run_in_background`)
- [ ] Wait sequentially only for dependent tasks
- [ ] **Immediately** update TODO upon each completion (`TaskUpdate`)
- [ ] Follow CLEAR framework
- [ ] Record intermediate outputs immediately
- [ ] Maintain context between agents

### After Work
- [ ] **Integrate results** and review
- [ ] Confirm TODO completion
- [ ] Quality verification (use `quality_reviewer` if needed)

---

## 📝 Change History

### V3.0 (2026-02-01)
- ✅ **English-first system with Korean user support**
  - System prompts in English for better Claude Code recognition
  - Trigger keywords in Korean + English (bilingual)
  - Output rules maintain Korean for user-facing content
- ✅ All sections converted to English
- ✅ Keyword mapping tables expanded with bilingual triggers

### V2.3 (2026-02-01)
- ✅ **Parallel execution optimization (PARALLEL-FIRST)**
  - STEP-BY-STEP → PARALLEL-FIRST principle change
  - 5-Stage → 4-Stage Thinking (2∥3 parallelized)
  - CLEAR Framework: "logical order" → "logical flow"
- ✅ **Chain patterns with parallel sections**
  - DevChain: (architect ∥ Explore)
  - ThinkChain: (insight_explorer ∥ connection_creator)
  - FastTrack: (complexity ∥ Explore)
  - DesignChain: (canvas-design ∥ theme-factory)
- ✅ TODO Management parallel support
- ✅ Memory System parallelized

### V2.2 (2026-02-01)
- ✅ Dynamic Chain Orchestration System (PRIORITY 1)
- ✅ 4-Layer prompt analysis
- ✅ Agent + Skill hybrid chain support

### V2.1 (2026-02-01)
- ✅ Per-subagent model assignment system
- ✅ Model column added to all mapping tables

### V2.0 (2026-02-01)
- ✅ GEMINI 5.1 practical elements integrated
- ✅ 36 keyword → skill auto-mapping
- ✅ 9 chain patterns
- ✅ Memory System introduced

### V1.0 (Previous)
- Initial CLAUDE.md setup
- STEP-BY-STEP, TODO, CLEAR framework
- 16 agents, 5 chain patterns

---

*Claude Code Integrated Guidelines V3.0 - English-First System with Korean User Support*
