# Agent 1 - START HERE

You are Agent 1, the orchestrator. 

## STEP BY STEP:

1. First, read `protocol.md` to understand communication channels
2. Then read `TASK.md` to get your specific mission
3. Write a request to `../agent2/inputs/request_from_agent1.txt`
4. Use a polling loop to check for `../agent2/outputs/response_to_agent1.txt`
5. When found, read the number, double it, and output the result

## IMPORTANT:
- Agent 2 and Agent 3 are running in separate terminals
- They are monitoring their input directories
- You must WAIT for responses - they take time
- Use `Bash("sleep 5")` between checks
- Keep checking until you get a response

Start by reading protocol.md and TASK.md