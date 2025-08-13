# Agent 1: Output Reader

You are Agent 1, responsible for reading outputs from Agent 2.

## Your Task

1. First, register yourself with the Guardian MCP server:
   - Use `register_agent` tool with:
     - agent_id: "agent1"
     - workspace_path: (current directory path)

2. Update your status to show you're waiting:
   - Use `update_status` tool with status "waiting" and details "Waiting for Agent 2 output"

3. Wait for Agent 2 to produce output:
   - Use `wait_for_output` tool with:
     - waiting_agent: "agent1"
     - from_agent: "agent2"
     - timeout_ms: 60000 (1 minute)

4. When output is available:
   - Read the file that Agent 2 created
   - Summarize what you found in the file
   - Update your status to "complete"

## Important
- Do NOT poll or repeatedly check - the MCP server will notify you
- The Guardian system uses event-driven notifications
- Trust the wait_for_output tool to tell you when the file is ready

## Success Criteria
- Successfully receive notification about Agent 2's output
- Read and summarize the webpage analysis created by Agent 2
- No polling loops used
