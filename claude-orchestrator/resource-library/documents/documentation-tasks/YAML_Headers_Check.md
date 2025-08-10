---
project: AncientDefenders
type: verification task
title: YAML Headers Integrity Check Task
version: 2025-01-11 17:00
document type: Task
summary:
  - Autonomous task to verify YAML header integrity
  - Checks for missing or incorrect headers
  - Validates references and summaries
  - Ensures consistent documentation metadata
tags: [task, verification, yaml, headers, documentation, autonomous]
---

# YAML Headers Integrity Check Task

## 🚀 Task Start Instructions

### For LLM Execution
**Read in this order:**
1. This entire task document
2. [CLAUDE.md](../../CLAUDE.md) - User interaction preferences
3. [EssentialWorkflowRules.md](../Rules/EssentialWorkflowRules.md) - Core workflow rules (for YAML format)

## 📋 Task Definition

### Purpose
Verify that all documentation files have proper YAML headers that follow project standards and contain accurate information.

### Scope
Check all markdown files in documentation folders for:
1. Presence of YAML headers
2. Correctness of header format and content
3. Validity of summaries
4. Existence of referenced files

### Exclusions
**Ignore all files in:**
- `/Archive/` directories
- `/old/` directories
- `/Klaus/` directories
- `/Source/` directories (code files)
- Root level files (README.md, BRANCH_WORKFLOW.md may not need headers)

## 🔍 Verification Checklist

### 1. Missing Headers Check
- [ ] Scan all .md files in /Docs/ and /Workflow/
- [ ] Identify files without YAML headers (no `---` at start)
- [ ] Exclude expected files (README.md at root)

### 2. Required Fields Check
For each file with headers, verify presence of:
- [ ] `project:` (must be "AncientDefenders")
- [ ] `type:` (describes document purpose)
- [ ] `title:` (human-readable title)
- [ ] `version:` (timestamp)
- [ ] `document type:` (Design/Technical/Status/Workflow/Template/Task/Guide)
- [ ] `summary:` (list of bullet points)
- [ ] `tags:` (list of relevant tags)

### 3. Field Content Validation
- [ ] **project**: Always "AncientDefenders" (not "Test_Love_Code")
- [ ] **version**: Format YYYY-MM-DD-## HH:MM
- [ ] **document type**: One of [Design, Technical, Status, Workflow, Template, Task, Guide]
- [ ] **summary**: 3-5 bullet points, each <20 words
- [ ] **tags**: Relevant, lowercase, hyphenated

### 4. References Check
- [ ] Extract all `references:` entries
- [ ] Verify each referenced file exists
- [ ] Check paths are correct (relative to project root)

### 5. Summary Relevance Check
- [ ] Read document content briefly
- [ ] Verify summary accurately reflects current content
- [ ] Flag summaries that seem outdated or incorrect

### 6. Document Type/Location Consistency
- [ ] Verify document type matches folder location:
  - **Design** → /Docs/Design/
  - **Technical** → /Docs/Technical/
  - **Status** → /Docs/Status/
  - **Workflow** → /Workflow/ (but not Templates or Tasks)
  - **Template** → /Workflow/Templates/
  - **Task** → /Workflow/Documentation_Tasks/
  - **Guide** → /Docs/Features/ or /Docs/
- [ ] Flag mismatched document types and locations

## 🔎 How to Check

### Step 1: Find Documentation Files
```bash
# Find all .md files in documentation folders
find /Docs -name "*.md" | grep -v "/old/" | grep -v "/Archive/" | grep -v "/Klaus/"
find /Workflow -name "*.md" | grep -v "/old/" | grep -v "/Archive/" | grep -v "/Klaus/"
```

### Step 2: Check Each File
For each markdown file:
1. Check if starts with `---\n`
2. Extract YAML header (content between first `---` and second `---`)
3. Parse YAML and validate fields
4. Check references exist
5. Compare summary to content

#### Step 3: Categorize Issues
Group findings by:
- Missing headers entirely
- Missing required fields
- Incorrect field values
- Type/location mismatches
- Broken references
- Outdated summaries

## 📊 Output Format

Create findings report at:
`/Docs/Status/Session_Findings_YAML_Headers_Check.md`

Use this exact structure:

```markdown
---
project: AncientDefenders
type: yaml headers verification findings
title: YAML Headers Integrity Check Findings
version: [current date/time]
document type: Status
summary:
  - [Number of files checked]
  - [Number of issues found]
  - [Most common issue type]
tags: [findings, yaml, headers, verification]
---

# YAML Headers Integrity Check Findings

## Task Summary
[Brief description of what was checked]

## Overall Findings Summary
[High-level summary: X files checked, Y issues found]

## Overall Recommendation
[Primary recommendation based on findings]

---

## Topic 1: Missing YAML Headers

### Problem Summary
[X files have no YAML headers at all]

### Files Affected
1. `[Full path to file 1]`
2. `[Full path to file 2]`

### Suggested Solution
Add YAML headers to all documentation files

### Priority
**[HIGH/MEDIUM/LOW]** - [Justification]

### User Feedback Options
- [ ] Add headers to all files
- [ ] Add headers to specific folders only
- [ ] Other: _________________________

---

## Topic 2: Incorrect Project Names

### Problem Summary
[X files still reference "Test_Love_Code" instead of "AncientDefenders"]

### Files Affected
[List files]

### Suggested Solution
Update project field to "AncientDefenders"

### Priority
**CRITICAL** - Affects project consistency

### User Feedback Options
- [ ] Fix all immediately
- [ ] Fix in batches
- [ ] Other: _________________________

---

[Continue for other topics: Missing Fields, Invalid Values, Type/Location Mismatch, Broken References, Outdated Summaries]
```

## 🎯 Success Criteria

Headers are considered valid if:
1. All documentation files have YAML headers
2. All required fields are present
3. Project name is consistently "AncientDefenders"
4. References point to existing files
5. Summaries accurately reflect content

## 📝 Expected Finding Categories

1. **Missing Headers**: Files with no YAML at all
2. **Incomplete Headers**: Missing required fields
3. **Wrong Project Name**: Still using "Test_Love_Code"
4. **Invalid Document Type**: Not one of the 7 valid types
5. **Type/Location Mismatch**: Document type doesn't match folder
6. **Broken References**: Point to non-existent files
7. **Outdated Summaries**: Don't match current content
8. **Format Issues**: Wrong version format, summary too long

---
*Run this task periodically to ensure documentation metadata integrity*