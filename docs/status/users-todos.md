# Claude Orchestrator - Master TODO List

*Located with handover documents for easy reference during sessions*

## 🔴 IMMEDIATE PRIORITY (Current Session)

### ✅ BREAKTHROUGH ACHIEVED: Agent Parallelization SOLVED!
- [x] **Discovered the solution**: `run_in_background=True` with Claude CLI
- [x] **Proven**: Main orchestrator never blocks
- [x] **Tested**: 3 parallel Claude agents working simultaneously
- [x] **Implemented**: Working orchestrator system with Python scripts
- [x] **Created**: Visual monitoring with tmux dashboard
- [x] **Documented**: Complete breakthrough in ORCHESTRATOR_BREAKTHROUGH.md

### 🎯 NEW DIRECTION: WezTerm-based Guardian System
**Decision Made**: No web dashboard. Focus on WezTerm terminal multiplexing.
**Project Rename**: "Claude Guardian" (better reflects protective/monitoring nature)

### 🎯 CORE FUNCTIONALITY TO PRESERVE & IMPROVE
**Current Working UX**: `/session-start` and `/session-end` commands
**Goal**: Transfer these to new system with agent-based monitoring for better, consistent handovers
**Success Metric**: `/session-end` produces reliable, high-quality handovers through agent guidance

### 📋 IMMEDIATE: Agent Communication Tests in WezTerm
- [x] **Test 1: Chain Communication** ✅ SUCCESSFUL
  - [x] Agent 1 asks Agent 2 to ask Agent 3 for random number
  - [x] Agent 3 → Agent 2 → Agent 1 (who doubles it)
  - [x] Documented in `test_evidence/01_chain_communication_SUCCESS.md`
  - **Result**: Full chain worked! Number 73 → doubled to 146
  - **Key Finding**: Need `--dangerously-skip-permissions` flag
  
- [x] **Test 2: Output Reading** ✅ SUCCESSFUL
  - [x] Agent 2 creates webpage summary (analyzed nius.de)
  - [x] Agent 1 reads Agent 2's output file WITHOUT BLOCKING
  - [x] Monitor script injected notifications into Agent 1
  - [x] Agent 1 stayed responsive (even told jokes!)
  - [x] Key solution: monitor_and_inject.sh polls MCP for agents
  - [x] Document in `test_evidence/02_output_reading_SUCCESS.md`
  
- [ ] **Test 3: Monitor/Approval Pattern**
  - [ ] Create rules file for ASCII art standards
  - [ ] Agent 1 starts Agent 2 as monitor
  - [ ] Agent 1 creates ASCII painting
  - [ ] Agent 2 evaluates and provides feedback
  - [ ] Loop until Agent 2 approves
  - [ ] Document in `test_evidence/03_monitor_approval.md`

- [ ] **Test 4: Session-End Guardian Pattern (CRITICAL)**
  - [ ] Main agent runs `/session-end` equivalent
  - [ ] Guardian agent monitors handover quality
  - [ ] Guardian ensures all required sections present
  - [ ] Guardian validates no contradictions
  - [ ] Guardian forces improvements if needed
  - [ ] Only approved handover gets saved
  - [ ] Document in `test_evidence/04_session_end_guardian.md`

### 📦 Installation Requirements Tracking
- [x] WezTerm installed
- [x] Fonts installed (JetBrains Mono, Nerd Fonts)
- [x] Claude CLI with `--dangerously-skip-permissions` flag support
- [ ] Document all requirements in REQUIREMENTS.txt
- [ ] Create setup.sh for one-click installation

### 🔑 Key Discoveries from Test 1
- **Agent Independence**: Each agent needs full Claude instance with tools
- **Permission Flag Required**: `--dangerously-skip-permissions` for cross-directory access
- **Prompt Engineering Critical**: Need explicit DO/DON'T instructions
- **Polling Inefficient**: Need event-driven hooks to replace sleep loops
- **Workspace Architecture Works**: agent-per-folder with inputs/outputs proven successful

### Session-End Workflow Fixes (Partially Complete)
- [x] Fix path issues in session-end command - DONE
- [x] Fix handover command syntax - DONE
- [x] Fix workflow order (sequential, one-by-one) - DONE THIS SESSION
- [x] Implement project root finding function - DONE THIS SESSION
- [x] Add recommendations logic for findings - DONE THIS SESSION
- [x] Improve sub-agent display format - DONE THIS SESSION
- [ ] **FIX: Git section doesn't execute automatically** - Agent skips to summary instead
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

### 🔧 WezTerm UI/UX Optimization
- [ ] Configure optimal pane layouts for multi-agent work
- [ ] Set up dynamic tab titles showing agent status
- [ ] Create color coding for different agent types
- [ ] Document keybindings and navigation
- [ ] Create launch scripts for common patterns
- [ ] Test with 4+ agents simultaneously

### 🏗️ Architecture Planning for Claude Guardian
- [ ] Document lessons learned from all tests
- [ ] Define agent communication protocols
- [ ] Design file structure for outputs/status/sessions
- [ ] Plan session management and cleanup strategy
- [ ] Create state management design

### 📂 Folder Structure Redesign
- [ ] Rename `resource-library/` to `templates/`
- [ ] Design agent-per-folder architecture
  - [ ] Each agent gets own directory with config/context/outputs
  - [ ] Agents can have specific MCP servers
  - [ ] Clean session cleanup (delete old agent folders)
- [ ] Simplify documentation structure
- [ ] Make project fully copy/paste ready

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

### 🎯 Core Command Migration to Guardian System
- [ ] **Migrate `/session-start` with Guardian Enhancement**
  - [ ] Guardian reads previous handover
  - [ ] Guardian ensures all required docs are read
  - [ ] Guardian monitors adherence to project rules
  - [ ] Guardian provides context reminders during session
  
- [ ] **Migrate `/session-end` with Guardian Control**
  - [ ] Multiple specialized agents for different checks
  - [ ] Guardian orchestrates the handover creation
  - [ ] Quality gates before handover approval
  - [ ] Consistent, high-quality output every time
  - [ ] No more manual fixing of handovers

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
