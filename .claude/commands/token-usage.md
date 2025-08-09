# /token-usage Command (Claude Code Version)

## Important Note
Context Guardian cannot directly track Claude Code's actual token usage.
This is a known limitation. The command provides alternative functionality.

## Trigger
When user types: `/token-usage`

## Action for Claude Code
Since we cannot access Claude Code's internal token tracking:
1. Show Context Guardian's manual tracking (if any)
2. Suggest using time-based checkpoints instead
3. Offer to create a checkpoint if needed

## Implementation
```bash
# Check Context Guardian status (manual tracking only)
python3 claude-orchestrator/tools/context_guardian.py --status
```

## Response Format
```
📊 Token Usage Status
━━━━━━━━━━━━━━━━━━━━
⚠️ Note: Claude Code's actual tokens not accessible
Manual tracking: [X] tokens (if manually added)

💡 Alternatives:
- Use time-based checkpoints (every 30 min)
- Create manual checkpoints with /create-checkpoint
- Track session progress in SQLite

Would you like to create a checkpoint now? (y/n)
```

## Known Limitations
- Cannot access Claude Code's real token count
- Context Guardian only tracks manually added content
- Best used with other LLM interfaces that can feed content

## Workaround
For Claude Code sessions, rely on:
- Time-based checkpoints
- Task-based checkpoints  
- Manual checkpoint creation
