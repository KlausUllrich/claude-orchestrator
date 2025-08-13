# Hybrid Architecture: MCP + Background Scripts + Message Injection

## PROVEN WORKING IN TEST 2!

## The Best of Both Worlds

### MCP Provides:
- **Centralized SQLite Database**: Persistent state across sessions
- **Shared Context**: All agents can access message history
- **Agent Discovery**: Agents can find each other
- **Audit Trail**: Complete history of all communications
- **Dashboard Ready**: Easy to build monitoring UI

### Background Scripts Provide:
- **Non-Blocking Execution**: Claude never waits
- **True Parallelism**: Multiple agents run simultaneously
- **Continuous Monitoring**: Monitor scripts poll MCP database
- **Message Injection**: Monitor injects notifications into agent terminals
- **No Timeouts**: Agents run until session-end

## How It Works (PROVEN IN TEST 2)

```
   Claude Agent 1          Claude Agent 2
  (in WezTerm pane)      (in WezTerm pane)
         |                       |
         |                       ↓
         |                  MCP Tools
         |                       |
         |                    MCP DB
         |                   (SQLite)
         |                       ↑
         |                Monitor Script
         |              (polls database)
         |                       |
         ←── Message Injection ──┘
     (via wezterm cli send-text)
```

1. **Real Claude agents** run in WezTerm panes with MCP tools
2. **Monitor script polls database** using `Bash(run_in_background=True)`
3. **When messages arrive**, monitor injects notification into agent's terminal
4. **Agent receives notification** as if user typed it
5. **Agent stays responsive** - can even tell jokes while "waiting"!
6. **No blocking, no polling by agents** - monitor does the work

## Simple Implementation

### Monitor Script (runs in background)
```bash
# monitor_and_inject.sh - Polls database for agents
while true; do
    NEW_MESSAGES=$(sqlite3 "$DB_PATH" "SELECT ... WHERE to_agent='$AGENT_ID'...")
    
    if [ ! -z "$NEW_MESSAGES" ]; then
        # Find agent's WezTerm pane
        PANE_ID=$(wezterm cli list | grep "$AGENT_ID" | awk '{print $1}')
        
        # INJECT notification into agent's terminal!
        wezterm cli send-text --pane-id "$PANE_ID" \
            "📬 SYSTEM: New MCP message available. Use check_messages tool."
        wezterm cli send-text --pane-id "$PANE_ID" $'\n'
    fi
    sleep 2
done
```

### How Claude Launches Agents
```python
# Launch agents - returns immediately!
Bash(command="python mcp_agent.py agent1 /path/to/db", run_in_background=True)
Bash(command="python mcp_agent.py agent2 /path/to/db", run_in_background=True)

# Claude is FREE to continue working
# Can check status anytime via database or BashOutput
```

### Communication Flow
```python
# Claude sends work to agent2
sqlite3 db "INSERT INTO messages (to_agent, content) VALUES ('agent2', 'create_output')"

# Agent2 sees message, creates output, notifies agent1
# Agent1 sees notification, reads output
# All automatic, no blocking!
```

## Key Advantages

1. **No Blocking**: Claude never waits for agents
2. **Persistent State**: Database survives crashes
3. **Observable**: Can query database anytime
4. **Simple**: Just Python + SQLite
5. **Scalable**: Add more agents easily
6. **No Timeouts**: Agents run until explicitly stopped

## Test 2 Implementation (SUCCESSFUL!)

### Setup
```bash
# 1. Start monitor script (in regular terminal)
./guardian/monitor_and_inject.sh agent1

# 2. Launch Agent 1 (in WezTerm pane 1)
cd guardian/tests/test2-output-reading/agent1
claude --dangerously-skip-permissions --mcp-config .claude/settings.json
# Tell Claude: "Read START_HERE_NONBLOCKING.md"

# 3. Launch Agent 2 (in WezTerm pane 2)  
cd guardian/tests/test2-output-reading/agent2
claude --dangerously-skip-permissions --mcp-config .claude/settings.json
# Tell Claude: "Read START_HERE.md and complete the task"
```

### What Actually Happened in Test 2
1. Agent 1 registered and said "Ready and waiting"
2. User asked Agent 1 to "tell a joke" - IT RESPONDED! (stayed responsive)
3. Agent 2 analyzed nius.de webpage using WebFetch
4. Agent 2 created output and notified via MCP
5. Monitor script saw notification in database
6. Monitor INJECTED "📬 SYSTEM: New MCP message available" into Agent 1
7. Agent 1 received injection and used check_messages tool
8. Agent 1 successfully read and summarized Agent 2's analysis
9. **NO BLOCKING OCCURRED!**

## Session Management

### Starting Agents
```python
# At session start
for agent in ["agent1", "agent2", "agent3"]:
    Bash(f"python mcp_agent.py {agent} {db_path}", run_in_background=True)
```

### Stopping Agents
```python
# At session end
Bash("python orchestrate.py stop")  # Sends stop signal via database
# Agents see stop signal and exit cleanly
```

## Why This Is The Solution

1. **PROVEN WORKING**: Test 2 complete success with real Claude agents
2. **Non-Blocking**: Agents stay responsive (can tell jokes while waiting!)
3. **Message Injection**: WezTerm CLI enables terminal injection
4. **Real MCP Tools**: Agents use actual MCP tools, not simulations
5. **Observable**: Everything logged in database
6. **Simple**: Monitor script is just bash + sqlite3
7. **Scalable**: Can monitor multiple agents simultaneously

## Next Steps

1. ✅ Test 2 COMPLETE - Non-blocking communication proven!
2. Refine notification format (make them commands)
3. Fix duplicate notification issue
4. Test 3: Monitor/approval pattern
5. Package as production-ready Guardian system

This is the architecture that actually works! 🎉