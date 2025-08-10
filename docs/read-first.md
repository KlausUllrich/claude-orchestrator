# Required Reading List - Claude Orchestrator

## 📚 MANDATORY DOCUMENTS

These documents MUST be read at the start of every session to understand the system:

### Core Understanding (Read in Order)
1. **`docs/status/handover-next.md`** - Previous session's handover
2. **`docs/status/users-todos.md`** - Master TODO list with priorities the user wants to achieve
3. **`QUICK-REFERENCE.md`** - How the orchestrator works (simple version)
4. **`docs/design/vision.md`** - Project goals and approach
5. **`docs/technical/architecture.md`** - How components fit together
6. **`claude-orchestrator/brain/rules/README.md`** - Rules system operation
7. **`docs/technical/known-limitations.md`** - What doesn't work and workarounds
8. **`CLAUDE.md`** - Core interaction rules for Claude

## 📋 Key Understanding Checklist

Before starting work, confirm understanding of:
- [ ] How commands flow: User → Claude → orchestrate.py → Python scripts
- [ ] Where handovers are stored: `docs/status/`
- [ ] Where databases live: `claude-orchestrator/short-term-memory/`
- [ ] What components work vs what's TODO
- [ ] No background process/daemon needed - commands execute directly
- [ ] Resource-library = templates, .claude/ = active components

## ⚠️ Critical Reminders

- **DO NOT** create new documentation unless explicitly requested
- **ALWAYS** check what exists before creating new files
- **ALWAYS** prefer editing existing files over creating new ones
- **TEST** simple implementations before adding complexity

**Key Understanding Points:**
- ❗ Orchestrator works through Claude commands, NOT a separate terminal
- ❗ Each project has its own complete orchestrator copy

## 📖 Additional Context-Specific Reading

The handover document may specify additional documents to read based on the specific work planned for the session. These will be listed in the handover under "Session-Specific Reading".

---
*This list ensures consistent understanding across all sessions. Update only when core documents change.*
