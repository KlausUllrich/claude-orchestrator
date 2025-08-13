# Claude Guardian Test Setup Reference

## Test 1: Chain Communication ✅ COMPLETED

### Purpose
Test multi-agent communication: Agent 1 → Agent 2 → Agent 3 → back

### Setup Structure
```
tests/
├── agent1/          # Orchestrator
│   ├── START_HERE.md
│   ├── TASK.md      # Only Agent 1 has the task
│   ├── protocol.md
│   ├── inputs/
│   └── outputs/
├── agent2/          # Messenger
│   ├── START_HERE.md
│   ├── protocol.md
│   ├── inputs/
│   └── outputs/
└── agent3/          # Number Generator
    ├── START_HERE.md
    ├── protocol.md
    ├── inputs/
    └── outputs/
```

### Running Tests

#### Required Flag
```bash
claude --dangerously-skip-permissions
```

#### Launch Order (Important!)
1. Start Agent 3 first (receiver)
2. Start Agent 2 second (relay)
3. Start Agent 1 last (initiator)

#### Commands for Each Agent
```bash
# Terminal 1 - Agent 3
cd agent3
claude --dangerously-skip-permissions
# Type: Read START_HERE.md and begin

# Terminal 2 - Agent 2
cd agent2
claude --dangerously-skip-permissions
# Type: Read START_HERE.md and begin

# Terminal 3 - Agent 1
cd agent1
claude --dangerously-skip-permissions
# Type: Read START_HERE.md and begin
```

### Key Files to Keep
- `setup_agent_workspaces.sh` - Creates clean test environment
- `RUN_TEST.md` - Quick reference for running tests
- Each agent's `START_HERE.md` - Clear instructions
- Each agent's `protocol.md` - Communication rules

### Results
- Test successful: Number 73 → doubled to 146
- Full documentation in: `__proposed_refactoring/test_evidence/01_chain_communication_SUCCESS.md`

## Test 2: Output Reading (PENDING)
- Agent 2 creates webpage summary
- Agent 1 reads and processes it

## Test 3: Monitor/Approval Pattern (PENDING)
- Agent 2 monitors Agent 1's work
- Approval required before completion

## Lessons Learned
1. **Permissions**: Must use `--dangerously-skip-permissions`
2. **Full Instances**: Each agent needs complete Claude session
3. **Clear Prompts**: Explicit DO/DON'T instructions essential
4. **Polling Issue**: Need event-driven system (future improvement)

## Quick Workspace Reset
```bash
./setup_agent_workspaces.sh
```
This recreates clean agent directories for testing.