#!/usr/bin/env python3
"""
Demonstrate how the SQLite session database works
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from session_db import SessionManager
from datetime import datetime

def demonstrate_db():
    """Show how the database works"""
    
    # Initialize the session manager
    manager = SessionManager()
    
    print("🚀 Starting a new session...")
    session_id = manager.start_session(
        current_task="Testing tool-development workflow",
        workflow="tool-development"
    )
    print(f"✅ Session created: {session_id}")
    
    print("\n📝 Logging a decision...")
    manager.log_decision(
        what_was_decided="Created tool-development workflow",
        reason="Need to dogfood the orchestrator",
        approved_by_user=True
    )
    print("✅ Decision logged")
    
    print("\n⚠️ Logging an issue...")
    manager.log_issue(
        issue_description="Context Guardian cannot track Claude Code tokens",
        resolution_attempted="Documented limitation, using time-based checkpoints",
        resolved=True
    )
    print("✅ Issue logged")
    
    print("\n💾 Creating a checkpoint...")
    checkpoint_num = manager.create_checkpoint(
        trigger_type="manual",
        current_task="Implementing SQLite session management",
        completed_items=["Created workflow", "Built database schema", "Added commands"],
        pending_decisions=["How to track tokens in Claude Code"],
        active_issues=[],
        next_steps="Test checkpoint system and update documentation",
        context_percent=0  # Since we can't track in Claude Code
    )
    print(f"✅ Checkpoint #{checkpoint_num} created")
    
    print("\n⏰ Checking if checkpoint is due...")
    is_due = manager.check_checkpoint_due()
    print(f"Checkpoint due: {is_due}")
    
    print("\n📊 Getting last checkpoint...")
    last_checkpoint = manager.get_last_checkpoint()
    if last_checkpoint:
        print(f"Last checkpoint: #{last_checkpoint['checkpoint_number']}")
        print(f"Created at: {last_checkpoint['timestamp']}")
        print(f"Task: {last_checkpoint['current_task']}")
    
    manager.close()
    print("\n✅ Database demonstration complete!")

if __name__ == "__main__":
    demonstrate_db()
