# Agent 1: Output Reader (Event-Driven Version)

You are Agent 1, responsible for reading outputs from Agent 2 using EVENT-DRIVEN communication.

## Your Task

1. **Register with Guardian**:
   ```
   register_agent:
     agent_id: "agent1"
     workspace_path: (current directory)
   ```

2. **Update status to waiting**:
   ```
   update_status:
     agent_id: "agent1"
     status: "waiting"
     details: "Waiting for Agent 2 output (event-driven)"
   ```

3. **Wait for output (THIS IS THE KEY STEP)**:
   ```
   wait_for_output:
     waiting_agent: "agent1"
     from_agent: "agent2"
     timeout_ms: 600000
   ```
   
   **IMPORTANT**: This tool will BLOCK until output is ready or timeout occurs.
   - Do NOT use a loop
   - Do NOT repeatedly check
   - Call it ONCE and wait
   - The Guardian will notify you instantly when output appears

4. **When notification received**:
   - The tool will return with the file path
   - Read the file using the Read tool
   - Summarize what you found
   - Update status to "complete"

## What NOT to do
❌ DO NOT create any loops
❌ DO NOT repeatedly call check_messages
❌ DO NOT poll for files
❌ DO NOT use sleep/wait commands

## What TO do
✅ Call wait_for_output ONCE
✅ Trust the event system
✅ Let Guardian handle the notification

## Success Criteria
- Zero polling loops
- Single call to wait_for_output
- Instant response when Agent 2 creates output
- Clean, event-driven communication