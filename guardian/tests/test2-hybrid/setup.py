#!/usr/bin/env python3
"""
Setup script for Test 2 with hybrid MCP + background approach
"""

import sqlite3
from pathlib import Path

def setup_database():
    """Create minimal MCP database for testing"""
    db_path = Path("/home/klaus/game-projects/claude-orchestrate/guardian/mcp-server/db/test.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create minimal tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            status TEXT DEFAULT 'inactive',
            last_heartbeat TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_agent TEXT,
            to_agent TEXT,
            message_type TEXT,
            content TEXT,
            file_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            read_at TIMESTAMP
        )
    """)
    
    # Register test agents
    cursor.execute("INSERT OR REPLACE INTO agents (id, status) VALUES ('agent1', 'inactive')")
    cursor.execute("INSERT OR REPLACE INTO agents (id, status) VALUES ('agent2', 'inactive')")
    
    conn.commit()
    conn.close()
    
    print(f"Database created at: {db_path}")
    return str(db_path)

if __name__ == "__main__":
    db_path = setup_database()
    print("\nTest 2 Hybrid Setup Complete!")
    print("\nHow to run the test:")
    print("1. In Claude, run these commands with run_in_background=True:")
    print(f'   Bash(command="python guardian/scripts/mcp_agent.py agent1 {db_path}", run_in_background=True)')
    print(f'   Bash(command="python guardian/scripts/mcp_agent.py agent2 {db_path}", run_in_background=True)')
    print("\n2. Send a message to trigger work:")
    print(f'   sqlite3 {db_path} "INSERT INTO messages (from_agent, to_agent, content) VALUES (\'claude\', \'agent2\', \'create_output\')"')
    print("\n3. Check status:")
    print(f'   sqlite3 {db_path} "SELECT * FROM messages"')
    print(f'   sqlite3 {db_path} "SELECT * FROM agents"')