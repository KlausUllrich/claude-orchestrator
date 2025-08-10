---
project: [project name]
title: Content Consistency Check Task
version: 2025-01-11 02:30
document type: Task
summary:
  - Autonomous task to verify content consistency
  - Checks for contradictions and outdated information
  - Validates synchronization between documents
  - Ensures consistent project information
tags: [task, verification, consistency, documentation, autonomous]
---

# Content Consistency Check Task

## 🚀 Task Start Instructions

### For LLM Execution
**Read in this order:**
1. This entire task document
2. [documentation-index.md](./docs/documentation-index.md) - Main documentation index
3. [architecture.md](./docs/technical/architecture.md) - Folder Strukture
4. [handover-next.md](./docs/status/handover-next.md) - Session handover for this session for context

## 📋 Task Definition

### Purpose
Verify that information is consistent across all documentation, identifying contradictions, outdated information, and synchronization issues between related documents.

### Scope
Check all documentation for consistency in:
1. Project names and terminology
2. Version numbers and dependencies
3. Workflow descriptions
4. Technical specifications
5. File paths and structure references
6. Code examples and snippets

### Exclusions
**Ignore all files in:**
- `/Archive/` directories
- `/old/` directories
- `/claude-orchestrator/` directories (code files)
- Temporary or backup files

## 🔍 Verification Checklist

### 1. Project Identity Consistency
- [ ] Verify the project name is used consistently everywhere
- [ ] Check project description consistency across README, docs, and templates
- [ ] Verify the project concept (design, vision, goal) is described consistently
- [ ] Check version numbers match across all documents
- [ ] Ensure no references to old project names (e.g., "Test_Code")

### 2. Technical Specifications
- [ ] the technical specifications areconsistent across all mentions
- [ ] tool and engine version specifications match
- [ ] System requirements consistent
- [ ] Dependencies listed consistently

### 3. Code Examples and Commands
- [ ] Build commands consistent across documentation
- [ ] File path examples use correct project structure
- [ ] Code snippets follow same conventions
- [ ] Tool usage examples are current
- [ ] Command syntax matches actual usage

### 4. Status and Progress Consistency
- [ ] Feature status consistent across design and technical docs
- [ ] TODO items synchronized across documents
- [ ] Completion percentages align roughly with reality (find obvious discrepancies)

## 🔎 How to Check

### Step 1: Gather Key Information
```bash
# Find all documentation files
find /docs -name "*.md" | grep -v "/old/" | grep -v "/archive/"
find /workflow -name "*.md" | grep -v "/old/" | grep -v "/a rchive/"
```

### Step 2: Check for Common Inconsistencies
```bash
# Check for old project name
rg "Test_Love_Code" --type md

# Check LÖVE2D version consistency
rg "love.*11\.[0-9]" --type md

# Check for version numbers
rg "version.*[0-9]+\.[0-9]+" --type md
```

### Step 3: Cross-Reference Analysis
For each major topic (project name, versions, paths, etc.):
1. Identify all documents mentioning the topic
2. Extract the specific information
3. Compare for consistency
4. Note any variations

### Step 4: Categorize Issues
Group findings by:
- Critical inconsistencies (project name, versions)
- Major inconsistencies (workflows, structures)
- Minor inconsistencies (descriptions, examples)
- Outdated information
- Missing synchronization

## 📊 Output Format

Create findings report at:
`/Docs/Status/Session_Findings_Content_Consistency_Check.md`

Use this exact structure:

```markdown
---
project: AncientDefenders
type: content consistency verification findings
title: Content Consistency Check Findings
version: [current date/time]
document type: Status
summary:
  - [Number of documents checked]
  - [Number of inconsistencies found]
  - [Most critical issue type]
tags: [findings, consistency, verification]
---

# Content Consistency Check Findings

## Task Summary
[Brief description of what was checked]

## Overall Findings Summary
[High-level summary: X documents checked, Y inconsistencies found]

## Overall Recommendation
[Primary recommendation based on findings]

---

## Topic 1: Project Name Inconsistencies

### Problem Summary
[X instances of incorrect project names found]

### Files Affected
1. `[Full path to file 1]` - Line [X]: "[quote]"
2. `[Full path to file 2]` - Line [Y]: "[quote]"

### Suggested Solution
Update all instances to use "AncientDefenders"

### Priority
**CRITICAL** - Affects project identity

### User Feedback Options
- [ ] Fix all immediately
- [ ] Review each instance first
- [ ] Other: _________________________

---

## Topic 2: Version Number Conflicts

### Problem Summary
[Different versions of LÖVE2D/Lua/Crystal mentioned]

### Files Affected
[List files with conflicting versions]

### Suggested Solution
Standardize on official versions from DevelopmentBootstrap.md

### Priority
**HIGH** - Affects development environment

### User Feedback Options
- [ ] Update all to latest versions
- [ ] Keep current versions
- [ ] Other: _________________________

---

[Continue for other topics: Workflow Inconsistencies, Path Conflicts, Outdated Examples, etc.]
```

## 🎯 Success Criteria

Content is considered consistent if:
1. Project name is "AncientDefenders" everywhere
2. Version numbers match across all documents
3. Workflow descriptions align with EssentialWorkflowRules.md
4. File paths and structures are accurate
5. No contradictory information exists
6. Cross-references are valid and accurate

## 📝 Expected Finding Categories

1. **Project Identity**: Wrong project names or descriptions
2. **Version Conflicts**: Different version numbers cited
3. **Workflow Mismatches**: Inconsistent process descriptions
4. **Path Errors**: Incorrect file or folder references
5. **Outdated Examples**: Code that doesn't match current structure
6. **Missing Sync**: Information updated in one place but not others
7. **Terminology Drift**: Same concept with different names
8. **Command Variations**: Different syntax for same operations

## 🔧 Common Inconsistency Patterns

1. **Outdated Examples**: Code that no longer matches current structure
2. **Version Drift**: Different documents citing different versions
3. **Path Changes**: Documentation not updated after restructuring
4. **Feature Evolution**: Design docs not matching implemented features
5. **Terminology Shift**: Same concept with different names
6. **Copy-Paste Errors**: Information copied but not fully updated
7. **Partial Updates**: Some occurrences updated, others missed

## 🧹 Cleanup After Task Completion

### Temporary Files Created
During execution, this task may create:
- Any grep/rg output files
- Temporary analysis results
- Comparison reports

### Cleanup Actions
After all fixes have been implemented:

1. **Findings Report Handling**:
   - [ ] Review the findings report at `/Docs/Status/Session_Findings_Content_Consistency_Check.md`
   - [ ] If all issues resolved, move to `Docs/Status/old/`
   - [ ] If some issues remain, update report with current status
   - [ ] Mark resolved inconsistencies with completion date

2. **Temporary Files**:
   - [ ] Delete any temporary analysis files
   - [ ] Remove grep/rg output files
   - [ ] Clear comparison reports

3. **Documentation Updates**:
   - [ ] Update affected documents with consistency fixes
   - [ ] Synchronize version numbers across all docs
   - [ ] Update DocumentationIndex.md if needed

4. **Future Monitoring**:
   - [ ] Schedule next consistency check (recommended: bi-weekly)
   - [ ] Create watch list for frequently inconsistent items
   - [ ] Set up automated consistency checks where possible

### Retention Policy
- **Findings Reports**: Keep for 2 months, then archive
- **Fixed Issues**: Log in documentation history
- **Patterns**: Track common inconsistency types
- **Metrics**: Monitor consistency improvement over time


### Git Workflow After Fixes
Since check tasks are performed in Git worktrees, follow these steps if tasked to make commits.

1. **Verify your location**:
   ```bash
   pwd  # Should show: .../worktrees/[CheckName]
   git status  # Confirm branch and changes
   ```

2. **Commit your changes**:
   ```bash
   git add -A
   git commit -m "Fix [check type] violations found during audit

   - [Brief summary of main fixes]
   - [Number of files affected]
   
   See Session_Findings_[CheckName].md for details"
   ```

3. **Push to remote**:
   ```bash
   git push -u origin [branch-name]
   ```

4. **Merge to main** (if authorized):
   ```bash
   # Direct push from worktree to main
   git push origin HEAD:main
   ```

### Important Notes
- **Always use relative paths** when in worktrees (e.g., `src/` not `/mnt/.../src/`)
- If you accidentally edit files in the main repo, see WorktreeGuidelines.md for recovery
- Keep findings report (`Session_Findings_*.md`) for audit trail
---
*Run this task periodically to ensure documentation consistency*