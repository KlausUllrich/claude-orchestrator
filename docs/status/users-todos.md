# Claude Orchestrator - Master TODO List

*Located with handover documents for easy reference during sessions*

## 🔴 IMMEDIATE PRIORITY (Next Session)

### The ONE Thing: Research & Implement Agent Parallelization
- [ ] **CRITICAL: Fully understand __evaluation/ folder contents**
  - [ ] Read and analyze all files in claude-orchestrator/__evaluation/
  - [ ] Study SIMPLE_SOLUTIONS.md for parallelization strategies
  - [ ] Review simple_parallel_coordinator.py implementation
  - [ ] Examine parallel_task_hook.py for hook integration
  - [ ] Test minimal_parallel_mcp.py approach
  - [ ] Analyze game_dev_examples.py for practical use cases
- [ ] **Discuss findings in depth with user**
  - [ ] Present analysis of each solution approach
  - [ ] Compare pros/cons of different methods
  - [ ] Get user input on preferred implementation
- [ ] **Design implementation strategy**
  - [ ] Choose between coordinator, hook, or MCP approach
  - [ ] Plan integration with existing orchestrator
  - [ ] Design testing framework for parallel execution
- [ ] **Test parallel vs sequential performance**
  - [ ] Create benchmark scenarios
  - [ ] Measure execution time differences
  - [ ] Document results and recommendations

### Session-End Workflow Fixes (Completed This Session)
- [x] Fix path issues in session-end command - DONE
- [x] Fix handover command syntax - DONE
- [x] Fix workflow order (sequential, one-by-one) - DONE THIS SESSION
- [x] Implement project root finding function - DONE THIS SESSION
- [x] Add recommendations logic for findings - DONE THIS SESSION
- [x] Improve sub-agent display format - DONE THIS SESSION
- [ ] Test with single task only: unreferenced_documents_check
- [ ] Test full flow: session-start → work → session-end → handover

### After Session-End Works
- [ ] Create TODO tracking system using database
- [ ] Integrate session TODOs with user-todos.md
- [ ] Create `short-term-memory/task-tracker.py`
- [ ] Implement `/task-add`, `/task-list`, `/task-complete` commands
- [ ] Rename session_state.db → session-context.db
- [ ] Create task-queue.db schema
- [ ] Create message-queue.db for agent communication

## 🟡 SHORT TERM (Next 2-3 Sessions)

### Code Organization
- [ ] Rename `rule_enforcer.py` → `rule-engine.py` (kebab-case)
- [ ] Create `brain/conductor.py` for main orchestration logic
- [ ] Move context_guardian.py to brain/context-monitor.py
- [ ] Link databases to `.orchestrator/state/` for project
- [ ] Create rules to keep the keep the project folder clean, up-to-date, maintain location-guidance and maintain a single-source-of-truth

### Session Handover Enhancement
- [x] Added validation task for handover structure
- [x] Added pre-save checklist to template
- [x] Added enforcement markers to template sections
- [x] Updated handover workflow with validation phase
- [ ] Test handover validation in actual workflow
- [ ] Include core rules (CLAUDE.md) in session start
- [ ] Include documentation-index in session start
- [ ] Include active workflow rules in session start
- [ ] Create emergency handover for context overflow
- [ ] Add session metrics tracking (duration, files modified, etc.)

### Workflow Files
- [ ] Create `workflows/tool-development/checks.yaml` - validation rules
- [ ] Create `workflows/tool-development/phases.yaml` - dev stages
- [ ] Complete game-dev workflow template
- [ ] Add workflow-specific document requirements

## 🟠 MEDIUM TERM (Dedicated Sessions Required)

### Token Tracking Session (HIGH PRIORITY)
- [ ] Research Claude-Flow's solution for token tracking
- [ ] Investigate Claude Code's checkpoint feature (name conflict)
- [ ] Test alternative tracking methods
- [ ] Find monitoring approach (if not tmux, then what?)
- [ ] Document findings and implement solution

### Validation & Checking System
- [x] Created handover_validation_check.md task document
- [ ] Optimize all documentation task files for efficiency
- [ ] Create `tools/doc-validator.py` - Check document format/location
- [ ] Create `tools/rule-validator.py` - Check rule compliance
- [ ] Create contradiction detector for documentation
- [ ] Add naming convention enforcer (automated)
- [ ] Add documentation location validator
- [ ] Create pre-session checklist automation
- [ ] Create post-session validation

### Resource Library Population
- [ ] Create hook templates in `resource-library/hooks/`
  - [ ] session-start variations (minimal, full, debug)
  - [ ] session-end variations (handover, emergency)
  - [ ] context-guard hooks
  - [ ] rule-enforce hooks
- [ ] Create agent templates in `resource-library/agents/`
  - [ ] doc-maintainer.md template
  - [ ] bug-hunter.md template
  - [ ] code-reviewer.md template
  - [ ] unity-specialist.md template
- [ ] Create document templates in `resource-library/documents/`
  - [ ] Basic handover template
  - [ ] Detailed handover template
  - [ ] Architecture templates
  - [ ] Status report templates

### External Tool Integration
- [ ] GitHub CLI Installation (`sudo pacman -S github-cli`)
- [ ] Test GitHub Issues integration
- [ ] Evaluate YouTrack MCP server
- [ ] Compare bug tracking options

## 🔵 LONG TERM (Future Development)

### Long-term Memory Implementation
- [ ] Create `knowledge-base.db` for facts & decisions
- [ ] Create `bug-patterns.db` for bug history
- [ ] Implement `retrieval.py` for search interface
- [ ] Evaluate vector databases
  - [ ] ChromaDB (local, Python-native)
  - [ ] Pinecone (cloud, powerful)
  - [ ] Simple numpy embeddings as MVP
- [ ] Consider knowledge graph alternative
- [ ] Design knowledge extraction from sessions
- [ ] Implement semantic search
- [ ] Create bug pattern recognition
- [ ] Consider how to keep important knowledge of the code base

### External Bridges
- [ ] YouTrack MCP bridge implementation
- [ ] Notebook LM integration research & implementation
- [ ] GitHub Issues integration (fallback)
- [ ] Unity MCP bridge enhancement
- [ ] Mem0 evaluation
- [ ] Test all integration points

### Configuration System
- [ ] Create `config/user.yaml` - user preferences
- [ ] Create `config/project.yaml` - project settings
- [ ] Create `config/defaults.yaml` - default settings
- [ ] Build configuration loading system
- [ ] Add configuration override mechanism

### Multi-Agent Coordination
- [ ] Implement code analysis tasks similar to doc tasks
- [ ] Design agent communication protocols
- [ ] Implement message-queue.db fully
- [ ] Create agent spawning system
- [ ] Build conflict resolution
- [ ] Test parallel agent execution
- [ ] Create agent coordination rules
- [ ] Message passing via SQLite
- [ ] Performance monitoring

### Advanced Features
- [ ] Hook chaining system
- [ ] Hook activation through orchestrate.py
- [ ] Automatic checkpoint suggestions (time-based)
- [ ] Session replay capability
- [ ] Cross-project learning
- [ ] Team collaboration features
- [ ] Visual progress tracking
- [ ] Web UI for monitoring (maybe?)

## 📝 Documentation TODOs

### User Guides
- [ ] Quick start guide
- [ ] Installation guide per project type
- [ ] Migration from existing projects
- [ ] Troubleshooting guide
- [ ] Command reference

### Developer Docs
- [ ] Workflow creation guide
- [ ] Hook development guide
- [ ] Agent template guide
- [ ] Bridge creation guide
- [ ] Update architecture.md with implementation details

### Architecture Docs
- [ ] System design document
- [ ] Database schemas documentation
- [ ] API documentation
- [ ] Message protocol spec

## 🐛 Known Issues to Fix
- [ ] Context Guardian cannot track Claude Code tokens
- [ ] Commands exist as documentation only, not executable
- [ ] No automatic integration between components
- [ ] Database naming confusion (needs better names)
- [ ] Rule enforcer needs rename to rule-engine.py

## 💡 Research Questions
- [ ] How does Notebook LM API work?
- [ ] Can we extract knowledge from Claude sessions automatically?
- [ ] Best vector DB for local game dev knowledge?
- [ ] Optimal agent communication patterns?
- [ ] How to integrate with Claude Code's internal features?
- [ ] Browser extension feasibility for claude.ai capture?
- [ ] Chrome extension prototype possibilities?

## 📚 Future Ideas (Parking Lot)

### UI/UX Enhancements
- Visual dashboard (web-based?)
- Voice notifications for warnings
- VSCode extension
- Terminal UI with rich formatting
- Progress visualization

### Advanced Features
- Machine learning on bug patterns
- Automatic workflow detection
- Cross-project knowledge transfer
- Real-time monitoring capabilities

### More Integrations
- More game engines (Godot, Unreal)
- More VCS (GitLab, Bitbucket)
- Project management tools (Jira, Linear)
- Communication tools (Slack, Discord)
- CI/CD pipelines

## ✅ Completed Items

### Session 2025-08-10 17:30 (Current)
- [x] Implemented /session-end command with agent-driven architecture
- [x] Created maintenance-agent for task execution
- [x] Created database-updater-agent for intelligent savepoints
- [x] Created handover_validation_check.md task
- [x] Added validation phase to handover workflow
- [x] Added pre-save checklist and enforcement markers to template
- [x] Discovered critical bugs in session-end implementation

### Session 2025-08-10 11:30
- [x] Redesigned handover system to be LLM-driven
- [x] Created brain/handover-manager.py with helper functions
- [x] Made /handover and /session-start commands executable

### Session 2025-01-11
- [x] Created claude-orchestrator foundation with Context Guardian
- [x] Built rule injection system for brain/rule_enforcer.py
- [x] Created modular rule enforcer
- [x] Separated rules into YAML files
- [x] Implemented naming convention enforcement
- [x] Fixed session naming (YYYY-MM-DD format)
- [x] Created rule injection hook

### Session 2025-08-09 (Today)
- [x] Created tool-development workflow (not integrated)
- [x] Built SQLite schema for short-term-memory
- [x] Session state table
- [x] Checkpoint table (called handover now)
- [x] Clarified orchestration approach
- [x] Created QUICK-REFERENCE.md
- [x] Created comprehensive TODO documentation

## 🎯 Success Metrics

### Week 1 Goals
- ✅ Context Guardian prevents overflow (sort of - doesn't track Claude)
- ✅ Basic project structure created
- [ ] SQLite state management operational
- [ ] One complete workflow template
- [ ] Successfully dogfooding the tool

### Month 1 Goals
- [ ] Full short-term memory system working
- [ ] 3+ complete workflow templates
- [ ] Basic long-term memory with search
- [ ] Multi-agent proof of concept
- [ ] Used on real game project

### Quarter 1 Goals
- [ ] Production-ready for game development
- [ ] Multiple successful projects using it
- [ ] Community feedback incorporated
- [ ] Performance optimized
- [ ] Documentation complete

---
*Last Updated: 2025-08-10 17:45*
*Next Review: After making commands work*
*Location: docs/status/todo.md (with handover documents)*
