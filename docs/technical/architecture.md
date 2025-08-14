---
project: claude-orchestrate
type: technical
title: "Claude Orchestrator/Guardian - System Architecture"
version: 2025-08-14-restructured
status: CURRENT
summary:
  - Corrected architecture: Claude agents + markdown instructions
  - Multi-agent WezTerm coordination with proven MCP foundation
  - Current productive tools preserved during evolution
  - Phase 1: Request-response, Phase 2: Hook-based helper assignment
tags: [architecture, multi-agent, wezterm, mcp, guardian, claude-agents, markdown-driven]
---

# Claude Orchestrator/Guardian - System Architecture

## Executive Summary

**Current Reality**: Dual-track development preserving working tools while building next-generation capabilities:
- **claude-orchestrator/**: ✅ **Working daily tools** (`/session-start`, `/session-end`, `orchestrate.py`)
- **guardian/**: 🎯 **Multi-agent system** with proven MCP foundation and non-blocking communication

**Key Achievement**: Test 2 SUCCESS - Non-blocking agent communication proven working with real Claude agents.

**Goal**: Evolution to Claude agents primed with markdown instructions, coordinated through MCP server, while maintaining all current productivity.

## System Overview

### High-Level Architecture
```
WezTerm Terminal Multiplexer
├── Main Agent (Pane 1)           # Primary user interaction + development
│   └── Requests help from helper agents via MCP
├── Helper Agent 1 (Pane 2)       # Claude + convention-enforcer/instructions.md
├── Helper Agent 2 (Pane 3)       # Claude + workflow-monitor/instructions.md  
├── Helper Agent N (Pane N)       # Claude + specialized MD instructions
└── Background Monitor             # monitor_and_inject.sh (proven working)

Central Coordination: MCP Server (Node.js + SQLite) ✅ Working
Communication: Non-blocking via background polling + message injection ✅ Proven
```

### Target Project Structure
```
any-project/
├── guardian/                   # 🎯 Droppable multi-agent system
│   ├── mcp-server/            # ✅ Working - Node.js + SQLite coordination
│   ├── helper-agents/         # 🎯 New - Claude agents + markdown instructions
│   │   ├── convention-enforcer/
│   │   │   ├── instructions.md      # "You are a convention enforcer..."
│   │   │   ├── naming-rules.md      # Specific rules to check
│   │   │   └── .claude/settings.json
│   │   └── workflow-monitor/
│   │       ├── instructions.md      # "You monitor workflows..."
│   │       └── .claude/settings.json
│   ├── utils/                 # ✅ Working - monitor_and_inject.sh
│   └── tests/                 # ✅ Working - Test 2 success examples
├── claude-orchestrator/       # ✅ Keep working during transition
└── [project files]
```

## Current Implementation Status

| Component | Status | Location | Description |
|-----------|--------|----------|-------------|
| **MCP Server** | ✅ Working | `guardian/mcp-server/` | Node.js server with SQLite coordination |
| **Non-blocking Communication** | ✅ Proven | `utils/monitor_and_inject.sh` | Background polling + message injection |
| **Agent Registration** | ✅ Working | MCP tools | Agents can register and discover each other |
| **Message Broker** | ✅ Working | MCP server | Inter-agent message routing |
| **WezTerm Integration** | ✅ Tested | Test 2 setup | Multi-pane coordination proven |
| **Session Management** | ✅ Daily use | `claude-orchestrator/` | `/session-start`, `/session-end` commands |
| **Helper Agent Framework** | 🎯 Next | `helper-agents/` | Claude instances + markdown instructions |
| **Migration Tools** | 📋 Planned | `migration/` | Extract patterns to markdown |

## Helper Agent Approach

### Core Concept: Claude Agents + Markdown Instructions
Helper agents are **Claude instances** that read markdown files containing their specialized instructions, rules, and templates. This follows the proven Test 2 pattern.

### Phase 1: Request-Response Pattern (Immediate)
```
Main Agent: "I'm creating a new script file 'MyScript.py'"
[sends message to convention-enforcer via MCP]

Convention Enforcer: [reads naming-rules.md]
Convention Enforcer: "Filename violates kebab-case rule. Suggest: my-script.py"
[sends response via MCP]

Main Agent: [receives feedback, acts on it]
```

### Phase 2: Hook-Based Pattern (Future)
```
Main Agent: [creates file]
Orchestrator: [detects file creation hook]
Orchestrator: [spawns convention-enforcer with file context]
Convention Enforcer: [validates against markdown rules]
Convention Enforcer: [reports issues or approval]
```

### Helper Agent Structure
```
helper-agents/convention-enforcer/
├── instructions.md          # "You are a convention enforcer agent..."
├── naming-rules.md          # Specific rules to check
├── file-organization.md     # Directory structure standards
├── examples/               # Good/bad examples
└── .claude/settings.json   # MCP configuration
```

## Technology Stack

### Current Stack (claude-orchestrator/)
| Component | Technology | Status |
|-----------|------------|--------|
| **Orchestration** | Python (`orchestrate.py`) | ✅ Working daily |
| **Database** | SQLite (session state) | ✅ Working |
| **Coordination** | File-based + background processes | ✅ Working |
| **Interface** | Single Claude instance + command hooks | ✅ Working |

### Target Stack (guardian/)
| Component | Technology | Status |
|-----------|------------|--------|
| **MCP Server** | Node.js + SQLite | ✅ Working |
| **Communication** | Background monitoring + message injection | ✅ Proven |
| **Agent Coordination** | MCP protocol + SQLite queues | ✅ Working |
| **Interface** | WezTerm multi-pane + Claude agents | ✅ Tested |
| **Instructions** | Markdown files | 🎯 Next priority |

## Migration Strategy

### Phase 1: Foundation Complete ✅
- ✅ MCP server working with SQLite backend
- ✅ Non-blocking communication proven (Test 2)
- ✅ WezTerm multi-pane coordination tested
- ✅ claude-orchestrator/ continues working

### Phase 2: Helper Agents (Current Priority)
- 🎯 Create first helper agent: convention-enforcer
- 🎯 Develop markdown instruction patterns
- 🎯 Test request-response coordination
- 🎯 Validate helper agent effectiveness

### Phase 3: Feature Parity (Next)
- 📋 Implement `/session-start`, `/session-end` in guardian/
- 📋 Migrate session management to multi-agent model
- 📋 Create migration tools for seamless transition
- 📋 Port Context Guardian as helper agent

### Phase 4: Enhanced Capabilities (Future)
- 🔮 Deploy full helper agent suite
- 🔮 Implement hook-based automatic assignment
- 🔮 Add vector database for long-term knowledge
- 🔮 Professional multi-agent development environment

## Success Metrics

### Technical Achievement
- ✅ **Non-blocking communication**: Test 2 proven - agents stay responsive
- ✅ **MCP coordination**: Reliable message routing between agents
- 🎯 **Helper agent effectiveness**: Markdown instructions guide specialized help
- 🎯 **Request-response flow**: Smooth coordination between main and helpers

### User Experience
- ✅ **Current productivity preserved**: claude-orchestrator/ continues working
- 🎯 **Multi-agent value**: Helpers provide meaningful specialized assistance
- 🎯 **Seamless transition**: Guardian adoption without workflow disruption
- 📋 **Enhanced capability**: True parallel agent coordination

### Long-term Goals
- 📋 **Automated standards**: Helper agents maintain project conventions
- 📋 **Knowledge accumulation**: Specialized agents build domain expertise
- 🔮 **Development efficiency**: Parallel support accelerates work
- 🔮 **Project sustainability**: Consistent quality over months/years

## Next Steps

### Immediate Priorities
1. **Create convention-enforcer helper agent** with markdown instructions
2. **Test Phase 1 request-response pattern** between main and helper
3. **Validate helper agent effectiveness** with real naming/organization rules
4. **Document helper agent patterns** for future specializations

### Development Focus
- **helper-agents/** directory structure and markdown patterns
- **Request-response workflow** via MCP messaging
- **WezTerm setup automation** for multi-agent development
- **Migration tools** to extract existing knowledge to markdown

## Reference Documentation

For detailed implementation information, see:

- **[MCP Server Details](mcp-server-details.md)** - Server implementation, database schema, tools
- **[Helper Agent Patterns](helper-agent-patterns.md)** - Markdown instruction patterns, examples
- **[Migration Strategy](migration-strategy.md)** - Detailed migration phases and tools
- **[Implementation Status](implementation-status.md)** - Current development status, test results
- **[System Flows](system-flows.md)** - Detailed flow diagrams and coordination patterns

---

## Summary

This architecture represents the **correct evolution path**: from working single-agent tools to Claude-agent collaborative orchestration. The foundation is proven (MCP + non-blocking communication), the approach is validated (Claude agents + markdown instructions), and the transition preserves all current productivity.

**Key achievements**: Working MCP foundation, proven non-blocking communication, clear helper agent vision.
**Next milestone**: First working helper agent with markdown-driven specialization.

---
*Architecture reflects working codebase and corrected Claude-agent approach. Updated: 2025-08-14*