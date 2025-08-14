---
project: [project name]
title: Session Handover YYYY-MM-DD [timestamp]
summary:
  - bullet point 1
  - bullet point 2
  - bullet point 3
  - bullet point 4
tags: [project name], handover, session, workflow]
---

<!-- HANDOVER PRE-SAVE CHECKLIST
Before saving this handover, verify:
[ ] Filename is exactly: handover-next.md
[ ] Location is: /docs/status/
[ ] Previous handover archived to: /docs/status/archive/
[ ] Timestamp reflects actual session end time
[ ] All [placeholders] have been replaced with actual content
[ ] All 12 required sections are present
[ ] TODOs from session are preserved
[ ] Critical LLM context section is filled
[ ] Run handover validation task before saving
-->

# Session Handover - [Brief Session Focus]

## 🔴 MANDATORY READS (EVERY SESSION)
<!-- DO NOT REMOVE - REQUIRED SECTION -->

**Read these documents in order - read ALL in FULL - NO EXCEPTIONS:**

### 1. Core Project Rules 
- [ ] `/docs/status/read-first.md` - must be read in full!

### 2. Current Task Context
- [ ] This entire handover document
- [ ] Previous session handover summary: `[link to previous]`

### 3. Task-Specific Required Reading
[List ONLY documents essential for THIS session's specific task]
- [ ] `[Document Path]` - **Why Required**: [Specific reason]
- [ ] `[Document Path]` - **Why Required**: [Specific reason]

### 4. Useful References
[read on demand]
- [ ] `/docs/documentation-index.md` - List all relevant documents with a summary

**💡 Better to spend tokens on proper onboarding than waste sessions debugging**

---

## Orchestrator Understanding
<!-- DO NOT REMOVE - REQUIRED SECTION -->
**Check Understanding:**
Before starting, confirm you understand:
- [ ] How commands flow: User → Claude → Commands → orchestrate.py → Python scripts
- [ ] Where documents are stored 
- [ ] Where databases live: `claude-orchestrator/short-term-memory/`
- [ ] What works vs what's TODO


## 📍 Current Development State
<!-- DO NOT REMOVE - REQUIRED SECTION -->

### Project Status
**Phase**: [e.g., "Phase 3 - New Widgets"]
**Sub-Phase**: [e.g., "TextInput Widget Implementation"]
**Overall Progress**: [e.g., "ScrollArea complete, 4 widgets remaining"]

### Last Session Summary
**Completed**:
- [Bullet point of what was actually finished]
- [Include verification status]

**Not Completed**:
- [What was attempted but not finished]
- [Why it wasn't completed]
- [New problems found]
- [Impact on current work]


## 🎯 This Session Goal
<!-- DO NOT REMOVE - REQUIRED SECTION -->

### Primary Objective
[One clear, specific goal that can be completed in this session]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] User verification obtained

### Time Boxing
- If primary objective not achieved in [X] attempts → STOP and investigate architecture
- do not use time as a reason not to finish a task

## ⚠️ Critical Warnings & Known Issues
<!-- DO NOT REMOVE - REQUIRED SECTION -->

### Architecture Warnings
[Based on lessons learned, bug patterns or long-term memory]

### Active Blockers
1. **[Blocker]**: [Description] → [Workaround if any]
2. **[Blocker]**: [Description] → [Impact on session]

## 📋 Session Task Breakdown
<!-- DO NOT REMOVE - REQUIRED SECTION -->

### Task 1: [Specific Task Name]
**Pre-requisites**:
- [ ] [What must be verified before starting]
- [ ] [Required system state]

**Steps**:
1. [ ] [Specific action with expected outcome]
2. [ ] [Test interactively - specify how]
3. [ ] [Get user verification]

**Potential Issues**:
- [Known problem] → [Solution approach]

### Task 2: [If time permits]
[Similar structure]

## 🔗 Additional References
<!-- DO NOT REMOVE - REQUIRED SECTION -->

### Framework Documentation
[list any code documentation relevant for the session]

### Relevant Code
- `[file:line]` - [What to look for]
- `[file:line]` - [Pattern to follow/avoid]

### Test Files
- `[test file]` - [How to run and what to verify]

## 💭 Context & Decisions
<!-- DO NOT REMOVE - REQUIRED SECTION -->

### Recent Technical Decisions
[Only include if affects this session]
- **[Decision]**: [Rationale] → [Impact]

### Architectural Considerations
- [Pattern to follow]
- [Anti-pattern to avoid]

## ⚡ Quick Reference
<!-- DO NOT REMOVE - REQUIRED SECTION -->
[helpful tools or command]


## 🏁 Session End Checklist
<!-- DO NOT REMOVE - REQUIRED SECTION -->

**Before ending session:**
[any workflow related tasks that are important to finish in the next session]

**Commit Reminders**:
- Only commit when user explicitly requests
- Include session summary in commit message

---

## 🚨 CRITICAL CONTEXT FOR LLM
<!-- DO NOT REMOVE THIS SECTION - REQUIRED -->

**Working Directory**: [Specify exact path where commands run]
**Command Syntax Notes**: [Any special syntax requirements]
**Common Pitfalls**: [Known issues to avoid]
**Test Results**: [If tests failed, include output]

[This section is CRITICAL for next session success]

---

## 🚨 DO NOT SKIP MANDATORY READS

The mandatory documents contain critical information about:
- How the user wants to interact
- Project coding standards
- Workflow rules that prevent problems
- Architectural decisions and patterns

Skipping these leads to:
- Repeated mistakes
- Wasted sessions
- User frustration
- 7+ session debugging marathons (like ScrollArea)

**Time invested in reading: 15-20 minutes**
**Time saved by reading: Multiple sessions**

---
