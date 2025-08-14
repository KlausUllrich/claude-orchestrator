---
project: claude-orchestrate
type: convention
title: "Documentation Index - Claude Orchestrator/Guardian Development"
version: 2025-08-14
status: CURRENT
summary:
  - Complete project documentation navigation
  - Parallel development: claude-orchestrator (stable) + guardian (next-gen)
  - Breakthrough findings prominently featured
  - Clear relevance indicators for all documents
tags: [navigation, documentation, architecture, breakthrough]
---

# Documentation Index - Claude Orchestrator/Guardian Development

## 🎯 Project Status Overview

**Current Architecture**: Parallel development of two systems
- **claude-orchestrator/**: 🟢 CURRENT - Stable working system with proven breakthroughs
- **guardian/**: 🟡 EVOLVING - Next generation system in active development
- **Migration Strategy**: Gradual transition preserving functionality

## 📚 Mandatory Session Reading

**Read in this exact order before starting any work:**

### 1. Core Rules & Standards
- [CLAUDE.md](../CLAUDE.md) - **FIRST** - Core interaction rules and hierarchy
- [docs/conventions.md](conventions.md) - Project standards and file naming conventions
- [docs/read-first.md](read-first.md) - Complete session checklist and understanding requirements

### 2. Current Session Context  
- [docs/status/handover-next.md](status/handover-next.md) - Latest session handover and current state
- [docs/status/users-todos.md](status/users-todos.md) - Master TODO list with user priorities

### 3. Core Architecture Understanding
- [docs/design/vision.md](design/vision.md) - **ENHANCED** - Project goals with breakthrough integration
- [docs/technical/architecture.md](technical/architecture.md) - System design and folder structure
- [claude-orchestrator/__proposed_refactoring/WHY.md](../claude-orchestrator/__proposed_refactoring/WHY.md) - **CRITICAL** - Deep problem analysis

## 🎉 Breakthrough Documentation

### The Core Discovery (🟢 CURRENT)
- [claude-orchestrator/__proposed_refactoring/BREAKTHROUGH_CLAUDE_PARALLELIZATION.md](../claude-orchestrator/__proposed_refactoring/BREAKTHROUGH_CLAUDE_PARALLELIZATION.md) - **THE SOLUTION** - True parallel Claude execution proven
- [claude-orchestrator/__proposed_refactoring/ORCHESTRATOR_BREAKTHROUGH.md](../claude-orchestrator/__proposed_refactoring/ORCHESTRATOR_BREAKTHROUGH.md) - Complete system documentation

### Architecture Decisions (🟢 CURRENT)
- [claude-orchestrator/__proposed_refactoring/GUARDIAN_ARCHITECTURE_DECISION.md](../claude-orchestrator/__proposed_refactoring/GUARDIAN_ARCHITECTURE_DECISION.md) - Architecture with hybrid approach
- [claude-orchestrator/__proposed_refactoring/PARALLELIZATION_APPROACHES_COMPARISON.md](../claude-orchestrator/__proposed_refactoring/PARALLELIZATION_APPROACHES_COMPARISON.md) - Complete analysis of all approaches

### Implementation Guides (🟢 CURRENT)
- [claude-orchestrator/__proposed_refactoring/README.md](../claude-orchestrator/__proposed_refactoring/README.md) - Clean overview of the solution
- [claude-orchestrator/__proposed_refactoring/WHY.md](../claude-orchestrator/__proposed_refactoring/WHY.md) - Complete problem analysis

### Technical Deep Dives (🟢 CURRENT)
- [claude-orchestrator/__proposed_refactoring/CLAUDE_CONTEXT_SHARING.md](../claude-orchestrator/__proposed_refactoring/CLAUDE_CONTEXT_SHARING.md) - Agent context sharing methods
- [claude-orchestrator/__proposed_refactoring/CLAUDE_MONITORING_CAPABILITIES.md](../claude-orchestrator/__proposed_refactoring/CLAUDE_MONITORING_CAPABILITIES.md) - Monitoring and observation capabilities

### Vision Updates (🟢 CURRENT)
- [claude-orchestrator/__proposed_refactoring/WHY.md](../claude-orchestrator/__proposed_refactoring/WHY.md) - **MANDATORY** - Complete problem analysis and requirements
- [docs/Archive/vision-update-breakthrough-archived.md](Archive/vision-update-breakthrough-archived.md) - 📁 Archived - Now integrated into main vision.md

## 💻 Working Implementation

### Current Stable System (claude-orchestrator/)
- [claude-orchestrator/README.md](../claude-orchestrator/README.md) - Tool overview and quick start
- [claude-orchestrator/orchestrator-tools/](../claude-orchestrator/orchestrator-tools/) - **Working implementation**
  - `orchestrator_system.py` - Core orchestrator implementation  
  - `start_orchestrator.sh` - Launch script
  - `orchestrator_tmux_visual.sh` - Visual monitoring dashboard
  - `web_dashboard.py` - Web interface (optional)
  - `orchestrator_ui.html` - UI mockup

### Next Generation System (guardian/)
- [guardian/README.md](../guardian/README.md) - Guardian system overview
- [guardian/HYBRID_ARCHITECTURE.md](../guardian/HYBRID_ARCHITECTURE.md) - Non-blocking multi-agent approach
- [guardian/mcp-server/](../guardian/mcp-server/) - MCP server implementation
- [guardian/tests/](../guardian/tests/) - Working test examples and validation

## 🧪 Test Evidence & Validation

### Proven Capabilities (🟢 CURRENT)
Located in `claude-orchestrator/__proposed_refactoring/test_evidence/`:
- `01_run_in_background_SUCCESS.md` - Proof of non-blocking execution
- `01_chain_communication_SUCCESS.md` - Agent chain communication proven
- `02_output_reading_SUCCESS.md` - Real-time output monitoring
- `04_file_signaling_SUCCESS.md` - File-based coordination working

### Identified Limitations (🟢 CURRENT)
- `02_task_tool_BLOCKS.md` - Task tool blocking behavior documented
- `03_mcp_approach_analysis.md` - MCP complexity analysis

## 📋 Project Documentation

### Design Documents (🟢 CURRENT)
- [docs/design/vision.md](design/vision.md) - **ENHANCED** - Complete project vision with breakthrough integration
  - Core problems and solutions
  - Architecture decisions with proven results
  - Implementation phases updated with current status
  - Strategic shift from theory to working system

### Technical Documents (🟢 CURRENT)
- [docs/technical/architecture.md](technical/architecture.md) - System design and structure
  - Tool structure (claude-orchestrator + guardian)
  - Installation and usage patterns
  - Component relationships
- [docs/technical/agent-feedback-system.md](technical/agent-feedback-system.md) - Documentation strategy
  - Permanent vs transient documentation
  - Lifecycle management approach
  - Agent feedback separation

### Status & Progress (🟢 CURRENT)
- [docs/status/handover-next.md](status/handover-next.md) - **Current session entry point**
- [docs/status/users-todos.md](status/users-todos.md) - **Master TODO list** 
  - Immediate, short-term, medium-term, and long-term tasks
  - Research topics and known issues
  - Organized by priority and timeframe
  - Success metrics and completed items

### Template & Resources (🟢 CURRENT)
- [claude-orchestrator/resource-library/documents/handovers/Session_Handover_Template.md](../claude-orchestrator/resource-library/documents/handovers/Session_Handover_Template.md) - Session handover template

## 🔧 Tool Components

### Claude-Orchestrator Structure (🟢 CURRENT - Stable)
```
claude-orchestrator/
├── brain/                  # Core orchestration logic
├── short-term-memory/      # Session state (SQLite)
├── long-term-memory/       # Persistent knowledge  
├── workflows/              # Project-type specific rules
├── resource-library/       # Templates and components
├── tools/                  # Utilities (Context Guardian)
├── bridges/                # External integrations
└── orchestrator-tools/     # Working implementation
```

### Guardian Structure (🟡 EVOLVING - Next Generation)
```
guardian/
├── mcp-server/            # Core MCP server with SQLite
├── tests/                 # Working test examples
└── utils/                 # Helper utilities
```

## 🚀 Quick Navigation

### For New Sessions
1. ✅ Read mandatory documents (order listed above)
2. ✅ Check current tasks: [users-todos.md](status/users-todos.md)
3. ✅ Review breakthrough: [BREAKTHROUGH_CLAUDE_PARALLELIZATION.md](../claude-orchestrator/__proposed_refactoring/BREAKTHROUGH_CLAUDE_PARALLELIZATION.md)
4. ✅ Understand current system: [architecture.md](technical/architecture.md)

### For Development Work
**Current Stable System:**
```bash
cd claude-orchestrator/orchestrator-tools
./start_orchestrator.sh
```

**Next Generation Testing:**
```bash
cd guardian/tests
./setup_test2.sh
```

### For Understanding the Breakthrough
1. Start with: [BREAKTHROUGH_CLAUDE_PARALLELIZATION.md](../claude-orchestrator/__proposed_refactoring/BREAKTHROUGH_CLAUDE_PARALLELIZATION.md)
2. Full system: [ORCHESTRATOR_BREAKTHROUGH.md](../claude-orchestrator/__proposed_refactoring/ORCHESTRATOR_BREAKTHROUGH.md)
3. Implementation: [guardian/README.md](../guardian/README.md)

## 📂 Archive & Legacy

### Temporary Workspace (🟡 EVOLVING)
- `claude-orchestrator/__proposed_refactoring/` - **Breakthrough workspace**
  - Contains all discovery documentation
  - To be extracted and reorganized as guardian/ matures
  - Critical findings preserved but location temporary

### Project Core Files (🟢 CURRENT - Test Environment)
- `CLAUDE.md` - Claude interaction rules
- `prime.md` - Project primer
- `.claude/` - Hooks and configuration

## 🎯 Key Success Metrics

### Achievements ✅
- **Parallel orchestration SOLVED** - Multiple Claude agents working simultaneously
- **Non-blocking execution PROVEN** - Main orchestrator stays responsive
- **Visual monitoring WORKING** - Real-time visibility into all agents
- **File-based coordination FUNCTIONAL** - Agents communicate through files
- **Context sharing AVAILABLE** - Session resuming enables knowledge transfer

### Next Milestones 🎯
- **Guardian system maturity** - Complete guardian/ implementation
- **Migration strategy** - Smooth transition from claude-orchestrator
- **Professional UI** - Enhanced user experience
- **Documentation consolidation** - Extract findings from __proposed_refactoring

## 🔄 Document Maintenance

### Relevance Status Legend
- **🟢 CURRENT**: Actively maintained, use for new work
- **🟡 EVOLVING**: Valid but being improved/replaced  
- **🔴 DEPRECATED**: Historical reference only
- **📁 ARCHIVED**: Keep for context but don't use

### Update Cycle
- **Each session**: Update handover-next.md and status documents
- **Major milestones**: Review and update architecture/vision documents
- **Breakthrough discoveries**: Document immediately, reorganize later
- **Migration events**: Archive old, promote new, update references

---
*This index provides complete navigation for the dual-track orchestrator/guardian development.*
*Updated: 2025-08-14 - Merged from two indexes with verified file references*