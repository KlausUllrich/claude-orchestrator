#!/usr/bin/env python3
"""
Simple Web Dashboard for Claude Agents
Shows real-time output from multiple Claude processes
"""

import asyncio
import json
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import sys

# Simple HTTP server (no external dependencies)
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver

class AgentManager:
    def __init__(self):
        self.agents = {}
        self.output_dir = Path(".orchestrate/dashboard/outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def launch_agent(self, agent_id: str, task: str):
        """Launch a Claude agent and capture output"""
        output_file = self.output_dir / f"{agent_id}.txt"
        
        # Launch Claude process
        cmd = f'claude -p "{task}" > {output_file} 2>&1'
        proc = subprocess.Popen(cmd, shell=True)
        
        self.agents[agent_id] = {
            "task": task,
            "process": proc,
            "output_file": str(output_file),
            "status": "running",
            "started": datetime.now().isoformat()
        }
        
        # Monitor process in background
        def monitor():
            proc.wait()
            self.agents[agent_id]["status"] = "completed"
            self.agents[agent_id]["completed"] = datetime.now().isoformat()
            
        thread = threading.Thread(target=monitor)
        thread.daemon = True
        thread.start()
        
    def get_status(self) -> Dict:
        """Get current status of all agents"""
        status = {}
        for agent_id, info in self.agents.items():
            output = ""
            if Path(info["output_file"]).exists():
                output = Path(info["output_file"]).read_text()
            
            status[agent_id] = {
                "task": info["task"],
                "status": info["status"],
                "started": info["started"],
                "completed": info.get("completed", ""),
                "output": output
            }
        return status

# HTML Dashboard
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Claude Agent Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #1a1a1a;
            color: #e0e0e0;
        }
        h1 {
            color: #4a9eff;
            text-align: center;
            margin-bottom: 30px;
        }
        .controls {
            text-align: center;
            margin-bottom: 20px;
        }
        button {
            background: #4a9eff;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background: #357abd;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
        }
        .agent-panel {
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 8px;
            overflow: hidden;
        }
        .agent-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .agent-status {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            background: rgba(255,255,255,0.2);
        }
        .status-running { background: #ffa500; }
        .status-completed { background: #00c851; }
        .agent-task {
            padding: 10px 15px;
            background: #333;
            border-bottom: 1px solid #444;
            font-size: 14px;
            color: #aaa;
        }
        .terminal {
            background: #1e1e1e;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            padding: 15px;
            height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 13px;
            line-height: 1.4;
        }
        .terminal::-webkit-scrollbar {
            width: 8px;
        }
        .terminal::-webkit-scrollbar-track {
            background: #1e1e1e;
        }
        .terminal::-webkit-scrollbar-thumb {
            background: #444;
            border-radius: 4px;
        }
        .timestamp {
            color: #666;
            font-size: 11px;
        }
        #status-message {
            text-align: center;
            margin: 10px;
            color: #4a9eff;
        }
    </style>
</head>
<body>
    <h1>🤖 Claude Multi-Agent Dashboard</h1>
    
    <div class="controls">
        <button onclick="launchAgents()">Launch Test Agents</button>
        <button onclick="refreshStatus()">Refresh</button>
        <button onclick="clearAll()">Clear All</button>
        <div id="status-message"></div>
    </div>
    
    <div id="agents-grid" class="grid"></div>
    
    <script>
        let agents = {};
        
        async function fetchStatus() {
            try {
                const response = await fetch('/status.json');
                const data = await response.json();
                return data;
            } catch (e) {
                console.error('Failed to fetch status:', e);
                return {};
            }
        }
        
        function updateDashboard(status) {
            const grid = document.getElementById('agents-grid');
            
            for (const [agentId, info] of Object.entries(status)) {
                let panel = document.getElementById(`agent-${agentId}`);
                
                if (!panel) {
                    // Create new panel
                    panel = document.createElement('div');
                    panel.id = `agent-${agentId}`;
                    panel.className = 'agent-panel';
                    panel.innerHTML = `
                        <div class="agent-header">
                            <span>${agentId.toUpperCase()}</span>
                            <span class="agent-status status-${info.status}">${info.status}</span>
                        </div>
                        <div class="agent-task">Task: ${info.task}</div>
                        <div class="terminal" id="terminal-${agentId}"></div>
                    `;
                    grid.appendChild(panel);
                }
                
                // Update status
                const statusBadge = panel.querySelector('.agent-status');
                statusBadge.className = `agent-status status-${info.status}`;
                statusBadge.textContent = info.status;
                
                // Update output
                const terminal = document.getElementById(`terminal-${agentId}`);
                if (info.output && info.output !== terminal.dataset.lastOutput) {
                    terminal.textContent = info.output;
                    terminal.dataset.lastOutput = info.output;
                    terminal.scrollTop = terminal.scrollHeight;
                }
            }
        }
        
        async function refreshStatus() {
            const status = await fetchStatus();
            updateDashboard(status);
            document.getElementById('status-message').textContent = 
                `Last updated: ${new Date().toLocaleTimeString()}`;
        }
        
        async function launchAgents() {
            // This would call your Python backend to launch agents
            const response = await fetch('/launch', { method: 'POST' });
            const result = await response.json();
            document.getElementById('status-message').textContent = result.message;
            setTimeout(refreshStatus, 1000);
        }
        
        function clearAll() {
            document.getElementById('agents-grid').innerHTML = '';
            agents = {};
        }
        
        // Auto-refresh every 2 seconds
        setInterval(refreshStatus, 2000);
        
        // Initial load
        refreshStatus();
    </script>
</body>
</html>
'''

def create_dashboard_server(manager: AgentManager):
    """Create simple HTTP server for dashboard"""
    
    class DashboardHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(DASHBOARD_HTML.encode())
            elif self.path == '/status.json':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                status = manager.get_status()
                self.wfile.write(json.dumps(status).encode())
            else:
                super().do_GET()
        
        def do_POST(self):
            if self.path == '/launch':
                # Launch test agents
                manager.launch_agent("agent1", "What is 2+2?")
                manager.launch_agent("agent2", "Name three colors")
                manager.launch_agent("agent3", "What is the capital of France?")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Agents launched!"}).encode())
            else:
                self.send_response(404)
                self.end_headers()
        
        def log_message(self, format, *args):
            # Suppress request logging
            pass
    
    return DashboardHandler

def main():
    print("🚀 Starting Claude Agent Dashboard")
    print("=" * 50)
    
    manager = AgentManager()
    
    # Create and start server
    PORT = 8888
    Handler = create_dashboard_server(manager)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"✅ Dashboard running at: http://localhost:{PORT}")
        print(f"📁 Output directory: {manager.output_dir}")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Shutting down dashboard...")

if __name__ == "__main__":
    main()