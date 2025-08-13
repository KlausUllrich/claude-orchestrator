# Run Chain Communication Test

## Setup (3 terminals/panes needed)

### Terminal 1 - Agent 3 (Start FIRST)
```bash
cd /home/klaus/game-projects/claude-orchestrate/claude-orchestrator/orchestrator-tools/tests/agent3
claude --dangerously-skip-permissions
```
Then type: `Read START_HERE.md and begin`

### Terminal 2 - Agent 2 (Start SECOND) 
```bash
cd /home/klaus/game-projects/claude-orchestrate/claude-orchestrator/orchestrator-tools/tests/agent2
claude --dangerously-skip-permissions
```
Then type: `Read START_HERE.md and begin`

### Terminal 3 - Agent 1 (Start LAST)
```bash
cd /home/klaus/game-projects/claude-orchestrate/claude-orchestrator/orchestrator-tools/tests/agent1
claude --dangerously-skip-permissions
```
Then type: `Read START_HERE.md and begin`

## Expected Flow:
1. Agent 3 starts monitoring for requests
2. Agent 2 starts monitoring for requests
3. Agent 1 sends request to Agent 2
4. Agent 2 forwards to Agent 3
5. Agent 3 generates number, responds to Agent 2
6. Agent 2 relays to Agent 1
7. Agent 1 doubles the number and outputs result

## Success Indicators:
- ✅ File appears: `agent2/inputs/request_from_agent1.txt`
- ✅ File appears: `agent3/inputs/request_from_agent2.txt`
- ✅ File appears: `agent3/outputs/response_to_agent2.txt`
- ✅ File appears: `agent2/outputs/response_to_agent1.txt`
- ✅ Agent 1 outputs: "FINAL_RESULT: Original was X, doubled is 2X"

## Troubleshooting:
- If agents can't access other directories, ensure `--dangerously-skip-permissions` flag is used
- If agents timeout, they may need to wait longer (increase sleep times)
- Check that all agents are in their correct directories