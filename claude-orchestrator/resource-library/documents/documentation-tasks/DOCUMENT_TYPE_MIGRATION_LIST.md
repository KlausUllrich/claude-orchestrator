---
project: AncientDefenders
type: migration checklist
title: Document Type Migration Checklist
version: 2025-01-11 18:00
document type: Task
summary:
  - List of documents needing type migration
  - From old 3-type system to new 7-type system
  - Organized by current type and location
  - Tracks migration progress
tags: [migration, document-types, checklist, task]
---

# Document Type Migration Checklist

## Overview
This checklist tracks the migration from the old 3-type system (Design, KnowledgeBase, Status) to the new 7-type system (Design, Technical, Status, Workflow, Template, Task, Guide).

## Migration Status

### ✅ Already Migrated
- [x] `/Workflow/Documentation_Tasks/Workflow_Check.md` - KnowledgeBase → Task
- [x] `/Workflow/Documentation_Tasks/YAML_Headers_Check.md` - KnowledgeBase → Task
- [x] `/Workflow/DevelopmentBootstrap.md` - KnowledgeBase → Workflow
- [x] `/Workflow/WorkflowOverview.md` - KnowledgeBase → Workflow

### 🔄 Documents Needing Migration

#### Current: KnowledgeBase → Technical
- [ ] `/Docs/KnowledgeBase/Architecture.md` → Technical
- [ ] `/Docs/KnowledgeBase/TechStack.md` → Technical
- [ ] `/Docs/Technical/ProjectReference.md` → Already Technical (verify)
- [ ] `/Docs/Technical/CodeStructure.md` → Already Technical (verify)
- [ ] `/Docs/Technical/Components/InitialStructure.md` → Technical

#### Current: KnowledgeBase → Workflow
- [ ] `/Docs/KnowledgeBase/ContextOptimization.md` → Workflow
- [ ] `/Docs/KnowledgeBase/DocumentationIndex.md` → Workflow
- [ ] `/Workflow/Rules/EssentialWorkflowRules.md` → Workflow
- [ ] `/Workflow/Rules/DocumentationTiers.md` → Workflow
- [ ] `/Workflow/WorkflowDecisionTree.md` → Workflow
- [ ] `/Workflow/ClaudeCrystalWorkflow.md` → Workflow

#### Current: Design → Design (No Change)
- [ ] `/Docs/Design/GameDesign.md` → Design (verify)
- [ ] `/Docs/Design/UIScreenDesign.md` → Design (verify)

#### Current: Status → Status (No Change)
- [ ] `/Docs/Status/ProjectProgress.md` → Status (verify)
- [ ] `/Docs/Status/CurrentImplementation.md` → Status (verify)
- [ ] All Session_Handover_*.md files → Status (verify)

#### Current: No Type → Guide
- [ ] `/Docs/Features/LocalizationSystem.md` → Guide
- [ ] `/Docs/PixelFontGuide.md` → Guide

#### Current: No Type → Technical
- [ ] `/Docs/Technical/APIReference.md` → Technical
- [ ] `/Docs/Technical/CoreSystems.md` → Technical
- [ ] `/Docs/Technical/TechnicalDecisions.md` → Technical
- [ ] `/Docs/Technical/Roadmap.md` → Technical
- [ ] `/Docs/Technical/ComponentDependencies.md` → Technical
- [ ] `/Docs/Technical/DataStructures.md` → Technical

#### Current: No Type → Design
- [ ] `/Docs/Requirements/Phase1_CoreFramework.md` → Design
- [ ] `/Docs/Requirements/Phase2_CombatDeepDive.md` → Design
- [ ] `/Docs/Requirements/Phase3_ProgressionSystems.md` → Design

## Migration Process

1. **Run YAML Headers Check** first to identify all files with missing/incorrect types
2. **Update each file's YAML header** with appropriate new document type
3. **Verify location** matches expected folder for that type
4. **Move files** if needed to match type/location consistency
5. **Run checks again** to verify migration success

## Type/Location Mapping Reference

| Document Type | Expected Location |
|--------------|-------------------|
| Design       | /Docs/Design/, /Docs/Requirements/ |
| Technical    | /Docs/Technical/, /Docs/KnowledgeBase/ (legacy) |
| Status       | /Docs/Status/ |
| Workflow     | /Workflow/, /Docs/KnowledgeBase/ (process docs) |
| Template     | /Workflow/Templates/ |
| Task         | /Workflow/Documentation_Tasks/ |
| Guide        | /Docs/Features/, /Docs/ |

## Notes

- Some KnowledgeBase documents will become Technical (architecture, APIs)
- Some KnowledgeBase documents will become Workflow (process docs)
- Requirements documents are Design type (they define what to build)
- Keep legacy KnowledgeBase support in doc_generator.cr during transition

---
*Check off items as they are migrated*