# Claude Orchestrator Commands

## Available Commands

### Session Management
- `/token-usage` - Check current context token usage
- `/create-checkpoint` - Manually create a session checkpoint
- `/list-checkpoints` - Show recent checkpoints (TODO)
- `/session-status` - Display current session information (TODO)

### Development Workflow  
- `/todo-status` - Show current TODO items from todo.md (TODO)
- `/mark-complete` - Mark a task as complete (with approval) (TODO)

## Usage
Type any command to trigger the corresponding action. Commands are designed to help manage the orchestrator session and prevent context overflow.

## Implementation Notes
Each command has its own documentation file in this directory with:
- Trigger conditions
- Implementation details  
- Response format
- Example usage

## Adding New Commands
1. Create a new .md file in this directory
2. Follow the format of existing commands
3. Document trigger, action, and response
4. Update this README with the new command
