# Multi-Terminal Dashboard for Claude Agents

## Vision
Real-time visibility into multiple Claude agents running in parallel, each in its own terminal with live output streaming.

## Option 1: Tmux-Based Solution

### Basic Tmux Setup
```bash
#!/bin/bash
# create_tmux_dashboard.sh

# Create new tmux session
tmux new-session -d -s claude_agents

# Split into 4 panes (2x2 grid)
tmux split-window -h
tmux split-window -v
tmux select-pane -t 0
tmux split-window -v

# Launch Claude in each pane
tmux send-keys -t 0 'claude -p "Agent 1 task"' C-m
tmux send-keys -t 1 'claude -p "Agent 2 task"' C-m
tmux send-keys -t 2 'claude -p "Agent 3 task"' C-m
tmux send-keys -t 3 'claude -p "Agent 4 task"' C-m

# Attach to session
tmux attach-session -t claude_agents
```

### Advanced Tmux with Logging
```bash
# Each pane logs to a file
tmux send-keys -t 0 'claude -p "task" | tee agent1.log' C-m

# Monitor logs in real-time from another terminal
tail -f agent*.log
```

## Option 2: Web Dashboard with WebSockets

### Architecture
```
Claude Agents → PTY → WebSocket Server → Web Dashboard
     ↓              ↓                ↓            ↓
 [Terminal]    [Capture]      [Broadcast]   [Display]
```

### Simple Python Implementation
```python
# websocket_dashboard.py
import asyncio
import websockets
import json
import pty
import os
import select
from threading import Thread

class AgentTerminal:
    def __init__(self, agent_id, command):
        self.agent_id = agent_id
        self.command = command
        self.master, self.slave = pty.openpty()
        self.output_buffer = []
        
    def start(self):
        # Fork and run command in PTY
        pid = os.fork()
        if pid == 0:  # Child
            os.dup2(self.slave, 0)
            os.dup2(self.slave, 1)
            os.dup2(self.slave, 2)
            os.execvp("claude", ["claude", "-p", self.command])
        else:  # Parent
            self.pid = pid
            self.read_output()
    
    def read_output(self):
        # Read from PTY and buffer output
        while True:
            r, w, e = select.select([self.master], [], [], 0.1)
            if self.master in r:
                data = os.read(self.master, 1024).decode('utf-8', errors='ignore')
                self.output_buffer.append(data)
                # Broadcast to websocket clients
                broadcast_update(self.agent_id, data)

async def websocket_handler(websocket, path):
    # Send current state to new client
    await websocket.send(json.dumps(get_current_state()))
    
    # Keep connection alive
    async for message in websocket:
        # Handle client commands if needed
        pass

# HTML Dashboard
dashboard_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Claude Agent Dashboard</title>
    <style>
        .terminal {
            background: #1e1e1e;
            color: #00ff00;
            font-family: monospace;
            padding: 10px;
            height: 300px;
            overflow-y: auto;
            margin: 10px;
            border: 1px solid #333;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .agent-header {
            background: #333;
            color: white;
            padding: 5px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Claude Multi-Agent Dashboard</h1>
    <div class="grid">
        <div>
            <div class="agent-header">Agent 1</div>
            <div class="terminal" id="agent1"></div>
        </div>
        <div>
            <div class="agent-header">Agent 2</div>
            <div class="terminal" id="agent2"></div>
        </div>
        <div>
            <div class="agent-header">Agent 3</div>
            <div class="terminal" id="agent3"></div>
        </div>
        <div>
            <div class="agent-header">Agent 4</div>
            <div class="terminal" id="agent4"></div>
        </div>
    </div>
    
    <script>
        const ws = new WebSocket('ws://localhost:8765');
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const terminal = document.getElementById(data.agent_id);
            terminal.innerHTML += data.output;
            terminal.scrollTop = terminal.scrollHeight;
        };
    </script>
</body>
</html>
'''
```

## Option 3: Terminal UI with Rich/Textual

### Using Python Textual
```python
# textual_dashboard.py
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Static, Header, Footer
from textual.reactive import reactive
import subprocess
import threading

class AgentPanel(Static):
    output = reactive("")
    
    def __init__(self, agent_id, command):
        super().__init__()
        self.agent_id = agent_id
        self.command = command
        self.start_agent()
    
    def start_agent(self):
        def run():
            proc = subprocess.Popen(
                ["claude", "-p", self.command],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in iter(proc.stdout.readline, ''):
                self.output += line
        
        thread = threading.Thread(target=run)
        thread.start()
    
    def watch_output(self, output):
        self.update(output)

class ClaudeDashboard(App):
    CSS = '''
    Grid {
        grid-size: 2 2;
        grid-gutter: 1;
    }
    AgentPanel {
        border: solid green;
        height: 100%;
        overflow-y: auto;
    }
    '''
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Grid():
            yield AgentPanel("agent1", "Task 1")
            yield AgentPanel("agent2", "Task 2")
            yield AgentPanel("agent3", "Task 3")
            yield AgentPanel("agent4", "Task 4")
        yield Footer()

if __name__ == "__main__":
    app = ClaudeDashboard()
    app.run()
```

## Option 4: Electron Desktop App

### Architecture
```
Electron App
├── Main Process (Node.js)
│   ├── Spawn Claude processes
│   ├── Capture output via node-pty
│   └── Send to renderer
└── Renderer Process (Web)
    ├── Terminal emulator (xterm.js)
    └── React/Vue dashboard
```

### Key Components
```javascript
// main.js (Electron main process)
const { spawn } = require('node-pty');

function createAgent(id, task) {
    const ptyProcess = spawn('claude', ['-p', task], {
        name: 'xterm-color',
        cols: 80,
        rows: 30,
        cwd: process.env.HOME,
    });
    
    ptyProcess.on('data', (data) => {
        // Send to renderer
        mainWindow.webContents.send(`terminal-output-${id}`, data);
    });
    
    return ptyProcess;
}

// renderer.js
const Terminal = require('xterm').Terminal;

const term1 = new Terminal();
term1.open(document.getElementById('terminal1'));

ipcRenderer.on('terminal-output-1', (event, data) => {
    term1.write(data);
});
```

## Option 5: Simple Script + Screen Recording

### Low-Tech But Effective
```bash
#!/bin/bash
# simple_multi_terminal.sh

# Open multiple terminal windows
gnome-terminal --title="Agent 1" -- bash -c "claude -p 'Task 1'; read"
gnome-terminal --title="Agent 2" -- bash -c "claude -p 'Task 2'; read"
gnome-terminal --title="Agent 3" -- bash -c "claude -p 'Task 3'; read"

# Or use xterm for more control
xterm -T "Agent 1" -e "claude -p 'Task 1'" &
xterm -T "Agent 2" -e "claude -p 'Task 2'" &
xterm -T "Agent 3" -e "claude -p 'Task 3'" &
```

## Recommended Approach for Guardian

### Phase 1: Tmux (Immediate)
```bash
# guardian_tmux.sh
tmux new-session -d -s guardian
tmux rename-window 'Claude Agents'

# Create layout
tmux split-window -h -p 50
tmux split-window -v -p 66
tmux split-window -v -p 50
tmux select-pane -t 0
tmux split-window -v -p 66
tmux split-window -v -p 50

# Status pane at bottom
tmux select-pane -t 0
tmux split-window -v -p 20
tmux send-keys -t 6 'watch -n 1 "cat .orchestrate/status/*.json | jq ."' C-m

# Launch agents
for i in {0..5}; do
    tmux send-keys -t $i "claude -p 'Agent $i task'" C-m
done

tmux attach-session -t guardian
```

### Phase 2: Web Dashboard (Next Week)
- Python FastAPI backend
- WebSocket for real-time updates
- PTY for terminal capture
- Simple HTML/JS frontend

### Phase 3: Professional Dashboard (Future)
- Electron or Tauri app
- Full terminal emulation
- Agent management UI
- Performance metrics
- Log persistence

## Key Technical Challenges

1. **Terminal Output Capture**: Need PTY to capture ANSI codes
2. **Real-time Streaming**: WebSockets or Server-Sent Events
3. **Process Management**: Keep track of PIDs, handle crashes
4. **Resource Usage**: Multiple Claude instances = high memory
5. **Security**: Dashboard should be local-only

## Implementation Priority

1. **Tmux script** - Can implement today, immediate visibility
2. **Simple web dashboard** - 1-2 days, good enough for demos
3. **Textual TUI** - 1 day, works in terminal
4. **Full Electron app** - 1 week, production quality

## Next Steps

1. Test tmux approach with real Claude commands
2. Build minimal web dashboard prototype
3. Evaluate terminal emulation libraries
4. Design agent management interface
5. Plan performance monitoring

The tmux solution is immediately achievable and provides the visibility you need!