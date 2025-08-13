#!/usr/bin/env python3
"""
Simple orchestration commands for Guardian
Claude can use this to manage agents
"""

import sqlite3
import sys
from pathlib import Path

class Orchestrator:
    def __init__(self, db_path=None):
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = Path(__file__).parent / "mcp-server/db/coordination.db"
    
    def send_message(self, from_agent, to_agent, content):
        """Send a message through MCP database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO messages (from_agent, to_agent, message_type, content, created_at)
            VALUES (?, ?, 'request', ?, datetime('now'))
        """, (from_agent, to_agent, content))
        
        conn.commit()
        conn.close()
        
        print(f"Message sent: {from_agent} → {to_agent}: {content}")
    
    def check_status(self):
        """Check status of all agents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, status, last_heartbeat FROM agents")
        agents = cursor.fetchall()
        
        print("\nAgent Status:")
        print("-" * 50)
        for agent_id, status, heartbeat in agents:
            print(f"{agent_id}: {status} (last seen: {heartbeat})")
        
        conn.close()
    
    def check_messages(self):
        """Check recent messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT from_agent, to_agent, content, read_at, created_at 
            FROM messages 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        messages = cursor.fetchall()
        
        print("\nRecent Messages:")
        print("-" * 50)
        for from_agent, to_agent, content, read_at, created_at in messages:
            status = "✓" if read_at else "○"
            print(f"{status} {from_agent} → {to_agent}: {content[:50]}")
            print(f"  {created_at}")
        
        conn.close()
    
    def stop_all(self):
        """Send stop signal to all agents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all active agents
        cursor.execute("SELECT id FROM agents WHERE status = 'active'")
        agents = cursor.fetchall()
        
        # Send stop message to each
        for (agent_id,) in agents:
            cursor.execute("""
                INSERT INTO messages (from_agent, to_agent, message_type, content, created_at)
                VALUES ('orchestrator', ?, 'control', 'STOP', datetime('now'))
            """, (agent_id,))
        
        conn.commit()
        conn.close()
        
        print(f"Stop signal sent to {len(agents)} agents")

def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print("Usage: orchestrate.py <command> [args]")
        print("Commands:")
        print("  send <from> <to> <message>  - Send message between agents")
        print("  status                       - Check agent status")
        print("  messages                     - Check recent messages")
        print("  stop                         - Stop all agents")
        return
    
    cmd = sys.argv[1]
    orch = Orchestrator()
    
    if cmd == "send" and len(sys.argv) >= 5:
        orch.send_message(sys.argv[2], sys.argv[3], ' '.join(sys.argv[4:]))
    elif cmd == "status":
        orch.check_status()
    elif cmd == "messages":
        orch.check_messages()
    elif cmd == "stop":
        orch.stop_all()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()