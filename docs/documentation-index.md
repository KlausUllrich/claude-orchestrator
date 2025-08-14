---
project: claude-orchestrate
type: convention
title: "Documentation Index - Claude Orchestrator/Guardian Development"
version: 2025-08-14-restructured
status: CURRENT
summary:
  - Complete project documentation navigation after restructuring
  - Streamlined technical documentation with specialized files
  - Clear session startup path and current development priorities
  - Proper organization replacing duplicate-heavy architecture.md
tags: [navigation, documentation, architecture, restructured]
---

# Documentation Index - Claude Orchestrator/Guardian Development

## 🎯 Project Status Overview

**Current Architecture**: Dual-track development with working foundation
- **claude-orchestrator/**: ✅ **WORKING DAILY** - Session tools (`/session-start`, `/session-end`)
- **guardian/**: ✅ **FOUNDATION READY** - MCP server + non-blocking communication proven
- **Current Priority**: Create first helper agent (convention-enforcer)
- **Key Achievement**: Test 2 SUCCESS - Non-blocking agent communication working

## 📚 Essential Session Reading (Streamlined)

**Read in this exact order before starting work:**

### 1. Core Rules & Standards
- **[CLAUDE.md](../CLAUDE.md)** - Core interaction rules and hierarchy ⭐ **FIRST**
- **[docs/conventions.md](conventions.md)** - Project standards and naming conventions
- **[docs/read-first.md](read-first.md)** - **UPDATED** Complete session checklist

### 2. Current Session Context
- **[docs/status/handover-next.md](status/handover-next.md)** - Latest session state and priorities
- **[docs/status/users-todos.md](status/users-todos.md)** - Master TODO list with current focus

### 3. Core System Understanding (Restructured)
- **[docs/technical/architecture.md](technical/architecture.md)** - **CONDENSED** Core overview (~200 lines)
- **[docs/technical/implementation-status.md](technical/implementation-status.md)** - **NEW** Current development state

### 4. Specialized Technical Documentation (New Structure)
- **[docs/technical/helper-agent-patterns.md](technical/helper-agent-patterns.md)** - **NEW** Claude agent + markdown patterns
- **[docs/technical/mcp-server-details.md](technical/mcp-server-details.md)** - **NEW** MCP implementation details
- **[docs/technical/migration-strategy.md](technical/migration-strategy.md)** - **NEW** Detailed migration planning
- **[docs/technical/system-flows.md](technical/system-flows.md)** - **NEW** Coordination and flow patterns

## 📊 Documentation Restructuring Summary

### ✅ **Completed Changes**
| Old Structure | New Structure | Benefit |
|---------------|---------------|---------|
| **architecture.md** (880 lines) | **architecture.md** (200 lines) + 5 specialized docs | 77% reduction in core reading |
| Massive duplicates | Single source per concept | Clear, accurate information |
| Fantasy implementations | Working codebase alignment | Reflects actual system |
| Mixed concerns | Specialized focus areas | Targeted information access |

### 🎯 **Reading Path Optimization**
- **Session startup**: ~400 lines (was 1000+ lines)
- **Specialized work**: Deep docs available when needed
- **Current priorities**: Clearly highlighted in restructured docs
- **Cross-references**: Clear navigation between related documents

## 🚀 Working Implementation Status

### Foundation Complete ✅
| Component | Status | Location | Evidence |
|-----------|--------|----------|----------|
| **MCP Server** | ✅ Working | `guardian/mcp-server/` | Test 2 success |
| **Non-blocking Communication** | ✅ Proven | `utils/monitor_and_inject.sh` | Agents stay responsive |
| **Agent Registration** | ✅ Working | MCP tools | Agents register/discover |
| **Background Monitoring** | ✅ Proven | Background scripts | Message injection works |
| **WezTerm Integration** | ✅ Tested | Test environment | Multi-pane coordination |

### Current Development Priority 🎯
- **Next Task**: Create convention-enforcer helper agent
- **Approach**: Claude instance + markdown instructions
- **Pattern**: Request-response coordination via MCP
- **Goal**: Validate helper agent framework effectiveness

### Daily Tools Preserved ✅
- **Session Management**: `/session-start`, `/session-end` in claude-orchestrator/
- **Handover System**: Working session continuity
- **Context Guardian**: Token monitoring and overflow prevention
- **Compatibility**: All current workflows continue working

## 🧪 Test Evidence & Validation

### Proven Capabilities ✅
**Test 2 - Non-Blocking Communication SUCCESS**:
- **Location**: `guardian/tests/test2-output-reading/`
- **Evidence**: `claude-orchestrator/__proposed_refactoring/test_evidence/02_output_reading_SUCCESS.md`
- **Achievement**: Agent 1 stayed responsive while Agent 2 analyzed webpage
- **Key Finding**: Background monitoring + message injection = non-blocking coordination

### Earlier Test Results ✅
- **Test 1**: Chain communication (Agent 1 → Agent 2 → Agent 3 → Agent 2 → Agent 1)
- **Parallel execution**: `run_in_background=True` enables true parallel Claude agents
- **File coordination**: Background process coordination proven

## 📁 Current Project Structure

### Guardian System (Active Development)
```
guardian/                           # 🎯 Current work location
├── mcp-server/                    # ✅ Working Node.js + SQLite coordination
├── utils/                         # ✅ Working monitor_and_inject.sh
├── tests/                         # ✅ Test 2 success evidence
└── helper-agents/                 # 🎯 Next: Create convention-enforcer
    └── convention-enforcer/       # 🎯 To be created
        ├── instructions.md        # Claude agent instructions
        ├── naming-rules.md        # Specific rules to enforce
        └── .claude/settings.json  # MCP configuration
```

### Claude-Orchestrator (Preserved Working)
```
claude-orchestrator/               # ✅ Continue using during transition
├── orchestrate.py                # ✅ Working coordination script
├── brain/                        # ✅ Session management
├── tools/                        # ✅ Context Guardian
└── resource-library/             # ✅ Templates (to extract to helper agents)
```

### Documentation (Restructured)
```
docs/
├── read-first.md                 # ✅ Updated session startup guide
├── conventions.md                # ✅ Project standards
├── technical/                    # ✅ Restructured technical docs
│   ├── architecture.md           # ✅ Condensed core overview
│   ├── implementation-status.md  # ✅ Current development state
│   ├── helper-agent-patterns.md  # ✅ Claude agent + markdown patterns
│   ├── mcp-server-details.md     # ✅ MCP implementation specifics
│   ├── migration-strategy.md     # ✅ Detailed migration planning
│   └── system-flows.md           # ✅ Coordination patterns
└── status/                       # ✅ Session handovers and TODOs
```

## 🔧 Quick Navigation by Work Type

### 🎯 Current Session Priority (Helper Agent Development)
1. **Start here**: [helper-agent-patterns.md](technical/helper-agent-patterns.md)
2. **Coordination details**: [system-flows.md](technical/system-flows.md)
3. **MCP tools**: [mcp-server-details.md](technical/mcp-server-details.md)
4. **Working example**: `guardian/tests/test2-output-reading/`

### 🔧 MCP Server Development
1. **Implementation details**: [mcp-server-details.md](technical/mcp-server-details.md)
2. **Current status**: [implementation-status.md](technical/implementation-status.md)
3. **Working code**: `guardian/mcp-server/`

### 📋 Migration Planning
1. **Strategy overview**: [migration-strategy.md](technical/migration-strategy.md)
2. **Current state**: [implementation-status.md](technical/implementation-status.md)
3. **Architecture transition**: [architecture.md](technical/architecture.md)

### 🚀 Session Management (Daily Use)
1. **Working tools**: `claude-orchestrator/` (/session-start, /session-end)
2. **Handover template**: `claude-orchestrator/resource-library/documents/handovers/`
3. **Status tracking**: [status/users-todos.md](status/users-todos.md)

## 📚 Reference Documentation

### Historical Context (Important Background)
- **[claude-orchestrator/__proposed_refactoring/WHY.md](../claude-orchestrator/__proposed_refactoring/WHY.md)** - Deep problem analysis
- **[docs/design/vision.md](design/vision.md)** - Project goals and strategic direction
- **Breakthrough documentation**: `claude-orchestrator/__proposed_refactoring/` (proven solutions)

### Legacy Architecture (Pre-Restructuring)
- **Old architecture.md**: Had 880 lines with massive duplicates
- **Fantasy implementations**: Python helper classes that never existed
- **Mixed concerns**: Communication + agents + flows all in one file
- **Result**: Difficult session startup, unclear priorities

## 🎯 Success Metrics

### Documentation Restructuring Success ✅
- **Reading time reduced**: 77% less essential reading for session startup
- **Information clarity**: Each concept documented once in appropriate location
- **Current priorities**: Clear focus on helper agent development
- **Accuracy**: Documentation reflects working codebase

### Technical Achievement ✅
- **Non-blocking communication**: Test 2 proven successful
- **MCP coordination**: Reliable message routing between agents
- **Working foundation**: Ready for helper agent implementation
- **Preserved productivity**: claude-orchestrator/ continues working

### Next Milestones 🎯
- **First helper agent working**: Convention-enforcer with markdown instructions
- **Request-response pattern proven**: Main agent ↔ helper agent coordination
- **Helper agent framework validated**: Patterns work with real Claude agents
- **Migration readiness**: Guardian can start replacing claude-orchestrator features

## 🔄 Current Development Focus

### Immediate Tasks (Next 1-2 Sessions)
1. **Create convention-enforcer helper agent**
   - Directory structure with markdown instructions
   - Test request-response pattern
   - Validate helper guidance quality

2. **Fix monitor duplicate notifications**
   - Add duplicate detection to monitor_and_inject.sh
   - Test with multiple rapid messages

3. **Document helper agent patterns**
   - Validate instruction templates work
   - Test with real project files

### Short-term Goals (Next 2-3 Sessions)
- **Additional helper agents**: workflow-monitor, documentation-maintainer
- **WezTerm automation**: Launch scripts for multi-agent environment
- **Migration tools**: Extract patterns from claude-orchestrator to markdown

---

## 🚀 Quick Start Commands

```bash
# Current working directory
cd /home/klaus/game-projects/claude-orchestrate/guardian/

# Check Test 2 success evidence
ls tests/test2-output-reading/

# Review MCP server status
ls mcp-server/

# Start working on helper agents
mkdir -p helper-agents/convention-enforcer
```

---

*This index reflects the restructured documentation with streamlined session startup and comprehensive specialized resources.*
*Updated: 2025-08-14 - Post-restructuring with 77% reading reduction and clear current priorities.*