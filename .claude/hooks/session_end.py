#!/usr/bin/env python3
"""
session_end.py - Session end hook that triggers cleanup analysis
Location: .claude/hooks/session_end.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime


def session_end():
    """Handle session end - prepare for cleanup"""
    claude_dir = Path('.claude')
    session_file = claude_dir / 'session_files.json'
    
    # Check if we have tracked files
    if not session_file.exists():
        # Silent exit - no session file means fresh start or already cleaned
        return 0
    
    try:
        with open(session_file, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        # Silent exit on read errors
        return 0
    
    files = data.get('files', [])
    
    if not files:
        # Silent exit - empty session means already cleaned or fresh start
        return 0
    
    # Generate summary
    print("\n" + "="*60)
    print("SESSION END - FILE SUMMARY")
    print("="*60)
    print(f"Session started: {data.get('session_start', 'Unknown')}")
    print(f"Files modified: {len(files)}")
    
    # Group files by action
    writes = [f for f in files if f.get('action') == 'write']
    edits = [f for f in files if f.get('action') == 'edit']
    
    if writes:
        print(f"\nFiles created ({len(writes)}):")
        for f in writes[:5]:
            print(f"  • {f['file']}")
        if len(writes) > 5:
            print(f"  ... and {len(writes) - 5} more")
    
    if edits:
        print(f"\nFiles edited ({len(edits)}):")
        for f in edits[:5]:
            print(f"  • {f['file']}")
        if len(edits) > 5:
            print(f"  ... and {len(edits) - 5} more")
    
    print("\n" + "-"*60)
    
    # Create a marker file with session details for the cleanup agent
    marker_file = claude_dir / 'pending_cleanup.json'
    with open(marker_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'files_count': len(files),
            'session_file': str(session_file),
            'files': files
        }, f, indent=2)
    
    # Request Claude to run the session-cleanup agent
    print("\n🤖 CLEANUP AGENT REQUEST")
    print("-"*60)
    print("Please use the session-cleanup agent to analyze and organize the files created during this session.")
    print(f"Files to review: {len(files)}")
    print("\nThe agent should:")
    print("1. Analyze all files created/modified during the session")
    print("2. Identify temporary or test files that can be removed")
    print("3. Suggest documentation improvements if needed")
    print("4. Ensure proper code organization")
    print("\nAfter cleanup is complete, run:")
    print("  python .claude/hooks/cleanup_complete.py")
    print("This will archive the session and reset tracking files.")
    print("-"*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(session_end())