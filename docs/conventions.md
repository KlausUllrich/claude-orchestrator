# Project Conventions - Claude Orchestrator/Guardian

## 📝 File Naming Standards

### Primary Convention: kebab-case
- **Files**: `my-document.md`, `session-handover.md`, `user-guide.md`
- **Folders**: `short-term-memory/`, `long-term-memory/`, `resource-library/`
- **Commands**: `/session-start`, `/token-usage`, `/create-handover`

### Exception Cases
- **Config files**: May use standard conventions (`.gitignore`, `package.json`)
- **Legacy files**: Keep existing names until natural migration opportunity
- **System files**: Follow platform conventions

## 📁 Directory Structure Standards

### Documentation Organization
```
docs/
├── conventions.md           # This file - project standards
├── read-first.md           # Mandatory session reading list
├── design/                 # Vision, specifications, UX design
├── technical/             # Architecture, implementation details
├── status/                # Session handovers, TODOs, progress
└── workflow/              # Process documentation
```

### Tool Structure (Both claude-orchestrator & guardian)
```
<tool-name>/
├── README.md              # Tool overview and quick start
├── brain/                 # Core logic and orchestration
├── short-term-memory/     # Session state (SQLite)
├── long-term-memory/      # Persistent knowledge
├── resource-library/      # Templates and reusable components
├── tools/                 # Utilities and helpers
└── workflows/             # Project-type specific rules
```

## 🏷️ Document Types & Headers

### Mandatory Front Matter (YAML)
```yaml
---
project: claude-orchestrate
type: [vision|technical|status|workflow|convention]
title: "Document Title"
version: YYYY-MM-DD HH:MM
status: [CURRENT|DRAFT|ARCHIVED|DEPRECATED]
summary:
  - Key point 1
  - Key point 2
tags: [relevant, keywords, here]
---
```

### Document Type Standards
- **vision**: Project goals, roadmap, strategic decisions
- **technical**: Architecture, implementation, code documentation
- **status**: Session handovers, progress reports, current state
- **workflow**: Process documentation, how-to guides
- **convention**: Standards, rules, project guidelines

## 🔄 Session Management Standards

### Required Reading Order
1. `CLAUDE.md` - Core interaction rules (FIRST)
2. `docs/conventions.md` - This document
3. `docs/read-first.md` - Session checklist
4. `docs/status/handover-next.md` - Previous session state
5. `docs/status/users-todos.md` - Current priorities

### Handover Document Standards
- **Filename**: `handover-YYYY-MM-DD-HHMM.md`
- **Location**: `docs/status/`
- **Always update**: `handover-next.md` (symlink or copy of latest)

## 🚀 Project Evolution Standards

### Parallel Development Phases
- **claude-orchestrator/**: Current working system (stable)
- **guardian/**: Next generation system (active development)
- **Migration strategy**: Gradual transition, preserve working functionality

### Document Relevance Indicators
- **🟢 CURRENT**: Actively maintained, up-to-date
- **🟡 EVOLVING**: Valid but being improved/replaced
- **🔴 DEPRECATED**: Keep for reference, don't use for new work
- **📁 ARCHIVED**: Historical value only

### Breakthrough Documentation
- **Location**: `__proposed_refactoring/` (temporary workspace)
- **Migration**: Extract key findings to permanent docs
- **Cleanup**: Archive or remove when superseded

## 💡 Code & Command Standards

### Python Scripts
- **Location**: `<tool>/brain/` for core logic
- **Naming**: `snake_case.py`
- **Entry points**: Clear, documented main functions

### Shell Commands
- **User commands**: `/kebab-case` format
- **Internal scripts**: `kebab_case.sh`
- **Documentation**: Help text in all commands

### Rule System Standards
- **Location**: `claude-orchestrator/brain/rules/` (YAML files)
- **Principle**: Single Source of Truth - never duplicate rules in code
- **Structure**: All rule files follow standard YAML format:
```yaml
priority: critical|high|medium|low
description: What this rule set does
rules:
  - List of rules
  - Another rule
```

### Rule System Architecture
- ❌ **Don't**: Hardcode rules in hooks or agents
- ❌ **Don't**: Copy rules into multiple locations
- ✅ **Do**: Always read from YAML files in brain/rules/
- ✅ **Do**: Use RuleEnforcer class to load rules consistently

### Rule Usage Example
```python
from brain.rule_enforcer import RuleEnforcer

# Loads all rules from brain/rules/ folder
enforcer = RuleEnforcer()

# Check naming convention (reads naming.yaml)
is_valid = enforcer.check_naming("my-file.md")
```

## 📋 Quality Standards

### Before Session End
- [ ] Update `handover-next.md`
- [ ] Verify all new files follow conventions
- [ ] Update relevant status documents
- [ ] Mark deprecated content clearly

### Documentation Maintenance
- **Review cycle**: Each major milestone
- **Cleanup rule**: Remove outdated content, don't accumulate
- **Single source of truth**: Avoid duplicate information

---
*This document defines the standards for the entire project ecosystem.*
*Update this file when establishing new conventions.*
*Version: 2025-08-14*