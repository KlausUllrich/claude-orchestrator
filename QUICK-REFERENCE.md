# QUICK REFERENCE - Claude Orchestrator

## How It Works (Simple Version)

```
User types command → Claude executes Python → Updates files/DB → Shows result
```

**NO separate terminal, NO background process, NO monitoring daemon**

## Key Directories

| What | Where | Purpose |
|------|-------|---------|
| Commands | `.claude/commands/` | Define what happens when user types /command |
| Logic | `claude-orchestrator/brain/` | Python scripts that do the work |
| Session Data | `claude-orchestrator/short-term-memory/` | SQLite databases |
| Handovers | `docs/status/` | Session continuity documents |
| Templates | `claude-orchestrator/resource-library/` | Copy from here |
| Active Hooks | `.claude/hooks/` | Actually run (symlinks) |

## Command Flow Example

```
/handover
    ↓
.claude/commands/handover.md says "execute orchestrate.py handover"
    ↓
claude-orchestrator/orchestrate.py handover
    ↓
brain/handover-manager.py create_handover()
    ↓
Creates docs/status/handover-TIMESTAMP.md
```

## What Already Exists

✅ **Working:**
- SQLite database and schema
- Rule enforcer with YAML rules
- All workflows (unity, love2d, web-dev, tool-development)
- Agents in .claude/agents/

⚠️ **Exists but doesn't work:**
- Token tracking (can't access Claude's tokens)
- Commands (just documentation, not executable)

❌ **TODO:**
- Make commands actually execute
- Task tracking
- Long-term memory
- External integrations

## Common Confusions

| Wrong Understanding | Right Understanding |
|---------------------|---------------------|
| Orchestrator runs in separate terminal | Runs through Claude commands |
| resource-library has active components | resource-library has templates to copy |
| Token tracking works | Known limitation in Claude Code |
| Need to build everything | Much already exists |

## Before Starting Any Session

1. Read `handover-next.md` completely
2. Read `architecture.md` to understand structure
3. Check what exists with `ls` before creating
4. Test simple things before complex
5. Get user approval for decisions
