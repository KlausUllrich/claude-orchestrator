# Agent Feedback System Design

## Problem Statement

Current documentation systems mix two fundamentally different types of content:

### 1. Permanent Project Documentation
- **Purpose**: Long-term project knowledge
- **Examples**: Architecture, design decisions, API docs
- **Lifecycle**: Lives forever, version controlled
- **Audience**: Future developers, team members

### 2. Transient Agent Feedback
- **Purpose**: Immediate visibility into agent actions
- **Examples**: "Reorganized 15 files", "Fixed bug #123", "Checked documentation index"
- **Lifecycle**: Useful for hours/days, then becomes clutter
- **Audience**: Current user reviewing agent work

## Current Problems

1. **Documentation Clutter**: Agent reports pile up in Docs/Status/
2. **Unclear Permanence**: Hard to know what's safe to delete
3. **Mixed Concerns**: Operational reports mixed with project knowledge
4. **Scale Issues**: Multi-agent systems would exponentially increase clutter

## Proposed Solution: Dual Documentation System

### Folder Structure
```
project-root/
├── Docs/                      # PERMANENT (git tracked)
│   └── [project documentation]
│
├── agent-feedback/            # TRANSIENT (git ignored)
│   ├── session-YYYY-MM-DD-HHMM/
│   │   ├── agent-name/
│   │   │   └── report-timestamp.md
│   │   └── session-summary.md
│   └── .cleanup              # Marker file: safe to delete all
│
└── .orchestrator/            # OPERATIONAL (tool state)
```

### Agent Decision Tree
```python
def where_to_write(content_type, importance):
    if content_type == "project_knowledge":
        if importance == "critical":
            return "Docs/Design/"  # Permanent, immutable
        else:
            return "Docs/Technical/"  # Permanent, evolvable
    
    elif content_type == "progress_update":
        if importance == "milestone":
            return "Docs/Status/"  # Permanent checkpoint
        else:
            return "agent-feedback/session-{date}/"  # Transient
    
    elif content_type == "agent_report":
        return "agent-feedback/session-{date}/{agent}/"  # Always transient
    
    elif content_type == "operational":
        return ".orchestrator/state/"  # Tool internal
```

### Lifecycle Management

#### Creation Phase
1. Agent performs task
2. Generates detailed report → `agent-feedback/`
3. Extracts key findings → Updates permanent docs
4. Logs completion → `.orchestrator/state/`

#### Review Phase
1. User reviews agent-feedback/ (manually or via UI)
2. Important findings promoted to Docs/
3. Feedback marked as reviewed

#### Cleanup Phase
```bash
# Safe cleanup patterns
rm -rf agent-feedback/session-*  # All sessions
rm -rf agent-feedback/session-2025-01-10-*  # Specific day
find agent-feedback -mtime +7 -delete  # Older than 7 days
```

### Benefits

1. **Clear Boundaries**: Obvious what's permanent vs transient
2. **Safe Cleanup**: Can delete entire agent-feedback/ without fear
3. **Scalable**: Works with many agents
4. **UI-Ready**: Future UI can monitor agent-feedback/ folder
5. **Git-Friendly**: Transient docs not tracked

### Implementation Phases

#### Phase 1: Folder Structure (Immediate)
- Create agent-feedback/ folder
- Add to .gitignore
- Update agents to use dual system

#### Phase 2: Agent Intelligence (Week 1)
- Agents categorize their output
- Automatic extraction of key findings
- Session summaries

#### Phase 3: Lifecycle Automation (Week 2)
- Auto-cleanup of old feedback
- Promotion workflows
- Review tracking

#### Phase 4: UI Integration (Future)
- Real-time monitoring of agent-feedback/
- One-click review and cleanup
- Visual diff of permanent doc updates

## Migration Strategy

### From Current System
```bash
# Move transient reports
mv Docs/Status/*_reorganization_*.md agent-feedback/
mv Docs/Status/*_findings_*.md agent-feedback/

# Keep permanent handovers
# Keep Docs/Status/Session_Handover_*.md
```

### Agent Code Changes
```python
class Agent:
    def report_findings(self, findings):
        # Transient detailed report
        self.write_feedback(
            f"agent-feedback/session-{date}/{self.name}/findings.md",
            detailed_report
        )
        
        # Permanent summary
        if findings.has_critical_updates():
            self.update_permanent(
                "Docs/Status/Session_Summary.md",
                findings.summary
            )
```

## Open Questions

1. **Retention Policy**: How long to keep agent-feedback?
   - Option A: 7 days
   - Option B: Until next session
   - Option C: User-configured

2. **Review Tracking**: How to know what's been reviewed?
   - Option A: Move to reviewed/ subfolder
   - Option B: Add .reviewed marker file
   - Option C: Track in .orchestrator/state/

3. **Extraction Automation**: How much to automate?
   - Manual: User decides what to promote
   - Semi-auto: Agent suggests, user approves
   - Full-auto: Agent extracts based on rules

## Next Steps

1. Create agent-feedback/ folder structure
2. Update .gitignore
3. Modify agent reporting patterns
4. Test with documentation reorganizer agent
5. Create cleanup utilities

---
*This design separates transient operational feedback from permanent project knowledge*