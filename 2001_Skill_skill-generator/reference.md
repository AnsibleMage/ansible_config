# Agent Skills Reference: Anthropic Guidelines

This document contains detailed reference information from Anthropic's official Agent Skills guide. Use this as a comprehensive resource when generating new skills.

## What Are Agent Skills?

**Definition**: Organized folders of instructions, scripts, and resources that agents can discover and load dynamically.

**Purpose**: Transform general-purpose agents into specialized experts for domain-specific tasks.

**Key Characteristics**:
- **Discoverable**: Claude can identify when to use each skill based on metadata
- **Modular**: Self-contained units that can be loaded independently
- **Extensible**: Can include code, documentation, templates, and other resources
- **Dynamic**: Loaded on-demand rather than always present in context

## Core Architecture

### File Structure

```
skill-name/
├── SKILL.md          # Required: Main skill definition
├── reference.md      # Optional: Extended documentation
├── examples.md       # Optional: Code samples and use cases
├── templates/        # Optional: Reusable templates
└── scripts/          # Optional: Executable code
    └── process.py
```

### SKILL.md Anatomy

Every SKILL.md must have two parts:

1. **YAML Frontmatter** (Required)
```yaml
---
name: skill-identifier
description: Brief description for skill discovery
---
```

2. **Markdown Body** (Required)
```markdown
# Skill Title

Instructions, guidelines, and documentation
```

## Progressive Disclosure Principle

**Concept**: Information is revealed in layers, from essential to detailed.

**Implementation Layers**:

1. **Layer 1: Metadata** (Always loaded at startup)
   - `name`: Skill identifier
   - `description`: When to use this skill
   - Purpose: Help Claude decide whether to load the skill

2. **Layer 2: SKILL.md Body** (Loaded when skill is triggered)
   - Detailed instructions
   - Process guidelines
   - Tool usage
   - Examples

3. **Layer 3: Reference Files** (Loaded when explicitly needed)
   - Extended documentation
   - Detailed examples
   - Technical specifications
   - Templates

**Benefits**:
- Faster startup (only metadata loaded initially)
- Reduced context usage (full content loaded only when needed)
- Better organization (complex topics in separate files)

## Metadata Best Practices

### Name Field

**Guidelines**:
- Use lowercase with hyphens (kebab-case)
- Be descriptive but concise
- 2-4 words typically
- Avoid generic terms

**Good Examples**:
- `pdf-form-filler`
- `api-doc-generator`
- `test-scenario-writer`
- `database-migration-helper`

**Poor Examples**:
- `helper` (too generic)
- `PDF_Form_Filler` (wrong case)
- `skill-for-generating-comprehensive-api-documentation` (too long)

### Description Field

**Purpose**: Provide "just enough information for Claude to know when each skill should be used"

**Guidelines**:
- Start with action verb (Generate, Create, Analyze, Process, etc.)
- Clearly state WHAT the skill does
- Indicate WHEN it should be triggered
- Mention key capabilities or constraints
- Keep under 200 characters
- Be specific, not generic

**Template**:
```
[Action verb] [what] for [context]. Supports [key features]. [Important constraints].
```

**Good Examples**:
```yaml
description: Generate comprehensive API documentation from OpenAPI specifications. Supports OpenAPI 2.0 and 3.0 with Markdown and HTML output formats.
```

```yaml
description: Create IEEE 829 compliant test scenarios with 7-step structure (metadata→purpose→preconditions→environment→data→steps→validation). Includes requirement traceability.
```

```yaml
description: Analyze and optimize database query performance. Provides indexing recommendations, query rewrites, and execution plan analysis for PostgreSQL and MySQL.
```

**Poor Examples**:
```yaml
description: Helps with PDFs
# Too vague, doesn't indicate when to use
```

```yaml
description: A comprehensive skill for handling all aspects of document processing including but not limited to PDF files, Word documents, Excel spreadsheets, and various other formats with support for reading, writing, editing, converting, and analyzing content.
# Too long, too broad, lacks focus
```

## Tool Selection Guidelines

### When to Use Code

**Use executable code when**:
- Task is deterministic and algorithmic
- Reliability and consistency are critical
- Performance matters (large data processing)
- Complex logic is involved

**Examples**:
- Sorting and filtering data
- Parsing structured formats (JSON, XML, CSV)
- Mathematical calculations
- Data validation
- Format conversions

### When to Use File Tools

**Read**: Examine existing files
- Before editing files
- Gathering context from documents
- Analyzing file contents

**Write**: Create new files or replace entirely
- Generating new documents
- Creating configuration files
- Complete file replacements

**Edit**: Precise modifications
- Updating specific sections
- Find-and-replace operations
- Incremental changes

### When to Use Bash

**Appropriate for**:
- System operations (file management, directory operations)
- Running external tools and commands
- Build processes and automation
- Git operations

**Avoid for**:
- File content manipulation (use Read/Write/Edit instead)
- Communication with user (output text directly)
- Simple operations better handled by specialized tools

### When to Use Web Tools

**WebFetch**: Retrieve and analyze specific web pages
- Fetching documentation
- Reading API responses
- Accessing specific URLs

**WebSearch**: Find information across the web
- Research tasks
- Finding latest information
- Discovering resources

## Instruction Writing

### Structure Template

```markdown
# [Skill Name]

Brief overview of what this skill does and when to use it.

## Purpose
Clear statement of the skill's goal and scope.

## Process
1. Step-by-step workflow
2. Decision points
3. Error handling

## Tools and Resources
- Which tools to use
- When to use each tool
- How to use them effectively

## Best Practices
- Domain-specific guidelines
- Quality standards
- Common pitfalls

## Examples
Concrete examples demonstrating key workflows

## Output Format
What the skill should produce
```

### Writing Style

**Do**:
- Use clear, direct language
- Be specific and actionable
- Provide concrete examples
- Explain the "why" behind instructions
- Anticipate edge cases
- Include error handling

**Don't**:
- Use vague or ambiguous terms
- Assume prior knowledge without explanation
- Skip important details
- Overload with unnecessary information
- Use jargon without definition

### Example Quality

**Poor instruction**:
```markdown
Read the file and process it appropriately.
```

**Good instruction**:
```markdown
1. Use the Read tool to load the input file
2. Verify the file format matches expectations (check for required fields)
3. If validation fails, explain the issue to the user and ask for clarification
4. Process the data according to the schema defined in reference.md
5. Use the Write tool to save results to the specified output path
```

## Code Integration

### Inline vs. Separate Files

**Inline code** (in SKILL.md):
- Short snippets (< 20 lines)
- Simple examples
- Configuration samples

**Separate files**:
- Complete programs
- Reusable libraries
- Complex logic
- Multiple functions

### Code Documentation

Every script should include:

```python
"""
Purpose: [What this does]
Usage: [How to run it]
Inputs: [What it expects]
Outputs: [What it produces]
Dependencies: [What it needs]
"""
```

### Code Execution Pattern

```markdown
## Data Processing

For deterministic data operations, use the included script:

1. Prepare input data in JSON format
2. Run the processor:
   ```bash
   python scripts/process_data.py input.json output.json
   ```
3. Validate the output meets requirements
4. Report results to the user
```

## Common Patterns

### Pattern 1: Document Processor

```yaml
---
name: document-processor
description: Process and transform documents between formats. Supports PDF, DOCX, Markdown with content extraction and formatting preservation.
---

# Document Processor

Process documents for format conversion and content extraction.

## Supported Formats
- Input: PDF, DOCX, TXT, Markdown
- Output: PDF, DOCX, HTML, Markdown, Plain Text

## Process
1. Read input file with Read tool
2. Detect format and validate structure
3. Extract content using appropriate parser
4. Transform to target format
5. Write output file with Write tool
6. Verify conversion quality

## Error Handling
- Invalid format: Report error and request valid file
- Corrupted file: Explain issue and ask for replacement
- Unsupported conversion: List supported combinations
```

### Pattern 2: Code Generator

```yaml
---
name: code-generator
description: Generate boilerplate code and scaffolding for common patterns. Supports REST APIs, database models, test suites in Python, JavaScript, TypeScript.
---

# Code Generator

Generate production-ready code from templates and specifications.

## Capabilities
- REST API endpoints (Express, FastAPI, Spring Boot)
- Database models (SQLAlchemy, Sequelize, TypeORM)
- Test suites (pytest, Jest, JUnit)
- Configuration files (Docker, CI/CD, linters)

## Process
1. Analyze requirements and select appropriate template
2. Gather necessary parameters (names, types, relationships)
3. Generate code using template engine
4. Add inline documentation and type hints
5. Create companion test file
6. Validate syntax and structure
7. Write files with proper directory structure

## Templates
See templates/ directory for available patterns
```

### Pattern 3: Analyzer

```yaml
---
name: performance-analyzer
description: Analyze application performance issues and provide optimization recommendations. Supports profiling data, database queries, API endpoints, and frontend metrics.
---

# Performance Analyzer

Identify bottlenecks and recommend optimizations.

## Analysis Types
- **Database**: Query plans, indexing, N+1 issues
- **API**: Response times, payload sizes, caching
- **Frontend**: Bundle size, render performance, network requests

## Process
1. Gather performance data (logs, profiles, metrics)
2. Use analysis script to identify patterns
3. Categorize issues by severity and impact
4. Generate recommendations with priority
5. Provide code examples for fixes
6. Estimate improvement potential

## Tools
- Read: Load profiling data
- Bash: Run analysis script
- Write: Generate report
```

## Quality Checklist

Before finalizing any skill, verify:

### Metadata Quality
- [ ] Name follows kebab-case convention
- [ ] Name is descriptive and specific (2-4 words)
- [ ] Description clearly states what and when
- [ ] Description is concise (under 200 chars)
- [ ] Description includes key capabilities

### Content Quality
- [ ] Instructions are clear and actionable
- [ ] Process is step-by-step and logical
- [ ] Tools are appropriate for the task
- [ ] Examples demonstrate key workflows
- [ ] Edge cases are addressed
- [ ] Error handling is included
- [ ] Output format is well-defined

### Structure Quality
- [ ] YAML frontmatter is valid
- [ ] Markdown is properly formatted
- [ ] Sections are logically organized
- [ ] Progressive disclosure is applied
- [ ] No unnecessary duplication
- [ ] References are clear and helpful

### Technical Quality
- [ ] Code is syntactically correct
- [ ] Tool usage follows best practices
- [ ] File paths are handled correctly
- [ ] Dependencies are documented
- [ ] Security considerations addressed

## Advanced Techniques

### Conditional Loading

Structure skills to load additional resources only when needed:

```markdown
## Advanced Features

For complex scenarios involving [specific condition], refer to the detailed guide:
- Read the advanced-patterns.md file for step-by-step instructions
- See examples/complex-scenarios.md for annotated examples
```

### Template Systems

Create reusable templates with placeholders:

```markdown
## Templates

Basic component template:
\`\`\`python
class {{ComponentName}}:
    """{{Description}}"""

    def __init__(self, {{parameters}}):
        {{initialization}}

    def {{main_method}}(self, {{args}}):
        {{implementation}}
\`\`\`

Fill placeholders based on user requirements.
```

### Multi-Stage Workflows

Break complex tasks into phases:

```markdown
## Workflow

### Phase 1: Discovery
1. Analyze requirements
2. Identify components
3. Map dependencies

### Phase 2: Design
1. Select patterns
2. Define interfaces
3. Plan structure

### Phase 3: Generation
1. Create files
2. Add tests
3. Validate

### Phase 4: Review
1. Check quality
2. Run tests
3. Report results
```

## Common Pitfalls

### Pitfall 1: Overly Broad Scope
**Problem**: Skill tries to do too many unrelated things
**Solution**: Split into multiple focused skills

### Pitfall 2: Insufficient Context
**Problem**: Instructions assume knowledge not provided
**Solution**: Include background in reference.md

### Pitfall 3: Poor Tool Choice
**Problem**: Using Bash for file operations instead of specialized tools
**Solution**: Follow tool selection guidelines

### Pitfall 4: Missing Error Handling
**Problem**: No guidance for failure cases
**Solution**: Document error scenarios and responses

### Pitfall 5: Vague Instructions
**Problem**: "Process appropriately" instead of specific steps
**Solution**: Provide explicit, actionable instructions

## Testing Skills

### Manual Testing
1. Create representative test cases
2. Invoke skill with various inputs
3. Verify outputs meet specifications
4. Test edge cases and error conditions
5. Refine based on results

### Validation Criteria
- Does Claude trigger the skill appropriately?
- Are instructions clear and followable?
- Do tools work as expected?
- Are outputs correct and complete?
- Are errors handled gracefully?

## Maintenance

### When to Update Skills
- New tools become available
- Better patterns are discovered
- User feedback indicates issues
- Requirements change
- Performance can be improved

### Versioning
Consider including version info for significant skills:
```yaml
---
name: skill-name
description: Skill description
version: 1.2.0
updated: 2025-01-15
---
```

## Resources

### Official Documentation
- Anthropic Agent Skills Guide: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Claude API Documentation: https://docs.anthropic.com/

### Best Practices
- Start simple, expand as needed
- Test with real-world scenarios
- Iterate based on feedback
- Document rationale for decisions
- Keep security in mind
- Make skills maintainable

### Community
- Share successful patterns
- Learn from others' skills
- Contribute improvements
- Report issues and gaps

---

**Remember**: Great skills are not just well-written instructions—they are thoughtfully designed systems that empower Claude to excel at specialized tasks. Every element should serve the goal of enabling excellent performance on domain-specific work.
