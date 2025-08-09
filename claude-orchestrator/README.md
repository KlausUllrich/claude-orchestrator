# Claude Orchestrator

A portable, non-invasive orchestration system for managing LLM context, documentation, and multi-agent coordination in any development project.

## 🎯 What It Does

Claude Orchestrator prevents the most common LLM development problems:
- **Context Overflow**: Monitors token usage, warns before limits
- **Rule Drift**: Keeps LLM behavior consistent across sessions
- **Knowledge Loss**: Maintains memory between sessions
- **Bug Marathons**: Tracks debugging history and patterns

## 🚀 Quick Start

```bash
# 1. Add to your project
cd your-project
git clone [this-repo] claude-orchestrator

# 2. Run setup
cd claude-orchestrator
./setup.sh --project-type unity  # or love2d, web, etc.

# 3. Start using
./orchestrate.py start           # Start monitoring
./orchestrate.py status          # Check current status
```

## 📁 Structure

```
claude-orchestrator/
├── brain/                    # Core orchestration logic
├── short-term-memory/        # Session state (SQLite)
├── long-term-memory/         # Persistent knowledge
├── workflows/                # Project-type specific rules
├── resource-library/         # Templates and components
├── tools/                    # Utility scripts
├── bridges/                  # External integrations
├── config/                   # Configuration files
└── development/              # Development docs (not distributed)
```

## 🔧 Core Features

### Context Guardian
Monitors token usage and prevents overflow:
```bash
python3 tools/context_guardian.py --watch
```

### Rule Enforcer
Maintains consistent behavior across sessions (coming soon)

### Knowledge Management
Persistent memory using SQLite and vector search (coming soon)

### Multi-Agent Support
Coordinate multiple Claude instances (planned)

## 📚 Documentation

- [Architecture](development/ARCHITECTURE.md) - System design and folder structure
- [Vision](development/VISION.md) - Project roadmap and goals
- [Session Status](development/SESSION_STATUS.md) - Current development status

## 🎮 Project Types Supported

- **Unity** - Unity engine with MCP integration
- **Love2D** - Love2D game development
- **Web** - Web application development
- More coming soon...

## 🤝 Contributing

This tool is under active development. Check the [development folder](development/) for current status and plans.

## 📝 License

Private project - not yet licensed for public use.

---

**Current Status**: Foundation built, Context Guardian working. See [development docs](development/) for details.
