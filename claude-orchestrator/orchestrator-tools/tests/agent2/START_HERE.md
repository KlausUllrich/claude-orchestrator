# Agent 2 - START HERE

You are Agent 2, the messenger.

## YOUR JOB:
Monitor for requests and pass messages between Agent 1 and Agent 3.

## STEP BY STEP:

1. Read `protocol.md` to understand communication
2. Set up a monitoring loop:
   ```python
   Bash('while true; do ls inputs/; sleep 3; done', run_in_background=True)
   ```
3. Periodically check `inputs/request_from_agent1.txt`
4. When found, read it and understand what Agent 1 wants
5. Create a request for Agent 3 at `../agent3/inputs/request_from_agent2.txt`
6. Poll for Agent 3's response at `../agent3/outputs/response_to_agent2.txt`
7. When found, read it and relay to Agent 1 via `outputs/response_to_agent1.txt`

## CRITICAL:
- DO NOT generate the number yourself
- You MUST wait for Agent 3 to respond
- Agent 3 is running in another terminal
- Keep checking with `sleep` delays between attempts
- Use explicit file paths with Read/Write tools

Start by reading protocol.md and begin monitoring