# Claude Agent Monitoring Capabilities

## What We Can Monitor

### 1. Process Status ✅
- **BashOutput tool**: Shows if process is `running` or `completed`
- **Exit code**: Available when completed
- **Process listing**: `ps aux | grep claude` shows running instances

### 2. File-Based Output 📄
- **Output appears all at once**: Claude writes the complete response when done
- **NOT incremental**: Cannot see partial output while Claude is "thinking"
- **File size changes**: Can detect when output is written (0 bytes → full size)
- **System notifications**: Get alerts when files are modified

### 3. What We CANNOT See ❌
- **Incremental output**: Claude doesn't stream output line by line
- **Current thinking**: No visibility into what Claude is processing
- **Progress percentage**: No built-in progress indicators
- **Intermediate results**: Output only appears when complete

## Monitoring Patterns

### Basic Status Check
```bash
# Check if still running
BashOutput(bash_id="bash_15")
# Returns: status=running or status=completed

# Check process
ps aux | grep "claude -p"

# Check output file
ls -la output.txt  # Size is 0 while running, >0 when done
```

### Completion Detection
1. **System notifications**: Automatic alerts when background bash completes
2. **File modification alerts**: System notifies when output file changes
3. **BashOutput status**: Changes from "running" to "completed"

### Workaround for Progress Monitoring

Since Claude doesn't provide incremental output, we need creative solutions:

#### Option 1: Status File Pattern
Have Claude agents write periodic status updates:
```bash
claude -p "Task: Do X. Also, use Write tool to update status.json every few steps"
```

#### Option 2: Wrapper Script
Create a wrapper that adds heartbeat:
```bash
#!/bin/bash
echo "Starting at $(date)" > status.txt
claude -p "$1" > output.txt 2>&1
echo "Completed at $(date)" >> status.txt
```

#### Option 3: Process Monitoring
Monitor system resources:
```bash
# Check if Claude process is consuming CPU
top -b -n 1 | grep claude
```

## Key Findings

### Output Behavior
- **Buffered writing**: Claude writes entire response at once
- **No streaming**: Cannot tail -f the output file effectively
- **Atomic completion**: File goes from empty to complete instantly

### Status Indicators
| Method | Information Available | Real-time? |
|--------|---------------------|------------|
| BashOutput | Running/Completed | Yes |
| File size | 0 = running, >0 = done | Yes |
| Process list | PID and command | Yes |
| File content | Full output | Only when complete |
| System notifications | Completion alerts | Yes |

## Best Practices

1. **Use descriptive output filenames** to track which agent is which
2. **Check BashOutput** for reliable status
3. **Monitor file sizes** as completion indicator
4. **Set up status files** if you need progress updates
5. **Use timeouts** for long-running tasks

## Example: Multi-Agent Monitoring

```python
# Launch agents
agents = []
for i, task in enumerate(tasks):
    cmd = f'claude -p "{task}" > agent_{i}.txt 2>&1'
    bash_id = Bash(cmd, run_in_background=True)
    agents.append({"id": bash_id, "task": task, "output": f"agent_{i}.txt"})

# Monitor loop
while agents:
    for agent in agents[:]:
        status = BashOutput(agent["id"])
        if status["status"] == "completed":
            # Read and process output
            output = Read(agent["output"])
            print(f"Agent completed: {output}")
            agents.remove(agent)
    
    # Brief pause
    time.sleep(1)
```

## Limitations Summary

✅ **What works well**:
- Knowing when agents complete
- Reading final results
- Running multiple agents in parallel

❌ **What doesn't work**:
- Seeing incremental progress
- Watching Claude "think"
- Getting partial results

## Conclusion

While we can't see inside Claude's thinking process, we have sufficient monitoring to:
1. Know when agents are done
2. Retrieve complete results
3. Manage multiple parallel agents
4. Detect failures (via exit codes)

The key insight: **Treat Claude agents as black boxes that eventually produce output**, not as observable processes with incremental updates.