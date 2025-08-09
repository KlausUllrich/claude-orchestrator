#!/usr/bin/env python3
"""
track_file.py - Track files created/edited during session
Location: .claude/hooks/track_file.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime


def track_file(action_type):
    """Track file operations during session"""
    claude_dir = Path('.claude')
    claude_dir.mkdir(exist_ok=True)
    
    session_file = claude_dir / 'session_files.json'
    debug_file = claude_dir / 'hooks_debug.log'
    
    # Load or create session data
    if session_file.exists():
        with open(session_file, 'r') as f:
            data = json.load(f)
    else:
        data = {
            'session_start': datetime.now().isoformat(),
            'files': []
        }
    
    file_path = None
    
    # Try multiple methods to get file info
    # Method 1: Environment variable CLAUDE_TOOL_INPUT (rarely used)
    tool_input = os.environ.get('CLAUDE_TOOL_INPUT', '')
    if tool_input:
        try:
            tool_data = json.loads(tool_input)
            file_path = tool_data.get('file_path')
        except json.JSONDecodeError:
            pass
    
    # Method 2: Try stdin - Claude Code passes JSON with tool_name and tool_input
    if not file_path and not sys.stdin.isatty():
        try:
            stdin_data = sys.stdin.read()
            if stdin_data:
                data_obj = json.loads(stdin_data)
                # Extract file_path from tool_input
                tool_input_data = data_obj.get('tool_input', {})
                file_path = tool_input_data.get('file_path')
        except Exception as e:
            # Log errors only if needed for debugging
            pass
    
    if file_path:
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action_type,
            'file': file_path
        }
        
        # Avoid duplicates for same file
        existing_files = [e['file'] for e in data['files']]
        if file_path not in existing_files:
            data['files'].append(entry)
        else:
            # Update timestamp for existing file
            for e in data['files']:
                if e['file'] == file_path:
                    e['timestamp'] = entry['timestamp']
                    e['action'] = action_type
    
    # Save updated data
    with open(session_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Silent success
    return 0


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else 'unknown'
    sys.exit(track_file(action))