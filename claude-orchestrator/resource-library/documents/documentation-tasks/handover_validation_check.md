---
project: claude-orchestrate
title: Handover Validation Check Task
version: 2025-08-10 17:45
document type: Task
summary:
  - Validates handover document structure and completeness
  - Ensures all required sections are present
  - Checks for template placeholders
  - Verifies format compliance
tags: [task, validation, handover, quality-check, documentation]
---

# Handover Validation Check Task

## 🚀 Task Start Instructions

### For LLM Execution
**Read in this order:**
1. This entire task document
2. `/docs/status/handover-next.md` - The handover to validate
3. `/claude-orchestrator/resource-library/documents/handovers/Session_Handover_Template.md` - The template to check against

## 📋 Task Definition

### Purpose
Validate that the session handover document follows the template structure, contains all required sections, and has no template placeholders remaining. This ensures session continuity and prevents information loss.

### Scope
Check handover document for:
1. Correct filename and location
2. All required sections present
3. No template placeholders
4. Proper formatting
5. Non-empty section content

### Exclusions
**This task does NOT validate:**
- Content accuracy (main agent's responsibility)
- TODO completeness (requires session context)
- Technical correctness
- Decision documentation completeness

## 🔍 Verification Checklist

### 1. File Location and Naming
- [ ] File exists at `/docs/status/handover-next.md`
- [ ] Filename is exactly `handover-next.md` (not date-based)
- [ ] Previous handover archived to `/docs/status/archive/`
- [ ] Archive includes timestamp in filename

### 2. Document Structure
- [ ] Has YAML frontmatter with required fields
- [ ] Title includes actual date and time (format: YYYY-MM-DD HH:MM)
- [ ] Summary has 4 bullet points
- [ ] Tags include relevant keywords

### 3. Required Sections Presence
Verify ALL these sections exist:
- [ ] `## 🔴 MANDATORY READS (EVERY SESSION)`
- [ ] `## Orchestrator Understanding`
- [ ] `## 📍 Current Development State`
- [ ] `## 🎯 This Session Goal` or `## 🎯 Next Session Goal`
- [ ] `## ⚠️ Critical Warnings & Known Issues`
- [ ] `## 📋 Session Task Breakdown`
- [ ] `## 🔗 Additional References`
- [ ] `## 💭 Context & Decisions`
- [ ] `## ⚡ Quick Reference`
- [ ] `## 🏁 Session End Checklist`
- [ ] `## 🚨 CRITICAL CONTEXT FOR LLM`
- [ ] `## 🚨 DO NOT SKIP MANDATORY READS`

### 4. Template Placeholder Check
Search for and flag any remaining placeholders:
- [ ] No `[project name]` - should be actual project name
- [ ] No `[YYYY-MM-DD]` - should be actual date
- [ ] No `[timestamp]` - should be actual time
- [ ] No `[Brief Session Focus]` - should be actual focus
- [ ] No `[Document Path]` - should be actual paths
- [ ] No `[Specific reason]` - should be actual reasons
- [ ] No `[Description]` - should be actual descriptions
- [ ] No `[TODO]` or `[...]` as placeholders

### 5. Section Content Validation
Verify sections are not empty:
- [ ] Mandatory Reads has at least `/docs/read-first.md` reference
- [ ] Mandatory Reads includes "must be read in full!"
- [ ] Orchestrator Understanding has checklist items
- [ ] Development State has Phase and Sub-Phase
- [ ] Session Goal has objective and success criteria
- [ ] Task Breakdown has at least one task
- [ ] Quick Reference has actual commands
- [ ] Critical Context has working directory specified

### 6. Critical Elements Check
- [ ] Working directory path is specified in Critical Context
- [ ] Previous handover is referenced with correct path
- [ ] At least one "**Why Required**" explanation in reading list
- [ ] Time boxing mentioned if applicable
- [ ] Commit reminders included if uncommitted changes exist

## 🔎 How to Check

### Step 1: Read Handover Document
```bash
# Check file exists
ls -la /docs/status/handover-next.md

# Read the handover
cat /docs/status/handover-next.md
```

### Step 2: Check Structure
```python
# Pseudo-code for section checking
required_sections = [
    "MANDATORY READS",
    "Orchestrator Understanding",
    "Current Development State",
    "Session Goal",
    "Critical Warnings",
    "Session Task Breakdown",
    "Additional References",
    "Context & Decisions",
    "Quick Reference",
    "Session End Checklist",
    "CRITICAL CONTEXT FOR LLM",
    "DO NOT SKIP MANDATORY READS"
]

for section in required_sections:
    if section not in handover_content:
        record_missing_section(section)
```

### Step 3: Search for Placeholders
```bash
# Search for common placeholders
grep -n "\[.*\]" /docs/status/handover-next.md | grep -E "\[(project name|YYYY|timestamp|TODO|Description)\]"
```

### Step 4: Validate Content Depth
- Check each section has meaningful content (not just heading)
- Verify examples are specific, not generic
- Ensure paths are real project paths

## 📊 Output Format

Create findings report at:
`/docs/status/session-reports/session-findings-handover-validation-[YYYY-MM-DD-HHMM].md`

Use this structure:

```markdown
---
project: claude-orchestrate
title: Handover Validation Check Findings
version: [YYYY-MM-DD HH:MM]
document type: Status
summary:
  - Validation result: PASSED/FAILED
  - Sections checked: 12
  - Issues found: [number]
tags: [findings, handover, validation, quality-check]
---

# Handover Validation Check Findings

## Task Summary
Validated handover document structure and completeness for `/docs/status/handover-next.md`

## Overall Result: [PASSED/FAILED]

[If PASSED]: ✅ Handover is properly structured and ready for next session

[If FAILED]: ❌ Handover has issues that must be fixed before session end

---

## Validation Results

### ✅ Passed Checks ([number]/[total])
- File location and naming correct
- All required sections present
- No template placeholders found
- [Other passed items]

### ❌ Failed Checks ([number]/[total])

#### Missing Sections
**Problem**: [Number] required sections are missing
**Sections**:
1. `[Section name]` - Critical for [reason]
2. `[Section name]` - Critical for [reason]

**Fix Required**: Add missing sections before saving

#### Template Placeholders Found
**Problem**: [Number] placeholders not replaced
**Locations**:
- Line [X]: "[placeholder text]"
- Line [Y]: "[placeholder text]"

**Fix Required**: Replace with actual content

#### Empty Sections
**Problem**: [Number] sections have no content
**Sections**:
- `[Section name]` - Only has heading
- `[Section name]` - Missing required content

**Fix Required**: Add meaningful content to sections

---

## Recommendations

### Immediate Actions Required
1. [Specific fix needed]
2. [Specific fix needed]

### Validation Must Pass Before
- Saving handover
- Ending session
- Archiving previous handover

---

## Checklist for Fixes
- [ ] Add missing sections: [list]
- [ ] Replace placeholders: [list]
- [ ] Add content to: [list]
- [ ] Re-run validation after fixes
```

## 🎯 Success Criteria

Handover validation passes when:
1. All 12 required sections are present
2. No template placeholders remain
3. Each section has meaningful content
4. Filename and location are correct
5. Critical context section is comprehensive

## 📝 Common Failures

### Most Often Missing Sections
1. **Orchestrator Understanding** - Often skipped entirely
2. **CRITICAL CONTEXT FOR LLM** - Frequently forgotten
3. **Session End Checklist** - Commonly omitted

### Most Common Placeholders Left
1. `[YYYY-MM-DD]` in timestamps
2. `[project name]` in various places
3. `[Document Path]` in reading lists
4. `[TODO]` markers

### Most Common Content Issues
1. Empty Quick Reference section
2. Missing working directory in Critical Context
3. No "Why Required" explanations
4. Generic task descriptions

## 🧹 Cleanup After Task Completion

### If Validation Passed
- Report success to orchestrating agent
- Proceed with handover save

### If Validation Failed
- Report issues to orchestrating agent
- Block handover save until fixed
- Re-run validation after fixes

### Report Handling
- Keep validation report for audit trail
- Archive with session reports

---
*Run before every handover save to ensure quality*