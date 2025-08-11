# /session-end Command

## Trigger
When user types: `/session-end`

## Action
Execute comprehensive session end workflow with user approval at key decision points.

## Implementation Steps

### Step 1: Get Configuration
First, run the orchestrator to get session configuration:
```bash
python orchestrate.py session end
```
This will output the workflow configuration and instructions.

### Step 2: Launch Parallel Tasks
After getting configuration, immediately launch:

#### A. Handover Creation
Execute the `/handover` command workflow

#### B. Maintenance Analysis Agents
For each maintenance task (starting with just `unreferenced_documents_check` for testing):

Use the Task tool to launch maintenance agent:
```
Task tool parameters:
- description: "Analyze [task_name]"
- subagent_type: "general-purpose"
- prompt: 
  "You are a maintenance agent for the claude-orchestrator project.
   
   Read the agent template at: 
   /home/klaus/game-projects/claude-orchestrate/claude-orchestrator/resource-library/agents/maintenance-agent/maintenance-agent.md
   
   Then execute the task document at:
   /home/klaus/game-projects/claude-orchestrate/claude-orchestrator/resource-library/documents/documentation-tasks/[task_name].md
   
   Mode: ANALYZE
   
   Create a findings report and save it to:
   /home/klaus/game-projects/claude-orchestrate/docs/status/session-reports/findings-[task_name]-[timestamp].md"
```

### Step 3: Complete Handover
1. Gather session information using `python orchestrate.py handover --summary info`
2. Create comprehensive handover document following template
3. Get user approval
4. Archive old handover BEFORE saving new one
5. Save to `docs/status/handover-next.md`

### Step 4: Review Maintenance Findings
Once agents complete:
1. Read each findings report
2. Present findings conversationally (one task at a time)
3. Get user decisions on what to fix
4. Save decisions to JSON file

### Step 5: Execute Approved Fixes
For each approved fix:
1. Launch maintenance agent in FIX mode with decisions file
2. Report what was done

### Step 6: Update Documentation
- Update users-todos.md with completed items
- Update any other affected documentation

### Step 7: Database Update
Create session savepoint with final state

### Step 8: Git Commit (Optional)
If not using --no-git flag:
1. Stage changes
2. Create commit with session summary
3. Push if requested

## Command Options

```bash
# Standard session end
/session-end

# Skip maintenance analysis
/session-end --no-cleanup

# Skip git operations
/session-end --no-git

# Emergency end (handover only)
/session-end --emergency
```

## Critical Implementation Notes

**IMPORTANT**: This command requires Claude to:
1. Run Python script to get configuration
2. **Actually launch Task tools** (not just print instructions)
3. Coordinate between multiple parallel agents
4. Handle the interactive handover process

The Python script (`orchestrate.py session end`) only provides configuration and instructions. Claude must execute the actual workflow using Task tools and other commands.

## Example Execution Flow

```
User: /session-end

Claude:
1. Runs: python orchestrate.py session end
   (Gets configuration and task list)

2. Launches in parallel:
   - /handover command process
   - Task tool for unreferenced_documents_check
   - Task tool for other maintenance tasks

3. Completes handover with user approval

4. Reviews maintenance findings with user

5. Executes approved fixes

6. Updates documentation and database

7. Commits changes if approved
```

## Known Issues & Workarounds

### Issue: Task Tool Parallel Execution
The Task tool may not support true parallel execution. If parallel launch fails:
- Launch tasks sequentially instead
- Start with handover first, then maintenance tasks

### Issue: Handover Save
Ensure handover is actually saved by:
1. Archiving old handover FIRST
2. Writing new handover to handover-next.md
3. Confirming file exists after save

## Testing Checklist

Before considering session-end working:
- [ ] Python script provides configuration
- [ ] Task tools actually launch (not just print)
- [ ] Maintenance agents create findings reports
- [ ] Handover is created and saved properly
- [ ] User can review and approve changes
- [ ] All approved changes are executed
- [ ] Git commit includes all changes

## Related Commands
- `/handover` - Create handover only
- `/session-start` - Start with previous handover
- Individual agent launches for debugging