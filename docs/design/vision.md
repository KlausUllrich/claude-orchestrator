---
project: claude-orchestrate
type: vision
title: "Claude Orchestrate - Vision & Design Document (Current Architecture)"
version: 2025-08-14
status: CURRENT
summary:
  - Multi-agent WezTerm system with main + helper agents
  - Non-blocking MCP communication with background polling layer
  - SQLite database for context sharing between agents
  - Helper agents monitor and support main agent
  - Long-term vector database planned
tags: [vision, architecture, multi-agent, wezterm, mcp, non-blocking]
---

# Claude Orchestrate - Vision Document

## Mission Statement

Create a multi-agent orchestration system running in WezTerm where multiple Claude agents work together to support long-term game development projects. The main agent handles user interaction while helper agents monitor, support, and ensure adherence to requirements, workflows, and conventions over extended development periods.

## Current Architecture Plan

### Core System Design

```
WezTerm Environment
├── Main Agent (User Interaction)
│   ├── Primary development work
│   ├── User communication
│   └── Task execution
│
├── Helper Agents (Support & Monitoring)
│   ├── Convention enforcement
│   ├── Workflow monitoring
│   ├── Requirements validation
│   ├── Documentation maintenance
│   └── Quality assurance
│
└── Optional Orchestrator Agent
    ├── Task coordination
    ├── Agent management
    └── System oversight
```

### Communication Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Main Agent    │    │  Helper Agent 1 │    │  Helper Agent N │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                     ┌──────────▼──────────┐
                     │    MCP Server       │
                     │   (Registration     │
                     │   & Communication)  │
                     └──────────┬──────────┘
                                │
                     ┌──────────▼──────────┐
                     │   SQLite Database   │
                     │  (Context Sharing   │
                     │   & State Storage)  │
                     └─────────────────────┘

Background Polling Layer (Non-Blocking)
├── Polls MCP for updates
├── Monitors agent status (busy/free)
├── Handles message urgency
│   ├── Non-urgent: Wait until agent free
│   └── Urgent: Interrupt agent immediately
└── Injects notifications to agents
```

## Breakthrough Technology Components

### 1. ✅ MCP Server Foundation
**Purpose**: Central communication hub for all agents
**Status**: Working implementation in guardian/mcp-server/
**Features**:
- Agent registration and discovery
- Message passing between agents
- SQLite database integration
- Persistent state management

### 2. ✅ Non-Blocking Communication Layer
**Purpose**: Prevent agents from blocking during communication
**Implementation**: Background polling + message injection
**Components**:
- **Background Polling**: Separate process monitors MCP for updates
- **Message Injection**: Injects notifications into agent terminals
- **Agent Status Monitoring**: Tracks busy/free state (TO BE IMPLEMENTED)
- **Urgency Handling**: Routes messages based on priority (TO BE IMPLEMENTED)

### 3. ✅ SQLite Context Sharing
**Purpose**: Share context and state between all agents
**Implementation**: Central database accessible via MCP
**Features**:
- Session state persistence
- Inter-agent message history
- Shared project context
- Task coordination data

### 4. 🎯 Agent Status Awareness (PLANNED)
**Purpose**: Intelligent message routing based on agent availability
**Components**:
- **Busy Detection**: Monitor when agents are actively working
- **Message Queue**: Hold non-urgent messages for busy agents
- **Interrupt Capability**: Force urgent messages through immediately
- **Status Broadcasting**: Keep all agents aware of system state

### 5. 🔮 Long-Term Memory (FUTURE)
**Purpose**: Vector database for accumulated project knowledge
**Implementation**: Integration with existing MCP/SQLite system
**Features**:
- Semantic search across all sessions
- Pattern recognition in development
- Solution library accumulation
- Cross-project learning

## Agent Roles & Responsibilities

### Main Agent
**Primary Role**: User interaction and development work
**Responsibilities**:
- Handle all user commands and requests
- Execute primary development tasks
- Coordinate with helper agents when needed
- Maintain session continuity

### Helper Agents (Multiple)
**Primary Role**: Support and monitoring
**Specific Responsibilities**:

#### Convention Enforcer Agent
- Monitor for naming convention violations
- Ensure file organization standards
- Validate documentation structure
- Report deviations to main agent

#### Workflow Monitor Agent
- Track adherence to defined processes
- Validate task completion criteria
- Monitor project phase transitions
- Ensure quality gates are met

#### Requirements Validator Agent
- Check implementation against requirements
- Monitor scope creep and changes
- Validate acceptance criteria
- Report requirement conflicts

#### Documentation Maintenance Agent
- Keep documentation current and accurate
- Generate automated status reports
- Maintain knowledge base
- Update handover documents

### Orchestrator Agent (Optional)
**Primary Role**: System coordination (if implemented)
**Responsibilities**:
- Manage agent spawning and lifecycle
- Coordinate complex multi-agent tasks
- Handle system-level decisions
- Provide oversight and control

## Technical Implementation

### WezTerm Environment
**Why WezTerm**: 
- Superior terminal multiplexing
- Professional development interface
- Tab/pane management for multiple agents
- Visual monitoring capabilities

### MCP Server (guardian/mcp-server/)
**Technology**: Node.js with SQLite
**Features**:
- Agent registration endpoint
- Message routing system
- Database abstraction layer
- Real-time communication handling

### Background Polling Layer
**Implementation**: Python/Node.js background processes
**Architecture**:
```python
class BackgroundPoller:
    def monitor_mcp_updates(self):
        # Continuously poll MCP for new messages
        
    def check_agent_status(self, agent_id):
        # Determine if agent is busy or free
        
    def route_message(self, message, urgency):
        if urgency == "high" or agent.is_free():
            self.inject_notification(agent_id, message)
        else:
            self.queue_message(agent_id, message)
```

### SQLite Database Schema
```sql
-- Agent registration and status
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    name TEXT,
    role TEXT,
    status TEXT, -- 'busy', 'free', 'offline'
    last_seen TIMESTAMP
);

-- Inter-agent messages
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    from_agent TEXT,
    to_agent TEXT,
    content TEXT,
    urgency TEXT, -- 'low', 'medium', 'high'
    delivered BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP
);

-- Shared context and state
CREATE TABLE context_store (
    key TEXT PRIMARY KEY,
    value TEXT,
    agent_id TEXT,
    timestamp TIMESTAMP
);
```

## Development Phases

### Phase 1: Agent Status Monitoring (IMMEDIATE)
**Goal**: Implement busy/free detection for agents
**Tasks**:
- [ ] Design agent status detection mechanism
- [ ] Implement status broadcasting to MCP
- [ ] Create status monitoring dashboard
- [ ] Test with 2-3 agents

### Phase 2: Intelligent Message Routing (SHORT-TERM)
**Goal**: Route messages based on urgency and agent status
**Tasks**:
- [ ] Implement message urgency classification
- [ ] Build message queuing system
- [ ] Create interrupt mechanism for urgent messages
- [ ] Test urgency handling scenarios

### Phase 3: Helper Agent Implementation (MEDIUM-TERM)
**Goal**: Deploy specialized helper agents
**Tasks**:
- [ ] Convention enforcer agent
- [ ] Workflow monitor agent
- [ ] Requirements validator agent
- [ ] Documentation maintenance agent

### Phase 4: Long-Term Memory Integration (FUTURE)
**Goal**: Add vector database for knowledge accumulation
**Tasks**:
- [ ] Select and integrate vector database
- [ ] Implement semantic search
- [ ] Create knowledge extraction from sessions
- [ ] Build cross-session learning

## Success Metrics

### Technical Metrics
- ✅ **Non-blocking communication**: Agents never block waiting for responses
- 🎯 **Agent status accuracy**: >95% correct busy/free detection
- 🎯 **Message delivery**: <1 second for urgent, <30 seconds for normal
- 🎯 **System stability**: 8+ hours continuous operation without issues

### User Experience Metrics
- ✅ **Multi-agent coordination**: 3+ agents working simultaneously
- 🎯 **Convention adherence**: Automated violation detection and correction
- 🎯 **Long-term consistency**: Project standards maintained over weeks/months
- 🎯 **Knowledge retention**: Previous session insights accessible and applied

### Project Management Metrics
- 🎯 **Requirements compliance**: Automated validation of implementation
- 🎯 **Documentation accuracy**: Always current and conflict-free
- 🎯 **Workflow adherence**: Process deviations caught and corrected
- 🎯 **Quality assurance**: Consistent standards across all development

## Current Implementation Status

### ✅ Completed Components
- **MCP Server**: Working implementation with SQLite integration
- **Basic Non-blocking**: Background polling and message injection proven
- **WezTerm Integration**: Test environment operational
- **Multi-agent Coordination**: 3+ agents proven working

### 🎯 Active Development
- **Agent Status Monitoring**: Design phase
- **Message Urgency System**: Planning phase
- **Helper Agent Framework**: Prototyping
- **Professional UI**: WezTerm optimization

### 📋 Planned Components
- **Orchestrator Agent**: Architecture design needed
- **Vector Database**: Technology selection and integration
- **Cross-session Learning**: Knowledge extraction automation
- **Team Collaboration**: Multi-user support

## Architecture Decisions

### ✅ Confirmed Decisions
- **Platform**: WezTerm for professional multi-agent interface
- **Communication**: MCP server with SQLite backend
- **Non-blocking**: Background polling + message injection pattern
- **Language**: Node.js for MCP, Python for background processes
- **Database**: SQLite for simplicity and reliability

### 🎯 Current Decisions Under Development
- **Agent Status Detection**: Method for determining busy/free state
- **Message Urgency**: Classification and routing algorithms
- **Helper Agent Framework**: Standard pattern for specialized agents
- **Orchestrator Role**: Whether to implement centralized coordination

### 📋 Future Decisions
- **Vector Database**: Local vs cloud, technology selection
- **Knowledge Extraction**: Automated vs manual promotion of insights
- **Team Features**: Multi-user collaboration approach
- **Cross-project**: Learning and pattern sharing between projects

## Integration with Existing Systems

### Guardian System (guardian/)
- **Current**: Next-generation MCP-based architecture
- **Status**: Working foundation with test validation
- **Evolution**: Becoming the main implementation platform

### Claude-Orchestrator (claude-orchestrator/)
- **Current**: Stable working system with proven capabilities
- **Status**: Legacy system with valuable patterns
- **Future**: Knowledge extraction and migration to guardian/

### Project Documentation
- **Current**: Organized in docs/ with clear conventions
- **Integration**: Helper agents will maintain and validate
- **Enhancement**: Automated accuracy and consistency checking

## Long-Term Vision

### Project Sustainability
**Goal**: Maintain large game development projects over months/years
**Approach**: 
- Helper agents prevent drift and decay
- Automated convention enforcement
- Continuous knowledge accumulation
- Long-term memory and pattern recognition

### Multi-Project Learning
**Goal**: Accumulate wisdom across multiple projects
**Approach**:
- Vector database with cross-project search
- Pattern library of successful solutions
- Automated application of proven approaches
- Continuous improvement of helper agents

### Team Collaboration
**Goal**: Support multiple developers on same project
**Approach**:
- Shared MCP server with multi-user support
- Role-based agent permissions
- Conflict resolution mechanisms
- Collaborative knowledge building

---

## Current Challenges

### Technical Challenges
1. **Agent Status Detection**: Reliable method to determine when agents are busy
2. **Message Urgency Classification**: Automated priority determination
3. **Context Synchronization**: Ensuring all agents have current project state
4. **Performance**: Maintaining responsiveness with multiple active agents

### Implementation Challenges
1. **Helper Agent Specialization**: Defining clear roles and boundaries
2. **User Experience**: Balancing automation with user control
3. **System Complexity**: Managing increasing number of components
4. **Migration Strategy**: Moving from claude-orchestrator to guardian

### Long-term Challenges
1. **Knowledge Accumulation**: Preventing information overload
2. **Agent Coordination**: Avoiding conflicts between helper agents
3. **System Evolution**: Adapting to changing development needs
4. **Maintenance**: Keeping the system itself well-maintained

---

*This vision represents the current architecture plan based on proven breakthrough technology and real implementation experience. The focus is on practical, working multi-agent coordination with intelligent support systems.*

**Last Updated**: August 2025 - Reflects current MCP-based architecture with WezTerm multi-agent plan