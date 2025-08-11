# Known Limitations - Claude Orchestrator

## Context Guardian Token Tracking in Claude Code

### The Issue
Context Guardian currently cannot automatically track token usage in Claude Code sessions because:
- Claude Code's token counting is internal and not exposed to external tools
- Context Guardian works by manually processing text through `add_content()`
- No API or integration point exists between Claude Code and external Python scripts

### Impact
- `/token-usage` command shows 0 or stale data
- Cannot trigger automatic checkpoints based on token percentage
- Context overflow prevention doesn't work as designed

### Workarounds

#### 1. Time-Based Checkpoints
Instead of token-based triggers, use time intervals:
- Checkpoint every 30 minutes (configured in workflow)
- Manual checkpoints with `/create-checkpoint`

#### 2. Task-Based Checkpoints  
Create checkpoints when completing major tasks:
- After implementing a feature
- Before starting new major work
- When switching context

#### 3. Session Management Focus
Use the orchestrator for what works:
- Session state tracking in SQLite
- Decision and issue logging
- Checkpoint creation and recovery
- Session handover documents

### Future Solutions

Potential improvements to explore:
1. **Claude Code Plugin**: Create a native Claude Code extension
2. **Estimation Mode**: Estimate tokens based on file sizes and changes
3. **Manual Update Command**: Add `/update-tokens <estimate>` command
4. **Alternative Metrics**: Track session time, files modified, decisions made

### For Other Environments

Context Guardian works properly when:
- Using Python scripts that can call `add_content()`
- Integrating with APIs that provide token counts
- Building custom LLM interfaces

## Checkpoint System (Working Features)

Despite token tracking limitations, these features work:
- Manual checkpoint creation
- Time-based checkpoint suggestions
- SQLite session state persistence
- Checkpoint recovery on session start
- Session handover documentation

## Recommendation

For Claude Code development, focus on:
1. Regular manual checkpoints
2. Time-based reminders (30 min default)
3. Task completion checkpoints
4. Session handover documents

The orchestrator still provides value through session management, even without automatic token tracking.

## User Notes
The user has gathered some research under: /home/klaus/game-projects/Feature Analysis/FEATURE-tokentracker/
The user wants a propoper analysis if a valuable token counter can be achieved.
