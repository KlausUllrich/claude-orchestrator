# /session-start Command

## Trigger
When user types: `/session-start`

## Action
Start a new session by reading the previous handover document.

## Implementation
Execute the orchestrator's session start command:
```bash
cd claude-orchestrator && python orchestrate.py session start
```

## Process
1. Reads `docs/status/handover-next.md` if it exists
2. Displays key sections:
   - Required reading list
   - Session summary from last time
   - Next session goals
   - Any warnings or issues
3. Reminds to read required documents
4. Sets context for continuing work

## Output Format
```
🚀 Starting new session...
✅ Handover loaded from: docs/status/handover-next.md

============================================================
📋 Previous Session Handover:
============================================================
[Shows handover content with focus on:
 - Required reading
 - Previous work summary  
 - Goals for this session]

============================================================
✅ Session started. Review the full handover at: docs/status/handover-next.md
📚 Don't forget to read the required documents listed in the handover!
```

## If No Handover Found
```
ℹ️ No previous handover found. Starting fresh session.
📚 Please read docs/read-first.md for required documentation.
```

## Related Commands
- `/handover` - Create handover at end of session