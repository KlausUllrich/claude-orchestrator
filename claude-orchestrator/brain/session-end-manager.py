#!/usr/bin/env python3
"""
Session End Manager - Minimal coordinator for session end workflow

This module provides minimal helper functions for the LLM orchestrator.
The actual logic and decisions are handled by agents and the orchestrating LLM.
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import subprocess
from typing import Dict, List, Optional, Tuple

class SessionEndManager:
    """Minimal session end coordinator - agents do the real work"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.orchestrator_root = Path(__file__).parent.parent
        self.db_path = self.orchestrator_root / "short-term-memory" / "session_state.db"
        self.reports_dir = self.project_root / "docs" / "status" / "session-reports"
        
    def get_task_documents_path(self) -> str:
        """Return path to task documents for agent execution"""
        return str(self.orchestrator_root / "resource-library" / "documents" / "documentation-tasks")
    
    def get_maintenance_agent_path(self) -> str:
        """Return path to maintenance agent template"""
        return str(self.orchestrator_root / "resource-library" / "agents" / "maintenance-agent" / "maintenance-agent.md")
    
    def get_reports_directory(self) -> str:
        """Return path where agents should save reports"""
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        return str(self.reports_dir)
    
    def get_session_info_for_agent(self) -> Dict:
        """Provide basic session info for agents to use"""
        info = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "reports_dir": str(self.reports_dir),
            "session_id": datetime.now().strftime("session-%Y%m%d-%H%M%S")
        }
        
        # Add git status
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            info["git_changes"] = len(result.stdout.strip().split('\n'))
        except:
            info["git_changes"] = "unknown"
        
        return info
    
    def create_session_savepoint(self, notes: str = "") -> Tuple[bool, str]:
        """
        Create a database savepoint - but let the agent decide what to record
        
        Args:
            notes: Agent-provided context about what was accomplished
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get or create session
            session_id = datetime.now().strftime("session-%Y%m%d-%H%M%S")
            
            # Check if session exists
            cursor.execute("SELECT session_id FROM session_state WHERE session_id = ?", (session_id,))
            if not cursor.fetchone():
                # Create session record
                cursor.execute("""
                    INSERT INTO session_state (session_id, status, current_task)
                    VALUES (?, 'ending', ?)
                """, (session_id, notes or "Session end"))
            
            # Create savepoint
            cursor.execute("""
                INSERT INTO checkpoints (
                    session_id,
                    trigger_type,
                    current_task,
                    next_steps,
                    checkpoint_number
                ) VALUES (?, 'session_end', ?, 'See handover document', 
                    (SELECT COALESCE(MAX(checkpoint_number), 0) + 1 
                     FROM checkpoints WHERE session_id = ?))
            """, (session_id, notes or "Session completed", session_id))
            
            conn.commit()
            conn.close()
            
            return True, f"Savepoint created for session {session_id}"
            
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
    
    def prompt_for_agent_execution(self) -> Dict:
        """Return information the orchestrator needs to launch agents"""
        return {
            "agent_template": self.get_maintenance_agent_path(),
            "task_documents": self.get_task_documents_path(),
            "reports_directory": self.get_reports_directory(),
            "session_context": self.get_session_info_for_agent(),
            "instructions": """
To execute maintenance tasks:
1. Use Task tool to launch maintenance-agent with each task document
2. Agents will analyze and create reports  
3. Review reports and present findings to user
4. Only execute changes after user approval

Example:
- Task: 'Check unreferenced docs' 
- Agent: maintenance-agent
- Document: unreferenced_documents_check.md
- Result: Report saved to session-reports/
"""
        }

# Minimal helper functions for orchestrator

def get_session_context():
    """Get context for session end"""
    manager = SessionEndManager()
    context = manager.prompt_for_agent_execution()
    
    print("Session End Context:")
    print(json.dumps(context, indent=2))
    return context

def create_savepoint(notes=""):
    """Create database savepoint"""
    manager = SessionEndManager()
    success, message = manager.create_session_savepoint(notes)
    print(message)
    return success

def get_git_status():
    """Simple git status for orchestrator"""
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print(f"Uncommitted changes:\n{result.stdout}")
        else:
            print("No uncommitted changes")
            
        return result.stdout
    except Exception as e:
        print(f"Git status failed: {e}")
        return None

if __name__ == "__main__":
    # Simple CLI interface
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "context":
            get_session_context()
        elif command == "savepoint":
            notes = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
            create_savepoint(notes)
        elif command == "git-status":
            get_git_status()
        else:
            print(f"Unknown command: {command}")
            print("Available: context, savepoint, git-status")
    else:
        print("Session End Manager")
        print("Usage: python session-end-manager.py [command]")
        print("Commands:")
        print("  context    - Get session end context for agents")
        print("  savepoint  - Create database savepoint")
        print("  git-status - Show git status")