# Claude Orchestrator - Folder Structure Design

## 1. Claude-Orchestrator Tool Structure (Development)

This is the structure of the claude-orchestrator tool itself - a self-contained, portable system that can be dropped into any project.

```
claude-orchestrator/            # Self-contained tool folder
├── README.md                   # Tool documentation
├── setup.sh                    # One-click setup script
├── orchestrate.py              # Main entry point
│
├── brain/                      # 🧠 Core orchestration logic
│   ├── conductor.py            # Main orchestrator
│   ├── context_monitor.py      # Token tracking
│   └── rule_engine.py          # Rule enforcement
│
├── short-term-memory/          # 💭 Session state (SQLite)
│   ├── session_state.db        # Current session data
│   ├── message_queue.db        # Agent communication
│   ├── task_tracker.db         # Active tasks
│   └── checkpoint_manager.py   # Session snapshots
│
├── long-term-memory/           # 🗄️ Persistent knowledge
│   ├── vector_store/           # ChromaDB/embeddings
│   ├── knowledge_base.db       # Facts & decisions
│   ├── bug_history.db          # Bug tracking
│   └── retrieval.py            # Search interface
│
├── workflows/                  # 🔄 Active workflows
│   ├── game-dev/              # Game development workflow
│   │   ├── rules.yaml         # Game dev specific rules
│   │   ├── phases.yaml        # Development phases
│   │   └── checks.yaml        # Validation rules
│   ├── web-dev/               # Web development workflow
│   └── active/                # Currently active workflow (symlink)
│
├── resource-library/          # 📚 Template resource pool
│   ├── hooks/                 # Available hooks
│   │   ├── session_start/     # Various session start hooks
│   │   ├── context_guard/     # Context monitoring hooks
│   │   ├── rule_enforce/      # Rule enforcement hooks
│   │   └── session_end/       # Cleanup hooks
│   ├── agents/                # Agent templates
│   │   ├── doc_maintainer/    # Documentation agent
│   │   ├── bug_hunter/        # Debugging specialist
│   │   ├── code_reviewer/     # Code quality agent
│   │   └── unity_specialist/  # Unity-specific agent
│   ├── documents/             # Document templates
│   │   ├── handovers/         # Session handover templates
│   │   ├── architecture/      # Design doc templates
│   │   └── status/            # Progress templates
│   └── project-types/         # Project-specific configs
│       ├── unity/             # Unity project setup
│       ├── love2d/            # Love2D project setup
│       └── web/               # Web project setup
│
├── tools/                     # 🔧 Utility scripts
│   ├── context_guardian.py    # Monitor context usage
│   ├── rule_validator.py      # Check rule compliance
│   ├── doc_generator.py       # Auto-generate docs
│   ├── session_analyzer.py    # Analyze past sessions
│   └── bug_extractor.py       # Extract bug patterns
│
├── bridges/                   # 🌉 External integrations
│   ├── unity_mcp.py          # Unity MCP bridge
│   ├── youtrack_mcp.py       # YouTrack integration
│   ├── github_issues.py      # GitHub integration
│   └── notebook_lm.py        # Notebook LM bridge
│
├── config/                    # ⚙️ Configuration
│   ├── defaults.yaml          # Default settings
│   ├── user.yaml             # User preferences
│   └── project.yaml          # Project-specific config
│
└── development/               # 🚧 Development workspace
    ├── VISION.md             # Tool vision & roadmap
    ├── ARCHITECTURE.md       # This document
    ├── TODO.md               # Development tasks
    └── experiments/          # Testing new features
```

## 2. Project Structure with Claude-Orchestrator Installed

This shows how a typical project looks after claude-orchestrator folder is added.

```
my-game-project/               # Any project root
├── .git/                      # Version control
├── .gitignore                 
├── README.md                  # Project readme
│
├── .claude/                   # 🎭 Claude's expected location
│   ├── hooks/                 # Active hooks (symlinks to orchestrator)
│   │   ├── session_start.py → ../claude-orchestrator/resource-library/hooks/...
│   │   ├── context_check.py → ../claude-orchestrator/resource-library/hooks/...
│   │   └── session_end.py → ../claude-orchestrator/resource-library/hooks/...
│   ├── agents/               # Active agents (symlinks or copies)
│   │   └── doc_maintainer.md → ../claude-orchestrator/resource-library/agents/...
│   └── config.yaml           # Claude-specific config
│
├── claude-orchestrator/       # 📦 The tool (portable folder)
│   ├── README.md             # Tool documentation
│   ├── setup.sh              # Tool setup script
│   ├── orchestrate.py        # Main entry point
│   ├── brain/                # Core logic
│   ├── short-term-memory/    # Session state
│   ├── long-term-memory/     # Persistent knowledge
│   ├── workflows/            # Project-type rules
│   ├── resource-library/     # Templates
│   ├── tools/                # Utilities
│   ├── bridges/              # External integrations
│   ├── config/               # Tool configuration
│   └── development/          # Tool development docs
│
├── Docs/                      # 📚 Project documentation
│   ├── Design/               # Project-specific design docs
│   ├── Technical/            # Project-specific technical docs
│   ├── Status/               # Project progress & handovers
│   └── README.md             # Documentation guide
│
├── agent-feedback/            # 📨 TRANSIENT - Not in git, safe to delete
│   ├── session-2025-01-11/   # Today's session
│   │   ├── context-guardian/ # Agent-specific folders
│   │   │   └── token-warning-2030.md
│   │   ├── doc-reorganizer/
│   │   │   └── reorganization-complete.md
│   │   └── bug-hunter/
│   │       └── bug-423-analysis.md
│   └── .cleanup             # Marker: everything here can be deleted
│
├── Source/                    # 💻 Project source code
│   └── [game code]           # Unity, Love2D, etc.
│
└── .orchestrator/            # 🎼 Project-specific orchestrator data
    ├── state/                # Project state (not in git)
    │   ├── current_session.db
    │   └── checkpoints/
    ├── memory/               # Project knowledge
    │   ├── facts.db          
    │   └── vectors/
    └── config.yaml          # Which workflows/rules are active
```

## Key Design Decisions

### Metaphorical Naming
- **brain/** - Core logic and decision making
- **short-term-memory/** - Temporary session data (SQLite)
- **long-term-memory/** - Persistent knowledge (Vector DB, facts)
- **resource-library/** - Reusable templates and components
- **bridges/** - Connections to external systems
- **workflows/** - Project-type specific rules and processes

### Portability Principles
1. **Self-contained**: Everything in one folder
2. **Non-invasive**: Minimal changes to project root
3. **Configurable**: Adapt to any project type
4. **Modular**: Enable/disable features as needed

### Installation Process
```bash
# 1. Copy the tool folder to any project
cd /path/to/your-project
cp -r /path/to/claude-orchestrator .

# 2. Run setup from within the tool folder
cd claude-orchestrator
./setup.sh --project-type unity  # or love2d, web, etc.

# 3. Setup creates:
#    - Symlinks in ../.claude/hooks/
#    - Project config in ../.orchestrator/
#    - Activates appropriate workflow

# 4. Start using
./orchestrate.py start           # Start monitoring
./orchestrate.py status          # Check status
./orchestrate.py enable hook context_guard  # Enable features
```

### Resource Library System

The resource-library contains templates that can be activated:

```bash
# List available resources
./orchestrate.py list hooks
./orchestrate.py list agents
./orchestrate.py list workflows

# Enable specific resources
./orchestrate.py enable hook session_start/minimal
./orchestrate.py enable agent bug_hunter
./orchestrate.py workflow activate game-dev

# Disable resources
./orchestrate.py disable agent doc_maintainer
```

### Workflow System

Workflows are project-type specific configurations:
- **game-dev/**: Rules for game development
- **web-dev/**: Rules for web development  
- **love2d/**: Specific Love2D patterns
- **unity/**: Unity-specific workflows

Each workflow contains:
- `rules.yaml` - Project-specific rules
- `phases.yaml` - Development phases
- `checks.yaml` - Validation rules
- `templates/` - Document templates

### Memory Architecture

**Short-term Memory** (Session State):
- Current context usage
- Active tasks
- Message queue
- Recent decisions

**Long-term Memory** (Persistent Knowledge):
- Project facts and decisions
- Bug history and solutions
- Code patterns
- Vector embeddings for search

### Development Folder

The `development/` folder is for tool development only:
- Vision and architecture documents
- TODO lists and planning
- Experiments and prototypes
- Not included when tool is distributed

## Migration from Current Structure

Current structure needs reorganization:
```bash
# Current (flat, mixed concerns)
claude-orchestrate/
├── context_guardian/     # Should move to tools/
├── VISION.md            # Should move to development/
├── README.md           # Keep at root
└── setup.sh            # Keep at root

# Target (organized, metaphorical)
claude-orchestrate/
├── brain/              # Core logic
├── short-term-memory/  # Session state
├── long-term-memory/   # Persistent knowledge
├── tools/              # Utilities (including context_guardian)
├── resource-library/   # Templates
├── development/        # Dev docs and experiments
└── [setup files]       # README, setup.sh, orchestrate.py
```
