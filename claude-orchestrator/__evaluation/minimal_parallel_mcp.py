#!/usr/bin/env python3
"""
Minimal MCP Server for Parallel Task Execution
A lightweight alternative to claude-flow, focused solely on parallel execution
No web dev stuff, no complex swarms, just parallel tasks for game dev
"""

import json
import sys
import sqlite3
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class MinimalParallelMCP:
    """
    Bare-bones MCP server that provides just two tools:
    1. queue_parallel_task - Add tasks to batch
    2. execute_parallel_batch - Run all tasks in parallel
    
    That's it. No complexity.
    """
    
    def __init__(self):
        self.pending_tasks = []
        self.db_path = Path(".orchestrate/mcp_state.db")
        self.init_db()
    
    def init_db(self):
        """Simple state tracking"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY,
                batch_id TEXT,
                tasks TEXT,
                executed_at TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle MCP requests"""
        method = request.get("method", "")
        params = request.get("params", {})
        
        if method == "tools/list":
            return self.list_tools()
        elif method == "queue_parallel_task":
            return self.queue_task(params)
        elif method == "execute_parallel_batch":
            return self.execute_batch()
        else:
            return {"error": f"Unknown method: {method}"}
    
    def list_tools(self) -> Dict:
        """List available tools"""
        return {
            "tools": [
                {
                    "name": "queue_parallel_task",
                    "description": "Queue a task for parallel execution",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "agent": {"type": "string"},
                            "task": {"type": "string"}
                        },
                        "required": ["agent", "task"]
                    }
                },
                {
                    "name": "execute_parallel_batch",
                    "description": "Execute all queued tasks in parallel",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        }
    
    def queue_task(self, params: Dict) -> Dict:
        """Queue a task"""
        agent = params.get("agent", "worker")
        task = params.get("task", "")
        
        self.pending_tasks.append({
            "agent": agent,
            "task": task,
            "queued_at": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "queued_count": len(self.pending_tasks),
            "message": f"Task queued ({len(self.pending_tasks)} pending)"
        }
    
    def execute_batch(self) -> Dict:
        """Generate parallel execution commands"""
        if not self.pending_tasks:
            return {
                "success": False,
                "message": "No tasks to execute"
            }
        
        # Generate the critical parallel commands
        commands = []
        for task in self.pending_tasks:
            agent = task["agent"]
            objective = task["task"]
            commands.append(f'Task("{agent.upper()}: {objective}")')
        
        # Save to history
        batch_id = f"batch_{int(datetime.now().timestamp() * 1000)}"
        self.conn.execute(
            "INSERT INTO task_history (batch_id, tasks, executed_at) VALUES (?, ?, ?)",
            (batch_id, json.dumps(self.pending_tasks), datetime.now())
        )
        self.conn.commit()
        
        # Clear pending
        count = len(self.pending_tasks)
        self.pending_tasks = []
        
        return {
            "success": True,
            "batch_id": batch_id,
            "task_count": count,
            "commands": "\n".join(commands),
            "instruction": "Execute ALL commands above in ONE message for parallel execution"
        }
    
    def run_stdio(self):
        """Run as stdio MCP server"""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line)
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

def create_mcp_config():
    """Generate MCP configuration for Claude Desktop"""
    config = {
        "mcpServers": {
            "parallel-tasks": {
                "command": "python3",
                "args": [str(Path(__file__).absolute())],
                "env": {}
            }
        }
    }
    
    config_path = Path.home() / ".claude" / "mcp_config.json"
    
    print("Add this to your Claude Desktop MCP configuration:")
    print(json.dumps(config, indent=2))
    print(f"\nConfiguration location: {config_path}")
    
    return config

# Standalone test mode
def test_mode():
    """Test the parallel coordinator without MCP"""
    mcp = MinimalParallelMCP()
    
    # Queue some tasks
    print("Queueing tasks...")
    mcp.queue_task({"agent": "researcher", "task": "Research physics optimizations"})
    mcp.queue_task({"agent": "coder", "task": "Implement object pooling"})
    mcp.queue_task({"agent": "tester", "task": "Create performance tests"})
    
    # Execute batch
    result = mcp.execute_batch()
    
    print("\n" + "=" * 70)
    print("PARALLEL EXECUTION COMMANDS:")
    print("=" * 70)
    print(result["commands"])
    print("=" * 70)
    print("\nCopy ALL commands above and paste into Claude Code in ONE message")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Minimal MCP Server for Parallel Tasks")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--config", action="store_true", help="Show MCP configuration")
    args = parser.parse_args()
    
    if args.test:
        test_mode()
    elif args.config:
        create_mcp_config()
    else:
        # Run as MCP server
        server = MinimalParallelMCP()
        server.run_stdio()
