# Proposed Architecture: Mixed Approach with Guardian System

## Overview

This architecture combines the best of what we've learned: Python for reliability, agents for flexibility, Guardian for enforcement, and dashboard for visibility. It also incorporates the full vision including memory systems, token tracking, and knowledge management. However, **implementation depends on proving autonomous agent execution first**.

## Core Architecture Principles

### 1. **Layered Enforcement**
- Soft guidance through patterns and examples
- Hard enforcement through Guardian vetos
- Visibility through dashboard monitoring

### 2. **Transparent Operations**
- Visible state in JSON/Markdown files
- No hidden Python complexity for logic
- Clear audit trail of all decisions

### 3. **Mixed Technology Use**
- Python: File I/O, validation, state management
- Agents: Complex reasoning and decisions
- Web: Real-time monitoring
- SQLite: Reliable state storage and agent communication
- Vector DB: Long-term knowledge retrieval

### 4. **Memory Hierarchy**
- Short-term: SQLite for session state and agent communication
- Long-term: Vector DB for project knowledge
- Knowledge Base: Searchable patterns and solutions

## System Components

### Layer 1: Core Infrastructure

```
.orchestrator/
├── state/                      # Visible state files
│   ├── session.json           # Current session state
│   ├── tasks.json             # Task queue
│   └── agents.json            # Active agents status
├── monitor/                    # Monitoring files
│   ├── activity.md            # Human-readable log
│   ├── alerts.md              # Guardian interventions
│   └── metrics.json           # Performance data
├── coordinator/               # Coordination logic
│   ├── queue.py               # Simple task queue
│   ├── validator.py           # Input validation
│   └── state_manager.py       # State persistence
└── token-tracker/             # Token usage monitoring
    ├── estimator.py           # Token estimation logic
    ├── checkpoint-trigger.py  # Auto-checkpoint system
    └── usage-stats.json       # Usage metrics
```

### Layer 2: Memory Systems

```
Short-Term Memory (SQLite)
├── session_state.db
│   ├── current_context        # What's happening now
│   ├── active_rules          # Rules being enforced
│   ├── recent_decisions      # Decisions this session
│   └── checkpoints           # Session snapshots
├── message_queue.db
│   ├── agent_messages        # Inter-agent communication
│   ├── pending_tasks         # Task coordination
│   └── shared_state          # Shared data between agents
└── hard_facts.db
    ├── api_documentation      # API references
    ├── tool_capabilities      # What tools can do
    ├── project_constants      # Unchanging project facts
    └── verified_patterns      # Proven code patterns

Long-Term Memory (Vector DB/Knowledge System)
├── knowledge_base/
│   ├── embeddings.db         # Vector embeddings
│   ├── code_patterns/        # Successful patterns
│   ├── bug_solutions/        # How bugs were fixed
│   ├── decisions/            # Architectural decisions
│   └── session_learnings/    # Extracted knowledge
├── bug_patterns.db
│   ├── symptoms              # How bugs manifest
│   ├── root_causes           # Why they happened
│   ├── solutions             # How they were fixed
│   └── prevention            # How to avoid them
└── retrieval_engine.py       # Semantic search interface
```

### Layer 3: Agent System

```
Main Agent (Primary Worker)
├── Executes user tasks
├── Launches sub-agents
├── Continues working (if autonomous execution works)
├── Queries long-term memory for context
└── Subject to Guardian oversight

Guardian Agent (Enforcer)
├── Reviews ALL actions
├── Has veto power
├── Cannot be dismissed
├── Maintains rule consistency
└── Reports to dashboard

Sub-Agents (Specialists)
├── Parallel task execution
├── Domain-specific work
├── Report back asynchronously
├── Can query memory systems
└── Also monitored by Guardian

Translator Agent (Humanizer)
├── Converts technical to human-readable
├── Maintains dashboard narratives
├── Groups related activities
└── Provides context

Memory Curator Agent (Knowledge Manager)
├── Extracts learnings from sessions
├── Updates knowledge base
├── Maintains bug patterns
├── Indexes new information
└── Cleans outdated knowledge
```

### Layer 4: Monitoring & Control

```
Web Dashboard (localhost:8080)
├── Real-time activity display
├── Human-readable status
├── Guardian interventions
├── Progress tracking
├── Token usage monitor
├── Memory system status
└── User controls

WebSocket Server
├── Streams agent activities
├── Broadcasts Guardian decisions
├── Handles user interventions
├── Token usage alerts
└── Maintains connections
```

## Critical Components Detail

### 1. Autonomous Execution System (MUST PROVE FIRST)

```python
class AutonomousAgentLauncher:
    """
    The critical component we must prove works
    """
    
    def launch_autonomous_agent(self, agent_type, task):
        """
        Launch agent that runs independently
        Main agent MUST be able to continue
        """
        # Option 1: Background process with file communication
        # Option 2: MCP server with async handling
        # Option 3: Webhook callbacks
        # MUST TEST WHICH WORKS
        
    def collect_results_async(self):
        """
        Gather results without blocking
        """
        # Check completion signals
        # Read results from files/database
        # Return immediately if not ready
```

### 2. Token Tracking System

```python
class TokenTracker:
    """
    Since we can't access Claude's actual tokens,
    we estimate and track manually
    """
    
    def __init__(self):
        self.estimation_model = self.load_estimation_rules()
        self.usage_log = []
        self.checkpoint_thresholds = [70, 80, 90]  # Percentage triggers
        
    def estimate_tokens(self, content):
        """
        Estimate token usage from content
        """
        # Rough estimation: ~1.3 tokens per word
        # Plus overhead for tool calls
        # Plus context window base usage
        
    def track_file_operation(self, operation, file_path, content_size):
        """
        Track token usage for file operations
        """
        estimated = self.estimate_operation_tokens(operation, content_size)
        self.usage_log.append({
            "time": datetime.now(),
            "operation": operation,
            "estimated_tokens": estimated
        })
        
        # Check if we need checkpoint
        if self.get_usage_percentage() > self.checkpoint_thresholds[0]:
            self.trigger_checkpoint_warning()
    
    def trigger_checkpoint_warning(self):
        """
        Alert user and suggest checkpoint
        """
        # Write to dashboard
        # Create alert file
        # Suggest handover creation
```

### 3. Short-Term Memory System

```python
class ShortTermMemory:
    """
    SQLite-based memory for current session
    Includes agent communication and hard facts
    """
    
    def __init__(self):
        self.session_db = sqlite3.connect(".orchestrator/memory/session_state.db")
        self.message_db = sqlite3.connect(".orchestrator/memory/message_queue.db")
        self.facts_db = sqlite3.connect(".orchestrator/memory/hard_facts.db")
        
    def store_decision(self, decision, rationale, context):
        """
        Store decisions made during session
        """
        self.session_db.execute("""
            INSERT INTO decisions (decision, rationale, context, timestamp)
            VALUES (?, ?, ?, ?)
        """, (decision, rationale, json.dumps(context), datetime.now()))
        
    def store_api_fact(self, api_name, endpoint, parameters, response_format):
        """
        Store hard facts about APIs
        """
        self.facts_db.execute("""
            INSERT OR REPLACE INTO api_documentation 
            (api_name, endpoint, parameters, response_format)
            VALUES (?, ?, ?, ?)
        """, (api_name, endpoint, json.dumps(parameters), json.dumps(response_format)))
        
    def get_relevant_facts(self, context):
        """
        Retrieve facts relevant to current context
        """
        # Query hard facts
        # Return API docs, tool capabilities, patterns
```

### 4. Long-Term Memory System

```python
class LongTermMemory:
    """
    Vector DB for semantic search across all project knowledge
    """
    
    def __init__(self):
        # Option 1: ChromaDB (local, simple)
        # Option 2: Pinecone (cloud, powerful)
        # Option 3: Simple numpy embeddings (minimal)
        self.vector_store = self.initialize_vector_db()
        self.bug_patterns_db = sqlite3.connect(".orchestrator/memory/bug_patterns.db")
        
    def store_learning(self, content, category, tags):
        """
        Store new knowledge with embeddings
        """
        embedding = self.create_embedding(content)
        self.vector_store.add(
            embeddings=[embedding],
            metadatas=[{"category": category, "tags": tags}],
            ids=[str(uuid4())]
        )
        
    def semantic_search(self, query, top_k=5):
        """
        Find relevant knowledge for query
        """
        query_embedding = self.create_embedding(query)
        results = self.vector_store.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results
        
    def record_bug_pattern(self, symptom, cause, solution):
        """
        Track bug patterns for future reference
        """
        self.bug_patterns_db.execute("""
            INSERT INTO bug_patterns (symptom, cause, solution, timestamp)
            VALUES (?, ?, ?, ?)
        """, (symptom, cause, solution, datetime.now()))
```

### 5. Guardian Enforcement System

```python
class GuardianSystem:
    """
    Hard enforcement layer with memory access
    """
    
    def __init__(self):
        self.rules = self.load_enforcement_rules()
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        self.veto_count = 0
        
    def review_action(self, agent_id, action, args):
        """
        Review every action before execution
        Check against rules AND past patterns
        """
        # Check immediate violations
        violations = self.check_violations(action, args)
        
        # Check against known bug patterns
        bug_risks = self.check_bug_patterns(action, args)
        
        # Check against past decisions
        conflicts = self.check_decision_conflicts(action, args)
        
        if violations or bug_risks or conflicts:
            self.veto_count += 1
            self.broadcast_veto(agent_id, violations, bug_risks, conflicts)
            raise GuardianVeto(violations)
            
        return True
```

### 6. External Integrations (Bridges)

```python
class ExternalBridges:
    """
    Connections to external tools and services
    """
    
    def __init__(self):
        self.youtrack = YouTrackBridge()  # Bug tracking
        self.github = GitHubBridge()      # Issues and PRs
        self.unity = UnityMCPBridge()     # Unity integration
        self.notebook_lm = NotebookLMBridge()  # Knowledge synthesis
        
    class YouTrackBridge:
        """
        Integration with YouTrack for bug tracking
        """
        def create_issue(self, title, description, context):
            # Create YouTrack issue with full context
            pass
            
        def update_issue(self, issue_id, status, resolution):
            # Update issue with resolution
            pass
    
    class NotebookLMBridge:
        """
        Integration with Notebook LM for knowledge synthesis
        """
        def synthesize_session(self, session_content):
            # Send session for analysis
            pass
            
        def extract_insights(self, project_docs):
            # Extract key insights
            pass
```

## Data Flow with Memory Systems

### Knowledge-Enhanced Operation Flow
```
1. User Request
   ↓
2. Main Agent receives task
   ↓
3. Query Long-Term Memory for relevant patterns
   ↓
4. Guardian reviews approach with bug pattern check
   ↓
5. Main Agent proceeds with knowledge context
   ↓
6. Store decisions in Short-Term Memory
   ↓
7. Sub-agents access shared memory for coordination
   ↓
8. Dashboard shows all activity with token usage
   ↓
9. Memory Curator extracts learnings
   ↓
10. Update Long-Term Memory for future sessions
```

## Technology Stack

### Backend
- Python 3.9+ (coordination, file I/O)
- SQLite (state management, short-term memory)
- Flask + SocketIO (web server)
- ChromaDB/Pinecone (vector search)

### Frontend  
- HTML5 + CSS3 (dashboard UI)
- JavaScript (real-time updates)
- WebSocket (live streaming)
- Chart.js (token usage visualization)

### Agent Communication
- SQLite message_queue.db (reliable messaging)
- JSON files (state sharing)
- Markdown (documentation)
- Task() commands (parallel execution)

### External Services
- YouTrack API (bug tracking)
- GitHub API (issue management)
- Unity MCP (game engine integration)
- Notebook LM API (knowledge synthesis)

## Additional Components from Vision

### 1. Bug Hunter Mode
```python
class BugHunterMode:
    """
    Specialized mode for focused debugging
    """
    def activate(self, bug_description):
        # Isolate context for specific bug
        # Load all previous attempts from long-term memory
        # Load relevant code and patterns
        # Create focused workspace
        # Track all attempts in bug_patterns.db
```

### 2. Workflow System
```
workflows/
├── game-dev/
│   ├── rules.yaml         # Game-specific rules
│   ├── phases.yaml        # Dev phases (prototype, alpha, beta)
│   └── patterns.yaml      # Common game patterns
├── web-dev/
│   ├── rules.yaml         # Web-specific rules
│   ├── phases.yaml        # Dev phases
│   └── patterns.yaml      # Web patterns
└── tool-development/
    ├── rules.yaml         # Tool dev rules
    ├── phases.yaml        # Dev phases
    └── patterns.yaml      # Tool patterns
```

### 3. Document Tier Management
```python
class DocumentManager:
    """
    Manage different document tiers appropriately
    """
    def __init__(self):
        self.immutable_docs = ["vision.md", "architecture.md"]  # Git controlled
        self.task_docs = self.youtrack_bridge  # In YouTrack
        self.knowledge_docs = self.long_term_memory  # In Vector DB
        self.status_docs = ["handover.md", "progress.md"]  # Auto-generated
```

## Success Metrics

### Must Have
- [ ] Autonomous agent execution works
- [ ] Guardian can block violations
- [ ] Dashboard shows real-time status
- [ ] Short-term memory for agent communication
- [ ] Basic token estimation and warnings

### Should Have
- [ ] Long-term memory with semantic search
- [ ] Bug pattern recognition
- [ ] YouTrack integration
- [ ] Workflow-specific rules
- [ ] Memory curator agent

### Nice to Have
- [ ] Notebook LM integration
- [ ] Advanced token prediction
- [ ] Cross-project learning
- [ ] Team collaboration features
- [ ] Session replay capability

## Open Questions

1. **Vector DB Choice?**
   - ChromaDB for simplicity?
   - Pinecone for power?
   - Custom embeddings for control?

2. **Token Tracking Accuracy?**
   - How accurate can estimation be?
   - Should we track by operation type?
   - Time-based vs token-based checkpoints?

3. **Memory Curation Frequency?**
   - After each session?
   - Continuously during session?
   - Manual trigger?

4. **External Tool Priority?**
   - YouTrack first?
   - GitHub Issues as alternative?
   - Notebook LM worth the complexity?

---

*This architecture represents the complete vision: enforcement through Guardian, visibility through dashboard, memory through SQLite and Vector DB, and integration with external tools. Implementation prioritizes proving autonomous execution, then building memory systems, then adding external integrations.*