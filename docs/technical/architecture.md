---
project: claude-orchestrate
type: technical
title: "Claude Orchestrator/Guardian - System Architecture"
version: 2025-08-14
status: CURRENT
summary:
  - Transition architecture: claude-orchestrator (working) → guardian (future)
  - Multi-agent WezTerm vision with MCP coordination
  - Current productive tools preserved during evolution
  - Template-driven helper agents with droppable deployment
tags: [architecture, multi-agent, wezterm, mcp, guardian, transition]
---

# Claude Orchestrator/Guardian - System Architecture

## Current Status: Dual-Track Development

**Reality**: We are in a transition period with two parallel systems:
- **claude-orchestrator/**: ✅ **WORKING & ACTIVELY USED** - Daily productivity tools (/session-start, /session-end, orchestrate.py)
- **guardian/**: 🔄 **FUTURE EVOLUTION** - Multi-agent system under development

**Goal**: Evolution, not replacement - Guardian will eventually provide all current functionality plus multi-agent capabilities while remaining droppable into any project.

## Overview

The system is evolving from a single-agent orchestration tool to a multi-agent coordination platform. The target is a droppable guardian/ system that provides WezTerm-based multi-agent coordination while preserving the portability and ease-of-use of the current claude-orchestrator approach.

## Current Working System (claude-orchestrator/)

### Active Daily Tools ✅
```bash
/session-start          # Working session initialization
/session-end            # Working session cleanup  
/handover              # Working session continuity
orchestrate.py         # Working coordination script
```

**Status**: These tools are production-ready and actively used. They must continue working during the transition to guardian/.

### Current Architecture
```
any-project/
├── claude-orchestrator/        # ✅ CURRENT - Self-contained working tool
│   ├── orchestrate.py         # Main coordination script
│   ├── brain/                 # Core logic (session management, etc.)
│   ├── resource-library/      # Templates and patterns
│   │   ├── documents/         # Handover templates, etc.
│   │   └── workflows/         # Process templates
│   ├── tools/                 # Context Guardian, utilities
│   └── short-term-memory/     # SQLite session state
│
├── .claude/                   # Active hooks and configuration
│   ├── commands/              # /session-start, /session-end definitions
│   └── hooks/                 # Active session management
│
├── docs/                      # Project documentation
│   └── status/                # Session handovers, progress tracking
│
└── [project files]           # Game code, assets, etc.
```

## Target Architecture (guardian/)

### Multi-Agent WezTerm Environment (Future)
```
WezTerm Terminal Multiplexer
├── Main Agent (Pane 1)           # Primary user interaction
│   ├── Handles user commands     # Including /session-start, /session-end
│   ├── Executes development tasks
│   └── Coordinates with helpers
│
├── Helper Agent 1 (Pane 2)       # Convention Enforcement
├── Helper Agent 2 (Pane 3)       # Workflow Monitoring  
├── Helper Agent N (Pane N)       # Specialized Support
│
└── System Monitor (Background)    # Status oversight
```

### Droppable Guardian System (Target)
```
any-project/
├── guardian/                   # 🎯 TARGET - Droppable multi-agent system
│   ├── setup.sh              # One-command installation
│   ├── mcp-server/            # Central coordination hub
│   │   ├── server.js          # Node.js MCP server
│   │   ├── lib/               # Component libraries  
│   │   └── db/                # SQLite coordination database
│   ├── agents/                # Helper agent implementations
│   │   ├── convention-enforcer/
│   │   ├── workflow-monitor/
│   │   └── documentation-maintainer/
│   ├── templates/             # Resource library for agent guidance
│   │   ├── conventions/       # What to enforce
│   │   ├── workflows/         # What to monitor
│   │   └── requirements/      # What to validate
│   ├── wezterm-integration/   # Terminal setup and automation
│   ├── background-layer/      # Non-blocking communication
│   └── migration-tools/       # Transition from claude-orchestrator
│
├── .guardian/                 # Project-specific state
│   ├── config.yaml           # Active agents, workflows
│   ├── session-state.db       # Current session data
│   └── agent-logs/           # Agent activity logs
│
├── .claude/                   # Maintained during transition
│   └── commands/             # /session-start → guardian equivalent
│
└── [project files]          # Unchanged project structure
```

## Communication Infrastructure

### Current System (File-based)
```
User → Claude → orchestrate.py → SQLite/Files → Results
```
**Status**: Working, reliable, currently used daily

### Target System (MCP-based)
```
┌─────────────────────────────────────────────────────────────┐
│                 WezTerm Multi-Pane Environment              │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Main Agent    │  Helper Agent 1 │    Helper Agent N       │
│   (Pane 1)      │   (Pane 2)      │     (Pane N)            │
└────────┬────────┴────────┬────────┴────────┬────────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                ┌──────────▼──────────┐
                │     MCP Server      │  ← Central coordination hub
                │   (Node.js/SQLite)  │
                └──────────┬──────────┘
                           │
                ┌──────────▼──────────┐
                │  SQLite Database    │  ← Shared state & context
                │   (coordination.db) │
                └─────────────────────┘
                           ▲
                           │
                ┌──────────▼──────────┐
                │ Background Polling  │  ← Non-blocking layer
                │   + Message Inject  │
                └─────────────────────┘
```

## Template-Driven Helper Agents

### Why Templates Are Essential
Helper agents cannot operate in the abstract - they need concrete guidance:
- **Convention Enforcer**: Needs specific naming rules, file organization patterns
- **Workflow Monitor**: Needs defined processes, milestones, quality gates  
- **Requirements Validator**: Needs acceptance criteria, scope definitions
- **Documentation Maintainer**: Needs templates, update patterns, formatting rules

### Template System Architecture
```
guardian/templates/
├── conventions/
│   ├── naming-rules.yaml      # Specific naming patterns to enforce
│   ├── file-organization.yaml # Directory structure requirements
│   └── code-standards.yaml    # Coding convention rules
│
├── workflows/
│   ├── game-development.yaml  # Game dev process steps
│   ├── feature-implementation.yaml # Feature workflow
│   └── bug-fixing.yaml        # Debugging process
│
├── requirements/
│   ├── acceptance-criteria.yaml # How to validate completeness
│   ├── scope-definitions.yaml  # Project boundary rules
│   └── quality-gates.yaml     # Milestone validation
│
└── documentation/
    ├── handover-template.md    # Session continuity format
    ├── status-report.md        # Progress report format
    └── architecture-doc.md     # Technical doc template
```

### Helper Agent Implementation Pattern
```python
class ConventionEnforcerAgent:
    def __init__(self):
        self.templates = TemplateLoader('guardian/templates/conventions/')
        self.naming_rules = self.templates.load('naming-rules.yaml')
        self.file_org_rules = self.templates.load('file-organization.yaml')
        
    def monitor_file_creation(self, filepath):
        """Check new files against naming conventions"""
        violations = []
        for rule in self.naming_rules:
            if not rule.validate(filepath):
                violations.append(rule.get_violation_message(filepath))
        
        if violations:
            self.notify_main_agent(violations)
```

## Current Implementation Status

### ✅ Working & Used Daily (claude-orchestrator/)
- **Session Management**: /session-start, /session-end commands
- **Handover System**: Session continuity and progress tracking
- **Context Guardian**: Token monitoring and overflow prevention
- **File Coordination**: SQLite state management
- **Resource Library**: Templates for documents and workflows

### 🔄 Active Development (guardian/)
- **MCP Server Foundation**: Node.js server with SQLite backend
- **Agent Registration**: Basic agent discovery and status tracking
- **Message Broker**: Inter-agent communication framework
- **Background Polling**: Non-blocking message delivery layer
- **WezTerm Integration**: Multi-pane test environment

### 📋 Planned Components (guardian/)
- **Agent Status Monitoring**: Busy/free detection for intelligent routing
- **Template-Driven Agents**: Convention enforcer, workflow monitor, etc.
- **Migration Tools**: Seamless transition from claude-orchestrator
- **Professional UI**: Enhanced WezTerm configuration and automation
- **Droppable Installation**: One-command setup for any project

## Migration Strategy

### Phase 1: Parallel Development (Current)
- ✅ Keep claude-orchestrator/ working and actively used
- 🔄 Build guardian/ foundation without disrupting current workflow
- 📋 Test guardian/ components in isolation

### Phase 2: Feature Parity (Next)
- 🎯 Implement /session-start, /session-end equivalents in guardian/
- 🎯 Migrate handover system to guardian/ multi-agent model
- 🎯 Port Context Guardian as helper agent
- 🎯 Create migration tools for seamless transition

### Phase 3: Enhanced Capabilities (Future)
- 🔮 Deploy specialized helper agents with template guidance
- 🔮 Add vector database for long-term knowledge accumulation
- 🔮 Implement intelligent message routing and agent coordination
- 🔮 Professional multi-agent development environment

### Phase 4: Full Migration (Future)
- 🔮 Guardian/ provides all claude-orchestrator/ functionality plus multi-agent
- 🔮 Archive claude-orchestrator/ as legacy (with full preservation)
- 🔮 Guardian/ becomes the standard droppable orchestration tool

## System Flow

### Current Flow (claude-orchestrator/)
```
User types /session-start
    ↓
.claude/commands/session-start.md → "execute orchestrate.py session_start"
    ↓
claude-orchestrator/orchestrate.py session_start
    ↓
claude-orchestrator/brain/session_manager.py
    ↓
Updates SQLite databases + Creates handover document
```

### Target Flow (guardian/)
```
User types /session-start in Main Agent (Pane 1)
    ↓
Guardian session manager initializes multi-agent environment
    ↓
Spawns helper agents in WezTerm panes 2-N
    ↓
Each helper agent registers with MCP server
    ↓
Background polling layer starts for each agent
    ↓
Template-driven monitoring begins
    ↓
Main agent proceeds with development work
    ↓
Helper agents provide continuous support and validation
```

## Integration Requirements

### Preserve Current Productivity
**Critical**: Guardian must not disrupt current daily workflow
**Approach**: 
- Parallel development until feature parity achieved
- Migration tools to transfer state and configuration
- Backward compatibility during transition period

### Template Migration
**Challenge**: Extract patterns from claude-orchestrator/resource-library/
**Solution**:
```bash
guardian/migration-tools/extract-templates.py
# Converts existing resource-library/ to guardian/templates/
# Maps current workflows to helper agent guidance
# Preserves institutional knowledge and patterns
```

### Installation Simplicity
**Requirement**: Guardian must be as easy to install as claude-orchestrator
**Target**:
```bash
# Copy guardian folder to any project
cp -r /path/to/guardian /path/to/my-project/

# One-command setup
cd my-project/guardian
./setup.sh --project-type game-dev

# Guardian configures:
# - WezTerm panes and session
# - Helper agents based on project type
# - Templates appropriate for domain
# - MCP server and background layer
# - Migration from existing claude-orchestrator (if present)
```

## Technology Stack

### Current Stack (claude-orchestrator/)
- **Language**: Python (orchestrate.py, brain/, tools/)
- **Database**: SQLite (session state, handovers)
- **Coordination**: File-based with background processes
- **Interface**: Single Claude instance with command hooks

### Target Stack (guardian/)
- **MCP Server**: Node.js with SQLite backend
- **Background Layer**: Python polling processes + bash injection
- **Agent Communication**: MCP protocol + SQLite message queues
- **Interface**: WezTerm multi-pane with specialized agents
- **Templates**: YAML configuration + Markdown patterns

### Transition Considerations
**Challenge**: Different technology stacks between current and target
**Solution**: Guardian includes compatibility layer for current tools
```python
# guardian/compatibility/claude-orchestrator-bridge.py
# Provides current orchestrate.py functionality
# Routes to appropriate guardian/ components
# Maintains API compatibility during transition
```

## Success Metrics

### Transition Success
- ✅ Current productivity maintained throughout transition
- ✅ All current functionality preserved in guardian/
- ✅ Droppable installation works reliably
- ✅ Template system guides helper agents effectively

### Multi-Agent Coordination
- 🎯 3+ agents working simultaneously without conflicts
- 🎯 Helper agents provide value through template-driven monitoring
- 🎯 Non-blocking communication maintains main agent responsiveness
- 🎯 Message routing intelligence prevents information overload

### Long-term Sustainability
- 🔮 Project standards maintained automatically over weeks/months
- 🔮 Knowledge accumulation through vector database integration
- 🔮 Reduced development friction through specialized agent support
- 🔮 Enhanced productivity through true multi-agent orchestration

---

## Summary

This architecture reflects the **current reality of a working system evolving toward multi-agent capabilities**. The claude-orchestrator/ system provides essential daily productivity that must be preserved, while guardian/ represents the future vision of template-driven helper agents coordinated through MCP infrastructure.

**Key principles**:
1. **Evolution, not revolution** - Build on what works
2. **Droppable deployment** - Guardian maintains portability
3. **Template-driven behavior** - Helper agents need concrete guidance
4. **Parallel development** - No disruption to current workflow
5. **Seamless migration** - Tools to transition smoothly

The architecture acknowledges both where we are (working single-agent system) and where we're going (multi-agent coordination platform) while providing a clear path between them.

---
*This document reflects the current transition state and will require refinement as guardian/ implementation progresses.*

## Core Architecture

### Multi-Agent WezTerm Environment
```
WezTerm Terminal Multiplexer
├── Main Agent (Pane 1)           # Primary user interaction
│   ├── Handles user commands
│   ├── Executes development tasks
│   └── Coordinates with helpers
│
├── Helper Agent 1 (Pane 2)       # Convention Enforcement
├── Helper Agent 2 (Pane 3)       # Workflow Monitoring  
├── Helper Agent N (Pane N)       # Specialized Support
│
└── System Monitor (Background)    # Status oversight
```

### Communication Infrastructure
```
┌─────────────────────────────────────────────────────────────┐
│                 WezTerm Multi-Pane Environment              │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Main Agent    │  Helper Agent 1 │    Helper Agent N       │
│   (Pane 1)      │   (Pane 2)      │     (Pane N)            │
└────────┬────────┴────────┬────────┴────────┬────────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                ┌──────────▼──────────┐
                │     MCP Server      │  ← Central coordination hub
                │   (Node.js/SQLite)  │
                └──────────┬──────────┘
                           │
                ┌──────────▼──────────┐
                │  SQLite Database    │  ← Shared state & context
                │   (coordination.db) │
                └─────────────────────┘
                           ▲
                           │
                ┌──────────▼──────────┐
                │ Background Polling  │  ← Non-blocking layer
                │   + Message Inject  │
                └─────────────────────┘
```

## System Components

### 1. Main Agent
**Role**: Primary user interface and development work
**Location**: WezTerm Pane 1
**Responsibilities**:
- Handle all user commands and interactions
- Execute primary development tasks (coding, debugging, etc.)
- Request support from helper agents when needed
- Maintain session context and continuity

**Communication Pattern**:
- Receives user input directly
- Sends coordination messages via MCP server
- Gets notifications from helper agents via background injection

### 2. Helper Agents (Multiple Specialized)
**Role**: Monitor, support, and enforce standards
**Location**: WezTerm Panes 2-N
**Types**:

#### Convention Enforcer Agent
- **Purpose**: Ensure naming conventions and file organization
- **Monitors**: File creation, directory structure, naming patterns
- **Actions**: Alert main agent of violations, suggest corrections

#### Workflow Monitor Agent  
- **Purpose**: Track adherence to defined development processes
- **Monitors**: Task completion, phase transitions, quality gates
- **Actions**: Validate milestones, report deviations, suggest next steps

#### Requirements Validator Agent
- **Purpose**: Ensure implementation matches requirements
- **Monitors**: Feature completeness, scope changes, acceptance criteria
- **Actions**: Flag requirement conflicts, validate deliverables

#### Documentation Maintenance Agent
- **Purpose**: Keep documentation current and accurate
- **Monitors**: Code changes, architectural decisions, status updates
- **Actions**: Update docs, generate reports, maintain handovers

### 3. MCP Server (Central Coordination)
**Technology**: Node.js with SQLite backend
**Location**: `guardian/mcp-server/`
**Components**:
- **AgentRegistry.js**: Track agent registration and status
- **MessageBroker.js**: Route messages between agents
- **DatabaseManager.js**: SQLite database abstraction
- **FileMonitor.js**: Watch for file-based coordination signals

**Database Schema**:
```sql
-- Agent registration and status
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    name TEXT,
    role TEXT,
    status TEXT,           -- 'busy', 'free', 'offline'
    workspace_path TEXT,
    last_seen TIMESTAMP
);

-- Inter-agent messages
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    from_agent TEXT,
    to_agent TEXT,
    message_type TEXT,
    content TEXT,
    urgency TEXT,          -- 'low', 'medium', 'high'
    delivered BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP
);

-- Shared context and project state
CREATE TABLE context_store (
    key TEXT PRIMARY KEY,
    value TEXT,
    agent_id TEXT,
    category TEXT,         -- 'session', 'project', 'temporary'
    timestamp TIMESTAMP
);
```

### 4. Non-Blocking Communication Layer
**Purpose**: Prevent agents from blocking during communication
**Implementation**: Background processes + message injection

#### Background Polling Process
```python
class BackgroundPoller:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.mcp_client = MCPClient()
        
    def monitor_messages(self):
        """Continuously poll MCP for new messages"""
        while True:
            messages = self.mcp_client.get_pending_messages(self.agent_id)
            for message in messages:
                self.handle_message(message)
            time.sleep(1)  # Non-blocking polling interval
            
    def handle_message(self, message):
        """Route message based on urgency and agent status"""
        if message.urgency == 'high' or self.agent_is_free():
            self.inject_notification(message)
        else:
            self.queue_for_later(message)
```

#### Message Injection Mechanism
```bash
# monitor_and_inject.sh - Injects messages into WezTerm panes
#!/bin/bash
AGENT_ID="$1"
MESSAGE="$2"

# Find WezTerm pane for this agent
PANE_ID=$(wezterm cli list-panes --format json | jq -r ".[] | select(.title | contains(\"$AGENT_ID\")) | .pane_id")

# Inject notification into agent's terminal
if [ -n "$PANE_ID" ]; then
    echo "🔔 $MESSAGE" | wezterm cli send-text --pane-id "$PANE_ID"
fi
```

### 5. Agent Status Monitoring (Planned)
**Purpose**: Intelligent message routing based on agent availability
**Implementation**: Monitor agent activity and queue management

```python
class AgentStatusMonitor:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.last_activity = time.time()
        self.current_task = None
        
    def detect_busy_state(self):
        """Determine if agent is currently busy"""
        # Methods to implement:
        # 1. Monitor typing activity in terminal
        # 2. Check for running processes
        # 3. Look for explicit status commands
        # 4. Timeout-based inference
        
    def update_status(self, status, details=None):
        """Broadcast status to MCP server"""
        self.mcp_client.update_agent_status(
            self.agent_id, status, details
        )
```

## Project Structure

### Current Dual Implementation
```
claude-orchestrate/
├── docs/                        # Project documentation
│   ├── design/vision.md         # Current architectural vision
│   ├── technical/architecture.md # This document
│   └── status/                  # Session management
│
├── guardian/                    # ✅ CURRENT - Next generation system  
│   ├── mcp-server/             # Node.js MCP server implementation
│   │   ├── server.js           # Main MCP server
│   │   ├── lib/                # Component libraries
│   │   └── db/                 # SQLite database
│   ├── tests/                  # Working test examples
│   │   ├── test2-hybrid/       # Multi-agent test setup
│   │   └── setup_wezterm_test2.sh
│   └── utils/                  # Background polling utilities
│       ├── monitor_and_inject.sh
│       └── orchestrate.py
│
└── claude-orchestrator/        # 🔄 LEGACY - Being migrated
    ├── __proposed_refactoring/ # Breakthrough documentation
    ├── orchestrator-tools/     # Legacy parallel execution proof
    ├── brain/                  # Outdated orchestrator model
    ├── resource-library/       # Some useful templates
    └── tools/                  # Context Guardian (to be migrated)
```

### Target Structure (Guardian Maturation)
```
guardian/                       # Main system implementation
├── mcp-server/                # Central coordination server
├── agents/                    # Helper agent implementations
│   ├── convention-enforcer/
│   ├── workflow-monitor/
│   ├── requirements-validator/
│   └── documentation-maintainer/
├── background-layer/          # Non-blocking communication
│   ├── polling/              # MCP polling processes
│   ├── injection/            # Message injection scripts
│   └── status-monitoring/    # Agent status detection
├── wezterm-integration/       # Terminal setup and management
├── tests/                     # Test environments and validation
└── utils/                     # Utilities and helper scripts
```

## Implementation Status

### ✅ Completed Components
- **MCP Server Foundation**: Working Node.js server with SQLite
- **Agent Registration**: AgentRegistry.js handles agent discovery
- **Message Broker**: MessageBroker.js routes inter-agent messages  
- **Background Polling**: monitor_and_inject.sh provides non-blocking layer
- **WezTerm Integration**: Test setup demonstrates multi-pane coordination
- **Database Schema**: SQLite tables for agents, messages, context

### 🎯 Active Development
- **Agent Status Monitoring**: Design and implementation of busy/free detection
- **Message Urgency System**: Priority classification and intelligent routing
- **Helper Agent Framework**: Standardized pattern for specialized agents
- **WezTerm Automation**: Enhanced setup and pane management

### 📋 Planned Components  
- **Specialized Helper Agents**: Convention enforcer, workflow monitor, etc.
- **Long-term Memory**: Vector database integration for accumulated knowledge
- **Professional UI**: Enhanced WezTerm configuration and monitoring
- **Migration Tools**: Automated transition from claude-orchestrator/ to guardian/

## System Flow

### Agent Registration Flow
```
1. Agent starts in WezTerm pane
2. Agent registers with MCP server (agent ID, role, workspace)
3. MCP server stores in agents table
4. Background poller starts for this agent
5. Agent becomes available for coordination
```

### Message Flow
```
1. Agent A sends message to Agent B via MCP server
2. MCP server stores in messages table
3. Background poller for Agent B detects new message
4. Poller checks Agent B status (busy/free)
5. If free or urgent: inject notification into Agent B's WezTerm pane
6. If busy and non-urgent: queue for later delivery
7. Agent B processes notification and responds
```

### Context Sharing Flow  
```
1. Agent stores context in MCP server (key-value pairs)
2. Other agents query context via MCP server
3. Shared context available across all agents
4. Context categorized: session, project, temporary
5. Automatic cleanup of temporary context
```

## Non-Blocking Architecture Details

### The Blocking Problem (Solved)
**Traditional approach**: Agent calls MCP server and waits for response
**Problem**: Main agent becomes unresponsive during coordination
**Impact**: Poor user experience, no true parallelization

### The Non-Blocking Solution
**Approach**: Background processes handle all MCP communication
**Implementation**: Polling + message injection pattern
**Result**: Main agent stays responsive, true multi-agent coordination

### Message Urgency Classification
```python
class MessageRouter:
    def classify_urgency(self, message):
        """Determine message priority"""
        urgent_keywords = ['error', 'critical', 'stop', 'urgent']
        normal_keywords = ['status', 'update', 'info']
        
        if any(keyword in message.content.lower() for keyword in urgent_keywords):
            return 'high'
        elif message.type in ['status_update', 'info']:
            return 'low'
        else:
            return 'medium'
            
    def route_message(self, message):
        """Route based on urgency and agent status"""
        urgency = self.classify_urgency(message)
        agent_status = self.get_agent_status(message.to_agent)
        
        if urgency == 'high' or agent_status == 'free':
            self.deliver_immediately(message)
        else:
            self.queue_message(message)
```

## Integration with Existing Systems

### Legacy claude-orchestrator/ Integration
**Valuable patterns to preserve**:
- **Parallel execution**: `run_in_background=True` breakthrough
- **Visual monitoring**: tmux dashboard concepts
- **Context Guardian**: Token monitoring and overflow prevention
- **Test evidence**: Breakthrough documentation and proof-of-concepts

**Migration strategy**:
1. Extract useful patterns from orchestrator-tools/
2. Implement Context Guardian as helper agent in guardian/
3. Adapt visual monitoring for WezTerm multi-pane setup
4. Archive legacy components while preserving breakthrough documentation

### Future Vector Database Integration
**Purpose**: Long-term knowledge accumulation across sessions
**Integration point**: Additional MCP server component
**Implementation**: 
```python
class VectorMemory:
    def __init__(self, mcp_server):
        self.mcp = mcp_server
        self.vector_db = ChromaDB()  # or similar
        
    def store_session_knowledge(self, session_data):
        """Extract and store key insights from session"""
        embeddings = self.extract_embeddings(session_data)
        self.vector_db.store(embeddings)
        
    def retrieve_relevant_context(self, query):
        """Find relevant past insights for current work"""
        return self.vector_db.similarity_search(query)
```

## Development Phases

### Phase 1: Core Agent Status Monitoring (Immediate)
- **Goal**: Implement reliable busy/free detection for agents
- **Tasks**:
  - [ ] Design status detection mechanisms
  - [ ] Implement status broadcasting to MCP
  - [ ] Create status monitoring dashboard  
  - [ ] Test with 2-3 agents in WezTerm

### Phase 2: Intelligent Message Routing (Short-term)
- **Goal**: Route messages based on urgency and agent availability
- **Tasks**:
  - [ ] Implement message urgency classification
  - [ ] Build message queuing system
  - [ ] Create interrupt mechanism for urgent messages
  - [ ] Test urgency handling scenarios

### Phase 3: Helper Agent Framework (Medium-term)
- **Goal**: Deploy specialized helper agents
- **Tasks**:
  - [ ] Convention enforcer agent implementation
  - [ ] Workflow monitor agent implementation
  - [ ] Requirements validator agent implementation
  - [ ] Documentation maintenance agent implementation

### Phase 4: Long-term Memory Integration (Future)
- **Goal**: Add vector database for knowledge accumulation
- **Tasks**:
  - [ ] Select and integrate vector database
  - [ ] Implement semantic search capabilities
  - [ ] Create automated knowledge extraction
  - [ ] Build cross-session learning system

## Success Metrics

### Technical Performance
- **Non-blocking communication**: 0 instances of main agent blocking
- **Message delivery latency**: <1 second for urgent, <30 seconds for normal
- **Agent status accuracy**: >95% correct busy/free detection
- **System stability**: 8+ hours continuous operation without issues

### User Experience
- **Multi-agent coordination**: 3+ agents working simultaneously without conflicts
- **Convention adherence**: Automated detection and correction of violations
- **Workflow compliance**: Process deviations caught and addressed
- **Knowledge retention**: Relevant past insights automatically surfaced

### Long-term Goals
- **Project consistency**: Standards maintained over weeks/months
- **Knowledge accumulation**: Continuous learning from each session
- **Error reduction**: Fewer repeated mistakes through helper agent monitoring
- **Development efficiency**: Faster iteration through multi-agent support

---

## Summary

This architecture represents a fundamental shift from single-agent development to **collaborative multi-agent orchestration**. The system leverages breakthrough non-blocking communication technology to enable true parallel agent coordination while maintaining responsive user interaction.

**Key innovations**:
1. **Multi-agent WezTerm environment** for professional development interface
2. **MCP server with SQLite** for centralized coordination and state management  
3. **Background polling + message injection** for non-blocking communication
4. **Specialized helper agents** for automated monitoring and enforcement
5. **Intelligent message routing** based on urgency and agent availability

The architecture is designed for **long-term project sustainability**, enabling consistent standards and accumulated knowledge across extended development periods.

---
*This document reflects the current architectural vision with proven technology foundation and clear implementation roadmap.*