# Test 2: Output Reading Pattern

## Objective
Demonstrate event-driven communication between agents using the Guardian MCP server.
Agent 2 creates output, Agent 1 automatically receives notification and reads it.

## Architecture
- Guardian MCP server provides coordination
- File monitoring detects new outputs
- Event-driven notifications (no polling)
- SQLite message queue for reliability

## How to Run

### Step 1: Install dependencies (if not done)
```bash
cd /home/klaus/game-projects/claude-orchestrate/guardian/mcp-server
npm install
```

### Step 2: Start Agent 2 (Writer) FIRST
```bash
cd /home/klaus/game-projects/claude-orchestrate/guardian/tests/test2-output-reading/agent2
claude --dangerously-skip-permissions
# Read START_HERE.md and follow instructions
```

### Step 3: Start Agent 1 (Reader) in another terminal
```bash
cd /home/klaus/game-projects/claude-orchestrate/guardian/tests/test2-output-reading/agent1
claude --dangerously-skip-permissions
# Read START_HERE.md and follow instructions
```

### Step 4: Observe
- Agent 2 will create webpage analysis
- Guardian detects the new file
- Agent 1 receives notification instantly
- No polling required!

## Expected Outcome
- Agent 2 creates `outputs/webpage_analysis.txt`
- Agent 1 receives notification via MCP
- Agent 1 reads and summarizes the analysis
- All communication logged in Guardian database

## Verification
Check the Guardian database:
```bash
sqlite3 /home/klaus/game-projects/claude-orchestrate/guardian/mcp-server/db/coordination.db
.tables
SELECT * FROM messages;
SELECT * FROM outputs;
```
