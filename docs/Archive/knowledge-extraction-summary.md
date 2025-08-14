---
project: claude-orchestrate  
type: technical
title: "Essential Knowledge Extraction Summary"
version: 2025-08-14
status: CURRENT
summary:
  - Key information from files being considered for removal
  - Recommendations for where to preserve essential content
tags: [consolidation, knowledge-extraction, streamlining]
---

# Essential Knowledge Extraction Summary

## Files Reviewed for Removal/Consolidation

### 1. QUICK-REFERENCE.md - **Core Concepts to Preserve**

#### Essential Information:
- **System Flow**: `User command → Claude executes Python → Updates files/DB → Shows result`
- **Key Principle**: NO separate terminal, NO background process, NO monitoring daemon
- **Directory Structure**: Clear mapping of where different components live

#### Recommended Action:
**MERGE** essential concepts into `docs/technical/architecture.md`:
- Add system flow diagram
- Include directory purpose table
- Preserve the "how it works" simple explanation

### 2. claude-orchestrator/brain/rules/rules-readme.md - **Rule System Core**

#### Essential Information:
- **Single Source of Truth**: All rules in YAML format
- **Architecture**: Rules are read by code, not hardcoded
- **File Structure**: `priority`, `description`, `rules` structure
- **Key Principle**: Never duplicate rules in code

#### Recommended Action:
**MOVE** to `docs/conventions.md` under "Rule System Standards" section:
- Add YAML structure documentation
- Include the core principle about single source of truth
- Reference the brain/rules/ folder location

### 3. docs/technical/known-limitations.md - **Critical Limitations**

#### Essential Information:
- **Context Guardian limitation**: Cannot track tokens in Claude Code automatically
- **Workarounds**: Manual checkpoints, task-based checkpoints
- **Working alternatives**: What Context Guardian CAN do
- **Future solutions**: Potential improvements

#### Recommended Action:
**SUMMARIZE** key limitations in `docs/technical/architecture.md`:
- Create "Current Limitations" section
- Focus on the most critical ones affecting daily use
- Keep solutions/workarounds
- Link to full file in archive if detailed analysis needed

## Extraction Plan

### Step 1: Update architecture.md
Add sections for:
- **System Flow** (from QUICK-REFERENCE.md)
- **Directory Structure** (enhanced table from QUICK-REFERENCE.md)
- **Current Limitations** (summary from known-limitations.md)

### Step 2: Update conventions.md  
Add section for:
- **Rule System Standards** (from rules-readme.md)
- **YAML Structure Requirements**
- **Single Source of Truth Principle**

### Step 3: Archive Original Files
Move to `docs/Archive/` with clear naming:
- `quick-reference-archived.md`
- `rules-readme-archived.md` 
- `known-limitations-archived.md`

### Step 4: Update read-first.md
Remove references to archived files, confirm new structure covers essential knowledge.

## Benefits of Consolidation

1. **Faster Session Startup**: Fewer mandatory documents
2. **Reduced Duplication**: Information in logical locations
3. **Better Maintenance**: Fewer files to keep updated
4. **Clearer Navigation**: Essential info in predictable places

## Information Preserved

- ✅ System flow understanding
- ✅ Directory structure clarity  
- ✅ Rule system architecture
- ✅ Critical limitations awareness
- ✅ Workaround strategies

---
*This extraction ensures no essential knowledge is lost during streamlining.*