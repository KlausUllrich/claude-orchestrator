#!/usr/bin/env python3
"""
Handover Manager - Helper tools for LLM-driven handover creation

This module provides utilities that the LLM can use to gather information
and save handover documents. The LLM remains in control of the content
creation and user interaction.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import sqlite3
import json
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))
from utils import find_project_root

class HandoverManager:
    """Provides helper functions for handover management"""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize handover manager
        
        Args:
            project_root: Root directory of the project (defaults to finding it)
        """
        if project_root is None:
            # Use utility to find project root reliably
            self.project_root = find_project_root()
            if not self.project_root:
                # Fallback to old method
                self.project_root = Path(__file__).parent.parent.parent
        else:
            self.project_root = Path(project_root)
            
        self.handover_dir = self.project_root / "docs" / "status"
        self.db_path = Path(__file__).parent.parent / "short-term-memory" / "session_state.db"
        self.todo_path = self.project_root / "docs" / "status" / "todo.md"
        
        # Ensure handover directory exists
        self.handover_dir.mkdir(parents=True, exist_ok=True)
    
    def gather_session_info(self) -> Dict[str, Any]:
        """Gather all available session information for LLM to analyze
        
        This is a helper function that collects raw data. The LLM will
        interpret this data and create the actual handover content.
        
        Returns:
            Dictionary with various session information
        """
        info = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "git_status": self._get_git_status(),
            "modified_files": self._get_modified_files(),
            "database_state": self._check_database_state(),
            "todo_items": self._get_todo_priorities(),
            "project_structure": self._get_relevant_structure(),
            "previous_handover": self._get_previous_handover_summary(),
            "session_goals": self._extract_session_goals(),
            "warnings": [],
            "template_path": str(self.project_root / "claude-orchestrator" / "resource-library" / "documents" / "handovers" / "Session_Handover_Template.md")
        }
        
        return info
    
    def archive_and_save_handover(self, content: str) -> str:
        """Archive existing handover and save new content
        
        This is called by the LLM after the user has approved the handover.
        
        Args:
            content: The complete handover content created by the LLM
            
        Returns:
            Path to the saved handover
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        
        # Archive existing handover if it exists
        self._archive_existing_handover(timestamp)
        
        # Save new handover
        handover_path = self.handover_dir / "handover-next.md"
        with open(handover_path, 'w') as f:
            f.write(content)
        
        # Also save timestamped archive
        archive_dir = self.handover_dir / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_path = archive_dir / f"handover-{timestamp}.md"
        with open(archive_path, 'w') as f:
            f.write(content)
        
        return str(handover_path)
    
    def read_handover(self) -> Optional[str]:
        """Read the most recent handover document
        
        Returns:
            Content of the handover document or None if not found
        """
        handover_path = self.handover_dir / "handover-next.md"
        
        if not handover_path.exists():
            return None
        
        with open(handover_path, 'r') as f:
            content = f.read()
        
        return content
    
    def _archive_existing_handover(self, timestamp: str):
        """Archive the existing handover-next.md if it exists"""
        current_handover = self.handover_dir / "handover-next.md"
        
        if current_handover.exists():
            archive_dir = self.handover_dir / "archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            archive_path = archive_dir / f"handover-archived-{timestamp}.md"
            
            with open(current_handover, 'r') as f:
                content = f.read()
            
            with open(archive_path, 'w') as f:
                f.write(content)
            
            return str(archive_path.relative_to(self.project_root))
        return None
    
    def _get_git_status(self) -> Dict[str, Any]:
        """Get detailed git status information"""
        status = {"branch": "unknown", "changes": [], "uncommitted_count": 0}
        
        try:
            # Get branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, cwd=self.project_root
            )
            status["branch"] = result.stdout.strip()
            
            # Get changed files
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=self.project_root
            )
            
            if result.stdout:
                changes = result.stdout.strip().split('\n')
                status["changes"] = changes
                status["uncommitted_count"] = len(changes)
            
            # Get last commit
            result = subprocess.run(
                ["git", "log", "-1", "--oneline"],
                capture_output=True, text=True, cwd=self.project_root
            )
            status["last_commit"] = result.stdout.strip()
            
        except Exception as e:
            status["error"] = str(e)
        
        return status
    
    def _get_modified_files(self) -> List[Dict[str, str]]:
        """Get list of recently modified files with context"""
        modified = []
        
        try:
            # Get git status for modified files
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=self.project_root
            )
            
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        status = line[:2]
                        filepath = line[3:]
                        
                        file_info = {
                            "path": filepath,
                            "status": "modified" if 'M' in status else "added" if 'A' in status else "other",
                            "git_status": status
                        }
                        
                        # Check if it's a Python file that might need testing
                        if filepath.endswith('.py'):
                            file_info["needs_testing"] = True
                        
                        # Check if it's a command file
                        if '.claude/commands' in filepath:
                            file_info["type"] = "command"
                        
                        modified.append(file_info)
            
        except Exception:
            pass
        
        return modified
    
    def _check_database_state(self) -> Dict[str, Any]:
        """Check database state and contents"""
        db_info = {
            "exists": self.db_path.exists(),
            "tables": [],
            "warnings": []
        }
        
        if not db_info["exists"]:
            db_info["warnings"].append("Session database not found")
            return db_info
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            db_info["tables"] = [t[0] for t in tables]
            
            # Check for expected tables
            expected = ['session_state', 'checkpoints', 'decisions', 'issues']
            missing = [t for t in expected if t not in db_info["tables"]]
            if missing:
                db_info["warnings"].append(f"Missing expected tables: {', '.join(missing)}")
            
            # Get row counts for existing tables
            for table in db_info["tables"]:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    db_info[f"{table}_count"] = count
                except:
                    pass
            
            conn.close()
            
        except Exception as e:
            db_info["warnings"].append(f"Database error: {str(e)}")
        
        return db_info
    
    def _get_todo_priorities(self) -> Dict[str, List[str]]:
        """Extract immediate and short-term priorities from TODO"""
        priorities = {
            "immediate": [],
            "short_term": [],
            "in_progress": []
        }
        
        if not self.todo_path.exists():
            return priorities
        
        try:
            with open(self.todo_path, 'r') as f:
                lines = f.readlines()
            
            section = None
            for line in lines:
                # Detect sections
                if "IMMEDIATE PRIORITY" in line:
                    section = "immediate"
                elif "SHORT TERM" in line:
                    section = "short_term"
                elif "MEDIUM TERM" in line or "LONG TERM" in line:
                    section = None
                # Extract items
                elif section and line.strip().startswith("- [ ]"):
                    item = line.strip()[6:]  # Remove "- [ ] "
                    if len(priorities[section]) < 5:  # Limit to 5 items per section
                        priorities[section].append(item)
                elif section and line.strip().startswith("- [x]"):
                    # Recently completed item
                    item = line.strip()[6:] + " (recently completed)"
                    if section == "immediate" and len(priorities["in_progress"]) < 3:
                        priorities["in_progress"].append(item)
        
        except Exception:
            pass
        
        return priorities
    
    def _get_relevant_structure(self) -> Dict[str, List[str]]:
        """Get relevant project structure for context"""
        structure = {
            "commands": [],
            "brain_modules": [],
            "workflows": [],
            "recent_docs": []
        }
        
        try:
            # List command files
            commands_dir = self.project_root / ".claude" / "commands"
            if commands_dir.exists():
                structure["commands"] = [f.name for f in commands_dir.glob("*.md")]
            
            # List brain modules
            brain_dir = self.project_root / "claude-orchestrator" / "brain"
            if brain_dir.exists():
                structure["brain_modules"] = [f.name for f in brain_dir.glob("*.py")]
            
            # List active workflows
            workflows_dir = self.project_root / "claude-orchestrator" / "workflows"
            if workflows_dir.exists():
                structure["workflows"] = [d.name for d in workflows_dir.iterdir() if d.is_dir()]
            
            # Recent documentation
            docs_status = self.project_root / "docs" / "status"
            if docs_status.exists():
                # Get recently modified docs
                docs = sorted(docs_status.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
                structure["recent_docs"] = [d.name for d in docs[:5]]
        
        except Exception:
            pass
        
        return structure
    
    def _get_previous_handover_summary(self) -> Dict[str, Any]:
        """Extract key information from previous handover"""
        summary = {
            "exists": False,
            "session_goals": [],
            "warnings": [],
            "incomplete_tasks": []
        }
        
        handover_path = self.handover_dir / "handover-next.md"
        if handover_path.exists():
            summary["exists"] = True
            try:
                with open(handover_path, 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # Extract session goals
                    in_goals = False
                    for line in lines:
                        if "Session Goal" in line or "Next Session Goals" in line:
                            in_goals = True
                        elif in_goals and line.startswith("#"):
                            in_goals = False
                        elif in_goals and line.strip().startswith("-"):
                            summary["session_goals"].append(line.strip())
                    
                    # Extract warnings
                    if "Critical Warnings" in content or "Known Issues" in content:
                        in_warnings = False
                        for line in lines:
                            if "Warning" in line or "Issues" in line:
                                in_warnings = True
                            elif in_warnings and line.startswith("#"):
                                in_warnings = False
                            elif in_warnings and "⚠️" in line:
                                summary["warnings"].append(line.strip())
            except Exception as e:
                summary["error"] = str(e)
        
        return summary
    
    def _extract_session_goals(self) -> List[str]:
        """Extract session goals from previous handover"""
        prev = self._get_previous_handover_summary()
        return prev.get("session_goals", [])
    
    def get_info_summary(self) -> str:
        """Get a formatted summary of session info for display
        
        This provides a human-readable summary that the LLM can show to the user.
        """
        info = self.gather_session_info()
        
        summary = []
        summary.append(f"📊 Session Information Summary")
        summary.append(f"{'='*60}")
        
        # Git status
        git = info.get("git_status", {})
        summary.append(f"\n📝 Git Status:")
        summary.append(f"  Branch: {git.get('branch', 'unknown')}")
        summary.append(f"  Uncommitted changes: {git.get('uncommitted_count', 0)}")
        if git.get('last_commit'):
            summary.append(f"  Last commit: {git['last_commit']}")
        
        # Modified files
        if info.get("modified_files"):
            summary.append(f"\n📁 Modified Files:")
            for file in info["modified_files"][:10]:  # Limit to 10
                summary.append(f"  - {file['path']} ({file['status']})")
        
        # Database state
        db = info.get("database_state", {})
        if db.get("warnings"):
            summary.append(f"\n⚠️ Database Warnings:")
            for warning in db["warnings"]:
                summary.append(f"  - {warning}")
        
        # TODO priorities
        todos = info.get("todo_items", {})
        if todos.get("immediate"):
            summary.append(f"\n🎯 Immediate Priorities from TODO:")
            for item in todos["immediate"][:3]:
                summary.append(f"  - {item}")
        
        # Project structure
        struct = info.get("project_structure", {})
        if struct.get("commands"):
            summary.append(f"\n📋 Available Commands: {', '.join(struct['commands'][:5])}")
        
        # Previous handover context
        prev = info.get("previous_handover", {})
        if prev.get("exists"):
            summary.append(f"\n📖 Previous Handover Context:")
            if prev.get("session_goals"):
                summary.append(f"  Expected goals for this session:")
                for goal in prev["session_goals"][:3]:
                    summary.append(f"    {goal}")
            if prev.get("warnings"):
                summary.append(f"  Carried-over warnings:")
                for warning in prev["warnings"][:2]:
                    summary.append(f"    {warning}")
        
        summary.append(f"\n{'='*60}")
        summary.append(f"\n💡 Use this information to create a comprehensive handover")
        summary.append(f"   following: {info.get('template_path', 'template')}")
        
        return '\n'.join(summary)


def main():
    """CLI interface for testing"""
    import sys
    
    manager = HandoverManager()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "info":
            print(manager.get_info_summary())
            
        elif sys.argv[1] == "gather":
            info = manager.gather_session_info()
            print(json.dumps(info, indent=2, default=str))
            
        elif sys.argv[1] == "save":
            if len(sys.argv) > 2:
                # Read content from stdin or file
                if sys.argv[2] == "-":
                    content = sys.stdin.read()
                else:
                    with open(sys.argv[2], 'r') as f:
                        content = f.read()
                
                path = manager.archive_and_save_handover(content)
                print(f"✅ Handover saved to: {path}")
            else:
                print("Usage: handover-manager.py save [file|-]")
                
        elif sys.argv[1] == "read":
            content = manager.read_handover()
            if content:
                print(content)
            else:
                print("No handover found")
    else:
        print("Usage: handover-manager.py [info|gather|save|read]")
        print("  info   - Show formatted session information")
        print("  gather - Get raw JSON data for LLM analysis")
        print("  save   - Archive and save handover content")
        print("  read   - Read current handover")


if __name__ == "__main__":
    main()