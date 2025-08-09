# /create-checkpoint Command

## Trigger
When user types: `/create-checkpoint`

## Action
Manually create a checkpoint with current session state.

## Process
1. Gather current state:
   - Current task being worked on
   - Completed items (with user approval)
   - Pending decisions awaiting user input
   - Active issues encountered
   - Next steps to take
   - Current token usage percentage

2. Create checkpoint in SQLite using SessionManager

3. Show summary to user

## Implementation
```python
from claude-orchestrator.short-term-memory.session_db import SessionManager

# Create checkpoint
manager = SessionManager()
checkpoint_num = manager.create_checkpoint(
    trigger_type="manual",
    current_task="[current work]",
    completed_items=["item1", "item2"],
    pending_decisions=["decision1"],
    active_issues=["issue1"],
    next_steps="[what's next]",
    context_percent=[current_percentage]
)
```

## Response Format
```
✅ Checkpoint #[X] Created Successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Current Task: [task description]
✓ Completed: 
  - [item 1]
  - [item 2]
⏳ Pending Decisions:
  - [decision 1]
⚠️ Active Issues:
  - [issue 1]
➡️ Next Steps: [what to do next]
📊 Context Usage: [X]%
```

## Example Usage
User: /create-checkpoint
Assistant: Let me create a checkpoint with the current session state...
[Shows checkpoint summary]
