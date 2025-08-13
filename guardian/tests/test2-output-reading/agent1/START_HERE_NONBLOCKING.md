# Agent 1: Non-Blocking Output Reader

You are Agent 1. Your job is to process outputs from Agent 2, but WITHOUT blocking.

## Your Task

1. Register yourself with the Guardian MCP server:
   - Use `register_agent` tool with:
     - agent_id: "agent1"
     - workspace_path: (current directory path)

2. Update your status to "active":
   - Use `update_status` with status "active" and details "Ready for work"

3. **STOP HERE AND WAIT FOR INSTRUCTIONS**
   - Do NOT use wait_for_output
   - Do NOT poll for messages
   - Just say: "Agent 1 registered and ready. Waiting for system notifications."

## What Will Happen

- A background monitoring script is watching the MCP database for you
- When Agent 2 creates output, the monitor will notify you
- You'll receive a message in this terminal telling you to check
- THEN you can use `check_messages` to see what's available

## Important
- NO BLOCKING
- NO POLLING
- Just register and wait for the system to tell you what to do