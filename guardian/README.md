# Guardian - Non-Blocking Multi-Agent Orchestration

**Status: PROVEN WORKING** ✅

Guardian enables non-blocking communication between multiple Claude agents using a hybrid approach: MCP for tools/data and bash monitoring with message injection.

## 🎯 Key Innovation

**The Blocking Problem**: Claude agents block when waiting for other agents  
**The Solution**: Background monitor script polls database and injects notifications into agent terminals

## 📁 Structure

```
guardian/
├── mcp-server/              # Core MCP server with SQLite
│   ├── server.js           # MCP server implementation
│   ├── lib/                # Server components
│   └── db/                 # SQLite database
├── tests/                   # Working test examples
│   └── test2-output-reading/
└── utils/                   # Helper scripts
    ├── monitor_and_inject.sh  # Database monitor with injection
    └── orchestrate.py         # Database management utilities
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd mcp-server
npm install
```

### 2. Start Monitor (in regular terminal)
```bash
./utils/monitor_and_inject.sh agent1
```

### 3. Launch Agent in WezTerm
```bash
cd tests/test2-output-reading/agent1
claude --dangerously-skip-permissions --mcp-config .claude/settings.json
```

### 4. Agent Gets Notifications!
The monitor will inject messages like:
```
📬 SYSTEM: New MCP message available. Use check_messages tool to read it.
```

## 🔧 How It Works

1. **Real Claude agents** run in WezTerm panes with MCP tools
2. **Monitor script** polls the MCP database for messages
3. **When messages arrive**, monitor injects them into agent's terminal
4. **Agent processes** the notification while staying responsive
5. **No blocking!** Agent can even tell jokes while "waiting"

## 📊 Test Results

**Test 2 Success**: Agent 1 stayed responsive while Agent 2 analyzed a webpage. When Agent 2 finished, the monitor injected a notification into Agent 1's terminal, who then read the output - all without blocking!

## 🛠 MCP Tools Available

- `register_agent` - Register with Guardian
- `send_message` - Send messages to other agents
- `check_messages` - Retrieve messages
- `notify_output_ready` - Notify about created outputs
- `update_status` - Update agent status
- `wait_for_output` - Wait for output (BLOCKS - avoid!)

## 📚 Documentation

- [HYBRID_ARCHITECTURE.md](HYBRID_ARCHITECTURE.md) - Full architecture details
- [tests/test2-output-reading/](tests/test2-output-reading/) - Working example

## 🎉 Key Achievement

We solved the fundamental blocking problem! Agents can now work asynchronously without polling, staying fully responsive while coordinating with other agents.