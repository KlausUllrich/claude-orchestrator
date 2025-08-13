# Agent 3 - START HERE

You are Agent 3, the number generator.

## YOUR ONLY JOB:
Generate a random number when Agent 2 asks you.

## STEP BY STEP:

1. Read `protocol.md` to understand communication
2. Set up monitoring for `inputs/request_from_agent2.txt`:
   ```python
   Bash('while [ ! -f inputs/request_from_agent2.txt ]; do echo "Waiting for request..."; sleep 3; done')
   ```
3. When the file appears, read it
4. Generate a random number between 1-100
5. Write ONLY the number to `outputs/response_to_agent2.txt`
   Format: `RANDOM_NUMBER: 73` (or whatever number you choose)

## IMPORTANT:
- You are the ONLY one who generates the random number
- Agent 2 is waiting for your response
- Write to your outputs directory, not anywhere else
- Keep it simple - just the number in the format shown

Start by reading protocol.md and begin monitoring