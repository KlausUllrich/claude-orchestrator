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

### Step 2: Complete Handover First (SEQUENTIAL)
1. Gather session information using `python orchestrate.py handover --summary info`
2. Create comprehensive handover document following template
3. Get user approval for the handover
4. Save using: `cat handover_content | python orchestrate.py handover --summary save`
5. Confirm handover is saved to `docs/status/handover-next.md`

### Step 3: Maintenance Task Selection
After handover is complete:
1. Ask user: "Would you like to run maintenance checks?"
2. If yes, explain you'll go through them one at a time
3. Available tasks (currently just `unreferenced_documents_check` for testing)

### Step 4: Process Maintenance Tasks ONE BY ONE
**CRITICAL**: Never launch multiple agents before reviewing results!

For EACH task (one at a time):
1. Tell user: "Running [task name] check..."
2. Launch ONE sub-agent using Task tool:
   ```
   Task tool parameters:
   - description: "Sub-Agent Assignment: (Maintenance) [task name]"
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
3. Wait for agent to complete and return results
4. Review findings with user:
   - Analyze and categorize findings (safe/risky/optional)
   - Make recommendations on what to fix
   - Explain what each finding means
5. Get user's specific decisions
6. If fixes approved, save decisions to JSON and launch fix-mode agent
7. Report what was done
8. Ask: "Would you like to run the next maintenance check?"
9. If yes, repeat from step 1 with next task

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
2. Complete handover FIRST (sequential, not parallel)
3. Process maintenance tasks ONE AT A TIME with user review
4. **Actually launch Task tools** (not just print instructions)
5. Make recommendations on findings before getting user decisions

The Python script (`orchestrate.py session end`) only provides configuration and instructions. Claude must execute the actual workflow using Task tools and other commands.

## Example Execution Flow

```
User: /session-end

Claude:
1. Runs: python orchestrate.py session end
   (Gets configuration and task list)

2. Creates and saves handover with user approval

3. Asks: "Would you like to run maintenance checks?"

4. If yes, for EACH task:
   - Launches ONE Task tool for that specific task
   - Waits for results
   - Reviews findings with recommendations
   - Gets user decisions
   - Executes fixes if approved
   - Asks about next task

5. Updates documentation and database

6. Commits changes if approved
```

## Known Issues & Workarounds

### RESOLVED: Parallel Execution Blocking
**Previous Issue**: Task tool blocked when running parallel agents
**Solution**: Redesigned workflow to be sequential:
- Handover completes first
- Maintenance tasks run one at a time with review

### Issue: Handover Save Syntax
**Correct syntax**: `python orchestrate.py handover --summary save`
**NOT**: `python orchestrate.py handover save`
The `--summary` flag is required!

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