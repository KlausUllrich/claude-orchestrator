#\!/usr/bin/env python3
import json
import sys

# Explicitly allow the operation with JSON output
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow"
    }
}))
sys.exit(0)
