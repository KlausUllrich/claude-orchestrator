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

# Session Handover - [Brief Session Focus]

## 🔴 MANDATORY READS (EVERY SESSION)

**Read these documents in order - NO EXCEPTIONS:**

### 1. Core Project Rules 
- [ ] `/docs/status/read-first.md` - must be read in full!

### 2. Current Task Context
- [ ] This entire handover document
- [ ] Previous session handover summary: `[link to previous]`

### 3. Task-Specific Required Reading
[List ONLY documents essential for THIS session's specific task]
- [ ] `[Document Path]` - **Why Required**: [Specific reason]
- [ ] `[Document Path]` - **Why Required**: [Specific reason]

**💡 Better to spend tokens on proper onboarding than waste sessions debugging**

---

## Orchestrator Understanding
**Check Understanding:**
Before starting, confirm you understand:
- [ ] How commands flow: User → Claude → Commands → orchestrate.py → Python scripts
- [ ] Where documents are stored 
- [ ] Where databases live: `claude-orchestrator/short-term-memory/`
- [ ] What works vs what's TODO


## 📍 Current Development State

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

### Primary Objective
[One clear, specific goal that can be completed in this session]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] User verification obtained

### Time Boxing
- If primary objective not achieved in [X] attempts → STOP and investigate architecture

## ⚠️ Critical Warnings & Known Issues

### Architecture Warnings
[Based on lessons learned, bug patterns or long-term memory]

### Active Blockers
1. **[Blocker]**: [Description] → [Workaround if any]
2. **[Blocker]**: [Description] → [Impact on session]

## 📋 Session Task Breakdown

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

### Framework Documentation
[list any code documentation relevant for the session]

### Relevant Code
- `[file:line]` - [What to look for]
- `[file:line]` - [Pattern to follow/avoid]

### Test Files
- `[test file]` - [How to run and what to verify]

## 💭 Context & Decisions

### Recent Technical Decisions
[Only include if affects this session]
- **[Decision]**: [Rationale] → [Impact]

### Architectural Considerations
- [Pattern to follow]
- [Anti-pattern to avoid]

## ⚡ Quick Reference
[helpful tools or command]


## 🏁 Session End Checklist

**Before ending session:**
[any workflow related tasks that are important to finish in the next session]

**Commit Reminders**:
- Only commit when user explicitly requests
- Include session summary in commit message

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
