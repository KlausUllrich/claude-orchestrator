# Documentation Index - Claude Orchestrator Development

## 📚 Active Documentation Structure

This project is using its own documentation system for development (dogfooding).

### Permanent Documentation (Docs/)

#### Design Documents
- [VISION.md](Design/VISION.md) - Complete project vision and roadmap
  - Core problems being solved
  - Architecture decisions
  - Open questions for discussion

#### Technical Documents
- [ARCHITECTURE.md](Technical/ARCHITECTURE.md) - System design and folder structure
  - Tool structure (claude-orchestrator folder)
  - Project structure with tool installed
  - Installation and usage patterns
- [Agent_Feedback_System.md](Technical/Agent_Feedback_System.md) - Transient vs permanent docs
  - Separation of concerns
  - Lifecycle management
  - Implementation strategy
- [Known_Limitations.md](Technical/Known_Limitations.md) - Current limitations and workarounds
  - Context Guardian token tracking in Claude Code
  - Workarounds and future solutions
  - Checkpoint system alternatives

#### Status Documents
- [Session_Handover_20250111_2030.md](Status/Session_Handover_20250111_2030.md) - Latest session handover
  - What was accomplished in last session
  - Current working features
  - Next immediate steps
- [Session_Handover_NEXT.md](Status/Session_Handover_NEXT.md) - Next session entry point
- [TODO.md](Status/TODO.md) - **Master TODO list** (240 lines)
  - Immediate, short-term, medium-term, and long-term tasks
  - Research topics and known issues
  - Organized by priority and timeframe
  - Success metrics and completed items

#### Workflow Documents
- Currently empty - workflow documentation moved to Status/TODO.md

### Transient Documentation (agent-feedback/)

Located in `agent-feedback/` folder (not in git):
- Session-specific agent reports
- Detailed task completions
- Temporary findings before extraction
- **Safe to delete at any time**

Current session: `agent-feedback/session-2025-01-11-2045/`

## 🔧 Tool Documentation

Located in `claude-orchestrator/` folder:
- [README.md](../claude-orchestrator/README.md) - Tool overview and quick start
- [development/](../claude-orchestrator/development/) - Development notes (to be removed for distribution)

## 📦 Project Files (Test Environment)

These files are from the original claude-template and used for testing:
- `CLAUDE.md` - Claude interaction rules
- `prime.md` - Project primer
- `QUICK-REFERENCE.md` - **NEW: Simple overview to prevent confusion**
- `.claude/` - Original hooks and configuration

## 🎯 Key Concepts

### Documentation Tiers (Being Evaluated)
1. **Design** - Vision, UX, specifications (immutable)
2. **Technical** - Architecture, implementation
3. **Status** - Progress, session handovers
4. **Workflow** - Process docs, TODOs

### Tool Components
- **brain/** - Core orchestration logic
- **short-term-memory/** - Session state (SQLite)
- **long-term-memory/** - Persistent knowledge
- **workflows/** - Project-type specific rules
- **resource-library/** - Templates and components
- **tools/** - Utilities (Context Guardian)
- **bridges/** - External integrations

## 🚀 Quick Navigation

### For Development
1. Check current tasks: [TODO.md](Status/TODO.md)
2. Review last session: [Handover_NEXT.md](Status/Handover_NEXT.md)
3. Review vision: [VISION.md](Design/VISION.md)
4. Understand structure: [ARCHITECTURE.md](Technical/ARCHITECTURE.md)

### For Testing
```bash
cd claude-orchestrator
./orchestrate.py status
python3 tools/context_guardian.py --watch
```

### For Distribution
The `claude-orchestrator/` folder is self-contained and can be copied to any project.
Before distribution, remove:
- This Docs folder
- Root project files (CLAUDE.md, prime.md)
- Development folder inside claude-orchestrator

---
*This index helps navigate the dogfooding documentation structure*