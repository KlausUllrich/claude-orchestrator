#!/usr/bin/env python3
"""
Utility functions for the Claude Orchestrator
"""

import os
from pathlib import Path
from typing import Optional

def find_project_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Find the project root by looking for .gitignore or other project markers.
    
    This function searches upward from the start path to find the project root,
    which is identified by the presence of certain marker files.
    
    Args:
        start_path: Starting directory to search from (defaults to current working directory)
    
    Returns:
        Path to project root if found, None otherwise
    """
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path).resolve()
    
    # Marker files that indicate project root
    markers = [
        '.gitignore',
        '.git',
        'claude-orchestrator',  # Our tool folder
        'CLAUDE.md'  # Project-specific Claude rules
    ]
    
    current = start_path
    
    # Search upward for project root
    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                # Verify this is the right project by checking for claude-orchestrator
                if (current / 'claude-orchestrator').exists():
                    return current
                # If we found .git or .gitignore but no orchestrator, keep looking
                elif marker in ['.gitignore', '.git']:
                    # This might be the project root even without orchestrator
                    return current
        current = current.parent
    
    # If we couldn't find it by searching up, try some common locations
    # This helps when running from inside nested directories
    common_paths = [
        Path.home() / 'game-projects' / 'claude-orchestrate',
        Path('/home/klaus/game-projects/claude-orchestrate'),
    ]
    
    for path in common_paths:
        if path.exists() and (path / 'claude-orchestrator').exists():
            return path
    
    return None


def find_orchestrate_py() -> Optional[Path]:
    """
    Find the orchestrate.py file reliably from anywhere.
    
    Returns:
        Path to orchestrate.py if found, None otherwise
    """
    # First try to find project root
    project_root = find_project_root()
    
    if project_root:
        orchestrate_path = project_root / 'claude-orchestrator' / 'orchestrate.py'
        if orchestrate_path.exists():
            return orchestrate_path
    
    # If that didn't work, try relative to this file
    this_file = Path(__file__).resolve()
    orchestrator_root = this_file.parent.parent
    orchestrate_path = orchestrator_root / 'orchestrate.py'
    
    if orchestrate_path.exists():
        return orchestrate_path
    
    return None


def get_relative_path_command() -> str:
    """
    Get the command to run orchestrate.py using relative paths.
    
    This ensures commands work regardless of the current working directory.
    
    Returns:
        Command string to run orchestrate.py
    """
    orchestrate_path = find_orchestrate_py()
    
    if not orchestrate_path:
        # Fallback to assuming we're in the right place
        return "python orchestrate.py"
    
    # Get relative path from current directory
    try:
        rel_path = orchestrate_path.relative_to(Path.cwd())
        return f"python {rel_path}"
    except ValueError:
        # Can't make relative path, use absolute
        return f"python {orchestrate_path}"


def ensure_in_orchestrator_dir() -> Path:
    """
    Ensure we're in the claude-orchestrator directory and return the path.
    
    Returns:
        Path to claude-orchestrator directory
    
    Raises:
        RuntimeError: If claude-orchestrator directory cannot be found
    """
    orchestrate_path = find_orchestrate_py()
    
    if not orchestrate_path:
        raise RuntimeError(
            "Cannot find claude-orchestrator directory. "
            "Please ensure you're in a project with claude-orchestrator installed."
        )
    
    orchestrator_dir = orchestrate_path.parent
    
    # Change to orchestrator directory if not already there
    if Path.cwd() != orchestrator_dir:
        os.chdir(orchestrator_dir)
    
    return orchestrator_dir


# Example usage in other modules:
# from brain.utils import find_project_root, get_relative_path_command
# 
# project_root = find_project_root()
# command = get_relative_path_command()
# print(f"Run: {command} handover --summary info")