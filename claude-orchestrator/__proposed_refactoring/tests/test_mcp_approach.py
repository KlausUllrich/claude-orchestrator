#!/usr/bin/env python3
"""
Test MCP Server Approach for Parallel Execution
Key Question: Does Claude block when calling MCP tools?
"""

import json
import sys
import sqlite3
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class TestMCPServer:
    """
    Test MCP server that can launch tasks in background
    """
    
    def __init__(self):
        self.pending_tasks = []
        self.running_tasks = {}
        self.db_path = Path(".orchestrate/tests/mcp/state.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """Initialize database for tracking"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS task_log (
                id INTEGER PRIMARY KEY,
                task_id TEXT,
                command TEXT,
                status TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle MCP protocol requests"""
        method = request.get("method", "")
        params = request.get("params", {})
        
        if method == "tools/list":
            return self.list_tools()
        elif method == "launch_background_task":
            return self.launch_background_task(params)
        elif method == "check_task_status":
            return self.check_task_status(params)
        elif method == "queue_task":
            return self.queue_task(params)
        elif method == "execute_batch":
            return self.execute_batch()
        else:
            return {"error": f"Unknown method: {method}"}
    
    def list_tools(self) -> Dict:
        """List available MCP tools"""
        return {
            "tools": [
                {
                    "name": "launch_background_task",
                    "description": "Launch a task in background immediately",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "command": {"type": "string"}
                        },
                        "required": ["task_id", "command"]
                    }
                },
                {
                    "name": "check_task_status",
                    "description": "Check status of a background task",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"}
                        },
                        "required": ["task_id"]
                    }
                },
                {
                    "name": "queue_task",
                    "description": "Queue a task for batch execution",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string"}
                        },
                        "required": ["command"]
                    }
                },
                {
                    "name": "execute_batch",
                    "description": "Execute all queued tasks in parallel",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        }
    
    def launch_background_task(self, params: Dict) -> Dict:
        """Launch a task in background and return immediately"""
        task_id = params.get("task_id", f"task_{int(time.time()*1000)}")
        command = params.get("command", "")
        
        # Log the launch
        print(f"[MCP {datetime.now().strftime('%H:%M:%S')}] Launching {task_id}: {command}")
        
        # Start subprocess in background
        proc = subprocess.Popen(command, shell=True, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        
        self.running_tasks[task_id] = {
            "process": proc,
            "command": command,
            "started_at": datetime.now()
        }
        
        # Log to database
        self.conn.execute(
            "INSERT INTO task_log (task_id, command, status, started_at) VALUES (?, ?, ?, ?)",
            (task_id, command, "running", datetime.now())
        )
        self.conn.commit()
        
        # Return immediately - this is the key!
        return {
            "success": True,
            "task_id": task_id,
            "status": "launched",
            "message": f"Task {task_id} launched in background"
        }
    
    def check_task_status(self, params: Dict) -> Dict:
        """Check status of a background task"""
        task_id = params.get("task_id")
        
        if task_id not in self.running_tasks:
            return {
                "success": False,
                "error": f"Unknown task: {task_id}"
            }
        
        task = self.running_tasks[task_id]
        proc = task["process"]
        
        if proc.poll() is None:
            return {
                "success": True,
                "task_id": task_id,
                "status": "running",
                "started_at": task["started_at"].isoformat()
            }
        else:
            stdout, stderr = proc.communicate()
            return {
                "success": True,
                "task_id": task_id,
                "status": "completed",
                "exit_code": proc.returncode,
                "stdout": stdout[:500],  # Truncate for brevity
                "stderr": stderr[:500]
            }
    
    def queue_task(self, params: Dict) -> Dict:
        """Queue a task for batch execution"""
        command = params.get("command")
        self.pending_tasks.append(command)
        
        return {
            "success": True,
            "queued_count": len(self.pending_tasks),
            "message": f"Task queued ({len(self.pending_tasks)} pending)"
        }
    
    def execute_batch(self) -> Dict:
        """Execute all queued tasks in parallel"""
        if not self.pending_tasks:
            return {
                "success": False,
                "message": "No tasks to execute"
            }
        
        # Launch all tasks
        launched = []
        for command in self.pending_tasks:
            task_id = f"batch_{int(time.time()*1000)}_{len(launched)}"
            proc = subprocess.Popen(command, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
            
            self.running_tasks[task_id] = {
                "process": proc,
                "command": command,
                "started_at": datetime.now()
            }
            launched.append(task_id)
        
        # Clear queue
        count = len(self.pending_tasks)
        self.pending_tasks = []
        
        return {
            "success": True,
            "launched_count": count,
            "task_ids": launched,
            "message": f"Launched {count} tasks in parallel"
        }
    
    def run_stdio(self):
        """Run as stdio MCP server"""
        print(f"[MCP Server Started at {datetime.now().strftime('%H:%M:%S')}]", file=sys.stderr)
        
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line)
                print(f"[MCP] Received: {request.get('method', 'unknown')}", file=sys.stderr)
                
                response = self.handle_request(request)
                
                # MCP response format
                output = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": response
                }
                
                print(json.dumps(output))
                sys.stdout.flush()
                
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if 'request' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()

def create_test_agents():
    """Create test agent scripts"""
    agents_dir = Path(".orchestrate/tests/mcp/agents")
    agents_dir.mkdir(parents=True, exist_ok=True)
    
    # Create test agents with different durations
    for name, duration in [("alpha", 15), ("beta", 10), ("gamma", 8)]:
        script = agents_dir / f"{name}.py"
        script.write_text(f'''#!/usr/bin/env python3
import time
from datetime import datetime
from pathlib import Path

print(f"[{{datetime.now().strftime('%H:%M:%S')}}] Agent {name.upper()}: Starting {{duration}}s task")

status_file = Path(".orchestrate/tests/mcp/status/{name}.txt")
status_file.parent.mkdir(parents=True, exist_ok=True)

for i in range({duration}):
    with open(status_file, 'w') as f:
        f.write(f"{name.upper()}: {{i+1}}/{duration} at {{datetime.now()}}")
    
    if i % 3 == 0:
        print(f"[{{datetime.now().strftime('%H:%M:%S')}}] Agent {name.upper()}: Progress {{i}}/{duration}")
    
    time.sleep(1)

with open(status_file, 'w') as f:
    f.write(f"{name.upper()}: COMPLETED at {{datetime.now()}}")

print(f"[{{datetime.now().strftime('%H:%M:%S')}}] Agent {name.upper()}: COMPLETED")
''')
        script.chmod(0o755)
    
    print("Test agents created:")
    print("  - alpha.py (15s)")
    print("  - beta.py (10s)")
    print("  - gamma.py (8s)")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test MCP Server")
    parser.add_argument("--create-agents", action="store_true", help="Create test agents")
    parser.add_argument("--server", action="store_true", help="Run as MCP server")
    parser.add_argument("--test", action="store_true", help="Run test commands")
    args = parser.parse_args()
    
    if args.create_agents:
        create_test_agents()
    elif args.server:
        server = TestMCPServer()
        server.run_stdio()
    elif args.test:
        # Test the server locally
        server = TestMCPServer()
        
        print("Testing MCP server locally...")
        
        # Test launching background task
        result = server.launch_background_task({
            "task_id": "test1",
            "command": "sleep 5 && echo 'Task complete'"
        })
        print(f"Launch result: {result}")
        
        # Check status
        time.sleep(1)
        status = server.check_task_status({"task_id": "test1"})
        print(f"Status: {status}")
        
        # Test batch execution
        server.queue_task({"command": "echo 'Task 1'"})
        server.queue_task({"command": "echo 'Task 2'"})
        result = server.execute_batch()
        print(f"Batch result: {result}")
    else:
        print("Use --create-agents, --server, or --test")