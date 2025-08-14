---
project: claude-orchestrate
type: workflow
title: "Required Reading List - Claude Orchestrator/Guardian"
version: 2025-08-14
status: CURRENT
summary:
  - Streamlined mandatory reading for session startup
  - Essential documents only
  - Clear understanding checklist
tags: [session-startup, mandatory-reading, workflow]
---

# Required Reading List - Claude Orchestrator/Guardian

## 📚 MANDATORY DOCUMENTS (Read in Order)

These documents MUST be read at the start of every session:

### 1. Core Rules & Standards
- **[CLAUDE.md](../CLAUDE.md)** - Core interaction rules and hierarchy of authority ⭐ **READ FIRST**
- **[docs/conventions.md](conventions.md)** - Project standards, naming conventions, and file organization

### 2. Current Session Context
- **[docs/status/handover-next.md](status/handover-next.md)** - Previous session's state and immediate next steps
- **[docs/status/users-todos.md](status/users-todos.md)** - Master TODO list with user priorities

### 3. Project Understanding
- **[docs/design/vision.md](design/vision.md)** - Project goals and strategic direction (with breakthrough updates)
- **[docs/technical/architecture.md](technical/architecture.md)** - How components fit together (claude-orchestrator + guardian)
- **[claude-orchestrator/__proposed_refactoring/WHY.md](../claude-orchestrator/__proposed_refactoring/WHY.md)** - Deep problem analysis and why current approach exists

## 📋 Session Startup Checklist

Before starting any work, confirm understanding of:

### System Architecture
- [ ] **Parallel development**: claude-orchestrator (stable) + guardian (evolving)
- [ ] **Breakthrough solution**: `run_in_background=True` enables parallel Claude agents
- [ ] **No background daemon**: Commands execute directly through Claude
- [ ] **File-based coordination**: Agents communicate through status files

### Project Understanding
- [ ] **Core problems**: Context overflow, rule drift, documentation chaos, bug marathons
- [ ] **Breakthrough impact**: How parallel execution changes everything
- [ ] **Current capabilities**: What works now vs what's planned
- [ ] **Pain points**: Why current approach is necessary (from WHY.md)

### Implementation Status
- [ ] **Working systems**: claude-orchestrator/ (proven) and guardian/ (next-gen)
- [ ] **Documentation location**: docs/ folder organization
- [ ] **Session management**: docs/status/ for handovers and TODOs
- [ ] **Templates & resources**: claude-orchestrator/resource-library/

### Current Capabilities
- [ ] **What works**: Parallel orchestration, visual monitoring, context sharing
- [ ] **Key limitations**: Task tool blocks, some tools need file-based workarounds
- [ ] **Next priorities**: Guardian system maturation and migration strategy

## ⚠️ Critical Session Rules

### Documentation Discipline
- **DO NOT** create new documentation unless explicitly requested
- **ALWAYS** check existing files before creating new ones
- **PREFER** editing existing files over creating duplicates
- **FOLLOW** kebab-case naming convention for all new files

### Development Approach
- **TEST** simple implementations before adding complexity
- **USE** working orchestrator-tools/ for stable functionality
- **EXPERIMENT** in guardian/ for next-generation features
- **PRESERVE** working functionality during migration

### Key Project Reminders
- **Orchestrator works through Claude commands** - NOT separate terminals
- **Each project has complete orchestrator copy** - Self-contained system
- **File references must be verified** - Many breakthroughs happened quickly
- **Breakthrough documentation is in __proposed_refactoring/** - Extract key findings

## 📖 Context-Specific Reading

**The handover document may specify additional reading based on planned work:**
- Specific breakthrough documents from `__proposed_refactoring/`
- Implementation guides for current development focus
- Test evidence for validation needs

Check the "Session-Specific Reading" section in [handover-next.md](status/handover-next.md).

## 🎯 Understanding Validation

**Before proceeding with work, you should be able to answer:**
1. What is the current session priority from users-todos.md?
2. What breakthrough enables parallel Claude execution?
3. Where are the working implementations located?
4. What is the difference between claude-orchestrator and guardian?
5. What are the core problems this project solves (from vision.md)?
6. Why is the current mixed approach necessary (from WHY.md)?
7. What file naming convention should be used?

---
*This streamlined list ensures efficient session startup with essential knowledge only.*
*For complete project navigation, see [documentation-index.md](documentation-index.md)*