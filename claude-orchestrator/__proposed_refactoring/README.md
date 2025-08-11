# Proposed Refactoring: Guardian-Based Architecture with Autonomous Agents

## Overview

This folder contains the complete design, architecture, and testing requirements for refactoring Claude Orchestrator to solve its fundamental problems while preserving what works.

## Key Documents

1. **[WHY.md](./WHY.md)** - The problems we're solving and why current approaches have limitations
2. **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Complete system design including Guardian, memory systems, and dashboard
3. **[PROJECT_PLAN.md](./PROJECT_PLAN.md)** - Phased implementation with proof requirements
4. **[TESTING_REQUIREMENTS.md](./TESTING_REQUIREMENTS.md)** - Specific tests that must pass before refactoring

## Critical Findings

### What Works (Keep These)
- Python for file I/O and validation
- SQLite for state management  
- Handover system with validation
- Basic workflow structure

### What Doesn't Work (Must Fix)
- **Main agent blocks on sub-agents** - No true parallelization
- **Temperature 1.0 chaos** - Inconsistent behavior across sessions
- **Hidden Python failures** - Can't debug when things go wrong
- **No enforcement mechanism** - Rules are just suggestions

### What We Need to Prove
1. **Autonomous agent execution** - Main can continue while sub-agents run
2. **Guardian enforcement** - Can actually block violations
3. **Real-time monitoring** - Dashboard updates fast enough
4. **Memory systems** - Agents can share knowledge effectively

## The Proposed Solution

### Core Components

1. **Guardian Agent** - Enforcer with veto power over all actions
2. **Live Dashboard** - Real-time web interface with human translations
3. **Memory Hierarchy** - Short-term (SQLite) and long-term (Vector DB)
4. **Autonomous Execution** - Agents work independently without blocking

### Architecture Highlights

```
User sees everything via Dashboard
         ↓
Guardian monitors and can veto
         ↓
Main Agent works continuously
         ↓
Sub-Agents run autonomously
         ↓
Memory systems provide context
```

## Current Status

### ✅ Designed
- Complete architecture documented
- Testing requirements defined
- Implementation plan created
- Fallback strategies identified

### 🔄 Next Steps
1. **Prove autonomous execution works** (Critical blocker)
2. Test Guardian enforcement mechanism
3. Build dashboard prototype
4. Test memory system performance

### ❌ Not Started
- Actual implementation
- Integration testing
- Migration from current system

## How to Use This Folder

### For Development
1. Read WHY.md to understand the problems
2. Study ARCHITECTURE.md for system design
3. Follow PROJECT_PLAN.md for implementation
4. Use TESTING_REQUIREMENTS.md to validate

### For Testing
```bash
# Create test scripts in this folder
__proposed_refactoring/
├── tests/
│   ├── test_autonomous_execution.py
│   ├── test_guardian_enforcement.py
│   ├── test_dashboard_updates.py
│   └── test_memory_systems.py
└── proofs/
    ├── poc_autonomous_agents/
    ├── poc_guardian_system/
    └── poc_dashboard/
```

### For Proof of Concepts
Each critical component needs proof before implementation:

1. **Autonomous Execution POC**
   - Try subprocess approach
   - Try MCP async approach  
   - Try file-based signaling
   - Pick what works

2. **Guardian POC**
   - Hook interception
   - Veto mechanism
   - Performance testing

3. **Dashboard POC**
   - WebSocket streaming
   - Update performance
   - Translation speed

## Decision Gates

### Gate 1: Autonomous Execution (Week 1)
- **Pass:** Main agent can work while sub-agents run → Continue
- **Fail:** Cannot achieve autonomy → Abandon refactor, enhance current

### Gate 2: Core Components (Week 2)  
- **Pass:** Guardian + Dashboard work → Continue
- **Fail:** Too complex/slow → Simplify approach

### Gate 3: Integration (Week 6)
- **Pass:** All components work together → Begin migration
- **Fail:** Integration issues → Keep components separate

## Important Notes

### We Are NOT:
- Throwing away working code
- Refactoring without proof
- Breaking current functionality
- Making assumptions about what works

### We ARE:
- Testing every critical assumption
- Keeping what works
- Fixing only what's broken
- Maintaining user control

## The Mixed Approach Philosophy

Instead of choosing one approach over another, we're combining:

- **Python's reliability** for deterministic operations
- **Agent flexibility** for complex reasoning
- **Guardian enforcement** for consistency
- **Dashboard visibility** for user control
- **Memory systems** for context preservation

## Success Criteria

The refactoring succeeds when:

1. **Consistency:** Same behavior despite temperature 1.0
2. **Visibility:** User sees everything in human terms
3. **Reliability:** Workflows complete without intervention
4. **Performance:** No blocking, fast responses
5. **Control:** User can intervene at any point

## Next Session Priorities

1. **Test autonomous execution methods** - This blocks everything else
2. Create minimal Guardian prototype
3. Build basic dashboard with WebSocket
4. Test SQLite concurrent access
5. Document what works and what doesn't

---

*This refactoring plan is based on real-world experience with the current system. Every problem listed has occurred multiple times. Every solution has been designed to address specific, observed failures.*

**Remember: We only refactor after proving the new approach works better.**