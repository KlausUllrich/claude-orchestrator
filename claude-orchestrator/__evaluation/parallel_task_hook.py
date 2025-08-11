#!/usr/bin/env python3
"""
Hook-based Parallel Task Manager for Claude Orchestrate
Integrates with your existing hook system to enable parallel execution
"""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Callable
from datetime import datetime

class ParallelTaskHook:
    """
    Hook that intercepts task creation and batches them for parallel execution
    Fits into your existing claude-template hook system
    """
    
    def __init__(self, db_path: str = ".orchestrate/state.db"):
        self.db_path = Path(db_path)
        self.pending_tasks = []
        self.batch_threshold = 3  # Auto-batch after N tasks
        self.auto_batch = True
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """Initialize simple task tracking"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS parallel_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                agent_type TEXT,
                task TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def pre_task(self, agent_type: str, task: str, **kwargs) -> Dict[str, Any]:
        """
        Hook called before task execution
        Intercepts and queues tasks for batching
        """
        # Add to pending batch
        self.pending_tasks.append({
            "agent_type": agent_type,
            "task": task,
            "timestamp": datetime.now().isoformat()
        })
        
        # Store in DB
        self.conn.execute(
            "INSERT INTO parallel_tasks (agent_type, task) VALUES (?, ?)",
            (agent_type, task)
        )
        self.conn.commit()
        
        # Check if we should auto-batch
        if self.auto_batch and len(self.pending_tasks) >= self.batch_threshold:
            return self.execute_batch()
        
        return {
            "action": "queue",
            "queued_count": len(self.pending_tasks),
            "message": f"Task queued for parallel execution ({len(self.pending_tasks)}/{self.batch_threshold})"
        }
    
    def execute_batch(self) -> Dict[str, Any]:
        """
        Generate and return parallel execution commands
        """
        if not self.pending_tasks:
            return {"action": "none", "message": "No tasks to execute"}
        
        # Generate parallel commands
        commands = self._generate_parallel_commands(self.pending_tasks)
        
        # Clear pending tasks
        count = len(self.pending_tasks)
        self.pending_tasks = []
        
        return {
            "action": "execute_parallel",
            "commands": commands,
            "task_count": count,
            "message": f"Execute {count} tasks in parallel"
        }
    
    def _generate_parallel_commands(self, tasks: List[Dict]) -> str:
        """Generate the critical single-message batch"""
        lines = [
            "# PARALLEL EXECUTION REQUIRED",
            "# Execute ALL of these Task commands in ONE message:",
            ""
        ]
        
        for task in tasks:
            agent = task["agent_type"]
            objective = task["task"]
            lines.append(f'Task("{agent}: {objective}")')
        
        lines.extend([
            "",
            "# END PARALLEL BATCH"
        ])
        
        return "\n".join(lines)
    
    def force_batch(self) -> str:
        """Force execution of pending tasks"""
        result = self.execute_batch()
        return result.get("commands", "")

class MessageQueueHook:
    """
    SQLite-based message queue for agent communication
    Prevents agents from interfering with each other
    """
    
    def __init__(self, db_path: str = ".orchestrate/messages.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()
    
    def _init_db(self):
        """Create message queue table"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS message_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_agent TEXT,
                recipient_agent TEXT,
                message_type TEXT,
                payload TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read_at TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def send_message(self, sender: str, recipient: str, 
                    msg_type: str, payload: Any) -> int:
        """Queue a message between agents"""
        cursor = self.conn.execute(
            """INSERT INTO message_queue 
               (sender_agent, recipient_agent, message_type, payload) 
               VALUES (?, ?, ?, ?)""",
            (sender, recipient, msg_type, json.dumps(payload))
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_messages(self, agent: str, mark_read: bool = True) -> List[Dict]:
        """Get pending messages for an agent"""
        cursor = self.conn.execute(
            """SELECT id, sender_agent, message_type, payload, created_at
               FROM message_queue 
               WHERE recipient_agent = ? AND status = 'pending'
               ORDER BY created_at""",
            (agent,)
        )
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "id": row[0],
                "sender": row[1],
                "type": row[2],
                "payload": json.loads(row[3]),
                "timestamp": row[4]
            })
        
        if mark_read and messages:
            msg_ids = [m["id"] for m in messages]
            placeholders = ','.join('?' * len(msg_ids))
            self.conn.execute(
                f"""UPDATE message_queue 
                    SET status = 'read', read_at = CURRENT_TIMESTAMP 
                    WHERE id IN ({placeholders})""",
                msg_ids
            )
            self.conn.commit()
        
        return messages

class SimpleOrchestrator:
    """
    Minimal orchestrator that coordinates parallel agents
    Integrates with your hook system
    """
    
    def __init__(self):
        self.task_hook = ParallelTaskHook()
        self.message_queue = MessageQueueHook()
        self.hooks = {
            "pre_task": self.task_hook.pre_task,
            "execute_batch": self.task_hook.execute_batch,
            "send_message": self.message_queue.send_message,
            "get_messages": self.message_queue.get_messages
        }
    
    def register_hook(self, name: str, func: Callable):
        """Register a custom hook"""
        self.hooks[name] = func
    
    def trigger_hook(self, name: str, *args, **kwargs) -> Any:
        """Trigger a registered hook"""
        if name in self.hooks:
            return self.hooks[name](*args, **kwargs)
        return None
    
    def queue_parallel_task(self, agent: str, task: str) -> Dict:
        """Queue a task for parallel execution"""
        return self.task_hook.pre_task(agent, task)
    
    def execute_parallel_batch(self) -> str:
        """Force execution of all pending tasks"""
        return self.task_hook.force_batch()
    
    def get_parallel_script(self, tasks: List[Dict[str, str]]) -> str:
        """
        Generate a complete script for Claude to execute
        This is the KEY - everything in ONE message
        """
        script = [
            "# Auto-generated parallel execution script",
            f"# Generated: {datetime.now().isoformat()}",
            "",
            "# CRITICAL: Copy ALL Task commands below",
            "# Paste them into Claude Code in ONE message",
            "",
            "# " + "=" * 60,
            "# BEGIN PARALLEL EXECUTION",
            "# " + "=" * 60,
            ""
        ]
        
        for task in tasks:
            agent = task.get("agent", "worker")
            objective = task.get("objective", "")
            script.append(f'Task("{agent.upper()}: {objective}")')
        
        script.extend([
            "",
            "# " + "=" * 60,
            "# END PARALLEL EXECUTION",
            "# " + "=" * 60,
            "",
            "# Remember: ALL tasks above must be executed SIMULTANEOUSLY"
        ])
        
        return "\n".join(script)

# Example usage with your hook system
def integrate_with_claude_template():
    """
    Example of how to integrate with your existing hook system
    """
    
    # Initialize orchestrator
    orchestrator = SimpleOrchestrator()
    
    # Your existing hook registration (from claude-template)
    # hook_manager.register("pre_task", orchestrator.trigger_hook)
    
    # Queue tasks through hooks
    orchestrator.queue_parallel_task("researcher", "Research Unity optimization")
    orchestrator.queue_parallel_task("coder", "Implement pooling system")
    orchestrator.queue_parallel_task("tester", "Create benchmarks")
    
    # Get batch commands
    commands = orchestrator.execute_parallel_batch()
    
    print("Execute these in Claude Code (ALL IN ONE MESSAGE):")
    print(commands)
    
    # Agent communication example
    orchestrator.message_queue.send_message(
        "researcher", "coder",
        "optimization_tips",
        {"tips": ["Use object pooling", "Batch draw calls"]}
    )
    
    # Coder agent retrieves messages
    messages = orchestrator.message_queue.get_messages("coder")
    print(f"\nMessages for coder: {messages}")

if __name__ == "__main__":
    # Demo
    integrate_with_claude_template()
