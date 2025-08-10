---
project: AncientDefenders
type: documentation verification task
title: Document Structure Check Task
version: 2025-01-11 02:50
document type: Task
summary:
  - Autonomous task to verify document structure
  - Checks YAML headers and formatting standards
  - Validates section organization and hierarchy
  - Ensures document type requirements met
tags: [task, verification, structure, documentation, autonomous]
---

# Document Structure Check Task

## 🚀 Task Start Instructions

### For LLM Execution
**Read in this order:**
1. This entire task document
2. [CLAUDE.md](../../CLAUDE.md) - User interaction preferences
3. [EssentialWorkflowRules.md](../Rules/EssentialWorkflowRules.md) - Core workflow rules
4. [DocumentationTiers.md](../Rules/DocumentationTiers.md) - Document structure standards

## 📋 Task Definition

### Purpose
Verify that all documents follow established structural conventions, ensuring consistency, readability, and proper organization across the entire documentation set.

### Scope
Check all documentation for:
1. YAML header compliance
2. Section hierarchy and organization
3. Formatting standards
4. Document type-specific requirements
5. Content quality standards

### Exclusions
**Skip checking files in:**
- `/Archive/` directories
- `/old/` directories
- `/Klaus/` directories
- Generated documentation
- Third-party files

## 🔍 Verification Checklist

### 1. YAML Header Validation
- [ ] Every document starts with `---`
- [ ] Contains all required fields:
  - `project: AncientDefenders`
  - `type:` (describes document purpose)
  - `title:` (human-readable title)
  - `version:` (YYYY-MM-DD HH:MM format)
  - `document type:` (one of 7 valid types)
  - `summary:` (3-5 bullet points, each <20 words)
  - `tags:` (relevant, lowercase, hyphenated)
- [ ] Ends with `---`
- [ ] No blank lines within header
- [ ] Valid YAML syntax

### 2. Document Title Structure
- [ ] Single H1 (`#`) after YAML header
- [ ] Title matches or relates to filename
- [ ] Clear, descriptive title
- [ ] No duplicate H1 headers

### 3. Section Hierarchy
- [ ] Proper heading progression (H1→H2→H3)
- [ ] No skipped levels
- [ ] Maximum depth H4 (`####`)
- [ ] Meaningful section names
- [ ] Consistent heading style

### 4. Content Formatting Standards
- [ ] Lists use consistent markers (`-` for unordered)
- [ ] Code blocks specify language (` ```lua `)
- [ ] Internal links use relative paths
- [ ] External links include descriptions
- [ ] Images have alt text
- [ ] Tables have headers

### 5. Document Type Requirements

#### Design Documents
- [ ] Overview/Vision section present
- [ ] Requirements/Specifications included
- [ ] Visual aids where appropriate
- [ ] User-focused language

#### Technical Documents
- [ ] Architecture/Implementation details
- [ ] Code examples are functional
- [ ] API documentation formatted
- [ ] Technical accuracy

#### Status Documents
- [ ] Current status clearly stated
- [ ] Last updated timestamp
- [ ] Progress indicators (%, checkboxes)
- [ ] Next steps defined

#### Workflow Documents
- [ ] Process/Steps clearly defined
- [ ] Action items marked
- [ ] Examples provided
- [ ] Prerequisites listed

#### Template Documents
- [ ] Placeholder markers present
- [ ] Usage instructions included
- [ ] Example usage shown
- [ ] Clear structure

#### Task Documents
- [ ] Task start instructions
- [ ] Objective clearly stated
- [ ] Verification checklist
- [ ] Output format defined
- [ ] Cleanup section

#### Guide Documents
- [ ] Prerequisites section
- [ ] Step-by-step instructions
- [ ] Troubleshooting section
- [ ] Examples included

### 6. Quality Standards
- [ ] No empty sections
- [ ] No placeholder text (Lorem ipsum)
- [ ] Appropriate section lengths
- [ ] Clear and concise writing
- [ ] Proper grammar and spelling

## 🔎 How to Check

### Step 1: Find All Documentation
```bash
# Find all markdown files
find Docs Workflow -name "*.md" -type f | grep -v "/old/" | grep -v "/Archive/" > docs_to_check.txt

# Count documents to check
total=$(wc -l < docs_to_check.txt)
echo "Checking $total documents"
```

### Step 2: Validate YAML Headers
```bash
# Check for missing YAML headers
while read -r file; do
  if ! head -1 "$file" | grep -q "^---$"; then
    echo "Missing YAML header: $file"
  fi
done < docs_to_check.txt

# Validate YAML syntax
while read -r file; do
  # Extract YAML header and validate
  sed -n '/^---$/,/^---$/p' "$file" | tail -n +2 | head -n -1 > temp_yaml.yml
  # Check for required fields
  for field in "project:" "type:" "title:" "version:" "document type:" "summary:" "tags:"; do
    if ! grep -q "^$field" temp_yaml.yml; then
      echo "$file missing field: $field"
    fi
  done
done < docs_to_check.txt
```

### Step 3: Check Structure
```bash
# Validate heading hierarchy
while read -r file; do
  awk '
    /^#+ / {
      level = gsub(/#/, "#")
      if (prev && level > prev + 1) {
        print FILENAME ":line " NR " - Skipped heading level"
      }
      prev = level
    }
  ' "$file"
done < docs_to_check.txt
```

### Step 4: Check Formatting
```bash
# Find code blocks without language
rg '```\s*$' --type md

# Find inconsistent list markers
rg '^\s*[\*\+] ' --type md

# Check for trailing whitespace
rg '\s+$' --type md
```

### Step 5: Validate Document Type Requirements
For each document:
1. Read YAML header `document type`
2. Check for required sections based on type
3. Verify type-specific formatting
4. Note any missing elements

## 📊 Output Format

Create findings report at:
`/Docs/Status/Session_Findings_Document_Structure_Check.md`

Use this exact structure:

```markdown
---
project: AncientDefenders
type: document structure verification findings
title: Document Structure Check Findings
version: [current date/time]
document type: Status
summary:
  - [Number of documents checked]
  - [Number with structure issues]
  - [Most common issue type]
tags: [findings, structure, documentation, verification]
---

# Document Structure Check Findings

## Task Summary
[Brief description of what was checked]

## Overall Findings Summary
[X documents checked, Y issues found across Z categories]

## Overall Recommendation
[Primary recommendation based on findings]

---

## Topic 1: Missing or Invalid YAML Headers

### Problem Summary
[X documents have missing or invalid YAML headers]

### Documents Affected
1. `/Docs/OldDesign.md` - No YAML header
2. `/Workflow/Process.md` - Missing required fields: version, tags
3. `/Docs/Technical/API.md` - Invalid YAML syntax
[Continue list...]

### Suggested Solution
Add or fix YAML headers following standards

### Priority
**CRITICAL** - Required for all documents

### User Feedback Options
- [ ] Fix all headers automatically
- [ ] Review each fix individually
- [ ] Generate headers from content
- [ ] Other: _________________________

---

## Topic 2: Heading Hierarchy Issues

### Problem Summary
[X documents have improper heading structure]

### Issues Found
1. `/Docs/Guide.md:45` - H3 directly after H1 (skipped H2)
2. `/Workflow/Rules.md:23` - Multiple H1 headers
[Continue list...]

### Suggested Solution
Restructure headings to follow proper hierarchy

### Priority
**HIGH** - Affects document navigation

### User Feedback Options
- [ ] Fix heading structure
- [ ] Review document organization
- [ ] Other: _________________________

---

## Topic 3: Document Type Requirement Violations

### Problem Summary
[X documents missing required sections for their type]

### Missing Requirements
1. `Design/GameFlow.md` - Missing "Requirements" section
2. `Technical/Database.md` - No code examples
3. `Status/Weekly.md` - No progress indicators
[Continue list...]

### Suggested Solution
Add missing sections per document type

### Priority
**MEDIUM** - Affects document completeness

### User Feedback Options
- [ ] Add all missing sections
- [ ] Update document types
- [ ] Other: _________________________

---

[Continue for Formatting Issues, Quality Problems, etc.]
```

## 🎯 Success Criteria

Document structure is compliant if:
1. 100% have valid YAML headers
2. All follow heading hierarchy rules
3. Document type requirements met
4. Consistent formatting throughout
5. No structural linting errors
6. Clear and organized content

## 📝 Expected Finding Categories

1. **YAML Header Issues**: Missing, incomplete, invalid
2. **Heading Problems**: Skipped levels, multiple H1s
3. **Format Violations**: Inconsistent lists, code blocks
4. **Type Mismatches**: Wrong sections for document type
5. **Link Issues**: Broken, absolute instead of relative
6. **Quality Issues**: Empty sections, placeholder text
7. **Syntax Errors**: Invalid markdown, YAML
8. **Style Inconsistencies**: Mixed formatting approaches

## 🔧 Common Structure Patterns

### Good Structure Example
```markdown
---
project: AncientDefenders
type: game feature design
title: Tower Defense Mechanics
version: 2025-01-11 14:30
document type: Design
summary:
  - Core tower defense gameplay loop
  - Tower types and upgrade paths
  - Enemy wave patterns and balancing
tags: [design, gameplay, towers, enemies]
---

# Tower Defense Mechanics

## Overview
[Clear introduction]

## Requirements
### Functional Requirements
[Structured list]

### Technical Requirements
[Clear specifications]

## Implementation Details
[Well-organized sections]
```

## 🧹 Cleanup After Task Completion

### Temporary Files Created
During execution, this task may create:
- `docs_to_check.txt` - List of documents
- `temp_yaml.yml` - Temporary YAML extraction
- Structure analysis outputs

### Cleanup Actions
After all fixes have been implemented:

1. **Findings Report Handling**:
   - [ ] Review findings at `/Docs/Status/Session_Findings_Document_Structure_Check.md`
   - [ ] If all issues resolved, move to `/Docs/Status/old/`
   - [ ] Update affected documents
   - [ ] Verify fixes don't break content

2. **Temporary Files**:
   - [ ] Delete `docs_to_check.txt`
   - [ ] Remove `temp_yaml.yml`
   - [ ] Clear analysis outputs

3. **Documentation Updates**:
   - [ ] Fix all structural issues
   - [ ] Update document templates
   - [ ] Create structure guide if needed

4. **Future Monitoring**:
   - [ ] Set up pre-commit hooks
   - [ ] Schedule monthly structure audits
   - [ ] Create linting configuration

### Retention Policy
- **Findings Reports**: Keep for 3 months
- **Structure Templates**: Maintain permanently
- **Linting Rules**: Version control
- **Fix History**: Document in git

---
*Run this task bi-weekly to maintain documentation quality*