---
project: [project name]
title: Unreferenced Documents Check Task
version: 2025-08-10 15:50
summary:
  - Autonomous task to find orphaned documents
  - Identifies unreferenced documentation files
  - Validates document reference integrity
  - Ensures all docs are properly linked
tags: [task, verification, orphaned, documentation, autonomous]
---

# Unreferenced Documents Check Task

## 🚀 Task Start Instructions

### For LLM Execution
**Read in this order:**
1. This entire task document
2. [documentation-index.md](./docs/documentation-index.md) - Main documentation index
3. [architecture.md](./docs/technical/architecture.md) - Folder Strukture

## 📋 Task Definition

### Purpose
Identify documents that are not referenced anywhere in the project, indicating they may be orphaned, outdated, or forgotten. This helps maintain a clean and navigable documentation structure.

### Scope
Check all documentation files to ensure they are:
1. Referenced in at least one other document
2. Listed in appropriate index files
3. Linked from relevant documents
4. Fit to the documentation structure

### Exclusions
**Ignore all files in:**
- `/archive/` directories
- `/old/` directories  
- `/src/` directories (code files)
- Root level files (README.md, CLAUDE.md, LICENSE, etc.)
- `/claude-orchestrator/` directories (code files)
- `Handover*` files (highly volatile, use-once documents)

## 🔍 Verification Checklist

### 1. Build Reference Map
- [ ] Scan all markdown files for references to other documents
- [ ] Create map of which documents reference which
- [ ] Include both direct links and mentions
- [ ] Track reference types (link, mention, include)

### 2. Index Coverage Check
- [ ] Verify all docs appear in documentation-index.md
- [ ] Check category-specific index files if they exist
- [ ] Ensure proper categorization in indexes
- [ ] Validate index descriptions match documents

### 3. Identify Unreferenced Documents
- [ ] Find documents with zero incoming references
- [ ] Exclude expected standalone files (README, LICENSE)
- [ ] Check if orphaned or legitimately standalone
- [ ] Verify they're not referenced in code

### 4. Cross-Reference Validation
- [ ] Session handovers reference summaries
- [ ] Templates reference their usage docs
- [ ] Task documents linked from workflow docs
- [ ] Design docs linked from implementation

### 5. Special Document Checks
- [ ] YAML header `references:` fields are bidirectional
- [ ] Template documents have usage examples
- [ ] Status documents linked from current handover
- [ ] Old handovers properly archived

### 6. Navigation Path Analysis
- [ ] Can reach all docs from documentation-index.md
- [ ] No dead-end documents (docs that don't link anywhere)
- [ ] Proper breadcrumb trails in document sets
- [ ] Clear navigation hierarchy

## 🔎 How to Check

### Step 1: Find All Documentation Files
```bash
# Find all markdown files in documentation directories
find /docs -name "*.md" | grep -v "/old/" | grep -v "/Archive/" > docs_list.txt
```

### Step 2: Build Reference Map
```bash
# Find all markdown references
for file in $(cat docs_list.txt); do
  echo "=== References in $file ==="
  # Find markdown links
  grep -o '\[.*\](.*.md)' "$file" | grep -o '(.*.md)' | tr -d '()'
  # Find direct mentions
  grep -o '[A-Za-z_-]*.md' "$file"
done
```

### Step 3: Identify Unreferenced Files
For each document:
1. Check if it appears in any other document
2. Check if it's in documentation-index.md
3. Check if it's in any YAML `references:` fields
4. Note its purpose and whether being unreferenced is expected

### Step 4: Categorize Findings
Group unreferenced documents by:
- Truly orphaned (should be evaluated by main agent or user for deletion/archivation)
- Missing from indexes (should be added)
- Legitimate standalone (document why)
- Old/outdated (should be archived)

## 📊 Output Format

Create findings report at:
`/docs/status/session_reports/session-findings-unreferenced-documents-check_[YYYY-MM-DD_hh:mm].md`

Use this exact structure:

```markdown
---
project: [project name]
title: Unreferenced Documents Check Findings
version: [YYYY-MM-DD hh:mm]
document type: Status
summary:
  - [Number of documents analyzed]
  - [Number of unreferenced documents found]
  - [Number requiring action]
tags: [findings, orphaned, documentation, verification]
---

# Unreferenced Documents Check Findings

## Task Summary
[Brief description of what was checked]

## Overall Findings Summary
[High-level summary: X documents analyzed, Y unreferenced found]

## Overall Recommendation
[Primary recommendation based on findings]

---

## Topic 1: Completely Orphaned Documents

### Problem Summary
[X documents have no references from any other document]

### Files Affected
1. `[Full path to file 1]` - [Brief description]
2. `[Full path to file 2]` - [Brief description]

### Suggested Solution
Archive or delete truly orphaned documents

### Priority
**HIGH** - Clutters documentation structure

### User Feedback Options
- [ ] My suggestion: [the suggestion of the executing agent]
- [ ] Archive all to /old/
- [ ] Delete permanently
- [ ] Review each individually
- [ ] Other

---

## Topic 2: Missing from Documentation Index

### Problem Summary
[X documents exist but aren't in documentation-index.md]

### Files Affected
[List files with their categories]

### Suggested Solution
Add to appropriate sections in DocumentationIndex.md

### Priority
**MEDIUM** - Affects discoverability

### User Feedback Options
- [ ] My suggestion: [suggestion from the executing agent]
- [ ] Add all to index
- [ ] Add selectively
- [ ] Other

---

## Topic 3: One-Way References

### Problem Summary
[X documents reference others but aren't referenced back]

### Files Affected
[List files and their reference patterns]

### Suggested Solution
Evaluate if bidirectional references needed

### Priority
**LOW** - May be intentional

### User Feedback Options
- [ ] Add return references
- [ ] Leave as-is
- [ ] Other

---

[Continue for other topics: Old Handovers, Outdated Docs, etc.]
```

## 🎯 Success Criteria

Documentation structure is healthy if:
1. All active documents are referenced somewhere
2. DocumentationIndex.md is comprehensive
3. No truly orphaned documents exist
4. Navigation paths are clear and complete
5. Old documents are properly archived

## 📝 Expected Finding Categories

1. **Orphaned Documents**: No references anywhere
2. **Missing from Index**: Not in DocumentationIndex.md
3. **Old Handovers**: Previous session handovers not archived
4. **Broken References**: Documents reference non-existent files
5. **One-Way References**: A→B but no B→A
6. **Dead Ends**: Documents that don't link anywhere
7. **Misplaced Documents**: In wrong directory for their type
8. **Duplicate Content**: Similar documents that should be merged

## 🔧 Reference Patterns to Check

1. **Markdown Links**: `[text](path/to/file.md)`
2. **Reference Lists**: In YAML headers
3. **See Also Sections**: At document end
4. **Inline Mentions**: "See DocumentName.md"
5. **Index Entries**: In DocumentationIndex.md
6. **Template Usage**: Documents using templates
7. **Task References**: Workflow documents mentioning tasks

## 🧹 Cleanup After Task Completion

### Temporary Files Created
During execution, this task may create:
- `/docs/status/session-reports/docs_list.txt` - List of all documentation files
- Reference mapping files
- Analysis output files

### Cleanup Actions
After all fixes have been implemented:

1. **Findings Report Handling**:
   - [ ] Review the findings report at `/docs/status/session-reports/session-findings-unreferenced-documents-check.md`
   - [ ] If all orphans handled, move report to `/docs/status/archive/`
   - [ ] Update report if some documents intentionally standalone
   - [ ] Document rationale for keeping unreferenced files

2. **Temporary Files**:
   - [ ] Delete `docs_list.txt`
   - [ ] Remove reference mapping files
   - [ ] Clear any analysis outputs

3. **Documentation Updates**:
   - [ ] Update documentation-index.md with missing entries
   - [ ] Add cross-references where appropriate
   - [ ] Archive truly orphaned documents to `/archive/`


### Retention Policy
- **Orphaned Docs**: Archive with explanation note in document
- **Reference Maps**: Regenerate each check, don't retain
- **Metrics**: Track orphan rate trends

---
*Run this task periodically to maintain documentation hygiene*
