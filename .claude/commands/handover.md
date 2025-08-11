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
   cd claude-orchestrator && python orchestrate.py handover --summary info
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

### Phase 3: Validation Check (BEFORE User Review)

**CRITICAL: Validate BEFORE showing to user to ensure quality!**

1. **Quick Structure Validation**
   ```bash
   # First, run quick validation check
   echo "$HANDOVER_DRAFT" | python orchestrate.py handover --summary validate
   ```
   - If validation fails, fix errors and re-validate
   - Only proceed when structure validation passes

2. **Full Validation Task (Optional for Complex Sessions)**
   - For important sessions, also run the full validation task:
   - Launch sub-agent with handover_validation_check task:
   ```
   Task Description: "Sub-Agent: Validate handover completeness"
   Prompt: "Act as maintenance-agent. Read the agent template and execute the 
           handover_validation_check task. Validate the handover draft for:
           - All required sections present and complete
           - No template placeholders remaining
           - Content accuracy and completeness
           - Proper context preservation"
   ```

3. **Fix Any Issues Found**
   - If validation fails, fix identified problems
   - Re-run validation until passes
   - Only proceed to user review when ALL validations pass

4. **Validation Checklist Summary**
   ✅ Structure validation passed (via orchestrate.py)
   ✅ All 12 required sections present
   ✅ No template placeholders remain
   ✅ Minimum content length met (500+ chars)
   ✅ YAML frontmatter present
   ✅ Working directory specified
   ✅ Mandatory reads section complete

### Phase 4: User Review (After Validation Passes)

1. **Present Validated Handover**
   - **CRITICAL**: Show the FULL validated handover at once - NOT step-by-step edits
   - Start with: "I've created and validated the session handover. Here it is for your review:"
   - Present the entire document
   - After showing, highlight: "Key points for next session: [brief summary]"
   - **NEVER** interrupt workflow if user comments - incorporate feedback and continue

2. **Get Feedback**
   - Ask: "Does this handover capture everything important from our session?"
   - User can approve as-is
   - Request specific adjustments
   - Add additional context

3. **Incorporate Changes**
   - Update handover based on feedback
   - If structural changes made, re-run validation
   - Get final approval before saving

### Phase 5: Save and Archive (After User Approval)

**CRITICAL: Ensure content is properly piped to prevent data loss!**

```bash
# Save the approved handover (content MUST be piped in)
cat handover_content | python orchestrate.py handover --summary save

# Or use echo for direct content:
echo "$HANDOVER_CONTENT" | python orchestrate.py handover --summary save

# NEVER run without content:
# python orchestrate.py handover --summary save  # ❌ THIS WILL SAVE EMPTY FILE!
```

**Post-Save Verification:**
- System will automatically check file was saved with content
- Will warn if file is empty or too small
- Will attempt recovery from archive if main save failed
- Will report final status with file size

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