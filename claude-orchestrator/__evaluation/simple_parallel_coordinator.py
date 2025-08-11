#!/usr/bin/env python3
"""
Simple Parallel Task Coordinator for Claude Orchestrate
Minimal solution for parallel sub-agent execution in Claude Code
No complex dependencies, just SQLite and clear batching
"""

import sqlite3
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

class SimpleParallelCoordinator:
    """
    Lightweight coordinator that:
    1. Queues tasks in SQLite
    2. Generates batch commands for Claude
    3. Tracks execution state
    4. No complex MCP server needed
    """
    
    def __init__(self, db_path: str = ".orchestrate/state.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()
    
    def _init_db(self):
        """Create simple tables for task coordination"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS task_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT,
                agent_type TEXT,
                objective TEXT,
                priority INTEGER DEFAULT 50,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                result TEXT
            );
            
            CREATE TABLE IF NOT EXISTS batches (
                batch_id TEXT PRIMARY KEY,
                status TEXT DEFAULT 'pending',
                task_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                executed_at TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_batch_status ON task_queue(batch_id, status);
        """)
        self.conn.commit()
    
    def queue_task(self, agent_type: str, objective: str, priority: int = 50) -> int:
        """Queue a single task for batch execution"""
        cursor = self.conn.execute(
            "INSERT INTO task_queue (agent_type, objective, priority) VALUES (?, ?, ?)",
            (agent_type, objective, priority)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def create_batch(self, task_ids: Optional[List[int]] = None) -> str:
        """Create a batch from pending tasks"""
        batch_id = f"batch_{int(time.time() * 1000)}"
        
        # If no specific tasks, grab all pending
        if task_ids is None:
            cursor = self.conn.execute(
                "SELECT id FROM task_queue WHERE status = 'pending' ORDER BY priority DESC"
            )
            task_ids = [row[0] for row in cursor.fetchall()]
        
        if not task_ids:
            return None
        
        # Update tasks with batch_id
        self.conn.execute(
            f"UPDATE task_queue SET batch_id = ?, status = 'batched' WHERE id IN ({','.join('?' * len(task_ids))})",
            [batch_id] + task_ids
        )
        
        # Create batch record
        self.conn.execute(
            "INSERT INTO batches (batch_id, task_count) VALUES (?, ?)",
            (batch_id, len(task_ids))
        )
        self.conn.commit()
        
        return batch_id
    
    def get_batch_commands(self, batch_id: str) -> str:
        """Generate Claude Code commands for parallel execution"""
        cursor = self.conn.execute(
            "SELECT agent_type, objective FROM task_queue WHERE batch_id = ? ORDER BY priority DESC",
            (batch_id,)
        )
        tasks = cursor.fetchall()
        
        if not tasks:
            return ""
        
        # Generate the critical single-message batch
        commands = []
        commands.append("# " + "=" * 60)
        commands.append("# PARALLEL EXECUTION BATCH")
        commands.append(f"# Batch ID: {batch_id}")
        commands.append(f"# Tasks: {len(tasks)}")
        commands.append("# " + "=" * 60)
        commands.append("")
        commands.append("# CRITICAL: Execute ALL of these in ONE message:")
        commands.append("")
        
        for agent_type, objective in tasks:
            # Format: Task("AGENT_TYPE: objective")
            task_cmd = f'Task("{agent_type.upper()}: {objective}")'
            commands.append(task_cmd)
        
        commands.append("")
        commands.append("# " + "=" * 60)
        commands.append("# END BATCH - EXECUTE ALL ABOVE SIMULTANEOUSLY")
        commands.append("# " + "=" * 60)
        
        return "\n".join(commands)
    
    def mark_batch_executed(self, batch_id: str):
        """Mark batch as executed"""
        self.conn.execute(
            "UPDATE batches SET status = 'executed', executed_at = CURRENT_TIMESTAMP WHERE batch_id = ?",
            (batch_id,)
        )
        self.conn.execute(
            "UPDATE task_queue SET status = 'running', started_at = CURRENT_TIMESTAMP WHERE batch_id = ?",
            (batch_id,)
        )
        self.conn.commit()
    
    def complete_task(self, task_id: int, result: Any):
        """Mark individual task as complete"""
        self.conn.execute(
            "UPDATE task_queue SET status = 'completed', completed_at = CURRENT_TIMESTAMP, result = ? WHERE id = ?",
            (json.dumps(result), task_id)
        )
        self.conn.commit()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current coordination status"""
        cursor = self.conn.execute("""
            SELECT status, COUNT(*) FROM task_queue GROUP BY status
        """)
        status_counts = dict(cursor.fetchall())
        
        cursor = self.conn.execute("""
            SELECT COUNT(*) as total, 
                   COUNT(CASE WHEN status = 'executed' THEN 1 END) as executed
            FROM batches
        """)
        batch_stats = cursor.fetchone()
        
        return {
            "tasks": status_counts,
            "batches": {
                "total": batch_stats[0],
                "executed": batch_stats[1]
            }
        }

class ParallelExecutor:
    """
    Simple executor that generates proper Claude instructions
    """
    
    @staticmethod
    def generate_claude_script(tasks: List[Dict[str, str]]) -> str:
        """Generate a complete Claude script for parallel execution"""
        
        script = []
        
        # Header
        script.append("#!/usr/bin/env python3")
        script.append('"""')
        script.append("AUTO-GENERATED PARALLEL EXECUTION SCRIPT")
        script.append(f"Generated: {datetime.now().isoformat()}")
        script.append('"""')
        script.append("")
        script.append("# " + "=" * 70)
        script.append("# INSTRUCTIONS FOR CLAUDE CODE:")
        script.append("# 1. Read ALL Task commands below")
        script.append("# 2. Execute them in a SINGLE message")
        script.append("# 3. Each task runs in PARALLEL, not sequentially")
        script.append("# " + "=" * 70)
        script.append("")
        script.append('print("PARALLEL BATCH EXECUTION")')
        script.append('print("=" * 70)')
        script.append("")
        
        # Task commands
        for task in tasks:
            agent = task.get("agent", "worker")
            objective = task.get("objective", "undefined task")
            script.append(f'print(\'Task("{agent.upper()}: {objective}")\')')
        
        script.append("")
        script.append('print("=" * 70)')
        script.append('print("EXECUTE ALL ABOVE IN ONE MESSAGE")')
        
        return "\n".join(script)
    
    @staticmethod
    def create_coordination_file(batch_id: str, tasks: List[Dict]) -> Path:
        """Create coordination file for agent state sharing"""
        coord_path = Path(f".orchestrate/batches/{batch_id}.json")
        coord_path.parent.mkdir(parents=True, exist_ok=True)
        
        coordination_data = {
            "batch_id": batch_id,
            "created": datetime.now().isoformat(),
            "tasks": tasks,
            "shared_memory": {},
            "agent_states": {}
        }
        
        with open(coord_path, 'w') as f:
            json.dump(coordination_data, f, indent=2)
        
        return coord_path

def main():
    """Example usage"""
    
    # Initialize coordinator
    coord = SimpleParallelCoordinator()
    
    # Queue some tasks
    print("Queueing tasks...")
    coord.queue_task("researcher", "Research Unity physics optimization patterns")
    coord.queue_task("coder", "Implement object pooling system") 
    coord.queue_task("tester", "Create performance benchmarks")
    coord.queue_task("documenter", "Update physics documentation")
    
    # Create batch
    batch_id = coord.create_batch()
    print(f"\nCreated batch: {batch_id}")
    
    # Get commands for Claude
    commands = coord.get_batch_commands(batch_id)
    print("\nCommands for Claude Code:")
    print(commands)
    
    # Save to file for easy execution
    output_path = Path(f".orchestrate/execute_{batch_id}.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(commands)
    
    print(f"\nCommands saved to: {output_path}")
    print("\nStatus:", coord.get_status())
    
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("1. Copy the Task commands above")
    print("2. Paste them ALL into Claude Code in ONE message")
    print("3. Claude will execute them in parallel")
    print("=" * 70)

if __name__ == "__main__":
    main()
