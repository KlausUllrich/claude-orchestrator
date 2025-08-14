---
project: claude-orchestrate
type: technical
title: "MCP Server Implementation Details"
version: 2025-08-14
status: CURRENT
summary:
  - Node.js MCP server with SQLite backend
  - Agent registration and message routing
  - Database schema and tool definitions
  - Working implementation in guardian/mcp-server/
tags: [mcp, server, implementation, database, tools]
---

# MCP Server Implementation Details

## Server Overview

**Location**: `guardian/mcp-server/`
**Technology**: Node.js with SQLite backend
**Status**: ✅ Working and tested (Test 2 success)

The MCP server provides centralized coordination for all Claude agents, handling registration, message routing, and shared state management.

## Core Components

### 1. Server Implementation (`server.js`)
```javascript
class GuardianMCPServer {
    constructor() {
        this.server = new Server({ name: 'guardian-orchestrator', version: '1.0.0' });
        this.dbPath = path.join(__dirname, 'db', 'coordination.db');
        this.db = new DatabaseManager(this.dbPath);
        this.registry = new AgentRegistry(this.db);
        this.broker = new MessageBroker(this.db, this.registry);
        this.monitor = new FileMonitor(this.broker);
    }
}
```

### 2. Component Libraries (`lib/`)
- **AgentRegistry.js**: Track agent registration and status
- **MessageBroker.js**: Route messages between agents
- **DatabaseManager.js**: SQLite database abstraction
- **FileMonitor.js**: Watch for file-based coordination signals

## Database Schema

### Agent Registration
```sql
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    name TEXT,
    role TEXT,
    status TEXT,           -- 'busy', 'free', 'offline'
    workspace_path TEXT,
    last_seen TIMESTAMP
);
```

### Inter-Agent Messages
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    from_agent TEXT,
    to_agent TEXT,
    message_type TEXT,
    content TEXT,
    urgency TEXT,          -- 'low', 'medium', 'high'
    delivered BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP
);
```

### Shared Context Store
```sql
CREATE TABLE context_store (
    key TEXT PRIMARY KEY,
    value TEXT,
    agent_id TEXT,
    category TEXT,         -- 'session', 'project', 'temporary'
    timestamp TIMESTAMP
);
```

### Output Notifications
```sql
CREATE TABLE outputs (
    id INTEGER PRIMARY KEY,
    agent_id TEXT,
    file_path TEXT,
    metadata TEXT,         -- JSON metadata
    created_at TIMESTAMP
);
```

## Available MCP Tools

### Agent Management
- **`register_agent`**: Register agent with orchestrator
- **`get_agent_list`**: List all registered agents and status
- **`update_status`**: Update agent status and details

### Message Coordination
- **`send_message`**: Send message to another agent
- **`check_messages`**: Check for messages addressed to agent
- **`notify_output_ready`**: Notify that output file is ready

### Blocking Tool (Avoid)
- **`wait_for_output`**: ❌ Blocks agent - use background monitoring instead

## Tool Usage Patterns

### Agent Registration
```javascript
// Each agent should register on startup
{
    "tool": "register_agent",
    "arguments": {
        "agent_id": "convention-enforcer",
        "workspace_path": "/path/to/agent/workspace",
        "capabilities": ["naming-validation", "file-organization"]
    }
}
```

### Message Sending
```javascript
{
    "tool": "send_message",
    "arguments": {
        "from_agent": "main-agent",
        "to_agent": "convention-enforcer",
        "message_type": "request",
        "content": "Check filename: MyScript.py",
        "file_path": "/path/to/MyScript.py"
    }
}
```

### Message Checking
```javascript
{
    "tool": "check_messages",
    "arguments": {
        "agent_id": "convention-enforcer",
        "mark_as_read": true
    }
}
```

## Non-Blocking Communication Layer

### Background Monitor (`utils/monitor_and_inject.sh`)
```bash
#!/bin/bash
AGENT_ID="$1"
DB_PATH="guardian/mcp-server/db/coordination.db"

while true; do
    # Check for new messages in database
    NEW_MESSAGES=$(sqlite3 "$DB_PATH" \
        "SELECT content FROM messages WHERE to_agent='$AGENT_ID' AND delivered=0")
    
    if [ ! -z "$NEW_MESSAGES" ]; then
        # Find agent's WezTerm pane
        PANE_ID=$(wezterm cli list-panes --format json | \
            jq -r ".[] | select(.title | contains(\"$AGENT_ID\")) | .pane_id")
        
        # Inject notification into agent's terminal
        if [ -n "$PANE_ID" ]; then
            echo "📬 SYSTEM: New MCP message available. Use check_messages tool." | \
                wezterm cli send-text --pane-id "$PANE_ID"
            wezterm cli send-text --pane-id "$PANE_ID" $'\n'
            
            # Mark as delivered
            sqlite3 "$DB_PATH" \
                "UPDATE messages SET delivered=1 WHERE to_agent='$AGENT_ID' AND delivered=0"
        fi
    fi
    
    sleep 2
done
```

### Why This Works
1. **No blocking**: Claude agents never wait for responses
2. **Event-driven**: Agents get notifications when messages arrive
3. **Responsive**: Agents can continue working (even tell jokes!) while "waiting"
4. **Reliable**: All communication logged in database
5. **Observable**: Easy to query database for coordination status

## Server Startup

### Installation
```bash
cd guardian/mcp-server
npm install
```

### Running Server
The MCP server runs automatically when Claude agents connect with the MCP configuration.

### Configuration
Each agent needs `.claude/settings.json`:
```json
{
  "mcpServers": {
    "guardian": {
      "command": "node",
      "args": ["../mcp-server/server.js"],
      "env": {}
    }
  }
}
```

## Testing and Validation

### Test 2 Success Pattern
1. **Agent 1** registers with MCP server
2. **Agent 2** registers with MCP server  
3. **Agent 2** creates output and notifies via MCP
4. **Background monitor** detects notification
5. **Monitor injects** message into Agent 1's terminal
6. **Agent 1** receives notification and processes result
7. **No blocking occurred** - Agent 1 stayed responsive throughout

### Database Queries for Monitoring
```sql
-- Check registered agents
SELECT * FROM agents;

-- Check pending messages
SELECT * FROM messages WHERE delivered = 0;

-- Check recent outputs
SELECT * FROM outputs ORDER BY created_at DESC LIMIT 10;

-- Check agent activity
SELECT agent_id, COUNT(*) as message_count 
FROM messages 
WHERE timestamp > datetime('now', '-1 hour') 
GROUP BY agent_id;
```

## Performance Considerations

### Database Optimization
- **Indexes**: Added on frequently queried columns (agent_id, timestamp, delivered)
- **Cleanup**: Automatic removal of old temporary context
- **Connection pooling**: Single connection per component

### Message Routing Efficiency
- **Direct routing**: Messages go directly to target agent
- **Batch processing**: Multiple messages handled in single poll cycle
- **Priority handling**: Urgent messages bypass normal queuing

### Resource Management
- **Memory usage**: SQLite keeps database in memory for speed
- **File handles**: Proper cleanup of database connections
- **Process monitoring**: Background monitors use minimal CPU

---

*This document covers the working MCP server implementation. For helper agent patterns, see [helper-agent-patterns.md](helper-agent-patterns.md).*