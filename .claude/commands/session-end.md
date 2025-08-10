# /session-end Command

## Trigger
When user types: `/session-end`

## Action
Execute comprehensive session end workflow with user approval at key decision points.

## Implementation
Execute the orchestrator's session end command:
```bash
cd claude-orchestrator && python orchestrate.py session end
```

## Overview
When you run `/session-end`, here's what happens:

```
1. Launch parallel tasks: handover creation + sub-agent analysis
2. Execute /handover command workflow (gather info → create → review → approve → save)
3. Review sub-agent findings and approve actions
4. Execute all approved changes
5. Update documentation and database
6. Optional: Clean up reports
7. Commit and push changes
```

## Workflow Phases

### Phase 1: Parallel Task Launch
Start immediately and concurrently:
- **Handover Creation**: Begin `/handover` command process
- **Sub-agents**: Execute maintenance analysis tasks

Sub-agents execute tasks based on configuration, which may include:
- unreferenced_documents_check
- document_structure_check  
- content_consistency_check
- yaml_headers_check
- documentation_index_check
- And others as configured

### Phase 2: Handover Process (Using /handover Command)
Execute the full `/handover` command workflow:

#### Information Gathering
```bash
cd claude-orchestrator && python orchestrate.py handover info
```
- Review session context
- Check system state
- Analyze memory systems
- Compare goals vs outcomes

#### Handover Creation
LLM creates comprehensive handover following template:
- Mandatory reads section
- Development state summary
- Next session goals
- Critical warnings
- Task breakdown
- References and context

#### User Review & Approval
```
📝 Session Handover Ready

[Shows complete handover document]

Options:
A) Approve and save handover
B) Request specific changes
C) Add additional context
```

#### Save After Approval
After user approves:
- Archive previous handover FIRST
- Save new handover to `docs/status/handover-next.md`
- Confirm successful save

### Phase 3: Sub-agent Findings Review
Once analysis completes, present dynamic proposal:

```
📊 Maintenance Analysis Complete

[Dynamic summary based on actual task results]

Found X improvement opportunities:
- Temporary files: [count]
- Documentation issues: [count]
- Structure problems: [count]

View detailed reports:
[List of generated reports]

Your options:
A) Apply all safe recommendations
B) Review each category
C) Skip cleanup
D) View detailed reports
```

### Phase 4: Execute Approved Changes
Apply changes from:
- Approved sub-agent recommendations
- Any handover revisions if needed

### Phase 5: Documentation Updates
Update all core documents from [`read-first.md`](../../docs/read-first.md):
- Mark completed TODOs in users-todos.md
- Update known-limitations.md if new ones found
- Sync architecture.md if structure changed
- Update other core docs as needed

### Phase 6: Database Update (Session Savepoint)
After all changes are made:
- Update session_state with 'ended' status
- Create final savepoint with type 'session_end'
- Record completed tasks and pending items
- Log unresolved issues

**Naming Clarification**: "Savepoint" = our database checkpoint, distinct from Claude native checkpoints (not yet available)

### Phase 7: Long-term Memory Update
**Currently**: Placeholder
**Future**: Extract patterns and learnings for knowledge base

### Phase 8: Cleanup Sub-agent Reports (Optional)
Before git commit, offer to clean up session reports:

```
📁 Session reports cleanup:

Created 4 analysis reports this session.
Archive them before commit? (Y/n)
```

### Phase 9: Git Commit and Push
Present commit proposal:

```
📝 Ready to commit session changes

Changes: X files modified

Suggested message:
"Session end: [main accomplishment from handover]
- [Key change 1]
- [Key change 2]
- Maintenance: [cleanup summary]"

Proceed? (Y/n)
```

## Command Options

```bash
# Standard session end
/session-end

# Skip maintenance analysis
/session-end --no-cleanup

# Skip git operations
/session-end --no-git

# Emergency end (handover only via /handover command)
/session-end --emergency
```

### Emergency Mode
`/session-end --emergency` focuses only on:
1. Execute `/handover` command in emergency mode
2. Quick handover creation and save
3. Skip all analysis and cleanup

## Example Flow

```
User: /session-end

Claude: 
====[ Session End Overview ]====
I'll help you end this session properly. Here's what will happen:
1. ⚡ Creating handover and running analysis in parallel
2. 📝 Review and save handover (using /handover workflow)
3. 📊 Review maintenance findings
4. ✨ Apply approved changes
5. 💾 Update docs and database
6. 📦 Commit your work

Starting now...

====[ Phase 1: Parallel Processing ]====
📝 Starting /handover command process...
🔍 Launching maintenance analysis...

====[ Phase 2: Handover Process ]====
Gathering information...
[Runs: python orchestrate.py handover info]

Creating comprehensive handover...
[Following template structure]

📝 **Session Handover Ready for Review:**

[Shows full handover document]

Main accomplishments:
- Implemented session-end command
- Created maintenance agent template

Next session priorities:
- Test full workflow
- Implement database updates

Approve handover? (Y/n/edit): Y
✅ Previous handover archived to: docs/status/archive/
✅ New handover saved to: docs/status/handover-next.md

⏳ Waiting for analysis to complete...
✅ Analysis complete (4 reports generated)

====[ Phase 3: Maintenance Review ]====
[Presents findings from sub-agents]

====[ Phases 4-9: Continue as defined ]====
[Execute approved changes, update docs, etc.]

✨ Session ended successfully!
📋 Next session: Run /session-start
```

## Integration with /handover Command

The session-end command reuses the complete `/handover` command workflow:
- Same information gathering process
- Same template-based creation
- Same user review and approval flow
- Same save mechanism (archive then save)

This ensures consistency and avoids duplication of the handover logic.

## Error Handling

- **Handover fails**: `/handover` command handles its own errors
- **Sub-agent fails**: Continue with partial results
- **Database fails**: Log to file, continue
- **Git fails**: Complete other steps, manual commit needed

## Task Configuration

The specific maintenance tasks run by sub-agents can be configured in:
`claude-orchestrator/config/session-end-tasks.yaml` (future)

Currently runs all available task documents from:
`claude-orchestrator/resource-library/documents/documentation-tasks/`

## Related Commands
- `/handover` - Create handover only (used internally by session-end)
- `/session-start` - Start with previous handover
- `/checkpoint` - Mid-session savepoint (TODO)