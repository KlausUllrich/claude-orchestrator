#!/usr/bin/env python3
"""
Session management functions for short-term memory
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import uuid

class SessionManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).parent / "session_state.db"
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.current_session_id = None
    
    def start_session(self, current_task=None, workflow="tool-development"):
        """Start a new session"""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S_") + str(uuid.uuid4())[:8]
        self.current_session_id = session_id
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO session_state (session_id, current_task, workflow)
            VALUES (?, ?, ?)
        """, (session_id, current_task, workflow))
        
        # Initialize checkpoint schedule
        cursor.execute("""
            INSERT INTO checkpoint_schedule (session_id, next_checkpoint_due)
            VALUES (?, ?)
        """, (session_id, datetime.now() + timedelta(minutes=30)))
        
        self.conn.commit()
        return session_id

    
    def create_checkpoint(self, trigger_type, current_task, completed_items=None, 
                         pending_decisions=None, active_issues=None, next_steps=None,
                         context_percent=0):
        """Create a checkpoint"""
        if not self.current_session_id:
            raise ValueError("No active session")
        
        cursor = self.conn.cursor()
        
        # Get checkpoint count
        cursor.execute("""
            SELECT checkpoint_count FROM checkpoint_schedule 
            WHERE session_id = ?
        """, (self.current_session_id,))
        row = cursor.fetchone()
        checkpoint_num = (row['checkpoint_count'] + 1) if row else 1
        
        # Create checkpoint
        cursor.execute("""
            INSERT INTO checkpoints (
                session_id, trigger_type, current_task, completed_items,
                pending_decisions, active_issues, next_steps, 
                context_usage_percent, checkpoint_number
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.current_session_id, trigger_type, current_task,
            json.dumps(completed_items or []),
            json.dumps(pending_decisions or []),
            json.dumps(active_issues or []),
            next_steps, context_percent, checkpoint_num
        ))
        
        # Update checkpoint schedule
        cursor.execute("""
            UPDATE checkpoint_schedule 
            SET last_checkpoint_time = CURRENT_TIMESTAMP,
                checkpoint_count = ?,
                next_checkpoint_due = ?
            WHERE session_id = ?
        """, (checkpoint_num, 
              datetime.now() + timedelta(minutes=30),
              self.current_session_id))
        
        self.conn.commit()
        return checkpoint_num

    
    def log_decision(self, what_was_decided, reason=None, approved_by_user=False):
        """Log a decision made during the session"""
        if not self.current_session_id:
            raise ValueError("No active session")
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO decisions (session_id, what_was_decided, reason, approved_by_user)
            VALUES (?, ?, ?, ?)
        """, (self.current_session_id, what_was_decided, reason, approved_by_user))
        self.conn.commit()
    
    def log_issue(self, issue_description, resolution_attempted=None, resolved=False):
        """Log an issue encountered"""
        if not self.current_session_id:
            raise ValueError("No active session")
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO issues (session_id, issue_description, resolution_attempted, resolved)
            VALUES (?, ?, ?, ?)
        """, (self.current_session_id, issue_description, resolution_attempted, resolved))
        self.conn.commit()
    
    def get_last_checkpoint(self):
        """Get the most recent checkpoint"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM checkpoints 
            ORDER BY timestamp DESC 
            LIMIT 1
        """)
        return cursor.fetchone()
    
    def check_checkpoint_due(self):
        """Check if a checkpoint is due"""
        if not self.current_session_id:
            return False
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT next_checkpoint_due FROM checkpoint_schedule
            WHERE session_id = ?
        """, (self.current_session_id,))
        row = cursor.fetchone()
        
        if row and row['next_checkpoint_due']:
            due_time = datetime.fromisoformat(row['next_checkpoint_due'])
            return datetime.now() >= due_time
        return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
