#!/usr/bin/env python3
"""
cleanup_complete.py - Archive and reset session tracking after cleanup
Location: .claude/hooks/cleanup_complete.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import shutil


def archive_session():
    """Archive completed session data and reset for next session"""
    claude_dir = Path('.claude')
    
    # Files to manage
    session_file = claude_dir / 'session_files.json'
    pending_file = claude_dir / 'pending_cleanup.json'
    debug_log = claude_dir / 'hooks_debug.log'
    
    # Create archive directory if needed
    archive_dir = claude_dir / 'archive'
    archive_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for archive
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Archive session files if they exist
    archived_any = False
    
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
            
            # Only archive if there was actual content
            if data.get('files'):
                archive_name = archive_dir / f'session_{timestamp}.json'
                
                # Add completion metadata
                data['session_completed'] = datetime.now().isoformat()
                data['cleanup_performed'] = True
                
                # Save to archive
                with open(archive_name, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"✓ Session archived to: {archive_name}")
                archived_any = True
            
            # Reset session file for next session
            reset_data = {
                'session_start': datetime.now().isoformat(),
                'files': []
            }
            with open(session_file, 'w') as f:
                json.dump(reset_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not archive session file: {e}", file=sys.stderr)
    
    # Clean up pending cleanup file
    if pending_file.exists():
        try:
            os.remove(pending_file)
            print("✓ Cleared pending cleanup marker")
        except Exception as e:
            print(f"Warning: Could not remove pending cleanup: {e}", file=sys.stderr)
    
    # Optionally rotate debug log if it's getting large
    if debug_log.exists():
        try:
            log_size = debug_log.stat().st_size
            # If log is over 1MB, rotate it
            if log_size > 1024 * 1024:
                archive_log = archive_dir / f'debug_log_{timestamp}.log'
                shutil.move(str(debug_log), str(archive_log))
                print(f"✓ Rotated debug log (was {log_size/1024:.1f}KB)")
        except Exception as e:
            print(f"Warning: Could not rotate debug log: {e}", file=sys.stderr)
    
    # Clean up old archives (keep only last 10)
    try:
        archives = sorted(archive_dir.glob('session_*.json'))
        if len(archives) > 10:
            for old_archive in archives[:-10]:
                old_archive.unlink()
                print(f"✓ Removed old archive: {old_archive.name}")
    except Exception as e:
        print(f"Warning: Could not clean old archives: {e}", file=sys.stderr)
    
    if archived_any:
        print("\n📦 Session cleanup complete - tracking reset for next session")
    else:
        print("\n✓ Cleanup complete - no session data to archive")
    
    # Trigger post-cleanup git check
    try:
        from post_cleanup import post_cleanup
        post_cleanup()
    except Exception as e:
        # Silent fail if post_cleanup not available or errors
        pass
    
    return 0


if __name__ == "__main__":
    sys.exit(archive_session())