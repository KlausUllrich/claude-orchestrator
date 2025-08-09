#!/usr/bin/env python3
"""
post_cleanup.py - Triggers after cleanup to commit changes
Location: .claude/hooks/post_cleanup.py
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


def check_git_repo():
    """Check if we're in a git repository"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_git_status():
    """Get current git status"""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def load_session_data():
    """Load the archived session data"""
    claude_dir = Path('.claude')
    archive_dir = claude_dir / 'archive'
    
    if not archive_dir.exists():
        return None
    
    # Get the most recent archive file
    archives = sorted(archive_dir.glob('session_*.json'), reverse=True)
    if not archives:
        return None
    
    with open(archives[0], 'r') as f:
        return json.load(f)


def generate_commit_message(session_data, changes):
    """Generate a meaningful commit message from session data"""
    if not session_data:
        return "Update: Session changes"
    
    files = session_data.get('files', [])
    if not files:
        return "Update: Minor changes"
    
    # Count actions
    writes = len([f for f in files if f.get('action') == 'write'])
    edits = len([f for f in files if f.get('action') == 'edit'])
    
    # Determine primary action
    if writes > edits:
        action = "feat" if writes > 2 else "add"
    elif edits > 0:
        action = "update"
    else:
        action = "chore"
    
    # Build message
    message_parts = []
    
    # Analyze file types
    hook_files = [f['file'] for f in files if '.claude/hooks' in f['file']]
    agent_files = [f['file'] for f in files if '.claude/agents' in f['file']]
    doc_files = [f['file'] for f in files if f['file'].endswith('.md')]
    
    if hook_files:
        message_parts.append("session tracking hooks")
    if agent_files:
        message_parts.append("agent definitions")
    if doc_files and not agent_files:  # Don't double-count agent .md files
        message_parts.append("documentation")
    
    if message_parts:
        summary = f"{action}: Update {', '.join(message_parts)}"
    else:
        summary = f"{action}: Session updates"
    
    # Add details
    details = []
    if writes > 0:
        details.append(f"- Added {writes} new file{'s' if writes != 1 else ''}")
    if edits > 0:
        details.append(f"- Modified {edits} file{'s' if edits != 1 else ''}")
    
    # Add session metadata
    session_duration = ""
    if 'session_start' in session_data and 'session_completed' in session_data:
        try:
            start = datetime.fromisoformat(session_data['session_start'])
            end = datetime.fromisoformat(session_data['session_completed'])
            duration = end - start
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            if hours > 0:
                session_duration = f" ({hours}h {minutes}m session)"
            else:
                session_duration = f" ({minutes}m session)"
        except:
            pass
    
    message = summary + session_duration
    if details:
        message += "\n\n" + "\n".join(details)
    
    return message


def post_cleanup():
    """Handle post-cleanup git operations"""
    print("\n" + "="*60)
    print("POST-CLEANUP GIT CHECK")
    print("="*60)
    
    # Check if we're in a git repo
    if not check_git_repo():
        print("ℹ️  Not a git repository - skipping commit")
        return 0
    
    # Check for changes
    changes = get_git_status()
    if not changes:
        print("✓ No changes to commit")
        return 0
    
    # Load session data for context
    session_data = load_session_data()
    
    # Count changes
    change_lines = changes.split('\n')
    modified_count = len([l for l in change_lines if l.startswith(' M')])
    added_count = len([l for l in change_lines if l.startswith('??')])
    
    print(f"\n📊 Git Status:")
    print(f"  • {modified_count} modified files")
    print(f"  • {added_count} untracked files")
    
    # Generate commit message
    commit_msg = generate_commit_message(session_data, changes)
    
    print("\n💡 Suggested commit message:")
    print("-"*40)
    print(commit_msg)
    print("-"*40)
    
    # Create a file with instructions for the Git Expert
    claude_dir = Path('.claude')
    git_request = claude_dir / 'git_commit_request.json'
    
    with open(git_request, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'changes': changes,
            'suggested_message': commit_msg,
            'session_data': session_data,
            'request': 'review_and_commit'
        }, f, indent=2)
    
    print("\n🤖 GIT EXPERT REQUEST")
    print("-"*60)
    print("Please use the git-expert agent to:")
    print("1. Review the changes made during this session")
    print("2. Refine the commit message if needed")
    print("3. Stage and commit the changes")
    print("4. Optionally push to remote repository")
    print("\nThe agent will help ensure everything is properly committed.")
    print("-"*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(post_cleanup())