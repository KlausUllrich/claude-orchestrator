---
project: claude-orchestrate
type: workflow
title: "Required Reading List - Claude Orchestrator/Guardian"
version: 2025-08-14-restructured
status: CURRENT
summary:
  - Streamlined mandatory reading for session startup
  - Essential documents with restructured technical documentation
  - Clear understanding checklist with current priorities
tags: [session-startup, mandatory-reading, workflow, restructured]
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

### 3. System Architecture Overview
- **[docs/technical/architecture.md](technical/architecture.md)** - **RESTRUCTURED** Core system overview, current status, next steps ⭐ **KEY DOCUMENT**
- **[docs/technical/implementation-status.md](technical/implementation-status.md)** - Current development state, test results, priorities

### 4. Deep Understanding (If Working on Specific Areas)
- **[docs/technical/helper-agent-patterns.md](technical/helper-agent-patterns.md)** - If working on helper agents
- **[docs/technical/mcp-server-details.md](technical/mcp-server-details.md)** - If working on MCP server
- **[docs/technical/migration-strategy.md](technical/migration-strategy.md)** - If working on migration
- **[docs/technical/system-flows.md](technical/system-flows.md)** - If working on coordination patterns

## 📋 Session Startup Checklist

Before starting any work, confirm understanding of:

### Current Development State ✅
- [ ] **Foundation Status**: MCP server working, non-blocking communication proven (Test 2 success)
- [ ] **Active Priority**: Creating first helper agent (convention-enforcer)
- [ ] **Working Tools**: claude-orchestrator/ continues to work during transition
- [ ] **Next Milestone**: Helper agent framework proven effective

### System Architecture Understanding ✅
- [ ] **Dual-track development**: claude-orchestrator/ (working) + guardian/ (evolving)
- [ ] **Helper agent approach**: Claude instances + markdown instructions (NOT Python classes)
- [ ] **Coordination**: MCP server + background monitoring for non-blocking communication
- [ ] **Phase 1 pattern**: Request-response between main agent and helpers

### Project Structure Clarity ✅
- [ ] **guardian/**: Working MCP foundation, ready for helper agents
- [ ] **claude-orchestrator/**: Preserved working tools (/session-start, /session-end)
- [ ] **docs/technical/**: Restructured with specialized documents
- [ ] **Current working directory**: `/home/klaus/game-projects/claude-orchestrate/guardian/`

### Implementation Priorities ✅
- [ ] **Immediate task**: Create convention-enforcer helper agent with markdown instructions
- [ ] **Test goal**: Validate request-response pattern between main and helper
- [ ] **Success criteria**: Helper provides useful guidance based on markdown rules
- [ ] **Key achievement**: First working Claude helper agent

## ⚠️ Critical Session Rules

### Documentation Discipline
- **DO NOT** create new documentation unless explicitly requested
- **ALWAYS** check existing files before creating new ones
- **USE** restructured technical docs for implementation details
- **FOLLOW** kebab-case naming convention for all new files

### Development Approach
- **FOCUS** on helper agent creation as current priority
- **USE** working guardian/ MCP foundation
- **TEST** request-response patterns with real Claude agents
- **PRESERVE** working claude-orchestrator/ functionality

### Key Project Reminders
- **Helper agents are Claude instances** reading markdown instructions
- **MCP server provides coordination** (already working and proven)
- **Non-blocking communication works** (Test 2 success validates approach)
- **Phase 1 is request-response** (main agent asks helper for specialized assistance)

## 📖 Context-Specific Reading

**Based on current session priorities, also read:**

### For Helper Agent Development (Current Priority)
- **[helper-agent-patterns.md](technical/helper-agent-patterns.md)** - Structure, instructions, examples
- **[system-flows.md](technical/system-flows.md)** - Request-response coordination patterns
- Working example: `guardian/tests/test2-output-reading/` (Test 2 success)

### For MCP Server Work
- **[mcp-server-details.md](technical/mcp-server-details.md)** - Implementation, database schema, tools
- Working implementation: `guardian/mcp-server/`

### For Migration Planning
- **[migration-strategy.md](technical/migration-strategy.md)** - Detailed phases and tools
- **[implementation-status.md](technical/implementation-status.md)** - Current state assessment

## 🎯 Understanding Validation

**Before proceeding with work, you should be able to answer:**
1. What is the current session priority? (Create convention-enforcer helper agent)
2. What breakthrough enables non-blocking communication? (Background monitoring + message injection)
3. Where is the working MCP foundation? (guardian/mcp-server/ with Test 2 success)
4. What is a helper agent? (Claude instance reading markdown instructions)
5. What is the Phase 1 coordination pattern? (Request-response via MCP messaging)
6. What tools are working daily? (claude-orchestrator/ /session-start, /session-end)
7. What file naming convention should be used? (kebab-case)

## 🚀 Quick Start for Current Session

### Immediate Actions (Based on Current Priority)
1. **Navigate to working directory**: `cd /home/klaus/game-projects/claude-orchestrate/guardian/`
2. **Check current status**: Review Test 2 success evidence and MCP server status
3. **Focus on helper agents**: Start creating convention-enforcer with markdown instructions
4. **Test coordination**: Validate request-response pattern works with real Claude agents

### Key Resources Ready to Use
- **MCP Server**: ✅ Working at `guardian/mcp-server/`
- **Background Monitor**: ✅ Working at `utils/monitor_and_inject.sh`
- **Test Environment**: ✅ Proven at `tests/test2-output-reading/`
- **Documentation**: ✅ Restructured and comprehensive

## 📊 Documentation Structure Changes

**NEW**: Technical documentation restructured for clarity and efficiency:
- **architecture.md**: Condensed core overview (was 880 lines → now ~200 lines)
- **mcp-server-details.md**: Detailed MCP implementation specifics
- **helper-agent-patterns.md**: Claude agent structure and examples
- **migration-strategy.md**: Comprehensive migration planning
- **implementation-status.md**: Current development state and test results
- **system-flows.md**: Detailed coordination patterns and flows

**BENEFIT**: Faster session startup, better targeted information, comprehensive details available when needed.

---
*This streamlined list ensures efficient session startup with essential knowledge only.*
*For complete project navigation after restructuring, see individual technical documents.*
*Updated: 2025-08-14 - Reflects restructured documentation and current priorities.*