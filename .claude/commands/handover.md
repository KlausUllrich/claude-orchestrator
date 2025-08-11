# /handover Command

## Trigger
When user types: `/handover`

## Philosophy
The LLM (Claude) creates a comprehensive handover document using all available context and memory systems.
The handover follows the template at `claude-orchestrator/resource-library/documents/handovers/Session_Handover_Template.md`

## LLM Process for Creating Handover

### Phase 1: Information Gathering

1. **Session Context Analysis**
   - Review entire conversation history
   - Identify what was attempted, completed, and failed
   - Extract key decisions and their rationale
   - Note any blockers or issues encountered

2. **System State Check**
   ```bash
   cd claude-orchestrator && python orchestrate.py handover info
   ```
   - Git status and uncommitted changes
   - Modified files and their state
   - Database warnings

3. **Memory Systems Check**
   - Short-term memory: Current session state
   - Long-term memory: Patterns, decisions, lessons learned
   - TODO list: Current priorities and progress

4. **Expectation vs Reality**
   - Compare session goals (from previous handover) with actual outcomes
   - Identify gaps and reasons for divergence
   - Note unexpected discoveries or complications

### Phase 2: Handover Creation

Following the template structure:

1. **Header with Metadata**
   - Project name
   - **CRITICAL**: Title format: `Session Handover: [descriptive session summary] YYYY-MM-DD HH:MM`
     - Example: `Session Handover: Fixed Session-End Workflow 2025-01-11 08:45`
     - Example: `Session Handover: Implemented Agent Architecture 2025-01-11 14:30`
   - Summary bullets (4 key points)
   - Relevant tags

2. **Mandatory Reads Section**
   - Always include `/docs/status/read-first.md`
   - Link to previous handover
   - Task-specific documents with WHY they're needed

3. **Development State**
   - Current phase and sub-phase
   - Overall progress assessment
   - What was completed (with verification status)
   - What wasn't completed and WHY

4. **Session Goal**
   - ONE clear, achievable objective
   - Specific success criteria
   - Time-boxing guidance

5. **Critical Warnings**
   - Architecture warnings from lessons learned
   - Active blockers with workarounds
   - Known issues that affect next session

6. **Task Breakdown**
   - Specific tasks with prerequisites
   - Step-by-step actions with expected outcomes
   - Potential issues and solutions

7. **References**
   - Relevant code locations (file:line format)
   - Patterns to follow/avoid
   - Test files and how to run them

8. **Context & Decisions**
   - Technical decisions that affect future work
   - Architectural considerations
   - Quick reference commands

9. **Session End Checklist**
   - What needs to be done before ending
   - Commit reminders and guidelines

### Phase 3: Validation Check

1. **Run Validation Task**
   - Use maintenance-agent with handover_validation_check task
   - Verify all sections present
   - Check for placeholders
   - Ensure completeness

2. **Fix Any Issues**
   - If validation fails, fix identified problems
   - Re-run validation until passes
   - Only proceed when structure is correct

### Phase 4: User Review

1. **Present Complete Handover**
   - **CRITICAL**: Show the FULL handover document at once - NOT step-by-step edits
   - Present the entire validated document to user
   - Highlight key sections after showing full document
   - Explain reasoning for priorities
   - **NEVER** interrupt workflow if user comments - incorporate feedback and continue

2. **Get Feedback**
   - User can approve as-is
   - Request specific adjustments
   - Add additional context

3. **Incorporate Changes**
   - Update handover based on feedback
   - Ensure all user concerns are addressed
   - Re-validate if structural changes made

### Phase 5: Save and Archive

```bash
# Save the approved handover
echo "[handover content]" | python orchestrate.py handover save
```

## Key Principles

1. **Comprehensive, Not Minimal**
   - Rich narrative, not bullet points
   - Context and reasoning, not just facts
   - Story of the session, not a checklist

2. **Future-Focused**
   - What the next session needs to know
   - Warnings to prevent repeated mistakes
   - Clear path forward

3. **Transparent Process**
   - User sees all analysis
   - User approves all content
   - User maintains control

## Information Sources

The LLM should gather from:
- Current conversation context
- Previous handover (`docs/status/handover-next.md`)
- TODO list (`docs/status/todo.md`)
- Project documentation
- Git status and changes
- Database state
- Test results
- Error logs
- User feedback during session

## Quality Checklist

### Pre-Save Validation
Must pass before saving:
- [ ] Filename is exactly `handover-next.md`
- [ ] All 12 required sections present
- [ ] No template placeholders remain
- [ ] Critical LLM context filled
- [ ] Previous handover archived
- [ ] Validation task passes

### Content Quality
A good handover:
- [ ] Tells the complete story of the session
- [ ] Explains WHY things happened, not just what
- [ ] Provides clear next steps
- [ ] Includes all necessary warnings
- [ ] Links to relevant documents
- [ ] Is readable by someone unfamiliar with the session
- [ ] Follows the template structure
- [ ] Preserves all TODOs from session
- [ ] Has user approval