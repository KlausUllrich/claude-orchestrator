# Claude Context Sharing Discovery

## The Key Finding: Session Resume Works!

We can share context between Claude instances using the `-r` (resume) flag!

## How It Works

### 1. Create Initial Context
```bash
# First Claude creates context and gets session ID
claude -p "Remember the number 42" --output-format json
# Returns: {"session_id":"a3bed98d-abde-48ae-ad3c-b26238ccd4d8", ...}
```

### 2. Resume Session with Context
```bash
# Another Claude can access that context!
claude -r a3bed98d-abde-48ae-ad3c-b26238ccd4d8 -p "What number did I ask you to remember?"
# Output: 42
```

## Available Context Sharing Methods

### Method 1: JSON Output Format
```bash
# Get session ID from any Claude command
SESSION_ID=$(claude -p "task" --output-format json | jq -r '.session_id')
```

### Method 2: Resume Flag
```bash
# Resume specific session
claude -r $SESSION_ID -p "continue task"

# Resume most recent session
claude -c -p "continue last task"
```

### Method 3: Session ID Assignment
```bash
# Create new session with specific ID
MY_UUID=$(uuidgen)
claude --session-id $MY_UUID -p "start task"

# BUT: Cannot reuse active session ID (gets "already in use" error)
```

## What This Enables

### 1. Context Handoff Between Agents
```bash
# Agent 1 builds context
SESSION=$(claude -p "Analyze this codebase..." --output-format json | jq -r '.session_id')

# Agent 2 continues with that context
claude -r $SESSION -p "Based on the analysis, implement..."
```

### 2. Parallel Agents with Shared Knowledge
```bash
# Main Claude creates shared context
SESSION=$(claude -p "Here's our project plan..." --output-format json | jq -r '.session_id')

# Multiple agents can resume from this point
claude -r $SESSION -p "Implement feature A" > agent1.txt &
claude -r $SESSION -p "Implement feature B" > agent2.txt &
claude -r $SESSION -p "Write tests" > agent3.txt &
```

### 3. Checkpoint and Recovery
```bash
# Save session ID for later
echo $SESSION_ID > checkpoint.txt

# Later, resume from checkpoint
claude -r $(cat checkpoint.txt) -p "Continue where we left off"
```

## JSON Output Format Details

The `--output-format json` provides rich metadata:

```json
{
    "type": "result",
    "subtype": "success",
    "is_error": false,
    "duration_ms": 2447,
    "duration_api_ms": 3239,
    "num_turns": 1,
    "result": "The actual response text",
    "session_id": "96be2b96-b4fe-4f8c-a90b-e427b843e87f",
    "total_cost_usd": 0.097016,
    "usage": {
        "input_tokens": 4,
        "cache_creation_input_tokens": 4228,
        "cache_read_input_tokens": 11298,
        "output_tokens": 6
    }
}
```

## Limitations

1. **Cannot reuse active session**: Get "already in use" error
2. **Session persistence unknown**: How long do sessions stay available?
3. **Context size limits**: Inherited from original session
4. **No context export**: Cannot dump full context to file

## Guardian Architecture Implications

This changes everything for the Guardian pattern:

```python
class GuardianWithContext:
    def __init__(self):
        # Create master context session
        result = claude("-p", "Master context setup", "--output-format", "json")
        self.master_session = json.loads(result)["session_id"]
    
    def launch_agent_with_context(self, task):
        # Each agent resumes from master context
        cmd = f'claude -r {self.master_session} -p "{task}" > output.txt'
        return Bash(cmd, run_in_background=True)
```

## Testing Context Persistence

```bash
# Test 1: Create context
SESSION=$(claude -p "X=100" --output-format json | jq -r '.session_id')

# Test 2: Multiple resumes
claude -r $SESSION -p "What is X?"  # Should output 100
claude -r $SESSION -p "X+50?"       # Should output 150

# Test 3: Parallel access
claude -r $SESSION -p "X*2?" > test1.txt &
claude -r $SESSION -p "X/2?" > test2.txt &
```

## Best Practices

1. **Store session IDs** for important contexts
2. **Use JSON output** to capture metadata
3. **Test session availability** before launching parallel agents
4. **Consider context size** when building shared knowledge
5. **Handle "already in use"** errors gracefully

## The Power of This Discovery

We can now:
- ✅ Share complex context between agents
- ✅ Build knowledge incrementally
- ✅ Create specialized agent teams with shared memory
- ✅ Implement checkpoint/recovery systems
- ✅ Pass work between agents seamlessly

This is a game-changer for multi-agent orchestration!