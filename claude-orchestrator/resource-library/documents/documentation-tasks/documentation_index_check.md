---
project: [project name]
title: Documentation Index Check Task
version: [YYYY-MM-DD hh:mm]
document type: Task
summary:
  - Autonomous task to verify documentation index
  - Ensures all docs are properly indexed
  - Validates categorization and paths
  - Checks index completeness and accuracy
tags: [task, verification, index, documentation, autonomous]
---

# Documentation Index Check Task

## 🚀 Task Start Instructions

### For LLM Execution
**Read in this order:**
1. This entire task document
2. [CLAUDE.md](../../CLAUDE.md) - User interaction preferences
3. [EssentialWorkflowRules.md](../Rules/EssentialWorkflowRules.md) - Core workflow rules
4. [DocumentationIndex.md](../../docs/documentation-index.md) - The index to verify

## 📋 Task Definition

### Purpose
Verify that documentation index accurately reflects all documentation in the project, serving as a reliable navigation hub with correct categorization, paths, and descriptions.

### Scope
Check the documentation index for:
1. Completeness (all docs listed)
2. Accuracy (correct paths and categories)
3. Quality (meaningful descriptions)
4. Structure (proper formatting)
5. Currency (up-to-date entries)

### Exclusions
**Skip indexing files in:**
- `/archive/` directories
- `/old/` directories
- `/src/` directories (code files)
- `.git/` directories

## 🔍 Verification Checklist

### 1. Index Completeness
- [ ] Every .md file in indexed directories appears in documentation-index.md
- [ ] No entries in index point to non-existent files
- [ ] Special documents (README.md, CLAUDE.md) listed
- [ ] No duplicate entries

### 2. Categorization Accuracy
- [ ] Documents listed under correct type section:
- [ ] **Getting Started** → read-first.md
- [ ] **Design** → Vision, UX, Game Design
- [ ] **Technical** → Architecture, Implementation
- [ ] **Status** → Progress, Session Handovers
- [ ] **Workflow** → Rules, Processes
- [ ] **Templates** → Document templates
- [ ] **Transient** → agent-feedback
- [ ] **Tool** → claude-orchestrator
- [ ] **Project Core Files** → not related to claude-orchestrator, but to the project

  - **Task** → Verification tasks
  - **Guide** → How-to guides
- [ ] YAML header `document type` matches index categorization
- [ ] No documents in wrong categories

### 3. Path Validation
- [ ] All file paths are relative from project root
- [ ] Links use proper markdown syntax: `[Name](path)`
- [ ] Paths use forward slashes consistently
- [ ] No broken links or incorrect paths
- [ ] Paths properly escaped if containing spaces

### 4. Description Quality
- [ ] Each entry has meaningful description
- [ ] Descriptions accurately reflect content
- [ ] No placeholder text ("TODO", "TBD")
- [ ] Descriptions concise (one line, <80 chars)
- [ ] Consistent description style

### 5. Structure and Format
- [ ] Index follows established format
- [ ] Sections ordered logically
- [ ] Consistent bullet/numbering style
- [ ] Proper markdown hierarchy (##, ###)
- [ ] Clean visual presentation

### 6. Special Sections
- [ ] "Quick Start" or "Key Entry Points" current
- [ ] Latest Session_Handover linked
- [ ] Essential documents highlighted
- [ ] Recently updated section if present
- [ ] Archived documents noted separately

## 🔎 How to Check

### Step 1: Gather All Documentation Files
```bash
# Find all markdown files in documentation directories
find Docs -name "*.md" -type f | grep -v "/old/" | grep -v "/Archive/" | sort > all_docs.txt
find Workflow -name "*.md" -type f | grep -v "/old/" | grep -v "/Archive/" | sort >> all_docs.txt

# Count total documents
total_docs=$(wc -l < all_docs.txt)
echo "Total documentation files: $total_docs"
```

### Step 2: Extract Indexed Files
```bash
# Extract all file paths from DocumentationIndex.md
grep -oE '\]\([^)]+\.md\)' Docs/KnowledgeBase/DocumentationIndex.md | sed 's/](\(.*\))/\1/' | sort > indexed_docs.txt

# Count indexed documents
indexed_docs=$(wc -l < indexed_docs.txt)
echo "Indexed documentation files: $indexed_docs"
```

### Step 3: Find Discrepancies
```bash
# Find documents not in index
echo "=== Missing from Index ==="
comm -23 all_docs.txt indexed_docs.txt

# Find broken links in index
echo "=== Broken Links in Index ==="
while read -r path; do
  if [ ! -f "$path" ]; then
    echo "Broken link: $path"
  fi
done < indexed_docs.txt
```

### Step 4: Verify Categorization
For each indexed document:
1. Read its YAML header `document type`
2. Check which section it's listed under
3. Verify they match
4. Note any mismatches

### Step 5: Assess Description Quality
Review each entry for:
- Accuracy of description
- Clarity and usefulness
- Consistency of style
- Appropriate length

## 📊 Output Format

Create findings report at:
`/Docs/Status/Session_Findings_Documentation_Index_Check.md`

Use this exact structure:

```markdown
---
project: AncientDefenders
title: Documentation Index Check Findings
version: [current date/time]
document type: Status
summary:
  - [bullet point 1]
  - [bullet point 2]
  - [bullet point 3]
tags: [findings, index, documentation, verification]
---

# Documentation Index Check Findings

## Task Summary
[Brief description of what was checked]

## Overall Findings Summary
[X documents found, Y indexed, Z issues identified]

## Overall Recommendation
[Primary recommendation based on findings]

---

## Topic 1: Missing Documents

### Problem Summary
[X documents not listed in DocumentationIndex.md]

### Documents Missing
1. `/Docs/Technical/NewComponent.md` - Component documentation
2. `/Workflow/Rules/RecentRule.md` - New workflow rule
[Continue list...]

### Suggested Solution
Add all missing documents to appropriate sections

### Priority
**HIGH** - Affects documentation discoverability

### User Feedback Options
- [ ] Add all missing documents
- [ ] Review each before adding
- [ ] Generate new index automatically
- [ ] Other: _________________________

---

## Topic 2: Broken Links

### Problem Summary
[X entries point to non-existent files]

### Broken Links Found
1. `[Old Design](Docs/Design/OldDesign.md)` - File moved/deleted
2. `[Legacy Guide](Docs/LegacyGuide.md)` - No longer exists
[Continue list...]

### Suggested Solution
Remove or update broken link entries

### Priority
**HIGH** - Creates poor user experience

### User Feedback Options
- [ ] Remove all broken links
- [ ] Find and update moved files
- [ ] Other: _________________________

---

## Topic 3: Miscategorized Documents

### Problem Summary
[X documents listed under wrong document type]

### Mismatches Found
1. `SessionHandover.md` - Listed under "Workflow", should be "Status"
2. `CodingGuide.md` - Listed under "Technical", should be "Guide"
[Continue list...]

### Suggested Solution
Move documents to correct category sections

### Priority
**MEDIUM** - Affects logical organization

### User Feedback Options
- [ ] [Agent recommendation]
- [ ] [user feedback with comments]

---

[Continue for Poor Descriptions, Format Issues, etc.]
```

## 🎯 Success Criteria

Documentation index is healthy if:
1. 100% of active documents are indexed
2. Zero broken links
3. All documents correctly categorized
4. Descriptions clear and accurate
5. Format consistent throughout
6. Easy to navigate and find documents

## 📝 Expected Finding Categories

1. **Missing Documents**: Files not in index
2. **Broken Links**: Entries pointing nowhere
3. **Wrong Categories**: Type mismatches
4. **Poor Descriptions**: Unclear, outdated, missing
5. **Format Issues**: Inconsistent structure
6. **Duplicate Entries**: Same doc listed twice
7. **Stale Entries**: Archived docs still listed
8. **Path Errors**: Incorrect relative paths

## 🔧 Index Maintenance Best Practices

1. **Add Immediately**: Index new docs upon creation
2. **Update Paths**: When moving files, update index
3. **Review Regularly**: Monthly full index audit
4. **Automate When Possible**: Use doc_generator.cr
5. **Preserve Structure**: Maintain consistent format
6. **Version Control**: Track all index changes

## 🧹 Cleanup After Task Completion

### Temporary Files Created
During execution, this task may create:
- `all_docs.txt` - List of all documentation files
- `indexed_docs.txt` - List of indexed files
- Comparison output files

### Cleanup Actions
After all fixes have been implemented:

1. **Findings Report Handling**:
   - [ ] Review findings at `/Docs/Status/Session_Findings_Documentation_Index_Check.md`
   - [ ] If all issues resolved, move to `/Docs/Status/old/`
   - [ ] Update DocumentationIndex.md with corrections
   - [ ] Commit with clear message about updates

2. **Temporary Files**:
   - [ ] Delete `all_docs.txt` and `indexed_docs.txt`
   - [ ] Remove comparison outputs
   - [ ] Clear any analysis files

3. **Documentation Updates**:
   - [ ] Update DocumentationIndex.md completely
   - [ ] Run doc_generator.cr if available
   - [ ] Update "last generated" timestamp

4. **Future Monitoring**:
   - [ ] Schedule monthly index reviews
   - [ ] Set up automated index generation
   - [ ] Create index update checklist

### Retention Policy
- **Findings Reports**: Keep for 3 months
- **Index Backups**: Keep last 3 versions
- **Generation Logs**: Keep for 1 month
- **Update History**: Maintain in git

---
*Run this task monthly to maintain navigation integrity*