---
project: claude-orchestrate
type: vision
title: Claude Orchestrate - Vision & Design Document
version: 2025-01-11 20:00
status: LIVING DOCUMENT - Open for Discussion
summary:
  - Context management system for game development with LLMs
  - Rethinking documentation tiers with tool-specific solutions
  - Multi-agent orchestration for complex projects
  - Focus on preventing context overflow and knowledge loss
tags: [vision, architecture, discussion, game-dev, orchestration]
---

# Claude Orchestrate - Vision Document

## Mission Statement

Create an intelligent orchestration system that manages context, documentation, and multi-agent coordination for game development projects, allowing developers to focus on creation while the system handles knowledge management, bug tracking, and session continuity.

## Core Problems We're Solving

### 1. Context Overflow Crisis
**Problem**: LLM sessions fill up, causing:
- Loss of critical knowledge mid-session
- Inability to complete complex tasks
- Manual intervention to salvage work
- Repeated work across sessions

**Current Reality**: Projects larger than single session context become unmanageable

### 2. Rule & Behavior Drift
**Problem**: LLMs gradually deviate from established patterns:
- Forgets project-specific rules
- Reverts to "standard practices" instead of project APIs
- Loses understanding of custom architecture
- Inconsistent behavior across sessions

### 3. Documentation Chaos
**Problem**: Current 7-tier system has issues:
- Too rigid for some needs
- Documents become stale/incorrect
- Errors propagate through handovers
- Manual maintenance overhead
- Not all tiers equally useful

### 4. Bug Marathon Syndrome
**Problem**: Simple bugs taking 20+ sessions because:
- Lost context about previous attempts
- No memory of what didn't work
- Missing understanding of system interactions
- Fragmented knowledge across sessions

### 5. Multi-Agent Coordination
**Problem**: Need parallel processing but:
- Tmux is too chaotic to manage
- Message passing loses data
- No unified state management
- Agents interfere with each other

## Rethinking Documentation Tiers

### Current 7-Tier System Analysis

| Tier | Current Purpose | Problems | Alternative Tool? |
|------|----------------|----------|-------------------|
| **Design** | Vision, UX specs | Works well, needs immutability | Keep as markdown, version controlled |
| **SystemSpec** | Engine-agnostic schemas | Often outdated | Could be code-as-spec? |
| **Technical** | Implementation details | Too broad, mixes concerns | Split into API docs + Architecture |
| **Execution** | Task guides | Overlaps with Task tier | Merge with Tasks or remove |
| **Task** | Specific work items | Better in task tracker | **→ YouTrack/GitHub Issues** |
| **Status** | Progress, handovers | Critical but manual | Automate with hooks |
| **Knowledge Base** | Project understanding | Not well integrated | **→ Vector DB or Notebook LM?** |

### Proposed Hybrid Architecture

```
Project Knowledge System
├── Immutable Core (Git)
│   ├── Vision & Design docs
│   ├── Architecture decisions
│   └── API Contracts
│
├── Task Management (YouTrack/GitHub)
│   ├── Features & Epics
│   ├── Bugs with full context
│   ├── Task dependencies
│   └── Progress tracking
│
├── Living Knowledge (Vector DB/Notebook LM)
│   ├── Code patterns & examples
│   ├── Decision history
│   ├── Bug solutions
│   └── Session learnings
│
└── Session State (SQLite)
    ├── Current context
    ├── Active rules
    ├── Recent decisions
    └── Message queue
```

## Architecture Components

### 1. Context Guardian
**Purpose**: Prevent context overflow
**Implementation**: Python hooks monitoring token usage
**Features**:
- Real-time token counting
- Multi-level warnings (70%, 80%, 90%)
- Automatic checkpointing
- Emergency handover at 90%

### 2. Rule Enforcer
**Purpose**: Maintain behavioral consistency
**Approach**: Micro-rules with context injection
**Features**:
- Immutable core rules
- Context-specific rule selection
- Periodic rule reminders
- Drift detection & correction

Tool: brain/rule_enforcer.py - The engine
Rules: brain/rules/subfolder/*.yaml - Separate, visible, modular
Several Rule Sets: naming, documentation, core, code, etc.
Hook: For periodic injection

Rules are defined ONCE in YAML files (brain/rules/)
RuleEnforcer reads these YAML files
Hooks just call the RuleEnforcer (no duplicate rules!)

### 3. Knowledge Orchestrator
**Purpose**: Manage distributed knowledge
**Tools Integration**:
- **Markdown**: Immutable design docs
- **YouTrack**: Tasks, bugs, progress
- **Vector DB**: Searchable knowledge
- **SQLite**: Session state, messages
- **Notebook LM**: Complex knowledge synthesis?

### 4. Multi-Agent Coordinator
**Purpose**: Enable parallel work without chaos
**Design Philosophy**:
- Agents share data, not context
- Message queue in SQLite
- Each agent has focused role
- Central orchestrator manages conflicts

### 5. Bug Hunter Mode
**Purpose**: Focused debugging with full history
**Features**:
- Isolated context for specific bug
- Full history of attempts
- Related code & decisions
- YouTrack integration for tracking

## Open Questions for Discussion

### Documentation Strategy
1. **Should we abandon the 7-tier system entirely?**
   - Keep only what works (Design, Status)?
   - Use specialized tools per need?
   
2. **Notebook LM Integration?**
   - Could it maintain project knowledge?
   - How would we integrate it?
   - Worth the complexity?

3. **Vector DB Selection**
   - Local ChromaDB for privacy?
   - Pinecone for power?
   - Simple embedding search sufficient?

### Tool Choices
1. **Bug Tracking**: YouTrack vs GitHub Issues vs Linear?
   - YouTrack: Powerful but complex
   - GitHub: Simple but limited
   - Linear: Modern but another tool

2. **Memory System**: Mem0 vs Custom vs Notebook LM?
   - Mem0: Ready-made but black box
   - Custom: Full control but more work
   - Notebook LM: Powerful but external

3. **Agent Communication**
   - SQLite message queue (simple, reliable)
   - Redis pub/sub (fast but complex)
   - File-based (primitive but debuggable)

### Workflow Patterns
1. **Parallel Agents**: When and how?
   - Always run doc agent parallel?
   - Spawn specialized agents on demand?
   - Fixed set vs dynamic spawning?

2. **Context Switching**
   - Hard cut at 90% context?
   - Gradual handover process?
   - Multiple small contexts vs one large?

3. **User Interaction**
   - How much automation vs control?
   - Approval gates where?
   - Visibility into agent actions?

## The Problem: Documentation Permanence vs. Agent Feedback
### Current Issue
Agents generate two types of documentation that are currently mixed together:

Permanent Project Knowledge - Design decisions, architecture, handovers that must persist
Transient Agent Reports - "I reorganized files", "I checked the index", "I fixed these bugs" - useful for immediate review but creates clutter over time

### The Dilemma

Users need visibility: When an agent does work, users want to review what happened
Projects need cleanliness: These reports quickly clutter the documentation
Knowledge must persist: Important findings need to be incorporated into permanent docs
Reports become stale: After review, agent reports lose value rapidly

### Future Vision Issues
In a multi-agent system with UI monitoring:

Multiple agents generating reports simultaneously
Sub-agents creating their own feedback documents
Monitoring agents producing status reports
All of this would exponentially increase documentation clutter


### Future Vision Proposal

**Clear Separation**

Docs/ = What matters next month
agent-feedback/ = What matters today
.orchestrator/ = What the tool needs

**Agent Responsibility**
Each agent decides:

Is this permanent knowledge? → Docs/
Is this temporary feedback? → agent-feedback/
Is this operational data? → .orchestrator/


**Lifecycle Management**
python# Agent creates feedback
create_feedback("agent-feedback/session-{date}/reorganizer/report.md")

User reviews (via UI or manually)
Extract important parts to permanent docs
update_permanent("Docs/Status/Session_Handover.md", key_findings)
Safe to clean: rm -rf agent-feedback/session-* # older than 7 days

**UI Integration (Future)**
UI reads from agent-feedback/ for recent activity
Shows alerts for new reports
Allows one-click cleanup
Prompts to extract important findings


   
   
## Implementation Phases

### Phase 0: Foundation (Week 1)
- [ ] Create base project structure
- [ ] Set up SQLite for state management  
- [ ] Import hook system from claude-template
- [ ] Create vision tracking document

### Phase 1: Context Guardian (Week 1)
- [ ] Token counting system
- [ ] Warning thresholds
- [ ] Automatic checkpointing
- [ ] Emergency handover

### Phase 2: Rule System (Week 2)
- [ ] Micro-rule architecture
- [ ] Rule injection hooks
- [ ] Drift detection
- [ ] Rule validation

### Phase 3: Knowledge Integration (Week 3)
- [ ] YouTrack MCP setup
- [ ] Vector DB exploration
- [ ] Knowledge extraction from sessions
- [ ] Search interface

### Phase 4: Multi-Agent (Week 4+)
- [ ] Agent spawning system
- [ ] Message queue
- [ ] Coordination protocols
- [ ] Conflict resolution

## Success Criteria

### Must Have (MVP)
- ✓ Prevents context overflow
- ✓ Maintains rules across sessions
- ✓ Tracks bugs with context
- ✓ Automates session handovers

### Should Have (v1.0)
- ✓ Parallel documentation agent
- ✓ Vector search for knowledge
- ✓ YouTrack integration
- ✓ Multi-agent coordination

### Nice to Have (Future)
- ✓ Notebook LM integration
- ✓ Visual progress tracking
- ✓ Team collaboration
- ✓ Cross-project learning

## Technical Decisions

### Confirmed
- **Language**: Python (you understand it, good ecosystem)
- **State DB**: SQLite (simple, reliable, portable)
- **Base Structure**: Extend claude-template hooks
- **Unity Bridge**: Your existing MCP implementation

### Under Consideration
- **Bug Tracker**: YouTrack vs GitHub Issues
- **Vector DB**: Local vs Cloud
- **Memory System**: Mem0 vs Custom
- **Agent Communication**: SQLite vs Redis vs Files
- **Persistent Monitor or Meta-Agent**: monitors the orchestrator, session, and can provide overview to the user what is going on with several agents running in parallel

### Rejected
- **Tmux Orchestrator**: Too chaotic for your needs
- **Claude-Flow**: Too complex, not game-focused
- **Pure sub-agents**: Context sharing issues

## Next Steps

1. **Immediate**: Build Context Guardian (prevents data loss)
2. **This Week**: Implement basic rule system
3. **Evaluate**: Test YouTrack MCP for bug tracking
4. **Experiment**: Try vector search for knowledge retrieval
5. **Document**: Keep updating this vision as we learn

## Discussion Topics

### For Next Session
1. **Documentation Tiers**: Which to keep, which to replace?
2. **Notebook LM**: Worth exploring for knowledge synthesis?
3. **Visual Interface**: Terminal only or add web UI later?
4. **Team Features**: Solo focus or plan for collaboration?

### Open Research
1. How does Notebook LM API work?
2. Can we extract knowledge from Claude sessions automatically?
3. Best vector DB for local game dev knowledge?
4. Optimal agent communication patterns?

---

## Notes Section

### User Feedback Integration Needed
- How do you currently use YouTrack?
- What's your experience with Notebook LM?
- Which documentation tiers cause most friction?
- What's your ideal bug tracking workflow?

### Technical Explorations
- Test ChromaDB for local vector search
- Evaluate YouTrack MCP capabilities
- Benchmark token counting accuracy
- Prototype message queue options

### Inspiration from User's Systems
- AWMS vision: Parallel documentation concept
- 7-tier system: Good structure, needs modernization  
- Hook system: Excellent foundation to build on
- Unity MCP: Already solved, can integrate

---

*This is a living document. Update as we learn and decide.*
