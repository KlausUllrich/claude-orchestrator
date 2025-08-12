# Orchestrator UI Design - Next Generation

## Your Requirements
1. ✅ Orchestrator uses near full screen
2. ✅ Tab switching between agents (horizontal tabs at top)
3. ✅ Scrollable agent windows
4. ✅ Direct input to each agent when not busy
5. ✅ Extensible for future features

## Recommended Solution: Web-Based Terminal UI

### Why Web Instead of Pure Terminal
- **Better UI control** - Tabs, layouts, scrolling
- **Easier to extend** - Add features without rewriting
- **Cross-platform** - Works on any OS
- **Modern UX** - Keyboard shortcuts, mouse support
- **Terminal emulation** - Full ANSI color support

## Architecture Design

```
┌──────────────────────────────────────────────────────┐
│  [Orchestrator] [Agent 1] [Agent 2] [Agent 3] [+]    │ <- Tabs
├──────────────────────────────────────────────────────┤
│                                                      │
│                                                      │
│           Main Terminal Area (xterm.js)             │
│                                                      │
│           Currently Selected Tab Content            │
│                                                      │
│                                                      │
├──────────────────────────────────────────────────────┤
│ Status: Ready | Agents: 3/3 idle | ▶ Run | ⚙ Settings│ <- Status bar
└──────────────────────────────────────────────────────┘
```

## Technology Stack

### Option 1: Electron App (Recommended)
```javascript
// Main benefits:
- Native app feel
- Full system integration  
- Keyboard shortcuts work perfectly
- Can package as installable app
- Direct PTY access for real terminals
```

### Option 2: Web App with Terminal Server
```python
# Python backend (FastAPI/Flask)
- WebSocket server for real-time
- PTY management for each agent
- Session state management

# Frontend (React/Vue)
- xterm.js for terminal emulation
- Tab management
- Keyboard shortcut handling
```

## Implementation Plan

### Phase 1: MVP Web Dashboard (1-2 days)
```python
# orchestrator_web_ui.py
- FastAPI backend
- WebSocket connections
- 4 terminal sessions (orchestrator + 3 agents)
- Basic tab switching
- Full-screen layout
```

### Phase 2: Enhanced Features (3-4 days)
- Keyboard shortcuts (Ctrl+1/2/3 for agents)
- Status indicators (busy/idle)
- Output history/logging
- Settings panel
- Task templates

### Phase 3: Advanced Features (1 week)
- Agent spawning (add more agents dynamically)
- Split pane views
- Macro/snippet system
- Export/import sessions
- Collaboration features

## Detailed MVP Implementation

### Backend Structure
```python
class OrchestratorWebUI:
    def __init__(self):
        self.terminals = {
            'orchestrator': Terminal(),
            'agent1': Terminal(),
            'agent2': Terminal(),
            'agent3': Terminal()
        }
        
    async def handle_websocket(self, websocket):
        # Route input/output between web and PTY
        
    def launch_orchestrator(self):
        # Start Claude with orchestrator prompt
        
    def launch_agent(self, agent_id, task):
        # Start Claude agent with task
```

### Frontend Structure
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .tab-bar {
            height: 40px;
            display: flex;
            background: #2b2b2b;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border-right: 1px solid #444;
        }
        .tab.active {
            background: #1a1a1a;
            color: #4a9eff;
        }
        .terminal-container {
            height: calc(100vh - 80px);
            background: #1a1a1a;
        }
        .status-bar {
            height: 40px;
            background: #2b2b2b;
            display: flex;
            align-items: center;
            padding: 0 20px;
        }
    </style>
</head>
<body>
    <div class="tab-bar">
        <div class="tab active" onclick="switchTab('orchestrator')">
            🎭 Orchestrator
        </div>
        <div class="tab" onclick="switchTab('agent1')">
            🤖 Agent 1 <span class="status">●</span>
        </div>
        <div class="tab" onclick="switchTab('agent2')">
            🤖 Agent 2 <span class="status">●</span>
        </div>
        <div class="tab" onclick="switchTab('agent3')">
            🤖 Agent 3 <span class="status">●</span>
        </div>
        <div class="tab" onclick="addAgent()">➕</div>
    </div>
    
    <div class="terminal-container" id="terminal"></div>
    
    <div class="status-bar">
        <span>Status: Ready</span>
        <span style="margin-left: 20px">Agents: 0/3 active</span>
        <button onclick="runParallel()">▶ Run All</button>
    </div>
    
    <script src="xterm.js"></script>
    <script>
        const terminals = {};
        let activeTab = 'orchestrator';
        
        function switchTab(tabId) {
            // Hide all terminals
            Object.keys(terminals).forEach(id => {
                terminals[id].element.style.display = 'none';
            });
            
            // Show selected terminal
            terminals[tabId].element.style.display = 'block';
            terminals[tabId].focus();
            activeTab = tabId;
            
            // Update tab styling
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey) {
                switch(e.key) {
                    case '1': switchTab('agent1'); break;
                    case '2': switchTab('agent2'); break;
                    case '3': switchTab('agent3'); break;
                    case '0': switchTab('orchestrator'); break;
                    case 'Tab': 
                        // Cycle through tabs
                        const tabs = ['orchestrator', 'agent1', 'agent2', 'agent3'];
                        const currentIndex = tabs.indexOf(activeTab);
                        const nextIndex = (currentIndex + 1) % tabs.length;
                        switchTab(tabs[nextIndex]);
                        e.preventDefault();
                        break;
                }
            }
        });
    </script>
</body>
</html>
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+0 | Switch to Orchestrator |
| Ctrl+1 | Switch to Agent 1 |
| Ctrl+2 | Switch to Agent 2 |
| Ctrl+3 | Switch to Agent 3 |
| Ctrl+Tab | Cycle through tabs |
| Ctrl+N | New agent |
| Ctrl+R | Run parallel tasks |
| Ctrl+K | Clear current terminal |
| Ctrl+S | Save session |
| Ctrl+L | Load session |

## Features Roadmap

### Immediate (MVP)
- [x] Full-screen orchestrator
- [x] Tab switching
- [x] Scrollable terminals
- [x] Direct input to agents
- [x] Status indicators

### Soon
- [ ] Persistent sessions
- [ ] Task history
- [ ] Quick commands palette
- [ ] Agent templates
- [ ] Output export

### Future
- [ ] Split pane view
- [ ] Agent chaining
- [ ] Visual workflow builder
- [ ] Performance metrics
- [ ] Team collaboration
- [ ] Plugin system

## Quick Start Implementation

### 1. Simple Python + HTML Version
```python
# orchestrator_web.py
import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import subprocess
import pty
import os
import select

app = FastAPI()

class TerminalManager:
    def __init__(self):
        self.terminals = {}
        
    def create_terminal(self, terminal_id, command):
        master, slave = pty.openpty()
        pid = os.fork()
        
        if pid == 0:  # Child
            os.setsid()
            os.dup2(slave, 0)
            os.dup2(slave, 1)
            os.dup2(slave, 2)
            os.execvp(command[0], command)
        else:  # Parent
            self.terminals[terminal_id] = {
                'master': master,
                'pid': pid,
                'command': command
            }
            return master

@app.get("/")
async def get():
    return HTMLResponse(open("orchestrator_ui.html").read())

@app.websocket("/ws/{terminal_id}")
async def websocket_endpoint(websocket: WebSocket, terminal_id: str):
    await websocket.accept()
    
    # Create or get terminal
    if terminal_id not in manager.terminals:
        if terminal_id == 'orchestrator':
            cmd = ['claude', '--append-system-prompt', 'orchestrator prompt...']
        else:
            cmd = ['bash']  # Placeholder for agents
        manager.create_terminal(terminal_id, cmd)
    
    # Bidirectional communication
    # ... PTY <-> WebSocket bridge ...

manager = TerminalManager()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. Electron Version (More Native)
```javascript
// main.js
const { app, BrowserWindow } = require('electron');
const pty = require('node-pty');

let mainWindow;
const terminals = {};

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        webPreferences: {
            nodeIntegration: true
        }
    });
    
    mainWindow.loadFile('index.html');
    
    // Create orchestrator terminal
    terminals.orchestrator = pty.spawn('claude', 
        ['--append-system-prompt', 'orchestrator...'], {
        name: 'xterm-color',
        cwd: process.env.HOME
    });
}

app.whenReady().then(createWindow);
```

## Why This Approach Will Scale

1. **Modular architecture** - Easy to add features
2. **Standard web tech** - Many developers can contribute
3. **Terminal emulation** - Full Claude experience
4. **WebSocket real-time** - Instant updates
5. **Extensible UI** - Add panels, widgets, etc.

## Next Steps

1. **Choose approach**: Web app vs Electron
2. **Build MVP**: Focus on core 4 features
3. **Test with real tasks**: Ensure it works
4. **Iterate based on use**: Add features as needed

## The Vision

Eventually, this becomes a full IDE for AI orchestration:
- Visual workflow designer
- Agent marketplace
- Team collaboration
- Performance analytics
- Template library
- Plugin ecosystem

But we start simple: 4 terminals, tabs, full-screen, direct input.

Want me to start building the MVP?