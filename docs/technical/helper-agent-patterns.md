---
project: claude-orchestrate
type: technical
title: "Helper Agent Patterns and Implementation"
version: 2025-08-14
status: CURRENT
summary:
  - Claude agents primed with markdown instructions
  - Specialized helper agent directory structures
  - Instruction patterns and examples
  - Request-response and hook-based coordination patterns
tags: [helper-agents, claude-agents, markdown, patterns, specialization]
---

# Helper Agent Patterns and Implementation

## Core Concept

Helper agents are **Claude instances** that read markdown files containing their specialized instructions, rules, and templates. They coordinate with the main agent through MCP messaging to provide specialized assistance.

## Helper Agent Structure

### Standard Directory Layout
```
guardian/helper-agents/
├── convention-enforcer/
│   ├── instructions.md          # Agent role and behavior
│   ├── naming-rules.md          # Specific rules to enforce
│   ├── file-organization.md     # Directory structure standards
│   ├── examples/               # Good/bad examples
│   │   ├── good-examples.md
│   │   └── violations.md
│   └── .claude/settings.json   # MCP configuration
│
├── workflow-monitor/
│   ├── instructions.md          # Agent role and behavior
│   ├── game-dev-process.md      # Development workflow steps
│   ├── quality-gates.md         # When to intervene
│   ├── checklist-templates.md   # Validation checklists
│   └── .claude/settings.json
│
└── documentation-maintainer/
    ├── instructions.md          # Agent role and behavior
    ├── doc-templates.md         # Documentation templates
    ├── update-patterns.md       # How to keep docs current
    ├── style-guide.md           # Writing standards
    └── .claude/settings.json
```

## Instruction File Patterns

### Base Instructions Template
```markdown
# [Agent Type] Agent Instructions

You are a specialized helper agent for [specific domain].

## Your Role
- [Primary responsibility]
- [Secondary responsibilities]
- [Interaction patterns]

## Your Resources
1. Read `[resource-file-1].md` for [specific guidance]
2. Read `[resource-file-2].md` for [specific rules]
3. Check `examples/` for [reference patterns]

## How to Help
1. When asked about [topic], check [specific rules]
2. Provide [type] of feedback
3. Suggest [type] of corrections
4. Reference the source of your guidance

## Response Format
- [Structured response pattern]
- [Required information to include]
- [Reference format]

## Coordination
- Register with MCP using agent_id: "[agent-name]"
- Check messages regularly with check_messages tool
- Send responses using send_message tool to main agent
```

### Convention Enforcer Example
```markdown
# Convention Enforcer Agent Instructions

You are a specialized helper agent that enforces project conventions and standards.

## Your Role
- Monitor file naming and organization
- Check against project standards in your resource files
- Provide specific feedback on violations
- Suggest corrections based on established rules

## Your Resources
1. Read `naming-rules.md` for file naming conventions
2. Read `file-organization.md` for directory structure requirements
3. Check `examples/` for good/bad patterns and common violations

## How to Help
1. When asked about a file/directory name, check naming-rules.md
2. When asked about file placement, check file-organization.md
3. Provide specific violations found with rule references
4. Suggest exact corrections with explanations
5. Reference the specific rule that was violated

## Response Format
**Violation Found**: [Specific issue description]
**Rule Violated**: [Reference to rule file and section]
**Suggested Fix**: [Exact correction to make]
**Explanation**: [Why this rule exists]

## Coordination
- Register with MCP using agent_id: "convention-enforcer"
- Check messages when notified by background monitor
- Send detailed analysis back to requesting agent
- Include file path and specific violation details in responses
```

## Resource File Patterns

### Naming Rules Example (`naming-rules.md`)
```markdown
# Project Naming Conventions

## File Naming Standards

### General Rules
- **Format**: kebab-case for all files
- **Pattern**: `descriptive-name.extension`
- **Examples**: `session-manager.py`, `helper-agent.md`, `test-results.json`

### Specific File Types

#### Python Scripts
- **Format**: `module-name.py`
- **Good**: `context-guardian.py`, `rule-enforcer.py`
- **Bad**: `ContextGuardian.py`, `rule_enforcer.py`, `ruleEnforcer.py`

#### Documentation
- **Format**: `topic-description.md`
- **Good**: `architecture.md`, `user-guide.md`, `api-reference.md`
- **Bad**: `Architecture.md`, `userGuide.md`, `API_Reference.md`

#### Configuration
- **Format**: `purpose-config.extension`
- **Good**: `mcp-settings.json`, `database-config.yaml`
- **Bad**: `settings.json`, `config.yaml`, `dbConfig.json`

## Directory Naming Standards

### General Rules
- **Format**: kebab-case for all directories
- **Pattern**: `purpose-description/`
- **Examples**: `helper-agents/`, `mcp-server/`, `test-results/`

### Specific Directories
- **Components**: `component-name/` (e.g., `convention-enforcer/`)
- **Utilities**: `utility-type/` (e.g., `background-monitors/`)
- **Documentation**: `content-type/` (e.g., `technical-docs/`)

## Common Violations

### Filename Issues
- **CamelCase**: `MyScript.py` → `my-script.py`
- **snake_case**: `my_script.py` → `my-script.py`
- **Spaces**: `my script.py` → `my-script.py`
- **Generic names**: `script.py` → `specific-purpose.py`

### Directory Issues
- **CamelCase**: `MyAgents/` → `my-agents/`
- **snake_case**: `helper_agents/` → `helper-agents/`
- **Generic names**: `utils/` → `specific-utilities/`
```

### File Organization Example (`file-organization.md`)
```markdown
# Project File Organization Standards

## Directory Structure Requirements

### Helper Agent Organization
```
guardian/helper-agents/[agent-name]/
├── instructions.md              # REQUIRED - Agent behavior
├── [domain]-rules.md           # REQUIRED - Specific rules
├── examples/                   # RECOMMENDED - Reference patterns
└── .claude/settings.json       # REQUIRED - MCP configuration
```

### Documentation Organization  
```
docs/
├── technical/                  # Implementation details
├── design/                     # Vision and specifications
├── status/                     # Session handovers, progress
└── workflow/                   # Process documentation
```

### Code Organization
```
guardian/
├── mcp-server/                 # Central coordination
├── helper-agents/              # Specialized Claude agents
├── utils/                      # Background monitoring tools
├── tests/                      # Test environments
└── wezterm-integration/        # Terminal setup
```

## Placement Rules

### By File Type
- **Agent instructions**: Always in `helper-agents/[agent-name]/instructions.md`
- **Specialized rules**: In agent directory with descriptive names
- **Examples**: In `examples/` subdirectory within agent directory
- **MCP config**: Always `.claude/settings.json` in agent directory

### By Content Type
- **Permanent documentation**: `docs/` hierarchy
- **Temporary status**: `docs/status/` with timestamps
- **Implementation code**: Appropriate component directory
- **Test setups**: `tests/` with descriptive names

## Common Organization Issues

### Misplaced Files
- **Rules in wrong location**: Rules belong in specific agent directories
- **Mixed concerns**: Agent-specific content mixed with general docs
- **Unclear hierarchy**: Files in root instead of appropriate subdirectories

### Poor Directory Structure
- **Flat organization**: Everything in one directory
- **Unclear purpose**: Directory names don't indicate contents
- **Mixed abstractions**: Different levels of detail in same directory
```

## Coordination Patterns

### Phase 1: Request-Response Pattern

#### Main Agent Request
```
Main Agent workflow:
1. Encounters decision point (e.g., creating new file)
2. Sends request to appropriate helper agent via MCP
3. Continues other work while waiting
4. Receives helper response via background notification
5. Acts on helper's guidance
```

#### Helper Agent Response
```
Helper Agent workflow:
1. Receives notification of new message
2. Uses check_messages tool to read request
3. Reads relevant resource files for guidance
4. Analyzes request against rules/standards
5. Sends structured response via send_message tool
```

#### Example Exchange
```
Main Agent → Convention Enforcer:
"I'm creating a new session management script. 
Proposed name: SessionManager.py
Path: guardian/brain/SessionManager.py"

Convention Enforcer → Main Agent:
"**Violation Found**: Filename uses CamelCase instead of kebab-case
**Rule Violated**: naming-rules.md section 'Python Scripts'
**Suggested Fix**: session-manager.py
**Path Issue**: File should be in guardian/utils/ not guardian/brain/
**Explanation**: Scripts are utilities, brain/ is for core logic classes"
```

### Phase 2: Hook-Based Pattern (Future)

#### Automatic Assignment
```
File Creation Hook workflow:
1. Main agent creates/modifies file
2. Orchestrator detects file system change
3. Orchestrator determines appropriate helper agent
4. Orchestrator spawns helper with file context
5. Helper validates file against all relevant rules
6. Helper reports findings to orchestrator
7. Orchestrator routes feedback to main agent
```

## Helper Agent Types

### Convention Enforcer
- **Domain**: File naming, directory organization, code standards
- **Resources**: naming-rules.md, file-organization.md, style-guide.md
- **Triggers**: File creation, directory changes, code structure questions

### Workflow Monitor  
- **Domain**: Development processes, quality gates, milestone validation
- **Resources**: workflow-steps.md, quality-gates.md, process-checklists.md
- **Triggers**: Phase transitions, milestone completion, process questions

### Documentation Maintainer
- **Domain**: Documentation accuracy, consistency, completeness
- **Resources**: doc-templates.md, style-guide.md, update-patterns.md
- **Triggers**: Code changes, architecture decisions, documentation requests

### Requirements Validator
- **Domain**: Feature completeness, acceptance criteria, scope management
- **Resources**: requirements-list.md, acceptance-criteria.md, scope-definitions.md
- **Triggers**: Feature implementation, scope changes, validation requests

## Implementation Guidelines

### Creating New Helper Agent
1. **Create directory**: `guardian/helper-agents/[agent-name]/`
2. **Write instructions.md**: Based on template with specific domain
3. **Create resource files**: Domain-specific rules and guidance
4. **Add examples**: Good/bad patterns for reference
5. **Configure MCP**: `.claude/settings.json` with server connection
6. **Test coordination**: Verify request-response pattern works

### Testing Helper Agent
1. **Launch agent**: In WezTerm pane with MCP configuration
2. **Register agent**: Use register_agent tool with appropriate ID
3. **Send test request**: From main agent via MCP messaging
4. **Verify response**: Check helper provides structured, useful feedback
5. **Validate references**: Ensure helper cites correct resource files

---

*This document defines patterns for creating specialized Claude helper agents. For MCP coordination details, see [mcp-server-details.md](mcp-server-details.md).*