#!/usr/bin/env python3
"""
Initialize the short-term memory SQLite database
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime

class SessionDB:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).parent / "session_state.db"
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize database with schema"""
        self.conn = sqlite3.connect(self.db_path)
        
        # Read and execute schema
        schema_file = Path(__file__).parent / "schema.sql"
        if schema_file.exists():
            with open(schema_file, 'r') as f:
                schema = f.read()
                self.conn.executescript(schema)
                self.conn.commit()
        
        print(f"✅ Database initialized at {self.db_path}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Initialize the database when run directly
    with SessionDB() as db:
        print("📊 Database structure created successfully!")
        
        # Show tables created
        cursor = db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\n📋 Tables created:")
        for table in tables:
            print(f"  - {table[0]}")
            
            # Show column info for each table
            cursor.execute(f"PRAGMA table_info({table[0]});")
            columns = cursor.fetchall()
            for col in columns:
                print(f"    • {col[1]} ({col[2]})")
