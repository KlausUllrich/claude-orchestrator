# Tool Development Workflow

## Purpose
This workflow is specifically designed for developing the Claude Orchestrator itself, implementing dogfooding principles where the tool is used to build itself.

## Activation
```bash
cd claude-orchestrator
./setup.sh --project-type tool-development
# or manually:
ln -sf tool-development workflows/active
```

## Key Features

### User Approval Required
- All task completions need explicit user confirmation
- No automated commits or releases
- Implementation decisions require approval

### Checkpoint System
- **Timer**: Suggests checkpoint every 30 minutes
- **Major Steps**: Suggests checkpoint after big tasks
- **Context**: Suggests checkpoint at 70% token usage  
- **Session End**: Automatic checkpoint on clean shutdown
- All checkpoints are suggestions except session-end

### Session Management
- Reads `session-handover-next.md` on start
- Tracks decisions and issues in SQLite
- Creates handover document on end
- Recovers from last checkpoint if needed

## Commands
- `/token-usage` - Check current context usage
- `/create-checkpoint` - Manually create checkpoint
- `/list-checkpoints` - Show recent checkpoints
- `/session-status` - Current session info

## File Structure
```
workflows/tool-development/
├── rules.yaml     # Behavior rules
├── config.yaml    # Checkpoint and component config
└── README.md      # This file
```
