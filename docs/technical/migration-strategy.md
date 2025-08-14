---
project: claude-orchestrate
type: technical
title: "Migration Strategy and Implementation Plan"
version: 2025-08-14
status: CURRENT
summary:
  - Detailed migration phases from claude-orchestrator to guardian
  - Preservation of working tools during transition
  - Helper agent implementation roadmap
  - Migration tools and compatibility bridges
tags: [migration, strategy, phases, transition, compatibility]
---

# Migration Strategy and Implementation Plan

## Migration Overview

**Goal**: Transition from single-agent claude-orchestrator/ to multi-agent guardian/ while preserving all current productivity and adding specialized helper capabilities.

**Approach**: Parallel development with gradual migration, ensuring no disruption to working tools.

## Current State Assessment

### Working Components (Preserve)
| Component | Location | Status | Action |
|-----------|----------|--------|--------|
| `/session-start` | `claude-orchestrator/` | ✅ Daily use | Keep working during transition |
| `/session-end` | `claude-orchestrator/` | ✅ Daily use | Keep working during transition |
| `orchestrate.py` | `claude-orchestrator/` | ✅ Daily use | Maintain compatibility |
| Session handovers | `claude-orchestrator/brain/` | ✅ Working | Port patterns to guardian |
| Context Guardian | `claude-orchestrator/tools/` | ✅ Working | Convert to helper agent |
| Resource library | `claude-orchestrator/resource-library/` | ✅ Used | Extract to markdown |

### Guardian Foundation (Ready)
| Component | Location | Status | Next Step |
|-----------|----------|--------|-----------|
| MCP Server | `guardian/mcp-server/` | ✅ Working | Production hardening |
| Non-blocking comms | `guardian/utils/monitor_and_inject.sh` | ✅ Proven | Integration testing |
| WezTerm setup | `guardian/tests/` | ✅ Tested | Automation scripts |
| Agent registration | MCP tools | ✅ Working | Helper agent integration |

## Phase 1: Helper Agent Foundation (Current Priority)

### Immediate Tasks (Next 1-2 Sessions)
1. **Create convention-enforcer helper agent**
   ```bash
   # Directory structure
   guardian/helper-agents/convention-enforcer/
   ├── instructions.md          # Agent role and behavior
   ├── naming-rules.md          # Extract from current conventions
   ├── file-organization.md     # Extract from current patterns
   ├── examples/               # Good/bad examples
   └── .claude/settings.json   # MCP configuration
   ```

2. **Test request-response pattern**
   - Main agent asks convention-enforcer about filename
   - Helper agent reads rules and responds with guidance
   - Validate non-blocking communication works
   - Document successful pattern

3. **Validate helper agent effectiveness**
   - Test with real project files and naming decisions
   - Verify helper provides useful, specific guidance
   - Ensure references to rule sources are accurate
   - Measure response time and reliability

### Phase 1 Success Criteria
- [ ] Convention-enforcer helper agent working
- [ ] Request-response pattern proven effective
- [ ] Main agent can get specialized help without blocking
- [ ] Helper agent references markdown rules correctly
- [ ] WezTerm multi-pane setup automated

## Phase 2: Core Session Management Migration (Next 2-3 Sessions)

### Session Management Port
1. **Implement guardian session commands**
   ```bash
   guardian/commands/
   ├── session-start.py         # Multi-agent session initialization
   ├── session-end.py          # Coordinated session cleanup
   └── handover-manager.py     # Multi-agent handover creation
   ```

2. **Multi-agent handover system**
   - Main agent creates handover draft
   - Helper agents validate their domains
   - Documentation-maintainer ensures consistency
   - Final handover reflects multi-agent insights

3. **Context Guardian as helper agent**
   ```bash
   guardian/helper-agents/context-guardian/
   ├── instructions.md          # Monitor context usage
   ├── overflow-prevention.md   # Rules for intervention
   ├── optimization-patterns.md # Context management strategies
   └── .claude/settings.json
   ```

### Migration Tools
```bash
guardian/migration/
├── extract-conventions.py      # Pull naming rules from existing patterns
├── extract-workflows.py        # Convert resource-library/ to markdown
├── session-state-migrator.py   # Transfer SQLite data
├── compatibility-bridge.py     # Maintain current command compatibility
└── validate-migration.py       # Verify nothing lost in transition
```

### Phase 2 Success Criteria
- [ ] Guardian session commands work equivalently to current
- [ ] Multi-agent handovers provide better quality than current
- [ ] Context Guardian helper prevents overflow
- [ ] Migration tools preserve all existing data
- [ ] Compatibility bridge maintains current workflow

## Phase 3: Enhanced Multi-Agent Capabilities (Medium-term)

### Additional Helper Agents
1. **Workflow Monitor**
   ```bash
   guardian/helper-agents/workflow-monitor/
   ├── instructions.md          # Monitor development processes
   ├── game-dev-process.md      # Specific workflow steps
   ├── quality-gates.md         # When to intervene
   └── milestone-checklists.md  # Validation criteria
   ```

2. **Documentation Maintainer**
   ```bash
   guardian/helper-agents/documentation-maintainer/
   ├── instructions.md          # Keep docs current and accurate
   ├── doc-templates.md         # Standard formats
   ├── update-patterns.md       # When/how to update
   └── consistency-rules.md     # Cross-document validation
   ```

3. **Requirements Validator**
   ```bash
   guardian/helper-agents/requirements-validator/
   ├── instructions.md          # Validate against requirements
   ├── acceptance-criteria.md   # Feature completion rules
   ├── scope-management.md      # Prevent scope creep
   └── validation-checklists.md # Systematic validation
   ```

### Advanced Coordination
- **Multi-helper coordination**: Helpers collaborate on complex validations
- **Escalation patterns**: When helpers need main agent attention
- **Conflict resolution**: When helpers disagree on guidance
- **Performance optimization**: Efficient helper assignment

### Phase 3 Success Criteria
- [ ] 4+ helper agents working simultaneously
- [ ] Helper collaboration patterns effective
- [ ] Conflict resolution mechanisms working
- [ ] Performance acceptable with multiple helpers

## Phase 4: Hook-Based Automation (Future)

### Automatic Helper Assignment
1. **File System Hooks**
   - Detect file creation/modification
   - Assign appropriate helper based on file type/location
   - Helper validates against all relevant rules
   - Report findings to main agent

2. **Process Hooks**
   - Detect phase transitions (design → implementation → testing)
   - Workflow monitor validates milestone completion
   - Requirements validator checks acceptance criteria
   - Documentation maintainer updates relevant docs

3. **Integration Hooks**
   - Git commit hooks for validation
   - Build process integration
   - Continuous validation during development

### Orchestrator Intelligence
- **Context-aware assignment**: Helper selection based on current work
- **Load balancing**: Distribute work across available helpers
- **Priority management**: Urgent validations vs. background monitoring
- **Learning patterns**: Improve assignment based on effectiveness

### Phase 4 Success Criteria
- [ ] Automatic helper assignment working reliably
- [ ] Hooks integrate seamlessly with development workflow
- [ ] Orchestrator intelligence improves over time
- [ ] Development efficiency measurably improved

## Migration Tools Implementation

### 1. Convention Extractor (`extract-conventions.py`)
```python
class ConventionExtractor:
    def extract_naming_patterns(self, codebase_path):
        """Analyze existing files to extract naming conventions"""
        # Scan files and directories
        # Identify patterns (kebab-case, snake_case, etc.)
        # Generate naming-rules.md from observed patterns
        
    def extract_organization_patterns(self, project_path):
        """Analyze directory structure for organization rules"""
        # Map directory purposes
        # Extract hierarchical patterns
        # Generate file-organization.md
```

### 2. Workflow Extractor (`extract-workflows.py`)
```python
class WorkflowExtractor:
    def extract_from_resource_library(self, resource_path):
        """Convert resource-library/ content to helper agent markdown"""
        # Parse existing workflow templates
        # Convert to helper agent instructions
        # Create process validation rules
        
    def extract_from_handovers(self, handover_path):
        """Learn workflow patterns from successful handovers"""
        # Analyze handover quality patterns
        # Extract process insights
        # Generate workflow validation rules
```

### 3. Session State Migrator (`session-state-migrator.py`)
```python
class SessionStateMigrator:
    def migrate_session_database(self, old_db, new_db):
        """Transfer session state to guardian format"""
        # Convert schema if needed
        # Preserve all session history
        # Update references to new structure
        
    def migrate_handover_history(self, old_handovers, new_format):
        """Convert handovers to guardian multi-agent format"""
        # Parse existing handovers
        # Enhance with helper agent insights
        # Maintain chronological history
```

### 4. Compatibility Bridge (`compatibility-bridge.py`)
```python
class CompatibilityBridge:
    def session_start_wrapper(self):
        """Provide /session-start compatibility during transition"""
        # Check if guardian/ is ready
        # Route to guardian if available, claude-orchestrator if not
        # Ensure identical user experience
        
    def session_end_wrapper(self):
        """Provide /session-end compatibility during transition"""
        # Coordinate both systems during overlap period
        # Ensure handovers work regardless of active system
        # Gradual cutover to guardian
```

## Risk Mitigation

### Rollback Plan
- **Complete backup**: Full claude-orchestrator/ preservation
- **Gradual cutover**: Command-by-command migration with fallbacks
- **Validation**: Extensive testing before each phase
- **Quick switch**: Ability to revert to claude-orchestrator/ instantly

### Data Protection
- **Session history**: All existing handovers preserved
- **Configuration**: Current settings maintained
- **Knowledge**: Resource library content extracted, not lost
- **Patterns**: Existing workflow patterns captured in helper agents

### Performance Monitoring
- **Response times**: Ensure guardian isn't slower than current system
- **Resource usage**: Monitor multi-agent memory/CPU overhead
- **Reliability**: Track failure rates and error patterns
- **User experience**: Measure actual productivity impact

## Success Metrics by Phase

### Phase 1 (Helper Agent Foundation)
- **Technical**: Helper agent responds within 2 seconds
- **Quality**: Helper guidance improves file organization measurably
- **Adoption**: Team prefers helper guidance over manual checking
- **Reliability**: Helper agent available 95%+ of the time

### Phase 2 (Session Management)
- **Functionality**: Guardian commands match claude-orchestrator/ exactly
- **Quality**: Multi-agent handovers provide more insights
- **Transition**: Zero productivity lost during migration
- **Compatibility**: Existing workflows unchanged

### Phase 3 (Multi-Agent Capabilities)  
- **Coordination**: 4+ helpers work without conflicts
- **Value**: Helpers catch issues current system misses
- **Efficiency**: Development speed increased by helper automation
- **Scalability**: System handles additional helpers gracefully

### Phase 4 (Hook-Based Automation)
- **Automation**: 80%+ of validations happen automatically
- **Accuracy**: Automatic assignment selects correct helper 90%+ of time
- **Integration**: Hooks don't disrupt development flow
- **Intelligence**: System learns and improves over time

## Timeline Estimates

### Phase 1: 1-2 weeks
- Convention-enforcer creation: 2-3 sessions
- Request-response pattern validation: 1-2 sessions
- WezTerm automation: 1-2 sessions

### Phase 2: 2-3 weeks  
- Session management port: 3-4 sessions
- Migration tools: 2-3 sessions
- Context Guardian helper: 2-3 sessions

### Phase 3: 3-4 weeks
- Additional helper agents: 4-6 sessions
- Advanced coordination: 2-3 sessions
- Performance optimization: 2-3 sessions

### Phase 4: 4-6 weeks
- Hook system implementation: 6-8 sessions
- Orchestrator intelligence: 4-6 sessions
- Integration and refinement: 4-6 sessions

**Total estimated timeline**: 3-4 months for complete migration

---

*This migration strategy ensures preservation of current productivity while building enhanced multi-agent capabilities. For implementation details, see [helper-agent-patterns.md](helper-agent-patterns.md) and [mcp-server-details.md](mcp-server-details.md).*